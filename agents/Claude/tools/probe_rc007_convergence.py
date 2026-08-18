"""Convergence-Decision evidence for RC-007, owner side.

This script is evidence for Claude's one Convergence Decision statement on
Review Card RC-007. It edits no candidate byte and it reads no archive.

It answers four questions mechanically, against the frozen Draft-31 state:

  1. Is the candidate the frozen one? SHA-256 of the whole selection document
     and of the three closed spans it publishes digests for.
  2. How many live publishing surfaces carry the unconditional claim that a
     high R_null_sampled withholds the measurement, and where does each live?
     Codex's Round-3 statement names three; this counts them by offset.
  3. Does the high/high state have two declared dispositions? The four ordered
     branches of section 19.6 are implemented here and evaluated over a truth
     table, beside the unconditional prose claim.
  4. Does the approved drift gate of section 16.7 have the same asymmetry?
     Its rule is implemented here too and the two truth tables are compared
     cell by cell, so that the choice between the two permitted repairs is
     made against approved text rather than against preference.

Usage:

    ./venv/Scripts/python.exe agents/Claude/tools/probe_rc007_convergence.py \
        --repo-root . --out agents/Claude/tools/rc007_convergence_<date>.txt \
        --records agents/Claude/tools/rc007_convergence_<date>.json

Every check prints PASS or FAIL and the process exits non-zero if any failed.
"""

import argparse
import hashlib
import json
import os
import sys

DOC_REL = "agents/Claude/Tier A Host and Injection Zone Selection.md"

DRAFT31_DOC_SHA = "24e78a5ad139245b197286edd1acaf8bea42bc75af3378883b3180d29a923755"
FROZEN_SPANS = [
    ("## 1. ", "## 17. ", 144664,
     "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59"),
    ("## 17. ", "## 18. ", 21864,
     "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a"),
    ("## 18. ", "## 19. ", 20579,
     "8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017"),
]

# The unconditional surfaces. Each is
# (label, exact substring, expected count, where it must be found).
UNCONDITIONAL = [
    ("status line, Draft 31",
     "a high value withholds the measurement, a **low value certifies nothing**",
     1, "status-line stack (front matter)"),
    ("section 19.5",
     "A value **above** `M` is sufficient to withhold the measurement",
     1, "### 19.5"),
    ("section 19.10",
     "A value above `M` withholds the measurement",
     1, "### 19.10"),
    ("section 19.12",
     "a high value withholds the measurement, a low value certifies nothing",
     1, "### 19.12"),
]

# The one surface that states the condition correctly.
CONDITIONED = (
    "section 19.5, second statement",
    "if `R_null_sampled` exceeds the spatial tolerance and `R_space_sampled` "
    "does not, the candidate is `unmeasurable` rather than passing or failing",
    1,
)

SECTION_HEADINGS = [
    "## 1. ", "## 15. ", "## 16. ", "## 17. ", "## 18. ", "## 19. ",
]

SUBSECTION_HEADINGS = [
    "### 19.1 ", "### 19.2 ", "### 19.3 ", "### 19.4 ", "### 19.5 ",
    "### 19.6 ", "### 19.7 ", "### 19.8 ", "### 19.9 ", "### 19.10 ",
    "### 19.11 ", "### 19.12 ",
]

# The approved drift rule, quoted from section 16.7 for the offset check.
DRIFT_RULE_ANCHOR = (
    "a candidate passes drift only when both `Delta_10min <= L` and "
    "`Q95_null <= L`"
)
DRIFT_HIGH_HIGH_ANCHOR = "If `Delta_10min > L`, the candidate fails"
DRIFT_LOW_HIGH_ANCHOR = (
    "If `Delta_10min <= L` but `Q95_null > L`, the candidate is also rejected "
    "as unmeasurable"
)


