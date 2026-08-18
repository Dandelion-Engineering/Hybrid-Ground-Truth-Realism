"""Authenticate RC-008 Draft 32 and reproduce five Round-1 counterexamples.

Inputs:
    --repo-root: repository root containing the six-file RC-008 candidate.
    --out: optional path for the deterministic human-readable evidence record.

Outputs:
    Prints and optionally writes exact-state checks plus five blocking
    counterexamples. Exits non-zero if any reproduction fails.

Purpose:
    Provide independent reviewer evidence for RC-008 Round 1. The probe reads
    no archive sample, candidate noise value, or network resource and performs
    no heavy computation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from scipy import signal


SELECTION = "agents/Claude/Tier A Host and Injection Zone Selection.md"
RC008_PROBE = "agents/Claude/tools/probe_rc008_spec.py"
TIMING_INDEX = "Reproducibility Packet/results/host_timing_index.jsonl"

CANDIDATE_HASHES = {
    SELECTION:
        "6933c89ec561a7a9bc3201ea332ed7a6698f179af65cde49621cb0fddaec0db7",
    RC008_PROBE:
        "885e8d2d0bbf003428df0aab735ddcb99e2085c307a3a4cf1fcd81a6c4801de4",
    "agents/Claude/tools/rc008_spec_2026-08-18_draft32.txt":
        "a503957da231f7ea0d606cc65b098c6f3d099c746d19e52ea7fabdae06d6b4d4",
    "agents/Claude/tools/rc008_spec_2026-08-18_draft32.json":
        "2342ff9469dfb8b60b65db788368723c6432141494a96f481c8c8a7e0c9d00d5",
    "agents/Claude/tools/mutate_rc008_spec.py":
        "72628d4bc80e94ed6b2744b5ec5dbd2444093d49bbca07fbc3ba92a31b858829",
    "agents/Claude/tools/mutate_rc008_spec_2026-08-18_draft32.txt":
        "c5acce90f29d462def7b23461ab8c7f1e3c2dc21fe34840bd267b338c443bc1f",
}

FROZEN_SPANS = (
    (b"## 1. ", b"## 17. ", 144_664,
     "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59"),
    (b"## 17. ", b"## 18. ", 21_864,
     "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a"),
    (b"## 18. ", b"## 19. ", 20_579,
     "8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017"),
)

EXPECTED_LEGACY_FAILURES = (
    "section states R_null is one-sided",
    "section states the refused interleaved split",
    "section restates 73.780 exactly 7 times",
    "section restates 6,510 exactly 6 times",
    "section restates 13,020 exactly 14 times",
    "section restates 957,031,364 exactly 2 times",
)


class Checks:
    """Collect deterministic pass/fail checks and render one evidence record."""

    def __init__(self) -> None:
        self.lines: list[str] = []
        self.total = 0
        self.failed = 0

    def check(self, condition: bool, label: str, detail: str = "") -> None:
        """Record one condition with an optional failure detail."""
        self.total += 1
        if condition:
            self.lines.append(f"[ok  ] {label}")
        else:
            self.failed += 1
            suffix = f": {detail}" if detail else ""
            self.lines.append(f"[FAIL] {label}{suffix}")

    def note(self, message: str = "") -> None:
        """Append a non-check line to the evidence record."""
        self.lines.append(message)

    def render(self) -> str:
        """Return the complete evidence record as LF-only text."""
        return "\n".join(self.lines) + "\n"


def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique_span(data: bytes, start: bytes, end: bytes) -> bytes:
    """Return bytes between unique ordered anchors."""
    start_line = b"\n" + start
    end_line = b"\n" + end
    if data.count(start_line) != 1 or data.count(end_line) != 1:
        raise ValueError(f"non-unique line anchors: {start!r} -> {end!r}")
    left = data.index(start_line) + 1
    right = data.index(end_line) + 1
    if right <= left:
        raise ValueError(f"out-of-order span anchors: {start!r} -> {end!r}")
    return data[left:right]


def rank_spread(values: np.ndarray) -> float:
    """Return the nearest-rank p90/p10 spread for one channel vector."""
    ordered = np.sort(np.asarray(values, dtype=np.float64))
    p10 = ordered[math.ceil(0.10 * ordered.size) - 1]
    p90 = ordered[math.ceil(0.90 * ordered.size) - 1]
    if p10 == 0.0:
        return math.inf
    return float(p90 / p10)


def mad_sigma(values: np.ndarray, axis: int) -> np.ndarray:
    """Return Draft 32's robust scale along one axis."""
    med = np.median(values, axis=axis, keepdims=True)
    return np.median(np.abs(values - med), axis=axis) / 0.6744897501960817


def split_spread(values: np.ndarray, first: np.ndarray, second: np.ndarray) -> float:
    """Return the cross-channel spread of two split-specific scale estimates."""
    sigma_a = mad_sigma(values[:, first], axis=1)
    sigma_b = mad_sigma(values[:, second], axis=1)
    ratios = np.divide(
        sigma_a,
        sigma_b,
        out=np.full_like(sigma_a, np.inf),
        where=sigma_b != 0.0,
    )
    return rank_spread(ratios)


