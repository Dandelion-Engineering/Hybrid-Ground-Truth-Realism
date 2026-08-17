"""End-to-end synthetic tests for the archive-reading drift command.

``measure_host_drift.py`` is the piece that turns a candidate host recording
into a drift verdict, and it decides which recording this whole experiment runs
on. It is therefore exercised end to end before it is ever pointed at the
archive: every case here builds a pair of local HDF5 files shaped like the raw
and processed NWB assets, runs the real command against them, and checks a
result that is known in advance by construction.

**Local files, real command.** The reader's only network dependency is
``utils.remote_hdf5.RemoteFile``. This harness substitutes a local-file object
with the same interface into the three modules that hold a reference to it, and
substitutes a synthetic asset listing for ``utils.dandi``. Nothing else is
mocked: the same ``main()`` runs, the same ragged index is resolved, the same
estimator computes the same statistic under the same pre-declared parameters,
and the same report is written.

**The input-error cases are the point of the exercise.** A malformed candidate
must stop the command without a verdict, because the host order is
first-admissible and a candidate recorded as failing the drift gate for a
reason that is not drift is handed to the next rank irrecoverably. Every one of
the four confirmations the selection document requires has at least one fixture
here that violates it, plus the three the reader adds on its own account: the
transfer ceiling, the probe-to-series mapping, and the session-to-asset
resolution.

**What this harness does not claim.** The fixtures are shaped like the assets,
not sampled from them. Their timestamps are a short evenly spaced ramp rather
than a 30 kHz stream, because only the first and last values and the length are
ever consumed. Nothing here is evidence about any real recording, and no case
asserts anything about what a candidate's drift will turn out to be.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Claude/tools/test_measure_host_drift.py"
"""

import argparse
import contextlib
import datetime
import hashlib
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile
import time
import traceback

import numpy as np

import h5py

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PACKET_SCRIPTS = os.path.join(PROJECT_ROOT, "Reproducibility Packet", "scripts")
sys.path.insert(0, PACKET_SCRIPTS)

from utils import archive_units, band_drift, dandi, host_anatomy  # noqa: E402
import screen_host_timing  # noqa: E402

BAND_LOCATION = "Field CA1"
OTHER_LOCATION = "Field CA3"
TARGET = "CA1"
PROBES = ("Probe00", "Probe01")
N_ROWS_PER_PROBE = 40
ROW_PITCH_UM = 20.0
BAND_ROW_LO = 10          # rel_y 200 um
BAND_ROW_HI = 28          # rel_y 560 um
EXTENT_S = 900.0          # 15 full 60 s bins
DEPTH_DESCRIPTION = ("Distance from the probe tip for each spike in micrometers, "
                     "computed from waveform center of mass. 0 = probe tip, values "
                     "increase toward brain surface.")
TIME_DESCRIPTION = "the spike times for each unit in seconds"

# Every distinct ``timestamps_reference_time`` the archive really carries.
#
# **This is the population, not a fixture.** It is the 79 distinct values of
# the 142 assets ``probe_conversion_pairs.py`` read across 71 sessions of
# DANDI 000409, taken from ``conversion_pairs_pinned_2026-08-16.json`` and
# ``conversion_pairs_sample60_2026-08-16.json`` in this folder and frozen here
# so the suite stays self-contained. Codex replayed all 71 independently and
# reproduced every value.
#
# **Why the suite carries it at all.** RC-004 exists because a rule that
# passed three review rounds and twenty-six mutations admitted 0 of these 71
# sessions, and nothing in a synthetic harness could have said so: a mutation
# proves a check depends on its mechanism, never that the check has a
# non-empty population. RC-004-F1 then tightened the grammar this field is
# read under, and a tightening is exactly the change that can empty a
# population again. The case that consumes this list is the one that says it
# did not.
MEASURED_REFERENCE_TIMES = (
    "2019-12-07T16:19:38.121000+00:00",
    "2019-12-08T20:01:23.391000+00:00",
    "2019-12-09T17:31:23.762000+00:00",
    "2019-12-11T11:02:46+00:00",
    "2020-01-08T15:52:42-05:00",
    "2020-01-09T15:43:57-05:00",
    "2020-01-21T13:52:24-05:00",
    "2020-01-21T14:03:44+00:00",
    "2020-01-22T08:28:49-05:00",
    "2020-01-22T10:50:59+00:00",
    "2020-01-22T15:39:54-05:00",
    "2020-01-23T15:12:02+00:00",
    "2020-01-28T11:34:01.365875-08:00",
    "2020-02-01T15:49:28.905174-08:00",
    "2020-02-11T14:25:12-05:00",
    "2020-02-18T14:24:19-05:00",
    "2020-02-20T13:15:02-05:00",
    "2020-02-24T14:41:02-05:00",
    "2020-02-28T10:07:18-05:00",
    "2020-03-03T14:27:51-05:00",
    "2020-03-04T13:14:42.728981-08:00",
    "2020-03-12T11:27:09.707868-07:00",
    "2020-03-22T12:56:40-04:00",
    "2020-05-23T12:31:58.311253-04:00",
    "2020-07-13T18:56:18+01:00",
    "2020-07-26T08:42:16-04:00",
    "2020-08-19T11:43:13.897987-04:00",
    "2020-08-19T12:43:13.897987-04:00",
    "2020-09-10T14:19:38.570886+01:00",
    "2020-09-16T08:11:47-04:00",
    "2020-09-20T19:12:54.571582+01:00",
    "2020-10-07T18:20:13.449770+01:00",
    "2020-11-25T13:17:54.132432+00:00",
    "2020-12-06T19:05:47.902000+00:00",
    "2020-12-07T19:34:42.945000+00:00",
    "2020-12-08T16:37:47.025234+00:00",
    "2021-01-16T19:51:02-05:00",
    "2021-01-19T17:15:10+00:00",
    "2021-01-21T17:05:26-05:00",
    "2021-01-25T15:32:41.052960-05:00",
    "2021-04-13T10:28:53.043796-04:00",
    "2021-04-13T11:28:53.043796-04:00",
    "2021-05-10T14:33:49.023776-04:00",
    "2021-05-10T15:33:49.023776-04:00",
    "2021-06-14T13:29:00.626588-04:00",
    "2021-06-22T13:25:20.389828-04:00",
    "2021-06-22T14:25:20.389828-04:00",
    "2021-07-02T14:28:23.348923-04:00",
    "2021-07-02T15:28:23.348923-04:00",
    "2021-07-19T13:24:23.683992-04:00",
    "2021-07-19T14:24:23.683992-04:00",
    "2021-07-20T09:58:58.347567-04:00",
    "2021-07-20T10:58:58.347567-04:00",
    "2021-11-09T19:32:47.033823+00:00",
    "2022-02-20T16:09:07.326998+00:00",
    "2022-04-14T16:36:16.565033-07:00",
    "2022-05-07T15:58:28.902138+01:00",
    "2022-06-16T11:49:20.330000+01:00",
    "2022-06-17T15:27:55.990000+01:00",
    "2022-08-02T16:36:06.329463-07:00",
    "2022-08-16T16:11:36.075354-07:00",
    "2022-08-20T17:11:20-07:00",
    "2022-09-12T14:33:06-04:00",
    "2022-09-12T15:33:06-04:00",
    "2022-10-05T16:28:57+01:00",
    "2022-10-07T16:14:14.729838+01:00",
    "2022-10-18T17:41:58+01:00",
    "2022-10-28T16:46:29+01:00",
    "2022-11-16T16:48:59.454308+00:00",
    "2023-02-01T16:39:26-08:00",
    "2023-02-07T13:41:46-08:00",
    "2023-04-06T16:08:54.319363+01:00",
    "2023-06-13T10:42:35.707675+01:00",
    "2023-07-12T14:17:48.191150-07:00",
    "2023-07-14T15:17:40.935162-07:00",
    "2023-08-15T17:10:15.346939-07:00",
    "2023-08-16T16:43:15.074954-07:00",
    "2023-08-29T16:43:29-07:00",
    "2023-09-01T13:56:04.163286-07:00",
)


# Every local reader built during a case, so the suite can ask afterwards which
# byte ranges of a fixture were actually touched. Cleared at the start of each
# run_case; readers are small and a case builds a handful.
READERS = []


def distinct_bytes(url):
    """Return the union, in bytes, of every range any reader touched on one file.

    The plan's ``cache_bound_bytes`` bounds *distinct* bytes -- a block fetched
    twice is transferred once, because the reader caches it. The local stand-in
    has no cache, so its ``n_bytes`` counter double-counts and is not the
    quantity to compare against a bound. This is.

    Args:
        url: the fixture path a reader was opened on.

    Returns:
        The size of the union of the touched ranges, in bytes.
    """
    spans = sorted(span for reader in READERS
                   if os.path.abspath(reader.url) == os.path.abspath(url)
                   for span in reader.touched)
    total, end = 0, 0
    for lo, hi in spans:
        if hi <= end:
            continue
        total += hi - max(lo, end)
        end = hi
    return total


class LocalFile(io.RawIOBase):
    """A local stand-in for ``RemoteFile`` with the same constructor and counters.

    The counters are deliberately named the same and mean something close but
    not identical: ``n_requests`` counts ``read`` calls rather than HTTP range
    requests, because there is no network here. What the counters are used for
    in these cases is ordering -- a planned read must transfer strictly less
    than a full one -- and that ordering holds under either meaning.
    """

    def __init__(self, url, size, block=None, timeout=None, retries=None):
        self._handle = open(url, "rb")
        self.url = url
        self.size = int(size)
        self.n_requests = 0
        self.n_bytes = 0
        # Every byte range this reader touches, so a case can ask what the read
        # cost in *distinct* bytes. n_bytes cannot answer that: this reader has
        # no cache, so a region read twice is counted twice and the total can
        # exceed the file size, while the plan's bound is on distinct blocks.
        self.touched = []
        READERS.append(self)

    def readable(self):
        """Return True."""
        return True

    def seekable(self):
        """Return True."""
        return True

    def writable(self):
        """Return False."""
        return False

    def seek(self, offset, whence=io.SEEK_SET):
        """Delegate to the underlying file."""
        return self._handle.seek(offset, whence)

    def tell(self):
        """Delegate to the underlying file."""
        return self._handle.tell()

    def read(self, n=-1):
        """Read and count, so the reported io counters stay meaningful."""
        start = self._handle.tell()
        data = self._handle.read(n if n is not None and n >= 0 else -1)
        self.n_requests += 1
        self.n_bytes += len(data)
        self.touched.append((start, start + len(data)))
        return data

    def readinto(self, buffer):
        """Read into a pre-allocated buffer."""
        data = self.read(len(buffer))
        buffer[:len(data)] = data
        return len(data)

    def close(self):
        """Close the underlying file."""
        if not self._handle.closed:
            self._handle.close()
        super().close()


class BlockLocalFile(LocalFile):
    """A local stand-in that caches fixed-width blocks the way ``RemoteFile`` does.

    :class:`LocalFile` reads whatever h5py asks for, which is the right shape
    for the cases that only need the command to run. It is the wrong shape for
    asking what a read *costs*: the real reader fetches whole blocks and caches
    them, so a scattered slice can cost a block of transfer for a few kilobytes
    of payload. Every byte counted here is a block byte, fetched once, which is
    the quantity the transfer bound in ``plan_transfer`` is a bound on.
    """

    def __init__(self, url, size, block=None, timeout=None, retries=None):
        LocalFile.__init__(self, url, size)
        self.block = int(block or 65536)
        self._pos = 0
        self._blocks = {}

    def seek(self, offset, whence=io.SEEK_SET):
        """Move a cursor of this object's own, not the backing file's."""
        if whence == io.SEEK_SET:
            self._pos = offset
        elif whence == io.SEEK_CUR:
            self._pos += offset
        elif whence == io.SEEK_END:
            self._pos = self.size + offset
        else:
            raise ValueError("unsupported whence %r" % whence)
        if self._pos < 0:
            raise ValueError("negative seek position %r" % self._pos)
        return self._pos

    def tell(self):
        """Return this object's cursor."""
        return self._pos

    def _block(self, index):
        """Fetch one whole block, counting it only the first time."""
        if index not in self._blocks:
            lo = index * self.block
            self._handle.seek(lo)
            payload = self._handle.read(min(self.block, self.size - lo))
            self._blocks[index] = payload
            self.n_requests += 1
            self.n_bytes += len(payload)
            self.touched.append((lo, lo + len(payload)))
        return self._blocks[index]

    def read(self, n=-1):
        """Read through the block cache."""
        remaining = self.size - self._pos
        if remaining <= 0:
            return b""
        want = remaining if n is None or n < 0 else min(n, remaining)
        out = bytearray()
        while want > 0:
            index, offset = divmod(self._pos, self.block)
            chunk = self._block(index)[offset:offset + want]
            if not chunk:
                break
            out += chunk
            self._pos += len(chunk)
            want -= len(chunk)
        return bytes(out)


def install_local_file():
    """Point every consumer of ``RemoteFile`` at :class:`LocalFile`.

    Each module bound the name at import time, so patching the defining module
    alone would leave the bindings untouched. Patching every consumer by name is
    the honest way to say which modules this substitution reaches.
    """
    archive_units.RemoteFile = LocalFile
    host_anatomy.RemoteFile = LocalFile
    screen_host_timing.RemoteFile = LocalFile


def session_id(name):
    """Turn a case name into a UUID-shaped session identifier.

    ``utils.dandi`` recognises a session only in the archive's own
    ``ses-<uuid>`` path form, so a fixture named after its case still has to
    carry a well-formed identifier. Deriving it from the name keeps each case's
    identifier stable across runs, which is what the permutation seeds need.

    Args:
        name: the case name.

    Returns:
        A 36-character hexadecimal identifier in ``8-4-4-4-12`` form.
    """
    digest = hashlib.sha256(name.encode("utf-8")).hexdigest()
    return "%s-%s-%s-%s-%s" % (digest[:8], digest[8:12], digest[12:16],
                               digest[16:20], digest[20:32])


def install_local_assets(pairs):
    """Substitute a synthetic asset listing addressed by local path.

    Args:
        pairs: a list of ``(session, raw_path, processed_path)`` tuples.
    """
    assets = []
    for session, raw_path, processed_path in pairs:
        assets.append({
            "asset_id": "raw-%s" % session,
            "path": "sub-TEST/sub-TEST_ses-%s%s" % (session, dandi.RAW_SUFFIX),
            "size": os.path.getsize(raw_path),
            "blob": raw_path,
        })
        assets.append({
            "asset_id": "processed-%s" % session,
            "path": "sub-TEST/sub-TEST_ses-%s%s" % (session, dandi.PROCESSED_SUFFIX),
            "size": os.path.getsize(processed_path),
            "blob": processed_path,
        })
    dandi.list_assets = lambda *a, **k: assets
    dandi.blob_url = lambda asset: asset["blob"]


def default_electrodes():
    """Build the electrode rows both files carry by default.

    Returns:
        A list of dicts with ``rel_y``, ``location`` and ``group_name``, two
        probes' worth, with a contiguous target-labelled band on each.
    """
    rows = []
    for probe in PROBES:
        for index in range(N_ROWS_PER_PROBE):
            rows.append({
                "rel_y": index * ROW_PITCH_UM,
                "location": (BAND_LOCATION if BAND_ROW_LO <= index <= BAND_ROW_HI
                             else OTHER_LOCATION),
                "group_name": probe,
            })
    return rows


def band_bounds():
    """Return the ``(lo, hi)`` rel_y bounds the default electrode table implies."""
    return BAND_ROW_LO * ROW_PITCH_UM, BAND_ROW_HI * ROW_PITCH_UM


UNSET = object()

# What the real assets carry. Session 7 read /general from one raw NWB per
# subject across 21 assets of DANDI 000409 and found this string on 20 of them,
# with "v0.9.1" on the twenty-first. The fixtures default to it because the
# command authenticates the conversion toolchain rather than recording it.
DEFAULT_PROVENANCE = {
    "general/source_script": "Created using NeuroConv v0.9.2",
    "general/lab": "cortexlab",
}

# The instant the fixtures declare their time values are counted from. NWB
# defines timestamps_reference_time as the origin every stored time in the file
# is relative to, and all 142 assets read across 71 sessions of DANDI 000409
# carry it as a timezone-aware ISO-8601 value with session_start_time equal to
# it. This one is a real value from that measurement, NYU-39's raw half.
#
# **It is a separate argument from the provenance mapping because they are
# separate axes.** Every fixture that varies the conversion statement still
# needs a valid reference time, or it would be refused for a reason the case was
# not written to exercise -- and every fixture that varies the reference time
# still needs a valid conversion statement, for the same reason in the other
# direction.
DEFAULT_REFERENCE_TIME = "2021-05-10T14:33:49.023776-04:00"


def _write_provenance(handle, provenance, reference_time=UNSET):
    """Write a fixture's conversion-provenance datasets.

    Args:
        handle: the open fixture file.
        provenance: mapping of NWB path to stored string.
        reference_time: the root reference-time value, defaulting to
            :data:`DEFAULT_REFERENCE_TIME`. ``None`` omits both root time
            datasets, which is the fixture for an asset that states no origin.
    """
    dt = h5py.string_dtype(encoding="utf-8")
    for nwb_path, value in (provenance or {}).items():
        dataset = handle.create_dataset(nwb_path, data=value, dtype=dt)
        dataset.attrs["file_name"] = "%s.py" % nwb_path.rsplit("/", 1)[-1]
    stamp = DEFAULT_REFERENCE_TIME if reference_time is UNSET else reference_time
    if stamp is not None:
        handle.create_dataset(archive_units.REFERENCE_TIME_PATH, data=stamp, dtype=dt)
        # Equal to the reference time, as it is on all 142 measured assets. It
        # is recorded and gates nothing, so it follows the same value rather
        # than becoming a second axis nothing reads.
        handle.create_dataset("session_start_time", data=stamp, dtype=dt)


def _write_electrode_table(handle, rows):
    """Write an NWB-shaped electrodes table."""
    group = handle.create_group("general/extracellular_ephys/electrodes")
    group.create_dataset("id", data=np.arange(len(rows), dtype=np.int64))
    group.create_dataset("rel_y", data=np.array([r["rel_y"] for r in rows],
                                                dtype=np.float64))
    group.create_dataset("rel_x", data=np.zeros(len(rows), dtype=np.float64))
    dt = h5py.string_dtype(encoding="utf-8")
    group.create_dataset("location", data=np.array([r["location"] for r in rows],
                                                   dtype=object), dtype=dt)
    group.create_dataset("group_name", data=np.array([r["group_name"] for r in rows],
                                                     dtype=object), dtype=dt)


def write_raw(path, rows, t_first_s, t_last_s, timing_source="timestamps",
              series_names=None, provenance=UNSET, reference_time=UNSET):
    """Write a raw-asset-shaped file: an electrode table and AP series timing.

    Args:
        path: destination path.
        rows: electrode rows from :func:`default_electrodes`.
        t_first_s: the AP stream's first aligned timestamp.
        t_last_s: its last aligned timestamp.
        timing_source: ``"timestamps"`` writes an aligned timestamp dataset;
            ``"starting_time"`` writes the nominal-rate alternative instead,
            which the reader must refuse.
        series_names: explicit AP series names, defaulting to one per probe.
        provenance: mapping of NWB path to stored string. It defaults to the
            shape the 21 measured assets of this dandiset carry, because the
            command now authenticates it on the raw asset as well; pass an
            explicit mapping, or an empty one, to build the fixtures that must
            be refused.
        reference_time: the declared session-time origin, defaulting to
            :data:`DEFAULT_REFERENCE_TIME`. ``None`` writes none at all, which
            the command must refuse as an input error.
    """
    names = series_names or ["ElectricalSeries%sAP" % probe for probe in PROBES]
    provenance = DEFAULT_PROVENANCE if provenance is UNSET else provenance
    with h5py.File(path, "w") as handle:
        _write_electrode_table(handle, rows)
        _write_provenance(handle, provenance, reference_time)
        acquisition = handle.create_group("acquisition")
        for name in names:
            node = acquisition.create_group(name)
            node.create_dataset("data", data=np.zeros((1000, 4), dtype=np.int16))
            if timing_source == "timestamps":
                node.create_dataset(
                    "timestamps",
                    data=np.linspace(t_first_s, t_last_s, 1000, dtype=np.float64))
            else:
                start = node.create_dataset("starting_time", data=float(t_first_s))
                start.attrs["rate"] = 30000.0


