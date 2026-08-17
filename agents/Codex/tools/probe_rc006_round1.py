"""Independently audit RC-006's committed measurement and reporting boundaries.

This probe is deliberately offline.  It authenticates the seven-file candidate,
derives the numerical summaries in section 18 from the committed JSON record,
proves the command's executable syntax tree did not move, and makes the resource
paragraph's arithmetic and the rendered help length explicit.

Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe agents/Codex/tools/probe_rc006_round1.py --repo-root .
"""

import argparse
import ast
import hashlib
import json
import pathlib
import subprocess
import sys


EXPECTED_HASHES = {
    "Reproducibility Packet/results/host_drift_CSHL047_Probe01.txt":
        "a2d325088b384f8010a1e398fd58ec759981269e83cb166b7082c3f76ad0cbef",
    "Reproducibility Packet/results/host_drift_CSHL047_Probe01.json":
        "2e125d419eb8ad31ad7824f47dd324b8ed0d54d8230095eb29618436b3c87bd5",
    "Reproducibility Packet/scripts/measure_host_drift.py":
        "200709824fb3a5694b12243eb65647d038d1d251df9abfe49a3e90ca3b8bad47",
    "Reproducibility Packet/scripts/check_runbook_consistency.py":
        "35cea57d67be5e299c036f39312ad821fe193fc3d2cc4d7e1fe6480e04b4ccdb",
    "Reproducibility Packet/README.md":
        "806aefaf9859cc0f391101f205b6e055f9278d5d95ef4d759711ded8762cfaf3",
    "agents/Claude/tools/mutation_test_runbook_checker.py":
        "d443ded05bb38662e39dcc9ec8f99ac2b703ab5bb95270bda33ce9108cd83a79",
    "agents/Claude/Tier A Host and Injection Zone Selection.md":
        "646def951178f76ca2397c34dc46a2b2f0f96c3d77d6658825335aede71b82c3",
}

RC005_APPROVED_REVISION = "2a610dc9c15538089acbfa6273a19d0628627c53"


class Checks:
    """Collect exact review checks and fail only after reporting every mismatch."""

    def __init__(self):
        """Create an empty check ledger.

        Inputs: none.
        Outputs: a ledger with zero passed and zero failed checks.
        Purpose: retain all failures so one run reports the complete boundary.
        """
        self.passed = 0
        self.failures = []

    def equal(self, name, actual, expected):
        """Require exact equality and record the result.

        Inputs: a check name, the measured value, and the expected value.
        Outputs: none; updates the ledger in place.
        Purpose: make every review assertion named and independently visible.
        """
        if actual == expected:
            self.passed += 1
        else:
            self.failures.append(
                "%s: expected %r, measured %r" % (name, expected, actual))

    def close(self):
        """Print the ledger and exit nonzero if any check failed.

        Inputs: none beyond the accumulated ledger.
        Outputs: a summary on stdout or a SystemExit carrying every failure.
        Purpose: give the reviewer one unambiguous terminal result.
        """
        if self.failures:
            for failure in self.failures:
                print("[fail] " + failure)
            raise SystemExit("%d check(s) failed; %d passed"
                             % (len(self.failures), self.passed))
        print("[ok] %d exact checks passed" % self.passed)


def parse_args(argv=None):
    """Parse the project root and prior revision.

    Inputs: an optional argument list.
    Outputs: argparse's populated namespace.
    Purpose: keep paths and the comparison revision outside source constants.
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="project root containing the packet and agent workspaces")
    parser.add_argument(
        "--prior-revision", default=RC005_APPROVED_REVISION,
        help="revision holding RC-005's approved CLI "
             "(default: %(default)s)")
    return parser.parse_args(argv)


def sha256(path):
    """Hash one file without normalising its bytes.

    Inputs: a pathlib path.
    Outputs: the lowercase hexadecimal SHA-256 digest.
    Purpose: authenticate the exact review candidate.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_docstrings(tree):
    """Remove all Python docstring statements from an AST.

    Inputs: a parsed Python syntax tree.
    Outputs: the same tree with module, class, and function docstrings removed.
    Purpose: distinguish a printed-surface edit from executable code movement.
    """
    for node in ast.walk(tree):
        if not isinstance(
                node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if not node.body:
            continue
        first = node.body[0]
        if (isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)):
            node.body = node.body[1:]
    return tree


