# Claude Human Report — Session 35

**Date and time:** 2026-08-16 07:41 PDT

**Phase:** Phase 2 — Execution

**Outcome:** RC-004's Round-2 repair is delivered and handed back to Codex. Both
of his Round-1 blocking findings are accepted in full, neither is disputed, and
his own probe was reproduced before anything was edited and re-run after. The
acceptance suite went 436 → 472 checks and the mutation harness 30 → 32, both
green. **The candidate is still not approved and the rank-1 measurement is still
blocked.**

---

## What this session did

Session 34 handed Codex a candidate that replaced a broken pair rule. He returned
Round 1 as **`Revisions Required`** with two blocking findings, each carrying an
executable counterexample in `agents/Codex/tools/probe_rc004_round1.py`. This
session repaired both.

**Before editing anything I ran his probe unmodified**, at the SHA-256 he
published. It exited 0, having reproduced both defects. That is the habit this
project has kept since Session 22 and it is worth keeping: a finding you have
watched fire is a different object from a finding you have read.

### RC-004-F1 — a value that is not a timestamp was reaching a verdict

`datetime.fromisoformat` is deliberately more permissive than ISO-8601 from
the pinned interpreter, CPython 3.12.10: it accepts **any single character**
where ISO-8601 puts the `T`. That is measured here, not read off a changelog.
So `2021-05-10Q14:33:49.023776-04:00` parsed, carried a timezone offset, agreed
with the identical value on the other half of the recording, and produced a drift
verdict with a report and a record. NWB specifies this field as an ISO-8601
timestamp; a value that is not one is a malformed input, and two files agreeing
about a malformed value is not evidence that they share a clock.

**The repair is a lexical gate before the parser.** The whole stripped value must
match an ISO-8601 *extended* date and time — `T` separator, `hh:mm` with optional
seconds and optional fraction, optional `Z` or `±hh[:mm]` offset — and the parser
then validates the values inside that shape, so month 13, hour 25 and 31 February
are still refused by `fromisoformat` rather than by the expression.

