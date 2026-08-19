"""Audit dominance claims in Claude's split-family sensitivity record.

The source probe reports, for each constructed fixture, which of the 32 fixed
block-interleaved split members withhold the measurement.  This script turns
that fixture-by-member table around: for each member, it computes the set of
fixtures on which that member withholds.  A member A strictly dominates B on
this constructed fixture set when B's withholding set is a proper subset of
A's.

This is a review of the recorded synthetic matrix only.  It does not read an
archive or candidate sample, and it makes no claim about real recordings.

Usage:

    ./venv/Scripts/python.exe agents/Codex/tools/probe_split_family_dominance.py \
        --records <split-family-sensitivity.json> --out <report.txt> \
        [--json <record.json>]
"""

import argparse
import hashlib
import io
import json
import sys


class Checks:
    """Collect named checks and render a stable text report."""

    def __init__(self):
        self.lines = []
        self.failed = 0

    def heading(self, text):
        """Append a section heading."""
        self.lines.extend(["", text])

    def check(self, name, condition, detail=""):
        """Record one Boolean check with an optional detail string."""
        if not condition:
            self.failed += 1
        suffix = "  [%s]" % detail if detail else ""
        self.lines.append("%s  %s%s" % (
            "PASS" if condition else "FAIL", name, suffix))

    def render(self):
        """Return the complete human-readable report."""
        total = sum(line.startswith(("PASS", "FAIL")) for line in self.lines)
        return "%s\n\nSummary\n%d checks, %d failed\n" % (
            "\n".join(self.lines), total, self.failed)


def load_record(path):
    """Read the source JSON and return its parsed object and SHA-256 digest."""
    with open(path, "rb") as handle:
        payload = handle.read()
    return json.loads(payload.decode("utf-8")), hashlib.sha256(payload).hexdigest()


def normalize(record):
    """Return sorted members, fixture rows, and member signatures as sets."""
    members = sorted(int(value) for value in record["members"])
    member_set = set(members)
    rows = {
        int(fixture): {int(value) for value in values}
        for fixture, values in record["withholding_members_by_fixture"].items()
    }
    signatures = {
        member: {fixture for fixture, values in rows.items() if member in values}
        for member in members
    }
    return members, member_set, rows, signatures


def dominance_relations(members, signatures):
    """Return all ordered strict set-dominance pairs (dominant, dominated)."""
    return sorted(
        (left, right)
        for left in members
        for right in members
        if left != right and signatures[right] < signatures[left]
    )


def main(argv=None):
    """Run the recorded-matrix audit and write text and optional JSON output."""
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--records", required=True,
                        help="Claude sensitivity probe's JSON record")
    parser.add_argument("--out", required=True,
                        help="path for the human-readable report")
    parser.add_argument("--json", default=None,
                        help="optional path for the structured audit record")
    args = parser.parse_args(argv)

    source, source_sha256 = load_record(args.records)
    members, member_set, rows, signatures = normalize(source)
    relations = dominance_relations(members, signatures)

    odd = {member for member in members if member % 2 == 1}
    even = member_set - odd
    expected = {(1, member) for member in odd - {1}}
    expected |= {(2, member) for member in even - {2}}
    relation_set = set(relations)
    duplicate_signatures = sorted(
        (left, right)
        for index, left in enumerate(members)
        for right in members[index + 1:]
        if signatures[left] == signatures[right]
    )

    checks = Checks()
    checks.heading("1. Authenticate and reconstruct the recorded matrix")
    checks.check("the record contains 32 unique members and 32 fixture rows",
                 len(members) == 32 and len(member_set) == 32
                 and set(rows) == member_set,
                 "source SHA-256 %s" % source_sha256)
    checks.check("every withholding entry names a member of the family",
                 all(values <= member_set for values in rows.values()),
                 "%d fixture-by-member cells" % (len(rows) * len(members)))
    checks.check("every member withholds on its own constructed fixture",
                 all(member in rows[member] for member in members),
                 "32 of 32 self-hits")

    checks.heading("2. Test the claimed absence of dominance")
    checks.check("the matrix contains 30 strict pairwise dominance relations",
                 len(relations) == 30,
                 "%d observed" % len(relations))
    checks.check("p=1 dominates every other odd member, and no others",
                 {(left, right) for left, right in relations if left == 1}
                 == {(1, member) for member in odd - {1}},
                 "15 strict supersets")
    checks.check("p=2 dominates every other even member, and no others",
                 {(left, right) for left, right in relations if left == 2}
                 == {(2, member) for member in even - {2}},
                 "15 strict supersets")
    checks.check("those are exactly all dominance relations in the matrix",
                 relation_set == expected,
                 "no cross-parity dominance")
    checks.check("no two members have equal withholding signatures",
                 not duplicate_signatures,
                 "32 distinct signatures")

    checks.heading("3. State the narrower result the matrix does support")
    checks.check("p=1 withholds on exactly the 16 odd-target fixtures",
                 signatures[1] == odd,
                 "signature size %d" % len(signatures[1]))
    checks.check("p=2 withholds on exactly the 16 even-target fixtures",
                 signatures[2] == even,
                 "signature size %d" % len(signatures[2]))
    checks.check("p=1 and p=2 are incomparable, disjoint, and cover all rows",
                 not signatures[1] <= signatures[2]
                 and not signatures[2] <= signatures[1]
                 and not (signatures[1] & signatures[2])
                 and signatures[1] | signatures[2] == member_set,
                 "a two-member OR envelope covers this constructed set")
    checks.check("the self-target fixture does not isolate every possible pin",
                 len(rows[1]) == 16 and len(rows[2]) == 1
                 and all(len(rows[member]) == 2
                         for member in members if member not in (1, 2)),
                 "row sizes are 16 for p_t=1, 1 for p_t=2, otherwise 2")

    output_record = {
        "source_sha256": source_sha256,
        "members": members,
        "dominance_relations": relations,
        "dominance_count": len(relations),
        "duplicate_signatures": duplicate_signatures,
        "signature_by_member": {
            str(member): sorted(signatures[member]) for member in members
        },
        "fixture_row_sizes": {
            str(fixture): len(rows[fixture]) for fixture in members
        },
        "boundary": (
            "Constructed-fixture matrix only; no archive or real-data claim. "
            "The source sweep supports self-hits and no single all-fixture "
            "member, but not an absence of pairwise dominance."
        ),
    }

    report = checks.render()
    sys.stdout.write(report)
    with io.open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(report)
    if args.json:
        with io.open(args.json, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(output_record, indent=2, sort_keys=True)
                         + "\n")
    return 1 if checks.failed else 0


if __name__ == "__main__":
    sys.exit(main())
