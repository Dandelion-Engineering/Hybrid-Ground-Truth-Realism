# references.md — Claude

**The running source ledger for this project.** Every paper, dataset, documentation page, or tool that informed my work gets an entry here, written when the source is fresh. At Phase 2 this file is reconciled with Codex's into the Technical Report's bibliography.

**Relationship to `Literature Foundation.md`.** The Literature Foundation is a dated Phase 0 artifact and its §6 is frozen as written. **This file is the living ledger** — new sources are added here, and corrections to existing entries are made here. Where the two disagree, this file governs.

**Entry format:** citation · what it covers · *how it informed the work* · verified link or DOI.

**Verification rule:** nothing enters this file from memory. Every entry below was located by live web search and carries a link or DOI that resolved during the session that added it.

---

## Legend

- **[ANCHOR]** — the paper whose stated open question this project exists to test.
- **[VERIFY]** — a specific claim attached to this source that still needs confirming from full text. Tracked in `Literature Foundation.md` §5.4.
- **[SUPERSEDED]** — a claim made in Session 1 that later evidence overturned. The corrected statement is given in the same entry. Kept visible rather than deleted, so the trail stays auditable.
- **[CLEARED]** — a former `[VERIFY]` item that has since been confirmed, with who confirmed it and how.

---

## Corrections log

Corrections propagate forward, not backward. `Literature Foundation.md` is a frozen Phase 0 artifact and keeps its original text; this ledger governs where the two disagree.

| Session | Claim corrected | Correction | Raised by |
|---|---|---|---|
| 2 | `hybrid_template_library` holds ~601 templates skewed toward visual cortex | Live first-party CSV holds **7,877 rows** — 2,183 Neuropixels 1.0 across 37 source datasets and 170 area labels. The tutorial's rendered table is a stale snapshot. | Codex Session 1; independently reproduced by Claude Session 2 |
| 2 | The anchor's Cohen's *d* (0.276 / 0.408) can serve as the ranking-flip threshold | It cannot: the two quantities are standardized over different denominators and sampling structures. The *d* values are **contextual calibration** — they establish that sorter-versus-sorter differences here are small-to-moderate. The decision threshold is the paired sorter gap measured **inside this experiment**, in raw accuracy units. | Codex Session 1; accepted by Claude Session 2 |
| 4 | SHYBRID relocation "carries its real spike train and per-spike waveform variability with it" | Overstated, and reasoned from the design idea rather than from the source. The implementation reuses observed spike times after a fixed shift and each spike's **fitted template amplitude**, but assigns **fresh random sub-sample jitter** to the insertion train and does not transport observed waveform shape. | Codex Session 3 from the public implementation; accepted by Claude Session 4 |
| 8 | The 50–200 µV rescaling target "brackets the `good` units" and is "too loud" for the MUA population | Reasoning from an undefined comparison. Donor `amplitude_uv` is the **peak-to-peak of an average waveform**; host `median_spike_amplitude_uV` is a **median over per-spike single-sided peaks**. Measured conversion: ratio median **1.207** on `ibl_quality_score == 1.0` units (p10 1.10, p90 1.51). Restated, the target is roughly **41–165 µV** in host-column terms, population-level only — never unit-level. The direction of the original observation survives; its numbers do not. | Flagged by Claude Session 7, sharpened by Codex Session 7, measured by Claude Session 8 |
| 9 | The derivation's first audit reported 31 hand-authored entries as disagreeing with the derived long names | 30 of the 31 were punctuation, not anatomy: the NWB export strips the commas the canonical Allen names carry, and `to_acronym` already resolves both spellings through `normalise`. An audit that does not use the same key its lookup uses is not auditing the lookup. On the normalised key the count is **44 agree, 0 disagree**. The one surviving finding was `IVn` claiming `PAG`'s long name, now withheld as a collision. | Claude Session 9, caught before the result was reported anywhere |

---

## Primary literature

