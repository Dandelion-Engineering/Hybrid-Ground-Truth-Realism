"""Check that every runbook command matches the command its script's --help prints.

`README.md` is the authority on how to reproduce each recorded result, and every
script repeats its own command in the ``Example`` block of its module docstring,
which ``argparse`` prints as the first thing a reader sees in ``--help``. Two
copies of the same command drift, and this project has already paid for that
once: the docstrings were written against a project-root working directory while
the runbook was written against this folder, so ``--help`` and ``README.md``
disagreed about where to stand and what to pass.

Keeping one copy is not an option -- a reader running ``--help`` should not have
to open a second file to find a working invocation -- so the copies are checked
instead. It compares:

1. **Coverage.** Every runnable script has exactly one numbered runbook step,
   and every step names a script that exists.
2. **The command.** The step's fenced command and the docstring's example are
   the same string, character for character.
3. **The step number.** The docstring names the same step the README puts it in.
4. **One command on each side.** A step carries exactly one ``bash`` fence and
   that fence exactly one line; an ``Example`` block carries exactly one
   indented line. Anything a reader would also run has to be somewhere the
   comparison can see it, or it is a second command nothing is checking.

The docstring is read with ``ast``, so what is compared is the string
``argparse`` will print rather than the source text that produces it. That
distinction is not pedantic: a backslash line continuation inside a non-raw
docstring is an escape, so Python deletes the newline and ``--help`` shows one
long line with runs of spaces in it while the source looks neatly wrapped.
Reading the source would have called that agreement. Comparing whole strings
rather than shell tokens is what makes it visible, since the tokens are
identical either way. Examples are therefore single-line, which also means they
copy-paste on PowerShell, where a trailing backslash is not a continuation.

Using ``ast`` also means nothing is imported: a script is parsed, never run.

A failure here is a documentation defect, not a scientific one -- but it is the
kind that makes a reader's first command fail, which is the same thing as the
packet not being reproducible.

Example
-------
Run from the ``Reproducibility Packet`` folder, which is the working directory
every command in ``README.md`` assumes; ``python`` means that folder's own
virtual environment, built in README's Setup section:

    python scripts/check_runbook_consistency.py

It writes no report. Exit status 0 means the runbook and the scripts agree; 1
means they do not, and every disagreement is printed.
"""

import argparse
import ast
import os
import re
import shlex
import sys

PACKET_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# This checker has no numbered step of its own: it reproduces no recorded
# result, so the runbook does not carry it as one. Anything else added to
# scripts/ is expected to be a runbook step and will fail coverage until it is.
NOT_A_STEP = {"check_runbook_consistency.py"}

STEP_HEADING = re.compile(r"^### Step (\d+) — (.+?)\s*\*\*\[(offline|archive)\]\*\*\s*$")
DOCSTRING_STEP = re.compile(r"\*\*Step (\d+)\*\*")


