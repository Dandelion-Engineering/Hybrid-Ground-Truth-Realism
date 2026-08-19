"""Independent terminal delta probe for RC-008 Draft 34.

The probe authenticates the nine-file Round-3 handoff and the three frozen
document spans, replays the owner's fast evidence, independently reconstructs
the ordered decision's split reach, and audits the repaired legacy-input
authentication from the legacy checker's own AST.

It also tests the sole surviving rationale for choosing contiguous halves.
Draft 34 says an interleaved split necessarily carries a free period parameter,
but the concrete alternative used throughout the review is the fixed even/odd
partition. That partition needs no tunable period and already changes the
decision on the owner's parity fixture. The construction varies the data's
periodicity, not a parameter of the fixed split rule.

All fixtures are local and deterministic. No archive or network resource is
read.

Example:
    ./venv/Scripts/python.exe agents/Codex/tools/probe_rc008_round3.py \
        --repo-root . --out agents/Codex/tools/rc008_round3_2026-08-19.txt \
        --records agents/Codex/tools/rc008_round3_2026-08-19.json
"""

import argparse
import ast
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

import numpy as np


DOC_REL = "agents/Claude/Tier A Host and Injection Zone Selection.md"
OWNER_SPEC_REL = "agents/Claude/tools/probe_rc008_spec.py"
LEGACY_SPEC_REL = "agents/Claude/tools/probe_rc007_spec.py"
OWNER_ROUND3_REL = "agents/Claude/tools/probe_rc008_round3.py"
TIMING_REL = "Reproducibility Packet/results/host_timing_index.jsonl"

CANDIDATE_DIGESTS = {
    DOC_REL:
        "ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89",
    OWNER_SPEC_REL:
        "2f20099bbb37e249efa3d609f9214e3b1f423e430052ce5e0cbe10c9aa7343c1",
    "agents/Claude/tools/rc008_spec_2026-08-19_draft34.txt":
        "94277e0e81bdaf760f524843a135fb6fd049a8537f4ae8b585f2d693a65c3d8f",
    "agents/Claude/tools/rc008_spec_2026-08-19_draft34.json":
        "7deafd99f8de066aee9964ad5a5921c2ef2c8af3e78325a9c807ba3f3068afe6",
    "agents/Claude/tools/mutate_rc008_spec.py":
        "2b19e1ec7ad7c4472cc6152b7b2b03e94323da561d7ddf2b22347d1e9208b9d6",
    "agents/Claude/tools/mutate_rc008_spec_2026-08-19_draft34.txt":
        "83b15d934b99e6c993f1de92dc8bab12da5f42c03af9b3c351e7949beef5ba71",
    OWNER_ROUND3_REL:
        "6210e7d2599b52840b1830155f2a64f54f57ebd49c7c6deeea7f3e5985f4d9d9",
    "agents/Claude/tools/rc008_round3_2026-08-19.txt":
        "4edf5eb05631f535861eba5344705ef8d17bd3a0f3cc7ded48162b82356d0464",
    "agents/Claude/tools/rc008_round3_2026-08-19.json":
        "3ca619e4896669b1190958397d388c2eff4a4aa07bd8d6f8cc0aa475340fe9c7",
}

FROZEN_SPANS = [
    ("## 1. ", "## 17. ", 144664,
     "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59"),
    ("## 17. ", "## 18. ", 21864,
     "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a"),
    ("## 18. ", "## 19. ", 20579,
     "8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017"),
]


class Checks:
    """Collect human-readable checks and structured evidence."""

    def __init__(self):
        self.lines = []
        self.records = {}
        self.passed = 0
        self.failed = 0

    def heading(self, value):
        """Append and print a section heading."""
        self.lines.extend(["", value])
        print("\n" + value)

    def check(self, name, condition, detail=""):
        """Record one Boolean check."""
        condition = bool(condition)
        if condition:
            self.passed += 1
        else:
            self.failed += 1
        line = "%s  %s" % ("PASS" if condition else "FAIL", name)
        if detail:
            safe = str(detail).encode("ascii", "backslashreplace").decode("ascii")
            line += "  [%s]" % safe
        self.lines.append(line)
        print(line)


