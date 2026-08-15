"""Independent delta probes for RC-002 Round 2.

The owner response replaces the logical-payload ceiling with a claimed upper
bound on distinct fixed-block reads.  The chunked fallback is the risky branch:
HDF5 does not promise that successive chunks occupy one contiguous file span.
This probe creates valid chunked ragged columns whose chunks are deliberately
interleaved with unrelated allocated chunks, then compares the claimed bound
with a fixed-block reader's actual bytes.

It also records two smaller response-boundary checks: case-insensitive output
aliases on Windows, and whether the new mutation harness actually includes the
F5 packet-placement repair it says is covered.

Nothing here reads the archive or any candidate asset.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Codex/tools/probe_rc002_round2.py" --repo-root .
"""

import argparse
import importlib.util
import os
import sys
import tempfile

import h5py
import numpy as np


def load_module(name, path):
    """Load one Python source file without requiring it to be a package."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fragment_ragged_columns(path, archive_units, chunk_elements=64,
                            filler_elements=8192):
    """Replace two ragged columns with valid but non-contiguous chunk layouts."""
    with h5py.File(path, "r+") as handle:
        node = handle[archive_units.UNITS_PATH]
        originals = {}
        descriptions = {}
        for name in (archive_units.TIME_COLUMN, archive_units.DEPTH_COLUMN):
            originals[name] = node[name][:]
            descriptions[name] = node[name].attrs.get("description")

        replacements = {}
        for name, values in originals.items():
            replacements[name] = node.create_dataset(
                name + "_fragmented",
                shape=(0,),
                maxshape=(None,),
                chunks=(chunk_elements,),
                dtype=values.dtype,
            )
            if descriptions[name] is not None:
                replacements[name].attrs["description"] = descriptions[name]

        filler = node.create_dataset(
            "rc002_fragment_filler",
            shape=(0,),
            maxshape=(None,),
            chunks=(filler_elements,),
            dtype=np.uint8,
        )
        filler_block = np.arange(filler_elements, dtype=np.uint8)

        n_values = len(originals[archive_units.TIME_COLUMN])
        for start in range(0, n_values, chunk_elements):
            stop = min(start + chunk_elements, n_values)
            for name in (archive_units.TIME_COLUMN, archive_units.DEPTH_COLUMN):
                dataset = replacements[name]
                dataset.resize((stop,))
                dataset[start:stop] = originals[name][start:stop]

                old = len(filler)
                filler.resize((old + filler_elements,))
                filler[old:] = filler_block
            handle.flush()

        for name in (archive_units.TIME_COLUMN, archive_units.DEPTH_COLUMN):
            del node[name]
            node.move(name + "_fragmented", name)
        handle.flush()


def probe_fragmented_chunks(repo_root, owner_harness):
    """Return the claimed/actual transfer and a ceiling-admission witness."""
    archive_units = owner_harness.archive_units
    rows = owner_harness.default_electrodes()
    units = owner_harness.band_units()
    depth_lo, depth_hi = owner_harness.band_bounds()
    with tempfile.TemporaryDirectory(prefix="rc002_round2_chunks_") as temp_dir:
        processed = os.path.join(temp_dir, "processed.nwb")
        owner_harness.write_processed(processed, rows, units)
        fragment_ragged_columns(processed, archive_units)
        size = os.path.getsize(processed)
        block_bytes = 4096
        original_reader = archive_units.RemoteFile
        archive_units.RemoteFile = owner_harness.BlockLocalFile
        try:
            read = archive_units.read_band_units(
                processed,
                size,
                block_bytes,
                owner_harness.PROBES[0],
                depth_lo,
                depth_hi,
            )
            bound = read["plan"]["cache_bound_bytes"]
            actual = read["io"]["bytes"]
            ceiling = (bound + actual) // 2
            admitted = archive_units.read_band_units(
                processed,
                size,
                block_bytes,
                owner_harness.PROBES[0],
                depth_lo,
                depth_hi,
                max_bytes=ceiling,
            )
        finally:
            archive_units.RemoteFile = original_reader
    return bound, actual, size, ceiling, admitted["io"]["bytes"]


def probe_case_alias(repo_root, owner_harness):
    """Return whether case-only aliases evade the CLI's output collision guard."""
    cli = owner_harness.load_cli()
    with tempfile.TemporaryDirectory(prefix="rc002_round2_alias_") as temp_dir:
        upper = os.path.join(temp_dir, "Verdict.txt")
        lower = os.path.join(temp_dir, "verdict.txt")
        with open(upper, "w", encoding="utf-8") as handle:
            handle.write("prior verdict\n")
        same_file = os.path.samefile(upper, lower)
        accepted = True
        try:
            cli.parse_args([
                "--session", "00000000-0000-0000-0000-000000000000",
                "--probe", "Probe00",
                "--target", "CA1",
                "--assets-cache", "unused.json",
                "--out", upper,
                "--records", lower,
            ])
        except SystemExit:
            accepted = False
    return same_file, accepted


