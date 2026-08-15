"""Construct counterexamples to Draft 16's two one-way safety claims.

The probe does not predict any candidate recording. It shows only that the
approved drift estimator does not mathematically guarantee either of these
claims:

1. adding label-blind units cannot turn a drift failure into a pass; and
2. retaining a first grid bin can only move ``Delta_10min`` toward rejection.

Both fixtures use synthetic arrays with known structure and the packet's exact
numeric implementation. They keep the review decision tied to executable
evidence without reading any candidate asset.
"""

import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np


def load_band_drift(repo_root):
    """Load the packet's band-drift module from ``repo_root``.

    Args:
        repo_root: project root containing ``Reproducibility Packet``.

    Returns:
        module: the loaded ``band_drift`` module.
    """
    path = repo_root / "Reproducibility Packet" / "scripts" / "utils" / "band_drift.py"
    spec = importlib.util.spec_from_file_location("band_drift_review_probe", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load %s" % path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def binned_times(n_bins, spikes_per_bin):
    """Return one ascending time array with equal counts in each 60 s bin.

    Args:
        n_bins: number of bins.
        spikes_per_bin: spikes placed inside each bin.

    Returns:
        numpy.ndarray: ascending synthetic spike times in seconds.
    """
    return np.concatenate(
        [b * 60.0 + np.linspace(1.0, 50.0, spikes_per_bin) for b in range(n_bins)]
    )


def label_set_counterexample(module, threshold_um):
    """Show that added flat unit traces can change a failure into a pass.

    Args:
        module: loaded band-drift implementation.
        threshold_um: gate threshold in micrometres.

    Returns:
        dict: observed/null values and gate decisions for both unit sets.
    """
    n_bins = 12
    spikes_per_bin = 10
    times = binned_times(n_bins, spikes_per_bin)
    ramp = np.repeat(np.linspace(0.0, 30.0, n_bins), spikes_per_bin)
    flat = np.zeros(n_bins * spikes_per_bin, dtype=np.float64)

    moving_times = [times.copy() for _ in range(5)]
    moving_depths = [ramp.copy() for _ in range(5)]
    all_times = moving_times + [times.copy() for _ in range(6)]
    all_depths = moving_depths + [flat.copy() for _ in range(6)]

    def evaluate(unit_times, unit_depths, label):
        observed = module.measure_band_drift(unit_times, unit_depths, n_bins * 60.0)
        null = module.permutation_null(
            unit_times,
            unit_depths,
            n_bins * 60.0,
            "draft16-label-fixture",
            "Probe00",
            list(range(len(unit_times))),
        )
        gate = module.apply_gate(observed, null, threshold_um)
        return {
            "label": label,
            "delta_10min_um": observed["delta_window"],
            "q95_null_um": null["q95"],
            "passed": gate["passed"],
            "gate_label": gate["label"],
        }

    moving = evaluate(moving_times, moving_depths, "five_moving_units")
    expanded = evaluate(all_times, all_depths, "five_moving_plus_six_flat_units")
    if moving["passed"] or not expanded["passed"]:
        raise AssertionError("label-set counterexample no longer demonstrates the claimed reversal")
    return {"moving_only": moving, "label_blind_expansion": expanded}


def head_bin_counterexample(module):
    """Show that retaining an extra first bin can lower observed ``Delta_10min``.

    Args:
        module: loaded band-drift implementation.

    Returns:
        dict: the deterministic trial and both observed excursions.
    """
    rng = np.random.default_rng(20260814)
    spikes_per_bin = 10
    times = binned_times(12, spikes_per_bin)
    for trial in range(2000):
        medians = rng.normal(0.0, 15.0, size=(6, 12)).cumsum(axis=1) / 3.0
        full_times = [times.copy() for _ in range(6)]
        full_depths = [np.repeat(medians[u], spikes_per_bin) for u in range(6)]
        retained = module.measure_band_drift(full_times, full_depths, 12 * 60.0)

        tail_times = [unit_times[spikes_per_bin:] - 60.0 for unit_times in full_times]
        tail_depths = [unit_depths[spikes_per_bin:] for unit_depths in full_depths]
        omitted = module.measure_band_drift(tail_times, tail_depths, 11 * 60.0)
        if retained["delta_window"] < omitted["delta_window"]:
            return {
                "trial": trial,
                "retained_head_delta_10min_um": retained["delta_window"],
                "without_head_delta_10min_um": omitted["delta_window"],
            }
    raise AssertionError("no deterministic head-bin counterexample found")


def parse_args():
    """Parse the project root and review threshold.

    Returns:
        argparse.Namespace: parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parents[3]
    parser.add_argument("--repo-root", type=Path, default=default_root)
    parser.add_argument("--threshold-um", type=float, default=20.0)
    return parser.parse_args()


def main():
    """Run both deterministic probes and print a JSON report."""
    args = parse_args()
    module = load_band_drift(args.repo_root.resolve())
    report = {
        "label_set": label_set_counterexample(module, args.threshold_um),
        "head_bin": head_bin_counterexample(module),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
