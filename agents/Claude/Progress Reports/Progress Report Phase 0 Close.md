# Progress Report — Phase 0 Close

**Written:** 2026-08-11 12:20 PDT
**Trigger:** Phase transition — Phase 0 (Literature Review) closed this session
**Agent:** Claude (Session 2)

---

## The short version

Phase 0 is done. Both agents surveyed the field independently, compared notes, disagreed about two things, settled both, and closed the phase. The project now has a **Claim Sheet** — the contract that says what we are testing, how, and what would count as success, failure, and inconclusive, all written down *before* any result exists. That draft is with Codex for review.

Two things changed the shape of the project along the way, and both are worth your attention. One is a mistake I made and Codex caught. The other is a measurement I ran this session that quietly reversed the order in which we have to make a key decision.

---

## What the project is actually asking, in plain terms

A brain recording probe picks up electrical spikes from many neurons at once, all overlapping. A **spike sorter** is the algorithm that untangles that blur and says which spike came from which neuron. Almost all of systems neuroscience is built on top of that step.

The awkward part: for a real recording, nobody knows the right answer. There is no answer key. So to test whether a spike sorter works, the field uses a trick called a **hybrid recording** — take a real recording, and inject some extra fake spikes into it at times you chose yourself. Now you know where those spikes are, so you can check whether the sorter found them.

That trick works only if the fake spikes are enough like real ones. If they are easier to find, every sorter looks better than it is. Worse, if they are easier for *one kind* of sorter than another, then comparing two sorters on hybrid data is partly comparing how well each one handles your fake spikes — not how well it does the real job.

The people who built the field's standard tool for making these hybrid recordings said, in print in their own paper, that they do not know whether their fake spikes are realistic enough. That is the sentence this project exists to test. ([The anchor paper, open access](https://doi.org/10.7554/eLife.110170.3).)

---

## Where things stand

**Phase 0 (literature review) closed today.** Phase 1 (turning the idea into a precise contract) is underway — the Claim Sheet draft exists and is in review. Nothing is blocked on you, and there is nothing in `director_requests.md` because nothing has needed you yet.

The plan we converged on tests three kinds of realism, **one at a time**, in order of how much work each takes to build:

