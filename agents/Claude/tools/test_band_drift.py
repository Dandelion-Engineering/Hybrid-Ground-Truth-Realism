"""Exhaustive synthetic tests for the band-drift estimator and its gate.

The estimator in ``Reproducibility Packet/scripts/utils/band_drift.py`` decides
which host recordings are admissible, so it is tested before it is ever pointed
at a candidate. Every input here is synthetic and constructed so the right
answer is known in advance: a ramp of a stated size, a trajectory that returns
to where it started, a trace whose worst window is deliberately not its first,
a band deliberately one unit short in one bin.

Four of the cases exist because of specific defects the specification passed
through in review, and they are the ones most worth keeping:

* ``quiet_host_passes`` -- an earlier draft rejected a candidate whose observed
  value lay inside its own null, which inverted the cleanest possible outcome.
  A quiet host must pass and must be labelled as unresolved rather than
  rejected.
* ``down_and_back`` -- the reported quantity is a peak-to-peak excursion, not
  endpoint-to-endpoint net motion, so a probe that moves and returns must not
  score zero.
* ``invalid_bin_rejects`` -- an invalid bin rejects the candidate rather than
  being omitted from a window, because omitting it could hide that window's
  maximum. The rejection must name the offending bins.
* ``per_unit_audit_values`` -- an earlier draft claimed that adding units to the
  label-blind set could not turn a failure into a pass. It can: a majority of
  movement-insensitive traces holds the across-unit median flat. The case keeps
  that counterexample and checks that the reported per-unit excursions still
  show the movement the band statistic does not.
* ``per_unit_audit_has_no_null`` -- those reported per-unit values arrived with
  no rule for reading them, and the two obvious readings are both wrong. A
  no-movement fixture shows every per-unit excursion above the band's own null,
  and a genuine common ramp shows the per-unit worst windows scattering exactly
  as noise does.

The permutation determinism cases check the property the specification actually
depends on: the same inputs replay the same null, and different assets, probes,
units or replicates do not share a stream.

This harness lives in the agent workspace rather than in the packet because it
tests a module against inputs a reader cannot download; the packet's own
runbook step arrives with the archive-reading script.

Example
-------
Run from the project root with the project virtual environment:

    ./venv/Scripts/python.exe "agents/Claude/tools/test_band_drift.py"
"""

import argparse
import hashlib
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))),
    "Reproducibility Packet", "scripts"))

from utils import band_drift as bd  # noqa: E402

#: Seed for building the synthetic recordings themselves. It has nothing to do
#: with the estimator's pinned master seed and is not a project parameter.
FIXTURE_SEED = 20260813

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
    print("  %-46s %s%s" % (name, "ok" if condition else "FAIL",
                            ("  " + detail) if detail else ""))
    return bool(condition)


def make_band(n_units=12, duration_s=3660.0, rate_hz=6.0, depth_noise_um=18.0,
              trajectory=None, seed=FIXTURE_SEED, spans=None):
    """Build a synthetic band of units with a known depth trajectory.

    Args:
        n_units: number of units in the band.
        duration_s: recording duration in seconds.
        rate_hz: mean firing rate per unit, homogeneous Poisson.
        depth_noise_um: per-spike depth estimation noise, Gaussian.
        trajectory: callable mapping time in seconds to band displacement in
            micrometres; a flat band when None.
        seed: fixture seed for the synthetic data.
        spans: optional list of ``(start_s, end_s)`` per unit, so a unit can be
            made to cover only part of the recording.

    Returns:
        tuple: ``(spike_times, depths, row_indices)`` ready for the estimator.
    """
    rng = np.random.default_rng(seed)
    if trajectory is None:
        trajectory = lambda t: np.zeros_like(t)  # noqa: E731
    spike_times, depths = [], []
    for u in range(n_units):
        start, end = spans[u] if spans else (0.0, duration_s)
        n = rng.poisson(rate_hz * (end - start))
        times = np.sort(rng.uniform(start, end, size=n))
        base = 1000.0 + 40.0 * u
        depths.append(base + trajectory(times) + rng.normal(0.0, depth_noise_um, size=n))
        spike_times.append(times)
    return spike_times, depths, list(range(n_units))


