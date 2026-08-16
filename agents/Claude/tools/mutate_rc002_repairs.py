"""Undo one RC-002 repair at a time and confirm the acceptance suite notices.

A harness written *after* a repair can encode the repair rather than the
property it is supposed to establish: every case passes, and would have passed
against a subtly different fix. The only way to know the difference is to remove
each repair and watch the suite go red.

Each mutation below reverts exactly one repair made for one of Codex's findings,
in its own clean copy of the tree, runs ``test_measure_host_drift.py`` there, and
requires the cases named beside it to fail. The unmutated control copy must pass.
One mutation per copy, so no mutation can mask or amplify another.

**What this harness covers, stated exactly rather than as "every repair".** It
covers F1, F2, F3, F4 and F6 from Codex's RC-002 Round-1 ledger, the Round-2
repairs F1-R1a, F1-R1b, F2-R1 and F6-R1, the three parts of the F1-R2 repair
made after RC-002 closed unapproved, and the four RC-003 Round-1 repairs --
provenance authentication on each asset, exact AP-series ownership, and the
per-path read budget. **It does not cover F5, and cannot.** F5's
repair was not an edit: it was moving the command into the packet and declaring
it pending in the runbook checker. This harness reverts one anchored string in
one file per copy, and neither half of F5 is a string it can revert. The
command's own ``sys.path`` line looks like the candidate and is not one --
CPython puts a directly executed script's own directory on ``sys.path`` anyway,
so removing that line changes nothing observable and a mutation entry for it
would have been a green tick with nothing behind it. What does cover the two
halves is stated so the gap is not silent: the acceptance suite runs the moved
command as a subprocess with ``PYTHONPATH`` cleared and requires ``--help`` to
work, and ``mutation_test_runbook_checker.py`` mutates the checker's
``PENDING_STEP`` handling. This paragraph is the narrowing Codex's RC-002-E1
asked for, and it replaces the claim that every finding's repair is mutated
here.

**The F1d entry is the one to read if you read only one.** It does not touch the
provenance read at all: it sets ``spent_bytes`` to zero, which leaves the plan
blind to everything preflight already transferred. That is byte-for-byte the
state the post-ceiling ``source_provenance`` call created, and what notices it
is not a case written for provenance but the invariant ``run_case`` now applies
to every fixture that reaches a record. The defect that closed RC-002 would fail
this suite today without anyone having to look for it.

**And it is the entry that caught a regression in this suite during the RC-003
repair, which is the strongest thing the harness has done.** The fixture F1d
used to rely on carried a 4.2 MB provenance value; the RC-003 repair refuses
that value, so the case was rewritten at a size the budget admits -- and at 32 KB
under the default 1 MiB blocks, one block covers the whole fixture, the
invariant's comparison is true whatever the plan says, and F1d went undetected.
Nothing else noticed: the suite was green at 321 checks and every other mutation
was still caught. The case now runs at 4 KiB blocks, where the preflight reads
are many blocks and a plan blind to them is short by a measurable amount. **The
lesson is not about block sizes.** It is that a repair somewhere else can
silently remove the coverage a mutation depends on, and the only thing that says
so is running the mutations again after the repair.

Three more of the entries are worth reading rather than counting. The F1 mutation
puts the ceiling back on the stored payload, which is the exact defect Codex
reproduced in Round 1. The F1b mutation puts the ceiling back on the two memory
figures separately, which is the Round-2 defect: each part fits and their sum
does not. The F2b mutation removes the per-unit column-length check, and what
the suite notices is not a refusal but a raise: without the check the command
does not reach a verdict, it crashes -- so either the case's own assertion or
the harness recording the exception counts as noticing, and both names are
listed.

**The RC-003 entries divide the two halves of one property, and that division
is the finding.** F1h removes the read budget and the suite still stops the run
-- because the retention cap catches the oversized value afterwards -- so the
mutation is caught by the *spend*, not by the verdict: `vlen_refusal` fails on
how many bytes moved, and nothing else does. That is exactly Codex's RC-003-F3
in miniature: an accounted spend and a refused one are different properties, and
a suite that only watched the verdict would have called the unbounded read
fixed. F1e is the mirror: it removes the retention cap, which the budget makes
look unreachable until HDF5 serves a cached value for sixteen bytes.

**One entry is platform-conditional and says so here rather than pretending
otherwise.** F6c removes the path-alias resolution and leaves a plain string
comparison. That is observable only on a case-insensitive filesystem, which is
what this project runs on; on a case-sensitive one the acceptance case correctly
asserts that two case-distinct paths are two files, and this mutation would not
be caught there. The reported total is therefore a statement about this machine
for that one entry.

This is evidence about the harness, not about any recording. Nothing here reads
the archive, and no fixture resembles a real candidate.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Claude/tools/mutate_rc002_repairs.py" --repo-root .
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

MUTATIONS = [
    ("F1 the ceiling watches only the stored payload", UNITS,
     'if max_bytes is not None and plan["peak_resident_bytes"] > max_bytes:',
     'if max_bytes is not None and plan["logical_bytes"] > max_bytes:',
     # The names below are prefixes of the *first token* of a failed check's
     # name, which is what the suite prints and what this file matches on.
     [("ceiling_blocks/a",), ("ceiling_blocks/refusal",),
      ("ceiling_resident/refused",)]),
    # Restores the superseded rule: round the element range out to whole chunks
    # and place it as one contiguous span, which is what assuming chunk
    # contiguity amounts to.
    ("F1a the chunk bound assumes one contiguous span", UNITS,
     '    chunk_map = layout.get("chunk_map")\n    chunk = layout["chunk_elements"]\n'
     '    if chunk_map is not None and chunk:',
     '    chunk_map = layout.get("chunk_map")\n    chunk = layout["chunk_elements"]\n'
     '    if chunk:\n'
     '        element_lo = (lo // chunk) * chunk\n'
     '        element_hi = ((hi + chunk - 1) // chunk) * chunk\n'
     '        start = (layout["offset"] or 0) + element_lo * layout["itemsize"]\n'
     '        span = (element_hi - element_lo) * layout["itemsize"]\n'
     '        return _blocks_covering(start, span, block_bytes), "chunk offsets"\n'
     '    if False:',
     # Only the bound check. The ceiling case is derived from the bound, so a
     # smaller bound makes a smaller ceiling and the read is still refused --
     # requiring that one to fail would be requiring the wrong thing.
     [("fragmented/bound_covers_actual",)]),
    ("F1b the memory figures are checked one at a time", UNITS,
     '        if max_bytes is not None and plan["peak_resident_bytes"] > max_bytes:',
     '        if max_bytes is not None and max(plan["cache_bound_bytes"],\n'
     '                                         plan["resident_bytes"]) > max_bytes:',
     [("combined/refused",)]),
    ("F1c the library's own chunk cache is not counted", UNITS,
     '"peak_resident_bytes": cache_bound + resident + structures + library_cache,',
     '"peak_resident_bytes": cache_bound + resident + structures,',
     # Only a chunked column has a library chunk cache, so only the chunked
     # fixture can see this term go missing.
     [("chunked/peak_includes_library_cache",)]),
    # The three below are the RC-002-F1-R2 repair, made after that card closed
    # unapproved. F1d is the accounting half: a plan blind to what preflight
    # already spent is byte-for-byte the state a post-ceiling read created.
    ("F1d the plan is blind to what preflight already spent", UNITS,
     "                             block_bytes, size, spent_bytes=remote.n_bytes,",
     "                             block_bytes, size, spent_bytes=0,",
     [("budget_admits/transfer_inside_the_bound",
       "case_budget_admits_a_value_it_can_afford/raised")]),
    ("F1e an oversized provenance value is retained whole", UNITS,
     "        out[path] = _capped(str(value), max_bytes)",
     "        out[path] = str(value)",
     [("cached_cap/retained_value_is_capped",)]),
    ("F1f a value whose stored size is readable is read anyway", UNITS,
     "        stored = _stored_value_bytes(node)",
     "        stored = None",
     [("stored_provenance/refused_before_the_read_not_by_the_budget",)]),
    # The four RC-003 Round-1 repairs. F1g and F1i are the two halves of
    # provenance authentication; F1h is the budget; F2d is series ownership.
    ("F1g the processed asset's provenance is recorded, not authenticated", UNITS,
     '        authentication = authenticate_provenance(\n'
     '            provenance, "processed asset %s" % url.rsplit("/", 1)[-1])',
     '        authentication = {"path": REQUIRED_PROVENANCE_PATH, "value": "",\n'
     '                          "token": CONVERSION_SOURCE_TOKEN, "source": "unchecked"}',
     [("no_processed_provenance/refused",), ("foreign_conversion/refused",)]),
    ("F1h the provenance read is unbounded again", UNITS,
     "            with reader.budget(max_bytes):\n                value = node[()]",
     "            if True:\n                value = node[()]",
     # Not the verdict: the retention cap still stops the run. What changes is
     # how many bytes moved to get there, which is the whole point of RC-003-F3.
     [("vlen_refusal/spend_is_far_below_the_value",)]),
    ("F1i the raw asset's provenance is not authenticated", CLI,
     '    try:\n'
     '        raw_auth = archive_units.authenticate_provenance(\n'
     '            raw_prov["provenance"], "raw asset %s" % raw_asset["path"])\n'
     '    except ValueError as exc:\n'
     '        raise SystemExit("[fatal] input error: %s" % exc)',
     '    raw_auth = {"path": archive_units.REQUIRED_PROVENANCE_PATH, "value": "",\n'
     '                "token": archive_units.CONVERSION_SOURCE_TOKEN,\n'
     '                "source": "unchecked"}',
     [("no_raw_provenance/refused", "case_missing_raw_provenance_is_an_input_error/raised")]),
    ("F2d AP-series ownership is a substring again", CLI,
     '    matches = [entry for entry in series if series_probe(entry["name"]) == probe]',
     '    matches = [entry for entry in series if probe in entry["name"]]',
     [("impostor/refused",)]),
    ("F2c a floating-point ragged index is accepted when whole", UNITS,
     "    if require_integer_dtype:", "    if False:",
     [("float_index/refused",), ("fractional_offsets/refused",)]),
    ("F2a structural columns are coerced, not checked", UNITS,
     "    values = node[name][:]\n    if np.issubdtype(values.dtype, np.integer):\n"
     "        return [int(v) for v in values]",
     "    values = node[name][:]\n    if True:\n"
     "        return [int(v) for v in values]",
     [("fractional_offsets/refused",), ("fractional_electrode/refused",)]),
    ("F2b one-value-per-unit lengths are unchecked", UNITS,
     'for name in ("label", "max_electrode", "times_index", "depths_index"):',
     'for name in ():',
     [("short_column/refused", "case_short_unit_column_is_refused/raised")]),
    ("F3a the asset pair is not authenticated", CLI,
     "    subjects = (dandi.subject_of(raw), dandi.subject_of(processed))",
     "    return raw, processed\n"
     "    subjects = (dandi.subject_of(raw), dandi.subject_of(processed))",
     [("cross_subject/refused",), ("stem_mismatch/refused",)]),
    ("F3b AP timestamp coverage is unchecked", CLI,
     "    if n_timestamps is None or n_samples is None or "
     "int(n_timestamps) != int(n_samples):",
     "    if False:",
     [("timestamp_coverage/refused",)]),
    ("F4 the band contiguity gap is typeable again", CLI,
     '    parser.add_argument("--block-kb", type=int, default=1024,',
     '    parser.add_argument("--max-gap-um", type=float, default=40.0)\n'
     '    parser.add_argument("--block-kb", type=int, default=1024,',
     [("pinned_gap/typed",)]),
    ("F6a the declared outputs are not cleared", CLI,
     "    clear_outputs((args.out, args.records))\n", "",
     [("stale/report",), ("stale/record",), ("stale/files",)]),
    ("F6b --out and --records may name one path", CLI,
     "    if args.records and same_output_path(args.records, args.out):",
     "    if False:",
     [("same_path/refused",), ("aliases/detour_caught",)]),
    ("F6c output paths are compared as strings", CLI,
     "    if os.path.exists(first) and os.path.exists(second):\n"
     "        try:\n"
     "            return os.path.samefile(first, second)\n"
     "        except OSError:\n"
     "            pass\n"
     "    return (os.path.normcase(os.path.realpath(first))\n"
     "            == os.path.normcase(os.path.realpath(second)))",
     "    return os.path.abspath(first) == os.path.abspath(second)",
     [("aliases/case_alias_caught",)]),
]


def read(path):
    """Read a file without rewriting its line endings."""
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


def run_suite(target, python):
    """Run the acceptance suite inside one copy.

    Returns:
        A ``(status, failed_names, summary)`` triple.
    """
    result = subprocess.run([python, os.path.join(target, HARNESS)],
                            capture_output=True, text=True, cwd=target)
    failed = set(re.findall(r"^  FAILED (\S+)", result.stdout, re.M))
    summary = [line for line in result.stdout.splitlines() if " checks, " in line]
    return result.returncode, failed, (summary[-1] if summary else result.stderr[-200:])


def parse_args(argv=None):
    """Parse command-line arguments."""
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
    """Run the control and every mutation, and report what was noticed."""
    args = parse_args(argv)
    work_root = args.work_root or tempfile.mkdtemp(prefix="rc002_mutation_")
    os.makedirs(work_root, exist_ok=True)
    problems = []
    try:
        control = clean_copy(args.repo_root, work_root, "control")
        status, failed, summary = run_suite(control, args.python)
        healthy = status == 0 and not failed
        print("%-46s exit=%d  %s  %s"
              % ("control (unmutated)", status,
                 "PASSES as it should" if healthy else "BROKEN", summary))
        if not healthy:
            problems.append("control")
        if not args.keep:
            shutil.rmtree(control, ignore_errors=True)

        for index, (name, relative, old, new, expected) in enumerate(MUTATIONS):
            target = clean_copy(args.repo_root, work_root, "mutation%02d" % index)
            apply_mutation(target, relative, old, new)
            status, failed, summary = run_suite(target, args.python)
            missed = [group for group in expected
                      if not any(case.startswith(prefix)
                                 for prefix in group for case in failed)]
            caught = status != 0 and not missed
            print("%-46s exit=%d  %s  %s"
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
    print("[ok] all %d mutations detected, and the unmutated control passes"
          % len(MUTATIONS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
