# Review Cycle Playbook

**Use whenever an artifact is being reviewed, and when responding after an artifact you created has been reviewed — the loop that brings an artifact still in active review to a single state both agents explicitly approve.**

**⚠️ Read the SUPERSEDING METHOD section below first — it governs, and the cycle described after it no longer binds.**

**Required inputs:**
- The artifact under review, and the chat that belongs to it.
- The reviewing agent's role: read the artifact against the standards and the artifact's own purpose.

**Output:**
- One artifact state that **both** agents have **explicitly** approved, with the feedback, edits, reasons, and approvals recorded in the artifact's chat.

**Applies these shared standards:** the append-never-overwrite discipline of the chat logs; the Standards section of `Project Details.md` (the reviewer reads the artifact against them).

---

---

# ⚠️ SUPERSEDING METHOD — Review boundary and convergence

**Directed by Randy Crespo and implemented at Claude Session 24 (addendum, 2026-08-14) and Codex Session 24 — the first session each agent runs from that point forward.**

**This section supersedes the rest of this playbook.** Everything above it — *The cycle*, *Quality checklist*, *Common failure modes* — is retained below only as the superseded record of how review ran through Claude Session 24 and Codex Session 23. Where the two disagree, this section governs. Where this section is silent, it is silent deliberately; do not reach above it to fill the gap without saying so in the review's own chat.

## The method, as directed

> ## Review boundary and convergence
>
> Before review begins, the owner creates a Review Card (in a new Review Card folder in the root directory) naming the
> candidate state, artifacts and sections in scope, purpose, acceptance
> tests, blocking-severity definition, and explicit exclusions or
> downstream gates. The candidate must be stable enough to accept,
> reject, or return; open-ended co-design happens before formal review.
>
> Round 1 is the only full-artifact review. The reviewer records all
> reasonably discoverable findings in one numbered ledger and does not
> stop at the first blocker.
>
> Round 2 and later are delta-only. They verify recorded findings and
> regressions introduced by the response. Unchanged, previously reviewed
> material is not re-audited from scratch.
>
> A new pre-existing blocker after Round 1 must be marked LATE-BLOCKER,
> must be genuinely capable of invalidating the scoped purpose, and must
> state why it was missed. A second late blocker, or any new blocker after
> Round 2, triggers human triage or a split. Non-blocking late findings
> become tracked follow-ups.
>
> A review has at most three owner-reviewer round-trips. The limit never
> forces approval. At the limit the outcome must be Approved, Approved
> with Follow-ups, Revisions Required, Split/Redesign Required, or
> Escalated.
>
> Once both agents approve the scoped candidate, that review closes.
> Later amendments, implementation work, data gates, new sections, or
> new versions receive new Review Cards and new chats. They do not keep
> the concluded review active.
>
> Reviewers may directly apply mechanical corrections. Substantive
> scientific, architectural, or interpretive changes are proposed as
> findings or patches for the owner to integrate, unless ownership is
> explicitly transferred.

**Transition rule, also directed:** *any artifact currently under review preserves its current state and starts the new review cycle with that state.* An in-flight review is not rewound and its candidate is not re-drafted; the state on disk at the moment of transition becomes the Round 1 candidate on a fresh Review Card, and the old review's chat is concluded with a `Summary.md` so its trail is preserved.

## Operating notes

These do not add rules. They record how the directed method was read on implementation, so both agents read it the same way. **Any of them may be corrected by the director**, and a disagreement about one of them belongs in the three-way chat rather than in a review.

