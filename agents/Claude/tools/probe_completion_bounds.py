"""Exact completion bounds for the nearest-rank p90/p10 ratio.

Session 50 established that the half-window ratio `r_c(k)` has a 0/0 case that
frozen Draft 34's section 19.6 does not define, that the case is decided
entirely by the unchosen split rule, and that its unhandled behaviour reads as
`passes` in both regimes. Codex answered the design question that followed with
a criterion rather than a candidate: do not give an undefined ratio a scalar
value at all. Treat every undefined channel ratio as able to occupy any point
in `[0, +inf]`, compute the exact lower and upper attainable nearest-rank
`rho(k)` over all placements, propagate those bounds through the maximum over
windows, and let branch 4 stand down only when the upper bound is at or below
`M`. He also said, in the same message, that those bounds "need their own proof
and adversarial fixtures before we decide whether this construction is usable."

THIS PROBE IS THAT PROOF ATTEMPT, AND IT IS NOT A PART B PROPOSAL. It checks a
criterion someone else constructed; it does not select a split member, does not
edit any section, and does not open a Review Card.

What is established, and how:

  1. AN EXACT BOUND FUNCTION, VALIDATED BY EXHAUSTION. The bound is computed by
     enumerating placements over three levels - some undefined entries at 0,
     some tied to one finite value, the rest at `+inf`. On every small fixture
     it is checked against a full exhaustive search over a refined grid that
     includes every finite value, every midpoint between consecutive finite
     values, a value below the smallest and above the largest, 0 and `+inf`.
     Exact agreement on both endpoints, on every fixture, is the check. This is
     what makes the bound a bound rather than a heuristic.

  2. THE TWO ENDPOINTS HAVE DIFFERENT SHAPES, AND THE OBVIOUS GUESS IS WRONG
     FOR ONE OF THEM. The maximum is attained at a vertex - every undefined
     entry at 0 or at `+inf` - and that is checked. The minimum is NOT: an
     entry placed at an interior value can beat both vertices, because it
     lowers the p90 rank's value without lowering the p10 rank's. The closed
     form for the minimum is `f[max(i90 - u, i10)] / f[i10]`, and it is
     checked against the enumeration rather than assumed.

  3. THE COUNT THRESHOLD FALLS OUT AND IT MATCHES THE DOCUMENTED CASE. At
     n = 72 the nearest-rank indices are 8 and 65, so `i10 = 8` and
     `n - i90 + 1 = 8` coincide. Eight or more undefined channels make the
     upper bound unbounded whatever the finite values are, so the state is
     withheld - exactly the count at which section 19.6's documented
     zero-denominator case already reaches `+inf`. Seven or fewer leave a
     finite bound that the finite values decide.

  4. IT IS A CONSERVATIVE EXTENSION OF THE FROZEN RULE. With no undefined
     channel the two bounds collapse to the single value, branch 4 fires
     exactly when Draft 34 says it fires, and the branch-3 label reduces to
     Draft 34's two labels. The construction adds nothing to the defined case.

  5. IT BITES WHERE THE CURRENT BEHAVIOUR IS PERMISSIVE. A constructed
     72-channel fixture with seven undefined channels passes under NumPy's NaN
     placement and is withheld under the bound. The direction is one-way: every
     scalar convention is itself a completion, so its value lies inside the
     interval and the bound withholds whenever any convention would.

  6. AND IT HAS COSTS THAT ARE RECORDED HERE RATHER THAN DISCOVERED LATER. The
     branch-3 label needs a third outcome that Draft 34's vocabulary does not
     have. Both endpoints are attained by exhibited completions, but no claim
     is made that every value between them is reachable, and none is needed:
     both rules read the endpoints alone. The trajectory of the bound against
     the undefined count is measured on one pool and recorded rather than
     generalized.

  7. ONE EXPECTED DEFECT THAT MEASUREMENT REFUTED. Section 19.4 writes the
     ranks as `ceil(0.10 n)` and `ceil(0.90 n)`. I expected the binary
     floating-point evaluation of that to disagree with exact integer
     arithmetic at some band size, and wrote the check to catch it. It does
     not: the two forms agree at every n from 1 to 200,000. The claim is
     withdrawn and the negative result is recorded, because a reader of a
     successor specification is entitled to know the stated form was checked
     rather than trusted.

BOUNDARY. Every value in this probe is constructed. No candidate sample has
ever been read for noise, no frequency claim is made about real recordings, and
nothing here says how often a channel is undefined in practice. The exhaustive
validation is over small n; at n = 72 the enumeration is validated against the
same closed forms the small-n exhaustion proved, plus a randomized search that
can only ever find values inside the claimed interval. Nothing here reads the
archive, the network, or any project record, and nothing here reopens RC-008 or
Draft 34.

Usage:

    ./venv/Scripts/python.exe \\
        agents/Claude/tools/probe_completion_bounds.py \\
        --out <path> [--records <path>] [--fixtures <n>]
"""

import argparse
import io
import itertools
import json
import math
import random
import sys

import numpy as np

BAND_CHANNELS = 72
M_STRICT = 2.0
INF = float("inf")


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


