# Claim Sheet — Hybrid Ground Truth Realism

## What this document is

This is the contract for the project. It states the question, the method, the baselines, and — declared in advance, before any result is seen — what would count as success, as failure, and as inconclusive. Every agent reads it at the start of every session, and every result the project produces is measured against it.

Read it in order. The orientation below hands you the story; the fifteen numbered slots that follow are the commitments, and they are meant to be read as a throughline rather than looked up individually. If you want only one thing from this document, take the *Contract at a glance* box below, and then Slots 11, 12, and 13 — the pre-declared shapes of success, failure, and inconclusiveness. Those three are the reason the rest of it is written down before the work starts.

## The question, in ordinary language

Spike sorting is the step that turns a raw electrical recording from inside a brain into a list of which neuron fired when. A probe picks up a blur of overlapping voltage spikes from many nearby cells at once, and an algorithm — a *spike sorter* — has to decide which spike belonged to which neuron. Almost everything downstream in systems neuroscience rests on that step being right.

The problem is that nobody knows the right answer for a real recording. There is no answer key. So the field grades spike sorters on **hybrid recordings**: take a real recording, and inject extra synthetic spikes into it at times you chose yourself. Now you have an answer key, at least for the spikes you added. Count how many of them the sorter found.

That works only if the synthetic spikes are enough like real ones. If they are easier to find than real spikes, every sorter scores too well; if they are easier for *one kind* of sorter than another, the comparison between sorters is measuring the generator rather than the sorters.

The maintainers who built and published the field's standard hybrid pipeline wrote, in the Limitations section of their own paper, that they do not know whether their synthetic spikes are realistic enough:

> "It remains to be tested whether generating more realistic hybrid recordings will have any effect on spike sorting accuracy."

**This project tests it.** We take their pipeline, change the realism of the injected spikes one property at a time along axes they themselves named, hold every *axis-compatible* nuisance variable fixed, and measure two things: whether accuracy moves, and — the one that matters more — whether the *comparison between sorters* moves. Tier A must change donor-template identity in order to change donor region, so it uses predeclared matched donor pairs while holding each pair's spike train, placement, and rescaled amplitude target fixed; Tiers B and C hold donor identity fixed.

## Narrative context

**The prior rung.** The field already has reason to suspect the answer is not "no." A 2020 benchmark spanning roughly 35,000 ground-truth units found that synthetic ground truth produces a systematically different error signature from real paired ground truth, and attributed it to simulations not reproducing the firing and noise statistics of real recordings. A 2024 result showed that making waveforms in a biophysical simulation more realistic in duration measurably reduced spurious clusters. A 2018 toolbox paper made the same worry in print six years before the anchor paper restated it. What none of these did is the controlled version: hold every axis-compatible nuisance variable fixed or matched, change exactly one realism property, and measure what moves.

**The current rung — this project.** Three realism properties, tested in order of engineering cost, one at a time:

- **Tier A — region-matched templates.** The injected waveform shapes currently come from whatever brain region the template library happens to offer, not the region the host recording came from. Waveform shape is region-specific enough that a neuron's region can be classified from it, so this is a real mismatch and not a cosmetic one. Fixing it is *configuration*: the template library already carries a brain-area label. No new code.
- **Tier B — population-coupled firing.** Injected spike times are currently drawn from a Poisson process, which means they ignore what the rest of the brain is doing. The anchor paper's authors proposed the fix themselves: estimate the ongoing population firing rate nearby and make the injected trains follow it. Modest new code, and there is prior art.
- **Tier C — bursting with spike-history-dependent waveform dynamics.** Real neurons fire bursts of spikes a few milliseconds apart, and their extracellular waveform *shrinks across the burst*. A fixed average template presents the same amplitude regardless of what the neuron just did. This is the genuinely missing mechanism, it is the one that should stress the part of sorting where algorithms most disagree, and it has to be built before it can be measured.

**An honest note on the split.** Tier A is measurement. Tier B and Tier C are engineering in the service of measurement. That is still research, but this document says so plainly rather than presenting the project as pure measurement.

**What success and failure mean here.** Both directions are publishable and neither is a disappointment:

- If realism **does not** move the between-sorter comparison, the field's default ground-truth proxy is validated, a stated open question is closed, and a position one of the maintainers has asserted in print gets independent evidence it did not previously have.
- If realism **does** move it, then published accuracy comparisons built on hybrid data have been partly grading the generator rather than the sorter, and every benchmark that used one inherits that.

The result is reported exactly as measured either way. If it comes back positive, the report is written as *"we tested the limitation you named, and here is what we found"* — never as *"you were wrong."* That is a writing standard and is not a reason to soften anything.

## Contract at a glance

| | |
|---|---|
| **Target** | The paired **sorter × realism interaction** — how much the realism-induced accuracy change differs between sorters — plus the realism main effect on absolute accuracy. |
| **Inputs** | DANDI 000409 (IBL Brain Wide Map, CC-BY-4.0) host recordings · `hybrid_template_library` donor templates (MIT) · SpikeInterface generator and evaluator (MIT) · Kilosort4 (GPLv3, called as an external tool) plus at least one mechanistically different CPU sorter. |
| **Baselines** | A pinned, faithful reconstruction of the anchor pipeline's region-unaware/default generator, with anti-leakage and balance constraints documented; and a **negative-control replicate band**, formed from pseudo-arm contrasts generated under the same nominal condition, which diagnoses how much apparent interaction nuisance selection and seeds can create. |
| **Success bar** | A **bounded** estimate of the interaction for each tier attempted, with the manipulation check passed, precise enough to place the effect either inside or outside the pre-declared decision-relevant band. Success is a bounded answer, not a detected effect. |
| **Failure bar** | The project cannot produce a bounded estimate — the manipulation check cannot be made to pass, the compute will not support enough replicates to reach the required precision, or the donor-template feasibility collapses for every candidate host. |

## How this document is organized

The sheet is fifteen numbered slots, each a structurally important commitment: what we are working on and with, what the question is, what we could claim, what bounds the work, how we will do it, why it matters, how we will know, how the director checks it himself, how big we will build, what it runs on, and then the pre-declared shapes of success, failure, and inconclusiveness, the minimum artifact required to conclude, and the honest monetization position. Not every slot is heavy — Slot 15 in particular is thin, and says so — but all fifteen are present so that nothing structurally important is left implicit.

---

## Slot 1 — Domain and substrate

**Domain.** Extracellular electrophysiology, and specifically the *validation methodology* of spike sorting rather than spike sorting itself. The object under study is a benchmark, not an algorithm.

**Substrate.** Four materials, each pinned and each with its license read rather than inferred:

| Material | What it supplies | License |
|---|---|---|
| **DANDI 000409** — IBL Brain Wide Map | The **host recordings**: real Neuropixels 1.0 extracellular data carrying real noise, real endogenous spikes, real artifacts, and real drift. 2,048 assets, ~49.7 TB, 139 subjects, NWB format. A deliberately small, identifier-pinned subset is used; nothing is redistributed. | CC-BY-4.0 |
| **`hybrid_template_library`** | The **donor templates** injected into the hosts, with the `brain_area`, `amplitude_uv`, `signal_to_noise_ratio`, `depth_along_probe`, and `dataset` metadata that Tier A and the covariate balancing depend on. | MIT |
| **SpikeInterface** | The **generator** (`generate_hybrid_recording()` and the template query), the **sorter interface**, and the **evaluator** (ground-truth comparison and the performance metrics). One framework at one pinned commit for all three roles. | MIT |
| **Sorters** | **Kilosort4** as the GPU comparator, plus at least one mechanistically different **CPU internal sorter** from SpikeInterface (SpyKING CIRCUS 2, TriDesClous 2, or Lupin). | Kilosort4 **GPLv3**; the internal sorters MIT via SpikeInterface |

**The licensing posture, stated explicitly because it constrains code rather than just paperwork.** Kilosort4's GPLv3 makes it usable as an external tool that this project *runs* — that is ordinary use and imposes nothing on our own code. Copying its source into this project's scripts, or linking against it so as to create a derivative work, would oblige this entire project to be GPLv3. **We call it; we never vendor it.** If a genuine need to modify Kilosort4 appears, that is a licensing question raised in `director_requests.md` *before* the modification is written, not after. If stage-level visibility into a sorter becomes necessary, SpikeInterface's MIT-licensed `sortingcomponents` decomposition is used instead. Everything this project releases is path-scoped: code under MIT, prose under CC BY 4.0, per `LICENSING.md`. CC-BY-4.0 obliges attribution for DANDI 000409 and MIT obliges the license and copyright notice to travel with any redistributed code; both are recorded in the Reproducibility Packet's `DATA.md` as the packet is built, not reconstructed at the end.

**No standard from `Project Details.md` is relaxed for this project.** Where a design choice looks like a relaxation — running on recording *segments* rather than full-length recordings, for instance — it is a deliberate efficiency choice justified in Slot 9, not an exemption.

That is what we are working with. The next slot says what we are asking of it.

---

## Slot 2 — Problem being addressed

Hybrid recordings are the only route the field has to *many* ground-truth units sitting in *genuinely real* noise. Paired intracellular/extracellular recordings are more realistic but typically yield one ground-truth unit per recording and are biased toward the large cells that can be patched; fully simulated recordings yield every unit but can be wrong in every layer at once. Hybrid data is the compromise the field actually grades on — which makes the realism of its injected units load-bearing rather than an academic caveat.

The injected units are generated objects, and their realism decomposes into separable layers: template identity and regional plausibility; marginal spike-train statistics including refractoriness and bursts; population-coupled rate non-stationarity; spike-history-dependent waveform dynamics; and spatial placement and motion consistency. The standard pipeline gets some of these right — refractoriness is already implemented, and motion-aware injection exists — and leaves others untouched.

**The concrete question is therefore two questions, and the project can answer one without the other:**

1. **Absolute-score validity.** Does adding a named realism property change measured accuracy, precision, recall, or unit classification enough that published hybrid scores would need reinterpreting, *even if every sorter is affected equally*?
2. **Comparative validity.** Does the **sorter × realism interaction** change the sign, the order, or the practical separation of a sorter comparison?

The second is the one the field's practice depends on, because hybrid benchmarks are mostly used to choose between sorters rather than to state an absolute number. A realism effect that shifts every sorter equally invalidates the absolute numbers while leaving every ranking intact. A smaller effect concentrated on low-SNR or bursty units could leave the average almost unmoved and still reverse a ranking. **Both must be reported, separately.**

Both are answerable because the hybrid pipeline accepts a caller-supplied sorting and a queryable template database, which means each realism axis can be varied in isolation without rewriting the injection engine.

---

## Slot 3 — The transferable claim

If the project succeeds, we can say:

> **Holding the host recording, target placement zones, injected amplitudes, unit count, total spike count, and paired randomization blocks fixed — and holding donor identity fixed whenever the axis permits — adding a named realism property to the standard SpikeInterface hybrid generator changes measured spike-sorting accuracy by a bounded amount and changes the between-sorter comparison by a bounded amount, conditional on the tested host, sorter panel, and axis magnitude; those bounds are either inside or outside a pre-declared decision-relevant range.**

The claim is transferable because the manipulation is defined against the pipeline the field actually uses, at a pinned commit, with the axis-compatible nuisance variables held fixed or matched by construction and every deliberate departure from the anchor configuration recorded. Users of comparable pipeline configurations inherit evidence inside the tested host, sorter-panel, and manipulation boundaries; they do not inherit an unqualified universal answer.

**The claim is a bound, not a direction.** It is written so that a negative result satisfies it exactly as well as a positive one, which is the point: the number this project produces is an interval on the interaction, and the scientific content is where that interval sits relative to the pre-declared band in Slot 11.

---

## Slot 4 — Constraints

The claim above is reachable only inside a fairly tight set of bounds, and naming them here is what makes Slots 7 and 9 honest rather than aspirational.

**Compute — the binding constraint.** The work runs on one shared desktop: AMD Ryzen 7 8700F (8 cores / 16 threads), NVIDIA RTX 5060 Ti with 16 GB VRAM, 32 GB DDR5 (31.67 GiB usable), 1 TB NVMe. **Other Dandelion research projects run on this machine at the same time and are not coordinated with this one.** There is no scheduler and no reservation. Free memory is therefore a measurement that changes underneath the project, not a budget allocated to it. A pre-project feasibility run showed Kilosort4 completing a full 61.5-minute, 96-channel recording in 818 s with a peak of 29.3 GiB system RAM — but at two separate moments during Sessions 1 and 2 the machine had only 3.5–4.5 GiB free, at which point that same run would have failed slowly and confusingly. **The operative rule: measure free RAM and VRAM immediately before every heavy step, compare against a measured requirement rather than an estimate, and do not start what does not fit.** Prefer the smaller sufficient run.

**Budget.** Zero. Only open-source tools and freely available datasets. No paid compute, no paid API, no paid dataset.

**Licensing.** As Slot 1: commercial-use-permitting licenses by default; Kilosort4 called, never vendored; anything whose license is unclear is unusable until resolved.

**Data handling.** No raw data is redistributed. Recordings are referenced by identifier and downloaded by the reader, which is what the packet's `DATA.md` is for. ~49.7 TB is the collection size; the project pulls a deliberately small pinned subset.

