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
│  ├── probe_missing_depth_actual_null.py
│  ├── probe_rc005_round1.py
│  ├── probe_rc005_round2.py
│  ├── probe_rc006_round1.py
│  ├── probe_rc006_round2.py
│  ├── probe_rc007_round1.py
│  ├── probe_rc007_round2.py
│  ├── probe_rc007_round3.py
│  ├── probe_rc007_round3_2026-08-18.txt
│  ├── probe_rc008_round1.py
│  ├── probe_rc008_round2.py
│  ├── probe_rc008_round3.py
│  └── rc008_round1_2026-08-18.txt … rc008_round3_2026-08-19.json
├── Session Summaries/
│  └── HumanReport1.md … HumanReport48.md
└── Progress Reports/
   ├── Progress Report Phase 1 Close.md
   ├── Progress Report Amendment Compute Schedule.md
   ├── Progress Report Session 8.md
   ├── Progress Report Amendment Real Control Donor Exclusion.md
   ├── Progress Report Session 16.md
   ├── Progress Report Session 24.md
   ├── Progress Report Session 32.md
   ├── Progress Report Session 40.md
   └── Progress Report Session 48.md
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
- **`tools/probe_rc005_round1.py`** — independent RC-005 full-pass evidence using generated local HDF5 only. It reproduces the whole-command contradiction in which the reconciled disposition is `unmeasurable` but the terminal console line says `passed=True`; it also proves the reader's declared resident/peak formula omits the returned per-spike boolean masks and records the downstream finite-only copies separately from that read-scoped blocker. At rank-1 size the missing mask term is 3,160,311 bytes. It reads no archive, candidate asset or network data.
- **`tools/probe_rc005_round2.py`** — independent RC-005 delta evidence using generated local HDF5 only. It positively matches the command's final line to the reconciled non-advancing record on a fixture whose point gate passes, verifies the point gate is labelled diagnostic, derives the mask-inclusive resident and peak terms outside the plan under test, refuses the exact old mask-omitting ceiling, admits the corrected peak, and checks the returned masks occupy exactly the charged bytes. It passes 10/10 and reads no archive, candidate asset or network data.
- **`tools/probe_rc006_round1.py`** — independent offline RC-006 full-pass evidence. It authenticates the seven-file candidate, proves the §1–§16 span and docstring-stripped executable state are unchanged, derives the committed numerical audit from JSON, reconciles all four resource-plan terms, exposes the actual headroom factors and 164-line help surface, and verifies the per-unit audit is assembled after reconciliation rather than consumed by it. It passes 52/52; the separate Step-11 replay is recorded in `HumanReport41.md`.
- **`tools/probe_rc006_round2.py`** — independent offline RC-006 delta evidence. It authenticates the nine-file response, proves that no packet or result file moved, derives both corrected resource decompositions and admission factors from the committed JSON record, verifies the narrowed working-set language and open follow-up, rechecks the frozen §1–§17 spans and unchanged disposition, and renders the 164-line ASCII-only help surface. It passes 48/48.
- **`tools/probe_rc007_round1.py`** — independent offline RC-007 full-pass evidence. It authenticates Draft 29 and reruns the owner checker; catches the stale relaxed ladder and missing lower-bound verdict; constructs the peak-versus-peak-to-peak ceiling counterexample and overlapping-disposition case; proves the sixty-window grid misses a one-chunk excursion; evaluates the ideal FFT high-pass impulse in the retained centre; checks the in-force Claim Sheet's host-specific effective-SNR gate against the proposed four-gate supersession; and confirms the layout probe contains no Python-level sample slice. It passes 12/12.
- **`tools/probe_rc007_round2.py`** — independent offline RC-007 delta evidence. It authenticates all eight Draft-30 files and three frozen document spans, checks the repaired level/verdict/grid contract, constructs two valid int16-lattice neighbour contexts that move the isolated-chunk Butterworth MAD estimate by −0.228% and +0.283%, and shows that reciprocal temporal changes can collapse the split-half p10/p90 spread from 4 to 1. It passes 31/31 and reads no archive, candidate sample or network resource.
- **`tools/probe_rc007_round3.py`** and **`tools/probe_rc007_round3_2026-08-18.txt`** — independent offline RC-007 final-delta evidence. They authenticate all eight Draft-31 files and frozen spans, reproduce the real-neighbour filter repair, tightened 170-chunk / 73.780-second coverage theorem and 957,031,364-byte transfer projection, then exercise the four-case ordered-branch truth table. They show that the high-space/high-null state is a homogeneity failure under the branches even though three live surfaces call high null sufficient to withhold the measurement. The probe passes 39/39 and reads no archive, candidate sample or network resource.
- **`tools/probe_rc008_round1.py`** and **`tools/rc008_round1_2026-08-18.txt`** — independent offline RC-008 full-pass evidence. They authenticate the six Draft-32 files and frozen spans, invoke the owner checker, and reproduce five blockers: the lower-floor extremum counterexample, the nominal-rate filter mismatch, an interleaving-direction reversal, a counterfeit legacy regression baseline, and a bad-channel pass reversal. The probe passes 32/32 and reads no archive, candidate noise value or network resource.
- **`tools/probe_rc008_round2.py`**, **`tools/rc008_round2_2026-08-19.txt`**, and **`tools/rc008_round2_2026-08-19.json`** — independent offline RC-008 delta evidence. They authenticate the nine Draft-33 files and frozen spans, replay the two fast owner probes, show that the split rule can change a would-be pass into `unmeasurable`, refute the claimed near-independence of contiguous halves with an above-300-Hz periodic construction, and stage a byte-different timing-index substitute that the supposedly fully authenticated regression wrapper still accepts at 168/168. The probe passes 27/27 and reads no archive, candidate noise value or network resource.
- **`tools/probe_rc008_round3.py`**, **`tools/rc008_round3_2026-08-19.txt`**, and **`tools/rc008_round3_2026-08-19.json`** — independent offline RC-008 terminal evidence. They authenticate all nine Draft-34 files and three frozen spans, replay the owner and legacy checks, verify syntax-tree-derived legacy-input completeness, and show that the reviewed fixed even/odd split has no tunable period while moving `passes` to `unmeasurable`. The probe passes 33/33 and reads no archive, candidate noise value or network resource.
- **`Session Summaries/HumanReport<N>.md`** — permanent detailed session reports for the director.
- **`Progress Reports/`** — director-facing reports triggered by phase changes, approved amendments, and the eight-session cadence. The newest is the Session 48 count-based report.

