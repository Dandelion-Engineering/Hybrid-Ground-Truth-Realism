"""Rebuild Codex's three RC-003 Round-1 constructions against the repaired candidate.

His probe, ``agents/Codex/tools/probe_rc003_round1.py``, no longer runs to
completion, and the reason is worth stating rather than leaving him to find:
**the repair moved two of the things it stood on.** Its first construction built
a provenance-free processed asset by calling ``owner.write_processed`` with no
``provenance`` argument, and that default is now a valid conversion-provenance
mapping, because the command authenticates provenance rather than recording it
and a fixture that omits it must now do so deliberately. Its second calls
``select_ap_series`` directly on an impostor name, which is now a ``SystemExit``
rather than a return value, so the probe raises there and its temporary
directory cleanup fails behind it on Windows. Neither is a disagreement with the
finding; both are the finding's repair showing up in his harness.

So this script rebuilds all three constructions **explicitly**, with every
fixture written here rather than taken from a default, and requires each of them
to be refused. It is not a replacement for his re-pin -- it is the evidence he
can check the repair against while he writes one.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Claude/tools/verify_rc003_round1_repairs.py" --repo-root .
"""

import argparse
import importlib.util
import os
import sys
import tempfile


def load_module(name, path):
    """Import one module from an explicit path.

    Args:
        name: the module name to register it under.
        path: the file to load.

    Returns:
        The imported module.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def close_readers(owner):
    """Close every file object the owner harness installed, so Windows can unlink."""
    for reader in owner.READERS:
        reader.close()
    del owner.READERS[:]


def main(argv=None):
    """Rebuild the three constructions and return nonzero unless all three are refused."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True,
                        help="project root holding agents/ and Reproducibility Packet/")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.repo_root)
    owner = load_module("rc003_owner_harness",
                        os.path.join(root, "agents", "Claude", "tools",
                                     "test_measure_host_drift.py"))
    owner.CLI = owner.load_cli()
    owner.install_local_file()
    units_module = owner.archive_units

    failures = []
    with tempfile.TemporaryDirectory(prefix="rc003_repairs_") as tmp:
        rows = owner.default_electrodes()
        units = owner.band_units()

        # RC-003-F1. The processed asset carries no conversion provenance at
        # all. It used to reach passed=True with an empty provenance record.
        missing = owner.run_case(
            tmp, "missing_required_provenance",
            lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S),
            lambda path: owner.write_processed(path, rows, units, provenance={}))
        f1_refused = (missing["status"] != 0
                      and missing["record"] is None
                      and "carries no general/source_script" in str(missing["status"]))
        print("F1 missing_provenance_refused=%s status=%s"
              % (f1_refused, str(missing["status"])[:150]))
        if not f1_refused:
            failures.append("F1: a processed asset with no provenance was not refused")

        # RC-003-F2. Asked for Probe00, the file carries Probe000 and Probe01.
        # select_ap_series used to return the Probe000 stream.
        impostor_names = ["ElectricalSeriesProbe000AP", "ElectricalSeriesProbe01AP"]
        series = [{"name": impostor_names[0], "timing_source": "timestamps",
                   "n_timestamps": 1000, "shape": [1000, 4],
                   "t_first_s": 0.0, "t_last_s": owner.EXTENT_S}]
        selected = None
        try:
            selected = owner.CLI.select_ap_series(series, owner.PROBES[0])
        except SystemExit as exc:
            selected = str(exc.code)
        f2_selector = isinstance(selected, str) and "belong to probe" in selected
        print("F2 selector_refuses_impostor=%s -> %s" % (f2_selector, str(selected)[:150]))
        if not f2_selector:
            failures.append("F2: the selector still accepted a name containing the token")

        impostor = owner.run_case(
            tmp, "substring_probe_verdict",
            lambda path: owner.write_raw(path, rows, 0.0, owner.EXTENT_S,
                                         series_names=impostor_names),
            lambda path: owner.write_processed(path, rows, units))
        f2_end_to_end = impostor["status"] != 0 and impostor["record"] is None
        print("F2 impostor_reaches_no_verdict=%s status=%s"
              % (f2_end_to_end, str(impostor["status"])[:150]))
        if not f2_end_to_end:
            failures.append("F2: the impostor series still reached a verdict")

        # RC-003-F3. A two-million-character variable-length source_script under
        # a one-byte ceiling. His measurement was 2,028,208 distinct bytes spent
        # before the promised refusal; the budget refuses the request instead.
        spend_dir = os.path.join(tmp, "vlen_pre_ceiling")
        os.makedirs(spend_dir)
        processed = os.path.join(spend_dir, "processed.nwb")
        big = "p" * 2000000
        owner.write_processed(processed, rows, units,
                              provenance={"general/source_script": big})
        lo, hi = owner.band_bounds()
        close_readers(owner)
        units_module.RemoteFile = owner.BlockLocalFile
        refused = None
        try:
            units_module.read_band_units(processed, os.path.getsize(processed), 4096,
                                         owner.PROBES[0], lo, hi, max_bytes=1,
                                         plan_only=True)
        except ValueError as exc:
            refused = str(exc)
        finally:
            units_module.RemoteFile = owner.LocalFile
        touched = owner.distinct_bytes(processed)
        f3_bounded = (refused is not None
                      and "not read whole" in refused
                      and touched < 100000)
        print("F3 vlen_bytes_touched=%d (Codex measured 2028208) bounded=%s"
              % (touched, f3_bounded))
        print("F3 refusal=%s" % (refused or "")[:150])
        if not f3_bounded:
            failures.append("F3: the variable-length value was not bounded before the spend")
        close_readers(owner)

    if failures:
        for failure in failures:
            print("FAILED %s" % failure)
        return 1
    print("[ok] all three Round-1 constructions are refused by the repaired candidate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
