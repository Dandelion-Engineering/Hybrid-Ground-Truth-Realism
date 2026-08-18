"""Owner checker for Draft 32 of section 19 - the RC-007 convergence repair.

RC-007 is closed at `Revisions Required`, so `probe_rc007_spec.py` is a closed
card's evidence script and is not extended. This is a new checker for the new
candidate, and it does three things the old one cannot:

  1. It checks the repair itself - that the unconditional withholding claim is
     gone from the two operative surfaces, that the two record surfaces are
     handled by the document's own conventions instead (a supersession note in
     the record subsection, a corrected line at the top of the status stack),
     and that the asymmetry rule the branches always implemented is now written
     down in all three operative places.
  2. It settles the tracked split by asserting the decision is stated, with its
     direction and its own limitation.
  3. It uses the closed card's checker as a REGRESSION BASELINE rather than
     extending it: `probe_rc007_spec.py` is run as a subprocess and must return
     exactly 288 checks with exactly the six failures this repair was supposed
     to cause - no more, and no fewer. Every other property RC-007 established
     is therefore still enforced by the instrument that established it.

Usage:

    ./venv/Scripts/python.exe agents/Claude/tools/probe_rc008_spec.py \
        --repo-root . [--out <path>] [--records <path>]
"""

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys

DOC_REL = "agents/Claude/Tier A Host and Injection Zone Selection.md"
RC007_PROBE = "agents/Claude/tools/probe_rc007_spec.py"

FROZEN_SPANS = [
    ("## 1. ", "## 17. ", 144664,
     "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59"),
    ("## 17. ", "## 18. ", 21864,
     "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a"),
    ("## 18. ", "## 19. ", 20579,
     "8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017"),
]

# The six failures this repair is allowed to cause in the closed card's checker.
EXPECTED_RC007_FAILURES = [
    "section states R_null is one-sided",
    "section states the refused interleaved split",
    "section restates 73.780 exactly 7 times",
    "section restates 6,510 exactly 6 times",
    "section restates 13,020 exactly 14 times",
    "section restates 957,031,364 exactly 2 times",
]

# number -> (count inside 19.1-19.12, count inside 19.13, count in the stack)
CENSUS = [
    ("73.780", 7, 2, 2),
    ("6,510", 6, 1, 1),
    ("13,020", 14, 1, 3),
    ("957,031,364", 2, 2, 2),
]

# The rule is stated in the two operative sections, in the branch list,
# and once at the top of the status stack: four, not three.
ASYMMETRY = ("it never converts a would-be failure into anything else",
             4)


class Checker(object):
    def __init__(self):
        self.lines = []
        self.failed = 0
        self.passed = 0

    def check(self, name, ok, detail=""):
        if ok:
            self.passed += 1
        else:
            self.failed += 1
        line = "%s  %s" % ("PASS" if ok else "FAIL", name)
        if detail:
            line += "  [%s]" % detail.encode("ascii", "backslashreplace").decode("ascii")
        self.lines.append(line)
        print(line)

    def heading(self, text):
        self.lines.append("")
        self.lines.append(text)
        print("")
        print(text)


