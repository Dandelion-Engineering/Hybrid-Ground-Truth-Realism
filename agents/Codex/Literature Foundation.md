# Literature Foundation — Codex

**Date:** 2026-08-11
**Phase:** Phase 0 — Literature Review
**Question:** Does the realism of hybrid ground truth change measured spike-sorting accuracy or the ranking between sorters?

## Scope and independence note

This survey was assembled from live searches of primary papers, official documentation, source code, and first-party dataset metadata. The project workflow required reading Claude's active handoff before beginning, so this was not a blinded review. The source checks, resource audit, and methodological synthesis below were nevertheless re-derived independently rather than copied or merged from Claude's foundation. Divergences are preserved for the Phase 0 comparison.

---

## 1. Domain and methods landscape

### 1.1 There are three imperfect kinds of spike-sorting ground truth

**Paired intracellular/extracellular or juxtacellular/extracellular recordings** provide real spike times for a real neuron in real noise. They are the realism ceiling, but they usually expose only one ground-truth unit per recording, are difficult to acquire, are often short or anesthetized, and overrepresent neurons that can be patched and detected. They cannot supply the many simultaneous units needed to stress merging, splitting, collisions, and high-density probe drift.

**Fully simulated recordings** can provide every unit and every spike, vary one mechanism at a time, and scale cheaply once the simulator exists. Their weakness is total model dependence: the voltage field, noise, spike trains, morphology, and drift can all be wrong together. Pachitariu et al. demonstrated that a biophysical benchmark with waveforms too slow relative to real Neuropixels units generated many false-positive clusters; merely accelerating the simulation twofold made waveform duration more realistic and reduced false positives. This is direct evidence that simulator realism can move measured sorter performance.

**Hybrid recordings** retain a real recording as background and add units with known spike times. They preserve real noise, endogenous spikes, artifacts, and—if handled correctly—motion, while allowing multiple injected ground-truth units. But the injected units remain generated objects. Their realism depends on at least five separable layers:

1. template identity and region/cell-type plausibility;
2. marginal spike-train statistics, including refractory periods and bursts;
3. population-coupled rate non-stationarity;
4. spike-history-dependent waveform dynamics, especially amplitude attenuation within bursts; and
5. spatial placement, density, and motion consistency with the host recording.

The present project is therefore not a contest among these ground-truth classes. It is a controlled sensitivity analysis of one widely used hybrid benchmark.

### 1.2 Existing hybrid generators preserve different pieces of reality

The current SpikeInterface path injects average templates into real recordings. Its default `generate_hybrid_recording()` call generates 10 units at 15 Hz with a 4 ms refractory period, adds independent amplitude jitter (`amplitude_std=0.05`), and can follow an externally supplied motion object. It accepts a caller-supplied sorting, so temporal realism can be changed without rewriting the injection engine. Region selection is likewise available through the template library's `brain_area` metadata. This means the project can isolate realism axes instead of building a new generator.

SHYBRID takes a different route: spikes from an observed unit are relocated on the probe to create a virtual unit. Its value here is conceptual. A relocated real train retains temporal structure that an average-template-plus-Poisson construction discards. It is not automatically a better control—donor selection and imperfect spike removal introduce their own bias—but it proves that retaining real train structure is technically possible.

Pachitariu et al.'s Kilosort4 hybrid benchmark occupies a middle position. It injected average waveforms, but modulated exponential inter-spike intervals by the local population firing rate measured in 100 ms bins and enforced a 2 ms refractory period. That is important for this project: **population-coupled firing is missing from the default SpikeInterface benchmark under test, but it is not a novel mechanism in the broader benchmarking literature.** The same study's full simulator went further by shuffling empirical inter-spike intervals for single units.

### 1.3 Region matching and temporal realism target different causal mechanisms

Jia et al. found distinct multichannel spatiotemporal extracellular waveform profiles across brain regions and improved region classification when multichannel rather than single-channel features were used. Region mismatch is therefore not merely a metadata-label mismatch; it can alter the spatial waveform features that template-matching and clustering stages consume.

Temporal realism has at least two non-equivalent tiers:

