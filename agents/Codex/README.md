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
│  ├─ HumanReport6.md
│  └─ HumanReport7.md
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
- `chats/Claude-Codex/Tier A Selection Review/` is active. Draft 3 remains the last same-state-approved selection artifact. Codex directly edited and explicitly approves Draft 4 SHA-256 `fa5b871e59ac5e07973eee96b02f3de33f385870138c76bf3699ecff3b8b1f75` as a strategy plus measured provenance, label-ambiguity, native-yield context, and a parameterized placement screen; Claude's owner re-review is open. No host is pinned.
- `chats/Claude-Codex/Compute Environment Update/` is concluded. Amendment 1 records the director's daytime/overnight allocation and corrected leaked-process explanation while preserving every live resource guard and capacity commitment.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` are synchronized Codex reviewer states at SHA-256 `37dcd0f8b20fcee6dc471e1eb396a0f01890a222c5807c70c03fae527a70959a` / `696b76e47ad5b4c42038abdeac18426652db8fb1d462804735d26da28d46c267`. Amendments 1 and 2 are `In force`; Amendments 3 and 4 are `Proposed` pending Claude's genuine owner re-review of those exact bytes. Amendment 3 also requires a separately approved exact pseudo-pool configuration before generation.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and its PDF are complete Phase 1 artifacts. Pass 2 remains a Phase 3 deliverable.
- `director_requests.md` contains one open non-blocking item: the Phase-1-close contract review. The shared-memory question is resolved and retired; its answer does not authorize bypassing the live headroom gates.
- The repository root `README.md` is the public live-run status page; its running log is append-only. Its latest entry forward-corrects the rig/protocol, NYU-39, and placement-parameter overclaims while preserving the earlier entry; it states that no host, sorter run, or result exists.
- Claude is the default writer for the Claim Sheet and later narrative artifacts. Codex is the required reviewer unless ownership is deliberately reassigned.
- The Reproducibility Packet is co-owned during execution. Codex owns Rung 0, the sorter-panel decision, the inference/negative-control harness, Tier A's independent balance/manipulation gate, and the two-part placement calibration: template spatial support for edge margin plus a predeclared native-spacing/generator basis for peak separation. Rung 0 must build and pin the host injection substrate before injection because SpikeInterface 0.104.8 does not preprocess inside `generate_hybrid_recording()` and the donor templates already carry `phase_shift`.

For resumption, read `Summary of Only Necessary Context.md`, then the latest `Session Summaries/HumanReport<N>.md`. Use `references.md` rather than memory for citations.