- **Approval stays explicit and state-specific.** "Once both agents approve the scoped candidate" is read as preserving the one non-negotiable idea from the superseded text: approval is stated in the chat, names a specific state, and is never inferred from an edit, a handoff, or silence. Nothing else from the superseded cycle is carried forward by implication.
- **Review Cards live in `Review Cards/` at the repository root**, one Markdown file per card, numbered `RC-<nnn> <short title>.md`. The folder's own `README.md` carries the template and the index.
- **A round-trip is one owner→reviewer→owner exchange.** Round 1 is the reviewer's full-artifact pass; the owner's response to it and the reviewer's Round 2 verification are the second; the limit is reached after the third. Count them in the Review Card, not from memory.
- **The findings ledger is numbered and lives in the review's chat**, in the reviewer's Round 1 message. Later rounds reference finding numbers rather than restating them.
- **"Mechanical" means the correction cannot change what any consumer of the artifact does** — typography, formatting, a stale digest, a cross-reference, a name with no reader-visible consequence. When a correction's mechanical status is arguable, the project's existing proof habits settle it rather than an assertion: a stripped-docstring syntax-tree comparison, a re-run of the other agent's probe, or an explicit statement that no numerical branch was touched. Anything that survives that test as substantive is a finding, not an edit.
- **An unchanged sentence that a change elsewhere has made false is a regression introduced by the response**, and is therefore in scope in Round 2 and later. It is not "previously reviewed material re-audited from scratch." This reading matters here: it is the single most productive finding class in this project's history, and the narrow reading would rule it out.
- **A LATE-BLOCKER that was created by an earlier repair rather than missed says so**, in those terms, in its "why it was missed" statement. "It was not a defect when Round 1 read it" is an accurate answer to that question, not an evasion of it.
- **Outcomes are recorded on the Review Card**, not only in the chat, so the card is readable as the review's whole history without the transcript.
- **Precedence against `Project Details.md`.** The constitution's *Cross-review* paragraph escalates a disagreement that has not converged in about two round-trips. This section sets a limit of three round-trips for the review as a whole. The two are compatible and both bind: a **specific disagreement** that has not converged in ~2 round-trips still escalates on its own, while the **review** ends at 3 round-trips with one of the five named outcomes. Neither is a licence to exceed the other.
- **The amendment protocol is untouched.** Changes to the Claim Sheet still run through `Playbooks/claim-sheet.md`'s amendment protocol, appended and dated, never overwritten. A Review Card scopes a review; it does not amend the contract.

## Quality checklist (superseding)

- [ ] A Review Card exists **before** review begins, naming candidate state, scope, purpose, acceptance tests, blocking-severity definition, and exclusions/downstream gates.
- [ ] The candidate was stable enough to accept, reject, or return — open-ended co-design finished before the card was written.
- [ ] Round 1 is a full-artifact pass with **one numbered ledger of all reasonably discoverable findings**, not a stop at the first blocker.
- [ ] Rounds 2+ are delta-only: recorded findings and regressions introduced by the response.
- [ ] Any post-Round-1 pre-existing blocker is marked **LATE-BLOCKER**, is genuinely purpose-invalidating, and states why it was missed.
- [ ] A second late blocker, or any new blocker after Round 2, went to human triage or a split rather than another round.
- [ ] The review closed within **three** owner-reviewer round-trips, with a named outcome: Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required · Escalated.
- [ ] Both approvals name the **same** scoped candidate state, explicitly.
- [ ] Non-blocking late findings were recorded as tracked follow-ups rather than absorbed silently.
- [ ] Reviewer edits were mechanical only, or ownership was explicitly transferred in the chat.
- [ ] On close, the chat was concluded with a `Summary.md`; later work opened a **new** card and a **new** chat rather than reviving this one.

## Failure modes this method is pointed at

- **Unbounded review.** A candidate re-opened round after round, each round finding something real, with no boundary that says when the artifact is done being reviewed. Costs compound and the artifact never reaches execution.
- **Serial blocking.** A reviewer stopping at the first blocker, so the owner repairs one thing and the next round produces the second — turning one review into many.
- **Co-design wearing review's clothes.** Using the review loop to design the artifact, which has no natural stopping point because there is no fixed candidate to accept or reject.
- **Scope drift.** A review that started on one section quietly expanding to the whole document, so no one can say what was approved.
- **Silent absorption.** A late non-blocking finding folded into a repair with no record, so the trail shows a converged review rather than a deferred item.

---

## ⬇️ SUPERSEDED — retained as the record of how review ran through Claude Session 24 and Codex Session 23

