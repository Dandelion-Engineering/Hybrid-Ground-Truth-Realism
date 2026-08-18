"""Independently probe the RC-007 Draft-30 response boundary.

This is a delta-only reviewer probe.  It authenticates the submitted state,
checks the repaired level/verdict/grid rules, and constructs two response-
specific counterexamples:

* real neighbouring samples can move the isolated-window Butterworth result by
  much more than the owner's twelve-fixture ``1e-06`` figure, even when every
  value lies on the rank-1 int16 voltage lattice; and
* within-window non-stationarity can cancel rather than only inflate the
  split-half ratio spread.

No archive, network resource, or candidate sample is read.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


CANDIDATE_HASHES = {
    "agents/Claude/Tier A Host and Injection Zone Selection.md":
        "48de3825a6727962fb9e698669eddd2dead5ac5e21362bc90afc69fa69689964",
    "agents/Claude/tools/probe_filter_chain.py":
        "ef96ce2120677dc3e1e6ee236b845a962c200f7228ef68dc86b5a6602f3c74ee",
    "agents/Claude/tools/filter_chain_2026-08-18.txt":
        "dfcea89d463808b224355615491bdbfc6007ce6880208d3a16529fdbe4bbae23",
    "agents/Claude/tools/filter_chain_2026-08-18.json":
        "b9f3e089e2b94e2d9e26743133d167bb258e3be169b5ce3f1b3fe625c7b72b15",
    "agents/Claude/tools/probe_rc007_spec.py":
        "9380458b083aca6b6a04ad4c4b665f27532343185d04ca1dc216cc22e7a2facf",
    "agents/Claude/tools/probe_rc007_spec_2026-08-18_draft30.txt":
        "a6027b1a53b1eebe8ae3ee4f88a2a991c2528f5a265518ad82907219146808d9",
    "agents/Claude/tools/mutate_rc007_spec.py":
        "a194d59e81ff8c3eff7e338ac7654b312471a0c82ba257ef53e30e23f3fb4f1b",
    "agents/Claude/tools/mutate_rc007_spec_2026-08-18_draft30.txt":
        "9b5ca1647d8d309112a2423e820939c29c98c9fc1e9bb093072bacbecd82c963",
}

FROZEN_SPANS = (
    (b"## 1. ", b"## 17. ", 144_664,
     "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59"),
    (b"## 17. ", b"## 18. ", 21_864,
     "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a"),
    (b"## 18. ", b"## 19. ", 20_579,
     "8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017"),
)


def parse_args() -> argparse.Namespace:
    """Parse the required repository-root argument."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True,
                        help="Path to the Hybrid Ground Truth Realism repository root.")
    return parser.parse_args()


class Checks:
    """Collect named checks and print one deterministic summary."""

    def __init__(self) -> None:
        self.total = 0
        self.failed = 0

    def check(self, condition: bool, label: str) -> None:
        """Record one Boolean condition under ``label``."""
        self.total += 1
        if condition:
            print(f"[ok  ] {label}")
        else:
            self.failed += 1
            print(f"[FAIL] {label}")