def replace_dataset(path, edits):
    """Rewrite named datasets inside a written fixture, keeping their attributes.

    Some malformed inputs cannot be requested from the fixture writers without
    giving the writers a knob for every possible defect. Writing a well-formed
    file and then replacing one dataset is closer to what a malformed asset
    actually is, and it keeps the writers honest: the defect is visible in the
    case rather than hidden in a default.

    Args:
        path: the fixture to edit in place.
        edits: a mapping from NWB path to the replacement array.
    """
    with h5py.File(path, "r+") as handle:
        for name, values in edits.items():
            attrs = dict(handle[name].attrs)
            del handle[name]
            dataset = handle.create_dataset(name, data=values)
            for key, value in attrs.items():
                dataset.attrs[key] = value


def fragment_ragged_columns(path, chunk_elements=64, filler_elements=8192):
    """Rewrite the two ragged columns so their chunks are not contiguous.

    HDF5 allocates a chunk where it can, and a file written incrementally
    alongside other growing datasets ends up with each column's chunks
    interleaved with unrelated data. This reproduces that: it appends one chunk
    of each column and then a much larger filler block, over and over, so
    successive chunks of one column end up thousands of bytes apart with other
    allocations in between. The file stays entirely valid.

    This is the construction Codex used to show that treating the
    first-to-last-chunk span as one contiguous region under-bounds a
    fixed-block read, and it stays here as a fixture for the repair.

    Args:
        path: a processed fixture written with ``chunk_elements=None``.
        chunk_elements: chunk length for the two rewritten columns.
        filler_elements: how much unrelated data to allocate between them.
    """
    columns = (archive_units.TIME_COLUMN, archive_units.DEPTH_COLUMN)
    with h5py.File(path, "r+") as handle:
        node = handle[archive_units.UNITS_PATH]
        originals = {name: node[name][:] for name in columns}
        descriptions = {name: node[name].attrs.get("description") for name in columns}
        replacements = {}
        for name in columns:
            replacements[name] = node.create_dataset(
                name + "_fragmented", shape=(0,), maxshape=(None,),
                chunks=(chunk_elements,), dtype=originals[name].dtype)
            if descriptions[name] is not None:
                replacements[name].attrs["description"] = descriptions[name]
        filler = node.create_dataset("fragment_filler", shape=(0,), maxshape=(None,),
                                     chunks=(filler_elements,), dtype=np.uint8)
        block = np.arange(filler_elements, dtype=np.uint8)
        n_values = len(originals[columns[0]])
        for start in range(0, n_values, chunk_elements):
            stop = min(start + chunk_elements, n_values)
            for name in columns:
                dataset = replacements[name]
                dataset.resize((stop,))
                dataset[start:stop] = originals[name][start:stop]
                old = len(filler)
                filler.resize((old + filler_elements,))
                filler[old:] = block
            handle.flush()
        for name in columns:
            del node[name]
            node.move(name + "_fragmented", name)
        handle.flush()


def write_processed(path, rows, units, depth_description=DEPTH_DESCRIPTION,
                    depth_dtype=np.float64, index_mutator=None, provenance=UNSET,
                    time_dtype=np.float64, chunk_elements=None,
                    reference_time=UNSET):
    """Write a processed-asset-shaped file: an electrode table and a units table.

    Args:
        path: destination path.
        rows: electrode rows, normally the same list the raw file carries.
        units: a list of dicts with ``probe``, ``max_electrode``, ``label``,
            ``times`` and ``depths``.
        depth_description: the depth column's stored description.
        depth_dtype: storage dtype for the depth column, so a fixture can prove
            the reported byte cost follows the file's own item size.
        time_dtype: storage dtype for the spike-time column, for the same
            reason.
        chunk_elements: chunk length for the two ragged columns, which makes
            them chunked rather than contiguous and so removes the file offsets
            the transfer bound uses when it can.
        index_mutator: optional callable taking the two index lists and
            returning the pair actually written, for the malformed-index cases.
        provenance: mapping of NWB path to stored string, defaulting to the
            measured shape. ``general/source_script`` is authenticated rather
            than recorded, so a fixture that omits it must do so deliberately.
        reference_time: the declared session-time origin, defaulting to
            :data:`DEFAULT_REFERENCE_TIME` -- the same value the raw writer
            uses, so the pair agrees unless a case makes it disagree. ``None``
            writes none at all.
    """
    provenance = DEFAULT_PROVENANCE if provenance is UNSET else provenance
    times = np.concatenate([u["times"] for u in units]) if units else np.zeros(0)
    depths = np.concatenate([u["depths"] for u in units]) if units else np.zeros(0)
    counts = [len(u["times"]) for u in units]
    ends = list(np.cumsum(counts)) if counts else []
    times_index, depths_index = [int(v) for v in ends], [int(v) for v in ends]
    if index_mutator is not None:
        times_index, depths_index = index_mutator(times_index, depths_index)
    dt = h5py.string_dtype(encoding="utf-8")
    with h5py.File(path, "w") as handle:
        _write_electrode_table(handle, rows)
        _write_provenance(handle, provenance, reference_time)
        node = handle.create_group("units")
        node.create_dataset("probe_name",
                            data=np.array([u["probe"] for u in units], dtype=object),
                            dtype=dt)
        node.create_dataset("kilosort2_label",
                            data=np.array([u["label"] for u in units], dtype=object),
                            dtype=dt)
        node.create_dataset("max_electrode",
                            data=np.array([u["max_electrode"] for u in units],
                                          dtype=np.int64))
        chunks = (chunk_elements,) if chunk_elements else None
        time_column = node.create_dataset("spike_times",
                                          data=times.astype(time_dtype), chunks=chunks)
        time_column.attrs["description"] = TIME_DESCRIPTION
        depth_column = node.create_dataset("spike_distances_from_probe_tip_um",
                                           data=depths.astype(depth_dtype), chunks=chunks)
        depth_column.attrs["description"] = depth_description
        node.create_dataset("spike_times_index",
                            data=np.array(times_index, dtype=np.int64))
        node.create_dataset("spike_distances_from_probe_tip_um_index",
                            data=np.array(depths_index, dtype=np.int64))


def synth_unit(seed, base_depth_um, rate_hz=0.5, noise_um=3.0, ramp_um_per_min=0.0,
               extent_s=EXTENT_S, start_s=0.0, gap=None, prepend_s=()):
    """Build one synthetic unit's spike times and per-spike depths.

    Args:
        seed: PRNG seed, so every fixture is reproducible.
        base_depth_um: the unit's typical depth.
        rate_hz: mean firing rate.
        noise_um: per-spike depth-estimation noise, as a standard deviation.
        ramp_um_per_min: a linear depth trend, in micrometres per minute.
        extent_s: the recording's session-time extent.
        start_s: earliest spike time, which may be negative to exercise the
            pre-origin exclusion.
        gap: optional ``(lo_s, hi_s)`` interval to leave empty, for the
            invalid-bin fixture.
        prepend_s: explicit spike times placed before every drawn one. A
            uniform draw over a whole recording essentially never lands in the
            few microseconds before session zero, so the pre-origin fixture
            states its spikes rather than hoping for them.

    Returns:
        An ascending ``times`` array and its aligned ``depths`` array.
    """
    rng = np.random.default_rng(seed)
    n = int(rate_hz * (extent_s - start_s))
    times = np.sort(rng.uniform(start_s, extent_s, n))
    if gap is not None:
        times = times[(times < gap[0]) | (times >= gap[1])]
    if len(prepend_s):
        times = np.concatenate([np.asarray(prepend_s, dtype=np.float64), times])
    depths = (base_depth_um
              + (ramp_um_per_min / 60.0) * times
              + rng.normal(0.0, noise_um, times.size))
    return times, depths


def band_units(n_units=8, ramp_um_per_min=0.0, labels=None, seed0=100,
               start_s=0.0, gap_unit=None, probe=PROBES[0], prepend_s=()):
    """Build a set of in-band units for the default electrode table.

    Args:
        n_units: how many units to place inside the band.
        ramp_um_per_min: a common depth trend shared by every unit.
        labels: per-unit quality labels, defaulting to a mix that is deliberately
            not all ``good``.
        seed0: base PRNG seed.
        start_s: earliest spike time for every unit.
        gap_unit: index of one unit to give a one-bin gap, or None.
        probe: which probe the units sit on.

    Returns:
        A list of unit dicts ready for :func:`write_processed`.
    """
    labels = labels or ["good", "mua", "good", "noise", "mua", "good", "mua", "good"]
    probe_offset = PROBES.index(probe) * N_ROWS_PER_PROBE
    units = []
    for index in range(n_units):
        row = BAND_ROW_LO + (index % (BAND_ROW_HI - BAND_ROW_LO + 1))
        times, depths = synth_unit(
            seed0 + index, base_depth_um=1000.0 + 10.0 * index,
            ramp_um_per_min=ramp_um_per_min, start_s=start_s,
            gap=(420.0, 480.0) if gap_unit == index else None,
            prepend_s=prepend_s)
        units.append({
            "probe": probe,
            "max_electrode": probe_offset + row,
            "label": labels[index % len(labels)],
            "times": times,
            "depths": depths,
        })
    return units


def out_of_band_unit(seed=900, probe=PROBES[0]):
    """Build one unit whose peak electrode sits outside the band."""
    times, depths = synth_unit(seed, base_depth_um=100.0)
    return {"probe": probe, "max_electrode": PROBES.index(probe) * N_ROWS_PER_PROBE + 2,
            "label": "good", "times": times, "depths": depths}


class Harness:
    """Collect pass/fail results and print one line per check."""

    def __init__(self):
        self.passed = 0
        self.failed = []

    def check(self, name, condition, detail=""):
        """Record one boolean check."""
        if condition:
            self.passed += 1
        else:
            self.failed.append((name, detail))
            print("  FAIL %s %s" % (name, detail), flush=True)

    def equal(self, name, got, want):
        """Record an equality check, printing both values when it fails."""
        self.check(name, got == want, "got %r, want %r" % (got, want))

    def close(self, name, got, want, tol):
        """Record a numeric closeness check."""
        self.check(name, abs(got - want) <= tol,
                   "got %r, want %r +/- %r" % (got, want, tol))


def run_case(tmp_root, name, raw_writer, processed_writer, argv_extra=(),
             gate="strict", session=None, capture=False):
    """Build one fixture pair, run the command, and return its outcome.

    Args:
        tmp_root: directory to build the fixture in.
        name: case name, used as the subdirectory name.
        raw_writer: callable taking the raw file's path.
        processed_writer: callable taking the processed file's path.
        argv_extra: extra command-line arguments.
        gate: which pre-declared threshold to apply.
        session: session identifier, defaulting to the case name.
        capture: collect the command's stdout instead of letting it through,
            for a case that has to assert something was *not* printed. Off by
            default, so the suite's console output is unchanged for every case
            that does not ask for it.

    Returns:
        A dict with ``status`` (0, or the SystemExit message), ``out`` (the
        report path), ``text`` (its contents or None), ``record`` (the JSON
        record or None) and ``stdout`` (the captured transcript, or None when
        ``capture`` is off -- None rather than "" so a case cannot assert a
        phrase is absent from a transcript it never collected).
    """
    import json
    session = session_id(session or name)
    case_dir = os.path.join(tmp_root, name)
    os.makedirs(case_dir, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    raw_writer(raw_path)
    processed_writer(processed_path)
    del READERS[:]
    install_local_assets([(session, raw_path, processed_path)])
    out = os.path.join(case_dir, "report.txt")
    records = os.path.join(case_dir, "record.json")
    argv = ["--session", session, "--probe", PROBES[0], "--target", TARGET,
            "--assets-cache", os.path.join(case_dir, "assets.json"),
            "--gate", gate, "--out", out, "--records", records]
    argv.extend(argv_extra)
    transcript = None
    if capture:
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                status = CLI.main(argv)
        except SystemExit as exc:
            status = str(exc.code)
        transcript = buffer.getvalue()
    else:
        try:
            status = CLI.main(argv)
        except SystemExit as exc:
            status = str(exc.code)
    text = None
    if os.path.exists(out):
        with open(out, "r", encoding="utf-8") as handle:
            text = handle.read()
    record = None
    if os.path.exists(records):
        with open(records, "r", encoding="utf-8") as handle:
            record = json.load(handle)
    if record is not None:
        # The RC-002-F1-R2 invariant, checked on every case that reaches a
        # record rather than on the one fixture that exposed it: the distinct
        # bytes the processed read actually touched must be inside what its plan
        # said they could be. The defect that closed that card was a single read
        # placed after the ceiling was enforced, and no case in this suite was
        # looking for it. The comparison is against the union of touched ranges
        # and not against io["bytes"], because the local reader has no cache and
        # counts a re-read twice while the bound is on distinct bytes.
        planned = (record.get("plan") or {}).get("cache_bound_bytes")
        touched = distinct_bytes(processed_path)
        if planned is not None:
            if not touched:
                raise AssertionError(
                    "case %r matched no reader against %s, so the transfer invariant "
                    "checked nothing. A check that cannot fail is not a check."
                    % (name, processed_path))
            if touched > planned:
                raise AssertionError(
                    "case %r touched %d distinct bytes of the processed asset against a "
                    "planned bound of %d. A read the plan does not cover is the defect "
                    "class that closed RC-002, and it fails here rather than in review."
                    % (name, touched, planned))
        # The RC-003-F3 invariant, on every case that reaches a record and on
        # both assets: what each provenance read asked for and what it actually
        # transferred must both be inside the budget the command published for
        # it. The first number was already bounded; the second is the one whose
        # bound was stated and not enforced, because the reader fetches whole
        # blocks and a request is not the transfer that serves it.
        for label, spend in (record.get("provenance_io") or {}).items():
            if spend["read_bytes"] > spend["read_budget_bytes"]:
                raise AssertionError(
                    "case %r asked for %d bytes of %s provenance against a published "
                    "budget of %d." % (name, spend["read_bytes"], label,
                                       spend["read_budget_bytes"]))
            if spend["transfer_bytes"] > spend["transfer_budget_bytes"]:
                raise AssertionError(
                    "case %r transferred %d distinct bytes reading %s provenance "
                    "against a published budget of %d. A budget on the request is not "
                    "a budget on the transfer, and this is where the difference fails."
                    % (name, spend["transfer_bytes"], label,
                       spend["transfer_budget_bytes"]))
    return {"status": status, "out": out, "text": text, "record": record,
            "stdout": transcript,
            "raw": raw_path, "processed": processed_path, "dir": case_dir}


def load_cli():
    """Import ``measure_host_drift.py`` from the packet's ``scripts/`` folder.

    The command lives in the packet because that is where the first real result
    has to be produced from. Importing it by path rather than by package is what
    lets this harness run it as a module while the packet's own ``scripts/``
    directory is on ``sys.path`` for its sibling imports.
    """
    path = os.path.join(PACKET_SCRIPTS, "measure_host_drift.py")
    spec = importlib.util.spec_from_file_location("measure_host_drift", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CLI = None


def case_clean_band_passes(h, tmp):
    """A quiet band passes both gate numbers and reports every required quantity."""
    rows = default_electrodes()
    lo, hi = band_bounds()
    units = band_units() + [out_of_band_unit()] + band_units(n_units=2, probe=PROBES[1],
                                                             seed0=300)
    result = run_case(
        tmp, "clean_band_passes",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    h.equal("clean/status", result["status"], 0)
    record = result["record"]
    h.check("clean/report written", result["text"] is not None)
    h.equal("clean/verdict passed", record["verdict"]["passed"], True)
    h.equal("clean/n_bins", record["grid"]["n_bins"], 15)
    h.close("clean/discarded_s", record["grid"]["discarded_s"], 0.0, 1e-9)
    h.equal("clean/in-band count", record["sets"]["in_band"]["n_total"], 8)
    h.equal("clean/units on probe", record["n_units_on_probe"], 9)
    h.equal("clean/included count", record["sets"]["included"]["n_total"], 8)
    h.equal("clean/audit rows", len(record["audit"]), 8)
    h.check("clean/delta below gate",
            record["observed"]["delta_window"] <= record["threshold_um"])
    h.check("clean/q95 below gate", record["null"]["q95"] <= record["threshold_um"])
    h.equal("clean/replay", record["checks"]["replay"],
            "identical over 200 replicates")
    h.equal("clean/threshold", record["threshold_um"], 20.0)
    h.check("clean/io bytes counted", record["io"]["bytes"] > 0)
    h.check("clean/report names Delta_10min", "Delta_10min" in result["text"])
    h.check("clean/report names the boundary",
            "neither bounds" in result["text"])


def case_labels_recorded_not_filtered(h, tmp):
    """Non-``good`` units are in the band set, and the labels are recorded."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "labels_recorded",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    record = result["record"]
    h.equal("labels/status", result["status"], 0)
    h.equal("labels/in-band total", record["sets"]["in_band"]["n_total"], 8)
    h.check("labels/good is a minority", record["sets"]["in_band"]["n_good"] < 8)
    h.equal("labels/labels recorded", len(record["sets"]["in_band"]["labels"]), 8)
    h.check("labels/non-good present",
            any(label != "good" for label in record["sets"]["in_band"]["labels"]))
    h.check("labels/rows are units-table rows",
            record["sets"]["in_band"]["rows"] == list(range(8)))


def case_common_ramp_fails_strict_passes_relaxed(h, tmp):
    """A 27 um common ramp fails at one row and passes at the declared two."""
    rows = default_electrodes()
    units = band_units(ramp_um_per_min=2.7)
    strict = run_case(
        tmp, "ramp_strict",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units), gate="strict")
    relaxed = run_case(
        tmp, "ramp_relaxed",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units), gate="relaxed")
    h.equal("ramp/strict status", strict["status"], 0)
    h.equal("ramp/strict fails", strict["record"]["verdict"]["passed"], False)
    h.equal("ramp/strict label", strict["record"]["verdict"]["label"], "resolved drift")
    h.close("ramp/strict delta", strict["record"]["observed"]["delta_window"], 27.0, 2.0)
    h.equal("ramp/relaxed threshold", relaxed["record"]["threshold_um"], 40.0)
    h.equal("ramp/relaxed passes", relaxed["record"]["verdict"]["passed"], True)
    h.equal("ramp/same observed value",
            strict["record"]["observed"]["delta_window"],
            relaxed["record"]["observed"]["delta_window"])


def case_plan_only_reads_no_spikes(h, tmp):
    """``--plan-only`` reports the exact byte cost and writes no report."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "plan_only",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units), argv_extra=["--plan-only"])
    h.equal("plan/status", result["status"], 0)
    h.check("plan/no report", result["text"] is None)
    h.check("plan/no record", result["record"] is None)


def case_plan_bytes_follow_stored_itemsize(h, tmp):
    """The planned byte count is the file's own item sizes, not an assumption."""
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    spikes = sum(len(u["times"]) for u in units)
    for dtype, per_spike, tag in ((np.float64, 16, "f8"), (np.float32, 12, "f4")):
        path_dir = os.path.join(tmp, "itemsize_%s" % tag)
        os.makedirs(path_dir, exist_ok=True)
        processed = os.path.join(path_dir, "processed.nwb")
        write_processed(processed, rows, units, depth_dtype=dtype)
        read = archive_units.read_band_units(processed, os.path.getsize(processed),
                                             1024 * 1024, PROBES[0], lo, hi,
                                             plan_only=True)
        h.equal("plan/%s spikes" % tag, read["plan"]["n_spikes"], spikes)
        h.equal("plan/%s logical bytes" % tag, read["plan"]["logical_bytes"],
                spikes * per_spike)


def case_transfer_ceiling_refuses(h, tmp):
    """A band larger than the declared ceiling stops before any spike is read.

    The ceiling is enforced twice and this case is the later one: a value that
    admits the whole of preflight and is still below the plan's combined peak,
    so what refuses is the plan check rather than the transfer budget the
    ceiling is also held open as. ``case_ceiling_refuses_before_the_bytes_move``
    is the earlier one.
    """
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "ceiling",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units),
        argv_extra=["--max-mib", "0.1"])
    h.check("ceiling/refused", "above the declared ceiling" in str(result["status"]),
            str(result["status"]))
    h.check("ceiling/refused by the plan not by the budget",
            "declared ceiling transfer budget" not in str(result["status"]),
            str(result["status"]))
    h.check("ceiling/no report", result["text"] is None)


def case_ceiling_refuses_before_the_bytes_move(h, tmp):
    """The declared ceiling refuses a fetch rather than reporting one.

    RC-003-F3 is why the ceiling is held open at all: it used to be checked
    once, against a plan written after preflight had already read the electrode
    table, the unit scalars, the descriptions and the provenance. Those reads
    are counted -- they land in ``spent_bytes`` and so inside the plan -- but
    counted is not refused, which is the distinction the whole finding turns on.

    **RC-004-F2 moved which asset this case meets first, and that is the point
    of the change rather than an accident of it.** The raw asset's provenance
    and clock read used to sit outside the ceiling entirely: at a one-byte
    ceiling the reviewer measured 23,920 distinct raw bytes moving, and the
    declared reference time being read and printed, before the processed side
    refused anything. The ceiling now covers that read too, so the run stops on
    the raw asset with nothing fetched from either file. Codex's Round-1 F2
    asked for exactly this: proof that the raw reference value is neither read
    nor printed before a below-minimum ceiling stops the command.

    The processed read's own before-the-first-fetch refusal is not lost with
    it -- no whole-command ceiling can admit the raw asset's ten kilobytes and
    still refuse the processed asset's first eight bytes -- so it is asserted
    directly against the reader in
    ``case_the_processed_ceiling_still_refuses_before_its_first_fetch``.
    """
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "ceiling_early",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units),
        argv_extra=["--max-mib", "0.000001"], capture=True)
    status = str(result["status"])
    h.check("ceiling_early/refused", "declared ceiling transfer budget" in status, status)
    h.check("ceiling_early/named as an input error", "input error" in status, status)
    h.check("ceiling_early/names the raw asset", "_desc-raw" in status, status)
    h.equal("ceiling_early/nothing_moved", distinct_bytes(result["processed"]), 0)
    h.equal("ceiling_early/nothing_moved_on_the_raw_asset",
            distinct_bytes(result["raw"]), 0)
    # Not read is the stronger claim and the byte count above carries it; this
    # is the one Codex asked for by name, and it guards the transcript against
    # a later change that prints a declared value from somewhere else.
    h.check("ceiling_early/the raw clock is not printed",
            result["stdout"] is not None
            and "counts its times from" not in result["stdout"],
            repr(result["stdout"]))
    h.check("ceiling_early/no report", result["text"] is None)


