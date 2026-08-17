"""Tests for the missing-depth sensitivity bounds around the band drift gate.

``Reproducibility Packet/scripts/utils/missing_depth.py`` decides whether a
host candidate's drift verdict survives every completion of the depths the
archive could not supply. A bound that is too narrow would pass a candidate
some completion would have failed, so the cases here are written to attack
narrowness first and only then to check that the bound is useful.

The shape of the evidence:

* ``median_interval_*`` -- the bin-level interval is claimed to be **exact**,
  so it is checked against brute-force enumeration of completions rather than
  against a looser bound: every completion's median lands inside it, both
  endpoints are attained by a real finite completion, and the zero-missing case
  reproduces ``numpy.median`` exactly. A bin whose depths are all missing is
  unbounded on both sides, which is that bin's exact attainable set.
* ``split_unit_*`` -- the module takes the complete record with NaN at the
  missing depths, so the missing samples' positions are input rather than
  reconstruction. The cases check that the split preserves order, that it
  survives spikes that share a time exactly, that an infinite depth raises
  rather than being read as missing, and that a non-finite spike time raises.
* ``pipeline_bound_contains_every_completion`` -- above the bin level the bound
  is an outer bound, and the property that matters is containment. Random bands
  are completed hundreds of times, each completion is run through the approved
  ``measure_band_drift``, and its ``Delta_10min`` must land inside the bound
  every time. Completion values are deliberately drawn far outside the observed
  depth range as well as inside it.
* ``null_bound_contains_approved_null`` -- the same property for the gate's
  second number, and the one this file exists to check hardest. The bound is
  claimed to be assumption-free: the approved null's permutation depends only
  on its seed and on the analysed spike *count*, which no completion changes,
  so the unknown values can be followed to their destination bins. The test is
  therefore direct rather than against a restatement of the definition: real
  completions are built, ``band_drift.permutation_null`` is run on each
  completed record exactly as the gate would run it, and its ``Q95_null`` must
  land inside ``null_interval``'s bound every time.
* ``null_rejects_bad_rows`` -- the row-index contract is the null's seed input,
  so it is validated exactly as ``band_drift.permutation_null`` validates it.
* ``codex_support_passing_counterexample`` -- the construction that defeated the
  first proposed disposition: 1,000 finite depths per bin split at 0 and 100 um
  with one missing depth, which passes every support floor at 0.0999%
  missingness while admitting 0 um and 100 um. **It also records a correction.**
  That construction was offered as evidence that the existing gate can accept a
  candidate whose missing depths decide it, and it was run through
  ``measure_band_drift`` alone. The gate is two numbers, and its second one
  already rejects this fixture: an exactly balanced bin has a knife-edge
  median, so permuting each unit's depths swings every bin median the full
  100 um and the null's 95th percentile lands at 100 um against a 20 um
  tolerance. The case asserts that rejection rather than the claim the
  construction was made for.
* ``gate_passing_counterexample`` -- the construction that survives that
  correction, and the one this module exists for. Fifteen units, depths drawn
  uniformly across 300 um so no bin median is knife-edge, and a block of
  missing depths in every bin. The observed record clears **both** gate numbers
  at the strict tolerance -- nothing in the approved pipeline objects to it --
  and the missing depths still admit an excursion above 70 um. The asymmetry
  that makes it possible: the band trace is a median across units, so
  independent per-unit resampling noise shrinks with the unit count and the
  null stays narrow, while a block of missing depths shifts every unit's median
  in the same direction at once and does not shrink.
* ``small_missingness_still_passes`` -- the mirror. A bound that called every
  candidate unstable would be as useless as no bound, so the same fixture at a
  twentieth of the missingness must come back a stable pass.
* ``zero_missing_reproduces_estimator`` -- a sensitivity layer that changes the
  answer on data with no missingness is a defect in the layer. Both the
  observation and the null must reproduce the approved estimator value for
  value, elementwise across every replicate.
* ``unbounded_bin_is_reported`` -- when half a bin is missing the interval is
  genuinely unbounded, and the layer must say so and refuse a disposition
  rather than produce a finite-looking number.
* ``support_invariance_*`` -- the three floors, one case each, plus a unit whose
  depths are wholly missing. Each must make the candidate unmeasurable rather
  than quietly changing the included set.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Claude/tools/test_missing_depth.py"
"""

import argparse
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))),
    "Reproducibility Packet", "scripts"))

from utils import band_drift as bd  # noqa: E402
from utils import missing_depth as md  # noqa: E402

FIXTURE_SEED = 20260816
RESULTS = []


def check(name, condition, detail=""):
    """Record one assertion's outcome and print it.

    Args:
        name: the case name.
        condition: the boolean being asserted.
        detail: text printed alongside, whether it passed or failed.

    Returns:
        bool: the condition, so a caller can branch on it.
    """
    RESULTS.append((name, bool(condition), detail))
    print("  %-52s %s%s" % (name, "ok" if condition else "FAIL",
                            ("  " + detail) if detail else ""))
    return bool(condition)


def brute_force_median_range(values, n_missing, probes):
    """Enumerate completions and return the extreme medians they produce.

    Args:
        values: the finite depths in one bin.
        n_missing: how many depths are missing from that bin.
        probes: candidate completion values to draw from, with repetition.

    Returns:
        tuple: ``(lowest, highest)`` median over every enumerated completion.
    """
    finite = list(values)
    lowest, highest = np.inf, -np.inf
    for combo in itertools.combinations_with_replacement(probes, n_missing):
        value = float(np.median(np.asarray(finite + list(combo), dtype=np.float64)))
        lowest = min(lowest, value)
        highest = max(highest, value)
    return lowest, highest