**The judgement worth recording is what I deliberately did *not* do.** The
obvious belt-and-braces move is to require the UTC offset in the grammar as well
as on the parsed value. It would have been harmless-looking and it would have
quietly destroyed one of the mutations: with two independent enforcers of one
property, **no single-line revert can defeat it**, so mutation F1L — which
removes the timezone requirement — would have gone from CAUGHT to MISSED with
nothing in the harness saying so. That is the Session-31 failure mode ("a repair
can silently remove the coverage a mutation depends on") arriving in advance
rather than in arrears. The grammar bounds the shape; `utcoffset` requires the
offset; one enforcer each. F1L is still caught.

**And the mirror, which is the direction this whole card exists in.** RC-004 was
opened because a rule nobody had measured against the real population admitted
**none** of it. A tightening is exactly the kind of change that can do that
again. So the new grammar is measured rather than argued about:
`case_the_grammar_admits_every_measured_reference_time` runs all **79 distinct
values of the 142 assets** the 71-session census read — frozen into the suite
from the two recorded census JSON files — and requires every one to parse to a
timezone-aware instant. It also pins the four lexical shapes and their counts, so
a later edit to that list reads as a change to the population rather than as a
different set of the same size. I verified separately that the frozen tuple is
exactly the set those two JSON files yield.

### RC-004-F2 — the raw clock read was outside the caller's declared ceiling

The command's `--max-mib` ceiling was passed only to the processed asset's read.
The raw asset's provenance read — which fetches half of the pair condition —
happened first and outside it. Under a synthetic one-byte ceiling, Codex measured
**23,920 distinct raw bytes moving and the raw clock being printed** before the
processed side refused anything.

`read_provenance` now takes the ceiling and holds it open around the file open
**and** the provenance read, exactly as the processed read does, and a refusal
there surfaces as `[fatal] input error reading <raw path>: …` rather than as a
traceback. Both narratives and the `--max-mib` help text were corrected; the
docstring no longer says the read happens before any ceiling exists.

**I described this as a tightening rather than as a free repair.** Unlike the
processed read, there is no plan behind the raw provenance read, so the argument
that licensed the ceiling there — that it can only refuse reads the later plan
check would have refused anyway — does not carry. A declared ceiling smaller than
the cost of opening the raw asset now stops a run that used to reach the
processed read. That is the class a declared ceiling exists to refuse; it
surfaces as an input error naming the ceiling; and at the 1024 MiB default it
cannot fire. On the real rank-1 candidate that read spent 22,104 request bytes
and 262,144 transfer bytes.

**One consequence I declared to Codex rather than letting him find it.** The
whole-command ceiling case now stops on the **raw** asset, because that is the
read the ceiling meets first. Every one of its old assertions still holds and
three were added — the status names the raw asset, zero distinct bytes move on
*either* file, and the transcript is captured and required not to contain the raw
clock line, which is his "not read or printed" asserted directly. But **no
whole-command ceiling can admit the raw asset's ten kilobytes and still refuse
the processed asset's first eight bytes**, so RC-003-F3's processed-side
before-the-first-fetch property moved to a direct-API case that asserts the same
zero distinct bytes and the same refusing scope. The property did not weaken;
only the layer it is asserted at moved, and the mutation that removes the
ceiling-hold is still caught at both layers.

---

## Challenges, and how they were handled

**1. A repair that would have blinded a sabotage.** Described above. The general
form is worth carrying: *before adding a second enforcer of a property, ask what
the existing mutation for that property reverts.* Redundancy in the code and
sensitivity in the harness pull in opposite directions, and the harness is the
only thing that tells you the code still depends on what it claims to.

**2. A whole-command test whose meaning moved under it.** Bringing the raw read
inside the ceiling changed which asset a one-byte ceiling refuses first. Left
alone the case would still have gone green, for a reason it was not written to
check — the exact "passes for the wrong reason" failure this project logged at
Sessions 32 and 34. I could not restore the old meaning at the command level
(the arithmetic forbids it), so the property moved down a layer to where it is
actually a property, and the reasoning is written into both cases' docstrings.

**3. Two documentation regressions my own repair created.** `_ceiling_budget`'s
docstring carried a universal "it cannot make anything infeasible" claim that was
true while `read_band_units` was its only caller and became too broad the moment
`read_provenance` became its second; and a comment cited RC-004-**F1** where it
meant **F2**. Neither changes a numerical branch, and both are exactly the class
the review method calls *a regression introduced by the response*. I found them
by grepping my own changed files for every sentence containing "ceiling" rather
than by rereading the diff.

**4. Evidence that has to match the bytes you publish.** Fixing those two
docstrings after the mutation harness had already run would have left the card's
digests describing a state the harness never saw. I re-ran the whole harness on
the final state rather than reasoning that comments cannot matter. Both runs are
recorded; the published digests are from the second.

### A fifth challenge, found after the handoff was already posted

Two sentences in my own new comment block were stated more confidently than they
were checked: one named the Python release that made `fromisoformat` permissive,
where the measured fact is about the interpreter this project pins; the other
asserted that ISO-8601 forbids a basic-format offset beside an extended date. I
went to check the second rather than leave it, and the source states the rule
about the two halves of a combined representation without mentioning the offset
at all. Extending it there is a reading, and the comment now says so.

**The cost of finding it late is the part worth recording.** The Round-2 handoff
had already been posted with a digest, so correcting two comments meant the
published digest was stale. Rather than leave it, or revert a correction to
protect a hash, I proved the change was comment-only — reconstructing the
published bytes, confirming they hash to the published digest, and comparing
docstring-stripped syntax trees — re-ran the whole mutation harness on the
corrected bytes, and appended a correction to the review chat naming the new
digest. **An append-only transcript makes a stale number a message, not an
edit**, which is the right shape: Codex sees both the number I gave him and why
it moved.

The general form: **a claim about an external standard is a citation, not a
comment.** If it is worth writing in the code, it is worth an entry in
`references.md` with its boundary stated — and writing that entry is what
exposed that the clause I was leaning on does not say what I said it said.


---

## Evidence, as run

| Check | Result |
|---|---|
| Acceptance suite | **472 checks, 0 failed**, 82 cases (was 436 / 80) |
| Mutation harness | **32 of 32 caught**, control green at 472 checks / 0 failed / 16.5 s, ~9 minutes |
| Codex's Round-1 probe, unmodified | no longer reproduces either counterexample; `raw_distinct_bytes` 23,920 → 0 |
| `verify_rc003_round1_repairs.py` | exits 0, untouched |
| `verify_rc003_round2_repairs.py` | exits 1 with exactly the two failures declared at Round 1, no new ones |
| `mutation_test_runbook_checker.py` | 18 of 18 |
| `check_runbook_consistency.py` | 10 steps agree, `measure_host_drift.py` still `PENDING` |
| `--help` rendered and scanned | ASCII-clean, both new help paragraphs render |

**Machine state, measured rather than inherited.** 07:06 PDT: 13,404 MB free
physical of 32,425; 30,683 MB committed of a 130,415 MB limit. 07:25 PDT, with
the harness running: 12,835 MB free, 32,931 MB committed. **Nothing this session
read the archive or the network**; the largest thing that ran was the mutation
harness, thirty-two sequential copies of a small synthetic tree, run twice.

---

## Decisions I made

1. **Accept both findings without dispute.** Both were reproduced from Codex's
   own probe before any edit.
2. **Keep the offset requirement outside the new grammar**, so mutation F1L
   still has something to remove.
3. **Widen the grammar slightly beyond the measured population** — omitted
   seconds, any fraction length, `Z`, whole-hour offsets — because those are
   legitimate ISO-8601 extended forms a later converter could emit, and
   refusing one would be the pessimistic mirror of the defect this card
   repairs. The basic-format offset `+hhmm` is *not* admitted, because ISO-8601
   requires the date and time halves of one representation to use the same
   format, basic or extended. Applying that to the *offset* is a reading
   rather than a quoted clause and the code says so; no measured asset
   spells its offset that way either.
4. **Freeze the 142-asset census into the acceptance suite** rather than have it
   read the census JSON files, so the suite stays self-contained and no check
   can silently not run.
5. **Move RC-003-F3's processed-side property to a direct-API case** rather than
   leave a command-level case passing for a new reason.
6. **Describe F2's repair as a tightening**, including the class of runs it now
   refuses, rather than claim it costs nothing.
7. **No root README entry this session.** The heartbeat check ran: no artifact
   finished, no phase closed, and a Round-2 repair of two review findings is the
   expected follow-through rather than a noteworthy event. Four consecutive
   sessions already have entries and the log is lean by design.

---

## Files created or updated

| Path | What changed |
|---|---|
| `Reproducibility Packet/scripts/utils/archive_units.py` | `REFERENCE_TIME_FORM` and its text; `reference_instant` gates the shape before parsing; `read_provenance` takes and holds the caller's ceiling; six docstring/comment corrections. Final digest `9ef16f58…` |
| `agents/Claude/references.md` | one entry: ISO 8601's basic/extended rule, marked a secondary source, with the boundary that the quoted clause is about the date and time halves and not the offset |
| `Reproducibility Packet/scripts/measure_host_drift.py` | the ceiling is passed to the raw provenance read and its refusal named as an input error; module narrative and `--max-mib` help corrected |
| `agents/Claude/tools/test_measure_host_drift.py` | `MEASURED_REFERENCE_TIMES` (79 values); `run_case(capture=)`; two new cases, one new direct-API case, three assertions added to the ceiling case |
| `agents/Claude/tools/mutate_rc002_repairs.py` | mutations **F1p** and **F1q**, and a paragraph saying what each isolates |
| `Review Cards/RC-004 Session Reference Time Pair Check.md` | Round-2 response, updated digests, updated acceptance tests, Round-2 log row, one new tracked follow-up |
| `Review Cards/README.md` | RC-004's index row moved to Round 2 |
| `chats/Claude-Codex/Session Reference Time Pair Check Review/…Active.md` | the Round-2 handoff appended |
| `agents/Claude/README.md` | the Session-30 ceiling-scope sentence corrected, three status pointers moved to Round 2 |
| `agents/Claude/Summary of Only Necessary Context.md` | rewritten for Session 36 |
| `agents/Claude/Session Summaries/HumanReport35.md` | this file |

**Not touched:** every approved state — the selection document, the estimator and
its harness, the Claim Sheet, the Accessible Claim Sheet — and
`verify_rc003_round2_repairs.py`, which I did not edit at all this round.

---

## Next steps

1. **Codex verifies Round 2, delta-only.** This is the second of the three
   round-trips the method allows.
2. **If it closes `Approved`, run rank 1** — CSHL047 Probe01, session
   `b52182e7…`, `--plan-only` first, then measure free RAM against
   `peak_resident_bytes` before reading. That is the first drift number this
   project will have.
3. **If it returns blockers**, Round 3 is the last round; a non-approval there
   triggers the Convergence Decision.
4. Tracked follow-ups on the card are unchanged, plus the new fourth one
   recording the stale workspace-README sentence.

**Boundary, unchanged.** No host is pinned. No candidate has a drift, noise or
effective-SNR value. No donor is selected, no generator or sorter has run, and no
scientific result exists.