**[ANCHOR] Buccino AP, Sridhar A, Feng D, Svoboda K, Siegle JH (2026). Efficient and reproducible pipelines for spike sorting large-scale electrophysiology data.** *eLife* 15:RP110170. [doi:10.7554/eLife.110170.3](https://doi.org/10.7554/eLife.110170.3)
*Added: Session 1 (2026-08-11).*
Nextflow + SpikeInterface + Code Ocean pipelines for large-scale sorting, benchmarked on hybrid recordings: 36 NP1.0 recordings (1,800 GT units) and 60 NP2.0 recordings (3,000 GT units). Hybrid generation used Poisson spike trains at 15 Hz mean, 10 hybrid units per recording across 5 randomised iterations, amplitudes rescaled to a defined range (e.g. 50–200 µV), and DREDge-estimated motion applied by spatial template interpolation. Kilosort4 outperformed Kilosort2.5 with accuracy effect sizes 0.276 (NP1.0) and 0.408 (NP2.0).
*How it informed the work:* Supplies the Limitations text this project tests and the exact generator configuration the control arm must reproduce. Its scale (36–60 recordings, thousands of GT units) establishes that a single shared desktop cannot match it, pushing the design toward paired comparisons rather than large N. Its amplitude rescaling range (50–200 µV) is adopted as the amplitude caliper for donor-template selection, and its 10-injected-units-per-recording figure as the minimum template count an arm requires.
**[SUPERSEDED]** — Session 1 proposed using this paper's effect sizes (0.276 NP1.0, 0.408 NP2.0) as the threshold for whether realism could flip a sorter ranking. **It cannot serve that role.** Cohen's *d* here is standardized over this paper's own variance structure and sampling design, and is not commensurable with a raw paired accuracy change measured in a different experiment. **Corrected use:** the *d* values are contextual calibration — they establish that sorter-versus-sorter differences in this domain are small-to-moderate, which tells this project how much precision it needs. The decision threshold is the paired sorter gap measured inside this experiment, in raw accuracy units. Raised by Codex in the Phase 0 comparison chat and accepted in Claude Session 2.

**Garcia S, Halcrow C, Windolf C, McKenzie ZM, Adkisson-Floro P, Mayorquin HR, Dichter B, Buccino AP, Yger P (2026). Opening the black box: a modular approach to spike sorting.** *eLife* reviewed preprint, 1 April 2026. [doi:10.7554/eLife.110588.1](https://doi.org/10.7554/eLife.110588.1)
*Added: Session 1 (2026-08-11).*
Decomposes spike sorters into five swappable stages (preprocessing, peak detection, feature extraction/clustering, template matching, deconvolution/cleaning), each with a `BenchmarkStudy` object. Ships an empirical simulator: 500 neurons, 384 channels, 30 kHz, gamma-distributed firing rates 0.1–30 Hz, trimodal depth distribution, static and motion-corrected variants. Raises a circularity concern: hybrid data injects spikes using motion-corrected templates, so sorters using the same motion correction gain an unfair advantage. The eLife assessment rates the evidence *incomplete*, citing a biophysical model based on one simulation, insufficiently diverse test datasets, and simplified Gaussian noise without LFP.
*How it informed the work:* Four distinct contributions. (1) The circularity confound argues against a Kilosort-only sorter panel, which would bias this project toward a null. (2) The stage-level decomposition is a live alternative design — measure which *stage* realism moves rather than treating sorters as black boxes. (3) Its critical review shows the standard a realism claim gets held to, which is why anything this project adds to the generator must be justified against measured properties of the real recording. (4) **It supplies the candidate non-Kilosort sorters.** Codex established from this paper and the current internal-sorter documentation that SpikeInterface exposes CPU-based **SpyKING CIRCUS 2**, **TriDesClous 2**, and **Lupin**, benchmarked here against Kilosort4: TriDesClous 2 is relatively fast; SpyKING CIRCUS 2 returns more units at the cost of false positives and runtime; Lupin trades runtime for higher simulated accuracy. All are MIT via SpikeInterface, so they carry none of Kilosort4's GPLv3 constraint. Their clustering and template-matching components differ from Kilosort4's, which makes them a more informative contrast than another Kilosort generation — but published runtimes from other hardware are not a feasibility claim for this shared desktop, and a pilot decides.
**[CLEARED]** — the project brief quotes this paper as saying the pipeline *"already has the key ingredients to challenge spike sorting algorithms."* Session 1 could only reach a rendering that gave the equivalent claim as "core features needed to properly challenge modern spike sorters," and flagged the quotation as unconfirmed. **Codex confirmed against the official eLife v1 XML ([elife-preprint-110588-v1.xml](https://cdn.elifesciences.org/preprints/110588/elife-preprint-110588-v1.xml)) that the document contains both formulations.** The brief's wording is a real quotation and is citable. The negative-result framing that leans on it is safe.

**Magland J, Jun JJ, Lovero E, et al. (2020). SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters.** *eLife* 9:e55167. [doi:10.7554/eLife.55167](https://doi.org/10.7554/eLife.55167)
*Added: Session 1 (2026-08-11).*
Ten sorters benchmarked on 650 recordings and ~35,000 ground-truth units from eleven laboratories. Defines the field's standard accuracy metric as n_match / (n_match + n_miss + n_fp), and reports the count of GT units above a threshold (default 0.8) alongside means. Finds no universal winner: MountainSort4 excels at low channel counts, IronClust on simulated and drifting data, Kilosort2 retains accuracy at low SNR.
*How it informed the work:* Supplies the accuracy metric definition and the above-threshold-count reporting convention (a mean hides whether a manipulation moved everything slightly or a few units a lot). Establishes the prior that sorter ranking is already a function of benchmark dataset. Most importantly, its observation that synthetic studies show precision > recall — *"despite the sophistication of many of these simulations, they may not yet be duplicating the firing and noise statistics of real-world electrophysiology recordings"* — is the strongest published empirical evidence that the firing-statistics realism axis is the right one to build.

**Buccino AP, Garcia S, Yger P (2022). Spike sorting: new trends and challenges of the era of high-density probes.** *Progress in Biomedical Engineering* 4(2):022005. [doi:10.1088/2516-1091/ac6b96](https://doi.org/10.1088/2516-1091/ac6b96)
*Added: Session 1 (2026-08-11).*
Review of modern spike sorting: method families, the three ground-truth strategies (paired, hybrid, fully synthetic), quality metrics, curation bias. Reports that across six sorters on one dataset only 33 of ~1,400 units were agreed by all six. Notes paired ground truth typically yields a single unit per dataset and is biased toward large pyramidal cells because those are the neurons that can be patched.
*How it informed the work:* The framing for why hybrid recordings are the strategy the field actually grades on — they are the only route to many ground-truth units on top of genuinely real noise — and therefore why their realism is load-bearing rather than an academic caveat. The 33/1,400 agreement figure calibrates how fragile any single-sorter accuracy claim is.

**Pachitariu M, Sridhar S, Pennington J, Stringer C (2024). Spike sorting with Kilosort4.** *Nature Methods*. [doi:10.1038/s41592-024-02232-7](https://doi.org/10.1038/s41592-024-02232-7) · preprint [doi:10.1101/2023.01.07.523036](https://doi.org/10.1101/2023.01.07.523036)
*Added: Session 1 (2026-08-11).*
Graph-based clustering, plus a simulation framework using densely sampled real electrical fields to generate non-stationary spike waveforms and realistic noise. Reports recovering ~80–90% of simulated units against ~50% for IronClust. Ablation attributes the gains to drift correction, deconvolution, and cross-correlogram-based merges/splits.
*How it informed the work:* Defines the primary sorter under test and its published performance band. Licensed **GPLv3** — call it as an external tool through SpikeInterface, never vendor or link against it.
**[CLEARED]** — whether the "non-stationary spike waveforms" in its simulator include ISI-dependent amplitude attenuation. **Codex resolved this: the non-stationarity is drift-dependent.** Kilosort4's hybrid benchmark *does* modulate exponential inter-spike intervals by the local population firing rate in 100 ms bins and enforces a 2 ms minimum ISI, and its full simulator shuffles empirical ISIs for single units — but there is no evidence of within-burst, history-dependent amplitude attenuation. **Tier C (burst plus waveform-history coupling) is therefore a genuinely missing mechanism, and Tier B (population-rate coupling) is not novel to the field even though it is absent from the SpikeInterface pipeline under test.**
*Second-order consequence, raised by Claude in Session 2 and carried into the Claim Sheet:* because Kilosort4's own benchmark already has population-rate coupling, adding that axis to the SpikeInterface pipeline moves the test data toward Kilosort4's home benchmark. A Kilosort4-favouring Tier B interaction cannot cleanly separate robustness from familiarity, and is predeclared as inconclusive-on-attribution rather than a clean positive. This is the Garcia et al. 2026 motion-correction circularity concern, pointed at a different mechanism.

**Garcia S, Windolf C, Boussard J, Dichter B, Buccino AP, Yger P (2024). A modular implementation to handle and benchmark drift correction for high-density extracellular recordings.** *eNeuro* 11(2):ENEURO.0229-23.2023. [doi:10.1523/ENEURO.0229-23.2023](https://doi.org/10.1523/ENEURO.0229-23.2023)
*Added: Session 1 (2026-08-11).*
MEArec-based benchmarks (10 min, 256 neurons, NP1.0-like 128 channels) across 12 scenarios crossing drift signal (zigzag rigid, zigzag non-rigid, bumps) × depth distribution (uniform, bimodal) × **firing-rate regime (homogeneous vs sine-modulated)**. Motion estimation error < 5 µm for smooth drift. Well-detected units: 165 static → 118 zigzag → 136 non-rigid → 107 bumps, with best-available correction applied; the authors state that even the best drift correction dramatically reduces sorting accuracy.
*How it informed the work:* Two uses. It is the methodological precedent for treating firing-rate non-stationarity as a benchmark variable (their sine-modulated rate condition), which de-risks that axis. And its magnitude — drift costs roughly a third of well-detected units even after correction — sets the scale a realism effect should be reported against, since "realism matters less than the thing you already correct for" is itself a decision-relevant result.

**Garcia S, Buccino AP, Yger P (2022). How do spike collisions affect spike sorting performance?** *eNeuro* 9(5):ENEURO.0105-22.2022. [doi:10.1523/ENEURO.0105-22.2022](https://doi.org/10.1523/ENEURO.0105-22.2022)
*Added: Session 1 (2026-08-11).*
Collisions defined as spikes from two units within a 2 ms lag; "collision recall" computed across 11 bins spanning [−2, +2] ms; template similarity by cosine similarity of flattened multi-channel templates. Template-matching sorters (Kilosort 1/2, SpyKING CIRCUS) resolve collisions substantially better than density-based ones (HerdingSpikes, IronClust), whose cross-correlogram reconstruction errors exceed 50% at small lags. Data: MEArec, 30 min, 20 neurons, 32-channel NeuroNexus layout, firing rates 5–15 Hz, correlation levels 0–20%.
*How it informed the work:* Identifies the concrete mechanism by which a bursting manipulation could move sorter *rankings* rather than only absolute accuracy: bursts produce within-unit near-coincident spikes, and collision handling is precisely where sorter families diverge. This is why the sorter panel should span mechanisms (template-matching vs density-based) rather than versions of one algorithm.

**Wouters J, Kloosterman F, Bertrand A (2021). SHYBRID: a graphical tool for generating hybrid ground-truth spiking data for evaluating spike sorting performance.** *Neuroinformatics* 19(1):141–158. [doi:10.1007/s12021-020-09474-8](https://doi.org/10.1007/s12021-020-09474-8) · PMID 32617751
*Added: Session 1 (2026-08-11).*
Generates hybrid ground truth by *relocating* a real unit's spikes to a different location on the recording probe, producing a virtual unit whose spike times are known by construction.
*How it informed the work:* The design contrast that defines the realism gap this project targets. SpikeInterface's construction is an average template plus Poisson spike times; SHYBRID's is a relocation of an observed unit, which preserves materially more of the observed train and amplitude structure. The existence of both designs means the field has already implicitly disagreed about which structure is worth preserving — which is itself an argument that the question deserves an experiment.
**[SUPERSEDED]** — Session 1 wrote that relocation "carries its real spike train and per-spike waveform variability with it." **That overstates what the implementation does, and it was reasoning from the design idea rather than from the source.** Codex audited the public implementation in Session 3 and established the narrower, supported statement: the relocation worker **reuses the observed spike times after a fixed shift, and reuses each spike's fitted template amplitude**, but it constructs the insertion train **without a jitter vector**, so fresh random sub-sample jitter is assigned by default. It does **not** preserve observed timing jitter, and it does not transport each observed waveform *shape* unchanged. Source: [`hybridizer/threads.py`](https://github.com/jwouters91/shybrid/blob/master/hybridizer/threads.py) and [`hybridizer/spikes.py`](https://github.com/jwouters91/shybrid/blob/master/hybridizer/spikes.py), both confirmed reachable by Claude in Session 4. Accepted by Claude in Session 4 during the Study Guide Pass 1 re-review; Study Guide §3.1 now states the narrow version.
**[VERIFY] — partly resolved, and the remainder is retired as not worth further effort.** The original open question was whether SHYBRID transports individual spike snippets or re-renders from an average template. The source audit above answers the operative half: a fixed template is fit per spike, with per-spike amplitude, so it is **not** a raw-snippet transport. What remains unresolved is only fine detail about the fitting path, which is not load-bearing — SHYBRID is a contrast case in this project, never a method it uses.

**Yger P, Spampinato GLB, Esposito E, Lefebvre B, Deny S, Gardella C, Stimberg M, Jetter F, Zeck G, Picaud S, Duebel J, Marre O (2018). A spike sorting toolbox for up to thousands of electrodes validated with ground truth recordings in vitro and in vivo.** *eLife* 7:e34518. [doi:10.7554/eLife.34518](https://doi.org/10.7554/eLife.34518)
*Added: Session 1 (2026-08-11).*
SpyKING CIRCUS. Real paired ground truth: 4.8% mean error in vitro (n=37 large-waveform neurons) against 2.7% for an optimal classifier; 14.8% mean error in vivo (n=2) against 13.9% optimal. Hybrid datasets at 4,225 electrodes: total error below 5% for spikes well above threshold; 4.4% SpyKING CIRCUS vs 4.2% Kilosort. Hybrid units were made by shuffling the electrode assignment of real extracted templates and injecting them elsewhere "at controlled firing rates." The authors state directly that *"it is not clear if this simulated data reproduce the conditions of actual recordings,"* noting real waveforms vary naturally in amplitude and shape.
*How it informed the work:* Supplies the in-vitro vs in-vivo error gap (4.8% → 14.8%, same sorter) that bounds the headroom a realism effect could plausibly occupy. Also demonstrates that the concern the 2026 anchor paper states was already stated in 2018 — this is a durable open question, not a one-off caveat, which strengthens the case that answering it is a contribution.

**Pouzat C, Delescluse M, Viot P, Diebolt J (2004). Improved spike-sorting by modeling firing statistics and burst-dependent spike amplitude attenuation: a Markov chain Monte Carlo approach.** *Journal of Neurophysiology* 91(6):2910–2928. [doi:10.1152/jn.00227.2003](https://doi.org/10.1152/jn.00227.2003) · PMID 14749321
*Added: Session 1 (2026-08-11).*
A spike sorter that jointly models firing statistics and spike waveform dynamics — explicitly, that "the events amplitude decays for short interspike intervals" — and reports that doing so lets the method cope with neurons firing doublets and generating highly dynamic waveforms.
*How it informed the work:* The mechanistic warrant for the bursting axis. A sorting method built two decades ago around ISI-dependent amplitude decay is prima facie evidence that the property is real, consequential for sorting accuracy, and absent from the hybrid generator the field currently grades with.

**Harris KD, Hirase H, Leinekugel X, Henze DA, Buzsáki G (2001). Temporal interaction between single spikes and complex spike bursts in hippocampal pyramidal cells.** *Neuron* 32(1):141–149. [doi:10.1016/S0896-6273(01)00447-0](https://doi.org/10.1016/S0896-6273(01)00447-0) · PMID 11604145
*Added: Session 1 (2026-08-11).*
CA1 pyramidal cells in behaving rats fire complex-spike bursts of several spikes at ≤6 ms interspike intervals with decreasing extracellular amplitude across the burst. Burst occurrence is most probable at 6–7 Hz discharge frequency. Burst probability is lower and bursts shorter after recent spiking activity than after prolonged (100 ms–1 s) silence. Burst initiation and length correlate with both extracellular spike amplitude and intracellular action-potential rising slope.
*How it informed the work:* The quantitative target the bursting implementation must hit — the ISI scale (≤6 ms), the history dependence (suppression following recent activity), and the coupling between burst structure and amplitude decay. Also the basis for the mandatory manipulation check: injected bursts must demonstrably reproduce these properties before any sorter time is spent, otherwise a null result is a statement about the implementation rather than about the field's method.

**Jia X, Siegle JH, Bennett C, Gale SD, Denman DJ, Koch C, Olsen SR (2019). High-density extracellular probes reveal dendritic backpropagation and facilitate neuron classification.** *Journal of Neurophysiology* 121(5):1831–1847. [doi:10.1152/jn.00680.2018](https://doi.org/10.1152/jn.00680.2018) · PMID 30840526
*Added: Session 1 (2026-08-11).*
Multi-channel extracellular waveforms show distinct spatiotemporal profiles across brain regions, and classification of neurons by brain region improves with multi-channel over single-channel waveforms. Regular-spiking / fast-spiking classes split at 0.4 ms waveform duration; a regular-spiking subclass with unidirectional backpropagating action potentials is identified in visual cortex and in many hippocampal cells.
*How it informed the work:* The empirical warrant for the region-matched-template axis. If waveform spatiotemporal structure is region-specific enough that region can be classified from it, then injecting a visual-cortex template into a recording from a different region is a measurable realism error rather than a cosmetic one.

**Rossant C, Kadir SN, Goodman DFM, Schulman J, Hunter ML, Saleem AB, Grosmark A, Belluscio M, Denfield GH, Ecker AS, Tolias AS, Solomon S, Buzsáki G, Carandini M, Harris KD (2016). Spike sorting for large, dense electrode arrays.** *Nature Neuroscience* 19(4):634–641. [doi:10.1038/nn.4268](https://doi.org/10.1038/nn.4268) · PMID 26974951
*Added: Session 1 (2026-08-11).*
KlustaKwik/phy for dense arrays, validated on data from cortex, hippocampus and thalamus in rat, mouse, macaque and marmoset, with error rates as low as 5%.
*How it informed the work:* The origin point of the hybrid-validation paradigm this project examines, and a cross-region performance band for calibrating expected accuracy.

**Jun JJ, Steinmetz NA, Siegle JH, Denman DJ, Bauza M, Barbarits B, Lee AK, Anastassiou CA, Andrei A, Aydın Ç, et al. (2017). Fully integrated silicon probes for high-density recording of neural activity.** *Nature* 551(7679):232–236. [doi:10.1038/nature24636](https://doi.org/10.1038/nature24636) · PMID 29120427
*Added: Session 3 (2026-08-11).*
The Neuropixels probe: a single integrated silicon shank with hundreds of densely spaced recording sites, yielding well-isolated spiking from hundreds of neurons per probe; more than 700 well-isolated single neurons recorded simultaneously from five brain structures in an awake mouse using two probes.
*How it informed the work:* Cited in Study Guide Pass 1 as the origin of the data regime this project operates in. It is the reason a neuron is heard on several neighbouring sites at once, which is what makes a *multichannel template* — the object this project injects and whose realism Tier A manipulates — meaningful at all. Also the reason the region-matching axis is testable: single-channel waveforms would not carry enough spatial structure for regional differences to be a manipulable property.

**Efron B (1979). Bootstrap methods: another look at the jackknife.** *The Annals of Statistics* 7(1):1–26. [doi:10.1214/aos/1176344552](https://doi.org/10.1214/aos/1176344552)
*Added: Session 3 (2026-08-11).*
Introduces the bootstrap: estimate the sampling distribution of a statistic by resampling the observed data rather than assuming a parametric form, and shows the jackknife to be a linear approximation to it.
*How it informed the work:* The methodological citation for the Claim Sheet's uncertainty machinery (Slot 7) and its plain-language explanation in Study Guide Pass 1. Its relevance here is specifically that it replaces a distributional assumption with computation — which matters because this project's estimand is a difference of paired differences with an estimated threshold (`G0`, `T`, `D`) carried through the same resampling, a quantity with no clean closed-form interval. **The load-bearing choice is not the bootstrap itself but the resampling unit:** randomization blocks, not injected units, because units inside one run share a recording, a noise environment, and a seed. Codex raised this in the Session 2 Claim Sheet review; the hierarchical scheme is the result.

**Buccino AP, Hurwitz CL, Garcia S, Magland J, Siegle JH, Hurwitz R, Hennig MH (2020). SpikeInterface, a unified framework for spike sorting.** *eLife* 9:e61834. [doi:10.7554/eLife.61834](https://doi.org/10.7554/eLife.61834)
*Added: Session 1 (2026-08-11).*
The unified Python API: >30 file formats, ≥10 sorters, preprocessing, postprocessing, curation, comparison, visualization.
*How it informed the work:* Establishes that this project's independent variable (the generator), its measurement instrument (the comparison module), and its sorter interface all live in one package at one pinnable commit — a structural advantage for a controlled study, and the reason a pinned upstream commit is a cheap and strong reproducibility guarantee here.

---

## Tools, documentation, and data resources

**SpikeInterface — Generation module documentation.** [spikeinterface.readthedocs.io/en/stable/modules/generation.html](https://spikeinterface.readthedocs.io/en/stable/modules/generation.html)
*Added: Session 1 (2026-08-11).*
API surface for hybrid and synthetic generation: `generate_hybrid_recording()`, `InjectTemplatesRecording`, `InjectDriftingTemplatesRecording`, `generate_drifting_recording()`, `make_one_displacement_vector()`. Spike-train controls are exposed via `generate_sorting_kwargs`, which accepts `firing_rates` (as a range) and `refractory_period_ms`. No parameter for bursting, ISI-dependent amplitude attenuation, or firing-rate non-stationarity appears in the documented surface; helper functions for injecting "overly synchronous spikes" address cross-unit synchrony, which is a different phenomenon.
*How it informed the work:* Primary evidence for the project's axis ratio — refractoriness already implemented (so not a delta), region matching supported by metadata (so a measurement), bursting and rate non-stationarity absent (so engineering must precede measurement). This is the observation that determines how much of the project is building versus measuring, and the Claim Sheet is required to be honest about that split.

**SpikeInterface — Benchmark spike sorting with hybrid recordings (how-to).** [spikeinterface.readthedocs.io/en/stable/how_to/benchmark_with_hybrid_recordings.html](https://spikeinterface.readthedocs.io/en/stable/how_to/benchmark_with_hybrid_recordings.html)
*Added: Session 1 (2026-08-11).*
The canonical workflow: `fetch_templates_database_info()` → pandas query → `query_templates_from_database()` → `scale_template_to_range()` and/or `relocate_templates()` → `generate_hybrid_recording()` (passing a `motion` object switches from `InjectTemplatesRecording` to `InjectDriftingTemplatesRecording`). Confirms the `templates_info` metadata columns: `brain_area` (70+ areas, e.g. VISa5, VISa6a, VISp5, VISp6a, VISrl6b), `probe`, `probe_manufacturer`, `depth_along_probe`, `amplitude_uv`, `noise_level_uv`, `signal_to_noise_ratio`, `template_index`, `best_channel_index`, `spikes_per_unit`, `dataset`, `dataset_path`.
*How it informed the work:* Confirms the region-matching axis is queryable with no new engineering, and identifies `amplitude_uv` and `signal_to_noise_ratio` as the covariates that must be matched across arms so a realism effect is not an amplitude effect in disguise.

**SpikeInterface/hybrid_template_library.** License: **MIT** (read at the repository). [github.com/SpikeInterface/hybrid_template_library](https://github.com/SpikeInterface/hybrid_template_library) · browser: [spikeinterface.github.io/hybrid_template_library](https://spikeinterface.github.io/hybrid_template_library/) · live metadata: [templates.csv](https://spikeinterface-template-database.s3.amazonaws.com/templates.csv)
*Added: Session 1 (2026-08-11). **Rewritten Session 2 (2026-08-11) — the Session 1 entry was wrong.***

**[SUPERSEDED]** — Session 1 recorded "over 600 templates" with `brain_area` values skewed toward visual cortex, taken from the SpikeInterface tutorial's rendered table. **That table is a stale snapshot and the claim is withdrawn.** Codex audited the live first-party CSV in its Session 1; Claude independently re-downloaded and reproduced it byte-for-byte in Session 2 (identical SHA-256). The correct figures are below. Templates are stored in Zarr in the `s3://spikeinterface-template-library` bucket; the two source collections are IBL Brain-Wide Map (Neuropixels 1.0) and Steinmetz & Ye 2022 (Neuropixels Ultra).

**Live metadata snapshot, verified 2026-08-11 by both agents independently:**

| Property | Value |
|---|---|
| Size / SHA-256 | 2,032,640 bytes · `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d` |
| ETag / Last-Modified | `a5f37c65cd175fa8b75178c5195b20a1` · 2024-09-29 08:56:05 GMT |
| Total rows | 7,877 |
| Neuropixels 1.0 (IBL) | 2,183 rows · 37 source datasets · 170 `brain_area` labels |
| Neuropixels Ultra | 5,694 rows · 57 source datasets |
| IBL `amplitude_uv` | 52.19 – 923.15 (median 184.17) |
| IBL `signal_to_noise_ratio` | 2.43 – 48.44 (median 9.77) |

Columns: `amplitude_uv`, `best_channel_index`, `brain_area`, `dataset`, `dataset_path`, `depth_along_probe`, `noise_level_uv`, `probe`, `probe_manufacturer`, `signal_to_noise_ratio`, `spikes_per_unit`, `template_index`.

*How it informed the work:* The template source for both the matched and mismatched arms of the region axis, and the resource whose adequacy decides whether that axis is runnable at all.

**Claude's Session 2 leave-one-dataset-out audit is the operative feasibility result.** Under a caliper of amplitude 50–200 µV (adopted from the anchor paper's own rescaling range) and SNR 5–15 (Claude's judgement call, and the softer of the two bounds), 1,149 of the 2,183 NP1.0 templates survive across 149 areas, and **37 areas hold ≥10 in-caliper templates** — ten being the anchor's injected-unit count per recording. But dropping each area's single largest contributing source dataset, which is what the donor/host leakage rule implies if the host turns out to be that dataset, leaves **only 7 areas with ≥10: CP (42), PIR (19), SUB (18), VISa5 (17), AId5 (14), MRN (14), ENTl5 (10)**. Thirteen of the 37 collapse to zero, because a single dataset supplied all their templates.

This is a conditional rather than a count: a host recording outside the library's 37 IBL source datasets leaves region selection essentially unconstrained; a host inside them constrains the axis to a 7-area shortlist. **Host selection is therefore downstream of donor availability, not parallel to it.** Both numbers move with the caliper.

Two standing obligations follow. The metadata table is hosted mutably, so any selection must pin its snapshot by hash and record the selected `template_index` rows — though the Last-Modified date shows the table has not actually moved since September 2024, which means the project is not racing a live-updating resource. And because the library's NP1.0 templates come from the same DANDI family as the host recordings, the host's own source dataset must be excluded from donor selection **and** the number of contributing source datasets balanced across arms, or provenance rides along with region as a confound.

Reproduce with `Reproducibility Packet/scripts/audit_template_library.py` (stdlib only); output at `Reproducibility Packet/results/template_audit_2026-08-11.txt`.

**Session 5 (2026-08-11) — what the `dataset` column actually contains, and what that changes.** The Session 2 audit treated `dataset` as an opaque provenance token, counted distinct values, and reported a worst case. Parsing it instead of counting it establishes the following, from the pinned snapshot:

- **Every one of the 2,183 Neuropixels 1.0 rows is a DANDI 000409 session.** The 37 "source datasets" are 37 probe insertions, spanning **24 sessions and 12 subjects** (`KS042, KS043, KS044, KS046, KS051, KS052, KS055, KS084, KS086, KS091, KS094, KS096`). Zero rows failed to parse. There is no second source collection for this probe type; the other 5,694 rows are Neuropixels Ultra, a different geometry.
- **"Exclude the host's source dataset" is therefore three different exclusions** — insertion, session, and subject — and they give different answers. Of the 37 areas holding ≥10 in-caliper templates, the number surviving a *worst-case* exclusion is 7 at insertion level, 6 at session level, and 4 at subject level. Areas drawn from a single animal (`SUB` 57, `ENTl5` 31, `ENTl6a`, `VISpor5`, `VISpor6a`, `ProS`) look healthy at insertion granularity and go to zero at subject granularity.
- **The exclusion can be made vacuous instead of chosen.** DANDI 000409 holds 459 raw ecephys recordings across 139 subjects, and only 12 of those subjects are in the library — so **429 of 459 candidate hosts share no insertion, session, or animal with any donor**, and each area keeps its full pool. The seven-area shortlist that has shaped this project's thinking since Session 2 is an artifact of assuming the host might be a library recording; it does not bind otherwise.
- **[SUPERSEDED by source review in Sessions 5–6]** The first residual-boundary note claimed one rig design, preprocessing chain, and species/strain without auditing each of those properties.
- **The verified residual boundary survives and belongs in the limitations.** Host and donor still share one dandiset, consortium, IBL acquisition program, and Neuropixels 1.0 probe type. Subject-level separation bounds leakage and animal idiosyncrasy; nothing available makes host and donor provenance independent, because this probe type has exactly one donor collection. The donor templates use their own extraction preprocessing, and rig/strain identity has not been established here.
- **CA1 has a hard ceiling of 16 templates**, and no caliper produces more. Twelve sit inside the provisional caliper; the four outside it are all KS044 `781b35fd` at 2,800 µm with amplitudes 213–488 µV and SNR 10–23 — high-quality, not marginal. Since Slot 7 fixes the 50–200 µV figure as a rescaling target rather than a donor requirement, treating them as eligible is contract-compliant. All sixteen come from four subjects and fifteen sit inside one 280 µm depth band.

Reproduce with `Reproducibility Packet/scripts/audit_donor_provenance.py`; output at `Reproducibility Packet/results/donor_provenance_2026-08-11.txt`.

**DANDI 000409 — IBL Brain-Wide Map.** License: **CC-BY-4.0** (read in the dataset's own DANDI metadata). [dandiarchive.org/dandiset/000409](https://dandiarchive.org/dandiset/000409) · metadata verified via the [DANDI API](https://api.dandiarchive.org/api/dandisets/000409/versions/draft/info/)
*Added: Session 1 (2026-08-11).*
2,048 assets, ~49.7 TB total, 139 subjects. Citation string as supplied by DANDI: International Brain Laboratory; Benson, Brandon; Benson, Julius; Birman, Daniel; et al. (2026). *IBL — Brain Wide Map* [Data set]. DANDI Archive. DANDI:000409.
*How it informed the work:* The substrate recording. Note that it is also the source of the template library's NP1.0 templates — convenient for region matching, but worth a Phase 1 discussion, since matching a recording against templates derived from the same dataset family is more realistic *and* edges toward circularity. **CC-BY-4.0 creates a real attribution obligation that belongs in the packet's `DATA.md`, recorded as the packet is built rather than reconstructed at the end. No raw data is redistributed.**
*Session 11 (2026-08-12):* that obligation is now discharged — `Reproducibility Packet/DATA.md` carries the licence, the access path, and **the archive's own 909-character citation string verbatim**, written into the file programmatically from the API response rather than transcribed, because it contains forty-odd author names with non-ASCII characters that hand-copying would corrupt. Use that file, not the abbreviated `et al.` form above, when the Technical Report's bibliography is reconciled at Phase 2.

**Session 5 (2026-08-11) — asset structure, and the anatomical annotation the project needs.** Enumerated through the public REST API and pinned at `Reproducibility Packet/results/dandi_000409_assets.json`:

- 2,048 assets = **918 NWB** + 1,130 MP4 video. The NWB files are **459 raw ecephys** (`_desc-raw_ecephys.nwb`, 18.2–197.3 GB, median 88.1) paired one-to-one with **459 processed** (`_desc-processed_behavior+ecephys.nwb`, ~0.5–1.5 GB), across **139 subjects**. Exactly one raw file per session; a session may hold more than one probe inside that file.
- **Every NWB carries `/general/extracellular_ephys/electrodes` with one Allen CCF *long name* per electrode** (`Field CA1`, `Rostrolateral area layer 5`, `void`), plus `rel_y` (position along probe), `rel_x`, CCF `x/y/z`, `group_name` (probe), and `channel_name`. Raw and processed files for a session carry **identical** electrode tables, verified on `sub-NYU-11/ses-6713a4a7`. The raw file additionally exposes `acquisition/ElectricalSeriesProbe00AP`.
- *How it informed the work:* **this is the pinned channel/trajectory mapping Slot 7 demands, already published** — the project does not have to construct it, and never has to invent a whole-recording region label. It also fixes the host-side vocabulary as long names, which the acronym-based donor library does not share; `utils/ccf_labels.py` is the bridge and `validate_ccf_label_map.py` checks it against the donor library's own (session, depth, acronym) records.
- **The table is readable without downloading the recording.** `utils/remote_hdf5.RemoteFile` gives h5py a block-caching HTTP-range file object, so screening one 18–197 GB candidate costs roughly 5–10 MB and a handful of requests. This is what makes host screening affordable at all on this project's budget.

**h5py 3.16.0** (BSD-3-Clause). [docs.h5py.org](https://docs.h5py.org/) · [github.com/h5py/h5py](https://github.com/h5py/h5py)
*Added: Session 5 (2026-08-11).*
Python interface to HDF5. Accepts any seekable Python file-like object in place of a path, which is the property this project depends on.
*How it informed the work:* The first dependency installed into the project venv, pinned in `requirements.txt` at install time along with its transitive `numpy==2.5.2` (BSD-3-Clause). Used only to read remote NWB metadata for host screening; it does not touch sample data. Its permissive licence raises nothing for a project that intends to publish its own code under MIT.

**Kilosort4.** License: **GPLv3** (read at the repository). [github.com/MouseLand/Kilosort](https://github.com/MouseLand/Kilosort) · docs [kilosort.readthedocs.io](https://kilosort.readthedocs.io/)
*Added: Session 1 (2026-08-11).*
The primary sorter under test. Version confirmed working on this machine during the pre-project feasibility run: Kilosort 4.1.7, SpikeInterface 0.104.8, PyTorch 2.11.0+cu128, CUDA 12.8, GPU capability `sm_120`.
*How it informed the work:* **The licence is the operative fact.** Running Kilosort4 as an external tool via SpikeInterface's sorter interface is ordinary use and imposes nothing on this project's own code. Copying its source into this project's scripts, or linking against it so as to create a derivative work, would oblige this project to be GPLv3. Call it; do not vendor it. If a genuine need to modify it appears, that is a licence question for `director_requests.md` *before* the modification is written. If stage-level visibility into a sorter is needed, use SpikeInterface's MIT-licensed `sortingcomponents` decomposition instead.

**SpikeInterface/hybrid_template_library — `python/upload_ibl_templates.py`, the IBL template builder.** License: **MIT** (the repository's, read Session 1). [upload_ibl_templates.py](https://github.com/SpikeInterface/hybrid_template_library/blob/main/python/upload_ibl_templates.py)
*Added: Session 6 (2026-08-11). Read after Codex's Session 5 review cited it to bound a claim of mine.*
The builder pairs a DANDI 000409 recording (`NwbRecordingExtractor`, `stream_mode="remfile"`) with IBL's own sorting pulled from the ONE database (`IblSortingExtractor(..., good_clusters_only=True)`), and the `brain_area` column of the donor metadata is a property carried on **that sorting**, not derived from the NWB. Templates are extracted **after** a preprocessing chain, quoted from the source: `common_reference(highpass_filter(phase_shift(astype(recording, "float32")), freq_min=1.0))`.
*How it informed the work:* Two things, one defensive and one constructive. **Defensive:** because `brain_area` comes from IBL's sorting metadata and the NWB electrode table is another export of the same IBL anatomical registration, my Session 5 label-map validation (1,401/1) is a strong *internal-consistency* check on the long-name↔acronym bridge and on depth-coordinate compatibility — **not** an independent validation of the atlas registration. Codex made that correction in review and it is right; the artifact now says so. **Constructive:** the donor waveforms already carry `phase_shift` (the Neuropixels ADC sample-shift correction), a 1 Hz high-pass and a common reference. Injecting them into a *raw* host and then applying the project's own preprocessing would apply `phase_shift` twice to the injected spikes and once to the real ones — a systematic difference between injected and real units, present in every arm. Injection must therefore happen into the **preprocessed** host with a chain matched to the donors', which is what the anchor pipeline's own workflow does. Flagged to Codex for Rung 0 to verify against the pinned SpikeInterface version rather than taken as settled.

**DANDI 000409 — the processed files' `/units` table (IBL's own Kilosort 2.5 sorting) and `/general` acquisition metadata.** License: **CC-BY-4.0**, Open Access. [dandiarchive.org/dandiset/000409](https://dandiarchive.org/dandiset/000409)
*Added: Session 7 (2026-08-12).*
Two parts of these files the project had not opened before this session.

**`/general`.** Every raw NWB carries `lab`, `institution`, `protocol`, `source_script`, `session_id`, a `subject` group (`subject_id`, `species`, `sex`, `date_of_birth`, `weight`, `uuid`) and an `ibl_metadata` group (`revision`). It carries **no `genotype`, `strain` or `description` field**, on any of the 21 subjects read.

**`/units`.** The processed file's sorting carries one row per cluster with, among others, `probe_name`, `max_electrode`, `distance_from_probe_tip_um`, `kilosort2_label` (`good` / `mua`), `firing_rate`, `spike_count`, `median_spike_amplitude_uV`, `ibl_quality_score`, `isi_violations_ratio`, `presence_ratio`, and `cumulative_drift_um_per_hour`. The scalar columns are one value per unit and cost nothing to read; the ragged per-spike columns (`spike_times`, `spike_amplitudes_uV`, `spike_distances_from_probe_tip_um`) are the size of the sorting and this project does not touch them.

*How it informed the work:* three things, in `Reproducibility Packet/scripts/audit_subject_provenance.py` and `screen_injection_placement.py`.

1. **Acquisition provenance became measurable.** All 12 donor subjects are `cortexlab`/UCL; all 9 candidate host subjects are `churchlandlab`/CSHL or `angelakilab`/NYU. This is the evidence behind proposed Claim Sheet Amendment 4 — host/donor separation is stronger than the contract claimed, the donor library is single-laboratory, and mouse strain is **unverifiable** rather than shared or different.
2. **The host's own unit density inside an injection zone became measurable**, which is what "overcrowding" in Slot 7 has to be judged against. Ten injected units are +3.7% to +45.5% of the native cluster count across the 13 candidate CA1 bands, or +17% to +1000% of the `good`-labelled count. Also confirmed the Session 5 raw/processed electrode-table equality on all 13 bands rather than the one session it was first checked on.
3. **A negative that matters.** `cumulative_drift_um_per_hour` reaches ~6.5 × 10⁶ on these files, so whatever it accumulates it is not net probe drift at that magnitude. It is **not** used, and drift remains an open gate needing a real measurement. This is recorded so a later session does not rediscover the column and treat its name as its definition.

*Boundary:* the units table is IBL's Kilosort 2.5 output as published, not this project's sorting and not ground truth. Its `median_spike_amplitude_uV` is computed by IBL on IBL's preprocessed data, and whether that convention matches the donor library's `amplitude_uv` column is **unverified** — so the observation that the 50–200 µV rescaling target brackets the `good` units' 51–110 µV medians is a flag for that check, not a validation of the target.

### `hybrid_template_library` — the upstream construction scripts, read at a pinned commit

**What it covers.** The Python that builds and consolidates the donor template database this project draws both Tier A arms from. Repository `SpikeInterface/hybrid_template_library`, **pinned commit `0023db29688842f74698bac40c48a86477ea39e7`** (2024-09-29, head of `main` when read on 2026-08-12 — the library has not moved since 2024). MIT.

**How it informed the project.** It settles what the `amplitude_uv` column in the consolidated metadata actually is, which the Claim Sheet's 50–200 µV rescaling target is stated in and which Session 7 compared against host numbers without knowing:

- `upload_ibl_templates.py:326` — `peak_to_peak = np.ptp(templates_extension_data.templates_array, axis=1)`; `consolidate_datasets.py:104,118` take that at the best channel and name it `amplitude_uv`. So it is the **peak-to-peak range over time of the average waveform**, not a per-spike amplitude.
- `upload_ibl_templates.py:44-59` — the best channel is the argmax of that same peak-to-peak, which is a *different* rule from IBL's `max_electrode`.
- `upload_ibl_templates.py:219-220` — templates are averaged on `common_reference(highpass_filter(..., freq_min=1.0))`, not IBL's preprocessing.
- `upload_ibl_templates.py:71` — only the **last 30 minutes** of each recording.
- `upload_ibl_templates.py:162` — `IblSortingExtractor(..., good_clusters_only=True)`. **The donor library is a good-clusters-only population by construction**, which nothing in the project had recorded.
- `upload_ibl_templates.py:154-156` — the zarr dataset name is `f"{dandiset_id}_{dandi_name}_{sorting_pid}.zarr"`, which is how a `dataset` cell in the snapshot resolves to a session and an IBL probe-insertion id.

*Link:* <https://github.com/SpikeInterface/hybrid_template_library/tree/0023db29688842f74698bac40c48a86477ea39e7>
*Citation:* SpikeInterface contributors. *hybrid_template_library*. GitHub, commit `0023db29`, 2024. MIT licence.

*Boundary:* read as source, not run. Nothing here has been executed, and the claim is about what the code computes, not about whether the templates in the bucket were produced by exactly this revision.

### The amplitude-convention measurement (this project's own result)

**What it covers.** Whether the donor library's `amplitude_uv` and DANDI 000409's `median_spike_amplitude_uV` are commensurate. `Reproducibility Packet/scripts/audit_amplitude_conventions.py` → `results/amplitude_conventions.txt`, on `sub-KS042/ses-07dc4b76`, 43.5 MB of metadata in 42 range requests.

**How it informed the project.** They are **not** the same quantity — a peak-to-peak span of an average versus a median over per-spike single-sided peaks. Evaluating the donor definition on host units via the file's own `waveform_mean` gives a ratio with median **1.207** on `ibl_quality_score == 1.0` units (p10 1.10, p90 1.51) and 1.250 over all units. That supports restating the 50–200 µV target as roughly **41–165 µV** in host-column terms at the population level, and does **not** support converting any single unit. It supersedes the flagged comparison in the entry above: the direction of that observation survives the correction, the numbers it was reached on do not.

*Boundary:* one session, and definitional only. The preprocessing difference between the donor pipeline and IBL's is untouched and unmeasured.

---

### Allen Institute Terms of Use — the licence that closed the ontology path

**What it covers.** The terms governing Allen Institute Content, including the Allen Mouse Brain Common Coordinate Framework structure ontology — the canonical source for a CCF structure-name↔acronym table. Read in full at [https://alleninstitute.org/terms-of-use/](https://alleninstitute.org/terms-of-use/) on 2026-08-12.

**How it informed the project.** It closed the obvious route to completing the CCF label map and forced a better one. The terms permit use, copying, distribution and derivative works "for research or other noncommercial purposes," and state that you "may not redistribute the Content or Improvements for commercial purposes without our written permission." Under *Project Details*' licensing standard that makes the ontology a restrictive input usable only under an explicitly approved, named exception stating the downstream limits — which here would mean shipping part of the Reproducibility Packet under a noncommercial restriction, a director-level decision about what Dandelion may release. **No exception was requested, because the ontology proved unnecessary:** the bridge was derived instead from DANDI 000409 (CC-BY-4.0) and `hybrid_template_library` (MIT). See `agents/Claude/Tier A Host and Injection Zone Selection.md` §12.

*Boundary:* this is a reading of published terms, not legal advice, and it is deliberately the conservative reading. It also does not claim the derived map is free of Allen's *intellectual* contribution — the structure names and acronyms are Allen's vocabulary, and the CCF registration behind IBL's annotations is inherited as given. What it claims is narrower and is the thing that matters for shipping: no Allen file was downloaded, vendored, or copied, and every correspondence in the packet was read off two commercial-use-permitting sources.

*Citation:* Allen Institute for Brain Science. *Terms of Use.* https://alleninstitute.org/terms-of-use/ (accessed 2026-08-12).

---

### `iblatlas` and `brainglobe-atlasapi` — permissive wrappers, checked and declined

**What it covers.** The two obvious permissively licensed packages that redistribute the Allen CCF ontology. `iblatlas`' licence file was read directly at [https://raw.githubusercontent.com/int-brain-lab/iblatlas/main/LICENSE](https://raw.githubusercontent.com/int-brain-lab/iblatlas/main/LICENSE) — "MIT License", "Copyright (c) 2023 International Brain Laboratory". `brainglobe-atlasapi` is BSD-3.

**How it informed the project.** It ruled out the shortcut of treating a permissive wrapper as a fix for a restrictive payload. Both licences are honest about the packages' own code; neither party is the Allen Institute, and a third party's permissive licence over a redistribution is not a grant of rights in the upstream content it redistributes. Importing the ontology through an MIT dependency would have been exactly the "import on the assumption that it will be fine" the standard forbids. Neither package is installed and neither is a project dependency.

*Boundary:* this is a decision about the *ontology data*, not a judgement about either package's code, which is permissively licensed and would be usable on its own terms.

*Citation:* International Brain Laboratory. *iblatlas.* MIT Licence. https://github.com/int-brain-lab/iblatlas — accessed 2026-08-12.

---

### The derived CCF label map (this project's own result)

**What it covers.** Whether the host and donor vocabularies can be bridged without an ontology. `Reproducibility Packet/scripts/derive_ccf_label_map.py` → `results/ccf_label_map_derived.txt` and `scripts/utils/ccf_label_map_derived.json`, over 32 of 37 donor insertions, 146.6 MB of metadata in 150 range requests, no recording data read.

**How it informed the project.** It closed the donor side of the label-map gap and supplied the first independent check of the hand-authored table's long-name spellings. Pairing each donor's `(session, depth, acronym)` with the nearest host electrode's CCF long name yields **138 entries — 94 structures the hand-authored table did not contain** — of which 119 acronyms saw exactly one host name and 23 cleared a two-thirds majority. Audited against `utils/ccf_labels.py`: **44 agree, 0 disagree.** Two entries were withheld because two acronyms claimed one long name (`PAG`/`IVn`, `VISpm6a`/`VISpm5`), which is boundary contamination the evidence cannot adjudicate. The derived layer is opt-in in `to_acronym`, and re-running `validate_ccf_label_map.py` after the change reproduced its tracked report byte for byte.

*Boundary:* coverage is bounded by the donor library. Of 209 distinct host long names on the assigned probes, **143 are mapped and 66 remain unmapped**, and those 66 would need the ontology if the region-unaware arm's placement ever lands in one. The 44 agreements are the only non-circular confirmation claimed: validating the *derived* entries against the evidence they were derived from would agree trivially, and that check was deliberately not run. This also validates the vocabulary bridge, not the atlas registration, which is IBL's and inherited as given.

---

### DANDI 000409's own description of `cumulative_drift_um_per_hour` — the drift column, read rather than inferred

**What it covers.** The `description` attribute the processed IBL NWB units table carries on its drift column, on `sub-KS042/ses-07dc4b76`. It was already captured, unread, in `Reproducibility Packet/results/amplitude_conventions.json` under `descriptions/`; no new download was needed to read it. Verbatim:

> "Sum of absolute depth changes between consecutive spikes, normalized to um/hour. Formula: sum(abs(diff(spike_depths)))/duration*3600. High values indicate either electrode drift or depth estimation noise. Scales with spike count (~0.79 correlation). NOT actual electrode displacement."

**How it informed the project.** Three things, one of them new.

1. **It confirms the project's existing decision not to use the column, and replaces the reason with a better one.** The packet's recorded note reaches the right conclusion by inference — the values reach millions of micrometres per hour, so they cannot be net displacement. IBL says so directly, in their own documentation, in capitals. An inference from an implausible magnitude is now a first-party statement.
2. **It explains the magnitude exactly.** The quantity is the total absolute path length of the per-spike depth estimate, summed over every consecutive spike pair and normalized by duration. Over the millions of spikes in a full recording, an estimate that jitters by a micrometre per spike accumulates metres per hour without the probe having moved at all.
3. **It is confounded with firing rate by construction — ~0.79 with spike count — and this is the new fact.** That makes the column *actively misleading* as a host gate rather than merely uninformative. A drift gate built on it would preferentially reject high-firing-rate units and, by extension, high-rate zones. Firing rate is not a nuisance this experiment can afford to select on: Tier B's whole manipulation is population-rate coupling, and a host chosen partly for being quiet would bias that tier before it started.

**What it constrains for the still-open drift gate.** A usable drift quantity must be **net displacement over time, not accumulated absolute step**, and must not scale with spike count. The description also names the confound any depth-derived measure inherits: electrode movement and depth-estimation noise enter this column identically, so a replacement built from the same `spike_depths` substrate has to state how it separates them, or declare that it does not and carry that as a limitation. This entry rules a measure out and names two properties a replacement needs; it does not provide one.

*Boundary:* one column's attribute on one session, and it is IBL's documentation of their own pipeline rather than a measurement of it. The `~0.79` correlation is their reported figure, not one this project has reproduced, and it should be cited as theirs unless and until it is.

*Citation:* International Brain Laboratory. *Brain Wide Map* (DANDI:000409), processed NWB units table, `cumulative_drift_um_per_hour` column `description` attribute. https://dandiarchive.org/dandiset/000409 (read 2026-08-13).

---

### What a "source dataset" count does and does not constrain (this project's own result)

**What it covers.** The provenance structure of the donor library's `dataset` column, measured rather than assumed. `agents/Claude/tools/source_count_granularity_probe.py` → `agents/Claude/tools/source_count_granularity_probe_2026-08-13.txt`, over the pinned snapshot `a6c86402…`, offline and stdlib-only. Two facts, both verified by assertion rather than by reading the parser:

1. **The `dataset` column *is* the probe-insertion identifier**, and both the session UUID and the subject are parsed out of that same string, so the three provenance granularities are strictly nested. The probe asserts one session and one subject per `dataset` across all 2,183 Neuropixels 1.0 rows and does not raise. **Consequence: fixing which `dataset` values a selected set uses determines that set's session and subject counts.**
2. **The 37 `dataset` values sit in 24 sessions and 12 animals** — independently reproducing the twelve Claim Sheet Amendment 2 point 1 already counts. The complete CA1 donor universe's four sources are four sessions and four animals.

The census over insertion subsets, by size k, of how many carry k distinct animals: 37/37 at k = 1, 608/666 at k = 2, 5,884/7,770 at k = 3, and **37,424 of 66,045 at k = 4** — with **74 of the k = 4 subsets drawing all four sources from a single animal**.

**How it informed the project.** Slot 7 requires the Tier A arms to be balanced on "the number of contributing source datasets," and Amendment 2 point 3 makes that count the floor beneath exact pairwise blocking. Both were written while `dataset` was treated as an opaque provenance token — the Session 2 leave-one-dataset-out audit that produced the 7-area shortlist treated it that way, and so did the matching rule that inherited it. Once the column is read, the token turns out to name the **finest** granularity, not the coarsest. So a control arm can satisfy the floor exactly — four sources against four — while being drawn from one animal and facing a four-animal target arm, which is the imbalance Slot 7's own sentence describes, wearing a matching source count. 43% of the four-source sets available at that stage differ from the target arm in animal count.

This produced the main change in Draft 4 of `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`: the provenance-count equality is tested at all three granularities first (Level A) and falls back to the contract's literal source count (Level B) only where Level A admits no complete assignment at that stage. Because the coarser counts are *determined* by the selected source set, the stronger condition filters the existing enumeration rather than enlarging it — at four sources it removes 28,621 of 66,045 subsets before any assignment is attempted.

*Boundary:* this is a pre-host combinatorial statement about the donor library, not a claim about any eventual candidate pool. Host-specific eligibility can only shrink the 37 sources, and every count above moves with it. It says what the constraint *permits*, not what the matcher will find. No host-specific pool was read, and none exists.

*Citation:* Dandelion Engineering, *Hybrid Ground Truth Realism*, Claude Session 16 (2026-08-13). Provenance-granularity census over the pinned `hybrid_template_library` metadata snapshot, SHA-256 `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`. Library: [github.com/SpikeInterface/hybrid_template_library](https://github.com/SpikeInterface/hybrid_template_library) (MIT).

---

### The converter that fixes what `spike_times` is counted from (accepted second-hand, boundary stated)

**What it covers.** DANDI 000409's own record names `catalystneuro/IBL-to-nwb` as its conversion repository. At pinned commit `54030ac4eb40a74978ac1f6ef6e966278b9d3f34`: the raw converter aligns AP samples with `SpikeSortingLoader.samples2times`; the sorting export carries IBL `spikes.times` through without rescaling or re-anchoring; and the sorting-interface documentation defines that field as **seconds from session start**. Codex located and pinned this in Session 20 and records the exact links in `agents/Codex/references.md`.

**How it informed the project.** It is the entire basis for §16.4's bin grid. Sessions 19 and 20 tried to *infer* the processed spike times' clock from the recorded timing index — first by preferring `t_last_s` over `duration_s`, then by an endpoint-containment test that chose between two hypotheses. Both were wrong, and wrong in the same way: endpoints that need not reach the recording boundaries cannot identify an origin or a scale, and equal bin counts are not evidence of equal clocks because an affine compression can leave `n_bins` untouched while moving spikes across internal boundaries. The converter's own semantics remove the inference: the grid anchors at session zero, its extent is `t_last_s`, and `duration_s = t_last_s - t_first_s` is a span rather than an alternative clock. Asset-level containment survives as a consistency check with no inferential role.

*Boundary, and it is the point of this entry:* **I did not fetch the repository or the documentation myself.** I accepted the reading from Codex's review turn, on the strength of its specificity and its consistency with the recorded timing index, and the entry is recorded at that strength rather than as a source I verified. Repository documentation is in any case not permission to assume a particular asset conforms, which is why §16.8 still requires per-asset provenance and containment before anything is computed.

*Citation:* CatalystNeuro, *IBL-to-nwb*, commit `54030ac4eb40a74978ac1f6ef6e966278b9d3f34`. https://github.com/catalystneuro/IBL-to-nwb — identified as the conversion repository by the DANDI 000409 record, https://dandiarchive.org/dandiset/000409 (via Codex, 2026-08-14).

---

### The candidate set's raw AP timebases are built two different ways (this project's own result)

**What it covers.** An offline re-reading of `Reproducibility Packet/results/host_timing_index.jsonl`, which has been on disk since Session 15 and whose per-series `n_timestamps`, `t_first_s` and `t_last_s` had never been compared against the nominal 30 kHz clock. Compute `(n - 1) / 30000` and the implied sample interval `(t_last_s - t_first_s) / (n - 1)` for each of the twenty-one recorded AP series, and they separate cleanly into two groups:

1. **Exactly nominal — five series, all CSHL Probe00, and all five are pinned candidates (ranks 3, 6, 8, 10, 11).** `t_first_s` is exactly `0.0` and `t_last_s` equals `(n - 1) / 30000` to the last representable bit in float64; the implied interval is nominal to twelve decimal places. These arrays are indistinguishable from `arange(n) / 30000`.
2. **Fitted alignment — the remaining sixteen**, with a non-zero offset (`+1.0` to `+1.3` s on four CSHL Probe01 series, `-2e-5` to `-6.5e-5` s on the NYU series) and a sample interval departing from nominal by up to about `1e-5` relative, which accumulates to between **0.5 and 49 ms** across a full recording. Rank 1 — CSHL047 `b52182e7` Probe01 — is in this group at `+1.138489` s and a rate ratio of `0.9999987`, or `-5.8` ms over its run.

**How it informed the project.** It does **not** contradict the converter provenance in the entry above: an identity alignment is still an alignment, and tens of milliseconds sit far inside a 60 s bin, so no gate parameter moves. What it establishes is a distinction the §16 rule needed and did not have — that the pinned session clock is a property of the *converter* rather than a uniform property of the recorded arrays, and that the exactly-nominal series are precisely the ones on which the containment sanity check has the least to say. That produced Draft 16's requirement that the archive reader report the two containment margins (`earliest_spike - t_first_s` and `t_last_s - latest_spike`) with the verdict rather than the verdict alone, since those margins *are* the resolution of the check. The same re-reading is what surfaced the head partial bin: five candidate series start at exactly zero, seven within `6.4e-5` s of it, and rank 1 at `1.138` s — so rank 1's first bin holds 58.86 s of recording inside a 60 s bin.

*Boundary:* this is a statement about how the timestamp arrays were constructed, inferred from their first, last and count — not from reading the arrays, which were never downloaded. It does not show that any series is misaligned, and it grades no candidate. Nothing here is a drift measurement; no candidate has been read.

*Citation:* Dandelion Engineering, *Hybrid Ground Truth Realism*, Claude Session 21 (2026-08-14). Nominal-clock comparison over the twenty-one AP series recorded in `Reproducibility Packet/results/host_timing_index.jsonl` by `screen_host_timing.py`. Source data: International Brain Laboratory, *Brain Wide Map*, [DANDI:000409](https://dandiarchive.org/dandiset/000409), CC-BY-4.0.

---

### What an NWB timestamp is counted from, in the format's own words

**What it covers.** The NWB format fixes a single root-level instant,
`timestamps_reference_time`, and defines every time value in the file as seconds
relative to it; by default it is the same value as `session_start_time`. PyNWB's
own tutorial states it as "the session start time is the reference time for all
timestamps in the file. For instance, an event with a timestamp of 0 in the file
means the event occurred exactly at the session start time."

**How it informed the project.** It is what makes the raw/processed
reference-time comparison a statement about the *coordinate* rather than about a
label. This project reads its band from the raw asset and its spikes from the
processed one, and Section 16.4's whole clock argument is that the two numbers
live in one coordinate. Under this definition, two assets that declare different
reference instants are declaring that the same stored number denotes two
different moments -- so the comparison is the direct form of the property that
Session 32's converter-version equality was standing in for. It is also what
makes the measured one-hour disagreement (entry below) a clock statement rather
than a cosmetic metadata difference, and what licensed the rule change RC-004
implements: compare the instants, not the version of the library that wrote
them. It is also the source of two properties of that implementation that are
not arbitrary -- the comparison is on instants and not on their text, because
the format constrains the moment rather than its spelling; and a value carrying
no UTC offset is refused rather than assumed local, because a wall-clock reading
without an offset does not denote a moment at all.

*Boundary:* the definition says what the files *declare*. It does not say that
any particular asset's stored arrays honour the declaration, which is why
per-asset provenance and endpoint containment stay in the evidence set and why
reference-time agreement is stated as necessary rather than sufficient.

*Citation:* Neurodata Without Borders, *NWB Format Specification* (`NWBFile`,
`timestamps_reference_time` / `session_start_time`),
[nwb-schema.readthedocs.io](https://nwb-schema.readthedocs.io/en/stable/format_description.html);
quoted wording from PyNWB, *NWB File Basics*,
[pynwb.readthedocs.io/en/stable/tutorials/general/plot_file.html](https://pynwb.readthedocs.io/en/stable/tutorials/general/plot_file.html)
(read 2026-08-16). The assets read here all declare `nwb_version` 2.9.0.

---

### DANDI 000409's two halves are always written by different converter versions, and eight of seventy-one disagree about the session clock (this project's own result)

**What it covers.** A bounded metadata read of both halves of 71 paired sessions
-- the 11 distinct sessions of the pinned Tier A host order, plus a
deterministic 60-session sample of the other 448, drawn by SHA-256 rank on a
pinned seed and excluding the 11 the hypothesis was formed on. Per asset:
`general/source_script` under the archive reader's own request and transfer
budgets, and `/session_start_time`, `/timestamps_reference_time`,
`/general/session_id` and the root `nwb_version` attribute under a second
declared budget. 74,186,752 bytes in 1,132 requests; no payload, no electrode
table, no spike times.

Two results, and they point opposite ways.

1. **The converter-version pair is uniform and uniformly unequal.** Every raw
   asset was written by NeuroConv 0.9.1 (1 of 71) or 0.9.2 (70 of 71); every
   processed asset by 0.9.4. **Version agreement holds on 0 of 71 sessions.**
2. **The declared clock agrees on 63 of 71, and the eight exceptions take
   exactly one value.** `processed - raw` on `timestamps_reference_time` is
   either `+0.0 s` or `+3600.0 s` and nothing else, never the other sign, with
   both halves still labelling the same UTC offset. All eight are NYU subjects
   whose declared local time falls in the US-Eastern daylight window; the two
   NYU sessions at `-05:00` agree, and the five non-NYU sessions at `-04:00`
   agree. `session_start_time` equals `timestamps_reference_time` on all 142
   assets, so the two comparisons never disagree.

**How it informed the project.** Session 32 added a rule requiring the two halves
to name the same converter version, from a reviewer finding, on evidence drawn
from 21 *raw* assets -- no processed asset's `source_script` had ever been read.
The first real candidate command stopped on it at rank 1. This measurement shows
the rule admits **nothing** in this dandiset, so no Tier A host could ever be
pinned while it stands; and that the property it stood in for is directly
readable and behaves differently, separating 63 sound sessions from 8 with a
genuine one-hour clock disagreement that version equality cannot see, because
those 8 carry the same version pair as the other 63. The proposal that follows
from it -- keep per-asset authentication, replace pair-version equality with
pair reference-instant equality, and pause rather than reject a disagreeing
candidate under Section 16.4 -- was put to Codex in
`chats/Claude-Codex/Session Clock Agreement/`, which he independently replayed
and accepted; that chat is **concluded** and the implementation is
`Review Cards/RC-004 Session Reference Time Pair Check.md`, open for his Round 1
at Claude Session 34.

*Boundary, and it is the load-bearing part:* the pattern is **described, not
explained**. A daylight-saving handling difference between the two conversion
passes fits every number, but no mechanism was measured and none is claimed.
Nor does this establish that the eight sessions' stored *arrays* disagree: the
declared instants differ, and whether the numeric spike times were shifted with
them is a separate question that endpoint containment against the raw AP extent
would settle cheaply and that has not been run. Those eight candidates are
paused, not rejected. No host is pinned, no drift value exists, and no candidate
payload was read.

*Citation:* Dandelion Engineering, *Hybrid Ground Truth Realism*, Claude Session
33 (2026-08-16). Conversion-provenance and declared-clock census over 71 paired
sessions of DANDI 000409, by `agents/Claude/tools/probe_conversion_pairs.py`
(SHA-256 `10ad5053a06ba35d32d17540a6511f459e2e6f72cd3fcbe613bbdc9af10873ec`);
recorded in `conversion_pairs_pinned_2026-08-16.txt` /`.json` and
`conversion_pairs_sample60_2026-08-16.txt` /`.json` beside it. Source data:
International Brain Laboratory, *Brain Wide Map*,
[DANDI:000409](https://dandiarchive.org/dandiset/000409), CC-BY-4.0.

### ISO 8601's basic and extended formats, and why the timestamp gate is a grammar

*What it covers.* ISO 8601 defines two written forms for the same instant: a
**basic** format without punctuation (`20260225T143000`) and an **extended**
format with it (`2026-02-25T14:30:00`). For a combined date-and-time
representation the standard's rule, as summarised in the Wikipedia article's
*Combined date and time representations* section, is: **"Either basic or
extended formats may be used, but both date and time must use the same
format."**

*How it informed the project.* Codex's RC-004 Round-1 finding F1 showed that
`datetime.fromisoformat` accepts any single character where ISO-8601 puts the
`T`, so `2021-05-10Q14:33:49.023776-04:00` parsed, carried a UTC offset, agreed
with the identical value on the other half of the recording, and reached a drift
verdict. The repair is `REFERENCE_TIME_FORM` in
`Reproducibility Packet/scripts/utils/archive_units.py`: the whole value must
match an ISO-8601 **extended** date-time before the parser sees it, and the
parser then validates the values inside that shape. The quoted rule is what
licenses refusing the mixed spelling `2021-05-10T14:33:49-0400`.

*Boundary, and it is why this entry exists rather than a bare assertion in a
comment.* **The quoted sentence is about the date and time halves. It does not
mention the UTC offset.** Extending it to the offset is this project's reading,
not a clause anyone has quoted to us, and both the code comment and the Review
Card label it that way. The independent support is that **no** value among the
142 assets measured across 71 sessions of DANDI 000409 spells its offset in the
basic form — all 79 distinct values use `±hh:mm` — so the reading refuses
nothing this dandiset contains, and a value it did refuse would surface as a
*paused* input error rather than as a drift verdict either way. **This entry is
a secondary source.** The standard itself is paywalled and has not been read;
if a claim in a public artifact ever has to rest on the offset half of this
rule, the primary text must be obtained first.

*A second, separate boundary.* The permissiveness of `fromisoformat` is recorded
here as **measured on the pinned interpreter, CPython 3.12.10**, by executing it
against the counterexample. No claim is made about which Python release
introduced the behaviour; the code comment says the same.

*Link:* [ISO 8601 — Wikipedia](https://en.wikipedia.org/wiki/ISO_8601),
*Combined date and time representations*; the standard itself is
ISO 8601-1:2019, [iso.org/iso-8601-date-and-time-format.html](https://www.iso.org/iso-8601-date-and-time-format.html)
(paywalled, not read).

*Citation:* International Organization for Standardization, *ISO 8601-1:2019,
Date and time — Representations for information interchange — Part 1: Basic
rules*. Accessed here only through the Wikipedia summary above, 2026-08-16,
Claude Session 35.

---

---

### The anchor pipeline's own preprocessing chain, read this session

**What it covers.** The four transformations the anchor pipeline applies before
sorting, read from the *eLife* 110170 article page on 2026-08-18: a phase-shift
correction for the multiplexed converters; a high-pass filter, "by default, a
high-pass filter with a cutoff frequency of 300 Hz is applied to preserve
high-frequency information in spike waveforms"; a denoising step that masks
noisy or dead channels and then applies either a common median reference or a
spatial high-pass, where "by default, CMR is used, since destriping can create
artifacts in spike waveforms"; and DREDge motion estimation, estimated but not
applied by default. The same page restates the hybrid generation this project
already had on the record — ten units, Poisson, 15 Hz mean rate, rescaled to a
user-defined range with 50–200 µV as the example.

**How it informed the work.** §19.3 of the Tier A selection document pins the
noise gate's preprocessing chain *to this chain*, minus the two steps it cannot
honestly reproduce, rather than inventing a chain of its own. The 300 Hz cutoff
and the global median reference are taken from here; the phase-shift omission
and the bad-channel-masking omission are declared against it, each with the
direction of its effect stated. Without this the gate would have been measuring
a signal nobody else measures.

*Boundary.* Read from the article page, not from the pipeline source. What the
implementation does at a given commit is a separate question this entry does not
answer, and §19.3 does not claim its chain equals the pipeline's — only that its
steps are the pipeline's steps.

*Link:* [elifesciences.org/articles/110170](https://elifesciences.org/articles/110170)

*Citation:* as the `[ANCHOR]` entry above. Read again for this purpose on
2026-08-18, Claude Session 43.

---

### SpikeForest's SNR definition, and the two thresholds it states

**What it covers.** Read from the *eLife* 55167 article page on 2026-08-18. The
paper defines SNR as "the ratio between the peak absolute amplitude of this
average spike waveform and the estimated noise on the channel where this peak
amplitude occurs," with noise estimated as the median absolute deviation divided
by 0.6745. It includes ground-truth units in its headline accuracy averages only
above an adjustable threshold "here set to 8," and reports a secondary analysis
over units with SNR ≥ 5. It also states that the accuracy/SNR relationship is
**sorter-dependent** — for IronClust "the SNR and log ISI-vr are predictive of
accuracy," while for KiloSort2 and MountainSort4 firing rate is the only
predictive metric, and KiloSort2 "can retain high accuracy down to lower SNR
than other sorters, but not for all such low-SNR units."

**How it informed the work.** Three separate things in §19. First, the scale
estimator: the MAD-over-0.6745 convention is this source's, not this project's,
and §19.3 pins the exact normal quantile `0.6744897501960817` while naming the
`1.5e-5` relative difference from the paper's rounded figure. Second, both rungs
of the level-tolerance ladder: `A_min/5 = 10.0 µV` strict and `A_max/8 =
25.0 µV` relaxed use **5 and 8, this source's own two numbers**, applied to the
two ends of the pinned amplitude range, so no multiplier in the derivation is
this project's. An earlier draft of §19 used a four-sigma detection scale that
this session could not verify from a primary source; it was replaced rather than
kept and labelled. Third, the *absence* of a saturation number: the
sorter-dependence finding is precisely why no published figure pins where
accuracy saturates, which is why §19.6's `snr_p2p = 40` ceiling is declared as
judgement and §19.10 says so.

**The convention boundary this source creates, and how §19 handles it.** Its SNR
is a **single-sided peak** over the noise estimate. This project's injection
target is a **peak-to-peak** span (§11.1). The extremum is at most the
peak-to-peak span with no fixed ratio, so applying its thresholds to a
peak-to-peak quantity is the *weaker* requirement, and §19.6 therefore states
every bound as a necessary and not a sufficient condition. **No conversion
between the two conventions is performed anywhere**, which is the §11.2 rule
applied to a new pair of quantities.

*Link:* [elifesciences.org/articles/55167](https://elifesciences.org/articles/55167)

*Citation:* as the Magland et al. entry above. Read for this purpose on
2026-08-18, Claude Session 43.

---

### SpikeInterface's `snr` quality metric — the amplitude convention, from the documentation

**What it covers.** The stable documentation page for the `snr` quality metric,
read 2026-08-18. `SNR = A_µs / σ_b`, where the amplitude is "the amplitude of
the largest peak (positive or negative) of the median waveform on the best
channel" and the noise is "the median absolute deviation of the signal on the
best channel, which is a robust estimator of the standard deviation of the
noise," at the normal scale factor. The page attributes the metric to Lemon and
Jackson and the implementation to the AllenSDK.

**How it informed the work.** It is the second, independent confirmation that
the field's SNR is a **single-sided extremum** over a MAD-derived σ, which is
what makes §19.6's refusal to convert conventions a rule rather than a
precaution. One source stating a convention is a convention; two sources
stating the same one is the convention the reader will assume, which is exactly
why a peak-to-peak quantity carrying the same word would be a §11.1-family
error.

*Boundary.* Documentation for the current stable release, not the pinned version
this project will eventually install. The convention is stable across releases
as far as this page shows; the exact scale constant should be re-read against the
installed version when the stack goes in.

*Link:* [spikeinterface.readthedocs.io/en/stable/modules/metrics/qualitymetrics/snr.html](https://spikeinterface.readthedocs.io/en/stable/modules/metrics/qualitymetrics/snr.html)

*Citation:* SpikeInterface developers, *Signal-to-noise ratio (snr)*,
SpikeInterface documentation, stable release. Accessed 2026-08-18, Claude
Session 43. The framework paper is the Buccino et al. 2020 entry above.

---

### Neuropixels 1.0's AP-band noise and converter resolution, read this session

**What it covers.** Read from the PubMed Central copy of Jun et al. 2017 on
2026-08-18: AP-band input-referred noise of **5.1 ± 0.6 µV RMS** for the
switchable configuration and **5.7 ± 0.8 µV RMS** for the passive one; the AP
band defined as 0.3–10 kHz; selectable gain from 50× to 2500×; and **10-bit
analog-to-digital converters**, chosen "to minimize base area and power
consumption."

**How it informed the work.** Two things in §19, both structural. First, the
converter resolution explains the `conversion` attribute this project measured
independently on the raw asset — **2.34375 µV per stored bit** — and the two
together make the quantization argument in §19.2: a MAD estimate computed on the
stored integers would be granular to about **1.74 µV** on a quantity whose whole
plausible range is roughly 5 to 15 µV, which is why §19.3 takes the estimate
*after* the pinned chain and not before it. Without the published noise figure,
"two to three bits" would have been a guess rather than a number. Second, the
5.1–5.7 µV figures are what let §19.6 state that its declared lower bound of
1.25 µV is not expected to bind, and say so with a source rather than an
intuition.

*Boundary.* These are the probe paper's own characterization figures, measured
under its conditions, and they are not a prediction of what an in-vivo IBL
recording will report after this project's declared preprocessing. §19 uses them
for scale and for the quantization argument, and gates on neither.

*Link:* [pmc.ncbi.nlm.nih.gov/articles/PMC5955206/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5955206/)

*Citation:* as the Jun et al. 2017 entry above. Read for this purpose on
2026-08-18, Claude Session 43.

---

### The raw AP stream's storage layout (this project's own result)

**What it covers.** `agents/Claude/tools/probe_raw_ap_layout.py` reads one raw
AP `ElectricalSeries` object header and its scaling attributes and never slices
the sample array. On rank 1's raw asset `d54fbf42-bb56-462c-b63a-36b9911753ec`,
series `ElectricalSeriesProbe01AP`: 130,188,000 samples × 384 channels, `int16`,
**gzip level 4**, chunk shape **13,020 × 384**, logical 99,984,384,000 bytes,
stored 53,163,508,785 bytes, `conversion` 2.34375e-06, `offset` 0.0, unit
`volts`, and **no `channel_conversion` table**. The run cost 192 range requests
and 12,582,912 bytes. Recorded at
`agents/Claude/tools/raw_ap_layout_CSHL047_Probe01_2026-08-18.{txt,json}`.

**How it informed the work.** It decided three things in §19 that would
otherwise have been assumptions. The chunk spans **every** channel, so reading
the 72-channel injection band costs exactly what reading all 384 costs — which
is why the common median reference is computed over the whole probe, at no
transfer cost, and why that choice needed noting rather than defending. Time is
addressable only at 0.434 s, so the sampling window is one chunk rather than a
duration someone preferred. And the compression ratio, 0.53172, is what turns
`K = 60` windows into the §19.9 transfer projection of 319,010,455 bytes — a
**projection from a whole-file average**, explicitly not a measurement of any
chunk, since no chunk of this dataset has been transferred.

*Boundary.* One asset. Chunk shape, compression, `conversion` and the absence of
`channel_conversion` are properties of rank 1's raw file, not of DANDI 000409,
and §19.6 makes each of them a required confirmation on any other candidate
rather than an inherited fact.

*Link:* the asset is addressed through the tracked listing
`Reproducibility Packet/results/dandi_000409_assets.json`; the dataset is
[DANDI 000409](https://dandiarchive.org/dandiset/000409), CC-BY-4.0.

*Citation:* this project's own measurement, Claude Session 43, 2026-08-18.


### SpikeInterface — `FilterRecording` and `highpass_filter`, read as source rather than as documentation

*What it covers.* The implementation of the preprocessing step the anchor
pipeline uses by default. `FilterRecording.__init__` defaults to
`filter_order=5`, `ftype="butter"`, `filter_mode="sos"` and
`direction="forward-backward"`, and that direction resolves to
`scipy.signal.sosfiltfilt` — so the filter is **zero phase**, not causal, and
the docstring says so in terms ("resulting in zero-phase filtering. Note this
doubles the effective filter order"). `highpass_filter` defaults
`margin_ms="auto"`, which resolves through `adjust_margin_ms_for_highpass` to
`5 × (1000 / freq_min)` milliseconds — **16.667 ms at a 300 Hz corner, exactly
500 samples at 30 kHz.** The margin is taken from real neighbouring samples and
stripped after filtering.

*How it informed the project.* It settled RC-007 finding F4 and changed §19.3's
pinned chain. Draft 29 contrasted its own rectangular DFT high-pass against "a
causal recursive filter with a 300 Hz corner" — a filter the anchor does not
use — and justified a 150-sample edge discard on a locality claim that is false
for the DFT operator. Reading the source made the better repair available:
adopt the anchor's operator and the anchor's own margin rule, which removes the
deviation entirely rather than hedging it. **Neither the filter design nor the
margin width is now this project's choice**, which is the same posture §19.6
takes toward the two SpikeForest multipliers.

*Boundary.* This is `main` at the time of reading, not a pinned release, and
`highpass_filter`'s margin default has changed at least once — the signature
still carries a `_skip_margin_warning_for_old_version` argument. §19.3
therefore pins its own margin **by value** (500 samples) and its own
`padlen` **by value** (18), rather than by reference to whatever a future
SpikeInterface or scipy resolves them to.

*Link:*
[`src/spikeinterface/preprocessing/filter.py`](https://github.com/SpikeInterface/spikeinterface/blob/main/src/spikeinterface/preprocessing/filter.py)

*Citation:* SpikeInterface contributors, `spikeinterface.preprocessing.filter`,
SpikeInterface, MIT licence. Source read 2026-08-18.

---

### This project's own measurement — the two filter constructions compared, Session 44

*What it covers.* `agents/Claude/tools/probe_filter_chain.py` and its records
`filter_chain_2026-08-18.txt` / `.json`. Three measurements on synthetic data,
no archive access: the rectangular DFT high-pass's impulse response at the
centre of a 13,020-sample window is exactly `−1/13020`, reproducing the
reviewer's figure to the last bit; the fifth-order Butterworth's slowest pole
sits at radius `0.980781307`, a time constant of **51.531 samples (1.718 ms)**,
so a 500-sample margin is 9.703 time constants; and, comparing one window
filtered in isolation against that same window filtered inside nine chunks of
continuous signal, the brick wall's scale estimate is off by **+1.14% and does
not improve with a wider margin**, while the Butterworth at a 500-sample margin
is off by **+1e-06**.

*How it informed the project.* It is the evidence behind §19.3's replacement of
the filter and behind the claim that the surviving margin deviation is bounded
rather than merely small. The middle result is the one that decided the design:
a global operator's error cannot be reduced by discarding more edge, which is
what makes the locality claim structural rather than a matter of picking a
bigger number.

*Boundary.* Synthetic signals from one pinned seed, twelve realizations, worst
case reported. It bounds the *isolation* deviation and nothing else; it says
nothing about the two remaining deviations, and it is not a measurement of any
candidate recording.

*Citation:* this project's own measurement, Claude Session 44, 2026-08-18.

---

## Pending — sources identified but not yet verified

These are named in `Literature Foundation.md` §5.4 and are **not** citable until an entry appears above.

- **Quirk & Wilson** — activity-dependent extracellular spike amplitude attenuation in rat hippocampal pyramidal cells, most dramatic during high-frequency bursts. Located at PMC6762418; full citation not yet confirmed.
- **Regional waveform-duration figures** (lateral posterior thalamus ~0.73 ± 0.12 ms with the smallest peak-to-trough ratio; superior colliculus ~0.33 ± 0.12 ms; cerebellum ~0.24 ± 0.07 ms) and the cortical-vs-thalamic burst-fraction comparison. Surfaced in search summaries within this literature; the exact source must be pinned before these numbers are used anywhere citable.
- **Steinmetz & Ye 2022** — Neuropixels Ultra templates, the second source dataset in `hybrid_template_library`. Cited by the library; the paper itself has not been read.
- **MEArec** (Buccino & Einevoll, *Neuroinformatics* 2021, [doi:10.1007/s12021-020-09467-7](https://doi.org/10.1007/s12021-020-09467-7)) — the fully synthetic simulator used by the drift and collision benchmarks. Listed here because those two benchmarks' numbers depend on it; read it only if this project ends up needing a fully synthetic arm.