def case_median_interval_matches_brute_force():
    """The bin-level interval is the attainable set, not an outer bound."""
    print("median_interval_matches_brute_force")
    rng = np.random.default_rng(FIXTURE_SEED)
    worst_gap = 0.0
    cases = 0
    for n in (1, 2, 3, 4, 5, 8, 11):
        for k in (1, 2, 3):
            for trial in range(6):
                values = np.round(rng.normal(0.0, 40.0, size=n), 3)
                spread = float(values.max() - values.min()) + 1.0
                probes = np.concatenate([
                    values,
                    values + 1e-6,
                    values - 1e-6,
                    [values.min() - spread, values.max() + spread, 0.0],
                ])
                lo, hi = md.median_interval(values, k)
                brute_lo, brute_hi = brute_force_median_range(values, k, probes)
                cases += 1
                if not np.isfinite(lo) or not np.isfinite(hi):
                    continue
                if brute_lo < lo - 1e-9 or brute_hi > hi + 1e-9:
                    check("containment n=%d k=%d trial=%d" % (n, k, trial), False,
                          "brute [%.6f, %.6f] escapes [%.6f, %.6f]"
                          % (brute_lo, brute_hi, lo, hi))
                    return
                worst_gap = max(worst_gap,
                                abs(brute_lo - lo), abs(brute_hi - hi))
    check("every enumerated completion lies inside the interval", True,
          "%d parameter cases" % cases)
    check("both endpoints are attained by a finite completion", worst_gap < 1e-9,
          "largest endpoint slack %.3e um" % worst_gap)


def case_median_interval_zero_missing():
    """With nothing missing the interval collapses onto numpy.median."""
    print("median_interval_zero_missing")
    rng = np.random.default_rng(FIXTURE_SEED + 1)
    worst = 0.0
    for n in range(1, 40):
        values = rng.normal(120.0, 30.0, size=n)
        lo, hi = md.median_interval(values, 0)
        worst = max(worst, abs(lo - float(np.median(values))),
                    abs(hi - float(np.median(values))))
    check("k=0 gives a degenerate interval at the median", worst == 0.0,
          "largest deviation %.3e um over n=1..39" % worst)


def case_median_interval_unbounded():
    """A bin more than half missing has no bound on the side it can reach."""
    print("median_interval_unbounded")
    values = np.array([10.0, 11.0, 12.0], dtype=np.float64)
    lo3, hi3 = md.median_interval(values, 3)
    lo10, hi10 = md.median_interval(values, 10)
    lo2, hi2 = md.median_interval(values, 2)
    check("k=3 against n=3 is unbounded on both sides",
          lo3 == -np.inf and hi3 == np.inf, "[%r, %r]" % (lo3, hi3))
    check("k=10 against n=3 is unbounded on both sides",
          lo10 == -np.inf and hi10 == np.inf, "[%r, %r]" % (lo10, hi10))
    check("k=2 against n=3 stays bounded",
          np.isfinite(lo2) and np.isfinite(hi2), "[%.3f, %.3f]" % (lo2, hi2))
    # A destination bin can receive every one of its values from the missing
    # set once the null permutes them, and then every real number is attainable.
    lo_all, hi_all = md.median_interval(np.empty(0), 4)
    check("a wholly missing bin is unbounded on both sides",
          lo_all == -np.inf and hi_all == np.inf, "[%r, %r]" % (lo_all, hi_all))


def case_median_interval_rejects_bad_input():
    """The interval takes the finite depths only and a non-negative count."""
    print("median_interval_rejects_bad_input")
    for name, args in (("empty bin with nothing missing", ([], 0)),
                       ("non-finite value", ([1.0, np.nan], 1)),
                       ("negative count", ([1.0, 2.0], -1))):
        try:
            md.median_interval(*args)
            check(name + " raises", False, "no error")
        except ValueError as error:
            check(name + " raises", True, str(error)[:44])


def make_band(n_units=9, duration_s=740.0, rate_hz=8.0, depth_noise_um=12.0,
              trajectory=None, seed=FIXTURE_SEED):
    """Build a synthetic band with a known depth trajectory.

    Args:
        n_units: number of units in the band.
        duration_s: recording duration in seconds.
        rate_hz: mean firing rate per unit, homogeneous Poisson.
        depth_noise_um: per-spike depth-estimation noise, Gaussian.
        trajectory: callable from time in seconds to displacement in
            micrometres; a flat band when None.
        seed: fixture seed.

    Returns:
        tuple: ``(times, depths, rows)`` lists ready for the estimator.
    """
    rng = np.random.default_rng(seed)
    if trajectory is None:
        def trajectory(_t):
            """Return a flat band displacement."""
            return 0.0
    times, depths = [], []
    for u in range(n_units):
        count = rng.poisson(rate_hz * duration_s)
        t = np.sort(rng.uniform(0.0, duration_s, size=count))
        base = 400.0 + 30.0 * u
        d = base + trajectory(t) + rng.normal(0.0, depth_noise_um, size=t.size)
        times.append(t)
        depths.append(d)
    return times, depths, list(range(n_units))


def punch_holes(times, depths, per_unit, seed=FIXTURE_SEED + 7):
    """Remove some spikes' depths, returning the finite record and the holes.

    Args:
        times: list of per-unit spike-time arrays.
        depths: list of per-unit depth arrays.
        per_unit: how many depths to remove from each of the first units, as a
            list; units past its length keep every depth.
        seed: fixture seed for which spikes lose their depth.

    Returns:
        tuple: ``(finite_times, finite_depths, missing_times, truth)`` where
        ``truth`` holds the removed depth values per unit, so a test can
        rebuild the complete record.
    """
    rng = np.random.default_rng(seed)
    finite_times, finite_depths, missing_times, truth = [], [], [], []
    for u, (t, d) in enumerate(zip(times, depths)):
        k = per_unit[u] if u < len(per_unit) else 0
        if k <= 0:
            finite_times.append(t)
            finite_depths.append(d)
            missing_times.append(np.empty(0, dtype=np.float64))
            truth.append(np.empty(0, dtype=np.float64))
            continue
        holes = np.sort(rng.choice(t.size, size=k, replace=False))
        mask = np.ones(t.size, dtype=bool)
        mask[holes] = False
        finite_times.append(t[mask])
        finite_depths.append(d[mask])
        missing_times.append(t[holes])
        truth.append(d[holes])
    return finite_times, finite_depths, missing_times, truth


