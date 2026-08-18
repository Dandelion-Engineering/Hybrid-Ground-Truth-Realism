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
TIMING_REL = os.path.join("Reproducibility Packet", "results", "host_timing_index.jsonl")
PROBE_REL = os.path.join("agents", "Claude", "tools", "probe_rc007_spec.py")

COPIED = (DOC_REL, LAYOUT_REL, REPORT_REL, FILTER_REL, TIMING_REL, PROBE_REL)

# (name, file, old, new) -- each old must appear exactly once in its file.
MUTATIONS = [
    # --- layout, and what the section derives from it ---------------------
    ("layout figure: chunk shape in the table",
     DOC_REL, "| chunk shape | **13,020 samples", "| chunk shape | **13,021 samples"),
    ("derived projection: whole-run transfer",
     DOC_REL, "319,010,455 bytes for a sixty-window run",
     "319,010,456 bytes for a sixty-window run"),
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
    ("threshold in the status line: the relaxed level ladder",
     DOC_REL, "the relaxation reads `10.0 → 25.0 µV` rather than the stale `12.5`",
     "the relaxation reads `11.0 → 25.0 µV` rather than the stale `12.5`"),
    ("boundary: the floor does not relax",
     DOC_REL, "**The floor does not relax.**", "**The floor relaxes too.**"),

    # --- the window grid --------------------------------------------------
    ("grid: the largest gap",
     DOC_REL, "at most `g = 170` chunks on rank 1", "at most `g = 171` chunks on rank 1"),
    ("grid: the guaranteed-detection duration",
     DOC_REL, "— **74.214 s** at rank 1's 0.434 s chunk",
     "— **64.214 s** at rank 1's 0.434 s chunk"),
    ("grid: the index formula in the parameter table",
     DOC_REL, "| windows | `K = 60`, at chunk indices `floor(k·(C−1)/(K−1) + 0.5)` |",
     "| windows | `K = 60`, at chunk indices `floor(k·C/K)` |"),
    ("grid: the coverage fraction",
     DOC_REL, "**0.600%** of rank 1's extent", "**0.006%** of rank 1's extent"),

    # --- the preprocessing chain -----------------------------------------
    ("filter: the pinned padlen in the chain step",
     DOC_REL, "`padlen=18` is scipy's own default for this particular `sos`",
     "`padlen=19` is scipy's own default for this particular `sos`"),
    ("filter: the margin width in the chain step",
     DOC_REL, "Then discard **500 samples (16.667 ms)** at each end",
     "Then discard **450 samples (15.000 ms)** at each end"),
    ("filter: the measured pole radius",
     DOC_REL, "pole radius `0.980781307`", "pole radius `0.980781306`"),
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
    ("retired string reintroduced: the old retained sample count",
     DOC_REL, "retaining **12,020** samples", "retaining **12,720** samples"),

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
