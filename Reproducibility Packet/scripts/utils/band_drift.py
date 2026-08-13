"""Band drift excursion, its permutation null, and the two-number drift gate.

This module implements one specification and nothing else: the drift quantity
used to screen candidate host recordings. It computes a band displacement trace
from per-spike depths, reports the peak-to-peak excursion over the whole
recording and over the worst ten-consecutive-bin window, builds a deterministic
within-unit permutation null for that worst-window statistic, and applies the
pass rule that uses both numbers.

Why not the archive's own drift column
--------------------------------------
The processed units table carries a cumulative drift column whose own
first-party description states that it sums absolute depth changes between
consecutive spikes, that it scales with spike count at roughly 0.79
correlation, and that it is "NOT actual electrode displacement". It is a path
length, so a probe that moves down and back scores like one that moves and
stays; and its spike-count scaling would make a host selected on it partly a
host selected for being quiet, which is not a neutral thing to do in a study
whose later manipulation is population-rate coupling. This module computes a
displacement instead, from per-spike depths and times that the same table
already carries as ragged per-unit arrays.

The quantity
------------
For one probe, one anatomical band and one recording:

1. Keep the units whose depth falls inside the band.
2. Partition the recording into complete fixed-length bins from t = 0. A final
   partial bin is discarded and its duration is reported.
3. ``d_u(b)`` is the median per-spike depth of unit ``u`` in bin ``b``, defined
   only where the unit has at least ``min_spikes_per_bin`` spikes in that bin.
4. ``delta_u(b) = d_u(b) - median_b' d_u(b')`` centres each unit on its own
   typical depth so units at different depths can be pooled.
5. ``D(b)`` is the median of ``delta_u(b)`` across included units. Real movement
   is common to the band; depth-estimation noise is not.
6. ``Delta_full = max_b D(b) - min_b D(b)`` over the whole recording, and
   ``Delta_10`` is the largest such range over any window of
   ``window_bins`` consecutive complete bins. Both are peak-to-peak excursions,
   not endpoint-to-endpoint net motion: a down-and-back trajectory stays
   visible. ``Delta_10`` is the gating quantity.

The null
--------
Within the complete bins, holding every spike time fixed and permuting a unit's
depth values among its own analysed spikes destroys the depth/time ordering
while preserving every analysed depth value, spike time and per-bin spike
count. Spikes in the discarded final partial bin enter neither the observed
statistic nor the null. The resulting ``Delta_10`` distribution is what this
estimator returns on this recording with no time ordering, and its nearest-rank
empirical 95th percentile ``Q95_null`` is the declared summary. Genuine movement
is present in the pool the null draws from and, under an additive common-motion
model, can widen this resolution diagnostic. That direction is demonstrated by
a synthetic ramp fixture, not assumed to be a general monotonic guarantee.
Removing an estimated movement trajectory before building the null would make
the diagnostic depend on the drift estimate it is meant to grade.

The permutations are deterministic rather than redrawable. Each unit and
replicate draws a 64-bit seed from a hash of the master seed, the asset, the
probe, the unit's table row index and the replicate index, so the whole null
replays byte for byte from the same inputs.

The pass rule
-------------
At threshold ``L``, a candidate passes only when ``Delta_10 <= L`` **and**
``Q95_null <= L``. Lying inside the null is not a failure: a genuinely quiet
host should often do so. A noise floor wider than the tolerance is the
unmeasurable failure, and so are too few qualifying units, any invalid complete
bin, and non-finite data. An absent measurement is never read as a pass.

Every gate parameter lives in ``PARAMS`` so that a caller reports the values it
actually used rather than repeating them.
"""

import hashlib

import numpy as np