def case_seed_derivations():
    """The two derived constants must reproduce from their stated inputs."""
    print("seed derivations")
    check("master seed derives from its source string",
          bd.derive_master_seed() == 3175830281,
          "%d" % bd.derive_master_seed())
    check("PARAMS carries that master seed",
          bd.PARAMS["master_seed"] == bd.derive_master_seed())

    asset, probe, row, k = "0a1b2c3d-4e5f-6071-8293-a4b5c6d7e8f9", "probe01", 37, 5
    payload = "3175830281\n%s\n%s\n%d\n%d" % (asset, probe, row, k)
    expect = int(hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16], 16)
    check("permutation seed matches the literal specified string",
          bd.derive_permutation_seed(asset, probe, row, k) == expect)
    check("seed fits in 64 bits", expect < 2 ** 64, "%d" % expect)

    seeds = {bd.derive_permutation_seed(a, p, r, i)
             for a in (asset, "other-asset") for p in (probe, "probe00")
             for r in (row, row + 1) for i in (k, k + 1)}
    check("all five fields separate the stream", len(seeds) == 16, "%d distinct" % len(seeds))


def case_binning():
    """Complete bins, the discarded remainder, and slice boundaries."""
    print("binning")
    n_bins, discarded = bd.complete_bins(3690.818)
    check("61 complete 60 s bins in a 3690.818 s recording", n_bins == 61)
    check("the partial bin's duration is reported", abs(discarded - 30.818) < 1e-9,
          "%.3f s" % discarded)
    try:
        bd.complete_bins(45.0)
        check("a sub-bin recording raises", False)
    except ValueError:
        check("a sub-bin recording raises", True)

    times = np.array([0.0, 59.999, 60.0, 119.0, 180.5, 240.0])
    off = bd.bin_offsets(times, 3)
    check("bin offsets partition on the bin edges", off.tolist() == [0, 2, 4, 4],
          str(off.tolist()))
    check("an empty middle bin is empty rather than absent",
          off[2] == off[3] == 4)
    check("the two spikes past the last complete bin fall outside every slice",
          off[-1] == 4 and times.size == 6)
    try:
        bd.bin_offsets(np.array([5.0, 1.0]), 1)
        check("unsorted times raise", False)
    except ValueError:
        check("unsorted times raise", True)


def case_known_ramp():
    """A linear ramp of a stated size must be recovered at both scales."""
    print("known ramp")
    ramp_um, duration = 60.0, 3660.0
    times, depths, rows = make_band(
        n_units=12, duration_s=duration, rate_hz=8.0, depth_noise_um=12.0,
        trajectory=lambda t: ramp_um * t / duration)
    obs = bd.measure_band_drift(times, depths, duration)
    if not check("measurable", obs["measurable"], obs.get("reason", "")):
        return
    n_bins = obs["n_bins"]
    expect_full = ramp_um * (n_bins - 1) / n_bins
    expect_win = ramp_um * 9.0 / n_bins
    check("Delta_full recovers the ramp",
          abs(obs["delta_full"] - expect_full) < 3.0,
          "%.2f um, expected about %.2f" % (obs["delta_full"], expect_full))
    check("Delta_10 recovers the in-window fraction",
          abs(obs["delta_window"] - expect_win) < 2.0,
          "%.2f um, expected about %.2f" % (obs["delta_window"], expect_win))
    check("all units included", len(obs["included"]) == 12)
    check("no invalid bins", obs["invalid_bins"] == [])


