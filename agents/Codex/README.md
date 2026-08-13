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
│  ├── HumanReport1.md … HumanReport13.md
│  └── HumanReport14.md
└── Progress Reports/
   ├── Progress Report Phase 1 Close.md
   ├── Progress Report Amendment Compute Schedule.md
   ├── Progress Report Session 8.md
   └── Progress Report Amendment Real Control Donor Exclusion.md
```

## What each file owns

- **`Summary of Only Necessary Context.md`** — authoritative next-session continuity, rewritten at every closeout.
- **`Literature Foundation.md`** — Codex's dated and frozen Phase 0 field survey.
- **`Tier A Real-Arm Donor Matching Rule.md`** — active pre-pool specification for the deterministic real-control donor matcher. Draft 2 was reviewed by Claude but remains blocked by Codex. Proposed Amendment 6 now has a Codex-approved revised state awaiting Claude owner re-review; only after it enters force may the prose be generalized to `N` and the source-count floor repaired. This is not an implementation or execution authorization.
- **`references.md`** — Codex's living source ledger and transferable citations.
- **`Session Summaries/HumanReport<N>.md`** — permanent detailed session reports for the director.
- **`Progress Reports/`** — director-facing reports triggered by phase changes, approved amendments and the eight-session cadence. The newest explains Amendment 5's real-control donor exclusion and required matched-policy cost report.

## Shared work outside this folder

- `chats/Claude-Codex/Phase 0 Literature Comparison/`, `Claim Sheet Review/`, `Study Guide Pass 1 Review/` and `Compute Environment Update/` are concluded.
- `chats/Claude-Codex/Tier A Selection Review/` is active. Draft 7 SHA-256 `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01` has explicit same-state approval from Claude and Codex for its declared strategy/evidence scope, including §14's independent baseline re-derivation and Amendment 3 supersession finding. It is not a pinned-host approval.
- `chats/Claude-Codex/Reproducibility Packet Review/` is concluded. Packet README `3b07aa5b…`, checker `4eb94018…` and Claude's 15-case mutation harness `d64134b1…` have explicit same-state approval. One command per runbook step/example remains a hard error; later packet work begins a new scoped review.
- `chats/Claude-Codex/Tier A Donor Matching Rule/` is active. Draft 2 SHA-256 `f4ab71c3216d172641706a199d0536520da538aff906eb29d94f06f3d6620310` remains blocked. Codex reviewed Claude's Amendment 6 proposal, accepted the `N = 10…16` design, repaired an eligibility/rota circularity and a missed fixed-sixteen sentence, and explicitly approved the revised synchronized sheets. Claude owner re-review is open. No pool or donor selection exists.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` are synchronized proposed states at SHA-256 `8fa0342279cfe4173ebb605fce4d3434e2647533f4af3a444b78a5f286cfaf48` / `c58446d64b58748230f019188812a8eb3b043e95f10151ab1420799cab487d68`. Amendments 1–5 are `In force`; Amendment 6 remains `Proposed` pending Claude approval of these exact bytes. The matching-rule draft, implementation, host-dependent exact configuration and manipulation gate remain separate approvals.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and PDF are approved Phase 1 artifacts. Pass 2 remains a Phase 3 deliverable.
- `director_requests.md` contains one open non-blocking Phase 1 contract-review item. No new director action is needed.
- Root `README.md` is the append-only public live-run page. Its latest entry already records Claude Session 14's proposed solution to the donor-loss conflict. Codex's review did not move that proposal into force, so no second heartbeat was added.
- The Reproducibility Packet is co-owned. Codex owns Rung 0, the sorter-panel decision, inference/negative-control harness, Tier A's independent balance/manipulation gate, and the two-part placement calibration.

## Current technical boundaries

- Rung 0 must build and pin the host injection substrate before injection because donor templates already carry `phase_shift` and SpikeInterface 0.104.8 does not preprocess inside `generate_hybrid_recording()`.
- Pre-rescaling scale factor is an integrity diagnostic, not a matching covariate.
- The matcher will use common U-derived scaling for amplitude/effective-SNR/depth, a global no-reuse assignment and no region term, but Draft 2 is blocked. Proposed Amendment 6 parameterizes real and pseudo arms by `N = 10…16`, preserves the full sixteen-key Z removal, computes `N` once over pre-pinned candidate sites and makes joint block-placement failure reject the host. It awaits Claude owner re-review. The later matcher revision must enforce source-count equality at insertion/session/subject/final relaxation stages; implementation/test review still precedes any host-specific pool.
- The derived CCF label layer is opt-in; recognized white-matter/fibre-tract labels remain non-injectable.
- Any non-CA1 zone change must define the removal set across parent/descendant labels before matching.
- No host is pinned and no Rung 0, generation or sorter run has occurred.

For resumption, read `Summary of Only Necessary Context.md`, then the latest human report. Use `references.md` rather than memory for citations.
