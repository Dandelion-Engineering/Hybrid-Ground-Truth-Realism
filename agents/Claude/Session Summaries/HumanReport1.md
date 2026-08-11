# Human Report 1 — Claude

**Date and time:** 2026-08-11 10:23 PDT
**Session:** Claude Session 1
**Phase:** Phase 0 — Literature Review
**Project state at session start:** Empty. One commit ("Project setup"), no agent work by either agent, no chats, no literature foundations.

---

## What I set out to do

This was the first session anyone has run on this project, so the workflow put me at the beginning: read the framework and the project idea, then start Phase 0, which is the independent literature survey that has to exist before the Claim Sheet gets written. Alongside that, one thing was waiting to be noticed — the repository already has a public remote, and the project's own instructions say that if it does, the first session creates the Live-Run README.

## What I accomplished

**1. The Phase 0 Literature Foundation** — `agents/Claude/Literature Foundation.md`

The main output. A six-section survey of the spike-sorting validation field, built entirely from live web searches conducted during this session. Every source carries a working link or DOI that resolved while I was looking at it; nothing is cited from memory, which is the cardinal Phase 0 rule. Sixteen sources are ledger-quality; four more are located but not yet verified and are quarantined in a *Pending* section where they cannot be cited.

The document covers: the methods landscape and the three ground-truth strategies; realistic benchmark performance ranges; the dataset/tool/license landscape; known failure modes and dead ends; and open questions that feed directly into the Claim Sheet.

**2. The running reference ledger** — `agents/Claude/references.md`

The living citation source of truth, separate from the frozen Phase 0 document. It carries every entry with a note on which decision it actually shaped, plus a *Pending* section for unverified sources and explicit `[VERIFY]` flags on claims I could not confirm from full text.

**3. The Live-Run README** — repository root `README.md`

The repository is public, so this was owed. It now shows a status banner (question, phase, `In Progress` tag, date), the run-provenance disclosure block the project requires because the agents chose this question rather than you, a lean running log, an orientation footer, and the contact block. The previous root README described the Collaboration Station framework, not this project.

**4. Fixed two files that were publicly claiming to be something else** — `CITATION.cff`, `LICENSING.md`

`CITATION.cff` still described Collaboration Station, so GitHub's "Cite this repository" button on a public repo would have generated a citation for the framework instead of this project. `LICENSING.md` still had `<YEAR>` / `<Project Title>` / `<URL>` placeholders. Both now describe this project, and both disclose that the research question was agent-selected.

**5. Opened the Phase 0 comparison chat with Codex** — `chats/Claude-Codex/Phase 0 Literature Comparison/`

Posted my findings and four specific questions I want Codex's judgement on before Phase 1 commits to anything. Phase 0 does not close until Codex's independent foundation exists and we have compared.

**6. Set up my workspace** — `agents/Claude/README.md`

---

## What I found that actually matters

Five things came out of the literature that I think change how this project should be planned. I am putting them here rather than only in the technical document because two of them cut against assumptions the project started with.

**The maintainers named a different limitation first, and proposed a fix for it.** The project brief quotes the sentence about templates not being matched to brain region. The sentence immediately before it, in the same Limitations section, says the ground-truth units had Poisson-distributed spike times that do not necessarily match the firing statistics of the original recording — and then proposes a specific remedy: estimate ongoing population firing rates and inject spike trains that follow the dynamics of nearby neurons. That is a maintainer-endorsed, implementable design, and it is *not the same thing* as the within-unit bursting the brief points at. It may be a third axis, and it may be cheaper to build than bursting is. I have raised it with Codex as a Phase 1 decision rather than acting on it unilaterally.

**Someone has already seen the fingerprint we are hunting for.** A 2020 benchmark study covering roughly 35,000 ground-truth units found that synthetic ground-truth data produces a systematically different error signature from real ground truth — and attributed it to simulations not yet reproducing the firing statistics of real recordings. That is prior empirical evidence, at large scale, pointing at exactly the axis this project would build. **It makes a negative result less likely than the project assumed going in.** That is worth knowing early: the project was framed around a clean negative being the more useful outcome, and it may not be the outcome we get.

**We now have a number to define "matters" against.** The anchor paper's own headline result — Kilosort4 beating Kilosort2.5 — has effect sizes of 0.276 and 0.408. That gives the Claim Sheet a principled yardstick: a realism effect smaller than the sorter-versus-sorter effect it is supposed to be contaminating cannot flip a ranking. Without this we would have been setting the success bar by intuition.

**Our obvious sorter choice is the one least likely to show an effect.** The companion paper from the same group flags that hybrid data injected using motion-corrected templates gives an unfair advantage to sorters that use the same motion correction. Kilosort4 and Kilosort2.5 are from one family and share that lineage. A separate paper shows sorters diverge most on *collision handling*, splitting along template-matching versus density-based lines. So a Kilosort-only comparison is the pairing most likely to return "no difference" — and a reviewer could fairly say we designed for that answer. I have asked Codex for a feasibility read on whether this machine can actually afford a second, mechanistically different sorter.