def probe_combined_resident(owner_harness):
    """Witness that the cache and converted arrays coexist above the ceiling."""
    archive_units = owner_harness.archive_units

    class InspectingBlockFile(owner_harness.BlockLocalFile):
        """Keep the most recent fixed-block reader available for inspection."""

        last = None
        instances = []

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            InspectingBlockFile.last = self
            InspectingBlockFile.instances.append(self)

    rows = owner_harness.default_electrodes()
    units = owner_harness.band_units()
    depth_lo, depth_hi = owner_harness.band_bounds()
    with tempfile.TemporaryDirectory(prefix="rc002_round2_resident_") as temp_dir:
        processed = os.path.join(temp_dir, "processed.nwb")
        owner_harness.write_processed(processed, rows, units)
        size = os.path.getsize(processed)
        original_reader = archive_units.RemoteFile
        archive_units.RemoteFile = InspectingBlockFile
        try:
            planned = archive_units.read_band_units(
                processed, size, 16384, owner_harness.PROBES[0], depth_lo,
                depth_hi, plan_only=True)
            plan = planned["plan"]
            ceiling = max(plan["cache_bound_bytes"], plan["resident_bytes"]) + 1
            admitted = archive_units.read_band_units(
                processed, size, 16384, owner_harness.PROBES[0], depth_lo,
                depth_hi, max_bytes=ceiling)
            cached_bytes = sum(len(block) for block in InspectingBlockFile.last._blocks.values())
            converted_bytes = sum(
                unit["times"].nbytes + unit["depths"].nbytes
                for unit in admitted["band_units"])
        finally:
            archive_units.RemoteFile = original_reader
            for reader in InspectingBlockFile.instances:
                reader.close()
    return ceiling, cached_bytes, converted_bytes


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True, help="project root")
    return parser.parse_args(argv)


def main(argv=None):
    """Run the three independent response-boundary probes."""
    args = parse_args(argv)
    repo_root = os.path.abspath(args.repo_root)
    owner_harness = load_module(
        "rc002_owner_harness",
        os.path.join(repo_root, "agents", "Claude", "tools",
                     "test_measure_host_drift.py"),
    )
    mutation_harness = load_module(
        "rc002_mutation_harness",
        os.path.join(repo_root, "agents", "Claude", "tools",
                     "mutate_rc002_repairs.py"),
    )

    bound, actual, file_size, ceiling, admitted_actual = probe_fragmented_chunks(
        repo_root, owner_harness)
    underbound = bound < actual
    admitted_over_ceiling = admitted_actual > ceiling
    print("fragmented chunks: bound=%d actual=%d file=%d underbound=%s; "
          "ceiling=%d admitted_actual=%d admitted_over_ceiling=%s"
          % (bound, actual, file_size, underbound, ceiling, admitted_actual,
             admitted_over_ceiling))

    same_file, alias_accepted = probe_case_alias(repo_root, owner_harness)
    print("case-only outputs: same_file=%s accepted_by_guard=%s"
          % (same_file, alias_accepted))

    resident_ceiling, cached_bytes, converted_bytes = probe_combined_resident(
        owner_harness)
    combined_resident = cached_bytes + converted_bytes
    combined_over_ceiling = combined_resident > resident_ceiling
    print("combined resident: ceiling=%d cached=%d converted=%d combined=%d "
          "combined_over_ceiling=%s"
          % (resident_ceiling, cached_bytes, converted_bytes, combined_resident,
             combined_over_ceiling))

    mutation_names = [entry[0] for entry in mutation_harness.MUTATIONS]
    f5_covered = any(name.startswith("F5") for name in mutation_names)
    print("mutation coverage: entries=%d F5_present=%s"
          % (len(mutation_names), f5_covered))

    # The transfer construction is the blocking claim this probe exists to
    # decide. The other two outputs are recorded follow-up/evidence issues.
    return 1 if not (underbound and admitted_over_ceiling and combined_over_ceiling) else 0


if __name__ == "__main__":
    raise SystemExit(main())