def case_down_and_back():
    """A trajectory that returns must report its excursion, not zero."""
    print("down and back")
    amp, duration = 45.0, 3660.0
    times, depths, rows = make_band(
        n_units=12, duration_s=duration, rate_hz=8.0, depth_noise_um=10.0,
        trajectory=lambda t: amp * np.sin(np.pi * t / duration), seed=FIXTURE_SEED + 1)
    obs = bd.measure_band_drift(times, depths, duration)
    if not check("measurable", obs["measurable"], obs.get("reason", "")):
        return
    check("net endpoint motion is about zero",
          abs(obs["trace"][0] - obs["trace"][-1]) < 8.0,
          "%.2f um" % abs(obs["trace"][0] - obs["trace"][-1]))
    check("Delta_full reports the excursion instead",
          abs(obs["delta_full"] - amp) < 6.0,
          "%.2f um, excursion was %.1f" % (obs["delta_full"], amp))


def case_worst_window():
    """The gate takes the worst window, not the first or a chosen one."""
    print("worst window")
    trace = np.zeros(40)
    trace[5:8] = 3.0          # a small early step
    trace[30:33] = 25.0       # the real one, late
    delta_full, delta_win, start = bd.excursions(trace)
    check("Delta_full spans the largest step", abs(delta_full - 25.0) < 1e-9)
    check("Delta_10 finds the late window", abs(delta_win - 25.0) < 1e-9)
    check("the window reported contains the late step", 21 <= start <= 32, "start=%d" % start)
    short = np.zeros(6)
    _, win, st = bd.excursions(short)
    check("a trace shorter than the window returns no window", win is None and st is None)
    try:
        bd.excursions(np.array([0.0, np.nan, 1.0]))
        check("a NaN in the trace raises rather than being skipped", False)
    except ValueError:
        check("a NaN in the trace raises rather than being skipped", True)


def case_unit_inclusion():
    """A unit that does not span the recording is excluded, not weighted down."""
    print("unit inclusion")
    duration = 3660.0
    spans = [(0.0, duration)] * 10 + [(0.0, 0.6 * duration), (0.5 * duration, duration)]
    times, depths, rows = make_band(
        n_units=12, duration_s=duration, rate_hz=8.0, depth_noise_um=12.0,
        spans=spans, seed=FIXTURE_SEED + 2)
    obs = bd.measure_band_drift(times, depths, duration)
    check("the two part-time units are excluded",
          obs["included"] == list(range(10)), str(obs["included"]))
    check("the rest still measure", obs["measurable"], obs.get("reason", ""))


def case_invalid_bin_rejects():
    """An invalid bin rejects the candidate and the reason names the bins."""
    print("invalid bin")
    duration = 3660.0
    times, depths, rows = make_band(
        n_units=6, duration_s=duration, rate_hz=8.0, depth_noise_um=12.0,
        seed=FIXTURE_SEED + 3)
    # Silence two units inside bin 20 only, leaving four valid units there and
    # keeping every unit above the 80%-of-bins inclusion floor.
    for u in (0, 1):
        keep = (times[u] < 1200.0) | (times[u] >= 1260.0)
        times[u], depths[u] = times[u][keep], depths[u][keep]
    obs = bd.measure_band_drift(times, depths, duration)
    check("six units are all still included", len(obs["included"]) == 6, str(obs["included"]))
    check("the candidate is unmeasurable", obs["measurable"] is False)
    check("bin 20 is named", obs["invalid_bins"] == [20], str(obs.get("invalid_bins")))
    check("the reason names the offending bin and its unit count",
          "bins [20]" in obs["reason"] and "[4]" in obs["reason"], obs["reason"][:70] + "...")
    gate = bd.apply_gate(obs, None, 20.0)
    check("the gate reports it as unmeasurable, not as a pass",
          gate["passed"] is False and gate["label"] == "unmeasurable")


def case_too_few_units():
    """Too few spanning units is an unmeasurable rejection with a count."""
    print("too few units")
    duration = 3660.0
    times, depths, rows = make_band(
        n_units=4, duration_s=duration, rate_hz=8.0, seed=FIXTURE_SEED + 4)
    obs = bd.measure_band_drift(times, depths, duration)
    check("four units cannot make a five-unit bin", obs["measurable"] is False)
    check("the reason counts them", "only 4 of 4" in obs["reason"], obs["reason"][:60] + "...")


