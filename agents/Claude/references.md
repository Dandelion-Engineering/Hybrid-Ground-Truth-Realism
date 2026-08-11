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
*How it informed the work:* The design contrast that defines the realism gap this project targets. Relocating a real unit carries its real spike train and per-spike waveform variability with it; SpikeInterface's average-template-plus-Poisson approach does not. The existence of both designs means the field has already implicitly disagreed about whether this realism matters.
**[VERIFY]** — whether SHYBRID transports individual spike snippets or re-renders from an average template. Only the abstract was reachable in Session 1. **Still open after Session 2:** Codex independently confirmed from the abstract that a real unit's spikes are relocated, but could not resolve the snippet-versus-average-template question from primary full text either. Both agents have it quarantined. It is not load-bearing for the design — SHYBRID is a contrast case, not a method this project uses — so it stays open rather than blocking anything.

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

**DANDI 000409 — IBL Brain-Wide Map.** License: **CC-BY-4.0** (read in the dataset's own DANDI metadata). [dandiarchive.org/dandiset/000409](https://dandiarchive.org/dandiset/000409) · metadata verified via the [DANDI API](https://api.dandiarchive.org/api/dandisets/000409/versions/draft/info/)
*Added: Session 1 (2026-08-11).*
2,048 assets, ~49.7 TB total, 139 subjects. Citation string as supplied by DANDI: International Brain Laboratory; Benson, Brandon; Benson, Julius; Birman, Daniel; et al. (2026). *IBL — Brain Wide Map* [Data set]. DANDI Archive. DANDI:000409.
*How it informed the work:* The substrate recording. Note that it is also the source of the template library's NP1.0 templates — convenient for region matching, but worth a Phase 1 discussion, since matching a recording against templates derived from the same dataset family is more realistic *and* edges toward circularity. **CC-BY-4.0 creates a real attribution obligation that belongs in the packet's `DATA.md`, recorded as the packet is built rather than reconstructed at the end. No raw data is redistributed.**

**Kilosort4.** License: **GPLv3** (read at the repository). [github.com/MouseLand/Kilosort](https://github.com/MouseLand/Kilosort) · docs [kilosort.readthedocs.io](https://kilosort.readthedocs.io/)
*Added: Session 1 (2026-08-11).*
The primary sorter under test. Version confirmed working on this machine during the pre-project feasibility run: Kilosort 4.1.7, SpikeInterface 0.104.8, PyTorch 2.11.0+cu128, CUDA 12.8, GPU capability `sm_120`.
*How it informed the work:* **The licence is the operative fact.** Running Kilosort4 as an external tool via SpikeInterface's sorter interface is ordinary use and imposes nothing on this project's own code. Copying its source into this project's scripts, or linking against it so as to create a derivative work, would oblige this project to be GPLv3. Call it; do not vendor it. If a genuine need to modify it appears, that is a licence question for `director_requests.md` *before* the modification is written. If stage-level visibility into a sorter is needed, use SpikeInterface's MIT-licensed `sortingcomponents` decomposition instead.

---

## Pending — sources identified but not yet verified

These are named in `Literature Foundation.md` §5.4 and are **not** citable until an entry appears above.

- **Quirk & Wilson** — activity-dependent extracellular spike amplitude attenuation in rat hippocampal pyramidal cells, most dramatic during high-frequency bursts. Located at PMC6762418; full citation not yet confirmed.
- **Regional waveform-duration figures** (lateral posterior thalamus ~0.73 ± 0.12 ms with the smallest peak-to-trough ratio; superior colliculus ~0.33 ± 0.12 ms; cerebellum ~0.24 ± 0.07 ms) and the cortical-vs-thalamic burst-fraction comparison. Surfaced in search summaries within this literature; the exact source must be pinned before these numbers are used anywhere citable.
- **Steinmetz & Ye 2022** — Neuropixels Ultra templates, the second source dataset in `hybrid_template_library`. Cited by the library; the paper itself has not been read.
- **MEArec** (Buccino & Einevoll, *Neuroinformatics* 2021, [doi:10.1007/s12021-020-09467-7](https://doi.org/10.1007/s12021-020-09467-7)) — the fully synthetic simulator used by the drift and collision benchmarks. Listed here because those two benchmarks' numbers depend on it; read it only if this project ends up needing a fully synthetic arm.
