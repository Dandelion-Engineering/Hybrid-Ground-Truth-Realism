# Claude Human Report — Session 50

**Date and time:** 2026-08-19 08:23 PDT

**Phase:** Phase 2 — Execution (specification design; the Part B redesign that RC-008 required)

**Outcome in one paragraph.** Codex's Session-49 audit found that my new
sensitivity sweep attached a claim to a correct matrix that its checks did not
test — I wrote *the family has no dominating member* where the check body only
tested that no member is cautious on every fixture and none on none. **I
accepted it and re-derived it independently: 30 strict pairwise dominance
relations, the exact structure Codex reported.** I then did the check nobody
had done — reproducing a probe byte-for-byte proves it is deterministic, not
that it is right — and **rebuilt all 1,024 cells along a deliberately different
code path, where they agree cell for cell.** That rebuild turned up a limit on
my own evidence that neither of us had stated: **450 of the 1,024 cells sit
exactly at the tolerance `M = 2.0`, all on the passing side**, so the fixture
family can only support claims about clearly separated values. Finally,
re-reading the frozen §19.6 for the reply found a sentence that is false:
**the half-window ratio has a 0/0 case the specification does not define, the
case is entirely decided by the split rule nobody has chosen, and its unhandled
behaviour reads as a pass in both regimes.** No host is pinned, no estimator
exists, no candidate noise value exists, and no gate moved.

---

## 1. Startup and controlling context

`.agent-turn` named Claude and no `.agent-session.lock` existed, so I created
the lock, re-read `.agent-turn`, confirmed it still named Claude, and began.

I read `AgentPrompt.md`, the complete `Project Details/Project Details.md`, and
my continuity file. For the chat protocol's Phase A I read the two active
transcripts: `chats/Claude-Codex-Human/Review Method Change/` (latest message is
Codex Session 42; Randy asked that it stay active; nothing pending on me) and
the new `chats/Claude-Codex/Part B Resolution Diagnostic Design/`, opened by
Codex at Session 49. The other eighteen chats are concluded and their
`Summary.md` files carry their context.

**No progress report is due.** The most recent count-based report is Session
48; the next is Session 56. No phase transition occurred and no Claim Sheet
amendment was approved.

**Cross-review.** Codex's `HumanReport49.md` was the newest unreviewed
collaborator work, and it is the substance of this session — it carries the
finding I answer below. I also read
`agents/Codex/tools/probe_split_family_dominance.py` in full before deciding
whether to accept its conclusion.

## 2. Codex's finding, accepted and independently re-derived

**The finding.** `probe_split_family_sensitivity.py` (Session 49) computed a
correct 32 × 32 matrix — every one of the 32 fixed split members run against 32
fixtures, one built at each member's own block length — and then one of its
checks carried the detail string *"the family has no dominating member"* while
its docstring said *"none dominates"*. The check body tested something weaker
and true: that no member withholds on every fixture and none on none. Dominance
is a pairwise set relation, and absence of an all-or-nothing member does not
imply its absence. Codex inverted the matrix and found **30 strict relations**.

**Why I did not simply accept the number.** A handed-over number gets
re-derived here; that rule has earned itself repeatedly. I computed the member
signatures from the record with my own code and got 30, with the same
structure.

**What I did that Codex could not.** Codex reproduced my probe byte-for-byte.
That establishes determinism, not correctness — nobody had checked the
arithmetic. `probe_split_family_narrowing.py` rebuilds the entire matrix from
the stated construction along a deliberately different path: repeat-and-tile
masks instead of `(i // p) % 2`, an explicit sort-based median instead of
`numpy.median`, an explicit nearest-rank index instead of a percentile helper.
**All 1,024 cells agree, and `R_space_sampled` agrees at exactly zero absolute
difference.** So the Session-49 matrix is right; only the sentence attached to
it was wrong.

**The structure, re-derived without Codex's code:**

| fact | value |
|---|---|
| strict pairwise dominance relations | **30** |
| `p = 1`'s withholding set | exactly the **16 odd**-target fixtures |
| `p = 2`'s withholding set | exactly the **16 even**-target fixtures |
| every other odd member's signature | exactly `{1, p}` |
| every other even member's signature | exactly `{p}` |
| cross-parity dominance | **none** |
| members sharing a signature | **none** — 32 distinct |

**Withdrawn:** *the family has no dominating member*; *none dominates*.
**Surviving:** 32 of 32 self-hits; no all-fixture member; no no-fixture member;
the split parameter reaches a decision.

## 3. A limit on my own evidence, found by the rebuild

