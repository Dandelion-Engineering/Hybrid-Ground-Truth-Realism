"""Independent Round-1 probes for Review Card RC-001.

The candidate's own harness is extensive, but a formal full-artifact review
should not establish correctness only by re-running tests written with the
candidate.  This probe independently reconstructs the observed statistic and a
small deterministic permutation null, stresses exact grid edges and excluded
head/tail spikes, verifies that null construction does not mutate caller data,
and exhausts the gate's decision boundaries.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Codex/tools/probe_rc001_round1.py" --repo-root .
"""

import argparse
import hashlib
import importlib.util
import pathlib

import numpy as np


def load_module(repo_root):
    """Load the candidate utility from an explicit repository root."""
    path = repo_root / "Reproducibility Packet" / "scripts" / "utils" / "band_drift.py"
    spec = importlib.util.spec_from_file_location("rc001_band_drift", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reference_observation(spike_times, depths, extent_s, params):
    """Recompute the observed statistic without calling candidate helpers."""
    width = params["bin_seconds"]
    n_bins = int(np.floor(extent_s / width))
    medians = []
    for times, values in zip(spike_times, depths):
        row = np.full(n_bins, np.nan, dtype=np.float64)
        for b in range(n_bins):
            take = (times >= b * width) & (times < (b + 1) * width)
            if int(take.sum()) >= params["min_spikes_per_bin"]:
                row[b] = np.median(values[take])
        medians.append(row)
    included = np.array(
        [np.isfinite(row).sum() >= params["min_bin_fraction"] * n_bins
         for row in medians],
        dtype=bool,
    )
    centred = np.stack([
        row - np.median(row[np.isfinite(row)])
        for row, keep in zip(medians, included) if keep
    ])
    units_per_bin = np.isfinite(centred).sum(axis=0)
    trace = np.array([
        np.median(centred[np.isfinite(centred[:, b]), b])
        if units_per_bin[b] >= params["min_units_per_bin"] else np.nan
        for b in range(n_bins)
    ])
    full = float(trace.max() - trace.min())
    windows = [
        float(trace[start:start + params["window_bins"]].max()
              - trace[start:start + params["window_bins"]].min())
        for start in range(n_bins - params["window_bins"] + 1)
    ]
    best = max(windows)
    start = windows.index(best)
    return {
        "included": np.flatnonzero(included).tolist(),
        "trace": trace,
        "units_per_bin": units_per_bin,
        "delta_full": full,
        "delta_window": best,
        "window_start": start,
    }


def reference_null(spike_times, depths, extent_s, asset, probe, rows, params):
    """Recompute a small null from the literal seed and binning rules."""
    width = params["bin_seconds"]
    n_bins = int(np.floor(extent_s / width))
    observed = reference_observation(spike_times, depths, extent_s, params)
    included = set(observed["included"])
    values = []
    for k in range(params["n_permutations"]):
        permuted = []
        for u, (times, source) in enumerate(zip(spike_times, depths)):
            values_u = source.copy()
            if u in included:
                analysed = (times >= 0.0) & (times < n_bins * width)
                payload = "%d\n%s\n%s\n%d\n%d" % (
                    params["master_seed"], asset, probe, rows[u], k
                )
                seed = int(hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16], 16)
                rng = np.random.Generator(np.random.PCG64(seed))
                values_u[analysed] = source[analysed][rng.permutation(int(analysed.sum()))]
            permuted.append(values_u)
        values.append(reference_observation(
            spike_times, permuted, extent_s, params
        )["delta_window"])
    values.sort()
    rank = int(np.ceil(params["null_percentile"] / 100.0 * len(values)))
    return values, values[rank - 1], rank


def make_random_fixture(rng, n_units, n_bins):
    """Build a supported fixture with irregular counts and missing unit-bins."""
    spike_times, depths = [], []
    common = np.cumsum(rng.normal(0.0, 2.0, size=n_bins))
    for u in range(n_units):
        times_u, depths_u = [], []
        # One different underfilled bin per unit exercises availability while
        # leaving at least five contributors in every bin.
        missing = {u % n_bins}
        for b in range(n_bins):
            count = 6 if b in missing else int(rng.integers(10, 16))
            times = b * 60.0 + np.sort(rng.uniform(0.0, 60.0, size=count))
            values = 1000.0 + 25.0 * u + common[b] + rng.normal(0.0, 8.0, size=count)
            times_u.extend(times.tolist())
            depths_u.extend(values.tolist())
        spike_times.append(np.asarray(times_u, dtype=np.float64))
        depths.append(np.asarray(depths_u, dtype=np.float64))
    return spike_times, depths