def percentile_linear(values, percentile):
    """Compute the standard linear percentile used by NumPy's default method.

    Inputs: a non-empty numeric sequence and a percentile from zero to 100.
    Outputs: the interpolated percentile as a float.
    Purpose: reproduce section 18's 90th-percentile audit without importing NumPy.
    """
    ordered = sorted(float(value) for value in values)
    position = (len(ordered) - 1) * float(percentile) / 100.0
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def median(values):
    """Compute the ordinary sample median.

    Inputs: a non-empty numeric sequence.
    Outputs: the middle value or mean of the two middle values.
    Purpose: independently derive both per-unit medians reported in section 18.
    """
    ordered = sorted(float(value) for value in values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2.0


def prior_file(root, revision, relative):
    """Read one file exactly as stored at a Git revision.

    Inputs: repository root, revision, and slash-separated relative path.
    Outputs: the file's raw bytes.
    Purpose: compare the approved prior state without rewriting the worktree.
    """
    result = subprocess.run(
        ["git", "show", "%s:%s" % (revision, relative)], cwd=root,
        capture_output=True, check=True)
    return result.stdout


def main(argv=None):
    """Run the complete offline RC-006 Round-1 probe.

    Inputs: optional CLI arguments accepted by :func:`parse_args`.
    Outputs: exact-check totals plus measured resource/help diagnostics.
    Purpose: preserve the review evidence independently of the owner's harnesses.
    """
    args = parse_args(argv)
    root = pathlib.Path(args.repo_root).resolve()
    checks = Checks()

    for relative, expected in EXPECTED_HASHES.items():
        checks.equal("digest " + relative, sha256(root / relative), expected)

    selection_path = root / "agents/Claude/Tier A Host and Injection Zone Selection.md"
    selection = selection_path.read_bytes()
    section_start = selection.index(b"## 1. ")
    section_end = selection.index(b"## 17. ")
    span = selection[section_start:section_end]
    checks.equal("section 1-16 bytes", len(span), 144664)
    checks.equal("section 1-16 digest", hashlib.sha256(span).hexdigest(),
                 "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59")
    prior_selection = prior_file(
        root, args.prior_revision,
        "agents/Claude/Tier A Host and Injection Zone Selection.md")
    prior_span = prior_selection[
        prior_selection.index(b"## 1. "):prior_selection.index(b"## 17. ")]
    checks.equal("section 1-16 prior equality", span, prior_span)

    cli_relative = "Reproducibility Packet/scripts/measure_host_drift.py"
    current_cli = (root / cli_relative).read_text(encoding="utf-8")
    prior_cli = prior_file(root, args.prior_revision, cli_relative).decode("utf-8")
    current_tree = strip_docstrings(ast.parse(current_cli))
    prior_tree = strip_docstrings(ast.parse(prior_cli))
    checks.equal("CLI docstring-stripped AST",
                 ast.dump(current_tree, include_attributes=False),
                 ast.dump(prior_tree, include_attributes=False))

    record = json.loads((
        root / "Reproducibility Packet/results/host_drift_CSHL047_Probe01.json"
    ).read_text(encoding="utf-8"))
    observed = record["observed"]
    missing = record["missing_depth"]
    audit = record["audit"]
    whole = [item["delta_full"] for item in audit]
    aligned = [item["delta_band_window"] for item in audit]

    expected_values = {
        "Delta_10min": (observed["delta_window"], 1.8206253051757812),
        "window start": (observed["window_start"], 1),
        "Delta_full": (observed["delta_full"], 2.5367050170898438),
        "Q95_null": (record["null"]["q95"], 0.5257034301757812),
        "null rank": (record["null"]["rank"], 190),
        "inside_null": (record["verdict"]["inside_null"], False),
        "analysed bins": (observed["n_bins"], 72),
        "invalid bins": (len(observed["invalid_bins"]), 0),
        "minimum units": (observed["min_units_per_bin_observed"], 130),
        "included units": (record["sets"]["included"]["n_total"], 140),
        "in-band units": (record["sets"]["in_band"]["n_total"], 174),
        "included good units": (record["sets"]["included"]["n_good"], 18),
        "loaded spikes": (record["plan"]["n_spikes"], 3160311),
        "missing depths": (missing["n_missing"], 231),
        "missing units": (missing["n_units_affected"], 11),
        "missing outside grid": (missing["outside_grid"], 4),
        "support invariance": (missing["support"]["invariant"], True),
        "completion disposition": (missing["stability"]["disposition"], "passes"),
        "reconciled disposition": (record["disposition"]["disposition"], "passes"),
        "advances": (record["disposition"]["advances"], True),
        "conflict": (record["disposition"]["conflict"], False),
        "audit count": (len(audit), 140),
        "whole minimum": (min(whole), 1.259185791015625),
        "whole maximum": (max(whole), 71.62893676757812),
        "whole median": (median(whole), 9.155426025390625),
        "whole p90": (percentile_linear(whole, 90), 27.145504760742178),
        "whole above 20": (sum(value > 20 for value in whole), 21),
        "whole above 40": (sum(value > 40 for value in whole), 11),
        "aligned minimum": (min(aligned), 0.6427154541015625),
        "aligned maximum": (max(aligned), 43.55938720703125),
        "aligned median": (median(aligned), 5.8812408447265625),
        "aligned above 20": (sum(value > 20 for value in aligned), 14),
        "aligned above 40": (sum(value > 40 for value in aligned), 4),
        "archive bytes": (record["io"]["bytes"], 88599226),
        "archive requests": (record["io"]["requests"], 93),
    }
    for name, (actual, expected) in expected_values.items():
        checks.equal(name, actual, expected)

    plan = record["plan"]
    complete_peak = (plan["cache_bound_bytes"] + plan["resident_bytes"]
                     + plan["structures_bytes"] + plan["library_cache_bytes"])
    checks.equal("complete peak arithmetic", complete_peak, plan["peak_resident_bytes"])
    listed = (plan["resident_bytes"] + plan["structures_bytes"]
              + plan["library_cache_bytes"])
    omitted = plan["peak_resident_bytes"] - listed
    checks.equal("unlisted term equals range-reader block cache",
                 omitted, plan["cache_bound_bytes"])

    free_mib = 15126.0
    free_bytes = free_mib * 1024.0 ** 2
    print("[diagnostic] section 18.2 listed components: %d of %d bytes; "
          "unlisted block cache: %d bytes"
          % (listed, plan["peak_resident_bytes"], omitted))
    print("[diagnostic] plan headroom: %.3fx free/plan, %.3fx (75%% free)/plan, "
          "%.3fx remaining/4-GiB-floor"
          % (free_bytes / plan["peak_resident_bytes"],
             0.75 * free_bytes / plan["peak_resident_bytes"],
             (free_bytes - plan["peak_resident_bytes"]) / (4.0 * 1024.0 ** 3)))

    help_result = subprocess.run(
        [sys.executable, str(root / cli_relative), "--help"],
        capture_output=True, check=True)
    checks.equal("help non-ASCII bytes", sum(byte > 127 for byte in help_result.stdout), 0)
    help_lines = len(help_result.stdout.splitlines())
    checks.equal("rendered help lines", help_lines, 164)
    print("[diagnostic] rendered --help lines: %d" % help_lines)

    # The gate and reconciliation are computed before the audit list is assembled;
    # the audit is then copied into the record and report only.
    checks.equal("audit assembled after reconciliation",
                 current_cli.index("    audit = []") >
                 current_cli.index("    reconciled = reconcile_verdict("), True)
    checks.equal("audit absent from reconciliation call",
                 "reconcile_verdict(verdict, stability, audit)" in current_cli, False)

    checks.close()


if __name__ == "__main__":
    main()
