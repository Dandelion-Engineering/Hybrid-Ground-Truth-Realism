# Claude Human Report — Session 46

**Date and time:** 2026-08-18 06:27 PDT

**Phase:** Phase 2 — Execution

**Outcome:** **RC-007 is closed at `Revisions Required` by explicit two-agent
consensus at the Convergence Decision** — the first time this project has used
that mechanism, and it cost one message each. Codex's F7-R2 blocker is accepted
and disputed in no part; I added one correction of its scope (the defect was
live on **four** surfaces, not three). The repair was then made **outside formal
review** as **Draft 32**, the tracked split-half question was **settled** while
it was still free to settle, and **RC-008** is open with a new chat and a
Round-1 request to Codex. **Nothing executable in §19 moved**, and that is
proved mechanically rather than asserted. No estimator exists, no candidate's
noise value was measured, no archive was read, no host is pinned, and rank 2
remains unmeasured.

---

## 1. What this session was for

Session 45 submitted the final Round-3 response the three-round review limit
allows. Codex's verdict arrived at 05:24 PDT: **`Revisions Required`**, on one
blocker the Round-3 response itself created. Under the superseding review method
that is a Convergence Decision trigger, not a fourth repair round. Codex wrote
their one convergence statement into the card and owed me mine.

So the session had exactly one thing it had to do — write my convergence
statement and either concur or counter-propose — and then, once the card
closed, as much of the repair as could be done well.

## 2. The blocker, and why it is real

Draft 31 said, in its withdrawal of an earlier false claim, that a value of the
internal-uncertainty diagnostic `R_null_sampled` above the tolerance `M` is
**sufficient** to withhold the measurement. §19.6's pass rule evaluates four
branches in order, and homogeneity is branch 3. So at an in-band noise level
with `R_space_sampled = 3`, `R_null_sampled = 3` and `M = 2`, branch 3 fires
first and the candidate **fails on homogeneity**; branch 4 — the withholding
branch — never runs, because its `R_space_sampled ≤ M` precondition is false.

Two published sentences, one state, two dispositions.

**I re-derived it before writing anything.** `probe_rc007_convergence.py`
implements §19.6's four branches from the document rather than from Codex's
description and evaluates them over the whole truth table. Codex's case
reproduces exactly. **39 checks, 0 failed.**

## 3. The one thing I found that Codex's statement did not

Codex named three live surfaces carrying the unconditional claim: the status
line, §19.5 and §19.10. **There are four.** The fourth is **§19.12**, the record
subsection describing Draft 31, which states the claim in the present tense and
was not marked superseded. A repair reconciling three surfaces would have left
the contradiction standing in the fourth, in a subsection a reader treats as the
document's own account of what it decided.

My probe locates each occurrence **by byte offset** against the section
headings and asserts where it lives, so the count is measured rather than
recalled — and `mutate_rc007_convergence.py` breaks the document four ways and
requires each break to be caught **on its own check** rather than merely on the
whole-document digest. **4 of 4 caught, control green.**

## 4. The decision I had to make, and how I refused to make it on preference

Codex permitted two repairs: condition the prose on `R_space_sampled ≤ M`, or
give a high null precedence and make the high/high case `unmeasurable`. The
first keeps the executable rule and edits prose; the second changes what the
gate does.

I did not want to choose that on taste, so I looked for something already
approved that answers the same question. **§16.7 does.** It is the drift gate's
pass rule, written in Session 17, reviewed under RC-001, approved and unedited
since — it lies inside the 144,664-byte span whose digest every review card in
this project publishes. Its rule is:

- `Delta_10min > L` → **fails**, labelled *resolved drift* or *noise-limited*
- `Delta_10min ≤ L` with `Q95_null > L` → **unmeasurable**

That is the same asymmetry, in the same order, in the same cell. I implemented
both rules from their own documents and compared them cell by cell: **they agree
in all four cells.** Reordering §19.6 to give the null precedence **changes
exactly one cell — the disputed one — and puts the noise gate out of parallel
with approved text precisely there**, a parallel §19.5 claims in its own words.

So the prose yields to the branches, and the rule the branches always
implemented is now written down once:

> **`R_null_sampled` can convert a would-be pass into `unmeasurable`, and can
> change how a failure reads; it never converts a would-be failure into anything
> else.**

That is §16.7's own line-level statement transposed rather than invented.

## 5. The argument against my own position, recorded rather than buried

Under the branch order a candidate can be **rejected on homogeneity using a
number the section itself says the estimator may not resolve at scale `M`**. If
`R_null_sampled > M`, §19.5's own words are that the two halves disagree by more
than the tolerance the gate asks about — so `R_space_sampled > M` in that state
may be the instrument rather than the band. On a project whose entire subject is
the difference between grading the instrument and grading the thing, that is
uncomfortable, and branch 3's `resolution-limited` label records the discomfort
without removing it.

What settles it against that argument is (a) rejection is the direction a host
screen is *allowed* to be wrong in — §19.6 already declares its floor conditions
necessary and not sufficient — and (b) the approved drift gate resolves the
identical cell the same way. Both halves are in the convergence statement, in
§19.13, and in the card.

**And the honest scale of the blocker is stated too:** branch 3 and branch 4 are
both rejections and both advance the pinned candidate order, so the choice
between the two repairs **does not change which host this project ends up
using.** It changes what the report says happened. That is not a reason the
blocker was small — two published sentences disagreed — but it is the truth
about its reach, and leaving it out would have made the finding sound larger
than it is.

## 6. The tracked question I closed while it was still free

RC-007 tracked one open design question: whether the split-half diagnostic
should use two **contiguous** halves of each window or **interleaved**
sub-blocks. Draft 31 deferred it on the grounds that a design change in a final
review round has nothing left to check it, and required it to be settled before
the estimator's first run.

**Draft 32 settles it: contiguous.** The reasoning is that interleaving would
reduce the cancellation problem by making the two half-estimates share their
local epochs — and estimates drawn from interleaved samples of the same 434 ms
are **positively correlated**, which pushes their ratio toward 1 and
**compresses the very spread the statistic exists to register**. That
compression is in the **permissive** direction, on the one side of the
instrument the decision rule actually uses. Contiguous halves touch at a single
boundary and are close to independent for a signal band-limited above 300 Hz,
which is what a disagreement measurement needs.

**And the contamination that motivated the alternative is not a defect under the
one-sided reading:** a high value withholds because the window's samples do not
support one scale per channel, and within-window non-stationarity is exactly
such a case.

§19.5 states the argument, states what it gives up (a low value still certifies
nothing), and **labels itself structural and unmeasured** — which is what I have
asked Codex to attack first in RC-008. This had to be decided now: the moment a
candidate's value is known, the rule stops being free to change.

## 7. How I proved that nothing else moved

RC-007 is closed, so its checker `probe_rc007_spec.py` — 288 checks — is a
closed card's evidence script, and the method says not to extend one. Rather
than port 288 checks into a new file (a whole-file rewrite of a test suite is a
coverage risk this project has already learned about), **I used it as a
regression baseline.**

`probe_rc008_spec.py` runs it as a subprocess against Draft 32 and requires
**exactly 288 checks with exactly six failures**, named individually, in both
directions — a seventh red is a finding, and so is a sixth that is not on the
list. The six are two string checks on text this repair deliberately changed,
and four restatement-census counts that grew because the new §19.13 and the new
status line restate the same numbers. The checker then **recounts the census by
region** and asserts that the counts inside §19.1–§19.12 are unchanged.

**57 checks, 0 failed.** `mutate_rc008_spec.py`: **12 of 12 mutations caught**,
control green, including "edit a closed section" and "break branch 4".

**One thing that will look like rot next session and is not.** `probe_rc007_convergence.py` was green against Draft 31 and goes **red against Draft 32**, because the first thing it does is authenticate the frozen candidate it was written to be evidence about. That is the method working rather than failing: a closed card's evidence script is allowed to go red, and its recorded output is committed beside it.

## 8. Two checker expectations of mine were wrong, and both in my favour to fix

The Draft-32 checker failed twice on its first run, and both were **my
expectations, not the artifact**:

1. I asserted the withdrawn wording was gone from §19.5. It is still there
   **once** — inside the sentence that withdraws it, because a withdrawal has to
   name what it withdraws. The check now asserts exactly that: one occurrence,
   and it is the withdrawal.
2. I expected the new rule sentence in three places. There are **four** — I had
   forgotten I also put it in the status line. The check now expects four and
   names the fourth.

That is now six sessions in a row where every failing check of mine was a wrong
expectation and every mutation the harness missed was a gap in my checker. The
artifact has not been the defect in any of them, which is worth saying because
it is the reason to keep writing the checks.

## 9. What I did not do

- **I did not measure anything.** No archive read, no candidate's noise value,
  no estimator, no packet file touched, no host pinned, rank 2 still unmeasured.
- **I did not re-argue any closed finding.** RC-008's *Out of scope* says so
  explicitly.
- **I did not extend the closed card's harness**, and I did not rewrite it.

## 10. Files created or updated

**Created**

- `agents/Claude/tools/probe_rc007_convergence.py` — convergence evidence, 39
  checks, `4f65da23…`
- `agents/Claude/tools/rc007_convergence_2026-08-18.txt` / `.json` —
  `bb1a78aa…` / `a0de6881…`
- `agents/Claude/tools/mutate_rc007_convergence.py` — 4 mutations, `98f6b8b6…`
- `agents/Claude/tools/mutate_rc007_convergence_2026-08-18.txt` — `16d5694d…`
- `agents/Claude/tools/probe_rc008_spec.py` — Draft-32 owner checker, 57 checks,
  `885e8d2d…`
- `agents/Claude/tools/rc008_spec_2026-08-18_draft32.txt` / `.json` —
  `a503957d…` / `2342ff94…`
- `agents/Claude/tools/mutate_rc008_spec.py` — 12 mutations, `72628d4b…`
- `agents/Claude/tools/mutate_rc008_spec_2026-08-18_draft32.txt` — `c5acce90…`
- `Review Cards/RC-008 Host Noise Gate, Convergence Repair.md`
- `chats/Claude-Codex/Section 19 Convergence Repair/Section 19 Convergence Repair - Active.md`
- `chats/Claude-Codex/Host Noise Gate/Summary.md`
- `agents/Claude/Session Summaries/HumanReport46.md` (this file)

**Updated**

- `agents/Claude/Tier A Host and Injection Zone Selection.md` → **Draft 32**,
  `6933c89e…` — §19.5, §19.6, §19.10, §19.12's supersession note, new §19.13,
  new status line
- `Review Cards/RC-007 Host Noise Gate Specification.md` — Claude's convergence
  statement, terminal disposition, **closed**
- `Review Cards/README.md` — RC-007 status, RC-008 row
- `README.md` (root) — one running-log entry, **86 dated entries**
- `chats/Claude-Codex/Host Noise Gate/Host Noise Gate - Active.md` → **renamed
  Concluded**, after appending my convergence statement
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`

## 11. Machine state, measured

- **06:09 PDT** — 14,914 MiB of 32,425 free; GPU 955 of 16,311 MiB used.
- Nothing heavy ran. The heaviest step was the Draft-32 mutation harness, twelve
  subprocess runs of two checkers over copies of one 301 KB document; about
  twenty seconds and no measurable memory pressure. **No archive was read.**

## 12. Next steps

1. **Codex's RC-008 Round 1.** A full-artifact pass over §19 at Draft 32. Four
   things named for attack: the `FilterRecording` identity claim, the settled
   contiguous split, whether a **fifth** unconditional surface exists, and
   whether the regression-baseline instrument could go green for the wrong
   reason.
2. **Then the estimator**, against whatever §19 says when RC-008 closes — a
   packet utility plus a synthetic harness, the shape `band_drift.py` took after
   §16 closed. **Not before.**
3. **Rank 2 (NYU-12 Probe01) can be measured for drift** at any time; the
   command is unchanged and takes about three minutes and 88.6 MB.

**Clause 5 now binds.** RC-008 is the one successor RC-007 is allowed. If it
also reaches a non-approval, the method requires the work to be split or
redesigned with the changed boundary named — not another card. Both agents know
that going in, and it is written at the top of RC-008.
