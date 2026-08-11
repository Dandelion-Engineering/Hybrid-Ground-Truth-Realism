# Literature Foundation — Claude

**Phase 0 field survey for *Does the realism of hybrid ground truth change measured spike-sorting accuracy?***

**Written:** 2026-08-11 (Claude Session 1)
**Status:** Complete as a first pass. Independent of Codex's foundation by design — divergence between the two readings is information, and the comparison happens in chat before Phase 0 closes.

**Sourcing discipline.** Every source below was located through a live web search in this session and carries a working link or DOI. Nothing is cited from training memory. Where I could reach only an abstract or a publisher landing page rather than full text, I say so at the point of the claim and mark what still needs verifying — those are flagged **[VERIFY]** and collected in §5.4.

---

## 1. Domain and methods landscape

### 1.1 The problem the field is actually solving

An extracellular probe records voltage; a neuron is not a channel. Spike sorting is the inverse problem of assigning each detected extracellular spike to the neuron that emitted it. With Neuropixels-class probes (hundreds of closely spaced sites, 30 kHz, hours-long sessions), this is a large-scale, high-throughput inference problem rather than the tetrode clustering exercise it was twenty years ago (Buccino, Garcia & Yger 2022).

The methods landscape has converged on a small number of families:

| Family | Mechanism | Representatives | Trade-off |
|---|---|---|---|
| **Density/clustering-based** | Detect peaks, extract features, cluster in feature space | MountainSort4/5, IronClust, HerdingSpikes2 | Fast and interpretable; degrades on overlapping (colliding) spikes |
| **Template-matching / deconvolution** | Learn templates, then greedily explain the raw trace as a sum of shifted templates | Kilosort 1–4, SpyKING CIRCUS, Circus-OMP, Wobble | Resolves collisions well; more parameters, more opaque |
| **Hybrid pipelines** | Cluster to get templates, then deconvolve | Kilosort family, most modern sorters | The de facto standard shape |

Garcia, Buccino & Yger (2022) measured the split that matters here directly: template-matching sorters (Kilosort 1/2, SpyKING CIRCUS) resolve synchronous spikes substantially better than density-based ones (HerdingSpikes, IronClust), with cross-correlogram reconstruction errors exceeding 50% at small lags for the density-based methods. **That is a mechanism-dependent sensitivity to a property of the spike trains, not of the waveforms** — which is exactly the kind of thing the realism axes in this project could move differentially across sorters.

The current state of the art is Kilosort4 (Pachitariu, Sridhar, Pennington & Stringer 2024), which added graph-based clustering and reports finding ~80–90% of simulated units against ~50% for IronClust. Its ablation study attributes the gains to drift correction, deconvolution, and cross-correlogram-based merges/splits.

### 1.2 The infrastructure layer

SpikeInterface (Buccino et al. 2020) is the unifying API: >30 file formats, ≥10 sorters, preprocessing, postprocessing, curation, comparison. It matters to this project for three reasons: it *is* the framework the anchor paper's pipeline is built on; its `generation` module *is* the standard hybrid generator; and its `comparison` module *is* how accuracy gets measured. Practically, this project's independent variable, dependent variable, and measurement instrument all live in one package at one pinnable commit — which is unusually good for a controlled study.

The companion paper (Garcia et al. 2026, *Opening the black box*) decomposes sorters into five swappable stages — preprocessing, peak detection, feature extraction and clustering, template matching, and deconvolution/cleaning — each with its own `BenchmarkStudy` object. **This is a live alternative design for how to answer this project's question**: rather than treating sorters as black boxes and measuring whether realism moves the ranking, one could measure which *stage* realism moves. Worth noting in Phase 1 as an option, not as the default.

### 1.3 The three ground-truth strategies

Buccino, Garcia & Yger (2022) name the three, and the trade-offs are the whole reason this project exists:

1. **Paired recordings** (juxtacellular or patch simultaneous with extracellular). Unimpeachable truth for the paired neuron. Fatal limitation, stated plainly in that review: *"In most cases only a single ground-truth neuron is available for each dataset."* Also biased — the neurons you can successfully patch are the big ones, so interneurons are undersampled.
2. **Hybrid recordings.** Real recording plus synthetic units injected at known times. Full realism of the *background*, arbitrary numbers of ground-truth units, but the injected units are only as realistic as the generator. Stated limitation: only a limited number of units can be injected before overcrowding compromises sorter performance.
3. **Fully synthetic** (MEArec, the *black box* simulator, Kilosort4's simulator). Total control and unlimited units; every property of the data is a modelling assumption.

**Hybrid is the strategy the field actually grades on**, because it is the only one that gives many ground-truth units on top of genuinely real noise. That is what makes the anchor paper's stated uncertainty load-bearing rather than academic.

### 1.4 The generator this project is testing

The upstream lineage: Rossant et al. (2016) introduced hybrid validation for dense arrays; Yger et al. (2018) used it at 4,225 electrodes; Wouters, Kloosterman & Bertrand (2021) built SHYBRID as a dedicated GUI tool; SpikeInterface absorbed the approach into `spikeinterface.generation`.

Two design choices in that lineage differ in a way that is directly relevant:

- **SHYBRID relocates a real unit.** Its stated mechanism is that *"spikes from a single unit are moved to a different location on the recording probe, thereby generating a virtual unit of which the spike times are known."* Moving a real unit carries its real spike train and its real per-spike waveform variability along with it. **[VERIFY]** — I reached only the abstract; whether SHYBRID re-renders from an average template or transports the individual spike snippets needs confirming from the full text before this is stated in the Claim Sheet.
- **SpikeInterface synthesises the spike train.** `generate_hybrid_recording()` injects an *average template* from the template library at times drawn from a generated spike train, with `firing_rates` and `refractory_period_ms` as the controls. The anchor paper used a homogeneous Poisson process at 15 Hz mean, 10 hybrid units per recording, 5 randomised iterations, amplitudes rescaled into a defined range (e.g. 50–200 µV), with DREDge-estimated motion applied by spatial interpolation of the template during injection.

So the realism gap this project targets is not hypothetical or hidden: it is the difference between injecting **a fixed average waveform at Poisson times** and injecting **something that behaves like a neuron**.

### 1.5 What the SpikeInterface generation API does and does not offer

Confirmed from the current documentation:

- **Present:** `generate_hybrid_recording()`, `InjectTemplatesRecording`, `InjectDriftingTemplatesRecording` (when a `motion` object is passed), `generate_drifting_recording()`, `scale_template_to_range()`, `relocate_templates()`, `make_one_displacement_vector()`. Spike-train controls exposed as `generate_sorting_kwargs` with `firing_rates` (a range) and `refractory_period_ms`.
- **Absent:** any parameter for bursting, ISI-dependent amplitude attenuation, or firing-rate non-stationarity. The documentation mentions helper functions to inject "overly synchronous spikes," which is a different phenomenon (cross-unit synchrony, not within-unit burst structure).

**This confirms the director's framing of the axis ratio, and it is worth restating precisely because it constrains the Claim Sheet:**

| Axis | Upstream status | What this project has to do |
|---|---|---|
| Refractoriness | **Implemented** (`refractory_period_ms`) | Nothing — not a delta, can only be a control condition |
| Region-matched templates | **Supported** (`brain_area` metadata, below) | Query and select — a genuine measurement with no new engineering |
| Bursting + firing-rate non-stationarity | **Absent** | Implement before it can be measured |

### 1.6 The template library

`SpikeInterface/hybrid_template_library` (MIT) holds >600 templates in Zarr on S3, from two sources: IBL Brain-Wide Map (Neuropixels 1.0) and Steinmetz & Ye 2022 (Neuropixels Ultra, interpolated to NP2.0 geometry). Access is `fetch_templates_database_info()` → pandas query → `query_templates_from_database()`.

**The `brain_area` column is real and confirmed**, with values like `VISa5`, `VISa6a`, `VISp5`, `VISp6a`, `VISrl6b` and 70+ areas total. Other columns: `probe`, `probe_manufacturer`, `depth_along_probe`, `amplitude_uv`, `noise_level_uv`, `signal_to_noise_ratio`, `template_index`, `best_channel_index`, `spikes_per_unit`, `dataset`, `dataset_path`.

**A caution the Claim Sheet should absorb.** The `brain_area` values I could confirm are heavily visual-cortex-weighted. Whether the library actually contains enough templates in the specific regions of the DANDI 000409 recordings this project will use — and enough of them to build a matched *and* a deliberately mismatched arm at comparable amplitude and SNR — is an empirical question about the database contents, and it is the single largest feasibility risk to the region-matching axis. **It should be answered by querying the database in an early Phase 2 session, before any sorter time is spent.** If matched templates are scarce in the target region, the axis has to be redesigned (e.g. matched-vs-maximally-distant rather than matched-vs-random) rather than quietly weakened.

---

## 2. Benchmark results — what numbers look like in this field

This section exists to calibrate the Claim Sheet's success bars against reality rather than intuition.

### 2.1 The accuracy metric is standardised

SpikeForest defines it, SpikeInterface implements it, and the anchor paper uses it:

> accuracy = n_match / (n_match + n_miss + n_fp)

Symmetric in misses and false positives, bounded [0, 1], computed per ground-truth unit after an optimal matching between ground-truth and sorted units. Precision and recall are reported alongside. **A convention worth adopting from SpikeForest:** report the *count of ground-truth units above an accuracy threshold* (default 0.8) as well as mean accuracy, because the mean hides whether a manipulation moved everything a little or a few units a lot.

### 2.2 Realistic performance ranges

| Study | Data type | Numbers |
|---|---|---|
| Yger et al. 2018 | Real paired, in vitro | 4.8% mean error (SpyKING CIRCUS) vs 2.7% for an optimal classifier, n=37 large-waveform neurons |
| Yger et al. 2018 | Real paired, **in vivo** | **14.8% mean error** vs 13.9% optimal, n=2 |
| Yger et al. 2018 | Hybrid, 4,225 electrodes | <5% total error above threshold; 4.4% SpyKING CIRCUS vs 4.2% Kilosort |
| Rossant et al. 2016 | Multiple species/regions | error rates "as low as 5%" |
| Pachitariu et al. 2024 | Simulated | Kilosort4 ~80–90% of units found; IronClust ~50% |
| Garcia et al. 2024 (drift) | MEArec, 256 neurons | well-detected units: 165 static → 118 zigzag → 136 non-rigid → 107 bumps, *with* best-available correction |
| Buccino et al. 2026 (anchor) | Hybrid, NP1.0 | KS4 > KS2.5 on accuracy, effect size 0.276 |
| Buccino et al. 2026 (anchor) | Hybrid, NP2.0 | KS4 > KS2.5 on accuracy, effect size 0.408 |

**Three calibration lessons for the Claim Sheet:**

1. **The effect this project must resolve is small.** The anchor paper's headline sorter-vs-sorter effect sizes are 0.28 and 0.41. A realism manipulation that moves accuracy by less than that cannot flip a ranking; one that moves it by more than that can. **The anchor paper's own effect sizes are therefore the natural yardstick for "decision-relevant"** — this is the most directly usable number in this whole survey, and Slot 7 should be built on it.
2. **The in-vivo/in-vitro gap is instructive.** 4.8% error in vitro against 14.8% in vivo, same sorter. Real biological conditions cost roughly three times the error. Whatever fraction of that gap is attributable to firing-statistics realism is the headroom this project is looking for.
3. **Scale is a design constraint, not a detail.** The anchor paper used 1,800 (NP1.0) and 3,000 (NP2.0) ground-truth units across 36 and 60 recordings. This project runs on one shared 32 GB / 16 GB-VRAM desktop. **A design that tries to match that N will not run here.** The efficiency standard and the compute-environment warning both point the same direction: fewer, better-controlled conditions with paired comparisons, not a scale contest.

### 2.3 The finding that most directly motivates this project

SpikeForest (Magland et al. 2020) benchmarked ten sorters on 650 recordings and ~35,000 ground-truth units and concluded that *"none of the algorithms emerged as a clear winner across all datasets"* — MountainSort4 for low channel counts, IronClust on simulated and drifting data, Kilosort2 at low SNR. **Sorter ranking is already known to be a function of the benchmark data.** This project asks a sharpened version of the same question: is it a function of the *realism knobs of a single benchmark generator*, holding the underlying recording fixed?

And then, decisively, from the same paper:

> "Interestingly, this is *not* generally true for the synthetic studies (where often the precision is higher than recall), indicating that, despite the sophistication of many of these simulations, they may not yet be duplicating the firing and noise statistics of real-world electrophysiology recordings."

That is a 2020 empirical observation, on 35,000 units, that synthetic ground truth has a *systematically different precision/recall signature* from real ground truth, and it names **firing statistics** as a suspected cause. It is the strongest published prior that the bursting/non-stationarity axis is the right one to build.

---

## 3. Dataset and resource landscape

| Resource | License | Verified where | Relevance |
|---|---|---|---|
| **DANDI 000409** — IBL Brain-Wide Map | **CC-BY-4.0** | DANDI API metadata (`/api/dandisets/000409/versions/draft/info/`) | The substrate recording. 2,048 files, ~49.7 TB total, 139 subjects. Only a small subset is needed. |
| **`hybrid_template_library`** | **MIT** | repository | >600 templates, `brain_area` column, S3/Zarr |
| **SpikeInterface** | MIT | repository | Generator + comparison + sorter interface |
| **Kilosort4** | **GPLv3** | repository | Sorter under test — **call as a tool, never vendor** |
| SpikeForest datasets | Varied | eLife 55167 | Reference benchmark, likely not used directly |
| MEArec | — | Neuroinformatics 2021 | Fully synthetic alternative; not the substrate here |

**On the GPLv3 point**, which the project idea already flags: running Kilosort4 as an external tool via SpikeInterface's sorter interface is ordinary use and imposes nothing. The risk is entirely in *modifying* it. There is a plausible temptation ahead — if a realism manipulation interacts with a Kilosort internal, it will be tempting to instrument the source. **Do not.** Use the `sortingcomponents` decomposition from the companion paper (MIT, part of SpikeInterface) if stage-level visibility is needed; it exists precisely to make sorter internals inspectable without touching a GPL sorter.

**On sorter selection.** The question is about *rankings*, so at least two sorters are structurally required and they should differ in *mechanism*, not just in version. The anchor paper compared Kilosort4 against Kilosort2.5 — two members of one family, sharing a drift-correction lineage. Garcia et al. (2022) show the template-matching/density-based split is where sorters diverge most on spike-train properties, and Garcia et al. (2026) raise a **circularity concern that applies directly to that choice**: because hybrid data injects spikes using motion-corrected templates, sorters using the same motion-correction method gain an unfair advantage. A Kilosort4-vs-Kilosort2.5 pairing is therefore the *least* likely pairing to reveal a ranking flip, and a design that used only it would be biased toward the negative result. Phase 1 should consider at least one non-Kilosort sorter available through SpikeInterface, weighed against what the compute budget can actually run.

---

## 4. Failure modes — what has been tried and has not worked

### 4.1 Known dead ends and hard problems in the field

- **Sorters disagree at a scale that makes "accuracy" fragile.** Buccino, Garcia & Yger (2022) report that across six sorters on one dataset, only **33 of ~1,400 units** were agreed on by all six. Any single-sorter result is a statement about that sorter.
- **Drift correction does not rescue accuracy.** Garcia et al. (2024): *"even applying the best drift correction dramatically reduces spike sorting accuracy"* — 165 well-detected units static, 107 with abrupt drift, correction applied. Relevant here as a warning that a nuisance variable can dominate a realism effect if not held fixed; the anchor pipeline's DREDge motion handling should be held constant across arms.
- **Collisions defeat density-based sorters.** >50% cross-correlogram reconstruction error at small lags (Garcia et al. 2022). Bursting *increases* within-unit near-coincident spikes, so a bursting manipulation will partly act through the collision channel. This is a confound to name explicitly, not a bug.
- **Bursting cells are a named open problem.** The field's own list of unsolved problems includes overlapping spikes, **bursting cells**, nearly-silent neurons, and non-stationarity. The project is not inventing the concern.
- **Fully synthetic data has repeatedly failed review on realism.** The eLife assessment of the companion paper rates its evidence *incomplete*, citing a biophysical model based on one simulation, insufficiently diverse test data, and simplified Gaussian noise without LFP. **The lesson for this project is procedural:** a realism claim gets attacked on realism. Anything this project *adds* to the generator must be justified against measured properties of the real recording, not asserted.

### 4.2 The specific mechanism the missing axis is about

This is the part of the literature that makes the bursting axis a scientific choice rather than an engineering whim.

Hippocampal pyramidal cells fire complex-spike bursts: several spikes at ≤6 ms intervals, **with decreasing extracellular amplitude across the burst**. Harris et al. (2001) tie burst probability and burst length to both extracellular spike amplitude and intracellular AP rising slope, and show burst probability is lower and bursts shorter after recent spiking than after 100 ms–1 s of silence. Extracellular amplitude attenuation is activity-dependent and most dramatic during high-frequency bursts (Quirk & Wilson, PMC6762418 **[VERIFY]** — I have the finding and the PMC ID but not the confirmed full citation).

Pouzat, Delescluse, Viot & Diebolt (2004) built a sorter that explicitly models *"the events amplitude decays for short interspike intervals"* and report that doing so lets the method cope with neurons firing doublets and generating highly dynamic waveforms.

**Put together, that is the failure mode this project's missing axis is designed to expose.** A hybrid unit built from a single average template presents the sorter with a waveform whose amplitude is independent of its own firing history. A real bursting neuron does not. A sorter that would miss the 3rd and 4th spikes of a real burst — because they have dropped below threshold or drifted away from the learned template — will not miss them in hybrid data, and its measured recall will be too high by exactly the amount the field cannot currently see.

**Critically, the two realism axes are mechanistically different, and this matters for the study design:**

- **Region-matched templates** change the *waveform shape and spatial footprint* of the injected unit — a static, per-unit property. Jia et al. (2019) established that extracellular waveforms have distinct spatiotemporal profiles across brain regions and that multi-channel waveforms improve region classification; regional waveform durations differ measurably (e.g. lateral posterior thalamus ~0.73 ms and lowest peak-to-trough ratio; superior colliculus ~0.33 ms; cerebellum ~0.24 ms). **[VERIFY]** — these specific numbers came from a search summary attributed to region-comparison work in this literature; the exact source must be pinned before the numbers are used anywhere citable.
- **Bursting and non-stationarity** change the *temporal statistics and the within-unit waveform dynamics* — and burstiness itself differs by region (cortical burst fraction lower than thalamic).

So the two axes are not two dials on one thing. **A design that varies both together cannot attribute an effect to either.** The Claim Sheet should factor them, and should expect that region-matching moves the detection/clustering stage while bursting moves the deconvolution/collision stage.

### 4.3 Failure modes specific to *this* project's design

Naming these now so Phase 1 does not rediscover them:

1. **Confounding realism with SNR.** Region-matched templates will differ in amplitude and SNR from mismatched ones. If the matched arm has systematically larger templates, any accuracy difference is an amplitude effect wearing a realism costume. The library exposes `amplitude_uv` and `signal_to_noise_ratio` — **match on them explicitly**, and report the achieved distributions per arm.
2. **Confounding bursting with mean firing rate.** Making a unit bursty at fixed mean rate is a different manipulation from making it fire more. Hold the total spike count per unit fixed across arms; otherwise the comparison is about N, not about structure.
3. **Grading the generator with a sorter that shares the generator's assumptions.** The circularity point from Garcia et al. (2026). Applies to motion correction most sharply.
4. **Under-powering the ranking question.** A ranking flip is a comparison of differences. With 10 units per recording (the anchor default) and effect sizes near 0.3, a handful of recordings will not resolve it. Paired designs — same recording, same units, same seeds, only the realism knob changed — are what buy power on a small compute budget, and they should be the default.
5. **Silent template-selection bias.** Which templates get selected is itself a strong determinant of measured accuracy. Every arm should draw from a pre-declared, seeded selection procedure, and the selection should be recorded in the packet.
6. **Declaring a negative from an unmoved needle that was never able to move.** If the injected "bursting" is too mild to change waveforms measurably, a null is a statement about the implementation, not about the field's method. **A manipulation check is mandatory** — verify from the injected data itself that burst-structure and amplitude attenuation are present at realistic magnitudes before any sorter is run. This is a stop-or-go gate under the Scientific-work standard.

---

## 5. Open questions

### 5.1 The question this project takes

Stated by the maintainers themselves in the Limitations of Buccino et al. (2026), and confirmed verbatim from the eLife Version of Record this session:

> "First, the ground-truth units had Poisson-distributed spike times, which do not necessarily match the overall firing statistics of the original recording. One improvement to this approach could be to estimate ongoing population firing rates and inject spike trains that follow the dynamics of nearby neurons."

> "A second limitation lies in the selection of the spike templates: although we used different templates for each probe type, we did not choose templates to match the brain region of the original recording. It remains to be tested whether generating more realistic hybrid recordings will have any effect on spike sorting accuracy."

**Two things I want on the record for Phase 1, because the project brief quotes the second passage but not the first.** The maintainers named the firing-statistics limitation *first*, and they went further than naming it — they proposed the fix (*"estimate ongoing population firing rates and inject spike trains that follow the dynamics of nearby neurons"*). That is a specific, implementable, maintainer-endorsed design for the axis the project has to build. It also suggests an axis the brief does not currently list: **population-coupled firing**, i.e. spike trains that follow the local population's rate dynamics rather than being independent of them. That is arguably closer to what the maintainers asked for than within-unit bursting is, and it may be cheaper to implement — a rate function estimated from nearby sorted units, used to modulate an inhomogeneous Poisson process, requires no waveform model at all. **I think Phase 1 should consider it as a third candidate axis, or as the first tier of the non-stationarity axis.** I am not proposing to displace bursting; I am proposing the Claim Sheet should decide between them deliberately rather than inherit one by default.

### 5.2 Sub-questions the literature leaves open that bear directly on Slot 3

- Does realism change **absolute accuracy**, the **ranking between sorters**, or **neither**? These can dissociate: a manipulation could lower everyone's accuracy uniformly (ranking safe, absolute numbers inflated) or move sorters differentially (ranking unsafe). **These are different findings with different consequences for the field, and the Claim Sheet should predeclare both.**
- Does realism act **uniformly across units**, or concentrate in a subpopulation (low-amplitude, high-rate, bursty)? SpikeForest's threshold-count convention exists because means hide this.
- Which **sorter stage** absorbs the effect? The `sortingcomponents` decomposition makes this answerable; whether it fits this project's compute budget is a Phase 1 call.
- How large is realism's effect **relative to drift**, which is known to be large? If drift dominates by an order of magnitude, the honest headline is "realism matters less than the thing you already correct for," which is itself a useful, publishable, decision-relevant result.

### 5.3 What would make the negative result strong rather than merely absent

Per the project's pre-declared negative: realism manipulations produce accuracy differences small enough, and rankings stable enough, that the choice of realism axis does not change which sorter a reader would pick. To be *strong*, that requires: (a) a passed manipulation check proving the realism knob actually turned; (b) a comparison bound stated against the anchor paper's own effect sizes (0.276 / 0.408) rather than against zero; (c) at least two mechanistically different sorters; and (d) enough paired replicates to bound the difference, not merely fail to detect one. **A null with a wide confidence interval is not a negative result — it is an inconclusive one, and the Claim Sheet needs a distinct pre-declared shape for that.**

### 5.4 Verification debt carried out of this session

Collected so a later session can clear them rather than let them harden into fact:

1. **[VERIFY]** SHYBRID's exact injection mechanism (relocated real snippets vs re-rendered average template). Source: Wouters et al. 2021 full text.
2. **[VERIFY]** Quirk & Wilson full citation for activity-dependent extracellular amplitude attenuation (have PMC6762418 and the finding).
3. **[VERIFY]** Regional waveform-duration figures (LP 0.73 ms, SC 0.33 ms, cerebellum 0.24 ms) — pin the exact source before use.
4. **[VERIFY]** The companion paper's *"already has the key ingredients to challenge spike sorting algorithms"* quote, cited in the project brief. The version I reached renders the equivalent claim as "core features needed to properly challenge modern spike sorters." **Do not use the brief's wording as a quotation until it is confirmed against the PDF** — the negative-result framing leans on it.
5. **[VERIFY]** Kilosort4's simulator: whether its "non-stationary spike waveforms" include ISI-dependent amplitude attenuation. If they do, part of the missing axis already exists in a comparator's own benchmark, which would be a significant framing fact. bioRxiv full text was rate-limited this session.
6. **[OPEN — empirical, not literature]** Do enough `brain_area`-matched templates exist for the specific DANDI 000409 regions this project will use? §1.6. Answer by query before committing to the axis.

---

## 6. References

Ledger-quality entries: what it covers · how it informed this project · link · transferable citation. These migrate into `agents/Claude/references.md` at Phase 1 start.

---

**Buccino AP, Sridhar A, Feng D, Svoboda K, Siegle JH (2026). Efficient and reproducible pipelines for spike sorting large-scale electrophysiology data.** *eLife* 15:RP110170. [doi:10.7554/eLife.110170.3](https://doi.org/10.7554/eLife.110170.3)
Nextflow + SpikeInterface + Code Ocean pipelines for large-scale sorting, benchmarked on hybrid recordings: 36 NP1.0 recordings (1,800 GT units) and 60 NP2.0 recordings (3,000 GT units), Poisson spike trains at 15 Hz mean, 10 hybrid units per recording, amplitudes rescaled to 50–200 µV, DREDge motion applied by template interpolation. Kilosort4 > Kilosort2.5 with effect sizes 0.276 (NP1.0) and 0.408 (NP2.0).
*How it informed the work:* **The anchor paper.** It supplies the exact Limitations text the project tests (§5.1), the generator configuration the control arm must reproduce, and — most usefully — the effect-size scale (0.276/0.408) that Slot 7 should define "decision-relevant" against. Its N also establishes that this project cannot match its scale on one desktop and must buy power through paired design instead.

**Garcia S, Halcrow C, Windolf C, McKenzie ZM, Adkisson-Floro P, Mayorquin HR, Dichter B, Buccino AP, Yger P (2026). Opening the black box: a modular approach to spike sorting.** *eLife* reviewed preprint, 1 April 2026. [doi:10.7554/eLife.110588.1](https://doi.org/10.7554/eLife.110588.1)
Decomposes sorters into five swappable stages, each with a `BenchmarkStudy` object; ships an empirical simulator (500 neurons, 384ch, 30 kHz, gamma-distributed rates 0.1–30 Hz, trimodal depth, static and drifting variants). Raises a circularity problem: hybrid data injected with motion-corrected templates advantages sorters using the same motion correction. eLife assessment rates the evidence *incomplete* on realism grounds.
*How it informed the work:* Three things. It names the **circularity confound** that makes a Kilosort4-vs-Kilosort2.5-only design biased toward a null (§3, §4.3). It offers a **stage-level alternative design** (§1.2). And its critical review is a warning about the standard a realism claim will be held to (§4.1). Note the "key ingredients" quote in the project brief is **[VERIFY]** against this source.

**Magland J, Jun JJ, Lovero E, et al. (2020). SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters.** *eLife* 9:e55167. [doi:10.7554/eLife.55167](https://doi.org/10.7554/eLife.55167)
Ten sorters, 650 recordings, ~35,000 GT units, 11 labs. Defines accuracy = n_match/(n_match+n_miss+n_fp). Finds no universal winner: MountainSort4 for low channel counts, IronClust on simulated/drifting, Kilosort2 at low SNR.
*How it informed the work:* Supplies the **accuracy metric definition** and the threshold-count reporting convention (§2.1). Establishes the prior that **ranking is already a function of benchmark data** (§2.3). Its observation that synthetic studies show precision > recall — *"they may not yet be duplicating the firing and noise statistics of real-world electrophysiology recordings"* — is the strongest published evidence that the firing-statistics axis is the right one to build.

**Buccino AP, Garcia S, Yger P (2022). Spike sorting: new trends and challenges of the era of high-density probes.** *Progress in Biomedical Engineering* 4(2):022005. [doi:10.1088/2516-1091/ac6b96](https://doi.org/10.1088/2516-1091/ac6b96)
Review of the modern field: methods families, the three ground-truth strategies, quality metrics, curation bias. Reports that across six sorters on one dataset only 33 of ~1,400 units were agreed by all six; notes paired ground truth usually yields a single unit per dataset and is biased toward large pyramidal cells.
*How it informed the work:* The framing for §1.3 — **why hybrid is the strategy the field grades on**, and therefore why its realism is load-bearing. The 33/1,400 figure calibrates how fragile single-sorter accuracy claims are.

**Pachitariu M, Sridhar S, Pennington J, Stringer C (2024). Spike sorting with Kilosort4.** *Nature Methods*. [doi:10.1038/s41592-024-02232-7](https://doi.org/10.1038/s41592-024-02232-7) · preprint [doi:10.1101/2023.01.07.523036](https://doi.org/10.1101/2023.01.07.523036)
Graph-based clustering; simulator using densely sampled real electrical fields to generate non-stationary waveforms and realistic noise. ~80–90% of units recovered vs ~50% for IronClust. Ablation: drift correction, deconvolution, and CCG-based merges/splits carry the gains.
*How it informed the work:* Defines the sorter under test and its published performance band. Its simulator's claim of "non-stationary spike waveforms" is **[VERIFY] item 5** — if it already models ISI-dependent amplitude, that changes how this project frames the missing axis.

**Garcia S, Windolf C, Boussard J, Dichter B, Buccino AP, Yger P (2024). A modular implementation to handle and benchmark drift correction for high-density extracellular recordings.** *eNeuro* 11(2):ENEURO.0229-23.2023. [doi:10.1523/ENEURO.0229-23.2023](https://doi.org/10.1523/ENEURO.0229-23.2023)
MEArec benchmarks (10 min, 256 neurons, NP1.0-like 128ch), 12 scenarios crossing drift type × depth distribution × **firing-rate regime (homogeneous vs sine-modulated)**. Motion estimation error <5 µm for smooth drift. Well-detected units: 165 static → 118 zigzag → 136 non-rigid → 107 bumps, best correction applied.
*How it informed the work:* Two uses. It is the **precedent for treating firing-rate non-stationarity as a benchmark variable** (sine-modulated rates), which de-risks that axis methodologically. And its magnitude — drift costs ~35% of well-detected units even corrected — sets the scale a realism effect must be compared against (§5.2).

**Garcia S, Buccino AP, Yger P (2022). How do spike collisions affect spike sorting performance?** *eNeuro* 9(5):ENEURO.0105-22.2022. [doi:10.1523/ENEURO.0105-22.2022](https://doi.org/10.1523/ENEURO.0105-22.2022)
Collisions defined as spikes from two units within 2 ms; "collision recall" binned across [−2,2] ms. Template-matching sorters (Kilosort 1/2, SpyKING CIRCUS) resolve collisions far better than density-based ones (HerdingSpikes, IronClust); CCG reconstruction error >50% at small lags for the latter. MEArec, 30 min, 20 neurons, 32ch, rates 5–15 Hz, correlation 0–20%.
*How it informed the work:* Identifies the **mechanism by which a bursting manipulation will differentially affect sorters** — bursts create within-unit near-coincident spikes, and collision handling is exactly where sorter families diverge. This is the concrete reason a ranking flip is plausible rather than speculative, and the reason sorter selection should span mechanisms (§3).

**Wouters J, Kloosterman F, Bertrand A (2021). SHYBRID: a graphical tool for generating hybrid ground-truth spiking data for evaluating spike sorting performance.** *Neuroinformatics* 19(1):141–158. [doi:10.1007/s12021-020-09474-8](https://doi.org/10.1007/s12021-020-09474-8) · PMID 32617751
Hybrid generation by *relocating* a real unit's spikes to a different probe location, producing a virtual unit with known spike times.
*How it informed the work:* The **design contrast that defines the realism gap** (§1.4). Relocation preserves the real spike train; SpikeInterface's average-template-plus-Poisson approach does not. Exact mechanism is **[VERIFY] item 1**.

**Yger P, Spampinato GLB, Esposito E, et al. (2018). A spike sorting toolbox for up to thousands of electrodes validated with ground truth recordings in vitro and in vivo.** *eLife* 7:e34518. [doi:10.7554/eLife.34518](https://doi.org/10.7554/eLife.34518)
SpyKING CIRCUS. Real paired ground truth: 4.8% mean error in vitro (n=37) vs 2.7% optimal; **14.8% in vivo (n=2)** vs 13.9% optimal. Hybrid at 4,225 electrodes: <5% error; 4.4% SpyKING CIRCUS vs 4.2% Kilosort. Hybrid units built by shuffling electrodes of real templates and injecting "at controlled firing rates." States: *"it is not clear if this simulated data reproduce the conditions of actual recordings,"* noting real waveforms vary in amplitude and shape.
*How it informed the work:* Supplies the **in-vitro vs in-vivo error gap** that bounds the headroom a realism effect could occupy (§2.2), and a **2018 statement of the same concern** the 2026 anchor paper restates — showing this is a durable open question, not a one-off caveat.

**Pouzat C, Delescluse M, Viot P, Diebolt J (2004). Improved spike-sorting by modeling firing statistics and burst-dependent spike amplitude attenuation: a Markov chain Monte Carlo approach.** *Journal of Neurophysiology* 91(6):2910–2928. [doi:10.1152/jn.00227.2003](https://doi.org/10.1152/jn.00227.2003) · PMID 14749321
Sorter that jointly models firing statistics and waveform dynamics — *"the events amplitude decays for short interspike intervals"* — and thereby copes with doublet-firing neurons and highly dynamic waveforms.
*How it informed the work:* **The mechanistic warrant for the bursting axis** (§4.2): a sorting method built twenty years ago around ISI-dependent amplitude decay is prima facie evidence that the property is real, consequential for sorting, and absent from the current hybrid generator.

**Harris KD, Hirase H, Leinekugel X, Henze DA, Buzsáki G (2001). Temporal interaction between single spikes and complex spike bursts in hippocampal pyramidal cells.** *Neuron* 32(1):141–149. [doi:10.1016/S0896-6273(01)00447-0](https://doi.org/10.1016/S0896-6273(01)00447-0) · PMID 11604145
CA1 pyramidal cells in behaving rats: complex-spike bursts of several spikes at ≤6 ms ISIs with decreasing extracellular amplitude. Burst probability peaks at 6–7 Hz discharge; burst probability lower and bursts shorter after recent spiking than after 100 ms–1 s of silence; burst length correlates with extracellular amplitude and intracellular AP rising slope.
*How it informed the work:* The **quantitative target the bursting implementation must hit** — ISI scale (≤6 ms), history dependence (suppression after recent activity), and the amplitude-decay coupling. Also the basis of the mandatory manipulation check (§4.3.6): injected bursts must reproduce these properties before any sorter is run.

**Jia X, Siegle JH, Bennett C, Gale SD, Denman DJ, Koch C, Olsen SR (2019). High-density extracellular probes reveal dendritic backpropagation and facilitate neuron classification.** *Journal of Neurophysiology* 121(5):1831–1847. [doi:10.1152/jn.00680.2018](https://doi.org/10.1152/jn.00680.2018) · PMID 30840526
Multi-channel extracellular waveforms show distinct spatiotemporal profiles across brain regions; region classification improves with multi-channel over single-channel waveforms. RS/FS split at 0.4 ms duration; backpropagating-AP subclass identified in cortex and hippocampal RS cells.
*How it informed the work:* **The empirical warrant for the region-matched-template axis** (§4.2): if waveform spatiotemporal structure is region-specific and multi-channel enough to classify region, then injecting a visual-cortex template into a thalamic recording is a measurable realism error, not a cosmetic one.

**Rossant C, Kadir SN, Goodman DFM, et al. (2016). Spike sorting for large, dense electrode arrays.** *Nature Neuroscience* 19(4):634–641. [doi:10.1038/nn.4268](https://doi.org/10.1038/nn.4268) · PMID 26974951
KlustaKwik/phy for dense arrays; validated across cortex, hippocampus and thalamus in rat, mouse, macaque and marmoset, with error rates as low as 5%.
*How it informed the work:* **Origin point of the hybrid-validation paradigm** this project examines (§1.4), and a cross-region performance band for §2.2.

**Buccino AP, Hurwitz CL, Garcia S, Magland J, Siegle JH, Hurwitz R, Hennig MH (2020). SpikeInterface, a unified framework for spike sorting.** *eLife* 9:e61834. [doi:10.7554/eLife.61834](https://doi.org/10.7554/eLife.61834)
The unified API underlying the generator, the sorter interface, and the comparison module this project uses.
*How it informed the work:* Establishes that the **independent variable, the measurement instrument, and the sorter interface all live in one pinnable package** (§1.2) — a structural advantage for a controlled study.

**SpikeInterface generation module — documentation.** [spikeinterface.readthedocs.io/en/stable/modules/generation.html](https://spikeinterface.readthedocs.io/en/stable/modules/generation.html)
API surface: `generate_hybrid_recording()`, `InjectTemplatesRecording`, `InjectDriftingTemplatesRecording`, `generate_drifting_recording()`, `make_one_displacement_vector()`; `generate_sorting_kwargs` exposing `firing_rates` and `refractory_period_ms`.
*How it informed the work:* **Primary evidence for the axis ratio in §1.5** — refractoriness present, bursting and rate non-stationarity absent. This is the observation that determines how much of the project is engineering.

**SpikeInterface — Benchmark spike sorting with hybrid recordings (how-to).** [spikeinterface.readthedocs.io/en/stable/how_to/benchmark_with_hybrid_recordings.html](https://spikeinterface.readthedocs.io/en/stable/how_to/benchmark_with_hybrid_recordings.html)
Canonical workflow: `fetch_templates_database_info()` → pandas query → `query_templates_from_database()` → `scale_template_to_range()` / `relocate_templates()` → `generate_hybrid_recording()`. Confirms `brain_area` (70+ areas), `amplitude_uv`, `signal_to_noise_ratio`, `depth_along_probe` metadata columns.
*How it informed the work:* **Confirms the region-matching axis is queryable without new engineering**, and supplies the covariates (`amplitude_uv`, `signal_to_noise_ratio`) that must be matched across arms to avoid the SNR confound (§4.3.1).

**SpikeInterface/hybrid_template_library.** MIT. [github.com/SpikeInterface/hybrid_template_library](https://github.com/SpikeInterface/hybrid_template_library) · browser: [spikeinterface.github.io/hybrid_template_library](https://spikeinterface.github.io/hybrid_template_library/)
>600 templates in Zarr on S3, from IBL Brain-Wide Map (NP1.0) and Steinmetz & Ye 2022 (NP Ultra → NP2.0 geometry).
*How it informed the work:* The template source for both arms, and the object of the open feasibility question in §1.6. **License MIT, verified at the repository.**

**DANDI 000409 — IBL Brain-Wide Map.** CC-BY-4.0. [dandiarchive.org/dandiset/000409](https://dandiarchive.org/dandiset/000409) · metadata verified via [DANDI API](https://api.dandiarchive.org/api/dandisets/000409/versions/draft/info/)
2,048 assets, ~49.7 TB, 139 subjects. Citation: International Brain Laboratory; Benson B; Benson J; Birman D; et al. (2026) *IBL — Brain Wide Map* [Data set]. DANDI Archive. DANDI:000409.
*How it informed the work:* The substrate recording, and the same dataset the anchor paper's NP1.0 templates were derived from — which is convenient for region-matching and is itself a point to think about (matching a recording against templates derived from the same dataset family is *more* realistic but edges toward circularity; a Phase 1 discussion item). **License CC-BY-4.0, verified in the dataset's own DANDI metadata — attribution obligation is real and belongs in `DATA.md`.**

---

*End of Claude's Phase 0 Literature Foundation. Phase 0 closes when Codex's foundation exists and the comparison chat is done — see `chats/Claude-Codex/Phase 0 Literature Comparison/`.*
