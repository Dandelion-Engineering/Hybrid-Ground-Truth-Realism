"""Read one probe's band units out of a processed IBL NWB file, over range requests.

``utils.band_drift`` defines the drift statistic that gates a Tier A host, and it
takes per-unit spike times and per-spike depths as plain arrays. This module is
what puts real arrays in front of it: it opens a processed NWB blob over HTTP
range requests and reads the ragged ``spike_times`` and
``spike_distances_from_probe_tip_um`` slices belonging to the units whose peak
electrode sits inside a pinned anatomical band -- and nothing else in the file.

**Targeted, because the alternative is the whole sorting.** The two ragged
columns hold every spike of every unit on every probe. A candidate's band holds
22 to 267 units out of many hundreds, so resolving each band unit's slice from
the column's own index and reading only that slice is the difference between a
few hundred megabytes and the entire sorting. The index arrays are one integer
per unit and are read in full, so every slice is known before any of them is
read and :func:`plan_transfer` can size the read before it happens.

**Several byte counts, because the read is paid for in more than one currency
and the parts of it are live at the same time.** The count this module first
reported was the stored payload of the slices, and a ceiling enforced on it
bounded neither what the read transfers nor what it holds. A range-request
reader fetches whole fixed-size blocks and *keeps* them -- its cache is
unbounded and lives until the read returns -- so a scattered slice can cost a
block or more of transfer for a few kilobytes of payload, and those blocks are
still resident when the arrays they fed are resident too. The arrays are
converted to float64 on the way in, so what is held is not what is stored
either. :func:`plan_transfer` therefore reports ``logical_bytes`` (the stored
payload, exact), ``cache_bound_bytes`` (an upper bound on the distinct block
bytes the read can fetch, including what has already been spent on metadata),
``resident_bytes`` (the converted arrays plus the largest slice at its stored
width) and ``structures_bytes`` (a measured bound on the Python containers the
read holds while it runs). ``peak_resident_bytes`` is the sum of the last
three, and it is the single quantity :func:`read_band_units` enforces its
ceiling against, because those three are live together rather than in turn.

**The block bound is derived from where the bytes actually are.** A contiguous
dataset whose file offset h5py will give is placed exactly. A chunked dataset is
placed from the file byte range of every chunk the slices touch, read from the
chunk index, because HDF5 does not promise that successive chunks occupy one
contiguous span -- an earlier version assumed they did, and on a file whose
chunks are interleaved with other data it under-bounded the transfer by a
quarter. Where neither route is available the bound is the whole file, which is
loose but is the only thing still true. ``bound_basis`` names which routes a
given plan used.

**Every read this module performs happens before that bound is computed, except
the per-unit slices the bound is about.** The electrode table, the unit scalars,
the column descriptions, the conversion provenance, the two column layouts and
the chunk index are all read while the reader's spend is still being counted, so
each of them lands inside ``spent_bytes`` and therefore inside the bound. The
provenance read used to sit *after* the ceiling was enforced, where it was
invisible to the plan and could transfer megabytes a caller had been told would
not be transferred; the rule the repair leaves behind is the general one, and it
is what the harness now checks on every fixture that performs a read.

**What it validates, and why validation lives here rather than in the caller.**
Four properties have to hold before a drift number computed from these arrays
means anything, and every one of them is a property of the file rather than of
the statistic:

1. the two ragged columns are partitioned identically, by offsets that are
   stored as integers, so that a unit's times and its depths are the same
   spikes in the same order;
2. the loaded values are finite, each unit's times ascend, and the depth column
   still carries its documented micrometre unit;
3. each unit's ``max_electrode`` -- also an integer as stored -- names exactly
   one electrode on that unit's own probe, and that electrode's ``rel_y`` is
   finite;
4. the processed file's electrode table agrees with the raw file's, because the
   band is derived from the raw table while ``max_electrode`` indexes the
   processed one.

**The structural columns are checked as stored, before anything converts them.**
``int()`` accepts a float and truncates it, so two ragged indices differing by
less than one, or an electrode reference that is not a whole number, would have
been read as a well-formed partition and as a valid row. Integrality and dtype
are therefore confirmed on the stored values, and every one-value-per-unit
column is required to hold one value per unit, before a single row is resolved.

**The two ragged indices are held to a stricter rule than the electrode
reference, because the schema is stricter about them.** ``spike_times_index``
and its depth counterpart are HDMF ``VectorIndex`` datasets, and the common
schema specifies unsigned-integer storage for them, so a floating-point index is
a malformed file rather than a permissible encoding -- integral values do not
make it well formed. Those two are required to be stored in an integer dtype.
``max_electrode`` is a custom IBL column that the schema does not type, so a
float column whose values are exactly whole is accepted there and its stored
dtype is reported. The asymmetry is deliberate and is the difference between
enforcing a specification and inventing one.

A violation of any of these raises :class:`ValueError`. That is deliberate and it
matters for the host order: a candidate whose *inputs* are malformed has not
failed the drift gate, and recording it as a drift failure would hand the host
to the next rank for a reason that has nothing to do with drift.

Nothing here computes, thresholds, or interprets a drift value. This module
reads and checks; ``utils.band_drift`` measures.
"""

import sys

import numpy as np

import h5py

from utils.remote_hdf5 import RemoteFile

