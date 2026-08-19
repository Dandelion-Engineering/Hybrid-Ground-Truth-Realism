"""The split-half ratio has an undefined case section 19.6 does not cover.

Draft 34's section 19.6 closes its degenerate-percentile paragraph with:

    "The half-window ratio `r_c(k)` is handled identically: a channel with a
     zero denominator contributes `+inf`, and `R_null_sampled` reaches `+inf`
     only if enough such channels reach the p90 rank. No undefined ratio
     enters a comparison."

The sentence before it fixes what "degenerate" means: `sigma_hat_c` is finite
whenever the retained samples are, "so the only live degenerate case is an
exact zero - a channel literally constant across the retained core."

That degenerate condition is the right one for `R_space_sampled`, which reads
`sigma_hat_c` over the whole retained core. It is the WRONG one for `r_c(k)`,
which reads the two halves. A channel can vary across the core - so it is not
degenerate by the stated test - while being constant WITHIN EACH HALF. Then
both `sigma_hat_c^A` and `sigma_hat_c^B` are exactly zero and the ratio is
0/0, which is NaN rather than `+inf`. The final sentence is false for that
case, and the case is reachable.

Three things this probe establishes, each on a constructed channel:

  1. the undefined case exists and is NOT the documented zero-denominator
     case: whole-core `sigma_hat_c` is nonzero, so section 19.6's own
     degenerate test does not catch it, and the ratio is NaN, not `+inf`;
  2. it is SPLIT-DEPENDENT, which is what puts it in Part B rather than Part
     A, and the dependence is total rather than marginal: on one mid-window
     step channel the ratio is undefined under exactly the 16 EVEN members and
     exactly 1.0 - the best value the statistic can take - under all 16 odd
     ones. Nothing in between occurs. The arithmetic behind that is checked
     rather than asserted: 6,510 carries exactly one factor of 2, so a member
     is even exactly when 6,510/p is odd, and an odd block count leaves each
     half holding a strict majority of one step value, which drives both MADs
     to zero. Whether a candidate has an undefined resolution diagnostic at
     all is therefore decided by the split rule that has not been chosen;
  3. its unhandled behaviour is PERMISSIVE in both regimes. With fewer than
     eight undefined channels of 72 the NaNs sort above the p90 rank and never
     reach the comparison; with eight or more `R_null_sampled` is itself NaN,
     `NaN > M` is False, branch 4 does not fire, and the disposition is
     `passes`. A resolution diagnostic that is undefined reads as a candidate
     that does not need one.

The documented `+inf` case is checked too, and it behaves exactly as written:
eight such channels of 72 do drive `R_null_sampled` to `+inf` and branch 4
does fire. That half of the paragraph is sound and is not disturbed here.

A fourth point is smaller but is a specification gap of the same kind: with a
NaN in the set, "sort the n band channels' values ascending" does not
determine an answer. NaN is unordered, so the result depends on the sorting
implementation - `numpy.sort` sinks NaN to the end, while Python's own
`sorted` returns different orders for different permutations of the SAME
multiset. Section 19.4 names the nearest-rank construction but not the
convention that makes it well defined here.

BOUNDARY. These are constructed channels. Nothing here says how often a
channel constant within a half occurs in a real recording, and no such channel
has been observed in this project - no candidate sample has ever been read for
noise. The claim is that the specification does not define the case, which is
a property of the specification and not of any recording. This is untested
design input for Part B, not a proposal and not a repair.

Nothing here reads the archive, the network, or any project record.

Usage:

    ./venv/Scripts/python.exe \\
        agents/Claude/tools/probe_null_ratio_undefined.py \\
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
BAND_CHANNELS = 72

# Section 19.4's nearest-rank ranks at n = 72, spelled out in section 19.4 of
# the frozen draft and restated here rather than imported.
P10_RANK = 8
P90_RANK = 65

# Admissible level values, so that branches 1 and 2 cannot fire and the
# question is decided at branches 3 and 4. Same device Session 49 used.
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


def sigma_hat(x):
    """Section 19.3's MAD scale estimate over the last axis."""
    x = np.asarray(x, dtype=float)
    med = np.median(x, axis=-1, keepdims=True)
    return np.median(np.abs(x - med), axis=-1) / MAD_SCALE


def divisors(n):
    """Every positive divisor of n, ascending - the split family's members."""
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


def ratio_under(channel, p):
    """One channel's `r_c(k)` under member p, with no guarding at all.

    Written deliberately without a finiteness guard, because the question is
    what section 19.6 as written produces, not what a careful implementation
    would produce.
    """
    mask = block_mask(p)
    with np.errstate(invalid="ignore", divide="ignore"):
        return float(sigma_hat(channel[mask]) / sigma_hat(channel[~mask]))


def step_channel(amplitude=1.0):
    """Constant within each contiguous half, but not across the core.

    Not degenerate by section 19.6's test - its whole-core `sigma_hat_c` is
    nonzero - yet both contiguous halves have exactly zero MAD.
    """
    x = np.full(RETAINED, -float(amplitude))
    x[HALF:] = float(amplitude)
    return x