def case_the_processed_ceiling_still_refuses_before_its_first_fetch(h, tmp):
    """RC-003-F3's property, asserted where it lives now that F2 moved the order.

    ``read_band_units`` enters the caller's ceiling before it opens the file, so
    a ceiling below the first fetch refuses with **zero distinct bytes
    transferred** rather than reporting a spend afterwards. The whole-command
    case that used to assert this now stops on the raw asset first, because
    RC-004-F2 put that read inside the same ceiling; the property did not
    change and this is where it is checked.
    """
    rows = default_electrodes()
    units = band_units()
    case_dir = os.path.join(tmp, "processed_ceiling")
    os.makedirs(case_dir, exist_ok=True)
    path = os.path.join(case_dir, "processed.nwb")
    write_processed(path, rows, units)
    lo, hi = band_bounds()
    del READERS[:]
    refusal = None
    try:
        archive_units.read_band_units(path, os.path.getsize(path), 1024 * 1024,
                                      PROBES[0], lo, hi, max_bytes=1,
                                      plan_only=True)
    except Exception as exc:  # the exception type is what is asserted below
        refusal = exc
    h.check("processed_ceiling/refused", refusal is not None,
            "a 1-byte ceiling admitted the read")
    h.check("processed_ceiling/refused by the budget and not by something else",
            isinstance(refusal, archive_units.ReadBudgetExceeded), repr(refusal))
    h.equal("processed_ceiling/named the refusing scope",
            getattr(refusal, "scope", None), archive_units.PREFLIGHT_SCOPE)
    h.equal("processed_ceiling/nothing_moved", distinct_bytes(path), 0)
    del READERS[:]


def case_a_non_iso_separator_is_an_input_error(h, tmp):
    """A value the parser accepts and ISO-8601 does not is refused, RC-004-F1.

    ``datetime.fromisoformat`` permits any single character where ISO-8601 puts
    ``T``, so ``2021-05-10Q14:33:49.023776-04:00`` parsed, carried an offset,
    agreed with the identical value on the other asset, and reached a drift
    verdict with a report and a record. NWB states this field as an ISO-8601
    timestamp; a value that is not one is a malformed input, and the two assets
    agreeing about a malformed value is not evidence that they share a clock.

    **Both halves carry the same bad value on purpose.** A fixture that spoiled
    only one would be refused by the pair comparison and would say nothing about
    the grammar; this one is admitted by every rule except the one under test.
    """
    rows = default_electrodes()
    units = band_units()
    separator = "2021-05-10Q14:33:49.023776-04:00"
    h.check("non_iso/fixture parses without the grammar",
            datetime.datetime.fromisoformat(separator).utcoffset() is not None,
            "the fixture must be one the parser accepts, or it tests nothing")
    h.check("non_iso/the grammar refuses it",
            archive_units.reference_instant(separator) is None, separator)
    result = run_case(
        tmp, "non_iso",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S, reference_time=separator),
        lambda p: write_processed(p, rows, units, reference_time=separator))
    status = str(result["status"])
    h.check("non_iso/refused", "is not an ISO-8601 timestamp" in status, status)
    h.check("non_iso/named as an input error", "input error" in status, status)
    h.check("non_iso/quotes the value", separator in status, status)
    h.check("non_iso/names the raw asset as the one at fault",
            "raw asset" in status, status)
    h.check("non_iso/states the form required",
            archive_units.REFERENCE_TIME_FORM_TEXT in status, status)
    h.check("non_iso/no report", result["text"] is None)
    h.check("non_iso/no record", result["record"] is None)
    # The adversarial near misses, at the API rather than through the command,
    # because the command costs a fixture pair each and the rule is one function.
    # Each is a value the parser would take and ISO-8601 does not.
    for near in ("2021-05-10 14:33:49.023776-04:00",
                 "2021-05-10t14:33:49.023776-04:00",
                 "2021-05-10_14:33:49.023776-04:00",
                 "2021-05-10T14:33:49.023776-0400",
                 "2021-05-10T14:33:49.023776-04:00 (US/Eastern)",
                 "session start 2021-05-10T14:33:49.023776-04:00"):
        h.check("non_iso/near miss refused %s" % near,
                archive_units.reference_instant(near) is None, near)
    # And the mirror, which is the direction this whole card was opened in:
    # the tightening must not refuse legitimate ISO-8601 spellings.
    for good in ("2021-05-10T14:33:49.023776-04:00",
                 "2021-05-10T18:33:49.023776+00:00",
                 "2021-05-10T18:33:49Z",
                 "2021-05-10T18:33:49.5+00:00",
                 "2021-05-10T18:33+00:00",
                 "2021-05-10T18:33:49+00",
                 "  2021-05-10T18:33:49+00:00  "):
        h.check("non_iso/still admitted %s" % good,
                archive_units.reference_instant(good) is not None, good)
    # A value the grammar admits and the calendar does not is still refused,
    # because the grammar bounds the shape and the parser validates the values.
    for impossible in ("2021-13-10T14:33:49-04:00", "2021-05-10T25:33:49-04:00",
                       "2021-02-31T14:33:49-04:00"):
        h.check("non_iso/impossible date refused %s" % impossible,
                archive_units.reference_instant(impossible) is None, impossible)


def case_the_grammar_admits_every_measured_reference_time(h, tmp):
    """The tightened grammar admits all 142 assets this dandiset really carries.

    **This is the case RC-004 exists to have.** The rule this card replaced was
    correct, well-tested, adversarially reviewed across three rounds, defended
    by twenty-six mutations -- and admitted 0 of the 71 sessions it would ever
    see, because every check it passed ran on fixtures we wrote. RC-004-F1's
    repair is a *tightening* of the field that replaced it, which is the change
    that can empty a population, so the repair is measured against the real one
    rather than argued about.

    ``MEASURED_REFERENCE_TIMES`` is the frozen census; see its comment for where
    it came from. Nothing here reads the archive.
    """
    h.equal("measured_grammar/the census is the size it says it is",
            len(MEASURED_REFERENCE_TIMES), 79)
    refused = [value for value in MEASURED_REFERENCE_TIMES
               if archive_units.reference_instant(value) is None]
    h.equal("measured_grammar/none of the measured values is refused", refused, [])
    aware = [value for value in MEASURED_REFERENCE_TIMES
             if archive_units.reference_instant(value).utcoffset() is not None]
    h.equal("measured_grammar/every admitted value is an instant",
            len(aware), len(MEASURED_REFERENCE_TIMES))
    # The four lexical shapes the census found, counted here so a later change
    # to this list is visible as a change to what the population contains
    # rather than as a silently different set of the same size.
    shapes = {}
    for value in MEASURED_REFERENCE_TIMES:
        key = re.sub(r"[0-9]", "9", value)
        shapes[key] = shapes.get(key, 0) + 1
    h.equal("measured_grammar/the four measured shapes", shapes, {
        "9999-99-99T99:99:99+99:99": 9,
        "9999-99-99T99:99:99-99:99": 22,
        "9999-99-99T99:99:99.999999+99:99": 19,
        "9999-99-99T99:99:99.999999-99:99": 29,
    })


