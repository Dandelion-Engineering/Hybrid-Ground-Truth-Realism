# Codex — Workspace

This directory contains Codex's work for the **Hybrid Ground Truth Realism** project.

## Folder map

```text
agents/Codex/
├── README.md
├── Summary of Only Necessary Context.md
├── Literature Foundation.md
├── Tier A Real-Arm Donor Matching Rule.md
├── references.md
├── tools/
│  ├── probe_draft16_safety_claims.py
│  ├── probe_rc001_round1.py
│  ├── probe_rc002_round1.py
│  ├── probe_rc002_round2.py
│  ├── probe_rc002_round3.py
│  ├── probe_rc003_round1.py
│  ├── probe_rc003_round2.py
│  ├── probe_rc004_round1.py
│  ├── probe_rc004_round2.py
│  ├── probe_nonfinite_depth_disposition.py
│  └── probe_missing_depth_actual_null.py
├── Session Summaries/
│  └── HumanReport1.md … HumanReport38.md
└── Progress Reports/
   ├── Progress Report Phase 1 Close.md
   ├── Progress Report Amendment Compute Schedule.md
   ├── Progress Report Session 8.md
   ├── Progress Report Amendment Real Control Donor Exclusion.md
   ├── Progress Report Session 16.md
   ├── Progress Report Session 24.md
   └── Progress Report Session 32.md
```

## What each file owns

- **`Summary of Only Necessary Context.md`** — authoritative next-session continuity, rewritten at every closeout.
- **`Literature Foundation.md`** — Codex's dated and frozen Phase 0 field survey.
- **`Tier A Real-Arm Donor Matching Rule.md`** — same-state-approved pre-pool specification for the deterministic real-control donor matcher. Claude and Codex explicitly approve Draft 6 SHA-256 `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`. It uses one fixed target manifest, `N = 10…16`, full-sixteen Z removal, two-level provenance-count equality at every stage, and a separate exact exposure-schedule/placement-specification gate before any host-specific manifest or pool. This is not an implementation, pool, configuration, balance verdict, or execution authorization.
- **`references.md`** — Codex's living source ledger and transferable citations.
- **`tools/probe_draft16_safety_claims.py`** — deterministic synthetic review probe showing that label-blind unit expansion and retaining a first bin do not have one-way safety guarantees. Its public labels now use `Delta_10min`; it reads no candidate asset.
- **`tools/probe_rc001_round1.py`** — independent RC-001 evidence: reference recomputation, deterministic-null replay, gate boundaries, repaired temporal-alias/unit-count cases, the heterogeneous-depth counterexample to Draft 23's universal cutoff, and an exhaustive 93,184-case check of Draft 24's replacement rank/offset bound. It uses synthetic arrays only and reads no candidate asset.
- **`tools/probe_rc002_round1.py`** — independent RC-002 refusal and resource-accounting probe. It reproduces seven adversarial constructions against the archive reader using synthetic local HDF5 fixtures only; it reads no archive or candidate asset.
- **`tools/probe_rc002_round2.py`** — independent RC-002 response probe. It constructs fragmented valid HDF5 chunks that defeat the claimed transfer bound, measures coexisting fixed-block cache and converted arrays against the ceiling, checks case-only output aliases on Windows, and audits the repair-mutation list. It reads no archive or candidate asset.
- **`tools/probe_rc002_round3.py`** — independent RC-002 terminal probe. It builds a local file with a large schema-valid stored conversion script and shows that `source_provenance()` runs after the safety ceiling, letting an admitted read exceed both the claimed transfer bound and combined resident bound. It reads no archive, candidate asset or network data.
- **`tools/probe_rc003_round1.py`** — independent RC-003 full-pass evidence. It shows that absent conversion provenance reaches a verdict, a substring-matched `Probe000` AP series can supply `Probe00`'s clock and reach a verdict, and a variable-length provenance value spends about 2.03 MB before a one-byte ceiling refuses it. A separate object-size diagnostic did not establish another blocker. It uses generated local HDF5 files only and reads no archive, candidate asset or network data.
- **`tools/probe_rc003_round2.py`** — independent RC-003 delta-pass evidence. It shows that negated NeuroConv text and mismatched raw/processed NeuroConv versions still reach a verdict, and that the default one-megabyte range cache transfers 2,081,456 distinct bytes before the claimed 65,536-byte provenance budget refuses the value. It uses generated local HDF5 files only and reads no archive, candidate asset or network data.
- **`tools/probe_rc004_round1.py`** — independent RC-004 full-pass evidence. It shows that Python's deliberately broad `fromisoformat` grammar accepts a non-ISO/NWB `Q` date-time separator and lets a malformed paired value reach a verdict, and that the raw reference-time read moves 23,920 distinct bytes outside a synthetic one-byte caller ceiling before the processed side refuses. It uses generated local HDF5 files only and reads no archive, candidate asset or network data.
- **`tools/probe_rc004_round2.py`** — independent RC-004 delta evidence. It reconstructs the exact 79-value reference-time population from the two recorded census JSON reports, proves the frozen owner-suite population is identical and fully admitted, rechecks the malformed separator, and exercises exact and one-byte-short raw-file ceilings with a block-caching local stand-in. It reads the recorded JSON files and generated local HDF5 only; it reads no archive, candidate asset or network data.
- **`tools/probe_nonfinite_depth_disposition.py`** — synthetic evidence against relying on finite-sample support alone after dropping missing depths. Against the approved point estimator, five units retain 14,000 finite samples in every bin and pass every support floor, while one missing depth per unit/bin admits compatible `Delta_10min` values of 0 and 100 µm. Claude Session 37 correctly showed that this balanced construction is already rejected by the gate's second number, so it proves a point-estimate defect rather than a whole-gate pass; a stronger spread fixture supplies the whole-gate counterexample. It reads no archive, candidate asset or network data.
- **`tools/probe_missing_depth_actual_null.py`** — independent pre-card evidence that the approved completed-data permutation null has an assumption-free, non-vacuous missing-depth interval: the completed vector length and missing source positions fix every seed-derived permutation before values are chosen. On the Session-37 state it passed 8/8, returned `[12.254, 18.618] µm`, contained three actual completions, and reproduced the zero-missing approved null element-for-element. The corrected Session-38 implementation preserves the first seven properties and deliberately removes the counterfactual API its eighth comparison called, so the old probe now raises only at that retired check. It uses synthetic arrays only and reads no archive, candidate asset or network data.
- **`Session Summaries/HumanReport<N>.md`** — permanent detailed session reports for the director.
- **`Progress Reports/`** — director-facing reports triggered by phase changes, approved amendments, and the eight-session cadence. The newest is the Session 32 count-based report; the next cadence report is Session 40.

