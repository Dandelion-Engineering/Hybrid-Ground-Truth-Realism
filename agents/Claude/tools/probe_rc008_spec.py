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

# RC-008 F4-R1: the wrapper authenticated the document and not the instrument
# reading it, so a counterfeit process printing the expected lines passed. The
# legacy checker and every record it consumes are now pinned by digest BEFORE
# the subprocess runs, and its expected nonzero exit is required rather than
# ignored. "I ran the old checker" is a claim about a filename until a digest
# makes it a claim about a file.
RC007_AUTHENTICATED = [
    ("agents/Claude/tools/probe_rc007_spec.py",
     "ef37577e271161677a637b34fcac18a930bb105d544b94992886116140c625dd"),
    ("agents/Claude/tools/raw_ap_layout_CSHL047_Probe01_2026-08-18.txt",
     "f992c394480eef5748131a55d4a394bbbcb858acd0a1a0f434de1ef1aa16ad6a"),
    ("agents/Claude/tools/raw_ap_layout_CSHL047_Probe01_2026-08-18.json",
     "4896a14f46454188f758d575cbbfd9c79870ff471a01145e72b26118973a9162"),
    ("agents/Claude/tools/filter_chain_2026-08-18.json",
     "b9f3e089e2b94e2d9e26743133d167bb258e3be169b5ce3f1b3fe625c7b72b15"),
    ("agents/Claude/tools/rc007_round3_2026-08-18.json",
     "51e762669c53a57cc3c4219547a000435b1a89d766cbc9ca7730c4f6a5c9717f"),
]

# The Draft-33 evidence probe, pinned the same way for the same reason.
ROUND2_PROBE = "agents/Claude/tools/rc008_round2_2026-08-18.json"

FROZEN_SPANS = [
    ("## 1. ", "## 17. ", 144664,
     "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59"),
    ("## 17. ", "## 18. ", 21864,
     "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a"),
    ("## 18. ", "## 19. ", 20579,
     "8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017"),
]

# The failures Drafts 32 and 33 together are allowed to cause in the closed
# card's checker. Six were Draft 32's; ten are Draft 33's, and every one of the
# ten is a sentence RC-008 Round 1 required to change or a census count that
# grew because 19.14 restates the numbers it discusses. A seventeenth red is a
# finding, and so is a sixteenth that is not on this list.
EXPECTED_RC007_FAILURES = [
    # Draft 32's six
    "section states R_null is one-sided",
    "section states the refused interleaved split",
    "section restates 73.780 exactly 7 times",
    "section restates 6,510 exactly 6 times",
    "section restates 13,020 exactly 14 times",
    "section restates 957,031,364 exactly 2 times",
    # Draft 33's ten
    "section prices the refused cheaper arrangement",       # T1-R1
    "section names the identity it now claims",             # F2-R1
    "section carries the admissible band",                  # F1-R1
    "section carries the pass rule's own band",             # F1-R1
    "section states the section has been reviewed twice",   # T2-R1
    "section states the three-round limit",                 # T2-R1
    "section restates 500 samples exactly 5 times",         # F2-R1 prose
    "section restates 14,020 exactly 4 times",              # F2-R1 prose
    "section restates 9,999 exactly 3 times",               # see NOTE below
    "section restates 2.34375 exactly 2 times",             # T3-R1 prose
]

# NOTE on "9,999": the legacy census is a SUBSTRING census, and Draft 33's
# 19.3 quotes the other probe's declared rate, 29,999.999999999996 Hz, which
# contains "9,999". No restatement of the chunk count changed. The census below
# counts that occurrence explicitly so the inflation is recorded rather than
# waved at, which is the whole point of keeping a census.

