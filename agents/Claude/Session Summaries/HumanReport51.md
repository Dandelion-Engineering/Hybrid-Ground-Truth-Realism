# Claude Human Report — Session 51

**Date and time:** 2026-08-19 10:25 PDT

**Phase:** Phase 2 — Execution (open-ended Part-B specification design, pre-card)

**Outcome:** Codex answered Session 50's question and named the exact next
object — an exact completion interval for the affected order statistic, with
"their own proof and adversarial fixtures" required before it could be
considered usable. This session built that proof. The bounds are exact,
validated by exhaustion against a brute-force search; the criterion survived
every check I could construct against it; and one half of it would have been
computed wrongly, in the permissive direction, by the obvious method. Four of
my own checks failed on the first run and all four are diagnosed in this
report. No successor Review Card exists, no split member is selected, no §19
draft was edited, no estimator exists, no candidate noise value has been read,
no host is pinned and no sorter has run.

---

## 1. Startup, controlling context and what I read

`.agent-turn` named Claude and `.agent-session.lock` was absent, so I created
the lock and re-read the turn before beginning project work; it still named
Claude.

I read `AgentPrompt.md` in full, all 557 lines of `Project Details/Project
Details.md` (in bounded chunks — the whole file exceeds the tool's single-read
limit), and my own `Summary of Only Necessary Context.md` in full. Both active
chats were read before replying to either: the three-party `Review Method
Change` chat has nothing pending from me and stays active by Randy's standing
request, and `Part B Resolution Diagnostic Design` did require a reply.

**Cross-review.** Codex's `HumanReport50.md` was the newest unreviewed
collaborator work and I read it in full, together with his Session-50 chat
message and his forward correction to it. I found nothing to dispute in either
— his replay of both my Session-50 probes reports byte-identical records, and
the pre-write digest I computed for the chat transcript this session
(`a9bfa198…`, 229 lines) matches the post-write digest recorded in his report
exactly, which is an independent confirmation that nothing has been altered in
that file between his session and mine. His forward correction (an interval
lying wholly above `M` is also withheld) is correct and I built a fixture for
it rather than taking it on trust; it passes.

**No count-based progress report is due.** Mine are at sessions 8, 16, 24, 32,
40 and 48; the next is 56. No phase transition occurred and no Claim Sheet
amendment was approved, so neither event trigger fired either.

## 2. What the session was for

Session 50 established a defect in frozen Draft 34: the half-window ratio
`r_c(k)` has a 0/0 case that §19.6's degenerate test does not catch, whose
occurrence is decided entirely by the split rule nobody has chosen, and whose
unhandled behaviour reads as `passes` in both regimes. I deliberately proposed
no repair and asked Codex one question instead: should we settle what the
diagnostic must do when it cannot be computed, before asking which split rule
computes it?

He agreed, and separated the word *undefined* into three layers — input
validity, per-channel value, band decision — rather than assigning it one
disposition. His conclusion was that the object to test next is a **completion
interval**: treat every undefined channel ratio as able to occupy any point in
`[0, +inf]`, compute the exact lower and upper attainable nearest-rank
`rho(k)`, propagate through the maximum over windows, and let branch 4 stand
down only when the upper bound is at or below `M`. He was explicit that this
is "a design criterion, not yet a successor candidate," and that the bounds
"need their own proof and adversarial fixtures before we decide whether this
construction is usable."

**That is what this session did, and doing it rather than proposing something
of my own is deliberate.** My most repeated error across this project is a
proposal made in the same draft that first constructs its argument — it has
cost four drafts. Session 50 was the first session that acted on the fix
instead of restating it. This session continues that: Codex constructed the
criterion, I checked it, and I have not proposed a Part B design.

## 3. The instrument

`agents/Claude/tools/probe_completion_bounds.py`, **45 checks, 0 failed, about
0.4 seconds**, SHA-256
`2c1c78beaf7345edf91e8393df70b8d049bfa0b462684c3463053b5431afddec`. It requires
`--out`, takes `--records` and `--fixtures`. Records:
`agents/Claude/tools/completion_bounds_2026-08-19.txt`
(`d14c1471bca1623f7fe6f5280cec225bd5e66ec7f54222178e1caa2495c62b66`) and
`…json` (`bb9465f0657e51b6c9c87d80d8d3b79265e744aa2496ee8dde9ba2d886f8870f`).
Two runs to different paths produced byte-identical records. `--help` renders
11 lines; the script, both records and the help output contain zero non-ASCII
bytes and no CR bytes.

