"""Missing-depth sensitivity bounds for the band drift gate.

Some spikes in the archive's processed units table carry a non-finite depth
while carrying a perfectly good spike time. The depth column is derived from a
waveform centre of mass, and a centre of mass divides by a sum of weights, so a
degenerate case leaves a NaN in the column; the measured pattern on two host
candidates is all-NaN, never infinite, and never in the times. Dropping those
samples and reporting the count is not sufficient, and this module exists
because of exactly why it is not.

Why a count is not enough
-------------------------
The pre-declared support floors -- at least ``min_spikes_per_bin`` depths in a
bin, a defined median in at least ``min_bin_fraction`` of bins per unit, at
least ``min_units_per_bin`` included units per bin -- bound how many finite
observations *remain*. They say nothing about how far apart the finite order
statistics sit around the median, and that spacing is what decides how far a
bin median can move when a missing value is restored. A construction with
14,000 finite depths per bin, half at 0 um and half at 100 um, and a single
missing depth -- 0.0071% missing, below the fraction measured on the real
rank-1 candidate -- passes every floor while admitting a whole-recording
``Delta_10min`` of either 0 um or 100 um against a 20 um gate. A small missing
fraction does not imply a small effect.

So the recovery this module implements is not "drop and count". It is "drop,
count, and bound what the dropped values could have done to the decision the
gate makes". A candidate whose bound straddles the threshold is unmeasurable
and stays paused; it is not passed on the strength of the point estimate.

The interval, and where it is exact
-----------------------------------
For one unit and one bin, let the finite depths be ``x_(1) <= ... <= x_(n)``
and let ``k`` depths be missing at spike times known to fall in that bin. The
complete bin holds ``N = n + k`` values, and the median reads ranks
``r1 = floor((N+1)/2)`` and ``r2 = ceil((N+1)/2)`` of the complete sorted array
and averages them. A median is nondecreasing and continuous in every argument,
so driving all ``k`` missing values below ``x_(1)`` minimises it and driving
them all above ``x_(n)`` maximises it, and every value between is attained by
some finite completion:

    lo = ( x_(r1-k) + x_(r2-k) ) / 2      unbounded below when r1 - k < 1
    hi = ( x_(r1)   + x_(r2)   ) / 2      unbounded above when r2 > n

**At the bin level this is the attainable set exactly**, and both endpoints are
reached by real completions (``x_(1) - 1`` and ``x_(n) + 1``), not only in a
limit. The complete-case median of the ``n`` finite values always lies inside
it, because dropping ``k`` values moves the read ranks by at most ``k``.

**Above the bin level it is an outer bound and not the attainable set.** The
same missing values enter both a bin median ``d_u(b)`` and the centring
constant ``c_u = median_b' d_u(b')`` that is subtracted from it, and interval
arithmetic ignores that dependence. The error runs one way: the propagated
interval is too wide, never too narrow. So this layer can call a candidate
unmeasurable that a dependence-aware treatment would have called stable, and it
cannot pass a candidate that some completion would have failed. That is the
direction a gate has to be wrong in, and it is stated here rather than papered
over with a claim of exactness.

Support invariance
------------------
The interval above varies the missing *values*. Inclusion *sets* can move too:
a bin holding 9 finite depths and 2 missing ones is excluded from the record we
hold and included under every completion. Ranging the bound over subsets as
well as values would make it a much larger and much less interpretable object,
so this module requires instead that the sets do not move at all --
:func:`support_invariance` checks every unit and every bin for the same
inclusion status whether the missing samples are counted toward the floors or
not, all three floors, both ways. A violation makes the candidate unmeasurable.
This is an equality, not a fitted tolerance, and both measured host candidates
satisfy it.

The counterfactual null
-----------------------
The gate is two numbers, so a completion could flip it through ``Q95_null`` as
well as through ``Delta_10min``. **An assumption-free interval on ``Q95_null``
does not exist in a non-vacuous form.** Under a completion a unit's analysed
pool holds ``n + k`` values and the null's seed-determined permutation is an
arrangement of that many elements -- a different arrangement, not a
perturbation of the computed one -- so bounding over completions would have to
bound over arrangements, under which any bin can receive any subset of the
pool. The bound would degenerate to the unit's whole observed depth range and
would be reporting the permutation's freedom rather than the missing data's.

:func:`null_interval` therefore evaluates a **declared counterfactual**, and
declares it: the counterfactual null permutes the observed depths among the
observed-depth spikes exactly as the actual null does -- same seeds, same
arrangement -- and leaves each completed value at its own spike's time. That
isolates the effect of the missing values from a nuisance that has nothing to
do with them, since two seeds already give two different nulls on data with no
missingness at all. The nearest-rank percentile is nondecreasing in every
sample value, so taking it separately over the replicates' lower and upper
bounds is sound.

What this module does not do
----------------------------
It does not decide whether a non-finite depth may be excluded at all; that is a
specification question settled outside the code. It does not touch non-finite
spike *times*, which remain input errors: a spike with no usable time cannot be
placed in a bin, and the interval above is defined only because the missing
depths' bins are known. It computes no point estimate of its own -- the point
estimate is whatever the approved ``band_drift`` estimator returns on the
finite record, which this module calls rather than reimplements.
"""

