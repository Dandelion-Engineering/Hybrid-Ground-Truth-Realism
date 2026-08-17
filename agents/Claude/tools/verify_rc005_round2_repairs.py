"""Revert each RC-005 Round-2 repair in a clean copy and require it to be caught.

**Why this exists.** Codex's Round-1 ledger raised two blockers, F1 and F2, and
both were repaired by *adding* something the previous state left out: a final
console line that reports the reconciled disposition rather than the point gate,
and a mask term inside the pre-read resident bound. New acceptance checks were
written for both. A check written after the defect is understood is exactly the
kind that can pass for a reason unrelated to what it names, and the project's own
finding is blunt about it: **a check that cannot fail is not a check.** Neither
repair is covered by ``mutate_rc002_repairs.py``, whose thirty-two mutations
target RC-002's repairs and are pinned to a closed card.

So each repair is reverted here -- in a throwaway copy, never in the repository --
and the suite is required to go red on named checks. Two of the four mutations
are the plain reversions; the other two are the near-misses a partial repair
would produce, because a mutation that only reverts the whole change cannot tell
a specific check from a coincidence.

**What each mutation establishes.**

1. *F1 reverted.* The command ends with the point gate's own ``passed=`` line
   again, exactly as it did when Codex found it. The paused fixture's transcript
   then ends in ``passed=True`` on a candidate the record refuses to advance,
   which is the defect itself, and the three console cases have to say so.

2. *F1 half-repaired.* The reconciled decision is printed last, but the point
   gate above it is no longer labelled a diagnostic. This is the state that looks
   repaired and still lets a reader take the wrong line as the answer, and it is
   what separates the "last line" checks from the "labelled" ones.

3. *F2 reverted.* ``resident_bytes`` drops the mask term while the plan still
   publishes ``mask_bytes``, which is the pre-repair formula. The ceiling set to
   exactly the peak-minus-masks then admits a read that retains bytes nobody
   counted -- the admission boundary the new case exists to pin.

4. *F2 mis-scoped.* The masks are charged once per largest slice rather than once
   per spike, which is the plausible wrong reading of what the reader retains: it
   keeps one mask per unit, all of them, not one the size of the biggest. The
   number is nonzero and too small, which is the direction that matters.

Every fixture the suite builds is local and synthetic. **Nothing here reads the
archive, the network, or any candidate asset, and nothing here is written back
into the repository.**

Example
-------
Run from the project root with the project virtual environment::

    ./venv/Scripts/python.exe agents/Claude/tools/verify_rc005_round2_repairs.py --repo-root .
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

DECISION_BLOCK = (
    '    print("[drift] point gate on the record held (diagnostic, not the decision): "\n'
    '          "passed=%s label=%s" % (verdict["passed"], verdict["label"]), flush=True)\n'
    '    print("[drift] decision: %s; advances=%s; gate and completion bound conflict=%s"\n'
    '          % (reconciled["disposition"], reconciled["advances"], reconciled["conflict"]),\n'
    '          flush=True)')

RESIDENT_BLOCK = (
    '    mask_bytes = total_spikes * MASK_ITEMSIZE\n'
    '    resident = (total_spikes * 16 + mask_bytes\n'
    '                + largest * (time_layout["itemsize"] + depth_layout["itemsize"]))')

# (name, file, anchor, replacement, expected failing check prefixes). Each entry
# in the expectation list is a group; the mutation counts as caught only when
# every group has at least one failing check that starts with one of its
# prefixes, so a mutation cannot be credited for breaking something unrelated.
MUTATIONS = [
    ("F1 the point gate is printed last again", CLI,
     DECISION_BLOCK,
     '    print("[drift] verdict: passed=%s label=%s" % (verdict["passed"], verdict["label"]),\n'
     '          flush=True)',
     [("pause/last line is the decision",),
      ("pause/console does not end in a passing verdict",),
      ("missing/last line is the decision",),
      ("clean/last line is the decision",)]),

    ("F1 the decision is last but the gate is unlabelled", CLI,
     DECISION_BLOCK,
     '    print("[drift] gate: passed=%s label=%s" % (verdict["passed"], verdict["label"]),\n'
     '          flush=True)\n'
     '    print("[drift] decision: %s; advances=%s; gate and completion bound conflict=%s"\n'
     '          % (reconciled["disposition"], reconciled["advances"], reconciled["conflict"]),\n'
     '          flush=True)',
     [("pause/the point gate is printed and labelled a diagnostic",),
      ("missing/the point gate is printed and labelled a diagnostic",),
      ("clean/the point gate is printed and labelled a diagnostic",)]),

    ("F2 the resident bound drops the mask term", UNITS,
     RESIDENT_BLOCK,
     '    mask_bytes = total_spikes * MASK_ITEMSIZE\n'
     '    resident = total_spikes * 16 + largest * (time_layout["itemsize"]\n'
     '                                              + depth_layout["itemsize"])',
     [("masks/resident carries the arrays, the masks and one slice",),
      ("masks/the ceiling the omission admitted is refused",),
      ("three_costs/resident is float64 plus the masks plus one slice",)]),

    ("F2 the masks are charged per largest slice", UNITS,
     RESIDENT_BLOCK,
     '    mask_bytes = largest * MASK_ITEMSIZE\n'
     '    resident = (total_spikes * 16 + mask_bytes\n'
     '                + largest * (time_layout["itemsize"] + depth_layout["itemsize"]))',
     [("masks/one byte per spike",),
      ("masks/what is held is what was charged",),
      ("three_costs/mask term is one byte per spike",)]),
]


def read(path):
    """Read a file without rewriting its line endings.

    Args:
        path: the file to read.

    Returns:
        Its text.
    """
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

    Args:
        target: the copy's root.
        relative: the file to edit, relative to that root.
        old: the anchor, which must appear exactly once.
        new: what replaces it.

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


def check_anchors(repo_root):
    """Require every mutation's anchor to match its file exactly once, first.

    Ten minutes of suite runs spent discovering that an anchor no longer matches
    is ten minutes spent proving nothing, and a mutation whose anchor has drifted
    reports MISSED for a reason that has nothing to do with the property.

    Args:
        repo_root: the project root.

    Returns:
        A list of complaints, empty when every anchor is unique.
    """
    problems = []
    for name, relative, old, _new, _expected in MUTATIONS:
        found = read(os.path.join(repo_root, relative)).count(old)
        if found != 1:
            problems.append("%s: %d matches in %s" % (name, found, relative))
    return problems


def run_suite(target, python):
    """Run the acceptance suite inside one copy.

    Args:
        target: the copy's root.
        python: the interpreter to run it with.

    Returns:
        A ``(status, failed_names, summary)`` triple.
    """
    result = subprocess.run([python, os.path.join(target, HARNESS)],
                            capture_output=True, text=True, cwd=target)
    failed = set(re.findall(r"^  FAILED (.*)$", result.stdout, re.M))
    summary = [line for line in result.stdout.splitlines() if " checks, " in line]
    return result.returncode, failed, (summary[-1] if summary else result.stderr[-200:])


def parse_args(argv=None):
    """Parse command-line arguments.

    Args:
        argv: argument list, defaulting to ``sys.argv[1:]``.

    Returns:
        The parsed namespace.
    """
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
    """Run the control and every reversion, and report what was noticed.

    Args:
        argv: argument list, defaulting to ``sys.argv[1:]``.

    Returns:
        0 when the control passes and every reversion is caught, 1 otherwise.
    """
    args = parse_args(argv)
    stale = check_anchors(args.repo_root)
    if stale:
        print("[fail] %d anchor(s) no longer match exactly once:" % len(stale))
        for problem in stale:
            print("  %s" % problem)
        return 1
    work_root = args.work_root or tempfile.mkdtemp(prefix="rc005_reversion_")
    os.makedirs(work_root, exist_ok=True)
    problems = []
    try:
        control = clean_copy(args.repo_root, work_root, "control")
        status, failed, summary = run_suite(control, args.python)
        healthy = status == 0 and not failed
        print("%-52s exit=%d  %s  %s"
              % ("control (unmutated)", status,
                 "PASSES as it should" if healthy else "BROKEN", summary))
        if not healthy:
            problems.append("control")
        if not args.keep:
            shutil.rmtree(control, ignore_errors=True)

        for index, (name, relative, old, new, expected) in enumerate(MUTATIONS):
            target = clean_copy(args.repo_root, work_root, "reversion%02d" % index)
            apply_mutation(target, relative, old, new)
            status, failed, summary = run_suite(target, args.python)
            missed = [group for group in expected
                      if not any(case.startswith(prefix)
                                 for prefix in group for case in failed)]
            caught = status != 0 and not missed
            print("%-52s exit=%d  %s  %s"
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
    print("[ok] all %d reversions detected, and the unmutated control passes"
          % len(MUTATIONS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