- **Population-rate coupling** changes when spikes occur over seconds to minutes while leaving a unit's within-train renewal structure and waveform response largely simple.
- **Burst/history coupling** changes short inter-spike intervals and the waveform emitted after recent spikes. Pouzat et al. built a sorter around non-Poisson discharge statistics and the empirical fact that spike-event amplitude decays at short ISIs. Harris et al. found CA1 complex-spike bursts whose probability and length depend on recent silence and whose burst properties correlate with extracellular amplitude.

These tiers must not be collapsed into a single “non-stationarity” switch. A null for population-rate coupling would not settle burst-dependent waveform dynamics.

### 1.4 The primary estimand is an interaction, not a main effect

For injected unit `u`, recording `r`, sorter `s`, and realism condition `c`, let `A(u,r,s,c)` be accuracy. The paired realism effect for a sorter is:

`Δ_s = A(u,r,s,realistic) - A(u,r,s,control)`.

The quantity that tests whether realism changes a sorter comparison is the **difference in differences**:

`I(s1,s2) = Δ_s1 - Δ_s2`.

A uniform accuracy loss can make absolute hybrid scores misleading while leaving rankings unchanged. Conversely, a small average main effect can hide a differential effect concentrated in low-SNR or bursty units that reverses a ranking. This is why a realism main effect, a sorter main effect, and their interaction must all be reported separately.

With only two sorters, “ranking stability” is just whether the paired performance difference changes sign. Rank correlations become meaningful only with a panel of at least three sorters. The design should therefore either use three credible sorters or avoid decorating a two-sorter sign comparison with rank-correlation language.

---

## 2. Benchmark results and calibration

### 2.1 The anchor benchmark supplies scale, but not a universal flip threshold

Buccino et al. injected 10 units in five randomized instances per recording, totaling 1,800 Neuropixels 1.0 and 3,000 Neuropixels 2.0 ground-truth units. Kilosort4 exceeded Kilosort2.5 with Cohen's d values of 0.276 (NP1) and 0.408 (NP2) for accuracy; effects were strongest below SNR 10. These are useful scale references and identify low-SNR units as a likely effect modifier.

They are **not**, by themselves, a decision threshold for this project. A ranking flip depends on the condition-specific paired gap between sorters and the sorter-by-realism interaction. Cohen's d from a different sample and variance structure cannot be subtracted directly from a raw accuracy change. The Claim Sheet should use the anchor effects as contextual calibration, then predeclare a decision rule in the units of this experiment—paired accuracy differences and their uncertainty.

The anchor's cost also matters. The authors estimated 870 hours for their NP1 sorter comparison and 846 hours for NP2 on a single workstation; their distributed workflow reduced effective wall time to roughly half a day. This project cannot imitate their scale on one shared desktop. It must gain precision through reuse of the same recording, injected unit identities, spike trains, placement, amplitude/SNR targets, and random seeds across realism arms.

### 2.2 Published performance varies sharply with benchmark class

There is no stable field-wide “normal accuracy” independent of the ground truth:

- In Yger et al., SpyKING CIRCUS averaged 4.8% error on 37 large-waveform in-vitro paired units but 14.8% on the two available large-waveform in-vivo paired units. On their hybrid comparison, SpyKING CIRCUS and Kilosort were close (4.4% versus 4.2% average error).
- SpikeForest aggregated more than 30,000 ground-truth units and found no universal winner across paired, simulated, and hybrid studies. Synthetic studies often showed precision higher than recall in a way paired studies did not, which the authors linked to imperfect firing and noise statistics.
- The current SpikeInterface hybrid tutorial is illustrative rather than a population estimate, but its own example found roughly 10–12 units above 0.8 accuracy for Kilosort2.5, Kilosort4, and SpyKING CIRCUS 2, with different precision/recall profiles.
- Pachitariu et al. benchmarked ten sorters on three hybrid recordings and separately showed that waveform realism in a biophysical simulation altered false-positive behavior.

This spread is not noise around one truth; it is evidence that benchmark construction is part of the measurement instrument. The project should not define success as “accuracy changed at all.” It should define which changes would alter a scientific or engineering decision.

### 2.3 Accuracy alone is insufficient

SpikeInterface defines unit matching from coincident spikes, then exposes accuracy, precision, recall, and unit classifications such as well-detected, false-positive, redundant, overmerged, and oversplit. Collision work by Garcia et al. further shows that sorter families can fail differently at short temporal separations.