import numpy as np

from utils import band_drift


def median_interval(values, n_missing):
    """Exact attainable interval of a bin median under missing depths.

    Args:
        values: the bin's finite depths, in any order; not modified.
        n_missing: the number of missing depths whose spike times fall in this
            bin. Zero returns a degenerate interval equal to the median.

    Returns:
        tuple: ``(lo, hi)`` in micrometres. ``-inf`` or ``+inf`` marks an
        unbounded side, which happens only when the missing count reaches
        roughly half the bin.

    Raises:
        ValueError: if ``values`` is empty, holds a non-finite value, or
            ``n_missing`` is negative.
    """
    x = np.asarray(values, dtype=np.float64)
    if x.size == 0:
        raise ValueError("a bin median interval needs at least one finite depth")
    if not np.all(np.isfinite(x)):
        raise ValueError("median_interval takes the finite depths only")
    k = int(n_missing)
    if k < 0:
        raise ValueError("n_missing must be non-negative, got %r" % (n_missing,))
    x = np.sort(x)
    n = x.size
    total = n + k
    r1 = (total + 1) // 2
    r2 = (total + 2) // 2
    lo = -np.inf if r1 - k < 1 else 0.5 * (x[r1 - k - 1] + x[r2 - k - 1])
    hi = np.inf if r2 > n else 0.5 * (x[r1 - 1] + x[r2 - 1])
    return float(lo), float(hi)


def missing_counts(missing_times, n_bins, bin_seconds=None):
    """Count missing-depth spikes per complete bin from their spike times.

    Args:
        missing_times: ascending finite times, in seconds, of the spikes whose
            depth was missing. An empty array is allowed.
        n_bins: the number of complete bins on the session grid.
        bin_seconds: bin length in seconds; defaults to ``band_drift.PARAMS``.

    Returns:
        numpy.ndarray: one non-negative integer count per complete bin. Missing
        spikes outside the complete-bin grid are not counted here and are
        reported separately by the caller.

    Raises:
        ValueError: if the times are not ascending or not finite.
    """
    times = np.asarray(missing_times, dtype=np.float64)
    offsets = band_drift.bin_offsets(times, n_bins, bin_seconds)
    return np.diff(offsets).astype(int)


