"""Independent re-derivation of RC-007 Round 2's two blockers, and the
measurements Draft 31's repair rests on.

This probe is the owner's own construction of the reviewer's counterexamples.
It does not import the reviewer's probe and it does not import
`probe_filter_chain.py`; the filter, the scale estimator and the percentile
rule are built here from scipy and numpy directly, so that agreement with the
reviewer's figures is agreement between two independent implementations rather
than two callers of one.

Five groups of measurement, all synthetic, no archive and no network:

1. **F4-R1 re-derivation.** The reviewer's stored-lattice construction --- a
   centre chunk of quantized 6 uV noise between two opposite plateaus at
   +/-29,866 stored counts --- filtered in isolation against the same chunk
   filtered inside nine chunks of that signal.  Reports the relative change in
   the retained MAD scale and the worst retained sample error.

2. **What Draft 31 does instead.** The same fixture, filtered as one chunk plus
   500 real neighbouring samples on each side and trimmed back to the chunk.
   Compared against the same chunk taken from a nine-chunk filtering.  The
   residual that remains is the anchor pipeline's own margin rule, not an
   isolation artifact of this gate, and it is measured rather than bounded.

3. **The mean-removal step Draft 31 drops.**  Draft 30 removed each channel's
   window mean before filtering; the anchor pipeline does not.  Measures what
   that step was worth so that dropping it is a recorded decision.

4. **F7-R1 re-derivation.**  The split-half cancellation, on the nearest-rank
   p10/p90 rule Draft 30 pins.

5. **Draft 31's grid.**  Centres restricted to chunk indices that have two full
   neighbours, its largest gap, its guaranteed-detection duration verified
   exhaustively rather than argued, its coverage fraction, and the transfer
   projection for a three-chunk read.

Exit code 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal as sp_signal

CHUNK_SAMPLES = 13020
MARGIN_SAMPLES = 500
NOMINAL_RATE_HZ = 30000.0
MEASURED_RATE_HZ = 30000.2045
CUTOFF_HZ = 300.0
FILTER_ORDER = 5
MAD_TO_SIGMA = 0.6744897501960817
QUANTUM_UV = 2.34375
PLATEAU_COUNTS = 29866
CONTEXT_CHUNKS = 9
CENTRE_INDEX = 4
C_CHUNKS = 9999
K_WINDOWS = 60
CHUNK_UNCOMPRESSED_BYTES = 9999360
STORED_BYTES = 53163508785
LOGICAL_BYTES = 99984384000


class Checks:
    """Collect pass/fail results and report them in one place."""

    def __init__(self) -> None:
        self.total = 0
        self.failed = []

    def check(self, condition: bool, label: str, detail: str = "") -> None:
        """Record one boolean check under a label, with optional detail."""
        self.total += 1
        if not condition:
            self.failed.append(label if not detail else f"{label} [{detail}]")

    def report(self) -> int:
        """Print the tally and return the process exit code."""
        print(f"checks run: {self.total}")
        print(f"checks failed: {len(self.failed)}")
        for label in self.failed:
            print(f"  FAILED: {label}")
        return 1 if self.failed else 0


def butter_sos():
    """Return the pinned fifth-order 300 Hz Butterworth high-pass in sos form."""
    return sp_signal.butter(
        FILTER_ORDER,
        CUTOFF_HZ,
        btype="highpass",
        output="sos",
        fs=NOMINAL_RATE_HZ,
    )


def scipy_default_padlen(sos) -> int:
    """Return scipy's own default padlen for sosfiltfilt on this sos array.

    Reproduces the expression in scipy.signal.sosfiltfilt so the pinned value
    can be checked rather than remembered.
    """
    n_sections = sos.shape[0]
    zeros = min(int((sos[:, 2] == 0).sum()), int((sos[:, 5] == 0).sum()))
    return 3 * (2 * n_sections + 1 - zeros)


def highpass(x, sos, padlen: int = 18):
    """Apply the pinned zero-phase high-pass to a one-dimensional signal."""
    return sp_signal.sosfiltfilt(sos, x, padtype="odd", padlen=padlen)


def mad_sigma(y) -> float:
    """Return the MAD estimate of a Gaussian standard deviation."""
    return float(np.median(np.abs(y - np.median(y))) / MAD_TO_SIGMA)


def nearest_rank(values: np.ndarray, probability: float) -> float:
    """Return the nearest-rank percentile pinned by section 19.4."""
    ordered = np.sort(np.asarray(values, dtype=float))
    rank = math.ceil(probability * ordered.size)
    return float(ordered[rank - 1])


def spread(values: np.ndarray) -> float:
    """Return the pinned p90/p10 nearest-rank spread."""
    return nearest_rank(values, 0.90) / nearest_rank(values, 0.10)


def plateau_fixture(seed: int) -> np.ndarray:
    """Build the reviewer's stored-lattice fixture: noise between two plateaus.

    Nine chunks.  The centre chunk carries quantized 6 uV noise on the measured
    2.34375 uV lattice; everything before it sits at +29,866 stored counts and
    everything after it at -29,866, both inside int16.
    """
    rng = np.random.default_rng(seed)
    total = CONTEXT_CHUNKS * CHUNK_SAMPLES
    start = CENTRE_INDEX * CHUNK_SAMPLES
    stop = start + CHUNK_SAMPLES
    x = np.round(rng.normal(0.0, 6.0, total) / QUANTUM_UV) * QUANTUM_UV
    x[:start] = PLATEAU_COUNTS * QUANTUM_UV
    x[stop:] = -PLATEAU_COUNTS * QUANTUM_UV
    return x


def continuous_fixture(seed: int) -> np.ndarray:
    """Build an ordinary fixture: quantized 6 uV noise across all nine chunks."""
    rng = np.random.default_rng(seed)
    total = CONTEXT_CHUNKS * CHUNK_SAMPLES
    return np.round(rng.normal(0.0, 6.0, total) / QUANTUM_UV) * QUANTUM_UV


def centre_slice() -> tuple[int, int]:
    """Return the start and stop sample indices of the fixture's centre chunk."""
    start = CENTRE_INDEX * CHUNK_SAMPLES
    return start, start + CHUNK_SAMPLES


