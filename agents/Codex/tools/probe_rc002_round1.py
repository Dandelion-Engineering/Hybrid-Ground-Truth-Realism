"""Adversarial Round-1 probes for RC-002's archive-reading drift command.

These probes reuse Claude's synthetic NWB writers but exercise paths the owner
harness does not cover.  They are evidence about the exact RC-002 candidate,
not a replacement for its acceptance suite and not evidence about any real
recording.

Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe agents/Codex/tools/probe_rc002_round1.py
"""

import importlib.util
import io
import json
import os
import shutil
import tempfile

import h5py
import numpy as np


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OWNER_HARNESS_PATH = os.path.join(
    PROJECT_ROOT, "agents", "Claude", "tools", "test_measure_host_drift.py")


def load_owner_harness():
    """Load Claude's fixture writers and command importer by exact path."""
    spec = importlib.util.spec_from_file_location("owner_rc002_harness", OWNER_HARNESS_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CLI = module.load_cli()
    module.install_local_file()
    return module


class BlockLocalFile(io.RawIOBase):
    """Local stand-in with RemoteFile's fixed-block cache and counters."""

    def __init__(self, url, size, block=None, timeout=None, retries=None):
        self._handle = open(url, "rb")
        self.size = int(size)
        self.block = int(block)
        self._pos = 0
        self._cache = {}
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
        """Move the cursor with RemoteFile-compatible semantics."""
        if whence == io.SEEK_SET:
            new = offset
        elif whence == io.SEEK_CUR:
            new = self._pos + offset
        elif whence == io.SEEK_END:
            new = self.size + offset
        else:
            raise ValueError("unsupported whence %r" % whence)
        if new < 0:
            raise ValueError("negative seek position %r" % new)
        self._pos = new
        return new

    def tell(self):
        """Return the current cursor."""
        return self._pos

    def _fetch(self, index):
        """Fetch and cache one complete fixed-width block."""
        if index not in self._cache:
            lo = index * self.block
            self._handle.seek(lo)
            payload = self._handle.read(min(self.block, self.size - lo))
            self._cache[index] = payload
            self.n_requests += 1
            self.n_bytes += len(payload)
        return self._cache[index]

    def read(self, n=-1):
        """Read through the fixed-block cache."""
        remaining = self.size - self._pos
        if remaining <= 0:
            return b""
        want = remaining if n is None or n < 0 else min(n, remaining)
        out = bytearray()
        while want > 0:
            index, offset = divmod(self._pos, self.block)
            chunk = self._fetch(index)[offset:offset + want]
            if not chunk:
                break
            out += chunk
            self._pos += len(chunk)
            want -= len(chunk)
        return bytes(out)

    def readinto(self, buffer):
        """Read into a caller-provided buffer."""
        payload = self.read(len(buffer))
        buffer[:len(payload)] = payload
        return len(payload)

    def close(self):
        """Close the backing file."""
        if not self._handle.closed:
            self._handle.close()
        super().close()


class Probe:
    """Collect compact evidence and return non-zero if a construction fails."""

    def __init__(self):
        self.passed = 0
        self.failed = []

    def check(self, name, condition, detail=""):
        """Record one expected construction."""
        if condition:
            self.passed += 1
            print("PASS %s%s" % (name, " (%s)" % detail if detail else ""))
        else:
            self.failed.append((name, detail))
            print("FAIL %s %s" % (name, detail))


def replace_dataset(handle, path, values):
    """Replace one HDF5 dataset while keeping its path fixed."""
    del handle[path]
    handle.create_dataset(path, data=values)


def fractional_index_case(owner, probe, tmp):
    """Show equal fractional ragged offsets are silently truncated to integers."""
    rows = owner.default_electrodes()
    units = owner.band_units()

    def write_processed(path):
        owner.write_processed(path, rows, units)
        with h5py.File(path, "r+") as handle:
            times = handle["units/spike_times_index"][:].astype(np.float64)
            depths = handle["units/spike_distances_from_probe_tip_um_index"][:].astype(
                np.float64)
            times[0] += 0.75
            depths[0] += 0.75
            replace_dataset(handle, "units/spike_times_index", times)
            replace_dataset(handle, "units/spike_distances_from_probe_tip_um_index", depths)

    result = owner.run_case(
        tmp, "fractional_indices",
        lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S),
        write_processed)
    probe.check(
        "fractional ragged offsets reach a verdict",
        result["status"] == 0 and result["record"] is not None,
        "status=%r" % result["status"])


def fractional_electrode_case(owner, probe, tmp):
    """Show a fractional max_electrode is silently truncated to a valid row."""
    rows = owner.default_electrodes()
    units = owner.band_units()

    def write_processed(path):
        owner.write_processed(path, rows, units)
        with h5py.File(path, "r+") as handle:
            values = handle["units/max_electrode"][:].astype(np.float64)
            values[0] += 0.75
            replace_dataset(handle, "units/max_electrode", values)

    result = owner.run_case(
        tmp, "fractional_electrode",
        lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S),
        write_processed)
    probe.check(
        "fractional max_electrode reaches a verdict",
        result["status"] == 0 and result["record"] is not None,
        "status=%r" % result["status"])


def timestamp_length_case(owner, probe, tmp):
    """Show an AP timestamp vector shorter than its data array is accepted."""
    rows = owner.default_electrodes()
    units = owner.band_units()

    def write_raw(path):
        owner.write_raw(path, rows, 0.0, owner.EXTENT_S)
        with h5py.File(path, "r+") as handle:
            target = "acquisition/ElectricalSeriesProbe00AP/timestamps"
            replace_dataset(handle, target, np.linspace(0.0, owner.EXTENT_S, 999))

    result = owner.run_case(
        tmp, "timestamp_length",
        write_raw,
        lambda path: owner.write_processed(path, rows, units))
    entry = result["record"] if result["record"] else {}
    probe.check(
        "mismatched AP data/timestamp lengths reach a verdict",
        result["status"] == 0 and entry.get("grid", {}).get("n_bins") == 15,
        "status=%r" % result["status"])