def unit_intervals(spike_times, depths, missing_times, n_bins, params=None):
    """Point bin medians and their missing-depth intervals for one unit.

    The point medians come from :func:`band_drift.bin_medians` so that this
    module never carries a second definition of the estimator's own quantity.
    Only bins that actually hold a missing spike get a non-degenerate interval.

    Args:
        spike_times: the unit's ascending finite-depth spike times, in seconds.
        depths: the unit's finite depths, aligned with ``spike_times``.
        missing_times: ascending times of its missing-depth spikes.
        n_bins: the number of complete bins.
        params: parameter overrides; defaults to ``band_drift.PARAMS``.

    Returns:
        dict: ``point``, ``lo`` and ``hi`` arrays of ``n_bins`` bin medians,
        NaN where the bin holds too few finite depths; ``n_finite`` and
        ``n_missing`` counts per bin; ``defined_finite`` and
        ``defined_complete`` boolean masks for the ten-spike floor evaluated
        without and with the missing samples; and ``missing_outside``, the
        count of missing spikes falling outside every complete bin.

    Raises:
        ValueError: if the arrays disagree in length, are not ascending, or
            hold non-finite values.
    """
    p = dict(band_drift.PARAMS)
    if params:
        p.update(params)
    times = np.asarray(spike_times, dtype=np.float64)
    values = np.asarray(depths, dtype=np.float64)
    if times.size != values.size:
        raise ValueError(
            "%d finite spike times and %d finite depths" % (times.size, values.size)
        )
    if values.size and not np.all(np.isfinite(values)):
        raise ValueError("unit_intervals takes the finite depths only")
    offsets = band_drift.bin_offsets(times, n_bins, p["bin_seconds"])
    point = band_drift.bin_medians(values, offsets, p["min_spikes_per_bin"])

    missing = np.asarray(missing_times, dtype=np.float64)
    per_bin_missing = missing_counts(missing, n_bins, p["bin_seconds"])
    missing_outside = int(missing.size - per_bin_missing.sum())

    n_finite = np.diff(offsets).astype(int)
    defined_finite = n_finite >= p["min_spikes_per_bin"]
    defined_complete = (n_finite + per_bin_missing) >= p["min_spikes_per_bin"]

    lo = point.copy()
    hi = point.copy()
    for b in np.flatnonzero(per_bin_missing > 0):
        if not defined_finite[b]:
            continue
        low, high = median_interval(
            values[offsets[b]:offsets[b + 1]], per_bin_missing[b]
        )
        lo[b], hi[b] = low, high
    return {
        "point": point,
        "lo": lo,
        "hi": hi,
        "n_finite": n_finite,
        "n_missing": per_bin_missing,
        "defined_finite": defined_finite,
        "defined_complete": defined_complete,
        "missing_outside": missing_outside,
    }


def support_invariance(tables, params=None):
    """Check that no inclusion status depends on the missing samples.

    Three floors are evaluated twice, once counting only the finite depths and
    once counting the missing ones as though they had been observed: the
    per-bin spike floor, the per-unit defined-bin fraction, and the per-bin
    included-unit floor. Every one of them must agree.

    Args:
        tables: list of per-unit dicts from :func:`unit_intervals`.
        params: parameter overrides; defaults to ``band_drift.PARAMS``.

    Returns:
        dict: ``invariant`` and, when False, ``reason``; plus ``included`` and
        ``included_complete`` unit masks, ``units_per_bin`` and
        ``units_per_bin_complete``, and ``bin_mismatches`` listing every
        ``(unit, bin)`` whose per-bin floor disagrees.

    Raises:
        ValueError: if ``tables`` is empty.
    """
    p = dict(band_drift.PARAMS)
    if params:
        p.update(params)
    if not tables:
        raise ValueError("support_invariance needs at least one unit table")
    n_bins = tables[0]["point"].size

    mismatches = []
    for u, table in enumerate(tables):
        differing = np.flatnonzero(table["defined_finite"] != table["defined_complete"])
        mismatches.extend((u, int(b)) for b in differing)

    defined = np.array([t["defined_finite"].sum() for t in tables], dtype=np.float64)
    defined_complete = np.array(
        [t["defined_complete"].sum() for t in tables], dtype=np.float64
    )
    floor = p["min_bin_fraction"] * n_bins
    included = defined >= floor
    included_complete = defined_complete >= floor

    units_per_bin = np.zeros(n_bins, dtype=int)
    units_per_bin_complete = np.zeros(n_bins, dtype=int)
    for u, table in enumerate(tables):
        if included[u]:
            units_per_bin += table["defined_finite"].astype(int)
        if included_complete[u]:
            units_per_bin_complete += table["defined_complete"].astype(int)
    valid = units_per_bin >= p["min_units_per_bin"]
    valid_complete = units_per_bin_complete >= p["min_units_per_bin"]

    result = {
        "included": included,
        "included_complete": included_complete,
        "units_per_bin": units_per_bin,
        "units_per_bin_complete": units_per_bin_complete,
        "bin_mismatches": mismatches,
        "invariant": True,
    }
    if mismatches:
        result.update(
            invariant=False,
            reason="%d unit/bin pairs cross the %d-spike floor only when the missing "
                   "depths are counted (first: %s); the inclusion set is not invariant "
                   "to the missing samples"
                   % (len(mismatches), p["min_spikes_per_bin"], mismatches[:5]),
        )
    elif not np.array_equal(included, included_complete):
        differing = np.flatnonzero(included != included_complete).tolist()
        result.update(
            invariant=False,
            reason="units %s cross the %.0f%% defined-bin floor only when the missing "
                   "depths are counted" % (differing[:5], 100 * p["min_bin_fraction"]),
        )
    elif not np.array_equal(valid, valid_complete):
        differing = np.flatnonzero(valid != valid_complete).tolist()
        result.update(
            invariant=False,
            reason="bins %s cross the %d-included-unit floor only when the missing "
                   "depths are counted" % (differing[:5], p["min_units_per_bin"]),
        )
    return result


