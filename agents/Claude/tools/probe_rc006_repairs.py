"""Check every claim the RC-006 Round-1 repairs put into section 18.

RC-006 Round 1 returned four findings against section 18's reporting surfaces:
an incomplete decomposition of the read plan (F1), a false headroom scale claim
(F2), two working-set samples presented as an isolated byte-exact allocation
measurement (F3), and a wrong rendered-help line count (F4).  The repairs are
prose, so a reversion harness of the ``verify_rc00*`` shape does not apply --
there is no behaviour to break.  What can be checked is that every number the
repaired prose states is the number the committed record actually holds, that
the arithmetic it now shows actually closes, and that the defective sentences
are gone rather than merely reworded.

This probe is read-only.  It reads the committed drift record and report, the
selection document, and the drift command's rendered help.  It reads no archive
and runs no measurement.

Exit status is 0 only when every check passes; any failure is printed with the
expected and actual values and the process exits 1.

Example:

    python agents/Claude/tools/probe_rc006_repairs.py --repo-root .
"""

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys


# The two spans of the selection document that RC-006 says must not move.  Both
# were taken from Draft 27, the state Codex authenticated at Round 1.
DRAFT27_SPANS = {
    "sections 1-16": (b"## 1. ", b"## 17. ", 144664,
                      "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59"),
    "section 17": (b"## 17. ", b"## 18. ", 21864,
                   "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a"),
}

# The free-memory reading taken immediately before the rank-1 read, and the two
# admission rules it was compared against.  The reading was recorded at
# mebibyte precision, which is the precision the derived factors carry.
FREE_MIB = 15126
MIB = 1024 * 1024
FLOOR_BYTES = 4 * 1024 ** 3
ADMIT_FRACTION = 0.75

# Sentences Draft 27 contained and Draft 28 must not.
DEFECTIVE = [
    "which clears the 75%-of-free rule and the 4 GiB floor by three orders of magnitude",
    "`--help` **165 lines, 0 non-ASCII**",
    "- **This section is unreviewed.**",
    "**The projection is now a measurement, and any later whole-command memory claim inherits it as one.**",
    "follow-up 1 now carrying a measurement instead of a projection",
]


class Checker(object):
    """Accumulates pass/fail results and prints each one as it is decided."""

    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, label, actual, expected):
        """Assert equality, printing the comparison either way.

        Args:
            label: what is being checked, printed verbatim.
            actual: the value found.
            expected: the value the repaired prose or the card states.
        """
        if actual == expected:
            self.passed += 1
            print("  ok    %-58s %s" % (label, actual))
        else:
            self.failed += 1
            print("  FAIL  %-58s got %r, expected %r" % (label, actual, expected))

    def truth(self, label, condition, detail=""):
        """Assert a boolean condition."""
        if condition:
            self.passed += 1
            print("  ok    %-58s %s" % (label, detail or "true"))
        else:
            self.failed += 1
            print("  FAIL  %-58s %s" % (label, detail or "false"))


def read_text(path):
    """Read a UTF-8 file without translating its line endings."""
    with io.open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def span_digest(body, start_marker, end_marker):
    """Return (length, sha256) of the bytes between two heading markers."""
    start = body.index(start_marker)
    end = body.index(end_marker)
    chunk = body[start:end]
    return len(chunk), hashlib.sha256(chunk).hexdigest()