def case_pre_origin_spikes_counted(h, tmp):
    """Spikes before session zero are counted and excluded, not dropped silently."""
    rows = default_electrodes()
    units = band_units(prepend_s=(-0.004, -0.003, -0.002))
    result = run_case(
        tmp, "pre_origin",
        lambda p: write_raw(p, rows, -0.005, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    record = result["record"]
    h.equal("pre_origin/status", result["status"], 0)
    h.equal("pre_origin/count is exact", record["grid"]["n_spikes_before_origin"],
            3 * record["sets"]["in_band"]["n_total"])
    h.equal("pre_origin/head_partial_s", record["grid"]["head_partial_s"], 0.0)
    h.check("pre_origin/report names them",
            "spikes before origin" in result["text"])


def case_head_partial_reported(h, tmp):
    """A stream starting after session zero reports its head undercoverage."""
    rows = default_electrodes()
    units = band_units(start_s=1.2)
    result = run_case(
        tmp, "head_partial",
        lambda p: write_raw(p, rows, 1.138489, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    record = result["record"]
    h.equal("head/status", result["status"], 0)
    h.close("head/head_partial_s", record["grid"]["head_partial_s"], 1.138489, 1e-9)
    h.equal("head/no pre-origin spikes", record["grid"]["n_spikes_before_origin"], 0)
    h.check("head/head slack non-negative", record["containment"]["head_slack_s"] >= 0)
    h.check("head/tail slack non-negative", record["containment"]["tail_slack_s"] >= 0)


def case_grid_extent_is_t_last(h, tmp):
    """The bin grid takes its length from ``t_last_s``, never from the span."""
    rows = default_electrodes()
    units = band_units(start_s=61.0)
    # t_last 900.0 with t_first 61.0: the span is 839 s, which would give 13
    # bins, while the session-time extent gives 15. The estimator must see 15.
    result = run_case(
        tmp, "grid_extent",
        lambda p: write_raw(p, rows, 61.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    record = result["record"]
    h.equal("extent/status", result["status"], 0)
    h.equal("extent/n_bins from t_last", record["grid"]["n_bins"], 15)
    h.check("extent/span would differ",
            band_drift.complete_bins(EXTENT_S - 61.0)[0] == 13)


def case_audit_values_come_from_the_estimator(h, tmp):
    """The reported per-unit values match a direct call, not a second centring."""
    rows = default_electrodes()
    units = band_units(ramp_um_per_min=1.0)
    result = run_case(
        tmp, "audit_values",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    record = result["record"]
    h.equal("audit/status", result["status"], 0)
    observed = band_drift.measure_band_drift(
        [u["times"] for u in units], [u["depths"] for u in units], EXTENT_S)
    h.equal("audit/rows align", [entry["row"] for entry in record["audit"]],
            observed["included"])
    h.equal("audit/delta_full", [entry["delta_full"] for entry in record["audit"]],
            observed["unit_delta_full"])
    h.equal("audit/own worst",
            [entry["delta_max_window"] for entry in record["audit"]],
            observed["unit_delta_max_window"])
    h.equal("audit/window start",
            [entry["max_window_start"] for entry in record["audit"]],
            observed["unit_max_window_start"])
    h.equal("audit/band window",
            [entry["delta_band_window"] for entry in record["audit"]],
            observed["unit_delta_band_window"])
    h.check("audit/report says never consumed",
            "never consumed" in result["text"])


def case_too_few_units_is_unmeasurable(h, tmp):
    """Four in-band units make the candidate unmeasurable, not a pass."""
    rows = default_electrodes()
    units = band_units(n_units=4)
    result = run_case(
        tmp, "too_few_units",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    record = result["record"]
    h.equal("few/status", result["status"], 0)
    h.equal("few/measurable", record["observed"].get("measurable"), False)
    h.equal("few/verdict passed", record["verdict"]["passed"], False)
    h.equal("few/label", record["verdict"]["label"], "unmeasurable")
    h.equal("few/no null", record["null"], None)
    h.equal("few/no audit", record["audit"], [])


def case_invalid_bin_is_unmeasurable(h, tmp):
    """A bin holding too few defined medians rejects rather than being skipped."""
    rows = default_electrodes()
    units = band_units(n_units=5, gap_unit=2)
    result = run_case(
        tmp, "invalid_bin",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    record = result["record"]
    h.equal("invalid/status", result["status"], 0)
    h.equal("invalid/measurable", record["observed"].get("measurable"), False)
    h.check("invalid/reason names bins", "bins" in record["observed"].get("reason", ""))
    h.equal("invalid/verdict", record["verdict"]["passed"], False)


def case_repeat_run_is_identical(h, tmp):
    """The whole command is deterministic: two runs write the same report."""
    rows = default_electrodes()
    units = band_units()
    first = run_case(
        tmp, "determinism_a",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units), session="determinism")
    second = run_case(
        tmp, "determinism_b",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units), session="determinism")
    h.equal("determinism/status", (first["status"], second["status"]), (0, 0))
    h.equal("determinism/identical report", first["text"], second["text"])
    h.equal("determinism/identical null",
            first["record"]["null"]["values"], second["record"]["null"]["values"])


def case_ragged_indices_must_agree(h, tmp):
    """Two ragged columns cut differently is an input error, not a drift result."""
    rows = default_electrodes()
    units = band_units()

    def mutate(times_index, depths_index):
        shifted = list(depths_index)
        shifted[0] += 1
        return times_index, shifted

    result = run_case(
        tmp, "ragged_disagree",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units, index_mutator=mutate))
    h.check("ragged/refused", "first disagree at unit 0" in str(result["status"]),
            str(result["status"]))
    h.check("ragged/named as input error", "input error" in str(result["status"]))
    h.check("ragged/no report", result["text"] is None)


def case_ragged_index_must_end_at_column_length(h, tmp):
    """A truncated index is refused rather than quietly dropping spikes."""
    rows = default_electrodes()
    units = band_units()

    def mutate(times_index, depths_index):
        shortened_t = list(times_index)
        shortened_d = list(depths_index)
        shortened_t[-1] -= 5
        shortened_d[-1] -= 5
        return shortened_t, shortened_d

    result = run_case(
        tmp, "ragged_truncated",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units, index_mutator=mutate))
    h.check("truncated/refused", "ends at" in str(result["status"]),
            str(result["status"]))
    h.check("truncated/no report", result["text"] is None)


def _nan_at(units, positions):
    """Copy a unit list and set NaN depths at explicit (unit, index) positions.

    Positions are stated rather than drawn, because a fixture that hopes a random
    draw lands where the check needs it is a fixture that can silently stop
    testing what it was written for.

    Args:
        units: unit dicts from :func:`band_units`.
        positions: iterable of ``(unit_index, spike_index)`` pairs.

    Returns:
        The same list, with the touched units' depth arrays replaced by copies.
    """
    touched = set(unit_index for unit_index, _ in positions)
    for unit_index in touched:
        units[unit_index]["depths"] = units[unit_index]["depths"].copy()
    for unit_index, spike_index in positions:
        units[unit_index]["depths"][spike_index] = np.nan
    return units


def case_infinite_depth_is_refused(h, tmp):
    """An infinite depth stops the command, on either sign.

    NaN and infinity are different failures of the same column. An infinity is a
    wrong value rather than an absent one, so widening a bound around it would
    turn corruption into uncertainty; it stays an input error.
    """
    rows = default_electrodes()
    for name, value in (("plus", np.inf), ("minus", -np.inf)):
        units = band_units()
        units[1]["depths"] = units[1]["depths"].copy()
        units[1]["depths"][7] = value
        result = run_case(
            tmp, "infinite_depth_%s" % name,
            lambda p: write_raw(p, rows, 0.0, EXTENT_S),
            lambda p: write_processed(p, rows, units))
        h.check("infinite/%s refused" % name,
                "infinite spike depths" in str(result["status"]),
                str(result["status"]))
        h.check("infinite/%s named as input error" % name,
                "input error" in str(result["status"]), str(result["status"]))
        h.check("infinite/%s no report" % name, result["text"] is None)


def case_missing_depth_is_bounded_rather_than_refused(h, tmp):
    """A NaN depth is measured with a bound around it, not refused.

    This is the whole-command half of the recovery: the record reaches a verdict,
    the exclusions are published three ways, and both of the gate's numbers carry
    an interval over every completion of the missing values.
    """
    rows = default_electrodes()
    # Three per unit across all eight, at spread positions, so the bound is
    # non-degenerate on both of the gate's numbers rather than only present.
    positions = [(unit, index) for unit in range(8) for index in (17, 190, 401)]
    units = _nan_at(band_units(), positions)
    result = run_case(
        tmp, "missing_depth_bounded",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    h.equal("missing/status", result["status"], 0)
    h.check("missing/report written", result["text"] is not None)
    if result["text"] is None or result["record"] is None:
        return
    text = result["text"]
    record = result["record"]
    missing = record["missing_depth"]
    h.check("missing/report has the section",
            "## Missing depths and the completion bound" in text)
    h.equal("missing/total counted", missing["n_missing"], len(positions))
    h.equal("missing/units affected", missing["n_units_affected"], 8)
    h.equal("missing/per-unit sums to the total",
            sum(entry["n_missing"] for entry in missing["per_unit"]),
            missing["n_missing"])
    h.equal("missing/per-bin sums to the gridded total",
            sum(entry["n_missing"] for entry in missing["per_bin"]),
            missing["n_missing"] - missing["outside_grid"])
    h.equal("missing/triples sum to the gridded total",
            sum(triple[2] for triple in missing["per_unit_bin"]),
            missing["n_missing"] - missing["outside_grid"])
    h.check("missing/support invariance holds", missing["support"]["invariant"],
            str(missing["support"].get("reason")))
    bounds = missing["bounds"]
    h.check("missing/bounds measurable", bounds.get("measurable"),
            str(bounds.get("reason")))
    if not bounds.get("measurable"):
        return
    point = record["observed"]["delta_window"]
    h.check("missing/point inside its own bound",
            bounds["delta_window_lo"] <= point <= bounds["delta_window_hi"],
            "%r not in [%r, %r]" % (point, bounds["delta_window_lo"],
                                    bounds["delta_window_hi"]))
    # Strictly wider on both sides, because a bound that collapses onto the
    # point would make every check above pass without the layer doing anything.
    h.check("missing/bound is strictly two-sided",
            bounds["delta_window_lo"] < point < bounds["delta_window_hi"],
            "%r against [%r, %r]" % (point, bounds["delta_window_lo"],
                                     bounds["delta_window_hi"]))
    null_bounds = missing["null_bounds"]
    h.check("missing/null bound present", null_bounds is not None)
    if null_bounds is not None:
        h.check("missing/null bound is strictly two-sided",
                null_bounds["q95_lo"] < null_bounds["q95_hi"],
                "[%r, %r]" % (null_bounds["q95_lo"], null_bounds["q95_hi"]))
        h.equal("missing/null bound replicate count",
                null_bounds["n_permutations"], record["null"]["n_permutations"])
        h.check("missing/report states the null bound",
                "Q95_null bound" in text)
    h.check("missing/disposition is one of the four",
            missing["stability"]["disposition"]
            in ("passes", "fails", "decision-unstable", "unmeasurable"),
            missing["stability"]["disposition"])
    h.check("missing/report carries the per-unit table",
            "per-unit exclusions" in text and "per-bin exclusions" in text)
    h.check("missing/report says where the bound is exact",
            "Above the bin it is an OUTER bound" in text)
    h.check("missing/report says the finite-only null is not a completion",
            "is NOT one of those completions" in text)
    disposition = record["disposition"]
    h.check("missing/final disposition recorded",
            disposition["disposition"] in ("passes", "fails", "unmeasurable"),
            disposition["disposition"])
    h.equal("missing/advances only on passes", disposition["advances"],
            disposition["disposition"] == "passes")
    h.check("missing/report carries the final disposition",
            "final disposition" in text)


def case_missing_depths_can_pause_a_passing_gate(h, tmp):
    """The layer can flip a passing gate to unmeasurable, and does here.

    Without a case in this direction every command-level check above would pass
    on a fixture where the layer changed nothing, which is the failure mode of a
    check that cannot fail. Twenty-five of one bin's thirty depths are dropped,
    which leaves that bin below the ten-spike floor on the finite record and
    above it on every completion -- a support-invariance violation, which is
    unmeasurable by declaration rather than by a fitted number.
    """
    rows = default_electrodes()
    units = band_units()
    times = units[2]["times"]
    in_bin = np.flatnonzero((times >= 300.0) & (times < 360.0))
    if in_bin.size < 26:
        h.check("pause/fixture has a full bin", False,
                "bin 5 of unit 2 holds only %d spikes" % in_bin.size)
        return
    units = _nan_at(units, [(2, int(index)) for index in in_bin[:in_bin.size - 5]])
    result = run_case(
        tmp, "missing_depth_pauses",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    h.equal("pause/status", result["status"], 0)
    if result["record"] is None:
        h.check("pause/record written", False)
        return
    record = result["record"]
    missing = record["missing_depth"]
    h.check("pause/support invariance violated",
            not missing["support"]["invariant"])
    h.check("pause/violation is reported by unit and bin",
            missing["support"]["n_bin_mismatches"] > 0,
            str(missing["support"]["n_bin_mismatches"]))
    h.equal("pause/completion disposition", missing["stability"]["disposition"],
            "unmeasurable")
    h.check("pause/no null bound was built", missing["null_bounds"] is None)
    h.equal("pause/final disposition", record["disposition"]["disposition"],
            "unmeasurable")
    h.equal("pause/does not advance", record["disposition"]["advances"], False)
    h.check("pause/the gate itself had passed", record["verdict"]["passed"],
            "the fixture no longer isolates the layer's effect: the gate failed too")
    h.check("pause/report names the violation",
            "VIOLATED" in (result["text"] or ""))


def case_no_missing_depth_skips_the_layer(h, tmp):
    """With nothing missing the layer is not run, and the report says so.

    Its bounds collapse onto the gate's own two numbers when no depth is missing,
    so running it would double the most expensive step of the run to reproduce
    values already in hand. The collapse itself is proved elementwise in
    ``test_missing_depth.py``; what this case checks is that the command skips
    the work and states that it did.
    """
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "no_missing_depth",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    h.equal("clean/status", result["status"], 0)
    if result["record"] is None:
        h.check("clean/record written", False)
        return
    record = result["record"]
    missing = record["missing_depth"]
    h.equal("clean/nothing missing", missing["n_missing"], 0)
    h.equal("clean/no unit affected", missing["n_units_affected"], 0)
    h.check("clean/no bounds computed", missing["bounds"] is None)
    h.check("clean/no null bound computed", missing["null_bounds"] is None)
    h.check("clean/no stability verdict", missing["stability"] is None)
    h.check("clean/report says the layer did not run",
            "the sensitivity layer was not run" in (result["text"] or ""))
    h.equal("clean/disposition follows the gate",
            record["disposition"]["disposition"],
            "passes" if record["verdict"]["passed"] else "fails")
    h.check("clean/disposition says why it is completion-independent",
            "no depth was missing" in record["disposition"]["reason"])
    h.equal("clean/no conflict is possible", record["disposition"]["conflict"], False)


def case_unsorted_times_are_refused(h, tmp):
    """Descending spike times are refused, because the binning assumes order."""
    rows = default_electrodes()
    units = band_units()
    units[0]["times"] = units[0]["times"].copy()
    units[0]["times"][5], units[0]["times"][6] = (units[0]["times"][6],
                                                  units[0]["times"][5])
    result = run_case(
        tmp, "unsorted_times",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    h.check("unsorted/refused", "not ascending" in str(result["status"]),
            str(result["status"]))
    h.check("unsorted/no report", result["text"] is None)


def case_depth_unit_must_be_stated(h, tmp):
    """A depth column that no longer states micrometres is refused."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "depth_unit",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units,
                                  depth_description="Distance from the probe tip."))
    h.check("depth_unit/refused", "does not state its unit" in str(result["status"]),
            str(result["status"]))
    h.check("depth_unit/no report", result["text"] is None)


def case_out_of_range_electrode_is_refused(h, tmp):
    """A max_electrode outside the table is an input error."""
    rows = default_electrodes()
    units = band_units()
    units[3] = dict(units[3])
    units[3]["max_electrode"] = 10_000
    result = run_case(
        tmp, "electrode_range",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    h.check("electrode_range/refused", "outside an electrode table" in str(result["status"]),
            str(result["status"]))
    h.check("electrode_range/no report", result["text"] is None)


def case_cross_probe_electrode_is_refused(h, tmp):
    """A unit whose peak electrode belongs to the other probe is an input error."""
    rows = default_electrodes()
    units = band_units()
    units[2] = dict(units[2])
    units[2]["max_electrode"] = N_ROWS_PER_PROBE + BAND_ROW_LO
    result = run_case(
        tmp, "cross_probe",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    h.check("cross_probe/refused", "belongs to probe" in str(result["status"]),
            str(result["status"]))
    h.check("cross_probe/no report", result["text"] is None)


def case_electrode_tables_must_agree(h, tmp):
    """A processed table that differs from the raw one is an input error."""
    raw_rows = default_electrodes()
    processed_rows = [dict(row) for row in raw_rows]
    processed_rows[BAND_ROW_LO + 1]["rel_y"] += 5.0
    units = band_units()
    result = run_case(
        tmp, "tables_disagree",
        lambda p: write_raw(p, raw_rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, processed_rows, units))
    h.check("tables/refused", "electrode tables disagree" in str(result["status"]),
            str(result["status"]))
    h.check("tables/no report", result["text"] is None)


def case_missing_timestamps_is_refused(h, tmp):
    """An AP series without aligned timestamps is an input error, not a rejection."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "no_timestamps",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S, timing_source="starting_time"),
        lambda p: write_processed(p, rows, units))
    h.check("timestamps/refused", "rather than aligned" in str(result["status"]),
            str(result["status"]))
    h.check("timestamps/named as input error", "input error" in str(result["status"]))
    h.check("timestamps/no report", result["text"] is None)


def case_containment_violation_is_refused(h, tmp):
    """A spike past the raw stream's last timestamp stops the command."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "containment",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S - 30.0),
        lambda p: write_processed(p, rows, units))
    h.check("containment/refused", "outside the raw AP interval" in str(result["status"]),
            str(result["status"]))
    h.check("containment/no report", result["text"] is None)


def case_unknown_probe_is_refused(h, tmp):
    """Asking for a probe the file does not carry stops the command."""
    rows = default_electrodes()
    units = band_units()
    case_dir = os.path.join(tmp, "unknown_probe")
    os.makedirs(case_dir, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    write_raw(raw_path, rows, 0.0, EXTENT_S)
    write_processed(processed_path, rows, units)
    unknown = session_id("unknown")
    install_local_assets([(unknown, raw_path, processed_path)])
    out = os.path.join(case_dir, "report.txt")
    try:
        status = CLI.main(["--session", unknown, "--probe", "Probe07",
                           "--target", TARGET, "--assets-cache",
                           os.path.join(case_dir, "assets.json"), "--out", out])
    except SystemExit as exc:
        status = str(exc.code)
    h.check("unknown_probe/refused", "no probe" in str(status), str(status))
    h.check("unknown_probe/no report", not os.path.exists(out))


def case_series_name_containing_the_probe_is_not_ownership(h, tmp):
    """A different probe's stream cannot supply this probe's clock, RC-003-F2.

    ``select_ap_series`` matched on ``probe in entry["name"]``. Asked for
    ``Probe00``, a file carrying ``ElectricalSeriesProbe000AP`` and
    ``ElectricalSeriesProbe01AP`` selected the first one and reached a passing
    verdict on a clock that belongs to a different probe. Nothing about that
    file is malformed -- the substring rule is what is wrong -- so it is a
    fixture rather than a mutation. The name is now decomposed and the probe
    token has to match exactly, so this file has *no* series for ``Probe00``
    and stops as an input error.
    """
    rows = default_electrodes()
    units = band_units()
    names = ["ElectricalSeriesProbe000AP", "ElectricalSeriesProbe01AP"]
    result = run_case(
        tmp, "impostor_series",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S, series_names=names),
        lambda p: write_processed(p, rows, units))
    h.check("impostor/refused", "belong to probe" in str(result["status"]),
            str(result["status"]))
    h.check("impostor/names the decomposition", "Probe000" in str(result["status"]),
            str(result["status"]))
    h.check("impostor/not a drift rejection",
            "not a drift rejection" in str(result["status"]), str(result["status"]))
    h.check("impostor/no report", result["text"] is None)
    h.check("impostor/no record", result["record"] is None)


def case_exact_series_ownership_still_selects(h, tmp):
    """The exact rule still finds each probe's own stream, on both probes.

    A tightening that refuses the impostor and also refuses the real thing would
    pass the case above and stop every candidate. The clean fixture's two names
    are the two the thirteen pinned candidates actually carry.
    """
    h.equal("ownership/probe00", CLI.series_probe("ElectricalSeriesProbe00AP"), "Probe00")
    h.equal("ownership/probe01", CLI.series_probe("ElectricalSeriesProbe01AP"), "Probe01")
    h.equal("ownership/impostor", CLI.series_probe("ElectricalSeriesProbe000AP"), "Probe000")
    h.equal("ownership/lf_band", CLI.series_probe("ElectricalSeriesProbe00LF"), "Probe00")
    h.equal("ownership/undecomposable", CLI.series_probe("SomethingElse"), None)
    entries = [{"name": "ElectricalSeriesProbe00AP"}, {"name": "ElectricalSeriesProbe01AP"}]
    h.equal("ownership/selects_probe01",
            CLI.select_ap_series(entries, "Probe01")["name"], "ElectricalSeriesProbe01AP")


def case_missing_session_is_refused(h, tmp):
    """A session that resolves to no asset pair stops the command."""
    rows = default_electrodes()
    units = band_units()
    case_dir = os.path.join(tmp, "missing_session")
    os.makedirs(case_dir, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    write_raw(raw_path, rows, 0.0, EXTENT_S)
    write_processed(processed_path, rows, units)
    install_local_assets([(session_id("present"), raw_path, processed_path)])
    out = os.path.join(case_dir, "report.txt")
    try:
        status = CLI.main(["--session", session_id("absent"), "--probe", PROBES[0],
                           "--target", TARGET, "--assets-cache",
                           os.path.join(case_dir, "assets.json"), "--out", out])
    except SystemExit as exc:
        status = str(exc.code)
    h.check("missing_session/refused", "expected exactly one" in str(status), str(status))
    h.check("missing_session/no report", not os.path.exists(out))


def case_plan_only_transfers_less(h, tmp):
    """Planning genuinely avoids the spike data rather than reading it quietly."""
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    case_dir = os.path.join(tmp, "plan_transfer")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, units)
    size = os.path.getsize(processed)
    planned = archive_units.read_band_units(processed, size, 1024 * 1024, PROBES[0],
                                            lo, hi, plan_only=True)
    full = archive_units.read_band_units(processed, size, 1024 * 1024, PROBES[0], lo, hi)
    h.check("plan_transfer/plan reads less",
            planned["io"]["bytes"] < full["io"]["bytes"],
            "plan %d, full %d" % (planned["io"]["bytes"], full["io"]["bytes"]))
    h.check("plan_transfer/full covers the slices",
            full["io"]["bytes"] - planned["io"]["bytes"] >= planned["plan"]["logical_bytes"],
            "difference %d, planned %d"
            % (full["io"]["bytes"] - planned["io"]["bytes"],
               planned["plan"]["logical_bytes"]))
    h.check("plan_transfer/plan carries no arrays",
            all("times" not in unit for unit in planned["band_units"]))
    h.check("plan_transfer/full carries arrays",
            all(unit["times"].size for unit in full["band_units"]))


def case_band_edges_are_inclusive(h, tmp):
    """Units sitting exactly on either band edge are inside the band."""
    rows = default_electrodes()
    lo, hi = band_bounds()
    units = band_units(n_units=6)
    edge_low = dict(units[0])
    edge_low["max_electrode"] = BAND_ROW_LO
    edge_high = dict(units[1])
    edge_high["max_electrode"] = BAND_ROW_HI
    just_below = dict(units[2])
    just_below["max_electrode"] = BAND_ROW_LO - 1
    just_above = dict(units[3])
    just_above["max_electrode"] = BAND_ROW_HI + 1
    spec = [edge_low, edge_high, just_below, just_above]
    case_dir = os.path.join(tmp, "band_edges")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, spec)
    read = archive_units.read_band_units(processed, os.path.getsize(processed),
                                         1024 * 1024, PROBES[0], lo, hi, plan_only=True)
    h.equal("band_edges/two inside", read["plan"]["n_units"], 2)
    h.equal("band_edges/rows", [unit["row"] for unit in read["band_units"]], [0, 1])
    h.equal("band_edges/low edge depth", read["band_units"][0]["rel_y_um"], lo)
    h.equal("band_edges/high edge depth", read["band_units"][1]["rel_y_um"], hi)


def case_empty_unit_is_carried_not_included(h, tmp):
    """A band unit with no spikes is read, reported, and left out of the estimate."""
    rows = default_electrodes()
    units = band_units()
    empty = dict(units[0])
    empty["max_electrode"] = BAND_ROW_LO + 3
    empty["label"] = "mua"
    empty["times"] = np.zeros(0, dtype=np.float64)
    empty["depths"] = np.zeros(0, dtype=np.float64)
    result = run_case(
        tmp, "empty_unit",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units + [empty]))
    record = result["record"]
    h.equal("empty_unit/status", result["status"], 0)
    h.equal("empty_unit/in band", record["sets"]["in_band"]["n_total"], 9)
    h.equal("empty_unit/included", record["sets"]["included"]["n_total"], 8)
    h.check("empty_unit/empty row excluded",
            8 not in record["sets"]["included"]["rows"])
    h.equal("empty_unit/verdict", record["verdict"]["passed"], True)


def case_threshold_cannot_be_typed(h, tmp):
    """No command-line path exists to a threshold the project did not declare."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "typed_threshold",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units),
        argv_extra=["--threshold-um", "25"])
    h.equal("typed_threshold/rejected", str(result["status"]), "2")
    h.check("typed_threshold/no report", result["text"] is None)
    h.equal("typed_threshold/gate values",
            sorted(CLI.GATES), ["relaxed", "strict"])
    h.equal("typed_threshold/strict is one row",
            band_drift.PARAMS[CLI.GATES["strict"]], 20.0)
    h.equal("typed_threshold/relaxed is two rows",
            band_drift.PARAMS[CLI.GATES["relaxed"]], 40.0)


def case_report_is_ascii_and_complete(h, tmp):
    """The report prints only ASCII and carries every quantity the section requires."""
    rows = default_electrodes()
    units = band_units(ramp_um_per_min=0.5)
    result = run_case(
        tmp, "report_contents",
        lambda p: write_raw(p, rows, 0.4, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    text = result["text"] or ""
    h.equal("report/status", result["status"], 0)
    h.check("report/ascii only", all(ord(char) < 128 for char in text))
    for required in ("head endpoint slack", "tail endpoint slack", "n_bins",
                     "discarded_s", "head_partial_s", "spikes before origin",
                     "in-band rows and labels", "included rows and labels",
                     "Q95_null", "deterministic replay", "own_worst", "band_win",
                     "raw_provenance", "raw_electrodes", "raw_timing",
                     "processed_units"):
        h.check("report/carries %r" % required, required in text)
    h.check("report/sources are ascii",
            all(ord(char) < 128
                for path in (os.path.join(PACKET_SCRIPTS, "measure_host_drift.py"),
                             os.path.join(PACKET_SCRIPTS, "utils", "archive_units.py"))
                for char in io.open(path, encoding="utf-8").read()))


def case_io_counts_every_read(h, tmp):
    """The reported transfer is all four reads, not only the units table."""
    rows = default_electrodes()
    units = band_units()
    sources = ("raw_provenance", "raw_electrodes", "raw_timing", "processed_units")
    result = run_case(
        tmp, "io_counts",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    io_record = result["record"]["io"]
    h.equal("io/status", result["status"], 0)
    for source in sources:
        h.check("io/%s counted" % source, io_record[source]["bytes"] > 0)
        h.check("io/%s requested" % source, io_record[source]["requests"] > 0)
    h.equal("io/total bytes", io_record["bytes"],
            sum(io_record[source]["bytes"] for source in sources))
    h.equal("io/total requests", io_record["requests"],
            sum(io_record[source]["requests"] for source in sources))


def case_only_band_units_are_read(h, tmp):
    """Off-probe and out-of-band units cost nothing, which the plan proves."""
    rows = default_electrodes()
    lo, hi = band_bounds()
    inside = band_units(n_units=3)
    outside = [out_of_band_unit(seed=901)]
    other_probe = band_units(n_units=4, probe=PROBES[1], seed0=400)
    case_dir = os.path.join(tmp, "only_band")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, inside + outside + other_probe)
    read = archive_units.read_band_units(processed, os.path.getsize(processed),
                                         1024 * 1024, PROBES[0], lo, hi, plan_only=True)
    h.equal("only_band/units planned", read["plan"]["n_units"], 3)
    h.equal("only_band/spikes planned", read["plan"]["n_spikes"],
            sum(len(unit["times"]) for unit in inside))
    h.equal("only_band/units on probe", read["n_units_on_probe"], 4)
    h.equal("only_band/units in file", read["n_units_total"], 8)



def case_provenance_is_reported_verbatim(h, tmp):
    """Conversion provenance present on both assets is reported and recorded."""
    rows = default_electrodes()
    units = band_units()
    provenance = {
        "general/source_script": "Created using NeuroConv v0.9.2",
        "general/lab": "cortexlab",
        "general/institution": "test fixture",
    }
    result = run_case(
        tmp, "provenance",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units, provenance=provenance))
    record = result["record"]
    h.equal("provenance/status", result["status"], 0)
    for path, value in provenance.items():
        h.equal("provenance/%s" % path.rsplit("/", 1)[-1],
                record["provenance"].get(path), value)
        h.check("provenance/%s in report" % path.rsplit("/", 1)[-1],
                value in (result["text"] or ""))
    h.check("provenance/file_name attribute carried",
            record["provenance"].get("general/source_script@file_name")
            == "source_script.py")
    h.check("provenance/raw side recorded too",
            record["raw_provenance"].get("general/source_script")
            == DEFAULT_PROVENANCE["general/source_script"])
    # Two keys must not render to one label. They did: clipped to nine
    # characters, general/source_script and general/source_script@file_name
    # were both "source_sc", so the report showed two values under one name.
    text = result["text"] or ""
    for key in ("general/source_script", "general/source_script@file_name",
                "general/lab", "general/institution"):
        h.check("provenance/report names %s whole" % key, key in text)
    pair = record["provenance_authentication"]["pair"]
    h.equal("provenance/raw version parsed from the statement",
            pair["raw_version"], "0.9.2")
    h.equal("provenance/processed version parsed from the statement",
            pair["processed_version"], "0.9.2")
    h.check("provenance/versions are among the measured ones",
            pair["versions_are_measured"] is True, pair)
    h.check("provenance/instant agreement is what was enforced",
            pair["reference_instants_agree"] is True, pair)
    h.equal("provenance/instant delta is zero", pair["reference_delta_s"], 0.0)
    # The reference time is read under the same two budgets as the rest of the
    # provenance, which is what keeps its cost inside the plan rather than
    # beside it. The whole-suite invariant already compares both spends against
    # both budgets on every case that reaches a record; what this asserts is
    # that the value really was read here rather than assumed.
    for source in ("provenance", "raw_provenance"):
        h.equal("provenance/%s carries the reference time" % source,
                record[source].get(archive_units.REFERENCE_TIME_PATH),
                DEFAULT_REFERENCE_TIME)
    for half in ("raw", "processed"):
        auth = record["provenance_authentication"][half]
        h.equal("provenance/%s declared value recorded verbatim" % half,
                auth["reference_value"], DEFAULT_REFERENCE_TIME)
        h.equal("provenance/%s instant normalized to UTC" % half,
                auth["reference_instant_utc"], "2021-05-10T18:33:49.023776+00:00")
    h.check("provenance/report states the reference time",
            "session reference time" in text and DEFAULT_REFERENCE_TIME in text)
    for label in ("raw", "processed"):
        spend = record["provenance_io"][label]
        h.check("provenance/%s budgets are published" % label,
                spend["read_budget_bytes"] == archive_units.PROVENANCE_MAX_BYTES
                and spend["transfer_budget_bytes"] >= spend["read_budget_bytes"],
                spend)
        h.check("provenance/%s report states both budgets" % label,
                "%d of %d bytes requested" % (spend["read_bytes"],
                                              spend["read_budget_bytes"]) in text,
                spend)


def case_missing_processed_provenance_is_an_input_error(h, tmp):
    """A processed asset with no conversion provenance stops, RC-003-F1.

    The selection document says an asset whose conversion provenance and values
    do not establish the common session clock is an input error to resolve, not
    a drift rejection. The command recorded provenance and gated on none of it,
    so this fixture -- schema-valid, complete, and carrying no statement of what
    produced it -- reached ``passed=True`` with an empty provenance record. The
    session-time origin the grid is anchored on is a property of the converter,
    so an asset that names no converter cannot establish it.
    """
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "no_processed_provenance",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units, provenance={}))
    status = str(result["status"])
    h.check("no_processed_provenance/refused", "carries no general/source_script" in status,
            status)
    h.check("no_processed_provenance/named as an input error", "input error" in status,
            status)
    h.check("no_processed_provenance/no report", result["text"] is None)
    h.check("no_processed_provenance/no record", result["record"] is None)


def case_missing_raw_provenance_is_an_input_error(h, tmp):
    """The raw asset is authenticated too; it supplies the grid's extent."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "no_raw_provenance",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S, provenance={}),
        lambda p: write_processed(p, rows, units))
    status = str(result["status"])
    h.check("no_raw_provenance/refused", "carries no general/source_script" in status,
            status)
    h.check("no_raw_provenance/names the raw asset", "raw asset" in status, status)
    h.check("no_raw_provenance/no report", result["text"] is None)


def case_foreign_conversion_is_an_input_error(h, tmp):
    """Provenance that names a different toolchain is not the pinned one."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "foreign_conversion",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(
            p, rows, units,
            provenance={"general/source_script": "exported by a local script v3"}))
    status = str(result["status"])
    h.check("foreign_conversion/refused", "is not the conversion statement" in status,
            status)
    h.check("foreign_conversion/quotes the value", "local script v3" in status, status)
    h.check("foreign_conversion/no report", result["text"] is None)


def case_negated_conversion_statement_is_an_input_error(h, tmp):
    """A value that denies the toolchain contains its name, RC-003-F1 Round 2.

    The first repair required the case-insensitive substring ``neuroconv``
    anywhere in the value. ``This asset was NOT created using NeuroConv;
    exported by LocalTool v3`` contains it, so the search answered yes to a file
    that says no and the asset reached ``passed=True``. A token search is not
    authentication: the whole value is matched against the statement the
    measured assets carry, so what is confirmed is a positive claim rather than
    the presence of a word inside an arbitrary sentence.
    """
    rows = default_electrodes()
    units = band_units()
    denial = "This asset was NOT created using NeuroConv; exported by LocalTool v3"
    h.check("negated_conversion/fixture_contains_the_old_token",
            archive_units.CONVERSION_SOURCE_TOKEN in denial.lower(),
            "the construction is only a construction if the substring rule admits it")
    result = run_case(
        tmp, "negated_conversion",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units,
                                  provenance={"general/source_script": denial}))
    status = str(result["status"])
    h.check("negated_conversion/refused",
            "is not the conversion statement" in status, status)
    h.check("negated_conversion/named as an input error", "input error" in status, status)
    h.check("negated_conversion/quotes the value", "LocalTool v3" in status, status)
    h.check("negated_conversion/no report", result["text"] is None)
    h.check("negated_conversion/no record", result["record"] is None)


def case_unequal_conversion_versions_are_admitted(h, tmp):
    """Two converter versions on one session's two halves no longer stop the run.

    RC-004's controlling measurement: across 71 sessions of DANDI 000409 -- the
    11 distinct sessions of the pinned candidate order plus a deterministic
    60-session holdout drawn from the other 448 -- every raw asset was written
    by NeuroConv 0.9.1 or 0.9.2 and every processed asset by 0.9.4. Version
    equality agreed on **0 of 71**, so the rule that required it could not admit
    any candidate in this dandiset. This fixture is that real pair shape: two
    legitimate conversion statements naming different versions, with the two
    halves declaring the same session-time origin. It has to reach a verdict,
    and both versions have to survive into the record.
    """
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "version_pair_real_shape",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S,
                            provenance={"general/source_script":
                                        "Created using NeuroConv v0.9.2"}),
        lambda p: write_processed(p, rows, units,
                                  provenance={"general/source_script":
                                              "Created using NeuroConv v0.9.4"}))
    h.equal("version_pair/verdict reached", result["status"], 0)
    record = result["record"]
    pair = record["provenance_authentication"]["pair"]
    h.equal("version_pair/raw version recorded", pair["raw_version"], "0.9.2")
    h.equal("version_pair/processed version recorded", pair["processed_version"], "0.9.4")
    h.check("version_pair/disagreement is recorded, not enforced",
            pair["versions_agree"] is False, pair)
    h.check("version_pair/both versions are among the measured ones",
            pair["versions_are_measured"] is True, pair)
    h.check("version_pair/instants are what agreed",
            pair["reference_instants_agree"] is True, pair)
    text = result["text"] or ""
    for version in ("0.9.2", "0.9.4"):
        h.check("version_pair/report names version %s" % version, version in text)
    h.check("version_pair/report does not claim one version",
            "name one version" not in text, text[:0])