#: Pre-declared gate parameters. A caller reports these rather than restating
#: them; changing one is a contract change, not a call-site choice.
PARAMS = {
    "bin_seconds": 60.0,
    "min_spikes_per_bin": 10,
    "min_bin_fraction": 0.8,
    "min_units_per_bin": 5,
    "window_bins": 10,
    "n_permutations": 200,
    "null_percentile": 95,
    "master_seed": 3175830281,
    "threshold_strict_um": 20.0,
    "threshold_relaxed_um": 40.0,
}

#: The string the master seed is derived from, kept so a reader can replay it.
MASTER_SEED_SOURCE = "Hybrid Ground Truth Realism|Tier A|drift permutation null|v1"


def derive_master_seed(source=MASTER_SEED_SOURCE):
    """Re-derive the master seed from the string it was taken from.

    Args:
        source: the exact UTF-8 string the seed was derived from.

    Returns:
        int: the first eight hexadecimal digits of its SHA-256, as an integer.
    """
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def derive_permutation_seed(asset_id, probe, unit_row_index, permutation_index,
                            master_seed=None):
    """Derive one replicate's 64-bit seed for one unit.

    The seed is a hash of the master seed, the processed asset, the probe, the
    unit's row index in the units table and the replicate index, joined by
    newlines. Domain separation on all five means no two units and no two
    replicates share a stream, and the whole null replays from these inputs
    alone.

    Args:
        asset_id: the processed asset's exact stored identifier string.
        probe: the probe's exact stored name string.
        unit_row_index: the unit's zero-based row index in the units table.
        permutation_index: the replicate index, ``0`` to ``n_permutations - 1``.
        master_seed: the pinned master seed; defaults to ``PARAMS``.

    Returns:
        int: a 64-bit seed for ``numpy.random.PCG64``.
    """
    if master_seed is None:
        master_seed = PARAMS["master_seed"]
    payload = "%d\n%s\n%s\n%d\n%d" % (
        master_seed, asset_id, probe, int(unit_row_index), int(permutation_index)
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def complete_bins(duration_s, bin_seconds=None):
    """Count the complete bins in a recording and the remainder they leave.

    Args:
        duration_s: the recording duration in seconds.
        bin_seconds: bin length in seconds; defaults to ``PARAMS``.

    Returns:
        tuple: ``(n_bins, discarded_s)`` -- the number of complete bins from
        ``t = 0`` and the duration of the discarded final partial bin.

    Raises:
        ValueError: if the recording is shorter than one bin.
    """
    if bin_seconds is None:
        bin_seconds = PARAMS["bin_seconds"]
    if not np.isfinite(duration_s) or duration_s <= 0:
        raise ValueError("duration_s must be a positive finite number, got %r" % (duration_s,))
    n_bins = int(np.floor(duration_s / bin_seconds))
    if n_bins < 1:
        raise ValueError(
            "recording of %.3f s holds no complete %.1f s bin" % (duration_s, bin_seconds)
        )
    return n_bins, float(duration_s - n_bins * bin_seconds)


def bin_offsets(spike_times, n_bins, bin_seconds=None):
    """Locate each complete bin's slice in a unit's time-sorted spike array.

    Spike times are sorted, so a bin's spikes are a contiguous range and the
    whole partition is described by ``n_bins + 1`` boundary indices. Spikes at
    or beyond the last complete bin's end are outside every returned slice.

    Args:
        spike_times: a unit's spike times in seconds, ascending.
        n_bins: the number of complete bins.
        bin_seconds: bin length in seconds; defaults to ``PARAMS``.

    Returns:
        numpy.ndarray: ``n_bins + 1`` boundary indices into ``spike_times``.

    Raises:
        ValueError: if ``spike_times`` is not ascending or is not finite.
    """
    if bin_seconds is None:
        bin_seconds = PARAMS["bin_seconds"]
    spike_times = np.asarray(spike_times, dtype=np.float64)
    if spike_times.size and not np.all(np.isfinite(spike_times)):
        raise ValueError("spike_times contains non-finite values")
    if spike_times.size > 1 and np.any(np.diff(spike_times) < 0):
        raise ValueError("spike_times must be ascending")
    edges = np.arange(n_bins + 1, dtype=np.float64) * bin_seconds
    return np.searchsorted(spike_times, edges, side="left")


def bin_medians(depths, offsets, min_spikes_per_bin=None):
    """Median depth per complete bin, NaN where the bin holds too few spikes.

    Args:
        depths: the unit's per-spike depths, in the same order as its times.
        offsets: boundary indices from :func:`bin_offsets`.
        min_spikes_per_bin: minimum spikes for a bin median to be defined;
            defaults to ``PARAMS``.

    Returns:
        numpy.ndarray: one median per complete bin, NaN where undefined.
    """
    if min_spikes_per_bin is None:
        min_spikes_per_bin = PARAMS["min_spikes_per_bin"]
    depths = np.asarray(depths, dtype=np.float64)
    counts = np.diff(offsets)
    out = np.full(counts.size, np.nan, dtype=np.float64)
    for b in range(counts.size):
        if counts[b] >= min_spikes_per_bin:
            out[b] = np.median(depths[offsets[b]:offsets[b + 1]])
    return out


def excursions(trace, window_bins=None):
    """Peak-to-peak excursion of a trace, whole and worst-window.

    Args:
        trace: the band trace ``D(b)``, one finite value per complete bin.
        window_bins: window length in bins; defaults to ``PARAMS``.

    Returns:
        tuple: ``(delta_full, delta_window, window_start)``. ``window_start`` is
        the first bin of the worst window, or ``None`` when the trace is too
        short to hold one.

    Raises:
        ValueError: if the trace holds a non-finite value.
    """
    if window_bins is None:
        window_bins = PARAMS["window_bins"]
    trace = np.asarray(trace, dtype=np.float64)
    if not np.all(np.isfinite(trace)):
        raise ValueError("trace contains non-finite values; an invalid bin is not skippable")
    delta_full = float(trace.max() - trace.min())
    if trace.size < window_bins:
        return delta_full, None, None
    best, best_start = -np.inf, 0
    for start in range(trace.size - window_bins + 1):
        window = trace[start:start + window_bins]
        span = float(window.max() - window.min())
        if span > best:
            best, best_start = span, start
    return delta_full, best, best_start


def _unit_tables(spike_times, depths, n_bins, bin_seconds, min_spikes_per_bin):
    """Build per-unit bin offsets and observed bin medians.

    Args:
        spike_times: list of per-unit ascending spike-time arrays.
        depths: list of per-unit depth arrays, aligned with ``spike_times``.
        n_bins: number of complete bins.
        bin_seconds: bin length in seconds.
        min_spikes_per_bin: minimum spikes for a defined bin median.

    Returns:
        tuple: ``(offsets, medians)``, both lists indexed by unit.

    Raises:
        ValueError: if a unit's arrays disagree in length or hold non-finite
            depths.
    """
    if len(spike_times) != len(depths):
        raise ValueError(
            "%d unit spike-time arrays and %d unit depth arrays"
            % (len(spike_times), len(depths))
        )
    offsets, medians = [], []
    for u, (times, depth) in enumerate(zip(spike_times, depths)):
        times = np.asarray(times, dtype=np.float64)
        depth = np.asarray(depth, dtype=np.float64)
        if times.size != depth.size:
            raise ValueError(
                "unit %d has %d spike times and %d depths" % (u, times.size, depth.size)
            )
        if depth.size and not np.all(np.isfinite(depth)):
            raise ValueError("unit %d has non-finite depth values" % u)
        off = bin_offsets(times, n_bins, bin_seconds)
        offsets.append(off)
        medians.append(bin_medians(depth, off, min_spikes_per_bin))
    return offsets, medians


def _trace_from_medians(medians, included, min_units_per_bin):
    """Centre each included unit and take the across-unit median per bin.

    Args:
        medians: list of per-unit bin-median arrays.
        included: boolean array marking the included units.
        min_units_per_bin: minimum valid units for a bin to be valid.

    Returns:
        tuple: ``(trace, units_per_bin, invalid_bins)``. ``trace`` holds NaN in
        any invalid bin; the caller decides what an invalid bin means.
    """
    n_bins = medians[0].size if medians else 0
    stack = np.full((int(included.sum()), n_bins), np.nan, dtype=np.float64)
    row = 0
    for u, keep in enumerate(included):
        if not keep:
            continue
        series = medians[u]
        valid = np.isfinite(series)
        stack[row] = series - np.median(series[valid])
        row += 1
    units_per_bin = np.isfinite(stack).sum(axis=0)
    trace = np.full(n_bins, np.nan, dtype=np.float64)
    usable = units_per_bin >= min_units_per_bin
    if usable.any():
        # nanmedian over an all-NaN column warns; only usable columns are taken.
        trace[usable] = np.nanmedian(stack[:, usable], axis=0)
    invalid_bins = np.flatnonzero(~usable)
    return trace, units_per_bin, invalid_bins


def measure_band_drift(spike_times, depths, duration_s, params=None):
    """Compute the observed band excursions and the diagnostics behind them.

    Args:
        spike_times: list of per-unit ascending spike-time arrays, in seconds,
            for the band's units only.
        depths: list of per-unit per-spike depth arrays in micrometres, aligned
            elementwise with ``spike_times``.
        duration_s: the recording duration in seconds.
        params: parameter overrides; defaults to ``PARAMS``.

    Returns:
        dict: ``measurable`` and, when it is False, ``reason`` naming the cause;
        ``delta_full`` and ``delta_window`` in micrometres when it is True; plus
        ``n_bins``, ``discarded_s``, ``included`` unit indices,
        ``units_per_bin``, ``min_units_per_bin_observed``, ``invalid_bins``,
        ``window_start`` and the centred per-unit ``trace``.

    Raises:
        ValueError: if the inputs are malformed -- mismatched array lengths,
            unsorted times, non-finite depths, or a recording shorter than one
            bin. A malformed input is a bug, not an unmeasurable candidate.
    """
    p = dict(PARAMS)
    if params:
        p.update(params)
    n_bins, discarded_s = complete_bins(duration_s, p["bin_seconds"])
    result = {"n_bins": n_bins, "discarded_s": discarded_s, "n_units_in_band": len(spike_times)}

    if len(spike_times) == 0:
        result.update(measurable=False, reason="no units in the band")
        return result

    offsets, medians = _unit_tables(
        spike_times, depths, n_bins, p["bin_seconds"], p["min_spikes_per_bin"]
    )
    defined = np.array([np.isfinite(m).sum() for m in medians], dtype=np.float64)
    included = defined >= p["min_bin_fraction"] * n_bins
    result["included"] = np.flatnonzero(included).tolist()
    result["bins_defined_per_unit"] = defined.astype(int).tolist()

    if included.sum() < p["min_units_per_bin"]:
        result.update(
            measurable=False,
            reason="only %d of %d band units span >= %.0f%% of the %d complete bins with >= %d "
                   "spikes; the gate needs at least %d"
                   % (int(included.sum()), len(spike_times), 100 * p["min_bin_fraction"],
                      n_bins, p["min_spikes_per_bin"], p["min_units_per_bin"]),
        )
        return result

    trace, units_per_bin, invalid = _trace_from_medians(
        medians, included, p["min_units_per_bin"]
    )
    result["units_per_bin"] = units_per_bin.tolist()
    result["min_units_per_bin_observed"] = int(units_per_bin.min())
    result["invalid_bins"] = invalid.tolist()

    if invalid.size:
        result.update(
            measurable=False,
            reason="%d of %d complete bins hold fewer than %d included units with a defined "
                   "median (first offenders: bins %s with %s units); an invalid bin inside a "
                   "window could hide that window's maximum, so it rejects rather than being "
                   "omitted"
                   % (invalid.size, n_bins, p["min_units_per_bin"],
                      invalid[:5].tolist(), units_per_bin[invalid[:5]].tolist()),
        )
        return result

    delta_full, delta_window, window_start = excursions(trace, p["window_bins"])
    if delta_window is None:
        result.update(
            measurable=False,
            reason="%d complete bins is shorter than the %d-bin gate window"
                   % (n_bins, p["window_bins"]),
        )
        return result

    result.update(
        measurable=True,
        delta_full=delta_full,
        delta_window=delta_window,
        window_start=int(window_start),
        trace=trace.tolist(),
    )
    return result


def permutation_null(spike_times, depths, duration_s, asset_id, probe,
                     unit_row_indices, params=None):
    """Build the deterministic within-unit permutation null for ``Delta_10``.

    Every spike time in a complete bin -- and therefore every complete-bin
    spike count -- is held fixed while each unit's analysed depth values are
    permuted among those times. Spikes in the discarded final partial bin do
    not enter the pool. The null therefore preserves bin validity exactly: no
    replicate can be invalid where the observation is valid.

    Args:
        spike_times: list of per-unit ascending spike-time arrays, in seconds.
        depths: list of per-unit depth arrays aligned with ``spike_times``.
        duration_s: the recording duration in seconds.
        asset_id: the processed asset's exact stored identifier string.
        probe: the probe's exact stored name string.
        unit_row_indices: each unit's row index in the units table, in the same
            order as ``spike_times``.
        params: parameter overrides; defaults to ``PARAMS``.

    Returns:
        dict: ``values`` (the replicate ``Delta_10`` values, ascending),
        ``q95`` (the nearest-rank empirical percentile), ``rank`` (the
        one-based rank taken) and ``n_permutations``.

    Raises:
        ValueError: if a replicate turns out unmeasurable, which the fixed bin
            counts make impossible unless the observation was too.
    """
    p = dict(PARAMS)
    if params:
        p.update(params)
    if len(unit_row_indices) != len(spike_times):
        raise ValueError(
            "%d row indices for %d units" % (len(unit_row_indices), len(spike_times))
        )
    normalized_rows = [int(row) for row in unit_row_indices]
    if any(row != normalized or normalized < 0
           for row, normalized in zip(unit_row_indices, normalized_rows)):
        raise ValueError("unit_row_indices must be distinct non-negative integers")
    if len(set(normalized_rows)) != len(normalized_rows):
        raise ValueError("unit_row_indices must be distinct non-negative integers")
    if len(depths) != len(spike_times):
        raise ValueError(
            "%d unit spike-time arrays and %d unit depth arrays"
            % (len(spike_times), len(depths))
        )
    n_bins, _ = complete_bins(duration_s, p["bin_seconds"])
    offsets, medians = _unit_tables(
        spike_times, depths, n_bins, p["bin_seconds"], p["min_spikes_per_bin"]
    )
    defined = np.array([np.isfinite(m).sum() for m in medians], dtype=np.float64)
    included = defined >= p["min_bin_fraction"] * n_bins

    if included.sum() < p["min_units_per_bin"]:
        raise ValueError(
            "the observation is unmeasurable: only %d included units, need at least %d"
            % (int(included.sum()), p["min_units_per_bin"])
        )
    observed_trace, _, observed_invalid = _trace_from_medians(
        medians, included, p["min_units_per_bin"]
    )
    if observed_invalid.size:
        raise ValueError(
            "the observation is unmeasurable: %d complete bins are invalid"
            % observed_invalid.size
        )
    _, observed_window, _ = excursions(observed_trace, p["window_bins"])
    if observed_window is None:
        raise ValueError(
            "the observation is unmeasurable: %d complete bins is shorter than the %d-bin "
            "gate window" % (n_bins, p["window_bins"])
        )

    pools = [np.asarray(d, dtype=np.float64) for d in depths]
    values = np.empty(p["n_permutations"], dtype=np.float64)
    for k in range(p["n_permutations"]):
        replicate = []
        for u in range(len(spike_times)):
            if not included[u]:
                replicate.append(medians[u])
                continue
            seed = derive_permutation_seed(
                asset_id, probe, normalized_rows[u], k, p["master_seed"]
            )
            rng = np.random.Generator(np.random.PCG64(seed))
            shuffled = pools[u].copy()
            first, stop = int(offsets[u][0]), int(offsets[u][-1])
            analysed = pools[u][first:stop]
            shuffled[first:stop] = analysed[rng.permutation(analysed.size)]
            replicate.append(bin_medians(shuffled, offsets[u], p["min_spikes_per_bin"]))
        trace, _, invalid = _trace_from_medians(
            replicate, included, p["min_units_per_bin"]
        )
        if invalid.size:
            raise ValueError(
                "permutation %d produced %d invalid bins; the null preserves bin counts, so "
                "this means the observation was already unmeasurable" % (k, invalid.size)
            )
        _, delta_window, _ = excursions(trace, p["window_bins"])
        values[k] = delta_window

    values.sort()
    rank = int(np.ceil(p["null_percentile"] / 100.0 * p["n_permutations"]))
    return {
        "values": values.tolist(),
        "q95": float(values[rank - 1]),
        "rank": rank,
        "n_permutations": int(p["n_permutations"]),
    }


def apply_gate(observed, null, threshold_um):
    """Apply the two-number drift pass rule at one threshold.

    A candidate passes only when the observed worst-window excursion and the
    null's declared upper summary are both at or below the threshold. An
    observation inside its own null is not a failure -- a genuinely quiet host
    should often be -- but a noise floor wider than the tolerance is, because
    the estimator then cannot speak at the resolution the gate is written in.

    Args:
        observed: the dict returned by :func:`measure_band_drift`.
        null: the dict returned by :func:`permutation_null`, or None when the
            observation was unmeasurable before a null was built.
        threshold_um: the threshold ``L`` in micrometres.

    Returns:
        dict: ``passed``, ``label`` and ``reason``, plus the two numbers the
        decision used.
    """
    if not observed.get("measurable", False):
        return {
            "passed": False,
            "label": "unmeasurable",
            "reason": observed.get("reason", "unmeasurable"),
            "threshold_um": float(threshold_um),
        }
    if null is None or "q95" not in null:
        raise ValueError("a measurable observation requires a permutation-null q95")
    delta = observed["delta_window"]
    q95 = null["q95"]
    if not all(np.isfinite(value) for value in (delta, q95, threshold_um)):
        raise ValueError("delta_window, q95 and threshold_um must all be finite")
    inside_null = delta <= q95
    verdict = {
        "delta_window": delta,
        "q95_null": q95,
        "threshold_um": float(threshold_um),
        "inside_null": bool(inside_null),
    }
    if delta > threshold_um:
        verdict.update(
            passed=False,
            label="resolved drift" if not inside_null else "noise-limited",
            reason="worst-window excursion %.2f um exceeds the %.1f um tolerance; the null's "
                   "95th percentile is %.2f um" % (delta, threshold_um, q95),
        )
    elif q95 > threshold_um:
        verdict.update(
            passed=False,
            label="unmeasurable",
            reason="the null's 95th percentile %.2f um is wider than the %.1f um tolerance, so "
                   "the estimator cannot resolve the gate on this candidate (observed %.2f um)"
                   % (q95, threshold_um, delta),
        )
    else:
        verdict.update(
            passed=True,
            label="no time-ordered drift resolved" if inside_null else "resolved, within tolerance",
            reason="worst-window excursion %.2f um and null 95th percentile %.2f um are both at "
                   "or below the %.1f um tolerance" % (delta, q95, threshold_um),
        )
    return verdict