def digest(path):
    """Return one file's SHA-256 digest."""
    with io.open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def span(raw, start, end):
    """Return bytes from one unique UTF-8 heading through the next."""
    start_b = ("\n" + start).encode("utf-8")
    end_b = ("\n" + end).encode("utf-8")
    if raw.count(start_b) != 1 or raw.count(end_b) != 1:
        raise ValueError("span headings are not unique: %s -> %s" % (start, end))
    return raw[raw.index(start_b) + 1:raw.index(end_b) + 1]


def load_module(path, name):
    """Load a Python file without invoking its guarded main function."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_probe(root, relative, extra, expected_exit):
    """Run one repository probe and return its process result."""
    command = [sys.executable,
               os.path.join(root, relative.replace("/", os.sep)),
               "--repo-root", root] + list(extra)
    result = subprocess.run(command, capture_output=True, text=True)
    return result, result.returncode == expected_exit


def disposition(level_loud, level_quiet, r_space, r_null,
                tolerance=2.0, ceiling=10.0, floor=1.25):
    """Apply Draft 34's ordered decision branches."""
    if level_loud > ceiling:
        return "fails-level-loud"
    if level_quiet < floor:
        return "fails-level-quiet"
    if r_space > tolerance:
        label = "resolved" if r_space > r_null else "resolution-limited"
        return "fails-homogeneity-%s" % label
    if r_null > tolerance:
        return "unmeasurable"
    return "passes"


def fixed_contiguous_indices(length):
    """Return Draft 34's unique equal contiguous partition."""
    half = length // 2
    return np.arange(0, half), np.arange(half, length)


def fixed_even_odd_indices(length):
    """Return the review's concrete even/odd interleaved partition."""
    return np.arange(0, length, 2), np.arange(1, length, 2)


def literal_rel_constants(tree):
    """Evaluate the legacy checker's top-level literal *_REL constants."""
    values = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or not target.id.endswith("_REL"):
            continue
        call = node.value
        if not (isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == "join"):
            continue
        parts = []
        for arg in call.args:
            if not isinstance(arg, ast.Constant) or not isinstance(arg.value, str):
                raise ValueError("non-literal path constant: %s" % target.id)
            parts.append(arg.value)
        values[target.id] = "/".join(parts)
    return values


def consumed_rel_names(tree):
    """Find *_REL names passed through root joins to file-reading helpers."""
    names = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id not in {"read_text", "max_rate_deviation"} or not node.args:
            continue
        join = node.args[0]
        if not (isinstance(join, ast.Call)
                and isinstance(join.func, ast.Attribute)
                and join.func.attr == "join"
                and len(join.args) >= 2):
            continue
        rel = join.args[1]
        if isinstance(rel, ast.Name) and rel.id.endswith("_REL"):
            names.add(rel.id)
    return names