UNITS_PATH = "units"
ELECTRODES_PATH = "general/extracellular_ephys/electrodes"
TIME_COLUMN = "spike_times"
DEPTH_COLUMN = "spike_distances_from_probe_tip_um"

# The depth column's own first-party description is the only statement in the
# file about what unit its values carry. Requiring this substring keeps the
# check first-party without turning a punctuation difference into a rejection;
# the whole description is reported verbatim beside the verdict.
DEPTH_UNIT_PHRASE = "micrometers"

# Read verbatim and reported, never gated on: the converter provenance that
# fixes the session-time origin is a claim about the conversion repository at a
# pinned commit, not something an asset can be made to prove about itself.
PROVENANCE_PATHS = (
    "general/source_script",
    "general/session_start_time",
    "general/institution",
    "general/lab",
)

# The per-value cap on conversion provenance, pinned here rather than passed in,
# because a value read from a candidate must not be able to choose the number
# that decides whether reading it was allowed. It is deliberately far above any
# plausible real value: IBL's source_script is a conversion script, and the
# largest of the four paths on a real asset is kilobytes.
PROVENANCE_MAX_BYTES = 65536


def _decode(values):
    """Decode an h5py string column into a list of str.

    Args:
        values: an h5py dataset slice holding bytes or str.

    Returns:
        A list of Python strings.
    """
    return [v.decode() if isinstance(v, bytes) else str(v) for v in values]


def read_flat_electrodes(handle):
    """Read one NWB file's electrode table as flat, globally indexed columns.

    ``max_electrode`` is a row index into this table, so the table has to be
    read flat. ``utils.host_anatomy.read_electrode_table`` groups the same rows
    by probe, which is the right shape for finding a band and the wrong shape
    for resolving a row index.

    Args:
        handle: an open :class:`h5py.File`.

    Returns:
        A dict with ``rel_y`` (list of float), ``group_name`` and ``location``
        (lists of str), all of length ``n_rows``, plus ``n_rows``.

    Raises:
        KeyError: if the file carries no electrode table, which is a malformed
            asset rather than an absent measurement.
    """
    if ELECTRODES_PATH not in handle:
        raise KeyError("file has no %s" % ELECTRODES_PATH)
    table = handle[ELECTRODES_PATH]
    rel_y = [float(v) for v in table["rel_y"][:]]
    return {
        "rel_y": rel_y,
        "group_name": _decode(table["group_name"][:]),
        "location": _decode(table["location"][:]),
        "n_rows": len(rel_y),
    }


def column_descriptions(handle, columns=(TIME_COLUMN, DEPTH_COLUMN)):
    """Read the units table's own description attribute for named columns.

    Args:
        handle: an open :class:`h5py.File`.
        columns: column names to describe.

    Returns:
        A dict from column name to its stored description, or to None where the
        column carries no description attribute.
    """
    node = handle[UNITS_PATH]
    out = {}
    for name in columns:
        if name not in node:
            out[name] = None
            continue
        value = node[name].attrs.get("description")
        if isinstance(value, bytes):
            value = value.decode()
        out[name] = str(value) if value is not None else None
    return out


def _stored_value_bytes(node):
    """Return a dataset's stored payload size in bytes, or None if HDF5 will not say.

    Args:
        node: whatever :meth:`h5py.File.__getitem__` returned for the path.

    Returns:
        The stored size in bytes, or None when there is no honest pre-read
        answer. A variable-length string is the case that matters: its
        characters live in HDF5's global heap and the dataset itself stores only
        the heap references, so on h5py 3.16.0 a 4,200,030-character value
        reports 16 bytes of storage and 8 bytes of ``nbytes``. Returning either
        as a size would be a fiction, and a fictional bound is worse than an
        absent one.
    """
    if not isinstance(node, h5py.Dataset):
        return None
    info = h5py.check_string_dtype(node.dtype)
    if info is not None and info.length is None:
        return None
    try:
        return int(node.id.get_storage_size())
    except (AttributeError, ValueError, RuntimeError):
        return None


def _capped(text, max_bytes):
    """Return ``text`` if it is within the cap, or a truncated, self-describing form.

    Args:
        text: the decoded value.
        max_bytes: the cap, applied here to characters. A UTF-8 character is at
            least one byte, so this never retains fewer bytes than the cap
            names, and at most four times it. The exact retained size is
            measured rather than assumed: the returned dict is charged into
            ``structures_bytes`` by :func:`plan_transfer`.

    Returns:
        The text, or its first ``max_bytes`` characters followed by a marker
        naming the full length, so a reader can tell a short value from a
        truncated one.
    """
    if len(text) <= max_bytes:
        return text
    return ("%s<truncated: %d characters read, %d-character provenance cap>"
            % (text[:max_bytes], len(text), max_bytes))


