# Progress Report — Amendment 5: Real Control Donor Exclusion

**Current date and time:** 2026-08-12 19:11 PDT
**Trigger:** Claim Sheet Amendment 5 entered force in Codex Session 11

## The short version

Tier A asks whether spike waveforms taken from the host brain region change the measured comparison between spike sorters. Its two arms must therefore differ on region while staying closely matched on loudness, signal quality, depth, placement and data provenance. The project buys statistical precision by pairing each CA1 waveform with a control waveform that resembles it.

That pairing creates a problem the standard unpaired hybrid pipeline does not have: the waveforms most similar to CA1 waveforms are often other CA1 waveforms. On the pinned donor table, a simple nearest-unused matcher puts 3 of 16 CA1 waveforms into the nominally region-blind control. When it first tries the same source-insertion restriction the contract prefers, it puts 8 of 16 there. The measurement is diagnostic rather than predictive—the final host-specific covariates and matching rule do not exist yet—but it is large enough that leaving the choice open would let the eventual rule decide the scientific contrast by accident.

Amendment 5 is now agreed and in force. The real control pool excludes the injection zone's own donor waveforms before matching. For the current CA1 recommendation, that means removing the sixteen CA1 donors identified by their source dataset plus row number.

## Why the change is fair to the question

The [standard SpikeInterface hybrid workflow](https://spikeinterface.readthedocs.io/en/latest/how_to/benchmark_with_hybrid_recordings.html) draws templates without building a region-matched arm, so it has no reason to pair every control waveform against a CA1 target. This project does pair because it is designed to extract a usable comparison from one desktop rather than a large compute cluster. The strong pull back toward CA1 is therefore created by this project's precision strategy, not inherited from the field's standard generator.

A genuinely unpaired region-blind draw of sixteen from the 2,183-template pool, with sixteen CA1 members, contains 0.117 CA1 templates in expectation; the chance of at least one is 0.111, or about one arm in nine. The no-reuse paired baseline is slightly different because a template cannot partner with itself: 0.110. Those are two correct sampling models, not conflicting estimates.

## The price must still be measured

Removing CA1 can make the remaining control waveforms harder to balance, can force the provenance match from insertion to session or subject level, or can make a required stratum infeasible. The amendment therefore requires the eventual frozen matching rule to run twice without generating data:

1. once on the eligible pool before CA1 removal;
2. once on the post-removal pool that is allowed to govern generation.

Both states must report their selected waveform pairs, CA1 count, covariate objective and balance, provenance granularity, relaxations and infeasibility. The un-removed state is diagnostic only. It cannot become the executable state after inspection. If the post-removal state cannot satisfy the already-declared balance, placement and provenance requirements, Tier A fails cleanly under the existing contract rather than loosening the design after seeing it.

## One contract contradiction was retired explicitly

Amendment 3 already removed CA1 donors from both “nothing changed” pseudo-arms. Its limitation paragraph therefore said that those pseudo-arms did not reproduce the chance CA1 donors the real control might contain. Amendment 5 makes that sentence false: the real control and pseudo-arms now draw from the same post-removal base pool on this property.

The old amendment was not rewritten. Amendment 5 explicitly supersedes only that sentence from its own date forward. The rest remains true, especially the important limit that no no-manipulation control can reproduce the matched arm's all-CA1 region homogeneity—because that homogeneity is the manipulation being tested.

## Where the project stands

- Amendments 1–5 are in force.
- The real-arm matching-rule lane is open, but no rule has been written or approved.
- No host is pinned. Drift, noise, post-rescaling effective SNR, placement calibration and the independent balance/manipulation gate remain open.
- The later exact host-dependent selector/configuration approval remains separate.
- No Rung 0, hybrid generation or sorter run has occurred. No scientific result exists.

The Slot 8 verification artifact is unchanged: it cannot be built until results exist. The Reproducibility Packet now has a runnable design-stage runbook and data guide, but its result-verification script remains correctly marked as absent rather than implied complete.

## What comes next

The next technical contract item is the real-arm matching rule. It must be fixed before the eligible host-specific pool is visible, contain no region term in either direction, and define its provenance blocking, covariate objective, deterministic tie/failure rules and relaxations. Only after that rule is independently reviewed can host-specific configuration work proceed toward the separate exact-state gate.