The minimum outcome set should therefore include:

- per-unit accuracy, precision, and recall;
- well-detected unit counts at predeclared thresholds;
- false-positive, redundant, overmerged, and oversplit unit counts;
- collision or short-ISI recall for the temporal axis;
- results stratified by SNR/amplitude and the manipulated unit property; and
- the sorter-by-realism interaction with paired uncertainty.

If only the aggregate median is reported, a realism effect confined to difficult units can disappear.

---

## 3. Dataset and resource landscape

### 3.1 DANDI 000409 — host recordings

DANDI 000409 is the IBL Brain Wide Map: 2,048 assets, about 49.7 TB, 139 subjects, NWB format, open access under CC-BY-4.0. The full collection is far too large and unnecessary. The project needs a deliberately selected, identifier-pinned subset with host-region metadata, duration, channel geometry, drift, and noise documented.

The host recording should be chosen jointly with template feasibility, not first. A region label is only experimentally useful if the library contains enough compatible templates to support matched and mismatched arms after amplitude/SNR calipers.

### 3.2 `hybrid_template_library` — current live audit

The official tutorial renders an older snapshot with 601 templates and more than 70 area labels. A direct audit of the live first-party `templates.csv` on 2026-08-11 found:

- **7,877 total rows**;
- **2,183 IBL/Neuropixels 1.0 rows** across **37 source datasets** and **170 distinct `brain_area` labels**;
- IBL template amplitude range **52.19–923.15 µV** (median **184.22 µV**);
- IBL SNR range **2.43–48.44** (median **9.78**);
- high-count IBL labels including SUB (168), CP (107), PIR (94), MRN (59), SSp-m6a (56), AON (53), ENTl5 (53), ENTl6a (51), VISa5 (50), and LP (47).

The downloaded CSV was 2,032,640 bytes with SHA-256 `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`; the S3 response reported ETag `a5f37c65cd175fa8b75178c5195b20a1` and Last-Modified `2024-09-29 08:56:05 GMT`.

This substantially reduces the broad feasibility risk for region matching. It does **not** prove feasibility for a specific recording because no host recording/region has yet been selected and the matched arm must survive joint area, probe, amplitude, SNR, and placement constraints. It also exposes a reproducibility obligation: the online table is mutable and the tutorial is stale. The packet must preserve or checksum the exact metadata snapshot and record selected row identifiers.

The library is MIT-licensed. Its IBL templates come from the same DANDI family proposed for host recordings. That improves domain match but creates potential donor/host leakage if the exact source dataset is reused. Selected template rows should exclude the host recording's own dataset unless a deliberate same-recording control is predeclared.

### 3.3 SpikeInterface — generator, sorter interface, and evaluator

SpikeInterface is MIT-licensed and provides the template query, injection engine, motion-aware injection, internal sorters, and ground-truth comparison objects. Using one framework lowers interface variance, but the project must pin an exact release/commit and record defaults rather than trust moving documentation.

The official hybrid tutorial already runs Kilosort2.5, Kilosort3, Kilosort4, and SpyKING CIRCUS 2. Current internal-sorter documentation also exposes SpyKING CIRCUS 2, TriDesClous 2, and Lupin. Garcia et al. report that these internal pipelines run on CPU; TriDesClous 2 is relatively fast, SpyKING CIRCUS 2 finds more units at the cost of false positives and runtime, and Lupin trades somewhat more runtime for higher simulated accuracy. These are scientifically more useful contrasts than another Kilosort generation because their clustering and template-matching components differ.

A defensible staged panel is therefore **Kilosort4 plus two CPU internal sorters**, provisionally TriDesClous 2 and SpyKING CIRCUS 2 or Lupin. The final choice requires a short same-recording feasibility pilot; published runtimes from other hardware are not a substitute for the shared-machine measurement.

### 3.4 Licensing boundary

- DANDI 000409: CC-BY-4.0; attribution required, raw data referenced rather than redistributed.
- `hybrid_template_library`: MIT.
- SpikeInterface and its internal sorters: MIT.
- Kilosort4: GPLv3; call it as an external tool, do not copy or vendor its source into project code.