def main(argv=None):
    """Run the independent terminal delta checks and write evidence."""
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--records", required=True)
    args = parser.parse_args(argv)
    root = os.path.abspath(args.repo_root)
    checks = Checks()

    checks.heading("1. Candidate authentication and frozen spans")
    observed = {}
    for relative, expected in CANDIDATE_DIGESTS.items():
        path = os.path.join(root, relative.replace("/", os.sep))
        got = digest(path)
        observed[relative] = got
        checks.check("authenticated: %s" % relative, got == expected, got[:16])
    timing_digest = digest(os.path.join(root, TIMING_REL.replace("/", os.sep)))
    checks.check("the newly pinned timing index is unchanged",
                 timing_digest ==
                 "043a4ea4b8374c26f8e6ce43c6031a0724a20461f827c67388d5be3f43beb3c7",
                 timing_digest[:16])
    raw_doc = io.open(os.path.join(root, DOC_REL.replace("/", os.sep)), "rb").read()
    for start, end, size, expected in FROZEN_SPANS:
        body = span(raw_doc, start, end)
        got = hashlib.sha256(body).hexdigest()
        checks.check("frozen span %s -> %s" % (start.strip(), end.strip()),
                     len(body) == size and got == expected,
                     "%d bytes %s" % (len(body), got[:8]))
    checks.records["candidate_digests"] = observed
    checks.records["timing_index_digest"] = timing_digest

    checks.heading("2. Owner fast-evidence replay")
    owner, owner_ok = run_probe(root, OWNER_SPEC_REL, [], 0)
    legacy, legacy_ok = run_probe(root, LEGACY_SPEC_REL, [], 1)
    with tempfile.TemporaryDirectory(prefix="rc008_codex_round3_") as scratch:
        owner_round3, round3_ok = run_probe(
            root, OWNER_ROUND3_REL,
            ["--out", os.path.join(scratch, "round3.txt"),
             "--records", os.path.join(scratch, "round3.json")], 0)
    checks.check("owner RC-008 checker exits green", owner_ok)
    checks.check("owner checker reports 241 / 0",
                 "241 checks, 0 failed" in owner.stdout)
    checks.check("legacy checker exits at its expected red state", legacy_ok)
    checks.check("legacy checker reports 288 / 16",
                 "288 checks, 16 failed" in legacy.stdout)
    checks.check("owner Round-3 probe exits green", round3_ok)
    checks.check("owner Round-3 probe reports 32 / 0",
                 "32 checks, 0 failed" in owner_round3.stdout)

    checks.heading("3. The split's exact reach")
    categories = [
        (12.0, 2.0),  # loud level fails before either split value is read
        (8.0, 1.0),   # quiet level fails before either split value is read
        (8.0, 2.0),   # level is in band
    ]
    null_pairs = [(1.0, 4.0), (4.0, 1.0)]
    illegal = []
    moved = []
    for loud, quiet in categories:
        for r_space in (1.5, 4.5):
            for left, right in null_pairs:
                first = disposition(loud, quiet, r_space, left)
                second = disposition(loud, quiet, r_space, right)
                pair = (loud, quiet, r_space, left, right, first, second)
                if first != second:
                    moved.append(pair)
                failure_first = first.startswith("fails")
                failure_second = second.startswith("fails")
                if failure_first != failure_second:
                    illegal.append(pair)
    checks.check("the split cannot move a failure across the failure boundary",
                 not illegal, "%d illegal transitions" % len(illegal))
    checks.check("inside M it can move pass to unmeasurable",
                 disposition(8.0, 2.0, 1.5, 1.0) == "passes"
                 and disposition(8.0, 2.0, 1.5, 4.0) == "unmeasurable")
    checks.check("outside M it changes only the homogeneity label",
                 disposition(8.0, 2.0, 4.5, 1.0).startswith("fails-homogeneity")
                 and disposition(8.0, 2.0, 4.5, 4.0).startswith(
                     "fails-homogeneity"))
    checks.records["reach"] = {"illegal": len(illegal),
                               "changed_cases_in_reduced_grid": len(moved)}

    checks.heading("4. The repaired legacy-input authentication")
    owner_module = load_module(
        os.path.join(root, OWNER_SPEC_REL.replace("/", os.sep)),
        "rc008_owner_spec_round3")
    legacy_source = io.open(
        os.path.join(root, LEGACY_SPEC_REL.replace("/", os.sep)),
        encoding="utf-8").read()
    legacy_tree = ast.parse(legacy_source)
    constants = literal_rel_constants(legacy_tree)
    consumed_names = consumed_rel_names(legacy_tree)
    consumed_paths = {constants[name] for name in consumed_names}
    derived_paths = set(owner_module.baseline_inputs(legacy_source))
    authenticated = {path for path, _ in owner_module.RC007_AUTHENTICATED}
    expected_authenticated = (consumed_paths - {DOC_REL}) | {LEGACY_SPEC_REL}
    checks.check("six literal legacy inputs are consumed",
                 len(consumed_paths) == 6, sorted(consumed_paths))
    checks.check("the independent AST walk finds the timing index",
                 TIMING_REL in consumed_paths)
    checks.check("the wrapper derives exactly those six input paths",
                 derived_paths == consumed_paths,
                 sorted(derived_paths ^ consumed_paths))
    checks.check("the authenticated set covers every record plus the checker",
                 authenticated == expected_authenticated,
                 sorted(authenticated ^ expected_authenticated))
    checks.records["legacy_inputs"] = sorted(consumed_paths)

    checks.heading("5. The sole surviving split ground")
    length = 13020
    contig_a, contig_b = fixed_contiguous_indices(length)
    even_a, odd_b = fixed_even_odd_indices(length)
    complete = np.arange(length)
    checks.check("the contiguous rule is a fixed equal partition",
                 len(contig_a) == len(contig_b) == 6510
                 and np.array_equal(np.sort(np.concatenate([contig_a, contig_b])),
                                    complete))
    checks.check("the concrete even/odd rule is also a fixed equal partition",
                 len(even_a) == len(odd_b) == 6510
                 and np.array_equal(np.sort(np.concatenate([even_a, odd_b])),
                                    complete))
    checks.check("the fixed even/odd rule takes no period parameter",
                 fixed_even_odd_indices.__code__.co_argcount == 1,
                 "arguments: length only")

    ratios_contiguous = np.ones(72)
    ratios_even_odd = np.asarray([2.0] * 8 + [1.0] * 56 + [0.5] * 8)
    def nearest_spread(values):
        """Return nearest-rank p90 / p10 for one channel vector."""
        ordered = np.sort(np.asarray(values, dtype=float))
        p10 = ordered[int(np.ceil(0.10 * len(ordered))) - 1]
        p90 = ordered[int(np.ceil(0.90 * len(ordered))) - 1]
        return float(p90 / p10)

    r_contiguous = nearest_spread(ratios_contiguous)
    r_even_odd = nearest_spread(ratios_even_odd)
    checks.check("the fixed rules reproduce the owner's 1 versus 4 values",
                 r_contiguous == 1.0 and r_even_odd == 4.0,
                 "%.1f / %.1f" % (r_contiguous, r_even_odd))
    checks.check("the fixed even/odd rule changes the decision without tuning",
                 disposition(8.0, 2.0, 1.5, r_contiguous) == "passes"
                 and disposition(8.0, 2.0, 1.5, r_even_odd) == "unmeasurable")

    text = raw_doc.decode("utf-8")
    section_195 = text[text.index("### 19.5 "):text.index("### 19.6 ")]
    checks.check("Draft 34 calls a free period the one surviving ground",
                 "An interleaved split carries a free parameter, the period"
                 in section_195
                 and "That is why contiguous halves are kept" in section_195)
    checks.check("the parity construction varies the data, not the fixed split",
                 "scale alternates between even and odd samples" in section_195
                 and "even/odd interleaving separates the parities" in section_195)
    checks.records["split_ground"] = {
        "contiguous_rule_arguments": fixed_contiguous_indices.__code__.co_argcount,
        "even_odd_rule_arguments": fixed_even_odd_indices.__code__.co_argcount,
        "r_null_contiguous": r_contiguous,
        "r_null_even_odd": r_even_odd,
        "contiguous_decision": disposition(8.0, 2.0, 1.5, r_contiguous),
        "even_odd_decision": disposition(8.0, 2.0, 1.5, r_even_odd),
        "finding": (
            "The sole rationale conflates a fixed even/odd partition with a "
            "tunable interleaving family; the exhibited construction changes "
            "the data periodicity, not a split-rule period."),
    }

    checks.heading("Summary")
    total = checks.passed + checks.failed
    summary = "%d checks, %d failed" % (total, checks.failed)
    checks.lines.append(summary)
    print(summary)
    checks.records["checks_total"] = total
    checks.records["checks_failed"] = checks.failed

    out = args.out if os.path.isabs(args.out) else os.path.join(root, args.out)
    records = (args.records if os.path.isabs(args.records)
               else os.path.join(root, args.records))
    with io.open(out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(checks.lines) + "\n")
    with io.open(records, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(checks.records, indent=2, sort_keys=True) + "\n")
    return 1 if checks.failed else 0


if __name__ == "__main__":
    sys.exit(main())
