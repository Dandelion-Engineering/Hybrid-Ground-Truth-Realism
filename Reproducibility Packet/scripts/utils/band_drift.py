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

1. Accept the caller-supplied band units. The archive reader, not this numeric
   utility, applies the label-blind ``max_electrode -> rel_y`` membership rule.
2. Partition the session-time extent into full-width fixed bins from ``t = 0``.
   A final underlength grid interval is discarded and its duration is reported.
   When the AP stream starts after session zero, the first full-width grid bin
   has less than a full bin of recording coverage; that coverage is reported by
   the archive reader and the bin is retained by the predeclared specification.
3. ``d_u(b)`` is the median per-spike depth of unit ``u`` in bin ``b``, defined
   only where the unit has at least ``min_spikes_per_bin`` spikes in that bin.
4. ``delta_u(b) = d_u(b) - median_b' d_u(b')`` centres each unit on its own
   typical depth so units at different depths can be pooled.
5. ``D(b)`` is the median of ``delta_u(b)`` across included units, under the
   modelling assumption that real movement is common to the band while
   depth-estimation noise is not. The assumption is not self-verifying: a
   majority of movement-insensitive traces can hold the across-unit median flat
   while a minority moves. ``measure_band_drift`` therefore returns each
   included unit's whole-recording excursion, its own worst-window excursion,
   and its excursion inside the band-selected window. The first two expose
   movement that the across-unit median can suppress; the third shows the
   composition aligned to the window that produced ``Delta_10``. Those
   per-unit values are reported and never consumed by the gate.
6. ``Delta_full = max_b D(b) - min_b D(b)`` over the whole recording, and
   ``Delta_10`` is the largest such range over any window of
   ``window_bins`` consecutive analysed bins. Both are peak-to-peak excursions,
   not endpoint-to-endpoint net motion: a down-and-back trajectory stays
   visible. ``Delta_10`` is the gating quantity.

The null
--------
Within the analysed full-width grid bins, holding every spike time fixed and
permuting a unit's depth values among its own analysed spikes destroys the
depth/time ordering while preserving every analysed depth value, spike time and
per-bin spike count. Spikes before the grid origin, and spikes in the discarded
final underlength interval, enter neither the observed statistic nor the null.
The resulting ``Delta_10`` distribution is what this estimator returns on this
recording with no time ordering, and its nearest-rank
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
unmeasurable failure, and so are too few qualifying units, any invalid analysed
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


def complete_bins(extent_s, bin_seconds=None):
    """Count full-width session-grid bins and the final remainder they leave.

    Args:
        extent_s: the final timestamp on the session-time grid, in seconds.
        bin_seconds: bin length in seconds; defaults to ``PARAMS``.

    Returns:
        tuple: ``(n_bins, discarded_s)`` -- the number of full-width grid
        bins from ``t = 0`` and the duration of the discarded final underlength
        interval. Throughout this module a "complete" bin means full-width on
        the session grid, which is what this function counts; it does not mean
        full recording coverage. A stream starting after session zero leaves
        bin 0 undercovered and the specification retains it, so the reader
        reports that coverage rather than inferring it from ``n_bins``.

    Raises:
        ValueError: if the recording is shorter than one bin.
    """
    if bin_seconds is None:
        bin_seconds = PARAMS["bin_seconds"]
    if not np.isfinite(extent_s) or extent_s <= 0:
        raise ValueError("extent_s must be a positive finite number, got %r" % (extent_s,))
    n_bins = int(np.floor(extent_s / bin_seconds))
    if n_bins < 1:
        raise ValueError(
            "session-time extent of %.3f s holds no full-width %.1f s grid bin"
            % (extent_s, bin_seconds)
        )
    return n_bins, float(extent_s - n_bins * bin_seconds)


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


