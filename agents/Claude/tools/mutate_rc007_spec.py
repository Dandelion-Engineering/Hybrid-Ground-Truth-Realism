"""Prove that ``probe_rc007_spec.py`` can go red, one breakage per clean copy.

A green claim checker over prose is worth nothing until someone shows it can
fail. This harness builds a minimal scratch tree holding only the three files
the checker reads, applies exactly one mutation to a clean copy each time, and
requires the checker to exit non-zero. A control run over the unmutated copy
must exit zero, so a harness that fails everything is caught too.

Each mutation targets a different family of check: a layout figure, a derived
projection, a threshold, a frozen span, and a declared boundary. A mutation
whose source string does not match its file exactly once is a hard failure
rather than a skipped case.

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
PROBE_REL = os.path.join("agents", "Claude", "tools", "probe_rc007_spec.py")

# (name, file, old, new) -- each old must appear exactly once in its file.
MUTATIONS = [
    ("layout figure: chunk shape in the table",
     DOC_REL, "| chunk shape | **13,020 samples", "| chunk shape | **13,021 samples"),
    ("derived projection: whole run transfer",
     DOC_REL, "319,010,455 bytes for a sixty-window run", "319,010,456 bytes for a sixty-window run"),
    ("threshold in the status line: strict level tolerance",
     DOC_REL, "the level tolerance `N` is `A_min/5 = 10.0", "the level tolerance `N` is `A_min/5 = 11.0"),
    ("threshold in the section body: strict spatial tolerance",
     DOC_REL, "`M = √(A_max/A_min) = 2.0`", "`M = √(A_max/A_min) = 2.5`"),
    ("boundary: the necessary-not-sufficient posture",
     DOC_REL, "necessary condition and not a sufficient one",
     "sufficient condition and not merely a necessary one"),
    ("boundary in the section body: the four-gates supersession",
     DOC_REL, "Host admissibility is therefore decided by four gates rather than five",
     "Host admissibility is therefore decided by five gates rather than four"),
    ("boundary in the status line: the four-gates supersession",
     DOC_REL, "host admissibility is therefore four gates rather than five",
     "host admissibility is therefore five gates rather than four"),
    ("frozen span: section 18 body",
     DOC_REL, "### 18.8 Boundaries on this section",
     "### 18.8 Boundaries on this section, revised"),
    ("record: the recorded offset",
     LAYOUT_REL, '"offset": 0.0', '"offset": 1.0'),
    ("record: the recorded compression level",
     LAYOUT_REL, '"compression_opts": 4', '"compression_opts": 6'),
    ("report: the no-samples-read statement",
     REPORT_REL, "No sample value was read", "Some sample values were read"),
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
    """Copy the four files the checker touches into a scratch tree.

    Args:
        repo_root: the real repository root.
        dest: the scratch root to build.

    Returns:
        The scratch root path.
    """
    if os.path.exists(dest):
        shutil.rmtree(dest)
    for rel in (DOC_REL, LAYOUT_REL, REPORT_REL, PROBE_REL):
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
    parser.add_argument("--python", default=sys.executable, help="interpreter to run the checker")
    args = parser.parse_args()
    repo_root = os.path.abspath(args.repo_root)
    work_root = os.path.abspath(args.work_root)

    clean = build_tree(repo_root, os.path.join(work_root, "clean"))
    code, n_failed = run_probe(args.python, clean)
    print(f"[control ] exit {code}, {n_failed} checks failed -- expected 0 and 0")
    failures = 0 if (code == 0 and n_failed == 0) else 1

    caught = 0
    for index, (name, rel, old, new) in enumerate(MUTATIONS):
        case = build_tree(repo_root, os.path.join(work_root, f"case{index:02d}"))
        path = os.path.join(case, rel)
        text = read(path)
        if text.count(old) != 1:
            print(f"[ANCHOR  ] {name}: source string matched {text.count(old)} times")
            failures += 1
            continue
        write(path, text.replace(old, new, 1))
        code, n_failed = run_probe(args.python, case)
        if code == 0 or n_failed is None or n_failed < 1:
            reason = "exit 0" if code == 0 else f"summary line said {n_failed}"
            print(f"[MISSED  ] {name} -- {reason}")
            failures += 1
        else:
            print(f"[caught  ] {name} -- {n_failed} checks failed")
            caught += 1

    shutil.rmtree(work_root, ignore_errors=True)
    print(f"\n{caught} of {len(MUTATIONS)} mutations caught, {failures} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
