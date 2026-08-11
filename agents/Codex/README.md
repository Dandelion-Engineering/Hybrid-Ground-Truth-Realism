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
│  └─ HumanReport3.md
└─ Progress Reports/
```

## What each file owns

- **`Summary of Only Necessary Context.md`** — next-session continuity. It is rewritten at every closeout and contains only state not already owned by `AgentPrompt.md`, `Project Details/`, or the playbooks.
- **`Literature Foundation.md`** — Codex's independent Phase 0 field survey. It is a dated evidence artifact; later corrections propagate into the living ledger and downstream artifacts rather than silently rewriting the original survey.
- **`references.md`** — Codex's living source ledger. It records what each verified source establishes, how it changed the project, and a transferable citation.
- **`Session Summaries/HumanReport<N>.md`** — sequential permanent session reports for the director.
- **`Progress Reports/`** — director-facing reports at phase transitions and the scheduled session cadence. None exists yet in Codex's workspace; Claude wrote the Phase 0-close report in its own workspace.

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
- `chats/Claude-Codex/Claim Sheet Review/` is the active exact-state Claim Sheet review channel. Codex Session 3 approved an edited sheet at SHA-256 `a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3`; Claude's owner re-review remains open.
- `chats/Claude-Codex/Study Guide Pass 1 Review/` is the active Study Guide review channel. Codex Session 3 approved source/PDF hashes `37f7246…` / `b428782…`; Claude's owner re-review remains open.
- `Claim Sheet.md` is the active Phase 1 contract draft. It is not same-state agreed until Claude explicitly approves the current reviewed bytes or the cycle converges on a later state.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and its PDF are active Phase 1 artifacts. Both exact states are Codex-approved but not yet owner-reapproved.
- `director_requests.md` contains the non-blocking shared-memory request. It does not authorize bypassing the live headroom gates.
- The repository root `README.md` is the public live-run status page; its running log is append-only.
- Claude is the default writer for the Claim Sheet and later narrative artifacts. Codex is the required reviewer unless ownership is deliberately reassigned.
- The Reproducibility Packet is co-owned during execution.

For resumption, read `Summary of Only Necessary Context.md`, then the latest `Session Summaries/HumanReport<N>.md`. Use `references.md` rather than memory for citations.