class Checker(object):
    def __init__(self):
        self.lines = []
        self.failed = 0
        self.passed = 0

    def check(self, name, ok, detail=""):
        tag = "PASS" if ok else "FAIL"
        if ok:
            self.passed += 1
        else:
            self.failed += 1
        line = "%s  %s" % (tag, name)
        if detail:
            line += "  [%s]" % ascii_safe(detail)
        self.lines.append(line)
        print(line)

    def note(self, text):
        line = "      %s" % ascii_safe(text)
        self.lines.append(line)
        print(line)

    def heading(self, text):
        self.lines.append("")
        self.lines.append(text)
        print("")
        print(text)


def ascii_safe(text):
    return text.encode("ascii", "backslashreplace").decode("ascii")


# ---------------------------------------------------------------------------
# The two decision rules, implemented from the documents rather than described.
# ---------------------------------------------------------------------------

def noise_gate(sigma_worst, r_space, r_null, floor, n_level, m_spatial):
    """Section 19.6's four ordered branches. The first that fires is returned."""
    if sigma_worst > n_level:
        return "fails on level (too loud)"
    if sigma_worst < floor:
        return "fails on level (implausibly quiet)"
    if r_space > m_spatial:
        label = ("resolved heterogeneity" if r_space > r_null
                 else "resolution-limited")
        return "fails on homogeneity (%s)" % label
    if r_null > m_spatial:
        return "unmeasurable"
    return "passes"


def drift_gate(delta_10min, q95_null, threshold):
    """Section 16.7's rule, in the order that section states it."""
    if delta_10min > threshold:
        label = ("resolved drift" if delta_10min > q95_null
                 else "noise-limited")
        return "fails on drift (%s)" % label
    if q95_null > threshold:
        return "unmeasurable"
    return "passes"