No additional paid resource is needed for Phase 0 or the proposed pilot.

---

## 4. Failure modes and known dead ends

### 4.1 Turning several knobs at once

Changing template region, spike timing, burst structure, amplitude-history coupling, density, and motion in one “realistic” arm would make any effect uninterpretable. Region identity should be tested with spike times fixed; temporal tiers should be tested with templates fixed. A combined arm can follow only after one-axis effects are identified.

### 4.2 A null without a manipulation check

A sorter null is uninterpretable unless the generated data show that the intended property changed at a realistic magnitude. Required pre-sorter gates include:

- region arm: predeclared separation in waveform features while amplitude, SNR, probe, and placement remain balanced;
- population-rate arm: agreement between injected and local host population-rate trajectories, plus unchanged mean rate and refractory violations;
- burst arm: target short-ISI/burst distribution and spike-history-dependent amplitude attenuation, plus unchanged long-timescale rate where intended.

Failure at this gate stops the sorter run. It is evidence about the generator implementation, not the scientific question.

### 4.3 Treating region as an isolated label

`brain_area` covaries with cell type, layer, source dataset, waveform duration, spatial extent, amplitude, SNR, and template quality. A matched-versus-random comparison can therefore become an amplitude or dataset comparison. Templates should be paired or caliper-matched on probe geometry, amplitude, SNR, depth/placement feasibility, and preferably source dataset family, while excluding the host's exact dataset.

### 4.4 Reusing effect sizes in incompatible units

The anchor Cohen's d values summarize sorter differences under its own variance structure. They do not define how large a raw accuracy interaction must be to reverse a ranking here. The project should report both raw paired differences and standardized effects, but predeclare decisions in raw accuracy/rank terms.

### 4.5 A homogeneous sorter panel

Kilosort2.5 versus Kilosort4 tests a family lineage more than the field's ranking stability. A null from that pair cannot support a general claim that rankings are realism-invariant. At least one CPU internal sorter with meaningfully different clustering/matching behavior is required; three sorters are preferable if the pilot fits the compute envelope.

### 4.6 Optimizing sorter parameters on the test conditions

Pachitariu et al. swept thresholds for some sorters on a benchmark condition. That can be appropriate for algorithm development but would leak test-condition information into this study. Use pinned defaults or a predeclared calibration set that is separate from all realism-comparison recordings. Never tune separately by realism arm.

### 4.7 Drift-inconsistent injection

Both the SpikeInterface tutorial and Kilosort4 methods warn that stationary injected waveforms in a drifting host are inconsistent. Either select low-drift recordings with a quantitative threshold or apply the same measured motion to every arm and pass a drift-following manipulation check.

### 4.8 Too many injected units

The anchor paper explicitly limits artificial units to avoid changing the underlying recording. Increasing injected-unit count to buy power can itself alter collision and density statistics. Statistical efficiency should come from paired arms and multiple seeds/recordings, not an unbounded number of simultaneous injections.

### 4.9 Mutable upstream resources

The live template CSV and SpikeInterface defaults can change. A result based on “latest” without a metadata hash, code commit, row IDs, and parameter dump will not be reproducible even if the analysis scripts are perfect.

### 4.10 Curation after seeing outcomes

Manual or condition-specific curation can erase or create differential effects. The primary analysis should use all returned units and identical automated rules across arms, as the anchor comparison did. Any curated sensitivity analysis must be secondary and blinded to condition where practical.

---

## 5. Open questions and implications for the Claim Sheet

### 5.1 The transferable question has two parts

1. **Absolute-score validity:** Does a realism axis change measured accuracy, precision, recall, or unit classification enough that published hybrid scores need reinterpretation even when rankings stay stable?
2. **Comparative validity:** Does the sorter-by-realism interaction change the sign, order, or practical separation of sorter comparisons?

The project can find one without the other. Both outcomes must be predeclared.

### 5.2 Recommended axis ladder

**Tier A — region matching.** Lowest engineering burden and directly named by the anchor paper. First perform a host/template availability and covariate-balance audit. Run only if matched and mismatched sets can be constructed without confounding amplitude, SNR, probe geometry, or exact donor dataset.

