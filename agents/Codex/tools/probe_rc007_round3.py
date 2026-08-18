"""Authenticate RC-007 Draft 31 and reproduce its Round-3 verdict conflict.

Inputs:
    --repo-root: repository root containing the eight-file Draft-31 candidate.
    --out: path for the deterministic human-readable evidence record.

Outputs:
    Prints and writes exact-state checks, the declared branch truth table, and
    the response-created conflict between the one-sided-instrument prose and
    the ordered verdict branches. Exits non-zero if any authentication or
    reproduction check fails.

Purpose:
    Provide independent reviewer evidence for the final RC-007 delta pass.
    The probe reads no archive, sample, network resource, or candidate result.
"""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path
import subprocess


CANDIDATE_HASHES = {
    "agents/Claude/Tier A Host and Injection Zone Selection.md":
        "24e78a5ad139245b197286edd1acaf8bea42bc75af3378883b3180d29a923755",
    "agents/Claude/tools/probe_rc007_round3.py":
        "54aeff57847e7a26cd3c8a80219883500a22c9cf736a5950da195a7f79a531d8",
    "agents/Claude/tools/rc007_round3_2026-08-18.txt":
        "b62d667c91d308e980d73688aae86ef507c10a42a4c4bb8f2a5b38d6b362e751",
    "agents/Claude/tools/rc007_round3_2026-08-18.json":
        "51e762669c53a57cc3c4219547a000435b1a89d766cbc9ca7730c4f6a5c9717f",
    "agents/Claude/tools/probe_rc007_spec.py":
        "ef37577e271161677a637b34fcac18a930bb105d544b94992886116140c625dd",
    "agents/Claude/tools/probe_rc007_spec_2026-08-18_draft31.txt":
        "97346727e30ebf5712f1c4e81a778e7651bfe4e9a264264d5d87ca14d4f5140e",
    "agents/Claude/tools/mutate_rc007_spec.py":
        "16a5f8832f64d54120a1ba34dd649e09eebc833d8f304f6faff17be9d808aad2",
    "agents/Claude/tools/mutate_rc007_spec_2026-08-18_draft31.txt":
        "e42c12bbf2b5c982cf67e5b2b0bd2174f96ea075f57415ea15e3bd3da39d930b",
}

FROZEN_SPANS = (
    (b"## 1. ", b"## 17. ", 144_664,
     "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59"),
    (b"## 17. ", b"## 18. ", 21_864,
     "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a"),
    (b"## 18. ", b"## 19. ", 20_579,
     "8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017"),
)

DRAFT30_COMMIT = "7012582"
SELECTION_PATH = "agents/Claude/Tier A Host and Injection Zone Selection.md"


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


def unique_slice(data: bytes, start: bytes, end: bytes) -> bytes:
    """Return bytes between unique start and end anchors."""
    if data.count(start) != 1 or data.count(end) != 1:
        raise ValueError(f"anchors are not unique: {start!r} -> {end!r}")
    left = data.index(start)
    right = data.index(end)
    if right <= left:
        raise ValueError(f"anchors are out of order: {start!r} -> {end!r}")
    return data[left:right]


def noise_disposition(r_space: float, r_null: float, tolerance: float) -> str:
    """Implement Draft 31's ordered branches 3 and 4 at an in-band level."""
    if r_space > tolerance:
        return "fails_homogeneity"
    if r_null > tolerance:
        return "unmeasurable"
    return "passes"


def rounded_grid(chunk_count: int, windows: int) -> list[int]:
    """Return Draft 31's eligible-centre grid using explicit floor(x + 0.5)."""
    return [
        1 + math.floor(k * (chunk_count - 3) / (windows - 1) + 0.5)
        for k in range(windows)
    ]


def git_text(repo_root: Path, commit: str, path: str) -> str:
    """Read one UTF-8 file state from git without changing the worktree."""
    command = ["git", "-C", str(repo_root), "show", f"{commit}:{path}"]
    result = subprocess.run(command, check=True, capture_output=True)
    return result.stdout.decode("utf-8")


