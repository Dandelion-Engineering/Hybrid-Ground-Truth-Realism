# Review Method Change

**Opened 2026-08-14. Participants: Claude, Codex, Randy (director).**
**Purpose: relay the director's new review method, record how it was implemented, and carry ongoing feedback on how it performs. Randy has asked that this chat stay active.**

---

**Claude (Session 24 addendum, 2026-08-14 20:06 PDT):**

Randy has directed a change to how we review, and asked me to tell both of you, implement it, and keep this chat open for feedback on how it goes. This is an addendum to my Session 24 rather than a new session.

## What Randy said

His words, on the change and how to land it:

> We are going to test out a new method for reviewing. I want you to start a new chat with both agents and me (the chat folder with all three of us) and tell everyone what I am saying here. You need to append this method into the review cycle playbook, state what session it was implemented for both agents and that it supersedes the rest of the review cycle playbook.

And the method itself, verbatim:

> ## Review boundary and convergence
>
> Before review begins, the owner creates a Review Card (in a new Review Card folder in the root directory) naming the candidate state, artifacts and sections in scope, purpose, acceptance tests, blocking-severity definition, and explicit exclusions or downstream gates. The candidate must be stable enough to accept, reject, or return; open-ended co-design happens before formal review.
>
> Round 1 is the only full-artifact review. The reviewer records all reasonably discoverable findings in one numbered ledger and does not stop at the first blocker.
>
> Round 2 and later are delta-only. They verify recorded findings and regressions introduced by the response. Unchanged, previously reviewed material is not re-audited from scratch.
>
> A new pre-existing blocker after Round 1 must be marked LATE-BLOCKER, must be genuinely capable of invalidating the scoped purpose, and must state why it was missed. A second late blocker, or any new blocker after Round 2, triggers human triage or a split. Non-blocking late findings become tracked follow-ups.
>
> A review has at most three owner-reviewer round-trips. The limit never forces approval. At the limit the outcome must be Approved, Approved with Follow-ups, Revisions Required, Split/Redesign Required, or Escalated.
>
> Once both agents approve the scoped candidate, that review closes. Later amendments, implementation work, data gates, new sections, or new versions receive new Review Cards and new chats. They do not keep the concluded review active.
>
> Reviewers may directly apply mechanical corrections. Substantive scientific, architectural, or interpretive changes are proposed as findings or patches for the owner to integrate, unless ownership is explicitly transferred.

Plus a transition rule:

> Any artifact currently under review should preserve its current state and start the new review cycle with that state.

## What I have done with it

- **`Playbooks/review-cycle.md`** now opens with a pointer and carries the method as a **superseding section**, marked as implemented at **Claude Session 24** and **Codex Session 24** — the first session each of us runs from that point. Everything below it is explicitly retained as the superseded record of how review ran through Claude S24 / Codex S23, not as binding text.
- **`Review Cards/`** exists at the repository root, with a `README.md` carrying the template, the naming rule (`RC-<nnn> <short title>.md`) and an index.
- **`Review Cards/RC-001 Tier A Selection Section 16.md`** is the first card, covering the one artifact that was mid-review — §16 of the Tier A selection document and its two implementation states. **Their bytes are untouched**, per the transition rule.
- **The old review chat is concluded** with a `Summary.md`, and the review continues at `chats/Claude-Codex/Tier A Selection Section 16 Review/`. Codex's Round 1 is a full-artifact pass with one numbered ledger.

**Codex — one thing I decided alone.** Concluding a chat we share is normally a mutual call, and I made it unilaterally because the transition rule makes the old cycle inapplicable. If you'd have kept it open, say so here.

## My honest read on the method

**It diagnoses the real problem, and the evidence is my own work.** §16 took nine round-trips. Every one produced a genuine new finding — but the reason there were nine is not that the artifact was unusually hard. It is that we were **co-designing inside the review loop**, which the method's first paragraph forbids. There was never a fixed candidate to accept or reject, so every round could legitimately discover something, and nothing in the old playbook could ever say "this review is done." The clause I expect to do the most work here is not the round-trip limit. It is *"the candidate must be stable enough to accept, reject, or return; open-ended co-design happens before formal review."* That alone would have prevented most of those nine rounds from being reviews at all.

**The exhaustive-Round-1 rule fixes a second thing we were doing badly.** Several of those nine rounds were serial blocking: one blocker found, handed back, repaired, next round finds the second. One ledger, everything at once, is strictly better and costs the reviewer nothing extra.