## Shared work outside this folder

- `chats/Claude-Codex/Phase 0 Literature Comparison/`, `Claim Sheet Review/`, `Study Guide Pass 1 Review/`, `Compute Environment Update/`, `Reproducibility Packet Review/`, and `Tier A Donor Matching Rule/` are concluded.
- `chats/Claude-Codex/Tier A Selection Review/` is concluded on the director's method transition. Its successor, `chats/Claude-Codex/Tier A Selection Section 16 Review/`, is also concluded: RC-001 closed `Approved` at Round 3 with exact same-state approval of Draft 24 and both implementation states. No Convergence Decision was needed. The separately reviewed archive CLI is now approved under RC-003; the first candidate measurement remains a later, separately governed action.
- `chats/Claude-Codex/Archive-Reading Drift Command Review/` is concluded. RC-002 closed unapproved at the Convergence Decision with both agents explicitly agreeing on `Revisions Required`; its frozen state was repaired outside formal review.
- `chats/Claude-Codex/Bounded Archive Read Review/` is concluded. Successor RC-003 closed `Approved` at Round 3 on the exact nine-file state both agents approved. Whole-statement provenance authentication, raw/processed converter-version agreement, exact series association, and pre-transfer distinct-block budgeting all pass. No Convergence Decision was needed, and no candidate asset was opened during review.
- `chats/Claude-Codex/Session Clock Agreement/` is concluded. The first real plan-only command showed that RC-003's converter-version equality admits none of the measured population. Claude and Codex independently reproduced 71 paired-session metadata reads: version equality is 0/71, while declared-reference-instant equality is 63/71 and isolates eight one-hour disagreements. Both agents agreed to a new Claude-owned, Codex-reviewed RC-004 that replaces the pair-version proxy with bounded reference-instant equality while preserving per-asset source authentication.
- `chats/Claude-Codex/Session Reference Time Pair Check Review/` is concluded. RC-004 closed `Approved` at Round 2 after Claude explicitly approved the same five-file state Codex had approved; the reference-instant pair check therefore unblocked the separately governed rank-1 read.
- `chats/Claude-Codex/Non-Finite Spike Depths/` is active. Rank 1 and a rank-2 holdout both carry sparse NaN depths with finite times. Claude corrected the pre-card sensitivity module to bound the actual completed-`N` null rather than a counterfactual; Codex authenticated the 86-check state and accepted that design, fatal infinity handling, and exact unbounded all-missing destinations. Claude now owns the whole reader/command/§17 candidate and RC-005. The strict finite-depth rule still binds until that card receives same-state approval.
- `chats/Claude-Codex-Human/Review Method Change/` is active at Randy's request. The bounded agent-only Convergence Decision, successor-card lineage, and forced redesign after repeated non-approval are agreed and written into the superseding review method. The newest observation records that a synthetic review can prove dependence on a proxy without showing that the proxy admits or discriminates the real population; Claude's preserved-byte handoff correctly turned the new evidence into a new card rather than an unreviewed hotfix.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` are synchronized at SHA-256 `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365` / `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. Amendments 1–6 are `In force`. The matching-rule prose, implementation/tests, host-dependent exact configuration, and manipulation gate remain separate approvals.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and PDF are approved Phase 1 artifacts. Pass 2 remains a Phase 3 deliverable.
- `director_requests.md` contains one open non-blocking Phase 1 contract-review item. No new director action is needed.
- Root `README.md` is the append-only public live-run page. Its newest heartbeat records that the point-estimate sensitivity design survived but the counterfactual null was returned before wiring because a direct completed-data null bound is available. It preserves the boundary that no host or scientific result exists. The project remains in progress.
- The Reproducibility Packet is co-owned. Its design-stage runbook remains same-state approved at ten steps. Codex owns Rung 0, the sorter-panel decision, inference/negative-control harness, Tier A's independent balance/manipulation gate, and the two-part placement calibration.

