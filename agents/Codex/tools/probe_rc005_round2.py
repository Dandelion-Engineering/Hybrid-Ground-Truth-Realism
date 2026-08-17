"""Independently verify the two RC-005 Round-2 repairs on local fixtures.

The owner suite now covers the repaired console and resident-memory paths. This
probe checks the same properties from their external boundaries: the command's
last non-empty line must positively encode the reconciled record, and the exact
mask-inclusive peak must be admitted while the peak with that retained term
removed is refused.

Only generated local HDF5 fixtures are used. No archive, network resource, or
candidate asset is opened.

Example
-------
Run from the project root with the project virtual environment::

    ./venv/Scripts/python.exe agents/Codex/tools/probe_rc005_round2.py --repo-root .
"""

import argparse
import importlib.util
import os
import shutil
import sys
import tempfile

import numpy as np


def load_module(path, name):
    """Load one Python file by absolute path under a private module name."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv=None):
    """Run the generated-fixture checks and return zero only when all pass."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="Hybrid Ground Truth Realism repository root")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.repo_root)
    packet_scripts = os.path.join(root, "Reproducibility Packet", "scripts")
    if packet_scripts not in sys.path:
        sys.path.insert(0, packet_scripts)

    harness = load_module(
        os.path.join(root, "agents", "Claude", "tools",
                     "test_measure_host_drift.py"),
        "rc005_round2_owner_harness",
    )
    harness.CLI = harness.load_cli()
    harness.install_local_file()

    failures = []

    def check(name, condition, detail=""):
        """Record and print one independent check."""
        label = "PASS" if condition else "FAIL"
        print("[%s] %s%s" % (label, name, " -- " + detail if detail else ""))
        if not condition:
            failures.append(name)

    tmp = tempfile.mkdtemp(prefix="rc005_codex_round2_")
    try:
        # F1: reconstruct the whole-command fixture on which the point gate
        # passes but the missing-depth layer pauses the candidate.
        rows = harness.default_electrodes()
        units = harness.band_units()
        in_bin = np.flatnonzero(
            (units[2]["times"] >= 300.0) & (units[2]["times"] < 360.0))
        units = harness._nan_at(
            units, [(2, int(index)) for index in in_bin[:in_bin.size - 5]])
        result = harness.run_case(
            tmp,
            "positive_console_decision",
            lambda path: harness.write_raw(path, rows, 0.0, harness.EXTENT_S),
            lambda path: harness.write_processed(path, rows, units),
            capture=True,
        )
        record = result["record"]
        lines = [line for line in (result["stdout"] or "").splitlines()
                 if line.strip()]
        last = lines[-1] if lines else "<missing>"
        diagnostic = [line for line in lines if "passed=" in line]
        check("paused fixture completes", result["status"] == 0,
              repr(result["status"]))
        check("point gate passes while the final record pauses",
              bool(record and record["verdict"]["passed"]
                   and record["disposition"]["disposition"] == "unmeasurable"
                   and record["disposition"]["advances"] is False),
              repr(record and record.get("disposition")))
        expected_last = ("[drift] decision: unmeasurable; advances=False; "
                         "gate and completion bound conflict=False")
        check("last line positively equals the reconciled decision",
              last == expected_last, repr(last))
        check("the only point-gate line labels itself diagnostic",
              len(diagnostic) == 1
              and "diagnostic, not the decision" in diagnostic[0]
              and "passed=True" in diagnostic[0],
              repr(diagnostic))

        # F2: derive the expected mask and resident terms from the fixture,
        # not from the plan under test. The former pre-repair peak is the exact
        # current peak minus the mask term; that ceiling must now refuse.
        rows = harness.default_electrodes()
        units = harness.band_units()
        lo, hi = harness.band_bounds()
        case_dir = os.path.join(tmp, "exact_mask_boundary")
        os.makedirs(case_dir, exist_ok=True)
        processed = os.path.join(case_dir, "processed.nwb")
        harness.write_processed(processed, rows, units)
        size = os.path.getsize(processed)
        block = 16 * 1024
        harness.CLI.archive_units.RemoteFile = harness.BlockLocalFile
        plan = harness.CLI.archive_units.read_band_units(
            processed, size, block, harness.PROBES[0], lo, hi,
            plan_only=True,
        )["plan"]
        spikes = sum(len(unit["times"]) for unit in units)
        largest = max(len(unit["times"]) for unit in units)
        expected_masks = spikes * np.dtype(np.bool_).itemsize
        expected_resident = (
            spikes * 16
            + expected_masks
            + largest * (plan["time_layout"]["itemsize"]
                         + plan["depth_layout"]["itemsize"])
        )
        expected_peak = (
            plan["cache_bound_bytes"]
            + expected_resident
            + plan["structures_bytes"]
            + plan["library_cache_bytes"]
        )
        check("mask term is one NumPy bool per spike",
              plan["mask_bytes"] == expected_masks,
              "%d against %d" % (plan["mask_bytes"], expected_masks))
        check("resident formula includes the independently derived mask term",
              plan["resident_bytes"] == expected_resident,
              "%d against %d" % (plan["resident_bytes"], expected_resident))
        check("peak remains the sum of the four top-level terms",
              plan["peak_resident_bytes"] == expected_peak,
              "%d against %d" % (plan["peak_resident_bytes"], expected_peak))

        omitted_ceiling = expected_peak - expected_masks
        refusal = None
        try:
            harness.CLI.archive_units.read_band_units(
                processed, size, block, harness.PROBES[0], lo, hi,
                max_bytes=omitted_ceiling,
            )
        except ValueError as exc:
            refusal = str(exc)
        check("the old mask-omitting peak is refused",
              refusal is not None
              and "peak_resident_bytes is above" in refusal
              and ("of which %d bytes are the retained missing-depth masks"
                   % expected_masks) in refusal,
              repr(refusal))

        admitted = harness.CLI.archive_units.read_band_units(
            processed, size, block, harness.PROBES[0], lo, hi,
            max_bytes=expected_peak,
        )
        held_masks = sum(
            unit["missing_depths"].nbytes for unit in admitted["band_units"])
        check("the exact mask-inclusive peak is admitted",
              admitted["plan"]["peak_resident_bytes"] == expected_peak,
              "%d against %d"
              % (admitted["plan"]["peak_resident_bytes"], expected_peak))
        check("the returned masks occupy exactly the charged bytes",
              held_masks == expected_masks,
              "%d against %d" % (held_masks, expected_masks))

        print("")
        print("RC-005 Round-2 independent probe: %d checks, %d failed"
              % (10, len(failures)))
        print("generated fixtures only; no archive or network read")
        return 1 if failures else 0
    finally:
        harness.CLI.archive_units.RemoteFile = harness.LocalFile
        for reader in harness.READERS:
            try:
                reader.close()
            except OSError:
                pass
        del harness.READERS[:]
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
