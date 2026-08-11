# Claude — Workspace

This is Claude's workspace for the **Hybrid Ground Truth Realism** project. If you have no prior context, read this file first and it will tell you where everything is and which of it you can trust.

---

## Folder tree

```
agents/Claude/
├─ README.md                              ← you are here
├─ Summary of Only Necessary Context.md   Rewritten every session. The resume file.
├─ Literature Foundation.md               Phase 0 field survey. Dated artifact, frozen.
├─ references.md                          Running source ledger. Living document.
├─ Session Summaries/                     One human-readable report per session.
│  ├─ HumanReport1.md
│  └─ HumanReport2.md
└─ Progress Reports/                      Director-facing reports, every 8th session
   └─ Progress Report Phase 0 Close.md    and at phase transitions.
```

---

## What each file is for

**`Summary of Only Necessary Context.md`** — The handoff to my own next session. Completely rewritten at the end of every session, because a new session starts with no memory of this one. It carries the current state, the decisions made and why, the open questions, and the next steps. It deliberately does **not** repeat anything in `Project Details/` or `AgentPrompt.md`, since those are re-read in full at the start of every session.

**`Literature Foundation.md`** — The Phase 0 survey of the spike-sorting validation field: methods landscape, benchmark ranges, datasets and licenses, failure modes, open questions, references. Its job is to make sure the Claim Sheet's method choices and success bars are informed by what the field has established rather than invented on the spot. **It is a dated artifact and is frozen as written** — corrections to it propagate forward into `references.md` and into later work, not backward into the document.

**`references.md`** — The running ledger of every source that informed my work: what it covers, how it shaped a decision, a verified link, and a citation ready to transfer into the Technical Report's bibliography. **This is the living document.** Where it and the Literature Foundation disagree, this file governs. It also carries a *Pending* section for sources located but not yet verified, which are not citable until they move up, and a **corrections log** at the top recording every claim later evidence overturned — kept visible rather than deleted, so the trail stays auditable. Entries are tagged `[ANCHOR]`, `[VERIFY]` (unconfirmed claim), `[CLEARED]` (formerly unconfirmed, now verified, with who verified it), and `[SUPERSEDED]` (wrong, with the correction alongside).

**`Session Summaries/HumanReport<N>.md`** — What happened in session N, written for the director: what was done, what was decided and why, what was hard, what files moved, and what comes next. Sequential and append-only as a set; earlier reports are never edited.

**`Progress Reports/`** — Director-facing reports written at every eighth session I run, and additionally at any phase transition or approved Claim Sheet amendment. Written at the bar of the Accessible Piece: clear, honest, jargon-free.

---

## Authoritative vs temporary

| File | Status |
|---|---|
| `Literature Foundation.md` | **Authoritative but frozen** — a recorded turn, not a living document |
| `references.md` | **Authoritative and living** — the source of truth for citations |
| `Summary of Only Necessary Context.md` | **Authoritative for one session only** — rewritten each time, never a historical record |
| `Session Summaries/*` | **Authoritative and permanent** — never edited after writing |
| `Progress Reports/*` | **Authoritative and permanent** |

There is no scratch area in this workspace yet. If one becomes necessary, it will be a `scratch/` subfolder and it will be labelled as non-authoritative here.

---

## Files I own or co-own outside this folder

The Phase 1 division of labor has not been decided yet, so this reflects the framework's default writer convention plus what I have actually created.

| Path | My relationship to it |
|---|---|
| `Claim Sheet.md` | **Written by me (Session 2), in review with Codex.** I am the default writer; Codex is the required reviewer and gives final approval. Not yet an agreed state — see the review chat. |
| `README.md` (repository root — the Live-Run README) | **Created and currently maintained by me.** Ownership is open to the Phase 1 labor split. Built per `Playbooks/live-run-readme.md`. |
| `CITATION.cff`, `LICENSING.md` | Updated by me in Session 1 to describe this project rather than the framework template. Shared. |
| `Reproducibility Packet/scripts/audit_template_library.py` | Written by me (Session 2). The packet is **co-owned** with Codex; this script is mine and is packet-ready as written. |
| `chats/Claude-Codex/Phase 0 Literature Comparison/` | Opened by me. **Concluded** — see its `Summary.md`. |
| `chats/Claude-Codex/Claim Sheet Review/` | Opened by me. Active. Shared channel — append only, never rewrite. |
| `Accessible Claim Sheet.md` (not yet created) | **Default writer**, Codex reviews. Deliberately deferred until the Claim Sheet converges, so the two do not drift apart while one is being edited. |
| `Technical Report/` (not yet created) | **Default writer**, Codex reviews. |
| `Accessible Piece/` (not yet created) | **Default writer**, Codex reviews. |
| `Study Guide/` (not yet created, two passes) | **Default writer**, Codex reviews. |
| `Reproducibility Packet/` | **Co-owned** with Codex — its contents come out of both agents' execution. Created Session 2, early, per the packet-ready-as-you-go standard. |
| `director_requests.md` (not yet created) | Shared, append-only. Either agent appends when it hits director-only work. Nothing has needed it yet. |

---

## How to navigate this folder with no prior context

1. **Read `Summary of Only Necessary Context.md`.** It is written for exactly this situation and will orient you faster than anything else here.
2. **Read the most recent `Session Summaries/HumanReport<N>.md`** for the narrative of how the work got where it is.
3. **Open `Literature Foundation.md`** only when you need the field grounding — method choices, realistic benchmark ranges, known dead ends, or the reasoning behind an axis choice. It is long by design; §5 (open questions) is the part that feeds the Claim Sheet most directly.
4. **Use `references.md` as the citation source of truth.** Do not cite anything from memory, and do not cite anything sitting in its *Pending* section.

If you are Codex: the chats folder is the right place to raise anything about this work, not an edit to these files. The exception is the review cycle — when an artifact I own is formally handed to you for review, you may edit it directly and hand it back stating what changed, per `Playbooks/review-cycle.md`.
