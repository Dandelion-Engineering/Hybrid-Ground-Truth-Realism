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
| [RC-001](RC-001%20Tier%20A%20Selection%20Section%2016.md) | `agents/Claude/Tier A Host and Injection Zone Selection.md` §16 + two implementation states | Claude | Codex | `chats/Claude-Codex/Tier A Selection Section 16 Review/` | **Open — Round 2, delta-only, on Codex** |

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
