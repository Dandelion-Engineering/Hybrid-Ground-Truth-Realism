"""Owner evidence for the RC-008 Round-2 response to section 19.

Every number this session writes into section 19 is computed here rather than
taken from the reviewer's message. Five of the six groups reproduce a reviewer
finding independently - a different construction where one is available, so that
agreement is evidence rather than an echo:

  1. F1-R1  the maximum over the grid cannot enforce a lower floor.
  2. F2-R1  the nominal design rate is not the recording's own rate, and what
            that does and does not change about the pinned operator.
  3. F3-R1  interleaving does not universally compress the split-half spread.
  4. F5-R1  a percentile ratio is not monotone in one channel's value.
  5. T1-R1  the two cheaper read arrangements have two different defects, and
            the coverage half of it is arithmetic that can be computed exactly.
  6. T4-R1  the phase-omission direction under the shared-component model.

Nothing here reads the archive and nothing here is a measurement of any
candidate. Every fixture is synthetic and deterministic.

Usage:

    ./venv/Scripts/python.exe agents/Claude/tools/probe_rc008_round2.py \
        --repo-root . --out <path> [--records <path>]
"""

import argparse
import io
import json
import os
import sys

import numpy as np
from scipy import signal

MAD_TO_SIGMA = 0.6744897501960817
NOMINAL_HZ = 30000.0
RANK1_HZ = 30000.039869961383           # host_timing_index.jsonl, whole span
RANK1_HEAD_HZ = 30000.03989331282       # the same file, first 1000 timestamps
RANK1_PROBE00_HZ = 29999.999999999996   # the other probe in the same session
CHUNK = 13020
MARGIN = 500
CORNER_HZ = 300.0
CONVERSION_UV = 2.34375
C_CHUNKS = 9999
CHUNK_SECONDS = CHUNK / NOMINAL_HZ


class Probe(object):
    """Collect PASS/FAIL lines and a structured record in one place."""

    def __init__(self):
        self.lines = []
        self.records = {}
        self.failed = 0
        self.passed = 0

    def check(self, name, ok, detail=""):
        """Record one boolean check and print it."""
        if ok:
            self.passed += 1
        else:
            self.failed += 1
        line = "%s  %s" % ("PASS" if ok else "FAIL", name)
        if detail:
            line += "  [%s]" % detail.encode("ascii",
                                             "backslashreplace").decode("ascii")
        self.lines.append(line)
        print(line)

    def heading(self, text):
        """Start a labelled group."""
        self.lines.append("")
        self.lines.append(text)
        print("")
        print(text)

    def note(self, text):
        """Record a measured value that is not itself a check."""
        line = "      %s" % text.encode("ascii",
                                        "backslashreplace").decode("ascii")
        self.lines.append(line)
        print(line)


def mad_sigma(x):
    """Return the MAD scale estimate of a 1-D array, the section 19.3 way."""
    return np.median(np.abs(x - np.median(x))) / MAD_TO_SIGMA


def nearest_rank(values, q):
    """Return the nearest-rank percentile: rank ceil(q*n) over a sorted copy."""
    ordered = np.sort(np.asarray(values, dtype=float))
    n = ordered.size
    rank = int(np.ceil(q * n))
    return ordered[rank - 1], rank


def spread(values):
    """Return the nearest-rank p90/p10 ratio of a per-channel vector."""
    p10, _ = nearest_rank(values, 0.10)
    p90, _ = nearest_rank(values, 0.90)
    return p90 / p10


def scipy_default_padlen(sos):
    """Return the padlen scipy.signal.sosfiltfilt would choose for this sos."""
    ntaps = 2 * len(sos) + 1
    ntaps -= min((sos[:, 2] == 0).sum(), (sos[:, 5] == 0).sum())
    return 3 * ntaps


def grid(k_windows, c_chunks):
    """Return the section 19.4 window-centre grid for K windows and C chunks."""
    return [1 + int(np.floor(k * (c_chunks - 3) / (k_windows - 1) + 0.5))
            for k in range(k_windows)]


