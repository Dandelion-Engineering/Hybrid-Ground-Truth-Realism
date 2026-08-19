"""Evidence for Claude's RC-008 Convergence Decision statement.

Codex's F8-R3 says Draft 34's sole surviving ground for the contiguous split -
that an interleaved split carries a free period whose effect cannot be signed -
is false for the fixed even/odd alternative the review actually examined. This
probe accepts that finding and computes the fact that makes it unnarrowable.

  1. The two rules are the two ENDPOINTS OF ONE FAMILY. Partition the 13,020
     retained samples into two equal halves by block-interleaving with block
     length p: sample i joins half A when (i // p) is even. Equal halves need
     p to divide 6,510, and 6,510 = 2*3*5*7*31 has exactly 32 divisors. p =
     6,510 IS the midpoint-contiguous rule and p = 1 IS the even/odd rule. So
     each is one fixed, parameterless member of a 32-member family, and "the
     alternative carries a free parameter" is a statement about which rule was
     named rather than about either partition. It cannot select between them
     in either direction.

  2. The parameter is DECISION-LIVE ACROSS THE FAMILY, not only at its two
     endpoints. On the parity construction Draft 34 already publishes,
     R_space_sampled is one number for all 32 members and R_null_sampled takes
     exactly two: 16 members reach `passes` and 16 reach `unmeasurable` on
     byte-identical data.

  3. What F8-R3 does NOT reach: Draft 34's exact branch reach. Every member of
     the family is a partition of the identical retained core, so the split is
     still invisible to R_space_sampled, and the 9/6/57 truth table recomputes
     unchanged.

The 16/16 count is a property of a fixture built to be parity-sensitive. It
shows the pinned parameter has a decision destination across the family; it
claims nothing about what a real recording would do, and no direction is
claimed for any member.

Nothing here reads the archive, the network, or any project record. Every
construction is synthetic and built from numpy directly.

Usage:

    ./venv/Scripts/python.exe agents/Claude/tools/probe_rc008_convergence.py \
        --out <path> [--records <path>]
"""

import argparse
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


class Checks(object):
    """Collect pass/fail lines and print them in the project's console form."""

    def __init__(self):
        self.lines = []
        self.failed = 0

    def heading(self, text):
        self.lines.append("")
        self.lines.append(text)

    def check(self, name, ok, detail=""):
        """Record one check; `detail` is printed either way."""
        if not ok:
            self.failed += 1
        self.lines.append("%s  %s%s" % ("PASS" if ok else "FAIL", name,
                                        ("  [%s]" % detail) if detail else ""))
        return ok

    def render(self):
        body = "\n".join(self.lines)
        total = sum(1 for line in self.lines
                    if line.startswith("PASS") or line.startswith("FAIL"))
        return "%s\n\nSummary\n%d checks, %d failed\n" % (body, total,
                                                          self.failed)


def sigma_hat(x, axis=-1):
    """MAD scale estimate along `axis`, the section 19.3 estimator."""
    med = np.median(x, axis=axis, keepdims=True)
    return np.median(np.abs(x - med), axis=axis) / MAD_SCALE


def nearest_rank(values, q):
    """Nearest-rank percentile: rank ceil(q * n) over ascending values."""
    ordered = np.sort(np.asarray(values, dtype=float))
    rank = int(np.ceil(q * ordered.size))
    return ordered[max(rank, 1) - 1]


def spread(values):
    """The p90/p10 nearest-rank ratio section 19.4 fixes."""
    return nearest_rank(values, 0.90) / nearest_rank(values, 0.10)


def disposition(sigma_worst, sigma_quiet, r_space, r_null, n_tol=N_STRICT,
                m_tol=M_STRICT, floor=FLOOR):
    """Section 19.6's four ordered branches; the first that fires wins."""
    if sigma_worst > n_tol:
        return "fails-level-loud"
    if sigma_quiet < floor:
        return "fails-level-quiet"
    if r_space > m_tol:
        return ("fails-homogeneity-resolved" if r_space > r_null
                else "fails-homogeneity-resolution-limited")
    if r_null > m_tol:
        return "unmeasurable"
    return "passes"


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


