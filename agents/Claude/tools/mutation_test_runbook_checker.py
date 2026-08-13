"""Break the packet one way at a time and confirm the checker says so.

Each case gets its own clean copy, so a mutation cannot mask or amplify another.
Written to a file rather than piped through a heredoc: the shell eats backslash
escapes, and one of these cases is entirely about a backslash.
"""
import io
import os
import shutil
import subprocess
import sys

PACKET = sys.argv[1]
WORK = sys.argv[2]
PYTHON = sys.argv[3]

BS = chr(92)
NL = chr(10)


def read(path):
    with io.open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write(path, text):
    with io.open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def sub(root, rel, old, new):
    path = os.path.join(root, rel)
    text = read(path)
    assert old in text, f"{rel}: anchor not found"
    write(path, text.replace(old, new, 1))


ZONE = "scripts/audit_zone_neighbour_enrichment.py"
ZONE_CMD = ("    python scripts/audit_zone_neighbour_enrichment.py --cache "
            "results/templates_snapshot_2026-08-11.csv --zone CA1 --out "
            "results/zone_neighbour_enrichment_CA1.txt")


def case_docstring_flag(root):
    sub(root, "scripts/audit_donor_provenance.py", "--host-subject NYU-11", "--host-subject KS042")


def case_readme_flag(root):
    sub(root, "README.md", "--zone CA1 --out results/zone_neighbour",
        "--zone SUB --out results/zone_neighbour")


def case_wrong_step_number(root):
    sub(root, "scripts/audit_template_library.py", "**Step 1**", "**Step 9**")


def case_step_unnamed(root):
    sub(root, "scripts/derive_ccf_label_map.py", "This is **Step 4** of", "This is a step of")


def case_no_example(root):
    path = os.path.join(root, "scripts/audit_subject_provenance.py")
    text = read(path)
    start = text.index(NL + "Example" + NL + "-------" + NL)
    end = text.index('"""', 3)
    write(path, text[:start + 1] + text[end:])


def case_two_examples(root):
    path = os.path.join(root, ZONE)
    text = read(path)
    end = text.index('"""', 3)
    extra = NL + "Example" + NL + "-------" + NL + "    python scripts/something_else.py" + NL
    write(path, text[:end] + extra + text[end:])


def case_orphan_script(root):
    write(os.path.join(root, "scripts/orphan_tool.py"), '"""An orphan with no runbook step."""' + NL)


def case_collapsed_continuation(root):
    wrapped = ("    python scripts/audit_zone_neighbour_enrichment.py " + BS + NL +
               "        --cache results/templates_snapshot_2026-08-11.csv " + BS + NL +
               "        --zone CA1 " + BS + NL +
               "        --out results/zone_neighbour_enrichment_CA1.txt")
    sub(root, ZONE, ZONE_CMD, wrapped)


def case_doubled_space(root):
    sub(root, ZONE, "--zone CA1 --out", "--zone CA1  --out")


def case_missing_script(root):
    os.remove(os.path.join(root, "scripts/audit_amplitude_conventions.py"))


CASES = [
    ("docstring flag changed", case_docstring_flag),
    ("README flag changed", case_readme_flag),
    ("wrong step number", case_wrong_step_number),
    ("step number not named", case_step_unnamed),
    ("Example block deleted", case_no_example),
    ("two Example blocks", case_two_examples),
    ("script with no step", case_orphan_script),
    ("collapsed line continuation", case_collapsed_continuation),
    ("doubled space in command", case_doubled_space),
    ("script named by a step is gone", case_missing_script),
]


def prepare(root):
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    shutil.copy(os.path.join(PACKET, "README.md"), os.path.join(root, "README.md"))
    shutil.copytree(os.path.join(PACKET, "scripts"), os.path.join(root, "scripts"),
                    ignore=shutil.ignore_patterns("__pycache__"))


def run_checker(root):
    result = subprocess.run(
        [PYTHON, os.path.join(root, "scripts/check_runbook_consistency.py"),
         "--readme", os.path.join(root, "README.md"),
         "--scripts", os.path.join(root, "scripts")],
        capture_output=True, text=True)
    return result.returncode, result.stdout


def main():
    prepare(os.path.join(WORK, "control"))
    code, output = run_checker(os.path.join(WORK, "control"))
    print(f"{'control (unmutated)':<34} exit={code}  "
          f"{'PASSES as it should' if code == 0 else 'FAILS -- the suite itself is broken'}")
    if code != 0:
        print(output)
        sys.exit(1)

    failures = 0
    for label, mutate in CASES:
        root = os.path.join(WORK, label.replace(" ", "_"))
        prepare(root)
        mutate(root)
        code, output = run_checker(root)
        caught = code == 1
        failures += 0 if caught else 1
        reason = ""
        for line in output.split(NL):
            if line.strip().startswith("- "):
                reason = line.strip()[2:]
                break
        print(f"{label:<34} exit={code}  {'CAUGHT' if caught else 'MISSED'}  {reason[:88]}")

    print()
    if failures:
        sys.exit(f"[fail] {failures} of {len(CASES)} mutations went undetected")
    print(f"[ok] all {len(CASES)} mutations detected, and the unmutated control passes")


if __name__ == "__main__":
    main()