def centred_intervals(tables, included):
    """Centre each included unit's interval on its own across-bin median.

    This mirrors :func:`band_drift.unit_traces` -- the centring rule itself is
    that function's and is not restated here -- and adds the interval the
    missing depths open around it. The centring constant is itself
    interval-valued, and subtracting an interval widens: the lower centred
    bound takes the unit's highest admissible centre and the upper bound takes
    its lowest. That is an outer bound, and the module docstring says which way
    its error runs.

    Args:
        tables: list of per-unit dicts from :func:`unit_intervals`.
        included: boolean mask over ``tables`` marking the included units.

    Returns:
        tuple: ``(point_stack, lo_stack, hi_stack)``, each an
        ``(n_included, n_bins)`` array with NaN in undefined bins. The point
        stack is :func:`band_drift.unit_traces` output, unchanged.

    Raises:
        ValueError: if an included unit has no defined bin median.
    """
    included = np.asarray(included, dtype=bool)
    point_stack = band_drift.unit_traces([t["point"] for t in tables], included)
    n_bins = tables[0]["point"].size
    lo_stack = np.full(point_stack.shape, np.nan, dtype=np.float64)
    hi_stack = np.full(point_stack.shape, np.nan, dtype=np.float64)
    row = 0
    for u, keep in enumerate(included):
        if not keep:
            continue
        table = tables[u]
        valid = np.isfinite(table["point"])
        if not valid.any():
            raise ValueError("included unit %d has no defined bin median" % u)
        centre_lo = float(np.median(table["lo"][valid]))
        centre_hi = float(np.median(table["hi"][valid]))
        lo_stack[row, valid] = table["lo"][valid] - centre_hi
        hi_stack[row, valid] = table["hi"][valid] - centre_lo
        row += 1
    if n_bins and point_stack.shape[1] != n_bins:
        raise ValueError("centred stack has %d bins, expected %d"
                         % (point_stack.shape[1], n_bins))
    return point_stack, lo_stack, hi_stack


def trace_intervals(lo_stack, hi_stack, min_units_per_bin=None):
    """Take the across-unit median of the centred bounds, bin by bin.

    The across-unit median is nondecreasing in every unit's value, so the
    median of the lower bounds and the median of the upper bounds bracket the
    band trace ``D(b)`` under every completion.

    Args:
        lo_stack: centred lower bounds from :func:`centred_intervals`.
        hi_stack: centred upper bounds, same shape.
        min_units_per_bin: minimum defined included units for a valid bin;
            defaults to ``band_drift.PARAMS``.

    Returns:
        tuple: ``(lo_trace, hi_trace, invalid_bins)``. Both traces hold NaN in
        any invalid bin.
    """
    if min_units_per_bin is None:
        min_units_per_bin = band_drift.PARAMS["min_units_per_bin"]
    lo_stack = np.asarray(lo_stack, dtype=np.float64)
    hi_stack = np.asarray(hi_stack, dtype=np.float64)
    if lo_stack.shape != hi_stack.shape:
        raise ValueError("bound stacks disagree in shape: %s and %s"
                         % (lo_stack.shape, hi_stack.shape))
    n_bins = lo_stack.shape[1]
    # NaN marks a bin the unit does not define; an infinite bound is a defined
    # bin whose interval is unbounded, and counting it as absent would report
    # an invalid bin where the honest answer is an unbounded one.
    units_per_bin = (~np.isnan(lo_stack)).sum(axis=0)
    usable = units_per_bin >= min_units_per_bin
    lo_trace = np.full(n_bins, np.nan, dtype=np.float64)
    hi_trace = np.full(n_bins, np.nan, dtype=np.float64)
    if usable.any():
        lo_trace[usable] = np.nanmedian(lo_stack[:, usable], axis=0)
        hi_trace[usable] = np.nanmedian(hi_stack[:, usable], axis=0)
    return lo_trace, hi_trace, np.flatnonzero(~usable)