def mismatched_subject_case(owner, probe, tmp):
    """Show a raw/processed pair from different subjects is accepted as one session."""
    rows = owner.default_electrodes()
    units = owner.band_units()
    case_dir = os.path.join(tmp, "mismatched_subject")
    os.makedirs(case_dir, exist_ok=True)
    raw_path = os.path.join(case_dir, "raw.nwb")
    processed_path = os.path.join(case_dir, "processed.nwb")
    owner.write_raw(raw_path, rows, 0.0, owner.EXTENT_S)
    owner.write_processed(processed_path, rows, units)
    session = owner.session_id("mismatched_subject")
    assets = [
        {"asset_id": "raw-mismatch", "path": "sub-A/sub-A_ses-%s%s" % (
            session, owner.dandi.RAW_SUFFIX), "size": os.path.getsize(raw_path),
         "blob": raw_path},
        {"asset_id": "processed-mismatch", "path": "sub-B/sub-B_ses-%s%s" % (
            session, owner.dandi.PROCESSED_SUFFIX), "size": os.path.getsize(processed_path),
         "blob": processed_path},
    ]
    owner.dandi.list_assets = lambda *args, **kwargs: assets
    owner.dandi.blob_url = lambda asset: asset["blob"]
    out = os.path.join(case_dir, "report.txt")
    records = os.path.join(case_dir, "record.json")
    argv = ["--session", session, "--probe", owner.PROBES[0], "--target", owner.TARGET,
            "--assets-cache", os.path.join(case_dir, "assets.json"), "--out", out,
            "--records", records]
    try:
        status = owner.CLI.main(argv)
    except SystemExit as exc:
        status = str(exc.code)
    record = None
    if os.path.exists(records):
        with open(records, "r", encoding="utf-8") as handle:
            record = json.load(handle)
    probe.check(
        "cross-subject raw/processed pair reaches a verdict",
        status == 0 and record is not None and record.get("subject") == "A",
        "status=%r" % status)


def transfer_ceiling_case(owner, probe, tmp):
    """Show max_bytes accepts a read whose fixed-block transfer exceeds the ceiling."""
    rows = owner.default_electrodes()
    units = owner.band_units()
    case_dir = os.path.join(tmp, "transfer_ceiling_actual")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    owner.write_processed(processed, rows, units)
    lo, hi = owner.band_bounds()
    ceiling = 60_000
    owner.archive_units.RemoteFile = BlockLocalFile
    try:
        result = owner.archive_units.read_band_units(
            processed, os.path.getsize(processed), 1024 * 1024, owner.PROBES[0], lo, hi,
            max_bytes=ceiling)
    finally:
        owner.archive_units.RemoteFile = owner.LocalFile
    probe.check(
        "declared ceiling is below actual fixed-block transfer",
        result["plan"]["bytes"] < ceiling < result["io"]["bytes"],
        "plan=%r ceiling=%r actual=%r" % (
            result["plan"]["bytes"], ceiling, result["io"]["bytes"]))


def stale_output_case(owner, probe, tmp):
    """Show an input-error rerun leaves the earlier verdict files in place."""
    rows = owner.default_electrodes()
    units = owner.band_units()
    first = owner.run_case(
        tmp, "stale_output",
        lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S),
        lambda path: owner.write_processed(path, rows, units))
    second = owner.run_case(
        tmp, "stale_output",
        lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S),
        lambda path: owner.write_processed(
            path, rows, units, depth_description="Distance from the probe tip."))
    probe.check(
        "input-error rerun leaves prior verdict artifacts",
        first["status"] == 0 and second["status"] != 0
        and second["text"] == first["text"] and second["record"] == first["record"],
        "first=%r second=%r" % (first["status"], second["status"]))


def unpinned_band_threshold_case(owner, probe, tmp):
    """Show a typed non-declared gap merges target islands and includes intervening units."""
    rows = owner.default_electrodes()
    for row in rows[:owner.N_ROWS_PER_PROBE]:
        row["location"] = owner.OTHER_LOCATION
    for index in (10, 11, 12, 25, 26, 27, 28):
        rows[index]["location"] = owner.BAND_LOCATION
    units = owner.band_units()
    result = owner.run_case(
        tmp, "unpinned_band_threshold",
        lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S),
        lambda path: owner.write_processed(path, rows, units),
        argv_extra=["--max-gap-um", "1000"])
    record = result["record"] or {}
    probe.check(
        "typed non-declared gap produces a verdict over intervening non-target rows",
        result["status"] == 0
        and record.get("max_gap_um") == 1000.0
        and record.get("sets", {}).get("in_band", {}).get("n_total") == 8,
        "status=%r" % result["status"])


def main():
    """Run every independent construction against the exact RC-002 candidate."""
    owner = load_owner_harness()
    probe = Probe()
    tmp = tempfile.mkdtemp(prefix="rc002_round1_")
    try:
        fractional_index_case(owner, probe, tmp)
        fractional_electrode_case(owner, probe, tmp)
        timestamp_length_case(owner, probe, tmp)
        mismatched_subject_case(owner, probe, tmp)
        transfer_ceiling_case(owner, probe, tmp)
        stale_output_case(owner, probe, tmp)
        unpinned_band_threshold_case(owner, probe, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("%d constructions reproduced, %d failed" % (probe.passed, len(probe.failed)))
    return 1 if probe.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
