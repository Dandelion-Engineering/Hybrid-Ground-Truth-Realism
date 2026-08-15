# Summary — Tier A Selection Review

**Date range:** 2026-08-12 (Claude Session 5) — 2026-08-14 (Claude Session 24 addendum, 19:58 PDT)
**Participants:** Claude, Codex
**Outcome:** **Concluded on a method change, not on convergence.** The director directed a new review method; its transition rule preserves an in-flight candidate's state and restarts the cycle under a Review Card. §16 and its two implementation states were **open on Codex** at the moment of transition and continue at `Review Cards/RC-001 Tier A Selection Section 16.md` in `chats/Claude-Codex/Tier A Selection Section 16 Review/`. No candidate state changed.

## State carried forward, unchanged

| File | SHA-256 |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` (Draft 22) | `5ca2d6ca188d27ad1cfd9352b9078855815b3fc274eb8cc2773a6e11063f4d1a` |
| `Reproducibility Packet/scripts/utils/band_drift.py` | `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063` |
| `agents/Claude/tools/test_band_drift.py` | `2117983084ceee241273e355077f8c6792ec60c24e6c0ed44813b3481bcd9c89` |

**§1–§15 are same-state approved by both agents.** §16 is the only open part.

## What this chat settled and put beyond dispute

**The contract-level decisions**, each reached through explicit two-sided approval: Amendments 2 through 6 were drafted, contested, repaired and put in force here — host chosen outside the donor library's twelve subjects; the negative-control pseudo-arm design; the injection zone's donors removed from the real region-unaware arm before matching; and Tier A's parameterization by `N`, the surviving zone donors. The agreed division of labor was not reopened.

**§15 — the pinned candidate order.** Thirteen host candidates in a fixed sequence, fixed *before* any remaining gate had been run on any of them, because "first-admissible" is not a rule until the sequence is. Two passes, 20 µm then 40 µm, with a declared gate order that can change cost but never a verdict.

**§16 — the drift quantity.** The archive's `cumulative_drift_um_per_hour` was retired on its own first-party description (a path length, spike-count-correlated at ~0.79, and "NOT actual electrode displacement" in IBL's words). The replacement is a band displacement trace built from per-spike centre-of-mass depths: 60-second session-grid bins anchored at zero with extent `t_last_s`, per-unit medians, within-unit centring, an across-unit median band trace, and peak-to-peak excursions over the whole recording and the worst ten-bin window. The gate is two numbers — `Delta_10 <= L` **and** `Q95_null <= L` — at 20 µm strict with one pre-declared relaxation to 40 µm. An inside-null result passes rather than being inverted into a rejection of the quietest possible host.

## The defect class this chat is most worth remembering for

Nineteen substantive corrections, and one class dominates: **"this mechanism widens it, therefore it always widens."** A directional claim true of the fixture that motivated it, promoted to a general guarantee, with the quieter case unchecked. It was caught five times, by both agents, in both directions:

- two Draft 16 guarantees (adding label-blind units cannot buy a pass; retaining the head bin can only move toward rejection) — both broken by deterministic fixtures against the packet's own implementation;
- the per-unit audit evaluated only inside the band-selected window, which a suppressed band picks arbitrarily;
- `Q95_null` called "systematically narrower" than a single unit's trace, reversed by a heterogeneous fixture;
- and the mirror of that repair — the audit's magnitude separation treated as visible in general, when its **absence** is not evidence at all.

The last of these is the one with teeth for the science: a fixture inside §16.7's own admitted parameters **passes both gate numbers** while ten of twenty-one units genuinely move 30 µm, with the movers' excursions overlapping the stationary ones — and the masking *strengthens* as the band grows, while the pinned candidates carry 22 to 267 band units. That is a published limitation of the drift result, not a solved problem, and it is stated in §16.4.

Other corrections worth carrying: endpoint containment cannot identify a clock's origin or scale (the converter's documented session-time semantics do); a median residual cannot establish coordinate equivalence (`max_electrode -> rel_y` does); a *span* is not an *end time*; and the permutation pool is analysed-bin spikes only, for both observation and null.

## Method note

Nine round-trips on §16, none of them a repeated disagreement — every round accepted the prior round's corrections in full and then produced a new finding, usually as a direct consequence of the repair. Both agents had independently written that they believed the chain had bottomed out. That pattern — real findings with no boundary that ends the review — is the specific thing the new method is pointed at, and this chat is its best available evidence in both directions.

## Boundary

This chat pinned no host, measured no candidate, selected no donor, opened no target manifest, installed no dependency, read no raw data, ran no generator and ran no sorter. **No scientific result exists.**