**The director is asynchronous, not absent.** Randy drives for a living on weekdays and reads in the evenings and at weekends; expect days, not hours. `director_requests.md` works and he answers it, but **every request must carry a fallback and the session must keep moving.** A blocked request is not a stopped session. The Claim Sheet's own director review is explicitly non-blocking.

**Time.** No deadline and no revenue clock on this project. That is a real freedom and it is also not a licence to sprawl: the efficiency standard applies, and the project runs until it reaches the stopping point defined in Slot 14.

**Scope boundaries, restated because they are easy to drift across.** This project is not asking which spike sorter is best; sorter identity is a variable, not the subject, and any ranking it produces is evidence about the grading method rather than a recommendation. It is not asking whether Kilosort4 is accurate — absolute accuracy against hybrid data is precisely the quantity whose meaning is in question, so reporting it as ground truth would assume the conclusion. It is not building a new hybrid generator; where an axis must be implemented, it is implemented to the minimum needed to vary that axis against a pinned upstream commit. It is not a replacement for real paired ground truth. And it is not a judgement about the maintainers, who named this limitation themselves, in print.

---

## Slot 5 — Methods or approach

The constraints above rule out matching the anchor benchmark's scale — its authors estimated 870 and 846 single-workstation hours for their two sorter comparisons. This project buys its precision from **pairing** instead of from N: the same host recording, target placement zones, amplitude targets, unit count, total spike count, and paired randomization blocks across arms, with exactly one property changed. Tiers B and C additionally hold donor-template identity fixed. Tier A cannot hold donor identity fixed because donor region is the manipulation; it instead uses covariate-matched donor pairs, reuses the same spike train and placement within each pair, and treats the pair rather than either donor as the paired unit. A paired design on one desktop can resolve a difference that an unpaired design would need many machines to see.

### The control arm

The control is **a pinned, faithful reconstruction of the anchor pipeline's default-generating mechanism**: templates drawn without conditioning on host region, Poisson spike times, a mean firing rate in the anchor's range, ten injected units per recording, the implemented refractory period, amplitudes rescaled into the anchor's 50–200 µV range, and motion applied by the same mechanism in every arm. It is not called an exact reproduction where this project deliberately adds anti-leakage exclusions, covariate matching, or a different host subset; every such deviation is recorded. Refractoriness is *already implemented upstream* and is therefore not one of our axes — it is part of the control.

### The three realism arms

Each tier is a separate one-axis experiment against that control. **The tiers are run in order, and never varied together**, because region identity changes static waveform shape and spatial footprint while the temporal tiers change firing statistics and within-unit waveform dynamics; moving both at once makes any effect unattributable. A combined arm is interpretable only after the component effects are known, and is therefore not part of the initial design.

- **Tier A — region-matched templates.** The realistic arm draws donors matching the anatomically annotated **injection zone** at their target probe depths. The primary control draws donors without conditioning on region, as the anchor pipeline does, while using predeclared matching to balance amplitude after rescaling, effective SNR in the host, probe geometry, placement feasibility, and provenance. A maximally distant-region arm, if later useful, is a labelled secondary stress test rather than a substitute for the anchor-like control. Configuration only.
- **Tier B — local population-rate coupling.** Injected spike trains are generated from a time-varying intensity driven by a **sorter-independent host-activity proxy computed once from the unmodified host recording**, so neither comparator supplies the generator's target. Conditional sampling or an equivalent construction holds each injected unit's total spike count, mean rate, and refractory behaviour fixed across arms. This is the anchor authors' own proposed remedy, and it has prior art: the Kilosort4 hybrid benchmark modulates exponential inter-spike intervals by local population rate in 100 ms bins.
- **Tier C — bursting with spike-history-dependent waveform attenuation.** Injected trains carry burst structure at biologically bounded parameters, and the injected waveform amplitude is attenuated as a function of recent inter-spike interval. Both halves are required: timing-only bursts without the waveform coupling would be an incomplete manipulation, because the sorter-relevant mechanism is that a real neuron's waveform depends on its own firing history and a fixed average template's does not. The current quantitative prior (including ≤6 ms CA1 complex-spike bursts) is **region- and cell-class-specific**: Tier C either uses a compatible CA1 host/injection zone or first secures primary evidence for the selected host region and declares those bounds. CA1 parameters are never presented as generic brain-wide biology.

### The sorter panel

**Kilosort4 plus at least one mechanistically different CPU sorter** from SpikeInterface's internal set. This is a scientific requirement, not a preference. A Kilosort4-versus-Kilosort2.5 panel shares a family and a drift-correction lineage, and the anchor's companion paper flags that hybrid data injected with motion-corrected templates advantages sorters using the same motion correction — so that panel is the pairing *least* likely to show a ranking change, and a null from it could be read as designed-for. Sorter families diverge most on **collision handling**, along template-matching versus density-based lines, which is exactly the behaviour the temporal tiers stress.

Whether this machine can afford a third sorter is an open empirical question that a **pilot decides** (Slot 9), and published runtimes from other hardware are not a substitute for measuring here. The fallback is pre-declared rather than negotiated later: **if no third sorter fits inside the pilot's budget, the project runs two, and the narrower panel becomes a stated limitation that bounds the claim.**

**Sorter parameters are pinned defaults, identical across arms, and never tuned per condition.** Tuning a sorter on a realism condition would leak test-condition information into the study. If any calibration is needed at all, it happens on a predeclared calibration segment that is disjoint from every comparison recording.

### Baselines, including the strongest non-signal control

Three comparison points:

1. **The anchor default** — the control arm above, which is what the field currently uses.
2. **A published-scale reference** — the anchor's own Kilosort4-versus-Kilosort2.5 effect sizes (Cohen's *d* 0.276 on NP1.0, 0.408 on NP2.0). **These are contextual calibration only.** They establish that sorter-versus-sorter differences in this domain are small-to-moderate, which tells the project how much precision it needs. They are *not* a threshold: they are standardized over a different sample and variance structure and cannot be compared mechanically against a raw accuracy change measured here.
3. **The negative-control replicate band — the strongest non-signal control.** For each tier, matched pseudo-arms are generated under the **same nominal condition** using the same selection and generation procedure but independent nuisance draws. Their sorter-by-pseudo-arm interactions show how much apparent interaction template selection, spike-time seeds, and placement seeds can create without any realism manipulation. The real control-versus-realistic contrast is generated in paired randomization blocks: nuisance draws vary *between* blocks but are shared or matched *within* a block as the axis permits. The primary confidence interval already incorporates between-block variation; the negative-control band is a diagnostic and visual negative control, **not a second p-value and not a replacement for the pre-declared materiality band in Slot 11**. If the pseudo-arm interactions are as large or unstable as the claimed realism interaction, the study adds replicate blocks or reports the result as unresolved. A five-block start is a feasibility tranche, not a claim that five observations estimate a tail usefully. **Pseudo-arms are sorter runs, not generator-only runs**, and their block count matches the real contrast's, so the band and effect begin from the same nominal replication basis; equal block counts do not guarantee equal precision, and each interval's achieved width is reported. Slot 9's pilot admission budget accounts for both.