**The design of the proof.** Two independent implementations of the same
quantity, required to agree exactly:

1. a fast **three-level enumeration** — some unknowns at 0, some tied to one
   finite value, the rest at `+inf` — which is what a real implementation
   would use; and
2. a **full exhaustive search** over a refined grid holding every finite value,
   every midpoint between consecutive finite values, one value below the
   smallest, one above the largest, 0 and `+inf`, over every tuple of unknowns.

Agreement on both endpoints on all 36 small fixtures, across six deliberately
different value shapes including fixtures carrying exact zeros and exact
infinities, is the check. That is the same discipline Session 50 learned the
hard way: a byte-for-byte replay proves determinism, not correctness, so a
result that matters gets rebuilt along a deliberately different path.

## 4. What the proof found

**The bounds are exact.** 36 of 36 fixtures, both endpoints, zero mismatches.

**The two endpoints do not have the same shape, and the obvious method is
wrong for one of them.** The maximum is attained at a *vertex* — every unknown
at 0 or at `+inf` — and that is checked, 36 of 36. The minimum is **not**: on
**24 of 36 fixtures** an interior placement strictly beats every vertex. The
mechanism is one sentence — an unknown placed between the p10 and p90 ranks
lowers the value at the p90 rank by one finite position while leaving the p10
rank untouched, where 0 lowers both and `+inf` lowers neither. The worked case
in the report is `n = 10` with finite values `1..9`: both vertices give 9.0, an
interior placement gives 8.0. The closed form for the minimum,
`f[max(i90 - u, i10)] / f[i10]`, matches the exhaustive minimum on all 30
fixtures where it applies.

**This is the finding with the most reach, because of its direction.** Anyone
implementing the interval from intuition would search the vertices, get a
minimum that is too high, and the branch-3 label reads the *lower* endpoint —
a too-high minimum makes `resolution-limited` reachable where it should not
be, and makes the honest third outcome unreachable. It is a permissive error
in a label, found before anything was written rather than after.

**The count threshold recovers a number the specification already has.** At
n = 72 the nearest-rank indices are 8 and 65, and `i10 = 8` coincides with
`n - i90 + 1 = 8`, so one count governs both ends. **Eight or more undefined
channels make the upper bound unbounded whatever the finite values are** —
which is exactly the count at which §19.6's documented zero-denominator case
already reaches `+inf` and fires branch 4. Seven or fewer leave a finite bound
that the finite values decide, and I built a fixture where seven undefined
channels are **proved** decision-irrelevant (bound [1.0497, 1.0570], branch 4
stands down). The rule does not invent a threshold and it is not a blanket
rejection of any candidate with one bad contact.

**It is a conservative extension, checked three ways.** With no undefined
channel the two endpoints collapse to the single value (24 of 24 fixtures),
branch 4 fires exactly when Draft 34 says it fires, and the third label is
unreachable across 72 spatial values. Nothing in Part A moves and nothing in
the defined half of Part B moves.

**The direction is one-way, checked rather than argued.** Assigning 0, 1,
`+inf` or the finite median to every undefined channel always lands inside the
enclosure, as do 2,400 randomly drawn mixed completions, and **no completion
withholds while the bounded rule stands down**. That is the same asymmetry
already settled for `Q95_null` and `R_null_sampled`: it can convert a would-be
pass into `unmeasurable` and can change how a failure reads, and never the
reverse.

**It bites where the current behaviour is permissive, and the mechanism is
worth naming.** A 72-channel fixture with 65 finite ratios (seven at 1.0,
fifty-eight at 3.0) and seven undefined passes today — NumPy's NaN placement
gives 1.0 — and returns `unmeasurable` under the bound, whose upper endpoint
is 3.0. **NumPy's NaN ordering IS the all-at-`+inf` vertex**, so the divergence
is in the comparison and not in the ordering: the library was reporting one
completion of many as though it were the value.

**The maximum over windows propagates exactly**, both endpoints, against an
exhaustive two-window search on 8 fixtures, because placements are independent
across windows.

## 5. Three costs and one refuted expectation, all recorded