def interval_excursions(lo_trace, hi_trace, window_bins=None):
    """Bound the whole-recording and worst-window excursions.

    For one window, the largest range any completion can produce is
    ``max(hi) - min(lo)`` inside it and the smallest is
    ``max(0, max(lo) - min(hi))``. The gating statistic is the largest range
    over all windows, so its upper bound is the largest per-window upper bound
    and its lower bound is the largest per-window lower bound: any completion's
    maximum over windows is at least that completion's value in the window
    achieving the latter.

    Args:
        lo_trace: per-bin lower bounds, all defined.
        hi_trace: per-bin upper bounds, all defined.
        window_bins: window length in bins; defaults to ``band_drift.PARAMS``.

    Returns:
        dict: ``delta_full_lo`` / ``delta_full_hi``; ``delta_window_lo`` /
        ``delta_window_hi`` and ``window_start_hi``, the first bin of the
        window achieving the upper bound; ``bounded``, False when either trace
        carries an infinite bound.

    Raises:
        ValueError: if the traces disagree in length, hold a NaN, or are
            shorter than one window.
    """
    if window_bins is None:
        window_bins = band_drift.PARAMS["window_bins"]
    lo_trace = np.asarray(lo_trace, dtype=np.float64)
    hi_trace = np.asarray(hi_trace, dtype=np.float64)
    if lo_trace.shape != hi_trace.shape:
        raise ValueError("traces disagree in length: %d and %d"
                         % (lo_trace.size, hi_trace.size))
    if np.any(np.isnan(lo_trace)) or np.any(np.isnan(hi_trace)):
        raise ValueError("an interval trace holds NaN; an invalid bin is not skippable")
    if lo_trace.size < window_bins:
        raise ValueError("%d bins is shorter than the %d-bin gate window"
                         % (lo_trace.size, window_bins))
    bounded = bool(np.all(np.isfinite(lo_trace)) and np.all(np.isfinite(hi_trace)))

    result = {
        "delta_full_lo": float(max(0.0, lo_trace.max() - hi_trace.min())),
        "delta_full_hi": float(hi_trace.max() - lo_trace.min()),
        "bounded": bounded,
    }
    best_hi, best_start, best_lo = -np.inf, 0, 0.0
    for start in range(lo_trace.size - window_bins + 1):
        window_lo = lo_trace[start:start + window_bins]
        window_hi = hi_trace[start:start + window_bins]
        upper = float(window_hi.max() - window_lo.min())
        lower = float(max(0.0, window_lo.max() - window_hi.min()))
        if upper > best_hi:
            best_hi, best_start = upper, start
        if lower > best_lo:
            best_lo = lower
    result.update(delta_window_hi=best_hi, delta_window_lo=best_lo,
                  window_start_hi=int(best_start))
    return result


