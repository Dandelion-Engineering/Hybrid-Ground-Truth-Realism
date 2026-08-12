# Progress Report — Phase 1 Close

**Date:** 2026-08-11 17:11 PDT
**Transition:** Phase 1 — Sharpening closed; Phase 2 — Execution opened

## Where the project stands

The planning contract is finished. Claude and Codex have explicitly approved the same technical [Claim Sheet](../../../Claim%20Sheet.md), the same [Accessible Claim Sheet](../../../Accessible%20Claim%20Sheet.md), and the same source/PDF pair for [Study Guide Pass 1](../../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.pdf). The initial division of labor is also agreed.

That means the project can now begin measuring rather than planning. It does **not** mean the scientific question has been answered. No sorter comparison, realism manipulation, or result exists yet.

The contract asks whether changing the realism of synthetic spikes changes measured spike-sorting accuracy and, more importantly, whether it changes the comparison between sorters. The motivating limitation comes directly from the maintainers of the hybrid pipeline ([Buccino et al., 2026](https://doi.org/10.7554/eLife.110170.3)).

## What is fixed before results exist

Three realism properties will be tested one at a time:

1. **Region-matched spike shapes.** Donor waveforms are matched to the local brain region where they are injected.
2. **Population-coupled firing.** Injected neurons follow changes in nearby population activity while keeping total spike count and average rate fixed.
3. **Bursting with waveform shrinkage.** Short bursts are paired with the amplitude attenuation real neurons show after recent firing.

Every axis has a stop-or-go manipulation check. If the intended property did not actually change at a biologically justified magnitude, no sorter run starts for that axis. This is what makes a negative result interpretable: without the gate, “realism did not matter” and “we implemented realism badly” would look identical.

The comparative decision rule is also fixed. The project measures how much the realism-induced accuracy change differs between sorters, then compares the size of that interaction with a pre-declared practical margin. A tightly bounded small effect is a real negative result. A wide interval centered near zero is **inconclusive**, never evidence that realism does not matter.

## What review changed

The review cycle materially changed the design before any result could reward one choice over another.

- A threshold borrowed from another paper was rejected because its standardized effect size was not comparable to the raw paired accuracy change measured here.
- Tier A was corrected from an impossible “same donor identity” pairing claim to matched donor slots; changing donor region necessarily changes donor identity.
- Tier B's population signal was made sorter-independent. An earlier version would have let a sorter help generate the data used to grade itself.
- A “significant in one arm, not significant in the other” rule was removed. The design now tests the difference directly.
- The negative control was recognized as full sorter work rather than generator-only work, doubling the minimum projected workload to 200 recording-minutes per candidate sorter per axis while leaving the 48-hour admission ceiling unchanged.
- The host constraint became sharper: CA1 is the only current candidate that satisfies the Tier A donor screen and Tier C's biology on its face, but it is not selected. Its worst-case donor exclusion leaves only six templates, so a host-specific feasibility query still decides it.
- The Study Guide now teaches the baseline as Poisson-like firing **plus the refractory period already implemented upstream**, which explains why refractoriness is a control-arm property rather than a missing realism axis.

These are not stylistic improvements. Several would have changed the experiment's answer or made it uninterpretable.

## What is working

- The live template snapshot has been audited by both agents independently: 7,877 rows total, including 2,183 IBL Neuropixels 1.0 templates across 170 area labels, with matching SHA-256 checks.
- The audit script already lives inside the Reproducibility Packet and can reproduce the pool-size screen without third-party dependencies.
- The technical and plain-language contracts carry the same fifteen slots, numerical budgets, success/failure rules, and non-transfer boundaries.
- Study Guide Pass 1 builds cleanly to 13 pages and gives the director the concepts needed to follow Phase 2: pairing, the interaction, the hierarchical bootstrap, the manipulation gate, and the honest third outcome.

## What is not working yet

The shared machine's system memory is heavily contended. Four measurements today found only 3.46, 3.96, 1.01, and 0.89 GiB free out of 31.67 GiB, while graphics memory remained mostly free. The known full-length Kilosort4 run peaked at 29.3 GiB of system memory. The open entry in `director_requests.md` asks whether there is a predictable quiet window or whether this project should deliberately adopt a permanent small-memory ceiling.

Nothing is blocked on that answer yet. The contract requires a live memory measurement immediately before every heavy step and forbids starting a run that cannot preserve its headroom. If the pilot does not fit, the agents will do smaller non-compute work and retry rather than override the gate.

Three scientific uncertainties also remain open by design:

- CA1 is a candidate host zone, not a selection.
- The sorter panel is not chosen until every candidate is timed and memory-profiled on the same 60-second segment.
- The negative-control band and the main interaction may have different achieved precision even with equal block counts; both widths must be reported.

## What happens next

Codex owns **Rung 0**, the feasibility pilot and sorter-panel decision. Immediately before any candidate run it will measure free RAM and VRAM. Each candidate gets one 60-second admission run, a 60-minute wall-clock ceiling, and strict live-headroom guards. The pilot records runtime and peak memory, then projects the per-candidate, per-axis, and whole-panel cost before admitting anything to the primary run.

Claude owns the Tier A host and injection-zone selection. That work checks the exact host's donor-source exclusion, local anatomy, placement capacity, and post-rescaling balance. Codex owns the independent Tier A manipulation/balance gate. The inference and negative-control harness is also Codex's responsibility. Tier B and Tier C implementation assignments follow the pilot, with the non-author grading each manipulation check.

The director's review of the Claim Sheet is now open through `director_requests.md`, but it is intentionally non-blocking. Any feedback that changes the plan becomes a dated amendment; execution continues in the meantime.
