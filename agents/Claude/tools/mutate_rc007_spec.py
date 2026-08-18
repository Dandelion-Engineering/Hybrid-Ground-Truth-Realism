"""Prove that ``probe_rc007_spec.py`` can go red, one breakage per clean copy.

A green claim checker over prose is worth nothing until someone shows it can
fail. This harness builds a minimal scratch tree holding only the files the
checker reads, applies exactly one mutation to a clean copy each time, and
requires the checker to exit non-zero. A control run over the unmutated copy
must exit zero, so a harness that fails everything is caught too.

The mutation set covers every family of claim Section 19 makes: a layout figure,
a derived projection, a threshold in the section and the same threshold in the
status line, a window-grid figure, a filter parameter, a filter measurement read
back from its own record, a measured sampling rate, a verdict branch, a
convention direction, a withdrawn proposal, a reintroduced retired string, a
percentile rank, and a frozen span.

Two of these families exist because Round 1 of RC-007 found the checker blind to
them, and one exists because Draft 30 repaired a claim rather than a number: a
retired string reintroduced beside its replacement leaves a document with two
answers, and a checker that only looks for the new string goes green on it.

A mutation whose source string does not match its file exactly once is a hard
failure rather than a skipped case, and the harness reads the child's own failed
-check count rather than its exit status alone, because these strings carry
non-ASCII characters on a cp1252 console and an encoding crash would otherwise
look exactly like a caught mutation.

Example:
    ./venv/Scripts/python.exe "agents/Claude/tools/mutate_rc007_spec.py" \
        --repo-root . --work-root "%TEMP%/rc007_mutation"
"""

import argparse
import io
import os
import shutil
import subprocess
import sys

DOC_REL = os.path.join("agents", "Claude", "Tier A Host and Injection Zone Selection.md")
LAYOUT_REL = os.path.join("agents", "Claude", "tools",
                          "raw_ap_layout_CSHL047_Probe01_2026-08-18.json")
REPORT_REL = os.path.join("agents", "Claude", "tools",
                          "raw_ap_layout_CSHL047_Probe01_2026-08-18.txt")
FILTER_REL = os.path.join("agents", "Claude", "tools", "filter_chain_2026-08-18.json")
ROUND3_REL = os.path.join("agents", "Claude", "tools",
                          "rc007_round3_2026-08-18.json")
TIMING_REL = os.path.join("Reproducibility Packet", "results", "host_timing_index.jsonl")
PROBE_REL = os.path.join("agents", "Claude", "tools", "probe_rc007_spec.py")

COPIED = (DOC_REL, LAYOUT_REL, REPORT_REL, FILTER_REL, ROUND3_REL, TIMING_REL,
          PROBE_REL)

