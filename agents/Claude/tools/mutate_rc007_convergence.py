"""Mutation harness for probe_rc007_convergence.py.

A checker that has never been shown to go red is not evidence. This harness
breaks the frozen selection document four ways, one breakage per clean copy,
and requires that the convergence probe fail on the *specific* check that
covers each breakage rather than only on the whole-document digest.

Every mutation also trips the digest check, because the candidate is frozen;
that is expected and is not what is being tested here. What is tested is that
the surface census, the approved-anchor check and the conditioned-statement
check each have real coverage.

Usage:

    ./venv/Scripts/python.exe agents/Claude/tools/mutate_rc007_convergence.py \
        --repo-root . --work-root <writable scratch directory>

The harness deletes its own working tree. It exits non-zero unless the control
run is green and every mutation is caught on its own check.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

DOC = os.path.join("agents", "Claude",
                   "Tier A Host and Injection Zone Selection.md")
PROBE = os.path.join("agents", "Claude", "tools", "probe_rc007_convergence.py")

MUTATIONS = [
    ("remove the 19.10 surface",
     "A value above `M` withholds the measurement",
     "A value above `M` is recorded",
     ["unconditional surface present exactly 1 time(s): section 19.10",
      "the unconditional claim is live on FOUR surfaces, not three"]),
    ("soften the 19.5 surface",
     "A value **above** `M` is sufficient to withhold the measurement",
     "A value **above** `M` may withhold the measurement",
     ["unconditional surface present exactly 1 time(s): section 19.5",
      "the unconditional claim is live on FOUR surfaces, not three"]),
    ("break the approved 16.7 anchor",
     "If `Delta_10min <= L` but `Q95_null > L`, the candidate is also rejected "
     "as unmeasurable",
     "If `Delta_10min <= L` but `Q95_null > L`, the candidate is also refused",
     ["section 16.7 anchor present exactly once"]),
    ("weaken the conditioned statement in 19.5",
     "if `R_null_sampled` exceeds the spatial tolerance and `R_space_sampled` "
     "does not, the candidate is `unmeasurable` rather than passing or failing",
     "if `R_null_sampled` exceeds the spatial tolerance the candidate is "
     "`unmeasurable`",
     ["the correctly conditioned statement is present exactly once"]),
]


def stage(case_root, repo_root, doc_text):
    os.makedirs(os.path.join(case_root, "agents", "Claude", "tools"))
    with open(os.path.join(case_root, DOC), "w", encoding="utf-8",
              newline="") as handle:
        handle.write(doc_text)
    shutil.copy(os.path.join(repo_root, PROBE), os.path.join(case_root, PROBE))


def run_probe(python, case_root, out_path):
    return subprocess.run(
        [python, os.path.join(case_root, PROBE), "--repo-root", case_root,
         "--out", out_path],
        capture_output=True, text=True)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--python", default=None,
                        help="interpreter to run the probe with; defaults to "
                             "the one running this harness")
    args = parser.parse_args(argv)

    repo_root = os.path.abspath(args.repo_root)
    python = args.python or sys.executable
    original = open(os.path.join(repo_root, DOC), encoding="utf-8").read()

    if not os.path.isdir(args.work_root):
        os.makedirs(args.work_root)
    work = tempfile.mkdtemp(prefix="rc007_conv_", dir=args.work_root)

    caught = 0
    problems = []
    try:
        control = os.path.join(work, "control")
        stage(control, repo_root, original)
        result = run_probe(python, control, os.path.join(work, "control.txt"))
        print("control run: exit %d" % result.returncode)
        if result.returncode != 0:
            problems.append("the control run is not green")

        for index, (name, old, new, expected) in enumerate(MUTATIONS):
            occurrences = original.count(old)
            if occurrences != 1:
                problems.append("%s: its source string matched %d times"
                                % (name, occurrences))
                print("%-44s ANCHOR STALE (%d matches)" % (name, occurrences))
                continue
            case = os.path.join(work, "m%d" % index)
            stage(case, repo_root, original.replace(old, new))
            result = run_probe(python, case,
                               os.path.join(work, "m%d.txt" % index))
            failed = [line for line in result.stdout.splitlines()
                      if line.startswith("FAIL")]
            hit = [check for check in expected
                   if any(check in line for line in failed)]
            ok = result.returncode != 0 and len(hit) == len(expected)
            print("%-44s caught=%-5s failing=%d specific=%d/%d"
                  % (name, ok, len(failed), len(hit), len(expected)))
            if ok:
                caught += 1
            else:
                problems.append("%s: %s" % (name, [l[:70] for l in failed]))

        print("")
        print("%d of %d mutations caught on their own check"
              % (caught, len(MUTATIONS)))
        for problem in problems:
            print("PROBLEM: %s" % problem)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    return 0 if caught == len(MUTATIONS) and not problems else 1


if __name__ == "__main__":
    sys.exit(main())
