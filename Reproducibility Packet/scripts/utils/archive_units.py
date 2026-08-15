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
per unit and are read in full, which makes the transfer that follows an exact
number rather than an estimate: :func:`read_band_units` reports the byte count
it is about to spend, and refuses to spend more than a caller-declared ceiling.

**What it validates, and why validation lives here rather than in the caller.**
Four properties have to hold before a drift number computed from these arrays
means anything, and every one of them is a property of the file rather than of
the statistic:

1. the two ragged columns are partitioned identically, so that a unit's times
   and its depths are the same spikes in the same order;
2. the loaded values are finite, each unit's times ascend, and the depth column
   still carries its documented micrometre unit;
3. each unit's ``max_electrode`` names exactly one electrode on that unit's own
   probe, and that electrode's ``rel_y`` is finite;
4. the processed file's electrode table agrees with the raw file's, because the
   band is derived from the raw table while ``max_electrode`` indexes the
   processed one.

A violation of any of these raises :class:`ValueError`. That is deliberate and it
matters for the host order: a candidate whose *inputs* are malformed has not
failed the drift gate, and recording it as a drift failure would hand the host
to the next rank for a reason that has nothing to do with drift.

Nothing here computes, thresholds, or interprets a drift value. This module
reads and checks; ``utils.band_drift`` measures.
"""

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


def source_provenance(handle):
    """Read whatever conversion provenance the asset carries, without gating on it.

    Args:
        handle: an open :class:`h5py.File`.

    Returns:
        A dict from path to its stored value as a string, omitting paths the
        file does not carry. Values are recorded for the report; no value here
        is required to hold, because the session-time convention this project
        relies on is pinned to a conversion-repository commit rather than
        asserted by the asset.
    """
    out = {}
    for path in PROVENANCE_PATHS:
        if path not in handle:
            continue
        node = handle[path]
        try:
            value = node[()]
        except (TypeError, ValueError):
            continue
        if isinstance(value, bytes):
            value = value.decode()
        out[path] = str(value)
        for key in ("file_name", "software", "version"):
            attr = node.attrs.get(key)
            if attr is None:
                continue
            if isinstance(attr, bytes):
                attr = attr.decode()
            out["%s@%s" % (path, key)] = str(attr)
    return out


def read_unit_scalars(handle):
    """Read the one-value-per-unit columns the band selection needs.

    Args:
        handle: an open :class:`h5py.File`.

    Returns:
        A dict with ``probe_name`` and ``label`` (lists of str),
        ``max_electrode`` (list of int), ``times_index`` and ``depths_index``
        (lists of int, the ragged columns' own end-offset indices),
        ``n_units``, and ``n_times`` / ``n_depths``, the two ragged columns'
        total lengths.

    Raises:
        KeyError: if the units table or either ragged column is absent.
    """
    if UNITS_PATH not in handle:
        raise KeyError("file has no /%s" % UNITS_PATH)
    node = handle[UNITS_PATH]
    for name in (TIME_COLUMN, DEPTH_COLUMN,
                 TIME_COLUMN + "_index", DEPTH_COLUMN + "_index"):
        if name not in node:
            raise KeyError("units table has no %s" % name)
    probe_name = _decode(node["probe_name"][:])
    labels = (_decode(node["kilosort2_label"][:])
              if "kilosort2_label" in node else [""] * len(probe_name))
    return {
        "probe_name": probe_name,
        "label": labels,
        "max_electrode": [int(v) for v in node["max_electrode"][:]],
        "times_index": [int(v) for v in node[TIME_COLUMN + "_index"][:]],
        "depths_index": [int(v) for v in node[DEPTH_COLUMN + "_index"][:]],
        "n_units": len(probe_name),
        "n_times": int(node[TIME_COLUMN].shape[0]),
        "n_depths": int(node[DEPTH_COLUMN].shape[0]),
    }


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


def plan_transfer(band_units, scalars, time_itemsize, depth_itemsize):
    """Compute exactly how many bytes the band units' slices will cost.

    The ragged indices are already in hand, so this is a count rather than an
    estimate -- which is what the project's compute rule asks for before a step
    that needs real memory.

    Args:
        band_units: the list returned by :func:`select_band_units`.
        scalars: the dict returned by :func:`read_unit_scalars`.
        time_itemsize: bytes per stored spike time.
        depth_itemsize: bytes per stored spike depth.

    Returns:
        A dict with ``n_units``, ``n_spikes``, ``bytes`` and ``per_unit``, the
        last a list of ``(row, n_spikes)`` pairs in row order.
    """
    index = scalars["times_index"]
    per_unit = []
    total_spikes = 0
    for unit in band_units:
        row = unit["row"]
        lo = index[row - 1] if row > 0 else 0
        hi = index[row]
        per_unit.append((row, hi - lo))
        total_spikes += hi - lo
    return {
        "n_units": len(band_units),
        "n_spikes": total_spikes,
        "bytes": total_spikes * (time_itemsize + depth_itemsize),
        "per_unit": per_unit,
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
        max_bytes: refuse to read more than this many bytes of spike data. None
            means no ceiling, which is the caller taking responsibility for the
            transfer.
        plan_only: resolve and validate the index and the band membership, then
            return without reading any spike data.

    Returns:
        A dict carrying ``probe``, ``band`` (the two bounds), ``plan`` (from
        :func:`plan_transfer`), ``descriptions``, ``provenance``,
        ``electrodes``, ``unit_electrodes`` (every unit on the probe),
        ``band_units`` (the in-band subset, each with ``times`` and ``depths``
        arrays unless ``plan_only``), ``n_units_on_probe`` and ``io`` (request
        count and bytes transferred, which includes metadata as well as spikes).

    Raises:
        KeyError: if the file lacks the units or electrodes table.
        ValueError: on any of the four input-error conditions this module
            checks, or if the planned transfer exceeds ``max_bytes``.
    """
    remote = RemoteFile(url, size, block=block_bytes)
    with h5py.File(remote, "r") as handle:
        electrodes = read_flat_electrodes(handle)
        scalars = read_unit_scalars(handle)
        check_ragged_alignment(scalars)
        descriptions = column_descriptions(handle)

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
        plan = plan_transfer(band_units, scalars,
                             times_dataset.dtype.itemsize, depths_dataset.dtype.itemsize)
        if max_bytes is not None and plan["bytes"] > max_bytes:
            raise ValueError(
                "reading %d band units would transfer %d bytes of spike data, above the "
                "declared ceiling of %d; raise the ceiling deliberately or read a smaller band"
                % (plan["n_units"], plan["bytes"], max_bytes))

        result = {
            "probe": probe,
            "band": {"depth_lo_um": float(depth_lo_um), "depth_hi_um": float(depth_hi_um)},
            "plan": plan,
            "descriptions": descriptions,
            "provenance": source_provenance(handle),
            "electrodes": electrodes,
            "unit_electrodes": unit_electrodes,
            "band_units": band_units,
            "n_units_on_probe": len(unit_electrodes),
            "n_units_total": scalars["n_units"],
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
