"""Independently check completion-bound formulas at the production band size.

Claude Session 51 validated a three-level enumeration against a refined-grid
search at small ``n``.  This reviewer probe closes the stated production-size
gap without importing or copying that implementation.  It derives the two
endpoints directly from the ranks at ``n = 72`` when at most seven ratios are
undefined, exhausts every multiset of undefined values over several discrete
rank patterns at that full band size, and exhibits the universal withholding
witness for eight or more undefined ratios.

The probe uses constructed values only.  It reads no archive or candidate and
does not select a split rule or create a Review Card.

Example
-------
    .\\venv\\Scripts\\python.exe \
        agents/Codex/tools/probe_completion_bounds_n72.py \
        --out agents/Codex/tools/completion_bounds_n72_2026-08-19.txt \
        --records agents/Codex/tools/completion_bounds_n72_2026-08-19.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from pathlib import Path


BAND_CHANNELS = 72
LOW_RANK = 8
HIGH_RANK = 65
INF = float("inf")


class Checks:
    """Accumulate named checks and render a deterministic text report."""

    def __init__(self) -> None:
        """Create an empty check ledger."""
        self.lines: list[str] = []
        self.failed = 0

    def heading(self, title: str) -> None:
        """Append one report section heading."""
        if self.lines:
            self.lines.append("")
        self.lines.append(title)

    def check(self, claim: str, condition: bool, detail: str) -> None:
        """Record a pass or failure with one evidence detail."""
        label = "PASS" if condition else "FAIL"
        self.lines.append(f"{label}  {claim}  [{detail}]")
        if not condition:
            self.failed += 1

    def note(self, detail: str) -> None:
        """Append a non-voting boundary or interpretation note."""
        self.lines.append(f"NOTE  {detail}")

    def render(self) -> str:
        """Return the report and its final check-count summary."""
        total = sum(
            line.startswith("PASS") or line.startswith("FAIL")
            for line in self.lines
        )
        return (
            "\n".join(self.lines)
            + f"\n\nSummary\n{total} checks, {self.failed} failed\n"
        )


def rank_ratio(values: list[float]) -> float | None:
    """Return the rank-65/rank-8 ratio under the declared edge conventions.

    ``None`` represents either 0/0 or infinity/infinity.  A zero denominator
    with a positive numerator returns positive infinity.
    """
    if len(values) != BAND_CHANNELS:
        raise ValueError("rank_ratio requires exactly 72 values")
    ordered = sorted(values)
    low = ordered[LOW_RANK - 1]
    high = ordered[HIGH_RANK - 1]
    if (low == 0.0 and high == 0.0) or (
        math.isinf(low) and math.isinf(high)
    ):
        return None
    if low == 0.0:
        return INF
    return high / low


def effective_upper(values: list[float | None]) -> float:
    """Return the conservative upper endpoint of candidate ratio values."""
    if any(value is None for value in values):
        return INF
    defined = [value for value in values if value is not None]
    return max(defined) if defined else INF


def closed_bounds_positive(defined: list[float], undefined: int) -> tuple[float, float]:
    """Derive the exact n=72 endpoints for 0..7 undefined ratios.

    The derivation applies when rank 8 of the sorted defined values is finite
    and strictly positive.  The minimum keeps that value at the denominator
    while spending every unknown below rank 65.  The maximum considers the
    only rank-live vertex classes: ``a`` unknowns below every defined value and
    the remainder above every defined value.
    """
    if not 0 <= undefined <= 7:
        raise ValueError("closed production-size formula requires 0 <= u <= 7")
    if len(defined) != BAND_CHANNELS - undefined:
        raise ValueError("defined count and undefined count must sum to 72")
    ordered = sorted(defined)
    denominator = ordered[LOW_RANK - 1]
    if denominator <= 0.0 or math.isinf(denominator):
        raise ValueError("rank-8 defined value must be finite and positive")

    minimum_index = max(HIGH_RANK - undefined, LOW_RANK)
    lower = ordered[minimum_index - 1] / denominator

    upper_candidates: list[float] = []
    for below in range(undefined + 1):
        low = ordered[LOW_RANK - below - 1]
        high = ordered[HIGH_RANK - below - 1]
        if low == 0.0:
            upper_candidates.append(INF)
        else:
            upper_candidates.append(high / low)
    return lower, max(upper_candidates)


def endpoint_witnesses(
    defined: list[float], undefined: int
) -> tuple[float | None, list[float | None]]:
    """Construct the lower witness and every upper-vertex witness directly."""
    ordered = sorted(defined)
    lower_fill = ordered[LOW_RANK - 1]
    lower = rank_ratio(ordered + [lower_fill] * undefined)
    upper = [
        rank_ratio(
            [0.0] * below
            + ordered
            + [INF] * (undefined - below)
        )
        for below in range(undefined + 1)
    ]
    return lower, upper


def histogram_oracle(
    defined: list[float], undefined: int, grid: list[float]
) -> tuple[float | None, float, bool, int]:
    """Exhaust every completion multiset over a discrete ordered grid.

    Combinations with replacement enumerate order patterns rather than ordered
    tuples, so the oracle remains small at n=72 while covering every placement
    of the undefined values on the supplied levels.
    """
    low: float | None = None
    seen: list[float | None] = []
    count = 0
    for indices in itertools.combinations_with_replacement(
        range(len(grid)), undefined
    ):
        completion = [grid[index] for index in indices]
        value = rank_ratio(list(defined) + completion)
        seen.append(value)
        count += 1
        if value is not None and (low is None or value < low):
            low = value
    return low, effective_upper(seen), any(value is None for value in seen), count


def production_patterns(undefined: int) -> list[tuple[str, list[float]]]:
    """Return full-size positive defined pools with distinct rank structures."""
    count = BAND_CHANNELS - undefined
    shapes = [
        ("flat", [1.0] * count),
        ("two-level", sorted([1.0] * min(20, count) + [3.0] * max(0, count - 20))),
        (
            "three-level",
            sorted(
                [0.5] * min(12, count)
                + [1.5] * min(40, max(0, count - 12))
                + [6.0] * max(0, count - 52)
            ),
        ),
    ]
    return [(name, values) for name, values in shapes if len(values) == count]


def random_positive_pool(rng: random.Random, undefined: int) -> list[float]:
    """Build one sorted positive finite production-size defined pool."""
    count = BAND_CHANNELS - undefined
    values = [0.05 + 12.0 * (rng.random() ** 2) for _ in range(count)]
    return sorted(values)


def parse_args() -> argparse.Namespace:
    """Parse required report paths and the deterministic stress count."""
    parser = argparse.ArgumentParser(
        description=(
            "Independently verify completion bounds at the production band "
            "size n=72."
        )
    )
    parser.add_argument("--out", required=True, type=Path, help="text report path")
    parser.add_argument(
        "--records", required=True, type=Path, help="JSON evidence path"
    )
    parser.add_argument(
        "--random-fixtures",
        type=int,
        default=512,
        help="number of positive finite rank patterns to stress",
    )
    return parser.parse_args()


def main() -> int:
    """Run every production-size check and write deterministic evidence."""
    args = parse_args()
    checks = Checks()
    records: dict[str, object] = {}
    rng = random.Random(19081952)

    checks.heading("1. Production ranks and the direct endpoint derivation")
    derived_ranks = (
        math.ceil(0.10 * BAND_CHANNELS),
        math.ceil(0.90 * BAND_CHANNELS),
    )
    checks.check(
        "the declared nearest ranks at n=72 are 8 and 65",
        derived_ranks == (LOW_RANK, HIGH_RANK),
        f"ranks {derived_ranks[0]} and {derived_ranks[1]}",
    )
    checks.check(
        "the lower and upper tail capacities both equal seven",
        LOW_RANK - 1 == BAND_CHANNELS - HIGH_RANK == 7,
        "seven arbitrary contacts fit below p10 or above p90",
    )

    checks.heading("2. Full-size histogram exhaustion over rank patterns")
    oracle_mismatches: list[tuple[str, int, float, float, float, float]] = []
    oracle_states = 0
    oracle_fixtures = 0
    for undefined in range(0, 8):
        for name, defined in production_patterns(undefined):
            lower, upper = closed_bounds_positive(defined, undefined)
            levels = sorted(
                set([0.0, 0.25, 0.5, 1.0, 1.5, 3.0, 6.0, 12.0, INF])
                | set(defined)
            )
            oracle_low, oracle_high, _, states = histogram_oracle(
                defined, undefined, levels
            )
            oracle_fixtures += 1
            oracle_states += states
            if oracle_low != lower or oracle_high != upper:
                oracle_mismatches.append(
                    (name, undefined, lower, upper, oracle_low or -1.0, oracle_high)
                )
    checks.check(
        "the closed endpoints equal exhaustive completion-multiset extrema "
        "on every n=72 discrete rank pattern",
        not oracle_mismatches,
        f"{oracle_fixtures} fixtures, {oracle_states} completion multisets, "
        f"{len(oracle_mismatches)} mismatches",
    )
    records["histogram_oracle"] = {
        "fixtures": oracle_fixtures,
        "completion_multisets": oracle_states,
        "mismatches": len(oracle_mismatches),
    }

    checks.heading("3. Independent endpoint witnesses on continuous pools")
    formula_mismatches: list[tuple[int, int]] = []
    containment_failures = 0
    completions_sampled = 0
    for fixture in range(args.random_fixtures):
        undefined = fixture % 8
        defined = random_positive_pool(rng, undefined)
        lower, upper = closed_bounds_positive(defined, undefined)
        lower_witness, upper_witnesses = endpoint_witnesses(defined, undefined)
        witnessed_upper = effective_upper(upper_witnesses)
        if lower_witness != lower or witnessed_upper != upper:
            formula_mismatches.append((fixture, undefined))
        for _ in range(32):
            completion = [
                rng.choice([0.0, INF, 12.0 * rng.random()])
                for _ in range(undefined)
            ]
            value = rank_ratio(defined + completion)
            if value is not None:
                completions_sampled += 1
                if not lower <= value <= upper:
                    containment_failures += 1
    checks.check(
        "the direct lower witness and all-zero/all-infinity vertex family "
        "attain the derived endpoints",
        not formula_mismatches,
        f"{args.random_fixtures} fixtures, {len(formula_mismatches)} mismatches",
    )
    checks.check(
        "sampled interior completions remain inside those independently "
        "derived endpoints",
        containment_failures == 0,
        f"{completions_sampled} defined completions, {containment_failures} outside",
    )
    records["continuous_stress"] = {
        "fixtures": args.random_fixtures,
        "defined_completions": completions_sampled,
        "endpoint_mismatches": len(formula_mismatches),
        "containment_failures": containment_failures,
    }

    checks.heading("4. The eight-contact threshold is a universal witness")
    threshold_failures: list[int] = []
    threshold_examples: dict[str, str] = {}
    for undefined in range(8, BAND_CHANNELS + 1):
        defined = [1.0 + index / 10.0 for index in range(BAND_CHANNELS - undefined)]
        completion = [0.0] * 8 + [INF] * (undefined - 8)
        value = rank_ratio(defined + completion)
        if value is not None and not math.isinf(value):
            threshold_failures.append(undefined)
        if undefined in (8, 64, 72):
            threshold_examples[str(undefined)] = (
                "undefined" if value is None else "inf"
            )
    checks.check(
        "for every undefined count from 8 through 72, one explicit completion "
        "makes the band ratio infinite or undefined",
        not threshold_failures,
        f"65 counts checked, {len(threshold_failures)} failures",
    )
    checks.check(
        "the threshold is the shared p10/p90 tail capacity plus one",
        8 == LOW_RANK == BAND_CHANNELS - HIGH_RANK + 1,
        "8 = rank(p10) = upper-tail contacts reaching rank(p90)",
    )
    edge_failures: list[tuple[int, str]] = []
    for undefined in range(0, 8):
        count = BAND_CHANNELS - undefined
        zero_rank = sorted([0.0] * 8 + [1.0] * (count - 8))
        zero_witness = rank_ratio(zero_rank + [INF] * undefined)
        if zero_witness is not None and not math.isinf(zero_witness):
            edge_failures.append((undefined, "zero"))
        infinite_rank = sorted([1.0] * 7 + [INF] * (count - 7))
        infinite_witness = rank_ratio(infinite_rank + [INF] * undefined)
        if infinite_witness is not None and not math.isinf(infinite_witness):
            edge_failures.append((undefined, "infinity"))
    checks.check(
        "for u=0..7, a zero or infinite rank-8 defined value is already "
        "withheld, leaving only the positive-finite case for the closed formula",
        not edge_failures,
        f"16 edge fixtures, {len(edge_failures)} failures",
    )
    records["threshold_witness"] = {
        "counts_checked": 65,
        "failures": len(threshold_failures),
        "examples": threshold_examples,
        "rank8_edge_failures": len(edge_failures),
    }

    checks.heading("5. Decision and label reach at the full band size")
    bite_defined = sorted([1.0] * 7 + [3.0] * 58)
    bite_lower, bite_upper = closed_bounds_positive(bite_defined, 7)
    clean_defined = [1.0 + 0.001 * index for index in range(65)]
    clean_lower, clean_upper = closed_bounds_positive(clean_defined, 7)
    checks.check(
        "seven undefined ratios can change a scalar-convention pass into a "
        "withheld state",
        bite_lower == 1.0 and bite_upper == 3.0 and bite_upper > 2.0,
        f"biting bound [{bite_lower:.6f}, {bite_upper:.6f}]",
    )
    checks.check(
        "seven undefined ratios can also be proved irrelevant to branch 4",
        clean_upper <= 2.0,
        f"clean bound [{clean_lower:.6f}, {clean_upper:.6f}]",
    )
    interval = (1.5, 4.0)
    label_map = {
        "resolved": 5.0 > interval[1],
        "resolution_limited": 1.2 <= interval[0],
        "unresolved": interval[0] < 3.0 <= interval[1],
    }
    checks.check(
        "comparison with both endpoints requires three mutually reachable "
        "branch-3 labels",
        all(label_map.values()),
        "resolved above, limited below, unresolved inside",
    )
    records["decision_examples"] = {
        "biting": [bite_lower, bite_upper],
        "decision_irrelevant": [clean_lower, clean_upper],
        "three_labels_reachable": all(label_map.values()),
    }

    checks.heading("6. Scope boundary")
    checks.note(
        "the evidence independently closes the owner report's n=72 gap for "
        "the branch-4-live range u=0..7 and proves the universal u>=8 witness"
    )
    checks.note(
        "constructed ratios only; no archive, network resource, candidate "
        "sample, packet file, host gate, or pinned order is read or moved"
    )
    checks.note(
        "this is co-design evidence outside formal review; it selects no split "
        "member and opens no successor Review Card"
    )

    records["boundary"] = (
        "constructed production-size ratios only; independent direct-rank "
        "derivation, not a candidate Part B specification"
    )
    report = checks.render()
    print(report, end="")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.records.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8", newline="\n")
    args.records.write_text(
        json.dumps(records, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 1 if checks.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