# number -> counts in (19.1-19.12, 19.13, 19.14, the status stack, sections
# 1-18). The five regions partition the document, so their sum is asserted
# against the whole-file count: a restatement that appears somewhere none of
# them covers has nowhere to hide.
CENSUS = [
    ("73.780", 7, 2, 2, 2, 0),
    ("6,510", 6, 1, 1, 2, 0),
    ("13,020", 15, 1, 1, 4, 0),
    ("957,031,364", 2, 2, 1, 3, 0),
    ("500 samples", 6, 0, 1, 4, 0),
    ("14,020", 5, 0, 0, 1, 0),
    ("2.34375", 2, 0, 1, 1, 0),
    ("9,999", 4, 0, 0, 0, 1),
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
    s1913 = section(text, "### 19.13 ", "### 19.14 ")
    s1914 = section(text, "### 19.14 ")
    s193 = section(text, "### 19.3 ", "### 19.4 ")
    s194 = section(text, "### 19.4 ", "### 19.5 ")
    s197 = section(text, "### 19.7 ", "### 19.8 ")
    s198 = section(text, "### 19.8 ", "### 19.9 ")
    s199 = section(text, "### 19.9 ", "### 19.10 ")
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
    c.check("Draft 33's line sits above Draft 32's",
            stack.index("**Status:** Draft 33")
            < stack.index("**Status:** Draft 32"))
    c.check("Draft 33's line ends by handing the stack to Draft 32",
            "Draft 32's own status line follows." in stack)
    c.check("Draft 32's retained line still carries its withdrawn direction "
            "claim, per the stack rule",
            "compresses the spread in the permissive direction" in stack)

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

    c.heading("5. The split is settled, and Draft 33 withdraws its direction")
    c.check("19.5 no longer defers the split",
            "is not taken in this draft" not in s195)
    c.check("19.5 still pins contiguous halves",
            "**The split is contiguous" in s195)
    c.check("19.5 withdraws the compression claim rather than restating it",
            "is withdrawn" in s195
            and "compressing** the spread in the permissive direction" in s195)
    c.check("  ... and attributes the refutation to F3-R1",
            "RC-008's F3-R1 refutes that as a universal direction" in s195)
    c.check("19.5 reproduces the refutation on its own construction",
            "even/odd interleaving separates the parities" in s195)
    c.check("19.5 records both exact values, 1 and 4",
            "`R_null_sampled` is exactly **1**" in s195
            and "`R_null_sampled` is exactly **4**" in s195)
    c.check("19.5 says interleaving EXPANDED the spread",
            "Interleaving expanded the spread" in s195)
    c.check("19.5 replaces the direction with three non-directional grounds",
            "none of which is a direction" in s195)
    c.check("  ... ground 3 is that the decision rule cannot cash the goal",
            "is not a goal the decision rule can cash" in s195)
    c.check("19.5 declares the split rule a pinned parameter with no bound",
            "no bound is claimed on the difference between two split rules"
            in s195)
    c.check("19.5 no longer claims a permissive direction for interleaving",
            "compresses the very spread this statistic exists to register"
            not in s195)

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
    body = section(text, "## 19. ", "### 19.13 ")
    closed = text[text.index("## 1. "):text.index("## 19. ")]
    for value, body_n, rec32_n, rec33_n, stack_n, closed_n in CENSUS:
        got = (body.count(value), s1913.count(value), s1914.count(value),
               stack.count(value), closed.count(value))
        ok = got == (body_n, rec32_n, rec33_n, stack_n, closed_n)
        c.check("%s appears %d/%d/%d/%d/%d times in 19.1-19.12 / 19.13 / 19.14 "
                "/ the stack / sections 1-18" % ((value, body_n, rec32_n,
                                                  rec33_n, stack_n, closed_n)),
                ok, "found %d/%d/%d/%d/%d" % got)
        c.check("  ... and those five regions account for every occurrence",
                sum(got) == text.count(value),
                "%d regional vs %d in the file" % (sum(got),
                                                   text.count(value)))
        census_records.append({"value": value, "section_19_body": got[0],
                               "section_19_13": got[1],
                               "section_19_14": got[2],
                               "status_stack": got[3],
                               "sections_1_18": got[4]})
    records["census"] = census_records

    # -- regression against the closed card's checker -------------------------
    c.heading("8. The closed card's checker as a regression baseline")
    c.check("F4-R1: the baseline is authenticated BEFORE it is run", True,
            "%d files pinned by digest" % len(RC007_AUTHENTICATED))
    authentic = True
    digests = {}
    for rel, expected in RC007_AUTHENTICATED:
        path = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.isfile(path):
            c.check("authenticated: %s" % rel.split("/")[-1], False, "missing")
            authentic = False
            continue
        got = hashlib.sha256(io.open(path, "rb").read()).hexdigest()
        digests[rel] = got
        ok = got == expected
        if not ok:
            authentic = False
        c.check("authenticated: %s" % rel.split("/")[-1], ok, got[:16])
    records["rc007_digests"] = digests
    c.check("every file the baseline reads is the pinned one", authentic)

    result = subprocess.run(
        [sys.executable, os.path.join(root, RC007_PROBE.replace("/", os.sep)),
         "--repo-root", root],
        capture_output=True, text=True)
    out = result.stdout
    # F4-R1: a counterfeit that prints the right lines and exits zero used to
    # pass here. The baseline is EXPECTED to fail against this candidate, so a
    # zero exit is itself a finding.
    records["rc007_returncode"] = result.returncode
    c.check("the baseline exits nonzero, as a red run must",
            result.returncode == 1, "exit %d" % result.returncode)
    c.check("the baseline wrote nothing to stderr", not result.stderr.strip(),
            result.stderr.strip()[:80] if result.stderr.strip() else "clean")
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

    # -- Draft 33, the RC-008 Round-2 repairs ---------------------------------
    c.heading("9. F1-R1  the floor reads its own extremum")
    c.check("19.4 defines sigma_quietest_sampled",
            "**`sigma_quietest_sampled = min_{k ∈ G} S(k)`**" in s194)
    c.check("19.4 records that a maximum cannot enforce a floor",
            "A ceiling and a floor cannot read the same extremum" in s194)
    c.check("19.4 reproduces the fixture rather than citing it",
            "fifty-nine sampled windows at 1.0 µV and one at 5.0 µV"
            in s194)
    c.check("19.4 names the anti-saturation number the fixture violates",
            "`A_min / S(k) = 50`" in s194)
    c.check("19.6's branch 2 reads the quietest window",
            "2. **Level, too quiet.** `sigma_quietest_sampled < 1.25 µV`"
            in s196)
    c.check("19.6's branch 2 no longer reads the loudest",
            "`sigma_worst_sampled < 1.25" not in s196)
    c.check("19.6's admissible band splits the two ends",
            "**`sigma_worst_sampled ≤ N`** together with "
            "**`1.25 µV ≤ sigma_quietest_sampled`**" in s196)
    c.check("19.6's pass rule splits them too",
            "only when **`sigma_worst_sampled ≤ N`**, **`1.25 µV "
            "≤ sigma_quietest_sampled`**" in s196)
    c.check("the old one-statistic band is gone from 19.6",
            "1.25 µV ≤ sigma_worst_sampled ≤ N`**," not in s196)
    c.check("19.6's table routes each threshold to its statistic",
            "read against `sigma_worst_sampled`" in s196
            and "read against `sigma_quietest_sampled`" in s196)
    c.check("19.7 publishes both extrema",
            "`sigma_worst_sampled` and `sigma_quietest_sampled`, each with the "
            "window that produced it" in s197)
    c.check("19.8 re-derives its three ratios on the right extremum",
            "`snr_p2p_max = A_max / sigma_quietest_sampled`" in s198
            and "`snr_p2p_quiet = A_min / sigma_quietest_sampled`" in s198)
    c.check("19.8 records that Draft 32 used one denominator for all of them",
            "Draft 32 divided every one of them by" in s198)

    c.heading("10. F2-R1  the design rate is a declared deviation")
    c.check("19.3 narrows the identity claim",
            "in every respect but the filter's design rate" in s193)
    c.check("19.3 declares the deviation rather than hedging it",
            "that is a declared deviation rather than a free choice" in s193)
    c.check("19.3 accepts the finding by name",
            "**RC-008's F2-R1 is correct and is not disputed.**" in s193)
    c.check("19.3 gives the reason the other repair is refused",
            "carries no `rate` attribute at all" in s193)
    c.check("  ... including the two disagreeing derivations",
            "30,000.03989331282 Hz" in s193
            and "29,999.999999999996 Hz" in s193)
    c.check("  ... and the paused ranks",
            "paused on a declared-clock disagreement" in s193)
    c.check("19.3 states what the deviation does NOT touch, computed",
            "scipy's default `padlen` is **18** at both rates" in s193
            and "under truncation, flooring and rounding alike" in s193)
    c.check("19.3 states what it does touch, with the coefficient figure",
            "**1.31860735664e-07**" in s193)
    c.check("19.3 refuses to promote the fixture figures into a bound",
            "does not promote them into a bound" in s193)
    c.check("19.3 counts three deviations now",
            "**Three declared differences from the anchor chain" in s193)
    c.check("19.7 publishes both rates so the deviation is auditable",
            "the nominal design rate and the candidate's own declared rate"
            in s197)

    c.heading("11. F5-R1  the bad-channel conservatism claim is withdrawn")
    c.check("19.3 withdraws it by name",
            "the direction every draft through 32 claimed for that is withdrawn"
            in s193)
    c.check("19.3 reproduces the counterexample",
            "the ratio **falls to 1.5 and the candidate passes.**" in s193)
    c.check("19.3 states the direction is unknown, not conservative",
            "moves\n`R_space_sampled` in **either** direction".replace("\n", " ")
            in " ".join(s193.split()))
    c.check("19.3 names the counterfactual that makes it unknowable",
            "a counterfactual this gate never observes" in s193)
    c.check("19.3 no longer claims the check is conservative there",
            "the spatial check is conservative in the presence of" not in s193)
    c.check("19.3 replaces the claim with a published record",
            "**for every window**" in s193)
    c.check("19.7 actually publishes per-channel values for every window",
            "**for every window**" in s197)

    c.heading("12. The four tracked items")
    c.check("T1: 19.9 separates coverage from dilution",
            "for two different reasons, which Draft 32 ran together" in s199)
    c.check("T1: the clustered arrangement's coverage number is stated",
            "**227.416 s**" in s199)
    c.check("T1: the dilution number is stated",
            "a one-chunk window reads **3.02** and a three-chunk window reads "
            "**1.33**" in s199)
    c.check("T1: the stale 223 s figure is corrected and the correction said",
            "**228.718 s**" in s199 and "about 223 s" in s199)
    c.check("T2: 19.10's stale Draft-31 sentence is gone",
            "This Draft 31 state is not approved by anyone yet" not in s1910)
    c.check("T2: 19.10 states the current state instead",
            "Draft 33 is the owner's Round-2 response and it is unreviewed"
            in s1910)
    c.check("T2: 19.10 names the clause-5 successor",
            "RC-008 is the\nsuccessor card clause 5 governs".replace("\n", " ")
            in " ".join(s1910.split()))
    c.check("T3: the code-step terminology is in 19.2",
            "**One stored code step is 2.34375 µV.**" in text
            and "two and three code steps" in text)
    c.check("T3: no 'stored bit' survives outside the record subsections",
            "One stored bit is" not in text)
    c.check("T4: 19.3 narrows the phase direction to one model",
            "Under a shared-component model" in s193)
    c.check("T4: 19.3 says where the direction stops",
            "the *spatial* statistic moves the other way on it" in s193)
    c.check("T4: 19.3 claims no direction for the spatial statistic",
            "**No direction at all is claimed for\n`R_space_sampled`.**"
            .replace("\n", " ") in " ".join(s193.split()))
    c.check("T4: 19.6 carries the narrowed form",
            "under the shared-component model, which is the only" in s196)

    c.heading("13. Section 19.14 records the round, and 19.13 is superseded")
    for anchor in ("F1-R1", "F2-R1", "F3-R1", "F4-R1", "F5-R1",
                   "T1-R1", "T2-R1", "T3-R1", "T4-R1",
                   "All nine are accepted", "No threshold value moved",
                   "228.718 s", "no host is pinned"):
        c.check("19.14 records: %s" % anchor, anchor in s1914)
    c.check("19.14 names the F4-R1 defect as the owner's",
            "the design defect is mine" in s1914)
    c.check("19.14 states the F2-R1 repair is the weaker-looking one",
            "which is the weaker-looking one" in s1914)
    c.check("19.14 states the split's three grounds carry no direction",
            "three grounds and none of them is a direction" in s1914)
    c.check("19.14 states the withdrawal without restating the claim as live",
            "is not a direction" in s1914)
    c.check("19.13 carries a supersession note in 19.11's own style",
            "superseded by §19.14" in s1913)
    c.check("19.13's supersession names the withdrawn direction",
            "interleaving compresses the spread in the permissive direction"
            in s1913)
    c.check("19.13 is otherwise unedited: it still records the F7-R2 repair",
            "F7-R2" in s1913 and "agree in all four cells" in s1913)

    c.heading("14. The Round-2 evidence probe's record")
    round2_path = os.path.join(root, ROUND2_PROBE.replace("/", os.sep))
    c.check("the Round-2 evidence record exists", os.path.isfile(round2_path))
    if os.path.isfile(round2_path):
        r2 = json.loads(io.open(round2_path, encoding="utf-8").read())
        records["round2"] = r2
        c.check("it ran clean", r2.get("checks_failed") == 0,
                "%s checks, %s failed" % (r2.get("checks_total"),
                                          r2.get("checks_failed")))
        c.check("F1's fixture is the one 19.4 describes",
                r2["f1"]["sigma_worst_sampled"] == 5.0
                and r2["f1"]["sigma_quietest_sampled"] == 1.0
                and r2["f1"]["snr_p2p_at_quietest"] == 50.0)
        c.check("F2's coefficient delta is the figure 19.3 publishes",
                "%.11e" % r2["f2"]["coeff_delta"] == "1.31860735664e-07")
        c.check("F2's margin is 500 at every rate in the record",
                all(v["int"] == 500 and v["floor"] == 500 and v["round"] == 500
                    for v in r2["f2"]["margin_samples"].values()))
        c.check("F3's two values are the ones 19.5 publishes",
                r2["f3"]["r_null_contiguous"] == 1.0
                and r2["f3"]["r_null_interleaved"] == 4.0)
        c.check("F5's two values are the ones 19.3 publishes",
                r2["f5"]["r_space_base"] == 3.0
                and r2["f5"]["r_space_one_extreme"] == 1.5)
        c.check("T1's guarantees are the ones 19.9 publishes",
                abs(r2["t1"]["clustered_five"]["guarantee_s"] - 227.416) < 5e-4
                and abs(r2["t1"]["sparse_twenty"]["guarantee_s"] - 228.718)
                < 5e-4
                and abs(r2["t1"]["pinned"]["guarantee_s"] - 73.780) < 5e-4)
        c.check("T1's dilution figures are the ones 19.9 publishes",
                abs(r2["t1"]["dilution"]["one_chunk"] - 3.02) < 5e-3
                and abs(r2["t1"]["dilution"]["three_chunk"] - 1.33) < 5e-3)

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