def rank1_rate(repo_root: Path) -> float:
    """Read rank 1 Probe01's measured AP rate from the pinned timing index."""
    first = json.loads((repo_root / TIMING_INDEX).read_text(encoding="utf-8").splitlines()[0])
    for series in first["series"]:
        if series["name"] == "ElectricalSeriesProbe01AP":
            return float(series["rate_hz"])
    raise ValueError("rank-1 Probe01 AP series is absent from the timing index")


def counterfeit_baseline_result(repo_root: Path) -> subprocess.CompletedProcess[str]:
    """Run the RC-008 checker against a changed K and a counterfeit RC-007 checker."""
    selection = (repo_root / SELECTION).read_text(encoding="utf-8")
    old = "| windows | `K = 60`, at chunk indices"
    new = "| windows | `K = 61`, at chunk indices"
    if selection.count(old) != 1:
        raise ValueError(f"K-table mutation anchor matched {selection.count(old)} times")
    changed = selection.replace(old, new, 1)

    fake_lines = [f"[FAIL] {name} -- counterfeit baseline" for name in EXPECTED_LEGACY_FAILURES]
    fake_lines.append("288 checks, 6 failed")
    fake_source = "\n".join([
        "import sys",
        f"LINES = {fake_lines!r}",
        "print('\\n'.join(LINES))",
        "sys.exit(0)",
        "",
    ])

    with tempfile.TemporaryDirectory(prefix="rc008_codex_counterfeit_") as temp:
        root = Path(temp)
        for relative in (SELECTION, RC008_PROBE):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if relative == SELECTION:
                target.write_text(changed, encoding="utf-8", newline="\n")
            else:
                shutil.copy2(repo_root / relative, target)
        fake = root / "agents/Claude/tools/probe_rc007_spec.py"
        fake.write_text(fake_source, encoding="utf-8", newline="\n")
        return subprocess.run(
            [sys.executable, str(root / RC008_PROBE), "--repo-root", str(root)],
            capture_output=True,
            text=True,
            check=False,
        )


