# Human Report 3 — Claude

**Date and time:** 2026-08-11 14:18 PDT

**Session:** Claude Session 3

**Phase at start:** Phase 1 — Sharpening. Claim Sheet reviewed and edited by Codex, handed back awaiting my re-review.

**Phase at end:** Phase 1 — Sharpening. Claim Sheet re-reviewed, further edited, handed back to Codex. Labor split agreed by both agents. Study Guide Pass 1 drafted and in review.

---

## Summary

This session had one obligation and one opportunity. The obligation was to genuinely re-review the Claim Sheet after Codex edited it — the step the review-cycle playbook names as the one most likely to be skipped, because it depends entirely on the owning agent choosing to come back. The opportunity was Study Guide Pass 1, which is mine under the labor split and does not depend on the review converging.

Both are done. I also created `director_requests.md` for the first time, because the machine measurement this session was bad enough to be worth Randy's attention.

## The Claim Sheet re-review

I verified the file on disk still hashed to the exact bytes Codex approved, then read the whole sheet and diffed it against my draft rather than reading Codex's description of what it changed. That distinction matters: reviewing a summary of edits is not reviewing edits.

**I accepted all six of Codex's diagnoses and all six of its implementations.** Four of them caught real errors in my draft, and I want them on the record rather than absorbed quietly:

1. **"Hold absolutely everything else fixed" was false for Tier A** — and it appeared in the sentence the entire document is built around. Changing a donor template's brain region necessarily changes which template it is. Codex replaced the claim with covariate-matched donor *pairs*, which is the honest version.
2. **Tier B's design was circular.** I had written that injected firing rates would follow "the population rate estimated from nearby host units" — but getting units requires *sorting the host*, which would have made one of the sorters under test a supplier of the target used to generate its own test data. Codex replaced it with a sorter-independent activity proxy computed once from the untouched recording. This was the most dangerous of the four because it would have survived into execution looking perfectly reasonable.
3. **My "loss of separation" decision rule was the significant-versus-non-significant fallacy.** I had declared that a sorter gap being statistically clear in one arm and unclear in the other counted as evidence the arms differed. It does not — that comparison has to be made directly. Worse, I had argued in my handoff that this was the *likelier* of the decision events, which means the error was load-bearing rather than decorative.
4. **The anchor paper's 50–200 µV range is a target for rescaling injected templates, not a property donor templates must already have.** I had imported a post-rescaling quantity as a pre-rescaling filter and then built a feasibility shortlist on top of it.

The correction I would least have found myself is the anatomical one. A Neuropixels probe passes through several brain regions on its way in, so labelling a whole recording with one region — which my draft did — would have made Tier A's manipulation partly fictional. Codex replaced it with a pinned injection zone and per-placement matching.

### Three things I found on re-review, and edited rather than approved

None of these contradicts Codex's work. Two are consequences of its edits that were not carried all the way through, and one is a gap between two slots that its Tier C edit turned into a real problem.

**1. The compute budget was missing half the experiment.** The design's strongest control generates matched "pseudo-arms" where nothing was actually manipulated, to measure how much apparent effect the machinery invents from random variation alone. Those pseudo-arms have to be *sorted*, not merely generated — the whole point is to compare sorter behaviour on them. But the pilot's admission budget extrapolated from the real arms only, understating the primary run's sorter load by a factor of two. I redefined the minimum tranche to include the negative control (200 recording-minutes per candidate sorter per tier), declared that the pseudo-arm block count matches the real block count, and deliberately *kept* Codex's 48-hour ceiling rather than doubling it — so the bar is now stricter than what it wrote. It still admits a sorter running about 14× slower than real time, against Kilosort4's measured 4.5× faster, so it is strict without being unreachable. I also required the *panel-level* projection be recorded, because a panel can consist entirely of individually admitted sorters and still not fit: at the ceiling, two sorters across three tiers project to 288 sorter-hours.

**2. Slot 11 stated the same decision two different ways.** The authoritative rule is that a derived margin quantity's confidence interval sits below zero; a later paragraph said the interaction's interval "lies wholly inside" the margin band. Within a single resample those are the same event, but as *interval* statements they are different operations — one carries the uncertainty in the estimated threshold, the other treats the threshold as exactly known. Two defensible operations, and the project would have had to pick one after seeing results, which is exactly when picking is worst. I made the first authoritative everywhere. I also declared a consequence rather than leaving it to be discovered: because the margin is built on an absolute value, its distribution is folded at zero, so a genuinely null result resamples slightly upward and the "bounded negative" verdict is *harder* to reach, not easier. The rule errs toward calling a real null "inconclusive" — the right direction, but it costs us the outcome we think is likelier, so it belongs in writing now.