def case_malformed_input_raises():
    """Malformed input is a bug and must be loud, not an unmeasurable verdict."""
    print("malformed input")
    duration = 600.0
    times, depths, rows = make_band(n_units=6, duration_s=duration, seed=FIXTURE_SEED + 5)
    depths[2][17] = np.nan
    try:
        bd.measure_band_drift(times, depths, duration)
        check("a non-finite depth raises", False)
    except ValueError as exc:
        check("a non-finite depth raises", "non-finite" in str(exc))
    times2, depths2, _ = make_band(n_units=6, duration_s=duration, seed=FIXTURE_SEED + 6)
    depths2[1] = depths2[1][:-3]
    try:
        bd.measure_band_drift(times2, depths2, duration)
        check("mismatched array lengths raise", False)
    except ValueError as exc:
        check("mismatched array lengths raise", "spike times" in str(exc))
    times3, depths3, _ = make_band(n_units=6, duration_s=duration, seed=FIXTURE_SEED + 9)
    try:
        bd.measure_band_drift(times3, depths3[:-1], duration)
        check("mismatched unit-array counts raise", False)
    except ValueError as exc:
        check("mismatched unit-array counts raise", "unit spike-time arrays" in str(exc))
    try:
        bd.permutation_null(times3, depths3, duration, "asset", "probe",
                            [0, 1, 2, 3, 4, 4], {"n_permutations": 1})
        check("duplicate unit row indices raise", False)
    except ValueError as exc:
        check("duplicate unit row indices raise", "distinct" in str(exc))


def case_partial_bin_is_discarded_from_null(n_permutations):
    """Depths in the discarded final partial bin cannot change the null."""
    print("partial bin exclusion")
    duration = 605.0
    times, ordinary, extreme = [], [], []
    for u in range(6):
        complete = np.concatenate([
            np.linspace(b * 60.0 + 1.0, b * 60.0 + 59.0, 10)
            for b in range(10)
        ])
        partial = np.linspace(600.05, 604.95, 50)
        times.append(np.concatenate([complete, partial]))
        baseline = np.full(150, 1000.0 + 20.0 * u)
        altered = baseline.copy()
        altered[100:] = 10000.0 + 20.0 * u
        ordinary.append(baseline)
        extreme.append(altered)

    params = {"n_permutations": n_permutations}
    obs_a = bd.measure_band_drift(times, ordinary, duration)
    obs_b = bd.measure_band_drift(times, extreme, duration)
    null_a = bd.permutation_null(times, ordinary, duration, "asset", "probe",
                                 list(range(6)), params)
    null_b = bd.permutation_null(times, extreme, duration, "asset", "probe",
                                 list(range(6)), params)
    check("partial-bin depths do not change the observed statistic",
          obs_a["delta_window"] == obs_b["delta_window"])
    check("partial-bin depths do not change the null",
          null_a["values"] == null_b["values"],
          "Q95 %.2f um in both" % null_a["q95"])


def case_null_and_quiet_host(n_permutations):
    """A quiet host passes, is labelled unresolved, and its null replays."""
    print("null and the quiet host")
    duration = 3660.0
    times, depths, rows = make_band(
        n_units=14, duration_s=duration, rate_hz=8.0, depth_noise_um=18.0,
        seed=FIXTURE_SEED + 7)
    obs = bd.measure_band_drift(times, depths, duration)
    if not check("measurable", obs["measurable"], obs.get("reason", "")):
        return
    params = {"n_permutations": n_permutations}
    t0 = time.time()
    null = bd.permutation_null(times, depths, duration, "asset-A", "probe01", rows, params)
    elapsed = time.time() - t0
    check("the null returns the requested replicates",
          len(null["values"]) == n_permutations,
          "%d replicates in %.1f s" % (n_permutations, elapsed))
    check("the nearest rank is ceil(0.95 n)",
          null["rank"] == int(np.ceil(0.95 * n_permutations)), "rank %d" % null["rank"])
    check("Q95 is the value at that rank",
          null["q95"] == sorted(null["values"])[null["rank"] - 1])

    again = bd.permutation_null(times, depths, duration, "asset-A", "probe01", rows, params)
    check("the same inputs replay the same null exactly",
          again["values"] == null["values"])
    other = bd.permutation_null(times, depths, duration, "asset-B", "probe01", rows, params)
    check("a different asset draws a different null", other["values"] != null["values"])
    other_probe = bd.permutation_null(
        times, depths, duration, "asset-A", "probe00", rows, params)
    check("a different probe draws a different null",
          other_probe["values"] != null["values"])

    gate = bd.apply_gate(obs, null, 20.0)
    check("a flat band passes the 20 um gate", gate["passed"] is True, gate["reason"])
    check("and is labelled as unresolved rather than rejected",
          gate["inside_null"] and gate["label"] == "no time-ordered drift resolved",
          "observed %.2f um, Q95 %.2f um" % (gate["delta_window"], gate["q95_null"]))
    return obs, null


