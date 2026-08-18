"""Mutation harness for probe_rc008_spec.py, the Draft-32 owner checker.

One breakage per clean copy of the repository's relevant files. Each mutation
reverts or damages exactly one property the convergence repair established, and
must be caught. The harness hard-fails rather than skipping when a mutation's
source string no longer matches the document exactly once, because a stale
anchor is a mutation that silently stopped testing anything.

Usage:

    ./venv/Scripts/python.exe agents/Claude/tools/mutate_rc008_spec.py \
        --repo-root . --work-root <writable scratch directory>

The harness deletes its own working tree and exits non-zero unless the control
run is green and every mutation is caught.
"""

import argparse
import io
import os
import shutil
import subprocess
import sys
import tempfile

DOC = os.path.join("agents", "Claude",
                   "Tier A Host and Injection Zone Selection.md")
TOOLS = os.path.join("agents", "Claude", "tools")
PROBE = os.path.join(TOOLS, "probe_rc008_spec.py")
# probe_rc008_spec.py runs the closed card's checker as a regression baseline,
# so the case tree needs it and every record it reads.
CARRIED = [
    os.path.join(TOOLS, "probe_rc007_spec.py"),
    os.path.join(TOOLS, "raw_ap_layout_CSHL047_Probe01_2026-08-18.json"),
    os.path.join(TOOLS, "raw_ap_layout_CSHL047_Probe01_2026-08-18.txt"),
    os.path.join(TOOLS, "filter_chain_2026-08-18.json"),
    os.path.join(TOOLS, "rc007_round3_2026-08-18.json"),
    os.path.join("Reproducibility Packet", "results", "host_timing_index.jsonl"),
]

MUTATIONS = [
    ("revert 19.5 to the unconditional claim",
     "A value **above** `M` withholds the measurement **where, and only where, "
     "`R_space_sampled ≤ M`**",
     "A value **above** `M` is sufficient to withhold the measurement"),
    ("drop the asymmetry rule from 19.5",
     "Stated as one rule: **`R_null_sampled` can convert a would-be pass into "
     "`unmeasurable`, and can change how a failure reads; it never converts a "
     "would-be failure into anything else.**",
     "Stated as one rule: the null is read in one direction only."),
    ("drop the asymmetry rule from 19.6",
     "can change how a failure reads — and it never converts a would-be "
     "failure into anything else.**",
     "can change how a failure reads.**"),
    ("revert 19.10's bullet to the unconditional form",
     "A value above `M` withholds the measurement **only where "
     "`R_space_sampled ≤ M`**",
     "A value above `M` withholds the measurement;"),
    ("remove 19.12's supersession note",
     "**This subsection records Draft 31 and is left as written, with one of "
     "its claims superseded by §19.13:",
     "**This subsection records Draft 31 and is left as written:"),
    ("unsettle the split decision",
     "the answer is **contiguous halves**",
     "the answer is not taken in this draft"),
    ("drop the direction of the refused alternative",
     "register, in the **permissive** direction, on the one side",
     "register, in some direction, on the one side"),
    ("hide that the split argument is unmeasured",
     "**This argument is structural and unmeasured**",
     "**This argument is settled**"),
    ("break 19.6's branch 4",
     "4. **Resolution.** `R_space_sampled ≤ M` and `R_null_sampled > M` "
     "→ **unmeasurable**",
     "4. **Resolution.** `R_null_sampled > M` → **unmeasurable**"),
    ("delete one restatement of the coverage duration from 19.13",
     "the coverage guarantee is 170 chunks / 73.780 s. §19.2's measured "
     "layout",
     "the coverage guarantee is unchanged. §19.2's measured layout"),
    ("remove 19.13's record of the counter-argument",
     "may not resolve at scale `M`",
     "may not matter here"),
    ("edit a closed section",
     "## 17. Sessions 36–39",
     "## 17. Sessions 36-39"),
]


def stage(case_root, repo_root, doc_text):
    for rel in [DOC, PROBE] + CARRIED:
        target = os.path.join(case_root, rel)
        parent = os.path.dirname(target)
        if not os.path.isdir(parent):
            os.makedirs(parent)
        if rel == DOC:
            io.open(target, "w", encoding="utf-8", newline="").write(doc_text)
        else:
            shutil.copy(os.path.join(repo_root, rel), target)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--python", default=None)
    args = parser.parse_args(argv)

    repo_root = os.path.abspath(args.repo_root)
    python = args.python or sys.executable
    original = io.open(os.path.join(repo_root, DOC), encoding="utf-8",
                       newline="").read()

    if not os.path.isdir(args.work_root):
        os.makedirs(args.work_root)
    work = tempfile.mkdtemp(prefix="rc008_mutation_", dir=args.work_root)

    caught = 0
    stale = 0
    problems = []
    try:
        control = os.path.join(work, "control")
        stage(control, repo_root, original)
        result = subprocess.run(
            [python, os.path.join(control, PROBE), "--repo-root", control],
            capture_output=True, text=True)
        print("control run: exit %d" % result.returncode)
        if result.returncode != 0:
            problems.append("the control run is not green")
            for line in result.stdout.splitlines():
                if line.startswith("FAIL"):
                    print("  control %s" % line)

        for index, (name, old, new) in enumerate(MUTATIONS):
            occurrences = original.count(old)
            if occurrences != 1:
                stale += 1
                problems.append("%s: source string matched %d times"
                                % (name, occurrences))
                print("%-52s ANCHOR STALE (%d matches)" % (name, occurrences))
                continue
            case = os.path.join(work, "m%d" % index)
            stage(case, repo_root, original.replace(old, new, 1))
            result = subprocess.run(
                [python, os.path.join(case, PROBE), "--repo-root", case],
                capture_output=True, text=True)
            reds = [line for line in result.stdout.splitlines()
                    if line.startswith("FAIL")]
            ok = result.returncode != 0 and bool(reds)
            print("%-52s caught=%-5s red=%d" % (name, ok, len(reds)))
            if ok:
                caught += 1
            else:
                problems.append("%s: not caught" % name)

        print("")
        print("%d of %d mutations caught" % (caught, len(MUTATIONS)))
        for problem in problems:
            print("PROBLEM: %s" % problem)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    return 0 if caught == len(MUTATIONS) and not problems and not stale else 1


if __name__ == "__main__":
    sys.exit(main())
