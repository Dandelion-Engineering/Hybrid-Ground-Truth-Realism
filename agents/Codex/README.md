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
│  └─ HumanReport1.md
└─ Progress Reports/
```

## What each file owns

- **`Summary of Only Necessary Context.md`** — next-session continuity. It is rewritten at every closeout and contains only state not already owned by `AgentPrompt.md`, `Project Details/`, or the playbooks.
- **`Literature Foundation.md`** — Codex's independent Phase 0 field survey. It is a dated evidence artifact; later corrections propagate into the living ledger and downstream artifacts rather than silently rewriting the original survey.
- **`references.md`** — Codex's living source ledger. It records what each verified source establishes, how it changed the project, and a transferable citation.
- **`Session Summaries/HumanReport<N>.md`** — sequential permanent session reports for the director.
- **`Progress Reports/`** — director-facing reports at phase transitions and the scheduled session cadence. None exists yet because Phase 0 remains open.

## Authority

| Path | Status |
|---|---|
| `Literature Foundation.md` | Authoritative Phase 0 evidence artifact; dated and frozen |
| `references.md` | Authoritative living citation ledger |
| `Summary of Only Necessary Context.md` | Authoritative only for the next Codex session |
| `Session Summaries/*` | Permanent historical record |
| `Progress Reports/*` | Permanent phase/cadence record |

## Shared work outside this folder

- `chats/Claude-Codex/Phase 0 Literature Comparison/` is the append-only comparison and review channel.
- The repository root `README.md` is the public live-run status page; its running log is append-only.
- Claude is the default writer for the Claim Sheet and later narrative artifacts. Codex is the required reviewer unless ownership is deliberately reassigned.
- The Reproducibility Packet is co-owned during execution.

For resumption, read `Summary of Only Necessary Context.md`, then the latest `Session Summaries/HumanReport<N>.md`. Use `references.md` rather than memory for citations.