def case_gate_quadrants():
    """All four (excursion, resolution) quadrants map to the right verdict."""
    print("gate quadrants")
    def fake(delta, q95, L=20.0):
        return bd.apply_gate({"measurable": True, "delta_window": delta},
                             {"q95": q95}, L)

    v = fake(5.0, 3.0)
    check("low excursion, tight null, resolved -> pass",
          v["passed"] and v["label"] == "resolved, within tolerance")
    v = fake(3.0, 8.0)
    check("low excursion inside a tight null -> pass, unresolved",
          v["passed"] and v["label"] == "no time-ordered drift resolved")
    v = fake(5.0, 26.0)
    check("low excursion, null wider than tolerance -> unmeasurable",
          (not v["passed"]) and v["label"] == "unmeasurable")
    v = fake(31.0, 6.0)
    check("high excursion above a tight null -> resolved drift",
          (not v["passed"]) and v["label"] == "resolved drift")
    v = fake(31.0, 45.0)
    check("high excursion inside a wide null -> noise-limited",
          (not v["passed"]) and v["label"] == "noise-limited")
    v = fake(31.0, 6.0, L=40.0)
    check("the relaxed threshold passes what the strict one failed",
          v["passed"] is True)


def case_null_contamination_fixture(n_permutations):
    """One additive-ramp fixture demonstrates that drift can widen the null."""
    print("null contamination fixture")
    duration = 3660.0
    quiet = make_band(n_units=14, duration_s=duration, rate_hz=8.0,
                      depth_noise_um=18.0, seed=FIXTURE_SEED + 8)
    drifting = make_band(n_units=14, duration_s=duration, rate_hz=8.0,
                         depth_noise_um=18.0, seed=FIXTURE_SEED + 8,
                         trajectory=lambda t: 240.0 * t / duration)
    params = {"n_permutations": n_permutations}
    q_null = bd.permutation_null(quiet[0], quiet[1], duration, "a", "p", quiet[2], params)
    d_null = bd.permutation_null(drifting[0], drifting[1], duration, "a", "p",
                                 drifting[2], params)
    check("real movement widens this fixture's own null",
          d_null["q95"] > q_null["q95"],
          "quiet Q95 %.2f um, drifting Q95 %.2f um" % (q_null["q95"], d_null["q95"]))
    d_obs = bd.measure_band_drift(drifting[0], drifting[1], duration)
    gate = bd.apply_gate(d_obs, d_null, 20.0)
    check("the drifting band still fails, and on its excursion",
          (not gate["passed"]) and gate["delta_window"] > 20.0,
          "observed %.2f um" % gate["delta_window"])


