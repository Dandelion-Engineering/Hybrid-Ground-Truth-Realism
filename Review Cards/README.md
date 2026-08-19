# Review Cards

A **Review Card** is the boundary of one review. It is written by the artifact's **owner, before review begins**, and it is what makes a review something an agent can finish rather than something that runs until nobody has anything left to say.

The method these cards implement was directed by Randy Crespo and is the superseding section of [`Playbooks/review-cycle.md`](../Playbooks/review-cycle.md), implemented at **Claude Session 24** and **Codex Session 24**. Read that section before writing or answering a card.

## What a card is for

Without a card, a review has no stated candidate, no stated scope, and no stated bar — so every round can legitimately discover something new, and the review has no natural end. The card fixes all three in advance, which is what lets a review reach one of four named outcomes inside three round-trips.

A card scopes a review. **It does not amend the Claim Sheet**, and it does not approve anything by existing.

## Naming and layout

- One Markdown file per card, in this folder: `RC-<nnn> <short title>.md`, numbered in creation order and never reused.
- The card is a living record of *its own* review: the owner writes it before Round 1, and both agents append the round log and the final outcome to it as the review runs.
- A card is never rewritten to describe a different candidate. A new candidate — a later amendment, the implementation of something this card only specified, a new section, a new version — gets a **new card and a new chat**.

## Index

| Card | Candidate | Owner | Reviewer | Chat | Status |
|---|---|---|---|---|---|
| [RC-001](RC-001%20Tier%20A%20Selection%20Section%2016.md) | `agents/Claude/Tier A Host and Injection Zone Selection.md` §16 + two implementation states | Claude | Codex | `chats/Claude-Codex/Tier A Selection Section 16 Review/` | **Approved — closed 2026-08-15** |
| [RC-002](RC-002%20Archive-Reading%20Drift%20Command.md) | `Reproducibility Packet/scripts/utils/archive_units.py` + `Reproducibility Packet/scripts/measure_host_drift.py` + its synthetic harness | Claude | Codex | `chats/Claude-Codex/Archive-Reading Drift Command Review/` | **Revisions Required — closed 2026-08-15** by Convergence Decision; candidate frozen and unapproved, repair continues on RC-003 |
| [RC-003](RC-003%20Archive-Reading%20Drift%20Command,%20Bounded-Read%20Repair.md) | the archive-reading drift command, bounded-read repair and response-created verification state | Claude | Codex | `chats/Claude-Codex/Bounded Archive Read Review/` | **Approved — closed 2026-08-16** with explicit same-state approval; no Convergence Decision needed |
| [RC-004](RC-004%20Session%20Reference%20Time%20Pair%20Check.md) | the session-reference-time pair check that replaces converter-version equality, and its suite and mutation state | Claude | Codex | `chats/Claude-Codex/Session Reference Time Pair Check Review/` | **Closed — `Approved` at Round 2, 2026-08-16.** Both agents explicitly approved the same five-file state (Codex 08:17 PDT, Claude 2026-08-16 09:09 PDT). Opened 2026-08-16 against RC-003's *approved* code on evidence that did not exist during that review. **Not a successor**; clause 5 does not apply. Two blocking findings at Round 1, both accepted and repaired; no Convergence Decision |
| [RC-005](RC-005%20Missing%20Depth%20Recovery,%20Wired.md) | the missing-depth recovery wired end to end: the reader's NaN/infinity split, `utils/missing_depth.py`, the command, §17 of the selection document, and both suites | Claude | Codex | `chats/Claude-Codex/Missing Depth Recovery Review/` | **Closed — `Approved with Follow-Ups` at Round 2, 2026-08-17.** Both agents explicitly approved the same seven-file state; F1 and F2 are repaired, two nonblocking close-time findings are tracked, and no Convergence Decision fired. Opened against RC-004's *approved* code on a defect class found after it closed: the rank-1 candidate carries 231 NaN depths. **Not a successor**; clause 5 does not apply. The missing-depth implementation gate is cleared; rank-1 measurement is the next separate execution step |
| [RC-006](RC-006%20Rank%201%20Drift%20Measurement%20and%20Step%2011.md) | the first real drift measurement of rank 1 (CSHL047 Probe01), §18 of the selection document, and the promotion of `measure_host_drift.py` to runbook step 11 | Claude | Codex | `chats/Claude-Codex/Rank 1 Drift Result/` | **Closed — `Approved` at Round 2, 2026-08-17.** Both agents explicitly approved the same nine-file state. All four Round-1 reporting findings are repaired; owner evidence passed 61/61 and the independent reviewer probe 48/48; no code or result byte moved in the response. Rank 1's strict drift gate is discharged, but no host is pinned and four host gates remain open. **Not a successor**; clause 5 does not apply |
| [RC-007](RC-007%20Host%20Noise%20Gate%20Specification.md) | the host noise gate specified as a contract: §19 of the selection document, the measured raw-AP storage layout it is built on, and the two instruments that check it | Claude | Codex | `chats/Claude-Codex/Host Noise Gate/` | **CLOSED — `Revisions Required`, two-agent consensus at the Convergence Decision, 2026-08-18.** Draft 31 is frozen and unapproved. The accepted F4-R1, F6-R1, tightened 170-chunk / 73.780-second coverage theorem and one-sided-null repairs reproduce, but the final response introduced one blocker (F7-R2): the unconditional claim that a high `R_null_sampled` withholds the measurement contradicts the ordered branches, which classify the high-space/high-null case as `fails on homogeneity`. **Claude concurs and adds that the claim is live on four surfaces, not three.** The repair is Draft 32, made **outside formal review**, and reaches review only through one successor card. No estimator exists, no candidate noise was measured, and no host is pinned. **Not a successor**; clause 5 does not apply |
| [RC-008](RC-008%20Host%20Noise%20Gate,%20Convergence%20Repair.md) | the host noise gate after the RC-007 convergence repair: §19 of the selection document, the withholding branches, split rule, level extrema and regression instruments | Claude | Codex | `chats/Claude-Codex/Section 19 Convergence Repair/` | **Open at the Convergence Decision — Draft 34 (`ecccfa56…`) is frozen and unapproved, 2026-08-19.** The terminal delta pass verifies every Round-3 repair: 241/241 specification checks, the expected 288/16 legacy state, 42/42 caught mutations, 32/32 owner evidence and 33/33 independent evidence. F8-R3 remains blocking because the draft's sole split rationale assigns a tunable period to the reviewed fixed even/odd alternative, even though that rule contains no period and changes `passes` to `unmeasurable`. Codex proposes and approves `Split/Redesign Required`; Claude owes the other four-field statement and explicit consensus or the smallest counterproposal. No fourth repair, estimator, candidate noise read or host decision is authorized. **Successor to RC-007; clause 5 applies — no second like-for-like successor is allowed** |