The rebuild's first run failed one check — one I had written asserting that no
null value sits within 0.01 of the threshold. It was my expectation that was
wrong, not the measurement, and what it exposed is worth more than the check
was: **450 of the 1,024 cells sit exactly at `M = 2.0`.** Branch 4's `>` is
strict, so every one of them passes. The 77 withholding cells all sit at 4.0 or
25/9 — the closest is `M + 0.778` — so the dominance structure itself is read
off well-separated values and is safe. But a non-strict comparison would flip
450 cells and produce a different table.

I replaced the invented margin with what is actually measurable: a check that
every withholding decision clears `M` by a wide margin, a check that the 450
ties exist and are all on the passing side, and a printed note that **this
fixture family supports claims about clearly separated values and must not be
used to argue anything near the threshold.** That is a restriction on my own
Session-49 evidence that neither agent had stated.

## 4. The new finding: the resolution diagnostic has an undefined case

Re-reading Draft 34's degenerate-percentile paragraph to write the reply, its
final sentences are false. §19.6 says the half-window ratio `r_c(k)` is
*"handled identically"* to `sigma_hat_c`, that *"a channel with a zero
denominator contributes `+inf`"*, and that *"No undefined ratio enters a
comparison."*

The degenerate test it imports — a channel *literally constant across the
retained core* — is the right test for `R_space_sampled`, which reads the whole
core. It is the wrong test for `r_c(k)`, which reads the two halves. **A
channel can vary across the core, and so pass that test, while being constant
within each half.** Then both half estimates are exactly zero and the ratio is
0/0 — NaN, not `+inf`.

`probe_null_ratio_undefined.py`, **20 checks, 0 failed**, on constructed
channels:

1. **The case exists and is not the documented one.** A mid-window step channel
   has whole-core `sigma_hat_c = 1.4826`, so §19.6's own degenerate test does
   not catch it; both contiguous halves have exactly zero MAD; the ratio is NaN.
2. **The dependence on the split is total, not marginal.** On that one channel
   the ratio is undefined under **exactly the 16 even members** and **exactly
   1.0 — the best value the statistic can take — under all 16 odd ones.**
   Nothing in between occurs. The reason is checked rather than asserted: 6,510
   carries exactly one factor of 2, so a member is even exactly when `6,510/p`
   is odd; an odd block count leaves each half holding a strict majority of one
   step value (smallest observed share 0.500154); and a MAD is exactly zero
   whenever a strict majority share the median value.
3. **The unhandled behaviour is permissive in both regimes.** With 7 undefined
   channels of 72 the NaNs sort above the p90 rank and never reach the
   comparison — disposition `passes`. With 8 of 72 the statistic is itself NaN,
   `NaN > M` is False, branch 4 does not fire — disposition `passes` again. The
   contrast is exact: **8 zero-denominator channels are `unmeasurable` at the
   same count and the same rank.**
4. **"Sort ascending" does not determine an answer with a NaN present.**
   `numpy.sort` sinks NaN to the end, a convention §19.4 does not state, while
   Python's own `sorted` returns different rank-65 values for two permutations
   of the same multiset.

**The documented `+inf` half of that paragraph is sound and I did not touch
it:** 8 such channels of 72 do reach `+inf` and branch 4 does fire; 7 do not.
That is exactly what *"only if enough such channels reach the p90 rank"* says.

**Why this matters for the redesign.** It binds every reading of Part B I can
see, including the one Codex correctly says my sweep does not defeat — pin one
member and disclose it. A pinned *even* member has an undefined diagnostic on a
channel where a pinned *odd* member has a perfect one, so the disclosure has to
disclose that too.

## 5. The decision I made about scope, and why

**I deliberately did not propose a Part B design.** My most repeated error is a
proposal made in the same draft that first constructs its argument, and it has
now cost three drafts in a row: Draft 33's three grounds, two false; Draft 34's
replacement, false. The fix is not another rule — it is to let the evidence
stand on its own and let the next session, or Codex, build on it.

So the chat reply carries two pieces of evidence, both labelled untested where
they live, and **a question rather than a candidate**: is the right first move
to settle what a Part B diagnostic must do when it *cannot be computed* —
undefined as withholding, as an input error, or as a published non-value — and
only then ask which member or members compute it? I think the failure semantics
are the load-bearing half, and I said in the chat that I have been wrong about
which half was load-bearing before and would rather hear Codex's reading than
assume mine.

## 6. Challenges, and two of my own checks that were wrong first

**Two of the checks I wrote this session failed on their first run, and in both
cases the artifact was right and my expectation was wrong.**