**3. The sheet never said whether the host recording stays the same across the three tiers — and Codex's Tier C edit made that load-bearing.** The contract reasons from a Tier A result to what it does and does not license about Tiers B and C, and requires Tiers A and B together as minimum content. If the host changes between tiers, every one of those cross-tier statements becomes a comparison across recordings as well as across axes. I declared one host and injection zone across all tiers by default, with any deviation recorded as a limitation and the cross-tier comparison *dropped* rather than made across hosts.

### The finding that came out of that third edit

This is the part I would point at if Randy reads only one paragraph of this report.

Codex's Tier C edit added a constraint: the burst parameters currently rest on hippocampal CA1 biology, so a Tier C run anywhere else needs fresh primary evidence or it is a synthetic stress test rather than a biological-realism test. My own Session 2 audit added a separate constraint: Tier A needs a region whose donor pool survives the rule that donors may not come from the host's own source dataset. Those two constraints were introduced independently, three sessions apart, by different agents, for unrelated reasons.

They intersect in exactly one place. **CA1 is the only region in the audit that satisfies both on its face** — 12 in-caliper Neuropixels 1.0 templates across 4 source datasets before any host-specific exclusion. It is a candidate and not a decision: CA1's worst-case count after removing its largest contributing dataset is 6, below the ten units the design injects, so its viability depends entirely on which dataset the chosen host belongs to. I have named it in the Claim Sheet so that host selection is run against both constraints simultaneously. The failure mode it forecloses is cheap to fall into and expensive to discover: satisfy Tier A, then find that Tier C cannot use the host Tier A picked.

### Where the review stands

I explicitly approved the state I handed back and recorded its hash. The loop is **not closed** — my three edits sit on top of the state Codex approved, so they need its approval or its pushback. I flagged one point where I expect it may disagree: I made the pilot budget stricter rather than raising the ceiling to absorb the doubled tranche, and I said in the chat that if Codex thinks the ceiling should have gone to 96 hours, I would rather have that argument now than at Rung 2.

**I also explicitly accepted the division of labor**, including Codex's extension that it owns Tier A's balance gate. That extension is straightforwardly right, and this session made it more so: I am now the agent proposing CA1, which makes me exactly the wrong one to grade whether the selection was balanced.

## Study Guide Pass 1

Written, built, and handed off for review. Thirteen pages, two `pdflatex` passes, zero overfull boxes, no errors.

The playbook is unusually clear that the audience is Randy specifically and that expert approval is not the test, so I built around the two things he actually needs to be able to do: read the Claim Sheet without stopping, and follow Phase 2 as a participant rather than a spectator. Concretely that meant introducing each concept at the moment it becomes necessary and making sure it is load-bearing later — burst amplitude shrinkage arrives as one of four reasons sorting is hard, then reappears as the thing Tier C manipulates and the thing CA1 is required for.

Math appears four times: the accuracy metric, one sorter's realism effect, the difference between two sorters' realism effects, and the decision margin. I kept the third because I could not find a way to make "difference in differences" precise in prose, and the entire project turns on it not being the same thing as "accuracy went down."

The largest deliberate omission is that the guide says almost nothing about how sorting algorithms work internally. Sorter identity is a variable in this project, not its subject, and a director who understood Kilosort4's internals but not the difference between a main effect and an interaction would be worse equipped for Phase 2, not better. What he gets instead is the one algorithmic fact that is load-bearing here — that sorter families diverge on collision handling — which is why the panel has to span families and why the temporal tiers are the ones that could move a ranking. I flagged this to Codex as the judgement most worth attacking.

Two new sources were verified by live search this session and added to my ledger: Jun et al. 2017 for Neuropixels, and Efron 1979 for the bootstrap. Nothing from the ledger's unverified *Pending* section is cited anywhere in the guide.

## The machine, and why I opened `director_requests.md`

I measured free memory at 14:16 PDT: **1.01 GiB free of 31.67 GiB**. VRAM was fine at 14,286 of 16,311 MiB.

That is the third consecutive session measuring a heavily contended machine, and the trend is the wrong way — 3.46 GiB, then 3.96 GiB, now 1.01 GiB. The feasibility run that proved Kilosort4 works here peaked at 29.3 GiB. Started at any of those three moments it would have failed, slowly and confusingly.

