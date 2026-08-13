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
│  ├── HumanReport1.md … HumanReport11.md
│  └── HumanReport12.md
└── Progress Reports/
   ├── Progress Report Phase 1 Close.md
   ├── Progress Report Amendment Compute Schedule.md
   ├── Progress Report Session 8.md
   └── Progress Report Amendment Real Control Donor Exclusion.md
```

## What each file owns

- **`Summary of Only Necessary Context.md`** — authoritative next-session continuity, rewritten at every closeout.
- **`Literature Foundation.md`** — Codex's dated and frozen Phase 0 field survey.
- **`Tier A Real-Arm Donor Matching Rule.md`** — active pre-pool specification for the deterministic real-control donor matcher. Draft 1 is owner-approved and awaits Claude review; it is not an implementation or execution authorization.
- **`references.md`** — Codex's living source ledger and transferable citations.
- **`Session Summaries/HumanReport<N>.md`** — permanent detailed session reports for the director.
- **`Progress Reports/`** — director-facing reports triggered by phase changes, approved amendments and the eight-session cadence. The newest explains Amendment 5's real-control donor exclusion and required matched-policy cost report.

## Shared work outside this folder

- `chats/Claude-Codex/Phase 0 Literature Comparison/`, `Claim Sheet Review/`, `Study Guide Pass 1 Review/` and `Compute Environment Update/` are concluded.
- `chats/Claude-Codex/Tier A Selection Review/` is active. Draft 7 SHA-256 `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01` has explicit same-state approval from Claude and Codex for its declared strategy/evidence scope, including §14's independent baseline re-derivation and Amendment 3 supersession finding. It is not a pinned-host approval.
- `chats/Claude-Codex/Reproducibility Packet Review/` is active. Claude approved the earlier validator-boundary repair, then handed off packet-relative `--help` examples and a consistency checker. Codex kept the two-copy design but repaired the outsider-clean boundary and checker coverage for multi-line fences and duplicate/gapped step numbers. Claude owner re-review is open on the exact hashes recorded in Codex Session 12; key states are packet README `00acb826…` and checker `094fbff1…`.
- `chats/Claude-Codex/Tier A Donor Matching Rule/` is active. Codex Draft 1 SHA-256 `1243742131b39dadde8fe86240d718f07d196826186a748e0344085344c1ee3f` fixes the pre-pool matching specification and awaits Claude exact-state review. No pool or donor selection exists.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` are synchronized states at SHA-256 `ac089232851705be86e8674987f29afd7fa553e0e55e08049868761549465b28` / `8bae94bcc84928766214fea64eba234af6a524804afe11bd7eb16504d265c17f`. Amendments 1–5 are `In force`. The matching-rule draft, implementation, host-dependent exact configuration and manipulation gate remain separate approvals.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and PDF are approved Phase 1 artifacts. Pass 2 remains a Phase 3 deliverable.
- `director_requests.md` contains one open non-blocking Phase 1 contract-review item. No new director action is needed.
- Root `README.md` is the append-only public live-run page. Its latest entry records the pre-pool matching-rule draft while preserving that review, implementation, host, generation and result remain open.
- The Reproducibility Packet is co-owned. Codex owns Rung 0, the sorter-panel decision, inference/negative-control harness, Tier A's independent balance/manipulation gate, and the two-part placement calibration.

## Current technical boundaries

- Rung 0 must build and pin the host injection substrate before injection because donor templates already carry `phase_shift` and SpikeInterface 0.104.8 does not preprocess inside `generate_hybrid_recording()`.
- Pre-rescaling scale factor is an integrity diagnostic, not a matching covariate.
- Draft 1 of the real-arm matcher uses common U-derived scaling for amplitude/effective-SNR/depth, feasibility-only provenance fallback, a global no-reuse assignment, and no region term. It must converge and then be implemented/tested under a separate same-state review before a host-specific pool is opened.
- The derived CCF label layer is opt-in; recognized white-matter/fibre-tract labels remain non-injectable.
- Any non-CA1 zone change must define the removal set across parent/descendant labels before matching.
- No host is pinned and no Rung 0, generation or sorter run has occurred.

For resumption, read `Summary of Only Necessary Context.md`, then the latest human report. Use `references.md` rather than memory for citations.
