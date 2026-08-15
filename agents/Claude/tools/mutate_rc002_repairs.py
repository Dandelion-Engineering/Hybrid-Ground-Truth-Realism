"""Undo one RC-002 repair at a time and confirm the acceptance suite notices.

A harness written *after* a repair can encode the repair rather than the
property it is supposed to establish: every case passes, and would have passed
against a subtly different fix. The only way to know the difference is to remove
each repair and watch the suite go red.

Each mutation below reverts exactly one of Codex's Round-1 findings in its own
clean copy of the tree, runs ``test_measure_host_drift.py`` there, and requires
the cases named beside it to fail. The unmutated control copy must pass. One
mutation per copy, so no mutation can mask or amplify another.

Two of the entries are worth reading rather than counting. The F1 mutation puts
the ceiling back on the stored payload, which is the exact defect Codex
reproduced. The F2b mutation removes the per-unit column-length check, and what
the suite notices is not a refusal but a raise: without the check the command
does not reach a verdict, it crashes -- so either the case's own assertion or
the harness recording the exception counts as noticing, and both names are
listed.

This is evidence about the harness, not about any recording. Nothing here reads
the archive, and no fixture resembles a real candidate.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Claude/tools/mutate_rc002_repairs.py" --repo-root .
"""

import argparse
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

PACKET_SCRIPTS = os.path.join("Reproducibility Packet", "scripts")
CLI = os.path.join(PACKET_SCRIPTS, "measure_host_drift.py")
UNITS = os.path.join(PACKET_SCRIPTS, "utils", "archive_units.py")
HARNESS = os.path.join("agents", "Claude", "tools", "test_measure_host_drift.py")

MUTATIONS = [
    ("F1 the ceiling watches only the stored payload", UNITS,
     'over = [(name, plan[name]) for name in ("cache_bound_bytes", "resident_bytes")',
     'over = [(name, plan[name]) for name in ("logical_bytes",)',
     # The names below are prefixes of the *first token* of a failed check's
     # name, which is what the suite prints and what this file matches on.
     [("ceiling_blocks/a",), ("ceiling_blocks/refusal",),
      ("ceiling_resident/refused",)]),
    ("F2a structural columns are coerced, not checked", UNITS,
     "    values = node[name][:]\n    if np.issubdtype(values.dtype, np.integer):\n"
     "        return [int(v) for v in values]",
     "    values = node[name][:]\n    if True:\n"
     "        return [int(v) for v in values]",
     [("fractional_offsets/refused",), ("fractional_electrode/refused",)]),
    ("F2b one-value-per-unit lengths are unchecked", UNITS,
     'for name in ("label", "max_electrode", "times_index", "depths_index"):',
     'for name in ():',
     [("short_column/refused", "case_short_unit_column_is_refused/raised")]),
    ("F3a the asset pair is not authenticated", CLI,
     "    subjects = (dandi.subject_of(raw), dandi.subject_of(processed))",
     "    return raw, processed\n"
     "    subjects = (dandi.subject_of(raw), dandi.subject_of(processed))",
     [("cross_subject/refused",), ("stem_mismatch/refused",)]),
    ("F3b AP timestamp coverage is unchecked", CLI,
     "    if n_timestamps is None or n_samples is None or "
     "int(n_timestamps) != int(n_samples):",
     "    if False:",
     [("timestamp_coverage/refused",)]),
    ("F4 the band contiguity gap is typeable again", CLI,
     '    parser.add_argument("--block-kb", type=int, default=1024,',
     '    parser.add_argument("--max-gap-um", type=float, default=40.0)\n'
     '    parser.add_argument("--block-kb", type=int, default=1024,',
     [("pinned_gap/typed",)]),
    ("F6a the declared outputs are not cleared", CLI,
     "    clear_outputs((args.out, args.records))\n", "",
     [("stale/report",), ("stale/record",), ("stale/files",)]),
    ("F6b --out and --records may name one path", CLI,
     "    if args.records and os.path.abspath(args.records) == os.path.abspath(args.out):",
     "    if False:",
     [("same_path/refused",)]),
]


