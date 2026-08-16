# Progress Report — Codex Session 32

**Date and time:** 2026-08-16 02:26 PDT

**Project phase:** Phase 2 — Execution

**Public state:** In Progress; no scientific result exists

## The short version

The project now has an approved way to inspect one candidate recording while
refusing any newly fetched archive block that would cross the declared
distinct-data ceiling. Actual retry traffic remains separately reported. That
closes the implementation gate that was still open in my Session 24 report. It
does **not** mean a host has been chosen: no candidate has been opened, no drift
value exists, and no scientific result exists.

The path here was longer than expected but bounded. The first archive-reader
review ended without approval after three rounds. Under the director's revised
review method, that failure could not be reset indefinitely: the agents agreed
on the defects, closed that card, and opened one tightly scoped successor. The
successor reached exact-state approval in its third and final round.

## What changed since Session 24

The probe-movement rule described in the previous report was repaired and
approved first. Its final form measures eleven consecutive one-minute points,
which span the intended ten minutes, and no longer claims that minute medians
can bound motion that happens entirely between those samples.

The next problem was safe archive access. A candidate in
[DANDI 000409](https://dandiarchive.org/dandiset/000409) is much too large to
download merely to decide whether it is suitable. The command therefore opens
the remote HDF5 file — the structured container used by the recording — and
requests only the small metadata and spike-depth slices needed for the declared
drift check. The implementation uses [h5py](https://docs.h5py.org/) to interpret
that container.

Review found three classes of boundary error across the original card and its
successor:

- a required provenance value could be missing, negated, or inconsistent
  between the raw and processed halves while the command still reached a
  verdict;
- a stream for a similarly named probe could be mistaken for the requested
  probe;
- a budget could count the bytes h5py *asked for* while the lower-level reader
  fetched a much larger cache block.

The approved state now requires a complete affirmative conversion statement on
both assets, requires the same converter version, parses the probe name exactly,
and refuses a distinct cache-block transfer before it occurs when that transfer
would cross the declared ceiling. The record keeps logical request bytes,
distinct transferred bytes, and total transferred bytes separate so that none
is presented as another.

## What was unexpected

The strongest surprise was where the extra bytes were spent. The Round-2 test
showed 2,081,456 distinct bytes transferred under what had been described as a
65,536-byte provenance budget. Measurement then showed that all of those bytes
belonged to four earlier ordinary reads, before the provenance read began. The
repair therefore had to hold the caller's outer ceiling open across the whole
operation, not just correct the one local check named by the finding.

I also investigated whether retry traffic invalidated the repaired distinct-byte
bound. It did not. Retries intentionally do not count as new distinct blocks,
while actual total traffic remains separately reported. Treating those two
quantities as interchangeable would have created a false blocker.

## What is working

- RC-001, the probe-movement gate, is approved on an exact prose,
  implementation, and test state.
- RC-003, the bounded archive reader, is approved on an exact nine-file state.
- My final rerun passed all 382 owner checks, all 26 repair-mutation challenges,
  all 18 checker-mutation challenges, both focused repair verifiers, and the
  packet consistency check.
- The bounded review method did what it was designed to do: defects stayed
  visible, the agents could not treat broad green tests as approval, and the
  review still reached a terminal decision.
- All adversarial work used generated local fixtures. No candidate or network
  resource was read during review.

## What is not working yet

There is still no host recording and no result. Reader approval only permits the
next plan-only candidate measurement; it does not approve the candidate, the
later placement and matching configuration, generation, or a sorter run.

The remaining Phase-2 path is substantial: measure candidates in the pinned
order, pass the drift, noise, and effective-SNR gates, approve the exact
placement schedule and matcher implementation, verify balance independently,
then separately authorize generation and sorter execution. The older director
request for a Phase-1 contract review remains open but nonblocking; no new
director decision is needed for the immediate step.

## What happens next

Claude owns the first real read. The planned first attempt is the pinned
CSHL047/Probe01 candidate under the strict gate, with a fresh machine-headroom
measurement and a plan-only output. If it refuses, the refusal is the result of
that attempt and the next candidate remains a separate action. If it produces a
drift record, that record still has to pass the contract before any host is
pinned.

## Verification artifact

There is no new director verification artifact this period. The final
`verify_realism.py` artifact still waits on a scientific result, and no
scientific result exists.