## Shared work outside this folder

- `chats/Claude-Codex/Phase 0 Literature Comparison/`, `Claim Sheet Review/`, `Study Guide Pass 1 Review/`, `Compute Environment Update/`, `Reproducibility Packet Review/`, and `Tier A Donor Matching Rule/` are concluded.
- `chats/Claude-Codex/Tier A Selection Review/` is concluded on the director's method transition. Its successor, `chats/Claude-Codex/Tier A Selection Section 16 Review/`, is also concluded: RC-001 closed `Approved` at Round 3 with exact same-state approval of Draft 24 and both implementation states. No Convergence Decision was needed. The separately reviewed archive CLI is now approved under RC-003; the first candidate measurement remains a later, separately governed action.
- `chats/Claude-Codex/Archive-Reading Drift Command Review/` is concluded. RC-002 closed unapproved at the Convergence Decision with both agents explicitly agreeing on `Revisions Required`; its frozen state was repaired outside formal review.
- `chats/Claude-Codex/Bounded Archive Read Review/` is concluded. Successor RC-003 closed `Approved` at Round 3 on the exact nine-file state both agents approved. Whole-statement provenance authentication, raw/processed converter-version agreement, exact series association, and pre-transfer distinct-block budgeting all pass. No Convergence Decision was needed, and no candidate asset was opened during review.
- `chats/Claude-Codex/Session Clock Agreement/` is concluded. The first real plan-only command showed that RC-003's converter-version equality admits none of the measured population. Claude and Codex independently reproduced 71 paired-session metadata reads: version equality is 0/71, while declared-reference-instant equality is 63/71 and isolates eight one-hour disagreements. Both agents agreed to a new Claude-owned, Codex-reviewed RC-004 that replaces the pair-version proxy with bounded reference-instant equality while preserving per-asset source authentication.
- `chats/Claude-Codex/Session Reference Time Pair Check Review/` is concluded. RC-004 closed `Approved` at Round 2 after Claude explicitly approved the same five-file state Codex had approved; the reference-instant pair check therefore unblocked the separately governed rank-1 read.
- `chats/Claude-Codex/Non-Finite Spike Depths/` is concluded. Its accepted design bounds both gate numbers over every completion, treats NaN alone as recoverable missing depth, keeps infinities fatal, and propagates all-missing destinations as defined but unbounded. Its successor is the RC-005 review below.
- `chats/Claude-Codex/Missing Depth Recovery Review/` is concluded. RC-005 closed `Approved with Follow-Ups` at Round 2 on the exact seven-file state both agents approved. The final console line now carries the reconciled decision, the point gate labels itself diagnostic, and the per-spike masks enter the resident/peak bound. Codex's independent delta probe passes 10/10; the owner suite passes 543/543 and the repair-reversion harness catches 4/4 with a green control. The implementation gate is cleared; rank-1 measurement remains a separate execution step.
- `chats/Claude-Codex/Rank 1 Drift Result/` is concluded. RC-006 closed `Approved` at Round 2 on the exact nine-file state both agents approved. All four reporting findings are repaired, the owner checker passes 61/61, Codex's delta probe passes 48/48, and no packet or result byte moved in the response. Only rank 1's strict drift gate is discharged; no host is pinned.
- `chats/Claude-Codex/Host Noise Gate/` is concluded. RC-007 closed `Revisions Required` by explicit two-agent consensus at the Convergence Decision; Draft 31 is frozen and unapproved.
- `chats/Claude-Codex/Section 19 Convergence Repair/` is active at the Convergence Decision. Draft 34 is frozen and unapproved after the terminal delta pass verified every repair but found its sole split rationale falsely assigns a tunable period to the fixed even/odd alternative. Codex proposes and approves `Split/Redesign Required`; Claude owes the other four-field statement and explicit consensus or the smallest counterproposal. No fourth repair, estimator or candidate noise read is authorized.
- `chats/Claude-Codex-Human/Review Method Change/` is active at Randy's request. The bounded agent-only Convergence Decision, successor-card lineage, and forced redesign after repeated non-approval are agreed and written into the superseding review method. The newest exchange records two reporting safeguards: pair accessible result sentences directly with the technical boundary list rather than translating from memory, and verify prose claims against correct instrument output independently rather than treating a green owner claim checker as sufficient by itself.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` are synchronized at SHA-256 `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365` / `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. Amendments 1–6 are `In force`. The matching-rule prose, implementation/tests, host-dependent exact configuration, and manipulation gate remain separate approvals.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and PDF are approved Phase 1 artifacts. Pass 2 remains a Phase 3 deliverable.
- `director_requests.md` contains one open non-blocking Phase 1 contract-review item. No new director action is needed.
- Root `README.md` is the append-only public live-run page. Its newest heartbeat records that the host-noise specification reached its review limit without approval and must change boundary before returning. Rank 1 has still passed only the predeclared depth-trace gate; no host or downstream execution is authorized. The project remains in progress.
- The Reproducibility Packet is co-owned. Its runbook now has eleven agreeing steps, including the independently replayed rank-1 measurement. Codex owns Rung 0, the sorter-panel decision, inference/negative-control harness, Tier A's independent balance/manipulation gate, and the two-part placement calibration.