def measure_missing_depth_sensitivity(spike_times, depths, missing_times,
                                      extent_s, params=None):
    """Measure the band drift and bound what the missing depths could do to it.

    The point estimate is :func:`band_drift.measure_band_drift` on the finite
    record, called rather than reimplemented, so this function never disagrees
    with the approved estimator about what the observation is. Around it, the
    function reports the interval every completion of the missing depths could
    have produced, and the exclusions that have to be published with it.

    Args:
        spike_times: list of per-unit ascending finite-depth spike times.
        depths: list of per-unit finite depths, aligned with ``spike_times``.
        missing_times: list of per-unit ascending missing-depth spike times,
            one entry per band unit; an empty array where a unit has none.
        extent_s: the raw AP stream's final aligned timestamp, in seconds.
        params: parameter overrides; defaults to ``band_drift.PARAMS``.

    Returns:
        dict: ``observed``, the point result from ``measure_band_drift``;
        ``measurable`` and, when False, ``reason``; ``support`` from
        :func:`support_invariance`; ``exclusions`` with ``total``,
        ``per_unit``, ``per_unit_bin`` (non-zero entries only) and
        ``outside_grid``; and, when measurable, ``delta_window_lo`` /
        ``delta_window_hi``, ``delta_full_lo`` / ``delta_full_hi``,
        ``window_start_hi``, ``bounded``, ``lo_trace`` and ``hi_trace``.

    Raises:
        ValueError: if the three lists disagree in length, or if the point
            estimate falls outside its own bound, which would mean the interval
            is wrong rather than merely wide.
    """
    p = dict(band_drift.PARAMS)
    if params:
        p.update(params)
    if not (len(spike_times) == len(depths) == len(missing_times)):
        raise ValueError(
            "%d unit time arrays, %d depth arrays and %d missing-time arrays"
            % (len(spike_times), len(depths), len(missing_times))
        )
    observed = band_drift.measure_band_drift(spike_times, depths, extent_s, p)
    result = {"observed": observed}
    n_bins, _ = band_drift.complete_bins(extent_s, p["bin_seconds"])

    tables = [
        unit_intervals(spike_times[u], depths[u], missing_times[u], n_bins, p)
        for u in range(len(spike_times))
    ]
    per_unit = [int(t["n_missing"].sum() + t["missing_outside"]) for t in tables]
    per_unit_bin = []
    for u, table in enumerate(tables):
        for b in np.flatnonzero(table["n_missing"] > 0):
            per_unit_bin.append((u, int(b), int(table["n_missing"][b])))
    result["exclusions"] = {
        "total": int(sum(per_unit)),
        "per_unit": per_unit,
        "per_unit_bin": per_unit_bin,
        "outside_grid": int(sum(t["missing_outside"] for t in tables)),
    }

    support = support_invariance(tables, p)
    result["support"] = support
    if not support["invariant"]:
        result.update(measurable=False, reason=support["reason"])
        return result
    if not observed.get("measurable", False):
        result.update(measurable=False,
                      reason=observed.get("reason", "unmeasurable"))
        return result

    included = np.zeros(len(tables), dtype=bool)
    included[observed["included"]] = True
    if not np.array_equal(included, support["included"]):
        raise ValueError(
            "the approved estimator included %d units and this module's own floor "
            "check included %d; one of the two reads the floor differently"
            % (int(included.sum()), int(support["included"].sum()))
        )
    _, lo_stack, hi_stack = centred_intervals(tables, included)
    lo_trace, hi_trace, invalid = trace_intervals(
        lo_stack, hi_stack, p["min_units_per_bin"]
    )
    if invalid.size:
        result.update(
            measurable=False,
            reason="%d analysed bins hold fewer than %d included units with a bounded "
                   "median (first: %s)"
                   % (invalid.size, p["min_units_per_bin"], invalid[:5].tolist()),
        )
        return result

    bounds = interval_excursions(lo_trace, hi_trace, p["window_bins"])
    point = observed["delta_window"]
    if bounds["bounded"] and not (
            bounds["delta_window_lo"] - 1e-9 <= point <= bounds["delta_window_hi"] + 1e-9):
        raise ValueError(
            "the point estimate %.6f um falls outside its own bound [%.6f, %.6f]"
            % (point, bounds["delta_window_lo"], bounds["delta_window_hi"])
        )
    result.update(measurable=True, lo_trace=lo_trace.tolist(),
                  hi_trace=hi_trace.tolist(), **bounds)
    return result