def case_one_instant_written_at_two_offsets_is_admitted(h, tmp):
    """The same instant declared at different UTC offsets passes the pair check.

    The comparison is on instants and not on strings, and this is the fixture
    that separates the two: ``2021-05-10T14:33:49.023776-04:00`` and
    ``2021-05-10T18:33:49.023776+00:00`` are different text and one point in
    time. A string comparison would call this a clock disagreement and pause a
    candidate that has none, which is the pessimistic mirror of the defect
    RC-004 exists to repair.
    """
    rows = default_electrodes()
    units = band_units()
    same_instant_utc = "2021-05-10T18:33:49.023776+00:00"
    h.check("offsets/fixture is two spellings of one instant",
            DEFAULT_REFERENCE_TIME != same_instant_utc
            and (archive_units.reference_instant(DEFAULT_REFERENCE_TIME)
                 == archive_units.reference_instant(same_instant_utc)),
            "%r against %r" % (DEFAULT_REFERENCE_TIME, same_instant_utc))
    result = run_case(
        tmp, "offset_spellings",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units, reference_time=same_instant_utc))
    h.equal("offsets/verdict reached", result["status"], 0)
    pair = result["record"]["provenance_authentication"]["pair"]
    h.equal("offsets/delta is zero", pair["reference_delta_s"], 0.0)
    h.equal("offsets/canonical instant is the UTC one",
            pair["reference_instant_utc"], same_instant_utc)
    auth = result["record"]["provenance_authentication"]
    h.equal("offsets/raw declared value kept verbatim",
            auth["raw"]["reference_value"], DEFAULT_REFERENCE_TIME)
    h.equal("offsets/processed declared value kept verbatim",
            auth["processed"]["reference_value"], same_instant_utc)


def case_reference_time_disagreement_is_an_input_error(h, tmp):
    """A one-hour difference in the declared origin stops the run.

    This is the defect the version proxy could not see. All eight disagreeing
    sessions in the 71-session measurement carry the *same* version pair as the
    sixty-three sound ones, and their declared instants differ by exactly
    +3,600 s. Every stored time in an NWB file is seconds counted from that
    instant, so the two halves are not on one coordinate -- and the raw asset
    supplies the grid's extent while the processed asset supplies the spikes.

    The disposition is Section 16.4's: an input error, which **pauses** the
    pinned order rather than rejecting the candidate.
    """
    rows = default_electrodes()
    units = band_units()
    shifted = "2021-05-10T15:33:49.023776-04:00"
    result = run_case(
        tmp, "reference_shift",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units, reference_time=shifted))
    status = str(result["status"])
    h.check("reference_shift/refused", "counts its times from" in status, status)
    h.check("reference_shift/names the difference", "+3600.000000 s" in status, status)
    h.check("reference_shift/quotes both values",
            DEFAULT_REFERENCE_TIME in status and shifted in status, status)
    h.check("reference_shift/named as an input error", "input error" in status, status)
    h.check("reference_shift/says it pauses rather than rejects",
            "pauses the pinned order" in status, status)
    h.check("reference_shift/no report", result["text"] is None)
    h.check("reference_shift/no record", result["record"] is None)


def case_the_pair_check_runs_before_the_payload(h, tmp):
    """A disagreeing pair is refused in preflight, not after the spikes are read.

    A pair check placed after the read would be correct and would cost the whole
    payload to reject the asset. This measures the difference directly: the
    distinct bytes touched on the refused fixture must stay below what the same
    fixture costs when it is read for a verdict.
    """
    rows = default_electrodes()
    units = band_units()
    agreed = run_case(
        tmp, "pair_preflight_ok",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    full = distinct_bytes(agreed["processed"])
    refused = run_case(
        tmp, "pair_preflight_refused",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units,
                                  reference_time="2021-05-10T15:33:49.023776-04:00"))
    spent = distinct_bytes(refused["processed"])
    h.equal("pair_preflight/verdict reached when they agree", agreed["status"], 0)
    h.check("pair_preflight/refused when they do not", "input error" in str(refused["status"]),
            str(refused["status"]))
    h.check("pair_preflight/matched a reader", spent > 0, spent)
    h.check("pair_preflight/costs less than a full read", spent < full,
            "%d distinct bytes refusing against %d reading" % (spent, full))


def case_missing_reference_time_is_an_input_error(h, tmp):
    """An asset that states no session-time origin cannot be placed on one.

    Both halves are checked, because both matter and for different reasons: the
    raw asset supplies the grid's extent and the processed asset supplies the
    spikes. Neither absence may become an agreement, a disagreement, or a drift
    verdict -- all three would be a missing measurement reported as a value.
    """
    rows = default_electrodes()
    units = band_units()
    processed = run_case(
        tmp, "no_processed_reference",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units, reference_time=None))
    status = str(processed["status"])
    h.check("no_reference/processed refused",
            "carries no timestamps_reference_time" in status, status)
    h.check("no_reference/processed named as an input error",
            "input error" in status, status)
    h.check("no_reference/processed names the asset", "processed asset" in status, status)
    h.check("no_reference/processed no report", processed["text"] is None)
    h.check("no_reference/processed no record", processed["record"] is None)
    raw = run_case(
        tmp, "no_raw_reference",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S, reference_time=None),
        lambda p: write_processed(p, rows, units))
    status = str(raw["status"])
    h.check("no_reference/raw refused",
            "carries no timestamps_reference_time" in status, status)
    h.check("no_reference/raw names the raw asset", "raw asset" in status, status)
    h.check("no_reference/raw no report", raw["text"] is None)


def case_timezone_naive_reference_time_is_an_input_error(h, tmp):
    """A wall-clock reading with no offset is not an instant.

    The eight disagreeing sessions in the 71-session measurement differ by
    exactly one hour while both halves still label themselves ``-04:00``, so the
    offset is the part of the value that carries the information. Admitting a
    naive value would mean choosing an offset for it -- UTC, or the machine's --
    which invents the very quantity the two assets are compared on. All 142
    measured assets carry an offset, so refusing rejects nothing this dandiset
    contains.
    """
    rows = default_electrodes()
    units = band_units()
    naive = "2021-05-10T14:33:49.023776"
    h.check("naive_reference/fixture parses as a datetime at all",
            archive_units.reference_instant(naive) is None
            and datetime.datetime.fromisoformat(naive) is not None,
            "the fixture must be well-formed ISO-8601 and still be refused")
    result = run_case(
        tmp, "naive_reference",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units, reference_time=naive))
    status = str(result["status"])
    h.check("naive_reference/refused", "is not an ISO-8601 timestamp" in status, status)
    h.check("naive_reference/names the offset as what is missing",
            "UTC offset" in status, status)
    h.check("naive_reference/named as an input error", "input error" in status, status)
    h.check("naive_reference/no report", result["text"] is None)
    h.check("naive_reference/no record", result["record"] is None)