1. **The third label is a change to published vocabulary.** Codex's
   `resolved` / `resolution-limited` / otherwise-`unresolved` rule is
   exhaustive and mutually exclusive over a swept spatial value and all three
   are reachable — but §19.6 publishes exactly two labels. A successor card
   must carry that explicitly.
2. **Interior attainment is left open and shown not to matter.** Both
   endpoints are attained by exhibited completions. Whether every value
   between them is reachable I could not settle — a uniform sweep cannot
   separate a real gap from grid resolution — and it is not load-bearing,
   because `stands_down` reads the upper endpoint alone and the label reads
   the two endpoints and the undefined flag. Worth knowing that the enclosure
   can collapse to a point: one undefined channel of 11 can leave the ratio
   pinned exactly.
3. **A second-order undefined case exists one level up.** If both selected
   order statistics are 0 the band ratio is itself 0/0 with no channel
   undefined at all. At n = 72 that needs 65 channels at exactly zero, so it
   is remote, and the bound already treats it as unbounded rather than
   passing. Recorded so a successor specification does not meet it first in an
   implementation.

**And one expected defect that measurement refuted.** I expected §19.4's own
`ceil(0.10 n)` and `ceil(0.90 n)`, evaluated in binary floating point, to
disagree with exact integer arithmetic at some band size, and wrote the check
to catch it. **It agrees at every n from 1 to 200,000.** The claim is
withdrawn, the check stays in as a negative result, and the docstring that
asserted the hazard was corrected.

## 6. Challenges — four of my own checks failed on the first run

The first run returned **39 checks, 4 failed**. Each is diagnosed here because
the project's rule is to say which resolution was taken.

- **The float-rank hazard (§3).** My *expectation* was wrong, not my test. I
  had asserted a disagreement existed; measurement over 1..400 found none, and
  a wider sweep to 200,000 found none either. **Resolution: withdraw the
  claim** and keep the check inverted, as a recorded negative result. This is
  the same error the summary logs as "do not assert an invented margin —
  measure the distribution," and it is the second session running that it has
  been caught by my own check rather than by a reviewer.
- **Two checks in §7 that compared against the wrong band size.** Both
  computed a bound at `n = 72 - 7 = 65` while claiming to describe the 72-
  channel fixture, which silently changes the nearest ranks from (8, 65) to
  (7, 59). **The tests were broken, the findings were sound.** Resolution:
  added a `frozen_disposition` helper that reproduces Draft 34's four branches
  against a *scalar* `R_null_sampled` — including the NaN comparison — and
  compared against the correct all-at-`+inf` vertex at n = 72.
- **The attainability check (§12).** The check expression was malformed and
  the claim behind it — that the enclosure has interior gaps — was one I could
  not establish. A dense sweep produced apparent gaps that turned out to be
  grid artifacts of a uniform x-grid under a compressive map. **Resolution:
  drop the claim entirely** and replace it with what is checkable: both
  endpoints are attained by exhibited witnesses, the enclosure can collapse to
  a point, and the open question is stated as open.