def read(path):
    """Read a file without rewriting its line endings."""
    with io.open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def clean_copy(repo_root, work_root, name):
    """Build a fresh tree holding only what the acceptance suite imports.

    Args:
        repo_root: the project root to copy from.
        work_root: where to build the copy.
        name: subdirectory name for this copy.

    Returns:
        The path of the new tree.
    """
    target = os.path.join(work_root, name)
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree(os.path.join(repo_root, PACKET_SCRIPTS),
                    os.path.join(target, PACKET_SCRIPTS),
                    ignore=shutil.ignore_patterns("__pycache__"))
    tools = os.path.join(target, "agents", "Claude", "tools")
    os.makedirs(tools)
    shutil.copy2(os.path.join(repo_root, HARNESS), tools)
    return target


def apply_mutation(target, relative, old, new):
    """Replace exactly one anchor in one file of one copy.

    Raises:
        AssertionError: unless the anchor appears exactly once, so a mutation
            that silently stopped applying is a loud failure rather than a
            quietly passing control run.
    """
    path = os.path.join(target, relative)
    text = read(path)
    assert text.count(old) == 1, "%s: %d matches for the anchor" % (relative, text.count(old))
    with io.open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text.replace(old, new, 1))


def run_suite(target, python):
    """Run the acceptance suite inside one copy.

    Returns:
        A ``(status, failed_names, summary)`` triple.
    """
    result = subprocess.run([python, os.path.join(target, HARNESS)],
                            capture_output=True, text=True, cwd=target)
    failed = set(re.findall(r"^  FAILED (\S+)", result.stdout, re.M))
    summary = [line for line in result.stdout.splitlines() if " checks, " in line]
    return result.returncode, failed, (summary[-1] if summary else result.stderr[-200:])


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="project root holding the packet and the agent workspace")
    parser.add_argument("--work-root", default=None,
                        help="where to build the copies (default: a temporary directory)")
    parser.add_argument("--python", default=sys.executable,
                        help="interpreter to run the suite with (default: this one)")
    parser.add_argument("--keep", action="store_true",
                        help="keep the copies instead of deleting them")
    return parser.parse_args(argv)


def main(argv=None):
    """Run the control and every mutation, and report what was noticed."""
    args = parse_args(argv)
    work_root = args.work_root or tempfile.mkdtemp(prefix="rc002_mutation_")
    os.makedirs(work_root, exist_ok=True)
    problems = []
    try:
        control = clean_copy(args.repo_root, work_root, "control")
        status, failed, summary = run_suite(control, args.python)
        healthy = status == 0 and not failed
        print("%-46s exit=%d  %s  %s"
              % ("control (unmutated)", status,
                 "PASSES as it should" if healthy else "BROKEN", summary))
        if not healthy:
            problems.append("control")
        if not args.keep:
            shutil.rmtree(control, ignore_errors=True)

        for index, (name, relative, old, new, expected) in enumerate(MUTATIONS):
            target = clean_copy(args.repo_root, work_root, "mutation%02d" % index)
            apply_mutation(target, relative, old, new)
            status, failed, summary = run_suite(target, args.python)
            missed = [group for group in expected
                      if not any(case.startswith(prefix)
                                 for prefix in group for case in failed)]
            caught = status != 0 and not missed
            print("%-46s exit=%d  %s  %s"
                  % (name, status, "CAUGHT" if caught else "MISSED %s" % (missed,),
                     ", ".join(sorted(failed)) or summary))
            if not caught:
                problems.append(name)
            if not args.keep:
                shutil.rmtree(target, ignore_errors=True)
    finally:
        if not args.keep:
            shutil.rmtree(work_root, ignore_errors=True)

    print("")
    if problems:
        print("[fail] %d not detected: %s" % (len(problems), problems))
        return 1
    print("[ok] all %d mutations detected, and the unmutated control passes"
          % len(MUTATIONS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