def case_malformed_reference_time_is_an_input_error(h, tmp):
    """A value that is not a timestamp at all is refused before it is compared."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "malformed_reference",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units,
                                  reference_time="session start, roughly noon"))
    status = str(result["status"])
    h.check("malformed_reference/refused", "is not an ISO-8601 timestamp" in status,
            status)
    h.check("malformed_reference/quotes the value", "roughly noon" in status, status)
    h.check("malformed_reference/no report", result["text"] is None)


def case_refused_reference_time_is_not_an_agreement(h, tmp):
    """A reference time the budget declined is an input error, not a comparison.

    The provenance read replaces a value it could not afford with a
    self-describing marker, so the string is present and is not the file's
    value. Comparing two markers would make two unread values agree, and
    comparing a marker with a real value would make a budget refusal look like a
    clock disagreement. Neither is admissible: an undetermined value is a
    missing measurement.
    """
    rows = default_electrodes()
    units = band_units()
    big = "2021-05-10T14:33:49.023776-04:00" + ("0" * (30 * archive_units.PROVENANCE_MAX_BYTES))
    result = run_case(
        tmp, "refused_reference",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units, reference_time=big))
    status = str(result["status"])
    h.check("refused_reference/refused", "not read whole" in status, status)
    h.check("refused_reference/names the path", "timestamps_reference_time" in status,
            status)
    h.check("refused_reference/named as an input error", "input error" in status, status)
    h.check("refused_reference/no report", result["text"] is None)
    h.check("refused_reference/no record", result["record"] is None)
    # And the marker itself must not be authenticatable, which is the property
    # the input error rests on rather than a second statement of it.
    marker = "%s a refusal>" % archive_units.PROVENANCE_UNREAD_PREFIX
    h.check("refused_reference/a marker is not a complete value",
            not archive_units.provenance_is_complete(marker), marker)
    h.check("refused_reference/a marker does not parse as an instant",
            archive_units.reference_instant(marker) is None, marker)


def case_provenance_token_is_case_insensitive(h, tmp):
    """The measured value's capitalisation is not what the rule turns on.

    ``NeuroConv`` is how the 21 measured assets spell it. Requiring that exact
    capitalisation would make a lower-cased spelling of the same toolchain an
    input error, which is a rejection on typography rather than on provenance.
    """
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "provenance_case",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(
            p, rows, units,
            provenance={"general/source_script": "created using neuroconv v0.9.2"}))
    h.equal("provenance_case/status", result["status"], 0)


def case_vlen_provenance_is_refused_before_it_is_spent(h, tmp):
    """A two-million-character variable-length value costs kilobytes, RC-003-F3.

    RC-002-F1-R2 was an accounting defect: the provenance read sat after the
    ceiling, so its bytes were in none of the plan's terms. Moving it into
    preflight fixed the accounting and *not* the spend -- the value was still
    read in full and only then reported, so a two-million-character
    ``general/source_script`` moved 2,028,208 bytes before a one-byte ceiling
    could refuse anything. HDF5 will not state a variable-length value's size in
    advance, but h5py asks the reader for the heap collection's bytes before
    they move, so the request is refused rather than the result measured.

    The two numbers this case pins are the ones that separate the two repairs:
    the bytes that actually moved, and the fact that the run stopped instead of
    passing with a truncated marker.
    """
    rows = default_electrodes()
    units = band_units()
    big = "# generated conversion source\n" + ("x = 123456789\n" * 145000)
    budget = archive_units.PROVENANCE_MAX_BYTES
    h.check("vlen_refusal/fixture_is_far_over_the_budget", len(big) > 20 * budget,
            "%d characters against a %d-byte budget" % (len(big), budget))
    result = run_case(
        tmp, "vlen_provenance",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units,
                                  provenance={"general/source_script": big}))
    status = str(result["status"])
    h.check("vlen_refusal/run_stopped", "not read whole" in status, status)
    h.check("vlen_refusal/named_as_an_input_error", "input error" in status, status)
    h.check("vlen_refusal/no_report", result["text"] is None)
    touched = distinct_bytes(result["processed"])
    h.check("vlen_refusal/matched_a_reader", touched > 0, touched)
    h.check("vlen_refusal/spend_is_far_below_the_value",
            touched < len(big) // 4,
            "%d distinct bytes touched against a %d-character value" % (touched, len(big)))


def case_budget_admits_a_value_it_can_afford(h, tmp):
    """A large-but-affordable provenance value is read, and its cost is in the plan.

    The refusal above would also be produced by a rule that refused every
    variable-length value, which would reject every real asset. This is the
    other side: a value one order of magnitude larger than the measured ones and
    still inside the budget is read whole, authenticated, and paid for inside
    the plan's own terms -- which is the RC-002-F1-R2 property, kept.
    """
    rows = default_electrodes()
    units = band_units()
    budget = archive_units.PROVENANCE_MAX_BYTES
    # The bulk sits on an optional path. ``general/source_script`` is
    # authenticated against the whole conversion statement, so padding *it* would
    # be refused for its form rather than admitted for its size, and the case
    # would stop proving anything about the budget.
    big = "test fixture, padded: " + "x" * (budget // 2)
    h.check("budget_admits/fixture_is_inside_the_budget", len(big) < budget,
            "%d characters against %d" % (len(big), budget))
    # 4 KiB blocks, deliberately. The whole-suite invariant compares the
    # distinct bytes touched against the plan's block-derived bound, and at the
    # 1 MiB default one block covers this whole fixture, so the comparison is
    # true whatever the plan says about preflight. At 4 KiB the preflight reads
    # are many blocks and a plan that forgets them is short by a measurable
    # amount -- which is what makes this case, and not only its own named
    # assertion, notice a plan blind to what preflight spent.
    result = run_case(
        tmp, "affordable_provenance",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(
            p, rows, units,
            provenance={"general/source_script": "Created using NeuroConv v0.9.2",
                        "general/institution": big}),
        argv_extra=("--block-kb", "4"))
    h.equal("budget_admits/status", result["status"], 0)
    record = result["record"]
    plan = record["plan"]
    spent = distinct_bytes(result["processed"])
    h.equal("budget_admits/value_read_whole",
            record["provenance"]["general/institution"], big)
    h.check("budget_admits/transfer_inside_the_bound",
            spent <= plan["cache_bound_bytes"],
            "%d touched against %d bounded" % (spent, plan["cache_bound_bytes"]))
    h.check("budget_admits/preflight_spend_counted",
            plan["spent_bytes"] >= len(big),
            "spent_bytes %d against a %d-character value"
            % (plan["spent_bytes"], len(big)))
    h.check("budget_admits/peak_covers_the_transfer",
            plan["peak_resident_bytes"] >= spent,
            "peak %d against %d transferred" % (plan["peak_resident_bytes"], spent))
    text = result["text"] or ""
    h.check("budget_admits/report_clips_the_rendered_value", big not in text,
            "a %d-character value must not be pasted whole into the report" % len(big))
    h.check("budget_admits/report_still_shows_the_head",
            "Created using NeuroConv v0.9.2" in text, text[:0])
    spend = record["provenance_io"]["processed"]
    # Not "at least the value's length": HDF5 serves a global-heap collection it
    # has already read without asking this reader again, so a 32 KB value can be
    # returned whole for a fraction of that in requests. What the budget governs
    # is what was asked for, and that is what is checked.
    h.check("budget_admits/request_spend_inside_its_budget",
            0 < spend["read_bytes"] <= spend["read_budget_bytes"],
            "%d characters, spend %s" % (len(big), spend))
    h.check("budget_admits/transfer_spend_inside_its_budget",
            0 < spend["transfer_bytes"] <= spend["transfer_budget_bytes"], spend)


def case_oversize_stored_provenance_is_not_read(h, tmp):
    """Where the file will state a value's stored size, an oversized one is refused.

    The cap has two halves because HDF5 answers the size question for only one
    of them. A fixed-length string dataset reports its stored bytes, so the read
    can be refused before it happens; a variable-length one keeps its characters
    in the global heap and reports 16 bytes of storage for a 4.2 MB value, so
    the only bound left there is on what is retained. This case is the first
    half, and it asserts the value really is in the file so that a refusal is
    not confused with an absence.
    """
    case_dir = os.path.join(tmp, "provenance_stored_size")
    os.makedirs(case_dir, exist_ok=True)
    path = os.path.join(case_dir, "provenance.nwb")
    big = ("y = 1\n" * 700000).encode()
    with h5py.File(path, "w") as handle:
        handle.create_dataset("general/source_script", data=np.bytes_(big))
        handle.create_dataset("general/lab", data="cortexlab",
                              dtype=h5py.string_dtype(encoding="utf-8"))
    reader = archive_units.BoundedReader(LocalFile(path, os.path.getsize(path)))
    with h5py.File(reader, "r") as handle:
        node = handle["general/source_script"]
        h.check("stored_provenance/file_really_holds_it", len(node[()]) == len(big),
                "%d bytes" % len(node[()]))
        h.check("stored_provenance/size_is_readable",
                archive_units._stored_value_bytes(node) == len(big),
                "%s" % archive_units._stored_value_bytes(node))
        out = archive_units.source_provenance(handle, reader)
    value = out["general/source_script"]
    h.check("stored_provenance/not_read", value.startswith("<not read:"), value[:90])
    h.check("stored_provenance/refused_before_the_read_not_by_the_budget",
            "stored bytes exceeds" in value, value[:90])
    h.check("stored_provenance/names_the_size", str(len(big)) in value, value[:90])
    h.check("stored_provenance/names_the_cap",
            str(archive_units.PROVENANCE_MAX_BYTES) in value, value[:90])
    h.check("stored_provenance/retained_is_small", len(value) < 200, len(value))
    h.equal("stored_provenance/small_value_untouched", out["general/lab"], "cortexlab")
    h.check("stored_provenance/refusal_is_not_authenticatable",
            not archive_units.provenance_is_complete(value), value[:60])


def case_transfer_budget_refuses_at_the_block_layer(h, tmp):
    """A budget on the request does not bound the transfer, RC-003-F3 Round 2.

    The first repair charged the length h5py asks for. The reader underneath
    fetches whole fixed-size blocks and keeps them, so a sixteen-byte read of a
    byte nothing has fetched yet costs a whole block: on the two-million-character
    construction at the command's default 1 MiB block, 2,081,456 distinct bytes
    moved before a 65,536-byte budget refused the value. A request and the
    transfer that serves it are different quantities, and only one of them was
    being bounded.

    This measures the difference directly and on the proxy itself, which is
    where the property lives. One read of sixteen bytes at an offset nothing has
    touched: under a transfer budget smaller than a block it is refused and
    **nothing moves**; under a transfer budget of one block it succeeds and
    exactly one block moves. The request is the same sixteen bytes in both.
    """
    case_dir = os.path.join(tmp, "transfer_budget")
    os.makedirs(case_dir, exist_ok=True)
    path = os.path.join(case_dir, "blob.bin")
    block = 4096
    with open(path, "wb") as handle:
        handle.write(b"z" * (block * 8))
    size = os.path.getsize(path)
    offset = block * 5

    del READERS[:]
    reader = archive_units.BoundedReader(BlockLocalFile(path, size, block=block))
    refused = None
    with reader.budget(65536, block // 2):
        reader.seek(offset)
        try:
            reader.read(16)
        except archive_units.ReadBudgetExceeded as exc:
            refused = str(exc)
    spend = reader.last_spend
    moved = distinct_bytes(path)
    h.check("transfer_budget/refused", refused is not None and "distinct bytes" in refused,
            repr(refused))
    h.check("transfer_budget/names_the_block_size",
            refused is not None and "%d-byte block size" % block in refused, repr(refused))
    h.check("transfer_budget/request_alone_would_have_been_admitted",
            16 <= spend["read_budget_bytes"],
            "the sixteen-byte request is far inside the 65536-byte request budget")
    h.equal("transfer_budget/nothing_moved", moved, 0)
    h.equal("transfer_budget/nothing_charged", spend["transfer_bytes"], 0)
    reader.close()

    del READERS[:]
    allowed = archive_units.BoundedReader(BlockLocalFile(path, size, block=block))
    with allowed.budget(65536, block):
        allowed.seek(offset)
        data = allowed.read(16)
    spend = allowed.last_spend
    h.equal("transfer_budget/one_block_budget_admits_the_read", len(data), 16)
    h.equal("transfer_budget/charged_the_whole_block", spend["transfer_bytes"], block)
    h.equal("transfer_budget/charged_the_request_separately", spend["read_bytes"], 16)
    h.equal("transfer_budget/one_block_moved", distinct_bytes(path), block)
    allowed.close()
    del READERS[:]


def case_provenance_transfer_is_bounded_at_the_default_block(h, tmp):
    """Codex's own construction, measured against the bound that governs it.

    A two-million-character variable-length ``general/source_script`` read
    through a block-caching reader at the command's default 1 MiB block. What
    the module now publishes for this read is
    :func:`archive_units.provenance_transfer_budget` of that block size, and the
    distinct bytes the file gives up must be inside it. The 65,536-byte figure
    is the budget on the *request*, and comparing a transfer against it was
    comparing two different quantities -- which is the finding, from the other
    side.
    """
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    case_dir = os.path.join(tmp, "provenance_block_expansion")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    big = "p" * 2000000
    write_processed(processed, rows, units,
                    provenance={"general/source_script": big})
    size = os.path.getsize(processed)
    block = 1024 * 1024
    budget = archive_units.provenance_transfer_budget(block)
    # First without a ceiling, so what refuses is the provenance budget alone.
    del READERS[:]
    archive_units.RemoteFile = BlockLocalFile
    refused = None
    try:
        archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi,
                                      plan_only=True)
    except ValueError as exc:
        refused = str(exc)
    finally:
        archive_units.RemoteFile = LocalFile
    touched = distinct_bytes(processed)
    h.check("block_expansion/refused", refused is not None and "not read whole" in refused,
            repr(refused))
    h.check("block_expansion/fixture_is_larger_than_the_budget_it_is_read_under",
            size > archive_units.PROVENANCE_MAX_BYTES,
            "%d-byte fixture against a %d-byte request budget"
            % (size, archive_units.PROVENANCE_MAX_BYTES))
    h.check("block_expansion/matched_a_reader", touched > 0, touched)
    h.check("block_expansion/whole_file_transfer_inside_the_transfer_budget",
            touched <= budget,
            "%d distinct bytes against a %d-byte provenance transfer budget"
            % (touched, budget))
    h.check("block_expansion/budget_is_block_denominated",
            budget >= block, "%d against a %d-byte block" % (budget, block))

    # Then with the one-byte ceiling of the reviewer's own construction, which
    # measured 2,081,456 distinct bytes spent before the refusal. Every one of
    # those bytes was spent by preflight *before* the provenance read, so the
    # provenance budget could not have prevented them and the ceiling is what
    # had to reach them.
    del READERS[:]
    archive_units.RemoteFile = BlockLocalFile
    ceiling_refused = None
    try:
        archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi,
                                      max_bytes=1, plan_only=True)
    except ValueError as exc:
        ceiling_refused = str(exc)
    finally:
        archive_units.RemoteFile = LocalFile
    h.check("block_expansion/one_byte_ceiling_refuses",
            ceiling_refused is not None
            and "declared ceiling transfer budget" in ceiling_refused,
            repr(ceiling_refused))
    h.equal("block_expansion/one_byte_ceiling_moves_nothing",
            distinct_bytes(processed), 0)
    del READERS[:]


def case_command_reports_a_block_readers_expansion(h, tmp):
    """Run the whole command over a block-caching reader so the invariant sees one.

    Every other end-to-end case runs on :class:`LocalFile`, which fetches
    exactly what it is asked for -- so its transfer equals its request and the
    whole-suite provenance invariant is comparing a quantity against itself.
    This case is the one that gives that invariant a reader whose transfer is
    larger than its request, which is the only shape in which the RC-003-F3
    defect exists at all.
    """
    rows = default_electrodes()
    units = band_units()
    archive_units.RemoteFile = BlockLocalFile
    try:
        result = run_case(
            tmp, "block_reader_command",
            lambda p: write_raw(p, rows, 0.0, EXTENT_S),
            lambda p: write_processed(p, rows, units),
            argv_extra=("--block-kb", "4"))
    finally:
        archive_units.RemoteFile = LocalFile
    h.equal("block_command/status", result["status"], 0)
    record = result["record"]
    for label in ("raw", "processed"):
        spend = record["provenance_io"][label]
        h.check("block_command/%s reader declares a block" % label,
                spend["block_bytes"] > 0, spend)
        h.check("block_command/%s transfer inside its budget" % label,
                spend["transfer_bytes"] <= spend["transfer_budget_bytes"], spend)
    # The raw asset's reader is opened for provenance and nothing else, so every
    # block it touches is new and the expansion is visible: a thirty-character
    # value costs whole blocks.
    raw_spend = record["provenance_io"]["raw"]
    h.check("block_command/raw transfer exceeds the request",
            raw_spend["transfer_bytes"] > raw_spend["read_bytes"],
            "a block reader cannot serve a request for less than a block: %s"
            % (raw_spend,))
    # The processed asset's reader has already fetched these blocks in
    # preflight, so the model charges nothing for them. That is the other half
    # of the same property: the budget is on *distinct* bytes, and a block the
    # reader is holding is not fetched twice.
    processed_spend = record["provenance_io"]["processed"]
    h.check("block_command/processed credits the blocks preflight already fetched",
            processed_spend["transfer_bytes"] < processed_spend["read_bytes"],
            processed_spend)
    # And the cap on the raw read's block, measured where it can be seen: at the
    # command's own 1 MiB default the reader this read opens must still use the
    # smaller block, because this is the read with no plan behind it and its
    # bound is block-denominated. Asserting it inside the case above would prove
    # nothing -- 4 KiB is under the cap however the cap is written.
    del READERS[:]
    case_dir = os.path.join(tmp, "block_reader_command")
    archive_units.RemoteFile = BlockLocalFile
    try:
        raw_only = archive_units.read_provenance(
            os.path.join(case_dir, "raw.nwb"),
            os.path.getsize(os.path.join(case_dir, "raw.nwb")), 1024 * 1024)
    finally:
        archive_units.RemoteFile = LocalFile
    h.equal("block_command/raw_block_is_capped",
            READERS[-1].block, archive_units.PROVENANCE_BLOCK_BYTES)
    h.equal("block_command/raw_bound_follows_the_capped_block",
            raw_only["provenance_io"]["transfer_budget_bytes"],
            archive_units.provenance_transfer_budget(
                archive_units.PROVENANCE_BLOCK_BYTES))
    h.check("block_command/capped_bound_is_far_below_the_callers",
            raw_only["provenance_io"]["transfer_budget_bytes"]
            < archive_units.provenance_transfer_budget(1024 * 1024),
            raw_only["provenance_io"])
    del READERS[:]


def case_a_ceiling_refusal_is_not_recorded_as_a_provenance_marker(h, tmp):
    """An enclosing budget's refusal must escape the handler for this one's.

    Budgets nest, and both raise the same exception class. The provenance read
    records its *own* refusals as self-describing markers and carries on, which
    is right: one unreadable optional value is not a reason to stop. Applying
    that to a refusal raised by the enclosing ceiling would turn a statement
    about the whole read into a note beside one path -- a failure reporting
    itself as a success -- so the refusing scope is named on the exception and
    only the provenance scope's own refusals are absorbed.
    """
    case_dir = os.path.join(tmp, "ceiling_marker")
    os.makedirs(case_dir, exist_ok=True)
    path = os.path.join(case_dir, "provenance.nwb")
    with h5py.File(path, "w") as handle:
        handle.create_dataset("general/source_script",
                              data="Created using NeuroConv v0.9.2",
                              dtype=h5py.string_dtype(encoding="utf-8"))
        handle.create_dataset("general/lab", data="cortexlab",
                              dtype=h5py.string_dtype(encoding="utf-8"))
    del READERS[:]
    reader = archive_units.BoundedReader(LocalFile(path, os.path.getsize(path)))
    escaped = None
    with h5py.File(reader, "r") as handle:
        with reader.budget(None, 8, label=archive_units.PREFLIGHT_SCOPE):
            try:
                recorded = archive_units.source_provenance(handle, reader)
            except archive_units.ReadBudgetExceeded as exc:
                escaped = exc
                recorded = None
    h.check("ceiling_marker/refusal escaped the provenance handler", escaped is not None,
            "source_provenance returned %r instead of re-raising" % (recorded,))
    h.equal("ceiling_marker/named the refusing scope",
            getattr(escaped, "scope", None), archive_units.PREFLIGHT_SCOPE)
    h.check("ceiling_marker/the two scopes have distinct labels",
            archive_units.PREFLIGHT_SCOPE != archive_units.PROVENANCE_SCOPE,
            "a label that matched would make the handler absorb both")
    reader.close()
    del READERS[:]


def case_a_cached_value_is_still_capped(h, tmp):
    """A value HDF5 serves from its own cache bypasses the budget, and is still bounded.

    The budget bounds what h5py *asks the reader for*. It does not bound what
    HDF5 hands back out of its own global-heap cache, and the two are not the
    same: after one read of a 2,000,000-character variable-length value, a
    second read of it costs **16 bytes** through the reader, so a budget of
    1,000 does not refuse it. That is not reachable through the command's own
    call sequence -- nothing reads ``general/*`` before ``source_provenance``,
    and every provenance read there is under the budget -- but it is reachable
    whenever HDF5 has the collection for another reason, and a bound that holds
    only because of a layout accident is not a bound.

    What holds regardless is the retention cap: the value is capped on the way
    into the returned dict and the marker names its real length, so it is not
    authenticatable. This case exists because the cap looked unreachable under
    the budget and was one edit away from being deleted as dead.
    """
    case_dir = os.path.join(tmp, "cached_provenance")
    os.makedirs(case_dir, exist_ok=True)
    path = os.path.join(case_dir, "provenance.nwb")
    big = "q" * 2000000
    with h5py.File(path, "w") as handle:
        handle.create_dataset("general/source_script", data=big,
                              dtype=h5py.string_dtype(encoding="utf-8"))
    reader = archive_units.BoundedReader(LocalFile(path, os.path.getsize(path)))
    with h5py.File(reader, "r") as handle:
        node = handle["general/source_script"]
        with reader.budget(4000000):
            first = node[()]
        h.equal("cached_cap/first_read_is_whole", len(first), len(big))
        before = reader.n_bytes
        out = archive_units.source_provenance(handle, reader, max_bytes=1000)
        spent = reader.n_bytes - before
    value = out["general/source_script"]
    h.check("cached_cap/second_read_bypassed_the_budget", spent < 1000,
            "%d bytes through the reader for a %d-character value" % (spent, len(big)))
    h.check("cached_cap/retained_value_is_capped", len(value) < 2000,
            "%d characters retained" % len(value))
    h.check("cached_cap/names_the_real_length", str(len(big)) in value, value[-90:])
    h.check("cached_cap/is_not_authenticatable",
            not archive_units.provenance_is_complete(value), value[-90:])


def case_null_distribution_is_reported(h, tmp):
    """The report carries the null's shape, not only its two endpoints."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "null_shape",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    text = result["text"] or ""
    record = result["record"]
    h.equal("null_shape/status", result["status"], 0)
    h.check("null_shape/deciles printed", "null deciles" in text)
    h.equal("null_shape/replicates recorded", len(record["null"]["values"]), 200)
    h.equal("null_shape/values ascending", record["null"]["values"],
            sorted(record["null"]["values"]))
    h.equal("null_shape/q95 is the declared rank",
            record["null"]["q95"], record["null"]["values"][record["null"]["rank"] - 1])
    h.equal("null_shape/decile rule matches q95",
            CLI.nearest_rank(record["null"]["values"], 95), record["null"]["q95"])
    h.equal("null_shape/first decile is the minimum",
            CLI.nearest_rank(record["null"]["values"], 0), record["null"]["values"][0])
    h.equal("null_shape/last decile is the maximum",
            CLI.nearest_rank(record["null"]["values"], 100), record["null"]["values"][-1])


def case_fractional_ragged_offsets_are_refused(h, tmp):
    """Ragged offsets that are not whole numbers are refused, not truncated.

    Two offsets 0.75 apart describe no partition at all, but ``int()`` turns
    them into an equal pair and the file reads as well-formed. The check has to
    happen on the stored values.

    The refusal now names the storage dtype rather than the fractional value,
    because a ``VectorIndex`` must be stored as an integer and that rule fires
    before anything looks at the values. The case is kept as the construction it
    always was: this file must not reach a verdict. What it no longer proves on
    its own is the integrality check, which ``case_fractional_electrode_is_refused``
    covers on the column where integrality is the only rule available.
    """
    rows = default_electrodes()
    units = band_units()

    def write(path):
        write_processed(path, rows, units)
        with h5py.File(path, "r") as handle:
            times = handle["units/spike_times_index"][:].astype(np.float64)
            depths = handle["units/spike_distances_from_probe_tip_um_index"][:].astype(
                np.float64)
        times[0] += 0.75
        depths[0] += 0.75
        replace_dataset(path, {"units/spike_times_index": times,
                               "units/spike_distances_from_probe_tip_um_index": depths})

    result = run_case(
        tmp, "fractional_offsets",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S), write)
    h.check("fractional_offsets/refused", "integer storage" in str(result["status"]),
            str(result["status"]))
    h.check("fractional_offsets/named as input error",
            "input error" in str(result["status"]))
    h.check("fractional_offsets/no report", result["text"] is None)
    h.check("fractional_offsets/no record", result["record"] is None)


def case_float_ragged_index_is_refused_even_when_whole(h, tmp):
    """A floating-point ragged index is malformed however round its values are.

    ``spike_times_index`` is an HDMF ``VectorIndex`` and the common schema
    specifies integer storage for it, so a float column is a malformed file and
    not a permissible encoding of the same partition. Accepting it because the
    conversion happens to be lossless would be this project inventing a laxer
    schema than the one the format has, on the dataset that decides which spikes
    belong to which unit.

    The contrast is deliberate and is asserted in the same run:
    ``max_electrode`` is a custom IBL column with no such specification, and the
    identical float encoding is accepted there and reported.
    """
    rows = default_electrodes()
    units = band_units()

    def write(path):
        write_processed(path, rows, units)
        with h5py.File(path, "r") as handle:
            times = handle["units/spike_times_index"][:].astype(np.float64)
            depths = handle["units/spike_distances_from_probe_tip_um_index"][:].astype(
                np.float64)
        h.check("float_index/values_are_whole",
                bool(np.all(times == np.floor(times))
                     and np.all(depths == np.floor(depths))))
        replace_dataset(path, {"units/spike_times_index": times,
                               "units/spike_distances_from_probe_tip_um_index": depths})

    result = run_case(
        tmp, "float_index",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S), write)
    status = str(result["status"])
    h.check("float_index/refused", "integer storage" in status, status)
    h.check("float_index/names_column", "spike_times_index" in status, status)
    h.check("float_index/names_schema", "VectorIndex" in status, status)
    h.check("float_index/input_error", "input error" in status)
    h.check("float_index/no_report", result["text"] is None)
    h.check("float_index/no_record", result["record"] is None)


def case_fractional_electrode_is_refused(h, tmp):
    """A ``max_electrode`` that is not a whole number is refused."""
    rows = default_electrodes()
    units = band_units()

    def write(path):
        write_processed(path, rows, units)
        with h5py.File(path, "r") as handle:
            values = handle["units/max_electrode"][:].astype(np.float64)
        values[0] += 0.75
        replace_dataset(path, {"units/max_electrode": values})

    result = run_case(
        tmp, "fractional_electrode",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S), write)
    h.check("fractional_electrode/refused", "not a whole number" in str(result["status"]),
            str(result["status"]))
    h.check("fractional_electrode/names the column",
            "max_electrode" in str(result["status"]))
    h.check("fractional_electrode/no report", result["text"] is None)


def case_integral_float_column_is_accepted_and_named(h, tmp):
    """A float column whose values are whole is accepted, and its dtype is reported.

    This is the deliberate boundary of the check above: NWB does not require the
    dtype, and a float column holding exact whole numbers is not ambiguous about
    which row it names. What would be wrong is accepting it silently, so the
    stored dtype travels into the record and the report.
    """
    rows = default_electrodes()
    units = band_units()

    def write(path):
        write_processed(path, rows, units)
        with h5py.File(path, "r") as handle:
            values = handle["units/max_electrode"][:].astype(np.float64)
        replace_dataset(path, {"units/max_electrode": values})

    result = run_case(
        tmp, "integral_float_column",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S), write)
    h.equal("integral_float/status", result["status"], 0)
    h.equal("integral_float/dtype recorded",
            result["record"]["integer_dtypes"]["max_electrode"], "float64")
    h.check("integral_float/dtype in report",
            "max_electrode float64" in (result["text"] or ""))


def case_short_unit_column_is_refused(h, tmp):
    """A one-value-per-unit column with too few values is refused.

    A short column would otherwise shorten the unit set silently: the units it
    stops covering simply would not resolve, and the band would be measured
    without them and without saying so.
    """
    rows = default_electrodes()
    units = band_units()

    def write(path):
        write_processed(path, rows, units)
        with h5py.File(path, "r") as handle:
            values = handle["units/max_electrode"][:]
        replace_dataset(path, {"units/max_electrode": values[:-1]})

    result = run_case(
        tmp, "short_column",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S), write)
    h.check("short_column/refused", "one value per unit" in str(result["status"]),
            str(result["status"]))
    h.check("short_column/no report", result["text"] is None)


def case_cross_subject_pair_is_refused(h, tmp):
    """A raw and a processed asset from different subjects are not one recording.

    The session UUID alone paired them, and everything downstream then took the
    band and the clock from one animal and the units from another, reporting the
    result under whichever subject the raw file named.
    """
    rows = default_electrodes()
    units = band_units()
    case_dir = os.path.join(tmp, "cross_subject")
    os.makedirs(case_dir, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    write_raw(raw_path, rows, 0.0, EXTENT_S)
    write_processed(processed_path, rows, units)
    session = session_id("cross_subject")
    assets = [
        {"asset_id": "raw-cross", "size": os.path.getsize(raw_path), "blob": raw_path,
         "path": "sub-A/sub-A_ses-%s%s" % (session, dandi.RAW_SUFFIX)},
        {"asset_id": "processed-cross", "size": os.path.getsize(processed_path),
         "blob": processed_path,
         "path": "sub-B/sub-B_ses-%s%s" % (session, dandi.PROCESSED_SUFFIX)},
    ]
    dandi.list_assets = lambda *a, **k: assets
    dandi.blob_url = lambda asset: asset["blob"]
    out = os.path.join(case_dir, "report.txt")
    try:
        status = CLI.main(["--session", session, "--probe", PROBES[0], "--target", TARGET,
                           "--assets-cache", os.path.join(case_dir, "assets.json"),
                           "--out", out])
    except SystemExit as exc:
        status = str(exc.code)
    h.check("cross_subject/refused", "same subject's recording" in str(status), str(status))
    h.check("cross_subject/named as input error", "input error" in str(status))
    h.check("cross_subject/no report", not os.path.exists(out))


def case_paired_stems_must_match(h, tmp):
    """Two assets of the same subject whose file stems differ are not one recording."""
    rows = default_electrodes()
    units = band_units()
    case_dir = os.path.join(tmp, "stem_mismatch")
    os.makedirs(case_dir, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    write_raw(raw_path, rows, 0.0, EXTENT_S)
    write_processed(processed_path, rows, units)
    session = session_id("stem_mismatch")
    assets = [
        {"asset_id": "raw-stem", "size": os.path.getsize(raw_path), "blob": raw_path,
         "path": "sub-A/sub-A_ses-%s%s" % (session, dandi.RAW_SUFFIX)},
        {"asset_id": "processed-stem", "size": os.path.getsize(processed_path),
         "blob": processed_path,
         "path": "sub-A/sub-A_ses-%s_run-2%s" % (session, dandi.PROCESSED_SUFFIX)},
    ]
    dandi.list_assets = lambda *a, **k: assets
    dandi.blob_url = lambda asset: asset["blob"]
    out = os.path.join(case_dir, "report.txt")
    try:
        status = CLI.main(["--session", session, "--probe", PROBES[0], "--target", TARGET,
                           "--assets-cache", os.path.join(case_dir, "assets.json"),
                           "--out", out])
    except SystemExit as exc:
        status = str(exc.code)
    h.check("stem_mismatch/refused", "stems differ" in str(status), str(status))
    h.check("stem_mismatch/no report", not os.path.exists(out))


def case_timestamps_must_cover_the_data(h, tmp):
    """An AP series with fewer timestamps than samples cannot supply the extent.

    ``t_last_s`` is the grid's whole extent, so a timestamp vector that stops
    short of the data is not the recording's last sample time -- and it looks
    exactly like a well-formed one from its endpoints alone.
    """
    rows = default_electrodes()
    units = band_units()

    def write(path):
        write_raw(path, rows, 0.0, EXTENT_S)
        with h5py.File(path, "r+") as handle:
            target = "acquisition/ElectricalSeries%sAP/timestamps" % PROBES[0]
            del handle[target]
            handle.create_dataset(target, data=np.linspace(0.0, EXTENT_S, 999))

    result = run_case(
        tmp, "timestamp_coverage",
        write, lambda p: write_processed(p, rows, units))
    h.check("timestamp_coverage/refused",
            "aligned timestamps" in str(result["status"])
            and "1000 samples" in str(result["status"]).replace("1000", "1000"),
            str(result["status"]))
    h.check("timestamp_coverage/named as input error",
            "input error" in str(result["status"]))
    h.check("timestamp_coverage/no report", result["text"] is None)


def case_band_gap_is_pinned(h, tmp):
    """The band's contiguity tolerance cannot be supplied, and it stays at 40 um.

    A wider tolerance merges separate islands of the target label across the
    structure between them, which changes which units the gate measures. The
    fixture holds two CA1 islands with CA3 rows between them; at the pinned
    tolerance only the island the band's own rule admits is measured.
    """
    rows = default_electrodes()
    for row in rows[:N_ROWS_PER_PROBE]:
        row["location"] = OTHER_LOCATION
    for index in (10, 11, 12, 25, 26, 27, 28):
        rows[index]["location"] = BAND_LOCATION
    units = band_units()
    typed = run_case(
        tmp, "typed_gap",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units),
        argv_extra=["--max-gap-um", "1000"])
    h.equal("pinned_gap/typed value rejected", str(typed["status"]), "2")
    h.check("pinned_gap/no report from the typed run", typed["text"] is None)
    pinned = run_case(
        tmp, "pinned_gap",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    record = pinned["record"]
    h.equal("pinned_gap/status", pinned["status"], 0)
    h.equal("pinned_gap/value is 40 um", record["max_gap_um"], 40.0)
    h.equal("pinned_gap/value is the module constant", CLI.BAND_MAX_GAP_UM, 40.0)
    h.equal("pinned_gap/band is one island",
            (record["band"]["depth_lo_um"], record["band"]["depth_hi_um"]),
            (500.0, 560.0))
    h.equal("pinned_gap/island is four rows", record["band"]["n_channels"], 4)
    h.check("pinned_gap/report says pinned", "pinned at 40" in (pinned["text"] or ""))
    # The same fixture read with the tolerance that used to be typeable: the two
    # islands merge into one band that spans the CA3 rows between them, which is
    # what makes the pinning a decision about which units get measured.
    raw = host_anatomy.read_electrode_table(pinned["raw"],
                                            os.path.getsize(pinned["raw"]), 1024 * 1024)
    merged = host_anatomy.contiguous_band(raw["probes"][PROBES[0]], TARGET, 1000.0)
    h.equal("pinned_gap/a wide tolerance would merge them",
            (merged["depth_lo_um"], merged["depth_hi_um"], merged["n_channels"]),
            (200.0, 560.0, 7))
    h.check("pinned_gap/merging admits more rows than the island",
            merged["n_channels"] > record["band"]["n_channels"])


def case_ceiling_bounds_the_block_transfer(h, tmp):
    """The ceiling stops the transfer it names, not only the stored payload.

    Against a block-caching reader the stored payload is not what gets fetched:
    a scattered slice costs whole blocks. A ceiling above the payload and below
    the real transfer used to admit the read.
    """
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    case_dir = os.path.join(tmp, "ceiling_blocks")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, units)
    size = os.path.getsize(processed)
    block = 16 * 1024
    archive_units.RemoteFile = BlockLocalFile
    try:
        planned = archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi,
                                                plan_only=True)
        full = archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi)
        plan = full["plan"]
        h.check("ceiling_blocks/bound covers the actual transfer",
                plan["cache_bound_bytes"] >= full["io"]["bytes"],
                "bound %d, actual %d" % (plan["cache_bound_bytes"], full["io"]["bytes"]))
        h.check("ceiling_blocks/actual exceeds the payload",
                full["io"]["bytes"] > plan["logical_bytes"],
                "actual %d, payload %d" % (full["io"]["bytes"], plan["logical_bytes"]))
        between = (plan["logical_bytes"] + full["io"]["bytes"]) // 2
        refused = None
        try:
            archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi,
                                          max_bytes=between)
        except ValueError as exc:
            refused = str(exc)
        h.check("ceiling_blocks/a ceiling above the payload is refused",
                refused is not None and "above the declared ceiling" in refused,
                repr(refused))
        h.check("ceiling_blocks/refusal_names_combined",
                refused is not None and "peak_resident_bytes is above" in refused,
                repr(refused))
        h.check("ceiling_blocks/refusal_names_parts",
                refused is not None and "retained block cache" in refused
                and "converted arrays" in refused and "Python structures" in refused,
                repr(refused))
        h.equal("ceiling_blocks/plan matches the planning read",
                planned["plan"]["cache_bound_bytes"], plan["cache_bound_bytes"])
    finally:
        archive_units.RemoteFile = LocalFile


def case_ceiling_can_bind_on_resident_memory(h, tmp):
    """The array term can be the one that drives the ceiling, not only the transfer.

    Stored float32 becomes float64 in memory, so the converted arrays are the
    larger term here and a transfer-only ceiling would not see them. The
    refusal is on the combined figure, so what this case establishes is that a
    ceiling sitting between the transfer bound and the arrays -- one the
    transfer alone would have cleared -- still refuses.
    """
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    case_dir = os.path.join(tmp, "ceiling_resident")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, units, depth_dtype=np.float32,
                    time_dtype=np.float32)
    size = os.path.getsize(processed)
    block = 4096
    archive_units.RemoteFile = BlockLocalFile
    try:
        planned = archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi,
                                                plan_only=True)
        plan = planned["plan"]
        h.check("ceiling_resident/resident exceeds payload",
                plan["resident_bytes"] > plan["logical_bytes"],
                "resident %d, payload %d" % (plan["resident_bytes"],
                                             plan["logical_bytes"]))
        h.check("ceiling_resident/array_term_is_larger",
                plan["resident_bytes"] > plan["cache_bound_bytes"],
                "resident %d, bound %d" % (plan["resident_bytes"],
                                           plan["cache_bound_bytes"]))
        between = (plan["cache_bound_bytes"] + plan["resident_bytes"]) // 2
        h.check("ceiling_resident/ceiling_clears_transfer",
                between > plan["cache_bound_bytes"])
        refused = None
        try:
            archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi,
                                          max_bytes=between)
        except ValueError as exc:
            refused = str(exc)
        h.check("ceiling_resident/refused_anyway",
                refused is not None and "peak_resident_bytes is above" in refused,
                repr(refused))
        h.check("ceiling_resident/refusal_names_arrays",
                refused is not None and "%d bytes of converted arrays"
                % plan["resident_bytes"] in refused, repr(refused))
    finally:
        archive_units.RemoteFile = LocalFile


def case_ceiling_covers_cache_and_arrays_together(h, tmp):
    """The cache and the converted arrays are live at once, so the ceiling sums them.

    The block reader keeps every block it fetched until the read returns, and
    the per-unit arrays accumulate while it does. Checking the two figures
    separately admitted a ceiling that neither exceeded on its own and both
    exceeded together: this measures the two coexisting quantities directly and
    requires that exact ceiling to be refused.
    """
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    case_dir = os.path.join(tmp, "combined_resident")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, units)
    size = os.path.getsize(processed)
    block = 16 * 1024

    class InspectingBlockFile(BlockLocalFile):
        """Remember the reader so its retained cache can be weighed afterwards."""

        last = None

        def __init__(self, *args, **kwargs):
            BlockLocalFile.__init__(self, *args, **kwargs)
            InspectingBlockFile.last = self

    archive_units.RemoteFile = InspectingBlockFile
    try:
        planned = archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi,
                                                plan_only=True)
        plan = planned["plan"]
        h.equal("combined/total_is_the_sum", plan["peak_resident_bytes"],
                plan["cache_bound_bytes"] + plan["resident_bytes"]
                + plan["structures_bytes"] + plan["library_cache_bytes"])
        h.check("combined/structures_charged", plan["structures_bytes"] > 0)
        # The ceiling the separate checks admitted: above each part, below the sum.
        admitted_before = max(plan["cache_bound_bytes"], plan["resident_bytes"]) + 1
        h.check("combined/old_ceiling_below_total",
                admitted_before < plan["peak_resident_bytes"],
                "ceiling %d, total %d" % (admitted_before,
                                          plan["peak_resident_bytes"]))
        refused = None
        try:
            archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi,
                                          max_bytes=admitted_before)
        except ValueError as exc:
            refused = str(exc)
        h.check("combined/refused_where_admitted",
                refused is not None and "peak_resident_bytes is above" in refused,
                repr(refused))
        full = archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi)
        cached = sum(len(payload) for payload
                     in InspectingBlockFile.last._blocks.values())
        converted = sum(unit["times"].nbytes + unit["depths"].nbytes
                        for unit in full["band_units"])
        h.check("combined/cache_coexists",
                cached > 0 and converted > 0 and cached + converted > admitted_before,
                "cached %d, converted %d, ceiling %d" % (cached, converted,
                                                         admitted_before))
        h.check("combined/bound_covers_coexistence",
                full["plan"]["peak_resident_bytes"] >= cached + converted,
                "bound %d, measured %d" % (full["plan"]["peak_resident_bytes"],
                                           cached + converted))
    finally:
        archive_units.RemoteFile = LocalFile


def case_chunked_columns_are_placed_from_the_chunk_index(h, tmp):
    """A chunked column has no dataset offset, so every chunk is located instead.

    A chunked read fetches whole chunks. Where those chunks sit is not something
    the dataset offset will say -- h5py gives None for a chunked dataset -- but
    the chunk index will say it per chunk, and that is what the plan asks.
    """
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    case_dir = os.path.join(tmp, "chunked")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, units, chunk_elements=64)
    size = os.path.getsize(processed)
    block = 16 * 1024
    archive_units.RemoteFile = BlockLocalFile
    try:
        full = archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi)
    finally:
        archive_units.RemoteFile = LocalFile
    plan = full["plan"]
    h.equal("chunked/basis_is_chunk_index", plan["bound_basis"], "chunk offsets")
    h.equal("chunked/layout reports the chunk",
            plan["time_layout"]["chunk_elements"], 64)
    h.equal("chunked/no_dataset_offset",
            plan["time_layout"]["offset"], None)
    h.check("chunked/all_chunks_located",
            plan["time_layout"]["chunk_map"]
            and all(entry is not None
                    for entry in plan["time_layout"]["chunk_map"].values()))
    h.check("chunked/bound covers the actual transfer",
            plan["cache_bound_bytes"] >= full["io"]["bytes"],
            "bound %d, actual %d" % (plan["cache_bound_bytes"], full["io"]["bytes"]))
    h.check("chunked/bound never exceeds the file",
            plan["cache_bound_bytes"] <= size,
            "bound %d, size %d" % (plan["cache_bound_bytes"], size))
    # A chunked column is the only case where HDF5 keeps a raw-data chunk cache
    # of its own, so it is the only case that can show the term is in the sum.
    h.check("chunked/library_cache_is_charged", plan["library_cache_bytes"] > 0,
            "library cache %d" % plan["library_cache_bytes"])
    h.equal("chunked/peak_includes_library_cache", plan["peak_resident_bytes"],
            plan["cache_bound_bytes"] + plan["resident_bytes"]
            + plan["structures_bytes"] + plan["library_cache_bytes"])


def case_fragmented_chunks_are_still_bounded(h, tmp):
    """Chunks scattered through the file are counted where they are, not as one span.

    HDF5 does not promise that a dataset's successive chunks occupy one
    contiguous region, and a file written incrementally beside other growing
    datasets does not. Rounding the first-to-last-chunk element range out to
    chunk boundaries and paying block alignment once therefore under-counted a
    fixed-block read by a quarter on this fixture, and a ceiling between the two
    numbers was admitted and then exceeded. Codex's construction, kept.
    """
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    case_dir = os.path.join(tmp, "fragmented")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, units)
    fragment_ragged_columns(processed)
    size = os.path.getsize(processed)
    block = 4096
    archive_units.RemoteFile = BlockLocalFile
    try:
        full = archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi)
        plan = full["plan"]
        offsets = sorted(entry[0] for entry in plan["time_layout"]["chunk_map"].values()
                         if entry is not None)
        gaps = [b - a for a, b in zip(offsets, offsets[1:])]
        h.check("fragmented/fixture_is_fragmented",
                len(offsets) > 2 and min(gaps) > plan["time_layout"]["itemsize"]
                * plan["time_layout"]["chunk_elements"],
                "smallest gap %r, chunk %r bytes"
                % (min(gaps) if gaps else None,
                   plan["time_layout"]["itemsize"]
                   * plan["time_layout"]["chunk_elements"]))
        h.check("fragmented/bound_covers_actual",
                plan["cache_bound_bytes"] >= full["io"]["bytes"],
                "bound %d, actual %d" % (plan["cache_bound_bytes"],
                                         full["io"]["bytes"]))
        h.check("fragmented/span_bound_would_not",
                _contiguous_span_bound(plan, block) < full["io"]["bytes"],
                "span bound %d, actual %d" % (_contiguous_span_bound(plan, block),
                                              full["io"]["bytes"]))
        ceiling = (plan["cache_bound_bytes"] + full["io"]["bytes"]) // 2
        refused = None
        try:
            archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi,
                                          max_bytes=ceiling)
        except ValueError as exc:
            refused = str(exc)
        h.check("fragmented/ceiling_refused",
                refused is not None and "peak_resident_bytes is above" in refused,
                repr(refused))
    finally:
        archive_units.RemoteFile = LocalFile


def _contiguous_span_bound(plan, block_bytes):
    """Recompute what the superseded span-based chunk bound would have said.

    Kept as a function rather than a number so the comparison in the fragmented
    case is against the old rule applied to this fixture, not against a digit
    copied out of a review message.
    """
    total = 0
    for layout in (plan["time_layout"], plan["depth_layout"]):
        chunk = layout["chunk_elements"]
        column = 0
        for _, n_spikes in plan["per_unit"]:
            if n_spikes <= 0:
                continue
            elements = ((n_spikes + chunk - 1) // chunk + 1) * chunk
            span = elements * layout["itemsize"]
            column += (span // block_bytes + 2) * block_bytes
        total += column + block_bytes
    return total + plan["spent_bytes"]


def case_unplaceable_columns_fall_back_to_the_whole_file(h, tmp):
    """When neither route locates the bytes, the bound is the only true one left.

    A contiguous dataset is placed from its offset and a chunked one from its
    chunk index. If a file gives neither -- an old library, a virtual or
    external dataset -- there is nothing left to say except that a reader cannot
    fetch more distinct bytes than the file holds. Loose, and still a bound; the
    basis says so rather than leaving a reader to assume the tight case.
    """
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    case_dir = os.path.join(tmp, "unplaceable")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, units, chunk_elements=64)
    size = os.path.getsize(processed)
    block = 16 * 1024
    original = archive_units.chunk_byte_ranges
    archive_units.chunk_byte_ranges = lambda dataset, slices: None
    archive_units.RemoteFile = BlockLocalFile
    try:
        full = archive_units.read_band_units(processed, size, block, PROBES[0], lo, hi)
    finally:
        archive_units.chunk_byte_ranges = original
        archive_units.RemoteFile = LocalFile
    plan = full["plan"]
    h.equal("unplaceable/basis_whole_file", plan["bound_basis"], "whole file")
    h.equal("unplaceable/bound_is_file_size", plan["cache_bound_bytes"], size)
    h.check("unplaceable/bound_covers_actual",
            plan["cache_bound_bytes"] >= full["io"]["bytes"],
            "bound %d, actual %d" % (plan["cache_bound_bytes"], full["io"]["bytes"]))


def case_plan_separates_the_costs(h, tmp):
    """The plan reports payload, bounded transfer and the memory terms separately."""
    rows = default_electrodes()
    units = band_units()
    lo, hi = band_bounds()
    spikes = sum(len(unit["times"]) for unit in units)
    largest = max(len(unit["times"]) for unit in units)
    case_dir = os.path.join(tmp, "three_costs")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    write_processed(processed, rows, units, depth_dtype=np.float32)
    read = archive_units.read_band_units(processed, os.path.getsize(processed),
                                         1024 * 1024, PROBES[0], lo, hi, plan_only=True)
    plan = read["plan"]
    h.equal("three_costs/payload is the stored size", plan["logical_bytes"], spikes * 12)
    h.equal("three_costs/resident is float64 plus one slice",
            plan["resident_bytes"], spikes * 16 + largest * 12)
    h.equal("three_costs/peak_is_the_sum",
            plan["peak_resident_bytes"],
            plan["cache_bound_bytes"] + plan["resident_bytes"]
            + plan["structures_bytes"] + plan["library_cache_bytes"])
    h.check("three_costs/no key called bytes", "bytes" not in plan)
    h.equal("three_costs/block size recorded", plan["block_bytes"], 1024 * 1024)
    h.check("three_costs/metadata already spent is included",
            plan["spent_bytes"] > 0 and plan["cache_bound_bytes"] > plan["spent_bytes"])


def case_output_paths_must_differ(h, tmp):
    """The report and the JSON record cannot be written to one path."""
    rows = default_electrodes()
    units = band_units()
    case_dir = os.path.join(tmp, "same_path")
    os.makedirs(case_dir, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    write_raw(raw_path, rows, 0.0, EXTENT_S)
    write_processed(processed_path, rows, units)
    session = session_id("same_path")
    install_local_assets([(session, raw_path, processed_path)])
    out = os.path.join(case_dir, "report.txt")
    try:
        status = CLI.main(["--session", session, "--probe", PROBES[0], "--target", TARGET,
                           "--assets-cache", os.path.join(case_dir, "assets.json"),
                           "--out", out, "--records", out])
    except SystemExit as exc:
        status = str(exc.code)
    h.check("same_path/refused", "same path" in str(status), str(status))
    h.check("same_path/nothing written", not os.path.exists(out))


def case_output_aliases_are_resolved_not_compared_as_strings(h, tmp):
    """Two spellings of one file are one file, and the guard has to know it.

    Comparing absolute-path strings misses every alias the filesystem itself
    resolves. Two are checked here: a path with a redundant ``..`` segment,
    which aliases everywhere, and a case-only difference, which aliases on the
    normally case-insensitive Windows filesystem this project runs on and does
    not on a case-sensitive one. The case-only assertion follows what the
    filesystem under the fixture actually does, measured rather than assumed,
    because a guard that rejected two genuinely distinct files would be a
    different bug of the same size.
    """
    rows = default_electrodes()
    units = band_units()
    case_dir = os.path.join(tmp, "aliases")
    nested = os.path.join(case_dir, "nested")
    os.makedirs(nested, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    write_raw(raw_path, rows, 0.0, EXTENT_S)
    write_processed(processed_path, rows, units)
    session = session_id("aliases")
    install_local_assets([(session, raw_path, processed_path)])

    def attempt(out, records):
        """Return the SystemExit message, or None when the pair was accepted."""
        try:
            CLI.parse_args(["--session", session, "--probe", PROBES[0],
                            "--target", TARGET, "--assets-cache",
                            os.path.join(case_dir, "assets.json"),
                            "--out", out, "--records", records])
        except SystemExit as exc:
            return str(exc.code)
        return None

    plain = os.path.join(case_dir, "verdict.txt")
    detoured = os.path.join(nested, "..", "verdict.txt")
    h.check("aliases/detour_caught",
            "same path" in str(attempt(plain, detoured)), str(attempt(plain, detoured)))

    upper = os.path.join(case_dir, "Verdict.txt")
    lower = os.path.join(case_dir, "verdict.txt")
    with open(upper, "w", encoding="utf-8") as handle:
        handle.write("an earlier verdict\n")
    try:
        case_insensitive = os.path.samefile(upper, lower)
    except OSError:
        case_insensitive = False
    refused = attempt(upper, lower)
    if case_insensitive:
        h.check("aliases/case_alias_caught",
                refused is not None and "same path" in refused, repr(refused))
    else:
        h.check("aliases/case_distinct_kept", refused is None,
                repr(refused))
    h.check("aliases/two_real_paths_allowed",
            attempt(plain, os.path.join(case_dir, "record.json")) is None)
    os.remove(upper)


def case_the_packet_command_runs_standalone(h, tmp):
    """The command works from the packet with nothing injected into its path.

    Everything else in this harness imports the command by path with the
    packet's ``scripts/`` folder already on ``sys.path``, which is exactly the
    condition that hid the command being unrunnable on its own before it moved
    into the packet. A reader running it from the packet has no such help, so
    this runs it as a subprocess with ``PYTHONPATH`` cleared and requires it to
    reach its own ``--help``.
    """
    import subprocess
    command = os.path.join(PACKET_SCRIPTS, "measure_host_drift.py")
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    result = subprocess.run([sys.executable, command, "--help"],
                            capture_output=True, text=True, cwd=tmp, env=env)
    h.equal("standalone/help_exits_cleanly", result.returncode, 0)
    h.check("standalone/help_describes_gate", "--gate" in result.stdout,
            result.stdout[-200:] + result.stderr[-200:])
    h.check("standalone/help_is_ascii",
            all(ord(char) < 128 for char in result.stdout), result.stdout[-200:])


def case_input_error_clears_the_earlier_verdict(h, tmp):
    """A failed rerun does not leave the previous run's verdict at its own paths.

    The exit status distinguishes the two runs; the files did not. A report that
    belongs to a different run is the kind of artifact that gets read later
    without its exit status beside it.
    """
    rows = default_electrodes()
    units = band_units()
    first = run_case(
        tmp, "stale_outputs",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    h.equal("stale/first run wrote a verdict", first["status"], 0)
    second = run_case(
        tmp, "stale_outputs",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units,
                                  depth_description="Distance from the probe tip."))
    h.check("stale/second run failed", second["status"] != 0, str(second["status"]))
    h.check("stale/report is gone", second["text"] is None)
    h.check("stale/record is gone", second["record"] is None)
    h.check("stale/files removed from disk",
            not os.path.exists(first["out"])
            and not os.path.exists(os.path.join(second["dir"], "record.json")))


def case_records_wording_is_conditional(h, tmp):
    """The report only points at the JSON record when one was actually written."""
    rows = default_electrodes()
    units = band_units()
    case_dir = os.path.join(tmp, "no_records")
    os.makedirs(case_dir, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    write_raw(raw_path, rows, 0.0, EXTENT_S)
    write_processed(processed_path, rows, units)
    session = session_id("no_records")
    install_local_assets([(session, raw_path, processed_path)])
    out = os.path.join(case_dir, "report.txt")
    status = CLI.main(["--session", session, "--probe", PROBES[0], "--target", TARGET,
                       "--assets-cache", os.path.join(case_dir, "assets.json"),
                       "--out", out])
    with open(out, "r", encoding="utf-8") as handle:
        text = handle.read()
    h.equal("no_records/status", status, 0)
    h.check("no_records/says it was not written", "not written, because --records" in text)
    h.check("no_records/does not claim one exists",
            "in the JSON record written beside this report" not in text)


def case_report_names_the_new_confirmations(h, tmp):
    """The report carries every confirmation and cost the command now performs."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "report_confirmations",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    text = result["text"] or ""
    h.equal("confirmations/status", result["status"], 0)
    for required in ("structural columns", "asset pair identity",
                     "conversion provenance", "raw asset provenance",
                     "session reference time",
                     "AP timestamp coverage", "stored payload", "block transfer",
                     "peak resident arrays", "live python structures",
                     "hdf5 chunk cache", "combined peak resident",
                     "pinned at 40 um"):
        h.check("confirmations/report carries %r" % required, required in text)
    h.check("confirmations/report is ascii", all(ord(char) < 128 for char in text))
    # RC-004's wording obligations, checked here rather than left to a reader.
    # The report must say what the reference-time check is worth, must not
    # promote it into an identification of the clock, and must say that version
    # equality is reported rather than gated -- an unchanged sentence that a
    # code change has made false is the most productive finding class this
    # project has, and these are the sentences the change put at risk.
    h.check("confirmations/report bounds what agreement establishes",
            "necessary declared" in text and "NOT an identification of the clock" in text,
            text[:0])
    h.check("confirmations/report says version equality does not gate",
            "gate nothing" in text and "admitted 0 of the 71 sessions" in text, text[:0])
    h.check("confirmations/report does not claim the pair names one version",
            "name one version" not in text, text[:0])


CASES = (
    case_clean_band_passes,
    case_labels_recorded_not_filtered,
    case_common_ramp_fails_strict_passes_relaxed,
    case_plan_only_reads_no_spikes,
    case_plan_bytes_follow_stored_itemsize,
    case_transfer_ceiling_refuses,
    case_ceiling_refuses_before_the_bytes_move,
    case_the_processed_ceiling_still_refuses_before_its_first_fetch,
    case_a_non_iso_separator_is_an_input_error,
    case_the_grammar_admits_every_measured_reference_time,
    case_pre_origin_spikes_counted,
    case_head_partial_reported,
    case_grid_extent_is_t_last,
    case_audit_values_come_from_the_estimator,
    case_too_few_units_is_unmeasurable,
    case_invalid_bin_is_unmeasurable,
    case_repeat_run_is_identical,
    case_ragged_indices_must_agree,
    case_ragged_index_must_end_at_column_length,
    case_infinite_depth_is_refused,
    case_missing_depth_is_bounded_rather_than_refused,
    case_missing_depths_can_pause_a_passing_gate,
    case_no_missing_depth_skips_the_layer,
    case_unsorted_times_are_refused,
    case_depth_unit_must_be_stated,
    case_out_of_range_electrode_is_refused,
    case_cross_probe_electrode_is_refused,
    case_electrode_tables_must_agree,
    case_missing_timestamps_is_refused,
    case_containment_violation_is_refused,
    case_unknown_probe_is_refused,
    case_series_name_containing_the_probe_is_not_ownership,
    case_exact_series_ownership_still_selects,
    case_missing_session_is_refused,
    case_plan_only_transfers_less,
    case_band_edges_are_inclusive,
    case_empty_unit_is_carried_not_included,
    case_threshold_cannot_be_typed,
    case_report_is_ascii_and_complete,
    case_io_counts_every_read,
    case_only_band_units_are_read,
    case_provenance_is_reported_verbatim,
    case_missing_processed_provenance_is_an_input_error,
    case_missing_raw_provenance_is_an_input_error,
    case_foreign_conversion_is_an_input_error,
    case_negated_conversion_statement_is_an_input_error,
    case_unequal_conversion_versions_are_admitted,
    case_one_instant_written_at_two_offsets_is_admitted,
    case_reference_time_disagreement_is_an_input_error,
    case_the_pair_check_runs_before_the_payload,
    case_missing_reference_time_is_an_input_error,
    case_timezone_naive_reference_time_is_an_input_error,
    case_malformed_reference_time_is_an_input_error,
    case_refused_reference_time_is_not_an_agreement,
    case_provenance_token_is_case_insensitive,
    case_vlen_provenance_is_refused_before_it_is_spent,
    case_budget_admits_a_value_it_can_afford,
    case_transfer_budget_refuses_at_the_block_layer,
    case_provenance_transfer_is_bounded_at_the_default_block,
    case_command_reports_a_block_readers_expansion,
    case_a_ceiling_refusal_is_not_recorded_as_a_provenance_marker,
    case_a_cached_value_is_still_capped,
    case_oversize_stored_provenance_is_not_read,
    case_null_distribution_is_reported,
    case_fractional_ragged_offsets_are_refused,
    case_float_ragged_index_is_refused_even_when_whole,
    case_fractional_electrode_is_refused,
    case_integral_float_column_is_accepted_and_named,
    case_short_unit_column_is_refused,
    case_cross_subject_pair_is_refused,
    case_paired_stems_must_match,
    case_timestamps_must_cover_the_data,
    case_band_gap_is_pinned,
    case_ceiling_bounds_the_block_transfer,
    case_ceiling_can_bind_on_resident_memory,
    case_ceiling_covers_cache_and_arrays_together,
    case_chunked_columns_are_placed_from_the_chunk_index,
    case_fragmented_chunks_are_still_bounded,
    case_unplaceable_columns_fall_back_to_the_whole_file,
    case_plan_separates_the_costs,
    case_output_paths_must_differ,
    case_output_aliases_are_resolved_not_compared_as_strings,
    case_the_packet_command_runs_standalone,
    case_input_error_clears_the_earlier_verdict,
    case_records_wording_is_conditional,
    case_report_names_the_new_confirmations,
)


def main():
    """Run every case against fresh local fixtures and report the totals."""
    global CLI
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--keep", action="store_true",
                        help="keep the fixture directory instead of deleting it")
    parser.add_argument("--tmp-root", default=None,
                        help="directory to build fixtures in (default: a temp dir)")
    args = parser.parse_args()

    CLI = load_cli()
    install_local_file()

    tmp = args.tmp_root or tempfile.mkdtemp(prefix="drift_reader_")
    os.makedirs(tmp, exist_ok=True)
    harness = Harness()
    started = time.time()
    try:
        for case in CASES:
            print("[case] %s" % case.__name__, flush=True)
            try:
                case(harness, tmp)
            except Exception as exc:  # noqa: BLE001 - a case that raises is a failed case
                # Without this, one unexpected exception ends the run and every
                # case after it is silently not run: the totals then describe a
                # smaller suite than the one that was asked for. An uncaught
                # exception from the command is also a real defect -- the
                # command's own contract is a named exit, not a traceback.
                harness.check("%s/raised" % case.__name__, False,
                              "%s: %s" % (type(exc).__name__, exc))
                traceback.print_exc()
    finally:
        # Close every local reader a case left open before the tree is removed.
        # On Windows an open handle makes rmtree fail, and ignore_errors=True
        # makes it fail *silently*: 111 drift_reader_* directories had
        # accumulated in the system temp folder by Session 31 because of this.
        # Recorded then rather than repaired, because the file was mid-review;
        # repaired here because it is the same file being handed over.
        for reader in READERS:
            try:
                reader.close()
            except OSError:
                pass
        del READERS[:]
        if not args.keep:
            shutil.rmtree(tmp, ignore_errors=True)
            if os.path.exists(tmp):
                print("[warn] fixture directory survived removal: %s" % tmp)

    elapsed = time.time() - started
    print("")
    print("%d checks, %d failed, %.1f s" % (harness.passed + len(harness.failed),
                                            len(harness.failed), elapsed))
    for name, detail in harness.failed:
        print("  FAILED %s %s" % (name, detail))
    return 1 if harness.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
