"""What the split-family sweep establishes, after Codex's dominance correction.

Session 49's `probe_split_family_sensitivity.py` computed a correct 32 x 32
matrix and then attached to it a claim its checks did not test. The check named
"no member is uniformly cautious and none is uniformly permissive" carried the
detail string "the family has no dominating member", and the module docstring
said "none dominates". Absence of an all-fixture or no-fixture member is not
absence of pairwise dominance, and Codex's Session-49 audit
(`agents/Codex/tools/probe_split_family_dominance.py`) showed the matrix
contains 30 strict dominance relations. That correction is accepted in full.

This probe does three things, in order:

  1. authenticates the Session-49 record by its SHA-256 before reading it;
  2. RECOMPUTES the whole 32 x 32 matrix from the stated construction along an
     independently written code path - different mask construction, an explicit
     sort-based median rather than `numpy.median`, and an explicit nearest-rank
     index - and requires it to agree with the record cell for cell. Codex's
     replay established that the Session-49 probe is deterministic; it did not
     establish that its implementation is right. This is that missing check;
  3. re-derives the dominance structure from the recomputed matrix WITHOUT
     Codex's code, and requires the count and the exact relation set to match
     what Codex reported.

It then records, as checks rather than prose, which Session-49 statements
survive and which are withdrawn.

WITHDRAWN: "the family has no dominating member"; "none dominates".
SURVIVING: every member withholds on the fixture built at its own block length
(32 of 32); no member withholds on every fixture; no member withholds on none;
the split parameter reaches a decision. Those four are what the matrix supports.

NEW, and it is Codex's, re-derived here: `p = 1` withholds on exactly the 16
odd-target fixtures and `p = 2` on exactly the 16 even-target fixtures; those
two are incomparable and their union covers all 32; every other odd member's
signature is `{1, p}` and every other even member's is `{p}`; the 30 relations
are exactly the 15 + 15 those two dominations generate.

BOUNDARY, and it governs everything above. These are 32 CONSTRUCTED fixtures,
each built to be visible to one member, and the dominance structure is a
property of that construction. Nothing here says how often such structure
occurs in a real recording, nothing here claims a direction for any member on
real data, and - this is the part of Codex's correction that matters most for
design - none of it defeats the reading under which one member is pinned and
disclosed. Different answers on adversarially member-matched fixtures are what
distinct conventions do.

Nothing here reads the archive, the network, or any candidate sample. Its only
input is a Session-49 record written by this workspace.

Usage:

    ./venv/Scripts/python.exe \\
        agents/Claude/tools/probe_split_family_narrowing.py \\
        --source agents/Claude/tools/split_family_sensitivity_2026-08-19.json \\
        --out <path> [--records <path>]
"""

import argparse
import hashlib
import io
import json
import sys

import numpy as np

RETAINED = 13020
HALF = RETAINED // 2
MAD_SCALE = 0.6744897501960817
M_STRICT = 2.0
N_STRICT = 10.0
FLOOR = 1.25

# The Session-49 record this probe corrects, pinned by digest. Codex's audit
# cites the same digest, so all three readings are of one set of bytes.
SOURCE_SHA256 = ("f51b4949e8406b7bb237a49ecb3af985ce5127896"
                 "a680e28c58b67f06a9b4fcb")

# The fixed sigma values Session 49 fed the branch rule so that branches 1 and
# 2 could not fire and branch 4 was what decided. Restated, not imported.
SIGMA_WORST = 6.0
SIGMA_QUIET = 5.0


class Checks(object):
    """Collect pass/fail lines and print them in the project's console form."""

    def __init__(self):
        self.lines = []
        self.failed = 0

    def heading(self, text):
        """Append a blank line and a section heading."""
        self.lines.append("")
        self.lines.append(text)

    def note(self, text):
        """Append a line that is deliberately NOT a check."""
        self.lines.append("NOTE  " + text)

    def check(self, name, ok, detail=""):
        """Record one check; `detail` is printed either way."""
        if not ok:
            self.failed += 1
        self.lines.append("%s  %s%s" % ("PASS" if ok else "FAIL", name,
                                        ("  [%s]" % detail) if detail else ""))
        return ok

    def render(self):
        """Return the full report with the trailing check-count summary."""
        body = "\n".join(self.lines)
        total = sum(1 for line in self.lines
                    if line.startswith("PASS") or line.startswith("FAIL"))
        return "%s\n\nSummary\n%d checks, %d failed\n" % (body, total,
                                                          self.failed)