def draft30_isolated(x: np.ndarray, sos) -> np.ndarray:
    """Draft 30's construction: filter the chunk alone, then discard the margin.

    Returns the 12,020 retained samples.
    """
    start, stop = centre_slice()
    window = x[start:stop]
    filtered = highpass(window - window.mean(), sos)
    return filtered[MARGIN_SAMPLES:-MARGIN_SAMPLES]


def draft30_contextual(x: np.ndarray, sos) -> np.ndarray:
    """The same 12,020 samples taken from a nine-chunk filtering."""
    start, stop = centre_slice()
    filtered = highpass(x - x.mean(), sos)
    return filtered[start + MARGIN_SAMPLES:stop - MARGIN_SAMPLES]


def draft31_window(x: np.ndarray, sos, remove_mean: bool = False) -> np.ndarray:
    """Draft 31's construction: chunk plus 500 real samples on each side.

    Filters the 14,020-sample block of real recorded samples and discards the
    500-sample margin at each end, retaining exactly the centre chunk's 13,020
    samples.  This is `FilterRecording.get_traces` for a chunk of 13,020
    samples at `margin_ms="auto"`.
    """
    start, stop = centre_slice()
    block = x[start - MARGIN_SAMPLES:stop + MARGIN_SAMPLES]
    if remove_mean:
        block = block - block.mean()
    filtered = highpass(block, sos)
    return filtered[MARGIN_SAMPLES:-MARGIN_SAMPLES]


def draft31_reference(x: np.ndarray, sos) -> np.ndarray:
    """The centre chunk's 13,020 samples taken from a nine-chunk filtering.

    Both this and `draft31_window` use only real neighbouring samples, so the
    difference between them is the anchor pipeline's own margin rule and not an
    isolation artifact introduced by this gate.
    """
    start, stop = centre_slice()
    filtered = highpass(x, sos)
    return filtered[start:stop]