**Two further self-corrections went in without being failures.** A check whose
condition was the literal `True` was replaced by one that can fail (the u = 0
entry of the trajectory must equal the pool's plain ratio); a check that
duplicated its predecessor's condition — and so could not fail independently —
was replaced by 2,400 sampled completions and a one-way violation count. Both
are instances of the standing lesson that a check that cannot fail is not a
check.

## 7. Decisions I made

- **Check Codex's criterion rather than propose an alternative.** He asked for
  a proof; a competing design would have been the error I have made four
  times.
- **Prove by exhaustion against a second implementation, not by argument.** I
  had an analytical argument for the vertex claim. It was right for the
  maximum and wrong for the minimum, and only the exhaustion revealed that.
- **State the honest reach of the proof rather than overstate it.** The
  exhaustive validation is at n = 10..12 and u = 1..3. At n = 72 the
  enumeration rests on that generalising, plus 2,400 samples that cannot prove
  a bound. I said so in the chat and named the check that would close the gap:
  a second independent derivation at n = 72, not more samples.
- **Add a public log entry.** The Live-Run heartbeat was checked and this
  cleared the bar the existing log sets — an exactness result, a permissive-
  direction implementation trap, and a withdrawn expectation. Banner date
  already read 2026-08-19 and was left alone.
- **Do not measure rank 2's drift.** Unchanged reasoning: the pinned order is
  first-admissible, rank 1 has not been rejected, and measuring rank 2 now is
  speculative compute against the *Efficiency* standard.
- **Ask a scoping question rather than answer it.** The semantics touch two
  specification surfaces — §19.6's label vocabulary and §19.7's publication
  set — and which of them a successor card's Part B covers is exactly the kind
  of scoping call that has cost a round before.

## 8. Reasoning paths explored and not taken

I considered deriving closed forms for both endpoints and shipping those alone.
Rejected: the derivation is the thing under test, and a closed form validated
only against its own derivation tests that two halves of one argument agree.
The closed form for the minimum is in the probe, but it is checked *against*
the exhaustion rather than trusted.

I considered demonstrating that the attainable set has gaps, which would have
been a sharper cost to report. The evidence did not support it and the
apparent gaps were grid artifacts; reporting it would have been a finding
manufactured from sampling resolution.

I considered whether the criterion could be *refuted* rather than confirmed —
specifically whether it could ever be less withholding than the current
`+inf` handling. It cannot: zero-denominator channels are defined, so the
completion machinery does not touch them, and for undefined channels every
scalar convention is itself a completion inside the enclosure.

## 9. Insights worth carrying

1. **An extreme over a box is not always at a vertex, and which endpoint fails
   depends on which direction each coordinate helps.** The maximum wants each
   unknown pushed to one extreme; the minimum wants some of them in the
   middle, because lowering the numerator's rank is free while lowering the
   denominator's is not.
2. **When a proposed rule reproduces a threshold the existing specification
   already has, that is evidence about the rule.** Eight of 72 was not chosen;
   it fell out of `i10 = n - i90 + 1` at n = 72.
3. **A library's default ordering can be exactly one completion of many.**
   NumPy was not sorting wrongly; it was reporting a single possibility as the
   answer. That reframes Session 50's finding: the defect is not NaN placement,
   it is treating a non-value as a value.
4. **A negative result from a check you wrote expecting a failure is worth
   keeping in the suite.** The float-rank check now records that the stated
   form was tested rather than trusted.

## 10. Files created or updated

**Created**

- `agents/Claude/tools/probe_completion_bounds.py`
- `agents/Claude/tools/completion_bounds_2026-08-19.txt`
- `agents/Claude/tools/completion_bounds_2026-08-19.json`
- `agents/Claude/Session Summaries/HumanReport51.md` (this file)

**Updated**

- `chats/Claude-Codex/Part B Resolution Diagnostic Design/Part B Resolution Diagnostic Design - Active.md` — one appended Claude message, EOF-verified
- `README.md` (root, public Live-Run) — one dated log entry, 93 → 94
- `agents/Claude/README.md` — Session-51 navigation
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten at closeout

**Not touched:** `Claim Sheet.md`, `Accessible Claim Sheet.md`, the Study
Guide, every Review Card, `agents/Claude/Tier A Host and Injection Zone
Selection.md` (still Draft 34, frozen and unapproved), every file in
`Reproducibility Packet/`, `requirements.txt`, `references.md` (no new external
source was read), and all nine RC-007/RC-008 scripts.

## 11. Resource and execution note

No heavy step ran. The work was local text and one synthetic probe of about
0.4 seconds. Readings taken at the moment, not inherited: **10:11 PDT — 13,307
MiB of 32,425 system RAM free, VRAM 14,880 of 16,311 free; 10:23 PDT — 13,332
MiB free, VRAM 14,887.** No archive read, no network request, no candidate
sample, no dependency installed, no GPU work, no background job, and no
temporary directory left behind.

## 12. Next steps

1. **Read Codex's reply before doing anything else in §19.** The ball is with
   him: I asked whether a successor card's Part B covers both §19.6's label
   vocabulary and §19.7's publication set, or whether the publication change
   belongs with Part A's §19.7 entry.
2. **The member comparison Codex named as step three is now unblocked in
   principle** — the semantics are proved — but it is his ordering and I have
   not started it.
3. **Do not write the successor card in the same session that first
   constructs its argument.** The three Session 49–51 probes are the evidence;
   consume them rather than re-deriving them.
4. **If the exactness proof needs to hold at n = 72 on its own terms**, the
   check to write is a second independent derivation at that size, not more
   sampling.
5. **Rank 2 stays unmeasured**, rank 1 stays unrejected, no host is pinned, and
   no downstream execution is authorized.
