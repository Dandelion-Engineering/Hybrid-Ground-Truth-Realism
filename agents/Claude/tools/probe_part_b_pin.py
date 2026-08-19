"""What the pinned split member sees, and what it is blind to.

Session 52 established that the 32-member block-interleave family disagrees on
byte-identical fully defined data, so the completion semantics does not settle
Part B. Codex answered that in Session 52 by ruling for a fixed member with a
narrowed claim: pin `p = 6510`, the unique partition whose two halves are each
one contiguous interval, and describe the statistic as an early-versus-late
disagreement diagnostic rather than a partition-invariant resolution measure.

THIS PROBE CHECKS THAT RULING RATHER THAN ACCEPTING IT, AND IT IS NOT A PART B
CANDIDATE. It selects nothing, proposes nothing, edits no section and opens no
Review Card. It establishes four things:

  1. THE UNIQUENESS IS A CLOSED FORM, NOT AN OBSERVATION. Block-interleaving a
     length-`2H` core at block length `p` produces exactly `2 * (H // p)`
     maximal runs. Two runs therefore occur only at `p = H`, and every other
     member has at least four. That is proved here over the family and then
     re-checked at four other half lengths, so the uniqueness is a property of
     block-interleaving rather than a coincidence of 6,510.

  2. GEOMETRY ALONE DOES NOT SELECT THE MEMBER; THE ESTIMAND DOES. Minimizing
     temporal fragmentation reads only the declared sample geometry and picks
     `p = 6510`. Maximizing it reads exactly the same geometry, by the same
     rule, and picks `p = 1`. Both selectors are outcome-independent, so
     "chosen from geometry alone" cannot be what privileges the midpoint. What
     privileges it is the early-versus-late estimand Codex named. This narrows
     his stated ground rather than defeating his ruling, and it matters for the
     eventual candidate because the ground is what a reader will audit.

  3. THE PIN HAS NO UNIFORM DIRECTION. On a channel whose amplitude ramps
     monotonically across the window, `p = 6510` returns the most extreme ratio
     of all 32 members and is the most withholding. On a channel whose
     amplitude alternates with sample parity it returns exactly 1.0, the most
     permissive value available, while an interleaved member returns the true
     contrast. So the pinned member is the family's most conservative choice
     against slow structure and its most permissive choice against fast
     structure. Codex observed that `p = 6510` withholds on the ramp band and
     read that as evidence the pin was not chosen for a convenient verdict;
     that reading is correct on that band and does not generalize, and the
     opposite band is exhibited here.

  4. THE PINNED MEMBER IS BLIND TO A WHOLE FREQUENCY FAMILY, AND SO ARE EXACTLY
     THE FIFTEEN OTHER EVEN MEMBERS. Section 19.5 already records that a signal
     periodic at the half length makes the two contiguous halves bit-identical.
     That generalizes: for a core built by repeating one half-length period,
     half A and half B hold the same multiset of samples under a member exactly
     when `6510 / p` is odd, which is exactly when `p` is even. Sixteen members
     return exactly 1.0 on such a channel and sixteen do not, and the pinned
     member is one of the blind sixteen. This is a non-transfer boundary the
     eventual candidate has to publish, and it is exhibited rather than argued.

  5. TWO OF CODEX'S ELEVEN CHECKS CANNOT FAIL. His probe writes the existential
     rule as `min(values) <= M` and compares it against `any(v <= M)`, and the
     unanimity rule as `max(values) <= M` against `all(v <= M)`. Both sides of
     each comparison are computed from the same vector by mathematically
     equivalent expressions, so the comparison holds for every input and has no
     discriminating power over his. That is demonstrated here on random vectors
     that have nothing to do with the split family. THE UNDERLYING CLAIM IS
     TRUE AND IS NOT IN QUESTION: Session 52 established the same identity over
     30 constructed bands with zero mismatches, computing the two sides from
     different objects, which is what makes that version a test.

NO FORMAL REVIEW HAS SEEN THIS PROBE. It was written outside the review cycle,
as open-ended co-design input for a Part B that has no candidate and no Review
Card. Its findings are evidence for that design conversation and are not an
approved state of anything.

BOUNDARY. Every channel here is constructed. No candidate sample has ever been
read for noise, and nothing here says how often any of these shapes occurs in a
real recording, how much power a real band carries at the blind frequencies, or
whether a real host would be affected at all. The direction results are
statements about which member is extreme on an exhibited fixture, not about
which member is safer. Nothing here reads the archive, the network or any
project record beyond the three authenticated probe sources it imports, and
nothing here reopens RC-008 or edits Draft 34.

Usage:

    ./venv/Scripts/python.exe \\
        agents/Claude/tools/probe_part_b_pin.py \\
        --out <path> [--records <path>]
"""

