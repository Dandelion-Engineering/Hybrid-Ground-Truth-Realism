# Codex Human Report — Session 30

**Date:** 2026-08-15
**Phase:** Phase 2 — Execution
**Outcome:** RC-003 Round 1 returned **`Revisions Required`** on three blocking findings. Candidate access remains blocked; Claude owns the delta-only Round 2 response.

## Startup and controlling state

The automation gate named Codex, no `.agent-session.lock` existed, and the lock was created before project work. I read `AgentPrompt.md`, Project Details, both agents' continuity and latest reports, every chat summary, every active chat involving Codex, the superseding review playbook, the reproducibility-packet playbook, the live-run README playbook, RC-003, all seven candidate files, and the relevant approved §16 clock requirements and upstream reader interfaces.

RC-002 was already closed unapproved by Convergence Decision in Claude Session 30. Claude had repaired outside formal review and opened the one allowed successor, RC-003. The successor correctly retained all seven unapproved files for a full-artifact Round 1:

| File | Authenticated SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/archive_units.py` | `c1050b07a2d376a6c379ba491fd282355f8cd6fd02bf649c3da2750dd929850c` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `0f9c4ad114277ed5e0eb58e7efa5b10c9ba10b15eb1b8ad01812e5695d50302b` |
| `agents/Claude/tools/test_measure_host_drift.py` | `4b4308388322d0ad7e7c29792b13f428d04e9d92567dd550e172dcb9ebcf5006` |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `f9e0d732696c635b8f4c7d84bba71dc59570436ca7a8b3c6283180ec0f979274` |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc` |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f` |
| `Reproducibility Packet/README.md` | `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5` |

Before the acceptance run, the machine reported 18.78 GiB free physical memory of 31.67 GiB and 106.82 GiB free virtual memory. No dependency install was needed.

## Round 1 decision

I do not approve the exact RC-003 state. The exhaustive first-round ledger contains three blockers.

### RC-003-F1 — required conversion provenance is not authenticated

Approved §16 says the exact processed asset's conversion provenance and values must establish the documented common session clock, and an asset that cannot establish it is an input error before computation. The candidate instead documents provenance as recorded and “never gated on,” omits absent allowlisted fields, and includes an owner case named `case_provenance_is_recorded_not_required`.

An independent processed fixture with no provenance reached exit 0 and a passing drift verdict with an empty provenance record. This violates both the approved clock confirmation and RC-003's purpose: a bad or unauthenticated input must not become a drift verdict.

### RC-003-F2 — AP-series ownership uses substring matching

`select_ap_series()` associates streams using `probe in entry["name"]`. For requested `Probe00`, `ElectricalSeriesProbe000AP` is therefore accepted. An end-to-end raw fixture containing `ElectricalSeriesProbe000AP` and `ElectricalSeriesProbe01AP`, paired with otherwise valid `Probe00` processed data, reached a passing verdict using the wrong stream's timestamps.

This is RC-002-F3 carried onto a previously untested association boundary. Exact stream ownership must be established before the raw clock can authenticate the requested probe.

### RC-003-F3 — variable-length provenance spends before the ceiling can refuse it

For a variable-length HDF5 string, the file reports only the heap reference size. The candidate then executes `node[()]`, decodes the complete value and converts it to `str` before `plan_transfer()` and the `max_bytes` comparison.

With a two-million-character `general/source_script` and a one-byte ceiling, the local range reader touched **2,028,208 distinct bytes before raising** the promised ceiling error. Moving the read into preflight means an admitted plan can account for a completed spend; it does not make the spend knowable or enforceable before it occurs. That contradicts RC-003's explicit secondary purpose.

## Independent evidence

I added `agents/Codex/tools/probe_rc003_round1.py`, SHA-256 `df97e1a045ff488148433d48f4cdba4de9b2a27c87c03ba0db0b4921920d47f1`. It uses generated local HDF5 fixtures only, reads no archive or network resource, reproduces all three blockers and exits zero.

Its separate structure-size diagnostic did not establish another finding: 214,725 bytes of measured post-read unique Python objects sat below 396,209 bytes in the plan's structure-plus-array terms. I did not promote the broader raw-read ceiling boundary or this diagnostic into unsupported extra blockers.

## Verification on the exact candidate

| Check | Codex rerun result |
|---|---|
| Owner end-to-end archive-command harness | **279 checks, 0 failed, 12.8 s** |
| Repair-mutation harness | Green 279-check control; **16/16** mutations caught |
| Packet-checker mutation harness | Green control; **18/18** mutations caught |
| Packet runbook checker | 10 numbered steps agree; 1 command declared pending |
| Approved estimator harness | **103 checks, 0 failed** |
| Estimator claim probes | **3/3 passed** |
| RC-001 probe | 0 independent failures |
| Draft-16 safety probe | Exact prior digits retained |
| RC-002 Round-3 probe | Expected exit 1; both old underbound flags false |
| RC-003 Round-1 probe | All three blocking constructions reproduced; exit 0 |
| Compilation | Clean on the four changed candidate files and the new Codex probe |
| Console safety | `measure_host_drift.py` 6,763 UTF-8 bytes, checker 3,585; zero non-ASCII in both |

The green owner and mutation totals are useful regression evidence. They do not exercise the three constructions above and therefore do not support approval.

## Project and method records

- Updated RC-003's status, Round 1 ledger, verification evidence and outcome.
- Appended the exact review response to `chats/Claude-Codex/Bounded Archive Read Review/` after verifying its physical UTF-8 tail and line count.
- Appended a bounded method observation to `chats/Claude-Codex-Human/Review Method Change/` after the same EOF verification. Claude did not narrow the successor scope, and I accepted his queued mutation-harness note as a valid method observation.
- Added one lean, public-facing running-log entry to the root README because three pre-execution blocker constructions are genuinely noteworthy.
- Updated Codex's README and continuity. No count-based progress report is due until Session 32.

## Boundaries and next owner

No archive, network resource or candidate asset was read. No host is pinned, no drift value exists, and no donor selection, exposure schedule, placement configuration, Rung 0, generation or sorter execution occurred. No scientific result exists.

Claude owns one complete Round 2 response to RC-003-F1 through F3. That review is delta-only over the repairs and any response-created state. Candidate access remains blocked until RC-003 closes with explicit same-state `Approved` consensus. If this successor eventually reaches a non-approval terminal disposition on the same scoped purpose, method clause 5 forbids a second like-for-like successor and requires a split or redesign.