No heavy step ran this session, so nothing was at risk. But the next scheduled heavy step is Codex's Rung 0 pilot, which is the first thing in the project that needs real memory, and at 1 GiB free it could not start. This is director-only by the project's own account — other Dandelion projects run on this machine uncoordinated with this one, and there is no scheduler and no way for an agent here to ask them to wait. So I created `director_requests.md` and logged it with the measurements, a clear statement of what is and is not blocked, and four fallbacks the agents are already taking.

**Nothing is blocked.** The request asks Randy for a quiet window, information about what else is running, or a decision that this project should permanently design around a small memory footprint — the last of which the agents would rather adopt deliberately than discover.

One note on ordering: the playbook describes the Phase-1-close entry as this file's first. That entry is still owed and will be logged when Phase 1 closes; this one precedes it because the blocker arrived first. I recorded that in the file so it does not read as a process error.

## Challenges and how they were handled

**The re-review was the hard part, and the difficulty was psychological rather than technical.** Codex's review was thorough, well-argued, and correct, and it had already explicitly approved the file. The path of least resistance was to agree and move on — which the playbook names as a failure mode by its exact shape ("accepting the diagnosis but silently swallowing the implementation"). The thing that made the difference was reading the diff rather than the summary, and then treating each edit as a claim to check rather than a fix to accept. The three findings all came from that: two of them are places where Codex's own correction implied a consequence elsewhere in the document that had not been followed through, which is a category of error only a second reader looking at the *whole* document can catch.

**Deferring the Accessible Claim Sheet a second time was a real decision, not drift.** I committed last session to writing it the moment the sheet converges. It did not converge — I handed edits back. Writing the plain-language companion against a state I had just modified and expected Codex to respond to would mean writing it twice and risking the two drifting apart, which is the specific defect the contract names. Study Guide Pass 1 was the better use of the session because it is conceptual foundation and is genuinely independent of the three joints still open. I said this explicitly in the chat rather than letting it look like a second silent deferral.

## Files created or updated

| Path | Change |
|---|---|
| `Claim Sheet.md` | Three re-review edits: negative control folded into the pilot's compute budget (Slots 5 and 9); the comparative decision rule made single-valued with its conservatism declared (Slot 11); one host/injection zone across tiers, with CA1 named as the leading candidate (Slot 7). Explicitly approved by me at SHA-256 `d3e75363…` and handed back. |
| `Study Guide/Pass 1 - Conceptual Foundation.tex` | **New.** Director's Study Guide, Pass 1. Builds to 13 pages with zero overfull boxes. |
| `Study Guide/Pass 1 - Conceptual Foundation.pdf` | **New.** The compiled artifact. |
| `chats/Claude-Codex/Claim Sheet Review/…Active.md` | Appended my re-review: acceptance of all six of Codex's edits with the four errors named, the three new edits, explicit approval of the new state, explicit acceptance of the labor split, and one flagged disagreement. |
| `chats/Claude-Codex/Study Guide Pass 1 Review/…Active.md` | **New channel.** Pass 1 handed off with explicit approval and four specific things I want attacked. |
| `director_requests.md` | **New.** First entry: shared-machine RAM contention, with measurements, fallbacks, and a clear statement that nothing is blocked. |
| `agents/Claude/references.md` | Two new verified entries — Jun et al. 2017 (Neuropixels) and Efron 1979 (bootstrap). |
| `agents/Claude/README.md` | Labor split recorded as agreed; Study Guide, the new chat, and `director_requests.md` added to the ownership table. |
| `README.md` (root, Live-Run) | One log entry — the compute-budget omission and the CA1 convergence. Study Guide row updated to "Pass 1 drafted, in review." |
| `agents/Claude/Session Summaries/HumanReport3.md` | This report. |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten for Session 4. |

## Next steps

1. **Codex approves my three Claim Sheet edits or pushes back.** If it pushes back on the pilot ceiling, that is the one disagreement I flagged and expect.
2. **The moment the sheet converges, I write the Accessible Claim Sheet** — it is the first thing in my Session 4 queue and it has now been deferred twice for the same sound reason, which is twice as many times as I would like.
3. **Codex reviews Study Guide Pass 1.** It is not complete until Codex explicitly approves it.
4. **Phase 1 closes** when the Claim Sheet, the Accessible Claim Sheet, and the Study Guide Pass 1 all have same-state approval from both agents, and the labor split is agreed — which it now is. Whoever closes it writes the phase-transition progress report and logs the structural `director_requests.md` entry.
5. **Phase 2 begins with Codex's Rung 0 pilot** — and it measures free memory immediately beforehand, against a machine that has been at or under 4 GiB free for three consecutive sessions.

**Nothing is blocked on the director**, including the request I filed this session.
