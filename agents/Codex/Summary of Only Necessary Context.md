# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 25 · 2026-08-15 00:17 PDT**

**Next Codex session will be Session 26. No count-based progress report is due until Session 32.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate archive, drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, rendered edge table, exposure schedule, selected donor, template array, Rung 0, hybrid generation or sorter run exists.

The public state remains `In Progress`. The next executable step is still blocked on exact pre-measurement design approval.

## Review method now governing

`Playbooks/review-cycle.md` opens with the director's superseding Review Card method:

- one stable candidate and written purpose/scope/acceptance boundary;
- Round 1 is the only full-artifact pass and records one complete numbered ledger;
- later rounds are delta-only: recorded findings and response-created regressions;
- at most three owner-reviewer round-trips;
- explicit state-specific approval is required.

Randy directed the agents to replace ordinary human escalation because he is asynchronous. Codex's five-clause agent-only **Convergence Decision** is now accepted by Claude and written into the playbook:

1. at a trigger, each agent writes the minimum shippable claim, controlling evidence, strongest contrary evidence and one acceptable safe disposition;
2. evidence controls what may ship; uncertainty on a blocker never becomes approval;
3. both agents explicitly agree on `Revisions Required`, `Split/Redesign Required`, or `Approved with Follow-ups` even if beliefs differ;
4. one successor card names `Supersedes:` and the material pre-review change;
5. a repeated same-purpose non-approval forces a real split/redesign rather than another card reset.

Claude's two applications are accepted: both statements and the terminal disposition live in the Review Card, and director-only questions keep the non-blocking `director_requests.md` route. Codex Session 25 mechanically corrected one stale quality-checklist reference from human triage to the Convergence Decision.

## RC-001 — Round 2 complete, candidate not approved

- **Card:** `Review Cards/RC-001 Tier A Selection Section 16.md`
- **Chat:** `chats/Claude-Codex/Tier A Selection Section 16 Review/Tier A Selection Section 16 Review - Active.md`
- **Current disposition:** **Revisions Required; open on Claude for the Round-3 owner response.**

Owner-returned Round-2 hashes:

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 23 — `e7dcfc54f495c96f62c4994cfa8178882edaba38aa0b48a15c3fcb107534b5bf`
- `Reproducibility Packet/scripts/utils/band_drift.py` — `4ac9fa56dc7a2035d1f9b037b9010ae448fc1c621f92ea93876db1c1fc06ab19`
- `agents/Claude/tools/test_band_drift.py` — `e2e63a037ee81886b01779535c22ce296502bc3a132ee3f77f9ad6f345869420`

Codex mechanically corrected two reciprocal typos, `9/10` → `10/9`, in the selection document. Its current reviewer-state SHA-256 is `90aebcb50a7cb6da50773519d41295b6a0ed4f22f76d978b123fddb8145ddf01`; utility and harness are unchanged.

### F1 — eleven-bin implementation verified

The repaired statistic uses eleven consecutive one-minute bin medians:

- smooth common 2.1 µm/min ramp: `Delta_10min = 21.000 µm`, `Q95_null = 18.717 µm`; strict gate fails;
- off-grid level construction: `Delta_10min = 30.000 µm`, `Q95_null = 0`; strict gate fails;
- forty randomized observations and a nine-permutation null match an independent reference;
- owner harness passes 96/96.

The eleven-bin change is a tightening relative to ten bins. The original point-mass within-bin fixture remains valid at `0/0 µm`.

### F1-R1 — blocking response regression

Draft 23 promotes the point-mass fixture into a universal rule: any displacement affecting fewer than half of a bin's spikes allegedly leaves the median exactly fixed, so the gate is blind below half.

Counterexample in `agents/Codex/tools/probe_rc001_round1.py`:

- five units, 31 full bins, 100 spikes per unit/bin;
- each unaffected bin has depths `[0 × 49, 1 × 2, 100 × 49]`, offset per unit;
- in one bin, the first 49% are shifted by `+30 µm`;
- median moves from `1` to `30 µm`;
- shipped utility reports `Delta_10min = 29.000 µm`, above the strict gate.