def complete_record(finite_times, finite_depths, missing_times, fill):
    """Rebuild a complete record from the finite one and a completion.

    The merge is a stable sort of the observed spikes followed by the missing
    ones, which is the same order :func:`masked_record` produces, so a
    completion and the NaN record the bound was computed from put every spike
    at the same position.

    Args:
        finite_times: list of per-unit observed spike times.
        finite_depths: list of per-unit observed depths.
        missing_times: list of per-unit missing-depth spike times.
        fill: list of per-unit completion values for those spikes.

    Returns:
        tuple: ``(times, depths)`` merged and sorted by time per unit.
    """
    times, depths = [], []
    for t, d, mt, mv in zip(finite_times, finite_depths, missing_times, fill):
        merged_t = np.concatenate([t, np.asarray(mt, dtype=np.float64)])
        merged_d = np.concatenate([d, np.asarray(mv, dtype=np.float64)])
        order = np.argsort(merged_t, kind="stable")
        times.append(merged_t[order])
        depths.append(merged_d[order])
    return times, depths


def masked_record(finite_times, finite_depths, missing_times):
    """Build the complete record the module takes, NaN at the missing depths.

    Args:
        finite_times: list of per-unit observed spike times.
        finite_depths: list of per-unit observed depths.
        missing_times: list of per-unit missing-depth spike times.

    Returns:
        tuple: ``(times, depths)`` with NaN exactly at the missing positions.
    """
    fill = [np.full(np.asarray(mt).size, np.nan, dtype=np.float64)
            for mt in missing_times]
    return complete_record(finite_times, finite_depths, missing_times, fill)


def case_split_unit_preserves_positions():
    """The split reads positions from the record rather than guessing them."""
    print("split_unit_preserves_positions")
    times = np.array([1.0, 2.0, 2.0, 2.0, 3.0], dtype=np.float64)
    depths = np.array([10.0, np.nan, 20.0, np.nan, 30.0], dtype=np.float64)
    finite_t, finite_d, missing_t = md.split_unit(times, depths)
    check("the observed spikes keep their order and values",
          np.array_equal(finite_t, np.array([1.0, 2.0, 3.0]))
          and np.array_equal(finite_d, np.array([10.0, 20.0, 30.0])))
    check("tied missing spikes are located by position, not by time",
          np.array_equal(missing_t, np.array([2.0, 2.0])),
          "two of three spikes at t=2.0 s are missing")
    check("the split accounts for every spike",
          finite_t.size + missing_t.size == times.size)

    empty = md.split_unit(np.empty(0), np.empty(0))
    check("an empty unit splits into three empty arrays",
          all(part.size == 0 for part in empty))


def case_split_unit_rejects_bad_input():
    """An infinite depth and a non-finite time both raise."""
    print("split_unit_rejects_bad_input")
    cases = [
        ("mismatched lengths", np.array([1.0, 2.0]), np.array([1.0])),
        ("a non-finite spike time", np.array([1.0, np.nan]),
         np.array([1.0, 2.0])),
        ("an infinite depth", np.array([1.0, 2.0]),
         np.array([1.0, np.inf])),
        ("a negative infinite depth", np.array([1.0, 2.0]),
         np.array([1.0, -np.inf])),
    ]
    for name, times, depths in cases:
        try:
            md.split_unit(times, depths)
            check("%s raises" % name, False, "no error")
        except ValueError as error:
            check("%s raises" % name, True, str(error)[:46])

    times, depths, _ = make_band(n_units=4, seed=FIXTURE_SEED + 50)
    depths[2] = depths[2].copy()
    depths[2][11] = np.inf
    try:
        md.measure_missing_depth_sensitivity(times, depths, 740.0)
        check("an infinite depth stops the whole measurement", False, "no error")
    except ValueError as error:
        check("an infinite depth stops the whole measurement", True,
              str(error)[:46])

    times[1] = times[1].copy()
    depths[2][11] = 400.0
    times[1][5] = np.nan
    try:
        md.measure_missing_depth_sensitivity(times, depths, 740.0)
        check("a non-finite spike time stops the whole measurement", False,
              "no error")
    except ValueError as error:
        check("a non-finite spike time stops the whole measurement", True,
              str(error)[:46])