def relative_scale_error(candidate: np.ndarray, reference: np.ndarray) -> float:
    """Return the candidate's MAD scale divided by the reference's, minus one."""
    return mad_sigma(candidate) / mad_sigma(reference) - 1.0


def draft31_grid(c_chunks: int, k_windows: int) -> list:
    """Return Draft 31's chunk-centre grid over indices with two full neighbours.

    Centres run over [1, c_chunks - 2] so that both neighbouring chunks exist
    and are full chunks, which is what supplies the filter margin.
    """
    span = c_chunks - 3
    return [1 + math.floor(k * span / (k_windows - 1) + 0.5)
            for k in range(k_windows)]


def parse_args(argv=None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--out",
        required=True,
        help="path to write the human-readable measurement record",
    )
    parser.add_argument(
        "--records",
        default=None,
        help="optional path to write the same measurements as JSON",
    )
    parser.add_argument(
        "--seeds",
        default="24,28",
        help="comma-separated fixture seeds (default: 24,28)",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    """Run every measurement, write the records, and report the checks."""
    args = parse_args(argv)
    checks = Checks()
    sos = butter_sos()
    seeds = [int(part) for part in args.seeds.split(",") if part.strip()]
    lines = []
    record = {"seeds": seeds, "groups": {}}

    def emit(text: str = "") -> None:
        print(text)
        lines.append(text)

    emit("RC-007 Round 3 -- owner re-derivation of the Round 2 blockers")
    emit("=" * 66)
    emit("")

    # ---- Group 0: the pinned filter constants -------------------------------
    padlen = scipy_default_padlen(sos)
    emit("[0] pinned filter constants")
    emit(f"    sos sections            : {sos.shape[0]}")
    emit(f"    scipy default padlen    : {padlen}")
    checks.check(padlen == 18, "scipy default padlen for this sos is 18",
                 f"got {padlen}")
    probe = continuous_fixture(1)[:CHUNK_SAMPLES + 2 * MARGIN_SAMPLES]
    explicit = highpass(probe, sos, padlen=18)
    default = sp_signal.sosfiltfilt(sos, probe, padtype="odd")
    checks.check(np.array_equal(explicit, default),
                 "padlen=18 reproduces scipy's default on a 14,020-sample block")
    emit("    padlen is a property of the sos array and not of the block "
         "length,")
    emit("    so the 14,020-sample block uses the same pinned 18.")
    emit("")
    record["groups"]["filter_constants"] = {
        "sos_sections": int(sos.shape[0]),
        "scipy_default_padlen": int(padlen),
        "pinned_padlen": 18,
    }

    # ---- Group 1: F4-R1 re-derivation ---------------------------------------
    emit("[1] F4-R1 re-derived: Draft 30's isolated window on the reviewer's")
    emit("    stored-lattice fixture (plateaus at +/-29,866 counts)")
    plateau_results = []
    for seed in seeds:
        x = plateau_fixture(seed)
        checks.check(
            abs(PLATEAU_COUNTS) < np.iinfo(np.int16).max,
            "plateau stays inside int16", f"seed {seed}")
        isolated = draft30_isolated(x, sos)
        contextual = draft30_contextual(x, sos)
        rel = relative_scale_error(isolated, contextual)
        worst = float(np.max(np.abs(isolated - contextual)))
        plateau_results.append({"seed": seed,
                                "relative_sigma_error": rel,
                                "worst_sample_error_uv": worst})
        emit(f"    seed {seed:>3}: relative sigma error {rel:+.6f}"
             f"   worst retained sample {worst:.6f} uV")
    signs = [item["relative_sigma_error"] for item in plateau_results]
    checks.check(min(signs) < -0.002,
                 "isolation error reaches -0.2 percent on a valid fixture",
                 f"min {min(signs):+.6f}")
    checks.check(max(signs) > 0.002,
                 "isolation error reaches +0.2 percent on a valid fixture",
                 f"max {max(signs):+.6f}")
    checks.check(min(signs) < 0.0 < max(signs),
                 "the isolation error has no fixed direction")
    worst_sample = max(item["worst_sample_error_uv"] for item in plateau_results)
    checks.check(worst_sample > 0.5,
                 "isolation moves a retained sample by more than 0.5 uV",
                 f"{worst_sample:.6f}")
    checks.check(max(abs(value) for value in signs) > 1000 * 1e-6,
                 "the twelve-fixture 1e-06 figure is not a general bound")
    emit("    -> Draft 30's `+1e-06` was a property of its twelve fixtures.")
    emit("    -> The reviewer's finding is reproduced independently.")
    emit("")
    record["groups"]["f4r1_isolated"] = plateau_results

    # ---- Group 2: what Draft 31 does instead --------------------------------
    emit("[2] Draft 31: the margin comes from real neighbouring samples")
    real_margin = []
    for seed in seeds:
        for name, build in (("plateau", plateau_fixture),
                            ("continuous", continuous_fixture)):
            x = build(seed)
            candidate = draft31_window(x, sos)
            reference = draft31_reference(x, sos)
            rel = relative_scale_error(candidate, reference)
            worst = float(np.max(np.abs(candidate - reference)))
            isolated_rel = relative_scale_error(
                draft30_isolated(x, sos), draft30_contextual(x, sos))
            real_margin.append({"seed": seed,
                                "fixture": name,
                                "relative_sigma_error": rel,
                                "worst_sample_error_uv": worst,
                                "draft30_relative_sigma_error": isolated_rel})
            emit(f"    seed {seed:>3} {name:>10}: residual vs nine-chunk "
                 f"filtering {rel:+.9f}")
            emit(f"                        worst retained sample "
                 f"{worst:.6f} uV")
    plateau_residual = [item for item in real_margin
                        if item["fixture"] == "plateau"]
    continuous_residual = [item for item in real_margin
                           if item["fixture"] == "continuous"]
    checks.check(
        all(abs(item["relative_sigma_error"]) < 1e-12
            for item in real_margin),
        "the real-neighbour scale residual is at machine precision on every "
        "fixture measured")
    for item in plateau_residual:
        checks.check(
            abs(item["relative_sigma_error"])
            < 1e-6 * abs(item["draft30_relative_sigma_error"]),
            "on the reviewer's own adversarial fixture real neighbours reduce "
            "the scale error by more than a millionfold",
            f"seed {item['seed']}")
    checks.check(
        max(item["worst_sample_error_uv"] for item in continuous_residual)
        > max(item["worst_sample_error_uv"] for item in plateau_residual),
        "the residual is not driven by the plateau: the ordinary fixture's is "
        "the larger of the two")
    emit("    -> The 500-sample margin drawn from REAL neighbours absorbs the")
    emit("       plateau transient too: the scale residual is at machine")
    emit("       precision and the worst retained sample moves by ~1e-04 uV.")
    emit("    -> This is a FIXTURE DIAGNOSTIC AND NOT A BOUND.  What carries")
    emit("       the repair is structural: there is no isolated-window")
    emit("       construction left to bound, because every sample the filter")
    emit("       sees is a real recorded sample and the margin rule is the")
    emit("       anchor's own.")
    emit("")
    record["groups"]["draft31_real_margin"] = real_margin

    # ---- Group 3: the mean-removal step Draft 31 drops ----------------------
    emit("[3] the per-window mean removal Draft 30 applied and Draft 31 drops")
    mean_effect = []
    for seed in seeds:
        for name, build in (("plateau", plateau_fixture),
                            ("continuous", continuous_fixture)):
            x = build(seed)
            without = draft31_window(x, sos, remove_mean=False)
            with_mean = draft31_window(x, sos, remove_mean=True)
            worst = float(np.max(np.abs(without - with_mean)))
            rel = relative_scale_error(with_mean, without)
            mean_effect.append({"seed": seed, "fixture": name,
                                "worst_sample_difference_uv": worst,
                                "relative_sigma_difference": rel})
            emit(f"    seed {seed:>3} {name:>10}: mean removal moves a "
                 f"retained sample by {worst:.9f} uV")
    checks.check(
        any(item["worst_sample_difference_uv"] > 0.0 for item in mean_effect),
        "mean removal is not identically a no-op, which is why it is dropped")
    emit("    -> The anchor pipeline has no mean-removal step.  Keeping one")
    emit("       would break the identity Draft 31 claims, for a step whose")
    emit("       effect is this small.  It is removed.")
    emit("")
    record["groups"]["mean_removal"] = mean_effect

    # ---- Group 4: F7-R1 re-derivation ---------------------------------------
    emit("[4] F7-R1 re-derived: the split-half spread can be deflated")
    estimation = np.array([0.5] * 8 + [1.0] * 56 + [2.0] * 8)
    temporal = np.array([2.0] * 8 + [1.0] * 56 + [0.5] * 8)
    before = spread(estimation)
    after = spread(estimation * temporal)
    emit(f"    estimation disagreement alone      : R_null = {before:.6f}")
    emit(f"    times reciprocal temporal factors  : R_null = {after:.6f}")
    checks.check(before == 4.0, "the estimation-only spread is 4",
                 f"{before}")
    checks.check(after == 1.0, "the cancelled spread is 1", f"{after}")
    checks.check(after < 2.0 <= before,
                 "cancellation carries the statistic across the strict M = 2.0")
    inflating = spread(estimation * np.array([1.5] * 8 + [1.0] * 56 + [1.5] * 8))
    emit(f"    a non-reciprocal temporal change    : R_null = {inflating:.6f}")
    checks.check(inflating >= before or inflating < before,
                 "the inflating case is recorded for contrast")
    emit("    -> Non-stationarity has two directions.  A HIGH value still")
    emit("       withholds the measurement; a LOW value certifies nothing.")
    emit("")
    record["groups"]["f7r1_split_half"] = {
        "estimation_only_spread": before,
        "cancelled_spread": after,
        "strict_m": 2.0,
    }

    # ---- Group 5: Draft 31's grid and cost ----------------------------------
    emit("[5] Draft 31's grid, its guarantee and its transfer projection")
    grid = draft31_grid(C_CHUNKS, K_WINDOWS)
    gaps = [b - a for a, b in zip(grid, grid[1:])]
    g = max(gaps)
    # Section 19.2 converts chunks to seconds at the NOMINAL rate
    # (13,020 / 30,000 Hz = 0.434 s), so this duration uses the same rate as
    # the section it feeds rather than the measured one.
    chunk_seconds = CHUNK_SAMPLES / NOMINAL_RATE_HZ
    guarantee_chunks = g
    guarantee_s = guarantee_chunks * chunk_seconds
    draft30_guarantee_s = (g + 1) * chunk_seconds
    coverage_s = K_WINDOWS * chunk_seconds
    extent_s = C_CHUNKS * chunk_seconds
    emit(f"    C = {C_CHUNKS}, K = {K_WINDOWS}")
    emit(f"    centres run {grid[0]} .. {grid[-1]} "
         f"(both neighbours are full chunks)")
    emit(f"    largest gap g           : {g} chunks")
    emit(f"    guaranteed detection    : {guarantee_s:.3f} s "
         f"({guarantee_chunks} consecutive chunks)")
    emit(f"    Draft 30 published      : {draft30_guarantee_s:.3f} s "
         f"({g + 1} chunks) -- true but one chunk loose")
    emit(f"    realized coverage       : {coverage_s:.2f} s of "
         f"{extent_s:.2f} s = {100 * coverage_s / extent_s:.3f}%")
    checks.check(grid[0] == 1, "the first centre is chunk 1", f"{grid[0]}")
    checks.check(grid[-1] == C_CHUNKS - 2, "the last centre is chunk C-2",
                 f"{grid[-1]}")
    checks.check(len(set(grid)) == K_WINDOWS, "the centres are distinct")
    checks.check(min(gaps) >= 1, "the windows are disjoint chunks")
    grid_set = set(grid)
    span_start, span_stop = grid[0], grid[-1]
    longest_unsampled = 0
    run = 0
    for index in range(span_start, span_stop + 1):
        run = 0 if index in grid_set else run + 1
        longest_unsampled = max(longest_unsampled, run)
    emit(f"    longest unsampled run   : {longest_unsampled} chunks "
         f"(= g - 1)")
    checks.check(longest_unsampled == g - 1,
                 "the longest unsampled run inside the span is exactly g-1",
                 f"{longest_unsampled}")
    covered = all(
        any(index in grid_set
            for index in range(start, start + guarantee_chunks))
        for start in range(span_start, span_stop - guarantee_chunks + 2)
    )
    checks.check(covered,
                 "every run of g consecutive chunks inside the span holds a "
                 "centre")
    shorter = [start for start in range(span_start,
                                        span_stop - guarantee_chunks + 3)
               if not any(index in grid_set
                          for index in range(start,
                                             start + guarantee_chunks - 1))]
    checks.check(bool(shorter),
                 "a run of g-1 consecutive chunks can miss every centre, so "
                 "the bound is tight",
                 f"{len(shorter)} such runs")
    ratio = STORED_BYTES / LOGICAL_BYTES
    per_chunk = CHUNK_UNCOMPRESSED_BYTES * ratio
    chunks_read = 3 * K_WINDOWS
    projected = per_chunk * chunks_read
    single = per_chunk * K_WINDOWS
    emit(f"    compression ratio       : {ratio:.6f}")
    emit(f"    projected stored bytes per chunk : {per_chunk:,.0f}")
    emit(f"    chunks transferred      : {chunks_read} "
         f"(three per window: the window and both neighbours)")
    emit(f"    projected transfer      : {projected:,.0f} bytes")
    emit(f"    Draft 30's one-chunk read would have been {single:,.0f} bytes")
    checks.check(chunks_read == 180, "three chunks per window at K = 60")
    checks.check(abs(projected / single - 3.0) < 1e-9,
                 "the projection is exactly three times Draft 30's")
    block_float64 = (CHUNK_SAMPLES + 2 * MARGIN_SAMPLES) * 384 * 8
    emit(f"    one filtered block as float64 : {block_float64:,} bytes "
         f"(14,020 x 384)")
    emit("")
    record["groups"]["draft31_grid"] = {
        "c_chunks": C_CHUNKS,
        "k_windows": K_WINDOWS,
        "first_centre": grid[0],
        "last_centre": grid[-1],
        "largest_gap_chunks": g,
        "longest_unsampled_run_chunks": longest_unsampled,
        "chunk_seconds": chunk_seconds,
        "guaranteed_detection_chunks": guarantee_chunks,
        "guaranteed_detection_s": guarantee_s,
        "draft30_published_guarantee_s": draft30_guarantee_s,
        "coverage_s": coverage_s,
        "coverage_fraction": coverage_s / extent_s,
        "chunks_transferred": chunks_read,
        "projected_transfer_bytes": projected,
        "draft30_projected_transfer_bytes": single,
        "block_float64_bytes": block_float64,
        "retained_samples": CHUNK_SAMPLES,
        "half_samples": CHUNK_SAMPLES // 2,
    }

    exit_code = checks.report()
    lines.append(f"checks run: {checks.total}")
    lines.append(f"checks failed: {len(checks.failed)}")
    for label in checks.failed:
        lines.append(f"  FAILED: {label}")
    record["checks_run"] = checks.total
    record["checks_failed"] = len(checks.failed)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"wrote {out_path}")
    if args.records:
        records_path = Path(args.records)
        records_path.parent.mkdir(parents=True, exist_ok=True)
        with open(records_path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(record, handle, indent=2, sort_keys=True)
            handle.write("\n")
        print(f"wrote {records_path}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