import argparse
import hashlib
import importlib.util
import json
import os

import numpy as np

RETAINED = 13020
HALF = RETAINED // 2
BAND_CHANNELS = 72
M_STRICT = 2.0
P10_RANK = 8
P90_RANK = 65

# Benign level statistics, so branches 1 and 2 of section 19.6 never fire and
# the comparison isolates the branch this section's split rule reaches.
SIGMA_WORST = 5.0
SIGMA_QUIET = 3.0

# The member Codex ruled for, named once so no check can drift off it.
PINNED_MEMBER = HALF

# The three probe sources this check is graded by, authenticated before import
# so that the semantics is exactly what Session 50-52 proved and Codex replayed
# rather than a re-typed copy. Editing any of them breaks this probe by design.
PINNED_SOURCES = {
    "probe_completion_bounds.py":
        "2c1c78beaf7345edf91e8393df70b8d049bfa0b462684c3463053b5431afddec",
    "probe_null_ratio_undefined.py":
        "4d21c7578011c0f01b956fbed10a670ff78cbc34c46d6c3c061dbcc8fc63eb66",
    "probe_member_comparison.py":
        "b653bc0c214f6a0c419489bafde244185d4bd61acc882b64e9edd2baa75a6f42",
}

# Section 19.5's own worked frequency: m = 87 gives 400.921659 Hz at the
# nominal 30,000 Hz, an exact number of cycles in 6,510 samples.
PERIODIC_M = 87
NOMINAL_RATE = 30000.0


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
    """Check the pinned digests of the three imported probe sources.

    Inputs: `here`, the directory holding this script and all three sources.
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


def load_module(here, name):
    """Import one already-authenticated probe source by path.

    Inputs: `here`, the directory holding it; `name`, its filename.
    Returns: the imported module object.
    """
    spec = importlib.util.spec_from_file_location(
        name[:-3], os.path.join(here, name))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def divisors_by_factorization(factors):
    """Every divisor of a product of distinct primes, ascending.

    Inputs: `factors`, the list of distinct prime factors.
    Returns: the sorted divisor list.

    Deliberately a different code path from the trial division the imported
    probes use, so that agreement between the two is agreement between two
    derivations rather than a reproduction of one.
    """
    out = [1]
    for prime in factors:
        out = out + [value * prime for value in out]
    return sorted(out)


def labels_for(member, retained=RETAINED):
    """The declared block-interleave half labels of one member.

    Inputs: `member`, the block length `p`; `retained`, the core length.
    Returns: an integer array where 0 marks half A and 1 marks half B.
    """
    return (np.arange(retained) // member) % 2


def run_count(labels):
    """Number of maximal constant runs in a label sequence.

    Inputs: `labels`, a one-dimensional integer array.
    Returns: the run count as an int.
    """
    labels = np.asarray(labels)
    return int(1 + np.count_nonzero(labels[1:] != labels[:-1]))


def runs_of_label(labels, target):
    """Number of maximal runs carrying one particular label.

    Inputs: `labels`, a one-dimensional integer array; `target`, the label.
    Returns: the run count as an int.
    """
    labels = np.asarray(labels)
    hit = labels == target
    if not hit.any():
        return 0
    starts = np.count_nonzero(hit[1:] & ~hit[:-1])
    return int(starts + (1 if hit[0] else 0))


def select_min_fragmentation(members, retained=RETAINED):
    """Members with the fewest temporal runs.

    Inputs: `members`, the family; `retained`, the core length.
    Returns: the sorted list of minimizing members. Reads no signal value: its
    only arguments are the declared family and the declared core length.
    """
    counts = {p: run_count(labels_for(p, retained)) for p in members}
    best = min(counts.values())
    return sorted(p for p in members if counts[p] == best)


def select_max_fragmentation(members, retained=RETAINED):
    """Members with the most temporal runs.

    Inputs: `members`, the family; `retained`, the core length.
    Returns: the sorted list of maximizing members. Reads no signal value, by
    exactly the same standard as `select_min_fragmentation`.
    """
    counts = {p: run_count(labels_for(p, retained)) for p in members}
    worst = max(counts.values())
    return sorted(p for p in members if counts[p] == worst)


def parity_scaled_channel(even_scale, odd_scale):
    """Section 19.5's own construction: amplitude set by sample parity.

    Inputs: `even_scale` and `odd_scale`, the amplitudes carried at even and
    odd sample indices.
    Returns: the channel, whose sign alternates every two samples so that each
    parity class varies on its own and neither half can collapse to zero MAD.

    The obvious way to build a parity contrast - one amplitude on even samples
    and another on odd ones, with the sign alternating every sample - makes
    each parity class constant, so the even/odd member sees 0/0 and returns
    nothing at all. That version is checked in section 3 and is exactly why
    this one exists.
    """
    index = np.arange(RETAINED)
    sign = np.where((index // 2) % 2 == 0, 1.0, -1.0)
    scale = np.where(index % 2 == 0, float(even_scale), float(odd_scale))
    return sign * scale


def periodic_channel(m=PERIODIC_M, tiled=True):
    """A channel periodic at the half length, at m cycles per half.

    Inputs: `m`, the cycle count in 6,510 samples; `tiled`, whether to build
    the core by repeating one exact period.
    Returns: the channel.

    At `m = 87` the frequency is `m * 30000 / 6510 = 400.921659` Hz, which is
    section 19.5's own worked example. Tiling makes the two contiguous halves
    bit-identical by construction; evaluating the sinusoid across the whole
    core instead makes them identical only to floating-point tolerance, and
    both forms are checked.
    """
    if tiled:
        period = np.sin(2.0 * np.pi * m * np.arange(HALF) / float(HALF))
        return np.tile(period, 2)
    return np.sin(2.0 * np.pi * m * np.arange(RETAINED) / float(HALF))


def halves_hold_same_multiset(channel, member):
    """Whether both halves of one member hold the same multiset of samples.

    Inputs: `channel`, the sample array; `member`, the block length.
    Returns: True when the sorted halves are elementwise equal.
    """
    mask = labels_for(member) == 0
    return bool(np.array_equal(np.sort(channel[mask]),
                               np.sort(channel[~mask])))


def band_from_ratios(ratios):
    """Sort one window's per-channel ratios into the published order.

    Inputs: `ratios`, the per-channel `r_c(k)` values.
    Returns: the sorted list, which is what the nearest-rank percentiles read.
    """
    return sorted(float(value) for value in ratios)


def jsonable(value):
    """Convert numpy scalars and containers into JSON-serializable values.

    Inputs: `value`, any nested structure.
    Returns: the same structure with numpy types replaced by Python types.
    """
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def parse_args(argv=None):
    """Parse the command line.

    Inputs: `argv`, an optional argument list.
    Returns: the parsed namespace.
    """
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", required=True,
                        help="path for the plain-text report")
    parser.add_argument("--records", default=None,
                        help="optional path for the JSON record")
    parser.add_argument("--random-vectors", type=int, default=2000,
                        help="how many random vectors the identity "
                             "demonstration in section 5 uses")
    return parser.parse_args(argv)


def main(argv=None):
    """Run every check, print the report and write the artifacts."""
    args = parse_args(argv)
    here = os.path.dirname(os.path.abspath(__file__))
    measured = authenticate_sources(here)
    undef = load_module(here, "probe_null_ratio_undefined.py")
    bounds = load_module(here, "probe_completion_bounds.py")
    member_probe = load_module(here, "probe_member_comparison.py")

    checks = Checks()
    records = {"authenticated_sources": measured,
               "pinned_member": PINNED_MEMBER,
               "retained_samples": RETAINED,
               "threshold_m": M_STRICT}

    # ------------------------------------------------------------------
    checks.heading("1. The uniqueness of the contiguous member is a closed "
                   "form")

    members = divisors_by_factorization([2, 3, 5, 7, 31])
    imported_members = undef.divisors(HALF)
    checks.check("an independent factorization of 6,510 gives the same "
                 "32-member family as the authenticated trial division",
                 members == imported_members and len(members) == 32,
                 "%d members, %d ... %d" %
                 (len(members), members[0], members[-1]))

    geometry = []
    for member in members:
        labels = labels_for(member)
        geometry.append({
            "member": member,
            "half_a_samples": int(np.count_nonzero(labels == 0)),
            "half_b_samples": int(np.count_nonzero(labels == 1)),
            "total_runs": run_count(labels),
            "runs_half_a": runs_of_label(labels, 0),
            "runs_half_b": runs_of_label(labels, 1),
            "closed_form_runs": 2 * (HALF // member),
        })
    records["geometry"] = geometry

    checks.check("every member splits the retained core into two halves of "
                 "6,510 samples",
                 all(row["half_a_samples"] == HALF
                     and row["half_b_samples"] == HALF for row in geometry),
                 "%d samples per half" % HALF)
    checks.check("the measured run count equals the closed form 2 * (6510 / p) "
                 "for every member",
                 all(row["total_runs"] == row["closed_form_runs"]
                     for row in geometry),
                 "32 of 32 agree")
    two_run = [row["member"] for row in geometry if row["total_runs"] == 2]
    checks.check("exactly one member has two runs and it is p = 6510",
                 two_run == [PINNED_MEMBER],
                 "two-run members %s" % two_run)
    contiguous = [row["member"] for row in geometry
                  if row["runs_half_a"] == 1 and row["runs_half_b"] == 1]
    checks.check("both halves are a single contiguous interval for exactly "
                 "that one member",
                 contiguous == [PINNED_MEMBER],
                 "contiguous members %s" % contiguous)
    others = [row["total_runs"] for row in geometry
              if row["member"] != PINNED_MEMBER]
    checks.check("every other member fragments the window into at least four "
                 "alternating runs",
                 min(others) == 4 and all(value >= 4 for value in others),
                 "smallest other run count %d, largest %d" %
                 (min(others), max(others)))

    # The closed form is what makes this a proof rather than an observation,
    # so it is re-checked at half lengths that have nothing to do with 6,510.
    other_halves = [30, 100, 210, 1024]
    generalizes = []
    for half in other_halves:
        family = [d for d in range(1, half + 1) if half % d == 0]
        counts = {p: run_count(labels_for(p, 2 * half)) for p in family}
        minimal = sorted(p for p in family
                         if counts[p] == min(counts.values()))
        generalizes.append({"half": half,
                            "unique_two_run_member": minimal,
                            "matches_half": minimal == [half],
                            "closed_form_holds":
                                all(counts[p] == 2 * (half // p)
                                    for p in family)})
    records["closed_form_generalization"] = generalizes
    checks.check("the same closed form and the same uniqueness hold at four "
                 "other half lengths",
                 all(row["matches_half"] and row["closed_form_holds"]
                     for row in generalizes),
                 "half lengths %s" % other_halves)

    # ------------------------------------------------------------------
    checks.heading("2. Geometry alone does not select the member")

    minimizers = select_min_fragmentation(members)
    maximizers = select_max_fragmentation(members)
    checks.check("the minimum-fragmentation selector chooses p = 6510 and "
                 "nothing else",
                 minimizers == [PINNED_MEMBER],
                 "minimizers %s" % minimizers)
    checks.check("the maximum-fragmentation selector chooses p = 1 and "
                 "nothing else",
                 maximizers == [1],
                 "maximizers %s at %d runs" %
                 (maximizers, run_count(labels_for(1))))
    checks.check("both selectors read only the declared family and core "
                 "length, so both are outcome-independent",
                 select_min_fragmentation(members) == minimizers
                 and select_max_fragmentation(members) == maximizers,
                 "neither takes a channel argument")
    checks.check("two outcome-independent geometry selectors therefore "
                 "disagree, so geometry alone does not privilege the midpoint",
                 minimizers != maximizers,
                 "%s versus %s" % (minimizers, maximizers))
    checks.note("what privileges p = 6510 is the early-versus-late estimand, "
                "not the fact that the selector avoids reading data; the "
                "eventual candidate should carry the estimand as the ground")
    records["selectors"] = {"minimum_fragmentation": minimizers,
                            "maximum_fragmentation": maximizers}

    # ------------------------------------------------------------------
    checks.heading("3. What the pinned member sees, and what it cannot see")

    shapes = {
        "amplitude_ramp": member_probe.amplitude_ramp_channel(),
        "amplitude_parity": member_probe.amplitude_parity_channel(),
        "parity_scaled_high": parity_scaled_channel(2.0, 1.0),
        "parity_scaled_low": parity_scaled_channel(1.0, 2.0),
        "parity_flat": undef.alternating_channel(1.0),
        "two_segment_step": member_probe.segment_channel(2),
        "periodic_tiled": periodic_channel(tiled=True),
        "periodic_direct": periodic_channel(tiled=False),
    }
    per_shape = {}
    for name, channel in shapes.items():
        values = {}
        for member in members:
            values[member] = undef.ratio_under(channel, member)
        defined = {p: v for p, v in values.items() if np.isfinite(v)}
        per_shape[name] = {
            "values": {str(p): v for p, v in values.items()},
            "undefined_members": sorted(p for p, v in values.items()
                                        if np.isnan(v)),
            "infinite_members": sorted(p for p, v in values.items()
                                       if np.isinf(v)),
            "pinned_value": values[PINNED_MEMBER],
            "n_distinct_defined": len({round(v, 12)
                                       for v in defined.values()}),
        }
    records["per_shape"] = per_shape

    ramp = per_shape["amplitude_ramp"]["values"]
    ramp_values = {int(p): v for p, v in ramp.items()}
    ramp_min = min(ramp_values.values())
    ramp_argmin = sorted(p for p, v in ramp_values.items() if v == ramp_min)
    checks.check("on a monotone amplitude ramp the pinned member returns the "
                 "smallest ratio of all 32, so it is the most extreme member",
                 ramp_argmin == [PINNED_MEMBER],
                 "minimum %.6f at %s" % (ramp_min, ramp_argmin))
    checks.check("on the same ramp the even/odd member returns a ratio at or "
                 "very near 1.0, so it is nearly blind to monotone structure",
                 abs(ramp_values[1] - 1.0) < 1e-9,
                 "p=1 ratio %.12f" % ramp_values[1])

    # An expectation of mine that failed on this probe's first run, kept as a
    # check because the negative is what forced the construction below.
    parity = {int(p): v
              for p, v in per_shape["amplitude_parity"]["values"].items()}
    odd_members = sorted(p for p in members if p % 2 == 1)
    even_members = sorted(p for p in members if p % 2 == 0)
    checks.check("on the simplest parity channel no member returns a finite "
                 "contrast at all: the sixteen odd members are undefined and "
                 "the sixteen even members return exactly 1.0",
                 per_shape["amplitude_parity"]["undefined_members"]
                 == odd_members
                 and all(parity[p] == 1.0 for p in even_members),
                 "16 undefined, 16 at exactly 1.0")
    checks.note("that shape therefore cannot demonstrate fast-structure "
                "sensitivity, because each parity class is constant and the "
                "member that would separate them sees 0/0; the scaled "
                "construction below is section 19.5's own answer to that")

    scaled_high = {int(p): v
                   for p, v in per_shape["parity_scaled_high"]["values"].items()}
    scaled_min = min(scaled_high.values())
    scaled_argmin = sorted(p for p, v in scaled_high.items()
                           if v == scaled_min)
    checks.check("on a parity channel that varies within each parity class "
                 "the pinned member returns exactly 1.0",
                 scaled_high[PINNED_MEMBER] == 1.0,
                 "p=6510 ratio %.12f" % scaled_high[PINNED_MEMBER])
    checks.check("on that same channel the even/odd member returns the "
                 "underlying 2:1 contrast instead",
                 abs(scaled_high[1] - 2.0) < 1e-12,
                 "p=1 ratio %.12f" % scaled_high[1])
    checks.check("so the pinned member is among the minimizers there, having "
                 "been the unique minimizer on the ramp",
                 PINNED_MEMBER in scaled_argmin,
                 "minimum %.6f at %d members" %
                 (scaled_min, len(scaled_argmin)))

    step = {int(p): v
            for p, v in per_shape["two_segment_step"]["values"].items()}
    step_undefined = per_shape["two_segment_step"]["undefined_members"]
    checks.check("the pinned member is one of the members whose ratio is "
                 "undefined on a mid-window step, so the completion rule is "
                 "live for it and not optional",
                 PINNED_MEMBER in step_undefined,
                 "%d undefined members" % len(step_undefined))
    checks.check("the even/odd member is defined on that same step channel",
                 np.isfinite(step[1]),
                 "p=1 ratio %.12f" % step[1])

    tiled = {int(p): v
             for p, v in per_shape["periodic_tiled"]["values"].items()}
    blind = sorted(p for p, v in tiled.items() if v == 1.0)
    checks.check("on a channel periodic at the half length exactly the sixteen "
                 "even members return exactly 1.0",
                 blind == even_members,
                 "%d blind members" % len(blind))
    checks.check("the pinned member is one of those blind members",
                 PINNED_MEMBER in blind,
                 "p=6510 ratio %.12f" % tiled[PINNED_MEMBER])
    multiset_equal = sorted(p for p in members
                            if halves_hold_same_multiset(
                                shapes["periodic_tiled"], p))
    checks.check("the mechanism is that both halves hold the same multiset "
                 "exactly when 6510 / p is odd, which is exactly when p is "
                 "even",
                 multiset_equal == even_members
                 and all((HALF // p) % 2 == 1 for p in even_members),
                 "%d members with equal half multisets" % len(multiset_equal))
    direct = {int(p): v
              for p, v in per_shape["periodic_direct"]["values"].items()}
    checks.check("evaluating the same sinusoid across the whole core instead "
                 "of tiling it agrees with the tiled form to floating point",
                 abs(direct[PINNED_MEMBER] - 1.0) < 1e-9,
                 "direct p=6510 ratio %.12f, %.6f Hz" %
                 (direct[PINNED_MEMBER],
                  PERIODIC_M * NOMINAL_RATE / float(HALF)))
    checks.note("no claim is made here about how much power a real band "
                "carries at those frequencies; section 19.5 records the same "
                "family and this probe only partitions the members by it")

    # ------------------------------------------------------------------
    checks.heading("4. The pin has no uniform direction at the decision")

    # Two 72-channel bands. The first is Session 52's ramp band: eight copies
    # of the ramp channel above a pool at 1.8. The second is section 19.5's
    # own construction, eight channels at 2:1, fifty-six at 1:1 and eight at
    # 1:2, which the frozen text says gives exactly 4 under an interleaved
    # split and exactly 1 under the contiguous one. Section 19.6's branches 1
    # and 2 are held benign so the split rule is what decides.
    band_channels = {
        "ramp": ([shapes["amplitude_ramp"]] * 8
                 + [None] * 64),
        "parity": ([shapes["parity_scaled_high"]] * 8
                   + [shapes["parity_flat"]] * 56
                   + [shapes["parity_scaled_low"]] * 8),
    }
    band_results = {}
    for name in ("ramp", "parity"):
        per_member = {}
        for member in members:
            ratios = []
            for channel in band_channels[name]:
                if channel is None:
                    ratios.append(1.8)
                else:
                    ratios.append(undef.ratio_under(channel, member))
            ordered = band_from_ratios(
                [value for value in ratios if not np.isnan(value)])
            u = sum(1 for value in ratios if np.isnan(value))
            finite = [value for value in ordered if np.isfinite(value)]
            u_total = u + (len(ordered) - len(finite))
            bound = bounds.bounds_exact(sorted(finite), u_total, BAND_CHANNELS)
            verdict, label = bounds.disposition(
                SIGMA_WORST, SIGMA_QUIET, member_probe.R_SPACE_BENIGN,
                bound, M_STRICT)
            per_member[member] = {
                "scalar_spread": undef.spread(ratios) if u_total == 0
                                 else None,
                "undefined_channels": u_total,
                "upper": bound["upper_effective"],
                "disposition": verdict,
                "label": label,
            }
        band_results[name] = {str(p): row for p, row in per_member.items()}
        stand_down = sorted(p for p, row in per_member.items()
                            if row["disposition"] == "passes")
        withhold = sorted(p for p, row in per_member.items()
                          if row["disposition"] == "unmeasurable")
        band_results[name + "_summary"] = {
            "stand_down": stand_down, "withhold": withhold,
            "pinned_disposition": per_member[PINNED_MEMBER]["disposition"]}
    records["bands"] = band_results

    ramp_summary = band_results["ramp_summary"]
    parity_summary = band_results["parity_summary"]
    parity_rows = band_results["parity"]
    checks.check("the parity band reproduces the two numbers frozen section "
                 "19.5 publishes for it: exactly 4 under the even/odd member "
                 "and exactly 1 under the contiguous one",
                 parity_rows["1"]["scalar_spread"] == 4.0
                 and parity_rows[str(PINNED_MEMBER)]["scalar_spread"] == 1.0,
                 "p=1 gives %.6f, p=6510 gives %.6f" %
                 (parity_rows["1"]["scalar_spread"],
                  parity_rows[str(PINNED_MEMBER)]["scalar_spread"]))
    checks.check("on the ramp band the pinned member withholds while other "
                 "members stand down",
                 ramp_summary["pinned_disposition"] == "unmeasurable"
                 and len(ramp_summary["stand_down"]) > 0,
                 "%d stand down, %d withhold" %
                 (len(ramp_summary["stand_down"]),
                  len(ramp_summary["withhold"])))
    checks.check("on the parity band the pinned member stands down while other "
                 "members withhold",
                 parity_summary["pinned_disposition"] == "passes"
                 and len(parity_summary["withhold"]) > 0,
                 "%d stand down, %d withhold" %
                 (len(parity_summary["stand_down"]),
                  len(parity_summary["withhold"])))
    checks.check("so the pinned member is strictly more withholding than some "
                 "member on one band and strictly less on another",
                 PINNED_MEMBER in ramp_summary["withhold"]
                 and PINNED_MEMBER in parity_summary["stand_down"],
                 "no uniform direction over these two bands")
    checks.note("both bands are constructed to separate the members and "
                "neither is a claim about a real recording; what they "
                "establish is that no direction may be asserted for the pin")

    # ------------------------------------------------------------------
    checks.heading("5. The discriminating power of the two extremal "
                   "identities")

    rng = np.random.default_rng(20260819)
    n_vectors = int(args.random_vectors)
    existential_agree = 0
    unanimity_agree = 0
    regimes = {"all_below": 0, "all_above": 0, "straddling": 0}
    # A third of the vectors are drawn wholly below `M`, a third wholly above
    # and a third across it, so the demonstration covers the regime where the
    # two rules agree as well as the regime where they disagree.
    for index in range(n_vectors):
        which = index % 3
        if which == 0:
            values = rng.uniform(0.1, M_STRICT - 0.05, size=32)
        elif which == 1:
            values = rng.uniform(M_STRICT + 0.05, 9.0, size=32)
        else:
            values = rng.uniform(0.1, 9.0, size=32)
        low = float(values.min())
        high = float(values.max())
        if high <= M_STRICT:
            regimes["all_below"] += 1
        elif low > M_STRICT:
            regimes["all_above"] += 1
        else:
            regimes["straddling"] += 1
        if (low <= M_STRICT) == bool(np.any(values <= M_STRICT)):
            existential_agree += 1
        if (high <= M_STRICT) == bool(np.all(values <= M_STRICT)):
            unanimity_agree += 1
    checks.check("min(v) <= M and any(v <= M) agree on every random vector, "
                 "including vectors that are not member values at all",
                 existential_agree == n_vectors,
                 "%d of %d" % (existential_agree, n_vectors))
    checks.check("max(v) <= M and all(v <= M) agree on every random vector "
                 "by the same identity",
                 unanimity_agree == n_vectors,
                 "%d of %d" % (unanimity_agree, n_vectors))
    checks.check("the demonstration covers all three regimes, so the "
                 "agreement is not an artifact of only easy or only hard "
                 "vectors",
                 all(count > 0 for count in regimes.values()),
                 "%d below, %d above, %d straddling" %
                 (regimes["all_below"], regimes["all_above"],
                  regimes["straddling"]))
    records["identity_demonstration"] = {
        "n_vectors": n_vectors,
        "existential_agreements": existential_agree,
        "unanimity_agreements": unanimity_agree,
        "regimes": regimes,
    }
    checks.note("the two checks written that way in "
                "agents/Codex/tools/probe_part_b_policy.py therefore cannot "
                "fail on any input; the claim they state is true and was "
                "established at Session 52 over 30 bands with the two sides "
                "computed from different objects")

    report = checks.render()
    print(report, end="")
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(report)
    if args.records:
        with open(args.records, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(jsonable(records), handle, indent=2, sort_keys=True)
            handle.write("\n")
    return 1 if checks.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
