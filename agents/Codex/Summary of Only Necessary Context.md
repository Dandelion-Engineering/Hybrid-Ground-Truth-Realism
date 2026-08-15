# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 27 · 2026-08-15 04:20 PDT**

**Next Codex session will be Session 28. No count-based progress report is due until Session 32.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate archive, drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, exposure schedule, donor assignment, template array, Rung 0, hybrid generation or sorter run exists.

The public state remains `In Progress`. RC-001's drift specification is approved. RC-002's archive-reading implementation exists but is **Revisions Required** after Round 1. Candidate reading remains blocked until explicit same-state approval of a corrected candidate.

## RC-002 — Round 1 Revisions Required

`Review Cards/RC-002 Archive-Reading Drift Command.md` is open. Codex completed the card's only exhaustive full-artifact pass and returned one complete ledger on 2026-08-15.

Exact candidate reviewed, untouched by Codex:

- `Reproducibility Packet/scripts/utils/archive_units.py` — `c5c21cb9a2e0f9cedd0f1cff7e98886cb77ccdd21e2ad763422a7b44f3146f12`
- `agents/Claude/tools/measure_host_drift.py` — `c71a5d9311b0785dcff5469e9c698f0f208946cafb00b32dd4eb0bddbda93cfb`
- `agents/Claude/tools/test_measure_host_drift.py` — `6ff3d26ce64016efabdf71aaab93c9a0d71526f37fdcbedae457c438f50a3b39`

### Blocking ledger

1. **Resource accounting:** the preflight counts logical HDF5 payload, not actual fixed-block network/cache bytes or peak `float64` materialization. A 57,600-byte logical plan passed a 60,000-byte ceiling while the reader transferred 81,360 bytes. Define and enforce the relevant logical, transfer/cache and peak-memory limits separately.
2. **Structural integrality and lengths:** ragged offsets and `max_electrode` are coerced to integers before validation, so fractional values silently truncate and reach a verdict. Validate source dtype/integrality and exact lengths of every unit-indexed scalar before conversion/indexing.
3. **Asset and clock identity:** raw-subject A and processed-subject B can pair under a shared session UUID, and AP data with 1,000 time samples plus 999 timestamps can reach a verdict. Require declared raw/processed subject/session/stem identity and `n_timestamps == data_time_axis`.
4. **Anatomy threshold:** arbitrary `--max-gap-um` changes the graded population and is not a predeclared scientific gate. Implement the exact finite 40 µm CA1 step check; do not expose a tuning knob.
5. **Packet placement/standalone execution:** the command is outside the Reproducibility Packet and direct invocation fails with `ModuleNotFoundError: screen_host_timing`. Move it into the packet and make its documented invocation runnable before approval or candidate access. Sibling packet-module imports are allowed by this card.

Tracked nonblocking F6: successful outputs survive a later input-error rerun at the same paths, and report/record paths may collide. Claude must respond explicitly and the command/runbook should define safe output ownership, but this may remain a documented follow-up if it does not affect the corrected measurement candidate.

### Independent evidence

`agents/Codex/tools/probe_rc002_round1.py`, SHA-256 `e4197bcaabb523929b34bc340b4d0419e0fc154c51618f08fd56d92beecbd27a`, reproduces seven synthetic constructions: fractional offsets; fractional peak electrodes; AP length mismatch; subject mismatch; transfer greater than logical plan; stale prior outputs; and a large gap merging CA1 islands. It uses local synthetic HDF5 fixtures only and reads no archive or candidate asset.

Positive evidence retained:

- archive-command owner harness: 163 checks, zero failures;
- approved estimator harness: 103/103;
- claim probes: 3/3;
- Codex RC-001 probe: 13/13 including 93,184 exhaustive cases;
- packet runbook checker: 10/10;
- Python compilation clean.

The explicit strict/relaxed gate selection and reuse of the approved estimator are accepted. Packet runbook Step 11 text may still follow executable approval. Aggregate green evidence, however, does not resolve F1–F5.

## Next owner and exact next gate

Claude owns the response to F1–F6 and the exact revised candidate. The active handoff is `chats/Claude-Codex/Archive-Reading Drift Command Review/Archive-Reading Drift Command Review - Active.md`.

If Claude returns a revision, Codex Round 2 is **delta-only**: authenticate the new exact state, check each ledger response, check response-created regressions, and issue one explicit state-specific outcome. Do not repeat an unconstrained full review and do not read a real candidate. Silence, a green harness, reviewer edits, handoff or downstream use are not approval.

## RC-001 approved foundation

RC-001 closed `Approved` at Round 3 on these exact states:

- selection document Draft 24 — `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`;
- drift utility — `eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0`;
- owner harness — `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861`.

The gate uses eleven consecutive one-minute medians and checks both `Delta_10min <= L` and `Q95_null <= L`, first at 20 µm and then at the single predeclared 40 µm relaxation. It does not bound sub-minute motion; within-bin transmission depends on depth ranks and episode placement. Neither missed nor transmitted sub-minute motion is a one-way safety property. Per-unit audit values remain nonvoting.

## Contract and approved state

Amendments 1–6 remain in force. Synchronized contract hashes:

- `Claim Sheet.md` — `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md` — `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

The real-arm donor-matching prose remains closed and same-state approved at Draft 6 `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`. §1–§15 of Claude's selection document remain approved. The thirteen-candidate order is pinned. None of those approvals authorizes archive reading, exact host-dependent configuration, placement, matching, generation or sorting.

## Review-method state

The bounded Review Card method in `Playbooks/review-cycle.md` controls:

- stable exact candidate plus Purpose/scope/acceptance boundary;
- one exhaustive Round 1 and complete numbered ledger;
- delta-only later rounds;
- at most three owner-reviewer round-trips;
- explicit state-specific approval.

The three-way method chat remains active at Randy's request. Codex's Session-27 feedback is positive but cost-aware: RC-002 produced a finite complete ledger, while the card Purpose still had to control where narrow wording would otherwise miss refusal and reproducibility failures.

## Public and director state

- Root `README.md` is State A / `In Progress`. Its newest entry forward-corrects the prior exact-byte claim and records RC-002's return before archive access.
- The Phase-1 director contract-review request remains open and nonblocking.
- Randy's review-method request is satisfied; the three-way chat remains active by instruction.
- No Slot 8 verification-artifact update exists because there is no result.
- `agents/Codex/Progress Reports/Progress Report Session 24.md` is the latest cadence report; the next is Session 32.

## Downstream gates remain separate

1. corrected archive-reading CLI and explicit RC-002 approval;
2. candidate measurement in pinned order;
3. exposure-schedule/placement specification, implementation, tests and approval;
4. matcher implementation, exhaustive/mutation tests and approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact candidate sites, T/K/N, U/Z/R, edge table, matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. generation authorization;
10. Rung 0/sorter execution authorization.

## Machine state at closeout

At 04:20 PDT, free RAM was about 0.03 of 31.67 GiB; GPU use was 1,085 of 16,311 MiB. No heavy work followed that observation. Measure again before any future step and do not infer headroom from these numbers.

`agents/Codex/Session Summaries/HumanReport27.md` contains the full evidence, decisions, file list and reasoning.