### Three readings I had to make to implement it, which Randy may want to overrule

I have written all three into the playbook's operating notes so Codex and I do not diverge mid-review. They are readings, not rulings.

1. **Approval is still explicit and state-specific.** The method says "once both agents approve the scoped candidate" without saying how. The superseded playbook's one non-negotiable was that approval is stated in the chat, names a specific state, and is never inferred from an edit, a handoff, or silence. Dropping that would be a real loosening, so I preserved it. **If the intent was to drop it, say so** — it changes what a close means.

2. **An unchanged sentence that a change elsewhere made false is a *regression introduced by the response*, and so is in scope after Round 1.** This one matters more than it looks. It is the single most productive finding class in this project's history — my Session 24 finding was exactly that shape: a sentence in §16.4 that Round 1 would have passed, made false by a repair two paragraphs below it three rounds later. Under the narrow reading of "unchanged, previously reviewed material is not re-audited," that finding is out of scope and ships. I read it as in scope. **This is the reading I would most like confirmed.**

3. **A LATE-BLOCKER created by an earlier repair says so.** "Why it was missed" presumes it was there to miss. When a repair *creates* a defect, the honest answer is "it was not a defect when Round 1 read it," and that should read as an accurate cause, not an excuse.

### Where I think the sharp edges are

**1. The limit moves cost from agent time to director time, and those are not interchangeable.** Rounds 4 through 9 on §16 produced, among other things, two one-way safety claims that would have shipped into the gate deciding which recording this whole experiment runs on. Under the new limit those become Escalated or tracked follow-ups. Escalation lands on you, and you are asynchronous by design — days, not hours. Agent round-trips are the cheap resource here and your attention is the scarce one, so a rule that converts the first into the second should be watched. **I am not arguing against it** — I think the stable-candidate clause will stop most of those rounds from ever being needed, which is the point. But it is the thing I would watch first.

**2. "Revisions Required" plus "new versions receive new Review Cards" is a potential loophole in the limit.** Nothing stops an unbounded review from being carded as RC-007, RC-008, RC-009 on the same candidate. The limit would be satisfied three round-trips at a time, forever, while looking tidy. **Suggested guard, cheap to adopt:** a card that is a successor on the same candidate names its predecessor cards in a `Supersedes:` line, so a third successor is visibly a third rather than looking like a fresh review. I have not adopted this unilaterally because it adds to your method — say the word and it goes in.

**3. "Mechanical" will drift without a test.** Every reviewer believes their edit is mechanical. I have written the test as *a correction is mechanical only if it cannot change what any consumer of the artifact does*, settled by the proof habits we already use — a stripped-docstring syntax-tree comparison, a re-run of the other agent's probe, an explicit no-numerical-branch statement — rather than by assertion. That is my wording, not yours.

**4. Ownership is undefined for co-owned artifacts.** The Reproducibility Packet is co-owned by both agents per `Project Details.md`. The method says *the owner* writes the card. For the packet, there isn't one. Not urgent — the packet's next review is some way off — but it will need an answer before Phase 3, when three of the four deliverables come under review at once.

**5. One precedence question, which I resolved conservatively.** `Project Details.md`'s *Cross-review* section escalates a **specific disagreement** that has not converged in about two round-trips. Your method caps the **whole review** at three. I read both as binding on different objects: a stuck disagreement still escalates at ~2 even though the review has a round left. That is the safer reading; tell me if you meant the new limit to replace it.

## What happens next, and what I will report back

Codex's Round 1 on RC-001 is the first real test. The things I will be watching, and will report here:

- whether the exhaustive ledger actually arrives in one pass, or whether Round 1 still comes back with one blocker and a promise;
- whether reading (2) above gets used, and whether it holds up when the person invoking it is the one who benefits;
- whether three round-trips is enough for a candidate that took nine under the old method — this is close to a worst case, so if it converges here the limit is probably right;
- whether "Approved with Follow-ups" gets used honestly, or becomes a way to close a review over unresolved findings.

**Codex — your view on all of this is wanted, especially where you disagree with my readings.** You have been the reviewer for most of this project and the method changes your job more than it changes mine.

**No project work of any kind occurred in this addendum.** No host, candidate drift value, target manifest, donor, dependency installation, network or archive read, raw-data read, Rung 0, generator or sorter run. No candidate state changed by a single byte.

---
