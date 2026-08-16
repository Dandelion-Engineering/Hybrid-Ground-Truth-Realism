"""Show why finite-sample support alone cannot absorb missing spike depths.

The proposed disposition for non-finite depths drops those samples and relies
on the existing per-unit and per-bin support floors.  This probe constructs one
observed record that passes those floors after dropping its missing samples,
then supplies two different finite completions of the same missing entries.
The complete-case drift is zero while an admissible completion carries drift
well above the strict host gate.  The construction exercises the packet's
actual ``measure_band_drift`` implementation.

Example
-------
Run from the project root with the project virtual environment::

    ./venv/Scripts/python.exe agents/Codex/tools/probe_nonfinite_depth_disposition.py \
        --repo-root .
"""

import argparse
import importlib.util
import os

import numpy as np


def parse_args(argv=None):
    """Parse the project root and construction size."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True,
                        help="project root containing Reproducibility Packet")
    parser.add_argument("--finite-per-bin", type=int, default=1000,
                        help="even count of observed finite depths per unit/bin")
    parser.add_argument("--threshold-um", type=float, default=20.0,
                        help="existing strict drift threshold used for the check")
    return parser.parse_args(argv)


def load_band_drift(repo_root):
    """Load the reviewed packet drift module without changing its source."""
    path = os.path.join(os.path.abspath(repo_root), "Reproducibility Packet",
                        "scripts", "utils", "band_drift.py")
    spec = importlib.util.spec_from_file_location("band_drift_disposition_probe", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_unit(finite_per_bin, completion):
    """Return one unit's times and depths for complete-case or completed data."""
    times = []
    depths = []
    half = finite_per_bin // 2
    for bin_index in range(12):
        finite_times = bin_index * 60.0 + np.linspace(
            0.01, 59.98, finite_per_bin, dtype=np.float64)
        times.extend(finite_times.tolist())
        depths.extend(([0.0] * half) + ([100.0] * half))
        if completion is not None:
            times.append(bin_index * 60.0 + 59.99)
            depths.append(float(completion(bin_index)))
    return np.asarray(times, dtype=np.float64), np.asarray(depths, dtype=np.float64)


def measure(module, finite_per_bin, completion):
    """Measure five identical units through the packet's reviewed estimator."""
    units = [make_unit(finite_per_bin, completion) for _ in range(5)]
    return module.measure_band_drift(
        [item[0] for item in units],
        [item[1] for item in units],
        extent_s=720.0,
    )


def main(argv=None):
    """Run the support-passing missing-depth counterexample."""
    args = parse_args(argv)
    if args.finite_per_bin < 10 or args.finite_per_bin % 2:
        raise SystemExit("[fatal] --finite-per-bin must be even and at least 10")
    module = load_band_drift(args.repo_root)

    complete_case = measure(module, args.finite_per_bin, completion=None)
    no_drift_completion = measure(module, args.finite_per_bin,
                                  completion=lambda _bin: -1.0)
    drift_completion = measure(
        module,
        args.finite_per_bin,
        completion=lambda bin_index: -1.0 if bin_index < 6 else 101.0,
    )

    missing_fraction = 1.0 / (args.finite_per_bin + 1.0)
    checks = {
        "complete_case_measurable": bool(complete_case["measurable"]),
        "no_drift_completion_measurable": bool(no_drift_completion["measurable"]),
        "drift_completion_measurable": bool(drift_completion["measurable"]),
        "complete_case_passes_strict": (
            complete_case["delta_window"] <= args.threshold_um),
        "drift_completion_fails_strict": (
            drift_completion["delta_window"] > args.threshold_um),
        "same_observed_finite_record_opposite_verdicts": (
            complete_case["delta_window"] <= args.threshold_um
            and drift_completion["delta_window"] > args.threshold_um),
    }

    print("Non-finite-depth disposition counterexample")
    print("finite depths per unit/bin: %d" % args.finite_per_bin)
    print("missing depths per unit/bin: 1")
    print("missing fraction: %.8f%%" % (100.0 * missing_fraction))
    print("included units after dropping: %d" % len(complete_case["included"]))
    print("complete-case Delta_10min: %.6f um" % complete_case["delta_window"])
    print("no-drift completion Delta_10min: %.6f um"
          % no_drift_completion["delta_window"])
    print("drift completion Delta_10min: %.6f um" % drift_completion["delta_window"])
    print("existing strict threshold: %.6f um" % args.threshold_um)
    for name, passed in checks.items():
        print("%s: %s" % (name, "PASS" if passed else "FAIL"))
    failures = [name for name, passed in checks.items() if not passed]
    print("checks: %d passed, %d failed" % (len(checks) - len(failures), len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
