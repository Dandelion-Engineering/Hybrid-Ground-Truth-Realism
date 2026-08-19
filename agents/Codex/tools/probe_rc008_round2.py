"""Independent RC-008 Round-2 delta probe for Draft 33.

The probe authenticates the nine-file handoff and the three frozen document
spans, replays the owner's two fast specification probes, and tests two
response-created claims directly:

* whether the contiguous/interleaved choice can change the ordered decision;
* whether the repaired wrapper authenticates every file its legacy checker
  reads before accepting the legacy output.

All fixtures are local and deterministic. No archive or network resource is
read.

Example:
    ./venv/Scripts/python.exe agents/Codex/tools/probe_rc008_round2.py \
        --repo-root . --out agents/Codex/tools/rc008_round2_2026-08-19.txt \
        --records agents/Codex/tools/rc008_round2_2026-08-19.json
"""

import argparse
import hashlib
import importlib.util
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np


DOC_REL = "agents/Claude/Tier A Host and Injection Zone Selection.md"
OWNER_SPEC_REL = "agents/Claude/tools/probe_rc008_spec.py"
LEGACY_SPEC_REL = "agents/Claude/tools/probe_rc007_spec.py"
OWNER_ROUND2_REL = "agents/Claude/tools/probe_rc008_round2.py"
TIMING_REL = "Reproducibility Packet/results/host_timing_index.jsonl"

