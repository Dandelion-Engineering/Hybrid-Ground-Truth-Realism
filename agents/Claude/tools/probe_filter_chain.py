"""Measure the two filter constructions section 19.3 has to choose between.

RC-007 Round 1 finding F4 says two things about the draft-29 preprocessing
chain, and both have to be settled with numbers rather than prose:

  (a) the anchor pipeline's high-pass was described as a causal recursive
      filter, and it is not -- SpikeInterface applies a fifth-order Butterworth
      forward and backward through scipy's sosfiltfilt, which is zero phase;
  (b) the draft's rectangular DFT high-pass was described as having its wrap
      confined to the discarded edge samples, and it is not -- the ideal
      filter's impulse response is global.

This script measures four things and writes them to a recorded file:

  1. the DFT high-pass impulse response at the centre of one 13020-sample
     window, against the closed form -1/n that the reviewer predicted;
  2. the pole radii of the fifth-order Butterworth high-pass at 300 Hz and the
     slowest resulting time constant, which is what a margin has to cover;
  3. how far an isolated 13020-sample window's scale estimate departs from the
     same window filtered inside a long continuous signal, for both
     constructions and at two margin widths;
  4. the same comparison on a window carrying a low-frequency excursion, which
     is the case a wrap-sensitive operator handles worst.

Nothing here reads the archive and nothing here is a candidate measurement.
The signals are synthetic and seedless-by-construction from one pinned seed.

Both constructions are applied to float64 microvolt-scaled data, per section
19.3 step 1, and the scale estimate is the MAD estimator section 19.3 step 5
pins.
"""

import argparse
import json
import os
import sys

import numpy as np
from scipy import signal

CHUNK_SAMPLES = 13020
NOMINAL_RATE_HZ = 30000.0
CUTOFF_HZ = 300.0
FILTER_ORDER = 5
MAD_TO_SIGMA = 0.6744897501960817
PINNED_SEED = 20260818
N_TRIALS = 12
CONTEXT_CHUNKS = 9


def brickwall_highpass(x, rate_hz=NOMINAL_RATE_HZ, cutoff_hz=CUTOFF_HZ):
    """Apply draft 29's rectangular DFT high-pass along the last axis.

    x: float array whose last axis is time.
    Returns an array of the same shape with every frequency bin strictly below
    cutoff_hz set to zero.
    """
    spectrum = np.fft.rfft(x, axis=-1)
    freqs = np.fft.rfftfreq(x.shape[-1], d=1.0 / rate_hz)
    spectrum[..., freqs < cutoff_hz] = 0.0
    return np.fft.irfft(spectrum, n=x.shape[-1], axis=-1)


def butter_sos(rate_hz=NOMINAL_RATE_HZ, cutoff_hz=CUTOFF_HZ, order=FILTER_ORDER):
    """Return the second-order sections of the anchor pipeline's high-pass.

    Fifth-order Butterworth, high-pass, designed at rate_hz, in sos form --
    the same design SpikeInterface's FilterRecording uses by default.
    """
    return signal.butter(order, cutoff_hz, btype="highpass", fs=rate_hz, output="sos")


def butter_highpass(x, sos):
    """Apply the Butterworth high-pass forward and backward along the last axis.

    Zero phase, via scipy.signal.sosfiltfilt, which is what SpikeInterface's
    default direction 'forward-backward' resolves to.
    """
    return signal.sosfiltfilt(sos, x, axis=-1)


def slowest_time_constant(sos):
    """Return (max pole radius, time constant in samples) for an sos filter.

    The time constant is -1 / ln(r) samples for the pole of largest radius r,
    which is the number of samples over which that mode decays by 1/e.
    """
    radii = []
    for section in sos:
        poles = np.roots(section[3:6])
        radii.extend(np.abs(poles).tolist())
    r_max = float(max(radii))
    tau = float(-1.0 / np.log(r_max))
    return r_max, tau


