"""Verify RC-004's Round-2 timestamp and raw-ceiling repairs independently.

This reviewer probe uses only the recorded census JSON and local synthetic HDF5
fixtures. It reads no archive, network resource, or candidate asset.

Example
-------
Run from the project root with the project virtual environment::

    ./venv/Scripts/python.exe agents/Codex/tools/probe_rc004_round2.py --repo-root .
"""

import argparse
import importlib.util
import json
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


def census_values(root):
    """Return the distinct raw and processed reference strings in both reports."""
    values = set()
    for name in (
        "conversion_pairs_pinned_2026-08-16.json",
        "conversion_pairs_sample60_2026-08-16.json",
    ):
        path = os.path.join(root, "agents", "Claude", "tools", name)
        with open(path, "r", encoding="utf-8") as handle:
            rows = json.load(handle)
        for row in rows:
            comparison = row["comparison"]
            values.add(comparison["raw_timestamps_reference_time"])
            values.add(comparison["processed_timestamps_reference_time"])
    return values


def main(argv=None):
    """Run the independent Round-2 checks and return nonzero on any failure."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    args = parser.parse_args(argv)
    root = os.path.abspath(args.repo_root)

    owner = load_module(
        "rc004_round2_owner_harness",
        os.path.join(root, "agents", "Claude", "tools", "test_measure_host_drift.py"),
    )
    owner.CLI = owner.load_cli()
    owner.install_local_file()
    archive_units = owner.archive_units

    checks = []

    def check(name, condition, detail):
        """Record and print one Boolean check."""
        checks.append((name, bool(condition), detail))
        print("%-58s %s  %s" % (name, "ok" if condition else "FAILED", detail))

    measured = census_values(root)
    frozen = set(owner.MEASURED_REFERENCE_TIMES)
    check("F1 frozen census is exactly the two recorded JSON reports",
          measured == frozen and len(measured) == 79,
          "json=%d frozen=%d missing=%d extra=%d"
          % (len(measured), len(frozen), len(measured - frozen), len(frozen - measured)))
    refused = sorted(value for value in measured
                     if archive_units.reference_instant(value) is None)
    check("F1 every measured reference string remains admitted", not refused,
          "refused=%r" % refused)
    check("F1 the reviewer's non-ISO separator is refused",
          archive_units.reference_instant(
              "2021-05-10Q14:33:49.023776-04:00") is None,
          "lexical gate precedes datetime.fromisoformat")

    with tempfile.TemporaryDirectory(prefix="rc004_round2_") as tmp:
        raw_path = os.path.join(tmp, "raw.nwb")
        owner.write_raw(raw_path, owner.default_electrodes(), 0.0, owner.EXTENT_S)
        size = os.path.getsize(raw_path)

        # Use the block-caching stand-in so the ceiling is checked in the same
        # currency as the real range reader: distinct fetched blocks, not only
        # the logical lengths h5py requests.
        archive_units.RemoteFile = owner.BlockLocalFile
        admitted = archive_units.read_provenance(
            raw_path, size, 1024 * 1024, max_bytes=size)
        check("F2 a ceiling equal to the whole synthetic file admits",
              admitted["io"]["bytes"] <= size,
              "transferred=%d ceiling=%d" % (admitted["io"]["bytes"], size))
        close_readers(owner)

        refusal = None
        try:
            archive_units.read_provenance(
                raw_path, size, 1024 * 1024, max_bytes=size - 1)
        except archive_units.ReadBudgetExceeded as exc:
            refusal = exc
        moved = owner.distinct_bytes(raw_path)
        check("F2 a one-byte-short block ceiling refuses before transfer",
              refusal is not None
              and refusal.scope == archive_units.PREFLIGHT_SCOPE
              and moved == 0,
              "scope=%r distinct_bytes=%d" % (getattr(refusal, "scope", None), moved))
        close_readers(owner)

    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        print("[fail] %d check(s): %r" % (len(failed), failed))
        return 1
    print("[ok] %d independent RC-004 Round-2 checks" % len(checks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
