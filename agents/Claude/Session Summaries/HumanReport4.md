# Human Report 4 — Claude

**Date and time:** 2026-08-11 16:15 PDT

**Session:** Claude Session 4

**Phase at start:** Phase 1 — Sharpening. Codex had approved an edited state of both the Claim Sheet and Study Guide Pass 1; both loops were open awaiting my re-review. The Accessible Claim Sheet did not exist and had been deferred twice.

**Phase at end:** Phase 1 — Sharpening, one step from closing. The Claim Sheet is **same-state closed**. The Accessible Claim Sheet is written and handed off. Study Guide Pass 1 is handed back with two edits. Phase 1 closes when Codex approves those two artifacts.

---

## Summary

Three things happened, in this order: I closed the Claim Sheet, I wrote the Accessible Claim Sheet that had been outstanding for two sessions, and I re-reviewed the Study Guide and found two defects in it that I fixed rather than waved through.

**The Claim Sheet is agreed.** I re-opened it at Codex's handoff hash, confirmed the bytes on disk matched before reading anything, and reviewed its two coherence edits against the whole artifact. Both were right, I found nothing to add, and I explicitly approved the same state. That closes a review that ran four turns across three sessions, in which each agent blocked the other and each accepted the block.

**The Accessible Claim Sheet exists.** It is the plain-language companion to the contract — same fifteen slots, same numbers, same commitments, written so you can read it alone, end to end, without the technical sheet open beside you. It is a translation, not a summary, and the thing I was most careful about is that no bound got softer on the way across.

**The Study Guide needed two more fixes.** I accepted all seven of Codex's corrections — four of which were genuine errors, three of them mine — and then found two of my own: a cross-reference that pointed at the wrong section, and a real gap where the guide taught injected spike timing as purely random and never mentioned that the pipeline already enforces a refractory period. That second one matters more than it sounds, and the reason is in its own section below.

No heavy compute ran. Free memory was measured at **0.89 GiB of 31.67** — the worst of four consecutive sessions — and recorded in `director_requests.md`.

---

## What I did, in detail

### 1. Closing the Claim Sheet

Codex's two edits were both cases of the contract saying slightly more than it could support.

The first: I had written that the negative control's repetition count matching the real comparison's would give them equal precision. It does not. Matching block counts fixes how many independent units enter each resample; it says nothing about how variable the thing inside them is. And the two are structurally different in exactly the way that would make their variances differ — the pseudo-comparisons draw their random nuisances independently, while the real comparison shares or matches them within a block, which is the entire point of pairing. So the negative-control band plausibly has the *larger* variance of the two and could come back noisier than the effect it is meant to calibrate, even at identical block counts. Codex's fix requires both achieved precisions to be reported rather than assumed equal, which makes that visible instead of hidden. Correct, and the kind of thing that would have been very annoying to discover during analysis.

The second: a numbered checklist in the success slot still described the older decision rule, even though I had rewritten the surrounding prose to make the new one authoritative the session before. Teaching two rules in one document is worse than teaching either. I checked the rest of the sheet for other survivals of the old phrasing and found none.

I approved the exact bytes. **Both agents have now explicitly approved the same state of the contract, and no disagreement survived.** Changes from here go through the amendment protocol rather than the review cycle.

The one disagreement I had predicted did not happen. In Session 3 I doubled the pilot's projected workload — because the negative control has to be *sorted*, not merely generated, which the earlier budget had missed — and deliberately kept the admission ceiling where Codex had set it rather than doubling it too. I expected pushback and said so. Codex agreed, and its reason was better than mine: I kept the ceiling because stricter felt safer; it kept the ceiling because *discovering that you underestimated a workload is not an argument for approving twice the budget*. That version of the rule generalises and mine does not.

### 2. Writing the Accessible Claim Sheet

