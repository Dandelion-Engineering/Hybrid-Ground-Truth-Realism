# Progress Report — Codex Session 40

**Date and time:** 2026-08-17 06:13 PDT

**Project phase:** Phase 2 — Execution

**Public state:** In Progress; no host or scientific result exists

## The short version

The project now has an approved way to handle the sparse missing spike-depth
values that stopped its first real candidate read. It does not guess those
values, silently discard them, or introduce a percentage chosen after seeing
the data. Instead, it asks what **every possible value** could have done to both
numbers in the predeclared drift gate. If all possibilities support one answer,
the recording can pass or fail; if they do not, it is reported unmeasurable and
keeps its place in the candidate order.

That safety layer passed exact-state review today. This is an implementation
milestone, not a research result: no candidate has a drift value and no host has
been selected.

## What changed since Session 32

My Session-32 report ended with an approved bounded reader and a planned first
candidate measurement. The next eight sessions exposed two problems that
synthetic review alone had not represented.

First, the reader required the raw and processed halves of a recording to name
the same conversion-software version. A bounded census of 71 sessions in
[DANDI 000409](https://dandiarchive.org/dandiset/000409/draft) showed that this
rule admits **none** of them: every raw half and processed half were converted by
different versions. Worse, the version pair could not identify the timing defect
the rule stood in for. The files expose that property directly through the NWB
`timestamps_reference_time` field, which defines time zero for all timestamps
([NWB format](https://nwb-schema.readthedocs.io/en/stable/format.html)). Those
declared instants agree on 63 of 71 sessions and differ by exactly one hour on
eight. A new review card replaced the empty proxy with bounded comparison of the
actual declared instants while retaining affirmative conversion authentication.

Second, the first real rank-1 read reached 3,160,311 spikes and found 231 whose
times were usable but whose waveform-derived depths were missing. Rank 2 showed
the same pattern. The old rule required every depth to be finite, so both
candidates paused before a drift verdict.

## Why “drop 231 and report it” was not enough

The missing fraction is tiny — roughly seven values in one hundred thousand —
and removing them leaves every predeclared sample-count floor intact. That still
does not prove safety. The drift estimator uses medians. A missing value near a
widely spaced middle pair can move a median far more than one near a dense
cluster, so the fraction missing does not bound its influence.

Generated examples made the problem concrete. A recording can pass every sample
floor and both drift-gate numbers on the finite values while possible values for
the missing entries move the answer from inside the 20-micrometre tolerance to
far outside it. The recovery therefore computes the full attainable interval
for each affected neuron and minute, propagates those intervals through the
same across-neuron summary and time-window scan the approved gate uses, and does
the same for the gate's permutation-based noise floor.

The harder noise-floor half turned out to be possible without assumptions. A
spike whose depth is missing still has a known time and still occupies one fixed
position in the completed vector. The deterministic shuffle therefore has the
same length, seed, and source-to-destination map before any missing value is
chosen. The unknown values can be followed through that fixed map and bounded
wherever they land.

## What review found

The interval mathematics survived independent stress: 120 generated fixtures,
1,080 finite completions, and zero values outside the claimed observation or
noise-floor bounds. The full wired state still came back from Round 1 for two
implementation defects:

- On the exact fixture where the new layer correctly paused a passing point
  gate, the written report and JSON were right but the command's **last console
  line still said `passed=True`**.
- The reader now retains one boolean marker per spike saying whether its depth
  is missing, but its pre-read memory bound had not added those markers —
  3,160,311 uncounted bytes at rank-1 size.

Both repairs passed the Round-2 delta review. The reconciled decision is now the
last printed line, with the point gate explicitly labelled as diagnostic. The
mask bytes enter the resident and peak formulas, the old mask-omitting ceiling
is refused, and the exact corrected peak is admitted. The changed owner suite
passed 543 checks; a new harness successfully undid four whole or partial
repairs and required the suite to fail; my separate probe passed 10 boundary
checks.

## What was unexpected

The most useful testing failure was a test that passed whether the repair was
present or absent. Its first version set the memory ceiling to “the calculated
peak minus the masks.” When the mask term was deliberately removed, the
calculated peak moved down too, so the test still refused the read and remained
green. It became evidence only after its boundary was derived from the fixture's
own spike count, which the formula under test could not move.

This is the same general lesson as the empty converter-version proxy: a check
can be internally consistent and still say nothing about the external property
it is supposed to establish. We now test not only that a mechanism exists, but
that its pass and fail boundaries can actually move independently of that
mechanism's own output.

## What is working

- RC-004's direct reference-instant pair check is approved.
- RC-005's complete missing-depth reader, bound, command wiring, specification,
  and tests are approved with documented follow-ups.
- A missing depth cannot silently change the candidate decision: it is counted
  per unit, per minute, and in total, and both gate numbers carry bounds over
  every completion.
- An infinity remains a fatal input error rather than being relabelled as
  uncertainty.
- Review stayed bounded: one full ledger, one repair response, one delta pass,
  and explicit same-state approval without a Convergence Decision.

## What is not working yet

There is still no drift measurement, selected host, target manifest, donor
assignment, generated hybrid recording, or sorter result. Four later-ranked
candidates also remain separately paused because their raw and processed files
declare different timing origins.

Two record-quality follow-ups from RC-005 remain visible: the command makes
avoidable finite-only array copies outside its currently declared read-only
memory ceiling, and its printed resident-array label should name the maximum
stored-width slice already included in the safe numeric total. These do not
weaken the approved decision or admission boundary.

No new director decision is needed for the immediate next step. The older
Phase-1 contract-review request remains open and nonblocking.

## What happens next

The next separate action is the rank-1 drift measurement. Immediately before
it begins, the agent must measure current free RAM, compare it with the command's
mask-inclusive peak, and refuse to start if it does not fit. If the command
produces a report, that report is evaluated under the strict gate and the
command becomes the packet's next numbered runbook step. Host selection, donor
matching, generation, and sorter execution remain separate later approvals.

## Verification artifact

There is no new director verification artifact this period. The final
`verify_realism.py` artifact still waits on a scientific result, and no
scientific result exists.
