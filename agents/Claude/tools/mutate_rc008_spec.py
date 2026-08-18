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
    os.path.join(TOOLS, "rc008_round2_2026-08-18.json"),
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
     "**The split is contiguous, and the reason Draft 32 gave for it is "
     "withdrawn.**",
     "**The split is deferred again.**"),
    ("restore the withdrawn compression direction",
     "**Interleaving expanded the spread, and expanded it from inside the "
     "strict tolerance to outside it.**",
     "**Interleaving compressed the spread, as Draft 32 said it would.**"),
    ("re-claim a direction for the split rule",
     "§19.5 now keeps contiguous halves on three grounds and none of them "
     "is a direction",
     "§19.5 now keeps contiguous halves on the direction it always had"),
    # -- Draft 33's own repairs ------------------------------------------
    ("revert branch 2 to the loudest window",
     "2. **Level, too quiet.** `sigma_quietest_sampled < 1.25 µV`",
     "2. **Level, too quiet.** `sigma_worst_sampled < 1.25 µV`"),
    ("delete the quietest-window quantity from 19.4",
     "   - **`sigma_quietest_sampled = min_{k ∈ G} S(k)`** — the "
     "quietest sampled window's band level, in µV;\n",
     ""),
    ("revert 19.6's admissible band to one statistic",
     "So the admissible band is **`sigma_worst_sampled ≤ N`** together "
     "with **`1.25 µV ≤ sigma_quietest_sampled`**",
     "So the admissible band is **`1.25 µV ≤ sigma_worst_sampled "
     "≤ N`**"),
    ("revert 19.8's ratio to the wrong denominator",
     "`snr_p2p_max = A_max / sigma_quietest_sampled`",
     "`snr_p2p_max = A_max / sigma_worst_sampled`"),
    ("re-widen the identity claim in 19.3",
     "`FilterRecording.get_traces` for a chunk of 13,020 samples in every "
     "respect but the filter's design rate**",
     "`FilterRecording.get_traces` for a chunk of 13,020 samples**"),
    ("drop the padlen/margin invariance from 19.3",
     "scipy's default `padlen` is **18** at both rates",
     "scipy's default `padlen` is unchanged"),
    ("restore the bad-channel conservatism claim",
     "the direction every draft through 32 claimed for that is withdrawn.**",
     "and the spatial check is conservative in the presence of them.**"),
    ("break the corrected coverage figure in 19.9",
     "the guarantee is **228.718 s**",
     "the guarantee is **223 s**"),
    ("restore 19.10's stale Draft-31 sentence",
     "**RC-008's Round 1 returned `Revisions Required` on five blocking "
     "findings and four tracked items; Draft 33 is the owner's Round-2 "
     "response and it is unreviewed**",
     "**This Draft 31 state is not approved by anyone yet**"),
    ("revert the code-step terminology",
     "**One stored code step is 2.34375 µV.**",
     "**One stored bit is 2.34375 µV.**"),
    ("re-widen the phase-omission direction",
     "**No direction at all is claimed for `R_space_sampled`.**",
     "The same direction holds for `R_space_sampled`."),
    ("remove 19.13's supersession note",
     "**This subsection records Draft 32 and is left as written, with one of "
     "its claims superseded by §19.14:",
     "**This subsection records Draft 32 and is left as written:"),
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


# RC-008 F4-R1: the wrapper trusted a subprocess by filename. These mutations
# leave the document untouched and damage the INSTRUMENT instead, which is the
# axis the reviewer's staged counterfeit exploited and which no document
# mutation can reach.
COUNTERFEIT = '''"""A counterfeit legacy checker that prints what the wrapper wants to see."""
import sys

EXPECTED = %r

for name in EXPECTED:
    print("[FAIL] %%s" %% name)
print("288 checks, %%d failed" %% len(EXPECTED))
sys.exit(0)
'''


def expected_failures(repo_root):
    """Return the wrapper's own expected-failure list, read from its source."""
    text = io.open(os.path.join(repo_root, PROBE), encoding="utf-8").read()
    start = text.index("EXPECTED_RC007_FAILURES = [")
    end = text.index("]", start)
    names = []
    for line in text[start:end].splitlines()[1:]:
        line = line.strip()
        if line.startswith('"'):
            names.append(line.split('"')[1])
    return names


def file_mutations(repo_root):
    """Return (name, relative path, replacement bytes) instrument mutations."""
    legacy = os.path.join(TOOLS, "probe_rc007_spec.py")
    record = os.path.join(TOOLS, "filter_chain_2026-08-18.json")
    original_record = io.open(os.path.join(repo_root, record),
                              encoding="utf-8").read()
    return [
        ("substitute a counterfeit legacy checker", legacy,
         COUNTERFEIT % (expected_failures(repo_root),)),
        ("change one byte of the legacy checker", legacy,
         io.open(os.path.join(repo_root, legacy), encoding="utf-8").read()
         + "\n# an undeclared executable change\n"),
        ("tamper with one carried record", record,
         original_record.replace("\n", "\n", 1) + " "),
    ]


def stage(case_root, repo_root, doc_text, overrides=None):
    overrides = overrides or {}
    for rel in [DOC, PROBE] + CARRIED:
        target = os.path.join(case_root, rel)
        parent = os.path.dirname(target)
        if not os.path.isdir(parent):
            os.makedirs(parent)
        if rel in overrides:
            io.open(target, "w", encoding="utf-8",
                    newline="").write(overrides[rel])
        elif rel == DOC:
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
    total = len(MUTATIONS)
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

        instrument = file_mutations(repo_root)
        for index, (name, rel, replacement) in enumerate(instrument):
            case = os.path.join(work, "f%d" % index)
            stage(case, repo_root, original, {rel: replacement})
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

        total = len(MUTATIONS) + len(instrument)
        print("")
        print("%d of %d mutations caught" % (caught, total))
        for problem in problems:
            print("PROBLEM: %s" % problem)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    return 0 if caught == total and not problems and not stale else 1


if __name__ == "__main__":
    sys.exit(main())