1. **Region-matched waveforms.** A neuron's electrical signature depends on which part of the brain it lives in — enough that you can classify a neuron's region just from its waveform shape ([Jia et al. 2019](https://doi.org/10.1152/jn.00680.2018)). Right now the fake spikes are copied from whatever region happens to be available, not the region of the recording they are being injected into. Fixing that needs no new code at all — the template library already labels its brain regions. This is pure measurement.
2. **Firing that follows the rest of the brain.** Real neurons speed up and slow down together with the population around them. The injected spikes currently fire at random, independent of everything else. The paper's own authors proposed this fix themselves. Modest new code.
3. **Bursting, with the waveform shrinking as the burst goes on.** Real neurons fire rapid bursts of spikes a few thousandths of a second apart, and — this is the interesting part — **the electrical signature gets smaller with each spike in the burst** ([Harris et al. 2001](https://doi.org/10.1016/S0896-6273%2801%2900447-0)). A fake spike copied from a fixed template always looks the same, no matter what the neuron just did. This is the genuinely missing piece, and it has to be built before it can be measured.

**An honest note on that split**, which is also written into the Claim Sheet: the first is measurement, the second and third are engineering done in order to make a measurement possible. That is still research, but the project says so rather than presenting itself as pure measurement.

---

## What was found that I did not expect

### 1. A prior that cuts against the comfortable answer

Going in, the appealing outcome was "realism does not matter" — the field's tool is fine, an open question closes, done. The literature makes that less likely than it looked. A 2020 study spanning roughly 35,000 ground-truth units found that synthetic test data produces a **systematically different pattern of errors** from real test data, and blamed it on firing statistics specifically ([SpikeForest](https://doi.org/10.7554/eLife.55167)). And a 2018 paper raised essentially the same worry six years before the paper we are anchoring on restated it.

So this is not a fresh suspicion nobody has had. It is a durable open question that several groups have gestured at and nobody has run the controlled version of. That is good for the project's value and bad for anyone hoping for a quick, tidy null.

### 2. I got something wrong, and my collaborator caught it

Worth reporting plainly, because how the two agents handle disagreement is part of what this framework is testing.

In my first session I proposed using the anchor paper's own measured difference between two spike sorters as the yardstick for "is this effect big enough to matter." Codex blocked it, and was right: those two numbers are scaled by different things, over different samples, so subtracting one from the other is not a meaningful operation. I accepted the correction without argument and rewrote that part of the contract. The decision threshold is now measured *inside our own experiment* rather than imported from someone else's.

I also carried a stale fact about the size of the template library — I had read the tutorial's example table and treated it as the real thing. Codex went and checked the live data. **Before accepting his numbers, I re-downloaded the file myself and confirmed it matched his byte for byte.** It did, exactly. That is not distrust; a checkable claim should get checked, and it took two minutes.

### 3. The measurement that reversed a decision order

This is the substantive new result from this session, and it changes how Phase 2 has to start.

The template library holds about 7,900 waveforms, roughly 2,200 of them from the probe type we would use. Filtered down to the ones with sensible signal strength — the range the anchor paper itself uses — **37 brain regions have enough templates to run the experiment.** Comfortable.

Then I applied a rule Codex had proposed and I agreed with: **you cannot inject spikes into a recording using templates that came from that same recording's own dataset.** That is leakage — the sorter would be finding spikes that were partly there already, and the test would be rigged in a way that is hard to see. Sensible rule. But when you actually enforce it, the picture narrows sharply: **only 7 brain regions survive** with enough templates left over. Thirteen of the original 37 drop to literally zero, because a single dataset had supplied all of their templates.

The consequence is a reversal of order. We had assumed we would pick a good recording first and then find matching templates. In fact **the templates constrain which recording we can use**, not the other way round. Either we pick from a shortlist of seven regions, or we deliberately pick a recording from outside the library's own sources and say why.

None of that makes the project harder. It makes a decision that would otherwise have been made carelessly in Phase 2 into one that is made deliberately, now, with the numbers in front of us. The script that produces it is already in the reproducibility packet, so you or anyone else can re-run it and change the filter to see how the answer moves.

---

## What is working

**The two-agent structure is doing real work rather than producing agreeable noise.** Codex blocked my first synthesis on two specific points, both were right, and both were caught before they reached the contract — which is exactly where a bad threshold does the most damage, because a success bar written wrong quietly determines the answer. In the other direction, my leave-one-out check sharpened his feasibility conclusion without contradicting it. Neither of us has rolled over, and neither has been obstructive.

**Both agents independently reached the same measurement of the same live resource**, down to the cryptographic checksum. That is a small thing, but it is the kind of small thing that makes the larger claims checkable.

**Nothing needed you, and nothing needed money.** No paid tools, no paid data, no downloads that required a login. Everything so far runs on open licenses that were read rather than assumed.

---

## What is not working, or is a live risk

**The machine is the real constraint, and it is tighter than the specs suggest.** The desktop has 32 GB of memory. A test run before this project started showed the main spike sorter using **29.3 GB** of it at peak. At two separate points during this session the machine had **under 4 GB free**, because other Dandelion projects run on it at the same time and are not coordinated with this one. Started at either of those moments, that run would have failed — slowly and confusingly, which is the expensive way to fail. The contract now requires measuring free memory immediately before every heavy step and simply not starting what does not fit. I recorded the measurements I took this session rather than describing them from memory.

**We may only be able to afford two spike sorters, not three.** Comparing two sorters from the same family is the setup *least* likely to show a difference, which means a null result from it would be weak evidence. We want a third, mechanically different one. Whether this machine can run it is an open question that a small pilot will answer. The contract pre-commits to the honest fallback: if it does not fit, we run two and say plainly that the narrow panel limits the claim — rather than discovering that mid-project and rationalizing it.

**The cheapest test is the least likely to answer the headline question**, and that is an uncomfortable shape. Region matching is the axis we can test with no new code, so we test it first. But changing waveform *shape* probably affects all sorters similarly, whereas changing *timing* hits the part where sorters genuinely disagree with each other. So there is a real risk of running the cheap test, getting nothing, and appearing to have answered the big question. The contract now states explicitly that **a null on the first axis licenses no conclusion about the other two, and the project cannot conclude on that axis alone.** I would rather have that written down before results exist than argue about it afterwards.

**One small verification item is still open**, and it is honest to leave it open: neither agent could confirm from the original source whether one older tool copies individual real spikes or an averaged version of them. It does not affect anything we are building, so it stays flagged rather than blocking anything.

---

## The verification artifact — what you will eventually be handed

The contract commits us, before any results exist, to building you a specific thing so that you can check the result yourself without reading the technical report. It is one command that produces two pictures and one sentence.

**Picture one: did the knob actually turn?** The same injected neuron, shown side by side as the plain version and the realistic version — the raw electrical trace, the spacing between its spikes, and its spike size plotted against that spacing. You do not need to know what a template is to see whether the two columns look different. If they look the same, the manipulation did nothing and nothing downstream matters.

**Picture two: did it change the answer?** The sorters' scores under both conditions, with a grey band behind them showing how much the numbers wobble from random chance alone. If the change sticks out of the grey band, it is real. If it sits inside it, it is noise.

Then one printed sentence saying which happened, in words.

There is nothing to show you yet — the first picture becomes buildable as soon as any generator passes its check, which is well before there are any sorter results. I will show it to you at that point rather than waiting for the end.

---

## What is next

1. Codex reviews the Claim Sheet; we converge on a single state we both explicitly approve.
2. I write the plain-language companion to the Claim Sheet, and the first pass of your Study Guide.
3. We agree who does what, and Phase 1 closes.
4. Phase 2 opens with the small feasibility pilot — install the software stack, pin every version, and time the candidate sorters on a one-minute segment to find out what this machine can actually afford before committing to anything larger.

**When the Claim Sheet is agreed, it gets logged for your review.** That review is deliberately non-blocking: we keep working while it is pending, and if you disagree with something, it runs through the amendment process and gets appended and dated rather than quietly rewritten. You are not a bottleneck by design, but the contract is genuinely yours to push back on — and Slots 11, 12, and 13, the pre-declared success, failure, and inconclusive shapes, are the parts most worth your ten minutes.
