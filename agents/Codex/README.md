# Codex — Workspace

This directory contains Codex's work for the **Hybrid Ground Truth Realism** project.

## Folder map

```text
agents/Codex/
├─ README.md
├─ Summary of Only Necessary Context.md
├─ Literature Foundation.md
├─ references.md
├─ Session Summaries/
│  ├─ HumanReport1.md
│  ├─ HumanReport2.md
│  ├─ HumanReport3.md
│  ├─ HumanReport4.md
│  ├─ HumanReport5.md
│  └─ HumanReport6.md
└─ Progress Reports/
   ├─ Progress Report Phase 1 Close.md
   └─ Progress Report Amendment Compute Schedule.md
```

## What each file owns

- **`Summary of Only Necessary Context.md`** — next-session continuity. It is rewritten at every closeout and contains only state not already owned by `AgentPrompt.md`, `Project Details/`, or the playbooks.
- **`Literature Foundation.md`** — Codex's independent Phase 0 field survey. It is a dated evidence artifact; later corrections propagate into the living ledger and downstream artifacts rather than silently rewriting the original survey.
- **`references.md`** — Codex's living source ledger. It records what each verified source establishes, how it changed the project, and a transferable citation.
- **`Session Summaries/HumanReport<N>.md`** — sequential permanent session reports for the director.
- **`Progress Reports/`** — director-facing reports at phase transitions and the scheduled session cadence. `Progress Report Phase 1 Close.md` records the agreed contract, remaining resource constraint, and start of execution.

## Authority

| Path | Status |
|---|---|
| `Literature Foundation.md` | Authoritative Phase 0 evidence artifact; dated and frozen |
| `references.md` | Authoritative living citation ledger |
| `Summary of Only Necessary Context.md` | Authoritative only for the next Codex session |
| `Session Summaries/*` | Permanent historical record |
| `Progress Reports/*` | Permanent phase/cadence record |

## Shared work outside this folder

- `chats/Claude-Codex/Phase 0 Literature Comparison/` is the concluded append-only Phase 0 comparison channel.
- `chats/Claude-Codex/Claim Sheet Review/` is concluded. Technical `Claim Sheet.md` SHA-256 `a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3` and `Accessible Claim Sheet.md` SHA-256 `73bff8f81dc2e31b47d4abbe1f61c8106a34dccb8ea6457051c3dba84a589760` have explicit same-state approval from both agents.
- `chats/Claude-Codex/Study Guide Pass 1 Review/` is concluded. Approved source/PDF hashes are `d33e74d73c41b3ef0b4edbe6de52c0cc4e5597bae2d048618edb5c4523f99819` / `75e1423294cb3c4695c14920851825d602379d9ffca1aab6bcb93cbd10d998a3`.
- `chats/Claude-Codex/Tier A Selection Review/` is active. Both agents approve `agents/Claude/Tier A Host and Injection Zone Selection.md` SHA-256 `3ae39913986a1961d674d2ed7b4714f89293fa6f0e8c02f039ebca3c186696cf` as a host-selection strategy, CA1 recommendation, and discharged duration gate. No host is pinned. Amendment 2 owner re-review and the newly required no-manipulation-control Amendment 3 remain open.
- `chats/Claude-Codex/Compute Environment Update/` is concluded. Amendment 1 records the director's daytime/overnight allocation and corrected leaked-process explanation while preserving every live resource guard and capacity commitment.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` are synchronized whole-file states at SHA-256 `8d06e5887e61b84a3ac7de71e6dcdd2eff9cbea070482faa066df109982dbfc7` / `9bb0478f39711404730efbb96e6a7b6fdc711c4dc69a6d217438d032657a8c1a`. Amendment 1 is `In force`; Amendment 2 is `Proposed` pending Claude's owner re-review. Later changes use the dated amendment protocol and keep both sheets in sync.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and its PDF are complete Phase 1 artifacts. Pass 2 remains a Phase 3 deliverable.
- `director_requests.md` contains one open non-blocking item: the Phase-1-close contract review. The shared-memory question is resolved and retired; its answer does not authorize bypassing the live headroom gates.
- The repository root `README.md` is the public live-run status page; its running log is append-only. Its latest entry corrects the unsupported rig/strain boundary, records the accepted no-manipulation control pending amendment, and states that no sorter or result exists.
- Claude is the default writer for the Claim Sheet and later narrative artifacts. Codex is the required reviewer unless ownership is deliberately reassigned.
- The Reproducibility Packet is co-owned during execution. Codex owns Rung 0, the sorter-panel decision, the inference/negative-control harness, and Tier A's independent balance/manipulation gate. Rung 0 must build and pin the host injection substrate before injection because SpikeInterface 0.104.8 does not preprocess inside `generate_hybrid_recording()` and the donor templates already carry `phase_shift`.

For resumption, read `Summary of Only Necessary Context.md`, then the latest `Session Summaries/HumanReport<N>.md`. Use `references.md` rather than memory for citations.
