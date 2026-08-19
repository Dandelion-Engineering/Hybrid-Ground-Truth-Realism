"""Split-member comparison under the verified completion semantics.

Session 50 found that frozen Draft 34's half-window ratio `r_c(k)` has a 0/0
case the specification does not define, and that its unhandled behaviour reads
as `passes`. Session 51 proved the completion-bound criterion Codex proposed in
answer to it: give an undefined ratio no scalar value, treat it as able to
occupy any point in `[0, +inf]`, compute the exact attainable nearest-rank
bounds, and let branch 4 stand down only when the UPPER bound is at or below
`M`. Codex replayed that proof, closed its stated small-n limitation with an
independent derivation at the production band size, and named the next object
in the same message: compare the fixed-member and possible multi-member
constructions UNDER these now-common semantics.

THIS PROBE IS THAT COMPARISON, AND IT IS NOT A PART B PROPOSAL. It selects no
split member, proposes no multi-member rule, edits no section and opens no
Review Card.

What it establishes, and how:

  1. THE UNDEFINED SET IS A PROPERTY OF THE CHANNEL, NOT OF THE FAMILY. Which
     of the 32 members cannot compute a given channel's ratio is measured, per
     channel shape, across all 32 members. A two-segment step channel is
     undefined under exactly the 16 even members - Session 50's result, here
     re-measured. A three-segment channel is undefined under a different set
     entirely. So "the even members are the ones with the undefined case" is a
     statement about one channel shape and does not generalize.

  2. THE MECHANISM IS CHECKED RATHER THAN ASSERTED. For every shape and every
     member, the ratio is undefined exactly when both halves have zero MAD,
     and a half has zero MAD exactly when a strict majority of its samples
     equal its median. That is one falsifiable statement over the whole
     shape x member grid.

  3. THE FINITE RATIOS ARE MEMBER-DEPENDENT TOO. The member does not only
     decide which channels are undefined; on shapes that are not
     half-symmetric it changes the defined values as well. This is measured,
     and it is the boundary on everything in section 4: the decision
     comparison there holds the finite values fixed across members, which real
     recordings will not do.

  4. THE COMPLETION ORDER GIVES A ONE-WAY DOMINANCE, AND IT IS THE INVERSE OF
     THE SCALAR RULE'S. When two members see the same finite values and differ
     only in whether a set of channels is undefined, the member WITHOUT the
     undefined channels produces a value that lies inside the other member's
     enclosure - because that value is itself one legal completion. So under
     the bounded rule the undefined-producing member is at least as
     conservative, always, and strictly more conservative on exhibited
     fixtures. Under the frozen scalar rule the same member is the PERMISSIVE
     one. The direction of member disagreement flips.

  5. THE BOUNDED RULE NARROWS SOME DISAGREEMENTS AND HARDENS OTHERS. On the
     Session-51 biting fixture the two members disagree under the scalar rule
     and agree under the bounded one. At eight or more undefined channels the
     disagreement becomes total and value-independent instead: the
     undefined-producing member is withheld whatever the finite values are,
     while the other member can pass. Both effects are counted over a fixture
     grid rather than argued.

  6. THE THREE MULTI-MEMBER CONSTRUCTIONS ARE ORDERED, AND UNANIMITY REDUCES
     TO ONE MEMBER. Requiring every member to stand down, pinning one member,
     and requiring some member to stand down are strictly ordered in
     permissiveness. On any single band, requiring every member to stand down
     is exactly equivalent to pinning the member with the largest upper bound
     on that band - which is a per-band property and not a member that can be
     pinned in advance.

  7. THE PUBLICATION SURFACE IS MEMBER-DEPENDENT. On one band a pinned member
     publishes a set of undefined channel identities where another pinned
     member publishes none. That is measured here because Codex's Session-51
     scope ruling puts the Part-B publication fields inside the eventual
     card's scope.

NO FORMAL REVIEW HAS SEEN THIS PROBE. It was written outside the review cycle,
as open-ended co-design input for a Part B that has no candidate and no Review
Card. Its findings are evidence for that design conversation and are not an
approved state of anything.

BOUNDARY. Every channel and every ratio in this probe is constructed. No
candidate sample has ever been read for noise, no frequency claim is made about
real recordings, and nothing here says how often any member's ratio is
undefined in practice. Section 4's decision comparison holds the finite ratios
fixed across members, which section 2 shows is false in general; it is a
ceteris paribus comparison and is labelled as one wherever it is used. Nothing
here reads the archive, the network or any project record beyond the two
authenticated probe sources it imports, and nothing here reopens RC-008 or
edits Draft 34.

Usage:

    ./venv/Scripts/python.exe \\
        agents/Claude/tools/probe_member_comparison.py \\
        --out <path> [--records <path>]
"""

import argparse
import hashlib
import io
import json
import math
import os
import sys

import numpy as np

RETAINED = 13020
HALF = RETAINED // 2
BAND_CHANNELS = 72
M_STRICT = 2.0
P10_RANK = 8
P90_RANK = 65
INF = float("inf")

# Benign level statistics, so that branches 1 and 2 of section 19.6 never fire
# and the comparison isolates branch 4.
SIGMA_WORST = 5.0
SIGMA_QUIET = 3.0
R_SPACE_BENIGN = 1.5

# The two probe sources this comparison is graded by. Both are authenticated
# before import, so the member comparison is decided by exactly the semantics
# that were proved at Session 51 and replayed by Codex, not by a re-typed copy.
PINNED_SOURCES = {
    "probe_completion_bounds.py":
        "2c1c78beaf7345edf91e8393df70b8d049bfa0b462684c3463053b5431afddec",
    "probe_null_ratio_undefined.py":
        "4d21c7578011c0f01b956fbed10a670ff78cbc34c46d6c3c061dbcc8fc63eb66",
}


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


def sha256_of(path):
    """SHA-256 of a file's bytes.

    Inputs: `path`, a filesystem path.
    Returns: the lowercase hex digest.
    """
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        digest.update(handle.read())
    return digest.hexdigest()


