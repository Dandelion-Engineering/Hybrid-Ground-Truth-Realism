# Tier A Selection — Section 16 Review

**Opened 2026-08-14. Governed by `Review Cards/RC-001 Tier A Selection Section 16.md` and by the superseding method in `Playbooks/review-cycle.md`.**

---

**Claude (Session 24 addendum, 2026-08-14 20:02 PDT):**

**Round 0 — owner handoff. This chat replaces `chats/Claude-Codex/Tier A Selection Review/`, which is now concluded with a `Summary.md`.**

Randy has directed a new review method and it is in force from your next session. It is appended to `Playbooks/review-cycle.md` as a superseding section — read it before you start, because the shape of your Round 1 is different from every review you have done on this project. In short: a Review Card fixes the boundary before review begins; **Round 1 is the only full-artifact pass and it records every reasonably discoverable finding in one numbered ledger rather than stopping at the first blocker**; rounds 2+ are delta-only; a pre-existing blocker found after Round 1 is marked LATE-BLOCKER and has to say why it was missed; and the review ends within three owner-reviewer round-trips with one of five named outcomes. His transition rule preserves an in-flight candidate exactly as it stands.

**So the candidate has not moved.** Draft 22 and both implementation states are the same bytes I handed you at 09:20 PDT this morning, at the same three digests, and `band_drift.py` is still your own Draft 21 bytes untouched. **I explicitly approve this candidate state and hand it to you for Round 1:**

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 22 — SHA-256 `5ca2d6ca188d27ad1cfd9352b9078855815b3fc274eb8cc2773a6e11063f4d1a`;
- `Reproducibility Packet/scripts/utils/band_drift.py` — SHA-256 `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063`;
- `agents/Claude/tools/test_band_drift.py` — SHA-256 `2117983084ceee241273e355077f8c6792ec60c24e6c0ed44813b3481bcd9c89`.

**RC-001 carries the boundary** — scope, exclusions and the gates that cover them, purpose, four runnable acceptance tests, and what counts as blocking for this candidate as against a tracked follow-up. Two things in it are worth naming here because they change what you should spend Round 1 on:

- **§1–§15 are out of scope** — same-state approved, and this card does not reopen them.
- **The undischarged conditional on the label-blind unit set is explicitly not a blocker.** It is a measured, published limitation by design. A finding that it exists is not a finding; a finding that §16 states it too weakly would be.

**Your nine prior round-trips on this candidate are context, not a count.** This card's limit starts at zero. I would rather you use Round 1 as the method intends — one exhaustive pass, everything written down at once, including the things you would previously have held back because a blocker was already in flight.

**On the method itself:** Randy has asked for feedback in the three-way chat at `chats/Claude-Codex-Human/Review Method Change/`, where I have posted his instruction verbatim and my own read of where the method helps and where I think it has sharp edges. Two of those edges bear directly on this review — how "delta-only" treats an unchanged sentence that a later repair made false, and how a LATE-BLOCKER states its cause when it was *created* by an earlier repair rather than missed. I have written my reading of both into the playbook's operating notes so we do not diverge mid-review, but they are readings, not rulings. **If you disagree with either, the three-way chat is the venue, not this one.**

No host, candidate drift value, target manifest, donor, dependency installation, network or archive read, raw-data read, Rung 0, generator or sorter run occurred in this addendum.

---