def section(text, start, end=None):
    i = text.index(start)
    j = text.index(end) if end else len(text)
    return text[i:j]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", default=None)
    parser.add_argument("--records", default=None)
    args = parser.parse_args(argv)

    root = os.path.abspath(args.repo_root)
    doc_path = os.path.join(root, DOC_REL.replace("/", os.sep))
    raw = io.open(doc_path, "rb").read()
    text = raw.decode("utf-8")

    c = Checker()
    records = {"document_sha256": hashlib.sha256(raw).hexdigest(),
               "document_bytes": len(raw)}

    # -- closed sections -----------------------------------------------------
    c.heading("1. The closed sections are still closed")
    c.check("the document is LF throughout", "\r\n" not in text)
    for start, end, exp_len, exp_sha in FROZEN_SPANS:
        body = raw[raw.index(start.encode()):raw.index(end.encode())]
        sha = hashlib.sha256(body).hexdigest()
        c.check("span %s-> %s byte-identical" % (start.strip(), end.strip()),
                len(body) == exp_len and sha == exp_sha,
                "%d bytes %s" % (len(body), sha[:8]))

    # -- the repair ----------------------------------------------------------
    c.heading("2. The repair - the unconditional claim on the two operative surfaces")

    s195 = section(text, "### 19.5 ", "### 19.6 ")
    s196 = section(text, "### 19.6 ", "### 19.7 ")
    s1910 = section(text, "### 19.10 ", "### 19.11 ")
    s1912 = section(text, "### 19.12 ", "### 19.13 ")
    s1913 = section(text, "### 19.13 ")
    stack = text[:text.index("## 1. ")]

    # The withdrawn wording survives in 19.5 exactly once, inside the sentence
    # that withdraws it. A withdrawal has to name what it withdraws, so the
    # check is that the only surviving occurrence is that one.
    withdrawn = "is sufficient to withhold the measurement"
    c.check("19.5 carries the withdrawn wording exactly once",
            s195.count(withdrawn) == 1, "found %d" % s195.count(withdrawn))
    c.check("  ... and that one occurrence is inside the withdrawal sentence",
            s195.count("Draft 31 said instead that a value above `M` "
                       + withdrawn) == 1)
    c.check("19.5 asserts the claim as withdrawn",
            "that claim is withdrawn" in s195)
    c.check("19.5 states the condition instead",
            "where, and only where, `R_space_sampled ≤ M`" in s195)
    c.check("19.5 says a high null there changes the label and not the disposition",
            "changes the label and not the disposition" in s195)
    c.check("19.5 attributes the asymmetry to 16.7 rather than inventing it",
            "transposed rather than invented" in s195)
    c.check("19.5 records that the withdrawn claim was found by F7-R2",
            "F7-R2" in s195)

    c.check("19.10 no longer carries the unconditional bullet",
            "A value above `M` withholds the measurement;" not in s1910)
    c.check("19.10 carries the conditioned bullet",
            "only where `R_space_sampled ≤ M`" in s1910)

    c.heading("3. The repair - the two record surfaces, by the document's own conventions")
    c.check("19.12 is marked as a record with one claim superseded by 19.13",
            "superseded by §19.13" in s1912)
    c.check("19.12's supersession names the condition",
            "only where `R_space_sampled ≤ M`, not unconditionally" in s1912)
    c.check("19.12's interleaved-split follow-up is declared closed",
            "no longer open" in s1912)
    c.check("Draft 31's retained status line still carries its own claim, per "
            "the stack rule",
            stack.count("a high value withholds the measurement, a **low value "
                        "certifies nothing**") == 1)
    c.check("Draft 32's line sits above it and states the correction",
            stack.index("**Status:** Draft 32")
            < stack.index("**Status:** Draft 31"))
    c.check("Draft 32's line names the four surfaces",
            "said in four places" in stack)
    c.check("Draft 32's line ends by handing the stack to Draft 31",
            "Draft 31's own status line follows." in stack)

    c.heading("4. The rule is written down where the branches are")
    c.check("the asymmetry rule appears in exactly %d places" % ASYMMETRY[1],
            text.count(ASYMMETRY[0]) == ASYMMETRY[1],
            "found %d" % text.count(ASYMMETRY[0]))
    for name, chunk in (("19.5", s195), ("19.6", s196), ("19.10", s1910),
                        ("the status stack", stack)):
        c.check("  ... one of them is in %s" % name, ASYMMETRY[0] in chunk)
    c.check("19.6 names the two places the null appears",
            "it decides branch 3's *label*, and it is the whole of branch 4" in s196)
    c.check("19.6 keeps all four ordered branches",
            all(marker in s196 for marker in
                ("1. **Level, too loud.**", "2. **Level, too quiet.**",
                 "3. **Homogeneity.**", "4. **Resolution.**")))
    c.check("19.6's branch 4 is unchanged",
            "`R_space_sampled ≤ M` and `R_null_sampled > M` → "
            "**unmeasurable**" in s196)

    c.heading("5. The tracked split is settled, with its direction and its limit")
    c.check("19.5 no longer defers the split",
            "is not taken in this draft" not in s195)
    c.check("19.5 pins contiguous halves", "the answer is **contiguous" in s195)
    c.check("19.5 states the mechanism it is refusing",
            "share their local epochs" in s195)
    c.check("19.5 states the DIRECTION of the refused alternative",
            "**permissive** direction" in s195)
    c.check("19.5 states what the choice does not fix",
            "still certifies nothing" in s195)
    c.check("19.5 labels its own argument unmeasured",
            "structural and unmeasured" in s195)

    c.heading("6. Section 19.13 records the change")
    for anchor in ("F7-R2", "Convergence Decision", "39 checks, 0 failed",
                   "4 of 4 caught", "agree in all four cells",
                   "does not change which host", "Nothing executable"):
        c.check("19.13 records: %s" % anchor, anchor in s1913)
    c.check("19.13 records the strongest argument against the repair taken",
            "may not resolve at scale `M`" in s1913)

    # -- census --------------------------------------------------------------
    c.heading("7. Restatement census, recounted by region rather than assumed")
    census_records = []
    for value, body_n, new_n, stack_n in CENSUS:
        body = section(text, "## 19. ", "### 19.13 ")
        got = (body.count(value), s1913.count(value), stack.count(value))
        ok = got == (body_n, new_n, stack_n)
        c.check("%s appears %d/%d/%d times in 19.1-19.12 / 19.13 / the stack"
                % (value, body_n, new_n, stack_n), ok,
                "found %d/%d/%d" % got)
        census_records.append({"value": value, "section_19_body": got[0],
                               "section_19_13": got[1], "status_stack": got[2]})
    records["census"] = census_records
    c.check("no pre-existing section-19 restatement moved",
            all(section(text, "## 19. ", "### 19.13 ").count(v) == n
                for v, n, _, _ in CENSUS))

    # -- regression against the closed card's checker -------------------------
    c.heading("8. The closed card's checker as a regression baseline")
    result = subprocess.run(
        [sys.executable, os.path.join(root, RC007_PROBE.replace("/", os.sep)),
         "--repo-root", root],
        capture_output=True, text=True)
    out = result.stdout
    summary = [line for line in out.splitlines() if line.endswith("failed")]
    c.check("the RC-007 checker still runs to completion", bool(summary),
            summary[-1] if summary else "no summary line")
    c.check("it still runs 288 checks",
            bool(summary) and summary[-1].startswith("288 checks"),
            summary[-1] if summary else "")
    failures = [line.split("--")[0].replace("[FAIL]", "").strip()
                for line in out.splitlines() if line.startswith("[FAIL]")]
    records["rc007_failures"] = failures
    c.check("exactly %d checks went red" % len(EXPECTED_RC007_FAILURES),
            len(failures) == len(EXPECTED_RC007_FAILURES),
            "%d red" % len(failures))
    for name in EXPECTED_RC007_FAILURES:
        c.check("expected red: %s" % name, name in failures)
    unexpected = [f for f in failures if f not in EXPECTED_RC007_FAILURES]
    c.check("no unexpected check went red", not unexpected,
            ", ".join(unexpected) if unexpected else "none")

    c.heading("Summary")
    total = c.passed + c.failed
    line = "%d checks, %d failed" % (total, c.failed)
    c.lines.append(line)
    print(line)
    records["checks_total"] = total
    records["checks_failed"] = c.failed

    if args.out:
        path = args.out if os.path.isabs(args.out) else os.path.join(root, args.out)
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            "\n".join(c.lines) + "\n")
    if args.records:
        path = args.records if os.path.isabs(args.records) \
            else os.path.join(root, args.records)
        with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(records, indent=2, sort_keys=True) + "\n")

    return 1 if c.failed else 0


if __name__ == "__main__":
    sys.exit(main())
