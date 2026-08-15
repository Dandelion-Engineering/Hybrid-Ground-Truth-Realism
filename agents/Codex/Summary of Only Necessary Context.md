# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 26 · 2026-08-15 02:17 PDT**

**Next Codex session will be Session 27. No count-based progress report is due until Session 32.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate archive, drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, rendered edge table, exposure schedule, selected donor, template array, Rung 0, hybrid generation or sorter run exists.

The public state remains `In Progress`. RC-001's pre-measurement drift specification is now approved, but every implementation, candidate-reading and execution gate downstream of it remains separate.

## RC-001 closed Approved

`Review Cards/RC-001 Tier A Selection Section 16.md` closed at Round 3 on 2026-08-15. Claude and Codex explicitly approve the same exact state:

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 24 — SHA-256 `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`;
- `Reproducibility Packet/scripts/utils/band_drift.py` — SHA-256 `eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0`;
- `agents/Claude/tools/test_band_drift.py` — SHA-256 `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861`.

No Convergence Decision was needed. The concluded chat and summary live at `chats/Claude-Codex/Tier A Selection Section 16 Review/`.

### What the approved drift state says

- `Delta_10min` uses eleven consecutive one-minute bin medians. Ten medians span only nine minutes between extremes, and an off-grid 600-second segment can touch eleven bins.
- The gate still requires both `Delta_10min <= L` and `Q95_null <= L`, first at 20 µm and then at the single pre-declared 40 µm relaxation.
- The universal half-bin cutoff is withdrawn. Within-bin transmission depends on the spike-depth rank distribution and episode placement.
- The equal-baseline `0/15/30 µm` sweep is a fixture result only. A spread fixture transmits `29 µm` at 2% displaced and `14.5 µm` for one displaced spike in 100.
- The valid replacement is a rank/offset bound, not a detectability cutoff. The statistic neither bounds sub-minute motion nor is reliably blind to it; neither direction is a safety property.
- The label-blind-unit limitation remains published and conditional. Per-unit audit values remain nonvoting and have no unit-level null or fixed ordering against the band `Q95_null`.
- The withdrawn unit-count masking direction stays withdrawn. Absence of per-unit magnitude separation is not evidence that the band is steady.

### Final evidence

- owner harness 103/103;
- claim probes 3/3;
- packet runbook checker 10/10;
- Codex safety probes reproduce at `7.966/8.346 µm` and `27.273/11.591 µm`;
- Codex's independent probe passes thirteen checks at SHA-256 `491239808ee4cf3b0d04a0858a795a87647fdf16de4779ac3b39248fbdbf59bc`, including 93,184 exhaustive small depth/mask/offset cases;
- Round-2 and Round-3 utility states have identical docstring-stripped executable ASTs.

## Review-method state

`Playbooks/review-cycle.md` is governed by Randy's superseding Review Card method:

- one stable candidate and written purpose/scope/acceptance boundary;
- Round 1 is the only full-artifact pass and records one complete numbered ledger;
- later rounds are delta-only: recorded findings and response-created regressions;
- at most three owner-reviewer round-trips;
- explicit state-specific approval is required.

The agent-only Convergence Decision, successor-card lineage, and forced split/redesign after repeated non-approval remain binding. RC-001 is the first live proof: Round 1 found the ten-versus-eleven-bin verdict defect; Round 2 found a repair-created universal cutoff; Round 3 verified the replacement bound and closed. The three-way method chat remains active at Randy's request and now carries Codex's positive but cost-aware assessment.

## Transcript correction to remember

During Codex Session 26, the first RC-001 approval append matched a repeated footer and landed before Claude's Round-3 response. The misplaced message remains in the append-only transcript. A dated physical-EOF correction re-states the exact approval after Claude's handoff and is the authoritative chronological response. The concluded chat summary records the error. Do not silently normalize or relocate either block.

## Contract and already approved state

Amendments 1–6 remain in force. Current synchronized hashes:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

The real-arm donor-matching prose remains closed and same-state approved:

- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` Draft 6 — `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`.

§1–§15 of Claude's host-selection document remain same-state approved. The thirteen-candidate order remains pinned. The packet's current design-stage review remains closed at ten steps; archive-reading CLI/Step 11 does not exist.

## Next owner and next gate

Claude owns the next host-selection implementation: the archive-reading CLI and packet step 11. It must receive its own Review Card and new chat before any candidate is read. Codex should review that exact implementation when handed off, not begin candidate measurement independently.

The implementation must validate the already-declared inputs before computing anything: aligned ragged spike-time/depth slices, finite micrometre depths, pinned shared session clock and containment, unambiguous same-probe `max_electrode -> rel_y` mapping, and complete composition/provenance outputs. It must use the approved estimator rather than reimplementing the statistic.

## Separate gates — do not collapse

1. archive-reading drift CLI, its own Review Card/packet step, then candidate measurement down the pinned order;
2. exposure-schedule/placement specification, implementation, synthetic tests and same-state approval;
3. matcher implementation, exhaustive/mutation tests and same-state approval;
4. noise and post-rescaling effective-SNR host gates;
5. footprint/placement calibration and joint ten-placement gate;
6. exact candidate sites, T/K/N, U/Z/R, edge table, un-removed/post-removal matching outputs and IDs;
7. independent Tier A balance/manipulation approval;
8. generation authorization;
9. Rung 0/sorter execution authorization.

Reviewer edits, commits, downstream use and silence are not same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. The latest entry records RC-001's close and keeps the no-archive/no-result boundary.
- The Phase 1 director contract-review request remains open and non-blocking.
- Randy's method request is satisfied and the three-way chat stays active by his instruction.
- No Slot 8 verification-artifact update exists because there is no result.
- `agents/Codex/Progress Reports/Progress Report Session 24.md` is the latest cadence report; the next is Session 32.

## Machine state at closeout

The machine was under severe RAM pressure. Free RAM was 0.03 GiB at 02:05 PDT, recovered to 2.26 GiB before the small synthetic suite, and was 2.43 GiB at 02:14 PDT. GPU use was 1,097 of 16,311 MiB. Do not infer future headroom from these numbers; measure immediately before any new step. Nothing needing gigabytes was attempted.

`agents/Codex/Session Summaries/HumanReport26.md` contains the full work, evidence, files and reasoning.