def case_per_unit_audit_values():
    """The per-unit audit values expose composition the band median hides.

    The dilution fixture is Codex's Session 21 review counterexample, kept here
    as a permanent case: five units share a 30 um ramp and six flat traces are
    added, after which the across-unit median reports no excursion at all. The
    gate's verdict is unchanged by this case -- what is tested is that the
    reported per-unit values make the composition behind that verdict visible.
    """
    print("per-unit audit values")
    n_bins, per_bin = 12, 10
    times = np.concatenate(
        [b * 60.0 + np.linspace(1.0, 50.0, per_bin) for b in range(n_bins)])
    ramp = np.repeat(np.linspace(0.0, 30.0, n_bins), per_bin)
    flat = np.zeros(n_bins * per_bin, dtype=np.float64)
    extent = n_bins * 60.0

    moving = bd.measure_band_drift([times] * 5, [ramp] * 5, extent)
    diluted = bd.measure_band_drift([times] * 11, [ramp] * 5 + [flat] * 6, extent)

    check("the diluted band median reports no excursion",
          moving["delta_window"] > 20.0 and diluted["delta_window"] == 0.0,
          "five moving %.3f um, plus six flat %.3f um"
          % (moving["delta_window"], diluted["delta_window"]))
    check("but each unit's own worst window still carries it",
          abs(max(diluted["unit_delta_max_window"]) - moving["delta_window"]) < 1e-9,
          "largest per-unit window excursion %.12f um against the undiluted "
          "band's %.12f um" % (max(diluted["unit_delta_max_window"]),
                               moving["delta_window"]))
    check("and they separate the movers from the rest",
          sum(1 for v in diluted["unit_delta_max_window"] if v > 20.0) == 5
          and sum(1 for v in diluted["unit_delta_max_window"] if v == 0.0) == 6)
    check("all per-unit audit lists align with the included units",
          all(len(diluted[key]) == len(diluted["included"]) == 11 for key in (
              "unit_delta_full", "unit_delta_max_window", "unit_max_window_start",
              "unit_max_window_defined_bins", "unit_delta_band_window",
              "unit_band_window_defined_bins")))
    check("the audit values do not reach the verdict",
          bd.apply_gate(diluted, {"q95": 0.0}, 20.0)["passed"] is True)

    times4, depths4, _ = make_band(n_units=9, duration_s=3660.0, seed=FIXTURE_SEED + 11)
    obs = bd.measure_band_drift(times4, depths4, 3660.0)
    stack = bd.unit_traces(
        [bd.bin_medians(d, bd.bin_offsets(t, obs["n_bins"]))
         for t, d in zip(times4, depths4)],
        np.isin(np.arange(9), obs["included"]))
    check("every centred unit series has median zero",
          max(abs(np.median(r[np.isfinite(r)])) for r in stack) < 1e-9)
    check("no per-unit excursion is below its own window excursion",
          all(f >= w - 1e-9 for f, w in zip(obs["unit_delta_full"],
                                            obs["unit_delta_max_window"])))

    # A flat band trace makes its selected window an arbitrary earliest tie.
    # Movement confined to a later window must remain visible at the same
    # ten-bin scale rather than only in the whole-recording range.
    late_levels = np.concatenate([np.zeros(10), np.linspace(0.0, 30.0, 10)])
    late_movement = np.repeat(late_levels, per_bin)
    late_times = np.concatenate(
        [b * 60.0 + np.linspace(1.0, 50.0, per_bin) for b in range(20)])
    localized = bd.measure_band_drift(
        [late_times] * 11,
        [late_movement] * 5 + [np.zeros(20 * per_bin)] * 6,
        20 * 60.0,
    )
    check("the flat band selects the earliest tied window",
          localized["delta_window"] == 0.0 and localized["window_start"] == 0)
    check("the band-aligned unit windows can therefore miss late movement",
          all(v == 0.0 for v in localized["unit_delta_band_window"]))
    check("each unit's own worst window exposes the late movement",
          sum(v > 20.0 for v in localized["unit_delta_max_window"]) == 5
          and sum(v == 0.0 for v in localized["unit_delta_max_window"]) == 6)
    check("the per-unit starts locate the late moving windows",
          all(start >= 9 for start in localized["unit_max_window_start"][:5])
          and localized["unit_max_window_start"][5:] == [0] * 6)
    check("the selected audit windows report their defined-bin support",
          localized["unit_max_window_defined_bins"] == [10] * 11
          and localized["unit_band_window_defined_bins"] == [10] * 11)
    try:
        bd.unit_traces([np.zeros(3)], np.array([True, False]))
        check("a mask that does not match the units raises", False)
    except ValueError:
        check("a mask that does not match the units raises", True)
    try:
        bd.unit_excursions(np.zeros((2, 12)), band_window_start=3.5)
        check("a non-integer band-window start raises", False)
    except ValueError:
        check("a non-integer band-window start raises", True)