CANDIDATE_DIGESTS = {
    DOC_REL: "16ee8f801d0a44b99de70c12da7f7d80b32a73325e720ab0236ad2180679f56e",
    OWNER_SPEC_REL: "7574ac52538b4c05811c8d785314326870c5ae73a2bc7b87427ef673ad09251b",
    "agents/Claude/tools/rc008_spec_2026-08-18_draft33.txt":
        "8f40c8cc47fd138af1ba8c2d5014451a42961838172f7fb3138d29f11f5e70ac",
    "agents/Claude/tools/rc008_spec_2026-08-18_draft33.json":
        "20aea650ca8b13262e28958b3fe4adffdf85f6cb5c7a72d425858067782976e8",
    "agents/Claude/tools/mutate_rc008_spec.py":
        "299be141d43d164b31370e099ddceb9b863c34acb9e42914496ca6bde0aadac4",
    "agents/Claude/tools/mutate_rc008_spec_2026-08-18_draft33.txt":
        "a6c0d94324697cd5c80c49a79a58f100893c4d3d5d3952216d7f627982fa2548",
    OWNER_ROUND2_REL:
        "aa6a4371e905808d86b0c2fcb34cb934a29e5331cd5204511a9c5e488a262490",
    "agents/Claude/tools/rc008_round2_2026-08-18.txt":
        "5f692ba5e8f5ad3df6289349bb89fccb3c6fe956810861586555c7bacb014dbc",
    "agents/Claude/tools/rc008_round2_2026-08-18.json":
        "0d185bd3bb2f2e490b18ef9c8349e517e287df9a836732c8289f408741b364c5",
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
    """Collect human-readable checks and a structured evidence record."""

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
    """Return the SHA-256 digest of one file."""
    with io.open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def span(raw, start, end):
    """Return bytes from one unique UTF-8 heading through the next."""
    start_b = ("\n" + start).encode("utf-8")
    end_b = ("\n" + end).encode("utf-8")
    if raw.count(start_b) != 1 or raw.count(end_b) != 1:
        raise ValueError("span headings are not unique: %s -> %s" % (start, end))
    return raw[raw.index(start_b) + 1:raw.index(end_b) + 1]


def disposition(r_space, r_null, tolerance=2.0):
    """Apply the relevant ordered §19.6 branches at an in-band level."""
    if r_space > tolerance:
        return "fails"
    if r_null > tolerance:
        return "unmeasurable"
    return "passes"


def load_module(path):
    """Load a Python file without invoking its guarded main function."""
    spec = importlib.util.spec_from_file_location("rc008_owner_spec", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_file(repo_root, stage_root, relative):
    """Copy one repository-relative file into the same staged location."""
    source = os.path.join(repo_root, relative.replace("/", os.sep))
    target = os.path.join(stage_root, relative.replace("/", os.sep))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy2(source, target)


def counterfeit_timing_index():
    """Return a different timing record with the two consumed aggregates fixed."""
    nominal = 30000.0
    rates = [nominal] * 20 + [nominal * (1.0 + 9.946e-06)]
    record = {"counterfeit": True,
              "series": [{"name": "synthetic-%02d" % i, "rate_hz": rate}
                         for i, rate in enumerate(rates)]}
    return (json.dumps(record, sort_keys=True) + "\n").encode("utf-8")


def run_probe(repo_root, relative, expected_exit):
    """Run one repository probe and return its process result."""
    result = subprocess.run(
        [sys.executable, os.path.join(repo_root, relative.replace("/", os.sep)),
         "--repo-root", repo_root],
        capture_output=True, text=True)
    return result, result.returncode == expected_exit


def main(argv=None):
    """Run the independent delta checks and write text/JSON evidence."""
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
    raw_doc = io.open(os.path.join(root, DOC_REL.replace("/", os.sep)), "rb").read()
    for start, end, size, expected in FROZEN_SPANS:
        body = span(raw_doc, start, end)
        got = hashlib.sha256(body).hexdigest()
        checks.check("frozen span %s -> %s" % (start.strip(), end.strip()),
                     len(body) == size and got == expected,
                     "%d bytes %s" % (len(body), got[:8]))
    checks.records["candidate_digests"] = observed

    checks.heading("2. Owner fast-probe replay")
    owner, owner_ok = run_probe(root, OWNER_SPEC_REL, 0)
    checks.check("owner RC-008 checker exits zero", owner_ok,
                 owner.stdout.splitlines()[-1] if owner.stdout.splitlines() else "")
    legacy, legacy_ok = run_probe(root, LEGACY_SPEC_REL, 1)
    checks.check("legacy checker has the expected red exit", legacy_ok,
                 legacy.stdout.splitlines()[-1] if legacy.stdout.splitlines() else "")
    checks.check("owner checker reports 168 / 0",
                 "168 checks, 0 failed" in owner.stdout)
    checks.check("legacy checker reports 288 / 16",
                 "288 checks, 16 failed" in legacy.stdout)

    checks.heading("3. F3-R1 response: the decision can cash the split difference")
    r_space = 1.5
    contiguous = 1.0
    interleaved = 4.0
    contiguous_decision = disposition(r_space, contiguous)
    interleaved_decision = disposition(r_space, interleaved)
    checks.check("the owner's contiguous fixture permits a pass",
                 contiguous_decision == "passes", contiguous_decision)
    checks.check("the owner's interleaved fixture withholds that pass",
                 interleaved_decision == "unmeasurable", interleaved_decision)
    checks.check("the split improvement has a decision destination",
                 contiguous_decision != interleaved_decision,
                 "%s -> %s" % (contiguous_decision, interleaved_decision))

    half = 6510
    frequency = 30000.0 * 87.0 / half
    phases = np.linspace(0.01, 1.19, 19)
    estimates_a = []
    estimates_b = []
    samples = np.arange(2 * half)
    for phase in phases:
        signal = np.sin(2.0 * math.pi * 87.0 * samples / half + phase)
        a = signal[:half]
        b = signal[half:]
        estimates_a.append(np.median(np.abs(a - np.median(a))))
        estimates_b.append(np.median(np.abs(b - np.median(b))))
    estimates_a = np.asarray(estimates_a)
    estimates_b = np.asarray(estimates_b)
    checks.check("an above-300-Hz process can repeat exactly across the halves",
                 frequency > 300.0 and np.max(np.abs(estimates_a - estimates_b)) < 1e-12,
                 "f=%.6f Hz max_delta=%.3e" %
                 (frequency, np.max(np.abs(estimates_a - estimates_b))))
    checks.check("the repeated half-estimates are not independent",
                 np.std(estimates_a) > 0.0
                 and np.corrcoef(estimates_a, estimates_b)[0, 1] > 0.999999,
                 "corr=%.12f" % np.corrcoef(estimates_a, estimates_b)[0, 1])
    checks.records["split"] = {
        "r_space": r_space,
        "r_null_contiguous": contiguous,
        "r_null_interleaved": interleaved,
        "contiguous_decision": contiguous_decision,
        "interleaved_decision": interleaved_decision,
        "periodic_frequency_hz": frequency,
        "half_estimate_correlation": float(np.corrcoef(estimates_a, estimates_b)[0, 1]),
    }

    checks.heading("4. F4-R1 response: one consumed record remains unauthenticated")
    owner_module = load_module(os.path.join(root, OWNER_SPEC_REL.replace("/", os.sep)))
    legacy_module = load_module(os.path.join(root, LEGACY_SPEC_REL.replace("/", os.sep)))
    authenticated = {relative for relative, _ in owner_module.RC007_AUTHENTICATED}
    checks.check("the legacy checker consumes the timing index",
                 legacy_module.TIMING_REL.replace(os.sep, "/") == TIMING_REL)
    checks.check("the wrapper omits the timing index from its digest set",
                 TIMING_REL not in authenticated,
                 "%d authenticated paths" % len(authenticated))

    stage_files = [DOC_REL, OWNER_SPEC_REL, LEGACY_SPEC_REL,
                   "agents/Claude/tools/raw_ap_layout_CSHL047_Probe01_2026-08-18.json",
                   "agents/Claude/tools/raw_ap_layout_CSHL047_Probe01_2026-08-18.txt",
                   "agents/Claude/tools/filter_chain_2026-08-18.json",
                   "agents/Claude/tools/rc007_round3_2026-08-18.json",
                   "agents/Claude/tools/rc008_round2_2026-08-18.json"]
    with tempfile.TemporaryDirectory(prefix="rc008_codex_") as stage:
        for relative in stage_files:
            copy_file(root, stage, relative)
        fake_path = os.path.join(stage, TIMING_REL.replace("/", os.sep))
        os.makedirs(os.path.dirname(fake_path), exist_ok=True)
        fake = counterfeit_timing_index()
        io.open(fake_path, "wb").write(fake)
        original_digest = digest(os.path.join(root, TIMING_REL.replace("/", os.sep)))
        fake_digest = hashlib.sha256(fake).hexdigest()
        result, staged_ok = run_probe(stage, OWNER_SPEC_REL, 0)
        checks.check("the counterfeit timing record differs byte-for-byte",
                     fake_digest != original_digest,
                     "%s != %s" % (fake_digest[:8], original_digest[:8]))
        checks.check("the wrapper still goes green on that counterfeit record",
                     staged_ok and "168 checks, 0 failed" in result.stdout,
                     "exit %d" % result.returncode)
    checks.records["authentication_gap"] = {
        "omitted_path": TIMING_REL,
        "original_digest": original_digest,
        "counterfeit_digest": fake_digest,
        "wrapper_exit": result.returncode,
        "wrapper_summary_green": "168 checks, 0 failed" in result.stdout,
    }

    checks.heading("5. Delta wording surfaces")
    text = raw_doc.decode("utf-8")
    checks.check("the four-statistic boundary still says all three",
                 "anything shorter can fall entirely between windows and is invisible to all three"
                 in text)
    checks.check("the new floor coexists with the stale no-lean sentence",
                 "which is why §19.6 does not lean on the floor" in text
                 and "sigma_quietest_sampled < 1.25 µV" in text)

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
