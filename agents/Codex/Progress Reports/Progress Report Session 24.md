# Progress Report — Codex Session 24

**Date and time:** 2026-08-14 22:15 PDT

**Project phase:** Phase 2 — Execution

**Public state:** In Progress; no scientific result exists

## The short version

The project is still choosing the recording that will host the first experiment. Since my Session 16 progress report, the two agents have finished the prose rule for matching the two waveform groups, fixed the order in which candidate recordings will be considered, and built a tested check for whether the probe stayed steady enough during a recording.

That steadiness check is **not approved yet**. Its first review under the director's new bounded-review method found a defect that can let a recording pass even when every tracked neuron moves farther than the declared tolerance. No real recording has been measured, so the defect was found at the cheapest and safest point: in synthetic data, before it could choose the experiment's host.

## Why probe movement matters

A Neuropixels probe records many neurons along a thin vertical shank. If the probe and tissue move relative to one another, a neuron's waveform can move across recording contacts. A spike sorter then has to distinguish biological spikes while the signal it sees is changing. This project therefore needs a host recording whose movement is below a limit chosen before any candidate is inspected.

The source archive is [DANDI 000409, the IBL Brain-Wide Map](https://dandiarchive.org/dandiset/000409). Its processed files expose a depth estimate for each spike. The proposed check groups those depths into one-minute bins, takes the middle value for each neuron in each minute, combines the neurons into one trace, and asks for the largest excursion across ten consecutive bins. A shuffled version of the same depths supplies a recording-specific noise reference. A candidate passes only when both numbers are at or below 20 micrometres in the strict pass.

That construction is deterministic, inexpensive, and well tested. The problem is what its ten-bin number means.

## What the new review found

Ten one-minute bin medians span only nine minutes between their centres. The document nevertheless called their range the worst movement inside a ten-minute segment and said it protected the experiment wherever that segment landed.

An independent test makes the mismatch concrete. Five synthetic neurons all followed a smooth ramp of 2.1 micrometres per minute. Over ten minutes they moved 21 micrometres, beyond the 20-micrometre limit. The implemented check reported 18.9 micrometres; its noise reference was 18.7; the candidate passed. This is not a borderline coding error. It is the definition doing exactly what it says while the document gives that number a stronger meaning than it has.

Two sharper cases expose the same root problem:

- a common 30-micrometre episode shorter than half of one minute disappeared from every minute median, the combined trace, the noise reference, and even the per-neuron audit; the check passed at zero;
- a ten-minute segment starting halfway through a minute can touch eleven grid bins, so it can contain a 30-micrometre range even when every aligned ten-bin window reports only 15.

These cases satisfy the check's declared inclusion rules, and every neuron carries the movement. They are therefore separate from the already-published limitation that the combined median can hide a *minority* of moving neurons. The owner has to revise the numerical definition or add another pre-measurement gate that covers the missing time scales. Wording alone cannot repair the smooth-ramp pass.

The same exhaustive pass found a second, smaller overclaim. One synthetic series had been used to say that hiding a moving minority gets easier as the number of neurons grows. The three examples did not actually hold the moving fraction fixed, and a fixed-fraction counterexample reverses the direction between two sizes. The safe conclusion is that masking can occur; the current evidence does not order the real candidate recordings by how many neurons they contain.

## What is working

- The new Review Card fixed the exact state, scope, purpose, runnable tests, and blocking rule before review began.
- Round 1 produced one complete ledger rather than returning the first defect and saving the next for another session.
- The shipped implementation agrees with its written algorithm. Its own harness passed 86 checks, and an independent recomputation matched forty randomized observations plus a deterministic permutation reference.
- No candidate data were opened. The fixed host order, archive reader, and every downstream execution gate remain untouched.

## What is not working yet

- The drift candidate cannot be approved until the time-window defect and the unsupported unit-count direction are repaired.
- The archive-reading command that would measure a real candidate remains deliberately unwritten.
- The director also asked the agents to replace human escalation with a consensus procedure that does not leave work waiting on his asynchronous response. I proposed a bounded agent-only decision: evidence decides what may ship; the agents agree on the safe terminal action — approval with follow-ups, revisions, or redesign — and a successor review cannot reset forever. Claude's response is pending; the review playbook has not been changed without that agreement.

## What happens next

Claude owns the drift specification and implementation response. Codex's next review is delta-only: verify the three recorded findings and any regression introduced by the repair, without reopening unchanged material. Only a same-state approval can close the card. Candidate measurement stays blocked until then.

The next larger pieces are still separate: the archive reader, the noise and effective-SNR host gates, placement calibration, the schedule and matching implementations, independent balance approval, generation, the feasibility pilot, and sorter runs. None has been collapsed into this review.

## Verification artifact

There is no new director verification artifact this period. The final `verify_realism.py` artifact still waits on a scientific result, and no scientific result exists.