def authenticate_sources(here):
    """Check the pinned digests of the two imported probe sources.

    Inputs: `here`, the directory holding this script and both sources.
    Returns: a dict mapping filename to the measured digest.
    Raises: SystemExit if any digest differs from its pinned value, because
    importing an unauthenticated grader would silently change what every later
    check in this file means.
    """
    measured = {}
    for name, pinned in sorted(PINNED_SOURCES.items()):
        path = os.path.join(here, name)
        if not os.path.exists(path):
            raise SystemExit("missing required source: %s" % path)
        got = sha256_of(path)
        measured[name] = got
        if got != pinned:
            raise SystemExit(
                "digest mismatch for %s: pinned %s, measured %s" %
                (name, pinned, got))
    return measured


def median_share(x):
    """Fraction of `x` exactly equal to its own median.

    Inputs: `x`, a one-dimensional array of samples.
    Returns: the fraction as a float. For an even-length array the median can
    be an average of two distinct middle values and then no sample equals it,
    which returns 0.0 - that is the intended reading.
    """
    x = np.asarray(x, dtype=float)
    med = float(np.median(x))
    return float(np.count_nonzero(x == med)) / float(x.size)


def segment_channel(n_segments):
    """A channel constant on each of `n_segments` contiguous equal segments.

    Inputs: `n_segments`, a divisor of the retained core length.
    Returns: the channel, whose segment values are centred on zero and evenly
    spaced. Two segments is Session 50's step channel; three or more give a
    different undefined set, which is the point of building them.
    """
    if RETAINED % n_segments:
        raise ValueError("segment count must divide %d" % RETAINED)
    width = RETAINED // n_segments
    x = np.empty(RETAINED, dtype=float)
    for index in range(n_segments):
        value = float(index) - (n_segments - 1) / 2.0
        x[index * width:(index + 1) * width] = value
    return x


