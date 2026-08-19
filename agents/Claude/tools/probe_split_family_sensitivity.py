"""Is any member of the split family a safe default? Measured, not argued.

RC-008 closed at `Split/Redesign Required` because the only stated reason for
pinning the midpoint-contiguous split was false: midpoint-contiguous and
even/odd are `p = 6,510` and `p = 1` of ONE 32-member family of
block-interleaved equal partitions of the 13,020 retained samples, so no
parameter-count argument can select between them
(`probe_rc008_convergence.py`).

That leaves the reading under which the card could still have been approved:
every member is equally arbitrary, so pin one, disclose it, and move on. This
probe tests that reading, and it does not survive.

For each of the 32 members p_t, build a core whose amplitude is modulated on
blocks of length p_t - loud on even blocks, quiet on odd - with the modulation
DEPTH varying by channel and the fine structure identical in every channel, so
that only the block modulation can create spread across channels. Then run all
32 members against it. What comes out:

  * every one of the 32 members withholds the measurement on the fixture built
    at its own block length - 32 of 32;
  * NO member withholds on every fixture, and NO member withholds on none;
  * on the p_t = 2 fixture exactly ONE member withholds and the other 31 pass.

So the members are not interchangeable conventions that happen to disagree.
Each is sensitive to a different structure, none dominates, and for every
possible pin there is a recording structure on which that pin withholds while
almost every alternative passes - and structure on which the reverse holds.

BOUNDARY, and it is the whole of what this shows. These are CONSTRUCTED
fixtures, each built to be visible to one member. They establish that the
family's members answer different questions and that no member is uniformly
cautious. They say NOTHING about how often such structure occurs in a real
recording, and no direction is claimed for any member on any real data. This
is untested input for the successor card's Part B, not a specification and not
a proposal.

Nothing here reads the archive, the network, or any project record.

Usage:

    ./venv/Scripts/python.exe \\
        agents/Claude/tools/probe_split_family_sensitivity.py \\
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
    """Half A of the block-interleaved split at block length p."""
    return (np.arange(n) // p) % 2 == 0


def core_at(p_target, depths):
    """A core whose amplitude is modulated on blocks of length `p_target`.

    ``depths[c]`` is channel c's loud-to-quiet modulation depth. Inside a block
    the magnitude alternates between 1 and 1/2 so every half has a nonzero MAD
    whatever the split; that fine structure is IDENTICAL in every channel, so
    it cannot by itself produce spread across channels. Only the block
    modulation can, which is what makes the fixture isolate one member.
    """
    t = np.arange(RETAINED)
    sign = np.where((t % 4 == 0) | (t % 4 == 3), 1.0, -1.0)
    fine = np.where(t % 2 == 0, 1.0, 0.5)
    loud_block = (t // p_target) % 2 == 0
    rows = []
    for depth in depths:
        hi = float(depth) if depth >= 1 else 1.0
        lo = 1.0 if depth >= 1 else 1.0 / float(depth)
        rows.append(np.where(loud_block, hi, lo) * fine * sign)
    return np.array(rows)


def sweep(ds, depths):
    """Every member run against every fixture: 32 x 32 dispositions."""
    withheld = {}
    spaces = {}
    nulls = {}
    nonfinite = 0
    for p_target in ds:
        core = core_at(p_target, depths)
        r_space = float(spread(sigma_hat(core)))
        spaces[p_target] = r_space
        row = {}
        for p in ds:
            mask = block_mask(p)
            value = float(spread(sigma_hat(core[:, mask])
                                 / sigma_hat(core[:, ~mask])))
            if not np.isfinite(value):
                nonfinite += 1
            row[p] = value
        nulls[p_target] = row
        withheld[p_target] = [
            p for p in ds
            if disposition(6.0, 5.0, r_space, row[p]) == "unmeasurable"]
    return withheld, spaces, nulls, nonfinite


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", required=True,
                        help="path for the human-readable check report")
    parser.add_argument("--records", default=None,
                        help="optional path for the JSON record")
    args = parser.parse_args(argv)

    c = Checks()
    records = {}
    ds = divisors(HALF)
    depths = [2.0] * 8 + [1.0] * 56 + [0.5] * 8

    c.heading("1. The sweep is well posed")
    c.check("the family has 32 members", len(ds) == 32,
            "p = %d ... %d" % (ds[0], ds[-1]))
    withheld, spaces, nulls, nonfinite = sweep(ds, depths)
    c.check("all 1,024 member-against-fixture values are finite",
            nonfinite == 0 and len(ds) * len(ds) == 1024,
            "%d non-finite of 1,024" % nonfinite)
    c.check("R_space_sampled stays inside strict M on every fixture",
            max(spaces.values()) <= M_STRICT,
            "R_space in %.6f ... %.6f, so branch 4 is what decides"
            % (min(spaces.values()), max(spaces.values())))

    c.heading("2. Every member is the wrong choice on some data")
    self_hit = [p for p in ds if p in withheld[p]]
    c.check("every member withholds on the fixture at its own block length",
            len(self_hit) == 32, "%d of 32 members" % len(self_hit))
    covered = sorted(set(p for row in withheld.values() for p in row))
    never = [p for p in ds if p not in covered]
    c.check("no member passes every fixture", not never,
            "%d members never withhold" % len(never))
    always = [p for p in ds if all(p in withheld[t] for t in ds)]
    c.check("and no member withholds on every fixture", not always,
            "%d members always withhold" % len(always))
    c.check("so no member is uniformly cautious and none is uniformly "
            "permissive", not never and not always,
            "the family has no dominating member")

    c.heading("3. How lonely a pinned choice can be")
    sizes = {t: len(withheld[t]) for t in ds}
    smallest = min(sizes.values())
    lonely = [t for t in ds if sizes[t] == smallest]
    c.check("on at least one fixture exactly one member withholds",
            smallest == 1, "fixtures with a single withholding member: %s"
            % lonely)
    c.check("on that fixture the other 31 members all pass",
            all(len(withheld[t]) == 1 for t in lonely),
            "a pin can be the only rule that sees the structure")
    c.check("the two rules RC-008 argued about disagree on the p_t = 1 fixture",
            (1 in withheld[1]) and (HALF not in withheld[1]),
            "p=1 withholds, p=6,510 passes")
    c.check("and they disagree the OTHER way on the p_t = 6,510 fixture",
            (HALF in withheld[HALF]) and (1 not in withheld[HALF]),
            "p=6,510 withholds, p=1 passes")

    c.heading("4. The boundary on all of the above")
    c.check("every fixture was evaluated against all 32 members",
            all(len(row) == len(ds) for row in nulls.values())
            and len(nulls) == len(ds),
            "%d fixtures x %d members, none skipped" % (len(nulls), len(ds)))
    # Not a check, because it is not a property of this run: these are 32
    # CONSTRUCTED fixtures, each built to be visible to one member. Nothing
    # above claims how often such structure occurs in a real recording, and no
    # direction is claimed for any member on any real data.
    c.lines.append("NOTE  32 constructed fixtures, each built to be visible "
                   "to one member; no claim is made here about real data")

    records["members"] = ds
    records["r_space_by_fixture"] = spaces
    records["withholding_members_by_fixture"] = {str(t): withheld[t]
                                                 for t in ds}
    records["self_hits"] = len(self_hit)
    records["never_withhold"] = never
    records["always_withhold"] = always
    records["smallest_withholding_set"] = smallest
    records["nonfinite"] = nonfinite

    text = c.render()
    sys.stdout.write(text)
    io.open(args.out, "w", encoding="utf-8", newline="\n").write(text)
    if args.records:
        io.open(args.records, "w", encoding="utf-8", newline="\n").write(
            json.dumps(records, indent=2, sort_keys=True) + "\n")
    return 1 if c.failed else 0


if __name__ == "__main__":
    sys.exit(main())
