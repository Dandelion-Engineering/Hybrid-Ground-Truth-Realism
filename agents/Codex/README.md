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
│  └── probe_rc002_round3.py
├── Session Summaries/
│  └── HumanReport1.md … HumanReport29.md
└── Progress Reports/
   ├── Progress Report Phase 1 Close.md
   ├── Progress Report Amendment Compute Schedule.md
   ├── Progress Report Session 8.md
   ├── Progress Report Amendment Real Control Donor Exclusion.md
   ├── Progress Report Session 16.md
   └── Progress Report Session 24.md
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
- **`Session Summaries/HumanReport<N>.md`** — permanent detailed session reports for the director.
- **`Progress Reports/`** — director-facing reports triggered by phase changes, approved amendments, and the eight-session cadence. The newest is the Session 24 count-based report; the next cadence report is Session 32.

## Shared work outside this folder

- `chats/Claude-Codex/Phase 0 Literature Comparison/`, `Claim Sheet Review/`, `Study Guide Pass 1 Review/`, `Compute Environment Update/`, `Reproducibility Packet Review/`, and `Tier A Donor Matching Rule/` are concluded.
- `chats/Claude-Codex/Tier A Selection Review/` is concluded on the director's method transition. Its successor, `chats/Claude-Codex/Tier A Selection Section 16 Review/`, is also concluded: RC-001 closed `Approved` at Round 3 with exact same-state approval of Draft 24 and both implementation states. No Convergence Decision was needed. The archive CLI is a separate RC-002 gate; candidate measurement remains later and blocked.
- `chats/Claude-Codex/Archive-Reading Drift Command Review/` is active. The final Round-3 verification repaired every recorded Round-2 item on its tested boundary but found F1-R2, a blocking post-ceiling provenance read. The method triggered its first Convergence Decision; Codex proposes terminal `Revisions Required`, and Claude's one statement plus disposition consensus are pending. The seven-file candidate is frozen and candidate reading remains blocked.
- `chats/Claude-Codex-Human/Review Method Change/` is active at Randy's request. The bounded agent-only Convergence Decision, successor-card lineage, and forced redesign after repeated non-approval are now agreed and written into the superseding review method. Codex accepts Claude's two applications; one stale quality-checklist reference to human triage was mechanically corrected.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` are synchronized at SHA-256 `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365` / `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. Amendments 1–6 are `In force`. The matching-rule prose, implementation/tests, host-dependent exact configuration, and manipulation gate remain separate approvals.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and PDF are approved Phase 1 artifacts. Pass 2 remains a Phase 3 deliverable.
- `director_requests.md` contains one open non-blocking Phase 1 contract-review item. No new director action is needed.
- Root `README.md` is the append-only public live-run page. Codex Session 29 records the post-ceiling provenance-read counterexample and the resulting Convergence Decision. The project remains in progress with no candidate measurement or result.
- The Reproducibility Packet is co-owned. Its design-stage runbook remains same-state approved at ten steps. Codex owns Rung 0, the sorter-panel decision, inference/negative-control harness, Tier A's independent balance/manipulation gate, and the two-part placement calibration.

## Current technical boundaries

- Rung 0 must build and pin the host injection substrate before injection because donor templates already carry `phase_shift` and SpikeInterface 0.104.8 does not preprocess inside `generate_hybrid_recording()`.
- Pre-rescaling scale factor is an integrity diagnostic, not a matching covariate.
- Same-state-approved matcher Draft 6 uses common U-derived scaling for amplitude/effective-SNR/depth, donor-equal global no-reuse assignment, and no region term. It computes T and `N` once from a pinned target manifest, preserves the full sixteen-key Z removal, makes joint block-placement failure reject the host, and tests exact insertion/session/subject-count equality before falling back at the same provenance stage to the contract's literal insertion-count floor.
- Before T is measured or any host-specific manifest/pool is opened, an exact exposure-schedule/placement specification and synthetic tests must pin the nuisance seed, amplitude target, and commanded-placement construction. Matcher implementation/test review follows as another same-state gate.
- The derived CCF label layer is opt-in; recognized white-matter/fibre-tract labels remain non-injectable. Any non-CA1 zone change must define the removal set across parent/descendant labels before matching.
- RC-001 is closed `Approved` on Draft 24 `c35987fe…`, utility `eace4cd35…`, and harness `946df906…`. The gate uses eleven consecutive one-minute medians; the universal half-bin cutoff is withdrawn; within-bin transmission depends on depth ranks and episode placement; and neither missed nor transmitted sub-minute motion is treated as a one-way safety property. The owner harness passes 103 checks, Codex's probe passes thirteen checks including 93,184 exhaustive small cases, and the utility's executable AST is unchanged from Round 2. The archive CLI is now under RC-002; candidate measurement remains blocked.
- RC-002's Round-3 seven-file state is frozen in the Convergence Decision: archive utility `2ee891ce…`, packet command `dfbb9cc8…`, owner harness `5101d000…`, repair harness `1e1ed5a9…`, checker mutation harness `ea85ede2…`, packet checker `848e6d03…`, and packet README `ae01b1a2…`. The recorded Round-2 items pass, but F1-R2 remains blocking because `source_provenance()` reads complete datasets after the combined ceiling has been enforced. Codex's Round-3 fixture was admitted at 267,001 bytes and then transferred/cached 4,232,336 bytes; probe SHA-256 `506d7280…`. Codex proposes terminal `Revisions Required`, Claude's statement is pending, and no candidate asset was opened.
- `.gitattributes` makes repository-wide checkout bytes explicit and is same-state approved by both agents. All paths default to `-text`; 17 framework files and 11 legacy packet outputs intentionally reconstruct CRLF. A temporary `core.autocrlf=true` clone matched all 153 reviewed tracked files byte-for-byte.
- No host is pinned, no candidate drift value has been read, and no dependency install, raw-data read, Rung 0, generation, or sorter run has occurred.

For resumption, read `Summary of Only Necessary Context.md`, then the latest human report. Use `references.md` rather than memory for citations.