## Template

Copy this into a new card and fill every field. A field that genuinely does not apply says so and says why; it is not deleted.

```markdown
# RC-<nnn> — <short title>

**Owner:** <agent>   **Reviewer:** <agent>
**Opened:** <YYYY-MM-DD HH:MM TZ>, <owner> Session <n>
**Chat:** `chats/<...>/`
**Supersedes:** <predecessor card, or `none`>
**Status:** Open — awaiting Round 1

## Candidate state
Exact files and digests. One state, stable enough to accept, reject, or return.

## In scope
Artifacts and sections this review covers.

## Out of scope
Named exclusions, and the downstream gates that will cover them instead.

## Purpose
What this candidate has to do for the project. The bar the review judges against.

## Acceptance tests
Concrete, runnable or checkable. What "this passes" means before anyone reads it.

## Blocking severity
What counts as a blocker for *this* candidate, as distinct from a follow-up.

## Round log
| Round | Date | Who | Findings | Outcome |
|---|---|---|---|---|

## Convergence Decision
Written only if a convergence trigger fires. Each agent, once: the minimum claim it thinks can ship, the evidence that controls, the strongest evidence against its own position, and one acceptable safe disposition.

## Outcome
One of: Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required. **`Escalated` was removed on 2026-08-14** by the director's instruction; a convergence trigger runs the agent-only Convergence Decision and the card still closes at one of these four.

## Tracked follow-ups
Non-blocking findings deferred out of this review, and where they go next.
```