**The bursting axis has a real mechanism behind it, not just a plausibility story.** Hippocampal cells fire bursts of spikes a few milliseconds apart whose extracellular amplitude *decreases across the burst*, and burst behaviour depends on the cell's recent firing history. A sorter built two decades ago specifically models that amplitude decay. A hybrid unit made from one fixed average waveform presents a spike whose size is independent of its own firing history; a real neuron does not. Whatever accuracy inflation that causes is currently invisible to the field.

## Decisions I made, and why

**I wrote the Literature Foundation before looking for Codex's.** The playbook requires independence — two readings of the same field diverge in useful ways, and merging early destroys that. Codex has not started, so this was easy, but I want it on record as deliberate.

**I created the Live-Run README rather than asking first.** The project brief is explicit: if the repository has a public remote, publication approval was given, and the first session creates it. It does, so I did. I checked the remote was real and reachable rather than inferring it from the config file.

**I quarantined unverified sources instead of writing around them.** Five claims I could reach only in summary form are flagged `[VERIFY]` and cannot be cited until someone confirms them from full text. One of them is a quotation the project brief itself uses — a version I reached renders it with different wording, and our negative-result framing leans on that quote, so it needs checking before it appears in anything public.

**I did not install any Python dependencies.** Phase 0 needs none, and the machine was under memory pressure (below). Installing SpikeInterface and PyTorch would have been unnecessary weight during someone else's run.

**I fixed `CITATION.cff` and `LICENSING.md` even though nobody asked.** The repository is public. A citation file that names the wrong work is a live incorrect claim, not a tidiness issue.

## Challenges, and how they went

**Rate limits and paywalls.** bioRxiv rate-limited me twice, and two publishers returned 403 or redirected to a login. I routed around them via PubMed abstracts, publisher landing pages, and the eLife full texts, and where I could only reach an abstract I said so at the point of the claim rather than filling the gap from memory. This is the source of the verification debt, and it is recorded rather than hidden — five specific items with what needs checking and where.

**The temptation to merge engineering into measurement.** The project brief is honest that one realism axis has to be *built* before it can be *measured*. The literature made clear these are mechanistically different manipulations — one changes waveform shape, the other changes temporal statistics — so varying them together would make any result unattributable. Naming that early is what keeps the study design honest.

**One feasibility question I could not answer from reading.** Whether the template library actually contains enough brain-region-matched templates, at comparable amplitude and signal quality, for the specific recordings we would use. The region values I could confirm skew heavily toward visual cortex. This is a database query rather than a literature question, it is cheap, and it should be run before Phase 1 commits to that axis. It is the largest single feasibility risk I found.

## Compute environment measured this session

Recorded per the project's standing instruction, so the next session inherits evidence rather than a hunch.

At **2026-08-11 10:23 PDT**:
- **RAM: 4.42 GiB free of 31.67 GiB** — about 86% in use. Another project was clearly running.
- **VRAM: 14,731 MiB free of 16,311 MiB** (1,580 MiB in use).
- **Project venv contains only `pip==25.0.1`.** SpikeInterface, PyTorch, and Kilosort4 are not yet installed here. There is no `requirements.txt` yet.

For context: the pre-project feasibility run that proved Kilosort4 works on this machine peaked at 29.3 GiB of system RAM. **Started at this moment, that run would have failed.** No heavy work was attempted this session, and none should be attempted without re-measuring at that moment.

## Files created or updated

| Path | What |
|---|---|
| `agents/Claude/Literature Foundation.md` | **Created** — Phase 0 survey, six sections, 16 verified sources |
| `agents/Claude/references.md` | **Created** — running source ledger with pending/verify sections |
| `agents/Claude/README.md` | **Created** — workspace guide |
| `agents/Claude/Session Summaries/HumanReport1.md` | **Created** — this file |
| `agents/Claude/Summary of Only Necessary Context.md` | **Rewritten** — was empty |
| `README.md` (repo root) | **Replaced** — Live-Run README, State A |
| `CITATION.cff` | **Replaced** — was describing the framework, not this project |
| `LICENSING.md` | **Updated** — placeholders filled |
| `chats/Claude-Codex/Phase 0 Literature Comparison/Phase 0 Literature Comparison - Active.md` | **Created** — opened, awaiting Codex |

## Next steps

**Blocking Phase 0 close:** Codex's independent Literature Foundation, then the comparison in chat. Nothing else closes the phase.

**For my next session, in priority order:**
1. Read Codex's Literature Foundation properly and respond in the comparison chat — this is also my cross-review obligation.
2. Run the template-library feasibility query (regions available vs regions in the candidate recordings, with amplitude and SNR distributions). Cheap, and it de-risks an axis before Phase 1 commits to it.
3. Clear as much verification debt as the rate limits allow — particularly the quoted sentence the project's framing depends on, and whether Kilosort4's own simulator already models the effect we are calling missing.
4. Begin the Claim Sheet once Phase 0 closes. I am the default writer for it; Codex reviews and approves.

**Nothing is blocked on you.** No `director_requests.md` entry was needed this session. If you want to weigh in on one thing, it would be this: the literature suggests a negative result is *less* likely than the project assumed at the outset, and there may be a third realism axis closer to what the maintainers actually asked for than the two in the brief. Both are agent decisions under the framework and Codex and I will settle them in Phase 1 — but you may want to know the shape of the project could shift slightly before the Claim Sheet lands in front of you.
