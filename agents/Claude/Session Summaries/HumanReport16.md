# Human Report 16 — Claude

**Current date and time:** 2026-08-13 04:18 PDT

**Session:** Claude Session 16

**Phase at start:** Phase 2 — Execution. All six Claim Sheet amendments `In force`. Codex had handed Draft 3 of the Tier A real-arm donor-matching rule across for exact-state review at the very end of its own Session 15. No host pinned, no host-specific pool opened, no donor selected, no generation, no Rung 0, no sorter run.

**Phase at end:** unchanged. Draft 4 of the matching rule is explicitly approved by me and handed back to Codex for owner re-review. Still no host, no pool, no result.

**Progress-report trigger:** yes — count-based, my session 16. `agents/Claude/Progress Reports/Progress Report Session 16.md` was written after the session's normal work, as an addition to it.

---

## Summary

This session was a review turn. Codex handed me Draft 3 of the rule that pairs each injection-zone donor template with a region-unaware control partner — the rule that has to be fixed *before* anyone can see the candidate pool, because once the pool is visible every remaining choice can be defended individually while the collection of them steers the answer.

I accepted every Draft 3 decision, including the one reading of mine that Codex rejected two sessions ago, and then found two defects that Draft 3 inherits rather than introduces. One of them has been in the project since its second session and is mine in origin. The other is a gap between what the contract pins and what the rule depends on.

The session produced a Draft 4 (approved and handed back), one new offline measurement tool with a recorded output, a `references.md` entry for that measurement, a `README.md` running-log entry, and the count-based progress report. Nothing heavy ran; total execution was stdlib parsing, hashing, and a 66,045-element enumeration that finishes in under a second.

## 1. Startup and inherited state

`.agent-turn` named Claude and `.agent-session.lock` did not exist. I created the lock, re-read `.agent-turn`, confirmed it still named Claude, and worked through `AgentPrompt.md`: the complete `Project Details/Project Details.md`, my `Summary of Only Necessary Context.md`, every `Summary.md` and `Active.md` in a chat I participate in, the review-cycle and progress-report playbooks, and the in-force contract state.

My own continuity file said "nothing is open on you in any chat." That was true when it was written and false by the time I read it: Codex posted the Draft 3 handoff at 03:11 PDT, an hour after my last session closed. **A continuity file describes the moment it was written, not the moment it is read**, and the chats are what settle what is open. Reading them first is what caught it.

Four hashes verified on disk before any reading: `Claim Sheet.md` `2feda611…`, `Accessible Claim Sheet.md` `679918f7…`, my host-selection Draft 7 `13c192d3…`, and Codex's matching rule at `e63e1031…` — all matching what the chat claimed.

## 2. What I accepted in Draft 3

Before the defects, what survived checking, because a review that reports only what it found is not a review:

- The **one-time target-eligibility manifest** that partitions the sixteen-key zone universe `Z` into survivors `T` and killed keys `K`, with `N = count(T)` computed once. This closes the eligibility/rota loop cleanly.
- Keeping the **removal set at all sixteen** while the target set shrinks. A key killed by a target-side gate is not established to clear the region-unaware gate, so it may not re-enter the control arm.
- The **host's block-placement gate kept separate from donor eligibility** — a failed block rejects the host rather than dropping a donor and redealing.
- The generalization of every cardinality to `N` and of the source count to `S_T`, computed from the actual survivors rather than assumed to remain four.
- The corrected exposure-weight statement, `(q + 1)/q`, replacing my erroneous 22% claim.
- **The reading Codex rejected in my Draft 2** — that the source-count floor could be suspended until the final fallback. Codex was right: a floor is what is preserved *while* pairwise blocking is relaxed, so it binds at every stage.

## 3. The first defect: the floor's unit is the finest granularity, not the coarsest

This is the substantive finding of the session.

### What I did

The rule makes exactly one provenance quantity binding: the selected controls must use exactly `S_T` distinct `dataset` values, where `S_T` is the distinct-`dataset` count of the surviving target set. That count has been the project's provenance measure since Session 2, when I wrote the leave-one-dataset-out audit that produced the 7-area shortlist. That script's own docstring says it "treated the `dataset` column as an opaque provenance token."

I opened `Reproducibility Packet/scripts/utils/template_metadata.py` and read what the column is. **`dataset` is the probe-insertion identifier** — the full `000409_sub-<subject>_ses-<session-uuid>_..._<insertion-uuid>.zarr` string — and both the session UUID and the subject are regex-parsed out of that same string.

I wrote `agents/Claude/tools/source_count_granularity_probe.py` to measure the consequences rather than argue them. It is stdlib-only, offline, reads the pinned snapshot and nothing else, and takes under a second.

### What it found

**The three levels nest strictly.** The probe asserts one session and one subject per `dataset` across all 2,183 Neuropixels 1.0 rows and does not raise. So choosing which `dataset` values a set uses *determines* that set's session and subject counts. I verified this by assertion rather than by reading the regex and believing it.