def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_filter_probe(path: Path):
    """Load the authenticated owner filter probe as a module."""
    spec = importlib.util.spec_from_file_location("owner_filter_probe", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def nearest_rank(values: np.ndarray, probability: float) -> float:
    """Return the one-based nearest-rank percentile used by Draft 30."""
    ordered = np.sort(np.asarray(values, dtype=np.float64))
    rank = math.ceil(probability * ordered.size)
    return float(ordered[rank - 1])


def spread(values: np.ndarray) -> float:
    """Return Draft 30's p90/p10 nearest-rank spread."""
    return nearest_rank(values, 0.90) / nearest_rank(values, 0.10)


def isolation_error(module, seed: int) -> tuple[float, float, float]:
    """Measure isolated/context error on one valid int16-lattice construction.

    The centre chunk contains quantized 6-uV noise.  The preceding and
    following context are opposite 69,998.4375-uV plateaus, equal to 29,866
    stored counts at the measured 2.34375-uV conversion and therefore inside
    int16.  A single affected channel survives a 384-channel common median.
    """
    n = module.CHUNK_SAMPLES
    start = 4 * n
    stop = 5 * n
    margin = 500
    quantum_uv = 2.34375
    plateau_counts = 29_866
    plateau_uv = plateau_counts * quantum_uv
    rng = np.random.default_rng(seed)
    signal_uv = np.round(rng.normal(0.0, 6.0, 9 * n) / quantum_uv) * quantum_uv
    signal_uv[:start] = plateau_uv
    signal_uv[stop:] = -plateau_uv

    sos = module.butter_sos()
    contextual = module.butter_highpass(signal_uv - signal_uv.mean(), sos)
    contextual = contextual[start + margin:stop - margin]
    window = signal_uv[start:stop]
    isolated = module.butter_highpass(window - window.mean(), sos)[margin:-margin]
    sigma_context = float(module.mad_sigma(contextual))
    sigma_isolated = float(module.mad_sigma(isolated))
    relative = sigma_isolated / sigma_context - 1.0
    sample_error = float(np.max(np.abs(isolated - contextual)))
    return relative, sample_error, plateau_counts


def main() -> int:
    """Run the independent Draft-30 delta probes."""
    args = parse_args()
    root = Path(args.repo_root).resolve()
    checks = Checks()

    for relative, expected in CANDIDATE_HASHES.items():
        checks.check(sha256(root / relative) == expected,
                     f"candidate digest: {relative}")

    document_path = root / "agents/Claude/Tier A Host and Injection Zone Selection.md"
    document_bytes = document_path.read_bytes()
    document = document_bytes.decode("utf-8")
    section19 = document[document.index("## 19. "):]
    for start_marker, stop_marker, size, expected in FROZEN_SPANS:
        start = document_bytes.index(start_marker)
        stop = document_bytes.index(stop_marker, start + len(start_marker))
        span = document_bytes[start:stop]
        checks.check(len(span) == size, f"frozen span byte count {start_marker!r}")
        checks.check(hashlib.sha256(span).hexdigest() == expected,
                     f"frozen span digest {start_marker!r}")

    # F1/F2/F3/F5/F6 response-state assertions.
    checks.check("sigma_worst_sampled < 1.25 µV" in section19,
                 "F1 lower level floor reaches an ordered verdict branch")
    checks.check("10.0 → 25.0 µV" in section19,
                 "F1 relaxation restatement is 10.0 to 25.0")
    peak, trough, sigma = 30.0, -20.0, 1.0
    checks.check(max(abs(peak), abs(trough)) / sigma <= 40.0
                 and (peak - trough) / sigma > 40.0,
                 "F2 single-sided-pass / peak-to-peak-fail counterexample")
    branch_positions = [section19.index(label) for label in (
        "1. **Level, too loud.**",
        "2. **Level, too quiet.**",
        "3. **Homogeneity.**",
        "4. **Resolution.**",
    )]
    checks.check(branch_positions == sorted(branch_positions),
                 "F3 verdict branches are ordered")
    checks.check("Host admissibility is five gates" in section19
                 and "§15.5 is not superseded in any clause" in section19,
                 "F6 four-gate supersession is withdrawn")

    c_chunks = 9_999
    k_windows = 60
    grid = [math.floor(k * (c_chunks - 1) / (k_windows - 1) + 0.5)
            for k in range(k_windows)]
    max_gap = max(b - a for a, b in zip(grid, grid[1:]))
    checks.check(grid[0] == 0 and grid[-1] == c_chunks - 1 and max_gap == 170,
                 "F5 grid spans the extent with largest gap 170")
    grid_set = set(grid)
    coverage_holds = all(
        any(index in grid_set for index in range(start, start + max_gap + 1))
        for start in range(c_chunks - max_gap)
    )
    checks.check(coverage_holds,
                 "F5 every 171-consecutive-chunk run contains a sampled chunk")

    owner_filter = load_filter_probe(root / "agents/Claude/tools/probe_filter_chain.py")
    record = json.loads((root / "agents/Claude/tools/filter_chain_2026-08-18.json").read_text(
        encoding="utf-8"))
    owner_500 = [item for item in record["margin_study"]
                 if item["construction"] == "butterworth_sosfiltfilt"
                 and item["margin_samples"] == 500]
    checks.check(max(abs(item["worst_relative_sigma_error"]) for item in owner_500) < 2e-6,
                 "F4 owner fixtures reproduce the approximately 1e-06 figure")

    negative_error, negative_sample, counts_a = isolation_error(owner_filter, 24)
    positive_error, positive_sample, counts_b = isolation_error(owner_filter, 28)
    checks.check(counts_a == counts_b == 29_866 and counts_a < np.iinfo(np.int16).max,
                 "F4 counterexamples stay on the measured int16 voltage lattice")
    checks.check(negative_error < -0.002 and positive_error > 0.002,
                 "F4 real-neighbour context moves the scale in both directions by >0.2 percent")
    checks.check(max(negative_sample, positive_sample) > 0.5,
                 "F4 real-neighbour context changes retained samples by >0.5 uV")
    checks.check(max(abs(negative_error), abs(positive_error)) > 1_000 * 1e-6,
                 "F4 twelve-fixture 1e-06 result is not a general isolation bound")

    # F7 response counterexample.  Eight low, 56 middle and eight high channel
    # ratios put nearest-rank p10 at 0.5 and p90 at 2.0.  A true temporal-scale
    # change with reciprocal channel factors cancels those differences exactly.
    estimation_ratios = np.array([0.5] * 8 + [1.0] * 56 + [2.0] * 8)
    nonstationary_factors = np.array([2.0] * 8 + [1.0] * 56 + [0.5] * 8)
    before = spread(estimation_ratios)
    after = spread(estimation_ratios * nonstationary_factors)
    checks.check(before == 4.0 and after == 1.0,
                 "F7 within-window nonstationarity can deflate R_null from 4 to 1")
    checks.check("Non-stationarity can only add to the disagreement" in section19,
                 "F7 contradicted one-way claim is present in Draft 30")

    # The in-force contract has only per-donor/site effective-SNR gates.  The
    # response nevertheless calls an invented host-aggregate precondition
    # discharged.  Identical band medians do not determine site SNR.
    claim_sheet = (root / "Claim Sheet.md").read_text(encoding="utf-8")
    amendment6 = claim_sheet[claim_sheet.index("### Amendment 6"):]
    checks.check("per-donor hard host-specific eligibility gates" in amendment6
                 and "pins the finite candidate-site set" in amendment6,
                 "F6 contract remains per-donor and per-site")
    band_sigma = 6.0
    amplitude = 50.0
    quiet_site_snr = amplitude / 4.0
    loud_site_snr = amplitude / 12.0
    checks.check(1.25 <= band_sigma <= 10.0
                 and quiet_site_snr >= 5.0 and loud_site_snr < 5.0,
                 "F6 one passing band aggregate permits opposite site-level SNR verdicts")
    checks.check("Gate 3's host-aggregate precondition is discharged by gate 2" in section19,
                 "F6 surviving aggregate-discharge claim is present")

    print()
    print(f"{checks.total} checks, {checks.failed} failed")
    print(f"F4 isolation errors: seed24={negative_error:+.9f}, "
          f"seed28={positive_error:+.9f}; sample maxima "
          f"{negative_sample:.6f}/{positive_sample:.6f} uV")
    print(f"F7 spread: estimation-only={before:.6f}, with nonstationarity={after:.6f}")
    return 1 if checks.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