def case_pipeline_bound_contains_every_completion(n_completions):
    """Every completion's Delta_10min lands inside the propagated bound."""
    print("pipeline_bound_contains_every_completion")
    rng = np.random.default_rng(FIXTURE_SEED + 3)
    escapes, worst_margin, runs = 0, np.inf, 0
    widths = []
    for fixture in range(3):
        def ramp(t, slope=1.4 + fixture):
            """Return a linear depth ramp."""
            return slope * t / 60.0
        times, depths, _ = make_band(trajectory=ramp, seed=FIXTURE_SEED + fixture)
        finite_t, finite_d, missing_t, truth = punch_holes(
            times, depths, [3, 5, 2, 0, 4, 1], seed=FIXTURE_SEED + 20 + fixture)
        masked_t, masked_d = masked_record(finite_t, finite_d, missing_t)
        result = md.measure_missing_depth_sensitivity(masked_t, masked_d, 740.0)
        if not check("fixture %d is measurable" % fixture,
                     result["measurable"], result.get("reason", "")[:40]):
            return
        lo = result["delta_window_lo"]
        hi = result["delta_window_hi"]
        widths.append(hi - lo)
        for trial in range(n_completions):
            if trial == 0:
                fill = truth
            elif trial == 1:
                fill = [np.full(mt.size, -5000.0) for mt in missing_t]
            elif trial == 2:
                fill = [np.full(mt.size, 5000.0) for mt in missing_t]
            else:
                fill = [rng.uniform(-2000.0, 2000.0, size=mt.size)
                        for mt in missing_t]
            full_t, full_d = complete_record(finite_t, finite_d, missing_t, fill)
            observed = bd.measure_band_drift(full_t, full_d, 740.0)
            if not observed["measurable"]:
                continue
            runs += 1
            value = observed["delta_window"]
            worst_margin = min(worst_margin, value - lo, hi - value)
            if value < lo - 1e-9 or value > hi + 1e-9:
                escapes += 1
    check("no completion escapes the bound", escapes == 0,
          "%d completions run, %d escapes" % (runs, escapes))
    check("the bound is not vacuously wide",
          all(width < 60.0 for width in widths),
          "widths %s um" % ", ".join("%.2f" % w for w in widths))
    check("the tightest completion still had room", worst_margin >= -1e-9,
          "smallest margin %.4f um" % worst_margin)


def case_zero_missing_reproduces_estimator(n_permutations):
    """With no missing depths the layer changes neither number."""
    print("zero_missing_reproduces_estimator")
    times, depths, rows = make_band(seed=FIXTURE_SEED + 4)
    observed = bd.measure_band_drift(times, depths, 740.0)
    result = md.measure_missing_depth_sensitivity(times, depths, 740.0)
    check("the point estimate is the approved estimator's own",
          result["observed"]["delta_window"] == observed["delta_window"],
          "%.6f um" % observed["delta_window"])
    check("the bound collapses onto the point estimate",
          result["delta_window_lo"] == observed["delta_window"]
          and result["delta_window_hi"] == observed["delta_window"],
          "[%.6f, %.6f]" % (result["delta_window_lo"], result["delta_window_hi"]))
    check("no exclusions are reported", result["exclusions"]["total"] == 0)

    params = {"n_permutations": n_permutations}
    approved = bd.permutation_null(times, depths, 740.0, "asset", "Probe00",
                                   rows, params)
    bounded = md.null_interval(times, depths, 740.0, "asset", "Probe00", rows,
                               params)
    check("the null's lower path reproduces the approved null elementwise",
          bounded["values_lo"] == approved["values"],
          "%d replicates identical" % n_permutations)
    check("the null's upper path reproduces the approved null elementwise",
          bounded["values_hi"] == approved["values"],
          "%d replicates identical" % n_permutations)
    check("the null bound collapses onto the approved percentile",
          bounded["q95_lo"] == approved["q95"] and bounded["q95_hi"] == approved["q95"],
          "q95 %.6f um" % approved["q95"])


def case_null_bound_contains_approved_null(n_permutations):
    """The approved null of every completed record lands inside the bound.

    This is the assumption-free claim, tested directly. Each completion is
    turned into a real complete record and handed to
    ``band_drift.permutation_null`` exactly as the gate would hand it the
    archive's own record; the resulting ``Q95_null`` must sit inside the
    interval computed from the NaN record alone.
    """
    print("null_bound_contains_approved_null")
    params = {"n_permutations": n_permutations}
    rng = np.random.default_rng(FIXTURE_SEED + 70)
    escapes, checked = [], 0
    fixtures = []

    times, depths, rows = make_band(seed=FIXTURE_SEED + 6)
    finite_t, finite_d, missing_t, truth = punch_holes(
        times, depths, [5, 3, 4], seed=FIXTURE_SEED + 30)
    fixtures.append(("sparse holes", finite_t, finite_d, missing_t, truth, rows,
                     740.0))

    finite_t, finite_d, missing_t, rows2, extent2 = spread_fixture(
        missing_per_bin=20)
    truth2 = [rng.uniform(0.0, 300.0, size=mt.size) for mt in missing_t]
    fixtures.append(("blocked holes", finite_t, finite_d, missing_t, truth2,
                     rows2, extent2))

    for label, f_t, f_d, m_t, truth_values, unit_rows, extent in fixtures:
        masked_t, masked_d = masked_record(f_t, f_d, m_t)
        bounded = md.null_interval(masked_t, masked_d, extent, "asset",
                                   "Probe00", unit_rows, params)
        fills = [
            ("observed truth", truth_values),
            ("all far below", [np.full(mt.size, -3000.0) for mt in m_t]),
            ("all far above", [np.full(mt.size, 3000.0) for mt in m_t]),
            ("mixed ramp", [np.linspace(-500.0, 500.0, mt.size) for mt in m_t]),
            ("random", [rng.uniform(-1000.0, 1000.0, size=mt.size)
                        for mt in m_t]),
        ]
        for name, fill in fills:
            full_t, full_d = complete_record(f_t, f_d, m_t, fill)
            q95 = bd.permutation_null(full_t, full_d, extent, "asset",
                                      "Probe00", unit_rows, params)["q95"]
            inside = bounded["q95_lo"] - 1e-9 <= q95 <= bounded["q95_hi"] + 1e-9
            checked += 1
            if not inside:
                escapes.append("%s/%s" % (label, name))
            check("%-13s %-14s inside [%.3f, %.3f]"
                  % (label, name, bounded["q95_lo"], bounded["q95_hi"]), inside,
                  "q95 %.3f um" % q95)
        check("%s: the bound is finite and not vacuous" % label,
              bounded["bounded"] and bounded["q95_hi"] - bounded["q95_lo"] < 120.0,
              "width %.3f um" % (bounded["q95_hi"] - bounded["q95_lo"]))
    check("no completed record's null escapes the bound", not escapes,
          "%d completions checked, escapes: %s" % (checked, escapes or "none"))