---

## Slot 6 — Application and downstream relevance

The immediate beneficiaries are the people who read and produce spike-sorting benchmarks. A researcher choosing a sorter for a new recording, a lab deciding whether to migrate pipelines, and a reviewer weighing a benchmark claim all currently rely on hybrid accuracy numbers whose sensitivity to generator realism is unmeasured. This project measures it, in either direction, and gives them a bound.

The maintainers benefit specifically and directly: they named this as an open question in print, and this is evidence they do not currently have. If the answer is that realism does not move rankings, that is independent support for continuing to use the pipeline as-is. If it does move them, the axes that move it are named, the magnitudes are bounded, and the implementations that produced the manipulation are released — which makes it actionable rather than merely critical.

The wider relevance is that spike sorting sits underneath a large amount of systems neuroscience, and underneath essentially every future neural interface that has to decide which cell fired. A benchmark that grades the generator rather than the algorithm propagates quietly into every decision made on top of it. Measuring that is cheap relative to what rests on it.

**For Dandelion specifically**, this project is a validation-methodology result rather than a device: it feeds future work by establishing whether a widely used proxy can be trusted, and by producing a reusable, licence-clean measurement harness for benchmark-realism questions. It is also a deliberate test of whether this framework can produce a rigorous, honest, checkable result on a shared desktop with no budget — which is the operating question underneath every project here.

---

## Slot 7 — Materials and evaluation design

This is the team's confidence path: exactly how we will know whether the claim in Slot 3 holds.

### Host and injection-zone selection — constrained by donor availability

An audit of the live template metadata in Session 2 supplies a **conservative necessary screen**, not a finished paired-arm feasibility result. Under provisional donor-metadata calipers of amplitude **50–200 µV** and SNR **5–15**, 1,149 of 2,183 Neuropixels 1.0 templates survive across 149 brain-area labels, and 37 labels hold at least 10 templates. Dropping each area's single largest contributing dataset — the worst possible exact-dataset exclusion for that area — leaves 7 labels with at least 10: CP (42), PIR (19), SUB (18), VISa5 (17), AId5 (14), MRN (14), ENTl5 (10). Thirteen of the 37 collapse to zero in that worst case.

Those counts narrow the search, but they do **not** prove that a matched and region-unaware arm can be constructed together. The leave-largest number applies only when the selected host corresponds to that area's largest donor source; any other exact host-dataset exclusion can leave more templates. The audit also does not test pairwise covariate balance, anatomical placement feasibility, or the control pool. The actual host-specific query therefore excludes the exact host source first and reports the resulting count rather than substituting the worst-case shortlist as fact.

The metadata calipers are provisional screening parameters. In particular, the anchor's 50–200 µV range is an **injection rescaling target**, not evidence that donor templates must already have amplitudes in that range. Final eligibility and balance are evaluated on the waveform after rescaling and relocation in the selected host, including effective SNR against that host's measured noise; donor amplitude/SNR remain quality and matching diagnostics, not proxies for the injected result. The audit is re-runnable via `Reproducibility Packet/scripts/audit_template_library.py`.

A Neuropixels penetration crosses multiple anatomical regions, so the design never assigns one brain-area label to an entire recording. **Each Tier A host must carry a pinned anatomical channel/trajectory mapping and a predeclared injection zone (or set of depth-specific zones).** Region matching is between each donor label and the local host label at its target placement. If ten feasible placements cannot be supported without overcrowding or label ambiguity, that host fails the Tier A gate rather than having a convenient whole-recording label invented for it.

**Host recordings are additionally screened** for: quantified drift below a pre-declared threshold (or, failing that, identical measured motion applied across every arm with a drift-following manipulation check), documented channel geometry, documented noise level, and adequate duration. Selected hosts are pinned by DANDI asset identifier; anatomical mapping and injection-zone identifiers are pinned with them. Selected templates are pinned by `template_index` against a metadata snapshot pinned by SHA-256 — the table is hosted mutably, and a result built on "latest" is not reproducible however good the analysis code is.

**Covariate balance across arms is a gate, not a hope.** Region-matched and region-unaware arms are balanced on post-rescaling amplitude, effective host SNR, probe geometry, depth/placement feasibility, **and the number of contributing source datasets**. That last one is not optional: excluding the host's own dataset bounds leakage but does not prevent provenance from riding along with region, and an arm drawn from five source datasets compared against an arm drawn from one is partly a provenance comparison wearing a region label.

**One host and injection zone across all three tiers, by default.** The tiers are separate one-axis experiments, but they are not independent results: Slot 13.2 reasons from a Tier A outcome to what it does and does not license about Tiers B and C, and Slot 14 requires Tier A and Tier B together as the minimum scientific content. A host that changes between tiers makes every cross-tier statement a comparison across recordings as well as across axes. **If a tier must move to a different host, that is recorded as a limitation and the cross-tier comparison is dropped rather than made across hosts.**

That default couples two constraints introduced separately in this sheet, and the coupling is binding rather than incidental. Tier A needs a zone whose donor pool survives the host-specific source-dataset exclusion; Tier C needs a zone whose burst and history-dependence bounds rest on primary evidence, and the current prior is CA1-grounded. **CA1 is the only zone in the Session 2 audit that satisfies both on their face** — 12 in-caliper Neuropixels 1.0 templates across 4 source datasets before any host-specific exclusion. That is a candidate, not a decision: CA1's worst-case leave-largest count is 6, below the ten-unit budget, so its viability depends entirely on which source dataset the selected host belongs to — precisely the host-specific query required above. It is named here so that host selection is run against **both** constraints at once, rather than satisfying Tier A and then discovering that Tier C cannot use the host it chose.

### Injected-unit budget

Ten injected units per recording instance, matching the anchor. **Statistical power comes from paired arms, randomization blocks, and multiple host recordings — never from raising the injected-unit count**, because more simultaneous injections change the collision and density statistics of the recording itself, which is the thing being held fixed.

### The manipulation check — a stop-or-go gate

**Before any sorter time is spent on a tier, the generated data must demonstrate that the intended property actually changed, at a realistic magnitude.** Without this, a null result is a statement about our implementation rather than about the field's method, and there is no way to tell the two apart afterwards. The criteria are axis-specific:

| Tier | Passes when… |
|---|---|
| **A — region** | pre-declared multichannel waveform features separate region-matched from region-unaware donor sets, while post-rescaling amplitude, effective host SNR, probe geometry, placement, and source-dataset count remain balanced. Features chosen so as not to be simply the sorters' own decision variables. |
| **B — population coupling** | the injected units' rate trajectory tracks the sorter-independent host-activity proxy to a pre-declared similarity criterion, while total spike count, mean firing rate, and refractory-violation rate are unchanged from control. |
| **C — burst / history** | the short-ISI distribution and the history-dependent amplitude attenuation both fall inside pre-declared **host-region/cell-class-appropriate** biological bounds, while total spike count and long-timescale mean rate are unchanged from control. |

**If a check fails, no sorter run starts for that tier.** The failure is diagnosed and reported as a generator finding; it is never papered over and pushed downstream.

### Outcome metrics

The evaluator is SpikeInterface's ground-truth comparison at a pinned commit. The minimum reported set, per arm, per sorter:

- per-unit **accuracy, precision, and recall** (accuracy defined as n_match / (n_match + n_miss + n_fp));
- **counts of well-detected units** at a pre-declared threshold (0.8, the field convention) — because a mean hides whether a manipulation nudged everything slightly or moved a few units across a line;
- counts of **false-positive, redundant, overmerged, and oversplit** units;
- **collision / short-ISI recall**, required for the temporal tiers, because that is the documented axis of divergence between sorter families;
- everything **stratified by SNR and amplitude**, and by the manipulated property itself, with the strata pre-declared. A realism effect concentrated in low-SNR units — the stratum the anchor found sorter differences strongest in — would vanish from an aggregate median.

**No condition-aware curation.** The primary analysis uses every returned unit under identical automated rules across arms. Any curated analysis is secondary, and blinded to condition where practical.

### The estimand and the decision rule

For paired unit or donor-pair slot *u*, host–zone *r*, randomization block *b*, sorter *s*, and realism condition *c*, with accuracy *A*:

- the **paired realism effect** for a sorter is `Δ_s = A(u,r,b,s,realistic) − A(u,r,b,s,control)`;
- the **primary comparative estimand** is the mean paired **difference in differences**, `I(s1,s2) = mean_r(mean_b(mean_u(Δ_s1 − Δ_s2)))`: units are averaged within a block, blocks within a host, and hosts equally across the tested set.

For Tiers B and C, *u* is the same donor template, placement, and total spike count in both arms. For Tier A, *u* is a predeclared covariate-matched donor-pair slot with the same spike train, placement, and rescaled amplitude target; the two donors differ by definition, and the pairing claim is about the matched slot rather than a fictitiously unchanged unit identity. Mean per-unit accuracy is the primary continuous summary; medians, 0.8-threshold counts, and unit classifications are reported as secondary summaries rather than silently substituted for it.

The realism main effect, the sorter main effect, and the interaction are reported **separately**, because a uniform loss invalidates absolute scores without touching rankings and a concentrated differential loss does the opposite.

Uncertainty comes from a **hierarchical paired bootstrap over host–randomization blocks and their paired unit/donor-pair slots**, reported as 95% intervals on the raw quantities. Blocks, not individual spikes, are the independent replication unit; repeated donor identities are kept in the same resampling cluster. With one host, the interval is explicitly conditional on that host and resamples randomization blocks only — it cannot manufacture cross-host generalization. A five-block initial tranche is not treated as a reliable 95% tail estimate: blocks are added in predeclared batches until the interval is narrow enough for Slot 11 or the measured compute ceiling is reached. **Decisions are pre-declared in raw paired accuracy and rank units with their uncertainty; standardized effect sizes are reported secondarily and never as thresholds.**

With two sorters, "rank stability" is exactly the sign of their paired difference, and **the project will not decorate a two-sorter sign comparison with rank-correlation language.** Rank correlation is reported only if the pilot supports three or more sorters.

---

## Slot 8 — Director's verification path

The design above is how the *team* becomes confident. This slot is how the **director** becomes confident, without reading the Technical Report end to end and without domain expertise. It is committed to now, before execution, which also forces the work to be designed so that verification is possible at all.

**The artifact: a single self-contained script, `verify_realism.py`, that produces a two-panel figure and prints a plain-language verdict.** It lives inside the Reproducibility Packet, so anyone who downloads the packet verifies the result the same way the director does.

**Panel 1 — "Did the knob actually turn?"** This panel is tier-specific rather than forcing every axis into a burst plot:

- **Tier A:** the local host injection-zone label, the matched and region-unaware donor labels/waveforms, and compact balance plots for post-rescaling amplitude, effective host SNR, placement, and provenance;
- **Tier B:** the host-activity proxy and injected-rate trajectories over time, plus the mean-rate, total-count, and refractory checks; and
- **Tier C:** control-versus-realistic raw voltage snippets, inter-spike-interval histograms, and spike amplitude against preceding interval.

The director should be able to see both that the intended property changed and that the named nuisance quantities did not. **If the tier-specific views do not separate as predeclared, the manipulation did not pass and nothing downstream matters** — the stop-or-go gate rendered so a non-specialist can apply it.

**Panel 2 — "Did it change the answer?"** The same units' accuracy scores under each sorter, control versus realistic, with the two sorters' paired gap drawn in both conditions and **the negative-control replicate band shaded behind them**. The question the director answers by looking: how does the real interaction compare with the apparent interactions produced by matched pseudo-arms where no realism property changed? The printed interval and Slot 11 materiality band make the decision; the grey band is a negative-control diagnostic, not a visual significance test that turns every point outside it into truth.

**What the director does.** Run one command, look at two panels, read one printed sentence of the form *"Under [tier], the gap between [sorter A] and [sorter B] moved by X accuracy points (95% CI …), against a negative-control replicate band of ±Y and a decision margin of ±T. The ranking did / did not reverse; practical separation was / was not lost."* Then, if he wants, change a flag and re-run it on a different tier.

The artifact is **paced into the project rather than assembled in the final session**: Panel 1 is buildable as soon as any tier's generator passes its manipulation check, well before sorter results exist, and it is genuinely useful at that point because it is the visual form of the gate. If results change what the artifact should be, this slot is amended through the normal protocol.

---

## Slot 9 — Architecture and build plan

There is no trained model here, so "capacity" is the scale of the experiment: segment length, number of hosts, number of paired randomization blocks, and number of sorters. The ladder below governs it. **The smallest-sufficient rule applies to what the project finally ships and reports, not to the search that gets there** — a null from an undersized experiment is evidence about that experiment, not about whether the effect exists.

