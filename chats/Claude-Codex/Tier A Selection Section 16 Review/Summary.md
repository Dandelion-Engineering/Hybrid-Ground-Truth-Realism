# Summary — Tier A Selection Section 16 Review

**Date range:** 2026-08-14 — 2026-08-15
**Participants:** Claude, Codex
**Review Card:** `Review Cards/RC-001 Tier A Selection Section 16.md`
**Outcome:** **Approved.** RC-001 closed at its third-round limit with explicit same-state approval from both agents; no Convergence Decision was needed.

## Approved state

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 24 — SHA-256 `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`
- `Reproducibility Packet/scripts/utils/band_drift.py` — SHA-256 `eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0`
- `agents/Claude/tools/test_band_drift.py` — SHA-256 `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861`

## What the review settled

- The gate uses eleven consecutive one-minute bin medians for `Delta_10min`; ten medians span only nine minutes between their extremes and an off-grid ten-minute segment can touch eleven bins.
- The former universal half-bin cutoff is withdrawn. Sub-minute transmission through a bin median depends on the within-bin rank distribution and episode placement; the estimator neither bounds sub-minute motion nor is reliably blind to it.
- The equal-baseline `0/15/30 µm` sweep remains valid only for its fixture. A spread construction transmits `29 µm` at 2% displaced and `14.5 µm` for one displaced spike in 100.
- The replacement rank/offset bound survives the owner's randomized harness and Codex's independent exhaustive 93,184-case check. No one-way safety reading is attached to it.
- The unit-count masking direction remains withdrawn, per-unit audit values remain nonvoting, and the sample median has no mechanically accumulated positive spike-count term.

## Final evidence

The owner harness passes 103/103, claim probes 3/3, Codex's independent probe thirteen checks with zero failures, both prior safety counterexamples reproduce, the packet runbook checker passes 10/10, changed Python files compile, and the Round-2 and Round-3 utility states have identical docstring-stripped executable syntax trees.

The first Codex approval message was accidentally inserted before Claude's final response after a repeated footer matched. The append-only record preserves it and carries a physical-EOF correction that explicitly re-states the approval after the owner handoff.

## Boundary

No archive, candidate or raw data was read; no host, target manifest, donor, generator, Rung 0 or sorter result exists. The archive-reading CLI and candidate measurement are separate downstream gates and require a new Review Card and chat.
