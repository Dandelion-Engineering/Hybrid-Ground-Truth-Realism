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
import hashlib
import importlib.util
import io
import os
import shutil
import sys
import tempfile
import time

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
        self.size = int(size)
        self.n_requests = 0
        self.n_bytes = 0

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
        data = self._handle.read(n if n is not None and n >= 0 else -1)
        self.n_requests += 1
        self.n_bytes += len(data)
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
              series_names=None):
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
    """
    names = series_names or ["ElectricalSeries%sAP" % probe for probe in PROBES]
    with h5py.File(path, "w") as handle:
        _write_electrode_table(handle, rows)
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


def write_processed(path, rows, units, depth_description=DEPTH_DESCRIPTION,
                    depth_dtype=np.float64, index_mutator=None, provenance=None):
    """Write a processed-asset-shaped file: an electrode table and a units table.

    Args:
        path: destination path.
        rows: electrode rows, normally the same list the raw file carries.
        units: a list of dicts with ``probe``, ``max_electrode``, ``label``,
            ``times`` and ``depths``.
        depth_description: the depth column's stored description.
        depth_dtype: storage dtype for the depth column, so a fixture can prove
            the reported byte cost follows the file's own item size.
        index_mutator: optional callable taking the two index lists and
            returning the pair actually written, for the malformed-index cases.
        provenance: optional mapping of NWB path to stored string, for the
            conversion-provenance fixture.
    """
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
        for nwb_path, value in (provenance or {}).items():
            dataset = handle.create_dataset(nwb_path, data=value, dtype=dt)
            dataset.attrs["file_name"] = "%s.py" % nwb_path.rsplit("/", 1)[-1]
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
        time_column = node.create_dataset("spike_times",
                                          data=times.astype(np.float64))
        time_column.attrs["description"] = TIME_DESCRIPTION
        depth_column = node.create_dataset("spike_distances_from_probe_tip_um",
                                           data=depths.astype(depth_dtype))
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
             gate="strict", session=None):
    """Build one fixture pair, run the command, and return its outcome.

    Args:
        tmp_root: directory to build the fixture in.
        name: case name, used as the subdirectory name.
        raw_writer: callable taking the raw file's path.
        processed_writer: callable taking the processed file's path.
        argv_extra: extra command-line arguments.
        gate: which pre-declared threshold to apply.
        session: session identifier, defaulting to the case name.

    Returns:
        A dict with ``status`` (0, or the SystemExit message), ``out`` (the
        report path), ``text`` (its contents or None) and ``record`` (the JSON
        record or None).
    """
    import json
    session = session_id(session or name)
    case_dir = os.path.join(tmp_root, name)
    os.makedirs(case_dir, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    raw_writer(raw_path)
    processed_writer(processed_path)
    install_local_assets([(session, raw_path, processed_path)])
    out = os.path.join(case_dir, "report.txt")
    records = os.path.join(case_dir, "record.json")
    argv = ["--session", session, "--probe", PROBES[0], "--target", TARGET,
            "--assets-cache", os.path.join(case_dir, "assets.json"),
            "--gate", gate, "--out", out, "--records", records]
    argv.extend(argv_extra)
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
    return {"status": status, "out": out, "text": text, "record": record,
            "raw": raw_path, "processed": processed_path, "dir": case_dir}


def load_cli():
    """Import ``measure_host_drift.py`` from beside this harness.

    The command lives in the agent workspace until it has actually been executed
    against a candidate, at which point it moves into the packet's ``scripts/``
    folder unchanged. Importing it by path rather than by package keeps that
    move a copy with no edit.
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "measure_host_drift.py")
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
        h.equal("plan/%s bytes" % tag, read["plan"]["bytes"], spikes * per_spike)