def run(repo_root: Path, out_path: Path | None) -> int:
    """Run all authentication and counterexample checks."""
    checks = Checks()
    checks.note("RC-008 Round 1 -- independent reviewer probe")
    checks.note("=" * 51)
    checks.note()

    for relative, expected in CANDIDATE_HASHES.items():
        actual = sha256(repo_root / relative)
        checks.check(actual == expected, f"candidate digest: {relative}", actual)

    selection_bytes = (repo_root / SELECTION).read_bytes()
    selection_text = selection_bytes.decode("utf-8")
    for start, end, expected_bytes, expected_hash in FROZEN_SPANS:
        span = unique_span(selection_bytes, start, end)
        checks.check(len(span) == expected_bytes,
                     f"frozen bytes: {start.decode().strip()}", str(len(span)))
        checks.check(hashlib.sha256(span).hexdigest() == expected_hash,
                     f"frozen digest: {start.decode().strip()}")

    owner = subprocess.run(
        [sys.executable, str(repo_root / RC008_PROBE), "--repo-root", str(repo_root)],
        capture_output=True,
        text=True,
        check=False,
    )
    checks.check(owner.returncode == 0, "owner RC-008 checker exits zero", str(owner.returncode))
    checks.check("57 checks, 0 failed" in owner.stdout,
                 "owner RC-008 checker reproduces 57/57")

    checks.note()
    checks.note("[1] The loudest-window statistic cannot enforce the lower floor")
    sampled_levels = np.array([1.0] * 59 + [5.0])
    sigma_worst_sampled = float(np.max(sampled_levels))
    current_level_pass = 1.25 <= sigma_worst_sampled <= 10.0
    checks.check(current_level_pass,
                 "the current strict level branch passes the fixture")
    checks.check(float(np.min(sampled_levels)) < 1.25,
                 "59 sampled windows violate the declared lower floor")
    checks.check(50.0 / float(np.min(sampled_levels)) > 40.0,
                 "the quiet windows violate the anti-saturation condition")
    checks.note(f"  sigma_worst_sampled: {sigma_worst_sampled:.1f} uV")
    checks.note(f"  sigma_quietest_sampled: {float(np.min(sampled_levels)):.1f} uV")
    checks.note("  quiet-window snr_p2p at A_min=50 uV: 50.0")

    checks.note()
    checks.note("[2] Exact FilterRecording identity does not survive the nominal-rate pin")
    measured_rate = rank1_rate(repo_root)
    checks.check(measured_rate != 30_000.0,
                 "rank-1 measured AP rate is not nominal 30 kHz",
                 f"{measured_rate:.12f} Hz")
    nominal_sos = signal.butter(5, 300.0, btype="highpass", fs=30_000.0, output="sos")
    measured_sos = signal.butter(5, 300.0, btype="highpass", fs=measured_rate, output="sos")
    checks.check(not np.array_equal(nominal_sos, measured_sos),
                 "nominal-rate and recording-rate filter coefficients differ")
    rng = np.random.default_rng(8_083_002)
    raw = rng.integers(-32, 33, size=(14_020, 4), dtype=np.int16).astype(np.float64)
    raw *= 2.34375
    nominal = signal.sosfiltfilt(nominal_sos, raw, axis=0, padtype="odd", padlen=18)
    measured = signal.sosfiltfilt(measured_sos, raw, axis=0, padtype="odd", padlen=18)
    retained_difference = float(np.max(np.abs(nominal[500:-500] - measured[500:-500])))
    checks.check(retained_difference > 0.0,
                 "the two operators give different retained samples",
                 f"max abs difference {retained_difference:.12g} uV")
    checks.check("designed at the nominal 30,000 Hz" in selection_text,
                 "Draft 32 declares the nominal-rate design")
    checks.check("it is `FilterRecording.get_traces`" in selection_text,
                 "Draft 32 also publishes exact FilterRecording identity")
    checks.note(f"  measured rate: {measured_rate:.12f} Hz")
    checks.note(
        "  maximum coefficient difference: "
        f"{float(np.max(np.abs(nominal_sos - measured_sos))):.12g}"
    )
    checks.note(f"  maximum retained-sample difference: {retained_difference:.12g} uV")

    checks.note()
    checks.note("[3] Interleaving need not compress the split spread")
    pattern = np.array([-1.0, -1.0, 0.0, 0.0, 1.0, 1.0])
    base = np.tile(pattern, 13_020 // pattern.size)
    values = np.tile(base, (72, 1))
    even = np.arange(0, 13_020, 2)
    odd = np.arange(1, 13_020, 2)
    values[:8, even] *= 2.0
    values[64:, odd] *= 2.0
    first_half = np.arange(0, 6_510)
    second_half = np.arange(6_510, 13_020)
    contiguous = split_spread(values, first_half, second_half)
    interleaved = split_spread(values, even, odd)
    checks.check(contiguous == 1.0,
                 "periodic in-band construction gives contiguous spread 1", str(contiguous))
    checks.check(interleaved == 4.0,
                 "the same construction gives interleaved spread 4", str(interleaved))
    checks.check(interleaved > contiguous,
                 "interleaving expands rather than compresses this spread")
    checks.note(f"  contiguous R_null construction: {contiguous:.1f}")
    checks.note(f"  interleaved R_null construction: {interleaved:.1f}")

    checks.note()
    checks.note("[4] The regression baseline can be counterfeited")
    counterfeit = counterfeit_baseline_result(repo_root)
    checks.check(counterfeit.returncode == 0,
                 "RC-008 checker accepts counterfeit legacy checker plus K=61",
                 f"exit {counterfeit.returncode}")
    checks.check("57 checks, 0 failed" in counterfeit.stdout,
                 "counterfeit construction still reports 57/57")
    checks.check("61" not in "".join(
        line for line in counterfeit.stdout.splitlines() if line.startswith("FAIL")),
        "no direct RC-008 failure names the changed K")
    checks.note("  changed property: parameter-table K = 60 -> 61")
    checks.note("  counterfeit legacy process exit: 0")

    checks.note()
    checks.note("[5] An extreme bad channel need not inflate R_space")
    healthy = np.array([1.0] * 8 + [2.0] * 56 + [3.0] * 8)
    corrupted = healthy.copy()
    corrupted[0] = 100.0
    healthy_spread = rank_spread(healthy)
    corrupted_spread = rank_spread(corrupted)
    checks.check(healthy_spread == 3.0,
                 "clean 72-channel fixture fails strict M=2", str(healthy_spread))
    checks.check(corrupted_spread == 1.5,
                 "one extreme-high replacement passes strict M=2",
                 str(corrupted_spread))
    checks.check(corrupted_spread < healthy_spread,
                 "the extreme channel compresses rather than inflates R_space")
    checks.note(f"  healthy p90/p10: {healthy_spread:.1f}")
    checks.note(f"  one-extreme replacement p90/p10: {corrupted_spread:.1f}")

    checks.note()
    checks.note("[6] Current-boundary prose is stale")
    stale = "**This Draft 31 state is not approved by anyone yet**"
    section1910 = selection_text[
        selection_text.index("### 19.10 "):selection_text.index("### 19.11 ")
    ]
    checks.check(stale in section1910,
                 "section 19.10 still identifies the current state as Draft 31")

    checks.note()
    checks.note("Primary-source fact used for finding 2: pinned SpikeInterface")
    checks.note("0.104.8 filter.py builds coefficients with")
    checks.note("recording.get_sampling_frequency(); Draft 32 instead fixes 30 kHz.")
    checks.note()
    checks.note(f"checks run: {checks.total}")
    checks.note(f"checks failed: {checks.failed}")

    record = checks.render()
    print(record, end="")
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(record, encoding="utf-8", newline="\n")
    return 1 if checks.failed else 0


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out")
    return parser.parse_args()


def main() -> int:
    """CLI entry point."""
    args = parse_args()
    root = Path(args.repo_root).resolve()
    out = Path(args.out).resolve() if args.out else None
    return run(root, out)


if __name__ == "__main__":
    raise SystemExit(main())
