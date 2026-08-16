"""Rebuild Codex's RC-003 Round-2 constructions and require each to be refused.

``agents/Codex/tools/probe_rc003_round2.py`` is the reviewer's own probe and it
is the one that re-pins the finding. This script exists because that probe no
longer runs to completion against the repaired candidate -- both of its F1
constructions now stop as input errors instead of reaching a verdict, so the
values it goes on to read are not there -- and because its F3 comparison is
against the wrong one of two numbers now that there are two.

Each construction is therefore rebuilt here explicitly, with every fixture
written in this file rather than taken from a default, so that a refusal cannot
be an accident of a default that changed underneath it.

**What each one establishes.**

1. *Negated toolchain.* ``This asset was NOT created using NeuroConv; exported
   by LocalTool v3`` contains the token the first repair searched for. The whole
   value is now matched against the conversion statement the 21 measured assets
   carry, so a value that denies the toolchain is refused rather than admitted
   by naming it.

2. *Converter version disagreement.* Both values are legitimate NeuroConv
   statements and both appear in this dandiset; what is refused is the pair. The
   clock claim is that one session's two halves share a coordinate, and two
   converter versions is not evidence that they do.

3. *Block expansion.* The reviewer measured 2,081,456 distinct bytes moving
   before a 65,536-byte provenance budget refused a two-million-character value,
   at the command's default 1 MiB block. This script measures where those bytes
   were actually spent, which is the part that decided the repair: **every one
   of them was spent by preflight before the provenance read began**, so no
   provenance budget could have prevented them. Two bounds now do. The
   provenance budget is denominated in blocks rather than in requested bytes,
   and the caller's declared ceiling is held open as a transfer budget for the
   whole read, so on the reviewer's own one-byte ceiling **nothing moves at
   all**.

Every fixture is local and synthetic. Nothing here reads the archive, the
network, or any candidate asset.

Example
-------
Run from the project root with the project virtual environment::

    ./venv/Scripts/python.exe agents/Claude/tools/verify_rc003_round2_repairs.py --repo-root .
"""

import argparse
import importlib.util
import os
import shutil
import sys
import tempfile

DENIAL = "This asset was NOT created using NeuroConv; exported by LocalTool v3"
RAW_STATEMENT = "Created using NeuroConv v0.9.2"
PROCESSED_STATEMENT = "Created using NeuroConv v0.9.1"


def load_owner(root):
    """Import the acceptance harness, which owns the fixture writers.

    Args:
        root: the project root.

    Returns:
        The imported module, with its CLI loaded and its local reader installed.
    """
    path = os.path.join(root, "agents", "Claude", "tools", "test_measure_host_drift.py")
    spec = importlib.util.spec_from_file_location("rc003_round3_owner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CLI = module.load_cli()
    module.install_local_file()
    return module


def close_readers(owner):
    """Close every recorded local reader, so Windows can remove the fixtures."""
    for reader in owner.READERS:
        try:
            reader.close()
        except OSError:
            pass
    del owner.READERS[:]


def check(failures, name, condition, detail):
    """Record one named requirement and print its outcome.

    Args:
        failures: the list to append to when ``condition`` is false.
        name: the requirement's name.
        condition: what must hold.
        detail: what to print beside it.
    """
    print("%-46s %s  %s" % (name, "ok" if condition else "FAILED", detail))
    if not condition:
        failures.append(name)


def negated_toolchain(owner, tmp, failures):
    """The denial contains the searched-for token and must still be refused."""
    rows = owner.default_electrodes()
    units = owner.band_units()
    result = owner.run_case(
        tmp, "negated_toolchain",
        lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S,
                                     provenance={"general/source_script": RAW_STATEMENT}),
        lambda path: owner.write_processed(path, rows, units,
                                           provenance={"general/source_script": DENIAL}))
    status = str(result["status"])
    token = owner.archive_units.CONVERSION_SOURCE_TOKEN
    check(failures, "F1 denial contains the old token", token in DENIAL.lower(), token)
    check(failures, "F1 denial reaches no verdict", result["record"] is None, status[:90])
    check(failures, "F1 denial is an input error",
          "input error" in status and "is not the conversion statement" in status,
          status[:110])
    close_readers(owner)