def mad_sigma(y, axis=-1):
    """Return the MAD-based scale estimate section 19.3 step 5 pins."""
    med = np.median(y, axis=axis, keepdims=True)
    return np.median(np.abs(y - med), axis=axis) / MAD_TO_SIGMA


def synth_signal(rng, n_samples, excursion_uv=0.0):
    """Build one channel of synthetic microvolt-scaled broadband data.

    White background at 6 uV, a 1/f-ish low-frequency component, a 50 Hz line
    component, and sparse spike-like transients -- everything a real AP stream
    carries that a high-pass has to remove or keep. excursion_uv adds a slow
    half-cycle drift of that peak amplitude, which is the case a wrap-sensitive
    operator handles worst.
    """
    t = np.arange(n_samples) / NOMINAL_RATE_HZ
    x = rng.normal(0.0, 6.0, n_samples)
    for freq, amp in ((2.0, 40.0), (7.0, 25.0), (17.0, 12.0)):
        x += amp * np.sin(2.0 * np.pi * freq * t + rng.uniform(0.0, 2.0 * np.pi))
    x += 8.0 * np.sin(2.0 * np.pi * 50.0 * t + rng.uniform(0.0, 2.0 * np.pi))
    n_spikes = max(1, n_samples // 3000)
    positions = rng.integers(40, n_samples - 40, n_spikes)
    shape = -np.exp(-0.5 * ((np.arange(-20, 40) - 0.0) / 6.0) ** 2)
    for pos in positions:
        x[pos - 20:pos + 40] += rng.uniform(60.0, 400.0) * shape
    if excursion_uv:
        x += excursion_uv * np.sin(np.pi * np.arange(n_samples) / n_samples)
    return x


def margin_discrepancy(rng, apply_filter, margin, excursion_uv):
    """Compare an isolated window against the same window filtered in context.

    Builds a long signal of CONTEXT_CHUNKS windows, filters it whole, and takes
    the centre window's retained core as the reference. Then filters that same
    centre window in isolation and takes its retained core. Returns the
    relative difference in the MAD scale estimate and the largest absolute
    per-sample difference, in microvolts.
    """
    n_long = CHUNK_SAMPLES * CONTEXT_CHUNKS
    long_signal = synth_signal(rng, n_long, excursion_uv=excursion_uv)
    start = CHUNK_SAMPLES * (CONTEXT_CHUNKS // 2)
    stop = start + CHUNK_SAMPLES

    reference_full = apply_filter(long_signal - long_signal.mean())
    reference = reference_full[start + margin:stop - margin]

    window = long_signal[start:stop]
    isolated_full = apply_filter(window - window.mean())
    isolated = isolated_full[margin:CHUNK_SAMPLES - margin]

    sigma_ref = float(mad_sigma(reference))
    sigma_iso = float(mad_sigma(isolated))
    return {
        "sigma_reference_uv": sigma_ref,
        "sigma_isolated_uv": sigma_iso,
        "relative_sigma_error": float(sigma_iso / sigma_ref - 1.0),
        "max_abs_sample_error_uv": float(np.max(np.abs(isolated - reference))),
    }


def run_margin_study(sos, margins, excursions):
    """Run margin_discrepancy over both constructions, margins and excursions.

    Returns a list of records, one per (construction, margin, excursion), each
    holding the worst case over N_TRIALS independent synthetic signals.
    """
    constructions = (
        ("dft_brickwall", brickwall_highpass),
        ("butterworth_sosfiltfilt", lambda x: butter_highpass(x, sos)),
    )
    records = []
    for name, fn in constructions:
        for margin in margins:
            for excursion in excursions:
                worst_sigma = 0.0
                worst_sample = 0.0
                sigma_ref_at_worst = 0.0
                for trial in range(N_TRIALS):
                    rng = np.random.default_rng(PINNED_SEED + trial)
                    out = margin_discrepancy(rng, fn, margin, excursion)
                    if abs(out["relative_sigma_error"]) > abs(worst_sigma):
                        worst_sigma = out["relative_sigma_error"]
                        sigma_ref_at_worst = out["sigma_reference_uv"]
                    worst_sample = max(worst_sample, out["max_abs_sample_error_uv"])
                records.append({
                    "construction": name,
                    "margin_samples": margin,
                    "margin_ms": 1000.0 * margin / NOMINAL_RATE_HZ,
                    "excursion_uv": excursion,
                    "trials": N_TRIALS,
                    "worst_relative_sigma_error": worst_sigma,
                    "sigma_reference_uv_at_worst": sigma_ref_at_worst,
                    "worst_max_abs_sample_error_uv": worst_sample,
                })
                print("  %-24s margin %4d  excursion %5.0f uV  "
                      "worst sigma error %+9.6f  worst sample error %8.4f uV"
                      % (name, margin, excursion, worst_sigma, worst_sample))
    return records


def impulse_report():
    """Measure the DFT high-pass impulse response at the window centre."""
    impulse = np.zeros(CHUNK_SAMPLES)
    impulse[0] = 1.0
    h = brickwall_highpass(impulse)
    centre = CHUNK_SAMPLES // 2
    return {
        "n": CHUNK_SAMPLES,
        "h_centre": float(h[centre]),
        "closed_form_minus_one_over_n": float(-1.0 / CHUNK_SAMPLES),
        "matches_closed_form": bool(abs(h[centre] + 1.0 / CHUNK_SAMPLES) < 1e-18),
        "max_abs_h_outside_150_sample_edges": float(np.max(np.abs(h[150:-150]))),
        "sum_abs_h_outside_150_sample_edges": float(np.sum(np.abs(h[150:-150]))),
    }


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo-root", required=True,
                        help="Project root. Used only to resolve --out and --records.")
    parser.add_argument("--out", required=True,
                        help="Path, relative to --repo-root, for the recorded text report.")
    parser.add_argument("--records",
                        help="Optional path, relative to --repo-root, for a JSON record.")
    parser.add_argument("--margins", default="150,500",
                        help="Comma-separated margin widths in samples. Default 150,500.")
    parser.add_argument("--excursions", default="0,200",
                        help="Comma-separated slow-excursion peak amplitudes in uV. "
                             "Default 0,200.")
    return parser.parse_args(argv)


def main(argv=None):
    """Measure both constructions and write the recorded report."""
    args = parse_args(argv)
    root = os.path.abspath(args.repo_root)
    if not os.path.isdir(root):
        raise SystemExit("repo root is not a directory: %s" % root)
    margins = [int(v) for v in args.margins.split(",") if v.strip()]
    excursions = [float(v) for v in args.excursions.split(",") if v.strip()]
    for margin in margins:
        if not 0 < margin < CHUNK_SAMPLES // 2:
            raise SystemExit("margin out of range: %d" % margin)

    print("probe_filter_chain: window %d samples at %.1f Hz nominal, cutoff %.1f Hz"
          % (CHUNK_SAMPLES, NOMINAL_RATE_HZ, CUTOFF_HZ))
    print("numpy %s, scipy %s" % (np.__version__, __import__("scipy").__version__))

    print("[1/3] DFT high-pass impulse response")
    impulse = impulse_report()
    print("  h[%d] = %+.15f, closed form -1/n = %+.15f, match %s"
          % (impulse["n"] // 2, impulse["h_centre"],
             impulse["closed_form_minus_one_over_n"], impulse["matches_closed_form"]))
    print("  max |h| outside the 150-sample edges = %.6e"
          % impulse["max_abs_h_outside_150_sample_edges"])

    print("[2/3] Butterworth pole radii")
    sos = butter_sos()
    r_max, tau = slowest_time_constant(sos)
    poles = {
        "order": FILTER_ORDER,
        "sections": int(sos.shape[0]),
        "max_pole_radius": r_max,
        "tau_samples": tau,
        "tau_ms": 1000.0 * tau / NOMINAL_RATE_HZ,
    }
    print("  %d sections, max pole radius %.9f, tau %.3f samples (%.4f ms)"
          % (poles["sections"], r_max, tau, poles["tau_ms"]))
    for margin in margins:
        print("  margin %4d samples = %6.3f tau, residual exp(-margin/tau) = %.3e"
              % (margin, margin / tau, float(np.exp(-margin / tau))))

    print("[3/3] isolated window versus the same window filtered in context")
    records = run_margin_study(sos, margins, excursions)

    lines = []
    lines.append("probe_filter_chain")
    lines.append("==================")
    lines.append("")
    lines.append("window samples      : %d" % CHUNK_SAMPLES)
    lines.append("nominal rate        : %.1f Hz" % NOMINAL_RATE_HZ)
    lines.append("cutoff              : %.1f Hz" % CUTOFF_HZ)
    lines.append("trials per cell     : %d" % N_TRIALS)
    lines.append("context length      : %d windows" % CONTEXT_CHUNKS)
    lines.append("pinned seed         : %d" % PINNED_SEED)
    lines.append("numpy / scipy       : %s / %s"
                 % (np.__version__, __import__("scipy").__version__))
    lines.append("")
    lines.append("1. DFT high-pass impulse response over one window")
    lines.append("   h[n/2]                         : %+.15e" % impulse["h_centre"])
    lines.append("   closed form -1/n               : %+.15e"
                 % impulse["closed_form_minus_one_over_n"])
    lines.append("   equal                          : %s" % impulse["matches_closed_form"])
    lines.append("   max |h| outside 150-sample edge: %.6e"
                 % impulse["max_abs_h_outside_150_sample_edges"])
    lines.append("   sum |h| outside 150-sample edge: %.6f"
                 % impulse["sum_abs_h_outside_150_sample_edges"])
    lines.append("   reading: the operator is not local; the discarded edges do not")
    lines.append("   contain its response.")
    lines.append("")
    lines.append("2. Fifth-order Butterworth high-pass at 300 Hz")
    lines.append("   second-order sections          : %d" % poles["sections"])
    lines.append("   largest pole radius            : %.12f" % poles["max_pole_radius"])
    lines.append("   slowest time constant          : %.4f samples (%.4f ms)"
                 % (poles["tau_samples"], poles["tau_ms"]))
    for margin in margins:
        lines.append("   margin %4d samples             : %.3f tau, residual %.3e"
                     % (margin, margin / tau, float(np.exp(-margin / tau))))
    lines.append("")
    lines.append("3. Isolated window versus the same window filtered in context")
    lines.append("   worst case over %d synthetic signals per cell." % N_TRIALS)
    lines.append("")
    lines.append("   %-24s %7s %10s %14s %14s"
                 % ("construction", "margin", "excursion", "sigma error", "sample error"))
    for rec in records:
        lines.append("   %-24s %7d %9.0f uV %+13.6f %11.4f uV"
                     % (rec["construction"], rec["margin_samples"], rec["excursion_uv"],
                        rec["worst_relative_sigma_error"],
                        rec["worst_max_abs_sample_error_uv"]))
    lines.append("")
    lines.append("   sigma error is the relative error in the MAD scale estimate over")
    lines.append("   the retained core; sample error is the largest absolute per-sample")
    lines.append("   difference over that same core. Both are worst-case over trials.")

    out_path = os.path.join(root, args.out)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print("wrote %s" % out_path)

    if args.records:
        rec_path = os.path.join(root, args.records)
        os.makedirs(os.path.dirname(rec_path) or ".", exist_ok=True)
        payload = {
            "window_samples": CHUNK_SAMPLES,
            "nominal_rate_hz": NOMINAL_RATE_HZ,
            "cutoff_hz": CUTOFF_HZ,
            "trials": N_TRIALS,
            "context_chunks": CONTEXT_CHUNKS,
            "pinned_seed": PINNED_SEED,
            "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
            "impulse": impulse,
            "butterworth": poles,
            "margin_study": records,
        }
        with open(rec_path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, indent=1, sort_keys=True)
            handle.write("\n")
        print("wrote %s" % rec_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