def alternating_channel(amplitude=1.0):
    """A well-behaved channel: nonzero MAD on the core and on every half."""
    pattern = np.tile(np.array([1.0, -1.0, -1.0, 1.0]), RETAINED // 4)
    return float(amplitude) * pattern


def dead_half_channel(amplitude=1.0):
    """Varies on contiguous half A and is constant on half B.

    This is section 19.6's documented case: a zero denominator with a nonzero
    numerator, which contributes `+inf`.
    """
    x = np.zeros(RETAINED)
    x[:HALF] = float(amplitude) * np.tile(np.array([1.0, -1.0]), HALF // 2)
    return x


def majority_share(x):
    """Largest fraction of `x` taking any one value.

    Deliberately not "the fraction equal to the first sample": on this channel
    the half that starts with one step value can hold a majority of the other,
    and the median follows the majority rather than the first sample.
    """
    _, counts = np.unique(np.asarray(x), return_counts=True)
    return float(counts.max()) / float(np.asarray(x).size)


def nearest_rank(values, rank):
    """The one-based `rank`-th value of `values` sorted ascending."""
    return float(np.sort(np.asarray(values, dtype=float))[rank - 1])


def spread(values):
    """Section 19.4's p90/p10 nearest-rank ratio at n = 72."""
    with np.errstate(invalid="ignore", divide="ignore"):
        return nearest_rank(values, P90_RANK) / nearest_rank(values, P10_RANK)


def disposition(r_space, r_null):
    """Section 19.6's four ordered branches; the first that fires wins."""
    if SIGMA_WORST > N_STRICT:
        return "fails-level-loud"
    if SIGMA_QUIET < FLOOR:
        return "fails-level-quiet"
    if r_space > M_STRICT:
        return ("fails-homogeneity-resolved" if r_space > r_null
                else "fails-homogeneity-resolution-limited")
    if r_null > M_STRICT:
        return "unmeasurable"
    return "passes"


def band_with(k, odd_channel_ratio):
    """A 72-channel ratio set: k copies of `odd_channel_ratio`, rest 1.0."""
    return [1.0] * (BAND_CHANNELS - k) + [odd_channel_ratio] * k


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

    c.heading("1. The undefined case exists and is not the documented one")
    step = step_channel()
    core_sigma = float(sigma_hat(step))
    c.check("the step channel's whole-core sigma_hat_c is nonzero, so section "
            "19.6's own degenerate test does not catch it",
            core_sigma > 0.0, "sigma_hat_c = %.6f" % core_sigma)
    half_a = float(sigma_hat(step[block_mask(HALF)]))
    half_b = float(sigma_hat(step[~block_mask(HALF)]))
    c.check("yet under p = 6,510 both halves have exactly zero MAD",
            half_a == 0.0 and half_b == 0.0,
            "sigma_hat^A = %.1f, sigma_hat^B = %.1f" % (half_a, half_b))
    contiguous = ratio_under(step, HALF)
    c.check("so the ratio is 0/0, which is NaN and not +inf",
            np.isnan(contiguous), "r_c = %r" % contiguous)

    c.heading("2. And it is split-dependent, which is what makes it Part B")
    interleaved = ratio_under(step, 1)
    c.check("the same channel under p = 1 gives a finite ratio of exactly 1.0",
            interleaved == 1.0, "r_c = %.6f" % interleaved)
    members = divisors(HALF)
    ratios = dict((p, ratio_under(step, p)) for p in members)
    undefined_members = [p for p in members if np.isnan(ratios[p])]
    finite_members = [p for p in members if not np.isnan(ratios[p])]
    c.check("exactly 16 of the 32 members are undefined on this one channel",
            len(undefined_members) == 16, "and 16 are finite")
    c.check("they are exactly the 16 EVEN members",
            undefined_members == [p for p in members if p % 2 == 0],
            "p = %d ... %d" % (undefined_members[0], undefined_members[-1]))
    c.check("and every one of the 16 odd members gives exactly 1.0, the best "
            "value the statistic can take",
            all(ratios[p] == 1.0 for p in finite_members)
            and finite_members == [p for p in members if p % 2 == 1],
            "no intermediate value occurs")

    c.heading("2a. Why, checked rather than told")
    c.check("6,510 carries exactly one factor of 2, so a member is even "
            "exactly when 6,510/p is odd",
            all((p % 2 == 0) == ((HALF // p) % 2 == 1) for p in members),
            "true for all 32 members")
    lopsided = [1.0] * 7 + [0.0] * 3
    c.check("a MAD is exactly zero whenever a strict majority of the samples "
            "share the median value", float(sigma_hat(lopsided)) == 0.0,
            "7 of 10 equal gives MAD 0")
    majorities = []
    for p in undefined_members:
        mask = block_mask(p)
        majorities.append(min(majority_share(step[mask]),
                              majority_share(step[~mask])))
    c.check("under every even member both halves hold a strict majority of "
            "one step value, which is what drives both MADs to zero",
            min(majorities) > 0.5,
            "smallest majority share %.6f" % min(majorities))
    c.note("whether a candidate has an undefined resolution diagnostic at all "
           "is therefore decided by the split rule that is not yet chosen: on "
           "this channel half the family is undefined and half is exactly 1.0")

    c.heading("3. The documented +inf case behaves exactly as documented")
    dead = dead_half_channel()
    dead_ratio = ratio_under(dead, HALF)
    c.check("a channel varying on half A and constant on half B gives +inf",
            np.isinf(dead_ratio) and dead_ratio > 0, "r_c = %r" % dead_ratio)
    c.check("with 8 of 72 such channels R_null_sampled is +inf and branch 4 "
            "fires", np.isinf(spread(band_with(8, dead_ratio)))
            and disposition(1.0, spread(band_with(8, dead_ratio)))
            == "unmeasurable",
            "disposition %s" % disposition(1.0,
                                           spread(band_with(8, dead_ratio))))
    c.check("with 7 of 72 it does not, which is what 'only if enough such "
            "channels reach the p90 rank' says",
            spread(band_with(7, dead_ratio)) == 1.0
            and disposition(1.0, spread(band_with(7, dead_ratio)))
            == "passes",
            "p90 sits at rank %d of 72" % P90_RANK)

    c.heading("4. The undefined case is permissive in BOTH regimes")
    few = spread(band_with(7, contiguous))
    c.check("with 7 of 72 undefined channels the NaNs sort above the p90 rank "
            "and never reach the comparison",
            few == 1.0 and disposition(1.0, few) == "passes",
            "R_null_sampled = %.6f, disposition %s"
            % (few, disposition(1.0, few)))
    many = spread(band_with(8, contiguous))
    c.check("with 8 of 72 R_null_sampled is itself NaN", np.isnan(many),
            "R_null_sampled = %r" % many)
    c.check("and NaN > M is False, so branch 4 does not fire",
            not (many > M_STRICT), "the comparison is False, not an error")
    c.check("so the disposition of a wholly undefined resolution diagnostic "
            "is `passes`", disposition(1.0, many) == "passes",
            "disposition %s" % disposition(1.0, many))
    c.check("the contrast is exact: 8 undefined channels pass where 8 "
            "zero-denominator channels are unmeasurable",
            disposition(1.0, many) == "passes"
            and disposition(1.0, spread(band_with(8, dead_ratio)))
            == "unmeasurable",
            "same count, same rank, opposite disposition")

    c.heading("5. 'Sort ascending' does not determine an answer with a NaN")
    mixed = band_with(8, contiguous)
    numpy_p90 = nearest_rank(mixed, P90_RANK)
    c.check("numpy.sort sinks NaN to the end, a convention section 19.4 does "
            "not state", np.isnan(numpy_p90), "rank 65 of 72 is %r"
            % numpy_p90)
    front = sorted([contiguous] * 8 + [1.0] * (BAND_CHANNELS - 8))[P90_RANK - 1]
    back = sorted([1.0] * (BAND_CHANNELS - 8) + [contiguous] * 8)[P90_RANK - 1]
    c.check("Python's own sorted returns different rank-65 values for two "
            "permutations of the SAME multiset",
            (np.isnan(front) != np.isnan(back)) or front != back,
            "NaN-first gives %r, NaN-last gives %r" % (front, back))
    c.note("NaN is unordered, so the nearest-rank rule needs a stated "
           "convention before it is implementable at all")

    c.heading("6. Boundary")
    c.note("constructed channels only; no candidate sample has ever been read "
           "for noise, and no frequency claim is made about real recordings")
    c.note("the claim is that the specification does not define the case, "
           "which is a property of the specification")
    c.note("this binds every Part B reading, including one that publishes "
           "R_null_sampled without letting it decide")

    records["core_sigma_step_channel"] = core_sigma
    records["ratio_contiguous"] = "nan" if np.isnan(contiguous) else contiguous
    records["ratio_interleaved"] = interleaved
    records["undefined_members"] = undefined_members
    records["finite_members"] = finite_members
    records["smallest_half_majority_share"] = min(majorities)
    records["ratio_dead_half"] = "inf" if np.isinf(dead_ratio) else dead_ratio
    records["dispositions"] = {
        "7_undefined_of_72": disposition(1.0, few),
        "8_undefined_of_72": disposition(1.0, many),
        "7_zero_denominator_of_72":
            disposition(1.0, spread(band_with(7, dead_ratio))),
        "8_zero_denominator_of_72":
            disposition(1.0, spread(band_with(8, dead_ratio))),
    }
    records["p10_rank"] = P10_RANK
    records["p90_rank"] = P90_RANK
    records["boundary"] = ("constructed channels; the finding is that section "
                           "19.6 does not define the 0/0 case, that the case "
                           "is split-dependent, and that its unhandled "
                           "behaviour is permissive")

    text = c.render()
    sys.stdout.write(text)
    io.open(args.out, "w", encoding="utf-8", newline="\n").write(text)
    if args.records:
        io.open(args.records, "w", encoding="utf-8", newline="\n").write(
            json.dumps(records, indent=2, sort_keys=True) + "\n")
    return 1 if c.failed else 0


if __name__ == "__main__":
    sys.exit(main())
