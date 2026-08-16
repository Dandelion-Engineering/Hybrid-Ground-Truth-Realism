# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 31 · 2026-08-15 23:24 PDT**

**Next Codex session will be Session 32. A count-based progress report is due in Session 32.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned.
No candidate archive, drift/noise/effective-SNR value, target-eligibility manifest,
host-specific pool, exposure schedule, donor assignment, template array, Rung 0,
hybrid generation, or sorter run exists.

The public state remains `In Progress`. RC-001's drift specification is approved.
RC-002 closed unapproved by Convergence Decision. Its one allowed successor,
RC-003, returned **`Revisions Required` at Round 2**. Candidate reading remains
blocked.

## RC-003 — Round 2 returned Revisions Required

`Review Cards/RC-003 Archive-Reading Drift Command, Bounded-Read Repair.md` is
open. Claude answered all three Round-1 findings and approved the response state.
Codex authenticated all eight declared hashes and performed the required
delta-only review. F2 passes, while F1 and F3 remain blocking. Codex does not
approve the exact Round-2 response state.

Round-2 response hashes:

- `Reproducibility Packet/scripts/utils/archive_units.py` — `787d53ab87069280583f3c4ec0264eb686033535402368d5f2bddfeec0a0d814`
- `Reproducibility Packet/scripts/measure_host_drift.py` — `1941c577b79a7e1d22ab8e25ff41791d1b2852050c980526b6685340bae67ae5`
- `agents/Claude/tools/test_measure_host_drift.py` — `326314a530355c27b3689919acaa9c7497b7605fa7e0de22d26212afe0b79aee`
- `agents/Claude/tools/mutate_rc002_repairs.py` — `1e5cffcd6856da215a197528bc66ba62b64d1546d276dcf5d291310bb765525d`
- `agents/Claude/tools/verify_rc003_round1_repairs.py` — `43402d14245965bfa42d47be1c54a4d80c57b4532e7e677f60e4bfccf20a648c`
- `agents/Claude/tools/mutation_test_runbook_checker.py` — `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc`
- `Reproducibility Packet/scripts/check_runbook_consistency.py` — `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f`
- `Reproducibility Packet/README.md` — `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5`

## Round-2 positive evidence

- owner archive-command harness: **325/325**, 13.7 s in Codex's rerun;
- repair-mutation harness: green 325-check control and **20/20** caught;
- owner Round-1 repair verification: all three constructions refused, including
  the F3 small-block construction at 33,456 touched bytes;
- packet checker: ten numbered steps agree plus one declared pending command;
- all changed, response-created, and reviewer Python files compile;
- exact series decomposition refuses `ElectricalSeriesProbe000AP` for requested
  `Probe00`, so RC-003-F2 passes.

The packet-checker mutation harness and estimator state were explicitly unchanged
and were not re-audited in this delta-only pass. Claude's response records their
green 18/18 and 103/103 evidence.

## Remaining Round-2 ledger

### RC-003-F1 — token presence is not provenance authentication

`authenticate_provenance()` requires only the case-insensitive substring
`neuroconv`. A processed source script saying `This asset was NOT created using
NeuroConv; exported by LocalTool v3` reaches a verdict. Raw `NeuroConv v0.9.2`
paired with processed `NeuroConv v0.9.1` also reaches a verdict with
`values_agree = false`; the owner suite expressly establishes that disagreement
is not gated. The approved common-clock contract requires the exact assets'
provenance and values to authenticate a positive shared conversion state before
computation, not merely for both strings to contain a tool name.

### RC-003-F2 — passes

The new exact series-name decomposition closes the Round-1 substring association
path. `Probe000` no longer supplies `Probe00`'s clock.

### RC-003-F3 — logical requests do not bound real block transfers

`BoundedReader` charges the length h5py asks it for, but `RemoteFile` can expand
that request to a full range-cache block before returning. With the default
1 MiB block and the two-million-character fixture, **2,081,456 distinct bytes
transfer before refusal** under the claimed **65,536-byte** provenance budget.
The stated per-path budget and pre-spend transfer property therefore remain
false under the command's default reader.

### RC-003-E1 — open, non-blocking wording

The response says the records file carries provenance values “in full,” but
optional paths may carry refusal or truncation markers. Only required,
authenticated `source_script` is necessarily complete at verdict.

Independent evidence: `agents/Codex/tools/probe_rc003_round2.py`, SHA-256
`d67bf2616b2b10ef6e7f3f34ad324cdfa327787eb8af5b71cb4f7fd1de4e9ef2`.
It uses generated local HDF5 fixtures only, reads no archive, network resource,
or candidate asset, reproduces both blockers, and exits zero.

## Next owner and review boundary

Claude owns the **final Round 3 response** to F1 and F3 plus the non-blocking E1
wording repair. Round 3 is delta-only over the repairs and response-created state.
Candidate access remains blocked until explicit same-state approval. No
Convergence Decision has fired on RC-003. If Round 3 does not reach approval,
method clause 5 forbids a second like-for-like successor and requires the work to
split or redesign with the changed boundary named.

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
thirteen-candidate order is pinned. None of those approvals authorizes archive
reading, exact host-dependent configuration, placement, matching, generation,
or sorting.

## Public and method state

- Root `README.md` is State A / `In Progress`; its newest entry records the two
  remaining RC-003 Round-2 blocker constructions.
- `chats/Claude-Codex/Bounded Archive Read Review/Bounded Archive Read Review -
  Active.md` is active; the Round-2 verdict is appended and Claude owns Round 3.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md`
  remains active by Randy's instruction and records the Round-2 method
  observation. No Randy decision is currently required.
- The Phase-1 director contract-review request remains open and nonblocking. No
  new director action is needed.
- No Slot 8 verification-artifact update exists because there is no result.
- The next count-based progress report is due in Codex Session 32.

## Downstream gates remain separate

1. RC-003 final Round 3 response and archive-reader approval or clause-5 redesign;
2. candidate measurement in pinned order;
3. exposure-schedule/placement specification, implementation, tests, and approval;
4. matcher implementation, exhaustive/mutation tests, and approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact candidate sites, T/K/N, U/Z/R, edge table, matching outputs, and IDs;
8. independent Tier A balance/manipulation approval;
9. generation authorization;
10. Rung 0/sorter execution authorization.

Measure machine headroom before any future heavy step. Do not infer it from a
previous session.

`agents/Codex/Session Summaries/HumanReport31.md` contains the complete evidence,
decision, file list, and reasoning.
