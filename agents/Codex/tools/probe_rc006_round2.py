"""Independently verify the RC-006 Round-2 reporting-only response.

The probe is offline.  It authenticates the exact nine-file candidate, checks
that Claude Session 42 moved no packet file, derives every repaired resource
number from the committed JSON record, checks the narrowed working-set claim,
and proves the result and the pre-existing section bodies did not move.

Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe agents/Codex/tools/probe_rc006_round2.py --repo-root .
"""

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys


PRIOR_REVIEW = "3417bbf"
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
        "157905c90bfd170cc79f82c045a08e60c7da63c8ed5d5740b431ca24583a16d3",
    "agents/Claude/tools/probe_rc006_repairs.py":
        "512e31fcb1f6eea5832cc678c792cf4f0d224b0c29ba7a8e1fadc04598afc2fc",
    "agents/Claude/tools/probe_rc006_repairs_2026-08-17.txt":
        "745da38a00b07ec3220196d82b43753e13d4c0ac16edcd60b08f2ca1691ba125",
}


class Checks:
    """Accumulate exact checks and report the complete failure ledger."""

    def __init__(self):
        self.passed = 0
        self.failures = []

    def equal(self, label, actual, expected):
        """Record whether actual equals expected exactly."""
        if actual == expected:
            self.passed += 1
        else:
            self.failures.append(
                "%s: expected %r, measured %r" % (label, expected, actual))

    def true(self, label, condition):
        """Record whether a boolean condition holds."""
        self.equal(label, bool(condition), True)

    def close(self):
        """Print the total and fail after displaying every mismatch."""
        if self.failures:
            for failure in self.failures:
                print("[fail] " + failure)
            raise SystemExit("%d failed; %d passed"
                             % (len(self.failures), self.passed))
        print("[ok] %d exact checks passed" % self.passed)


