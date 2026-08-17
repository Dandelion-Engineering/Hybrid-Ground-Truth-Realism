"""Probe an assumption-free bound for the completed-data permutation null.

The pre-card missing-depth design says that an assumption-free interval for
``Q95_null`` is necessarily vacuous because adding the missing values changes
the permutation.  This probe checks the premise directly.  The completed spike
times, the number and original positions of the missing depths, and the
deterministic seed are all known before any missing value is chosen.  Therefore
each replicate's permutation of the *complete* vector is fixed across every
completion.  Unknown values can be followed to their destination bins and the
same exact bin-median interval used by the candidate can be propagated through
the approved null.

This is reviewer evidence, not packet code.  It uses synthetic arrays only and
does not read an archive or alter the candidate implementation.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Codex/tools/probe_missing_depth_actual_null.py" --permutations 200
"""

import argparse
import os
import sys

import numpy as np


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "Reproducibility Packet", "scripts"))

from utils import band_drift as bd  # noqa: E402
from utils import missing_depth as md  # noqa: E402


FIXTURE_SEED = 20260817


def split_fixture(n_units=15, n_bins=12, finite_per_bin=200,
                  missing_per_bin=1, width_um=300.0, seed=FIXTURE_SEED):
    """Build finite observations plus known-time missing-depth positions.

    Args:
        n_units: number of band units.
        n_bins: number of complete one-minute bins.
        finite_per_bin: observed finite depths in every unit/bin.
        missing_per_bin: missing depths in every unit/bin.
        width_um: width of each bin's uniform finite-depth distribution.
        seed: deterministic fixture seed.

    Returns:
        tuple: finite times, finite depths, missing times, row indices and
        recording extent.
    """
    rng = np.random.default_rng(seed)
    finite_times, finite_depths, missing_times = [], [], []
    for _ in range(n_units):
        unit_times, unit_depths, unit_missing = [], [], []
        for b in range(n_bins):
            base = 60.0 * b
            unit_times.extend(
                (base + np.linspace(0.01, 55.0, finite_per_bin)).tolist()
            )
            unit_depths.extend(
                rng.uniform(0.0, width_um, size=finite_per_bin).tolist()
            )
            if missing_per_bin:
                unit_missing.extend(
                    (base + np.linspace(56.0, 59.0, missing_per_bin)).tolist()
                )
        finite_times.append(np.asarray(unit_times, dtype=np.float64))
        finite_depths.append(np.asarray(unit_depths, dtype=np.float64))
        missing_times.append(np.asarray(unit_missing, dtype=np.float64))
    return (
        finite_times,
        finite_depths,
        missing_times,
        list(range(n_units)),
        float(n_bins * 60.0),
    )


def merge_layout(finite_times, finite_depths, missing_times):
    """Reconstruct complete time order with NaN placeholders for missing values.

    The synthetic fixture has distinct times.  A production reader should
    preserve the original all-spike order or a missing-position mask directly,
    rather than attempting to reconstruct the order from times when ties are
    possible.

    Args:
        finite_times: observed spike times.
        finite_depths: observed depths aligned with ``finite_times``.
        missing_times: known times of missing-depth spikes.

    Returns:
        tuple: complete ascending times and aligned values, with NaN exactly at
        the missing positions.
    """
    finite_times = np.asarray(finite_times, dtype=np.float64)
    finite_depths = np.asarray(finite_depths, dtype=np.float64)
    missing_times = np.asarray(missing_times, dtype=np.float64)
    times = np.concatenate([finite_times, missing_times])
    values = np.concatenate([
        finite_depths,
        np.full(missing_times.size, np.nan, dtype=np.float64),
    ])
    order = np.argsort(times, kind="stable")
    return times[order], values[order]


def complete_record(finite_times, finite_depths, missing_times, fills):
    """Merge a chosen finite completion into complete per-unit arrays.

    Args:
        finite_times: list of observed per-unit spike times.
        finite_depths: aligned observed depths.
        missing_times: list of known missing-depth times.
        fills: completion values aligned with ``missing_times``.

    Returns:
        tuple: complete per-unit times and depths, time sorted.
    """
    all_times, all_depths = [], []
    for times, depths, missing, fill in zip(
            finite_times, finite_depths, missing_times, fills):
        merged_times = np.concatenate([times, missing])
        merged_depths = np.concatenate([depths, np.asarray(fill, dtype=np.float64)])
        order = np.argsort(merged_times, kind="stable")
        all_times.append(merged_times[order])
        all_depths.append(merged_depths[order])
    return all_times, all_depths