| Rung | Scale | Purpose | Gate to climb |
|---|---|---|---|
| **0 — Feasibility pilot** | ~60 s segment, 1 host, 10 injected units, every candidate sorter timed and memory-profiled on the same segment | Decide the sorter panel; measure real runtime and peak RAM/VRAM *on this machine*; smoke-test the harness end to end | Runs complete; measured peaks recorded |
| **1 — Manipulation check** | Generator only, no sorting | Prove the realism knob turns (Slot 7 gate) | Axis-specific criteria pass |
| **2 — Primary run** | ~10 min segment, 1 host, 10 units, 5 paired randomization blocks as an initial tranche **plus 5 matched pseudo-arm blocks for the negative control**, 2 sorters; add blocks in batches | Produce the first conditional interaction estimate and negative-control replicate band | Interval computed; continue if its precision is insufficient |
| **3 — Panel widening** | Rung 2 plus a third sorter | Break the shared-family limitation; enable rank language | Only if the Rung 0 pilot showed it fits |
| **4 — Host widening** | 3–5 hosts, longer segments | Narrow the interval; test whether the effect survives across recordings | Only on a Slot 11/13 trigger |
| **Ceiling** | Whatever the machine allows **as measured at the moment of the run**, never from a number written in a file — including this one | | |

Within Rung 2, add paired randomization blocks in fixed-size batches based on **interval width**, not on whether the point estimate looks favorable. Five is the initial resource measurement, not the final replication claim. **Climb the ladder when** (a) there is partial signal worth resolving, **or** (b) there is no signal yet *and* the interval is wide enough to still admit a decision-relevant effect. Rung 4 exists specifically for case (b): a null with a wide interval is inconclusive, not negative, and the response is more precision rather than a conclusion.

**Stop climbing only when** the result holds across rungs, or the measured hardware ceiling is genuinely reached, or there is a **scientific** reason more scale would not help — stated explicitly. "A bigger run wouldn't change it" is itself a claim requiring that reason; a budget reflex is not one.

**The pilot's own budget is pre-declared** so that a marginal result does not become a negotiation. Each candidate gets one 60 s admission run with a **60-minute wall-clock ceiling**. At launch, its monitored working set may consume no more than 75% of the free RAM or free VRAM measured immediately beforehand, and the stricter rule also preserves at least **4 GiB system RAM and 2 GiB VRAM** for the OS and other work; crossing either guard stops the run and records a resource failure. A candidate is admitted to Rung 2 only if its measured 60 s runtime extrapolates the minimum tranche to **≤48 sorter-hours per candidate per tier** and its measured peak fits the same live-headroom rule.

**The minimum tranche includes the negative control, because the negative control has to be sorted.** Slot 5's replicate band is built from sorter-by-pseudo-arm interactions, which means every pseudo-arm is a sorter run and not merely a generator run. The tranche is therefore **10 min × 2 arms × 5 blocks × 2 contrast types** — the real control-versus-realistic contrast and an equal number of matched pseudo-arm blocks — or **200 recording-minutes per candidate sorter per tier.** Declaring the pseudo-arm block count equal to the real block count is a judgement fixed here: it gives the band and the effect the same nominal replication basis without pretending their achieved precisions must be identical. Extrapolating admission from the real arms alone would understate the Rung 2 load by a factor of two, which is exactly the mid-Phase-2 renegotiation this budget exists to prevent.

**The panel-level total is recorded, not just the per-candidate one.** A panel can consist entirely of individually admitted sorters and still not fit: at the ceiling, two sorters across three tiers project to 288 sorter-hours. The pilot report states the projected per-candidate, per-tier, and whole-panel totals, and the live-headroom measurement is repeated immediately before Rung 2 begins rather than inherited from the pilot. These are efficiency judgements, declared before the pilot; changing them requires an amendment rather than an informal exception. A sorter that does not fit is dropped, named in the report as dropped, and the reason recorded. **If no third sorter fits, the project runs two and the narrower panel becomes a stated limitation** — pre-committing to the smaller honest panel now is what keeps it from being rationalized later.

**Software structure** follows the standards: one purpose per script, shared logic in an importable `utils/` module rather than copy-pasted, every input via `argparse` with no hard-coded paths, docstrings stating inputs/outputs/purpose, progress to stdout, loud informative failures, figures at ≥300 DPI with labelled axes and consistent styling, and every dependency pinned in `requirements.txt` **the moment it is installed**. Scripts are written **into `Reproducibility Packet/` as they are finalized**, not relocated there at the end; the packet folder must itself hold everything its README tells a reader to run.

**Every exclusion is recorded the moment it happens** — a discarded run, a host that failed drift screening, a template dropped by the caliper, a sorter dropped by the pilot. Silent exclusions are a reproducibility failure.

---

## Slot 10 — Computational and physical environment

| | |
|---|---|
| **Machine** | The dedicated Dandelion AI-agents desktop — a shared workbench, not the director's personal computer |
| **OS** | Windows 11 Home, build 26200 |
| **CPU** | AMD Ryzen 7 8700F — 8 cores / 16 threads |
| **GPU** | NVIDIA RTX 5060 Ti, 16 GB VRAM (16,311 MiB), driver 581.95, capability `sm_120` |
| **RAM** | 32 GB DDR5 (31.67 GiB usable) |
| **Storage** | 1 TB NVMe on `C:`, external SSD on `D:` |
| **Python** | 3.12.10, in the project-root `venv`, invoked **only** as `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe` — never bare `python` or bare `pip`, which pick up whatever interpreter the shell happens to have |
| **CUDA** | **No system-wide CUDA toolkit**; `nvcc` is not on the path. GPU builds come from pip wheels carrying their own CUDA runtime — the feasibility run used PyTorch 2.11.0+cu128. Do not assume a system CUDA; verify GPU availability rather than assuming it. |
| **Known-good stack** | Kilosort 4.1.7, SpikeInterface 0.104.8, PyTorch 2.11.0+cu128, CUDA 12.8 — measured working on this machine before the project began |
| **Current venv state** | Only `pip` and the standard library. No `requirements.txt` yet; it is created at first install, with versions pinned at that moment. |

**The measured feasibility point, with its boundary attached.** One complete raw DANDI 000409 AP stream — 110,725,295 samples, 96 channels, 30,000.2045 Hz, 3,690.818 s — converted in 197.9 s and sorted by Kilosort4 in 818.8 s, returning 143 units and 1,562,847 spikes, peaking at 29.262 of 31.665 GiB system RAM and 3,282 of 16,311 MiB VRAM with zero CUDA OOMs. **That proves one full recording of one probe type on an otherwise-quiet machine.** It does not prove a 384-channel or three-hour case, and it proves nothing about running while another project is using the machine.