def null_interval(spike_times, depths, missing_times, extent_s, asset_id, probe,
                  unit_row_indices, params=None):
    """Bound ``Q95_null`` under the declared missing-depth counterfactual.

    The counterfactual is stated in the module docstring and is not an
    assumption-free bound: it holds the null's arrangement fixed -- same seeds,
    same permutation of the observed depths among the observed-depth spikes --
    and lets each completed value sit at its own spike's time. The point path
    reproduces :func:`band_drift.permutation_null` replicate for replicate,
    which is the property to test this function on.

    Args:
        spike_times: list of per-unit ascending finite-depth spike times.
        depths: list of per-unit finite depths, aligned with ``spike_times``.
        missing_times: list of per-unit ascending missing-depth spike times.
        extent_s: the raw AP stream's final aligned timestamp, in seconds.
        asset_id: the processed asset's exact stored identifier string.
        probe: the probe's exact stored name string.
        unit_row_indices: each unit's row index in the units table.
        params: parameter overrides; defaults to ``band_drift.PARAMS``.

    Returns:
        dict: ``q95`` (the point value, identical to the approved null's),
        ``q95_lo`` and ``q95_hi``, ``rank``, ``n_permutations``, and the three
        sorted replicate arrays as ``values``, ``values_lo`` and ``values_hi``.

    Raises:
        ValueError: if a replicate is unmeasurable, which fixed bin counts make
            impossible unless the observation was too.
    """
    p = dict(band_drift.PARAMS)
    if params:
        p.update(params)
    if not (len(spike_times) == len(depths) == len(missing_times)
            == len(unit_row_indices)):
        raise ValueError("the four per-unit lists disagree in length")
    rows = [int(row) for row in unit_row_indices]
    n_bins, _ = band_drift.complete_bins(extent_s, p["bin_seconds"])

    tables = [
        unit_intervals(spike_times[u], depths[u], missing_times[u], n_bins, p)
        for u in range(len(spike_times))
    ]
    support = support_invariance(tables, p)
    if not support["invariant"]:
        raise ValueError("the observation is not support-invariant: %s"
                         % support["reason"])
    included = support["included"]
    if included.sum() < p["min_units_per_bin"]:
        raise ValueError(
            "the observation is unmeasurable: only %d included units, need at least %d"
            % (int(included.sum()), p["min_units_per_bin"])
        )

    offsets = [
        band_drift.bin_offsets(np.asarray(spike_times[u], dtype=np.float64),
                               n_bins, p["bin_seconds"])
        for u in range(len(spike_times))
    ]
    pools = [np.asarray(d, dtype=np.float64) for d in depths]
    values = np.empty(p["n_permutations"], dtype=np.float64)
    values_lo = np.empty(p["n_permutations"], dtype=np.float64)
    values_hi = np.empty(p["n_permutations"], dtype=np.float64)

    for k in range(p["n_permutations"]):
        replicate = []
        for u in range(len(spike_times)):
            if not included[u]:
                replicate.append(tables[u])
                continue
            seed = band_drift.derive_permutation_seed(
                asset_id, probe, rows[u], k, p["master_seed"]
            )
            rng = np.random.Generator(np.random.PCG64(seed))
            shuffled = pools[u].copy()
            first, stop = int(offsets[u][0]), int(offsets[u][-1])
            analysed = pools[u][first:stop]
            shuffled[first:stop] = analysed[rng.permutation(analysed.size)]
            point = band_drift.bin_medians(shuffled, offsets[u], p["min_spikes_per_bin"])
            lo, hi = point.copy(), point.copy()
            for b in np.flatnonzero(tables[u]["n_missing"] > 0):
                if not tables[u]["defined_finite"][b]:
                    continue
                low, high = median_interval(
                    shuffled[offsets[u][b]:offsets[u][b + 1]],
                    tables[u]["n_missing"][b],
                )
                lo[b], hi[b] = low, high
            replicate.append({
                "point": point, "lo": lo, "hi": hi,
                "defined_finite": tables[u]["defined_finite"],
                "n_missing": tables[u]["n_missing"],
            })
        point_stack, lo_stack, hi_stack = centred_intervals(replicate, included)
        units_per_bin = np.isfinite(point_stack).sum(axis=0)
        if np.any(units_per_bin < p["min_units_per_bin"]):
            raise ValueError(
                "permutation %d produced an invalid bin; the null preserves bin counts, "
                "so this means the observation was already unmeasurable" % k
            )
        point_trace = np.nanmedian(point_stack, axis=0)
        lo_trace, hi_trace, _ = trace_intervals(lo_stack, hi_stack,
                                                p["min_units_per_bin"])
        _, delta_window, _ = band_drift.excursions(point_trace, p["window_bins"])
        bounds = interval_excursions(lo_trace, hi_trace, p["window_bins"])
        values[k] = delta_window
        values_lo[k] = bounds["delta_window_lo"]
        values_hi[k] = bounds["delta_window_hi"]

    values.sort()
    values_lo.sort()
    values_hi.sort()
    rank = int(np.ceil(p["null_percentile"] / 100.0 * p["n_permutations"]))
    return {
        "values": values.tolist(),
        "values_lo": values_lo.tolist(),
        "values_hi": values_hi.tolist(),
        "q95": float(values[rank - 1]),
        "q95_lo": float(values_lo[rank - 1]),
        "q95_hi": float(values_hi[rank - 1]),
        "rank": rank,
        "n_permutations": int(p["n_permutations"]),
    }