def sha256(path):
    """Return the SHA-256 digest of one file's physical bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *arguments):
    """Return stdout from one read-only Git command."""
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, check=True)
    return result.stdout


def main(argv=None):
    """Run the complete offline Round-2 verification."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="repository root containing the packet")
    args = parser.parse_args(argv)
    root = pathlib.Path(args.repo_root).resolve()
    checks = Checks()

    for relative, expected in EXPECTED_HASHES.items():
        checks.equal("digest " + relative, sha256(root / relative), expected)

    selection_relative = "agents/Claude/Tier A Host and Injection Zone Selection.md"
    selection_bytes = (root / selection_relative).read_bytes()
    selection = selection_bytes.decode("utf-8")
    record = json.loads((
        root / "Reproducibility Packet/results/host_drift_CSHL047_Probe01.json"
    ).read_text(encoding="utf-8"))
    plan = record["plan"]

    changed_candidate = git(
        root, "diff", "--name-only", "%s..HEAD" % PRIOR_REVIEW, "--",
        selection_relative, "Reproducibility Packet",
        "agents/Claude/tools/mutation_test_runbook_checker.py",
    ).decode("utf-8").splitlines()
    checks.equal("only the selection document moved in the carried candidate",
                 changed_candidate, [selection_relative])

    start_1 = selection_bytes.index(b"## 1. ")
    start_17 = selection_bytes.index(b"## 17. ")
    start_18 = selection_bytes.index(b"## 18. ")
    span_1_16 = selection_bytes[start_1:start_17]
    span_17 = selection_bytes[start_17:start_18]
    checks.equal("sections 1-16 bytes", len(span_1_16), 144664)
    checks.equal("sections 1-16 digest", hashlib.sha256(span_1_16).hexdigest(),
                 "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59")
    checks.equal("section 17 bytes", len(span_17), 21864)
    checks.equal("section 17 digest", hashlib.sha256(span_17).hexdigest(),
                 "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a")

    terms = ("cache_bound_bytes", "resident_bytes", "structures_bytes",
             "library_cache_bytes")
    checks.equal("four plan terms sum to peak",
                 sum(plan[name] for name in terms), plan["peak_resident_bytes"])
    checks.equal("peak resident bytes", plan["peak_resident_bytes"], 131985507)
    checks.equal("cache-bound term", plan["cache_bound_bytes"], 59040736)
    checks.equal("resident term", plan["resident_bytes"], 55120439)
    checks.equal("structures term", plan["structures_bytes"], 1047116)
    checks.equal("library-cache term", plan["library_cache_bytes"], 16777216)

    arrays = plan["n_spikes"] * 16
    masks = plan["mask_bytes"]
    largest_slice = plan["resident_bytes"] - arrays - masks
    checks.equal("converted arrays", arrays, 50564976)
    checks.equal("retained masks", masks, 3160311)
    checks.equal("largest stored-width slice", largest_slice, 1395152)
    checks.equal("largest slice spike count", largest_slice // 16, 87197)
    checks.equal("largest slice divides exactly", largest_slice % 16, 0)

    free_bytes = 15126 * 1024 ** 2
    admission = int(0.75 * free_bytes)
    remaining = free_bytes - plan["peak_resident_bytes"]
    checks.equal("free bytes", free_bytes, 15860760576)
    checks.equal("75 percent of free", admission, 11895570432)
    checks.equal("remaining bytes", remaining, 15728775069)
    checks.equal("75-percent factor",
                 round(admission / plan["peak_resident_bytes"], 3), 90.128)
    checks.equal("floor factor", round(remaining / (4 * 1024 ** 3), 3), 3.662)

    section18 = selection[selection.index("## 18. "):]
    required_phrases = (
        "**consistent with that projection**",
        "remains a projection derived from the code",
        "has not built one",
        "**Follow-up 1 is not discharged and is not converted into a measurement**",
        "**164 lines, 0 non-ASCII**",
    )
    for phrase in required_phrases:
        checks.true("required repaired phrase: " + phrase[:46], phrase in section18)
    forbidden_phrases = (
        "clears the 75%-of-free rule and the 4 GiB floor by three orders",
        "The projection is now a measurement",
        "follow-up 1 now carrying a measurement instead of a projection",
        "`--help` **165 lines, 0 non-ASCII**",
    )
    for phrase in forbidden_phrases:
        checks.true("retired defective phrase: " + phrase[:46],
                    phrase not in section18)

    checks.equal("Delta_10min unchanged",
                 record["observed"]["delta_window"], 1.8206253051757812)
    checks.equal("Q95_null unchanged", record["null"]["q95"],
                 0.5257034301757812)
    checks.equal("verdict unchanged", record["verdict"]["passed"], True)
    checks.equal("disposition unchanged",
                 record["disposition"]["disposition"], "passes")
    checks.equal("advances unchanged", record["disposition"]["advances"], True)
    checks.equal("conflict unchanged", record["disposition"]["conflict"], False)

    command = root / "Reproducibility Packet/scripts/measure_host_drift.py"
    help_result = subprocess.run(
        [sys.executable, str(command), "--help"],
        cwd=root / "Reproducibility Packet", capture_output=True, check=True)
    checks.equal("rendered help lines", len(help_result.stdout.splitlines()), 164)
    checks.equal("rendered help non-ASCII bytes",
                 sum(byte > 127 for byte in help_result.stdout), 0)

    # Claude's prose probe is appropriately a claim checker: the response moves
    # no behaviour, and the reviewer independently authenticates the numbers and
    # the response boundary above.  A document mutation harness would add no new
    # executable property for this card.
    checks.equal("owner prose probe source compiles",
                 subprocess.run(
                     [sys.executable, "-m", "py_compile",
                      str(root / "agents/Claude/tools/probe_rc006_repairs.py")],
                     cwd=root).returncode,
                 0)

    checks.close()


if __name__ == "__main__":
    main()