**The library is far narrower than its source count suggests.** 37 `dataset` values, **24 sessions, 12 animals** — independently reproducing the twelve that Amendment 2 point 1 already counts. The CA1 sixteen's four sources are four sessions and four animals.

**Equal source counts do not imply equal animal counts, and the gap is large:**

| Subset size | Possible subsets | Spanning that many animals | Share |
|---|---|---|---|
| 1 | 37 | 37 | 100% |
| 2 | 666 | 608 | 91.3% |
| 3 | 7,770 | 5,884 | 75.7% |
| **4** | **66,045** | **37,424** | **56.7%** |

At the size that applies, **28,621 of 66,045 four-source control sets span fewer than four animals, and 74 span exactly one.**

So a control arm can satisfy the floor *exactly* — four sources against four — while being a one-animal arm facing a four-animal target arm. That is Slot 7's own sentence surviving the constraint written to prevent it, wearing a matching source count.

### The fix, and why it is free

Draft 4 makes the equality two-level. **Level A** matches all three counts. **Level B** is Draft 3's floor, `S_T` alone. Every stage tests Level A first and Level B only if Level A admits no complete assignment at that stage; a stage relaxes only when Level B also fails there.

Three properties made me willing to make this edit inside Codex's artifact rather than only propose it:

1. **No feasibility is lost.** Level B remains reachable everywhere, so nothing that would have worked can now fail. A tightening that could push a host to Slot 12.3 would have been a decision to hand over, not to make.
2. **The search shrinks.** Because the coarser counts are determined by the source set, Level A filters Codex's existing enumeration — at `S_T = 4` it removes 28,621 of 66,045 subsets before any assignment is attempted.
3. **It binds in exactly two places.** Stage 1 (insertion-blocked): all three automatic. Stage 2 (session-blocked): sessions and subjects automatic, so the levels coincide. Stage 3 (subject-blocked): subjects automatic, sessions not — two targets from different sessions of one animal can both draw controls from a single session. Stage 4: nothing automatic.

I was explicit in the handoff that I am **not** claiming the contract requires this. Slot 7 names a source-dataset count and Amendment 2 point 3 makes it the floor; Level B satisfies both literally. What I claim is that Level A applies Amendment 2's own stated reasoning — that once the provenance keys are parsed rather than hashed, the sheet should ask for the stronger check the parsing makes available — to the count itself. If Codex reads that as needing contract visibility, I will write the amendment.

## 4. The second defect: the rule is pinned on top of an unpinned input

Section 2.2 consumes an exposure schedule carrying, per occurrence, a **commanded placement** and a **placement seed**. All three matching quantities in Section 4 — realized amplitude, realized effective SNR, realized depth — are measured *at that commanded placement*, and Section 3's edge eligibility depends on it too.

Amendment 2 point 5 and Amendment 6 point 4 both say those seeds "are randomized" and neither says where the randomness comes from. Amendment 6 pins the rota order to a SHA-256 derivation from `1910753866` precisely so that "the gates select a subset; they cannot select its order." Nothing does the equivalent for the placements.

**This is the same defect class Codex closed in Amendment 6 point 1 in Session 14** — its own note there was that a pinned threshold evaluated at an unpinned site is not a pinned gate. Here: a pinned matching rule over unpinned placements is not a pinned matching. Section 1 says the document exists so no one can try several defensible options once the pool is visible and keep the most reassuring one; redrawing the schedule is one more option that can be tried, and Section 10's claim that the rule's *inputs* are fixed in advance does not hold without it.

Draft 4 requires the schedule's nuisance draws to be a recorded deterministic function of a master seed derived by the construction the contract already uses twice, one stream per occurrence identifier, with a matching failure semantic. Independence across occurrences, blocks and pseudo-arms — which the negative-control band genuinely needs — is preserved. What is removed is the freedom to draw twice and keep one.

**This is in Codex's lane and I said so.** The exposure schedule and the placement rule are its work; I have written a requirement on them into a document it owns. I offered explicitly to have it moved into the placement-rule specification or into a contract amendment. What I would not do is leave it in a chat message — that is exactly the Session 15 lesson.

## 5. A third, smaller correction

Section 4 said "U includes Z." `U` is the *eligible* region-unaware pool, so it contains the zone donors that clear region-unaware eligibility, not necessarily all sixteen — and Codex's own Section 2.4 says a key killed by a target-side gate is not established to clear the region-unaware one. The conclusion is untouched, since `R = U minus Z` removes exactly the zone rows `U` does hold. Restated at its true strength.

## 6. The pass I had to run on my own first pass

My first edit added the two-level test plus a sentence mapping the old phrase onto it — and left all four stage bullets restating Level B literally in their operative text. **A governing paragraph does not repair an operative sentence that contradicts it.** That is the same shape as the Amendment 6 supersession problem, and I nearly shipped it after spending a session writing about it. The second pass rewrote all four bullets and the "no fifth stage" sentence, and a third one-line pass fixed a sentence I had written badly enough to confuse a reader.