This is the artifact I had deferred twice, each time for a defensible reason — the technical sheet was under active edit, the two documents have to stay in sync, and writing the companion against a state about to change means writing it twice. My own handoff notes said two deferrals was the limit. The sheet converged this session, so I wrote it this session.

It walks the same fifteen slots in the same order, so you can jump between the two documents slot-for-slot if you ever want the technical version of something. Everything is in it: the axes, the gate, the compute ladder, the arithmetic, the success bar, the failure bar, the eight ways the project must decline to answer its own question, the monetization slot with its honest *none identified*.

Three choices I made that are worth your knowing:

**I explained the decision rule with its uncomfortable consequence attached.** The comparative decision runs on `D = |I| − T` — the size of the realism effect minus a margin. Because it uses the effect's *size* regardless of direction, a genuinely near-zero effect resamples slightly upward, which makes the "realism does not matter" verdict **harder** to reach, not easier. That is conservative in the right direction, but it is conservative in the direction that costs us the outcome we think is likelier. It is in the plain-language document in full rather than compressed away, because a rule that quietly disadvantages the result you expect is exactly the rule a reader should be able to see.

**I named three specific errors this project made and had corrected in review**, at the points where the corrected rule appears: the borrowed threshold that was not comparable to anything measured here, the design where a sorter would have supplied the target used to generate its own test data, and the decision rule that treated "significant in one arm, not the other" as evidence the arms differ. My reasoning is that a contract that has been through two adversarial review rounds should let its reader see which rules were always there and which replaced a mistake — that difference is the only direct evidence the review cycle does anything. I flagged it to Codex as strikeable if it thinks it oversteps.

**I gave every number its caveat in the same breath.** The template audit's numbers are the easiest thing in this project to quote misleadingly — the "only 7 brain regions survive" figure is a worst case, not a count, and an earlier version of the public log overstated it. Every one of those numbers carries its boundary in the sentence that states it.

Every link in the document was checked this session. Two of the thirteen returned a block from the publisher's bot protection rather than a page; I confirmed both DOIs are registered and resolve to the correct papers through the Crossref API, so they are live links behind a paywall's front door, not dead ones.

### 3. Re-reviewing the Study Guide

Codex found seven things. Four were errors rather than preferences, and three of the four were mine. The one that bothers me most:

**The interaction sign was backwards in the one sentence of the document written to be read aloud.** The interaction is sorter 1's realism effect minus sorter 2's, so a negative value means realism hurt sorter *one* more. I wrote the opposite. Worse, the same paragraph said that a near-zero interaction "validates absolute scores," which inverts the central distinction the whole guide exists to teach — a near-zero interaction says the *comparison between sorters* is stable and says nothing whatever about whether the absolute numbers can be trusted. Two errors in one paragraph, in the paragraph most likely to be quoted back.

I also had the guide teaching an older version of the decision rule than the contract I had myself made authoritative one session earlier, and I had compressed Tier A's work down to "no new code" when it is a constrained selection-and-balance problem with a gate on it. Codex's edits are right on all three.

The seventh correction is the one I would least have made myself: Codex relabelled the expectation that Tier A moves absolute scores more readily than the comparison as *the project's prior* rather than an established fact. It appears as a prior in the contract; I had let it harden into a statement of fact in translation. That is exactly how a hedge dies — not by being removed, but by being restated slightly more confidently each time.

**Then I found two things of my own.**

The first is small: a forward reference pointed at the wrong section. It said the argument was in §3.3 (the manipulation check) when it is in §3.2. Trivial to fix, but this is a document whose stated test is that you can read the contract without stopping, and a reference that lands on the wrong section is a stop.

The second is not small, and it is the finding of this session worth carrying forward.

### The gap the guide had, and why an absence is harder to catch than an error

The guide taught injected spike timing as a purely random process with no memory. That is how the pipeline is usually described, and it is very nearly true. But the pipeline also enforces a **refractory period** — the brief window after firing during which a real neuron physically cannot fire again — and the guide never mentioned it.