def case_transfer_ceiling_refuses(h, tmp):
    """A band larger than the declared ceiling stops before any spike is read."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "ceiling",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units),
        argv_extra=["--max-mib", "0.001"])
    h.check("ceiling/refused", "above the declared ceiling" in str(result["status"]),
            str(result["status"]))
    h.check("ceiling/no report", result["text"] is None)


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


def case_non_finite_depth_is_refused(h, tmp):
    """A NaN depth stops the command instead of reaching the median."""
    rows = default_electrodes()
    units = band_units()
    units[1]["depths"] = units[1]["depths"].copy()
    units[1]["depths"][7] = np.nan
    result = run_case(
        tmp, "nonfinite_depth",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    h.check("nonfinite/refused", "non-finite spike depths" in str(result["status"]),
            str(result["status"]))
    h.check("nonfinite/no report", result["text"] is None)


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


def case_ambiguous_series_is_refused(h, tmp):
    """Two AP series matching one probe stops rather than guessing the clock."""
    rows = default_electrodes()
    units = band_units()
    names = ["ElectricalSeriesProbe00AP", "ElectricalSeriesProbe00CopyAP"]
    result = run_case(
        tmp, "ambiguous_series",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S, series_names=names),
        lambda p: write_processed(p, rows, units))
    h.check("ambiguous/refused", "AP series match probe" in str(result["status"]),
            str(result["status"]))
    h.check("ambiguous/no report", result["text"] is None)


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
            full["io"]["bytes"] - planned["io"]["bytes"] >= planned["plan"]["bytes"],
            "difference %d, planned %d"
            % (full["io"]["bytes"] - planned["io"]["bytes"], planned["plan"]["bytes"]))
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
                     "raw_electrodes", "raw_timing", "processed_units"):
        h.check("report/carries %r" % required, required in text)
    h.check("report/sources are ascii",
            all(ord(char) < 128
                for path in (os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "measure_host_drift.py"),
                             os.path.join(PACKET_SCRIPTS, "utils", "archive_units.py"))
                for char in io.open(path, encoding="utf-8").read()))


def case_io_counts_every_read(h, tmp):
    """The reported transfer is all three reads, not only the units table."""
    rows = default_electrodes()
    units = band_units()
    result = run_case(
        tmp, "io_counts",
        lambda p: write_raw(p, rows, 0.0, EXTENT_S),
        lambda p: write_processed(p, rows, units))
    io_record = result["record"]["io"]
    h.equal("io/status", result["status"], 0)
    for source in ("raw_electrodes", "raw_timing", "processed_units"):
        h.check("io/%s counted" % source, io_record[source]["bytes"] > 0)
        h.check("io/%s requested" % source, io_record[source]["requests"] > 0)
    h.equal("io/total bytes", io_record["bytes"],
            sum(io_record[source]["bytes"]
                for source in ("raw_electrodes", "raw_timing", "processed_units")))
    h.equal("io/total requests", io_record["requests"],
            sum(io_record[source]["requests"]
                for source in ("raw_electrodes", "raw_timing", "processed_units")))


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



def case_provenance_is_recorded_not_required(h, tmp):
    """Conversion provenance present on the asset is reported verbatim."""
    rows = default_electrodes()
    units = band_units()
    provenance = {
        "general/source_script": "ibl-to-nwb 54030ac4eb40a74978ac1f6ef6e966278b9d3f34",
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


CASES = (
    case_clean_band_passes,
    case_labels_recorded_not_filtered,
    case_common_ramp_fails_strict_passes_relaxed,
    case_plan_only_reads_no_spikes,
    case_plan_bytes_follow_stored_itemsize,
    case_transfer_ceiling_refuses,
    case_pre_origin_spikes_counted,
    case_head_partial_reported,
    case_grid_extent_is_t_last,
    case_audit_values_come_from_the_estimator,
    case_too_few_units_is_unmeasurable,
    case_invalid_bin_is_unmeasurable,
    case_repeat_run_is_identical,
    case_ragged_indices_must_agree,
    case_ragged_index_must_end_at_column_length,
    case_non_finite_depth_is_refused,
    case_unsorted_times_are_refused,
    case_depth_unit_must_be_stated,
    case_out_of_range_electrode_is_refused,
    case_cross_probe_electrode_is_refused,
    case_electrode_tables_must_agree,
    case_missing_timestamps_is_refused,
    case_containment_violation_is_refused,
    case_unknown_probe_is_refused,
    case_ambiguous_series_is_refused,
    case_missing_session_is_refused,
    case_plan_only_transfers_less,
    case_band_edges_are_inclusive,
    case_empty_unit_is_carried_not_included,
    case_threshold_cannot_be_typed,
    case_report_is_ascii_and_complete,
    case_io_counts_every_read,
    case_only_band_units_are_read,
    case_provenance_is_recorded_not_required,
    case_null_distribution_is_reported,
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
            case(harness, tmp)
    finally:
        if not args.keep:
            shutil.rmtree(tmp, ignore_errors=True)

    elapsed = time.time() - started
    print("")
    print("%d checks, %d failed, %.1f s" % (harness.passed + len(harness.failed),
                                            len(harness.failed), elapsed))
    for name, detail in harness.failed:
        print("  FAILED %s %s" % (name, detail))
    return 1 if harness.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
