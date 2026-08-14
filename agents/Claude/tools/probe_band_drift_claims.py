"""Session 19 owner re-review probes for the band-drift estimator.

Three independent checks, none of which reads a candidate recording:

1. Reproduce the partial-bin contamination defect Codex reported, by restoring
   the pre-repair full-array permutation on a copy of the shipped module and
   showing that changing only discarded-tail depths moves ``Q95_null``.
2. Confirm the repaired pool is exactly the set of spikes whose times fall in
   complete bins, on randomized fixtures rather than one hand-built case.
3. Confirm no null value can change the rejection when observed ``Delta_10``
   exceeds the gate -- the observable bound the reviewed draft claims.
"""
import argparse
import importlib.util
import os
import sys

import numpy as np


def load_module(path):
    """Import band_drift.py from an explicit path.

    Args:
        path: filesystem path to the module.

    Returns:
        module: the imported module object.
    """
    spec = importlib.util.spec_from_file_location("band_drift_probe", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_band(rng, n_units, duration_s, bin_seconds, rate_hz, depth_um, drift_um=0.0):
    """Build a synthetic band of per-unit spike times and depths.

    Args:
        rng: a numpy Generator.
        n_units: number of units in the band.
        duration_s: total span the spikes cover, in seconds.
        bin_seconds: bin width, used only to report the tail.
        rate_hz: per-unit firing rate.
        depth_um: per-unit base depth.
        drift_um: total linear ramp applied across the recording.

    Returns:
        tuple: ``(spike_times, depths)``, both lists of arrays.
    """
    times, depths = [], []
    for u in range(n_units):
        n = int(rate_hz * duration_s)
        t = np.sort(rng.uniform(0.0, duration_s, size=n))
        d = depth_um + 40.0 * u + rng.normal(0.0, 3.0, size=n) + drift_um * (t / duration_s)
        times.append(t)
        depths.append(d)
    return times, depths


def probe_partial_bin_defect(bd, rng):
    """Show the pre-repair permutation let discarded depths reach the null."""
    duration_s = 1830.0  # 30 complete 60 s bins plus a 30 s tail
    times, depths = make_band(rng, 8, duration_s, 60.0, 4.0, 3000.0)
    contaminated = [d.copy() for d in depths]
    n_changed = 0
    for t, d in zip(times, contaminated):
        tail = t >= 1800.0
        d[tail] += 9000.0
        n_changed += int(tail.sum())

    def null_q95(dep, patched):
        original = bd.permutation_null
        if patched:
            def full_pool(spike_times, dps, dur, asset, probe, rows, params=None):
                p = dict(bd.PARAMS)
                if params:
                    p.update(params)
                n_bins, _ = bd.complete_bins(dur, p["bin_seconds"])
                offsets, medians = bd._unit_tables(
                    spike_times, dps, n_bins, p["bin_seconds"], p["min_spikes_per_bin"])
                defined = np.array([np.isfinite(m).sum() for m in medians], dtype=np.float64)
                included = defined >= p["min_bin_fraction"] * n_bins
                pools = [np.asarray(x, dtype=np.float64) for x in dps]
                values = np.empty(p["n_permutations"], dtype=np.float64)
                for k in range(p["n_permutations"]):
                    replicate = []
                    for u in range(len(spike_times)):
                        if not included[u]:
                            replicate.append(medians[u])
                            continue
                        seed = bd.derive_permutation_seed(asset, probe, rows[u], k,
                                                          p["master_seed"])
                        gen = np.random.Generator(np.random.PCG64(seed))
                        shuffled = pools[u][gen.permutation(pools[u].size)]
                        replicate.append(bd.bin_medians(shuffled, offsets[u],
                                                        p["min_spikes_per_bin"]))
                    trace, _, invalid = bd._trace_from_medians(
                        replicate, included, p["min_units_per_bin"])
                    values[k] = bd.excursions(trace, p["window_bins"])[1]
                values.sort()
                rank = int(np.ceil(0.95 * p["n_permutations"]))
                return {"values": values.tolist(), "q95": float(values[rank - 1])}
            fn = full_pool
        else:
            fn = original
        return fn(times, dep, duration_s, "asset-x", "Probe00",
                  list(range(len(times))))["q95"]

    pre_clean = null_q95(depths, True)
    pre_dirty = null_q95(contaminated, True)
    post_clean = null_q95(depths, False)
    post_dirty = null_q95(contaminated, False)
    obs_clean = bd.measure_band_drift(times, depths, duration_s)["delta_window"]
    obs_dirty = bd.measure_band_drift(times, contaminated, duration_s)["delta_window"]
    print("partial-bin contamination (%d tail depths moved by 9000 um)" % n_changed)
    print("  observed Delta_10   clean %.4f um   contaminated %.4f um   (identical: %s)"
          % (obs_clean, obs_dirty, obs_clean == obs_dirty))
    print("  pre-repair  Q95_null clean %.4f um   contaminated %.4f um   (defect: %s)"
          % (pre_clean, pre_dirty, pre_clean != pre_dirty))
    print("  as shipped  Q95_null clean %.4f um   contaminated %.4f um   (repaired: %s)"
          % (post_clean, post_dirty, post_clean == post_dirty))
    return pre_clean != pre_dirty and post_clean == post_dirty and obs_clean == obs_dirty


def probe_pool_identity(bd, rng):
    """Confirm [offsets[0], offsets[-1]) is exactly the complete-bin index set."""
    ok = True
    for trial in range(200):
        duration_s = float(rng.uniform(200.0, 4000.0))
        n_bins, _ = bd.complete_bins(duration_s, 60.0)
        n = int(rng.integers(50, 400))
        t = np.sort(rng.uniform(-2.0, duration_s + 5.0, size=n))
        off = bd.bin_offsets(t, n_bins, 60.0)
        sliced = set(range(int(off[0]), int(off[-1])))
        expected = set(np.flatnonzero((t >= 0.0) & (t < n_bins * 60.0)).tolist())
        if sliced != expected:
            ok = False
            print("  MISMATCH at trial %d: duration %.3f" % (trial, duration_s))
            break
    print("complete-bin slice equals the complete-bin index set over 200 randomized "
          "fixtures: %s" % ok)
    return ok


def probe_pass_bound(bd):
    """Confirm no null value lets a candidate with Delta_10 > L pass."""
    observed = {"measurable": True, "delta_window": 25.0}
    passes = []
    for q95 in [0.0, 1.0, 10.0, 19.999, 20.0, 25.0, 1e6]:
        verdict = bd.apply_gate(observed, {"q95": q95}, 20.0)
        passes.append(verdict["passed"])
    print("candidate with observed Delta_10 25 um (L 20 um) passes for any q95 in "
          "{0, 1, 10, 19.999, 20, 25, 1e6}: %s" % any(passes))
    quiet = {"measurable": True, "delta_window": 5.0}
    tight = bd.apply_gate(quiet, {"q95": 3.0}, 20.0)["passed"]
    wide = bd.apply_gate(quiet, {"q95": 30.0}, 20.0)["passed"]
    print("quiet candidate (Delta_10 5 um) passes with a tight null: %s; with a wide "
          "null: %s" % (tight, wide))
    return (not any(passes)) and tight and not wide


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True, help="path to band_drift.py")
    parser.add_argument("--seed", type=int, default=19, help="fixture seed")
    args = parser.parse_args()
    if not os.path.exists(args.module):
        sys.exit("module not found: %s" % args.module)
    bd = load_module(args.module)
    rng = np.random.default_rng(args.seed)
    results = [
        probe_partial_bin_defect(bd, rng),
        probe_pool_identity(bd, rng),
        probe_pass_bound(bd),
    ]
    print("\n%d of %d probes passed" % (sum(results), len(results)))
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