Two costs, and the second is the real one.

It is inaccurate about the pipeline, mildly. But more importantly it leaves an absence unexplained. The contract says, in a single line, that refractoriness is *already implemented upstream* and is therefore part of the control arm rather than one of the three realism axes. A reader who has been taught that injected timing is memoryless, and who then meets three realism axes none of which is refractoriness, has no way to tell whether it was considered and set aside for a good reason or simply overlooked. The honest answer is the first. The guide gave no way to know that.

**What makes this worth a paragraph in a report rather than a line in a changelog** is that both agents read this document carefully — I wrote it and Codex reviewed it page by page against primary sources — and both of us checked what was *said* rather than what was *missing*. Every one of the nine corrections across both reviews was to a sentence that existed. Neither of us caught the one place where the problem was that no sentence existed at all. That is a real asymmetry in how review works, and it is worth knowing about before Phase 3, when the artifact under review is the technical report and the absent sentence is a limitation nobody wrote down.

Adding the paragraph pushed the build to 14 pages with the final section stranded alone on the last one — the same pagination failure Codex hit and fixed in its review. I compressed my own addition rather than enlarging the page, and the document is back to 13 pages with zero overfull and zero underfull boxes. I rendered the changed page and the final page as images and inspected both.

### 4. Cross-review, and a correction absorbed into my ledger

I read Codex's `HumanReport3.md`, both active review chats, its edits to both artifacts, and the resulting states. That satisfies the cross-review requirement, and the two artifact-specific review cycles ran on top of it.

One correction propagated into my own source ledger. My Session 1 entry for SHYBRID — a different hybrid-data tool, used in this project only as a design contrast — said that relocating a real neuron "carries its real spike train and per-spike waveform variability with it." Codex audited the actual implementation and found the narrower truth: it reuses observed spike times after a fixed shift and each spike's fitted amplitude, but assigns *fresh* random sub-sample jitter to the inserted train and does not transport each observed waveform shape. My entry was reasoning from the design idea rather than from the source, which is precisely the failure the ledger's own verification rule exists to prevent. It is now marked superseded with the correction alongside, and it partly closes a question both agents had failed to resolve in Phase 0.

---

## Challenges, and how they were handled

**The Accessible Claim Sheet's real difficulty is not vocabulary.** Translating "hierarchical paired bootstrap" into plain language is easy. Translating it without losing the *reason* it is hierarchical — that ten injected units inside one recording are not ten independent experiments, so treating them as such would produce a confidence far too high — is the actual work, because that reason is the commitment and the phrase is only its label. I wrote every statistical passage by asking what decision it constrains and then explaining that, rather than by finding simpler words for the term.

**Deciding whether to edit an artifact that had already been reviewed twice.** The review cycle escalates a disagreement that has not converged in about two round-trips, and the Study Guide was at two. But neither of my findings was a disagreement — one was a wrong cross-reference and one was a missing fact — so handing them back was cheaper than a dispute and cost the project nothing in wall-clock terms, since Codex has to open the channel anyway to review the Accessible Claim Sheet. I said so explicitly in the handoff and offered to withdraw the refractory paragraph rather than argue for it if Codex disagrees that it earns its lines.

**The pagination regression.** Adding text mid-document stranded the final section on a fourteenth page. The tempting fix is to stretch the page it fell off. The right fix is to make the addition shorter, since the addition caused it — which also produced a tighter paragraph than the one I first wrote.

---

## Files created or updated

