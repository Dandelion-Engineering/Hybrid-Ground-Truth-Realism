# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 30 · 2026-08-15 21:25 PDT**

**Next Codex session will be Session 31. No count-based progress report is due until Session 32.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate archive, drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, exposure schedule, donor assignment, template array, Rung 0, hybrid generation or sorter run exists.

The public state remains `In Progress`. RC-001's drift specification is approved. RC-002 closed unapproved by Convergence Decision; its one allowed successor, RC-003, returned **`Revisions Required` at Round 1** on three blockers. Candidate reading remains blocked.

## RC-003 — Round 1 returned Revisions Required

`Review Cards/RC-003 Archive-Reading Drift Command, Bounded-Read Repair.md` is open. RC-002 closed `Revisions Required` with both agents' explicit agreement; Claude reproduced F1-R2, repaired outside formal review and opened the one successor method clause 4 allows. Codex authenticated all seven successor hashes, read the whole scoped candidate, completed the exhaustive Round 1 ledger and did not approve it.

Current RC-003 candidate state:

- `Reproducibility Packet/scripts/utils/archive_units.py` — `c1050b07a2d376a6c379ba491fd282355f8cd6fd02bf649c3da2750dd929850c`
- `Reproducibility Packet/scripts/measure_host_drift.py` — `0f9c4ad114277ed5e0eb58e7efa5b10c9ba10b15eb1b8ad01812e5695d50302b`
- `agents/Claude/tools/test_measure_host_drift.py` — `4b4308388322d0ad7e7c29792b13f428d04e9d92567dd550e172dcb9ebcf5006`
- `agents/Claude/tools/mutate_rc002_repairs.py` — `f9e0d732696c635b8f4c7d84bba71dc59570436ca7a8b3c6283180ec0f979274`
- `agents/Claude/tools/mutation_test_runbook_checker.py` — `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc`
- `Reproducibility Packet/scripts/check_runbook_consistency.py` — `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f`
- `Reproducibility Packet/README.md` — `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5`

## Round-1 positive evidence

- owner archive-command harness: **279/279**, 12.8 s in Codex's rerun;
- repair-mutation harness: green 279-check control and **16/16** caught;
- packet-checker mutation harness: green control and **18/18** caught;
- packet checker: ten numbered steps plus one checked pending command;
- approved estimator harness: **103/103**;
- estimator claim probes: **3/3**;
- Codex RC-001 probe: zero failures;
- safety-probe digits unchanged;
- RC-002 terminal probe returns its repaired expected exit 1 with both old underbound flags false;
- all changed candidate Python files and Codex's new RC-003 probe compile;
- console help remains ASCII-only.

These suites are useful regression evidence and remain green. They do not exercise the three independent constructions below and therefore do not establish approval.

## Complete Round-1 blocker ledger

### RC-003-F1 — required conversion provenance is not authenticated

Approved §16 requires the exact processed asset's conversion provenance and values to establish the documented common session clock, with absence or failure treated as an input error before computation. The candidate says provenance is recorded and “never gated on”; a processed fixture with no provenance reaches a passing verdict with an empty provenance record.

### RC-003-F2 — AP-series ownership uses substring matching

For requested `Probe00`, `select_ap_series()` accepts `ElectricalSeriesProbe000AP` because it uses `probe in entry["name"]`. An end-to-end fixture with `Probe000` and `Probe01` raw streams reaches a passing `Probe00` verdict using the wrong stream's timestamps. This carries RC-002-F3 onto a previously untested selector boundary.

### RC-003-F3 — variable-length provenance spends before refusal

When HDF5 does not expose a variable-length string's global-heap size, `source_provenance()` performs `node[()]`, decode and `str` before planning or ceiling enforcement. With a two-million-character provenance value and `max_bytes=1`, the reader touches **2,028,208 distinct bytes before raising** the promised refusal. Preflight accounting after materialization does not make cost knowable or enforceable before spend.

Independent evidence: `agents/Codex/tools/probe_rc003_round1.py`, SHA-256 `df97e1a045ff488148433d48f4cdba4de9b2a27c87c03ba0db0b4921920d47f1`. It uses generated local HDF5 files only and exits zero after reproducing all three. Its separate structure diagnostic did not establish another blocker.

## Next owner and review boundary

Claude owns one complete Round 2 response to F1–F3. Round 2 is delta-only over the repairs and response-created state. Candidate access remains blocked until explicit same-state approval. No Convergence Decision has fired on RC-003. If this successor eventually reaches a terminal non-approval disposition on the same purpose, method clause 5 forbids a second like-for-like successor and requires the work to split or redesign.

## RC-001 approved foundation

RC-001 closed `Approved` at Round 3 on:

- selection document Draft 24 — `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`;
- drift utility — `eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0`;
- owner harness — `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861`.

The gate uses eleven consecutive one-minute medians and checks both `Delta_10min <= L` and `Q95_null <= L`, first at 20 µm and then at the single predeclared 40 µm relaxation. It does not bound sub-minute motion; neither missed nor transmitted sub-minute motion is a one-way safety property. Per-unit audit values remain nonvoting.

## Contract and approved state

Amendments 1–6 remain in force. Synchronized contract hashes:

- `Claim Sheet.md` — `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md` — `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

The real-arm donor-matching prose remains same-state approved at Draft 6 `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`. Sections 1–15 of Claude's selection document remain approved. The thirteen-candidate order is pinned. None of those approvals authorizes archive reading, exact host-dependent configuration, placement, matching, generation or sorting.

## Public and method state

- Root `README.md` is State A / `In Progress`; its newest entry records the three RC-003 Round-1 blocker constructions.
- `chats/Claude-Codex/Archive-Reading Drift Command Review/` is concluded with RC-002 unapproved.
- `chats/Claude-Codex/Bounded Archive Read Review/Bounded Archive Read Review - Active.md` is active; Codex's full Round-1 ledger is appended and Claude owns Round 2.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` remains active by Randy's instruction and now records the successor-scope and mutation-evidence observations.
- The Phase-1 director contract-review request remains open and nonblocking. No new director action is needed.
- No Slot 8 verification-artifact update exists because there is no result.
- The next count-based progress report is Codex Session 32.

## Downstream gates remain separate

1. RC-003 Round 2 response and eventual archive-reader approval;
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

`agents/Codex/Session Summaries/HumanReport30.md` contains the complete evidence, decision, file list and reasoning.
