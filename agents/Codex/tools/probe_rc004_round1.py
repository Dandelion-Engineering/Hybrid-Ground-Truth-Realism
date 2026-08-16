"""Probe RC-004's timestamp grammar and outer-ceiling boundary.

This reviewer probe builds only local synthetic HDF5 fixtures. It reads no
archive, network resource, or candidate asset.

Example
-------
Run from the project root with the project virtual environment::

    ./venv/Scripts/python.exe agents/Codex/tools/probe_rc004_round1.py --repo-root .
"""

import argparse
import contextlib
import importlib.util
import io
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
    """Run two purpose-level counterexamples and report their outcomes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    args = parser.parse_args(argv)
    root = os.path.abspath(args.repo_root)

    owner = load_module(
        "rc004_round1_owner_harness",
        os.path.join(root, "agents", "Claude", "tools", "test_measure_host_drift.py"),
    )
    owner.CLI = owner.load_cli()
    owner.install_local_file()

    failures = []
    with tempfile.TemporaryDirectory(prefix="rc004_round1_") as tmp:
        rows = owner.default_electrodes()
        units = owner.band_units()

        # datetime.fromisoformat deliberately accepts any one-character date/time
        # separator, which is wider than the ISO-8601/NWB form this candidate says
        # it authenticates. Two identical non-ISO values therefore reach a drift
        # verdict rather than the card's required malformed-input error.
        non_iso = "2021-05-10Q14:33:49.023776-04:00"
        malformed = owner.run_case(
            tmp,
            "non_iso_separator",
            lambda path: owner.write_raw(
                path, rows, 0.0, owner.EXTENT_S, reference_time=non_iso
            ),
            lambda path: owner.write_processed(
                path, rows, units, reference_time=non_iso
            ),
        )
        malformed_reached_verdict = (
            malformed["status"] == 0 and malformed["record"] is not None
        )
        print(
            "F1 non_iso_separator_reaches_verdict=%s status=%s"
            % (malformed_reached_verdict, malformed["status"])
        )
        if not malformed_reached_verdict:
            failures.append("non-ISO separator did not reproduce the permissive parse")
        close_readers(owner)

        # RC-004 condition 5 says both clock reads remain inside the caller's
        # outer transfer ceiling. The CLI still applies --max-mib only when it
        # opens the processed asset, after it has already read and printed the
        # raw asset's reference time (and performed the other raw reads).
        transcript = io.StringIO()
        with contextlib.redirect_stdout(transcript):
            ceiling = owner.run_case(
                tmp,
                "raw_clock_outside_outer_ceiling",
                lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S),
                lambda path: owner.write_processed(path, rows, units),
                argv_extra=("--max-mib", "0.000001", "--plan-only"),
            )
        printed = transcript.getvalue()
        raw_bytes = owner.distinct_bytes(ceiling["raw"])
        raw_clock_read_before_refusal = (
            "[drift] raw asset counts its times from" in printed
            and raw_bytes > 1
            and "declared ceiling transfer budget" in str(ceiling["status"])
        )
        print(
            "F2 raw_clock_read_before_one_byte_ceiling_refusal=%s raw_distinct_bytes=%d status=%s"
            % (raw_clock_read_before_refusal, raw_bytes, ceiling["status"])
        )
        if not raw_clock_read_before_refusal:
            failures.append("raw clock did not reproduce outside the outer ceiling")
        close_readers(owner)

    if failures:
        for failure in failures:
            print("FAILED %s" % failure)
        return 1
    print("[ok] both RC-004 Round-1 counterexamples reproduce")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