def case_finite_only_null_is_not_a_completion(n_permutations):
    """The finite-only null is a diagnostic, not one of the completed records.

    Running the approved null on the observed depths alone permutes ``n``
    elements where every completion permutes ``N = n + k``. The module says so
    rather than claiming containment, and this case is the evidence that the
    distinction is real on a fixture rather than only in the argument.
    """
    print("finite_only_null_is_not_a_completion")
    params = {"n_permutations": n_permutations}
    finite_t, finite_d, missing_t, rows, extent = spread_fixture(
        missing_per_bin=20)
    masked_t, masked_d = masked_record(finite_t, finite_d, missing_t)
    bounded = md.null_interval(masked_t, masked_d, extent, "asset", "Probe00",
                               rows, params)
    finite_only = bd.permutation_null(finite_t, finite_d, extent, "asset",
                                      "Probe00", rows, params)
    # Draw the completion from the fixture's own depth distribution. A constant
    # completion at the distribution's centre would put a point mass exactly on
    # the median and pin every bin median to it, which makes the two nulls
    # differ for a degenerate reason rather than the one under test.
    fill_rng = np.random.default_rng(FIXTURE_SEED + 80)
    truth = [fill_rng.uniform(0.0, 300.0, size=mt.size) for mt in missing_t]
    full_t, full_d = complete_record(finite_t, finite_d, missing_t, truth)
    completed = bd.permutation_null(full_t, full_d, extent, "asset", "Probe00",
                                    rows, params)
    check("a completed record's null differs from the finite-only null",
          finite_only["q95"] != completed["q95"],
          "finite-only %.4f um, completed %.4f um"
          % (finite_only["q95"], completed["q95"]))
    check("the completed record's null is inside the bound",
          bounded["q95_lo"] - 1e-9 <= completed["q95"] <= bounded["q95_hi"] + 1e-9,
          "[%.3f, %.3f] um" % (bounded["q95_lo"], bounded["q95_hi"]))


def case_null_rejects_bad_rows(n_permutations):
    """Row indices are validated exactly as the approved null validates them."""
    print("null_rejects_bad_rows")
    params = {"n_permutations": min(4, n_permutations)}
    times, depths, rows = make_band(n_units=7, seed=FIXTURE_SEED + 15)
    bad = [
        ("too few row indices", rows[:-1]),
        ("a duplicate row index", [0, 1, 2, 3, 4, 5, 5]),
        ("a negative row index", [0, 1, 2, 3, 4, 5, -1]),
        ("a non-integer row index", [0, 1, 2, 3, 4, 5, 6.5]),
    ]
    for name, unit_rows in bad:
        errors = []
        for fn in (bd.permutation_null, md.null_interval):
            try:
                fn(times, depths, 740.0, "asset", "Probe00", unit_rows, params)
                errors.append(None)
            except ValueError as error:
                errors.append(str(error))
        check("%s raises in both nulls" % name,
              errors[0] is not None and errors[1] is not None,
              "approved: %s" % (errors[0] or "no error")[:34])


def case_unbounded_bin_is_reported(n_permutations):
    """Half a bin missing is unbounded, and the layer refuses a disposition."""
    print("unbounded_bin_is_reported")
    params = {"n_permutations": n_permutations}
    finite_t, finite_d, missing_t, rows, extent = spread_fixture(
        per_bin=10, missing_per_bin=10)
    masked_t, masked_d = masked_record(finite_t, finite_d, missing_t)
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, extent)
    check("support invariance still holds", result["support"]["invariant"],
          result.get("reason", "")[:40])
    check("the observation bound is unbounded", result["measurable"]
          and not result["bounded"],
          "[%.1f, %.1f] um" % (result["delta_window_lo"],
                               result["delta_window_hi"]))
    bounded = md.null_interval(masked_t, masked_d, extent, "asset", "Probe00",
                               rows, params)
    check("the null bound is unbounded too", not bounded["bounded"],
          "[%.1f, %.1f] um" % (bounded["q95_lo"], bounded["q95_hi"]))
    verdict = md.stability_verdict(result, bounded,
                                   bd.PARAMS["threshold_strict_um"])
    check("the disposition is unmeasurable rather than a number",
          verdict["disposition"] == "unmeasurable" and not verdict["stable"],
          verdict["reason"][:44])


def codex_construction(finite_per_bin, missing_per_bin=1, n_units=5, n_bins=12,
                       low=0.0, high=100.0):
    """Rebuild the support-passing counterexample as a missing-depth record.

    Every unit and bin holds ``finite_per_bin`` observed depths split evenly
    between ``low`` and ``high``, so the complete-case median sits midway and a
    single missing value decides which side the complete median lands on.

    Args:
        finite_per_bin: even count of observed depths per unit and bin.
        missing_per_bin: missing depths per unit and bin.
        n_units: number of identical units.
        n_bins: number of complete bins.
        low: the lower depth level in micrometres.
        high: the upper depth level in micrometres.

    Returns:
        tuple: ``(finite_times, finite_depths, missing_times, rows, extent_s)``.
    """
    half = finite_per_bin // 2
    times, depths, missing = [], [], []
    for _ in range(n_units):
        t, d, m = [], [], []
        for b in range(n_bins):
            base = b * 60.0
            t.extend((base + np.linspace(0.01, 59.9, finite_per_bin)).tolist())
            d.extend([low] * half + [high] * half)
            m.extend((base + np.linspace(59.91, 59.98,
                                         missing_per_bin)).tolist())
        times.append(np.asarray(t, dtype=np.float64))
        depths.append(np.asarray(d, dtype=np.float64))
        missing.append(np.asarray(m, dtype=np.float64))
    return times, depths, missing, list(range(n_units)), n_bins * 60.0