def unit_traces(medians, included):
    """Centre each included unit on its own across-bin median.

    This is the single definition of the centring step ``delta_u(b) = d_u(b) -
    median_b' d_u(b')``. The band trace and the per-unit audit values are both
    built from it, so a caller reporting per-unit excursions never restates the
    centring rule.

    Args:
        medians: list of per-unit bin-median arrays, one entry per band unit.
        included: boolean mask over ``medians`` marking the included units.

    Returns:
        numpy.ndarray: an ``(n_included, n_bins)`` array of centred series, in
        ascending order of the unit's index in ``medians``. NaN marks a bin
        where that unit has no defined median.

    Raises:
        ValueError: if the mask does not match ``medians``, or if an included
            unit has no defined bin median to centre on. Neither is reachable
            through :func:`measure_band_drift`, whose inclusion rule requires a
            defined median in at least ``min_bin_fraction`` of the bins.
    """
    included = np.asarray(included, dtype=bool)
    if included.size != len(medians):
        raise ValueError(
            "%d unit median arrays and a mask of length %d"
            % (len(medians), included.size)
        )
    n_bins = medians[0].size if len(medians) else 0
    stack = np.full((int(included.sum()), n_bins), np.nan, dtype=np.float64)
    row = 0
    for u, keep in enumerate(included):
        if not keep:
            continue
        series = np.asarray(medians[u], dtype=np.float64)
        valid = np.isfinite(series)
        if not valid.any():
            raise ValueError("included unit %d has no defined bin median" % u)
        stack[row] = series - np.median(series[valid])
        row += 1
    return stack


def unit_excursions(stack, band_window_start=None, window_bins=None):
    """Report each unit's whole, own-worst and band-window excursions.

    These are audit quantities. They expose the composition behind the
    across-unit median ``D(b)`` -- including a minority that moves in a window
    other than the one selected from a flat or differently moving band trace --
    and no gate consumes them.

    Args:
        stack: centred per-unit series from :func:`unit_traces`.
        band_window_start: first bin of the band's gating window, or None when
            no aligned band-window value is requested.
        window_bins: window length in bins; defaults to ``PARAMS``.

    Returns:
        dict: six lists, each aligned with the rows of ``stack``:
        ``delta_full``; ``delta_max_window`` and ``max_window_start`` for each
        unit's own worst window; ``max_window_n_defined`` for that window;
        ``delta_band_window`` inside the band-selected window; and
        ``band_window_n_defined`` for that window. An excursion is None when
        fewer than two defined bin medians are present in its span.

    Raises:
        ValueError: if ``stack`` is not two-dimensional, ``window_bins`` is not
            a positive integer, or ``band_window_start`` does not identify a
            complete window inside ``stack``.
    """
    if window_bins is None:
        window_bins = PARAMS["window_bins"]
    stack = np.asarray(stack, dtype=np.float64)
    if stack.ndim != 2:
        raise ValueError("stack must be a two-dimensional unit-by-bin array")
    if isinstance(window_bins, (bool, np.bool_)) or int(window_bins) != window_bins \
            or int(window_bins) <= 0:
        raise ValueError("window_bins must be a positive integer")
    window_bins = int(window_bins)
    n_units, n_bins = stack.shape

    def span(row):
        """Return a range and defined count; one point cannot define motion."""
        valid = row[np.isfinite(row)]
        return (
            float(valid.max() - valid.min()) if valid.size >= 2 else None,
            int(valid.size),
        )

    delta_full = [span(row)[0] for row in stack]
    delta_max_window = [None] * n_units
    max_window_start = [None] * n_units
    max_window_n_defined = [0] * n_units
    if n_bins >= window_bins:
        for u, row in enumerate(stack):
            for start in range(n_bins - window_bins + 1):
                value, count = span(row[start:start + window_bins])
                if value is None:
                    continue
                if delta_max_window[u] is None or value > delta_max_window[u]:
                    delta_max_window[u] = value
                    max_window_start[u] = start
                    max_window_n_defined[u] = count

    delta_band_window = [None] * n_units
    band_window_n_defined = [0] * n_units
    if band_window_start is not None:
        if isinstance(band_window_start, (bool, np.bool_)) \
                or int(band_window_start) != band_window_start:
            raise ValueError("band_window_start must be an integer")
        band_window_start = int(band_window_start)
        if band_window_start < 0 or band_window_start + window_bins > n_bins:
            raise ValueError(
                "band window [%d, %d) falls outside %d bins"
                % (band_window_start, band_window_start + window_bins, n_bins)
            )
        for u, row in enumerate(stack):
            value, count = span(
                row[band_window_start:band_window_start + window_bins]
            )
            delta_band_window[u] = value
            band_window_n_defined[u] = count

    return {
        "delta_full": delta_full,
        "delta_max_window": delta_max_window,
        "max_window_start": max_window_start,
        "max_window_n_defined": max_window_n_defined,
        "delta_band_window": delta_band_window,
        "band_window_n_defined": band_window_n_defined,
    }


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
    stack = unit_traces(medians, included)
    units_per_bin = np.isfinite(stack).sum(axis=0)
    trace = np.full(n_bins, np.nan, dtype=np.float64)
    usable = units_per_bin >= min_units_per_bin
    if usable.any():
        # nanmedian over an all-NaN column warns; only usable columns are taken.
        trace[usable] = np.nanmedian(stack[:, usable], axis=0)
    invalid_bins = np.flatnonzero(~usable)
    return trace, units_per_bin, invalid_bins