def render_help(repo_root):
    """Run the drift command's --help from inside the packet and return it."""
    packet = os.path.join(repo_root, "Reproducibility Packet")
    python = os.path.join(repo_root, "venv", "Scripts", "python.exe")
    if not os.path.exists(python):
        python = sys.executable
    result = subprocess.run(
        [python, os.path.join("scripts", "measure_host_drift.py"), "--help"],
        cwd=packet, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        raise SystemExit("--help exited %d" % result.returncode)
    return result.stdout.decode("utf-8")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="path to the repository root")
    args = parser.parse_args()

    root = os.path.abspath(args.repo_root)
    doc_path = os.path.join(root, "agents", "Claude",
                            "Tier A Host and Injection Zone Selection.md")
    record_path = os.path.join(root, "Reproducibility Packet", "results",
                               "host_drift_CSHL047_Probe01.json")
    report_path = os.path.join(root, "Reproducibility Packet", "results",
                               "host_drift_CSHL047_Probe01.txt")

    for path in (doc_path, record_path, report_path):
        if not os.path.exists(path):
            raise SystemExit("missing input: %s" % path)

    doc = read_text(doc_path)
    body = doc.encode("utf-8")
    record = json.load(io.open(record_path, "r", encoding="utf-8"))
    report = read_text(report_path)
    plan = record["plan"]

    checker = Checker()

    print("F1 -- the plan decomposition names all four terms and closes")
    terms = ["cache_bound_bytes", "resident_bytes", "structures_bytes",
             "library_cache_bytes"]
    total = 0
    for term in terms:
        value = plan[term]
        total += value
        checker.truth("section 18.2 states %s" % term,
                      "{:,}".format(value) in doc, "{:,}".format(value))
    checker.check("four terms sum to peak_resident_bytes", total,
                  plan["peak_resident_bytes"])
    checker.check("peak_resident_bytes", plan["peak_resident_bytes"], 131985507)
    checker.check("cache_bound_bytes is the largest term",
                  max(plan[t] for t in terms), plan["cache_bound_bytes"])
    checker.truth("the report also names all four",
                  all("{:,}".format(plan[t]).replace(",", "") in report
                      for t in terms))
    # The resident term's own three parts, which section 18.2 now spells out.
    arrays = plan["n_spikes"] * 16
    mask = plan["mask_bytes"]
    slice_bytes = plan["resident_bytes"] - arrays - mask
    checker.check("resident: converted arrays", arrays, 50564976)
    checker.check("resident: retained masks", mask, 3160311)
    checker.check("resident: largest slice at stored width", slice_bytes, 1395152)
    checker.check("largest slice is a whole number of spikes",
                  slice_bytes % 16, 0)
    checker.check("largest unit spike count", slice_bytes // 16, 87197)
    checker.check("resident parts sum", arrays + mask + slice_bytes,
                  plan["resident_bytes"])
    checker.check("spent-before-band bytes", plan["spent_bytes"], 9073136)
    checker.check("hdf5 cache is two 8 MiB halves",
                  plan["time_layout"]["library_cache_bytes"]
                  + plan["depth_layout"]["library_cache_bytes"],
                  plan["library_cache_bytes"])

    print("")
    print("F2 -- the admission factors are the stated ones")
    free_bytes = FREE_MIB * MIB
    peak = plan["peak_resident_bytes"]
    admit = ADMIT_FRACTION * free_bytes
    remaining = free_bytes - peak
    checker.check("free bytes at the recorded reading", free_bytes, 15860760576)
    checker.check("75 percent of free", int(admit), 11895570432)
    checker.check("remaining after the plan", remaining, 15728775069)
    checker.check("75%-of-free factor", round(admit / peak, 3), 90.128)
    checker.check("4 GiB floor factor", round(remaining / FLOOR_BYTES, 3), 3.662)
    checker.truth("both rules admit", admit >= peak and remaining >= FLOOR_BYTES)
    checker.truth("the floor is the binding rule",
                  remaining / FLOOR_BYTES < admit / peak)
    checker.truth("no factor reaches three orders of magnitude",
                  max(admit / peak, remaining / FLOOR_BYTES) < 1000)
    for stated in ["**90.128**", "**3.662**", "15,860,760,576",
                   "11,895,570,432", "15,728,775,069", "4,294,967,296"]:
        checker.truth("section 18.2 states %s" % stated, stated in doc)

    print("")
    print("F3 -- the working-set observation is reported as consistent, not measured")
    checker.truth("section 17.12's projection is still called a projection",
                  "remains a projection derived from the code" in doc)
    checker.truth("the step is called consistent with the projection",
                  "**consistent with that projection**" in doc)
    checker.truth("no whole-command empirical ceiling is claimed",
                  "has not built one" in doc)
    checker.truth("follow-up 1 is stated as still open",
                  "**Follow-up 1 is not discharged and is not converted into a "
                  "measurement**" in doc)
    section18 = doc[doc.index("## 18. "):]
    checker.check("the projection's value appears once in section 18",
                  section18.count("50,561,280"), 1)

    print("")
    print("F4 -- the rendered help count")
    help_text = render_help(root)
    checker.check("rendered help lines", len(help_text.splitlines()), 164)
    checker.check("non-ASCII characters in help",
                  sum(1 for ch in help_text if ord(ch) > 127), 0)
    checker.truth("section 18.7 states 164 lines",
                  "**164 lines, 0 non-ASCII**" in doc)

    print("")
    print("The defective sentences are gone and the repairs are marked")
    for sentence in DEFECTIVE:
        checker.truth("gone: %s" % sentence[:48], sentence not in doc)
    for marker in ["RC-006-F1 is repaired", "RC-006-F2 is repaired",
                   "RC-006-F3 is repaired", "RC-006-F4 is repaired"]:
        checker.check("marked once: %s" % marker, doc.count(marker), 1)

    print("")
    print("Nothing outside section 18 and the status stack moved")
    for label, (start, end, length, digest) in sorted(DRAFT27_SPANS.items()):
        found_length, found_digest = span_digest(body, start, end)
        checker.check("%s bytes" % label, found_length, length)
        checker.check("%s sha256" % label, found_digest, digest)
    checker.check("Draft 28 status line present", doc.count("**Status:** Draft 28 "), 1)
    checker.check("Draft 27 status line retained", doc.count("**Status:** Draft 27 "), 1)

    print("")
    print("The measured result did not move")
    checker.check("Delta_10min in the record",
                  round(record["observed"]["delta_window"], 3), 1.821)
    checker.check("Q95_null in the record",
                  round(record["null"]["q95"], 3), 0.526)
    checker.check("the gate still passes", record["verdict"]["passed"], True)
    checker.check("the label is unchanged", record["verdict"]["label"],
                  "resolved, within tolerance")
    checker.check("inside_null is unchanged", record["verdict"]["inside_null"], False)
    checker.check("disposition", record["disposition"]["disposition"], "passes")
    checker.check("advances", record["disposition"]["advances"], True)
    checker.check("conflict", record["disposition"]["conflict"], False)

    print("")
    print("%d checks, %d failed" % (checker.passed + checker.failed, checker.failed))
    return 1 if checker.failed else 0


if __name__ == "__main__":
    sys.exit(main())