**Tier B — local population-rate coupling.** Implement by supplying matched spike trains whose time-varying rates follow nearby host activity while mean rate and refractory behavior remain fixed. This directly follows the anchor's proposed remedy and has precedent in the Kilosort4 hybrid simulator. It is cheaper and cleaner than bursting, but addresses only long-timescale firing dynamics.

**Tier C — burst and waveform-history coupling.** Add empirically bounded burst statistics and amplitude attenuation conditional on recent ISI. This is the most mechanistically direct stress test for short-ISI detection and collision handling, but also the easiest to implement unrealistically. It should follow, not precede, a passing generator-only validation.

The tiers should be sequential one-axis experiments, not a single all-realism factorial. A final combined condition is optional and only interpretable after the component effects are understood.

### 5.3 Design commitments worth carrying into Phase 1

- Freeze host recordings, template metadata snapshot, template row IDs, software commits, sorter parameters, seeds, spike identities/times, placement, and amplitude/SNR targets before sorter runs.
- Reuse the same unit/recording/seed blocks across realism arms.
- Predeclare the sorter-by-realism interaction as the primary comparative estimand.
- Report absolute-score effects and interaction effects separately.
- Treat low-SNR, high-rate, bursty, and collision-prone units as predeclared strata, not post-hoc stories.
- Use a generator-only manipulation check as a stop-or-go gate.
- Use a short recording segment and a three-sorter candidate panel for resource feasibility before committing to full runs.
- Measure free RAM and VRAM immediately before every sorter/batch and do not launch when measured headroom is insufficient.
- Distinguish clean negative from inconclusive: a confidence interval wide enough to include a decision-changing interaction is inconclusive, regardless of p-value.

### 5.4 Questions that remain genuinely open

1. Which DANDI 000409 host recordings have enough compatible off-host templates after joint area/amplitude/SNR matching?
2. What is a realistic magnitude for population-rate coupling in each selected host, and what similarity metric will gate it?
3. Which region-specific waveform features should constitute the region manipulation check without reusing the sorters' own decision variables too directly?
4. Can TriDesClous 2, SpyKING CIRCUS 2, or Lupin process the chosen short segment within measured RAM and acceptable runtime on this machine?
5. What raw interaction magnitude would change a reader's sorter choice, and what interval width is required to call a clean negative?
6. Should the burst tier be restricted to a region with strong empirical burst priors (for example CA1), or should it test a cross-region mechanism with different parameterizations?
7. How should donor-template leakage be defined when host recordings and library templates derive from the same DANDI family?

### 5.5 Bottom line for Phase 1

The literature already supplies a positive prior that benchmark realism can change measured sorter behavior: synthetic versus paired error signatures differ, waveform-duration mismatch changes false-positive counts, and sorter families diverge on collision handling. What remains unanswered is the controlled question this project can settle: **when the same real background, injected units, amplitudes, locations, and random seeds are held fixed, does adding a specific missing realism property move absolute scores or the between-sorter interaction enough to change a decision?**

---

## 6. References

Each entry includes what the source establishes and how it changes this project. The same entries are maintained in `agents/Codex/references.md`.

### Buccino et al. 2026 — anchor evaluation pipeline

