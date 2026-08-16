# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 32 · 2026-08-16 02:28 PDT**

**Next Codex session will be Session 33. The next count-based progress report is due in Session 40.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** RC-001's drift
specification and RC-003's bounded archive reader are approved. This removes the
implementation gate for the first separately governed candidate measurement; it
does not itself measure, approve, or pin a host.

No candidate archive, drift/noise/effective-SNR value, target-eligibility
manifest, host-specific pool, exposure schedule, donor assignment, template
array, Rung 0, hybrid generation, or sorter run exists. The public state remains
`In Progress`.

## RC-003 — approved and concluded

`Review Cards/RC-003 Archive-Reading Drift Command, Bounded-Read Repair.md`
closed **`Approved` at Round 3** on 2026-08-16. Claude and Codex explicitly
approved the same nine-file state; no Convergence Decision was needed. The
review transcript is concluded and summarized under
`chats/Claude-Codex/Bounded Archive Read Review/`.

Approved hashes:

- `Reproducibility Packet/scripts/utils/archive_units.py` — `96a31b3d46e18a7f387cc5d9d5c3fe37984f1346139477deb57f8f062ce1556e`
- `Reproducibility Packet/scripts/measure_host_drift.py` — `0bf08153fde8b48a6485596c6b8375920fe56d33a66fd0a35c41833f484335e5`
- `agents/Claude/tools/test_measure_host_drift.py` — `92e9091391e05b687225d1c0b7c1e7783bbb34cae194dcd8f5e11a6946e15286`
- `agents/Claude/tools/mutate_rc002_repairs.py` — `9955ef603ae0a7d7ebd094459d41b18933e32e52b0d3fb69a29b30cee8dc72f4`
- `agents/Claude/tools/verify_rc003_round1_repairs.py` — `2b7d9ef6eadae52f3c44ee603177efa474dcf692167278b67cbd50db6a79211d`
- `agents/Claude/tools/verify_rc003_round2_repairs.py` — `9fb49fe8bfc098e25490e98cb596c13e20ebff7af3cac0c65421e468092112a0`
- `agents/Claude/tools/mutation_test_runbook_checker.py` — `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc`
- `Reproducibility Packet/scripts/check_runbook_consistency.py` — `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f`
- `Reproducibility Packet/README.md` — `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5`

The approval establishes:

- whole affirmative `general/source_script` authentication on both exact assets;
- matching raw/processed NeuroConv versions before a drift payload;
- exact probe-series ownership rather than substring association;
- separate logical request, distinct cache-block transfer, and actual total-byte
  accounting;
- a nested outer transfer ceiling covering the complete read and refusing the
  next new block before it moves;
- accurate reporting for optional refused or truncated provenance paths.

Codex's independent evidence on the exact state was 382/382 owner checks, a
green control plus 26/26 repair mutations caught, a green control plus 18/18
checker mutations caught, both focused repair verifiers, ten packet runbook
steps plus one declared pending command, compilation, and `git diff --check`.
A retry construction was examined and ruled out: retries are deliberately not
new distinct blocks, while actual total traffic remains separately reported in
`io.bytes`.

## Immediate next owner and action

Claude owns the first real candidate read. The pinned first attempt is:

- subject/probe: **CSHL047 / Probe01**;
- session: `b52182e7-39f6-4914-9717-136db589706e`;
- gate: `--gate strict`;
- output state: **plan-only**;
- prerequisite: measure fresh machine headroom before execution.

That command is separately governed. A refusal is a valid result of the attempt.
A successful plan-only record still does not pin or approve the host; it only
supplies evidence for the next gate. Do not skip the pinned order or carry this
session's machine-headroom reading forward.

## Approved foundation and contract

RC-001 closed `Approved` on selection Draft 24 `c35987fe…`, drift utility
`eace4cd35…`, and owner harness `946df906…`. The gate uses eleven consecutive
one-minute medians and checks both `Delta_10min <= L` and `Q95_null <= L`, first
at 20 µm and then at the single predeclared 40 µm relaxation. It does not bound
sub-minute motion; neither missed nor transmitted sub-minute motion is a
one-way safety property. Per-unit audit values remain nonvoting.

Amendments 1–6 remain in force. Contract hashes remain:

- `Claim Sheet.md` — `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md` — `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

The real-arm donor-matching prose remains same-state approved at Draft 6
`51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`.
Sections 1–15 of Claude's selection document remain approved. The
thirteen-candidate order is pinned. None of those approvals authorizes exact
host-dependent placement or matching, generation, or sorting.

## Public, method, and reporting state

- Root `README.md` is State A / `In Progress`; its newest entry records RC-003
  approval and states that no candidate or result exists.
- `chats/Claude-Codex/Bounded Archive Read Review/Bounded Archive Read Review -
  Concluded.md` contains the exact approval; its sibling `Summary.md` is current.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md`
  remains active by Randy's instruction. It records that the successor reached
  approval at its last allowed round and that the cumulative bounded review
  method worked. No Randy decision is currently required.
- `agents/Codex/Progress Reports/Progress Report Session 32.md` is the current
  director-facing cadence report.
- The Phase-1 director contract-review request remains open and nonblocking. No
  new director action is needed.
- No Slot 8 verification-artifact update exists because there is no result.

## Downstream gates remain separate

1. first candidate measurement in the pinned order;
2. exposure-schedule/placement specification, implementation, tests, and approval;
3. matcher implementation, exhaustive/mutation tests, and approval;
4. noise and post-rescaling effective-SNR host gates;
5. footprint/placement calibration and joint ten-placement gate;
6. exact candidate sites, T/K/N, U/Z/R, edge table, matching outputs, and IDs;
7. independent Tier A balance/manipulation approval;
8. generation authorization;
9. Rung 0/sorter execution authorization.

`agents/Codex/Session Summaries/HumanReport32.md` contains the complete final
review evidence, decision, file list, and boundary reasoning.
