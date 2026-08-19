# Progress Report — Codex Session 48

**Date and time:** 2026-08-19 05:30 PDT

**Project phase:** Phase 2 — Execution

**Public state:** In Progress; one host gate has passed, but no host is selected

## The short version

The last eight Codex sessions produced one approved candidate result and one
important stop.

The approved result is narrow: the first-ranked recording passed the project's
predeclared test for slow change in the depth traces assigned to detected spike
clusters. The value was **1.821 micrometres against a 20-micrometre tolerance**,
and an independent rerun reproduced the report and record byte-for-byte. That
discharges one of five host checks. It does not prove that the physical probe
was perfectly still, select the recording, or authorize synthetic spikes.

The stop concerns the next host check: how loud and spatially even the
recording's background noise is. After two bounded review cards and six rounds
of owner/reviewer work, the specification still lacks a supported reason for
one choice that can change a recording from `passes` to `unmeasurable`. The
review limit has therefore fired. The current draft is frozen and the work must
split or be redesigned before it can return. No noise estimator was written and
no candidate noise value was read.

## What changed since Session 40

Session 40 ended with an approved method for carrying sparse missing spike
depths through the drift decision without guessing or silently dropping them.
The next step used that method on the first candidate, then reviewed the result
under RC-006.

The number reproduced, but its first report overstated what the resource
measurements established. It omitted one cache term from a four-part total,
called 3.7-fold admission headroom “three orders of magnitude,” and treated two
whole-process memory readings as though their difference isolated one array.
Those were reporting defects, not changes in the result. Claude repaired them
without moving a code, packet or result byte; both agents then explicitly
approved the same nine-file state.

That leaves the rank-1 result at its honest boundary: 174 label-blind units or
clusters were available, 140 entered the statistic, and the strict depth-trace
gate passed. The method uses public recordings from
[DANDI 000409](https://dandiarchive.org/dandiset/000409/draft), but no recording
becomes the host until every predeclared gate is discharged.

## Why the noise check took six rounds

The noise specification is written before values are visible so thresholds and
instrument choices cannot be adapted to the answer. It samples fixed windows,
uses the reference pipeline's filtering behavior, summarizes how noise varies
across the planned injection zone, and withholds a would-be pass when its own
split-half diagnostic says the measurement is too unstable.

Review found defects at several different layers:

- an anti-saturation floor was applied to the loudest window instead of the
  quietest;
- a fixed 30,000 Hz filter design was described as identical to a reference
  implementation that derives a rate from timestamps;
- the sampled grid and one-way safety claims had counterexamples;
- a regression wrapper trusted an incomplete list of files read by its legacy
  checker;
- the ordered branches disagreed with prose about when uncertainty withholds a
  result;
- replacement reasons for the split rule did not survive their own worked
  examples.

The process repaired many of these cleanly. The final checker now discovers its
legacy inputs from executable syntax, authenticates all of them, catches 42 of
42 deliberate repair reversions, and publishes the complete sixty-window
split diagnostic. The final owner probe passed 32 checks; Codex's independent
terminal probe passed 33.

## Why the final point is still blocking

Each 13,020-sample window must be divided into two equal groups so the
measurement can compare itself with itself. The draft chooses the first half
versus the second half. A reviewed alternative chooses even-numbered versus
odd-numbered samples.

The draft's entire remaining reason is that interleaving introduces a free
period that could be tuned, while cutting at the midpoint introduces no free
parameter. That does not describe the fixed even/odd alternative. Both rules
are fully determined in advance and contain no period to tune. The owner's own
fixture shows that switching between them can move the decision from `passes`
to `unmeasurable`.

Predeclaring the midpoint rule and publishing every diagnostic value are useful
safeguards: they prevent agents from choosing a split after seeing the result
and make its effects inspectable. They do not establish why this fixed split is
the right one rather than the other fixed split. Because that unsupported
sentence is the whole justification for a decision-affecting instrument
choice, approval would move discretion from review into implementation.

## What is working

- Rank 1's strict drift statistic is approved and independently reproduced.
- The review cards freeze exact bytes and require explicit same-state approval.
- Candidate values remain unread while the noise instrument is debated.
- Independent probes attack decision boundaries, not only happy-path outputs.
- Mutation tests now demonstrate that the regression checker notices every
  consumed legacy input and every enumerated repair reversal.
- The bounded review limit prevents an endless sequence of increasingly local
  wording fixes from becoming de facto approval.

## What is not working yet

- RC-008 Draft 34 is frozen and unapproved.
- No supported rule yet selects the split used by the host-noise diagnostic.
- No host-noise estimator, candidate noise value or noise decision exists.
- No host is selected. Effective SNR, joint ten-placement feasibility and
  balance remain open alongside noise.
- Rank 2 is unmeasured, and no target manifest, donor assignment, generated
  hybrid recording or sorter result exists.

No new director decision is required at this exact step. The agents must first
complete their required terminal-disposition exchange. The older Phase-1
contract-review request remains open and nonblocking.

## What happens next

Claude must write the other required Convergence statement and either agree
with Codex's proposed **`Split/Redesign Required`** disposition or provide the
smallest safe counterproposal. There is no fourth repair round on this card and
no second like-for-like successor.

If the agents agree on redesign, the next specification must change the
boundary: for example, isolate and justify the split instrument separately, or
predeclare a multi-split decision whose direction and cost are explicit. Only
an explicitly approved redesigned specification can authorize implementation.
Candidate noise stays unknown until then.

## Verification artifact

There is no new director verification artifact this period. The final
`verify_realism.py` artifact still waits on a scientific result. The approved
rank-1 gate is a feasibility input, not the experiment's result.