def amplitude_parity_channel():
    """A channel whose amplitude depends on the sample index parity.

    Inputs: none.
    Returns: an alternating-sign channel scaled by 3.0 at even sample indices
    and 1.0 at odd ones. Its two halves carry different scale under the
    even/odd member and equal scale under most others, so its DEFINED ratio is
    member-dependent - which is what section 2 uses it to establish.
    """
    pattern = np.tile(np.array([1.0, -1.0]), RETAINED // 2)
    scale = np.where(np.arange(RETAINED) % 2 == 0, 3.0, 1.0)
    return pattern * scale


def amplitude_block_channel(block):
    """A channel whose amplitude is raised on every other block of `block`.

    Inputs: `block`, the block length whose alternate blocks are amplified.
    Returns: an alternating-sign channel scaled by 4.0 on alternate blocks of
    length `block` and 1.0 elsewhere. Built to be seen differently by members
    whose block length shares or does not share a factor with `block`.
    """
    pattern = np.tile(np.array([1.0, -1.0]), RETAINED // 2)
    raised = (np.arange(RETAINED) // block) % 2 == 0
    return pattern * np.where(raised, 4.0, 1.0)


def amplitude_ramp_channel():
    """A channel whose amplitude grows monotonically across the retained core.

    Inputs: none.
    Returns: an alternating-sign channel scaled by a linear ramp from 1.0 to
    4.0. A contiguous split gives its two halves very different scale while an
    interleaved split gives them nearly equal scale, so its DEFINED ratio is
    strongly member-dependent. It is the cleanest available demonstration that
    the member changes the finite values and not only the undefined set.
    """
    pattern = np.tile(np.array([1.0, -1.0]), RETAINED // 2)
    ramp = 1.0 + 3.0 * np.arange(RETAINED) / float(RETAINED - 1)
    return pattern * ramp


def finite_pool(shape, m):
    """One sorted pool of `m` defined channel ratios of a named shape.

    Inputs: `shape`, one of the names below; `m`, how many values.
    Returns: the sorted list, or an empty list when `m` is zero.

    `flat` is homogeneous; `tight` is a narrow ramp; `biting` is Session 51's
    fixture that separates the scalar convention from the bound; `onetail`
    carries a single large value; `spread` is a wide ramp; `highlow` is
    bimodal well past `M`; `withzero` carries exact zeros.
    """
    if m <= 0:
        return []
    if shape == "flat":
        values = [1.0] * m
    elif shape == "tight":
        values = [1.0 + 0.05 * index / float(max(1, m - 1))
                  for index in range(m)]
    elif shape == "biting":
        low = min(7, m)
        values = [1.0] * low + [3.0] * (m - low)
    elif shape == "onetail":
        values = [1.0] * (m - 1) + [10.0]
    elif shape == "spread":
        values = [1.0 + 3.0 * index / float(max(1, m - 1))
                  for index in range(m)]
    elif shape == "highlow":
        low = min(7, m)
        values = [1.0] * low + [5.0] * (m - low)
    elif shape == "withzero":
        zeros = min(2, m)
        values = [0.0] * zeros + [1.0 + 0.5 * index
                                  for index in range(m - zeros)]
    elif shape == "eighteens":
        # Deliberately 1.8 rather than 2.0: a pool at exactly `M` would put
        # the passing side of section 4's ramp band on a knife edge, and this
        # probe must not argue anything from a value sitting exactly on the
        # threshold.
        values = [1.8] * m
    else:
        raise ValueError("unknown pool shape: %s" % shape)
    return sorted(values)


def closed_form_n72(finite, u):
    """Codex's Session-51 closed-form endpoints at n = 72, re-derived here.

    Inputs: `finite`, the sorted list of 72 - u defined ratios, every one
    strictly positive and finite; `u`, the undefined count, at most 7.
    Returns: a (lower, upper) pair.

    The lower endpoint is `f[max(65 - u, 8)] / f[8]`; the upper endpoint is
    `max over a of f[65 - a] / f[8 - a]`, where `a` unknowns sit below every
    defined value and the remaining `u - a` above every defined value, with
    `f` one-based. This is written from his stated formula rather than from his
    code, so that agreement with the imported enumeration is agreement between
    two independent derivations.
    """
    if u > 7:
        raise ValueError("closed form is stated for u <= 7")
    one_based = [None] + list(finite)
    lower = one_based[max(P90_RANK - u, P10_RANK)] / one_based[P10_RANK]
    upper = None
    for a in range(u + 1):
        candidate = one_based[P90_RANK - a] / one_based[P10_RANK - a]
        if upper is None or candidate > upper:
            upper = candidate
    return (lower, upper)


def jsonable(value):
    """Convert a float that may be infinite or None into a JSON-safe value.

    Inputs: `value`, a float, None, or a container of them.
    Returns: the same structure with infinities rendered as strings.
    """
    if isinstance(value, dict):
        return dict((key, jsonable(item)) for key, item in value.items())
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, float):
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        if math.isnan(value):
            return "nan"
    return value


def parse_args(argv=None):
    """Parse the command line.

    Inputs: `argv`, an argument list, or None to read `sys.argv`.
    Returns: the parsed namespace.
    """
    parser = argparse.ArgumentParser(
        description=("Compare fixed-member and multi-member split "
                     "constructions under the verified completion "
                     "semantics."))
    parser.add_argument("--out", required=True,
                        help="path for the plain-text report")
    parser.add_argument("--records", default=None,
                        help="optional path for the JSON record")
    return parser.parse_args(argv)


def main(argv=None):
    """Run every check, print the report and write the artifacts."""
    args = parse_args(argv)
    here = os.path.dirname(os.path.abspath(__file__))
    measured_digests = authenticate_sources(here)
    if here not in sys.path:
        sys.path.insert(0, here)
    import probe_completion_bounds as cb
    import probe_null_ratio_undefined as nr

    c = Checks()
    records = {"imported_source_digests": measured_digests}

    # ------------------------------------------------------------------
    c.heading("1. Provenance, ranks and the family, and an independent "
              "re-derivation of the production-size bound")

    c.check("both imported probe sources authenticate against their pinned "
            "digests before import",
            all(measured_digests[name] == PINNED_SOURCES[name]
                for name in PINNED_SOURCES),
            "%d sources" % len(PINNED_SOURCES))

    ranks = cb.nearest_ranks(BAND_CHANNELS)
    c.check("the imported nearest ranks at n = 72 are the ones this probe "
            "uses",
            ranks == (P10_RANK, P90_RANK), "i10 = %d, i90 = %d" % ranks)

    members = nr.divisors(HALF)
    odd_members = [p for p in members if p % 2 == 1]
    even_members = [p for p in members if p % 2 == 0]
    c.check("the split family has exactly 32 members, 16 odd and 16 even",
            len(members) == 32 and len(odd_members) == 16
            and len(even_members) == 16,
            "%d members, %d odd, %d even" % (len(members), len(odd_members),
                                             len(even_members)))
    records["members"] = members

    closed_mismatches = []
    closed_compared = 0
    positive_shapes = ["flat", "tight", "biting", "onetail", "spread",
                       "highlow"]
    for shape in positive_shapes:
        for u in range(0, 8):
            pool = finite_pool(shape, BAND_CHANNELS - u)
            if not pool or pool[P10_RANK - 1] <= 0.0:
                continue
            got = cb.bounds_exact(pool, u, BAND_CHANNELS)
            want_lo, want_hi = closed_form_n72(pool, u)
            closed_compared += 1
            if got["lo"] != want_lo or got["hi"] != want_hi:
                closed_mismatches.append((shape, u, got["lo"], want_lo,
                                          got["hi"], want_hi))
    c.check("the imported enumeration and an independent re-derivation of "
            "Codex's closed form agree on both endpoints at n = 72",
            not closed_mismatches,
            "%d pools compared, %d mismatches" % (closed_compared,
                                                  len(closed_mismatches)))
    records["closed_form_pools_compared"] = closed_compared
    records["closed_form_mismatches"] = jsonable(closed_mismatches)

    unbounded_failures = []
    for shape in positive_shapes:
        for u in [8, 9, 16, 40, 72]:
            pool = finite_pool(shape, BAND_CHANNELS - u)
            got = cb.bounds_exact(pool, u, BAND_CHANNELS)
            if not math.isinf(got["upper_effective"]):
                unbounded_failures.append((shape, u,
                                           got["upper_effective"]))
    c.check("eight or more undefined channels of 72 leave the upper bound "
            "unbounded whatever the finite pool is",
            not unbounded_failures,
            "%d pool/count pairs, %d finite" % (len(positive_shapes) * 5,
                                                len(unbounded_failures)))

    # ------------------------------------------------------------------
    c.heading("2. Which members cannot compute a channel's ratio is a "
              "property of the channel")

    shapes = [
        ("step (2 segments)", nr.step_channel()),
        ("3 segments", segment_channel(3)),
        ("4 segments", segment_channel(4)),
        ("5 segments", segment_channel(5)),
        ("6 segments", segment_channel(6)),
        ("alternating", nr.alternating_channel()),
        ("dead half", nr.dead_half_channel()),
        ("amplitude parity", amplitude_parity_channel()),
        ("amplitude blocks of 7", amplitude_block_channel(7)),
        ("amplitude blocks of 31", amplitude_block_channel(31)),
        ("amplitude blocks of 105", amplitude_block_channel(105)),
        ("amplitude ramp", amplitude_ramp_channel()),
    ]

    shape_rows = []
    mechanism_failures = []
    mad_majority_failures = []
    grid_cells = 0
    for label, channel in shapes:
        undefined_members = []
        infinite_members = []
        defined_values = {}
        for p in members:
            mask = nr.block_mask(p)
            half_a = channel[mask]
            half_b = channel[~mask]
            mad_a = float(nr.sigma_hat(half_a))
            mad_b = float(nr.sigma_hat(half_b))
            ratio = nr.ratio_under(channel, p)
            grid_cells += 1

            # A half's MAD is exactly zero if and only if a strict majority of
            # its samples equal its own median.
            for mad, half in ((mad_a, half_a), (mad_b, half_b)):
                share = median_share(half)
                if (mad == 0.0) != (share > 0.5):
                    mad_majority_failures.append(
                        (label, p, mad, share))

            is_undefined = math.isnan(ratio)
            both_zero = (mad_a == 0.0 and mad_b == 0.0)
            if is_undefined != both_zero:
                mechanism_failures.append((label, p, mad_a, mad_b, ratio))
            if is_undefined:
                undefined_members.append(p)
            elif math.isinf(ratio):
                infinite_members.append(p)
            else:
                defined_values[p] = ratio

        finite_values = sorted(set(round(v, 12)
                                   for v in defined_values.values()))
        shape_rows.append({
            "shape": label,
            "undefined_members": undefined_members,
            "infinite_members": infinite_members,
            "n_undefined": len(undefined_members),
            "distinct_finite_ratios": len(finite_values),
            "finite_min": min(defined_values.values())
                          if defined_values else None,
            "finite_max": max(defined_values.values())
                          if defined_values else None,
        })

    c.check("the ratio is undefined exactly when both halves have zero MAD, "
            "on every shape and every member",
            not mechanism_failures,
            "%d shape/member cells, %d disagreements" %
            (grid_cells, len(mechanism_failures)))
    c.check("a half's MAD is exactly zero exactly when a strict majority of "
            "its samples equal its own median",
            not mad_majority_failures,
            "%d halves checked, %d disagreements" %
            (grid_cells * 2, len(mad_majority_failures)))

    step_row = shape_rows[0]
    c.check("the step channel is undefined under exactly the 16 even members "
            "- Session 50's result, re-measured here",
            step_row["undefined_members"] == even_members,
            "%d undefined" % step_row["n_undefined"])

    step_odd_values = []
    step_channel = shapes[0][1]
    for p in odd_members:
        step_odd_values.append(nr.ratio_under(step_channel, p))
    c.check("the step channel's ratio is exactly 1.0 under every odd member, "
            "which is what licenses section 4's construction",
            all(value == 1.0 for value in step_odd_values),
            "min %.12f, max %.12f" % (min(step_odd_values),
                                      max(step_odd_values)))

    patterns = {}
    for row in shape_rows:
        key = tuple(row["undefined_members"])
        patterns.setdefault(key, []).append(row["shape"])
    shapes_undefined_on_even = [row["shape"] for row in shape_rows
                               if row["undefined_members"] == even_members]
    shapes_undefined_on_odd = [row["shape"] for row in shape_rows
                              if row["undefined_members"] == odd_members]
    c.check("one shape is undefined under exactly the 16 EVEN members and "
            "another under exactly the 16 ODD members, so neither parity "
            "class is the one that fails",
            bool(shapes_undefined_on_even) and bool(shapes_undefined_on_odd),
            "even: %s; odd: %s" % (shapes_undefined_on_even or "none",
                                   shapes_undefined_on_odd or "none"))

    non_parity = [row for row in shape_rows
                  if row["undefined_members"]
                  and row["undefined_members"] != even_members
                  and row["undefined_members"] != odd_members
                  and row["undefined_members"] != members]
    c.check("and at least one shape's undefined set is not a parity class at "
            "all, so the undefined set is not indexed by parity in general",
            bool(non_parity),
            "%d such shapes of %d; %d distinct undefined patterns over the "
            "battery" % (len(non_parity), len(shape_rows), len(patterns)))

    def describe_set(values):
        """Render a member set compactly but completely.

        Inputs: `values`, a sorted list of members.
        Returns: the literal list when short, otherwise the parity name plus
        the full list, so no reader has to infer which 16 are meant.
        """
        if not values:
            return "none"
        if values == even_members:
            return "the 16 even members %s" % (values,)
        if values == odd_members:
            return "the 16 odd members %s" % (values,)
        if values == members:
            return "all 32 members"
        return "%s" % (values,)

    for row in shape_rows:
        c.note("shape %-24s undefined under %2d: %s"
               % (row["shape"], row["n_undefined"],
                  describe_set(row["undefined_members"])))
        c.note("shape %-24s +inf under %2d: %s; %d distinct defined ratios, "
               "range %s"
               % (row["shape"], len(row["infinite_members"]),
                  describe_set(row["infinite_members"]),
                  row["distinct_finite_ratios"],
                  "none" if row["finite_min"] is None
                  else "%.6f to %.6f" % (row["finite_min"],
                                         row["finite_max"])))

    member_dependent = [row for row in shape_rows
                        if row["distinct_finite_ratios"] > 1]
    widest = max(member_dependent,
                 key=lambda row: row["finite_max"] - row["finite_min"]) \
        if member_dependent else None
    c.check("at least one shape's DEFINED ratio differs across members, so "
            "the member changes the finite values and not only which ones "
            "are undefined",
            bool(member_dependent),
            "%d of %d shapes vary; widest %s" %
            (len(member_dependent), len(shape_rows),
             "none" if widest is None
             else "%s, %.6f to %.6f" % (widest["shape"], widest["finite_min"],
                                        widest["finite_max"])))
    no_undefined_but_varying = [row for row in shape_rows
                                if not row["undefined_members"]
                                and not row["infinite_members"]
                                and row["distinct_finite_ratios"] > 1]
    c.check("member dependence does not require an undefined case at all: at "
            "least one shape has NO undefined and NO infinite member and "
            "still takes several different defined ratios across members",
            bool(no_undefined_but_varying),
            "%d such shapes; widest %s" %
            (len(no_undefined_but_varying),
             "none" if not no_undefined_but_varying
             else "%s, %d distinct values from %.6f to %.6f"
             % (no_undefined_but_varying[0]["shape"],
                no_undefined_but_varying[0]["distinct_finite_ratios"],
                no_undefined_but_varying[0]["finite_min"],
                no_undefined_but_varying[0]["finite_max"])))
    straddling = [row for row in member_dependent
                  if row["finite_min"] < 1.0 < row["finite_max"]]
    c.note("WITHDRAWN EXPECTATION: I expected some shape's defined ratio to "
           "straddle 1.0 across members and wrote the check to catch it; %d "
           "of %d varying shapes do, so the expectation is withdrawn and the "
           "measurement is recorded instead"
           % (len(straddling), len(member_dependent)))
    c.check("on this battery every member-varying shape has 1.0 as one "
            "endpoint of its range - stated as a property of these fixtures, "
            "not as a general claim",
            all(row["finite_min"] == 1.0 or row["finite_max"] == 1.0
                for row in member_dependent),
            "%d varying shapes, ranges %s" %
            (len(member_dependent),
             [(row["shape"], round(row["finite_min"], 6),
               round(row["finite_max"], 6)) for row in member_dependent]))
    records["shape_rows"] = jsonable(shape_rows)
    records["undefined_set_patterns"] = dict(
        (",".join(str(p) for p in key) or "empty", value)
        for key, value in patterns.items())

    # ------------------------------------------------------------------
    c.heading("3. The completion order gives a one-way dominance, and it is "
              "the inverse of the scalar rule's (finite values held fixed)")

    c.note("every cell below is a ceteris paribus band: k channels whose "
           "ratio is undefined under one member and exactly 1.0 under the "
           "other, plus a fixed pool of 72 - k defined ratios shared by both")
    c.note("section 2 shows the shared-pool assumption is false in general; "
           "it is imposed here to isolate the effect of the undefined set")

    pool_shapes = ["flat", "tight", "biting", "onetail", "spread", "highlow",
                   "withzero"]
    bounded_counts = [0, 1, 2, 7]
    unbounded_counts = [8, 16, 72]
    outside_enclosure = []
    bounded_permissive = []
    bounded_conservative = []
    scalar_permissive = []
    scalar_conservative = []
    agree_bounded = 0
    agree_scalar = 0
    cells = 0
    grid_rows = []
    for shape in pool_shapes:
        for k in bounded_counts + unbounded_counts:
            pool = finite_pool(shape, BAND_CHANNELS - k)
            with_undefined = cb.bounds_exact(pool, k, BAND_CHANNELS)
            without = cb.rho(list(pool) + [1.0] * k, P10_RANK, P90_RANK)
            cells += 1

            # The value the member without the undefined channels computes is
            # itself one completion, so it must lie inside the enclosure.
            if without is not None and with_undefined["lo"] is not None:
                if not (with_undefined["lo"] - 1e-12 <= without
                        <= with_undefined["hi"] + 1e-12):
                    outside_enclosure.append((shape, k, without,
                                              with_undefined["lo"],
                                              with_undefined["hi"]))

            stands_with = cb.stands_down(with_undefined, M_STRICT)
            without_bound = {"lo": without, "hi": without,
                             "undefined_reachable": without is None,
                             "upper_effective": (INF if without is None
                                                 else without)}
            stands_without = cb.stands_down(without_bound, M_STRICT)
            if stands_with and not stands_without:
                bounded_permissive.append((shape, k))
            if stands_without and not stands_with:
                bounded_conservative.append((shape, k))
            if stands_with == stands_without:
                agree_bounded += 1

            scalar_with = cb.numpy_nan_rho(pool, k, BAND_CHANNELS)
            frozen_with = cb.frozen_disposition(
                SIGMA_WORST, SIGMA_QUIET, R_SPACE_BENIGN, scalar_with,
                M_STRICT)
            frozen_without = cb.frozen_disposition(
                SIGMA_WORST, SIGMA_QUIET, R_SPACE_BENIGN,
                INF if without is None else without, M_STRICT)
            if frozen_with == "passes" and frozen_without == "unmeasurable":
                scalar_permissive.append((shape, k))
            if frozen_without == "passes" and frozen_with == "unmeasurable":
                scalar_conservative.append((shape, k))
            if frozen_with == frozen_without:
                agree_scalar += 1

            grid_rows.append({
                "pool": shape, "k": k,
                "lo": with_undefined["lo"], "hi": with_undefined["hi"],
                "upper_effective": with_undefined["upper_effective"],
                "value_without_undefined": without,
                "stands_down_with_undefined": stands_with,
                "stands_down_without_undefined": stands_without,
                "frozen_with_undefined": frozen_with,
                "frozen_without_undefined": frozen_without,
            })

    c.check("the value computed by the member with no undefined channel "
            "always lies inside the other member's enclosure",
            not outside_enclosure,
            "%d cells, %d escapes" % (cells, len(outside_enclosure)))
    c.check("under the bounded rule the undefined-producing member is never "
            "the more permissive of the two",
            not bounded_permissive,
            "%d cells, %d permissive" % (cells, len(bounded_permissive)))
    c.check("under the bounded rule the undefined-producing member IS "
            "strictly more conservative on exhibited cells",
            bool(bounded_conservative),
            "%d of %d cells" % (len(bounded_conservative), cells))
    c.check("under the frozen scalar rule the same member is the PERMISSIVE "
            "one on exhibited cells - the direction flips",
            bool(scalar_permissive),
            "%d of %d cells" % (len(scalar_permissive), cells))
    c.check("but the frozen scalar rule's member disagreement has NO "
            "direction: it is permissive on some cells and conservative on "
            "others, where the bounded rule is one-way",
            bool(scalar_permissive) and bool(scalar_conservative),
            "%d permissive, %d conservative: %s" %
            (len(scalar_permissive), len(scalar_conservative),
             scalar_conservative))
    c.check("the equal count of bounded-conservative and scalar-permissive "
            "cells is a coincidence and the cells are NOT the same cells",
            set(bounded_conservative) != set(scalar_permissive),
            "%d and %d cells, %d in common" %
            (len(bounded_conservative), len(scalar_permissive),
             len(set(bounded_conservative) & set(scalar_permissive))))
    c.note("member dispositions agree on %d of %d cells under the bounded "
           "rule and on %d of %d under the frozen scalar rule"
           % (agree_bounded, cells, agree_scalar, cells))
    c.note("bounded-conservative cells: %s" % (bounded_conservative,))
    c.note("scalar-permissive cells: %s" % (scalar_permissive,))
    records["ceteris_paribus_grid"] = jsonable(grid_rows)
    records["agreement"] = {"bounded": agree_bounded, "scalar": agree_scalar,
                            "cells": cells}

    biting_pool = finite_pool("biting", BAND_CHANNELS - 7)
    biting_bound = cb.bounds_exact(biting_pool, 7, BAND_CHANNELS)
    biting_scalar = cb.numpy_nan_rho(biting_pool, 7, BAND_CHANNELS)
    biting_without = cb.rho(list(biting_pool) + [1.0] * 7, P10_RANK, P90_RANK)
    c.check("on Session 51's biting fixture the two members DISAGREE under "
            "the scalar rule and AGREE under the bounded rule",
            (biting_scalar <= M_STRICT and biting_without > M_STRICT
             and not cb.stands_down(biting_bound, M_STRICT)),
            "scalar %.6f vs %.6f; bound [%.6f, %.6f]" %
            (biting_scalar, biting_without, biting_bound["lo"],
             biting_bound["hi"]))
    records["biting"] = jsonable({
        "scalar_with_undefined": biting_scalar,
        "value_without_undefined": biting_without,
        "lo": biting_bound["lo"], "hi": biting_bound["hi"]})

    absolute = []
    for shape in pool_shapes:
        for k in unbounded_counts:
            pool = finite_pool(shape, BAND_CHANNELS - k)
            with_undefined = cb.bounds_exact(pool, k, BAND_CHANNELS)
            without = cb.rho(list(pool) + [1.0] * k, P10_RANK, P90_RANK)
            if cb.stands_down(with_undefined, M_STRICT):
                absolute.append((shape, k, "withheld member stood down"))
    flat_unbounded_split = []
    for k in unbounded_counts:
        pool = finite_pool("flat", BAND_CHANNELS - k)
        with_undefined = cb.bounds_exact(pool, k, BAND_CHANNELS)
        without = cb.rho(list(pool) + [1.0] * k, P10_RANK, P90_RANK)
        if (not cb.stands_down(with_undefined, M_STRICT)
                and without is not None and without <= M_STRICT):
            flat_unbounded_split.append(k)
    c.check("at eight or more undefined channels the undefined-producing "
            "member is withheld whatever the finite pool is",
            not absolute,
            "%d pool/count pairs, %d stood down" %
            (len(pool_shapes) * len(unbounded_counts), len(absolute)))
    c.check("and the other member can still pass there, so the disagreement "
            "becomes total and value-independent",
            flat_unbounded_split == unbounded_counts,
            "counts %s" % (flat_unbounded_split,))

    # ------------------------------------------------------------------
    c.heading("4. The three multi-member constructions, and what unanimity "
              "reduces to")

    def band_readings(channel_label, channel, pool, k):
        """Per-member bound and stand-down for one band, all 32 members.

        Inputs: `channel_label`, a name for the record; `channel`, the array
        whose ratio each member either computes or cannot; `pool`, the fixed
        defined ratios of the other 72 - k channels; `k`, how many copies of
        the channel the band holds.
        Returns: a dict keyed by member with the bound, upper_effective and
        stand-down verdict.
        """
        out = {}
        for p in members:
            ratio = nr.ratio_under(channel, p)
            if math.isnan(ratio):
                bound = cb.bounds_exact(pool, k, BAND_CHANNELS)
            else:
                values = list(pool) + [ratio] * k
                value = cb.rho(values, P10_RANK, P90_RANK)
                bound = {"lo": value, "hi": value,
                         "undefined_reachable": value is None,
                         "upper_effective": INF if value is None else value}
            out[p] = {"upper_effective": bound["upper_effective"],
                      "lo": bound["lo"], "hi": bound["hi"],
                      "stands_down": cb.stands_down(bound, M_STRICT)}
        return out

    band_channels = [("step (2 segments)", nr.step_channel()),
                     ("3 segments", segment_channel(3)),
                     ("amplitude parity", amplitude_parity_channel()),
                     ("amplitude blocks of 31", amplitude_block_channel(31)),
                     ("amplitude ramp", amplitude_ramp_channel())]
    bands = []
    for channel_label, channel in band_channels:
        for pool_shape in ["flat", "onetail", "biting"]:
            for k in [1, 7]:
                pool = finite_pool(pool_shape, BAND_CHANNELS - k)
                bands.append((channel_label, channel, pool_shape, pool, k,
                              band_readings(channel_label, channel, pool,
                                            k)))
    # One band built specifically so that member dependence acts through the
    # DEFINED ratios alone: eight copies of the ramp channel, which is never
    # undefined under any member, occupy exactly the p10 rank above a pool of
    # 1.8, so the p90/p10 ratio is 1.8 divided by a member-dependent value.
    ramp_channel = amplitude_ramp_channel()
    ramp_pool = finite_pool("eighteens", BAND_CHANNELS - 8)
    ramp_band = ("amplitude ramp", ramp_channel, "eighteens", ramp_pool, 8,
                 band_readings("amplitude ramp", ramp_channel, ramp_pool, 8))
    bands.append(ramp_band)

    order_failures = []
    unanimity_equals_worst = []
    strict_pinned_vs_unanimity = 0
    strict_pinned_vs_existential = 0
    band_rows = []
    for channel_label, channel, pool_shape, pool, k, readings in bands:
        uppers = dict((p, readings[p]["upper_effective"]) for p in members)
        unanimity = all(readings[p]["stands_down"] for p in members)
        existential = any(readings[p]["stands_down"] for p in members)
        worst_upper = max(uppers.values())
        best_upper = min(uppers.values())

        # Unanimity is exactly the verdict of the member with the largest
        # upper bound on this band; existential is that of the smallest.
        if unanimity != (worst_upper <= M_STRICT):
            unanimity_equals_worst.append((channel_label, pool_shape, k,
                                           "unanimity"))
        if existential != (best_upper <= M_STRICT):
            unanimity_equals_worst.append((channel_label, pool_shape, k,
                                           "existential"))
        for p in members:
            pinned = readings[p]["stands_down"]
            if unanimity and not pinned:
                order_failures.append((channel_label, pool_shape, k, p,
                                       "unanimity stood down, pinned did "
                                       "not"))
            if pinned and not existential:
                order_failures.append((channel_label, pool_shape, k, p,
                                       "pinned stood down, existential did "
                                       "not"))
            if pinned and not unanimity:
                strict_pinned_vs_unanimity += 1
            if existential and not pinned:
                strict_pinned_vs_existential += 1

        withheld = [p for p in members if not readings[p]["stands_down"]]
        band_rows.append({
            "channel": channel_label, "pool": pool_shape, "k": k,
            "unanimity_stands_down": unanimity,
            "existential_stands_down": existential,
            "n_members_withholding": len(withheld),
            "worst_upper": worst_upper, "best_upper": best_upper,
        })

    c.check("the three constructions are ordered: unanimity implies every "
            "pinned member, and every pinned member implies existential",
            not order_failures,
            "%d bands x 32 members, %d order violations" %
            (len(bands), len(order_failures)))
    c.check("unanimity is exactly the verdict of the member with the largest "
            "upper bound on that band, and existential of the smallest",
            not unanimity_equals_worst,
            "%d bands, %d mismatches" % (len(bands),
                                         len(unanimity_equals_worst)))
    c.check("the ordering is strict rather than an equality: some pinned "
            "member stands down where unanimity does not, and existential "
            "stands down where some pinned member does not",
            strict_pinned_vs_unanimity > 0
            and strict_pinned_vs_existential > 0,
            "of %d band x member cells, %d strict against unanimity and %d "
            "strict against existential" %
            (len(bands) * len(members), strict_pinned_vs_unanimity,
             strict_pinned_vs_existential))

    step_bands = [row for row in band_rows
                  if row["channel"] == "step (2 segments)"]
    seg3_bands = [row for row in band_rows if row["channel"] == "3 segments"]
    partial = [row for row in band_rows
               if 0 < row["n_members_withholding"] < len(members)]
    fewest = min(partial, key=lambda row: row["n_members_withholding"]) \
        if partial else None
    c.check("unanimity is withheld by as few as one member of 32, so its "
            "cost is set by the single most withholding convention rather "
            "than by agreement across the family",
            fewest is not None and fewest["n_members_withholding"] == 1,
            "fewest withholding on any partially-withholding band: %s"
            % ("none" if fewest is None
               else "%d member(s) on %s/%s/k=%d"
               % (fewest["n_members_withholding"], fewest["channel"],
                  fewest["pool"], fewest["k"])))
    c.note("%d of %d bands split the family - at least one member withholds "
           "and at least one stands down; on the rest all 32 agree"
           % (len(partial), len(band_rows)))
    c.note("step bands with at least one withholding member: %d of %d; "
           "three-segment bands: %d of %d"
           % (sum(1 for row in step_bands if row["n_members_withholding"]),
              len(step_bands),
              sum(1 for row in seg3_bands if row["n_members_withholding"]),
              len(seg3_bands)))
    for row in band_rows:
        c.note("band %-18s pool %-8s k=%d  withholding members %2d  "
               "unanimity %s  existential %s"
               % (row["channel"], row["pool"], row["k"],
                  row["n_members_withholding"],
                  "stands down" if row["unanimity_stands_down"] else "no",
                  "stands down" if row["existential_stands_down"] else "no"))
    records["multi_member_bands"] = jsonable(band_rows)

    # The member with the largest upper bound is a per-band property, so
    # "require every member to stand down" is not a member that can be
    # pinned in advance.
    worst_members = {}
    always_worst = set(members)
    for channel_label, channel, pool_shape, pool, k, readings in bands:
        uppers = dict((p, readings[p]["upper_effective"]) for p in members)
        worst = max(uppers.values())
        winners = tuple(sorted(p for p in members if uppers[p] == worst))
        worst_members.setdefault(winners, []).append(
            "%s/%s/k=%d" % (channel_label, pool_shape, k))
        always_worst &= set(winners)
    c.check("no single member has the largest upper bound on every band, so "
            "unanimity cannot be replaced by pinning one member chosen in "
            "advance",
            not always_worst,
            "%d distinct maximizing sets over %d bands; members maximal on "
            "all bands: %s" % (len(worst_members), len(bands),
                               sorted(always_worst) or "none"))
    for key, value in sorted(worst_members.items(),
                             key=lambda item: (-len(item[1]), item[0])):
        c.note("maximizing set %s sets unanimity on %d band(s), e.g. %s"
               % (describe_set(list(key)), len(value), value[0]))
    records["unanimity_setting_members"] = dict(
        (",".join(str(p) for p in key), value)
        for key, value in worst_members.items())
    records["members_maximal_on_every_band"] = sorted(always_worst)

    # ------------------------------------------------------------------
    c.heading("4.1 The completion semantics does not settle the split: the "
              "members can disagree with no undefined channel present")

    ramp_readings = ramp_band[5]
    ramp_undefined = [p for p in members
                      if math.isnan(nr.ratio_under(ramp_channel, p))]
    ramp_down = [p for p in members if ramp_readings[p]["stands_down"]]
    ramp_withheld = [p for p in members
                     if not ramp_readings[p]["stands_down"]]
    ramp_values = dict((p, ramp_readings[p]["upper_effective"])
                       for p in members)
    c.check("on this band no member's ratio is undefined, so the completion "
            "rule is never invoked and every member reports a single value",
            not ramp_undefined
            and all(not math.isinf(ramp_values[p]) for p in members),
            "%d undefined members; %d distinct reported values" %
            (len(ramp_undefined), len(set(round(ramp_values[p], 12)
                                          for p in members))))
    c.check("and the members still disagree on branch 4: some stand down and "
            "some withhold on byte-identical data, from finite-value "
            "variation alone",
            bool(ramp_down) and bool(ramp_withheld),
            "%d stand down, %d withhold; reported values %.6f to %.6f" %
            (len(ramp_down), len(ramp_withheld),
             min(ramp_values.values()), max(ramp_values.values())))
    c.check("the two sides are not a knife edge at M: every reported value "
            "is strictly away from the threshold",
            all(ramp_values[p] != M_STRICT for p in members),
            "closest approach %.6f against M = %.6f" %
            (min((abs(ramp_values[p] - M_STRICT) for p in members)),
             M_STRICT))
    undefined_fields = set(
        (len([q for q in [p]
              if math.isnan(nr.ratio_under(ramp_channel, q))]),
         bool(ramp_readings[p]["lo"] is None))
        for p in members)
    endpoint_pairs = set((round(ramp_readings[p]["lo"], 12),
                          round(ramp_readings[p]["hi"], 12))
                         for p in members)
    c.check("the undefined-specific Part-B publication fields - identity "
            "count and reachable-undefined state - are identical under all "
            "32 members here, so they do not distinguish the members",
            len(undefined_fields) == 1,
            "%d distinct undefined-field states" % len(undefined_fields))
    c.check("but the published endpoint pair DOES distinguish them, so "
            "Codex's publication set is sufficient to audit this case",
            len(endpoint_pairs) > 1,
            "%d distinct endpoint pairs over 32 members" %
            len(endpoint_pairs))
    c.note("so the disagreement here is auditable from the record rather "
           "than hidden by it, which is a point in favour of the Session-51 "
           "scope ruling rather than against it")

    # The mechanism, checked rather than asserted: the eight ramp copies hold
    # the p10 rank and the pool holds the p90 rank, so the reported value is
    # exactly 1.8 divided by the member's own ramp ratio, and branch 4 stands
    # down exactly when that ratio is at or above 1.8 / M.
    mechanism_breaks = []
    for p in members:
        ratio = nr.ratio_under(ramp_channel, p)
        expected = 1.8 / min(ratio, 1.8)
        if abs(ramp_values[p] - expected) > 1e-12:
            mechanism_breaks.append((p, ratio, ramp_values[p], expected))
        if ramp_readings[p]["stands_down"] != (min(ratio, 1.8)
                                              >= 1.8 / M_STRICT):
            mechanism_breaks.append((p, ratio, "verdict"))
    c.check("the mechanism is exactly 1.8 divided by the member's own ramp "
            "ratio, and branch 4 stands down exactly when that ratio is at "
            "or above 1.8 / M = 0.9",
            not mechanism_breaks,
            "%d members, %d departures from the mechanism" %
            (len(members), len(mechanism_breaks)))
    largest_four = sorted(members)[-4:]
    c.check("and the withholding set is NOT simply the longest block "
            "lengths: an intuition that 'more contiguous means more "
            "asymmetric' does not order these members",
            sorted(ramp_withheld) != sorted(largest_four),
            "withholding %s against the four longest %s" %
            (sorted(ramp_withheld), largest_four))
    c.note("the member's ramp ratio is what decides it, and that ratio is "
           "not monotone in block length; no causal story beyond the "
           "measured ratio is claimed here")
    c.note("ramp ratio by member: %s"
           % ([(p, round(nr.ratio_under(ramp_channel, p), 6))
               for p in sorted(members)],))
    c.note("standing down: %s" % (sorted(ramp_down),))
    c.note("withholding: %s" % (sorted(ramp_withheld),))
    records["ramp_band"] = jsonable({
        "pool": "eighteens", "k": 8,
        "undefined_members": ramp_undefined,
        "stand_down_members": sorted(ramp_down),
        "withholding_members": sorted(ramp_withheld),
        "reported_values": dict((str(p), ramp_values[p]) for p in members)})

    # ------------------------------------------------------------------
    c.heading("5. The publication surface is member-dependent")

    pub_rows = []
    asymmetric = 0
    for channel_label, channel in band_channels:
        for k in [1, 7]:
            counts = {}
            for p in members:
                ratio = nr.ratio_under(channel, p)
                counts[p] = k if math.isnan(ratio) else 0
            distinct = sorted(set(counts.values()))
            if len(distinct) > 1:
                asymmetric += 1
            pub_rows.append({
                "channel": channel_label, "k": k,
                "undefined_identities_published": distinct,
                "members_publishing_none":
                    sum(1 for p in members if counts[p] == 0),
                "members_publishing_k":
                    sum(1 for p in members if counts[p] == k)})
    c.check("on at least one band a pinned member must publish undefined "
            "channel identities where another pinned member publishes none",
            asymmetric > 0,
            "%d of %d bands asymmetric" % (asymmetric, len(pub_rows)))
    c.check("the size of that published set is decided by the member and not "
            "by the band, so two disclosed conventions on identical data "
            "publish different Part-B records",
            all(row["members_publishing_none"] > 0
                and row["members_publishing_k"] > 0
                for row in pub_rows if len(
                    row["undefined_identities_published"]) > 1),
            "%d asymmetric bands, all with both a publishing and a "
            "non-publishing member" % asymmetric)
    for row in pub_rows:
        c.note("band %-24s k=%d  published undefined counts %s; %d of 32 "
               "members publish none and %d publish %d"
               % (row["channel"], row["k"],
                  row["undefined_identities_published"],
                  row["members_publishing_none"],
                  row["members_publishing_k"], row["k"]))
    records["publication_surface"] = jsonable(pub_rows)

    # ------------------------------------------------------------------
    c.heading("6. Boundary")
    c.note("every channel and every ratio here is constructed; no candidate "
           "sample has ever been read for noise and no frequency claim is "
           "made about real recordings")
    c.note("section 3 holds the finite ratios fixed across members, which "
           "section 2 measures to be false in general; it is a ceteris "
           "paribus comparison of the undefined set alone")
    c.note("the one-way dominance rests on the imported enumeration being "
           "exact, which was proved at Session 51 for small n and "
           "independently derived by Codex at n = 72")
    c.note("this probe compares constructions; it selects no member, "
           "proposes no Part B rule, opens no Review Card and edits neither "
           "Draft 34 nor RC-008")

    records["threshold_m"] = M_STRICT
    records["band_channels"] = BAND_CHANNELS
    records["boundary"] = ("constructed channels and constructed ratio pools "
                           "only; the claims are about the split family's "
                           "behaviour under the completion semantics, not "
                           "about real recordings")

    text = c.render()
    sys.stdout.write(text)
    io.open(args.out, "w", encoding="utf-8", newline="\n").write(text)
    if args.records:
        io.open(args.records, "w", encoding="utf-8", newline="\n").write(
            json.dumps(records, indent=2, sort_keys=True) + "\n")
    return 1 if c.failed else 0


if __name__ == "__main__":
    sys.exit(main())