def read_text(path):
    """Read a UTF-8 file without rewriting its line endings.

    Args:
        path: file to read.

    Returns:
        The file's contents as a string.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def parse_readme_steps(readme_path):
    """Extract the numbered runbook steps and their commands.

    Args:
        readme_path: path to the packet's README.md.

    Returns:
        A dict from script basename to (step_number, command_string, mode).

    Raises:
        ValueError: if a step's fenced command is missing, unclosed, empty,
            longer than one line, duplicated by a second fence in the same
            step, or malformed; if two steps claim the same script; or if the
            step numbers are not unique and contiguous from 1.
    """
    text = read_text(readme_path)
    if "## The runbook" not in text:
        raise ValueError(f"{readme_path} has no '## The runbook' section")
    body = text.split("## The runbook", 1)[1]

    steps = {}
    step_numbers = {}
    current = None
    awaiting_command = False
    in_step = False
    in_fence = False
    command_lines = []
    for line in body.split("\n"):
        line = line.rstrip("\r")
        if in_fence:
            if line.startswith("```"):
                if not command_lines:
                    raise ValueError(f"step {current[0]}'s command fence is empty")
                if len(command_lines) > 1:
                    raise ValueError(
                        f"step {current[0]}'s command fence contains "
                        f"{len(command_lines)} non-empty lines; commands must be one line"
                    )
                command = command_lines[0]
                tokens = shlex.split(command)
                if len(tokens) < 2 or tokens[0] != "python":
                    raise ValueError(
                        f"step {current[0]} does not start with 'python <script>'"
                    )
                name = os.path.basename(tokens[1])
                if name in steps:
                    raise ValueError(
                        f"{name} is claimed by steps {steps[name][0]} and {current[0]}"
                    )
                steps[name] = (current[0], command, current[1])
                in_fence = False
                awaiting_command = False
                command_lines = []
            elif line.strip():
                command_lines.append(line.strip())
            continue

        if line.startswith("## "):
            # A new section ends the step region, so a fenced command below it
            # belongs to the section rather than to the last step.
            in_step = False
        heading = STEP_HEADING.match(line)
        if heading:
            if awaiting_command:
                raise ValueError(f"step {current[0]} has no fenced command")
            number = int(heading.group(1))
            if number in step_numbers:
                raise ValueError(
                    f"step number {number} is used by both "
                    f"'{step_numbers[number]}' and '{heading.group(2)}'"
                )
            step_numbers[number] = heading.group(2)
            current = (number, heading.group(3))
            awaiting_command = True
            in_step = True
            continue
        if line.startswith("```bash"):
            if awaiting_command:
                in_fence = True
                command_lines = []
                continue
            if in_step:
                # The step's command was already read, so this fence is a second
                # command the reader would run and nothing would be comparing.
                raise ValueError(
                    f"step {current[0]} has more than one ```bash command fence"
                )
    if in_fence:
        raise ValueError(f"step {current[0]}'s command fence is not closed")
    if awaiting_command:
        raise ValueError(f"step {current[0]} has no fenced command")
    numbers = sorted(step_numbers)
    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        raise ValueError(
            f"runbook step numbers are {numbers}; expected contiguous numbering {expected}"
        )
    return steps


def parse_docstring_example(script_path):
    """Extract a script's docstring example command and the step it names.

    The docstring is taken from the parsed module rather than from the source
    text, so this returns what ``argparse`` prints. The script is parsed, never
    imported.

    Args:
        script_path: path to a packet script.

    Returns:
        A tuple of (command_string, step_number_or_None).

    Raises:
        ValueError: if the script has no module docstring, no Example block,
            more than one Example block, or an Example block that does not
            contain exactly one indented command line.
    """
    docstring = ast.get_docstring(ast.parse(read_text(script_path)), clean=False)
    if docstring is None:
        raise ValueError("no module docstring")
    marker = "\nExample\n-------\n"
    if docstring.count(marker) == 0:
        raise ValueError("no 'Example' block in the module docstring")
    if docstring.count(marker) > 1:
        raise ValueError(f"{docstring.count(marker)} 'Example' blocks in the module docstring")
    after = docstring[docstring.index(marker) + len(marker):]

    # Every indented line in the block is collected, not just the first run of
    # them: --help prints the whole block, so a second command further down is
    # a second command the reader sees, and stopping at the first blank line
    # would leave it uncompared.
    command_lines = [line for line in after.split("\n")
                     if line.startswith("    ") and line.strip()]
    if not command_lines:
        raise ValueError("'Example' block contains no indented command")
    if len(command_lines) > 1:
        raise ValueError(
            f"'Example' block contains {len(command_lines)} indented command lines; it must "
            "contain exactly one, because --help prints all of them and README.md carries one"
        )

    named = DOCSTRING_STEP.search(after)
    return command_lines[0].strip(), int(named.group(1)) if named else None


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--readme", default=os.path.join(PACKET_ROOT, "README.md"),
                        help="packet runbook to check (default: this packet's README.md)")
    parser.add_argument("--scripts", default=os.path.join(PACKET_ROOT, "scripts"),
                        help="scripts directory to check (default: this packet's scripts/)")
    args = parser.parse_args()

    if not os.path.isfile(args.readme):
        sys.exit(f"[fatal] --readme is not a file: {args.readme}")
    if not os.path.isdir(args.scripts):
        sys.exit(f"[fatal] --scripts is not a directory: {args.scripts}")

    try:
        steps = parse_readme_steps(args.readme)
    except (OSError, ValueError) as exc:
        sys.exit(f"[fatal] could not parse the runbook: {exc}")
    on_disk = {name for name in sorted(os.listdir(args.scripts))
               if name.endswith(".py") and name not in NOT_A_STEP}

    problems = []

    missing_step = sorted(on_disk - set(steps))
    for name in missing_step:
        problems.append(f"{name}: no numbered step in the runbook names it")
    missing_file = sorted(set(steps) - on_disk)
    for name in missing_file:
        problems.append(f"{name}: step {steps[name][0]} names a script that is not in {args.scripts}")

    print(f"{'step':>5}  {'script':<38}{'verdict'}")
    print("-" * 62)
    for name, (step, readme_command, mode) in sorted(steps.items(), key=lambda kv: kv[1][0]):
        if name not in on_disk:
            print(f"{step:>5}  {name:<38}MISSING")
            continue
        try:
            doc_command, doc_step = parse_docstring_example(os.path.join(args.scripts, name))
        except (SyntaxError, ValueError) as exc:
            problems.append(f"{name}: {exc}")
            print(f"{step:>5}  {name:<38}NO EXAMPLE")
            continue
        verdicts = []
        if doc_command != readme_command:
            verdicts.append("COMMAND DIFFERS")
            # Same tokens with different characters is the collapsed-continuation
            # failure this check exists for, and it is invisible without saying so.
            note = ("" if shlex.split(doc_command) != shlex.split(readme_command) else
                    "\n    (identical shell tokens, different characters -- look for a "
                    "collapsed line continuation or a doubled space)")
            problems.append(
                f"{name}: step {step} and the docstring example disagree\n"
                f"    README:    {readme_command}\n"
                f"    docstring: {doc_command}{note}"
            )
        if doc_step is None:
            verdicts.append("STEP UNNAMED")
            problems.append(f"{name}: the docstring example does not name its runbook step")
        elif doc_step != step:
            verdicts.append("STEP DIFFERS")
            problems.append(
                f"{name}: the docstring calls it step {doc_step}, the runbook step {step}")
        print(f"{step:>5}  {name:<38}{' + '.join(verdicts) if verdicts else 'ok (' + mode + ')'}")

    for name in missing_step:
        print(f"{'-':>5}  {name:<38}NOT IN THE RUNBOOK")
    print()

    if problems:
        print(f"[fail] {len(problems)} disagreement(s) between README.md and the scripts:\n")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)
    print(f"[ok] {len(steps)} runbook steps agree with their scripts' --help examples")


if __name__ == "__main__":
    main()