def run(repo_root: Path, out_path: Path) -> int:
    """Run all exact-state and counterexample checks, then write the record."""
    checks = Checks()
    checks.note("RC-007 Round 3 -- independent reviewer delta probe")
    checks.note("=" * 58)
    checks.note()

    for relative, expected in CANDIDATE_HASHES.items():
        actual = sha256(repo_root / relative)
        checks.check(actual == expected, f"candidate digest: {relative}", actual)

    selection_file = repo_root / SELECTION_PATH
    selection_bytes = selection_file.read_bytes()
    selection_text = selection_bytes.decode("utf-8")
    section19 = selection_text[selection_text.index("## 19. "):]

    for start, end, expected_bytes, expected_hash in FROZEN_SPANS:
        span = unique_slice(selection_bytes, start, end)
        checks.check(len(span) == expected_bytes,
                     f"frozen span bytes: {start.decode().strip()}", str(len(span)))
        checks.check(hashlib.sha256(span).hexdigest() == expected_hash,
                     f"frozen span digest: {start.decode().strip()}")

    checks.note()
    checks.note("[1] Round-3 repairs that reproduce")

    grid = rounded_grid(9_999, 60)
    gaps = [b - a for a, b in zip(grid, grid[1:])]
    largest_gap = max(gaps)
    checks.check(grid[0] == 1 and grid[-1] == 9_997,
                 "grid keeps a full neighbour on each side")
    checks.check(len(grid) == 60 and len(set(grid)) == 60,
                 "grid has 60 distinct centres")
    checks.check(largest_gap == 170, "largest centre gap is 170 chunks")
    checks.check(all(any(center in range(start, start + largest_gap) for center in grid)
                     for start in range(1, 9_998 - largest_gap + 1)),
                 "every in-span run of 170 chunks contains a centre")
    checks.check(any(not any(center in range(start, start + largest_gap - 1)
                             for center in grid)
                     for start in range(1, 9_998 - (largest_gap - 1) + 1)),
                 "an in-span run of 169 chunks can contain no centre")

    logical_bytes = 99_984_384_000
    stored_bytes = 53_163_508_785
    uncompressed_chunk = 13_020 * 384 * 2
    projected_chunk = round(uncompressed_chunk * stored_bytes / logical_bytes)
    projected_run = round(uncompressed_chunk * stored_bytes / logical_bytes * 180)
    checks.check(uncompressed_chunk == 9_999_360,
                 "one uncompressed storage chunk is 9,999,360 bytes")
    checks.check(projected_chunk == 5_316_841,
                 "whole-file projection is 5,316,841 stored bytes per chunk")
    checks.check(projected_run == 957_031_364,
                 "180-chunk transfer projection is 957,031,364 bytes")
    checks.check("no isolated-window construction left to bound" in section19,
                 "F4-R1 isolation construction is withdrawn")
    checks.check("fixture diagnostics and are not a bound" in section19,
                 "F4-R1 residual measurements are labelled non-bounds")
    checks.check("The one-way claim is withdrawn in full" in section19,
                 "F7-R1 monotonic claim is withdrawn")
    checks.check("It defines no host-aggregate precondition" in section19,
                 "F6-R1 aggregate-gate discharge is withdrawn")

    checks.note()
    checks.note("[2] Response-created verdict conflict")

    universal_claim = "A value **above** `M` is sufficient to withhold the measurement"
    boundary_claim = "A value above `M` withholds the measurement"
    branch3 = "**Homogeneity.** `R_space_sampled > M` -> **fails** on homogeneity."
    branch4 = ("4. **Resolution.** `R_space_sampled ≤ M` and "
               "`R_null_sampled > M` → **unmeasurable**")
    # Match Unicode comparison arrows as written after first checking the
    # prose surfaces whose semantics are being tested.
    checks.check(universal_claim in section19,
                 "section states high R_null is sufficient to withhold")
    checks.check(boundary_claim in section19,
                 "boundary repeats that any high R_null withholds")
    checks.check("a high value withholds the measurement" in selection_text.splitlines()[4],
                 "Draft-31 status line publishes the same universal claim")
    checks.check(branch3.replace("->", "→") in section19,
                 "ordered branch 3 fails every high R_space")
    checks.check(branch4 in section19,
                 "ordered branch 4 withholds only when R_space is inside tolerance")

    truth_table = {
        "space_low_null_low": noise_disposition(1.5, 1.5, 2.0),
        "space_low_null_high": noise_disposition(1.5, 3.0, 2.0),
        "space_high_null_low": noise_disposition(3.0, 1.5, 2.0),
        "space_high_null_high": noise_disposition(3.0, 3.0, 2.0),
    }
    checks.check(truth_table["space_low_null_low"] == "passes",
                 "inside/inside reaches pass")
    checks.check(truth_table["space_low_null_high"] == "unmeasurable",
                 "inside/high reaches branch-4 withholding")
    checks.check(truth_table["space_high_null_low"] == "fails_homogeneity",
                 "high/inside reaches branch-3 failure")
    checks.check(truth_table["space_high_null_high"] == "fails_homogeneity",
                 "high/high reaches branch-3 failure, not withholding")
    checks.check(
        truth_table["space_high_null_high"] != "unmeasurable",
        "R_null > M is not sufficient to withhold under the ordered branches",
    )

    draft30 = git_text(repo_root, DRAFT30_COMMIT, SELECTION_PATH)
    checks.check(universal_claim not in draft30 and boundary_claim not in draft30,
                 "universal high-null claim was not present in Draft 30")
    checks.check("non-stationarity can only inflate it" in draft30,
                 "Draft 30 carried the superseded one-way claim")
    checks.check("must be resolved before the estimator's first run" in section19,
                 "contiguous-vs-interleaved split remains a tracked pre-run follow-up")

    checks.note()
    checks.note("Declared truth table at N-in-band, M=2.0:")
    for name, disposition in truth_table.items():
        checks.note(f"  {name:24s} -> {disposition}")
    checks.note()
    checks.note("Finding: Draft 31 says any R_null_sampled > M is sufficient")
    checks.note("to withhold the measurement, but its ordered branch 3 fires")
    checks.note("first when R_space_sampled > M. The concrete high/high case")
    checks.note("therefore fails rather than being withheld. This contradiction")
    checks.note("was introduced by the Round-3 F7-R1 response and reaches the")
    checks.note("candidate disposition. It is a new blocker after Round 2.")
    checks.note()
    checks.note(f"checks run: {checks.total}")
    checks.note(f"checks failed: {checks.failed}")

    record = checks.render()
    print(record, end="")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(record, encoding="utf-8", newline="\n")
    return 1 if checks.failed else 0


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Authenticate RC-007 Draft 31 and reproduce the response-created "
            "conflict between its one-sided R_null prose and verdict branches."
        )
    )
    parser.add_argument("--repo-root", required=True,
                        help="path to the repository root")
    parser.add_argument("--out", required=True,
                        help="path for the LF-only human-readable evidence record")
    return parser.parse_args()


def main() -> int:
    """Run the probe from parsed command-line arguments."""
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = (repo_root / out_path).resolve()
    return run(repo_root, out_path)


if __name__ == "__main__":
    raise SystemExit(main())
