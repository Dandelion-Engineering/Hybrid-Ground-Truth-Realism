"""How much missingness it takes before the drift gate stops being decided.

The missing-depth sensitivity bound in
``Reproducibility Packet/scripts/utils/missing_depth.py`` can only be judged
against a sense of scale: a bound that pauses every candidate is as useless as
no bound, and one that pauses none is decorative. This probe sweeps the
missing-depth count on one synthetic band and prints where the bound crosses
the strict 20 um tolerance while the approved two-number gate still passes the
observed record.

**The crossover it prints is a property of this fixture and is not a rule.**
It is not a threshold, it is not proposed as one, and no code reads it. The
disposition rule is the pre-declared tolerance ``L`` applied to the bound, with
no fitted percentage anywhere. This exists so that a reader -- and the agent
reading a real candidate's exclusion count -- knows whether a measured
missingness is in the regime where the question can bite at all, for a band
with this many units and this much depth spread. A narrower depth spread, fewer
units or fewer spikes per bin all move it.

The band is built so the null stays narrow on purpose: depths are drawn
uniformly across the spread in every bin, so no bin median is knife-edge. The
band trace is a median across units, so independent per-unit resampling noise
shrinks with the unit count, while a block of missing depths shifts every
unit's median in the same direction at once and does not shrink. That asymmetry
is the whole reason a gate-passing counterexample exists.

**One thing this fixture is not.** Every unit is affected in every bin here,
which is the worst case for that asymmetry and is not what the two real
candidates carry: on those, 11 of 140 and 10 of 182 included units hold any
missing depth at all, and the across-unit median is taken over the rest. So the
percentage printed below must not be compared against a real candidate's
whole-band missing fraction as though the two meant the same thing. Whether a
real candidate is decision-stable is settled by running the bound on it, not by
reading this table.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Claude/tools/probe_missing_depth_crossover.py" \\
        --repo-root .
"""

import argparse
import os
import sys

import numpy as np


def parse_args(argv=None):
    """Parse the project root and the fixture's shape.

    Args:
        argv: argument list; defaults to the process arguments.

    Returns:
        argparse.Namespace: the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="project root holding the Reproducibility Packet")
    parser.add_argument("--units", type=int, default=15,
                        help="units in the synthetic band")
    parser.add_argument("--bins", type=int, default=12,
                        help="complete 60 s bins in the recording")
    parser.add_argument("--per-bin", type=int, default=200,
                        help="observed depths per unit and bin")
    parser.add_argument("--width-um", type=float, default=300.0,
                        help="width of the uniform depth spread in micrometres")
    parser.add_argument("--permutations", type=int, default=40,
                        help="null replicates per sweep point")
    parser.add_argument("--missing", type=int, nargs="+",
                        default=[0, 1, 2, 3, 5, 10, 20, 40],
                        help="missing depths per unit and bin to sweep")
    parser.add_argument("--threshold-um", type=float, default=20.0,
                        help="the strict tolerance the sweep is read against")
    parser.add_argument("--seed", type=int, default=11,
                        help="fixture seed for the synthetic depths")
    return parser.parse_args(argv)


def build_band(n_units, n_bins, per_bin, missing_per_bin, width_um, seed):
    """Build one synthetic band with a uniform within-bin depth spread.

    Args:
        n_units: units in the band.
        n_bins: complete bins in the recording.
        per_bin: observed depths per unit and bin.
        missing_per_bin: missing depths per unit and bin.
        width_um: width of the uniform depth spread in micrometres.
        seed: fixture seed.

    Returns:
        tuple: ``(times, depths, missing_times, rows, extent_s)``.
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


def main(argv=None):
    """Run the sweep and print one row per missing-depth count."""
    args = parse_args(argv)
    sys.path.insert(0, os.path.join(os.path.abspath(args.repo_root),
                                    "Reproducibility Packet", "scripts"))
    from utils import band_drift as bd
    from utils import missing_depth as md

    params = {"n_permutations": args.permutations}
    print("missing-depth crossover sweep")
    print("band: %d units, %d bins, %d observed depths per unit and bin, "
          "%.1f um uniform spread" % (args.units, args.bins, args.per_bin,
                                      args.width_um))
    print("null: %d replicates per point; tolerance %.1f um"
          % (args.permutations, args.threshold_um))
    print("every unit is affected in every bin here, which is the worst case for")
    print("the across-unit median and is not what a real candidate carries")
    print("the crossover below is a property of this fixture and is not a rule")
    print("")
    header = ("%6s %8s %10s %10s %10s %10s %10s  %-18s %s"
              % ("k/bin", "missing%", "delta", "delta_lo", "delta_hi", "q95_fin",
                 "q95_hi", "disposition", "approved gate"))
    print(header)
    print("-" * len(header))

    first_unstable = None
    last_stable = None
    for missing_per_bin in args.missing:
        times, depths, missing, rows, extent = build_band(
            args.units, args.bins, args.per_bin, missing_per_bin,
            args.width_um, args.seed)
        # The module takes the complete record with NaN at the missing depths,
        # so the missing samples' positions are input rather than reconstruction.
        masked_t, masked_d = [], []
        for unit_times, unit_depths, unit_missing in zip(times, depths, missing):
            merged_t = np.concatenate([unit_times, unit_missing])
            merged_d = np.concatenate([
                unit_depths,
                np.full(unit_missing.size, np.nan, dtype=np.float64),
            ])
            order = np.argsort(merged_t, kind="stable")
            masked_t.append(merged_t[order])
            masked_d.append(merged_d[order])
        result = md.measure_missing_depth_sensitivity(masked_t, masked_d, extent)
        if not result["measurable"]:
            print("%6d %8s  %s" % (missing_per_bin, "-", result["reason"][:70]))
            continue
        bounded = md.null_interval(masked_t, masked_d, extent, "asset",
                                   "Probe00", rows, params)
        verdict = md.stability_verdict(result, bounded, args.threshold_um)
        # The approved gate reads the finite-only null, which is the number the
        # command reports; the bound above is over the completed-record null.
        approved_null = bd.permutation_null(times, depths, extent, "asset",
                                            "Probe00", rows, params)
        gate = bd.apply_gate(result["observed"], approved_null,
                             args.threshold_um)
        fraction = 100.0 * missing_per_bin / float(args.per_bin + missing_per_bin)
        print("%6d %8.3f %10.3f %10.3f %10.3f %10.3f %10.3f  %-18s %s"
              % (missing_per_bin, fraction, result["observed"]["delta_window"],
                 result["delta_window_lo"], result["delta_window_hi"],
                 approved_null["q95"], bounded["q95_hi"], verdict["disposition"],
                 "pass" if gate["passed"] else gate["label"]))
        if verdict["disposition"] == "passes":
            last_stable = (missing_per_bin, fraction)
        elif first_unstable is None and verdict["disposition"] != "passes":
            first_unstable = (missing_per_bin, fraction)

    print("")
    if last_stable and first_unstable:
        print("crossover between %.3f%% and %.3f%% missing on this fixture "
              "(%d and %d per unit/bin)"
              % (last_stable[1], first_unstable[1], last_stable[0],
                 first_unstable[0]))
    else:
        print("no crossover inside the swept range")
    print("read it as scale, not as a threshold: no code consumes this number")
    return 0


if __name__ == "__main__":
    sys.exit(main())