The mechanic that caught it was reading the finished section back as a reviewer rather than trusting the diff.

## 7. One probe recorded without an edit

The common ruler is estimated over **edge-occurrences**, so each candidate is weighted by how many target occurrence sets it is feasible for. That weighting is not neutral — feasibility breadth is partly a depth and band-margin property, and the standard deviations set the relative weight of the three quantities in the cost. Section 4 argues carefully about which *pool* supplies the ruler and is silent about which *unit* it is computed over.

I still think Codex's unit is right: the values that enter `abs(z_target - z_candidate)` are edge-occurrence values, so estimating spread over anything else prices the differences in units they are not taken in. So it is recorded in Section 10 and in the handoff, with no edit and no carve-out. A third ruler diagnostic for a choice I believe is correct would be noise.

## 8. What I verified rather than read

- Draft 3's digest on disk before reading a word.
- The provenance nesting, by assertion across all 2,183 rows.
- The full `(sessions, subjects)` census at k = 1…4, not only the headline. The 74 single-animal four-subsets are `(2,1) 10 + (3,1) 48 + (4,1) 16`.
- CA1's sixteen: 4 insertions, 4 sessions, 4 animals, `[6, 5, 3, 2]`, KS044/KS046/KS051/KS055 — matching the recorded history exactly.
- `C(37, 4) = 66,045` re-derived independently of the enumeration.
- Both edit passes asserted **exactly one match per replacement across the whole file before any write** — 15 and 8 replacements.
- The finished file: zero curly quotes, zero U+FFFD, no CRLF, balanced fences, `git diff --check` clean. Non-ASCII is 16 em dashes, 1 en dash, 3 ellipses.
- The chat append verified by reading the file back and confirming the prior content is a byte-exact prefix.

## 9. Cross-review

I read Codex's `HumanReport15.md` in full as the required recent-work review. I have no disagreement with it. Its §5 is the section my first finding lands next to; the finding is new information rather than a correction of anything it says, and it went into the chat and the artifact rather than into a note here.

## 10. Machine state

Measured at 04:18 PDT: **RAM 7.66 GiB free of 31.67 (75% in use); VRAM 1,025 MiB used of 16,311; 648.2 GB free on `C:`.** Nothing heavy ran. No network read, no dependency install, no raw-data read, no template-array pull, no candidate-pool inspection, no generator, no Rung 0, no sorter run.

## 11. Files created or updated

| Path | What changed |
|---|---|
| `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` | Reviewer edits, Draft 3 → **Draft 4**, `5dc8022d…`. Two-level provenance-count equality; derived-seed requirement on the exposure schedule; ruler-pool sentence restated; four stage bullets rewritten; new failure semantic; Section 9 tests extended; reviewer approval recorded in Section 10. |
| `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md` | Appended my Session 16 review, findings, verification list and exact-state handoff. |
| `agents/Claude/tools/source_count_granularity_probe.py` | **New.** Offline stdlib probe measuring what a distinct-`dataset` count does and does not constrain. |
| `agents/Claude/tools/source_count_granularity_probe_2026-08-13.txt` | **New.** Its recorded output; Draft 4 cites these numbers. |
| `agents/Claude/references.md` | New entry: the provenance-granularity census as one of this project's own results, with its pre-host boundary stated. |
| `agents/Claude/Progress Reports/Progress Report Session 16.md` | **New.** Count-based progress report. |
| `README.md` (repository root, Live-Run) | New running-log entry for both findings. |
| `agents/Claude/README.md` | Workspace tree, tools description and chat-status rows updated. |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten for Session 17. |
| `agents/Claude/Session Summaries/HumanReport16.md` | This file. |

## 12. What is next

1. **Codex re-reviews Draft 4**, and decides where the derived-seed requirement should live.
2. **The drift gate is still mine and still open.** Last session established that the shipped drift column is unusable — accumulated absolute path length, confounded with spike count at ~0.79 by IBL's own report. The replacement quantity has to be defined, and its threshold's basis justified, **before** any candidate recording is measured against it.
3. **The capacity gate needs re-establishing** under Amendment 6's stricter joint-placement condition; the Session 8 sweep no longer discharges it.
4. Five of the ten packet steps remain not-re-run, and the README says so. Best folded into work that needs the archive anyway.

## 13. What I got wrong, and what it cost

- **My continuity file told me nothing was open on me.** It was accurate when written and stale by the time I read it. Cost: nothing, because I read the chats before acting.
- **I shipped a first pass with four operative sentences contradicting the paragraph I had just written to govern them.** Cost: one extra pass. Found by re-reading the section as a reviewer, which is the only reason it did not go out.
- **The `dataset`-as-opaque-token reading is originally mine**, from Session 2, and it propagated into Slot 7's phrasing, Amendment 2's floor and two drafts of Codex's rule before anyone read the column. Cost: the constraint has been weaker than intended for eleven sessions. It cost nothing downstream only because no pool has ever been opened — which is the argument for doing all of this before the data is visible.
