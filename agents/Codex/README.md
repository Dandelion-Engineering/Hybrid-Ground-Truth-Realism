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
├── Session Summaries/
│  ├── HumanReport1.md … HumanReport15.md
│  └── HumanReport16.md
└── Progress Reports/
   ├── Progress Report Phase 1 Close.md
   ├── Progress Report Amendment Compute Schedule.md
   ├── Progress Report Session 8.md
   ├── Progress Report Amendment Real Control Donor Exclusion.md
   └── Progress Report Session 16.md
```

## What each file owns

- **`Summary of Only Necessary Context.md`** — authoritative next-session continuity, rewritten at every closeout.
- **`Literature Foundation.md`** — Codex's dated and frozen Phase 0 field survey.
- **`Tier A Real-Arm Donor Matching Rule.md`** — active pre-pool specification for the deterministic real-control donor matcher. Codex explicitly approves Draft 5 SHA-256 `23148d2d8896db70f48d13bd712bbf4ba04987b7f348866918a98431fc324cf7`; Claude exact-state review is open. It uses one fixed target manifest, `N = 10…16`, full-sixteen Z removal, two-level provenance-count equality at every stage, and a separate exact exposure-schedule/placement-specification gate before any host-specific manifest or pool. This is not an implementation, pool, configuration, balance verdict or execution authorization.
- **`references.md`** — Codex's living source ledger and transferable citations.
- **`Session Summaries/HumanReport<N>.md`** — permanent detailed session reports for the director.
- **`Progress Reports/`** — director-facing reports triggered by phase changes, approved amendments and the eight-session cadence. The newest is the Session 16 count-based report covering Amendment 6, the provenance-granularity finding and the new schedule/placement pre-pool gate.

## Shared work outside this folder

- `chats/Claude-Codex/Phase 0 Literature Comparison/`, `Claim Sheet Review/`, `Study Guide Pass 1 Review/` and `Compute Environment Update/` are concluded.
- `chats/Claude-Codex/Tier A Selection Review/` is active. Draft 7 SHA-256 `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01` has explicit same-state approval from Claude and Codex for its declared strategy/evidence scope, including §14's independent baseline re-derivation and Amendment 3 supersession finding. It is not a pinned-host approval.
- `chats/Claude-Codex/Reproducibility Packet Review/` is concluded. Packet README `3b07aa5b…`, checker `4eb94018…` and Claude's 15-case mutation harness `d64134b1…` have explicit same-state approval. One command per runbook step/example remains a hard error; later packet work begins a new scoped review.
- `chats/Claude-Codex/Tier A Donor Matching Rule/` is active. Amendment 6 is in force. Claude reviewed Draft 3 and returned Draft 4 with a stronger provenance-count preference and a nuisance-seed requirement. Codex genuinely owner-re-reviewed those edits, accepted the scientific correction, replaced the under-specified later seed with an exact pre-pool schedule/placement-specification gate, and explicitly approved Draft 5 at `23148d2d…`. Claude exact-state review is open. No schedule implementation, matcher implementation, manifest, pool, edge table or donor selection exists.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` are synchronized at SHA-256 `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365` / `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. Amendments 1–6 are `In force`. The matching-rule prose, implementation/tests, host-dependent exact configuration and manipulation gate remain separate approvals.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and PDF are approved Phase 1 artifacts. Pass 2 remains a Phase 3 deliverable.
- `director_requests.md` contains one open non-blocking Phase 1 contract-review item. No new director action is needed.
- Root `README.md` is the append-only public live-run page. Its latest entry already records the provenance-granularity and redrawable-schedule findings, and its working-record section states that the pre-pool matcher draft awaits same-state review. Draft 5 has not converged, so no additional heartbeat was added.
- The Reproducibility Packet is co-owned. Codex owns Rung 0, the sorter-panel decision, inference/negative-control harness, Tier A's independent balance/manipulation gate, and the two-part placement calibration.

## Current technical boundaries

- Rung 0 must build and pin the host injection substrate before injection because donor templates already carry `phase_shift` and SpikeInterface 0.104.8 does not preprocess inside `generate_hybrid_recording()`.
- Pre-rescaling scale factor is an integrity diagnostic, not a matching covariate.
- Draft 5 uses common U-derived scaling for amplitude/effective-SNR/depth, donor-equal global no-reuse assignment and no region term. It computes T and `N` once from a pinned target manifest, preserves the full sixteen-key Z removal, makes joint block-placement failure reject the host, and tests exact insertion/session/subject-count equality before falling back at the same provenance stage to the contract's literal insertion-count floor. Claude exact-state review is open.
- Before T is measured or any host-specific manifest/pool is opened, an exact exposure-schedule/placement specification and synthetic tests must pin the nuisance-seed, amplitude-target and commanded-placement construction. Matcher implementation/test review follows as another same-state gate.
- The derived CCF label layer is opt-in; recognized white-matter/fibre-tract labels remain non-injectable.
- Any non-CA1 zone change must define the removal set across parent/descendant labels before matching.
- No host is pinned and no Rung 0, generation or sorter run has occurred.

For resumption, read `Summary of Only Necessary Context.md`, then the latest human report. Use `references.md` rather than memory for citations.
