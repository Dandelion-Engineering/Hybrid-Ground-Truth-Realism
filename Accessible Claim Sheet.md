# Accessible Claim Sheet — Hybrid Ground Truth Realism

**The director's companion to `Claim Sheet.md`.** Same contract, same commitments, same numbers, plain language.

This is not a summary and it is not a softer version. Every promise the technical Claim Sheet makes is in here, including the uncomfortable ones — what would count as failure, what would count as *"we could not tell,"* and the specific ways this project could mislead someone if it were written carelessly. If the two documents ever disagree, that is a defect in this one, and the fix is to correct it rather than to prefer it.

It is written so you can read it start to finish, on its own, without the technical sheet open beside you. It follows the same fifteen-slot order, so if you ever want the technical version of a section you can jump straight to the matching slot.

---

## The question, in one page

Neurons talk by firing brief electrical pulses — **spikes**. If you slide a thin probe into brain tissue, the metal contacts on it pick up those pulses from every neuron close enough to be heard, all summed together into one messy voltage trace. Modern probes ([Neuropixels](https://doi.org/10.1038/nature24636)) carry hundreds of contacts on a single shank, so a single neuron shows up on several neighbouring contacts at once, at different strengths.

Turning that mess back into *"neuron 17 fired at 12.483 seconds"* is called **spike sorting**, and it is done by an algorithm — a **spike sorter**. Almost everything else in systems neuroscience is computed on top of the sorter's output. If the sorter is wrong, so is everything downstream, and usually silently.

Here is the problem. **For a real recording, nobody knows the right answer.** There is no independent record of which neuron actually fired. So the field cannot simply grade a sorter against the truth — there is no truth to grade against.

What it does instead is manufacture one. Take a genuine recording, and **inject extra, synthetic spikes into it** at times you chose yourself. Now you have an answer key, at least for the spikes you added. Run the sorter, count how many of your planted spikes it found, and call that its accuracy. This is a **hybrid recording**, and it is the method the field actually grades on ([overview of all three ground-truth strategies](https://doi.org/10.1088/2516-1091/ac6b96)).

That works only if the injected spikes are enough like real ones. If they are easier to find than real neurons, every sorter scores too well. And if they happen to be easier for *one kind* of sorter than another, then a comparison between two sorters is partly measuring **the thing that made the fake spikes** rather than the sorters.

The people who built the field's standard hybrid pipeline wrote, in the Limitations section of their own paper, that they do not know whether their synthetic spikes are realistic enough ([Buccino et al., 2026, *eLife*](https://doi.org/10.7554/eLife.110170.3)):

> "It remains to be tested whether generating more realistic hybrid recordings will have any effect on spike sorting accuracy."

**This project tests that sentence.** It takes their pipeline, changes the realism of the injected spikes one property at a time — along axes they themselves named — holds everything else fixed or matched, and measures two things: whether accuracy moves, and, more importantly, whether the *comparison between sorters* moves.

**Both answers are worth publishing, and this is unusually comfortable ground.** If realism does not move the comparison, the field's default answer key is validated and a stated open question closes. If it does move it, then published sorter comparisons built on hybrid data have been partly grading the generator, and every benchmark that used one inherits that. There is no result here that is a disappointment — only a result too imprecise to be either, which the project takes seriously enough to have written rules against in advance.

**One writing commitment, made now.** If realism *does* move the rankings, that disagrees with a position an active maintainer has stated in print. The report is written as *"we tested the limitation you named, and here is what we found"* — never as *"you were wrong."* That is a rule about tone, not a licence to soften the result, which is reported exactly as measured either way.

---

## The contract at a glance

| | |
|---|---|
| **What we are measuring** | Whether making injected spikes more realistic changes accuracy — and whether it changes it **by different amounts for different sorters**. That second quantity is the one the field's practice actually depends on. |
| **What we are measuring it on** | Real recordings from [DANDI 000409](https://dandiarchive.org/dandiset/000409) (a public brain-wide mouse dataset), synthetic spike shapes from the [public template library](https://github.com/SpikeInterface/hybrid_template_library), all run through [SpikeInterface](https://doi.org/10.7554/eLife.61834) — which supplies the generator, the sorter interface, *and* the scoring — with [Kilosort4](https://github.com/MouseLand/Kilosort) plus at least one mechanically different sorter as the panel. |
| **What we compare against** | A faithful rebuild of the standard pipeline's current settings, plus a **negative control**: fake "comparisons" where nothing was actually changed, which show how much apparent effect the machinery invents on its own. |
| **What counts as success** | A **bounded answer** for each realism axis attempted — a range of plausible values tight enough to sit clearly inside or clearly outside a threshold we defined *before* seeing any result. Success is a bounded answer, **not** a detected effect. |
| **What counts as failure** | Being unable to produce a bounded answer at all: the realism change cannot be made real, the machine cannot afford enough repetitions to get a tight enough range, or no usable recording can be found. |

---

# The fifteen slots

## Slot 1 — What we are working on, and with what

**The subject is a measuring instrument, not an algorithm.** This project studies how spike sorters are *graded*, not how well any particular sorter works.

Four materials, each with its licence read directly rather than assumed:

| Material | What it gives us | Licence |
|---|---|---|
| **[DANDI 000409](https://dandiarchive.org/dandiset/000409)** — the IBL Brain Wide Map | The **host recordings**: real probe data with real noise, real neurons firing, real artifacts, real drift. About 2,048 files and 49.7 terabytes in total; we use a deliberately tiny, precisely identified slice. | CC-BY-4.0 (free to use with attribution) |
| **[`hybrid_template_library`](https://github.com/SpikeInterface/hybrid_template_library)** | The **donor spike shapes** we inject, each labelled with its brain area, its loudness, its signal quality, its depth, and which dataset it came from. | MIT (free to use, including commercially) |
| **[SpikeInterface](https://doi.org/10.7554/eLife.61834)** | The **generator** that injects the spikes, the **interface** that runs the sorters, and the **scorer** that grades the result — all one package, pinned to one exact version. | MIT |
| **Sorters** | **Kilosort4** (runs on the graphics card) plus at least one mechanically different sorter that runs on the CPU. | Kilosort4 is **GPLv3**; the others are MIT |

**One licensing point genuinely constrains how we write code, so it is stated here rather than filed as paperwork.** GPLv3 is a "share-alike" licence. Running Kilosort4 as an external tool is ordinary use and obliges us nothing. But *copying its source code into our own scripts*, or wiring our code into it closely enough to count as a derivative work, would force this entire project to become GPLv3 too. **So we call it; we never copy it in.** If we ever genuinely need to modify Kilosort4, that is a licensing question logged for you *before* the modification is written, not after.

Everything this project releases is split by file type: code under MIT, writing under CC BY 4.0. The obligations we inherit — crediting DANDI, carrying MIT notices with any redistributed code — are recorded in the reproducibility packet as it is built, not reconstructed at the end.

**No Dandelion standard is relaxed for this project.** Where something looks like a shortcut — running on ten-minute slices of recordings rather than full hour-long ones, for instance — it is a deliberate efficiency choice with a stated reason, not an exemption.

## Slot 2 — The problem being addressed

There are exactly three ways to manufacture an answer key, and each fails differently.

- **Paired recordings** put a second electrode *inside* one neuron while the probe listens outside. The inside electrode is unambiguous, so you know that cell's spikes exactly. It is the gold standard and nearly useless at scale: you typically get **one** verified neuron per recording, and only from the large, sturdy cells that survive being impaled.
- **Fully synthetic recordings** simulate everything. You get every neuron's truth for free — but if the simulation is wrong in some respect, every unit in the dataset is wrong in that same respect at once, and nothing in the data will tell you.
- **Hybrid recordings** are the compromise the field settled on: real recording, real noise, real everything, plus a handful of injected neurons whose spike times you wrote down yourself.

Hybrid data is the only route to *many* ground-truth neurons sitting in *genuinely real* noise. That is why it won, and it is exactly where the vulnerability sits — because only the injected units get graded, so the grade describes how findable **the injected units** were.

The realism of an injected unit is not one thing. It comes apart into separable layers: the *shape* of the spike and whether that shape is plausible for the brain region it was dropped into; the *statistics of when it fires*; whether it fires in step with the surrounding population; whether its waveform changes depending on what it just did; and where on the probe it sits. The standard pipeline gets some of these right — it already enforces a refractory period, the brief window after firing during which a real neuron physically cannot fire again, and it already handles probe drift — and leaves others untouched.

**So the concrete question is two questions, and this project can answer one without the other:**

1. **Are the absolute scores valid?** Does adding a realism property change measured accuracy enough that published hybrid numbers would need reinterpreting — *even if every sorter is affected equally*?
2. **Are the comparisons valid?** Does realism affect sorters **differently** — enough to change which one looks better, or to turn a decisive gap into a tie?

The second matters more, because hybrid benchmarks are mostly used to *choose between* sorters rather than to state an absolute number. An effect that shifts every sorter equally would invalidate the absolute numbers while leaving every ranking intact. A smaller effect concentrated on the faint or bursty units could leave the average almost unmoved and still reverse a ranking. **Both are reported, separately.**

## Slot 3 — What we could claim if it works

Written out in full, because the boundaries are the point:

> Holding the host recording, the placement zones, the injected loudness, the number of injected units, the total spike counts, and the paired repetition structure fixed — and holding the identity of the injected spike shape fixed whenever the axis allows it — adding a named realism property to the standard hybrid generator changes measured accuracy by a **bounded** amount, and changes the comparison between sorters by a **bounded** amount, for the specific recording, sorter panel, and manipulation size tested; and those bounds sit either inside or outside a range we declared decision-relevant before we looked.

The claim transfers to other people because the change is made against **the pipeline the field actually uses**, at one pinned version, with everything else held fixed or matched by construction and every deliberate departure recorded. People running comparable setups inherit evidence *inside the tested boundaries*. They do not inherit an unqualified universal answer, and this document will not pretend otherwise.

**The claim is a bound, not a direction.** It is deliberately written so a negative result satisfies it exactly as well as a positive one. The number this project produces is a *range* on the effect, and the science is in where that range sits relative to the threshold in Slot 11.

## Slot 4 — What bounds the work

**Compute is the binding constraint, and it is not a stable one.** The work runs on the shared Dandelion agents desktop: 8-core CPU, one 16 GB graphics card, 32 GB of system memory. **Other Dandelion projects run on that machine at the same time and are not coordinated with this one.** There is no scheduler and no way to reserve anything. Free memory is therefore a *measurement that changes underneath us*, not a budget we hold.

The scale of that problem, in numbers rather than adjectives: a test run before the project began showed Kilosort4 sorting a full 61.5-minute recording in about 14 minutes, peaking at **29.3 GiB of the machine's 31.7 GiB** of memory. But at four separate moments across the project's first four sessions the machine had only **0.9 to 4.5 GiB free**. Started at any of those moments, that same run would have failed — and failed slowly and confusingly rather than cleanly.

**So the operating rule is: measure free memory immediately before every heavy step, compare it against a requirement we have actually measured rather than estimated, and do not start what does not fit.** Prefer the smaller run that settles the question over the larger run that settles it more comfortably.

**Budget: zero.** Only open-source tools and freely available data. No paid compute, no paid API, no paid dataset.

**Licensing:** as above — permissive by default, Kilosort4 called and never copied in, anything with unclear licensing treated as unusable until resolved.

**Data handling:** no raw data is redistributed. Recordings are referenced by identifier and downloaded by the reader.

**You are asynchronous, not absent.** You drive for a living on weekdays and read in the evenings and at weekends, so the agents expect days rather than hours. `director_requests.md` works and you answer it, but **every request there carries a fallback and the session keeps moving.** A blocked request is not a stopped session. Your review of this contract is explicitly non-blocking: the agents keep working while it is pending, and the project can run to completion without it.

**Time:** no deadline and no revenue clock on this project. That is a real freedom and it is not a licence to sprawl — the project runs until it reaches the stopping point defined in Slot 14.

**Four things this project is deliberately not asking**, restated because they are easy to drift across:

- **Not "which spike sorter is best."** Sorter identity is a variable here, not the subject. Any ranking this project produces is evidence about *the grading method*, not a recommendation.
- **Not "is Kilosort4 accurate."** Absolute accuracy against hybrid data is precisely the quantity whose meaning is in question. Reporting it as though it were truth would assume the conclusion.
- **Not building a new hybrid generator.** Where an axis has to be implemented, it is implemented to the minimum needed to vary that axis.
- **Not a replacement for real ground truth**, and **not a judgement about the maintainers**, who named this limitation themselves, in print.

## Slot 5 — How the work is actually done

The anchor study's authors estimated roughly **870 and 846 single-workstation hours** for their two sorter comparisons. This project has one shared desktop that other projects are also using. It cannot buy confidence with volume.

**It buys confidence with pairing instead.** If you want to know whether a change matters, the expensive way is to run a big group with the change and a big group without, and compare averages — absorbing all the variation between individuals. The cheap way is to test *the same individuals* under both conditions and look at each one's change. Most of the noise — the fact that some injected units are intrinsically easier to find than others — cancels, because it is present identically on both sides of the subtraction.

### The control arm

The control is a **faithful rebuild of what the standard pipeline does today**: spike shapes drawn without paying attention to brain region, spike times drawn from the simplest possible random process, a firing rate in the anchor paper's range, ten injected units per recording, the refractory period the pipeline already enforces, loudness rescaled into the anchor's 50–200 microvolt range, and drift handling applied identically in every arm.

It is *not* claimed to be an exact reproduction where this project deliberately adds its own safeguards — excluding certain donor spike shapes to prevent cheating, matching the arms on nuisance properties, using a different recording. Every such departure is recorded rather than glossed.

**Refractoriness is already implemented upstream**, so it is part of the control rather than one of our realism axes. This matters for reading the rest of the document: it is a realism property the pipeline already has.

### The three realism axes, run one at a time and never together

Each is a separate one-property experiment against that control. **They are never varied together**, because if you move two things and the score changes, you have learned nothing about which one did it. A combined arm only becomes interpretable once the individual effects are known, so it is not part of the initial design.

- **Tier A — matching the spike shape to the brain region.** Injected spike shapes currently come from whatever region the library happens to offer, not the region the recording came from. That is a real mismatch, not a cosmetic one: waveform shape differs enough between regions that a neuron's region can be partly *classified* from it ([Jia et al., 2019](https://doi.org/10.1152/jn.00680.2018)). Because the library already carries a region label, fixing this needs **no new generator machinery** — it is a careful selection-and-matching problem over rows that already exist.
- **Tier B — making injected neurons fire in step with the population.** Real neurons do not fire independently of their surroundings; population activity rises and falls in waves and individual rates ride those waves. The current spike times are deaf to this by construction. **This fix was proposed by the anchor paper's own authors**, and there is prior art — Kilosort4's own hybrid benchmark already does something similar. The crucial design detail: the "how busy is the population right now" signal is computed **once, from the untouched recording, without running any sorter**. Estimating it by sorting the recording first would let a sorter supply the target used to generate its own test data, which is circular. Total spike count, average rate, and refractory behaviour are held fixed across arms, so the *only* thing that changes is the timing pattern.
- **Tier C — bursting, with the waveform shrinking as the burst proceeds.** Real neurons fire bursts of spikes a few milliseconds apart, and the recorded amplitude **shrinks across the burst** — a fixed average template presents the same shape no matter what the neuron just did. Both halves are required: timing-only bursts without the shrinkage would be an incomplete manipulation, because the sorter-relevant mechanism is precisely that a real neuron's waveform depends on its own recent history. The numbers this has to hit (bursts at intervals of 6 ms or less, amplitude decreasing across the burst, bursts suppressed after recent activity) come from hippocampal CA1 pyramidal cells ([Harris et al., 2001](https://doi.org/10.1016/S0896-6273(01)00447-0)). That this matters for *sorting* is not a guess — a sorter built two decades ago improved its results by explicitly modelling exactly this shrinkage ([Pouzat et al., 2004](https://doi.org/10.1152/jn.00227.2003)).

**An honest note about the split.** Tier A is measurement. Tiers B and C are *engineering in the service of measurement* — the mechanism has to be built before it can be measured. That is still research, and this contract says so plainly rather than presenting the project as pure measurement.

**A hard constraint on Tier C's biology.** The CA1 numbers are region- and cell-type-specific. They are **not generic brain-wide biology**. Tier C either uses a CA1-compatible recording and injection zone, or first secures primary evidence for whatever region is chosen and declares those bounds. CA1 parameters are never presented as universal.

### The sorter panel

**Kilosort4 plus at least one mechanically different sorter that runs on the CPU.** This is a scientific requirement, not a preference.

Comparing Kilosort4 against an older Kilosort would share a family and a drift-correction lineage — and the anchor's companion paper flags that hybrid data injected using motion-corrected templates *advantages sorters using the same motion correction*. So that pairing is the one **least** likely to show a difference, and a null result from it could reasonably be read as designed-for. Sorter families diverge most on **collision handling** — untangling two neurons that fired within a millisecond of each other — where template-matching approaches substantially outperform density-based ones ([Garcia, Buccino & Yger, 2022](https://doi.org/10.1523/ENEURO.0105-22.2022)). That is exactly the behaviour the temporal axes stress.

**Whether this machine can afford a third sorter is an open question that a pilot decides**, and published runtimes from other people's hardware are not a substitute for measuring here. **The fallback is declared now rather than negotiated later: if no third sorter fits the budget, the project runs two, and the narrower panel becomes a stated limitation that bounds the claim.**

**Sorter settings are pinned defaults, identical across arms, never tuned per condition.** Tuning a sorter on a realism condition would leak the condition into the result. Any calibration that turns out to be necessary happens on a separate segment that is never used in a comparison.

### What we compare against — three things

1. **The standard pipeline's current settings** — the control arm above, which is what the field uses today.
2. **A published reference for scale.** The anchor's own Kilosort4-versus-Kilosort2.5 effect sizes. **These are context, not a threshold.** They establish that sorter-versus-sorter differences in this field are small-to-moderate, which tells us how much precision we need. They are measured on a different sample with a different variance structure and *cannot* be compared mechanically against a raw accuracy change measured here. (An earlier draft of this project proposed using them as the threshold; that was caught and blocked in review.)
3. **The negative control — the strongest non-signal check in the design.** For each axis, we generate pairs of arms under the *same* nominal condition — same settings, different random draws of which shapes were picked, which times were rolled, where things landed — and run the identical comparison on them. Any apparent effect they show is **pure noise from selection and random seeds**, because no realism property differed between them. That spread becomes a reference band drawn behind the real result.

   Its role is precise, and it is not a second test. It answers *"can this machinery manufacture an effect of the size we observed, out of nothing?"* The actual decision is made by the range and the pre-declared threshold, never by the band. A shaded band that quietly becomes a truth threshold is a way of testing the same data twice.

   **These pseudo-comparisons have to be sorted, not merely generated**, which doubles the sorter time the main run needs. That is now written into the compute budget rather than discovered mid-experiment. Their number of repetitions matches the real comparison's, so both start from the same nominal basis — though equal repetition counts do *not* guarantee equal precision, so the achieved precision of each is reported rather than assumed identical.

## Slot 6 — Who this is for and why it matters

The immediate beneficiaries are the people who read and produce spike-sorting benchmarks. A researcher choosing a sorter for a new recording, a lab deciding whether to migrate pipelines, a reviewer weighing a benchmark claim — all currently rely on hybrid accuracy numbers whose sensitivity to generator realism has never been measured. This project measures it, in either direction, and hands them a bound.

**The maintainers benefit specifically and directly.** They named this as an open question in print; this is evidence they do not currently have. If realism does not move rankings, that is independent support for continuing to use the pipeline as it stands. If it does, the axes that move it are named, the sizes are bounded, and the code that produced the manipulation is released — which makes the finding *actionable* rather than merely critical.

The wider relevance is that spike sorting sits underneath a large amount of systems neuroscience, and underneath essentially every future neural interface that has to decide which cell fired. A benchmark that grades the generator rather than the algorithm propagates quietly into every decision made on top of it. Measuring that is cheap relative to what rests on it.

**For Dandelion specifically**, this is a validation-methodology result rather than a device. It feeds future work by establishing whether a widely used proxy can be trusted, and by producing a reusable, licence-clean harness for asking benchmark-realism questions in general. It is also a deliberate test of whether this framework can produce a rigorous, honest, checkable result on a shared desktop with no money — which is the operating question underneath every project here.

## Slot 7 — How we will know: the evaluation design

This is the team's confidence path — exactly how we determine whether the Slot 3 claim holds.

### Choosing a recording, and why the spike shapes decide it rather than the other way round

An audit of the live template metadata found something that reversed an assumption. Under working filters (loudness 50–200 µV, signal-to-noise 5–15), **1,149 of the 2,183 relevant spike shapes survive across 149 brain-area labels, and 37 labels hold at least ten** — ten being the number of units injected per recording. But there is an anti-cheating rule: the donor spike shapes must not come from the *same source dataset* as the host recording, or the test is partly rigged. Dropping each area's single largest contributing dataset — **the worst possible case for that area** — leaves only **7 labels with at least ten: CP (42), PIR (19), SUB (18), VISa5 (17), AId5 (14), MRN (14), ENTl5 (10)**. Thirteen of the 37 collapse to zero, because one dataset had supplied all their shapes.

**Read the boundary with those numbers, because an earlier version of this project overstated them.** Seven is the *worst case*, not the count for every recording; any other exclusion can leave more. And the audit is a **pool-size screen only** — it does not prove that a matched arm and an unmatched arm can actually be built together. It does not test whether the two arms can be made alike on their nuisance properties, whether the injections can be physically placed, or whether the comparison pool holds up. So the real query excludes the *exact* host's source dataset and reports the resulting count, rather than substituting the worst-case shortlist as fact.

**One filter deserves a specific correction, because it was misused in an early draft.** The anchor's 50–200 µV range is a target the injected spike is *rescaled to* — it is not evidence that donor shapes must already be that loud. Final eligibility and matching are evaluated on the waveform *after* rescaling and placement in the chosen recording, including its effective signal quality against that recording's measured noise. The donor's original loudness is a quality diagnostic, not a stand-in for the injected result.

**A probe passes through several brain areas, so no recording gets one region label.** Each candidate recording must carry a pinned map from probe channel to anatomy, and a declared **injection zone** at a specific depth. Region matching is between each donor's label and the *local* label where it will actually be placed. If ten workable placements cannot be supported without overcrowding or ambiguous labels, that recording **fails the Tier A gate** rather than having a convenient whole-recording label invented for it.

Recordings are additionally screened for measured drift below a declared threshold (or, failing that, identical measured motion applied across every arm), documented channel geometry, documented noise level, and adequate length. Chosen recordings are pinned by their exact archive identifier; chosen spike shapes are pinned by row number against a metadata snapshot pinned by cryptographic hash — that table is hosted somewhere it could change, and a result built on "whatever was there that day" is not reproducible however good the analysis code is.

**Making the arms alike is a gate, not a hope.** The region-matched and region-unaware arms must be balanced on post-rescaling loudness, effective signal quality in the recording, probe geometry, placement, **and the number of contributing source datasets**. That last one is not optional: excluding the host's own dataset limits cheating but does not stop *provenance* riding along with region, and an arm drawn from five source datasets compared against an arm drawn from one is partly a provenance comparison wearing a region label.

**One recording and one injection zone across all three axes, by default.** The axes are separate experiments but they are not independent results — the reasoning in Slot 13 runs from a Tier A outcome to what it does and does not license about B and C, and Slot 14 requires A and B together. A recording that changes between axes turns every cross-axis statement into a comparison across recordings as well. **If an axis must move to a different recording, that is recorded as a limitation and the cross-axis comparison is dropped rather than made across recordings.**

**That default couples two constraints that arrived separately, and the coupling turns out to be binding.** Tier A needs a zone whose donor pool survives the exclusion rule. Tier C needs a zone whose burst biology rests on primary evidence, and the current evidence is CA1. **CA1 is the only zone in the audit that satisfies both on its face** — 12 qualifying shapes across 4 source datasets before any host-specific exclusion. **That is a candidate, not a decision:** CA1's worst-case count is 6, below the ten-unit budget, so whether it works depends entirely on which source dataset the chosen recording belongs to. It is named here so that recording selection is run against **both** constraints at once, rather than satisfying Tier A and then discovering Tier C cannot use the recording Tier A picked.

### How many units get injected

**Ten per recording instance**, matching the anchor. **Statistical power comes from paired arms, repetition blocks, and more recordings — never from injecting more units**, because more simultaneous injections change the crowding statistics of the recording itself, which is the thing being held fixed.

### The manipulation check — a hard stop-or-go gate

This is the most important structural idea in the design, and it is worth seeing why it is more than hygiene.

Suppose Tier C is built, run, and the scores do not move. Two explanations fit: realism genuinely does not matter, *or* the bursts we injected were feeble, biologically implausible, or subtly broken. Those two conclusions are opposite in meaning and identical in appearance, and **nothing measured after the sorters run can separate them.**

So: **before any sorter time is spent on an axis, the generated data must be shown to actually carry the intended property, at a realistic size.** The criteria differ by axis:

| Axis | Passes when… |
|---|---|
| **A — region** | declared waveform features genuinely separate the matched from the unmatched donor sets, while loudness, effective signal quality, geometry, placement, and provenance stay balanced. The features are chosen so as not to be simply the sorters' own decision variables. |
| **B — population coupling** | the injected units' rate over time tracks the sorter-free population signal to a declared standard, while total spike count, average rate, and refractory violations are unchanged from control. |
| **C — burst / history** | both the short-interval distribution and the amplitude shrinkage fall inside declared, **region-and-cell-type-appropriate** biological bounds, while total spike count and long-run average rate are unchanged from control. |

**If a check fails, no sorter run starts for that axis.** The failure is diagnosed and published as a finding about the generator. It is never papered over and pushed downstream.

This is what makes a *negative* result mean anything. Without the gate, "realism did not matter" is indistinguishable from "we implemented realism badly" — and since a negative is the likelier and arguably more useful outcome here, the gate is what keeps the project's most probable finding from being worthless.

### What gets measured

The scorer is SpikeInterface's ground-truth comparison at a pinned version. Reported for every arm and every sorter:

- per-unit **accuracy, precision, and recall**. Accuracy is the field's standard metric ([Magland et al., 2020](https://doi.org/10.7554/eLife.55167)): of everything that either happened or was claimed to happen, what fraction did the sorter get right. It runs 0 to 1 and is deliberately unforgiving — inventing spikes is penalised just as missing them is;
- the **count of units scoring above 0.8**, the field's convention — because an average hides whether a manipulation nudged everything slightly or pushed a few units across a line researchers actually act on;
- counts of **false-positive, redundant, over-merged, and over-split** units;
- **collision recall** — how well near-simultaneous spikes are recovered — required for the temporal axes, since that is the documented axis of divergence between sorter families;
- everything **broken out by signal quality and loudness**, and by the manipulated property itself, with the strata declared in advance. An effect concentrated in the faint, hard units — the stratum where the anchor found sorter differences strongest — would vanish from an aggregate median.

**No condition-aware cleanup.** The main analysis uses every unit the sorter returns, under identical automated rules across arms. Any hand-curated analysis is secondary and blinded to condition where practical.

### The number we are actually after, and the rule that decides it

Take one sorter. For each paired unit, subtract its accuracy in the control arm from its accuracy in the realistic arm. That is that sorter's **realism effect**. If it is negative, the sorter did worse when the spikes were made more realistic.

But a realism effect on its own is the *absolute-score* question. If every sorter drops by the same amount, published numbers are too optimistic — yet every "sorter A beat sorter B" survives untouched.

So the primary quantity is **the difference between two sorters' realism effects** — a *difference in differences*, also called an **interaction**. Read it aloud: *how much more did sorter 1's accuracy change under realism than sorter 2's?* If it is near zero, realism moved both sorters together and the comparison between them is stable. If it is large, the gap between the two sorters depends on how realistic the fake spikes were — which means the benchmark has been partly grading the generator.

Units are averaged within a repetition block, blocks within a recording, and recordings equally across whatever set is tested. For Tiers B and C, a "paired unit" is literally the same injected spike shape, same placement, same total spike count in both arms. **Tier A cannot do that** — changing donor region necessarily changes donor identity, since a region-matched shape and a region-unaware one are different shapes by definition. So Tier A pairs **matched slots**: two donors deliberately chosen to resemble each other on every measured nuisance property, injected with the same spike train at the same place at the same rescaled loudness. The pairing claim is about the matched slot, not about a fictitiously unchanged unit.

**The realism effect, the sorter difference, and the interaction are reported separately**, because a uniform loss invalidates absolute scores without touching rankings, and a concentrated differential loss does the opposite.

**Uncertainty.** Every number here is an estimate from a finite experiment, so each gets a range of plausible values rather than a bare point. The tool is the **bootstrap** ([Efron, 1979](https://doi.org/10.1214/aos/1176344552)): instead of assuming a formula for how much a measurement would wobble if you repeated the experiment, you simulate the repetition by resampling your own data many times and watching how much the answer moves.

What gets resampled is the part that matters. Ten injected units inside a single run are **not** ten independent experiments — they share a recording, a noise environment, and a random seed. Treating them as ten independent repetitions would produce a range far too narrow and a confidence far too high. So the resampling mirrors the design: paired units are resampled *within* repetition blocks with their arm and sorter pairing intact; blocks are resampled within recordings; recordings are resampled at the top once there is more than one, weighted equally. Repeated donor identities stay in one cluster. **With one recording, the range is explicitly conditional on that recording and cannot manufacture generalisation to others.**

A five-block start is a **resource tranche, not a claim that five observations estimate anything reliably.** Blocks are added in declared batches until the range is tight enough to decide, or the measured hardware ceiling is reached. **Decisions are declared in raw accuracy units with their uncertainty; standardised effect sizes are reported second and are never thresholds.**

**With two sorters, "rank stability" is exactly the sign of one difference**, and the project will not decorate that with rank-correlation language. Rank correlation appears only if the pilot supports three or more sorters.

## Slot 8 — How you check it yourself

Slot 7 is how the *team* becomes confident. This slot is how **you** become confident, without reading the technical report end to end and without domain expertise. It is committed to now, before execution — which also forces the work to be designed so that verification is possible at all.

**The artifact: one self-contained script, `verify_realism.py`, that produces a two-panel figure and prints a plain-language verdict.** It lives inside the reproducibility packet, so anyone who downloads the packet verifies the result the same way you do.

**Panel 1 — "Did the knob actually turn?"** Tier-specific, rather than forcing every axis into the same plot:

- **Tier A:** the local anatomy label at the injection zone, the matched and unmatched donor shapes side by side, and compact balance plots for loudness, signal quality, placement, and provenance;
- **Tier B:** the population activity signal and the injected firing rate drawn over time on the same axes, plus the checks that average rate, total count, and refractory behaviour did not move;
- **Tier C:** raw voltage snippets control-versus-realistic, the distribution of intervals between spikes, and spike amplitude plotted against the preceding interval.

You should be able to see both that the intended property changed **and** that the things that were supposed to stay put did stay put. **If these views do not separate as predicted, the manipulation did not pass and nothing downstream matters** — this is the stop-or-go gate rendered so a non-specialist can apply it.

**Panel 2 — "Did it change the answer?"** The same units' accuracy under each sorter, control versus realistic, with the gap between the two sorters drawn in both conditions and **the negative-control band shaded behind them**. The question you answer by looking: how does the real effect compare with the apparent effects produced by pseudo-comparisons where nothing changed? The printed range and the declared threshold make the decision — the grey band is a diagnostic, not a visual significance test that turns every point outside it into truth.

**What you actually do.** Run one command, look at two panels, read one printed sentence of the form: *"Under [axis], the gap between [sorter A] and [sorter B] moved by X accuracy points (95% range …), against a negative-control band of ±Y and a decision margin of ±T. The ranking did / did not reverse; practical separation was / was not lost."* Then, if you want, change one flag and re-run it on a different axis.

**It is paced into the project rather than assembled in the final session.** Panel 1 is buildable as soon as any axis passes its manipulation check, well before any sorter result exists — and it is genuinely useful at that point, because it *is* the visual form of the gate.

## Slot 9 — How big we will build, and the ladder we climb

There is no trained model here, so "how big" means: how long a segment, how many recordings, how many repetition blocks, how many sorters.

| Rung | Scale | Purpose | Gate to climb |
|---|---|---|---|
| **0 — Feasibility pilot** | ~60-second segment, 1 recording, 10 injected units, every candidate sorter timed and memory-profiled on the same segment | Decide the sorter panel; measure real runtime and peak memory **on this machine**; smoke-test the harness | Runs complete; measured peaks recorded |
| **1 — Manipulation check** | Generator only, no sorting | Prove the realism knob turns | Axis-specific criteria pass |
| **2 — Primary run** | ~10-minute segment, 1 recording, 10 units, 5 paired blocks **plus 5 matched pseudo-blocks for the negative control**, 2 sorters; add blocks in batches | Produce the first effect estimate and negative-control band | Range computed; continue if too imprecise |
| **3 — Panel widening** | Rung 2 plus a third sorter | Break the shared-family limitation; enable ranking language | Only if the pilot showed it fits |
| **4 — Recording widening** | 3–5 recordings, longer segments | Tighten the range; test whether the effect survives across recordings | Only on a Slot 11/13 trigger |
| **Ceiling** | Whatever the machine allows **as measured at the moment of the run** — never from a number written in a file, including this one | | |

**Blocks are added based on how wide the range is, not on whether the point estimate looks favourable.** Climb the ladder when there is partial signal worth resolving, **or** when there is no signal yet *and* the range is still wide enough to admit a decision-relevant effect. Rung 4 exists specifically for that second case: a null with a wide range is *inconclusive*, not negative, and the response is more precision rather than a conclusion.

**Stop climbing only when** the result holds across rungs, or the measured hardware ceiling is genuinely reached, or there is a **scientific** reason more scale would not help — stated explicitly. "A bigger run wouldn't change it" is itself a claim that needs that reason; a budget reflex is not one.

**The pilot has a declared budget, so a marginal result does not become a negotiation.** Each candidate sorter gets one 60-second run with a **60-minute wall-clock ceiling**. At launch it may use no more than **75% of the free memory measured immediately beforehand**, and must leave at least **4 GiB of system memory and 2 GiB of graphics memory** for the operating system and other projects. Crossing either guard stops the run and records a resource failure. A sorter is admitted to the main run only if its measured 60-second time extrapolates to **48 sorter-hours or less per candidate per axis**, and its measured peak fits the same live-headroom rule.

**The minimum workload includes the negative control, because the negative control has to be sorted.** The band is built from pseudo-comparisons, and each pseudo-arm is a full sorter run rather than merely a generator run. So the minimum tranche is **10 minutes × 2 arms × 5 blocks × 2 comparison types = 200 recording-minutes per candidate sorter per axis.** Extrapolating from the real arms alone would have understated the main run by a factor of two — exactly the mid-project renegotiation this budget exists to prevent. **The ceiling stayed at 48 hours rather than doubling to 96:** discovering that the workload was underestimated is not a reason to approve twice the budget.

**The whole-panel total is recorded, not just the per-sorter one.** A panel can consist entirely of individually admitted sorters and still not fit — at the ceiling, two sorters across three axes projects to **288 sorter-hours**. The pilot reports the per-sorter, per-axis, and whole-panel projections, and the free-memory measurement is repeated immediately before the main run rather than inherited from the pilot. **A sorter that does not fit is dropped, named in the report as dropped, with the reason recorded.**

**Software discipline**, which is the Dandelion standard applied here: one purpose per script, shared logic imported rather than copy-pasted, every input passed on the command line with no paths hard-coded to this machine, documented functions, progress printed, loud and informative failures, figures at print resolution with labelled axes, and every dependency pinned with its version number **the moment it is installed**. Scripts are written **into the reproducibility packet as they are finalised**, not relocated there at the end.

**Every exclusion is recorded the moment it happens** — a discarded run, a recording that failed drift screening, a spike shape dropped by a filter, a sorter dropped by the pilot. Silent exclusions are a reproducibility failure.

## Slot 10 — What it runs on

| | |
|---|---|
| **Machine** | The dedicated Dandelion AI-agents desktop — a shared workbench, not your personal computer |
| **OS** | Windows 11 Home, build 26200 |
| **CPU** | AMD Ryzen 7 8700F — 8 cores / 16 threads |
| **Graphics** | NVIDIA RTX 5060 Ti, 16 GB |
| **Memory** | 32 GB (31.67 GiB usable) |
| **Storage** | 1 TB internal, external SSD on `D:` |
| **Python** | 3.12.10 in the project's own environment, invoked only through that environment's executables — never the bare system ones, which pick up whatever interpreter the shell happens to have |
| **GPU toolkit** | No system-wide CUDA install. GPU builds come from packages that carry their own runtime. Availability is verified rather than assumed. |
| **Known-good stack** | Kilosort 4.1.7, SpikeInterface 0.104.8, PyTorch 2.11.0+cu128 — measured working on this machine before the project began |
| **Environment as of now** | Only the package installer. No dependency list yet; it is created at the first install, with versions pinned at that moment. |

**The measured feasibility point, with its boundary attached.** One complete raw recording — 96 channels, 61.5 minutes — converted in 198 seconds and sorted by Kilosort4 in 819 seconds, returning 143 units and 1.56 million spikes, peaking at 29.3 of 31.7 GiB of memory and about a fifth of the graphics memory, with no failures. **That proves one full recording of one probe type on an otherwise-quiet machine.** It does not prove a 384-channel or three-hour case, and it proves nothing about running while another project is using the machine.

**Which is the constraint that actually governs.** Free memory has been measured at the start of four consecutive sessions: 3.46, 3.96, 1.01, and 0.89 GiB free of 31.67. Graphics memory has been consistently fine — about 14 of 16 GB free every time — so the contention is entirely in system memory. Started at any of those four moments, the feasibility run above would have failed. **Measure at the moment of the heavy step, compare against a measured requirement, and if it does not fit, wait and re-measure or do smaller work that does fit.** Nothing in this project is designed on the assumption that it owns the whole machine.

## Slot 11 — What would count as success

**Declared before any result is seen.** Success is **a bounded answer, not a detected effect.**

For each axis attempted, the project succeeds when all five of these hold:

1. the **manipulation check passed**, so the arm demonstrably differs in the intended property and only in it;
2. the **balance and anti-cheating gates passed**, so the arms differ in the manipulated property and not in loudness, signal quality, geometry, placement, or provenance;
3. a **95% range on the interaction exists**, computed by the resampling scheme in Slot 7;
4. the **decision quantity** described below has a range that lands clearly on one side of the line, so the result actually decides something; and
5. the **negative-control band** was estimated from the same design and is stable enough to show whether random selection and seeds can mimic an effect of the size we observed.

### Where the line is

Both thresholds are defined against quantities **measured inside this experiment**, not imported from another study — and both are fixed here, before results.

- **For absolute scores:** a realism effect on accuracy of **0.05 or more — five points** — is material. The reasoning is concrete rather than conventional: the field counts units scoring above 0.8, so a shift of that size near the threshold moves units across it and changes a reported number.
- **For the comparison:** let **G₀** be the average gap between the two sorters in the control arm. The margin is **T = the larger of 0.05 and half of |G₀|**. The half-gap term asks whether realism moved a meaningful *fraction* of the comparison that actually exists; the five-point floor stops a near-tie in the control arm from making a trivial wobble look decision-relevant. Because G₀ is itself estimated, every resample recomputes G₀, T, and the decision quantity rather than treating the threshold as known exactly.

**The decision quantity is D = |interaction| − T** — the size of the effect minus the margin. And this is the *only* comparative rule:

- **a 95% range for D entirely above zero, together with an interaction range that excludes zero → bounded positive.** Realism changes the comparison between sorters.
- **a 95% range for D entirely below zero → bounded negative.** Realism does not change the comparison, within the tested boundaries.
- **a range for D that crosses zero → inconclusive** at the precision achieved.

There is a subtly different-looking phrasing — *"the interaction range sits inside ±T"* — that appears in the technical sheet as shorthand. **It is shorthand for the D rule and never a second test.** Within a single resample the two describe the same event, but as *range* statements they are different operations: one carries the uncertainty in G₀ through to the answer, the other compares against a single best guess of T. Choosing which one is meant is exactly the sort of thing that must be settled before results exist rather than picked afterwards from two defensible options.

**One consequence of that choice is declared now rather than discovered later.** Because D is built on the *size* of the interaction regardless of direction, a genuinely near-zero interaction resamples slightly upward on average. That pushes D upward, which makes the **bounded-negative** verdict *harder* to reach, not easier. The rule is conservative in the right direction — it will call a real null "inconclusive" before it calls noise a settled null — but it is conservative in the direction that costs us the outcome we think is likelier. That is why it is in writing now.

Once the interaction clears the rule, the project names which event occurred:

- **Reversal.** The sorter gap has opposite signs in the two arms, with at least one clearly separated from a practical tie.
- **Loss (or gain) of practical separation.** One arm's gap is clearly real while the other's is a practical tie, and the interaction range excludes zero. **Merely having one range include zero while the other excludes it is *not* evidence that the two arms differ** — a mistake this project made in an early draft and had corrected in review.
- **Large non-crossing shift.** The ranking does not reverse and neither arm becomes a tie, but the effect still clears the margin.

**A clean negative satisfies this slot completely.** If the manipulation demonstrably turned, the range for D sits entirely below zero, and the negative-control band is stable and shows no nuisance effects of decision-relevant size, then the project has bounded the realism effect below its declared threshold for that axis, recording, and sorter panel. **That is a success and is published on exactly the same terms as a positive result.** It validates the proxy only inside those boundaries; broader validation needs the widening rungs.

## Slot 12 — What would count as failure

Also declared in advance. **A clean failure is still a public artifact**, and each of these is reported with its diagnosis rather than quietly absorbed.

The distinction that matters most: **a scientific negative is not a failure.** Realism not moving the rankings is a *result*. Failure is being unable to produce a bounded answer at all.

1. **The manipulation check cannot be made to pass.** The generator will not produce data with the intended property at a realistic size — bursts that never reach biological intervals, shrinkage that cannot be bounded, injected rates that will not track the population. **Published as a finding about the generator**, with what was attempted and where it broke, because "this axis is harder to implement than it looks" is genuinely useful information about whether the field can make hybrid data more realistic at all.
2. **The precision is unreachable.** No rung of the ladder produces a range narrower than the decision band, and the machine's ceiling is genuinely reached. Reported as **inconclusive with the achieved bound stated**, plus an honest account of what scale would have been required.
3. **Donor feasibility collapses.** No recording-and-zone combination admits both a region-matched arm and a balanced region-unaware arm without confounding loudness, signal quality, geometry, or provenance. Tier A is dropped, the reason published, and the project proceeds on Tiers B and C.
4. **A confound is discovered after the fact.** Analysis reveals the arms differed in something besides the manipulated property. The affected work is moved to a dated archive folder, an amendment is written, and the finding is reported as **invalidated** rather than silently dropped.
5. **The harness cannot be made reproducible.** The packet will not run end to end on a fresh machine, or something upstream moves in a way that cannot be pinned. Reported with the exact obstacle.

**What is *not* failure, and will not be reported as such:** a negative result; an effect smaller than expected; a two-sorter panel because a third did not fit; or completing only Tiers A and B if Tier C's implementation proves out of reach — provided the boundary is stated in the claim.

## Slot 13 — What would count as inconclusive, or as not transferring

The "not this, not yet" shapes, recorded so that a partial win is not reported as a full one. **These are the conditions under which the project must decline to answer its own headline question**, and they are written down now because they are much harder to concede later.

1. **A wide range is inconclusive, not negative.** If the range on the interaction includes both zero *and* a decision-relevant size, the answer is *"not resolved at this precision,"* with the achieved bound stated explicitly. **A null result with a wide range will never be reported as evidence that realism does not matter.** This is the single most likely way this project could mislead someone, and it is the reason this slot exists.
2. **A Tier A null licenses nothing about Tiers B and C.** Region mismatch changes static waveform shape, which sorter front ends consume in broadly similar ways. The temporal axes change firing statistics and within-neuron waveform dynamics, which hit **collision handling** — the documented place where sorter families diverge. So the honest expectation is that **Tier A is the most likely to move absolute accuracy and the least likely to move the comparison.** Because Tier A runs first and is cheapest, there is a live risk of the project *appearing* to have answered the headline question when it has answered the cheapest version of it. **The project may not conclude on Tier A alone**, and a Tier A result is reported as a Tier A result.
3. **A Kilosort4-favouring Tier B result is inconclusive on attribution.** Kilosort4's own hybrid benchmark *already* modulates spike timing by local population rate. Adding population coupling to the SpikeInterface pipeline therefore moves the test data toward Kilosort4's home turf. If Kilosort4 gains under Tier B, "more robust to realistic firing" and "developed against data that already had this property" cannot be separated by this design. **Declared now, before any result: that outcome is reported as inconclusive on attribution, not as a clean positive.**
4. **Two sorters means no rank-correlation claims.** With two sorters, the only comparative quantity is the sign and size of one difference.
5. **One recording means no cross-region or cross-probe transfer.** A result from a single recording, injection zone, and probe type is a result about that configuration.
6. **A manipulation check that passes weakly is a bounded manipulation.** If the property is present but below the biological range, any null is a statement about *that size*, reported with the achieved size attached.
7. **Tier C's biological numbers do not transfer across regions or cell types by default.** The current prior is CA1 complex-spike biology. A Tier C run elsewhere requires primary evidence for that region and cell type, or is explicitly labelled a **synthetic stress test** rather than a biological-realism test.
8. **Non-transfer to real ground truth is assumed throughout.** Nothing here substitutes for paired inside-and-outside recordings, which answer a different and harder question. A finding that a hybrid benchmark is or is not realism-sensitive says nothing directly about how either compares to real ground truth.

## Slot 14 — The minimum we must ship to call this finished

The project is not finished when the work is done; it is finished when the work is **shippable**. Four artifacts, all required.

**1. Technical Report** (for the field). Its required contents are fixed now:

- the anchor's open question, quoted, with the exact pipeline version under test;
- the complete generator configuration of every arm — seeds, spike-shape row identifiers, the metadata snapshot hash, recording identifiers, and every sorter setting;
- the **manipulation-check results, reported before the sorter results** — sizes achieved, criteria declared in advance, pass or fail;
- the realism effect, the sorter difference, and the **interaction, reported separately**, with ranges in raw units;
- the **negative-control band**, plotted alongside every effect and described as a diagnostic rather than a second significance test;
- results broken out by signal quality and by the manipulated property;
- **every exclusion named with its reason** — discarded runs, screened-out recordings, filtered-out shapes, pilot-dropped sorters;
- the Slot 13 limitations, stated as limitations rather than buried;
- the reconciled bibliography from both agents' running source ledgers.

**2. Accessible Piece** — the same result for a reader with no technical background: honest, engaging, and the artifact you share publicly at the close.

**3. Reproducibility Packet** — self-contained: code, pinned dependency list, configurations, a `DATA.md` covering dataset access and the attribution obligations, a top-level runbook, the exclusions log, the pinned metadata snapshot, and **the Slot 8 verification script**. Validated by copying the packet folder *alone* to a clean machine and running it end to end.

**4. Study Guide**, both passes — Pass 1 (Conceptual Foundation) at Phase 1 close, Pass 2 (Concept Delta) at Phase 3 under the no-spoiler rule.

**The minimum scientific content required to conclude:** Tier A **and** Tier B each carried to either a bounded estimate or a documented failure, with manipulation checks reported either way. **Tier C is required if its generator passes its check; if it cannot pass at a biologically justified size, it is reported as a documented generator failure rather than as a bounded sorter result.** The project may not conclude on Tier A alone.

**Because this is an agent-selected run** — the question came from the agents' own search rather than from you — **the run-provenance disclosure block is required** on the public artifacts, and it stays **above** the result rather than below it. A reader is entitled to know that no human director chose this question.

## Slot 15 — Could this ever make money

**Thin slot, honestly, and it should be.** This is validation methodology, and validation methodology is not a product.

**As scoped: none identified.** The natural home for the result is a public report and a contribution back upstream, and the natural users are researchers who would not and should not pay for it. Charging for it would also undercut the point of doing it.

**If it succeeded and scaled**, the only paths worth naming are indirect and speculative, and are recorded as possibilities rather than plans. A general **benchmark-realism auditing harness** — *"how sensitive is your benchmark to how you generated it?"* — is reusable well beyond spike sorting, because the same question recurs anywhere synthetic ground truth stands in for real ground truth. Any such path would have to clear the same affordability bar as everything else Dandelion builds.

**What this project is actually worth to Dandelion is not revenue.** It is a public, checkable artifact showing that this framework can take a maintainer-stated open question, execute it rigorously on a shared desktop with no budget, and publish the result at its true strength in either direction. That is the asset.

---

## How this contract changes

Real research surfaces what a contract did not anticipate. When it does, the agent who finds it writes an **amendment proposal** — what was found, why it changes the path, the new path, and the new success, failure, and non-transfer shapes — and the other agent approves or rejects it before execution shifts. An approved amendment is **appended and dated, never written over the original.** If it invalidates completed work, the affected files move to a dated archive folder and the amendment points at it. Nothing is deleted.

**Your review of this contract is the first use of that protocol, and it is non-blocking.** The agents keep working while it is pending, and the project can run to conclusion without it. Your review is welcome at whatever pace your life allows.

**These two documents are kept in sync.** Whenever the technical Claim Sheet is amended, this one is updated in the same session. Drift between them is a defect, not a backlog item.

---

## Amendments

Everything above this line is the contract as the agents agreed it, and it is never rewritten. Changes get **added on** here, in order, each dated. Each one says what we found, why it changes the plan, what the new plan is, and what it does to the definitions of success and failure. They are numbered the same way in both documents, so Amendment 2 here is Amendment 2 there.

**Read the status line.** *Proposed* means one agent wrote it and the other has not signed off yet — the work continues on the original text until they do. *In force* means both agents have explicitly approved it.

---

### Amendment 1 — The machine has a schedule now, and we had the memory story wrong

**Which parts this changes:** Slot 4 (what bounds the work) and Slot 10 (what it runs on).
**Written by:** Claude, Session 6, 2026-08-11 — at Codex's request.
**Status:** In force. Claude and Codex explicitly approved this amendment on 2026-08-11; Codex's exact-state approval was recorded in Session 6 at 22:10 PDT.

**What we found.** Four times across Sessions 2–5 the agents measured the machine's free memory and found almost none — between 0.9 and 4.5 GiB out of 31.7 — and both of them wrote that up as the *other* research projects competing with this one for the machine. **That was wrong, and you are the one who found out why:** the memory was being held by leftover Claude automation processes that had finished their work and never shut down, roughly 28 GiB of them, doing nothing at all. You cleared them. A fix so that stops happening is being built, not finished. You also decided how the two research projects share the desktop: **this one gets the daytime, the other gets overnight.**

**Why it changes the contract.** Slot 4 currently tells a reader, as a statement of fact, that other projects run on the machine at the same time and that there is no schedule and no way to reserve anything. There is a schedule now. Leaving the old sentence there would force some future session to work out from an old chat log which half of the contract still applies. Slot 10 also cites two of those misread measurements as evidence about competition.

**Here is the honest part, and it is the reason this amendment exists at all.** The measurements were right; the *explanation* attached to them was invented. Neither agent could see what was holding the memory, and neither said so — the number was ours to report, the cause was not ours to assert. That is recorded here rather than quietly fixed, because a project that will publish a negative result has to be a project that says out loud when it got something wrong.

**What actually changes.**

1. **The description of the machine.** Two Dandelion research projects share it under your allocation: this one aims heavy work at the daytime; the other aims at overnight. It is a convention, not a reservation — nothing enforces it and nothing guarantees the memory will be there.
2. **The old measurements are marked as misattributed.** No future session may reason from the *shape* of that four-session decline; it was measuring accumulating dead processes, not competition.
3. **The leak fix is in progress, not done.** If free memory ever collapses again while the graphics card's memory stays untouched, that pattern is now a *known signature* and gets named in the session report rather than re-diagnosed from scratch.
4. **Nothing about how we decide to start a job changes.** Measure free memory immediately before every heavy step. A run may take at most 75% of what was free at that moment, and must leave at least 4 GiB of system memory and 2 GiB of graphics memory for everything else. If it does not fit, do not start it. Never inherit a number from a file — including this one, and including a number measured during a quiet stretch.
5. **No part of the experiment gets bigger or smaller because of this.** The ladder, the segment lengths, the block counts, the compute ceilings and the sorter panel are all exactly as they were. If the panel ends up smaller, it will be because the pilot measured it smaller.

**Does this change what counts as success or failure?** No. It adds no rule about results and removes none. "We ran out of machine before we ran out of question" is still a possible, publishable failure — a schedule is not a guarantee.

---

### Amendment 2 — We can pick a recording that avoids the leakage problem entirely, and CA1 has exactly sixteen usable donor cells

**Which parts this changes:** Slot 7 (how we will know), Slot 5 (how the work is done), Slot 9 (how big we build), Slot 13 (what does not transfer).
**Written by:** Claude, Session 6, 2026-08-11, from the Session 5 provenance work and Codex's review of it.
**Status:** In force. Codex explicitly approved this exact wording in its Session 6 (2026-08-11 22:11 PDT), after first cutting two claims about shared rigs and mouse strain that the evidence never established; Claude approved the same wording in Session 7 (2026-08-12 09:48 PDT), having gone and checked what the recordings actually say about where the animals came from. Amendment 4 is what that check found; it adds to this one rather than reopening it.

**What we found.** The library of donor spike shapes has a column naming where each one came from. Nobody had opened it — the earlier work counted the distinct values without reading them. Read properly, it says that **every single donor shape for this probe type comes from the same public collection our host recordings come from**: 37 probe insertions, 24 recording sessions, 12 mice. Three things follow.

- **"Don't use donors from the host's own recording" turns out to mean three different things** — same probe insertion, same session, or same *mouse* — and they give very different answers. Some brain areas look perfectly healthy under the loosest reading and drop to **zero usable donors** under the strictest. The contract never said which one it meant.
- **We can sidestep the whole question rather than answer it.** The collection holds 459 raw recordings from 139 mice, and only 12 of those mice contributed donor shapes. So **429 of the 459 possible host recordings come from an animal that contributed nothing** — pick the host there and all three readings become moot at once, at no cost, and every brain area keeps its full set of donors.
- **CA1 — the region we want to inject into — has a hard ceiling of sixteen donor shapes in the entire library.** Not sixteen after filtering. Sixteen in total. There is no filter setting that produces more, because no more exist.

**Why it changes the contract.** Two reasons. First, the contract asks the two arms to be balanced on the *number* of source recordings they draw from; now that we can read the actual identities, matching the identities is strictly better than matching a count, and the contract should ask for the better thing. Second, the plan calls for five repeat rounds with ten injected units each — fifty slots — drawn from a pool of sixteen. **Repeating the experiment cannot introduce donor cells that do not exist.** That changes what a Tier A result *means*, which is a contract question, not a detail.

**What actually changes.**

1. **The host recording must come from one of the 127 mice that contributed no donor shapes.** That is now the rule, replacing "exclude the host's own source recording." Chosen rather than filtered.
2. **What that does *not* fix goes in the limitations, in plain sight.** Host and donors still come from the same collection, the same consortium, the same IBL acquisition program and the same probe type. Nothing available fixes that, because this probe type has exactly one donor collection in existence. **Separating the animals is not the same as independent sources**, and no artifact this project ships is allowed to imply otherwise.
3. **Where possible, each donor and its counterpart in the other arm come from the same source recording** — same insertion if we can get it, else same session, else same animal. If we have to settle for less, we say so, per arm, with the reason. We do not quietly fall back to matching counts.
4. **All sixteen CA1 donors are eligible.** The amplitude range in the contract was always a target for *after* rescaling, not a requirement the donor had to already meet — so the four higher-amplitude ones are in. Sixteen donors for a ten-slot arm: six spares.
5. **The sixteen get used on a deliberate rota rather than by random draw**, so each appears three or four times across the fifty slots instead of some appearing eight times by chance. The randomness moves to the things we have plenty of: which slot, which spike times, which position on the probe.

**A new "this does not transfer" clause.** Because the matched arm uses up essentially the whole CA1 donor supply, **a Tier A result is a statement about those sixteen spike shapes in that one recording — not about region-matched injection in general.** More repeat rounds make the number more precise; they cannot make it more general. **This gets said even if the final interval is narrow**, because a tight number around an exhausted pool is precision, not generality, and confusing the two is exactly the kind of overclaim this contract exists to prevent.

**Does this change what counts as success or failure?** The success criteria keep their shape. The pre-declared failure — "no host and region combination can support both arms fairly, so Tier A is dropped and we publish why" — is unchanged, and is still what happens if the remaining checks kill more than six of the sixteen.

**One thing deliberately left out.** Codex also proposed changing how Tier A's "nothing actually changed" control band is built. The two agents do not yet agree on that, so it is **not** in this amendment and the original design still stands. Nothing gets generated on the new construction until that is settled and written down separately. If it stays unsettled, it comes to you.

---

### Amendment 3 — The "nothing changed" comparison has to be lopsided in the same way the real one is

**Which parts this changes:** Slot 5 (how the work is done), Slot 8 (your verification picture), Slot 11 (what counts as success), Slot 14 (what gets published).
**Written by:** Claude, Session 7, 2026-08-12 — at Codex's request, settling the one disagreement Amendment 2 left open.
**Status:** Proposed. Codex has not signed off on the exact wording yet, and **nothing may be generated on this design until it does.**

**The thing this is about.** The contract's strongest safety check is a fake comparison. We build two arms where **nothing was actually changed**, sort them exactly like the real ones, and look at how much apparent difference the machinery invents on its own. If the invented difference is as big as the real one, the real one means nothing. That grey band is the second thing you look at in your verification picture.

**What we found.** The real Tier A comparison is lopsided. One arm draws its spike shapes from a pool of **sixteen** — every CA1 donor in existence for this probe. The other draws from a pool of about **1,149**. The fake comparison, as originally written, draws both of its arms from one pool, so it is *even* where the real one is *lopsided*. It therefore cannot tell us what we need to know: how much apparent difference this particular lopsided design can manufacture out of nothing.

**The disagreement, and how it was settled.** Codex proposed fixing it by making the fake comparison a straight *repeat* of the real one, and reading how much the answer wobbles between repeats. I pushed back, and Codex withdrew the proposal after reading the argument. The reason is worth keeping, because it is the whole point of the check: **a repeat would reproduce a mistake as faithfully as it reproduces a real effect.** If our own selection machinery quietly biases one arm, every repeat contains that same bias, the wobble between repeats is tiny, the band looks reassuringly tight — and we publish an artifact of our own procedure as a finding. The check exists to catch exactly that, so it cannot be built in a way that hides it.

**What actually changes.**

1. **The first fake arm draws from a fixed set of sixteen** shapes taken from the big region-blind pool — chosen once, by a fixed random seed, to spread out across amplitude, signal quality and depth roughly like the real CA1 sixteen do. Those sixteen get named in the published run configuration.
2. **The second fake arm draws from the whole big pool**, matched to the first one by exactly the same matching procedure the real comparison uses.
3. **Neither fake arm pays any attention to brain region.** Nothing is manipulated — which is what makes it a genuine "nothing changed" check — while the *lopsidedness* of the real design is reproduced faithfully.
4. **The sixteen get used on the same deliberate rota** as the real arm's sixteen, so donor reuse matches too.
5. **The cost does not move.** Same two fake arms per round, same five rounds, same compute budget.
6. **This applies to Tier A only.** Tiers B and C reuse the same spike shape in both arms, so their pools are already even and their fake comparison is built as originally written. The report says, per tier, which construction produced that tier's band.

**The one thing it cannot do, said now rather than later.** It copies the lopsidedness, the reuse, the matching and the seeds. It does **not** copy the fact that the real matched arm is all-CA1, and no honest "nothing changed" check can, because being all-CA1 *is* the change. So a tight band means "the lopsided machinery did not invent a difference this big." It does not mean "region is the only thing that differs between the arms" — that is what the balance checks and the manipulation gate are for.

**Does this change what counts as success or failure?** No. Same thresholds, same intervals, same failure shapes. It fixes how one diagnostic is built, and it adds one publishing obligation: the figure caption has to say which construction produced the band it is showing.

---

### Amendment 4 — The donated spike shapes and the host recording come from different labs, and all the donations come from one lab

**Which parts this changes:** Slot 7 (how we will know), Slot 13 (what does not transfer).
**Written by:** Claude, Session 7, 2026-08-12, from going and checking the recordings rather than arguing about them.
**Status:** Proposed. Codex has not signed off yet.

**Why this exists.** Amendment 2 said host and donor recordings still share "the same collection, the same consortium, the same acquisition program and the same probe type" — a sentence Codex had just corrected, because an earlier draft of it also claimed they shared a rig design and a mouse strain, which nobody had checked. Rather than accept the correction on the argument alone, I went and read what the recordings themselves say. It cost 89 MB of file headers and no recording data at all.

**What the recordings say.**

- **They carry no mouse strain or genotype field whatsoever.** So that claim was not merely unsupported — it is **uncheckable from our own materials.** The rule is now that we never report strain as the same *or* as different, in any artifact.
- **All twelve donor animals belong to one laboratory**: `cortexlab`, University College London. Every donated spike shape this project can use, in both arms, comes from that one lab.
- **All nine candidate host animals belong to different labs entirely** — three at Cold Spring Harbor, six at New York University. There is **no overlap** with the donor lab, and even the version of the behavioural task differs between the two sides.

**Why it matters, in both directions.** The good direction: picking a host from an animal that donated nothing turns out to separate host from donor by *laboratory, institution and rig*, not just by animal. That is a stronger separation than the contract claims, and now it is something a reader can verify rather than take our word for. The other direction is the one that goes in the limitations: **the entire donor library is one laboratory's work.** So a Tier A result is not a statement about "CA1 spike shapes." It is a statement about *one lab's* CA1 spike shapes, from sixteen cells in twelve mice. There is no alternative library for this probe, so this is not a choice we made — but it is a boundary we have to say out loud.

**What actually changes.**

1. **The limitations section states the checked position**: same collection, consortium, acquisition program and probe type; **different** laboratory, institution and task version. With the file that proves it.
2. **Strain and genotype get named as uncheckable** — once, plainly, so a reader is not left to guess from silence.
3. **"Host lab contributed no donors" becomes a recorded property, not a new hurdle.** Every current candidate already passes it, so it eliminates nobody. It is written down so a future search knows it was checked rather than assumed.
4. **The evidence has a boundary.** One recording was read per animal, so the lab is confirmed for that recording. In this dataset an animal belongs to one lab, so this is safe — but the evidence is what it is, and it gets described that way.

**A new "this does not transfer" clause.** *The donated shapes are one laboratory's.* Whatever Tier A finds is conditional on that lab's recording and processing practice, on top of being conditional on those sixteen CA1 shapes. Both conditions get stated together.

**Does this change what counts as success or failure?** No. Nothing here can make a tier pass or fail. It adds one limitation and one verified fact.

---

## If you read only one part of this

Read the three sentences below. Everything above is what makes them precise.

1. **We are measuring whether making fake spikes more realistic changes which spike sorter looks better** — not which sorter is best.
2. **A "no" is a real result and gets published exactly as loudly as a "yes."** A *"we could not tell"* is a third, separate answer, and the contract forbids reporting it as a "no."
3. **Nothing gets sorted until we have shown, visibly, that the realism knob actually turned** — because otherwise "realism did not matter" and "we built it badly" look identical forever.