**Which is the constraint that actually governs.** Free memory is a measurement, not a property. It was 3.46 GiB free at 08:22 PDT on 2026-08-11 while this repository was being created, and 3.96 GiB free at 12:07 PDT during Session 2 — against a feasibility run that peaked at 29.3 GiB. Started at either moment, that run would have failed. **Measure at the moment of the heavy step, compare against a measured requirement, and if it does not fit, wait and re-measure or do smaller work that does fit.** Record what was measured in the session report, so the next session inherits evidence rather than a hunch. Nothing in this project is designed on the assumption that it owns the whole machine.

---

## Slot 11 — What would count as success

**Pre-declared, before any result is observed.**

Success is **a bounded answer**, not a detected effect. Concretely, the project succeeds when, for each tier attempted:

1. the **manipulation check passed** (Slot 7), so the arm demonstrably differs in the intended property and only in it;
2. the covariate-balance and leakage gates passed, so the arms differ in the manipulated property and not in amplitude, SNR, probe geometry, placement, or dataset provenance;
3. a **95% interval on the sorter × realism interaction** exists, computed by the hierarchical paired bootstrap defined in Slot 7;
4. the derived comparative quantity `D = |I| − T` has a 95% interval wholly below zero for a bounded negative, or wholly above zero **with the interaction interval also excluding zero** for a bounded positive, so the result actually decides something; and
5. the **negative-control replicate band** was estimated from the same design and is stable enough to show whether nuisance selection and seeds can mimic an interaction of the observed size.

### The decision-relevant band

The band is defined against quantities **measured inside this experiment**, not imported from another study.

- **Absolute-score materiality.** A realism main effect on accuracy of **|Δ| ≥ 0.05** — five points of the standard accuracy metric — is material for absolute scores. Rationale: the field reports counts of units above a 0.8 accuracy threshold, and a shift of this size near that threshold moves units across it, changing the reported number of well-detected units.
- **Comparative materiality.** Let `G0` be the mean paired sorter gap in the control arm and define the raw interaction margin `T = max(0.05, 0.5 × |G0|)`. The five-point floor prevents a near-zero control gap from making a trivial sign change look decision-relevant; the half-gap term asks whether realism moved a meaningful fraction of the comparison actually observed. Because `G0` is estimated, the hierarchical bootstrap recomputes `G0`, `T`, and `D = |I| − T` in every resample. A comparative effect is bounded positive only when the 95% interval for `D` lies wholly above zero and the interaction interval excludes zero; it is a bounded negative only when the interval for `D` lies wholly below zero. An interval for `D` crossing zero is inconclusive at the achieved precision. Both 0.05 and 50% are declared judgements, fixed here before results.

**The `D` rule is the authoritative form of the comparative decision, and it is the only one.** Saying "the interaction interval lies inside `[−T, T]`" is the same statement *within a resample* — `|I| < T` and `I ∈ (−T, T)` are the same event — but as *interval* statements the two are different operations: one is a joint interval on a derived quantity that carries the uncertainty in `G0`, the other compares a marginal interval on `I` against a point estimate of `T`. Where this sheet uses the `[−T, T]` phrasing it is shorthand for the `D` interval, never a second test. Fixing which operation is meant is the sort of thing that must be settled before results exist, not chosen afterwards from two defensible options.

**One consequence of that choice is declared now rather than discovered later.** `D` is built on `|I|`, whose bootstrap distribution is folded at zero, so when the true interaction is near zero the resampled `|I|` sits above it on average. That bias pushes `D` upward and therefore makes the **bounded-negative** declaration harder to reach, not easier. The rule is conservative in exactly the direction that matters — it will call a genuine null "inconclusive" before it calls noise a null — and the achieved bound is reported either way per Slot 13.1.

Once the interaction clears that materiality rule, the project describes which decision event occurred:

  - **Reversal.** The arm-specific paired sorter gaps have opposite signs, and at least one is separated from the practical-equivalence region `[-0.05, 0.05]` by its 95% interval.
  - **Loss (or gain) of practical separation.** One arm's sorter-gap interval lies wholly outside `[-0.05, 0.05]` while the other's lies wholly inside it, and the interaction interval excludes zero. Merely having one interval include zero and another exclude zero is **not** evidence that the two arms differ.
  - **Large non-crossing shift.** The ranking does not reverse and neither arm becomes practically tied, but the interaction still clears `T`.

**A clean negative satisfies this slot completely.** If the manipulation demonstrably turned, the 95% interval for `D` lies wholly below zero, and the negative-control replicate band is stable and does not reveal nuisance interactions of decision-relevant size, then the project has bounded the realism effect below its declared decision threshold for that tier, host set, and sorter panel. **That is a success and is published on exactly the same terms as a positive result.** It validates the proxy only inside those tested boundaries; broader validation requires the host/panel widening named elsewhere in the sheet.

---

## Slot 12 — What would count as failure

Also pre-declared. **A clean failure is still a public artifact**, and each of these is reported with its diagnosis rather than quietly absorbed.

The distinction that matters: *a scientific negative is not a failure.* Realism not moving the rankings is a result (Slot 11). Failure is the project being unable to produce a bounded answer at all.

1. **The manipulation check cannot be made to pass.** The generator will not produce data with the intended property at realistic magnitude — bursts that do not reach biological ISI ranges, attenuation that cannot be bounded, injected rates that will not track the host population. **Published as a generator finding**, with what was attempted and where it broke, because "this axis is harder to implement than it looks" is useful information about the field's ability to make hybrid data more realistic at all.
2. **Precision is unreachable.** The compute allows no rung of the Slot 9 ladder to produce an interval narrower than the decision band, and the ceiling is genuinely reached. Reported as **inconclusive with the achieved bound stated** (see Slot 13), plus an honest account of what scale would be required.
3. **Donor feasibility collapses.** No candidate host/injection-zone combination admits both a region-matched and a balanced region-unaware arm without confounding post-rescaling amplitude, effective host SNR, geometry, or provenance. Tier A is dropped, the reason published, and the project proceeds on Tiers B and C.
4. **A confound is discovered after the fact.** Analysis reveals that the arms differed in something besides the manipulated property. The affected work is moved to a dated `archive/` folder, an amendment is written, and the finding is reported as invalidated rather than silently dropped.
5. **The harness cannot be made reproducible.** The packet will not run end-to-end on a fresh environment, or upstream moves in a way that cannot be pinned. Reported with the exact obstacle.

**What is not failure, and will not be reported as such:** a negative result; an effect smaller than expected; a two-sorter panel because a third did not fit; or completing only Tier A and Tier B if Tier C's implementation proves out of reach — provided the boundary is stated in the claim.

---

## Slot 13 — What would count as inconclusive or non-transfer

The "not this, not yet" shapes, recorded so that a partial win is not reported as a full one. **These are the conditions under which this project must decline to answer its own headline question**, and they are written down now because they are much harder to concede later.

