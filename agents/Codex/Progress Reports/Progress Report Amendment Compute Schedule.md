# Progress Report — Amendment 1: Compute Schedule and Corrected Memory Story

**Trigger:** Codex wrote the approving turn on Claim Sheet Amendment 1

**Date:** 2026-08-11

## The short version

The project's first contract amendment is now in force. It corrects what the agents thought was happening to the shared computer's memory and records the daytime/overnight schedule Randy set, while leaving every safety rule and every scientific commitment unchanged.

The correction matters because the original measurements were real but their explanation was not. Across four sessions the machine showed only 0.9–4.0 GiB of free system memory. Both agents described that as other research work competing for the machine. Randy established that the memory was actually held by finished Claude automation processes that had failed to exit. He cleared them; a process-leak fix was being built rather than confirmed complete.

The honest record is now: **we measured the number correctly and asserted a cause we could not observe.** The declining series must not be used to reason about competition or future availability.

## What changed in the contract

Two Dandelion research projects share this desktop under a director-set convention:

- this project aims heavy work at the daytime;
- the other project aims at overnight; and
- the convention is not a reservation or guarantee.

That final point is load-bearing. A schedule lowers expected overlap; it does not promise that a run fits. The machine can still contain a leaked process, an overnight job can overrun, or free memory can change between two measurements.

## What did not change

Every launch guard is preserved:

- measure free system memory and graphics-card memory immediately before each heavy step;
- a run may use no more than 75% of what was free at that moment;
- preserve at least 4 GiB of system memory and 2 GiB of graphics memory;
- never inherit a number from a report, including a quiet-window number; and
- do not start a run that does not fit.

The experiment did not become larger or smaller. Segment lengths, randomization blocks, the 48-sorter-hour admission ceiling, the 200-recording-minute primary tranche, the sorter-panel rule, and the definitions of success, failure, and inconclusive are unchanged. If the panel narrows, the 60-second pilot will have measured that it must narrow.

## Where the project stands

Phase 2 remains open and **no sorter has run**. The host-selection strategy now has explicit approval from both agents at its declared scope, and all eleven current CA1 candidate assets pass the duration gate. A host is still not pinned; drift, noise, effective signal-to-noise after rescaling, ten-placement feasibility, and covariate balance remain open.

The first proposed technical correction beyond Amendment 1 is still under review: the CA1 donor pool contains exactly sixteen templates for a ten-unit arm. Both agents agree on an exposure-balanced schedule and on reporting the result as conditional on those sixteen templates. They also converged on a no-manipulation control that mirrors the finite-versus-large donor-pool asymmetry without changing the compute budget. Those pieces do not govern execution until their synchronized amendments receive exact-state approval.

## What is working

The amendment protocol did what it was meant to do: a changed fact was added to the contract rather than left in a chat, the earlier language remains visible, and the operative rules are now unambiguous to a future session.

The resource design is also behaving correctly. Rung 0 is a one-minute pilot precisely so feasibility is measured on this machine before the project commits to hundreds of sorter-minutes. SpikeInterface's [official hybrid-recording workflow](https://spikeinterface.readthedocs.io/en/latest/how_to/benchmark_with_hybrid_recordings.html) confirms that the caller chooses the recording into which templates are injected; the pilot will therefore pin its preprocessing and injection order rather than assume the library does it.

## What is not working or not finished

- The process-leak fix was not confirmed landed. A future collapse in free system memory with graphics memory unchanged remains a known warning signature.
- Amendment 2 still awaits Claude's owner re-review after Codex removed two unsupported claims about shared rig design and mouse strain.
- The no-manipulation pseudo-control needs its own synchronized Amendment 3 because its two arms intentionally use different pool constructions under the same non-region-conditioned state.
- The host is not pinned and the scientific measurement has not begun.

No director action is required. The only open director request remains the non-blocking Phase 1 contract review.

## Next stretch

Claude's next review should close or revise Amendment 2 and author Amendment 3. Host selection then continues through the remaining gates. Codex's next execution step is Rung 0: pin the injection substrate and sorter commands, measure live RAM/VRAM, and run only if the existing admission rules pass.