# (name, file, old, new) -- each old must appear exactly once in its file.
MUTATIONS = [
    # --- layout, and what the section derives from it ---------------------
    ("layout figure: chunk shape in the table",
     DOC_REL, "| chunk shape | **13,020 samples", "| chunk shape | **13,021 samples"),
    ("derived projection: whole-run transfer",
     DOC_REL, "957,031,364 bytes for a sixty-window run",
     "957,031,365 bytes for a sixty-window run"),
    ("derived projection: the chunks a run transfers",
     DOC_REL, "is **180 chunks** at 9,999,360", "is **170 chunks** at 9,999,360"),
    ("record: the recorded offset",
     LAYOUT_REL, '"offset": 0.0', '"offset": 1.0'),
    ("record: the recorded compression level",
     LAYOUT_REL, '"compression_opts": 4', '"compression_opts": 6'),
    ("report: the no-samples-read statement",
     REPORT_REL, "No sample value was read", "Some sample values were read"),

    # --- thresholds, in the section and in the status line ----------------
    ("threshold in the section body: strict spatial tolerance",
     DOC_REL, "`M = √(A_max/A_min) = 2.0`", "`M = √(A_max/A_min) = 2.5`"),
    ("threshold in the parameter table: the level floor",
     DOC_REL, "| **level floor** | **1.25 µV, strict and relaxed alike** |",
     "| **level floor** | **2.25 µV, strict and relaxed alike** |"),
    ("status line: the guaranteed-detection duration",
     DOC_REL, "so the guarantee is **170 chunks, 73.780 s**",
     "so the guarantee is **170 chunks, 63.780 s**"),
    ("status line: the isolation errors",
     DOC_REL, "by **−0.228%** and **+0.283%** at two",
     "by **−0.228%** and **+0.228%** at two"),
    ("status line: the refusal to bound the chunk-size difference",
     DOC_REL, "this draft states **no bound** on that difference",
     "this draft states **a bound** on that difference"),
    ("boundary: the floor does not relax",
     DOC_REL, "**The floor does not relax.**", "**The floor relaxes too.**"),

    # --- the window grid --------------------------------------------------
    ("grid: the largest gap",
     DOC_REL, "at most `g = 170` chunks on rank 1", "at most `g = 171` chunks on rank 1"),
    ("grid: the guaranteed-detection duration",
     DOC_REL, "— **73.780 s** at rank 1's 0.434 s chunk",
     "— **63.780 s** at rank 1's 0.434 s chunk"),
    ("grid: the tight bound stated in chunks",
     DOC_REL, "`g = 170` consecutive whole chunks",
     "`g = 171` consecutive whole chunks"),
    ("grid: the tightness claim itself",
     DOC_REL, "tight in both directions", "loose in both directions"),
    ("grid: the eligibility rule for a window centre",
     DOC_REL, "a full chunk on each side of it",
     "a full chunk on one side of it"),
    ("grid: the index formula in the parameter table",
     DOC_REL,
     "| windows | `K = 60`, at chunk indices "
     "`1 + floor(k·(C−3)/(K−1) + 0.5)` |",
     "| windows | `K = 60`, at chunk indices `floor(k·(C−1)/(K−1) + 0.5)` |"),
    ("grid: the coverage fraction",
     DOC_REL, "**0.600%** of rank 1's extent", "**0.006%** of rank 1's extent"),

    # --- the preprocessing chain -----------------------------------------
    ("filter: the pinned padlen in the chain step",
     DOC_REL, "`padlen=18` is scipy's own default for this particular `sos`",
     "`padlen=19` is scipy's own default for this particular `sos`"),
    ("filter: the margin width in the chain step",
     DOC_REL, "Then discard the **500 margin samples (16.667 ms)** at each end",
     "Then discard the **450 margin samples (15.000 ms)** at each end"),
    ("filter: the retained core after the margin",
     DOC_REL, "**retaining exactly the window chunk's 13,020 samples**",
     "**retaining exactly the window chunk's 12,020 samples**"),
    ("filter: where the margin samples come from",
     DOC_REL,
     "the **last 500 samples of the chunk before it** and the "
     "**first 500 samples of the chunk after it**",
     "the **last 500 samples of the window itself** and the "
     "**first 500 samples of the window itself**"),
    ("filter: the identity the chain now claims",
     DOC_REL, "**it is `FilterRecording.get_traces` for a chunk of 13,020 samples**",
     "**it is roughly what `FilterRecording.get_traces` does**"),
    ("filter record: the closed-form impulse verdict",
     FILTER_REL, '"matches_closed_form": true', '"matches_closed_form": false'),
    ("filter record: the filter order",
     FILTER_REL, '"order": 5', '"order": 4'),

    # --- a first-party record the section quotes --------------------------
    ("timing index: a measured sampling rate",
     TIMING_REL, '"rate_hz": 30000.29837671036', '"rate_hz": 30000.99837671036'),

    # --- the rules the gate reads ----------------------------------------
    ("verdict branch: the resolution branch's heading",
     DOC_REL, "4. **Resolution.**", "4. **Resolutions.**"),
    ("verdict branch: the input-error consequence",
     DOC_REL, "the reason is published, and **the pinned order does not advance past it.**",
     "the reason is published, and **the pinned order advances past it.**"),
    ("convention: the direction of the floor substitution",
     DOC_REL, "imposing `snr_p2p ≥ θ` instead is the **weaker** requirement",
     "imposing `snr_p2p ≥ θ` instead is the **stronger** requirement"),
    ("percentile: the resolved ranks at 72 channels",
     DOC_REL, "those are ranks **8** and **65**", "those are ranks **8** and **64**"),

    # --- the withdrawal, and a retired string put back --------------------
    ("withdrawal: the consequence for section 15.5",
     DOC_REL, "**Consequence for §15.5: none.**", "**Consequence for §15.5: one clause.**"),
    ("withdrawal: the surviving gate count",
     DOC_REL, "the five gates stand as written", "the four gates stand as written"),
    ("superseded string reintroduced outside the withdrawal record",
     DOC_REL, "**Common median reference.** Subtract",
     "**Per-channel mean removal** over the window, then "
     "**Common median reference.** Subtract"),
    ("superseded value reintroduced outside the withdrawal record",
     DOC_REL, "the retained 13,020 samples into two disjoint halves of 6,510",
     "the retained 12,020 samples into two disjoint halves of 6,010"),

    # --- Draft 31's own claims -------------------------------------------
    ("isolation: the negative counterexample in the chain paragraph",
     DOC_REL, "at another, with retained samples moving by **0.547 µV**",
     "at another, with retained samples moving by **0.047 µV**"),
    ("isolation: the counterexample in the round-2 record",
     DOC_REL, "at another, more than a thousand times the claimed figure",
     "at another, less than a thousand times the claimed figure"),
    ("isolation: the refusal to promote the residual into a bound",
     DOC_REL, "fixture diagnostics and are not a bound",
     "fixture diagnostics and are a bound"),
    ("isolation: the independent re-derivation figures",
     DOC_REL, "worst samples `0.547247` and `0.547407 µV`",
     "worst samples `0.547247` and `0.547408 µV`"),
    ("split half: the one-sided statement",
     DOC_REL, "**`R_null_sampled` is one-sided.**",
     "**`R_null_sampled` is two-sided.**"),
    ("split half: the cancelled spread",
     DOC_REL, "the spread is exactly **1**", "the spread is exactly **2**"),
    ("split half: what a passing candidate passes on",
     DOC_REL, "reaches it on `R_space_sampled` alone",
     "reaches it on `R_space_sampled` and `R_null_sampled`"),
    ("split half: the ideal ratio at the new half length",
     DOC_REL, "an `R_null_sampled` near **1.05**",
     "an `R_null_sampled` near **1.06**"),
    ("gate 3: the withdrawal of the discharge claim",
     DOC_REL, "there is none here for §19 to discharge",
     "there is one here for §19 to discharge"),
    ("cost: the three-chunk read",
     DOC_REL, "transfers three chunks and retains one",
     "transfers one chunk and retains one"),
    ("cost: the filtered block in float64",
     DOC_REL, "**43,069,440 bytes as `float64`**",
     "**39,997,440 bytes as `float64`**"),
    ("cost: the refused cheaper arrangement",
     DOC_REL, "twenty windows of five chunks", "twenty windows of four chunks"),
    ("dropped step: the measured size of the mean removal",
     DOC_REL, "**1.746e-10 µV**", "**1.746e-08 µV**"),
    ("standing: the number of review rounds",
     DOC_REL, "This section has been reviewed twice",
     "This section has been reviewed once"),
    ("round 3 record: the isolated scale error at one seed",
     ROUND3_REL, '"relative_sigma_error": -0.002284446744258206',
     '"relative_sigma_error": -0.000002284446744258'),
    ("round 3 record: the cancelled split-half spread",
     ROUND3_REL, '"cancelled_spread": 1.0', '"cancelled_spread": 4.0'),

    # --- the spans that must not move ------------------------------------
    ("frozen span: section 18 body",
     DOC_REL, "### 18.8 Boundaries on this section",
     "### 18.8 Boundaries on this section, revised"),
]