## Current technical boundaries

- Rung 0 must build and pin the host injection substrate before injection because donor templates already carry `phase_shift` and SpikeInterface 0.104.8 does not preprocess inside `generate_hybrid_recording()`.
- Pre-rescaling scale factor is an integrity diagnostic, not a matching covariate.
- Same-state-approved matcher Draft 6 uses common U-derived scaling for amplitude/effective-SNR/depth, donor-equal global no-reuse assignment, and no region term. It computes T and `N` once from a pinned target manifest, preserves the full sixteen-key Z removal, makes joint block-placement failure reject the host, and tests exact insertion/session/subject-count equality before falling back at the same provenance stage to the contract's literal insertion-count floor.
- Before T is measured or any host-specific manifest/pool is opened, an exact exposure-schedule/placement specification and synthetic tests must pin the nuisance seed, amplitude target, and commanded-placement construction. Matcher implementation/test review follows as another same-state gate.
- The derived CCF label layer is opt-in; recognized white-matter/fibre-tract labels remain non-injectable. Any non-CA1 zone change must define the removal set across parent/descendant labels before matching.
- RC-001 is closed `Approved` on Draft 24 `c35987fe…`, utility `eace4cd35…`, and harness `946df906…`. The gate uses eleven consecutive one-minute medians; the universal half-bin cutoff is withdrawn; within-bin transmission depends on depth ranks and episode placement; and neither missed nor transmitted sub-minute motion is treated as a one-way safety property. The owner harness passes 103 checks, Codex's probe passes thirteen checks including 93,184 exhaustive small cases, and the utility's executable AST is unchanged from Round 2.
- RC-002 closed unapproved at its Convergence Decision, its one allowed successor RC-003 closed `Approved`, and RC-004 closed `Approved` at Round 2 on the exact five-file reference-instant state. Rank 1 then passed plan-only input authentication but the measurement stopped before a verdict on non-finite depth values. The strict finite-depth confirmation remains operative; any recovery must be designed before RC-005 and same-state approved.
- `.gitattributes` makes repository-wide checkout bytes explicit and is same-state approved by both agents. All paths default to `-text`; 17 framework files and 11 legacy packet outputs intentionally reconstruct CRLF. A temporary `core.autocrlf=true` clone matched all 153 reviewed tracked files byte-for-byte.
- No host is pinned and no candidate drift value exists. Rank 1's plan-only read completed and its real drift command stopped with no output because sparse NaN depths violate the still-binding input confirmation; a rank-2 diagnostic shows the same class. Support floors alone cannot authorize dropping them. The pre-card completed-`N` sensitivity design is now accepted, but the reader, command, §17 and RC-005 do not yet exist as one stable candidate. No Rung 0, generation or sorter run is authorized, and the rank-5/7/9/13 declared-clock disagreements remain separately paused.

For resumption, read `Summary of Only Necessary Context.md`, then the latest human report. Use `references.md` rather than memory for citations.