def stability_verdict(sensitivity, null_bounds, threshold_um):
    """Decide whether the missing depths can change the gate's disposition.

    The gate passes a candidate only when both numbers sit at or below ``L``.
    A completion that raises either above ``L`` flips it, so the disposition is
    stable in exactly two cases: both upper bounds at or below ``L``, or one
    lower bound above it. Everything else -- including an unbounded side and a
    violated support invariance -- leaves the candidate unmeasurable and
    paused. No tolerance is fitted anywhere in this rule; ``L`` is the gate's
    own pre-declared threshold.

    Args:
        sensitivity: the dict from :func:`measure_missing_depth_sensitivity`.
        null_bounds: the dict from :func:`null_interval`, or None when the
            observation was unmeasurable before a null was built.
        threshold_um: the threshold ``L`` in micrometres.

    Returns:
        dict: ``stable``, ``disposition`` (``"passes"``, ``"fails"``,
        ``"decision-unstable"`` or ``"unmeasurable"``), ``reason``, and the
        four bounds the decision used where they exist.

    Raises:
        ValueError: if a measurable sensitivity result arrives without a null.
    """
    threshold = float(threshold_um)
    if not sensitivity.get("measurable", False):
        return {
            "stable": False,
            "disposition": "unmeasurable",
            "reason": sensitivity.get("reason", "unmeasurable"),
            "threshold_um": threshold,
        }
    if null_bounds is None:
        raise ValueError("a measurable sensitivity result requires a null bound")
    delta_lo = float(sensitivity["delta_window_lo"])
    delta_hi = float(sensitivity["delta_window_hi"])
    q95_lo = float(null_bounds["q95_lo"])
    q95_hi = float(null_bounds["q95_hi"])
    verdict = {
        "delta_window_lo": delta_lo,
        "delta_window_hi": delta_hi,
        "q95_null_lo": q95_lo,
        "q95_null_hi": q95_hi,
        "threshold_um": threshold,
    }
    if not sensitivity.get("bounded", False) or not np.isfinite(q95_hi):
        verdict.update(
            stable=False,
            disposition="unmeasurable",
            reason="a required missing-depth bound is unbounded, so no completion-"
                   "independent disposition exists at the %.1f um tolerance" % threshold,
        )
    elif delta_hi <= threshold and q95_hi <= threshold:
        verdict.update(
            stable=True,
            disposition="passes",
            reason="every completion of the missing depths leaves both numbers at or "
                   "below %.1f um: excursion at most %.2f um, null 95th percentile at "
                   "most %.2f um" % (threshold, delta_hi, q95_hi),
        )
    elif delta_lo > threshold or q95_lo > threshold:
        verdict.update(
            stable=True,
            disposition="fails",
            reason="no completion of the missing depths brings both numbers to or below "
                   "%.1f um: excursion at least %.2f um, null 95th percentile at least "
                   "%.2f um" % (threshold, delta_lo, q95_lo),
        )
    else:
        verdict.update(
            stable=False,
            disposition="decision-unstable",
            reason="the missing depths straddle the %.1f um tolerance: excursion in "
                   "[%.2f, %.2f] um and null 95th percentile in [%.2f, %.2f] um, so the "
                   "gate's disposition is not determined by the observed record"
                   % (threshold, delta_lo, delta_hi, q95_lo, q95_hi),
        )
    return verdict