def read(path):
    """Read a UTF-8 file without newline translation.

    Args:
        path: the file to read.

    Returns:
        The file's text.
    """
    with io.open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write(path, text):
    """Write a UTF-8 file without newline translation.

    Args:
        path: the file to write.
        text: the text to write.
    """
    with io.open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def build_tree(repo_root, dest):
    """Copy the files the checker touches into a scratch tree.

    Args:
        repo_root: the real repository root.
        dest: the scratch root to build.

    Returns:
        The scratch root path.
    """
    if os.path.exists(dest):
        shutil.rmtree(dest)
    for rel in COPIED:
        target = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copyfile(os.path.join(repo_root, rel), target)
    return dest


def run_probe(python, root):
    """Run the checker against a scratch tree.

    Args:
        python: interpreter to run it with.
        root: the scratch repository root.

    Returns:
        A ``(returncode, n_failed)`` pair, where ``n_failed`` is read from the
        checker's own summary line and is None when that line is absent. A
        non-zero exit alone would not distinguish a caught mutation from a
        crash, which is how a mutation passes for the wrong reason.
    """
    result = subprocess.run(
        [python, os.path.join(root, PROBE_REL), "--repo-root", root],
        capture_output=True, text=True,
    )
    n_failed = None
    for line in result.stdout.splitlines():
        if line.endswith(" failed") and " checks, " in line:
            n_failed = int(line.split(" checks, ")[1].split(" ")[0])
    return result.returncode, n_failed


def main():
    """Run the control and every mutation.

    Returns:
        Process exit status: 0 when the control passed and every mutation was
        caught.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo-root", required=True, help="path to the repository root")
    parser.add_argument("--work-root", required=True, help="scratch directory to build in")
    parser.add_argument("--python", default=sys.executable,
                        help="interpreter to run the checker")
    args = parser.parse_args()
    repo_root = os.path.abspath(args.repo_root)
    work_root = os.path.abspath(args.work_root)

    clean = build_tree(repo_root, os.path.join(work_root, "clean"))
    code, n_failed = run_probe(args.python, clean)
    print("[control ] exit %s, %s checks failed -- expected 0 and 0" % (code, n_failed))
    failures = 0 if (code == 0 and n_failed == 0) else 1

    caught = 0
    for index, (name, rel, old, new) in enumerate(MUTATIONS):
        case = build_tree(repo_root, os.path.join(work_root, "case%02d" % index))
        path = os.path.join(case, rel)
        text = read(path)
        if text.count(old) != 1:
            print("[ANCHOR  ] %s: source string matched %d times" % (name, text.count(old)))
            failures += 1
            continue
        write(path, text.replace(old, new, 1))
        code, n_failed = run_probe(args.python, case)
        if code == 0 or n_failed is None or n_failed < 1:
            reason = "exit 0" if code == 0 else "summary line said %s" % n_failed
            print("[MISSED  ] %s -- %s" % (name, reason))
            failures += 1
        else:
            print("[caught  ] %s -- %d checks failed" % (name, n_failed))
            caught += 1

    shutil.rmtree(work_root, ignore_errors=True)
    print("\n%d of %d mutations caught, %d failures" % (caught, len(MUTATIONS), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
