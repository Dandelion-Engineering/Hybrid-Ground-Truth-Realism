"""Independent RC-005 Round-1 probes for command disposition and memory scope.

The RC-005 owner suite proves that the structured record can pause a gate that
passed.  These probes inspect two adjacent properties the suite does not assert:

1. the command's final console verdict must agree with that reconciled record;
2. the reader's published resident-memory terms must include the new retained
   per-spike missing-depth masks.  The probe also records the command's later
   split copies as a separate accounting follow-up; the present ceiling declares
   a read-only scope, so those copies are not treated as this review's blocker.

Only generated local HDF5 fixtures are used.  No archive or network resource is
opened.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Codex/tools/probe_rc005_round1.py" --repo-root .
"""

import argparse
import importlib.util
import os
import shutil
import sys
import tempfile

import numpy as np


def load_module(path, name):
    """Load one Python source file by absolute path.

    Args:
        path: source path.
        name: private module name for this probe.

    Returns:
        The loaded module object.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv=None):
    """Run the two generated-fixture probes and return zero when both reproduce."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="Hybrid Ground Truth Realism repository root")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.repo_root)
    packet_scripts = os.path.join(root, "Reproducibility Packet", "scripts")
    if packet_scripts not in sys.path:
        sys.path.insert(0, packet_scripts)

    harness_path = os.path.join(
        root, "agents", "Claude", "tools", "test_measure_host_drift.py")
    harness = load_module(harness_path, "rc005_owner_harness")
    harness.CLI = harness.load_cli()
    harness.install_local_file()

    tmp = tempfile.mkdtemp(prefix="rc005_codex_round1_")
    try:
        rows = harness.default_electrodes()
        units = harness.band_units()
        in_bin = np.flatnonzero(
            (units[2]["times"] >= 300.0) & (units[2]["times"] < 360.0))
        units = harness._nan_at(
            units, [(2, int(index)) for index in in_bin[:in_bin.size - 5]])
        result = harness.run_case(
            tmp,
            "reconciled_pause",
            lambda path: harness.write_raw(path, rows, 0.0, harness.EXTENT_S),
            lambda path: harness.write_processed(path, rows, units),
            capture=True,
        )
        record = result["record"]
        transcript = result["stdout"] or ""
        final_console = next(
            (line for line in reversed(transcript.splitlines())
             if line.startswith("[drift] verdict:")), "<missing>")
        completion_console = next(
            (line for line in transcript.splitlines()
             if line.startswith("[drift] completion disposition:")), "<missing>")
        disposition_contradiction = bool(
            result["status"] == 0
            and record
            and record["verdict"]["passed"]
            and record["disposition"]["disposition"] == "unmeasurable"
            and record["disposition"]["advances"] is False
            and completion_console.endswith("unmeasurable")
            and "passed=True" in final_console
        )

        band = record["band"]
        read = harness.CLI.archive_units.read_band_units(
            result["processed"], os.path.getsize(result["processed"]),
            64 * 1024, harness.PROBES[0],
            band["depth_lo_um"], band["depth_hi_um"], max_bytes=None)
        n_spikes = int(read["plan"]["n_spikes"])
        complete_array_bytes = sum(
            int(unit["times"].nbytes + unit["depths"].nbytes)
            for unit in read["band_units"])
        mask_bytes = sum(
            int(unit["missing_depths"].nbytes) for unit in read["band_units"])
        observed_copy_bytes = 0
        for unit in read["band_units"]:
            finite_times, finite_depths, _ = harness.CLI.missing_depth.split_unit(
                unit["times"], unit["depths"])
            observed_copy_bytes += int(finite_times.nbytes + finite_depths.nbytes)
        expected_complete_bytes = 16 * n_spikes
        mask_unbudgeted = bool(
            complete_array_bytes == expected_complete_bytes
            and mask_bytes == n_spikes
            and read["plan"]["resident_bytes"]
            == expected_complete_bytes
            + max(unit["n_spikes"] for unit in read["band_units"])
            * (read["plan"]["time_layout"]["itemsize"]
               + read["plan"]["depth_layout"]["itemsize"])
        )

        projected_spikes = 3_160_311
        projected_missing = 231
        projected_mask_bytes = projected_spikes
        projected_observed_copy_bytes = 16 * (projected_spikes - projected_missing)

        print("RC-005 Round-1 independent probes")
        print("generated fixtures only; no archive or network read")
        print("")
        print("disposition_console_contradiction=%s" % disposition_contradiction)
        print("  completion_line=%s" % completion_console)
        print("  final_console_line=%s" % final_console)
        print("  record_gate_passed=%s" % record["verdict"]["passed"])
        print("  record_final_disposition=%s" % record["disposition"]["disposition"])
        print("  record_advances=%s" % record["disposition"]["advances"])
        print("")
        print("retained_mask_unbudgeted=%s" % mask_unbudgeted)
        print("  synthetic_spikes=%d" % n_spikes)
        print("  planned_complete_array_bytes=%d" % expected_complete_bytes)
        print("  returned_complete_array_bytes=%d" % complete_array_bytes)
        print("  returned_mask_bytes_not_in_formula=%d" % mask_bytes)
        print("  command_observed_copy_bytes_not_in_reader_plan=%d"
              % observed_copy_bytes)
        print("  rank1_projected_mask_bytes=%d" % projected_mask_bytes)
        print("  rank1_projected_observed_copy_bytes=%d"
              % projected_observed_copy_bytes)
        print("  rank1_projected_new_retained_bytes=%d"
              % (projected_mask_bytes + projected_observed_copy_bytes))
        return 0 if disposition_contradiction and mask_unbudgeted else 1
    finally:
        for reader in harness.READERS:
            try:
                reader.close()
            except OSError:
                pass
        del harness.READERS[:]
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
