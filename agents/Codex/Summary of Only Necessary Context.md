# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 36 · 2026-08-16.**

**Next Codex session will be Session 37. The next count-based progress report is due in Session 40.**

## Current phase and controlling boundary

**Phase 2 — Execution is open. No scientific result exists.** RC-004 closed
`Approved` at Round 2, and its reference-instant pair check now governs. The
rank-1 plan-only read then completed, but the real drift command stopped before
a verdict because the approved input confirmation requires every spike depth to
be finite. Rank 1 is paused, not rejected. No host is pinned and no candidate
has a drift, noise, effective-SNR, donor, placement, generation or sorter value.

The strict finite-depth confirmation remains operative. Do not modify packet
code, open RC-005, resume rank 1, or advance the pinned order until the current
pre-card design discussion converges and a later exact implementation state is
same-state approved.

## The real-input finding

Claude Session 36 measured the affected class with a read-only diagnostic:

- rank 1 CSHL047 / Probe01: 231 NaN depths across 11 of 174 band units and
  3,160,311 band spikes; 0 non-finite times; 140 units meet support both before
  and after dropping; no unit loses a qualifying bin;
- rank 2 NYU-12 / Probe01: 222 NaN depths across 10 of 267 band units and
  4,898,466 band spikes; 0 non-finite times; 182 units meet support both ways;
  no unit loses a qualifying bin;
- every affected unit in both diagnostics is labelled `mua`, but the unit set
  remains label-blind and that association is descriptive only.

The diagnostic is `agents/Claude/tools/probe_nonfinite_depths.py` at SHA-256
`ade3660f…`. Codex reviewed its logic and recorded outputs but did not repeat an
archive read this session.

## Codex Session 36 disposition

Claude proposed dropping non-finite depths, publishing them, keeping non-finite
times fatal, and relying on §16.7's existing support floors. **Codex declined
that disposition as written.** Support floors bound how many finite values
remain; they do not bound the influence of values that are missing, the spacing
of the finite order statistics, or the selection effect of wholly missing
units. A published missing count is an audit output, not a protection on the
gate.

Independent synthetic evidence is
`agents/Codex/tools/probe_nonfinite_depth_disposition.py`, SHA-256
`efb03c8e661bba8eabd87010c94cf2fed61bff34a4433b514704e62e5765e729`,
against approved `band_drift.py` `eace4cd3…`. Five units retain 14,000 finite
depths in all twelve bins and one missing depth per unit/bin (0.00714235%). All
support floors pass. The finite-only point estimate gives `Delta_10min = 0 µm`,
while compatible completions of the same missing entries give 0 and 100 µm
against the 20 µm strict gate. Six of six checks pass. The construction does not
claim every NaN hides a physical value; it proves that counts alone do not
identify a decision-stable host-drift quantity.

## Counterproposal and immediate owner

`chats/Claude-Codex/Non-Finite Spike Depths/Non-Finite Spike Depths - Active.md`
contains the full ruling. The pre-write 200-line UTF-8 prefix remained
byte-identical, and the Session-36 Codex header occurs exactly once after it.

**Immediate owner: Claude, before formal review.** Accept the following design
boundary or counter-propose the smallest conservative recovery:

1. non-finite times remain input errors; non-finite depths may be dropped only
   for the point estimate;
2. use missing counts plus finite order statistics to build an assumption-free
   sensitivity interval, propagated through within-unit centring, the band
   median, `Delta_10min`, and the null quantity the gate consumes;
3. the existing 20/40 µm rule, not a fitted missingness percentage, decides
   stability; if compatible completions change the disposition or a required
   bound is unbounded, the candidate is unmeasurable and remains paused;
4. publish exclusions and sensitivity outputs per unit, per bin and in total;
5. before RC-005, cover Claude's three mirror failures, a wholly missing-depth
   unit, Codex's support-passing construction, and exhaustive small-array
   containment checks for the order-statistic interval.

This is open-ended design, not a candidate review. A Review Card is created only
after the owner has a stable implementation/documentation candidate.

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

The public root README has a forward correction recording that sample-count
floors are insufficient and that the proposal was returned before
implementation. No additional source was read and `references.md` did not
change.

## Downstream gates remain separate

1. converge on the non-finite-depth disposition;
2. implement/document a stable candidate, open RC-005, and obtain same-state
   approval;
3. resume rank-1 plan/measurement in the pinned order;
4. exposure-schedule/placement specification and approval;
5. matcher implementation, exhaustive/mutation tests and approval;
6. noise and post-rescaling effective-SNR host gates;
7. footprint/placement calibration and joint ten-placement gate;
8. exact sites, T/K/N, U/Z/R, edge table, matching outputs and IDs;
9. independent Tier A balance/manipulation approval;
10. separate generation authorization and later Rung 0/sorter authorization.

Ranks 5, 7, 9 and 13 remain paused on declared-clock disagreement. Their payload
diagnostic remains out of order. `chats/Claude-Codex-Human/Review Method Change/`
stays active by Randy's instruction; no new director decision is needed.

`agents/Codex/Session Summaries/HumanReport36.md` is the detailed record of this
ruling, counterexample, append verification and boundary.
