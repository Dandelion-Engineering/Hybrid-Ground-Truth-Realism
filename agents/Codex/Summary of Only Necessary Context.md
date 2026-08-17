# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 37 · 2026-08-17.**

**Next Codex session will be Session 38. The next count-based progress report is due in Session 40.**

## Current phase and controlling boundary

**Phase 2 — Execution is open. No scientific result exists.** RC-004 remains
closed `Approved`, but the first rank-1 measurement stopped before a drift
verdict because sparse NaN depths violate the still-binding finite-depth input
confirmation. Rank 1 and the rank-2 holdout remain paused, not rejected. No
host is pinned and no candidate has a drift, noise, effective-SNR, donor,
placement, generation or sorter value.

Do not modify the approved reader/command, resume the pinned order, or open
RC-005 until the missing-depth recovery is a complete stable pre-card state and
then receives same-state approval.

## Claude Session 37: accepted work and correction

Claude accepted Codex Session 36's rejection of count-only exclusion and built
`Reproducibility Packet/scripts/utils/missing_depth.py` (`2064304e…`) plus a
59-check harness (`73a7c59…`). Codex reproduced **59/59** at the pinned 200
permutations.

Accepted design pieces:

- exact unit/bin median attainable intervals from finite order statistics and
  missing counts;
- support invariance across all three existing inclusion floors;
- conservative propagation through centring, the across-unit median and the
  excursion statistic;
- exclusion publication per unit, per bin and in total; and
- the existing 20/40 µm tolerance as the decision boundary, with no fitted
  missingness percentage.

Claude also correctly narrowed Codex's first counterexample. The balanced
0/100 µm construction proves the **point estimate** can change from 0 to 100 µm
while support remains green, but the existing two-number gate already rejects
that fixture because `Q95_null = 100 µm`. Claude's stronger spread fixture
supplies the whole-gate example: the observed record passes at `Delta_10min =
10.367 µm` and pinned-200 `Q95_null = 14.604 µm`, while missing completions admit
an excursion bound to `73.45 µm`.

## Codex Session 37 null ruling

**The proposed fixed-arrangement null is not accepted as the voting
sensitivity quantity.** Claude argued that the actual completed-data null is
necessarily vacuous because restoring values changes the permutation length.
But the completed length `N`, original missing source positions and replicate
seed are all known before missing values are chosen. Therefore
`rng.permutation(N)` is fixed across every completion. Follow the unknown source
slots to their destination bins and propagate their exact median intervals
through the actual approved null.

Independent evidence is
`agents/Codex/tools/probe_missing_depth_actual_null.py`, SHA-256
`d1fdfefae8d9b3f0bdfbc8e9de25c82f7ddae83688855c0a2482d4af8cac09b1`.
At 200 permutations it passes 8/8: finite actual-null interval
`[12.254, 18.618] µm`, width `6.365 µm`; low/high/mixed actual completions all
inside; zero-missing lower/upper paths each reproduce all 200 approved-null
replicates; actual and counterfactual intervals are distinct.

The reader must preserve original all-spike order or a missing-position mask,
not merely missing times, because tied times cannot reconstruct source order.
The current counterfactual may remain only as a clearly nonvoting diagnostic
with a separate purpose.

## Immediate owner and next step

**Immediate owner: Claude, still before formal review.** The active chat contains
the full ruling. Claude should:

1. implement the completed-`N` actual-null interval;
2. add actual full-null completion containment, zero-missing identity,
   unbounded and row-index validation tests;
3. wire the reader so it excludes non-finite depths for the point path while
   preserving missing positions and keeping non-finite times fatal;
4. publish exclusions and both sensitivity intervals in the command output;
5. write the forward §17 disposition without editing closed §16; and
6. create RC-005 and a fresh review chat only when that whole state is stable.

This is open-ended co-design, not a review round. The strict finite-depth rule
continues to bind until a later exact state is same-state approved.

## Approved foundation still in force

- RC-001: Draft 24 `c35987fe…`, drift utility `eace4cd35…`, owner harness
  `946df906…`, closed `Approved`.
- RC-003: bounded archive reader closed `Approved` at its recorded nine-file
  state.
- RC-004: reference-instant pair check closed `Approved` at its exact five-file
  state (`archive_units.py` `9ef16f58…`, `measure_host_drift.py` `156f6f0f…`,
  owner suite `c508233d…`, mutation harness `97860ad9…`, carried verifier
  `f4ee4ae6…`).
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

## Downstream gates remain separate

1. converge on and same-state approve the non-finite-depth recovery under
   RC-005;
2. resume rank-1 plan/measurement in the pinned order;
3. exposure-schedule/placement specification and approval;
4. matcher implementation, exhaustive/mutation tests and approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact sites, T/K/N, U/Z/R, edge table, matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. separate generation authorization and later Rung 0/sorter authorization.

Ranks 5, 7, 9 and 13 remain paused on declared-clock disagreement. Their
payload diagnostic remains out of order. The three-way Review Method Change
chat stays active by Randy's instruction; no new director decision is needed.

`agents/Codex/Session Summaries/HumanReport37.md` is the detailed record of the
cross-review, actual-null construction, tests, append verification and boundary.
