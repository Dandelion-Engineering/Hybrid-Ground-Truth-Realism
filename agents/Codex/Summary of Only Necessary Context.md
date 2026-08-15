# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 28 · 2026-08-15 06:30 PDT**

**Next Codex session will be Session 29. No count-based progress report is due until Session 32.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate archive, drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, exposure schedule, donor assignment, template array, Rung 0, hybrid generation or sorter run exists.

The public state remains `In Progress`. RC-001's drift specification is approved. RC-002's archive-reading implementation is **Revisions Required after Round 2**. Candidate reading remains blocked until explicit same-state approval of a corrected candidate.

## RC-002 — Round 2 Revisions Required

`Review Cards/RC-002 Archive-Reading Drift Command.md` is open. Claude's Session-28 response accepted all Round-1 findings. Codex authenticated the response and completed the delta-only reviewer pass.

Exact six-file response state reviewed, untouched by Codex:

- `Reproducibility Packet/scripts/utils/archive_units.py` — `19dbcc765cd5a64b41d370c642c318055cfe619cd5d4beb40dc0b69ccac132ea`
- `Reproducibility Packet/scripts/measure_host_drift.py` — `7f99419ee202dd189d9f7a96d36d6d73c31723b5da21ee34cbe889d80c8ca2d5`
- `agents/Claude/tools/test_measure_host_drift.py` — `ad4985cb83eaa6be135d4e0db88785cfb4aeeb20cd4de03c131aae1c81d5a798`
- `agents/Claude/tools/mutate_rc002_repairs.py` — `89785076ffb4856264b761d523a2b897341bc2024b63fa7803bcb4bf4e6f1b12`
- `Reproducibility Packet/scripts/check_runbook_consistency.py` — `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f`
- `Reproducibility Packet/README.md` — `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5`

### Blocking ledger

1. **F1-R1a — fragmented-chunk transfer underbound.** The response's chunk fallback treats selected HDF5 chunks as one contiguous file span and pays fixed-block alignment once. In a valid generated file whose ragged-column chunks are physically separated by unrelated chunks, the plan reports `241,664` bytes while the reader transfers `327,680`. A `284,672`-byte ceiling is admitted and exceeded. Repair with actual per-chunk byte ranges/distinct blocks or a genuinely conservative per-chunk bound, and retain the fragmented fixture.
2. **F1-R1b — separately checked live memory.** The fixed-block cache remains resident while converted arrays accumulate. On the standard fixture, a ceiling of `81,361` passes, yet `81,360` cached bytes coexist with `57,600` bytes of returned float64 arrays: at least `138,960` live bytes before other metadata and temporaries. Replace separate ceiling checks with one conservative combined peak-resident bound and do not call a partial array count exact process peak memory.
3. **F2-R1 — schema-invalid ragged index dtype.** NWB `Units/spike_times_index` is an HDMF `VectorIndex`, which requires unsigned-integer storage. Whole-valued floating-point ragged indexes remain malformed. Require integer storage dtype for `spike_times_index` and `spike_depths_index` before conversion. This finding does not require rejecting a whole-valued floating custom `max_electrode` column if that compatibility choice remains explicit and reported.

### Accepted repairs and follow-ups

- **F3 passes:** raw/processed subject and paired-stem identity plus AP timestamp/data-axis equality are checked.
- **F4 passes:** the runtime anatomy-gap control is gone and the predeclared finite 40 µm check is pinned.
- **F5 passes:** the command lives in the packet, runs directly, and the checker exposes a narrow validated `PENDING_STEP` state until first real execution.
- **F6 mostly passes:** stale outputs are cleared and optional-record wording is conditional. Nonblocking F6-R1 remains because `abspath` equality accepts case-only aliases on case-insensitive Windows filesystems; normalize/resolve identity before first real execution.
- **E1 is nonblocking:** the repair-mutation harness has eight entries but no F5 mutation. Add one or narrow the statement that it removes every finding's repair. Direct F5 tests pass.

### Independent and owner evidence

`agents/Codex/tools/probe_rc002_round2.py`, SHA-256 `ea806c590ed5f92764175c3ef798aa15bcea0613386a68c752c58c2ddc070781`, reproduces both F1 blockers, the Windows alias follow-up, and the absent F5 mutation using generated local fixtures only. It reads no archive or candidate asset.

Positive evidence retained:

- archive-command owner harness: 231 checks, zero failures;
- repair-mutation harness: unmutated control green, all eight listed mutations caught;
- approved estimator harness: 103/103;
- estimator claim probes: 3/3;
- Codex RC-001 probe: zero failures;
- safety-probe digits unchanged;
- packet checker: ten steps plus one pending script;
- checker mutation harness: green control and 15/15 mutations caught;
- moved command `--help` and Python compilation: clean.

Aggregate green evidence does not resolve the three blockers. The NWB/HDMF schema source is recorded in `agents/Codex/references.md`.

## Next owner and exact next gate

Claude owns the **final Round 3 owner response**. The active handoff is `chats/Claude-Codex/Archive-Reading Drift Command Review/Archive-Reading Drift Command Review - Active.md`.

Codex's next pass, if requested, must authenticate the exact revised state and check only the Round-2 ledger plus response-created regressions. If the final response does not remove the existing blockers, or if Codex finds a new blocker, do not begin another ordinary revision round: write the card's Convergence Decision and choose `Approve`, `Approve with Follow-up`, or `Reject and Redesign` under `Playbooks/review-cycle.md`. Silence, a green harness, reviewer edits, handoff or downstream use are not approval. Do not read a real candidate before explicit approval.

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

The real-arm donor-matching prose remains closed and same-state approved at Draft 6 `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`. Sections 1–15 of Claude's selection document remain approved. The thirteen-candidate order is pinned. None of those approvals authorizes archive reading, exact host-dependent configuration, placement, matching, generation or sorting.

## Review-method state

The bounded Review Card method in `Playbooks/review-cycle.md` controls: stable exact candidate plus Purpose/scope/acceptance boundary; one exhaustive Round 1 and complete numbered ledger; delta-only later rounds; at most three owner-reviewer round-trips; and explicit state-specific approval.

Session 28's method feedback is in the active three-way chat. Response-created files were handled cleanly by explicit declaration and the delta-only rule. Mutation testing was useful but did not substitute for an independent property construction: the mutation harness passed while the fragmented-layout F1 defect remained, and its evidence description exceeded its actual F5 coverage. No playbook amendment was made mid-card.

## Public and director state

- Root `README.md` is State A / `In Progress`. Its newest entry records the Round-2 ceiling failures and continued block before archive access.
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

Measure machine headroom before any future heavy step. Do not infer it from a previous session.

`agents/Codex/Session Summaries/HumanReport28.md` contains the full evidence, decisions, file list and reasoning.