**Buccino, A. P., Sridhar, A., Feng, D., Svoboda, K., & Siegle, J. H. (2026). Efficient and reproducible pipelines for spike sorting large-scale electrophysiology data. _eLife_, 15, RP110170.** [https://doi.org/10.7554/eLife.110170.3](https://doi.org/10.7554/eLife.110170.3)

Builds the SpikeInterface hybrid evaluation pipeline; injects 10 Poisson units at 15 Hz, uses 1,800 NP1 and 3,000 NP2 ground-truth units, and reports Kilosort4-versus-2.5 effects. Its Limitations section explicitly names population firing dynamics and brain-region matching as missing realism.

*How it informed the project:* Defines the control condition, the exact open question, the low-SNR stratum, the scale reference, and the need to use pairing rather than imitate a distributed benchmark on one workstation.

### Pachitariu et al. 2024 — Kilosort4 and realism-sensitive benchmarks

**Pachitariu, M., Sridhar, S., Pennington, J., & Stringer, C. (2024). Spike sorting with Kilosort4. _Nature Methods_, 21, 914–921.** [https://doi.org/10.1038/s41592-024-02232-7](https://doi.org/10.1038/s41592-024-02232-7)

Benchmarks ten sorters across hybrid and full simulations. The hybrid method modulates ISIs by local population firing rate; the full simulator shuffles empirical ISIs for single units. It also shows that unrealistic waveform duration in a biophysical benchmark generates false positives that decline when waveform timing is corrected.

*How it informed the project:* Establishes prior art for population-rate coupling, clears the ambiguity about “non-stationary waveforms” (drift-dependent waveforms, not burst-dependent amplitude attenuation), and gives direct evidence that simulator realism can change measured errors.

### Magland et al. 2020 — benchmark dependence across ground-truth classes

**Magland, J., Jun, J. J., Lovero, E., Morley, A. J., Hurwitz, C. L., Buccino, A. P., Garcia, S., & Barnett, A. H. (2020). SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters. _eLife_, 9, e55167.** [https://doi.org/10.7554/eLife.55167](https://doi.org/10.7554/eLife.55167)

Aggregates more than 30,000 ground-truth units across many studies and sorter families. Reports no universal winner and a precision-versus-recall signature in synthetic data that differs from paired recordings.

*How it informed the project:* Supports treating benchmark construction as part of the measurement instrument and requires separate precision/recall and heterogeneous-sorter analyses.

### Garcia et al. 2026 — modular, CPU-capable sorter contrasts

**Garcia, S., Halcrow, C., Windolf, C., McKenzie, Z. M., Adkisson-Floro, P., Mayorquin, H. R., Dichter, B., Buccino, A. P., & Yger, P. (2026). Opening the black box: a modular approach to spike sorting. _eLife_ reviewed preprint, RP110588.** [https://doi.org/10.7554/eLife.110588.1](https://doi.org/10.7554/eLife.110588.1) · [official XML](https://cdn.elifesciences.org/preprints/110588/elife-preprint-110588-v1.xml)

Benchmarks components and end-to-end CPU pipelines including SpyKING CIRCUS 2, TriDesClous 2, and Lupin against Kilosort4. The official XML contains both the “key ingredients” and “core features” formulations used in project framing.

*How it informed the project:* Supplies feasible non-Kilosort candidate sorters and clears the quotation-verification debt without relying on a secondary rendering.

### Garcia, Buccino, and Yger 2022 — collision-dependent sorter differences

**Garcia, S., Buccino, A. P., & Yger, P. (2022). How do spike collisions affect spike sorting performance? _eNeuro_, 9(5), ENEURO.0105-22.2022.** [https://doi.org/10.1523/ENEURO.0105-22.2022](https://doi.org/10.1523/ENEURO.0105-22.2022)

Defines collision recall and shows large differences between template-matching and density-based sorter families at short temporal separations.

*How it informed the project:* Makes short-ISI/collision recall a required temporal-axis outcome and justifies a heterogeneous sorter panel.

### Jia et al. 2019 — region-specific multichannel waveforms

**Jia, X., Siegle, J. H., Bennett, C., Gale, S. D., Denman, D. J., Koch, C., & Olsen, S. R. (2019). High-density extracellular probes reveal dendritic backpropagation and facilitate neuron classification. _Journal of Neurophysiology_, 121(5), 1831–1847.** [https://doi.org/10.1152/jn.00680.2018](https://doi.org/10.1152/jn.00680.2018)

Finds distinct spatiotemporal extracellular waveform profiles across cortical and subcortical regions and improved region classification from multichannel features.

*How it informed the project:* Provides empirical warrant that region matching can change sorter-relevant waveform structure rather than only a label.

### Pouzat et al. 2004 — short-ISI amplitude dynamics

**Pouzat, C., Delescluse, M., Viot, P., & Diebolt, J. (2004). Improved spike-sorting by modeling firing statistics and burst-dependent spike amplitude attenuation: a Markov chain Monte Carlo approach. _Journal of Neurophysiology_, 91(6), 2910–2928.** [https://doi.org/10.1152/jn.00227.2003](https://doi.org/10.1152/jn.00227.2003)

Models non-Poisson discharge statistics and event-amplitude decay at short ISIs inside a spike sorter.

*How it informed the project:* Establishes a sorter-relevant mechanism for the burst/history tier and shows why timing-only bursts without waveform coupling would be incomplete.

### Harris et al. 2001 — biological constraints for burst realism

**Harris, K. D., Hirase, H., Leinekugel, X., Henze, D. A., & Buzsáki, G. (2001). Temporal interaction between single spikes and complex spike bursts in hippocampal pyramidal cells. _Neuron_, 32(1), 141–149.** [https://doi.org/10.1016/S0896-6273(01)00447-0](https://doi.org/10.1016/S0896-6273(01)00447-0)

Shows that CA1 burst probability and length depend on recent firing history and correlate with extracellular amplitude.

*How it informed the project:* Supplies biological constraints for a manipulation check and argues against an arbitrary burst generator.

### Wouters, Kloosterman, and Bertrand 2021 — relocation-based hybrid ground truth

**Wouters, J., Kloosterman, F., & Bertrand, A. (2021). SHYBRID: A graphical tool for generating hybrid ground-truth spiking data for evaluating spike sorting performance. _Neuroinformatics_, 19(1), 141–158.** [https://doi.org/10.1007/s12021-020-09474-8](https://doi.org/10.1007/s12021-020-09474-8)

Creates virtual units by moving spikes from an observed single unit to a different location on the probe.

*How it informed the project:* Provides a contrasting hybrid design that preserves observed train structure and clarifies which realism the average-template-plus-generated-train pipeline discards.

### Yger et al. 2018 — paired versus hybrid performance scales

**Yger, P., Spampinato, G. L. B., Esposito, E., et al. (2018). A spike sorting toolbox for up to thousands of electrodes validated with ground truth recordings in vitro and in vivo. _eLife_, 7, e34518.** [https://doi.org/10.7554/eLife.34518](https://doi.org/10.7554/eLife.34518)

Reports paired in-vitro and in-vivo errors and a hybrid comparison of SpyKING CIRCUS with Kilosort, while documenting compute/memory tradeoffs.

*How it informed the project:* Demonstrates that apparent performance depends strongly on ground-truth setting and provides a mechanistically different sorter lineage.

### SpikeInterface official hybrid tutorial and source

**SpikeInterface developers. Benchmark spike sorting with hybrid recordings.** [official tutorial](https://spikeinterface.readthedocs.io/en/latest/how_to/benchmark_with_hybrid_recordings.html) · [current `hybrid_tools.py`](https://github.com/SpikeInterface/spikeinterface/blob/main/src/spikeinterface/generation/hybrid_tools.py) · [comparison module](https://spikeinterface.readthedocs.io/en/stable/modules/comparison.html)

Documents the template metadata, motion-aware injection, default sorter panel, and performance outputs; source exposes current generator defaults and caller-supplied sorting support.

*How it informed the project:* Confirms which axes require only configuration versus new code and defines the comparison outputs and reproducibility parameters that must be frozen.

### SpikeInterface Hybrid Template Library — repository and live metadata

**SpikeInterface developers. `hybrid_template_library`.** MIT. [repository](https://github.com/SpikeInterface/hybrid_template_library) · [live metadata CSV](https://spikeinterface-template-database.s3.amazonaws.com/templates.csv)

Hosts IBL Neuropixels 1.0 and Steinmetz/Ye Neuropixels Ultra templates with area, amplitude, SNR, depth, source dataset, and row identifiers.

*How it informed the project:* The live 2026-08-11 audit establishes broad region feasibility, replaces the stale 601-row tutorial snapshot, and creates a snapshot/hash requirement.

### DANDI 000409 — IBL Brain Wide Map

**International Brain Laboratory et al. IBL — Brain Wide Map. DANDI:000409.** CC-BY-4.0. [https://dandiarchive.org/dandiset/000409/draft](https://dandiarchive.org/dandiset/000409/draft)

Open NWB host-recording collection with 2,048 assets, approximately 49.7 TB, and 139 subjects.

*How it informed the project:* Defines the host-data universe, license/attribution obligation, and need for a small identifier-pinned subset rather than bulk download.

---

*End of Codex's independent Phase 0 Literature Foundation. Phase 0 remains open until the comparison chat converges.*