def source_provenance(handle, max_bytes=PROVENANCE_MAX_BYTES):
    """Read whatever conversion provenance the asset carries, without gating on it.

    Args:
        handle: an open :class:`h5py.File`.
        max_bytes: the pinned per-value cap. A value whose stored size the file
            will report, above the cap, is not read at all. A value whose size
            the file will not report is read and then retained only up to the
            cap. Either way what this function returns is bounded, and it says
            in the value itself which of the two happened.

    Returns:
        A dict from path to its stored value as a string, omitting paths the
        file does not carry and replacing an oversized value with a marker
        naming its size and the cap. Values are recorded for the report; no
        value here is required to hold, because the session-time convention this
        project relies on is pinned to a conversion-repository commit rather
        than asserted by the asset.

    Note:
        **This reads the file, so it belongs in preflight, and that is a repair
        rather than a preference.** An earlier version was called after
        :func:`read_band_units` had already enforced its memory ceiling, which
        made every byte it transferred invisible to the plan: a schema-valid
        file carrying a 4,200,030-character ``general/source_script`` was
        admitted under a 174,368-byte transfer bound and a 267,001-byte peak,
        and then transferred and retained 4,232,336 bytes. It is now called
        before the reader's spend is captured, so its cost is inside
        ``spent_bytes`` and therefore inside ``cache_bound_bytes`` and
        ``peak_resident_bytes``. The cap is the second half of the repair: for a
        variable-length string there is no pre-read size to refuse on, so the
        bound that can still be enforced is on what is retained.
    """
    out = {}
    for path in PROVENANCE_PATHS:
        if path not in handle:
            continue
        node = handle[path]
        stored = _stored_value_bytes(node)
        if stored is not None and stored > max_bytes:
            out[path] = ("<not read: %d stored bytes exceeds the %d-byte provenance cap>"
                         % (stored, max_bytes))
            continue
        try:
            value = node[()]
        except (TypeError, ValueError):
            continue
        if isinstance(value, bytes):
            value = value.decode()
        out[path] = _capped(str(value), max_bytes)
        for key in ("file_name", "software", "version"):
            attr = node.attrs.get(key)
            if attr is None:
                continue
            if isinstance(attr, bytes):
                attr = attr.decode()
            out["%s@%s" % (path, key)] = _capped(str(attr), max_bytes)
    return out


def read_integer_column(node, name, require_integer_dtype=False):
    """Read a units-table column that must be integral as it is stored.

    A ragged partition offset and an electrode row reference are both indices
    into something else, so a value that is not a whole number is not a small
    inaccuracy -- it is a structural claim the file cannot support. ``int()``
    would accept it and truncate: two offsets 0.75 apart become one partition,
    and a fractional electrode becomes a real row. The check therefore runs on
    the stored values, before any conversion.

    ``require_integer_dtype`` is the stricter rule the ragged indices are held
    to. They are HDMF ``VectorIndex`` datasets and the common schema specifies
    unsigned-integer storage, so a floating-point index is a malformed file and
    exact whole values do not repair it. The custom ``max_electrode`` column
    carries no such specification, so it is read with the flag off: whole-valued
    floats are accepted there and the stored dtype is reported.

    Args:
        node: the open units-table group.
        name: the column name.
        require_integer_dtype: reject a non-integer storage dtype outright,
            for columns whose schema requires integer storage.

    Returns:
        The column as a list of Python ints.

    Raises:
        ValueError: if the column is not stored in an integer dtype and either
            ``require_integer_dtype`` is set or its values are not all finite
            whole numbers.
    """
    values = node[name][:]
    if np.issubdtype(values.dtype, np.integer):
        return [int(v) for v in values]
    if require_integer_dtype:
        raise ValueError(
            "units column %r is stored as %s, but it is an HDMF VectorIndex and the "
            "common schema specifies integer storage for it; a floating-point ragged "
            "index is a malformed file rather than an encoding choice, and values that "
            "happen to be whole do not make it well formed" % (name, values.dtype))
    if not np.issubdtype(values.dtype, np.floating):
        raise ValueError(
            "units column %r has dtype %s, which is neither integer nor float; it is "
            "used as an index and must be whole numbers" % (name, values.dtype))
    if not np.all(np.isfinite(values)):
        raise ValueError(
            "units column %r holds %d non-finite values and is used as an index"
            % (name, int((~np.isfinite(values)).sum())))
    fractional = values != np.floor(values)
    if np.any(fractional):
        first = int(np.argmax(fractional))
        raise ValueError(
            "units column %r is stored as %s and its value at row %d is %r, which is not a "
            "whole number; it indexes another table and truncating it would invent a "
            "structure the file does not state" % (name, values.dtype, first, values[first]))
    return [int(v) for v in values]