def case_codex_support_passing_counterexample(n_permutations):
    """The construction that defeated the count-only disposition is caught."""
    print("codex_support_passing_counterexample")
    finite_t, finite_d, missing_t, rows, extent = codex_construction(1000)
    fraction = 1.0 / (1000.0 + 1.0)
    masked_t, masked_d = masked_record(finite_t, finite_d, missing_t)
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, extent)
    check("every support floor still passes", result["support"]["invariant"],
          "%.6f%% missing" % (100.0 * fraction))
    check("the complete-case point estimate is flat",
          abs(result["observed"]["delta_window"]) < 1e-9,
          "%.6f um" % result["observed"]["delta_window"])
    check("the bound reaches the 100 um completion",
          result["delta_window_hi"] >= 100.0 - 1e-6,
          "[%.3f, %.3f] um" % (result["delta_window_lo"],
                               result["delta_window_hi"]))

    params = {"n_permutations": n_permutations}
    bounded = md.null_interval(masked_t, masked_d, extent, "asset", "Probe00",
                               rows, params)
    verdict = md.stability_verdict(result, bounded,
                                   bd.PARAMS["threshold_strict_um"])
    check("the candidate does not reach a stable pass",
          verdict["disposition"] != "passes", verdict["disposition"])

    # The correction this case exists to record. The construction was posted as
    # evidence that the existing gate can accept a candidate whose missing
    # depths decide it, and it was run through ``measure_band_drift`` only. The
    # gate is two numbers. Its second one already rejects this fixture: an
    # exactly balanced bin has a knife-edge median, so permuting each unit's
    # depths swings every bin median the full 100 um between the two levels,
    # and the null's 95th percentile lands far above the tolerance.
    approved_null = bd.permutation_null(finite_t, finite_d, extent, "asset",
                                        "Probe00", rows, params)
    gate = bd.apply_gate(result["observed"], approved_null,
                         bd.PARAMS["threshold_strict_um"])
    check("the point estimate alone would have passed",
          result["observed"]["delta_window"] <= bd.PARAMS["threshold_strict_um"],
          "%.6f um against a %.1f um gate"
          % (result["observed"]["delta_window"],
             bd.PARAMS["threshold_strict_um"]))
    check("but the approved gate already rejects it on the null",
          not gate["passed"] and gate["label"] == "unmeasurable",
          "q95 %.3f um, label %s" % (approved_null["q95"], gate["label"]))


def spread_fixture(n_units=15, n_bins=12, per_bin=200, missing_per_bin=20,
                   width_um=300.0, seed=FIXTURE_SEED + 60):
    """Build a band the whole approved gate passes on the observed record.

    Depths are drawn uniformly across ``width_um`` in every bin, so no bin
    median is knife-edge and the permutation null stays narrow: the band trace
    is a median across units, and independent per-unit resampling noise shrinks
    with the unit count. A block of missing depths in every bin does not shrink
    that way -- it shifts every unit's median in the same direction at once --
    which is why a construction can exist that the two-number gate accepts and
    the missing depths still decide.

    Args:
        n_units: number of units in the band.
        n_bins: number of complete bins.
        per_bin: observed depths per unit and bin.
        missing_per_bin: missing depths per unit and bin.
        width_um: width of the uniform depth spread in micrometres.
        seed: fixture seed.

    Returns:
        tuple: ``(finite_times, finite_depths, missing_times, rows, extent_s)``.
    """
    rng = np.random.default_rng(seed)
    times, depths, missing = [], [], []
    for _ in range(n_units):
        t, d, m = [], [], []
        for b in range(n_bins):
            base = b * 60.0
            t.extend((base + np.linspace(0.01, 55.0, per_bin)).tolist())
            d.extend(rng.uniform(0.0, width_um, size=per_bin).tolist())
            if missing_per_bin:
                m.extend((base + np.linspace(56.0, 59.0,
                                             missing_per_bin)).tolist())
        order = np.argsort(np.asarray(t, dtype=np.float64), kind="stable")
        times.append(np.asarray(t, dtype=np.float64)[order])
        depths.append(np.asarray(d, dtype=np.float64)[order])
        missing.append(np.asarray(m, dtype=np.float64)
                       if m else np.empty(0, dtype=np.float64))
    return times, depths, missing, list(range(n_units)), n_bins * 60.0


def case_gate_passing_counterexample(n_permutations):
    """A candidate the whole approved gate passes, decided by its missing depths.

    This is the case the module exists for, and it is stronger than the
    bimodal construction above: the observed record clears **both** gate
    numbers at the strict tolerance, so nothing in the approved pipeline
    objects to it, and the missing depths still admit an excursion three times
    the tolerance.
    """
    print("gate_passing_counterexample")
    params = {"n_permutations": n_permutations}
    threshold = bd.PARAMS["threshold_strict_um"]
    finite_t, finite_d, missing_t, rows, extent = spread_fixture()
    masked_t, masked_d = masked_record(finite_t, finite_d, missing_t)
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, extent)
    approved_null = bd.permutation_null(finite_t, finite_d, extent, "asset",
                                        "Probe00", rows, params)
    gate = bd.apply_gate(result["observed"], approved_null, threshold)
    check("the approved gate passes the observed record", gate["passed"],
          "delta %.3f um, q95 %.3f um against %.1f um"
          % (result["observed"]["delta_window"], approved_null["q95"], threshold))
    check("support invariance holds", result["support"]["invariant"],
          "%.3f%% of samples missing"
          % (100.0 * result["exclusions"]["total"]
             / (result["exclusions"]["total"]
                + sum(t.size for t in finite_t))))
    bounded = md.null_interval(masked_t, masked_d, extent, "asset", "Probe00",
                               rows, params)
    verdict = md.stability_verdict(result, bounded, threshold)
    check("the missing depths leave it decision-unstable",
          verdict["disposition"] == "decision-unstable",
          "excursion in [%.2f, %.2f] um"
          % (result["delta_window_lo"], result["delta_window_hi"]))


