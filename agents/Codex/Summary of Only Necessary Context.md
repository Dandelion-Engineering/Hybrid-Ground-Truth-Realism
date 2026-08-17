# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 38 · 2026-08-17.**

**Next Codex session will be Session 39. The next count-based progress report is due in Session 40.**

## Current phase and controlling boundary

**Phase 2 — Execution is open. No scientific result exists.** RC-004 remains
closed `Approved`, but the first rank-1 drift command stopped before a verdict
because sparse NaN depths violate the still-binding finite-depth confirmation.
Rank 1 and the rank-2 holdout remain paused, not rejected. No host is pinned and
no candidate has a drift, noise, effective-SNR, donor, placement, generation or
sorter value.

The missing-depth recovery now has an accepted pre-card design, but no whole
reader/command/§17 candidate and no RC-005 exist. Do not resume the pinned order,
read another candidate payload, or treat the recovery as approved execution
code until RC-005 closes with explicit same-state approval.

## Claude Session 38 and the accepted correction

Claude accepted Codex Session 37's ruling that the fixed-arrangement
counterfactual did not bound the gate's actual null. The corrected
`Reproducibility Packet/scripts/utils/missing_depth.py` is
`5a9cfde418069799ce159ce3d25890004bdff6f95f8b8f75fc99ab51833ea17c`.

The corrected completed-`N` construction is the accepted pre-card design:

- every entry point takes the complete aligned spike-time/depth arrays, with
  NaN at missing positions, so tied times never require reconstruction;
- the complete analysed spike count, original missing source positions and
  replicate seed fix each approved permutation before missing values are
  chosen;
- missing slots are followed to their destination bins and the exact bin-
  median interval is propagated through centring, the across-unit median,
  `Delta_10min` and the nearest-rank null percentile;
- the interval is exact per bin and conservative above it, with error only
  toward pausing a candidate that a dependence-aware treatment might admit;
- the finite-only null remains a point diagnostic and is not described as a
  completed record when `k > 0`; and
- no fitted missingness threshold is introduced; the existing 20/40 µm gate
  judges decision stability.

## Codex Session 38 rulings

The full ruling is appended to the active Non-Finite Spike Depths chat. It is a
design disposition before formal review, not approval of an executable
candidate.

1. **Completed-`N` null accepted.** It is the actual completed-data quantity the
   gate consumes, not a substitute counterfactual.
2. **NaN is the only missing-depth marker.** `+inf` and `-inf` remain fatal input
   errors. Both measured candidates carry NaN only; relaxing infinities would
   extend the recovery to an unmeasured wrong-value class.
3. **An all-missing null destination is defined but unbounded.** If its complete
   count meets the floor, `(-inf, +inf)` is the exact attainable median set and
   must propagate to an unmeasurable disposition. An empty bin with no missing
   values still raises.
4. **Pre-card prose correction:** qualify the universal statement that both
   interval endpoints are attained. Finite bounded endpoints are attained; an
   unbounded side has no finite completion at infinity, although every finite
   value on that side is attainable.

## Evidence reproduced

- Owner harness `435272af…`: **86/86** at 200 permutations and 200 completion
  draws.
- Approved `test_band_drift.py`: **103/103** at 200 permutations.
- Codex's Session-37 probe `d1fdfefa…` preserves seven completed-data checks —
  `[12.254, 18.618] µm`, three completions contained, and zero-missing identity —
  then raises only when its retired eighth check calls the removed
  counterfactual signature. Do not edit it to make the old comparison green.
- The corrected crossover fixture reaches the 20 µm gate between 0.498% and
  0.990% missing under its deliberately systematic construction. This is
  scale on that fixture, not a threshold or a comparison to either real
  candidate's whole-band missing fraction.

## Immediate owner and next step

**Immediate owner: Claude.** Build one stable whole state before RC-005:

1. change the archive reader to preserve the complete aligned record and
   missing positions;
2. enforce the accepted NaN/infinity split;
3. have `measure_host_drift.py` publish exclusions per unit, per bin and total,
   the finite-only point diagnostics, both completed-data bounds and the
   stability disposition;
4. append forward §17 to the selection document without editing closed §16;
5. rerun the reader acceptance suite and both mutation harnesses after wiring;
6. fix the one unbounded-endpoint prose sentence; and
7. open RC-005 and a fresh review chat only after that whole state is stable.

The strict finite-depth rule continues to bind until the later exact state is
same-state approved. Ranks 5, 7, 9 and 13 remain separately paused on declared-
clock disagreement, and their payload diagnostic remains out of order.

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

1. stabilize and same-state approve the non-finite-depth recovery under RC-005;
2. resume rank-1 plan/measurement in the pinned order;
3. exposure-schedule/placement specification and approval;
4. matcher implementation, exhaustive/mutation tests and approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact sites, T/K/N, U/Z/R, edge table, matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. separate generation authorization and later Rung 0/sorter authorization.

The three-way Review Method Change chat stays active by Randy's instruction; no
new director decision is needed.

`agents/Codex/Session Summaries/HumanReport38.md` is the detailed record of the
design authentication, tests, rulings, append verification and boundary.
