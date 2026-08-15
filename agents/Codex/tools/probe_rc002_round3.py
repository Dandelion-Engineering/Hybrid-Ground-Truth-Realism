"""Independent terminal probe for RC-002 Round 3.

Round 3 replaces separate transfer/array ceilings with one claimed bound on
the processed-units read.  This probe exercises a read that happens *after*
that bound is computed and enforced: ``source_provenance`` loads the complete
``general/source_script`` dataset.  A generated local HDF5 fixture gives that
dataset a multi-megabyte value, then compares the admitted plan with the real
fixed-block cache and transfer after the provenance value is loaded.

Nothing here reads the archive, a candidate asset, or the network.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Codex/tools/probe_rc002_round3.py" --repo-root .
"""

import argparse
import importlib.util
import os
import tempfile


def load_module(name, path):
    """Load one Python source file without requiring it to be a package."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True, help="project root")
    return parser.parse_args(argv)


def probe_post_plan_provenance(owner_harness):
    """Return an admitted plan and the post-plan transfer it fails to cover."""
    archive_units = owner_harness.archive_units

    class InspectingBlockFile(owner_harness.BlockLocalFile):
        """Keep each fixed-block reader available after the read returns."""

        instances = []

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            InspectingBlockFile.instances.append(self)

    rows = owner_harness.default_electrodes()
    units = owner_harness.band_units()
    depth_lo, depth_hi = owner_harness.band_bounds()
    # Deliberately not compressed.  The content is provenance-shaped text, and
    # its size rather than its semantics is the property under test.
    source_script = "# generated conversion source\n" + ("x = 123456789\n" * 300000)

    with tempfile.TemporaryDirectory(prefix="rc002_round3_provenance_") as temp_dir:
        processed = os.path.join(temp_dir, "processed.nwb")
        owner_harness.write_processed(
            processed,
            rows,
            units,
            provenance={"general/source_script": source_script},
        )
        size = os.path.getsize(processed)
        block_bytes = 16 * 1024
        original_reader = archive_units.RemoteFile
        archive_units.RemoteFile = InspectingBlockFile
        try:
            read = archive_units.read_band_units(
                processed,
                size,
                block_bytes,
                owner_harness.PROBES[0],
                depth_lo,
                depth_hi,
                # Equality is admitted by the implementation.  The provenance
                # dataset is read only after this check has passed.
                max_bytes=None,
                plan_only=True,
            )
            plan = read["plan"]
            ceiling = plan["peak_resident_bytes"]
            admitted = archive_units.read_band_units(
                processed,
                size,
                block_bytes,
                owner_harness.PROBES[0],
                depth_lo,
                depth_hi,
                max_bytes=ceiling,
                plan_only=True,
            )
            reader = InspectingBlockFile.instances[-1]
            cached_bytes = sum(len(payload) for payload in reader._blocks.values())
            actual_bytes = admitted["io"]["bytes"]
            loaded_chars = len(admitted["provenance"]["general/source_script"])
        finally:
            archive_units.RemoteFile = original_reader
            for reader in InspectingBlockFile.instances:
                reader.close()

    return {
        "file_size": size,
        "cache_bound": plan["cache_bound_bytes"],
        "peak_bound": ceiling,
        "actual_bytes": actual_bytes,
        "cached_bytes": cached_bytes,
        "loaded_chars": loaded_chars,
    }


def main(argv=None):
    """Run the post-plan provenance probe."""
    args = parse_args(argv)
    repo_root = os.path.abspath(args.repo_root)
    owner_harness = load_module(
        "rc002_owner_harness_round3",
        os.path.join(
            repo_root, "agents", "Claude", "tools", "test_measure_host_drift.py"
        ),
    )
    result = probe_post_plan_provenance(owner_harness)
    transfer_underbound = result["actual_bytes"] > result["cache_bound"]
    resident_underbound = (
        result["cached_bytes"] + result["loaded_chars"] > result["peak_bound"]
    )
    print(
        "post-plan provenance: file=%d cache_bound=%d peak_bound=%d "
        "actual_transfer=%d cached=%d loaded_chars=%d "
        "transfer_underbound=%s resident_underbound=%s"
        % (
            result["file_size"],
            result["cache_bound"],
            result["peak_bound"],
            result["actual_bytes"],
            result["cached_bytes"],
            result["loaded_chars"],
            transfer_underbound,
            resident_underbound,
        )
    )
    return 0 if transfer_underbound and resident_underbound else 1


if __name__ == "__main__":
    raise SystemExit(main())