- The knife-edge check in §3 above — I asserted a margin I had invented rather
  than measuring the distribution. Replaced with the measurement.
- In the undefined-ratio probe I claimed only `p = 6,510` would be undefined on
  the step channel, and measured five members. The cause was that my check
  computed each half's share of its **first sample** rather than of its
  **majority value**, and the half that begins with one step value can hold a
  majority of the other. The finding was **broader** than I had reasoned — 16
  members, not one — and the corrected check states the mechanism.

That is the second session running in which a check in my own new probe was
wrong before it was right. It is recorded in the workspace README as well as
here.

**One thing I nearly reported as a defect and did not.** My continuity file
paraphrases §19.6 as saying degenerate channels *"can drive the ratio to
`+inf`, which fires branch 3."* Read as a guarantee that would be false, since
fewer than 8 degenerate channels of 72 never reach the p90 rank. **The document
does not say that** — it says *"if enough of them"* and *"only if enough such
channels reach the p90 rank."* The looseness was in my summary of the document,
not in the document. I read the source before writing the claim, which is why
it is in this paragraph rather than in the chat.

## 7. Files created or updated

**Created**

- `agents/Claude/tools/probe_split_family_narrowing.py` — SHA-256
  `37c864618bbe5ddbdfc1d438357fc643461239ca42542d48a99e942904a399d4`, 24
  checks, 0 failed, ~19 s
- `agents/Claude/tools/split_family_narrowing_2026-08-19.txt` — `4375175f…`
- `agents/Claude/tools/split_family_narrowing_2026-08-19.json` — `1b9b3bd1…`
- `agents/Claude/tools/probe_null_ratio_undefined.py` — SHA-256
  `4d21c7578011c0f01b956fbed10a670ff78cbc34c46d6c3c061dbcc8fc63eb66`, 20
  checks, 0 failed, ~2 s
- `agents/Claude/tools/null_ratio_undefined_2026-08-19.txt` — `5ff8e2fa…`
- `agents/Claude/tools/null_ratio_undefined_2026-08-19.json` — `5cc4d438…`
- `agents/Claude/Session Summaries/HumanReport50.md` (this file)

**Updated**

- `chats/Claude-Codex/Part B Resolution Diagnostic Design/Part B Resolution Diagnostic Design - Active.md`
  — appended one message, 6,298 bytes; file now 8,876 bytes
- `README.md` (root, public Live-Run) — one dated log entry, **92 → 93**,
  counted from the file rather than incremented
- `agents/Claude/README.md` — tree entries for both new probes, the withdrawal
  marked on the Session-49 probe's entry, and the tool counts corrected to
  **thirty scripts and fifty recorded outputs**, counted from the directory
  this session. 302 → 316 lines, CRLF throughout
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten

**Not touched:** `Claim Sheet.md`, `Accessible Claim Sheet.md`, the Study Guide,
every file in `Reproducibility Packet/`, `agents/Claude/Tier A Host and
Injection Zone Selection.md` (Draft 34 stays frozen and unapproved), every
Review Card, `references.md` (no new external source was read),
`requirements.txt`, and every closed card's probe.

## 8. Resource and execution note

**Nothing heavy ran, so no heavy-step admission measurement was required.** No
archive read, no network request, no GPU work, no dependency installed, no
background job, and no candidate sample touched. Readings taken during the
session: **08:08 — 14,803 MiB of 32,425 free, VRAM 14,870 of 16,311; 08:34 —
14,412 MiB free, VRAM 14,873.** Both probes are synthetic and local; the
narrowing probe's only input is a Session-49 record written by this workspace,
authenticated by digest before it is read.

**Public heartbeat.** The Live-Run README was updated, because the session both
withdrew a published claim and found a specification defect that changes what
the redesign has to settle first. No phase closed and no artifact was finished.

## 9. Next steps

1. **Codex's reading of the failure-semantics question** is what the Part B
   design should turn on next. It is in the active chat.
2. **The successor Review Card is still not to be written in the session that
   first constructs its argument.** It must name `Supersedes: RC-008` and carry
   the Part A / Part B boundary as its material change, and RC-008 consumed
   clause 5, so a fourth like-for-like §19 repair is forbidden.
3. **Whatever Part B becomes, it has to define the undefined case** — and,
   separately, state the sort convention that makes the nearest-rank rule
   implementable when a non-finite value is present.
4. **Rank 2 drift stays unmeasured.** The pinned order is first-admissible and
   rank 1 has not been rejected, so measuring it now is speculative compute
   against the *Efficiency* standard.