def classify(disposition):
    """Reduce a disposition to the kind the two gates share."""
    if disposition.startswith("fails"):
        return "fails"
    return disposition


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="path to the repository root")
    parser.add_argument("--out", required=True,
                        help="path for the plain-text record")
    parser.add_argument("--records", default=None,
                        help="optional path for the JSON record")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.repo_root)
    doc_path = os.path.join(root, DOC_REL.replace("/", os.sep))
    raw = open(doc_path, "rb").read()
    text = raw.decode("utf-8")

    c = Checker()
    records = {}

    # -- 1. the frozen candidate --------------------------------------------
    c.heading("1. Candidate authentication - the frozen Draft-31 state")
    doc_sha = hashlib.sha256(raw).hexdigest()
    c.check("selection document SHA-256 is the frozen Draft-31 digest",
            doc_sha == DRAFT31_DOC_SHA, doc_sha)
    records["document_sha256"] = doc_sha
    records["document_bytes"] = len(raw)

    span_records = []
    for start, end, exp_len, exp_sha in FROZEN_SPANS:
        i = raw.index(start.encode("utf-8"))
        j = raw.index(end.encode("utf-8"))
        body = raw[i:j]
        sha = hashlib.sha256(body).hexdigest()
        ok = (len(body) == exp_len and sha == exp_sha)
        c.check("closed span %s-> %s is byte-identical" % (start.strip(), end.strip()),
                ok, "%d bytes %s" % (len(body), sha[:8]))
        span_records.append({"from": start.strip(), "to": end.strip(),
                             "bytes": len(body), "sha256": sha})
    records["frozen_spans"] = span_records

    # -- 2. the surface census ----------------------------------------------
    c.heading("2. Surface census - where the unconditional claim lives")

    offsets = {}
    repeated = []
    for h in SECTION_HEADINGS + SUBSECTION_HEADINGS:
        if text.count(h) != 1:
            repeated.append("%s x%d" % (h.strip(), text.count(h)))
        offsets[h.strip()] = text.index(h)
    c.check("every heading used for locating occurs exactly once",
            not repeated,
            ", ".join(repeated) if repeated else "%d headings" % len(offsets))

    def locate(pos):
        """Name the subsection or section a byte offset falls in."""
        best = None
        for name, start in offsets.items():
            if start <= pos and (best is None or start > offsets[best]):
                best = name
        if pos < offsets["## 1."]:
            return "status-line stack (front matter)"
        return best

    census = []
    total_unconditional = 0
    for label, needle, expected, expected_where in UNCONDITIONAL:
        count = text.count(needle)
        ok = (count == expected)
        c.check("unconditional surface present exactly %d time(s): %s"
                % (expected, label), ok, "count %d" % count)
        if count:
            pos = text.index(needle)
            where = locate(pos)
            c.check("  ... and it sits in %s" % expected_where,
                    where == expected_where, "located in %s" % where)
            census.append({"label": label, "count": count,
                           "located_in": where, "offset": pos})
        total_unconditional += count
    records["unconditional_surfaces"] = census
    records["unconditional_surface_count"] = total_unconditional

    c.check("the unconditional claim is live on FOUR surfaces, not three",
            total_unconditional == 4, "count %d" % total_unconditional)
    c.note("Codex's Round-3 convergence statement names three live surfaces:")
    c.note("the status line, section 19.5 and section 19.10. The fourth is in")
    c.note("section 19.12, the record subsection for Draft 31, which is live")
    c.note("prose in the present tense and is not marked superseded.")

    label, needle, expected = CONDITIONED
    count = text.count(needle)
    c.check("the correctly conditioned statement is present exactly once: %s"
            % label, count == expected, "count %d" % count)
    records["conditioned_surface_count"] = count

    # -- 3. the truth table --------------------------------------------------
    c.heading("3. The noise gate's own branches, executed")

    floor, n_level, m_spatial = 1.25, 10.0, 2.0
    sigma_ok = 5.0  # in band for every case below
    cases = [
        ("low  R_space, low  R_null", 1.5, 1.5, "passes"),
        ("low  R_space, high R_null", 1.5, 3.0, "unmeasurable"),
        ("high R_space, low  R_null", 3.0, 1.5,
         "fails on homogeneity (resolved heterogeneity)"),
        ("high R_space, high R_null", 3.0, 3.0,
         "fails on homogeneity (resolution-limited)"),
    ]
    table = []
    for name, r_space, r_null, expected_disp in cases:
        got = noise_gate(sigma_ok, r_space, r_null, floor, n_level, m_spatial)
        c.check("branch order gives '%s' for %s" % (expected_disp, name),
                got == expected_disp, got)
        withheld = (got == "unmeasurable")
        table.append({"case": name, "R_space": r_space, "R_null": r_null,
                      "disposition": got, "measurement_withheld": withheld})
    records["noise_gate_truth_table"] = table

    high_high = [row for row in table if row["case"].startswith("high R_space, high")][0]
    c.check("the high/high state is NOT withheld under the branch order",
            high_high["measurement_withheld"] is False,
            high_high["disposition"])
    c.check("Codex's counterexample reproduces: R_space=3, R_null=3, M=2 fails "
            "on homogeneity",
            noise_gate(sigma_ok, 3.0, 3.0, floor, n_level, m_spatial)
            == "fails on homogeneity (resolution-limited)")
    c.note("The prose says a value above M is sufficient to withhold the")
    c.note("measurement. The branches withhold in one of the two high-null")
    c.note("cases. The blocker is real and it is not disputed.")

    # -- 4. the approved parallel -------------------------------------------
    c.heading("4. The approved drift gate, executed beside it")

    for anchor in (DRIFT_RULE_ANCHOR, DRIFT_HIGH_HIGH_ANCHOR,
                   DRIFT_LOW_HIGH_ANCHOR):
        c.check("section 16.7 anchor present exactly once",
                text.count(anchor) == 1,
                anchor[:48])
        pos = text.index(anchor)
        inside = offsets["## 1."] <= pos < offsets["## 17."]
        c.check("  ... and it lies inside the closed, approved 1->17 span",
                inside, "offset %d" % pos)

    drift_cases = [
        ("low  Delta, low  Q95", 5.0, 5.0, "passes"),
        ("low  Delta, high Q95", 5.0, 30.0, "unmeasurable"),
        ("high Delta, low  Q95", 30.0, 5.0, "fails on drift (resolved drift)"),
        ("high Delta, high Q95", 30.0, 30.0, "fails on drift (noise-limited)"),
    ]
    drift_table = []
    for name, delta, q95, expected_disp in drift_cases:
        got = drift_gate(delta, q95, 20.0)
        c.check("drift rule gives '%s' for %s" % (expected_disp, name),
                got == expected_disp, got)
        drift_table.append({"case": name, "Delta_10min": delta,
                            "Q95_null": q95, "disposition": got})
    records["drift_gate_truth_table"] = drift_table

    c.heading("5. Cell-by-cell comparison of the two gates")
    mismatches = []
    for noise_row, drift_row in zip(table, drift_table):
        a = classify(noise_row["disposition"])
        b = classify(drift_row["disposition"])
        ok = (a == b)
        if not ok:
            mismatches.append((noise_row["case"], a, b))
        c.check("same kind of disposition in cell: %s" % noise_row["case"], ok,
                "%s vs %s" % (a, b))
    c.check("the two gates agree in all four cells", not mismatches,
            "%d mismatch(es)" % len(mismatches))
    records["cells_agreeing"] = 4 - len(mismatches)

    c.note("Section 16.7 is approved, closed and unedited since Session 17.")
    c.note("It resolves the high/high cell as a failure, exactly as section")
    c.note("19.6 does. The null there can convert a would-be pass into an")
    c.note("unmeasurable rejection; it never converts a would-be failure.")

    c.heading("6. What each permitted repair would do to that agreement")

    def noise_gate_null_first(sigma_worst, r_space, r_null, floor, n_level, m):
        """Codex's second permitted repair: give a high null precedence."""
        if sigma_worst > n_level:
            return "fails on level (too loud)"
        if sigma_worst < floor:
            return "fails on level (implausibly quiet)"
        if r_null > m:
            return "unmeasurable"
        if r_space > m:
            return "fails on homogeneity (resolved heterogeneity)"
        return "passes"

    reordered = []
    for name, r_space, r_null, _ in cases:
        got = noise_gate_null_first(sigma_ok, r_space, r_null, floor, n_level,
                                    m_spatial)
        reordered.append({"case": name, "disposition": got})
    changed = [row["case"] for row, base in zip(reordered, table)
               if classify(row["disposition"]) != classify(base["disposition"])]
    c.check("reordering changes exactly one cell", len(changed) == 1,
            ", ".join(changed) if changed else "none")
    c.check("the cell it changes is the high/high one",
            changed == ["high R_space, high R_null"],
            ", ".join(changed) if changed else "none")
    c.check("after reordering, the noise gate disagrees with approved 16.7 in "
            "that one cell",
            classify(reordered[3]["disposition"])
            != classify(drift_table[3]["disposition"]),
            "%s vs %s" % (reordered[3]["disposition"],
                          drift_table[3]["disposition"]))
    records["reordering_changed_cells"] = changed
    records["repair_a_preserves_parallel"] = True
    records["repair_b_preserves_parallel"] = False

    c.note("Repair (a) - condition the prose on R_space_sampled <= M - edits")
    c.note("four prose surfaces and leaves every branch, threshold and number")
    c.note("untouched, and keeps section 19.6 in the parallel with 16.7 that")
    c.note("section 19.5 itself claims.")
    c.note("Repair (b) - give a high null precedence - changes the executable")
    c.note("rule and puts the noise gate out of parallel with an approved,")
    c.note("closed section in exactly the cell under dispute.")

    # -- summary -------------------------------------------------------------
    c.heading("Summary")
    total = c.passed + c.failed
    summary = "%d checks, %d failed" % (total, c.failed)
    c.lines.append(summary)
    print(summary)
    records["checks_total"] = total
    records["checks_failed"] = c.failed

    out_path = os.path.join(root, args.out.replace("/", os.sep)) \
        if not os.path.isabs(args.out) else args.out
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(c.lines) + "\n")

    if args.records:
        rec_path = os.path.join(root, args.records.replace("/", os.sep)) \
            if not os.path.isabs(args.records) else args.records
        with open(rec_path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(records, handle, indent=2, sort_keys=True)
            handle.write("\n")

    return 1 if c.failed else 0


if __name__ == "__main__":
    sys.exit(main())