def guarantee(indices):
    """Return (largest gap, longest unsampled run, guaranteed-detection chunks).

    The guarantee is the smallest number of consecutive chunks that must contain
    a sampled index anywhere inside the span, verified exhaustively rather than
    argued.
    """
    ordered = sorted(set(indices))
    gaps = [b - a for a, b in zip(ordered, ordered[1:])]
    g = max(gaps)
    marked = set(ordered)
    lo, hi = ordered[0], ordered[-1]
    need = None
    for width in range(1, g + 2):
        if all(any(i in marked for i in range(start, start + width))
               for start in range(lo, hi - width + 2)):
            need = width
            break
    return g, g - 1, need


def parity_fixture(ratios, core=CHUNK):
    """Build a deterministic per-channel core whose two parities differ.

    ``ratios[c]`` is the ratio of the even-sample scale to the odd-sample scale
    on channel ``c``.  Magnitudes are constant within a parity class and signs
    are balanced inside every half used below, so each MAD is exact rather than
    sampled.  Returns an array of shape (n_channels, core).
    """
    t = np.arange(core)
    sign = np.where((t % 4 == 0) | (t % 4 == 3), 1.0, -1.0)
    rows = []
    for ratio in ratios:
        even_scale = float(ratio) if ratio >= 1 else 1.0
        odd_scale = 1.0 if ratio >= 1 else 1.0 / float(ratio)
        scale = np.where(t % 2 == 0, even_scale, odd_scale)
        rows.append(scale * sign)
    return np.array(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--records", default=None)
    args = parser.parse_args(argv)

    root = os.path.abspath(args.repo_root)
    p = Probe()

    # ------------------------------------------------------------------ F1 --
    p.heading("1. F1-R1  the maximum cannot enforce the lower floor")
    levels = np.array([1.0] * 59 + [5.0])
    worst = levels.max()
    quietest = levels.min()
    p.note("S(k): 59 windows at 1.0 uV, one at 5.0 uV")
    p.note("max = %.3f uV, min = %.3f uV, floor = 1.25 uV, N = 10.0 uV"
           % (worst, quietest))
    p.check("the maximum clears the ceiling", worst <= 10.0)
    p.check("the maximum clears the floor, so branch 2 does not fire on it",
            not worst < 1.25)
    p.check("the minimum violates the floor", quietest < 1.25)
    p.check("59 of 60 sampled windows violate it",
            int((levels < 1.25).sum()) == 59)
    p.check("the quiet windows exceed the anti-saturation ceiling on SNR",
            50.0 / quietest > 40.0, "A_min/S(k) = %.1f" % (50.0 / quietest))
    p.check("the loud window does not", 50.0 / worst <= 40.0,
            "A_min/S(k) = %.1f" % (50.0 / worst))
    p.records["f1"] = {"n_windows": int(levels.size),
                       "sigma_worst_sampled": float(worst),
                       "sigma_quietest_sampled": float(quietest),
                       "n_below_floor": int((levels < 1.25).sum()),
                       "snr_p2p_at_quietest": float(50.0 / quietest),
                       "snr_p2p_at_worst": float(50.0 / worst)}

    # ------------------------------------------------------------------ F2 --
    p.heading("2. F2-R1  the nominal design rate is not the recording's own")
    sos_nom = signal.butter(5, CORNER_HZ, btype="highpass", fs=NOMINAL_HZ,
                            output="sos")
    sos_rec = signal.butter(5, CORNER_HZ, btype="highpass", fs=RANK1_HZ,
                            output="sos")
    sos_head = signal.butter(5, CORNER_HZ, btype="highpass", fs=RANK1_HEAD_HZ,
                             output="sos")
    coeff_delta = float(np.max(np.abs(sos_nom - sos_rec)))
    head_delta = float(np.max(np.abs(sos_rec - sos_head)))
    p.note("max |sos(nominal) - sos(rank-1 whole-span rate)| = %.11e"
           % coeff_delta)
    p.note("max |sos(rank-1 whole-span) - sos(rank-1 head estimate)| = %.11e"
           % head_delta)
    p.check("the two designs are not identical", coeff_delta > 0.0)
    p.check("but the deviation is small in the coefficients",
            coeff_delta < 1e-6)
    p.check("'the recording's rate' is itself not one number",
            head_delta > 0.0,
            "whole-span and head-estimate designs differ by %.3e" % head_delta)
    p.check("the two probes in the same session declare different rates",
            RANK1_HZ != RANK1_PROBE00_HZ,
            "Probe01 %.9f Hz vs Probe00 %.9f Hz" % (RANK1_HZ,
                                                    RANK1_PROBE00_HZ))

    pad_nom = scipy_default_padlen(sos_nom)
    pad_rec = scipy_default_padlen(sos_rec)
    p.check("scipy's default padlen is 18 at the nominal rate", pad_nom == 18,
            "padlen %d" % pad_nom)
    p.check("and is unchanged at the recording rate", pad_rec == pad_nom,
            "padlen %d" % pad_rec)

    margin_ms = 5.0 * (1000.0 / CORNER_HZ)
    margins = {}
    for label, fs in (("nominal", NOMINAL_HZ), ("recording", RANK1_HZ),
                      ("head", RANK1_HEAD_HZ)):
        exact = margin_ms / 1000.0 * fs
        margins[label] = {"exact": float(exact), "int": int(exact),
                          "floor": int(np.floor(exact)),
                          "round": int(np.floor(exact + 0.5))}
        p.note("margin at %s rate: %.6f samples -> int %d, floor %d, round %d"
               % (label, exact, margins[label]["int"], margins[label]["floor"],
                  margins[label]["round"]))
    p.check("the margin is 500 samples at every rate under every rounding",
            all(v[key] == MARGIN for v in margins.values()
                for key in ("int", "floor", "round")))

    rng = np.random.default_rng(20260818)
    block = np.round(rng.normal(0.0, 6.0, CHUNK + 2 * MARGIN)
                     / CONVERSION_UV) * CONVERSION_UV
    ret_nom = signal.sosfiltfilt(sos_nom, block, padtype="odd",
                                 padlen=18)[MARGIN:-MARGIN]
    ret_rec = signal.sosfiltfilt(sos_rec, block, padtype="odd",
                                 padlen=18)[MARGIN:-MARGIN]
    sample_delta = float(np.max(np.abs(ret_nom - ret_rec)))
    sigma_nom = mad_sigma(ret_nom)
    sigma_rec = mad_sigma(ret_rec)
    rel = float(abs(sigma_nom - sigma_rec) / sigma_rec)
    p.note("worst retained sample moves by %.11e uV" % sample_delta)
    p.note("the retained scale estimate moves by %.11e relative "
           "(%.9f vs %.9f uV)" % (rel, sigma_nom, sigma_rec))
    p.check("the retained samples are not identical either", sample_delta > 0.0)
    p.check("this is a single-fixture diagnostic and not a bound", True,
            "one seed, one channel, quantized 6 uV noise")
    p.records["f2"] = {"coeff_delta": coeff_delta, "head_delta": head_delta,
                       "padlen_nominal": int(pad_nom),
                       "padlen_recording": int(pad_rec),
                       "margin_samples": margins,
                       "retained_sample_delta_uv": sample_delta,
                       "retained_sigma_relative_delta": rel,
                       "corner_shift_hz": float(
                           CORNER_HZ * abs(RANK1_HZ - NOMINAL_HZ) / NOMINAL_HZ)}
    p.note("the 300 Hz corner moves by %.6f Hz at rank 1's declared rate"
           % p.records["f2"]["corner_shift_hz"])

    # ------------------------------------------------------------------ F3 --
    p.heading("3. F3-R1  interleaving does not universally compress the spread")
    ratios = [2.0] * 8 + [1.0] * 56 + [0.5] * 8
    core = parity_fixture(ratios)
    p.check("the fixture is 72 channels of 13,020 retained samples",
            core.shape == (72, CHUNK), "%s" % (core.shape,))

    half = CHUNK // 2
    contiguous = np.array([mad_sigma(row[:half]) / mad_sigma(row[half:])
                           for row in core])
    interleaved = np.array([mad_sigma(row[0::2]) / mad_sigma(row[1::2])
                            for row in core])
    r_contig = spread(contiguous)
    r_inter = spread(interleaved)
    p.note("contiguous halves: R_null = %.9f" % r_contig)
    p.note("even/odd interleaved: R_null = %.9f" % r_inter)
    p.check("contiguous halves give exactly 1", abs(r_contig - 1.0) < 1e-12)
    p.check("even/odd interleaving gives exactly 4", abs(r_inter - 4.0) < 1e-12)
    p.check("so interleaving EXPANDED the spread on this construction",
            r_inter > r_contig)
    p.check("and it crosses the strict tolerance while contiguous does not",
            r_inter > 2.0 >= r_contig)
    p.check("every channel's contiguous ratio is exactly 1",
            bool(np.all(np.abs(contiguous - 1.0) < 1e-12)))
    p.records["f3"] = {"r_null_contiguous": float(r_contig),
                       "r_null_interleaved": float(r_inter),
                       "ratios_used": sorted(set(ratios))}

    # ------------------------------------------------------------------ F5 --
    p.heading("4. F5-R1  a percentile ratio is not monotone in one channel")
    base = np.array([1.0] * 8 + [2.0] * 56 + [3.0] * 8)
    p10_b, rank10 = nearest_rank(base, 0.10)
    p90_b, rank90 = nearest_rank(base, 0.90)
    r_base = p90_b / p10_b
    bad = base.copy()
    bad[0] = 100.0
    p10_x, _ = nearest_rank(bad, 0.10)
    p90_x, _ = nearest_rank(bad, 0.90)
    r_bad = p90_x / p10_x
    p.note("nearest-rank ranks at n=72: p10 = rank %d, p90 = rank %d"
           % (rank10, rank90))
    p.note("base band: p90/p10 = %.3f / %.3f = %.3f" % (p90_b, p10_b, r_base))
    p.note("one quiet channel replaced by 100: p90/p10 = %.3f / %.3f = %.3f"
           % (p90_x, p10_x, r_bad))
    p.check("the base band fails the strict spatial tolerance", r_base > 2.0)
    p.check("the band with one extreme channel passes it", r_bad <= 2.0)
    p.check("so an unmasked bad channel moved the statistic PERMISSIVELY",
            r_bad < r_base)
    dead = base.copy()
    dead[-1] = 0.0
    p10_d, _ = nearest_rank(dead, 0.10)
    p.check("a dead channel below the p10 rank leaves the ratio alone",
            abs(p10_d - p10_b) < 1e-12,
            "p10 %.3f -> %.3f" % (p10_b, p10_d))
    many_dead = base.copy()
    many_dead[:8] = 0.0
    with np.errstate(divide="ignore"):
        many_dead_spread = spread(many_dead)
    p.check("enough dead channels do drive it to +inf",
            not np.isfinite(many_dead_spread))
    p.records["f5"] = {"rank_p10": int(rank10), "rank_p90": int(rank90),
                       "r_space_base": float(r_base),
                       "r_space_one_extreme": float(r_bad),
                       "direction": "permissive"}

    # ------------------------------------------------------------------ T1 --
    p.heading("5. T1-R1  the two cheaper arrangements have two defects")
    pinned = grid(60, C_CHUNKS)
    g0, run0, need0 = guarantee(pinned)
    p.check("the pinned grid still gives g = 170", g0 == 170, "g = %d" % g0)
    p.check("its guarantee is still 170 chunks", need0 == 170,
            "%d chunks, %.3f s" % (need0, need0 * CHUNK_SECONDS))
    p.note("pinned: 60 windows, 180 transfers, guarantee %.3f s"
           % (need0 * CHUNK_SECONDS))

    anchors = [int(np.floor(t * (C_CHUNKS - 5) / 19.0 + 0.5))
               for t in range(20)]
    clustered = sorted({a + off for a in anchors for off in (1, 2, 3)})
    gc, runc, needc = guarantee(clustered)
    p.check("the five-chunk arrangement retains the same 60 cores",
            len(clustered) == 60, "%d cores" % len(clustered))
    p.note("clustered: 20 groups of 5, 100 transfers, g = %d, guarantee "
           "%d chunks = %.3f s" % (gc, needc, needc * CHUNK_SECONDS))
    p.check("its coverage guarantee is much worse than the pinned grid's",
            needc > 3 * need0,
            "%.3f s vs %.3f s" % (needc * CHUNK_SECONDS,
                                  need0 * CHUNK_SECONDS))

    sparse = grid(20, C_CHUNKS)
    gs, runs, needs = guarantee(sparse)
    p.note("twenty single-chunk windows: 60 transfers, g = %d, guarantee "
           "%d chunks = %.3f s" % (gs, needs, needs * CHUNK_SECONDS))
    p.check("twenty single-chunk windows degrade the guarantee too",
            needs > 3 * need0,
            "%.3f s" % (needs * CHUNK_SECONDS))

    # dilution: one loud chunk inside a three-chunk MAD window
    excursion = 3.0
    rng2 = np.random.default_rng(7)
    quiet = rng2.normal(0.0, 1.0, 2 * CHUNK)
    loud = rng2.normal(0.0, excursion, CHUNK)
    one_chunk = mad_sigma(loud)
    three_chunk = mad_sigma(np.concatenate([quiet[:CHUNK], loud,
                                            quiet[CHUNK:]]))
    p.note("a 3x excursion of one chunk reads %.4f in a one-chunk window and "
           "%.4f in a three-chunk window" % (one_chunk, three_chunk))
    p.check("aggregating three cores dilutes the excursion",
            three_chunk < 0.55 * one_chunk,
            "%.1f%% of the undiluted value"
            % (100.0 * three_chunk / one_chunk))
    p.check("the two defects are different: one is coverage, one is dilution",
            needc > need0 and three_chunk < one_chunk)
    p.records["t1"] = {
        "pinned": {"transfers": 180, "g": int(g0), "guarantee_chunks": int(need0),
                   "guarantee_s": float(need0 * CHUNK_SECONDS)},
        "clustered_five": {"transfers": 100, "g": int(gc),
                           "guarantee_chunks": int(needc),
                           "guarantee_s": float(needc * CHUNK_SECONDS)},
        "sparse_twenty": {"transfers": 60, "g": int(gs),
                          "guarantee_chunks": int(needs),
                          "guarantee_s": float(needs * CHUNK_SECONDS)},
        "dilution": {"excursion": excursion, "one_chunk": float(one_chunk),
                     "three_chunk": float(three_chunk),
                     "fraction_retained": float(three_chunk / one_chunk)}}

    # ------------------------------------------------------------------ T4 --
    p.heading("6. T4-R1  the phase-omission direction, and where it stops")
    n = 4000
    rng3 = np.random.default_rng(99)
    shared = rng3.normal(0.0, 4.0, n)
    private = rng3.normal(0.0, 3.0, (72, n))
    aligned = shared + private
    shifted = np.array([np.roll(shared, c % 8) for c in range(72)]) + private
    cmr_aligned = aligned - np.median(aligned, axis=0)
    cmr_shifted = shifted - np.median(shifted, axis=0)
    sig_aligned = np.array([mad_sigma(row) for row in cmr_aligned])
    sig_shifted = np.array([mad_sigma(row) for row in cmr_shifted])
    p.note("shared-component model: median sigma after CMR is %.4f aligned and "
           "%.4f with the phase shift left in"
           % (np.median(sig_aligned), np.median(sig_shifted)))
    p.check("leaving the shift in raises the level statistic",
            np.median(sig_shifted) > np.median(sig_aligned))
    p.check("under the shared-component model every channel rises",
            bool(np.all(sig_shifted > sig_aligned)),
            "%d of 72 channels rise" % int((sig_shifted > sig_aligned).sum()))
    r_aligned = spread(sig_aligned)
    r_shifted = spread(sig_shifted)
    p.check("the SPATIAL statistic does not inherit that direction",
            r_shifted < r_aligned,
            "R_space %.4f -> %.4f, the opposite way" % (r_aligned, r_shifted))
    p.note("so the direction is a claim about the level under one model, and "
           "not a claim about every statistic this section computes")
    p.records["t4"] = {
        "median_sigma_aligned": float(np.median(sig_aligned)),
        "median_sigma_shifted": float(np.median(sig_shifted)),
        "channels_rising": int((sig_shifted > sig_aligned).sum()),
        "r_space_aligned": float(r_aligned),
        "r_space_shifted": float(r_shifted)}

    p.heading("Summary")
    total = p.passed + p.failed
    line = "%d checks, %d failed" % (total, p.failed)
    p.lines.append(line)
    print(line)
    p.records["checks_total"] = total
    p.records["checks_failed"] = p.failed
    p.records["numpy_version"] = np.__version__
    p.records["scipy_version"] = __import__("scipy").__version__

    out = args.out if os.path.isabs(args.out) else os.path.join(root, args.out)
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        "\n".join(p.lines) + "\n")
    if args.records:
        rec = args.records if os.path.isabs(args.records) \
            else os.path.join(root, args.records)
        with io.open(rec, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(p.records, indent=2, sort_keys=True) + "\n")

    return 1 if p.failed else 0


if __name__ == "__main__":
    sys.exit(main())