def read_unit_scalars(handle):
    """Read the one-value-per-unit columns the band selection needs.

    Args:
        handle: an open :class:`h5py.File`.

    Returns:
        A dict with ``probe_name`` and ``label`` (lists of str),
        ``max_electrode`` (list of int), ``times_index`` and ``depths_index``
        (lists of int, the ragged columns' own end-offset indices),
        ``n_units``, ``n_times`` / ``n_depths``, the two ragged columns' total
        lengths, and ``integer_dtypes``, each structural column's stored dtype
        as a string, so the report can say what was checked rather than that a
        check was made.

    Raises:
        KeyError: if the units table or either ragged column is absent.
        ValueError: if either ragged index is not stored in an integer dtype, if
            a structural column is not integral as stored, or if any
            one-value-per-unit column does not hold exactly one value per unit.
            A short column would otherwise silently shorten the unit set.
    """
    if UNITS_PATH not in handle:
        raise KeyError("file has no /%s" % UNITS_PATH)
    node = handle[UNITS_PATH]
    for name in (TIME_COLUMN, DEPTH_COLUMN,
                 TIME_COLUMN + "_index", DEPTH_COLUMN + "_index", "probe_name",
                 "max_electrode"):
        if name not in node:
            raise KeyError("units table has no %s" % name)
    probe_name = _decode(node["probe_name"][:])
    n_units = len(probe_name)
    scalars = {
        "probe_name": probe_name,
        "label": (_decode(node["kilosort2_label"][:])
                  if "kilosort2_label" in node else [""] * n_units),
        "max_electrode": read_integer_column(node, "max_electrode"),
        "times_index": read_integer_column(node, TIME_COLUMN + "_index",
                                           require_integer_dtype=True),
        "depths_index": read_integer_column(node, DEPTH_COLUMN + "_index",
                                            require_integer_dtype=True),
        "n_units": n_units,
        "n_times": int(node[TIME_COLUMN].shape[0]),
        "n_depths": int(node[DEPTH_COLUMN].shape[0]),
        "integer_dtypes": {name: str(node[name].dtype) for name in
                           ("max_electrode", TIME_COLUMN + "_index",
                            DEPTH_COLUMN + "_index")},
    }
    for name in ("label", "max_electrode", "times_index", "depths_index"):
        if len(scalars[name]) != n_units:
            raise ValueError(
                "the units table holds %d probe_name values but %d %s values; every "
                "one-value-per-unit column must have one value per unit"
                % (n_units, len(scalars[name]), name))
    return scalars


def check_ragged_alignment(scalars):
    """Confirm the two ragged columns partition their spikes identically.

    The drift statistic pairs each spike's time with that spike's depth, so the
    two columns must not merely have the same total length -- they must cut it
    into the same per-unit slices, in the same order. NWB stores each ragged
    column's end offsets in its own ``_index`` dataset, and nothing in the
    format requires two such columns to agree. This checks that they do.

    Args:
        scalars: the dict returned by :func:`read_unit_scalars`.

    Raises:
        ValueError: if either index is not non-decreasing, if either fails to
            end at its column's length, or if the two indices differ anywhere.
            Each is an input error rather than an unmeasurable candidate.
    """
    times_index = scalars["times_index"]
    depths_index = scalars["depths_index"]
    n_units = scalars["n_units"]
    for name, index, total in (("%s_index" % TIME_COLUMN, times_index, scalars["n_times"]),
                               ("%s_index" % DEPTH_COLUMN, depths_index, scalars["n_depths"])):
        if len(index) != n_units:
            raise ValueError(
                "%s has %d entries for %d units" % (name, len(index), n_units))
        if any(index[i] > index[i + 1] for i in range(len(index) - 1)):
            raise ValueError("%s is not non-decreasing" % name)
        if index and index[0] < 0:
            raise ValueError("%s starts at a negative offset %d" % (name, index[0]))
        if index and index[-1] != total:
            raise ValueError(
                "%s ends at %d but the column holds %d values" % (name, index[-1], total))
    if times_index != depths_index:
        first = next(i for i in range(n_units) if times_index[i] != depths_index[i])
        raise ValueError(
            "the %s and %s ragged indices first disagree at unit %d (%d vs %d); a unit's "
            "times and depths would not be the same spikes"
            % (TIME_COLUMN, DEPTH_COLUMN, first, times_index[first], depths_index[first]))


def resolve_unit_electrodes(scalars, electrodes, probe):
    """Map each unit on one probe to a finite ``rel_y`` on that same probe.

    Args:
        scalars: the dict returned by :func:`read_unit_scalars`.
        electrodes: the dict returned by :func:`read_flat_electrodes`, from the
            **same** file, so that ``max_electrode`` indexes the table the
            depths are taken from.
        probe: the probe name to restrict to, exactly as stored.

    Returns:
        A list of dicts, one per unit on ``probe``, each with ``row`` (units
        table row index), ``probe``, ``max_electrode``, ``rel_y_um`` and
        ``label``.

    Raises:
        ValueError: if a unit's ``max_electrode`` is out of range, belongs to a
            different probe, or resolves to a non-finite ``rel_y``. Band
            membership is decided by this mapping, so an ambiguous mapping is an
            input error and never permission to translate the band.
    """
    rows = []
    for row, unit_probe in enumerate(scalars["probe_name"]):
        if unit_probe != probe:
            continue
        electrode = scalars["max_electrode"][row]
        if not 0 <= electrode < electrodes["n_rows"]:
            raise ValueError(
                "unit %d on probe %r has max_electrode %d, outside an electrode table of "
                "%d rows" % (row, probe, electrode, electrodes["n_rows"]))
        owner = electrodes["group_name"][electrode]
        if owner != unit_probe:
            raise ValueError(
                "unit %d says probe %r but its max_electrode %d belongs to probe %r"
                % (row, unit_probe, electrode, owner))
        rel_y = electrodes["rel_y"][electrode]
        if not np.isfinite(rel_y):
            raise ValueError(
                "unit %d resolves to electrode %d whose rel_y is %r, not a finite depth"
                % (row, electrode, rel_y))
        rows.append({
            "row": row,
            "probe": unit_probe,
            "max_electrode": electrode,
            "rel_y_um": float(rel_y),
            "label": scalars["label"][row],
        })
    return rows


