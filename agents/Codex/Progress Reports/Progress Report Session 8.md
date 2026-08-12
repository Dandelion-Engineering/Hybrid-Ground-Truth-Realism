# Progress Report — Codex Session 8

**2026-08-12 13:11 PDT**

**Project phase:** Phase 2 — Execution

**Public state:** In Progress

## The short version

The project still has **no scientific answer** to its main question. No host recording has been selected, no hybrid recording has been generated, and no spike sorter has run.

This stretch of work has been about making sure the first experiment will mean what we think it means before we spend the compute. That has paid off. The agents found that two amplitude columns previously compared as though they measured the same thing do not; replaced an ambiguous template “identifier” that repeated across the library; and tightened the strongest negative control so its selection recipe is genuinely fixed before the data it will operate on exists.

The host-selection strategy has now passed same-state review through Draft 5. That is approval of the **strategy and evidence**, not approval of a host. Three Claim Sheet amendments are in force; a fourth, governing the Tier A negative control, remains proposed while Claude re-reviews Codex's latest corrections.

## Why the negative control matters

Tier A asks whether a spike sorter behaves differently when injected spike shapes come from the same brain region as the host recording. The region-matched arm has only sixteen available CA1 donor shapes, while the region-blind arm draws from a much larger pool. That asymmetry can itself create differences through repeated donors, matching choices, or random seeds.

The safety check therefore builds two “fake” arms in which **neither arm uses brain region at all**, but one still draws from a fixed set of sixteen and the other from the full eligible pool. If that fake comparison produces an interaction as large as the real comparison, the project has evidence that its own machinery can manufacture the apparent effect.

This is not an optional polish step. It is the part that distinguishes “the sorter reacted to regional realism” from “the experimental procedure created a difference.” The construction is now written as Amendment 3 of the Claim Sheet. It is still blocked from use until both agents approve exactly the same text and, later, exactly the same host-dependent configuration.

## What changed in this review

### 1. The selector's template identifier was not unique

The contract said to record a selected donor by `template_index`. The live Neuropixels 1.0 snapshot contains 2,183 rows, but only **187 distinct** `template_index` numbers because the count starts over inside each source dataset. A row number by itself therefore cannot tell a reader which waveform was selected.

The contract now uses the pair **(source dataset, row number)**. That pair is unique for all 2,183 rows and will be used for both the real and fake arms. This is a small-looking repair with a large reproducibility consequence: without it, two independent implementations could honestly read the same configuration and inject different waveforms.

### 2. A fixed seed did not make the search reproducible

Claude correctly argued that the rule for choosing the fake sixteen should be fixed before the eligible pool is visible. But the first written recipe still left several choices open: which random-number generator interprets the seed, how the starting set is drawn, which swap is tried first, whether the first improvement or best improvement wins, and what happens when the search budget expires.

The revised rule closes those choices. It uses a SHA-256 ranking of the unique template addresses for the starting set; evaluates complete one-for-one swap sweeps; takes the best strict improvement with an exact tie rule; never stops partway through a sweep; and records whether it stopped because no better swap existed or because the 100,000-comparison ceiling was reached. A zero-variance or non-finite input fails loudly instead of triggering an improvised fallback.

This is a **bounded search**, not a claim that every possible sixteen-template combination was examined. That distinction is now explicit.

### 3. The reason for fixing the rule early was corrected

The previous draft said that matching the CA1 shapes more closely would necessarily make the safety band narrower, while matching them less closely would widen it. That sounds intuitive, but the band is produced by actual sorter behaviour and the project has not measured a monotonic relationship between the matching score and the band width.

The stronger and simpler reason to precommit is the one that survives scrutiny: if several defensible recipes are tried after the pool is visible, the agents could keep whichever one happens to produce the most reassuring band. Fixing one recipe beforehand closes that path without pretending we know how the band must move.

## The amplitude check, in ordinary language

The donor library records amplitude as the full trough-to-peak swing of an **average waveform**. The host files record the median of **individual spikes' one-sided peaks**. Both numbers are in microvolts, which made them look comparable even though they describe different objects.

Claude measured the conversion between those definitions on 1,821 units in one processed recording. The median ratio was roughly 1.2, with enough spread that it supports only a rough population-level restatement, not a per-neuron conversion. Codex independently reproduced the cohort counts and ratio medians from the saved raw JSON and checked the definitions against the [`hybrid_template_library` source pinned to the project's commit](https://github.com/SpikeInterface/hybrid_template_library/tree/0023db29688842f74698bac40c48a86477ea39e7).

The check does **not** settle the preprocessing difference. The donor averages and host amplitudes were computed after different preprocessing chains. That remaining comparison belongs to the short Rung 0 pilot, when the real injection stack exists.

One related decision is now explicit: the amount by which a donor waveform is scaled will be **reported as a diagnostic**, but it will not become a new matching covariate or a post-hoc pass/fail threshold. The sorter sees the final rendered waveform. The gates that matter are its achieved amplitude, effective signal-to-noise ratio, placement, and provenance. Rung 0 must still verify finite scale factors, no clipping or overflow, and the intended final amplitudes.

## What is working

- Metadata-only range reads continue to answer expensive questions without downloading 18–197 GB recordings. The source dataset is [DANDI 000409](https://dandiarchive.org/dandiset/000409), but this session used only the already-tracked results and no new recording read.
- The candidate search has discharged anatomy, duration, and label ambiguity. CA1 remains the first region to test because it also has the strongest biological basis for the later burst manipulation.
- The current candidate order is practical rather than superlative: test the strongest candidate first and select the first one that clears every gate, instead of finishing a census to claim a “best” recording the study does not need.
- Draft 5's same-state review is closed at its declared scope. The amplitude-convention evidence and its one-session limitation are both on the record.

## What is not working yet

- **No host is pinned.** Drift, noise, post-rescaling effective signal-to-noise ratio, placement calibration, and the final covariate-balance gate remain open.
- **Placement is still parameterized.** Donor waveform footprint can justify the edge margin, but the minimum spacing between injected peaks needs a separate basis from native peak spacing and the generator's relocation behaviour.
- **Amendment 3 is not in force.** Codex approves the revised technical and accessible sheets, but Claude must genuinely re-review those exact states. Tier A generation remains blocked until that same-state cycle closes; the later host-dependent selector configuration has its own separate approval gate.
- **The complete region-label bridge is unfinished.** This does not block the CA1 host search, but it will matter when the region-blind arm's placements are finalized.
- **The Reproducibility Packet is not assembled.** The surviving scripts are being written inside it, but its own runbook, dependency file, data guide, and clean-copy test are still future work.

There is no new director-only blocker. The Phase 1 contract-review request remains open and non-blocking, and the agents do not need a decision from Randy unless the Amendment 3 review fails to converge.

## What comes next

1. Claude re-reviews the revised Amendment 3 states. If the same bytes are approved, its status can move to `In force`; otherwise the specific disagreement stays visible.
2. Codex prepares the two-part placement calibration and the 60-second Rung 0 substrate without launching a heavy run prematurely.
3. The first candidate is tested for drift, noise, effective signal-to-noise ratio, and balance. Native yield and scale factors remain visible diagnostics, not silently invented thresholds.
4. Immediately before any heavy step, the session measures live RAM and graphics memory and applies the project's admission floors. A schedule is not a guarantee that the machine is free.
5. Only after every host gate, contract gate, and exact-configuration gate passes can Tier A generation begin.

The director's verification artifact has no new state to show yet. That is appropriate: the experiment has not generated a result, and the project should not manufacture a verification update before there is something real to verify.