def load_source(path):
    """Read the Session-49 record and return its object and SHA-256 digest."""
    payload = io.open(path, "rb").read()
    return json.loads(payload.decode("utf-8")), hashlib.sha256(
        payload).hexdigest()


def divisors(n):
    """Every positive divisor of n, ascending."""
    out = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            if d != n // d:
                out.append(n // d)
        d += 1
    return sorted(out)


def median_by_sort(x, axis=-1):
    """Median by explicit sort, deliberately not `numpy.median`.

    Written this way so that a defect in the Session-49 estimator would have to
    be reproduced by a different construction to survive this probe.
    """
    ordered = np.sort(np.asarray(x, dtype=float), axis=axis)
    n = ordered.shape[axis]
    lo = np.take(ordered, [n // 2 - 1], axis=axis)
    hi = np.take(ordered, [n // 2], axis=axis)
    if n % 2 == 1:
        return np.squeeze(np.take(ordered, [n // 2], axis=axis), axis=axis)
    return np.squeeze((lo + hi) / 2.0, axis=axis)


def sigma_by_sort(x):
    """MAD scale estimate along the last axis, via `median_by_sort`."""
    med = median_by_sort(x)
    return median_by_sort(np.abs(x - med[..., None])) / MAD_SCALE


def nearest_rank_index(values, q):
    """Nearest-rank percentile by explicit one-based rank index."""
    ordered = np.sort(np.asarray(values, dtype=float))
    rank = -(-int(round(q * 100)) * ordered.size // 100)  # ceil(q * n)
    return ordered[max(rank, 1) - 1]


def spread_by_rank(values):
    """The p90/p10 nearest-rank ratio, built from `nearest_rank_index`."""
    return nearest_rank_index(values, 0.90) / nearest_rank_index(values, 0.10)


def mask_by_repeat(p, n=RETAINED):
    """Half A of the block-interleaved split, built by repeat-and-tile.

    Session 49 built the same mask as `(arange(n) // p) % 2 == 0`. This builds
    it as a tiled pair of length-p runs, which is a different construction of
    the same set and is valid because every member divides 6,510 and therefore
    2p divides 13,020.
    """
    if n % (2 * p):
        raise ValueError("block length %d does not tile %d samples" % (p, n))
    return np.tile(np.repeat(np.array([True, False]), p), n // (2 * p))


def core_by_tile(p_target, depths):
    """Session 49's fixture, rebuilt from its stated definition by tiling.

    Channel c's amplitude is modulated on blocks of length `p_target`, loud on
    even blocks. Inside a block the magnitude alternates 1, 1/2 and the sign
    runs +, -, -, + so every half has a nonzero MAD whatever the split. That
    fine structure is identical in every channel, so only the block modulation
    can create spread across channels.
    """
    sign = np.tile(np.array([1.0, -1.0, -1.0, 1.0]), RETAINED // 4)
    fine = np.tile(np.array([1.0, 0.5]), RETAINED // 2)
    loud = mask_by_repeat(p_target)
    rows = []
    for depth in depths:
        hi = float(depth) if depth >= 1 else 1.0
        lo = 1.0 if depth >= 1 else 1.0 / float(depth)
        rows.append(np.where(loud, hi, lo) * fine * sign)
    return np.array(rows)


def disposition(sigma_worst, sigma_quiet, r_space, r_null):
    """Section 19.6's four ordered branches; the first that fires wins."""
    if sigma_worst > N_STRICT:
        return "fails-level-loud"
    if sigma_quiet < FLOOR:
        return "fails-level-quiet"
    if r_space > M_STRICT:
        return ("fails-homogeneity-resolved" if r_space > r_null
                else "fails-homogeneity-resolution-limited")
    if r_null > M_STRICT:
        return "unmeasurable"
    return "passes"


def recompute(members, depths):
    """Rebuild the 32 x 32 matrix along the independent path.

    Returns the withholding table keyed by fixture, the per-fixture
    `R_space_sampled`, and the per-fixture per-member null ratios.
    """
    withheld = {}
    spaces = {}
    nulls = {}
    for target in members:
        core = core_by_tile(target, depths)
        r_space = float(spread_by_rank(sigma_by_sort(core)))
        spaces[target] = r_space
        row = {}
        for p in members:
            mask = mask_by_repeat(p)
            row[p] = float(spread_by_rank(sigma_by_sort(core[:, mask])
                                          / sigma_by_sort(core[:, ~mask])))
        nulls[target] = row
        withheld[target] = [
            p for p in members
            if disposition(SIGMA_WORST, SIGMA_QUIET, r_space,
                           row[p]) == "unmeasurable"]
    return withheld, spaces, nulls


def signatures(members, withheld):
    """For each member, the set of fixtures on which it withholds."""
    return {p: set(t for t in members if p in withheld[t]) for p in members}


def strict_dominance(members, sigs):
    """Ordered pairs (a, b) where b's signature is a proper subset of a's."""
    return sorted((a, b) for a in members for b in members
                  if a != b and sigs[b] < sigs[a])


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True,
                        help="the Session-49 sensitivity probe's JSON record")
    parser.add_argument("--out", required=True,
                        help="path for the human-readable check report")
    parser.add_argument("--records", default=None,
                        help="optional path for this probe's JSON record")
    args = parser.parse_args(argv)

    c = Checks()
    source, digest = load_source(args.source)

    c.heading("1. Authenticate the record before reading it")
    c.check("the source record is the one Codex audited",
            digest == SOURCE_SHA256, "SHA-256 %s" % digest)
    members = sorted(int(v) for v in source["members"])
    recorded = {int(k): sorted(int(v) for v in vs) for k, vs
                in source["withholding_members_by_fixture"].items()}
    c.check("it carries 32 members and one fixture row for each",
            len(members) == 32 and sorted(recorded) == members,
            "%d members, %d rows" % (len(members), len(recorded)))
    c.check("the members are exactly the divisors of 6,510",
            members == divisors(HALF),
            "6,510 = 2 * 3 * 5 * 7 * 31")

    c.heading("2. Recompute the matrix along an independent path")
    depths = [2.0] * 8 + [1.0] * 56 + [0.5] * 8
    withheld, spaces, nulls = recompute(members, depths)
    mismatched = [t for t in members if sorted(withheld[t]) != recorded[t]]
    c.check("the recomputed withholding table agrees with the record for "
            "every one of the 1,024 cells", not mismatched,
            "%d of 32 fixture rows differ" % len(mismatched))
    recorded_space = {int(k): float(v) for k, v
                      in source["r_space_by_fixture"].items()}
    worst_space = max(abs(spaces[t] - recorded_space[t]) for t in members)
    c.check("and the recomputed R_space_sampled agrees to 1e-12 relative",
            all(np.isclose(spaces[t], recorded_space[t], rtol=1e-12, atol=0.0)
                for t in members),
            "largest absolute difference %.3e" % worst_space)
    c.check("R_space_sampled stays inside strict M on every fixture, so "
            "branch 4 is what decides", max(spaces.values()) <= M_STRICT,
            "R_space in %.6f ... %.6f" % (min(spaces.values()),
                                          max(spaces.values())))

    c.heading("2a. Where the 1,024 decisions actually sit against M = 2.0")
    flat = [nulls[t][p] for t in members for p in members]
    held = [nulls[t][p] for t in members for p in withheld[t]]
    ties = [v for v in flat if v == M_STRICT]
    c.check("every withholding decision clears M by a wide margin, so the "
            "dominance structure is not read off ties",
            min(v - M_STRICT for v in held) > 0.5,
            "%d withheld cells, closest is M + %.6f"
            % (len(held), min(v - M_STRICT for v in held)))
    c.check("but 450 of the 1,024 cells sit EXACTLY at M, and every one of "
            "them is on the passing side",
            len(ties) == 450 and not [v for v in held if v == M_STRICT],
            "branch 4's '>' is strict, so an exact tie passes")
    c.check("so a non-strict branch 4 would produce a different table",
            len(ties) > 0, "%d cells would flip from pass to withhold"
            % len(ties))
    c.note("this fixture family therefore supports claims about clearly "
           "separated values and must NOT be used to argue anything near M")

    c.heading("3. Re-derive the dominance structure without Codex's code")
    sigs = signatures(members, withheld)
    relations = strict_dominance(members, sigs)
    odd = set(p for p in members if p % 2 == 1)
    even = set(members) - odd
    expected = set((1, p) for p in odd - set([1]))
    expected |= set((2, p) for p in even - set([2]))
    c.check("the matrix contains 30 strict pairwise dominance relations",
            len(relations) == 30,
            "%d found, against Codex's 30" % len(relations))
    c.check("they are exactly p=1 over the other 15 odd members and p=2 over "
            "the other 15 even members", set(relations) == expected,
            "no cross-parity dominance")
    c.check("p=1 withholds on exactly the 16 odd-target fixtures",
            sigs[1] == odd, "signature size %d" % len(sigs[1]))
    c.check("p=2 withholds on exactly the 16 even-target fixtures",
            sigs[2] == even, "signature size %d" % len(sigs[2]))
    c.check("p=1 and p=2 are incomparable and their union covers all 32",
            not sigs[1] <= sigs[2] and not sigs[2] <= sigs[1]
            and not (sigs[1] & sigs[2]) and sigs[1] | sigs[2] == set(members),
            "disjoint, 16 + 16")
    c.check("every other odd member's signature is exactly {1, p}",
            all(sigs[p] == set([1, p]) for p in odd - set([1])),
            "15 members, size 2 each")
    c.check("every other even member's signature is exactly {p}",
            all(sigs[p] == set([p]) for p in even - set([2])),
            "15 members, size 1 each")
    c.check("no two members share a signature",
            len(set(frozenset(sigs[p]) for p in members)) == 32,
            "32 distinct signatures")

    c.heading("4. What Session 49 claimed, checked one statement at a time")
    self_hits = [p for p in members if p in withheld[p]]
    never = [p for p in members if not sigs[p]]
    always = [p for p in members if sigs[p] == set(members)]
    c.check("SURVIVES: every member withholds on the fixture built at its own "
            "block length", len(self_hits) == 32, "32 of 32")
    c.check("SURVIVES: no member withholds on every fixture", not always,
            "%d members always withhold" % len(always))
    c.check("SURVIVES: no member withholds on no fixture", not never,
            "%d members never withhold" % len(never))
    c.check("SURVIVES: on the p_t = 2 fixture exactly one member withholds",
            len(withheld[2]) == 1, "the other 31 pass")
    c.check("WITHDRAWN: 'the family has no dominating member' is false on "
            "this very matrix", len(relations) > 0,
            "30 relations, so the Session-49 detail string is withdrawn")
    c.check("the Session-49 check that carried that string tested something "
            "weaker and that weaker thing is true",
            (not never) and (not always) and len(relations) == 30,
            "the body was right; the detail string overreached")

    c.heading("5. The boundary, and what is still open")
    c.check("every fixture was evaluated against all 32 members",
            all(len(nulls[t]) == 32 for t in members) and len(nulls) == 32,
            "32 fixtures x 32 members, none skipped")
    c.note("32 CONSTRUCTED fixtures, each built to be visible to one member; "
           "the dominance structure is a property of that construction")
    c.note("nothing here defeats 'pin one member and disclose it' - distinct "
           "conventions are expected to disagree on member-matched fixtures")
    c.note("the two-member {1, 2} cover is a fact about this constructed set "
           "and is NOT proposed as a real-data diagnostic")

    records = {
        "source_sha256": digest,
        "members": members,
        "recomputed_withholding_by_fixture": {str(t): sorted(withheld[t])
                                              for t in members},
        "recomputed_r_space_by_fixture": spaces,
        "signature_by_member": {str(p): sorted(sigs[p]) for p in members},
        "dominance_relations": [list(pair) for pair in relations],
        "dominance_count": len(relations),
        "cells_exactly_at_M": len(ties),
        "withheld_cells": len(held),
        "closest_withheld_margin_above_M": min(v - M_STRICT for v in held),
        "withdrawn": ["the family has no dominating member", "none dominates"],
        "surviving": [
            "every member withholds on the fixture at its own block length",
            "no member withholds on every fixture",
            "no member withholds on no fixture",
            "the split parameter reaches a decision"],
        "boundary": ("32 constructed fixtures, each built to be visible to "
                     "one member; no real-data claim, and no defeat of the "
                     "pin-one-and-disclose-it reading"),
    }

    text = c.render()
    sys.stdout.write(text)
    io.open(args.out, "w", encoding="utf-8", newline="\n").write(text)
    if args.records:
        io.open(args.records, "w", encoding="utf-8", newline="\n").write(
            json.dumps(records, indent=2, sort_keys=True) + "\n")
    return 1 if c.failed else 0


if __name__ == "__main__":
    sys.exit(main())
