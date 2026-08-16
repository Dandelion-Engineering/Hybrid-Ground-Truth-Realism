"""Independent Round-1 probes for RC-003's archive-reading command.

Every fixture is local and synthetic.  The probes exercise three properties the
owner suite does not reject: the required conversion-provenance confirmation,
exact AP-series ownership, and whether a memory ceiling can stop a variable-
length provenance read before its bytes are spent.  A fourth diagnostic weighs
the post-read structures against the plan's structure-plus-array terms.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Codex/tools/probe_rc003_round1.py" --repo-root .
"""

import argparse
import importlib.util
import os
import sys
import tempfile

import h5py
import numpy as np


def load_module(name, path):
    """Import one module from an explicit path."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unique_size(*roots):
    """Measure reachable Python objects once each, including owned ndarray buffers."""
    seen = set()

    def walk(value, depth=0):
        identity = id(value)
        if identity in seen:
            return 0
        seen.add(identity)
        total = sys.getsizeof(value)
        if depth >= 8:
            return total
        if isinstance(value, dict):
            for key, item in value.items():
                total += walk(key, depth + 1)
                total += walk(item, depth + 1)
        elif isinstance(value, (list, tuple, set, frozenset)):
            for item in value:
                total += walk(item, depth + 1)
        return total

    return sum(walk(root) for root in roots)


def close_readers(owner):
    """Close every file object installed by the owner harness."""
    for reader in owner.READERS:
        reader.close()
    del owner.READERS[:]


def main(argv=None):
    """Run the independent fixtures and return nonzero unless all defects reproduce."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    args = parser.parse_args(argv)
    root = os.path.abspath(args.repo_root)
    owner_path = os.path.join(root, "agents", "Claude", "tools",
                              "test_measure_host_drift.py")
    owner = load_module("rc003_owner_harness", owner_path)
    owner.CLI = owner.load_cli()
    owner.install_local_file()
    units_module = owner.archive_units

    failures = []
    with tempfile.TemporaryDirectory(prefix="rc003_round1_") as tmp:
        rows = owner.default_electrodes()
        units = owner.band_units()

        # The approved selection specification says an asset whose conversion
        # provenance and values do not establish the common clock is an input
        # error.  The candidate and its owner suite deliberately accept the
        # opposite boundary: an asset with no provenance reaches a verdict.
        missing = owner.run_case(
            tmp, "missing_required_provenance",
            lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S),
            lambda path: owner.write_processed(path, rows, units))
        missing_reaches_verdict = (
            missing["status"] == 0
            and missing["record"] is not None
            and missing["record"]["provenance"] == {}
            and "passed" in missing["record"]["verdict"])
        print("missing_provenance_reaches_verdict=%s" % missing_reaches_verdict)
        if not missing_reaches_verdict:
            failures.append("missing-provenance construction did not reach a verdict")

        # Probe ownership is inferred with `probe in series_name`.  A different
        # probe name containing the requested token is therefore accepted as
        # the requested probe's clock, rather than rejected as an input error.
        impostor_name = "ElectricalSeriesProbe000AP"
        series = [{"name": impostor_name, "timing_source": "timestamps",
                   "n_timestamps": 1000, "shape": [1000, 4],
                   "t_first_s": 0.0, "t_last_s": owner.EXTENT_S}]
        selected = owner.CLI.select_ap_series(series, owner.PROBES[0])
        impostor_selected = selected["name"] == impostor_name
        print("substring_probe_impostor_selected=%s selected=%s"
              % (impostor_selected, selected["name"]))
        if not impostor_selected:
            failures.append("substring probe impostor was not selected")

        impostor = owner.run_case(
            tmp, "substring_probe_verdict",
            lambda path: owner.write_raw(
                path, rows, 0.0, owner.EXTENT_S,
                series_names=[impostor_name, "ElectricalSeriesProbe01AP"]),
            lambda path: owner.write_processed(path, rows, units))
        impostor_reaches_verdict = (
            impostor["status"] == 0
            and impostor["record"] is not None
            and "passed" in impostor["record"]["verdict"])
        print("substring_probe_impostor_reaches_verdict=%s"
              % impostor_reaches_verdict)
        if not impostor_reaches_verdict:
            failures.append("substring probe impostor did not reach a verdict")

        # A variable-length HDF5 string reports only its heap reference size.
        # The candidate consequently materializes it before the ceiling check.
        # Set a one-byte ceiling and show that megabytes have already been read
        # by the time the promised refusal occurs.
        spend_dir = os.path.join(tmp, "vlen_pre_ceiling")
        os.makedirs(spend_dir)
        processed = os.path.join(spend_dir, "processed.nwb")
        big = "p" * 2_000_000
        owner.write_processed(
            processed, rows, units,
            provenance={"general/source_script": big})
        lo, hi = owner.band_bounds()
        close_readers(owner)
        units_module.RemoteFile = owner.BlockLocalFile
        refused = None
        try:
            units_module.read_band_units(
                processed, os.path.getsize(processed), 4096, owner.PROBES[0],
                lo, hi, max_bytes=1, plan_only=True)
        except ValueError as exc:
            refused = str(exc)
        finally:
            units_module.RemoteFile = owner.LocalFile
        touched = owner.distinct_bytes(processed)
        spent_before_refusal = (
            refused is not None and "above the declared ceiling" in refused
            and touched > 1_000_000)
        print("vlen_bytes_spent_before_one_byte_refusal=%d defect=%s"
              % (touched, spent_before_refusal))
        if not spent_before_refusal:
            failures.append("variable-length provenance did not reproduce pre-ceiling spend")

        # Diagnostic: capture the exact roots used by plan_transfer, then weigh
        # those same roots after the per-unit arrays and bookkeeping have been
        # attached.  This is reported independently of the three blockers.
        structure_dir = os.path.join(tmp, "post_read_structures")
        os.makedirs(structure_dir)
        structure_path = os.path.join(structure_dir, "processed.nwb")
        empty_units = []
        for index in range(267):
            empty_units.append({
                "probe": owner.PROBES[0],
                "max_electrode": owner.BAND_ROW_LO
                + index % (owner.BAND_ROW_HI - owner.BAND_ROW_LO + 1),
                "label": "mua",
                "times": np.zeros(0, dtype=np.float64),
                "depths": np.zeros(0, dtype=np.float64),
            })
        owner.write_processed(structure_path, rows, empty_units)
        captured = {}
        original_plan = units_module.plan_transfer

        def capture_plan(band_units, scalars, time_layout, depth_layout,
                         block_bytes, file_size, spent_bytes=0, held=()):
            captured["roots"] = (band_units, scalars, time_layout, depth_layout) + tuple(held)
            plan = original_plan(
                band_units, scalars, time_layout, depth_layout, block_bytes,
                file_size, spent_bytes=spent_bytes, held=held)
            captured["pre_unique"] = unique_size(*captured["roots"])
            return plan

        units_module.plan_transfer = capture_plan
        try:
            read = units_module.read_band_units(
                structure_path, os.path.getsize(structure_path), 4096,
                owner.PROBES[0], lo, hi)
        finally:
            units_module.plan_transfer = original_plan
        post_unique = unique_size(*captured["roots"])
        claimed_objects = (read["plan"]["structures_bytes"]
                           + read["plan"]["resident_bytes"])
        print("post_read_unique_objects=%d claimed_structures_plus_arrays=%d "
              "pre_unique=%d delta=%d"
              % (post_unique, claimed_objects, captured["pre_unique"],
                 post_unique - captured["pre_unique"]))
        close_readers(owner)

    if failures:
        for failure in failures:
            print("FAILED %s" % failure)
        return 1
    print("[ok] three blocking constructions reproduced; structure diagnostic printed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