def block_mask(p, n=RETAINED):
    """Half A of the block-interleaved split at block length p.

    Sample i joins half A when (i // p) is even. This is a function of the
    index range and p alone: it never looks at the data.
    """
    return (np.arange(n) // p) % 2 == 0


def parity_core(ratios, base):
    """Draft 34's 72 x 13,020 parity core, reproduced exactly.

    ``ratios[c]`` is channel c's even-to-odd scale ratio and ``base[c]`` scales
    the whole row. Magnitudes are constant inside a parity class and the signs
    are balanced, so every MAD is exact rather than sampled.
    """
    t = np.arange(RETAINED)
    sign = np.where((t % 4 == 0) | (t % 4 == 3), 1.0, -1.0)
    rows = []
    for ratio, scale in zip(ratios, base):
        even = float(ratio) if ratio >= 1 else 1.0
        odd = 1.0 if ratio >= 1 else 1.0 / float(ratio)
        rows.append(scale * np.where(t % 2 == 0, even, odd) * sign)
    return np.array(rows)


def family(c, records):
    """1. Both named split rules are members of one 32-member family."""
    c.heading("1. The two rules are endpoints of one block-interleaved family")
    ds = divisors(HALF)
    c.check("equal halves require p to divide 6,510, which has 32 divisors",
            len(ds) == 32 and ds[0] == 1 and ds[-1] == HALF,
            "p in %d ... %d, %d members" % (ds[0], ds[-1], len(ds)))
    c.check("6,510 factors as 2 * 3 * 5 * 7 * 31, so the count is 2**5",
            2 * 3 * 5 * 7 * 31 == HALF and 2 ** 5 == len(ds),
            "2**5 = %d" % 2 ** 5)

    c.check("p = 6,510 IS the midpoint-contiguous rule",
            np.array_equal(np.flatnonzero(block_mask(HALF)),
                           np.arange(HALF)),
            "half A is exactly indices 0 ... 6,509")
    c.check("p = 1 IS the canonical even/odd rule",
            np.array_equal(np.flatnonzero(block_mask(1)),
                           np.arange(0, RETAINED, 2)),
            "half A is exactly the even indices")
    c.check("every member splits the core into two halves of 6,510",
            all(int(block_mask(p).sum()) == HALF for p in ds),
            "32 of 32 members")

    # The point of F8-R3, made structurally: a member's mask is a function of
    # p and the retained length. Two different cores give the same mask, so no
    # member of the family consumes candidate data in order to be defined.
    loud = parity_core([2.0] * 72, [1.0] * 72)
    quiet = parity_core([0.5] * 72, [7.0] * 72)
    c.check("a member's mask is fixed before any data: same p, same mask",
            all(np.array_equal(block_mask(p, loud.shape[1]),
                               block_mask(p, quiet.shape[1])) for p in ds),
            "no member reads the core to be defined")
    c.check("so 'the alternative carries a free parameter' names 32 fixed "
            "rules, not one",
            len(ds) == 32,
            "the free parameter belongs to the family, not to either endpoint")
    records["family"] = {"n_members": len(ds), "divisors": ds,
                         "contiguous_p": HALF, "even_odd_p": 1}
    return ds


def liveness(c, records, ds):
    """2. The pinned parameter is decision-live across the whole family."""
    c.heading("2. The parameter's decision destination across all 32 members")
    ratios = [2.0] * 8 + [1.0] * 56 + [0.5] * 8
    core = parity_core(ratios, [1.0] * 72)

    r_space = spread(sigma_hat(core))
    c.check("Draft 34's parity fixture reproduces at R_space_sampled = 1.5",
            abs(r_space - 1.5) < 1e-12, "R_space = %.12f" % r_space)

    nulls = {}
    partitions_agree = True
    for p in ds:
        mask = block_mask(p)
        a, b = core[:, mask], core[:, ~mask]
        nulls[p] = float(spread(sigma_hat(a) / sigma_hat(b)))
        rejoined = np.concatenate([a, b], axis=1)
        if not np.array_equal(np.sort(rejoined, axis=1),
                              np.sort(core, axis=1)):
            partitions_agree = False

    # A NaN would be counted as a pass by the `> M` comparison, which is
    # exactly how the count could look clean while meaning nothing.
    finite = [p for p in ds if np.isfinite(nulls[p])]
    c.check("every member's R_null_sampled is finite on this fixture",
            len(finite) == len(ds),
            "%d of %d finite, so the counts below are not a NaN artifact"
            % (len(finite), len(ds)))

    values = sorted(set(round(v, 12) for v in nulls.values()))
    c.check("R_null_sampled takes exactly two values across the family",
            values == [1.0, 4.0], "values = %s" % values)

    withheld = [p for p in ds if nulls[p] > M_STRICT]
    passing = [p for p in ds if nulls[p] <= M_STRICT]
    c.check("16 members reach `unmeasurable` on byte-identical data",
            len(withheld) == 16, "p = %s" % withheld)
    c.check("16 members reach `passes` on the same data",
            len(passing) == 16, "p = %s" % passing)
    c.check("the family splits on the PARITY OF p on this fixture",
            all(p % 2 == 1 for p in withheld) and all(p % 2 == 0
                                                      for p in passing),
            "odd p withholds, even p passes")

    d_cont = disposition(6.0, 5.0, r_space, nulls[HALF])
    d_even = disposition(6.0, 5.0, r_space, nulls[1])
    c.check("the pinned rule p = 6,510 is one of the 16 that pass",
            d_cont == "passes" and HALF in passing, d_cont)
    c.check("the reviewed rule p = 1 is one of the 16 that withhold",
            d_even == "unmeasurable" and 1 in withheld, d_even)
    c.check("so the choice of member decides the disposition, 16 ways each",
            d_cont != d_even, "%s vs %s" % (d_cont, d_even))
    records["liveness"] = {"r_space": float(r_space),
                           "r_null_values": values,
                           "withheld_p": withheld, "passing_p": passing,
                           "contiguous_disposition": d_cont,
                           "even_odd_disposition": d_even,
                           "n_finite": len(finite)}
    return core, nulls


def unreached(c, records, ds, core):
    """3. What F8-R3 does not reach: Draft 34's exact branch reach."""
    c.heading("3. What the finding does not reach")

    # Every member is a partition of the identical core, so R_space_sampled is
    # one number for the whole family, not 32 of them. This is the fact Draft
    # 34's reach bound rests on, and F8-R3 leaves it standing.
    base = spread(sigma_hat(core))
    agree = True
    spaces_seen = []
    for p in ds:
        mask = block_mask(p)
        rejoined = np.concatenate([core[:, mask], core[:, ~mask]], axis=1)
        if not np.array_equal(np.sort(rejoined, axis=1),
                              np.sort(core, axis=1)):
            agree = False
        # Recomputed from the member's own rejoined halves, not from `core`,
        # so this compares 32 independently computed values against the base.
        spaces_seen.append(float(spread(sigma_hat(rejoined))))
    c.check("all 32 members are partitions of the identical retained core",
            agree, "checked by sorting, not asserted")
    c.check("so R_space_sampled recomputes to one value from all 32 members",
            len(spaces_seen) == 32
            and max(abs(v - base) for v in spaces_seen) == 0.0,
            "R_space = %.12f, max deviation %.3e over 32 members"
            % (base, max(abs(v - base) for v in spaces_seen)))

    # Draft 34's truth table, recomputed here rather than cited.
    worsts, quiets, spaces = [6.0, 12.0], [1.0, 5.0], [1.5, 3.0]
    lows, highs = [0.5, 1.0, 1.9], [2.1, 4.0, np.inf]
    moved = relabelled = unchanged = 0
    illegal = []
    for w in worsts:
        for q in quiets:
            for s in spaces:
                for lo in lows:
                    for hi in highs:
                        a = disposition(w, q, s, lo)
                        b = disposition(w, q, s, hi)
                        if a == b:
                            unchanged += 1
                        elif tuple(sorted((a, b))) == ("passes",
                                                       "unmeasurable"):
                            moved += 1
                        elif tuple(sorted((a, b))) == (
                                "fails-homogeneity-resolution-limited",
                                "fails-homogeneity-resolved"):
                            relabelled += 1
                        else:
                            illegal.append((a, b))
    c.check("Draft 34's reach recomputes unchanged: 9 moved",
            moved == 9, "%d moved" % moved)
    c.check("6 relabelled and 57 untouched",
            relabelled == 6 and unchanged == 57,
            "%d relabelled, %d untouched" % (relabelled, unchanged))
    c.check("and no other transition exists", not illegal,
            "%d illegal transitions" % len(illegal))
    c.check("so a change of member can never cross the failure boundary",
            not illegal and moved == 9,
            "the reach bound survives F8-R3; only its RATIONALE fell")
    records["unreached"] = {"moved": moved, "relabelled": relabelled,
                            "unchanged": unchanged, "illegal": len(illegal),
                            "r_space_family_constant": float(base)}


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", required=True,
                        help="path for the human-readable check report")
    parser.add_argument("--records", default=None,
                        help="optional path for the JSON record")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    c = Checks()
    records = {}
    ds = family(c, records)
    core, _ = liveness(c, records, ds)
    unreached(c, records, ds, core)

    text = c.render()
    sys.stdout.write(text)
    io.open(args.out, "w", encoding="utf-8", newline="\n").write(text)
    if args.records:
        io.open(args.records, "w", encoding="utf-8", newline="\n").write(
            json.dumps(records, indent=2, sort_keys=True) + "\n")
    return 1 if c.failed else 0


if __name__ == "__main__":
    sys.exit(main())
