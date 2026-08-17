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


def case_readme_second_command(root):
    command = ZONE_CMD.strip()
    sub(root, "README.md", command + NL + "```",
        command + NL + "python scripts/unexpected_second_command.py" + NL + "```")


def case_wrong_step_number(root):
    sub(root, "scripts/audit_template_library.py", "**Step 1**", "**Step 9**")


def case_duplicate_step_number(root):
    sub(root, "README.md", "### Step 4 —", "### Step 3 —")
    sub(root, "scripts/derive_ccf_label_map.py", "**Step 4**", "**Step 3**")


def case_noncontiguous_step_number(root):
    sub(root, "README.md", "### Step 4 —", "### Step 11 —")
    sub(root, "scripts/derive_ccf_label_map.py", "**Step 4**", "**Step 11**")


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


def case_readme_second_fence(root):
    """A second command fence in the same step, after the first one closed.

    The fence-level form of the second-command escape: the first fence is
    correct, so a parser that stops looking once a step has a command never
    sees the second one a reader would also run.
    """
    command = ZONE_CMD.strip()
    sub(root, "README.md", command + NL + "```",
        command + NL + "```" + NL + NL + "```bash" + NL +
        "python scripts/unexpected_second_fence.py" + NL + "```")


def case_docstring_second_command(root):
    """A second indented command in the same Example block, after a blank line.

    The docstring-level form of the same escape. ``--help`` prints the whole
    block, so the reader sees both commands.
    """
    sub(root, ZONE, ZONE_CMD,
        ZONE_CMD + NL + NL + "    python scripts/unexpected_second_command.py --wrong")


PENDING_ANCHOR = "PENDING_STEP = {" + chr(10)


def declare_pending(root, name, reason):
    """Add one entry to the checker's PENDING_STEP map in a throwaway copy.

    Args:
        root: the copied packet's root.
        name: script basename to declare as pending a runbook step.
        reason: the declaration's stated reason.

    Returns:
        None. The copy's checker is rewritten in place.

    These three cases used to mutate the single real declaration, so when step 11
    emptied PENDING_STEP they lost their anchor and the harness stopped at case
    16 rather than reporting a miss. Building the declaration here means the
    cases exercise the checker's pending branches whether or not any real script
    is pending -- which is the property that broke.
    """
    sub(root, "scripts/check_runbook_consistency.py", PENDING_ANCHOR,
        PENDING_ANCHOR + '    "' + name + '":' + NL + '        "' + reason + '",' + NL)


def case_pending_declaration_names_a_stepped_script(root):
    """A script cannot be both a numbered step and pending one.

    That combination is how the exemption could quietly outlive its reason: the
    step arrives, the declaration stays, and the checker would be excusing a
    script it is also verifying. It has to be an error, not a preference.
    """
    declare_pending(root, "audit_template_library.py", "a script that already has step 1")


def case_pending_declaration_names_a_missing_script(root):
    """A declaration naming a script that is not there is stale, not harmless."""
    declare_pending(root, "a_script_that_does_not_exist.py", "declared but absent")


def case_pending_script_docstring_claims_a_step(root):
    """A pending script whose own docstring names a step contradicts its exemption.

    The declaration says no step exists; the docstring says one does. The checker
    has a branch for exactly that disagreement, and this is the case that keeps
    it honest now that no real script is pending.
    """
    write(os.path.join(root, "scripts/pending_tool.py"),
          '"""A pending tool that claims a step below its Example block.' + NL + NL +
          "Example" + NL + "-------" + NL +
          "    python scripts/pending_tool.py --demo" + NL + NL +
          "The command above is **Step 3** of the runbook." + NL + '"""' + NL)
    declare_pending(root, "pending_tool.py", "declared pending while naming a step")


CASES = [
    ("docstring flag changed", case_docstring_flag),
    ("README flag changed", case_readme_flag),
    ("README second command", case_readme_second_command),
    ("wrong step number", case_wrong_step_number),
    ("duplicate step number", case_duplicate_step_number),
    ("noncontiguous step number", case_noncontiguous_step_number),
    ("step number not named", case_step_unnamed),
    ("Example block deleted", case_no_example),
    ("two Example blocks", case_two_examples),
    ("script with no step", case_orphan_script),
    ("collapsed line continuation", case_collapsed_continuation),
    ("doubled space in command", case_doubled_space),
    ("script named by a step is gone", case_missing_script),
    ("README second command fence", case_readme_second_fence),
    ("docstring second command", case_docstring_second_command),
    ("pending declaration names a stepped script",
     case_pending_declaration_names_a_stepped_script),
    ("pending declaration names a missing script",
     case_pending_declaration_names_a_missing_script),
    ("pending script docstring claims a step",
     case_pending_script_docstring_claims_a_step),
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
    return result.returncode, result.stdout + result.stderr


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
            if line.strip().startswith("[fatal]"):
                reason = line.strip()
                break
        print(f"{label:<34} exit={code}  {'CAUGHT' if caught else 'MISSED'}  {reason[:88]}")

    print()
    if failures:
        sys.exit(f"[fail] {failures} of {len(CASES)} mutations went undetected")
    print(f"[ok] all {len(CASES)} mutations detected, and the unmutated control passes")


if __name__ == "__main__":
    main()