def select_band_units(unit_electrodes, depth_lo_um, depth_hi_um):
    """Keep the units whose peak electrode sits inside the pinned band.

    Args:
        unit_electrodes: the list returned by :func:`resolve_unit_electrodes`.
        depth_lo_um: the band's lower ``rel_y`` bound, inclusive.
        depth_hi_um: the band's upper ``rel_y`` bound, inclusive.

    Returns:
        The subset of ``unit_electrodes`` inside the band, in units-table row
        order. The selection reads no quality label: every unit whose peak
        electrode lands in the band contributes, which is the pre-declared
        label-blind rule.
    """
    return [unit for unit in unit_electrodes
            if depth_lo_um <= unit["rel_y_um"] <= depth_hi_um]


def chunk_byte_ranges(dataset, slices):
    """Locate in the file every chunk a set of element slices touches.

    An HDF5 chunk is stored contiguously, but successive chunks of one dataset
    are not: the library allocates each chunk where it can, so a file written
    incrementally, or alongside other growing datasets, interleaves them with
    unrelated data. Treating the first-to-last chunk span as one contiguous
    region therefore under-counts the blocks a fixed-block reader touches, by
    however much other data sits between them. The chunk index knows where each
    one is, so this asks it rather than assuming.

    Args:
        dataset: an open chunked :class:`h5py.Dataset`.
        slices: ``(lo, hi)`` element ranges, half-open.

    Returns:
        A dict from a chunk's first element to its ``(byte_offset, size)``, with
        None for a chunk the file has not allocated (an unwritten chunk costs no
        transfer). None if the dataset is not chunked or the chunk index will
        not answer, which the caller must treat as an unknown layout rather than
        as an empty one.
    """
    chunks = dataset.chunks
    if not chunks:
        return None
    chunk = int(chunks[0])
    wanted = set()
    for lo, hi in slices:
        if hi <= lo:
            continue
        for start in range((lo // chunk) * chunk, hi, chunk):
            wanted.add(start)
    ranges = {}
    for start in sorted(wanted):
        try:
            info = dataset.id.get_chunk_info_by_coord((start,))
        except (AttributeError, TypeError, ValueError, OSError, RuntimeError):
            return None
        if info is None or getattr(info, "byte_offset", None) is None:
            ranges[start] = None
            continue
        ranges[start] = (int(info.byte_offset), int(info.size))
    return ranges


def column_layout(dataset, slices=None):
    """Describe one stored column's layout, as the file itself reports it.

    Args:
        dataset: an open :class:`h5py.Dataset`.
        slices: the ``(lo, hi)`` element ranges the read will take. When given
            and the dataset is chunked, the chunk index is consulted so the
            plan can place every touched chunk exactly. Reading the index costs
            range requests, so the caller does this before it records what the
            read has already spent.

    Returns:
        A dict with ``itemsize``, ``offset`` (the dataset's byte offset in the
        file when it is stored contiguously, else None), ``chunk_elements``
        (the first chunk dimension when the dataset is chunked, else None),
        ``chunk_map`` (from :func:`chunk_byte_ranges`, else None),
        ``storage_bytes`` (what the file spends on it), ``library_cache_bytes``
        (the size HDF5's own raw-data chunk cache is allowed to reach for this
        dataset, which is memory the read occupies without ever appearing in a
        Python object) and ``compression``.
    """
    try:
        offset = dataset.id.get_offset()
    except (AttributeError, TypeError, ValueError):
        offset = None
    chunks = dataset.chunks
    try:
        storage_bytes = int(dataset.id.get_storage_size())
    except (AttributeError, TypeError, ValueError):
        storage_bytes = None
    library_cache_bytes = 0
    if chunks:
        try:
            library_cache_bytes = int(dataset.id.get_access_plist().get_chunk_cache()[1])
        except (AttributeError, TypeError, ValueError, OSError, RuntimeError):
            # Unreadable rather than absent: charge the library's documented
            # default rather than nothing, because nothing would be a claim.
            library_cache_bytes = 1024 * 1024
    return {
        "itemsize": int(dataset.dtype.itemsize),
        "offset": None if offset is None else int(offset),
        "chunk_elements": int(chunks[0]) if chunks else None,
        "chunk_map": (chunk_byte_ranges(dataset, slices)
                      if slices is not None and chunks else None),
        "storage_bytes": storage_bytes,
        "library_cache_bytes": library_cache_bytes,
        "compression": dataset.compression,
    }


def _blocks_covering(start, length, block_bytes):
    """Return the block indices a byte range occupies."""
    if length <= 0:
        return set()
    return set(range(start // block_bytes,
                     (start + length - 1) // block_bytes + 1))


def _slice_blocks(lo, hi, layout, block_bytes):
    """Name the distinct blocks one column slice can cost, and how it was placed.

    A block-caching reader fetches whole fixed-width blocks, so the cost of a
    slice is the blocks it lands in rather than its own length. Three regimes,
    in decreasing order of what the file will tell us:

    * **a chunked dataset whose chunk index answered** -- every chunk the slice
      touches is placed at its own file byte range, and the blocks covering
      those ranges are returned. A chunked read fetches whole chunks, so a
      partially used chunk still costs all of its blocks;
    * **contiguous storage with a known file offset** -- the slice's byte range
      is known directly;
    * **neither** -- nothing is known about where the bytes are, so no block set
      can be named and the caller must fall back to the whole file.

    Args:
        lo: first element of the slice.
        hi: one past the last element.
        layout: the dict from :func:`column_layout`.
        block_bytes: the reader's block size.

    Returns:
        A ``(blocks, basis)`` pair. ``blocks`` is a set of block indices, or
        None when the layout is unknown; ``basis`` names how it was derived.
    """
    if hi <= lo:
        return set(), None
    chunk_map = layout.get("chunk_map")
    chunk = layout["chunk_elements"]
    if chunk_map is not None and chunk:
        blocks = set()
        for start in range((lo // chunk) * chunk, hi, chunk):
            if start not in chunk_map:
                return None, "whole file"
            located = chunk_map[start]
            if located is None:
                continue
            blocks |= _blocks_covering(located[0], located[1], block_bytes)
        return blocks, "chunk offsets"
    if layout["offset"] is not None and not chunk:
        start = layout["offset"] + lo * layout["itemsize"]
        return (_blocks_covering(start, (hi - lo) * layout["itemsize"], block_bytes),
                "dataset offsets")
    return None, "whole file"


def python_structure_bytes(*objects):
    """Measure the live Python containers a read holds, conservatively.

    The block cache and the converted arrays are the two large terms in what
    this read occupies, but they are not the only ones: the unit scalars, the
    electrode table and the per-unit records are lists and dicts of Python
    objects that stay alive for the whole read. This walks them with
    :func:`sys.getsizeof` and counts a shared object once per reference, which
    over-counts rather than under-counts.

    Args:
        *objects: the containers to charge for.

    Returns:
        The total in bytes.
    """

    def walk(obj, depth):
        total = sys.getsizeof(obj)
        if depth >= 6:
            return total
        if isinstance(obj, dict):
            for key, value in obj.items():
                total += walk(key, depth + 1) + walk(value, depth + 1)
        elif isinstance(obj, (list, tuple, set, frozenset)):
            for item in obj:
                total += walk(item, depth + 1)
        return total

    return sum(walk(obj, 0) for obj in objects)


def band_slices(band_units, index):
    """Return each band unit's ``(lo, hi)`` element range in the ragged columns."""
    return [_slice_bounds(index, unit["row"]) for unit in band_units]


def plan_transfer(band_units, scalars, time_layout, depth_layout,
                  block_bytes, file_size, spent_bytes=0, held=()):
    """Size the band units' read before any of it is spent.

    The numbers answer different questions and the project's compute rule needs
    all of them: what the slices hold, what the network fetch can cost, and what
    has to fit in memory at once. Reporting one of them as ``bytes`` is what let
    a ceiling pass a read that then transferred more than the ceiling allowed;
    reporting the memory ones separately is what let a ceiling pass a read whose
    parts each fit but which together did not.

    Args:
        band_units: the list returned by :func:`select_band_units`.
        scalars: the dict returned by :func:`read_unit_scalars`.
        time_layout: :func:`column_layout` for the spike-time column.
        depth_layout: :func:`column_layout` for the spike-depth column.
        block_bytes: the reader's block size, which is what actually gets
            fetched.
        file_size: the asset's total size, which caps distinct block bytes.
        spent_bytes: bytes already transferred resolving the index and the
            metadata. Already spent, and part of what this read costs.
        held: any further live containers the caller holds for the duration of
            the read -- the electrode table and the per-unit records -- charged
            into ``structures_bytes``.

    Returns:
        A dict with ``n_units``, ``n_spikes``, ``per_unit`` (``(row, n_spikes)``
        pairs), ``logical_bytes`` (exact stored payload), ``cache_bound_bytes``
        (an upper bound on distinct block bytes, ``spent_bytes`` included),
        ``resident_bytes`` (the converted arrays plus the largest slice at its
        stored width), ``structures_bytes`` (the live Python containers),
        ``library_cache_bytes`` (what HDF5's own raw-data chunk cache is allowed
        to reach for the two columns), ``peak_resident_bytes`` (the sum of the
        previous four), ``bound_basis`` naming how the block bound was derived,
        plus ``block_bytes``, ``spent_bytes`` and the two layouts.

    Note:
        ``cache_bound_bytes`` bounds *distinct* blocks. A range request that
        fails and is retried re-transfers its block, and that is deliberately
        outside this bound: it is a network condition rather than a property of
        the read being planned.

        ``peak_resident_bytes`` adds the memory terms because they are live at
        the same moment, not one after another: the reader's block cache is
        unbounded and is not released until the read returns, so the last unit's
        arrays are resident while every block that fed the first unit is still
        resident too. Its declared scope is the block cache, the converted
        per-unit arrays with the largest stored-width slice, the Python
        containers this call is given, and the ceiling HDF5's own raw-data chunk
        cache is allowed to reach for the two columns. What it does **not**
        cover is named rather than left to be discovered: the interpreter's
        baseline, the allocator's fragmentation overhead, and any transient
        h5py allocation outside a chunk cache. It bounds this read's own
        footprint, not the process's.
    """
    index = scalars["times_index"]
    per_unit = []
    total_spikes = 0
    largest = 0
    slices = []
    for unit in band_units:
        lo, hi = _slice_bounds(index, unit["row"])
        per_unit.append((unit["row"], hi - lo))
        total_spikes += hi - lo
        largest = max(largest, hi - lo)
        slices.append((lo, hi))

    bounded_bytes = 0
    bases = []
    for layout in (time_layout, depth_layout):
        known_blocks = set()
        unknown = False
        for lo, hi in slices:
            blocks, basis = _slice_blocks(lo, hi, layout, block_bytes)
            if blocks is None:
                unknown = True
                break
            known_blocks |= blocks
            if basis is not None and basis not in bases:
                bases.append(basis)
        if unknown:
            # Nothing is known about where this column's bytes sit, so the only
            # remaining true statement is that the reader cannot fetch more
            # distinct bytes than the file holds.
            if "whole file" not in bases:
                bases.append("whole file")
            bounded_bytes += int(file_size)
            continue
        for block in known_blocks:
            bounded_bytes += min(block_bytes, max(0, file_size - block * block_bytes))
        # One block per column for the object-header and chunk-index metadata
        # h5py reads alongside the payload, which is not inside the payload's
        # own byte range and so is not in the block set above.
        bounded_bytes += block_bytes

    cache_bound = min(int(file_size), spent_bytes + bounded_bytes)
    resident = total_spikes * 16 + largest * (time_layout["itemsize"]
                                              + depth_layout["itemsize"])
    structures = python_structure_bytes(band_units, scalars, time_layout,
                                        depth_layout, *held)
    library_cache = (time_layout.get("library_cache_bytes", 0)
                     + depth_layout.get("library_cache_bytes", 0))
    return {
        "n_units": len(band_units),
        "n_spikes": total_spikes,
        "per_unit": per_unit,
        "logical_bytes": total_spikes * (time_layout["itemsize"]
                                         + depth_layout["itemsize"]),
        "cache_bound_bytes": cache_bound,
        "resident_bytes": resident,
        "structures_bytes": structures,
        "library_cache_bytes": library_cache,
        "peak_resident_bytes": cache_bound + resident + structures + library_cache,
        "bound_basis": (" + ".join(bases) if bases else "no slices"),
        "block_bytes": int(block_bytes),
        "spent_bytes": int(spent_bytes),
        "time_layout": time_layout,
        "depth_layout": depth_layout,
    }


def _slice_bounds(index, row):
    """Return the ``[lo, hi)`` bounds of one unit's ragged slice."""
    return (index[row - 1] if row > 0 else 0), index[row]


def read_band_units(url, size, block_bytes, probe, depth_lo_um, depth_hi_um,
                    max_bytes=None, plan_only=False):
    """Read the pinned band's per-unit spike times and per-spike depths.

    Args:
        url: direct S3 URL of the **processed** NWB blob.
        size: the blob's size in bytes.
        block_bytes: HTTP range-request block size. Scattered ragged slices
            transfer far less at 1 MiB than at the module default.
        probe: the probe name to read, exactly as stored in ``probe_name``.
        depth_lo_um: the pinned band's lower ``rel_y`` bound, inclusive.
        depth_hi_um: the pinned band's upper ``rel_y`` bound, inclusive.
        max_bytes: refuse the read if ``peak_resident_bytes`` -- the block cache,
            the converted arrays and the live Python structures together --
            would exceed this many bytes. That single quantity is what a free-RAM
            measurement has to be compared against, and because it contains the
            block-transfer bound it also refuses everything a transfer-only
            ceiling would have refused. None means no ceiling, which is the
            caller taking responsibility for the whole footprint.
        plan_only: resolve and validate the index and the band membership, then
            return without reading any spike data.

    Returns:
        A dict carrying ``probe``, ``band`` (the two bounds), ``plan`` (from
        :func:`plan_transfer`), ``descriptions``, ``provenance``,
        ``electrodes``, ``unit_electrodes`` (every unit on the probe),
        ``band_units`` (the in-band subset, each with ``times`` and ``depths``
        arrays unless ``plan_only``), ``n_units_on_probe``,
        ``integer_dtypes`` (each structural column as stored) and ``io``
        (request count and bytes transferred, which includes metadata as well
        as spikes).

    Raises:
        KeyError: if the file lacks the units or electrodes table.
        ValueError: on any of the four input-error conditions this module
            checks, or if the planned peak resident footprint exceeds
            ``max_bytes``.
    """
    remote = RemoteFile(url, size, block=block_bytes)
    with h5py.File(remote, "r") as handle:
        electrodes = read_flat_electrodes(handle)
        scalars = read_unit_scalars(handle)
        check_ragged_alignment(scalars)
        descriptions = column_descriptions(handle)
        # Read here, in preflight, and never after the ceiling is enforced.
        # source_provenance reads complete stored datasets, so a call placed
        # after the check spends bytes the plan has already promised were
        # bounded -- which is exactly what it used to do.
        provenance = source_provenance(handle)

        depth_description = descriptions.get(DEPTH_COLUMN)
        if not depth_description or DEPTH_UNIT_PHRASE not in depth_description.lower():
            raise ValueError(
                "the %s column's description does not state its unit as %r; it reads %r"
                % (DEPTH_COLUMN, DEPTH_UNIT_PHRASE, depth_description))

        unit_electrodes = resolve_unit_electrodes(scalars, electrodes, probe)
        if not unit_electrodes:
            raise ValueError(
                "no unit names probe %r; the file's probes are %s"
                % (probe, sorted(set(scalars["probe_name"]))))
        band_units = select_band_units(unit_electrodes, depth_lo_um, depth_hi_um)

        node = handle[UNITS_PATH]
        times_dataset = node[TIME_COLUMN]
        depths_dataset = node[DEPTH_COLUMN]
        # The layouts are resolved before spent_bytes is read, because placing a
        # chunked column costs range requests of its own and they are part of
        # what this read spends.
        slices = band_slices(band_units, scalars["times_index"])
        time_layout = column_layout(times_dataset, slices)
        depth_layout = column_layout(depths_dataset, slices)
        plan = plan_transfer(band_units, scalars, time_layout, depth_layout,
                             block_bytes, size, spent_bytes=remote.n_bytes,
                             held=(electrodes, unit_electrodes, descriptions,
                                   provenance))
        if max_bytes is not None and plan["peak_resident_bytes"] > max_bytes:
            raise ValueError(
                "reading %d band units (%d spikes, %d bytes of stored payload) would hold "
                "%d bytes at once -- %d bytes of retained block cache (%s), %d bytes of "
                "converted arrays, %d bytes of Python structures and %d bytes of HDF5 "
                "chunk cache, all live together -- and peak_resident_bytes is above the "
                "declared ceiling of %d. Raise the ceiling deliberately against a "
                "measurement of free memory, or read a smaller band."
                % (plan["n_units"], plan["n_spikes"], plan["logical_bytes"],
                   plan["peak_resident_bytes"], plan["cache_bound_bytes"],
                   plan["bound_basis"], plan["resident_bytes"],
                   plan["structures_bytes"], plan["library_cache_bytes"], max_bytes))

        result = {
            "probe": probe,
            "band": {"depth_lo_um": float(depth_lo_um), "depth_hi_um": float(depth_hi_um)},
            "plan": plan,
            "descriptions": descriptions,
            "provenance": provenance,
            "electrodes": electrodes,
            "unit_electrodes": unit_electrodes,
            "band_units": band_units,
            "n_units_on_probe": len(unit_electrodes),
            "n_units_total": scalars["n_units"],
            "integer_dtypes": scalars["integer_dtypes"],
            "plan_only": bool(plan_only),
        }
        if plan_only:
            result["io"] = {"requests": remote.n_requests, "bytes": remote.n_bytes}
            return result

        for unit in band_units:
            lo, hi = _slice_bounds(scalars["times_index"], unit["row"])
            times = np.asarray(times_dataset[lo:hi], dtype=np.float64)
            depths = np.asarray(depths_dataset[lo:hi], dtype=np.float64)
            if times.size != depths.size:
                raise ValueError(
                    "unit %d read %d times and %d depths from the same slice [%d, %d)"
                    % (unit["row"], times.size, depths.size, lo, hi))
            if times.size and not np.all(np.isfinite(times)):
                raise ValueError(
                    "unit %d carries %d non-finite spike times"
                    % (unit["row"], int((~np.isfinite(times)).sum())))
            if depths.size and not np.all(np.isfinite(depths)):
                raise ValueError(
                    "unit %d carries %d non-finite spike depths"
                    % (unit["row"], int((~np.isfinite(depths)).sum())))
            if times.size > 1 and np.any(np.diff(times) < 0):
                raise ValueError(
                    "unit %d's spike times are not ascending; the binning assumes they are"
                    % unit["row"])
            unit["slice"] = [int(lo), int(hi)]
            unit["n_spikes"] = int(times.size)
            unit["times"] = times
            unit["depths"] = depths
        result["io"] = {"requests": remote.n_requests, "bytes": remote.n_bytes}
    return result


def electrode_tables_agree(raw_probe_rows, processed, probe):
    """Compare the raw and processed files' electrode tables for one probe.

    The band is derived from the raw file's table, while ``max_electrode``
    indexes the processed file's. If the two disagree, a band derived from one
    is being applied to units placed by the other.

    Args:
        raw_probe_rows: the raw file's per-electrode dicts for ``probe``, as
            ``utils.host_anatomy.read_electrode_table`` returns them.
        processed: the dict returned by :func:`read_flat_electrodes` on the
            processed file.
        probe: the probe name.

    Returns:
        A dict with ``agree`` and, when they do not, ``detail`` naming the first
        difference and the two row counts.
    """
    processed_rows = [(processed["rel_y"][i], processed["location"][i])
                      for i in range(processed["n_rows"])
                      if processed["group_name"][i] == probe]
    raw_rows = [(row["depth_um"], row["location"]) for row in raw_probe_rows]
    if len(raw_rows) != len(processed_rows):
        return {"agree": False,
                "detail": "raw table has %d rows for probe %s, processed has %d"
                          % (len(raw_rows), probe, len(processed_rows))}
    for index, (raw_row, processed_row) in enumerate(zip(raw_rows, processed_rows)):
        if raw_row != processed_row:
            return {"agree": False,
                    "detail": "row %d differs: raw %r, processed %r"
                              % (index, raw_row, processed_row)}
    return {"agree": True, "detail": "%d rows identical" % len(raw_rows)}