def actual_null_interval(finite_times, finite_depths, missing_times, extent_s,
                         asset_id, probe, rows, params=None):
    """Bound the approved null over all completions of the missing depths.

    Unlike the proposed fixed-arrangement counterfactual, this applies the
    approved permutation to the complete ``n + k`` vector.  The permutation is
    fixed by its seed and vector length, so each replicate exposes exactly how
    many unknown source values land in every destination bin.

    Args:
        finite_times: list of observed per-unit spike-time arrays.
        finite_depths: aligned observed finite depths.
        missing_times: known per-unit times of the missing depths.
        extent_s: complete recording grid extent.
        asset_id: seed input used by the approved null.
        probe: seed input used by the approved null.
        rows: original unit-table row indices.
        params: optional approved-parameter overrides.

    Returns:
        dict: sorted lower and upper replicate bounds, their nearest-rank
        percentile endpoints, and the support-invariance result.

    Raises:
        ValueError: if the split record is not support invariant or the lists
        disagree in length.
    """
    p = dict(bd.PARAMS)
    if params:
        p.update(params)
    if not (len(finite_times) == len(finite_depths) == len(missing_times)
            == len(rows)):
        raise ValueError("the four per-unit lists disagree in length")
    normalized_rows = [int(row) for row in rows]
    if any(row != normalized or normalized < 0
           for row, normalized in zip(rows, normalized_rows)):
        raise ValueError("rows must be distinct non-negative integers")
    if len(set(normalized_rows)) != len(normalized_rows):
        raise ValueError("rows must be distinct non-negative integers")

    n_bins, _ = bd.complete_bins(extent_s, p["bin_seconds"])
    finite_tables = [
        md.unit_intervals(
            finite_times[u], finite_depths[u], missing_times[u], n_bins, p
        )
        for u in range(len(finite_times))
    ]
    support = md.support_invariance(finite_tables, p)
    if not support["invariant"]:
        raise ValueError("the split record is not support invariant: %s"
                         % support["reason"])
    included = support["included_complete"]

    layouts = [
        merge_layout(finite_times[u], finite_depths[u], missing_times[u])
        for u in range(len(finite_times))
    ]
    offsets = [
        bd.bin_offsets(times, n_bins, p["bin_seconds"])
        for times, _ in layouts
    ]
    lower_values = np.empty(p["n_permutations"], dtype=np.float64)
    upper_values = np.empty(p["n_permutations"], dtype=np.float64)

    for replicate_index in range(p["n_permutations"]):
        lower_stack = np.full((int(included.sum()), n_bins), np.nan)
        upper_stack = np.full((int(included.sum()), n_bins), np.nan)
        output_row = 0
        for u, keep in enumerate(included):
            if not keep:
                continue
            _, known = layouts[u]
            first, stop = int(offsets[u][0]), int(offsets[u][-1])
            seed = bd.derive_permutation_seed(
                asset_id, probe, normalized_rows[u], replicate_index,
                p["master_seed"]
            )
            rng = np.random.Generator(np.random.PCG64(seed))
            permuted = known.copy()
            analysed = known[first:stop]
            permuted[first:stop] = analysed[rng.permutation(analysed.size)]

            lo = np.full(n_bins, np.nan, dtype=np.float64)
            hi = np.full(n_bins, np.nan, dtype=np.float64)
            for b in range(n_bins):
                complete_count = offsets[u][b + 1] - offsets[u][b]
                if complete_count < p["min_spikes_per_bin"]:
                    continue
                destination = permuted[offsets[u][b]:offsets[u][b + 1]]
                values = destination[np.isfinite(destination)]
                n_missing = int(destination.size - values.size)
                if values.size == 0:
                    lo[b], hi[b] = -np.inf, np.inf
                else:
                    lo[b], hi[b] = md.median_interval(values, n_missing)

            valid = ~np.isnan(lo)
            centre_lo = float(np.median(lo[valid]))
            centre_hi = float(np.median(hi[valid]))
            lower_stack[output_row, valid] = lo[valid] - centre_hi
            upper_stack[output_row, valid] = hi[valid] - centre_lo
            output_row += 1

        lo_trace, hi_trace, invalid = md.trace_intervals(
            lower_stack, upper_stack, p["min_units_per_bin"]
        )
        if invalid.size:
            raise ValueError("replicate %d has invalid complete-data bins" %
                             replicate_index)
        bounds = md.interval_excursions(lo_trace, hi_trace, p["window_bins"])
        lower_values[replicate_index] = bounds["delta_window_lo"]
        upper_values[replicate_index] = bounds["delta_window_hi"]

    lower_values.sort()
    upper_values.sort()
    rank = int(np.ceil(
        p["null_percentile"] / 100.0 * p["n_permutations"]
    ))
    return {
        "values_lo": lower_values.tolist(),
        "values_hi": upper_values.tolist(),
        "q95_lo": float(lower_values[rank - 1]),
        "q95_hi": float(upper_values[rank - 1]),
        "rank": rank,
        "support": support,
    }