def main():
    """Run all independent probes and return a shell status."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=pathlib.Path, required=True)
    args = parser.parse_args()
    bd = load_module(args.repo_root.resolve())
    failures = []

    def check(name, condition, detail=""):
        """Record and print one probe result."""
        ok = bool(condition)
        print("%-58s %s%s" % (name, "ok" if ok else "FAIL", "  " + detail if detail else ""))
        if not ok:
            failures.append(name)

    rng = np.random.default_rng(24001)
    random_failure = None
    for trial in range(40):
        n_bins = int(rng.integers(10, 25))
        n_units = int(rng.integers(6, 16))
        times, depths = make_random_fixture(rng, n_units, n_bins)
        observed = bd.measure_band_drift(times, depths, n_bins * 60.0 + 17.25)
        expected = reference_observation(times, depths, n_bins * 60.0 + 17.25, bd.PARAMS)
        same = (
            observed["measurable"]
            and observed["included"] == expected["included"]
            and np.array_equal(observed["units_per_bin"], expected["units_per_bin"])
            and np.allclose(observed["trace"], expected["trace"], atol=0.0, rtol=0.0)
            and observed["delta_full"] == expected["delta_full"]
            and observed["delta_window"] == expected["delta_window"]
            and observed["window_start"] == expected["window_start"]
        )
        if not same:
            random_failure = trial
            break
    check("40 randomized observations match an independent reference",
          random_failure is None,
          "first mismatch trial %d" % random_failure if random_failure is not None else "")

    n_bins, per_bin, n_units = 12, 10, 6
    grid = np.concatenate([
        b * 60.0 + np.arange(per_bin, dtype=np.float64) * 5.0
        for b in range(n_bins)
    ])
    levels = np.repeat(np.array([0, 1, 2, 4, 8, 16, 8, 4, 2, 1, 0, -1.0]), per_bin)
    times, depths = [], []
    for u in range(n_units):
        times.append(np.concatenate(([-0.001], grid, [n_bins * 60.0])))
        depths.append(np.concatenate(([1e9], 1000.0 + 20.0 * u + levels, [-1e9])))
    edge = bd.measure_band_drift(times, depths, n_bins * 60.0 + 0.5)
    check("negative and exact-tail spikes stay outside analysed bins",
          edge["delta_full"] == 17.0 and edge["delta_window"] == 17.0,
          "Delta_full %.3f, Delta_10 %.3f" % (edge["delta_full"], edge["delta_window"]))
    check("the exact worst window is located on the session grid",
          edge["window_start"] == 2, "start %d" % edge["window_start"])

    small_params = dict(bd.PARAMS)
    small_params["n_permutations"] = 9
    before_times = [row.copy() for row in times]
    before_depths = [row.copy() for row in depths]
    shipped = bd.permutation_null(times, depths, n_bins * 60.0 + 0.5,
                                  "asset-RC001", "probe01", list(range(n_units)),
                                  small_params)
    ref_values, ref_q95, ref_rank = reference_null(
        times, depths, n_bins * 60.0 + 0.5, "asset-RC001", "probe01",
        list(range(n_units)), small_params
    )
    check("small deterministic null matches an independent replay bytewise",
          shipped["values"] == ref_values and shipped["q95"] == ref_q95
          and shipped["rank"] == ref_rank)
    check("null construction does not mutate caller arrays",
          all(np.array_equal(a, b) for a, b in zip(times, before_times))
          and all(np.array_equal(a, b) for a, b in zip(depths, before_depths)))

    boundary_values = (0.0, 19.999, 20.0, 20.001, 40.0, 40.001)
    gate_ok = True
    for threshold in (20.0, 40.0):
        for delta in boundary_values:
            for q95 in boundary_values:
                verdict = bd.apply_gate(
                    {"measurable": True, "delta_window": delta}, {"q95": q95}, threshold
                )
                gate_ok &= verdict["passed"] == (delta <= threshold and q95 <= threshold)
                if delta > threshold:
                    expected_label = "resolved drift" if delta > q95 else "noise-limited"
                    gate_ok &= verdict["label"] == expected_label
                elif q95 > threshold:
                    gate_ok &= verdict["label"] == "unmeasurable"
    check("all strict/relaxed decision-boundary combinations match the rule", gate_ok)

    # The candidate calls ten consecutive one-minute bin medians a worst
    # ten-minute excursion.  Ten bin centres span only nine minutes.  A smooth
    # common ramp can therefore move more than one row inside an actual
    # ten-minute segment while both implemented gate numbers remain below it.
    n_bins, per_bin = 61, 100
    regular = np.concatenate([
        b * 60.0 + np.linspace(0.1, 59.9, per_bin) for b in range(n_bins)
    ])
    smooth = 2.1 * regular / 60.0
    smooth_times = [regular.copy() for _ in range(5)]
    smooth_depths = [smooth + 100.0 * u for u in range(5)]
    smooth_obs = bd.measure_band_drift(smooth_times, smooth_depths, n_bins * 60.0)
    smooth_null = bd.permutation_null(
        smooth_times, smooth_depths, n_bins * 60.0, "smooth-alias", "probe01",
        list(range(5))
    )
    smooth_gate = bd.apply_gate(smooth_obs, smooth_null, 20.0)
    check("smooth 21 um per ten minutes passes the declared 20 um gate",
          smooth_gate["passed"] and abs(smooth_obs["delta_window"] - 18.9) < 1e-10,
          "actual 21.000, Delta_10 %.3f, Q95 %.3f"
          % (smooth_obs["delta_window"], smooth_null["q95"]))

    # A common displacement occupying fewer than half of one bin is present in
    # the per-spike depths but erased by every per-bin median.  The per-unit
    # audit uses the same medians and therefore does not expose it either.
    n_bins, per_bin = 12, 10
    regular = np.concatenate([
        b * 60.0 + np.linspace(2.0, 56.0, per_bin) for b in range(n_bins)
    ])
    brief = np.zeros(regular.size, dtype=np.float64)
    brief[(regular >= 322.0) & (regular < 346.0)] = 30.0
    brief_times = [regular.copy() for _ in range(5)]
    brief_depths = [brief + 100.0 * u for u in range(5)]
    brief_obs = bd.measure_band_drift(brief_times, brief_depths, n_bins * 60.0)
    brief_null = bd.permutation_null(
        brief_times, brief_depths, n_bins * 60.0, "brief-alias", "probe01",
        list(range(5))
    )
    brief_gate = bd.apply_gate(brief_obs, brief_null, 20.0)
    check("common 30 um within-bin movement passes at 0/0 and vanishes from audit",
          brief_gate["passed"] and brief_obs["delta_window"] == 0.0
          and brief_null["q95"] == 0.0
          and brief_obs["unit_delta_max_window"] == [0.0] * 5)

    # An arbitrary ten-minute segment may contain portions of eleven session
    # bins.  No aligned ten-bin window below contains both extreme bins.
    levels = np.array([0.0] + [15.0] * 9 + [30.0, 15.0])
    offset = np.repeat(levels, per_bin)
    offset_depths = [offset + 100.0 * u for u in range(5)]
    offset_obs = bd.measure_band_drift(brief_times, offset_depths, n_bins * 60.0)
    offset_null = bd.permutation_null(
        brief_times, offset_depths, n_bins * 60.0, "offset-alias", "probe01",
        list(range(5))
    )
    offset_gate = bd.apply_gate(offset_obs, offset_null, 20.0)
    check("off-grid ten-minute segment can span 30 um while gate passes at 15/0",
          offset_gate["passed"] and offset_obs["delta_window"] == 15.0
          and offset_null["q95"] == 0.0)

    # Draft 22's three size points are not a fixed moving fraction, and the
    # directional pattern is not monotonic even when the fraction really is
    # fixed.  This is a prose/fixture overclaim, separate from the verdict bug.
    stated_fractions = (5 / 11.0, 10 / 21.0, 20 / 41.0)
    check("the document's 11/21/41 masking series is not a fixed fraction",
          len(set(stated_fractions)) == 3,
          "fractions %.4f, %.4f, %.4f" % stated_fractions)

    def masking_value(total, moving, seed):
        """Return Delta_10 for one fixed-fraction masking construction."""
        grid = np.concatenate([
            b * 60.0 + np.linspace(1.0, 50.0, 12) for b in range(61)
        ])
        index = np.floor(grid / 60.0).astype(int)
        ramp = np.clip((index - 45) / 9.0, 0.0, 1.0)
        values = []
        for u in range(total):
            rng_u = np.random.default_rng(seed + u)
            row = 1000.0 + 40.0 * u + rng_u.normal(0.0, 20.0, size=grid.size)
            if u < moving:
                row = row + 30.0 * ramp
            values.append(row)
        return bd.measure_band_drift(
            [grid.copy() for _ in range(total)], values, 61 * 60.0
        )["delta_window"]

    fixed_fraction = [masking_value(n, int(0.4 * n), 7013) for n in (10, 20, 40)]
    check("a fixed-fraction admitted fixture reverses the claimed monotonic direction",
          fixed_fraction[1] > fixed_fraction[0],
          "Delta_10 %.3f, %.3f, %.3f at 10, 20, 40 units"
          % tuple(fixed_fraction))

    print("%d independent probe failures" % len(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
