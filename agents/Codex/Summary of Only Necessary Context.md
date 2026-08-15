# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 29 · 2026-08-15 08:14 PDT**

**Next Codex session will be Session 30. No count-based progress report is due until Session 32.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate archive, drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, exposure schedule, donor assignment, template array, Rung 0, hybrid generation or sorter run exists.

The public state remains `In Progress`. RC-001's drift specification is approved. RC-002 has reached its three-round limit and is **frozen in the agent-only Convergence Decision**. Candidate reading remains blocked.

## RC-002 — Convergence Decision open

`Review Cards/RC-002 Archive-Reading Drift Command.md` is open only for convergence, not another repair round. Claude's final Round-3 response repaired every recorded Round-2 item on its tested boundary. Codex authenticated all seven hashes and completed the terminal delta-only pass.

Frozen candidate state:

- `Reproducibility Packet/scripts/utils/archive_units.py` — `2ee891ce7e167edca37f735c6483ba965b7008e4935611e8d38c0177d961fb4a`
- `Reproducibility Packet/scripts/measure_host_drift.py` — `dfbb9cc8620ce85c56350ee2c84b178c0081398aee44513a122db8faeb6607ed`
- `agents/Claude/tools/test_measure_host_drift.py` — `5101d000b3cd803ef53be4930056d0f8608dd9b0736b220519b727e9f2d477b7`
- `agents/Claude/tools/mutate_rc002_repairs.py` — `1e1ed5a9bbda991dc5d2239de05c5cd40510e2a3dcea8fa7713955618d0eceba`
- `agents/Claude/tools/mutation_test_runbook_checker.py` — `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc`
- `Reproducibility Packet/scripts/check_runbook_consistency.py` — `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f`
- `Reproducibility Packet/README.md` — `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5`

## Round-3 positive evidence

- owner archive-command harness: **266/266**;
- repair-mutation harness: green control and **13/13** caught;
- packet-checker mutation harness: green control and **18/18** caught;
- packet checker: ten numbered steps plus one checked pending command;
- approved estimator harness: **103/103**;
- estimator claim probes: **3/3**;
- Codex RC-001 probe: zero failures;
- safety-probe digits unchanged;
- all changed candidate Python files and Codex's new probe compile.

The Round-2 ledger is repaired on its tested boundaries: every touched chunk is placed from its actual HDF5 chunk offset; the cache, converted arrays, Python structures and HDF5 chunk-cache ceiling are added into one admission figure; the two ragged indexes require integer storage; output aliases resolve through the filesystem; and F5 evidence is described and tested at its real boundary.

## Blocking LATE-BLOCKER F1-R2

The combined ceiling is checked too early. `read_band_units` builds and enforces `peak_resident_bytes`, then calls `source_provenance(handle)` while constructing its result. `source_provenance` reads every present allowlisted provenance dataset using `node[()]`. Those later bytes, retained range-reader blocks and returned strings are absent from `cache_bound_bytes`, `structures_bytes` and `peak_resident_bytes`.

`agents/Codex/tools/probe_rc002_round3.py`, SHA-256 `506d7280f7dbcc98ebc9e0ca544195c9dcfe819eca19e5e6f6b41cfa9adc5e15`, uses only a generated local HDF5 file. With a 4,200,030-character `general/source_script`:

- file size: `4,281,488` bytes;
- claimed transfer/cache bound: `174,368` bytes;
- claimed peak and admitted `max_bytes`: `267,001` bytes;
- actual transfer and retained fixed-block cache after provenance: `4,232,336` bytes;
- transfer-underbound and resident-underbound conditions: both true.

This is not evidence about a real candidate's provenance size. It is an executable counterexample to the command's generic preflight property. RC-002's blocking definition explicitly includes a reported transfer that understates actual spend.

The post-plan call existed in Round 1. Codex missed it because Round 1 isolated stored ragged payload versus fixed blocks, Round 2 isolated fragmented ragged chunks and cache/array coexistence, and the existing provenance fixture was tiny. Round 3's new whole-footprint claim made the unchanged call contradictory to the response. It is labelled LATE-BLOCKER and, because it was found after Round 2, triggers convergence.

## Convergence state and next owner

Codex wrote the required four-part statement in the Review Card and active review chat:

- minimum shippable claim: preserve validated repairs in a later candidate, but do not ship or run this bounded reader;
- controlling evidence: the post-plan provenance fixture and source call order;
- strongest contrary evidence: all suites are green and real provenance may be smaller, but neither proves the generic admission property;
- safe disposition: **`Revisions Required`**, because the defect is local and repairable outside formal review.

Claude owns the next action: write the owner Convergence Decision statement once and explicitly agree with or minimally counter-propose the terminal disposition. **Claude must not edit the frozen candidate inside RC-002.** If both agents agree on `Revisions Required`, close RC-002 without approval, conclude the chat, repair outside formal review, and open at most one like-for-like successor card naming `Supersedes: RC-002`.

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

- Root `README.md` is State A / `In Progress`; its newest entry records the post-ceiling provenance counterexample and the Convergence Decision.
- `chats/Claude-Codex/Archive-Reading Drift Command Review/Archive-Reading Drift Command Review - Active.md` remains active until both convergence statements and terminal disposition consensus exist.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` remains active by Randy's instruction and records that RC-002 is the method's first live Convergence Decision.
- The Phase-1 director contract-review request remains open and nonblocking. No new director action is needed.
- No Slot 8 verification-artifact update exists because there is no result.
- The next count-based progress report is Codex Session 32.

## Downstream gates remain separate

1. RC-002 terminal disposition, then any successor archive-reader approval;
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

`agents/Codex/Session Summaries/HumanReport29.md` contains the complete evidence, decision, file list and reasoning.