def case_small_missingness_still_passes(n_permutations):
    """The layer does not pause a candidate whose missing depths cannot decide it.

    A bound that called everything unstable would be as useless as no bound at
    all, so the same fixture is re-run with a twentieth of the missing samples
    and must come back a stable pass.
    """
    print("small_missingness_still_passes")
    params = {"n_permutations": n_permutations}
    threshold = bd.PARAMS["threshold_strict_um"]
    finite_t, finite_d, missing_t, rows, extent = spread_fixture(
        missing_per_bin=1)
    masked_t, masked_d = masked_record(finite_t, finite_d, missing_t)
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, extent)
    bounded = md.null_interval(masked_t, masked_d, extent, "asset", "Probe00",
                               rows, params)
    verdict = md.stability_verdict(result, bounded, threshold)
    check("the disposition is a stable pass",
          verdict["disposition"] == "passes" and verdict["stable"],
          "excursion at most %.2f um, null at most %.2f um"
          % (result["delta_window_hi"], bounded["q95_hi"]))
    check("the bound is wider than the point estimate but under the gate",
          result["delta_window_hi"] > result["observed"]["delta_window"]
          and result["delta_window_hi"] <= threshold,
          "%.3f um point, %.3f um bound"
          % (result["observed"]["delta_window"], result["delta_window_hi"]))


def case_support_invariance_bin_floor():
    """A bin that only clears the ten-spike floor with its missing depths."""
    print("support_invariance_bin_floor")
    times, depths, _ = make_band(n_units=7, seed=FIXTURE_SEED + 8)
    finite_t, finite_d, missing_t, _ = punch_holes(times, depths, [0] * 7)
    # Thin one unit's first bin to nine observed spikes plus two missing ones.
    t, d = finite_t[0], finite_d[0]
    in_bin = t < 60.0
    keep = np.flatnonzero(in_bin)[:9]
    outside = np.flatnonzero(~in_bin)
    dropped = np.flatnonzero(in_bin)[9:11]
    order = np.concatenate([keep, outside])
    finite_t[0], finite_d[0] = t[order], d[order]
    missing_t[0] = np.sort(t[dropped])
    masked_t, masked_d = masked_record(finite_t, finite_d, missing_t)
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, 740.0)
    check("the candidate is unmeasurable", not result["measurable"],
          result.get("reason", "")[:52])
    check("the reason names the unit/bin pair",
          "unit/bin" in result.get("reason", ""),
          "%d mismatches" % len(result["support"]["bin_mismatches"]))


def case_support_invariance_unit_floor():
    """A unit that only clears the 80% defined-bin floor with its missing depths."""
    print("support_invariance_unit_floor")
    times, depths, _ = make_band(n_units=7, duration_s=740.0, rate_hz=8.0,
                                 seed=FIXTURE_SEED + 9)
    finite_t, finite_d, missing_t, _ = punch_holes(times, depths, [0] * 7)
    t, d = finite_t[0], finite_d[0]
    keep_mask = np.ones(t.size, dtype=bool)
    missing = []
    # Take four bins down to nine observed spikes, keeping one missing spike in
    # each, which is enough to cross the 80% floor on a twelve-bin recording.
    for b in range(4):
        idx = np.flatnonzero((t >= b * 60.0) & (t < (b + 1) * 60.0))
        keep_mask[idx[9:]] = False
        missing.append(t[idx[9]])
    finite_t[0], finite_d[0] = t[keep_mask], d[keep_mask]
    missing_t[0] = np.asarray(sorted(missing), dtype=np.float64)
    masked_t, masked_d = masked_record(finite_t, finite_d, missing_t)
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, 740.0)
    check("the candidate is unmeasurable", not result["measurable"],
          result.get("reason", "")[:52])


def case_all_depths_missing_unit():
    """A unit whose depths are wholly missing makes the candidate unmeasurable."""
    print("all_depths_missing_unit")
    times, depths, _ = make_band(n_units=7, seed=FIXTURE_SEED + 10)
    masked_t = [t.copy() for t in times]
    masked_d = [d.copy() for d in depths]
    masked_d[2] = np.full(masked_t[2].size, np.nan, dtype=np.float64)
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, 740.0)
    check("the candidate is unmeasurable", not result["measurable"],
          result.get("reason", "")[:52])
    check("the wholly missing unit is the one reported",
          all(pair[0] == 2 for pair in result["support"]["bin_mismatches"]),
          "%d bin mismatches, all on unit 2"
          % len(result["support"]["bin_mismatches"]))
    check("its exclusions are counted",
          result["exclusions"]["per_unit"][2] == masked_t[2].size,
          "%d spikes" % result["exclusions"]["per_unit"][2])


def case_dropping_takes_a_bin_below_the_unit_floor():
    """Dropping must not silently rescue a bin the floors would have rejected."""
    print("dropping_takes_a_bin_below_the_unit_floor")
    times, depths, _ = make_band(n_units=6, seed=FIXTURE_SEED + 11)
    masked_t = [t.copy() for t in times]
    masked_d = [d.copy() for d in depths]
    # Remove every observed depth from one bin of five units at once, so the
    # bin falls below the five-included-unit floor on the observed record.
    for u in range(5):
        idx = np.flatnonzero((masked_t[u] >= 180.0) & (masked_t[u] < 240.0))
        masked_d[u][idx] = np.nan
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, 740.0)
    check("the candidate is unmeasurable", not result["measurable"],
          result.get("reason", "")[:52])


