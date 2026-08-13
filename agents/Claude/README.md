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
├─ Tier A Host and Injection Zone         Phase 2 working analysis. Live, and under
│  Selection.md                           review by Codex.
├─ Session Summaries/                     One human-readable report per session.
│  ├─ HumanReport1.md
│  ├─ HumanReport2.md
│  ├─ HumanReport3.md
│  ├─ HumanReport4.md
│  ├─ HumanReport5.md
│  ├─ HumanReport6.md
│  ├─ HumanReport7.md
│  ├─ HumanReport8.md
│  ├─ HumanReport9.md
│  ├─ HumanReport10.md
│  ├─ HumanReport11.md
│  └─ HumanReport12.md
├─ tools/                                 Test harnesses for packet tooling. Not part
│  └─ mutation_test_runbook_checker.py    of the packet; see below.
└─ Progress Reports/                      Director-facing reports, every 8th session,
   ├─ Progress Report Phase 0 Close.md    at phase transitions, and at approved
   ├─ Progress Report Amendment           Claim Sheet amendments.
   │  Provenance and Finite Donor Pool.md
   ├─ Progress Report Session 8.md
   └─ Progress Report Amendment
      Negative Control Pools.md
```

---

## What each file is for

**`Summary of Only Necessary Context.md`** — The handoff to my own next session. Completely rewritten at the end of every session, because a new session starts with no memory of this one. It carries the current state, the decisions made and why, the open questions, and the next steps. It deliberately does **not** repeat anything in `Project Details/` or `AgentPrompt.md`, since those are re-read in full at the start of every session.

**`Literature Foundation.md`** — The Phase 0 survey of the spike-sorting validation field: methods landscape, benchmark ranges, datasets and licenses, failure modes, open questions, references. Its job is to make sure the Claim Sheet's method choices and success bars are informed by what the field has established rather than invented on the spot. **It is a dated artifact and is frozen as written** — corrections to it propagate forward into `references.md` and into later work, not backward into the document.

**`references.md`** — The running ledger of every source that informed my work: what it covers, how it shaped a decision, a verified link, and a citation ready to transfer into the Technical Report's bibliography. **This is the living document.** Where it and the Literature Foundation disagree, this file governs. It also carries a *Pending* section for sources located but not yet verified, which are not citable until they move up, and a **corrections log** at the top recording every claim later evidence overturned — kept visible rather than deleted, so the trail stays auditable. Entries are tagged `[ANCHOR]`, `[VERIFY]` (unconfirmed claim), `[CLEARED]` (formerly unconfirmed, now verified, with who verified it), and `[SUPERSEDED]` (wrong, with the correction alongside).

**`Session Summaries/HumanReport<N>.md`** — What happened in session N, written for the director: what was done, what was decided and why, what was hard, what files moved, and what comes next. Sequential and append-only as a set; earlier reports are never edited.

**`tools/`** — Harnesses that test the packet's own tooling but do not belong inside the packet, because they reproduce no result and a reader copying the packet out should not be told to run them. Currently one: `mutation_test_runbook_checker.py`, which breaks a throwaway copy of the packet ten different ways and confirms `check_runbook_consistency.py` catches each one, plus an unmutated control. Takes the packet path, a scratch directory and the interpreter as arguments; never touches the real packet.

**`Progress Reports/`** — Director-facing reports written at every eighth session I run, and additionally at any phase transition or approved Claim Sheet amendment. Written at the bar of the Accessible Piece: clear, honest, jargon-free.

**`Tier A Host and Injection Zone Selection.md`** — The Phase 2 analysis behind my share of the labor split: which host recording and which anatomical injection zone Tier A should use, what the donor pool for that zone actually is, and what the choice costs. It is a **host-selection strategy and zone recommendation under active review**, not a completed selection — no host asset is pinned. Codex owns Tier A's independent balance and manipulation gate precisely so the agent proposing the selection is not the agent approving it. Draft 6 carries Codex's Session 5 reviewer edits and rulings (§7), my Session 6 owner re-review (§8), Session 7's §9 (acquisition provenance, measured) and §10 (the placement screen, parameterized) as Codex reviewed and edited them, Session 8's §11 (the amplitude-convention check, run), Session 9's §12 (the CCF label map completed without importing an ontology), and Session 10's §13 (how hard a region-blind matcher pulls toward the injection zone). Session 11's §14 records the independent re-derivation of Codex's corrected expectation and the two contract defects that re-derivation exposed. **§1–§14 are same-state approved by both agents** as Draft 7, `13c192d3…`, at Codex's Session 11 turn. It states what it has not tested as prominently as what it has.

---

## Authoritative vs temporary

| File | Status |
|---|---|
| `Literature Foundation.md` | **Authoritative but frozen** — a recorded turn, not a living document |
| `references.md` | **Authoritative and living** — the source of truth for citations |
| `Tier A Host and Injection Zone Selection.md` | **Live and under review** — a proposal, not a settled selection. Nothing in it is pinned until Codex's gate closes. |
| `tools/*` | **Authoritative as tests, not as artifacts** — re-runnable, but nothing depends on their output |
| `Summary of Only Necessary Context.md` | **Authoritative for one session only** — rewritten each time, never a historical record |
| `Session Summaries/*` | **Authoritative and permanent** — never edited after writing |
| `Progress Reports/*` | **Authoritative and permanent** |

There is no scratch area in this workspace. `tools/` is not one — everything in it is meant to be re-runnable by anyone. If a true scratch area becomes necessary it will be a `scratch/` subfolder, labelled non-authoritative here.

---

## Files I own or co-own outside this folder

**The Phase 1 division of labor is agreed by both agents as of Session 3** (proposed by me in the Claim Sheet review chat, extended and accepted by Codex, explicitly accepted by me). My share: the **Accessible Claim Sheet**, **Study Guide Pass 1**, and **Tier A host/injection-zone selection**. Codex's share: the **Rung 0 feasibility pilot**, the **sorter-panel decision**, the **inference and negative-control harness**, and **Tier A's balance/manipulation gate** — the last one deliberately, so the agent choosing the templates is not the agent grading whether the choice was balanced. Tiers B and C are assigned after Rung 0, and for each one the manipulation check is owned by whoever did *not* write that tier's generator.

| Path | My relationship to it |
|---|---|
| `Claim Sheet.md` | **Written by me (Session 2); reviewed and edited by Codex (Sessions 2 and 3); re-reviewed and edited by me (Session 3); re-reviewed and explicitly approved by me (Session 4).** **Same-state closed** at SHA-256 `a5f5860…` — both agents approved identical bytes and no disagreement survived. Changes from here go through the amendment protocol, not the review cycle. **Session 6 added an `## Amendments` section.** **As of Codex's Session 11, Amendments 1 through 5 are all `In force`** — Amendment 5 (injection-zone donors removed from the real control arm) entered force when Codex approved my Session 11 state unchanged, which also unblocks Tier A's donor-matching rule. The approved text above that section is untouched and still governs. |
| `README.md` (repository root — the Live-Run README) | **Created and currently maintained by me.** Ownership is open to the Phase 1 labor split. Built per `Playbooks/live-run-readme.md`. |
| `CITATION.cff`, `LICENSING.md` | Updated by me in Session 1 to describe this project rather than the framework template. Shared. |
| `Reproducibility Packet/scripts/audit_template_library.py` | Written by me (Session 2), **refactored onto `utils/template_metadata.py` in Session 10** — the duplicated fetch, parse, float and caliper helpers are gone, and the refactored script was shown to reproduce its tracked report byte for byte from a live fetch. Gained `--cache` for offline re-runs. Packet-ready as written. |
| `Reproducibility Packet/scripts/audit_zone_neighbour_enrichment.py` | Written by me (Session 10). Measures how strongly a region-blind covariate matcher is pulled toward the injection zone's own donors, which is the evidence behind Amendment 5. Stdlib only, offline against the tracked snapshot. Packet-ready as written. |
| `Reproducibility Packet/scripts/utils/` | Written by me (Session 5): `remote_hdf5.py`, `dandi.py`, `template_metadata.py`, `ccf_labels.py`; plus `host_anatomy.py` (Session 7). `anatomy_index.py` is Codex's (Session 6). Shared logic, imported rather than copy-pasted, per the software standard. Co-owned with Codex like the rest of the packet. |
| `Reproducibility Packet/scripts/audit_donor_provenance.py` · `survey_host_anatomy.py` · `validate_ccf_label_map.py` | Written by me (Session 5) for Tier A selection. Packet-ready as written. |
| All ten packet step scripts | **Their `--help` examples were rewritten in Session 12** and are now generated from the packet runbook rather than transcribed, so `--help` and `README.md` print the same command. Behaviour is unchanged and every tracked result still replays byte for byte. |
| `Reproducibility Packet/scripts/screen_host_timing.py` | Written by me (Session 6), hardened by Codex (Session 6). Applies the duration gate by measuring each candidate's real rate and duration from its own `timestamps` dataset. Packet-ready as written; resumable via `host_timing_index.jsonl`. |
| `Reproducibility Packet/scripts/audit_subject_provenance.py` | Written by me (Session 7). Reads each subject's laboratory, institution and protocol from its own NWB header, and records which subject fields the substrate does not carry at all. Packet-ready as written. |
| `Reproducibility Packet/scripts/derive_ccf_label_map.py` | Written by me (Session 9). Derives the CCF long-name↔acronym bridge from DANDI 000409 (CC-BY-4.0) and the template library (MIT) rather than importing the Allen ontology, whose terms are noncommercial. Emits `results/ccf_label_map_derived.txt`, the replay records beside it, and the map at `scripts/utils/ccf_label_map_derived.json`. Supports `--from-records` for no-network replay. Packet-ready as written. |
| `Reproducibility Packet/scripts/audit_amplitude_conventions.py` | Written by me (Session 8). Settles whether the donor library's `amplitude_uv` and the host files' `median_spike_amplitude_uV` are the same quantity — they are not — by reading both definitions from primary sources and then measuring the conversion on host units via the files' own `waveform_mean`. Packet-ready as written. |
| `Reproducibility Packet/scripts/screen_injection_placement.py` | Written by me (Session 7). Applies Slot 7's placement and label-ambiguity gate, reports the capacity sweep, and measures the host's own unit density and amplitude distribution inside each candidate zone. Has a `--from-records` mode that rebuilds its report with no network reads. Packet-ready as written. |
| `requirements.txt` | **Created by me (Session 5)** at the project's first dependency install (`h5py`, `numpy`). Shared and append-as-you-install: whoever installs a package pins it here in the same session. |
| `chats/Claude-Codex/Phase 0 Literature Comparison/` | Opened by me. **Concluded** — see its `Summary.md`. |
| `chats/Claude-Codex/Claim Sheet Review/` | Opened by me. **Concluded** (Codex, Session 4) — see its `Summary.md`. |
| `chats/Claude-Codex/Study Guide Pass 1 Review/` | Opened by me (Session 3). **Concluded** (Codex, Session 4) — see its `Summary.md`. |
| `chats/Claude-Codex/Tier A Selection Review/` | Opened by me (Session 5). **Active, and the live one.** Codex reviewed, edited and ruled (Session 5); I re-reviewed and contested one ruling (Session 6); Codex accepted the counter-proposal and asked for it in the contract (Session 6); I closed Amendment 2, wrote Amendments 3 and 4, and applied the placement gate (Session 7). Codex reviewed and edited both amendments and Draft 4 (Session 7); I re-reviewed, approved Amendment 4 into force, and edited Amendment 3 (Session 8). Codex repaired three parts of Amendment 3 and approved a new state (Session 8); I verified those repairs, accepted them, and removed the injection zone's own donor pool from the pseudo-arm's search space (Session 9). Codex extended that removal to both pseudo-arms and replaced the evaluation cap with a 64-sweep cap (Session 9); I verified both, put Amendment 3 into force, and proposed Amendment 5 (Session 10). Codex corrected Amendment 5's no-reuse expectation and added the matched-policy counterfactual (Session 10); I re-derived that correction three ways, accepted both changes, and edited the amendment to retire a sentence in Amendment 3 that it falsifies (Session 11). Codex approved Draft 7 and all three edits unchanged and put Amendment 5 into force (Session 11). **Still active** because host selection and the matching-rule/configuration gates remain open; nothing in it is currently open on me. The arm-asymmetric scale-factor question was ruled on by Codex and accepted — it is a manipulation-check diagnostic, not a matching covariate. Codex owns the footprint/placement calibration; both agents declined to set an overcrowding threshold. |
| `chats/Claude-Codex/Reproducibility Packet Review/` | Opened by Codex (Session 11) to hand back its correction to the packet runbook's description of the label-map validator. **Active.** I verified the correction against the source and approved those exact bytes (Session 12), then opened a new cycle in the same channel by rewriting all ten scripts' `--help` examples and adding the consistency checker. Open on: twelve states, and two judgement calls I deliberately left to Codex. |
| `chats/Claude-Codex/Compute Environment Update/` | Opened by me (Session 5 addendum). **Concluded** (Codex, Session 6) — see its `Summary.md`. Amendment 1 is `In force`. |
| `Study Guide/Pass 1 - Conceptual Foundation.tex` | **Written by me (Session 3); reviewed and edited by Codex (Session 3); re-reviewed by me (Session 4); explicitly approved by Codex (Session 4) at the same source/PDF state.** Same-state closed at source `d33e74d…` / PDF `75e1423…`. 13 pages. Changes from here go through the amendment protocol. |
| `Accessible Claim Sheet.md` | **Written by me (Session 4) against the exact approved Claim Sheet state; explicitly approved by Codex (Session 4) without edits.** Same-state closed at SHA-256 `73bff8f…`. Mine under the agreed labor split. **It must be kept in sync with the technical sheet forever; drift between them is a defect, not a backlog item** — every amendment so far has gone into both sheets in the same session, which is the standard. |
| `Technical Report/` (not yet created) | **Default writer**, Codex reviews. |
| `Accessible Piece/` (not yet created) | **Default writer**, Codex reviews. |
| `Study Guide/Pass 2 - Concept Delta.tex` (not yet created) | **Default writer**, Codex reviews. Phase 3, under the no-spoiler rule. |
| `Reproducibility Packet/` | **Co-owned** with Codex — its contents come out of both agents' execution. Created Session 2, early, per the packet-ready-as-you-go standard. |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | Written by me (Session 12). Compares every runbook step against its script's `--help` example so the two cannot drift; reads the docstring through `ast`, so what it checks is what a reader actually sees. Tested by mutation — see `tools/` above. Handed off for review, not yet approved as a state. |
| `Reproducibility Packet/README.md` · `DATA.md` · `requirements.txt` · `.gitignore` | **Written by me (Session 11)** — the packet's runbook, its data-source/licence/citation document, its own pinned dependency list, and its own ignore rules. The self-containment claim was tested rather than asserted: the folder was copied alone to a location with no other project file reachable, a fresh environment was built from `requirements.txt`, and the five offline steps reproduced their tracked reports byte for byte. The five archive-reading steps are marked in the README as not re-run. **Session 12 added the design-document pointer and the consistency-check section, and Codex corrected the Step 5 description of the label-map validator; `DATA.md` is same-state approved at `f8c6ce26…` and README is handed off at `a99d44c3…`.** Co-owned like the rest of the packet. |
| `Reproducibility Packet/results/` | Outputs and pinned upstream snapshots from my Session 5 scripts. The two snapshots (`templates_snapshot_2026-08-11.csv`, `dandi_000409_assets.json`) are **inputs a reader needs**, not rebuildable outputs — upstream is mutable, so "re-download it" is not equivalent. `.gitignore` carries a note so nobody adds a rule that catches them. |
| `director_requests.md` | **Created by me (Session 3).** Shared, append-only. The shared-machine RAM entry is **resolved and retired** — the director answered it at the end of Session 5 and the reply is recorded in place, including a correction to my own reading of the trend. Codex's Phase-1-close contract review remains open and does not block. |

---

## How to navigate this folder with no prior context

1. **Read `Summary of Only Necessary Context.md`.** It is written for exactly this situation and will orient you faster than anything else here.
2. **Read the most recent `Session Summaries/HumanReport<N>.md`** for the narrative of how the work got where it is.
3. **Open `Literature Foundation.md`** only when you need the field grounding — method choices, realistic benchmark ranges, known dead ends, or the reasoning behind an axis choice. It is long by design; §5 (open questions) is the part that feeds the Claim Sheet most directly.
4. **Use `references.md` as the citation source of truth.** Do not cite anything from memory, and do not cite anything sitting in its *Pending* section.

If you are Codex: the chats folder is the right place to raise anything about this work, not an edit to these files. The exception is the review cycle — when an artifact I own is formally handed to you for review, you may edit it directly and hand it back stating what changed, per `Playbooks/review-cycle.md`.
