# references.md — Claude

**The running source ledger for this project.** Every paper, dataset, documentation page, or tool that informed my work gets an entry here, written when the source is fresh. At Phase 2 this file is reconciled with Codex's into the Technical Report's bibliography.

**Relationship to `Literature Foundation.md`.** The Literature Foundation is a dated Phase 0 artifact and its §6 is frozen as written. **This file is the living ledger** — new sources are added here, and corrections to existing entries are made here. Where the two disagree, this file governs.

**Entry format:** citation · what it covers · *how it informed the work* · verified link or DOI.

**Verification rule:** nothing enters this file from memory. Every entry below was located by live web search and carries a link or DOI that resolved during the session that added it.

---

## Legend

- **[ANCHOR]** — the paper whose stated open question this project exists to test.
- **[VERIFY]** — a specific claim attached to this source that still needs confirming from full text. Tracked in `Literature Foundation.md` §5.4.

---

## Primary literature

**[ANCHOR] Buccino AP, Sridhar A, Feng D, Svoboda K, Siegle JH (2026). Efficient and reproducible pipelines for spike sorting large-scale electrophysiology data.** *eLife* 15:RP110170. [doi:10.7554/eLife.110170.3](https://doi.org/10.7554/eLife.110170.3)
*Added: Session 1 (2026-08-11).*
Nextflow + SpikeInterface + Code Ocean pipelines for large-scale sorting, benchmarked on hybrid recordings: 36 NP1.0 recordings (1,800 GT units) and 60 NP2.0 recordings (3,000 GT units). Hybrid generation used Poisson spike trains at 15 Hz mean, 10 hybrid units per recording across 5 randomised iterations, amplitudes rescaled to a defined range (e.g. 50–200 µV), and DREDge-estimated motion applied by spatial template interpolation. Kilosort4 outperformed Kilosort2.5 with accuracy effect sizes 0.276 (NP1.0) and 0.408 (NP2.0).
*How it informed the work:* Supplies the Limitations text this project tests, the exact generator configuration the control arm must reproduce, and the effect-size scale (0.276 / 0.408) against which "decision-relevant" should be defined in the Claim Sheet's success/failure shapes. Its scale (36–60 recordings, thousands of GT units) also establishes that a single shared desktop cannot match it, pushing the design toward paired comparisons rather than large N.

**Garcia S, Halcrow C, Windolf C, McKenzie ZM, Adkisson-Floro P, Mayorquin HR, Dichter B, Buccino AP, Yger P (2026). Opening the black box: a modular approach to spike sorting.** *eLife* reviewed preprint, 1 April 2026. [doi:10.7554/eLife.110588.1](https://doi.org/10.7554/eLife.110588.1)
*Added: Session 1 (2026-08-11).*
Decomposes spike sorters into five swappable stages (preprocessing, peak detection, feature extraction/clustering, template matching, deconvolution/cleaning), each with a `BenchmarkStudy` object. Ships an empirical simulator: 500 neurons, 384 channels, 30 kHz, gamma-distributed firing rates 0.1–30 Hz, trimodal depth distribution, static and motion-corrected variants. Raises a circularity concern: hybrid data injects spikes using motion-corrected templates, so sorters using the same motion correction gain an unfair advantage. The eLife assessment rates the evidence *incomplete*, citing a biophysical model based on one simulation, insufficiently diverse test datasets, and simplified Gaussian noise without LFP.
*How it informed the work:* Three distinct contributions. (1) The circularity confound argues against a Kilosort-only sorter panel, which would bias this project toward a null. (2) The stage-level decomposition is a live alternative design — measure which *stage* realism moves rather than treating sorters as black boxes. (3) Its critical review shows the standard a realism claim gets held to, which is why anything this project adds to the generator must be justified against measured properties of the real recording.
**[VERIFY]** — the project brief quotes this paper as saying the pipeline *"already has the key ingredients to challenge spike sorting algorithms."* The version reached in Session 1 renders the equivalent claim as "core features needed to properly challenge modern spike sorters." Confirm against the PDF before using the brief's wording as a quotation; the negative-result framing leans on it.

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
**[VERIFY]** — whether the "non-stationary spike waveforms" in its simulator include ISI-dependent amplitude attenuation. If they do, part of this project's "missing" axis already exists inside a comparator's own benchmark, which materially changes the framing. bioRxiv full text was rate-limited in Session 1.

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
**[VERIFY]** — whether SHYBRID transports individual spike snippets or re-renders from an average template. Only the abstract was reachable in Session 1.

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

**SpikeInterface/hybrid_template_library.** License: **MIT** (read at the repository). [github.com/SpikeInterface/hybrid_template_library](https://github.com/SpikeInterface/hybrid_template_library) · browser: [spikeinterface.github.io/hybrid_template_library](https://spikeinterface.github.io/hybrid_template_library/)
*Added: Session 1 (2026-08-11).*
Over 600 templates stored in Zarr format in the `s3://spikeinterface-template-library` bucket on AWS S3. Two source datasets: IBL Brain-Wide Map (Neuropixels 1.0) and Steinmetz & Ye 2022 (Neuropixels Ultra, interpolated to NP2.0 geometry).
*How it informed the work:* The template source for both the matched and mismatched arms. **Open feasibility question:** whether it holds enough templates in the specific regions of the target DANDI 000409 recordings, at comparable amplitude and SNR, to build both arms. The confirmed `brain_area` values skew toward visual cortex. Query the database before committing to the region axis; if matched templates are scarce, redesign the axis rather than weaken it.

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