The hard cutoff is therefore not a general property of sample medians. This is a response-created regression, not a pre-existing LATE-BLOCKER. The local repair must constrain the `0/15/30 µm` result to its equal-baseline fixture and state the actual general boundary without a new direction claim: sub-minute motion has no guaranteed detectability under bin medians, and its transmission depends on the within-bin depth distribution and episode timing. `Delta_10min` remains not a bound on sub-minute motion.

### F2 and F3 verified

- F2: the unit-count direction is withdrawn. At fixed 40% moving fraction, seed 7025 reports `12.192`, `11.529`, `14.190 µm` at 10/20/40 units. The replacement 41-unit masking fixture passes at `14.941/7.125 µm` without claiming a direction.
- F3: the text now gives the valid sample-median invariant — observations can move a realized median, but the statistic does not mechanically accumulate a positive term per spike.

### Validation state

- owner harness: 96/96;
- claim probes: 3/3;
- both safety counterexamples reproduce;
- packet runbook checker: 10/10;
- updated Codex independent probe: 12/12, SHA-256 `a29144e247ec5a845bb67699b9e8f5d6a4c89ab3d5458743254e2f223dae33cc`;
- renamed safety probe: SHA-256 `d1c9220dc0f0890744d920638210f501abdc9b53b84256ef89afbc59e6bca6ac`.

## Round-3 boundary

Round 3 is the final exact-state opportunity. Review only the F1-R1 repair and regressions introduced by that repair; do not re-audit unchanged §16 from scratch.

If the exact returned state resolves the regression, Codex may approve it explicitly and close RC-001 with Claude's matching approval. If Round 3 does not close, run the agent-only Convergence Decision; do not park on Randy.

The archive-reading CLI and every candidate measurement remain blocked until RC-001 closes.

## Contract and approved state

Amendments 1–6 remain in force. Current synchronized hashes:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

The real-arm donor-matching prose remains closed and same-state approved:

- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` Draft 6 — `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`

§1–§15 of Claude's host-selection document remain outside RC-001 and same-state approved. The thirteen-candidate order remains pinned. The packet's current design-stage review remains closed at ten steps; the archive-reading CLI/Step 11 does not exist.

## Separate gates — do not collapse

1. Claude's Round-3 F1-R1 response and Codex's final delta-only exact-state verification;
2. archive-reading drift CLI, its own Review Card/packet step, then candidate measurement down the pinned order;
3. exposure-schedule/placement specification, implementation, synthetic tests and same-state approval;
4. matcher implementation, exhaustive/mutation tests and same-state approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact candidate sites, T/K/N, U/Z/R, edge table, un-removed/post-removal matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. generation authorization;
10. Rung 0/sorter execution authorization.

Reviewer edits, commits, downstream use and silence are not same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. Codex Session 25 appended a forward correction: the eleven-summary repair holds, but the universal half-minute cutoff does not.
- The Phase 1 director contract-review request remains open and non-blocking.
- Randy's method request is satisfied and the three-way chat stays active by his instruction.
- No Slot 8 verification-artifact update exists because there is no result.
- `agents/Codex/Progress Reports/Progress Report Session 24.md` is the latest count-based report; the next cadence report is Session 32.

## Append-only evidence

- RC-001 transcript pre-write: 17,708 bytes, SHA-256 `f16b356ac1f22264b4e6e653711ad16c970880fac847c23018cc16c81a23a4bf`; the new file preserves that exact prefix and contains one Codex Session 25 header after the prior 104 lines.
- Three-way transcript pre-write: 20,453 bytes, SHA-256 `3606c6fd1c36a3bc3774a073eed6ceba1ed88f794ed387be6dd99e71d58857b0`; the new file preserves that exact prefix and contains one Codex Session 25 header after the prior 154 lines.

`agents/Codex/Session Summaries/HumanReport25.md` contains the full work and reasoning.
