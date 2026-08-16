"""Probe RC-003 Round-2 provenance authentication and pre-spend bounding.

This is a delta-only reviewer probe. It builds local synthetic HDF5 fixtures;
it reads no archive, network resource, or candidate asset.

Example
-------
Run from the project root with the project virtual environment::

    ./venv/Scripts/python.exe agents/Codex/tools/probe_rc003_round2.py --repo-root .
"""

import argparse
import importlib.util
import os
import tempfile


def load_module(name, path):
    """Load one module from ``path`` under the explicit module ``name``."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def close_readers(owner):
    """Close the owner harness's recorded file objects for Windows cleanup."""
    for reader in owner.READERS:
        reader.close()
    del owner.READERS[:]


def main(argv=None):
    """Run the two response-boundary constructions and report their outcomes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    args = parser.parse_args(argv)
    root = os.path.abspath(args.repo_root)

    owner = load_module(
        "rc003_round2_owner_harness",
        os.path.join(root, "agents", "Claude", "tools", "test_measure_host_drift.py"),
    )
    owner.CLI = owner.load_cli()
    owner.install_local_file()
    units_module = owner.archive_units

    failures = []
    with tempfile.TemporaryDirectory(prefix="rc003_round2_") as tmp:
        rows = owner.default_electrodes()
        units = owner.band_units()

        # F1 repair boundary. The implementation searches for one substring,
        # so a statement that expressly denies NeuroConv still authenticates.
        denied = owner.run_case(
            tmp,
            "negated_toolchain",
            lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S),
            lambda path: owner.write_processed(
                path,
                rows,
                units,
                provenance={
                    "general/source_script": (
                        "This asset was NOT created using NeuroConv; exported by LocalTool v3"
                    )
                },
            ),
        )
        denied_reached_verdict = denied["status"] == 0 and denied["record"] is not None
        print(
            "F1 negated_toolchain_reaches_verdict=%s status=%s"
            % (denied_reached_verdict, denied["status"])
        )
        if not denied_reached_verdict:
            failures.append("F1 construction did not reach the expected false authentication")
        close_readers(owner)

        # The response also deliberately permits different raw/processed
        # source_script values. Those values are the only asset-level evidence
        # it checks, so disagreement does not establish one shared conversion
        # state even though the command records it and emits a verdict.
        mismatch = owner.run_case(
            tmp,
            "conversion_version_mismatch",
            lambda path: owner.write_raw(
                path,
                rows,
                0.0,
                owner.EXTENT_S,
                provenance={"general/source_script": "Created using NeuroConv v0.9.2"},
            ),
            lambda path: owner.write_processed(
                path,
                rows,
                units,
                provenance={"general/source_script": "Created using NeuroConv v0.9.1"},
            ),
        )
        mismatch_reached_verdict = (
            mismatch["status"] == 0
            and mismatch["record"] is not None
            and mismatch["record"]["provenance_authentication"]["values_agree"] is False
        )
        print(
            "F1 mismatched_conversion_values_reach_verdict=%s status=%s"
            % (mismatch_reached_verdict, mismatch["status"])
        )
        if not mismatch_reached_verdict:
            failures.append("F1 mismatch construction did not reach the expected verdict")
        close_readers(owner)

        # F3 repair boundary. BoundedReader charges the logical length h5py
        # requests, but RemoteFile transfers and caches whole blocks. With the
        # command's default 1 MiB block, structural access can therefore spend
        # one MiB before a 65,536-byte provenance budget refuses the value.
        case_dir = os.path.join(tmp, "block_expansion")
        os.makedirs(case_dir)
        processed = os.path.join(case_dir, "processed.nwb")
        big = "p" * 2_000_000
        owner.write_processed(
            processed,
            rows,
            units,
            provenance={"general/source_script": big},
        )
        lo, hi = owner.band_bounds()
        close_readers(owner)
        units_module.RemoteFile = owner.BlockLocalFile
        refusal = None
        try:
            units_module.read_band_units(
                processed,
                os.path.getsize(processed),
                1024 * 1024,
                owner.PROBES[0],
                lo,
                hi,
                max_bytes=1,
                plan_only=True,
            )
        except ValueError as exc:
            refusal = str(exc)
        finally:
            units_module.RemoteFile = owner.LocalFile
        touched = owner.distinct_bytes(processed)
        budget = units_module.PROVENANCE_MAX_BYTES
        transfer_exceeds_budget = refusal is not None and touched > budget
        print(
            "F3 default_block_transfer=%d provenance_budget=%d exceeds_budget=%s"
            % (touched, budget, transfer_exceeds_budget)
        )
        print("F3 refusal=%s" % (refusal or "")[:180])
        if not transfer_exceeds_budget:
            failures.append("F3 block-expansion construction did not exceed the budget")
        close_readers(owner)

    if failures:
        for failure in failures:
            print("FAILED %s" % failure)
        return 1
    print("[ok] both Round-2 response boundaries reproduce")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