def measure_band_drift(spike_times, depths, extent_s, params=None):
    """Compute the observed band excursions and the diagnostics behind them.

    Args:
        spike_times: list of per-unit ascending spike-time arrays, in seconds,
            for the band's units only.
        depths: list of per-unit per-spike depth arrays in micrometres, aligned
            elementwise with ``spike_times``.
        extent_s: the raw AP stream's final aligned timestamp on the shared
            session-time grid, in seconds. This is ``t_last_s``, not the
            ``t_last_s - t_first_s`` span recorded as ``duration_s`` by the
            timing screen.
        params: parameter overrides; defaults to ``PARAMS``.

    Returns:
        dict: ``measurable`` and, when it is False, ``reason`` naming the cause;
        ``delta_full`` and ``delta_window`` in micrometres when it is True; plus
        ``n_bins``, ``discarded_s``, ``included`` unit indices,
        ``units_per_bin``, ``min_units_per_bin_observed``, ``invalid_bins``,
        ``window_start``, and ``trace``, the across-unit band trace ``D(b)``
        built from the centred per-unit series. When it is measurable it also
        carries six per-unit audit lists aligned with ``included``:
        ``unit_delta_full``; ``unit_delta_max_window`` and
        ``unit_max_window_start`` for each unit's own worst window;
        ``unit_max_window_defined_bins`` for its support; and
        ``unit_delta_band_window`` / ``unit_band_window_defined_bins`` inside
        the band-selected window. The gate reads ``delta_window`` and never
        these audit values.

    Raises:
        ValueError: if the inputs are malformed -- mismatched array lengths,
            unsorted times, non-finite depths, or a recording shorter than one
            bin. A malformed input is a bug, not an unmeasurable candidate.
    """
    p = dict(PARAMS)
    if params:
        p.update(params)
    n_bins, discarded_s = complete_bins(extent_s, p["bin_seconds"])
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
            reason="only %d of %d band units span >= %.0f%% of the %d analysed bins with >= %d "
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
            reason="%d of %d analysed bins hold fewer than %d included units with a defined "
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
            reason="%d analysed bins is shorter than the %d-bin gate window"
                   % (n_bins, p["window_bins"]),
        )
        return result

    unit_audit = unit_excursions(
        unit_traces(medians, included), window_start, p["window_bins"]
    )
    result.update(
        measurable=True,
        delta_full=delta_full,
        delta_window=delta_window,
        window_start=int(window_start),
        trace=trace.tolist(),
        unit_delta_full=unit_audit["delta_full"],
        unit_delta_max_window=unit_audit["delta_max_window"],
        unit_max_window_start=unit_audit["max_window_start"],
        unit_max_window_defined_bins=unit_audit["max_window_n_defined"],
        unit_delta_band_window=unit_audit["delta_band_window"],
        unit_band_window_defined_bins=unit_audit["band_window_n_defined"],
    )
    return result


def permutation_null(spike_times, depths, extent_s, asset_id, probe,
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
        extent_s: the raw AP stream's final aligned timestamp on the shared
            session-time grid, in seconds (``t_last_s``, not the timing
            screen's ``duration_s`` span).
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
    n_bins, _ = complete_bins(extent_s, p["bin_seconds"])
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
            "the observation is unmeasurable: %d analysed bins are invalid"
            % observed_invalid.size
        )
    _, observed_window, _ = excursions(observed_trace, p["window_bins"])
    if observed_window is None:
        raise ValueError(
            "the observation is unmeasurable: %d analysed bins is shorter than the %d-bin "
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