def run_probe(n_permutations):
    """Run zero-missing, containment and non-vacuity checks.

    Args:
        n_permutations: number of deterministic null replicates.

    Returns:
        int: zero when every check passes, otherwise one.
    """
    checks = []

    def check(name, condition, detail):
        """Record and print one check."""
        checks.append((name, bool(condition)))
        print("  %-50s %s  %s" %
              (name, "ok" if condition else "FAIL", detail))

    params = {"n_permutations": int(n_permutations)}
    finite_t, finite_d, missing_t, rows, extent = split_fixture()
    actual = actual_null_interval(
        finite_t, finite_d, missing_t, extent, "asset", "Probe00", rows, params
    )
    check(
        "completed-data bound is finite",
        np.isfinite(actual["q95_lo"]) and np.isfinite(actual["q95_hi"]),
        "[%.3f, %.3f] um" % (actual["q95_lo"], actual["q95_hi"]),
    )
    check(
        "completed-data bound is non-vacuous",
        actual["q95_hi"] - actual["q95_lo"] < 100.0,
        "width %.3f um" % (actual["q95_hi"] - actual["q95_lo"]),
    )

    fills = [
        ("all low", [np.full(times.size, -3000.0) for times in missing_t]),
        ("all high", [np.full(times.size, 3000.0) for times in missing_t]),
        ("mixed", [np.linspace(-500.0, 500.0, times.size)
                   for times in missing_t]),
    ]
    for name, fill in fills:
        complete_t, complete_d = complete_record(
            finite_t, finite_d, missing_t, fill
        )
        q95 = bd.permutation_null(
            complete_t, complete_d, extent, "asset", "Probe00", rows, params
        )["q95"]
        inside = actual["q95_lo"] - 1e-9 <= q95 <= actual["q95_hi"] + 1e-9
        check(
            "%s completion is contained" % name,
            inside,
            "q95 %.3f um" % q95,
        )

    zero_missing = [np.empty(0, dtype=np.float64) for _ in finite_t]
    zero = actual_null_interval(
        finite_t, finite_d, zero_missing, extent,
        "asset", "Probe00", rows, params
    )
    approved = bd.permutation_null(
        finite_t, finite_d, extent, "asset", "Probe00", rows, params
    )
    check(
        "zero-missing lower path reproduces approved null",
        zero["values_lo"] == approved["values"],
        "%d replicates" % n_permutations,
    )
    check(
        "zero-missing upper path reproduces approved null",
        zero["values_hi"] == approved["values"],
        "%d replicates" % n_permutations,
    )

    counterfactual = md.null_interval(
        finite_t, finite_d, missing_t, extent,
        "asset", "Probe00", rows, params
    )
    differs = (
        actual["values_lo"] != counterfactual["values_lo"]
        or actual["values_hi"] != counterfactual["values_hi"]
    )
    check(
        "actual and counterfactual nulls are distinct",
        differs,
        "actual [%.3f, %.3f], counterfactual [%.3f, %.3f] um"
        % (actual["q95_lo"], actual["q95_hi"],
           counterfactual["q95_lo"], counterfactual["q95_hi"]),
    )

    failed = [name for name, ok in checks if not ok]
    print("%d checks, %d failed" % (len(checks), len(failed)))
    return 1 if failed else 0


def main():
    """Parse CLI arguments and run the synthetic probe."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--permutations", type=int, default=40,
        help="deterministic null replicates; use 200 for the pinned gate count",
    )
    args = parser.parse_args()
    return run_probe(args.permutations)


if __name__ == "__main__":
    sys.exit(main())