| Path | Change |
|---|---|
| `Accessible Claim Sheet.md` | **New.** The plain-language companion to the contract: all fifteen slots, every number, every bound. Handed to Codex for review. |
| `Study Guide/Pass 1 - Conceptual Foundation.tex` | Two edits: corrected a wrong section cross-reference; added the refractory period and why it belongs to the control arm rather than to an axis. |
| `Study Guide/Pass 1 - Conceptual Foundation.pdf` | Rebuilt. 13 pages, zero overfull/underfull boxes, changed and final pages visually inspected. |
| `chats/Claude-Codex/Claim Sheet Review/Claim Sheet Review - Active.md` | My explicit approval of Codex's exact state, closing the loop; plus the Accessible Claim Sheet handoff with the three places I want attacked first. |
| `chats/Claude-Codex/Study Guide Pass 1 Review/Study Guide Pass 1 Review - Active.md` | My re-review: seven corrections accepted with the reasoning, two further edits, new hashes, handed back. |
| `agents/Claude/references.md` | SHYBRID entry marked superseded with the source-verified narrower statement; the partly-resolved verification item retired; a Session 4 row added to the corrections log. |
| `director_requests.md` | Fourth memory measurement appended to the existing entry, with a note that the "should we design for a permanent ~4 GiB ceiling" question is now the practically important one. |
| `README.md` (repository root) | Banner updated; one running-log entry recording that the contract is agreed and what the review cost; the Accessible Claim Sheet added to the reading list. |
| `agents/Claude/README.md` | Ownership table and workspace map refreshed. |
| `agents/Claude/Session Summaries/HumanReport4.md` | This report. |
| `agents/Claude/Summary of Only Necessary Context.md` | Completely rewritten for Session 5. |

---

## What did not happen, and why

- **No sorter run, no generator run, no recording download, no dependency install.** None of this session's work needed compute, and the contract requires memory to be measured immediately before a heavy step rather than as session decoration — but I measured anyway, because the trend is now the thing being tracked.
- **No progress report.** This was my Session 4, not an eighth session, and no phase transition or approved amendment occurred. Phase 1 has not closed; when it does, whichever agent closes it writes that report.
- **The Claim Sheet review chat was not concluded**, even though its loop closed. The Accessible Claim Sheet review is running in the same channel, and the two documents are required to stay in sync, so a sync defect found there is a Claim Sheet matter.
- **Nothing is blocked on you.** The memory request stays open and non-blocking.

---

## Machine state

Measured at **16:06 PDT: 0.89 GiB free system RAM of 31.67; 14,409 MiB free VRAM of 16,311.**

Four consecutive sessions, all under 4.5 GiB, and the last two under 1.1: **3.46 → 3.96 → 1.01 → 0.89**. Graphics memory has been fine every single time — about 14 of 16 GB free at every measurement — so whatever else is running on that machine is memory-bound rather than GPU-bound. The run that proved Kilosort4 works here peaked at 29.3 GiB.

This does not block anything yet, and the next heavy step (Codex's pilot) is deliberately small enough to have a chance of fitting. But four points in one direction is a trend rather than bad luck, and the useful question has shifted. It is no longer "when is the machine quiet"; it is **"should this project adopt a small permanent memory ceiling deliberately?"** That is a real design decision — it would constrain segment length and possibly the sorter panel — and the agents would rather adopt it on purpose and record it through the amendment protocol than keep re-measuring and hoping for a window. A reply of *"yes, design for about 4 GiB"* would be more useful than no reply, and better than a quiet window nobody can predict.

---

## Next steps

1. **Codex reviews the Accessible Claim Sheet** and either approves it or edits and hands it back.
2. **Codex approves or pushes back on the Study Guide Pass 1 pair** as handed back this session.
3. **Phase 1 closes** when both of those reach same-state approval. The closing agent writes the phase-transition progress report and logs the *Claim Sheet ready for director review* entry in `director_requests.md`.
4. **Phase 2 begins with Codex's Rung 0 feasibility pilot**, which measures live memory immediately beforehand and obeys the declared headroom guards.
5. **My first Phase 2 job is Tier A host and injection-zone selection**, run against both constraints at once — donor availability after the anti-cheating exclusion, and Tier C's requirement that the burst biology rest on primary evidence. CA1 is the only candidate that satisfies both on its face, and whether it actually works depends on a host-specific query nobody has run yet.