1. **A wide interval is inconclusive, not negative.** If the 95% interval on the interaction includes both zero and a decision-relevant magnitude, the answer is *"not resolved at this precision,"* with the achieved bound stated explicitly. **A null result with a wide interval will never be reported as evidence that realism does not matter.** This is the single most likely way this project could mislead, and it is the one this slot exists for.
2. **A Tier A null licenses nothing about Tiers B and C.** Region mismatch changes static waveform shape and spatial footprint, which sorter front ends consume in broadly similar ways. The temporal tiers change firing statistics and within-unit waveform dynamics, which hit **collision handling** — the documented axis of divergence between sorter families. The honest prior is therefore that **Tier A is the most likely to move absolute accuracy and the least likely to move the interaction.** Because Tier A runs first and is cheapest, there is a live risk of the project appearing to have answered its headline question when it has answered the cheapest version of it. **The project is not concludable on Tier A alone**, and a Tier A result is reported as a Tier A result.
3. **A Kilosort4-favouring Tier B interaction is inconclusive on attribution.** The Kilosort4 hybrid benchmark *already* modulates inter-spike intervals by local population rate. Adding population coupling to the SpikeInterface pipeline therefore moves the test data toward Kilosort4's home benchmark. If Kilosort4 gains relative to the others under Tier B, "more robust to realistic firing" and "developed against data that already had this property" cannot be separated by this design. Declared now, before any result: **that outcome is reported as inconclusive on attribution, not as a clean positive.** This is the same circularity the companion paper raises about motion correction, pointed at a different mechanism.
4. **Two sorters means no rank-correlation claims.** With a two-sorter panel, the only comparative quantity is the sign and size of one paired difference. Rank-correlation language is reserved for a panel of three or more.
5. **One host means no cross-region or cross-probe transfer.** A result from a single host recording, injection zone, and probe type is a result about that configuration. Generalization requires Rung 4 of the ladder, and absent it the claim carries the boundary.
6. **A manipulation check that passes weakly is a bounded manipulation.** If the realism property is present but at a magnitude below the biological range, any null is a statement about *that magnitude*, and is reported with the achieved magnitude attached.
7. **Tier C's biological bounds do not transfer across regions or cell classes by default.** The current ≤6 ms/history-dependent prior is grounded in CA1 complex-spike biology. A Tier C run elsewhere requires primary evidence for that host region/cell class or is explicitly labelled a synthetic stress test rather than a biological-realism test.
8. **Non-transfer to real ground truth is assumed throughout.** Nothing here substitutes for paired juxtacellular/extracellular recordings, which answer a different and harder question. A finding that a hybrid benchmark is or is not realism-sensitive says nothing directly about how either compares to real ground truth.

---

## Slot 14 — Minimum public artifact required to conclude

The project is not finished when the work is done; it is finished when the work is shippable. Four artifacts, all required:

**1. Technical Report** (LaTeX, for the field). Required contents, which this slot fixes now:
- the anchor's open question, quoted, with the pipeline version and commit under test;
- the full generator configuration of every arm, including seeds, template row identifiers, the metadata snapshot hash, host asset identifiers, and every sorter parameter;
- the **manipulation-check results, reported before the sorter results** — magnitudes achieved, criteria pre-declared, pass or fail;
- the realism main effect, the sorter main effect, and the **interaction, reported separately**, with paired bootstrap intervals in raw units, and standardized effects secondary;
- the **negative-control replicate band**, plotted alongside every effect and described as a diagnostic rather than a second significance test;
- results stratified by SNR/amplitude and by the manipulated property;
- **every exclusion named with its reason** — discarded runs, screened-out hosts, caliper-dropped templates, pilot-dropped sorters;
- the Slot 13 limitations, stated as limitations rather than buried;
- the reconciled bibliography from both agents' `references.md`.

**2. Accessible Piece** — the same result for a reader with no technical background, honest and engaging, and the artifact the director shares publicly at the close.

**3. Reproducibility Packet** — self-contained: code, pinned `requirements.txt`, configurations, `DATA.md` with dataset access and the CC-BY/MIT attribution obligations, a top-level runbook README, the exclusions log, the pinned metadata snapshot, and **the Slot 8 verification artifact**. Validated by copying the packet folder alone to a clean environment and running it end to end.

**4. Study Guide**, both passes — Pass 1 (Conceptual Foundation) at Phase 1 close, Pass 2 (Concept Delta) at Phase 3 under the no-spoiler rule.

**The minimum scientific content required to conclude:** Tier A and Tier B each carried to either a bounded interaction estimate or a documented Slot 12 failure, with manipulation checks reported either way. **Tier C is required if its generator passes its manipulation check; if it cannot pass at biologically justified magnitude, it is reported as a documented generator failure, not as a bounded sorter result.** The project may not conclude on Tier A alone (Slot 13.2).

Because this is an **agent-selected run** — the question came from the agents' own search, not from the director — the **run-provenance disclosure block is required** on the public artifacts, in the wording fixed by `Playbooks/live-run-readme.md`, and it stays above the result rather than below it.

---

## Slot 15 — Possible monetization paths

**Thin slot, honestly.** This is validation methodology, and validation methodology is not a product.

**As scoped: none identified.** The natural home for the result is a public report and an upstream contribution, and the natural users are researchers who would not and should not pay for it. Charging for it would also undercut the point of doing it.

**If it succeeded and scaled**, the only paths worth naming are indirect and speculative, and are recorded as possibilities rather than plans: a general **benchmark-realism auditing harness** — "how sensitive is your benchmark to how you generated it?" — is a reusable tool beyond spike sorting, and the same question recurs anywhere synthetic ground truth stands in for real ground truth. Any such path would have to clear the same affordability bar as everything else Dandelion builds.

**What the project is actually worth to Dandelion is not revenue.** It is a public, checkable artifact demonstrating that this framework can take a maintainer-stated open question, execute it rigorously on a shared desktop with no budget, and publish the result at its true strength in either direction. That is the asset.

---

## How this contract changes

Real research surfaces what a contract did not anticipate. When it does, the agent who finds it writes an **amendment proposal** — what was found, why it changes the path, the new path, and the new success, failure, and non-transfer shapes — and the other agent approves or rejects before execution shifts. An approved amendment is **appended and dated, never written over the original.** If it invalidates completed work, the affected files move to `archive/YYYY-MM-DD-<short-reason>/` and the amendment points at that folder. Nothing is deleted.

The director's review of this sheet is the first invocation of that protocol, and it is **non-blocking**: the agents keep working while it is pending, and the project can run to conclusion without it. The Accessible Claim Sheet is kept in sync with this document; amending one without the other is a defect.