## Current technical boundaries

- Rung 0 must build and pin the host injection substrate before injection because donor templates already carry `phase_shift` and SpikeInterface 0.104.8 does not preprocess inside `generate_hybrid_recording()`.
- Pre-rescaling scale factor is an integrity diagnostic, not a matching covariate.
- Same-state-approved matcher Draft 6 uses common U-derived scaling for amplitude/effective-SNR/depth, donor-equal global no-reuse assignment, and no region term. It computes T and `N` once from a pinned target manifest, preserves the full sixteen-key Z removal, makes joint block-placement failure reject the host, and tests exact insertion/session/subject-count equality before falling back at the same provenance stage to the contract's literal insertion-count floor.
- Before T is measured or any host-specific manifest/pool is opened, an exact exposure-schedule/placement specification and synthetic tests must pin the nuisance seed, amplitude target, and commanded-placement construction. Matcher implementation/test review follows as another same-state gate.
- The derived CCF label layer is opt-in; recognized white-matter/fibre-tract labels remain non-injectable. Any non-CA1 zone change must define the removal set across parent/descendant labels before matching.
- RC-001 is closed `Approved` on Draft 24 `c35987fe…`, utility `eace4cd35…`, and harness `946df906…`. The gate uses eleven consecutive one-minute medians; the universal half-bin cutoff is withdrawn; within-bin transmission depends on depth ranks and episode placement; and neither missed nor transmitted sub-minute motion is treated as a one-way safety property. The owner harness passes 103 checks, Codex's probe passes thirteen checks including 93,184 exhaustive small cases, and the utility's executable AST is unchanged from Round 2.
- RC-002 closed unapproved at its Convergence Decision; its one allowed successor RC-003 closed `Approved`; RC-004 closed `Approved` at Round 2; RC-005 closed `Approved with Follow-Ups` at Round 2; RC-006 closed `Approved` at Round 2; RC-007 closed `Revisions Required`; and its sole successor RC-008 is at the Round-3 Convergence Decision with Draft 34 frozen and unapproved. Codex proposes `Split/Redesign Required`; Claude's statement and consensus are due. The strict all-finite-depth confirmation is superseded only as §17 declares: NaN is bounded as missing, either infinity remains fatal, and a decision-unstable completion bound pauses the candidate.
- `.gitattributes` makes repository-wide checkout bytes explicit and is same-state approved by both agents. All paths default to `-text`; 17 framework files and 11 legacy packet outputs intentionally reconstruct CRLF. A temporary `core.autocrlf=true` clone matched all 153 reviewed tracked files byte-for-byte.
- No host is pinned. Rank 1's approved depth-trace result is `Delta_10min = 1.821 µm` with `Q95_null = 0.526 µm`; completion and reconciliation pass, discharging one of five host gates. Noise, effective SNR, joint ten-placement feasibility, and balance remain open. Rank 2 is unmeasured. No Rung 0, generation or sorter run is authorized, and the rank-5/7/9/13 declared-clock disagreements remain separately paused.

For resumption, read `Summary of Only Necessary Context.md`, then the latest human report. Use `references.md` rather than memory for citations.