def case_missing_outside_the_grid():
    """A missing spike past the last complete bin is counted, not binned."""
    print("missing_outside_the_grid")
    times, depths, _ = make_band(n_units=7, seed=FIXTURE_SEED + 13)
    masked_t = [t.copy() for t in times]
    masked_d = [d.copy() for d in depths]
    masked_t[0] = np.concatenate([masked_t[0], np.array([735.0])])
    masked_d[0] = np.concatenate([masked_d[0], np.array([np.nan])])
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, 740.0)
    check("the candidate stays measurable", result["measurable"],
          result.get("reason", "")[:40])
    check("the outside-grid spike is counted",
          result["exclusions"]["outside_grid"] == 1
          and result["exclusions"]["total"] == 1)
    check("no bin carries an interval because of it",
          not result["exclusions"]["per_unit_bin"],
          "%d unit/bin entries" % len(result["exclusions"]["per_unit_bin"]))


def case_exclusions_are_published():
    """Every excluded sample is reported per unit, per bin and in total."""
    print("exclusions_are_published")
    times, depths, _ = make_band(n_units=8, seed=FIXTURE_SEED + 14)
    per_unit = [6, 0, 3, 11, 0, 2]
    finite_t, finite_d, missing_t, _ = punch_holes(times, depths, per_unit,
                                                   seed=FIXTURE_SEED + 40)
    masked_t, masked_d = masked_record(finite_t, finite_d, missing_t)
    result = md.measure_missing_depth_sensitivity(masked_t, masked_d, 740.0)
    exclusions = result["exclusions"]
    expected = per_unit + [0, 0]
    check("per-unit counts match the construction",
          exclusions["per_unit"] == expected, "%s" % exclusions["per_unit"])
    check("the total matches their sum",
          exclusions["total"] == sum(expected), "%d" % exclusions["total"])
    check("per unit/bin entries sum to the same total",
          sum(entry[2] for entry in exclusions["per_unit_bin"])
          + exclusions["outside_grid"] == sum(expected),
          "%d entries" % len(exclusions["per_unit_bin"]))


def case_stability_verdict_quadrants():
    """The four dispositions, one synthetic bound each."""
    print("stability_verdict_quadrants")
    null_tight = {"q95_lo": 2.0, "q95_hi": 3.0}
    cases = [
        ("passes", {"measurable": True, "bounded": True,
                    "delta_window_lo": 4.0, "delta_window_hi": 9.0}, null_tight),
        ("fails", {"measurable": True, "bounded": True,
                   "delta_window_lo": 25.0, "delta_window_hi": 31.0}, null_tight),
        ("decision-unstable", {"measurable": True, "bounded": True,
                               "delta_window_lo": 8.0, "delta_window_hi": 44.0},
         null_tight),
        ("unmeasurable", {"measurable": True, "bounded": False,
                          "delta_window_lo": 1.0,
                          "delta_window_hi": float("inf")}, null_tight),
    ]
    for expected, sensitivity, null in cases:
        verdict = md.stability_verdict(sensitivity, null, 20.0)
        check("%-18s is reported" % expected,
              verdict["disposition"] == expected, verdict["disposition"])
    unmeasurable = md.stability_verdict(
        {"measurable": False, "reason": "support invariance failed"}, None, 20.0)
    check("an unmeasurable observation needs no null",
          unmeasurable["disposition"] == "unmeasurable"
          and not unmeasurable["stable"], unmeasurable["reason"][:40])
    fails_on_null = md.stability_verdict(
        {"measurable": True, "bounded": True, "delta_window_lo": 1.0,
         "delta_window_hi": 2.0}, {"q95_lo": 26.0, "q95_hi": 30.0}, 20.0)
    check("a null floor above the tolerance fails on its own",
          fails_on_null["disposition"] == "fails",
          fails_on_null["reason"][:44])
    unbounded_null = md.stability_verdict(
        {"measurable": True, "bounded": True, "delta_window_lo": 1.0,
         "delta_window_hi": 2.0},
        {"q95_lo": 1.0, "q95_hi": float("inf")}, 20.0)
    check("an unbounded null alone makes it unmeasurable",
          unbounded_null["disposition"] == "unmeasurable",
          unbounded_null["reason"][:44])


def main():
    """Run every case and report the tally."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--permutations", type=int, default=40,
                        help="replicates for the null cases; lower than the pinned "
                             "gate count because these cases test agreement between "
                             "two paths rather than the null's own value")
    parser.add_argument("--completions", type=int, default=120,
                        help="random completions per fixture in the containment case")
    args = parser.parse_args()

    print("missing-depth sensitivity bounds, synthetic tests")
    print("permutations per null case: %d; completions per containment fixture: %d"
          % (args.permutations, args.completions))
    print("")

    case_median_interval_matches_brute_force()
    case_median_interval_zero_missing()
    case_median_interval_unbounded()
    case_median_interval_rejects_bad_input()
    case_split_unit_preserves_positions()
    case_split_unit_rejects_bad_input()
    case_pipeline_bound_contains_every_completion(args.completions)
    case_zero_missing_reproduces_estimator(args.permutations)
    case_null_bound_contains_approved_null(args.permutations)
    case_finite_only_null_is_not_a_completion(args.permutations)
    case_null_rejects_bad_rows(args.permutations)
    case_unbounded_bin_is_reported(args.permutations)
    case_codex_support_passing_counterexample(args.permutations)
    case_gate_passing_counterexample(args.permutations)
    case_small_missingness_still_passes(args.permutations)
    case_support_invariance_bin_floor()
    case_support_invariance_unit_floor()
    case_all_depths_missing_unit()
    case_dropping_takes_a_bin_below_the_unit_floor()
    case_missing_outside_the_grid()
    case_exclusions_are_published()
    case_stability_verdict_quadrants()

    failed = [name for name, ok, _ in RESULTS if not ok]
    print("")
    print("%d checks, %d failed" % (len(RESULTS), len(failed)))
    for name in failed:
        print("  FAIL  %s" % name)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