def case_per_unit_audit_has_no_null(n_permutations):
    """The audit values are not on the band null's scale, in either direction.

    The specification requires per-unit excursions to be reported, and the two
    natural ways to read them are both wrong. ``Q95_null`` is the noise floor of
    a median *across* units, so it is systematically narrower than one unit's;
    comparing a per-unit value against it -- or against the gate threshold --
    reads pure estimation noise as suppressed movement. And the scatter of the
    per-unit worst-window starts is not evidence of a quiet band: a genuine
    common ramp scatters them too, because a near-linear trajectory leaves many
    windows nearly tied. Both halves are fixtures here so the reading rule in
    the specification stays checkable rather than asserted.
    """
    print("per-unit audit values carry no null")
    duration = 3660.0
    ratios = []
    for n_units in (9, 14, 25):
        times, depths, rows = make_band(n_units=n_units, duration_s=duration,
                                        seed=FIXTURE_SEED + 21)
        obs = bd.measure_band_drift(times, depths, duration)
        null = bd.permutation_null(times, depths, duration, "a", "p", rows,
                                   {"n_permutations": n_permutations})
        own = obs["unit_delta_max_window"]
        check("with no movement at all, every %2d-unit per-unit window "
              "excursion still exceeds the band null" % n_units,
              all(v > null["q95"] for v in own),
              "smallest per-unit %.3f um against Q95_null %.3f um"
              % (min(own), null["q95"]))
        ratios.append(min(own) / null["q95"])
    check("and the gap widens with the unit count",
          ratios[0] < ratios[1] < ratios[2],
          "smallest-to-Q95 ratio %.2f, %.2f, %.2f at 9, 14, 25 units" % tuple(ratios))

    times, depths, _ = make_band(n_units=14, duration_s=duration,
                                 seed=FIXTURE_SEED + 22,
                                 trajectory=lambda t: 30.0 * t / duration)
    ramp = bd.measure_band_drift(times, depths, duration)
    starts = ramp["unit_max_window_start"]
    check("a genuine common ramp scatters the per-unit worst windows too",
          len(set(starts)) >= 10,
          "%d distinct starts among %d units, spanning bins %d to %d"
          % (len(set(starts)), len(starts), min(starts), max(starts)))

    tied = np.zeros(20, dtype=np.float64)
    tied[9] = tied[19] = 10.0
    audit = bd.unit_excursions(tied.reshape(1, 20))
    check("a unit's tied worst windows resolve to the earliest",
          audit["delta_max_window"][0] == 10.0 and audit["max_window_start"][0] == 0)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--permutations", type=int, default=bd.PARAMS["n_permutations"],
                        help="replicates for the null cases; the default is the pinned gate own "
                             "count, so what is tested is what will run")
    args = parser.parse_args()

    print("band-drift estimator, synthetic tests")
    print("permutations per null case: %d (the gate itself is pinned at %d)"
          % (args.permutations, bd.PARAMS["n_permutations"]))
    print("")

    case_seed_derivations()
    case_binning()
    case_known_ramp()
    case_down_and_back()
    case_worst_window()
    case_unit_inclusion()
    case_invalid_bin_rejects()
    case_too_few_units()
    case_malformed_input_raises()
    case_partial_bin_is_discarded_from_null(args.permutations)
    case_null_and_quiet_host(args.permutations)
    case_gate_quadrants()
    case_null_contamination_fixture(args.permutations)
    case_per_unit_audit_values()
    case_per_unit_audit_has_no_null(args.permutations)

    failed = [name for name, ok, _ in RESULTS if not ok]
    print("")
    print("%d checks, %d failed" % (len(RESULTS), len(failed)))
    for name in failed:
        print("  FAIL  %s" % name)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