*The sections below governed until the method above was implemented. They are kept because concluded reviews were run under them and their trail should stay readable, not because they still bind.*

## Purpose

Cross-review, by default, keeps the work moving by propagating corrections *forward* — a problem found in concluded work is fixed in the next piece, not by reopening the old one. While an artifact is still in active review, however, its owner and reviewer use this playbook to converge on a single state **both agents explicitly approve**, instead of stalling in comment-and-wait or drifting on an assumption that silence meant assent. This applies to every artifact review, not only to artifacts whose approval is a downstream gate.

Its one non-negotiable idea: **approval is always explicit and always about a specific artifact state.** An edit is not approval. A handoff is not approval. Silence is never approval. The loop is closed only when both agents have said, in the chat, that they approve *the same* state of the artifact.

## The cycle

1. **The owner hands off an explicitly approved state.** After creating or revising the artifact, the owning agent records what was created or changed and why, hands the artifact to the reviewer, and **explicitly approves the state being handed off**. The reviewing agent then reads it against the standards and the artifact's purpose.
2. **The reviewer may edit directly, then hands back with explicit approval.** If the review finds changes, the reviewer may implement them in the artifact itself rather than only describing them. In the artifact's chat the reviewer then states **what changed and why**, hands the artifact back, and **explicitly approves the state being handed off**. (If the review finds nothing to change, the reviewer explicitly approves the state as-is — that closes the loop.)
3. **The owner genuinely re-reviews — this step only happens if the owner comes back to the artifact.** The owning agent must re-open the artifact and review **both the feedback and the edits**, not wave them through. Then:
   - If the owner accepts both, the owner **explicitly approves** the artifact. The loop is closed.
   - If the owner does not accept both — **including accepting the diagnosis but not the reviewer's implementation of it** — or discovers a separate problem upon re-review the owner may edit the artifact and hand it back to the reviewer, stating **what changed** and **explicitly approving the state being handed off**. Back to step 1 on the new state.
4. **Continue until both agents explicitly approve the same state.** Approval is **never inferred** from an edit, a handoff, silence, or implication. Every edited handoff states its approval, every acceptance states it, and the artifact is not done until both approvals name the same state.
5. **Escalate rather than loop.** If the same issue has not converged after roughly two full review round-trips, escalate that **specific disagreement** to Randy rather than looping indefinitely. Escalate the point in dispute, not the whole artifact.
6. **The chat is the record.** The artifact's chat records the feedback, edits, reasons, handoffs, and approvals. Git history preserves file-level provenance; in-file attribution is optional unless separately required.

## Quality checklist

- [ ] Every handoff in the chat states **what changed, why, and an explicit approval** of the state being handed off.
- [ ] The owning agent actually re-opened and re-reviewed the reviewer's edits — it did not treat the reviewer's edit as final by default.
- [ ] The closing state carries **two** explicit approvals naming the **same** artifact state.
- [ ] No approval was inferred from an edit, a handoff, or silence.
- [ ] A disagreement still unresolved after ~2 round-trips was escalated to Randy, scoped to the specific point.

## Common failure modes

- **Inferred approval.** Treating the reviewer's edit, a handoff, or silence as sign-off. The loop stays open until both approvals are stated.
- **The initial handoff carries no owner approval.** Creation is not itself explicit approval. The owner must approve the state being handed to the reviewer; otherwise an as-is reviewer approval still leaves the two-approval requirement open.
- **The owner never comes back.** The owning agent has to re-open the artifact after it is reviewed; if it never does, the re-review in step 3 simply does not happen and the "agreed state" is a fiction. Owning an artifact includes returning to it.
- **Accepting the diagnosis but silently swallowing the implementation.** If the owner agrees there was a problem but not with how the reviewer fixed it, that is a real disagreement — edit and hand back, don't quietly accept edits you'd have made differently.
- **Looping instead of escalating.** Re-editing the same contested point past ~2 round-trips. Hand the specific disagreement to Randy.
- **Reopening concluded work.** This loop is for artifacts in active review, not for reaching back into already-approved work — those corrections still propagate forward per the standard cross-review discipline.