def nearest_ranks(n):
    """Section 19.4's nearest-rank indices, 1-based, in integer arithmetic.

    Inputs: n, the number of band channels.
    Returns: (i10, i90), the ranks holding the p10 and p90 values.
    """
    return (-(-n // 10), -(-(9 * n) // 10))


def nearest_ranks_float(n):
    """The same two ranks computed the way section 19.4 spells them.

    Inputs: n, the number of band channels.
    Returns: (i10, i90) from `ceil(0.10 n)` and `ceil(0.90 n)` in binary
    floating point. Check section 3 finds this agrees with the integer form
    at every n from 1 to 200,000; the expectation that it would not is
    withdrawn.
    """
    return (int(math.ceil(0.10 * n)), int(math.ceil(0.90 * n)))


def rho(values, i10, i90):
    """The nearest-rank p90/p10 ratio of one window's channel ratios.

    Inputs: `values`, the complete list of n per-channel ratios, each a real
    number in [0, +inf]; `i10` and `i90`, 1-based ranks.
    Returns: the ratio as a float, or None when the ratio is itself undefined
    because both selected order statistics are 0 or both are `+inf`.
    """
    ordered = sorted(values)
    low = ordered[i10 - 1]
    high = ordered[i90 - 1]
    if low == 0.0 and high == 0.0:
        return None
    if math.isinf(low) and math.isinf(high):
        return None
    if low == 0.0:
        return INF
    return high / low


def bounds_exact(finite, u, n):
    """Exact attainable bounds of `rho` over all completions of u unknowns.

    Inputs: `finite`, the sorted list of the n - u defined channel ratios;
    `u`, the number of undefined channels; `n`, the band channel count.
    Returns: a dict with `lo`, `hi` (floats, over completions whose ratio is
    defined), `undefined_reachable` (bool) and `upper_effective`, which is
    `+inf` whenever an undefined ratio is reachable and `hi` otherwise.

    The enumeration places `a` unknowns at 0, `b` tied to one finite value and
    the remaining `u - a - b` at `+inf`. Check section 1 validates that this
    family contains both extremes by exhaustive comparison against a refined
    grid on small fixtures.
    """
    i10, i90 = nearest_ranks(n)
    anchors = list(finite) if finite else [1.0]
    lo = None
    hi = None
    undefined_reachable = False
    for a in range(u + 1):
        for b in range(u - a + 1):
            c = u - a - b
            for anchor in anchors:
                values = ([0.0] * a + [anchor] * b + list(finite)
                          + [INF] * c)
                value = rho(values, i10, i90)
                if value is None:
                    undefined_reachable = True
                    continue
                if lo is None or value < lo:
                    lo = value
                if hi is None or value > hi:
                    hi = value
    upper = INF if (undefined_reachable or hi is None) else hi
    return {"lo": lo, "hi": hi, "undefined_reachable": undefined_reachable,
            "upper_effective": upper}


def bounds_vertex_only(finite, u, n):
    """The same bounds restricted to placements at 0 or `+inf` only.

    Inputs and returns match `bounds_exact`. Used to check which endpoint the
    vertex family is sufficient for; it is sufficient for the maximum and not
    for the minimum.
    """
    i10, i90 = nearest_ranks(n)
    lo = None
    hi = None
    undefined_reachable = False
    for a in range(u + 1):
        values = [0.0] * a + list(finite) + [INF] * (u - a)
        value = rho(values, i10, i90)
        if value is None:
            undefined_reachable = True
            continue
        if lo is None or value < lo:
            lo = value
        if hi is None or value > hi:
            hi = value
    return {"lo": lo, "hi": hi, "undefined_reachable": undefined_reachable}


def lo_closed(finite, u, n):
    """The closed form for the minimum: `f[max(i90 - u, i10)] / f[i10]`.

    Inputs and returns as in `bounds_exact`, but only the minimum, and only
    where it is defined: the form needs at least `i10` finite values and a
    strictly positive value at the p10 rank. Returns None where it does not
    apply, so the caller can restrict the comparison rather than force it.
    """
    i10, i90 = nearest_ranks(n)
    m = len(finite)
    if m < i10 or m < 1:
        return None
    denominator = finite[i10 - 1]
    if denominator == 0.0 or math.isinf(denominator):
        return None
    index = max(i90 - u, i10)
    if index > m:
        return None
    numerator = finite[index - 1]
    if math.isinf(numerator):
        return INF
    return numerator / denominator


def refined_grid(finite):
    """Candidate completion values dense enough to expose a missed extreme.

    Inputs: `finite`, the sorted defined ratios.
    Returns: a sorted list holding 0, `+inf`, every finite value, every
    midpoint between consecutive distinct finite values, one value below the
    smallest and one above the largest.
    """
    grid = set([0.0, INF])
    usable = [v for v in finite if not math.isinf(v)]
    grid.update(usable)
    for left, right in zip(usable, usable[1:]):
        if right > left:
            grid.add((left + right) / 2.0)
    if usable:
        smallest = min(usable)
        largest = max(usable)
        grid.add(smallest / 2.0 if smallest > 0 else 0.5)
        grid.add(largest * 2.0 if largest > 0 else 1.0)
    else:
        grid.update([0.5, 1.0, 2.0])
    return sorted(grid)


def bounds_brute(finite, u, n):
    """Exhaustive bounds over every completion drawn from the refined grid.

    Inputs and returns match `bounds_exact`, minus `upper_effective`. This is
    the reference the enumeration is validated against; it is only affordable
    for small n and small u.
    """
    i10, i90 = nearest_ranks(n)
    grid = refined_grid(finite)
    lo = None
    hi = None
    undefined_reachable = False
    for combination in itertools.product(grid, repeat=u):
        value = rho(list(finite) + list(combination), i10, i90)
        if value is None:
            undefined_reachable = True
            continue
        if lo is None or value < lo:
            lo = value
        if hi is None or value > hi:
            hi = value
    return {"lo": lo, "hi": hi, "undefined_reachable": undefined_reachable}


def max_over_windows(per_window):
    """Propagate per-window bounds through `R_null_sampled = max_k rho(k)`.

    Inputs: a list of dicts as returned by `bounds_exact`, one per window.
    Returns: a dict of the same shape for the maximum. Placements are chosen
    independently in each window, so both endpoints are the windowwise
    maximum of that endpoint.
    """
    los = [b["lo"] for b in per_window if b["lo"] is not None]
    his = [b["hi"] for b in per_window if b["hi"] is not None]
    undefined = any(b["undefined_reachable"] for b in per_window)
    lo = max(los) if los else None
    hi = max(his) if his else None
    upper = INF if (undefined or hi is None) else hi
    return {"lo": lo, "hi": hi, "undefined_reachable": undefined,
            "upper_effective": upper}


def max_over_windows_brute(window_finites, u_per_window, n):
    """The same maximum computed by exhausting completions in every window.

    Inputs: `window_finites`, one sorted finite list per window;
    `u_per_window`, the undefined count per window; `n`, band channels.
    Returns: a dict with `lo` and `hi` for `max_k rho(k)`.
    """
    i10, i90 = nearest_ranks(n)
    grids = [refined_grid(f) for f in window_finites]
    products = [list(itertools.product(g, repeat=u))
                for g, u in zip(grids, u_per_window)]
    lo = None
    hi = None
    for choice in itertools.product(*products):
        values = []
        undefined = False
        for finite, placement in zip(window_finites, choice):
            value = rho(list(finite) + list(placement), i10, i90)
            if value is None:
                undefined = True
                break
            values.append(value)
        if undefined:
            continue
        worst = max(values)
        if lo is None or worst < lo:
            lo = worst
        if hi is None or worst > hi:
            hi = worst
    return {"lo": lo, "hi": hi}


def stands_down(bound, threshold):
    """Whether branch 4 may stand down under Codex's corrected criterion.

    Inputs: `bound`, a dict from `bounds_exact` or `max_over_windows`;
    `threshold`, the spatial threshold `M`.
    Returns: True only when the upper completion bound is at or below `M`.
    """
    return bound["upper_effective"] <= threshold


def branch3_label(r_space, bound):
    """The branch-3 label under completion bounds, with a third outcome.

    Inputs: `r_space`, the spatial ratio that already fired branch 3;
    `bound`, a dict from `bounds_exact` or `max_over_windows`.
    Returns: `resolved heterogeneity` when the whole enclosure lies strictly
    below `r_space`, `resolution-limited` when it lies wholly at or above it,
    and `unresolved` otherwise - including whenever an undefined ratio is
    reachable at all.
    """
    if bound["undefined_reachable"] or bound["lo"] is None:
        return "unresolved"
    if r_space > bound["hi"]:
        return "resolved heterogeneity"
    if r_space <= bound["lo"]:
        return "resolution-limited"
    return "unresolved"


def disposition(sigma_worst, sigma_quiet, r_space, bound, threshold,
                level=10.0, floor=1.25):
    """The four ordered branches of section 19.6 with branch 4 bounded.

    Inputs: the two level statistics, the spatial ratio, a bounds dict, the
    spatial threshold `M`, and the level threshold and floor.
    Returns: a (disposition, label) pair; the label is None outside branch 3.
    """
    if sigma_worst > level:
        return ("fails", "level")
    if sigma_quiet < floor:
        return ("fails", "implausibly quiet")
    if r_space > threshold:
        return ("fails", branch3_label(r_space, bound))
    if not stands_down(bound, threshold):
        return ("unmeasurable", None)
    return ("passes", None)


def frozen_disposition(sigma_worst, sigma_quiet, r_space, r_null, threshold,
                       level=10.0, floor=1.25):
    """Draft 34's four ordered branches with a SCALAR `R_null_sampled`.

    Inputs: the two level statistics, the spatial ratio, the scalar
    resolution ratio - which may be NaN - and the spatial threshold, level
    threshold and floor.
    Returns: the disposition string. A NaN `r_null` compares False against
    `M`, which is exactly the unhandled behaviour Session 50 recorded.
    """
    if sigma_worst > level:
        return "fails"
    if sigma_quiet < floor:
        return "fails"
    if r_space > threshold:
        return "fails"
    if r_null > threshold:
        return "unmeasurable"
    return "passes"


def numpy_nan_rho(finite, u, n):
    """The ratio the current unhandled behaviour produces, via NumPy's sort.

    Inputs: as `bounds_exact`.
    Returns: the float `numpy.sort` yields when the undefined entries are NaN
    and are sunk to the end of the order, which is NaN when a NaN reaches the
    p90 rank.
    """
    i10, i90 = nearest_ranks(n)
    values = np.array(list(finite) + [np.nan] * u, dtype=float)
    ordered = np.sort(values)
    low = ordered[i10 - 1]
    high = ordered[i90 - 1]
    if np.isnan(low) or np.isnan(high):
        return float("nan")
    if low == 0.0:
        return INF
    return float(high / low)


def random_finite(rng, m, style):
    """Build one sorted finite ratio vector of a named shape.

    Inputs: `rng`, a seeded `random.Random`; `m`, how many values; `style`,
    one of `spread`, `tight`, `bimodal`, `withzero`, `withinf`, `flat`.
    Returns: the sorted list.
    """
    if style == "flat":
        values = [1.0] * m
    elif style == "tight":
        values = [1.0 + rng.random() * 0.05 for _ in range(m)]
    elif style == "bimodal":
        values = [1.0 if i < m // 2 else 6.0 for i in range(m)]
    elif style == "withzero":
        values = [0.0] * min(2, m) + [1.0 + rng.random() * 3
                                      for _ in range(max(0, m - 2))]
    elif style == "withinf":
        values = [1.0 + rng.random() * 3 for _ in range(max(0, m - 2))] \
            + [INF] * min(2, m)
    else:
        values = [1.0 + rng.random() * 9 for _ in range(m)]
    return sorted(values[:m])


def parse_args(argv=None):
    """Parse the command line.

    Inputs: `argv`, an argument list, or None to read `sys.argv`.
    Returns: the parsed namespace.
    """
    parser = argparse.ArgumentParser(
        description=("Prove exact completion bounds for the nearest-rank "
                     "p90/p10 ratio when some channel ratios are undefined."))
    parser.add_argument("--out", required=True,
                        help="path for the plain-text report")
    parser.add_argument("--records", default=None,
                        help="optional path for the JSON record")
    parser.add_argument("--fixtures", type=int, default=36,
                        help="number of random small fixtures to exhaust")
    return parser.parse_args(argv)


def main(argv=None):
    """Run every check, print the report and write the artifacts."""
    args = parse_args(argv)
    c = Checks()
    records = {}
    rng = random.Random(19081951)

    c.heading("1. The bound function is exact, checked by exhaustion")
    styles = ["spread", "tight", "bimodal", "withzero", "withinf", "flat"]
    mismatches = []
    vertex_hi_mismatches = []
    vertex_lo_mismatches = []
    closed_lo_mismatches = []
    closed_lo_compared = 0
    below_one = []
    exhausted = 0
    for index in range(args.fixtures):
        n = 10 + (index % 3)
        u = 1 + (index % 3)
        style = styles[index % len(styles)]
        finite = random_finite(rng, n - u, style)
        got = bounds_exact(finite, u, n)
        want = bounds_brute(finite, u, n)
        exhausted += 1
        if (got["lo"] != want["lo"] or got["hi"] != want["hi"]
                or got["undefined_reachable"] != want["undefined_reachable"]):
            mismatches.append((n, u, style, got, want))
        vertex = bounds_vertex_only(finite, u, n)
        if vertex["hi"] != want["hi"]:
            vertex_hi_mismatches.append((n, u, style))
        if vertex["lo"] != want["lo"]:
            vertex_lo_mismatches.append((n, u, style, vertex["lo"],
                                         want["lo"]))
        closed = lo_closed(finite, u, n)
        if closed is not None and want["lo"] is not None:
            closed_lo_compared += 1
            if closed != want["lo"]:
                closed_lo_mismatches.append((n, u, style, closed, want["lo"]))
        if want["lo"] is not None and want["lo"] < 1.0:
            below_one.append((n, u, style, want["lo"]))

    c.check("the three-level enumeration equals a full exhaustive search on "
            "every small fixture, on both endpoints",
            not mismatches,
            "%d fixtures exhausted, %d mismatches" % (exhausted,
                                                      len(mismatches)))
    c.check("the maximum is attained at a vertex - every unknown at 0 or at "
            "+inf", not vertex_hi_mismatches,
            "%d of %d fixtures disagree" % (len(vertex_hi_mismatches),
                                            exhausted))
    c.check("the minimum is NOT attained at a vertex, so the obvious guess "
            "is wrong for that endpoint", bool(vertex_lo_mismatches),
            "%d of %d fixtures have an interior minimum strictly below every "
            "vertex" % (len(vertex_lo_mismatches), exhausted))
    c.check("the closed form f[max(i90 - u, i10)] / f[i10] equals the "
            "exhaustive minimum wherever it applies",
            not closed_lo_mismatches and closed_lo_compared > 0,
            "%d fixtures compared, %d mismatches"
            % (closed_lo_compared, len(closed_lo_mismatches)))
    c.check("the lower bound is never below 1, because the p90 rank sits "
            "above the p10 rank in a sorted non-negative set", not below_one,
            "%d fixtures below 1" % len(below_one))
    records["fixtures_exhausted"] = exhausted
    records["exhaustive_mismatches"] = len(mismatches)
    records["vertex_minimum_failures"] = len(vertex_lo_mismatches)
    records["closed_form_minimum_compared"] = closed_lo_compared

    c.heading("2. A worked interior minimum, so the failure above is concrete")
    interior = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    interior_n = 10
    interior_u = 1
    interior_want = bounds_brute(interior, interior_u, interior_n)
    interior_vertex = bounds_vertex_only(interior, interior_u, interior_n)
    i10_i, i90_i = nearest_ranks(interior_n)
    c.check("at n = 10 the ranks are 1 and 9", (i10_i, i90_i) == (1, 9),
            "ranks %d and %d" % (i10_i, i90_i))
    c.check("placing the unknown at +inf gives the top-rank value 9.0 over "
            "1.0", interior_vertex["lo"] == 9.0,
            "vertex minimum %.6f" % interior_vertex["lo"])
    c.check("placing it at an interior value pushes the p90 rank down one "
            "finite value without moving the p10 rank",
            interior_want["lo"] == 8.0,
            "exhaustive minimum %.6f" % interior_want["lo"])
    c.check("so the interior placement strictly beats both vertices",
            interior_want["lo"] < interior_vertex["lo"],
            "%.6f < %.6f" % (interior_want["lo"], interior_vertex["lo"]))
    records["interior_minimum_example"] = {
        "finite": interior, "u": interior_u, "n": interior_n,
        "vertex_lo": interior_vertex["lo"], "exact_lo": interior_want["lo"]}

    c.heading("3. The ranks at n = 72, and an expected defect that "
              "measurement refuted")
    i10, i90 = nearest_ranks(BAND_CHANNELS)
    c.check("integer arithmetic gives ranks 8 and 65 at n = 72",
            (i10, i90) == (8, 65), "ranks %d and %d" % (i10, i90))
    disagreeing = [n for n in range(1, 200001)
                   if nearest_ranks_float(n) != nearest_ranks(n)]
    c.check("section 19.4's own ceil(0.10 n) and ceil(0.90 n), evaluated in "
            "binary floating point, agree with exact integer arithmetic at "
            "every n from 1 to 200,000", not disagreeing,
            "%d disagreements" % len(disagreeing))
    c.note("I wrote that check expecting it to FAIL and to yield an "
           "implementation hazard. It did not. The stated form is safe at "
           "every band size this project could use; the integer form used "
           "here is belt and braces, not a repair, and the hazard claim is "
           "withdrawn")
    c.check("i10 and n - i90 + 1 coincide at n = 72, which is why one count "
            "governs both ends", i10 == BAND_CHANNELS - i90 + 1,
            "i10 = %d, n - i90 + 1 = %d" % (i10, BAND_CHANNELS - i90 + 1))
    records["ranks_at_72"] = [i10, i90]
    records["float_rank_disagreements_to_200000"] = len(disagreeing)

    c.heading("4. The count threshold at n = 72")
    uniform_hi = {}
    for u in range(0, 13):
        finite = [1.0 + 0.01 * k for k in range(BAND_CHANNELS - u)]
        bound = bounds_exact(finite, u, BAND_CHANNELS)
        uniform_hi[u] = bound["upper_effective"]
    c.check("with 7 or fewer undefined channels the upper bound is finite",
            all(math.isfinite(uniform_hi[u]) for u in range(0, 8)),
            "u = 7 gives %.6f" % uniform_hi[7])
    c.check("with 8 or more it is unbounded whatever the finite values are",
            all(math.isinf(uniform_hi[u]) for u in range(8, 13)),
            "u = 8 gives %r" % uniform_hi[8])
    c.check("8 is exactly the count at which the documented zero-denominator "
            "case already reaches +inf", i10 == 8,
            "the p10 rank is %d, so 8 entries at 0 reach it" % i10)
    records["upper_bound_by_undefined_count"] = {
        str(u): ("inf" if math.isinf(v) else v)
        for u, v in sorted(uniform_hi.items())}

    c.heading("5. It is a conservative extension of the frozen rule")
    collapse_failures = []
    branch4_failures = []
    label_failures = []
    compared = 0
    for index in range(24):
        finite = random_finite(rng, BAND_CHANNELS, styles[index % 6])
        bound = bounds_exact(finite, 0, BAND_CHANNELS)
        direct = rho(finite, i10, i90)
        if direct is None:
            continue
        compared += 1
        if bound["lo"] != direct or bound["hi"] != direct:
            collapse_failures.append((index, bound, direct))
        if (direct > M_STRICT) != (not stands_down(bound, M_STRICT)):
            branch4_failures.append((index, direct))
        for spatial in [1.0, 3.0, 12.0]:
            frozen_label = ("resolved heterogeneity" if spatial > direct
                            else "resolution-limited")
            if branch3_label(spatial, bound) != frozen_label:
                label_failures.append((index, spatial, direct))
    c.check("with no undefined channel the two bounds collapse to the single "
            "value", not collapse_failures and compared == 24,
            "%d fixtures, %d disagreements" % (compared,
                                               len(collapse_failures)))
    c.check("branch 4 then fires exactly when Draft 34 says it fires",
            not branch4_failures,
            "%d disagreements over %d fixtures" % (len(branch4_failures),
                                                   compared))
    c.check("and the third label is unreachable, so the rule reduces to "
            "Draft 34's two", not label_failures,
            "%d disagreements over %d spatial values"
            % (len(label_failures), compared * 3))
    records["conservative_extension_failures"] = (
        len(collapse_failures) + len(branch4_failures) + len(label_failures))

    c.heading("6. Every scalar convention is a completion, so the bound "
              "dominates all of them")
    convention_failures = []
    convention_rows = []
    for index in range(18):
        u = 1 + (index % 7)
        finite = random_finite(rng, BAND_CHANNELS - u, styles[index % 6])
        bound = bounds_exact(finite, u, BAND_CHANNELS)
        for scalar in [0.0, 1.0, INF, finite[len(finite) // 2]]:
            value = rho(list(finite) + [scalar] * u, i10, i90)
            if value is None:
                continue
            if bound["lo"] is None or not (bound["lo"] <= value
                                           <= bound["upper_effective"]):
                convention_failures.append((index, scalar, value, bound))
        convention_rows.append((u, bound["lo"], bound["upper_effective"]))
    c.check("assigning 0, 1, +inf or the finite median to every undefined "
            "channel always lands inside the enclosure",
            not convention_failures,
            "%d assignments checked, %d outside"
            % (18 * 4, len(convention_failures)))
    sample_failures = []
    one_way_failures = []
    sampled = 0
    for index in range(12):
        u = 1 + (index % 7)
        finite = random_finite(rng, BAND_CHANNELS - u, styles[index % 6])
        bound = bounds_exact(finite, u, BAND_CHANNELS)
        for _ in range(200):
            placement = [rng.choice([0.0, INF, rng.random() * 12.0])
                         for _ in range(u)]
            value = rho(list(finite) + placement, i10, i90)
            if value is None:
                continue
            sampled += 1
            if not (bound["lo"] <= value <= bound["upper_effective"]):
                sample_failures.append((index, value))
            if value > M_STRICT and stands_down(bound, M_STRICT):
                one_way_failures.append((index, value))
    c.check("randomly drawn completions, including mixtures of 0, +inf and "
            "interior values, all land inside the enclosure",
            not sample_failures,
            "%d completions drawn, %d outside" % (sampled,
                                                  len(sample_failures)))
    c.check("no completion withholds while the bounded rule stands down, so "
            "the direction is one-way", not one_way_failures,
            "%d one-way violations over %d completions"
            % (len(one_way_failures), sampled))
    records["scalar_convention_failures"] = len(convention_failures)
    records["sampled_completions"] = sampled
    records["sampled_completion_failures"] = len(sample_failures)

    c.heading("7. It bites where the current unhandled behaviour passes")
    bite_finite = sorted([1.0] * 7 + [3.0] * 58)
    bite_u = 7
    bite = bounds_exact(bite_finite, bite_u, BAND_CHANNELS)
    bite_numpy = numpy_nan_rho(bite_finite, bite_u, BAND_CHANNELS)
    c.check("the fixture has 65 finite ratios and 7 undefined ones",
            len(bite_finite) + bite_u == BAND_CHANNELS,
            "%d finite, %d undefined" % (len(bite_finite), bite_u))
    bite_frozen = frozen_disposition(6.0, 5.0, 1.0, bite_numpy, M_STRICT)
    c.check("NumPy's NaN placement gives a ratio at or below M, so the "
            "current unhandled behaviour passes",
            bite_numpy <= M_STRICT and bite_frozen == "passes",
            "NumPy ratio %.6f, frozen disposition %s"
            % (bite_numpy, bite_frozen))
    c.check("the upper completion bound exceeds M, so the bounded rule "
            "withholds", bite["upper_effective"] > M_STRICT,
            "bound [%.6f, %.6f]" % (bite["lo"], bite["upper_effective"]))
    c.check("and the disposition changes from passes to unmeasurable",
            disposition(6.0, 5.0, 1.0, bite, M_STRICT)[0] == "unmeasurable",
            "disposition %s" % (disposition(6.0, 5.0, 1.0, bite,
                                            M_STRICT)[0],))
    vertex_top = rho(list(bite_finite) + [INF] * bite_u, i10, i90)
    c.check("NumPy's placement IS the all-at-+inf vertex for the ranks, so "
            "the divergence is in the comparison and not in the ordering",
            bite_numpy == vertex_top,
            "NumPy %.6f, all-at-+inf vertex %.6f" % (bite_numpy, vertex_top))
    c.check("that vertex is one completion of many, and it is not the "
            "extreme one", vertex_top < bite["upper_effective"],
            "vertex %.6f against upper bound %.6f"
            % (vertex_top, bite["upper_effective"]))
    records["biting_fixture"] = {
        "numpy_ratio": bite_numpy, "lo": bite["lo"],
        "hi": bite["upper_effective"], "all_at_inf_vertex": vertex_top,
        "frozen_disposition": bite_frozen,
        "bounded_disposition": disposition(6.0, 5.0, 1.0, bite,
                                           M_STRICT)[0]}

    c.heading("8. A seven-undefined fixture that is PROVED decision-"
              "irrelevant")
    clean_finite = [1.0 + 0.001 * k for k in range(BAND_CHANNELS - 7)]
    clean = bounds_exact(clean_finite, 7, BAND_CHANNELS)
    c.check("with homogeneous finite ratios the upper bound stays at or below "
            "M with 7 undefined channels", clean["upper_effective"] <= M_STRICT,
            "bound [%.6f, %.6f]" % (clean["lo"], clean["upper_effective"]))
    c.check("so branch 4 stands down and the undefined entries are proved "
            "irrelevant to the decision rather than assumed to be",
            stands_down(clean, M_STRICT)
            and disposition(6.0, 5.0, 1.0, clean, M_STRICT)[0] == "passes",
            "disposition %s" % (disposition(6.0, 5.0, 1.0, clean,
                                            M_STRICT)[0],))
    c.note("this is the property that keeps the rule from being a blanket "
           "rejection of any candidate with one undefined channel")
    records["decision_irrelevant_fixture"] = {
        "lo": clean["lo"], "hi": clean["upper_effective"]}

    c.heading("9. The corrected rule covers an interval lying wholly above M")
    above_finite = sorted([1.0] * 8 + [5.0] * 57)
    above = bounds_exact(above_finite, 7, BAND_CHANNELS)
    c.check("the whole enclosure lies above M", above["lo"] > M_STRICT
            and above["upper_effective"] > M_STRICT,
            "bound [%.6f, %.6f]" % (above["lo"], above["upper_effective"]))
    c.check("the corrected criterion withholds it, which the first wording "
            "omitted", not stands_down(above, M_STRICT)
            and disposition(6.0, 5.0, 1.0, above, M_STRICT)[0]
            == "unmeasurable",
            "disposition %s" % (disposition(6.0, 5.0, 1.0, above,
                                            M_STRICT)[0],))
    c.check("the rule reads only the upper bound, so the lower bound is never "
            "consulted by branch 4",
            stands_down({"upper_effective": 1.0, "lo": 0.5, "hi": 1.0,
                         "undefined_reachable": False}, M_STRICT)
            and stands_down({"upper_effective": 1.0, "lo": 1.0, "hi": 1.0,
                             "undefined_reachable": False}, M_STRICT),
            "two different lower bounds, same standing-down decision")
    records["wholly_above_fixture"] = {"lo": above["lo"],
                                       "hi": above["upper_effective"]}

    c.heading("10. The branch-3 label needs a third outcome, and all three "
              "are reachable")
    label_bound = {"lo": 1.5, "hi": 4.0, "undefined_reachable": False,
                   "upper_effective": 4.0}
    resolved = branch3_label(5.0, label_bound)
    limited = branch3_label(1.2, label_bound)
    unresolved = branch3_label(3.0, label_bound)
    c.check("a spatial value above the whole enclosure gives resolved "
            "heterogeneity", resolved == "resolved heterogeneity", resolved)
    c.check("a spatial value at or below the whole enclosure gives "
            "resolution-limited", limited == "resolution-limited", limited)
    c.check("a spatial value inside the enclosure gives a third outcome that "
            "Draft 34's vocabulary does not have",
            unresolved == "unresolved", unresolved)
    c.check("the three outcomes are exhaustive and mutually exclusive over a "
            "swept spatial value",
            len(set(branch3_label(v / 10.0, label_bound)
                    for v in range(1, 100))) == 3,
            "swept 99 spatial values, %d distinct labels"
            % len(set(branch3_label(v / 10.0, label_bound)
                      for v in range(1, 100))))
    c.check("an unbounded enclosure can never be labelled resolved",
            branch3_label(1e9, {"lo": 1.0, "hi": None,
                                "undefined_reachable": True,
                                "upper_effective": INF}) == "unresolved",
            "unresolved even at a spatial value of 1e9")
    c.note("adding a third label is a change to section 19.6's published "
           "vocabulary and any successor card must carry it explicitly")

    c.heading("11. The maximum over windows propagates exactly")
    window_failures = []
    for index in range(8):
        n_w = 10
        u_w = 1 + (index % 2)
        finites = [random_finite(rng, n_w - u_w, styles[(index + k) % 6])
                   for k in range(2)]
        per_window = [bounds_exact(f, u_w, n_w) for f in finites]
        got = max_over_windows(per_window)
        want = max_over_windows_brute(finites, [u_w, u_w], n_w)
        if got["lo"] != want["lo"] or got["hi"] != want["hi"]:
            window_failures.append((index, got, want))
    c.check("the windowwise maximum of each endpoint equals the exhaustive "
            "bound on the maximum, because placements are independent across "
            "windows", not window_failures,
            "8 two-window fixtures, %d disagreements" % len(window_failures))
    c.check("a single unbounded window makes the whole diagnostic unbounded",
            math.isinf(max_over_windows(
                [{"lo": 1.0, "hi": 1.0, "undefined_reachable": False},
                 {"lo": 1.0, "hi": None,
                  "undefined_reachable": True}])["upper_effective"]),
            "one undefined-reachable window carries the maximum")
    records["window_propagation_failures"] = len(window_failures)

    c.heading("12. Both endpoints are attained; the interior is not claimed")
    witness = bounds_exact(bite_finite, bite_u, BAND_CHANNELS)
    hi_witness = rho(list(bite_finite) + [0.0] * bite_u, i10, i90)
    lo_witness = rho(list(bite_finite) + [bite_finite[i10 - 1]] * bite_u,
                     i10, i90)
    c.check("the upper endpoint is attained by an exhibited completion - "
            "every unknown at 0", hi_witness == witness["hi"],
            "witness %.6f, bound %.6f" % (hi_witness, witness["hi"]))
    c.check("the lower endpoint is attained by an exhibited completion - "
            "every unknown tied to the p10 value", lo_witness == witness["lo"],
            "witness %.6f, bound %.6f" % (lo_witness, witness["lo"]))
    pinned = bounds_exact(sorted([1.0] * 5 + [50.0] * 5), 1, 11)
    c.check("the enclosure can collapse to a single point, so an undefined "
            "channel is not automatically uncertainty in the decision",
            pinned["lo"] == pinned["hi"],
            "one undefined channel of 11 leaves the ratio pinned at %.6f"
            % pinned["lo"])
    c.note("no claim is made that every value between the endpoints is "
           "reachable. A uniform sweep cannot separate a real gap from grid "
           "resolution, so the question is left open, and it is not "
           "load-bearing: `stands_down` reads the upper endpoint alone and "
           "`branch3_label` reads the two endpoints and the undefined flag, "
           "so no interior value enters any decision")
    records["endpoint_witnesses"] = {"lo": lo_witness, "hi": hi_witness}
    records["collapsed_enclosure_example"] = pinned["lo"]

    c.heading("13. The band-level 0/0 case, one level up")
    both_zero = [0.0] * 9 + [1.0]
    c.check("a window in which both selected order statistics are 0 has no "
            "ratio at all", rho(both_zero, 1, 9) is None,
            "9 of 10 channels at exactly 0")
    deep = bounds_exact([0.0] * 65, 7, BAND_CHANNELS)
    c.check("at n = 72 that needs at least 65 channels at exactly 0, and it "
            "makes the upper bound unbounded rather than passing",
            deep["undefined_reachable"]
            and math.isinf(deep["upper_effective"]),
            "undefined reachable %r" % deep["undefined_reachable"])
    c.note("this is a second-order undefined case that lives one level above "
           "the per-channel one and is not the subject of the Part B "
           "question; it is recorded so that a successor specification does "
           "not meet it for the first time in an implementation")

    c.heading("14. How the bound moves with the undefined count")
    pool = [1.0 + 0.05 * k for k in range(BAND_CHANNELS)]
    trajectory = []
    for u in range(0, 8):
        finite = sorted(pool[:BAND_CHANNELS - u])
        bound = bounds_exact(finite, u, BAND_CHANNELS)
        trajectory.append((u, bound["lo"], bound["upper_effective"]))
    non_decreasing = all(trajectory[k][2] <= trajectory[k + 1][2] + 1e-12
                         for k in range(len(trajectory) - 1))
    c.check("the u = 0 entry of the trajectory is exactly the pool's plain "
            "nearest-rank ratio, which anchors the rest of it",
            trajectory[0][2] == rho(pool, i10, i90),
            "u = 0 gives %.6f" % trajectory[0][2])
    c.note("measured upper bounds over u = 0..7 on one pool: %s"
           % [round(row[2], 6) for row in trajectory])
    c.note("on this pool the upper bound is %s in u; that is one pool and is "
           "not a general monotonicity claim"
           % ("non-decreasing" if non_decreasing else "NOT monotone"))
    records["undefined_count_trajectory"] = [
        {"u": row[0], "lo": row[1],
         "hi": ("inf" if math.isinf(row[2]) else row[2])}
        for row in trajectory]
    records["upper_bound_non_decreasing_on_pool"] = bool(non_decreasing)

    c.heading("15. Boundary")
    c.note("every value here is constructed; no candidate sample has ever "
           "been read for noise and no frequency claim is made about real "
           "recordings")
    c.note("the exhaustive validation is over n = 10..12 and u = 1..3; at "
           "n = 72 the enumeration is used on the strength of that "
           "validation, not on a separate exhaustion")
    c.note("this probe checks a criterion Codex constructed; it is not a "
           "Part B proposal, it selects no split member, and it opens no "
           "Review Card")
    c.note("nothing here reopens RC-008 or edits Draft 34")

    records["threshold_m"] = M_STRICT
    records["band_channels"] = BAND_CHANNELS
    records["boundary"] = ("constructed values only; the claim is that the "
                           "completion bounds are exact and that the "
                           "criterion built on them is a conservative "
                           "extension of the frozen rule")

    text = c.render()
    sys.stdout.write(text)
    io.open(args.out, "w", encoding="utf-8", newline="\n").write(text)
    if args.records:
        io.open(args.records, "w", encoding="utf-8", newline="\n").write(
            json.dumps(records, indent=2, sort_keys=True) + "\n")
    return 1 if c.failed else 0


if __name__ == "__main__":
    sys.exit(main())