def version_disagreement(owner, tmp, failures):
    """Two legitimate statements naming two versions must be refused as a pair."""
    rows = owner.default_electrodes()
    units = owner.band_units()
    au = owner.archive_units
    check(failures, "F1 both values are legitimate statements",
          au.conversion_version(RAW_STATEMENT) == "0.9.2"
          and au.conversion_version(PROCESSED_STATEMENT) == "0.9.1",
          "%s / %s" % (RAW_STATEMENT, PROCESSED_STATEMENT))
    result = owner.run_case(
        tmp, "version_disagreement",
        lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S,
                                     provenance={"general/source_script": RAW_STATEMENT}),
        lambda path: owner.write_processed(
            path, rows, units,
            provenance={"general/source_script": PROCESSED_STATEMENT}))
    status = str(result["status"])
    check(failures, "F1 disagreeing pair reaches no verdict", result["record"] is None,
          status[:90])
    check(failures, "F1 disagreeing pair is an input error",
          "input error" in status and "states conversion version 0.9.2" in status,
          status[:110])
    close_readers(owner)


def block_expansion(owner, tmp, failures):
    """Measure where the reviewer's 2,081,456 bytes were spent, and bound them."""
    au = owner.archive_units
    rows = owner.default_electrodes()
    units = owner.band_units()
    low, high = owner.band_bounds()
    case_dir = os.path.join(tmp, "block_expansion")
    os.makedirs(case_dir, exist_ok=True)
    processed = os.path.join(case_dir, "processed.nwb")
    owner.write_processed(processed, rows, units,
                          provenance={"general/source_script": "p" * 2000000})
    size = os.path.getsize(processed)
    block = 1024 * 1024
    budget = au.provenance_transfer_budget(block)

    # Where the bytes go, with no ceiling in force: the provenance read is
    # instrumented so its own share of the transfer is separable from what
    # preflight spent before it.
    real = au.source_provenance
    marks = {}

    def instrumented(handle, reader, *args, **kwargs):
        """Record the distinct bytes touched on either side of the real call."""
        marks["before"] = owner.distinct_bytes(processed)
        out = real(handle, reader, *args, **kwargs)
        marks["after"] = owner.distinct_bytes(processed)
        marks["spend"] = reader.last_spend
        return out

    del owner.READERS[:]
    au.source_provenance = instrumented
    au.RemoteFile = owner.BlockLocalFile
    refused = None
    try:
        au.read_band_units(processed, size, block, owner.PROBES[0], low, high,
                           plan_only=True)
    except ValueError as exc:
        refused = str(exc)
    finally:
        au.RemoteFile = owner.LocalFile
        au.source_provenance = real
    whole = owner.distinct_bytes(processed)
    close_readers(owner)

    check(failures, "F3 oversized value is refused",
          refused is not None and "not read whole" in refused, repr(refused)[:110])
    check(failures, "F3 provenance read's own transfer is inside its budget",
          marks["spend"]["transfer_bytes"] <= marks["spend"]["transfer_budget_bytes"],
          "%d of %d bytes" % (marks["spend"]["transfer_bytes"],
                              marks["spend"]["transfer_budget_bytes"]))
    check(failures, "F3 budget is block-denominated", budget >= block,
          "%d against a %d-byte block" % (budget, block))
    print("%-46s     %d spent before provenance, %d by it, %d in total"
          % ("F3 where the reviewer's bytes were spent", marks["before"],
             marks["after"] - marks["before"], whole))

    # And the reviewer's own one-byte ceiling, which measured 2,081,456 bytes.
    del owner.READERS[:]
    au.RemoteFile = owner.BlockLocalFile
    ceiling_refused = None
    try:
        au.read_band_units(processed, size, block, owner.PROBES[0], low, high,
                           max_bytes=1, plan_only=True)
    except ValueError as exc:
        ceiling_refused = str(exc)
    finally:
        au.RemoteFile = owner.LocalFile
    moved = owner.distinct_bytes(processed)
    close_readers(owner)
    check(failures, "F3 one-byte ceiling refuses before the fetch",
          ceiling_refused is not None
          and "declared ceiling transfer budget" in ceiling_refused,
          repr(ceiling_refused)[:110])
    check(failures, "F3 one-byte ceiling moves nothing", moved == 0,
          "%d distinct bytes against the 2081456 measured at Round 2" % moved)


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="project root holding the packet and the agent workspace")
    return parser.parse_args(argv)


def main(argv=None):
    """Rebuild all three constructions and report whether each is refused."""
    args = parse_args(argv)
    root = os.path.abspath(args.repo_root)
    owner = load_owner(root)
    failures = []
    tmp = tempfile.mkdtemp(prefix="rc003_round3_")
    try:
        negated_toolchain(owner, tmp, failures)
        version_disagreement(owner, tmp, failures)
        block_expansion(owner, tmp, failures)
    finally:
        close_readers(owner)
        shutil.rmtree(tmp, ignore_errors=True)
    print("")
    if failures:
        print("[fail] %d requirement(s) not met: %s" % (len(failures), failures))
        return 1
    print("[ok] all three Round-2 constructions are refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
