# Progress Report — the provenance amendment, and what checking it turned up

**Written:** 2026-08-12, Claude Session 7
**Trigger:** Claim Sheet Amendment 2 reached `In force` this session — an approved amendment is a reporting event.
**Phase:** 2 (Execution). No sorter has run. No scientific result exists yet.

---

## The short version

Amendment 2 is now part of the contract. It says the project will pick its host recording from an animal that contributed none of the synthetic spike shapes we inject — which removes a contamination problem entirely rather than managing it — and it admits that the pool of usable CA1 spike shapes is exactly sixteen, forever, which bounds what a Tier A result can claim.

Approving it meant re-reading it properly, and re-reading it properly meant checking a sentence in it that neither agent had evidence for. That check turned into the most interesting thing this session produced, and it went in both directions at once: **the recordings are more separated than we claimed, and the spike-shape library is narrower than we said.**

Separately, one of the remaining checks on candidate host recordings got done: **can ten synthetic neurons actually fit inside the target brain region?** Nine of thirteen candidates can. Four cannot. And the answer depends on a number nobody has measured yet, which is now the top of the list.

---

## A little background, so the rest reads cleanly

**What we are testing.** Spike sorting is the problem of deciding which of the electrical blips in a brain recording came from which neuron. There is no answer key for a real recording, so the field grades sorting software using **hybrid recordings**: take a real recording, inject synthetic spikes at times you chose, and see whether the software finds them. The maintainers of the standard tool for this wrote in print that they do not know whether their synthetic spikes are realistic enough for the resulting scores to mean what everyone treats them as meaning. We are testing that.

**Where the pieces come from.** The synthetic spike shapes are real waveforms harvested from other recordings — a public library called [`hybrid_template_library`](https://github.com/SpikeInterface/hybrid_template_library). The host recording they get injected into comes from [DANDI 000409](https://dandiarchive.org/dandiset/000409), the International Brain Laboratory's Brain Wide Map. The [IBL](https://www.internationalbrainlab.com/) is a consortium of many labs running a deliberately standardized experiment, which is why so much of this data is comparable at all.

**Why "where it came from" keeps mattering.** If a donated spike shape came from the very recording we inject it into, the test is partly rigged — the sorting software would be finding a shape that is already there. That is the contamination problem Amendment 2 closes.

---

## What Amendment 2 settles

Two things, both found by reading a column of data nobody had opened.

**One.** Every donated spike shape for this probe type comes from twelve mice inside the same public collection our host recordings come from. But that collection holds 139 mice. So we simply pick a host from one of the other 127, and the contamination question stops existing rather than getting managed by degrees.

**Two, and less comfortable.** The brain region we intend to inject into — CA1, part of the hippocampus — has exactly **sixteen** donated spike shapes in the entire library. Not sixteen after filtering. Sixteen in total. Our design injects ten at a time and repeats five times, which is fifty slots drawn from sixteen shapes. **Repeating the experiment cannot create spike shapes that do not exist.** So a Tier A result will be precise about *those sixteen* and cannot be general about region-matched injection, and the amendment requires us to say so even if the final number looks tight. A narrow answer around an exhausted pool is precision, not generality, and treating one as the other is the exact overclaim this project exists to avoid making.

---

## The unexpected part: what happened when I checked a sentence

Amendment 2 originally ended with a limitations sentence listing what picking a distant mouse does *not* fix — including that host and donor share "the same rig design" and "the same mouse strain." Codex, reviewing, cut both: nobody had checked them.

I could have accepted that on the argument. Instead I read the recordings' own metadata — 21 animals, about 89 megabytes of file headers, no actual recording data. Three findings.

**The strain claim was not weakly supported. It was uncheckable.** These files carry no genotype or strain field at all. So the honest position is not "the same" and not "different" — it is *we cannot know from our own materials*, and the project now says that once, plainly, so a reader is not left inferring from a silence.

**All twelve donor animals belong to one laboratory** — `cortexlab` at University College London. Every synthetic spike shape available to this project for this probe, in both arms of the experiment, is one lab's work.

**All nine candidate host animals belong to different labs** — three at Cold Spring Harbor, six at NYU. No overlap with the donor lab at all.

Both directions matter. The good one: picking a host from a non-donating animal turns out to separate host from donor by *laboratory, institution and rig*, not just by animal — a stronger claim than the contract made, and now one a reader can verify instead of taking our word for. The other one goes in the limitations: **the donor library is one laboratory's work**, so whatever we find about "region-matched spike shapes" is really about one lab's spike shapes. There is no alternative library for this probe, so this is not a choice we made — but it is a boundary we have to state. That is now written as **Amendment 4**, awaiting Codex's sign-off.

There is a small methodological point worth keeping here, because it will recur: **removing an unverified claim can quietly create a new one.** A limitations list that stops mentioning strain reads, to a careful reader, as though strain were checked and found different. Going and looking was cheap. Guessing which way the silence pointed would not have been.

---

## What else got done: can ten neurons actually fit?

The contract has carried an unresolved requirement since it was written: a host recording is only usable if ten synthetic neurons can be placed inside the target region *without crowding each other and without ambiguity about what tissue they are in*. Otherwise the host fails, rather than getting a convenient label invented for it.

That check ran this session, on all thirteen candidate brain regions found so far, again from file metadata only — 170 MB, no recording data, nothing downloaded.

**The ambiguity half came back clean.** Every one of the thirteen candidate CA1 zones is **100% pure**: every recording contact inside the zone is labelled CA1, with the nearest differently-labelled contact exactly one contact-row beyond each edge. That is better than expected and closes that half of the requirement outright.

**The crowding half separates the field: nine pass, four fail.** The four failures are simply short zones — a CA1 band 420 micrometres tall cannot hold ten well-separated neurons the way a 700-micrometre one can.

**And here is the honest catch.** A synthetic neuron is not a point; its signal spreads over a stretch of the probe, so it has to sit far enough inside the zone for its whole footprint to land in CA1. **How far is "far enough" is a number nobody has measured yet** — it needs the actual waveform files from the upstream library. I ran the check across a range of plausible values instead of picking one, and the range matters a great deal: at a generous setting, nine zones pass; at a conservative one, only two do. So the verdict is currently *parameterized*, not decided, and measuring that footprint has just become the highest-value remaining piece of this work.

**Two things fell out sideways, both useful.** One candidate — NYU-39 — passes the geometry check and should still be dropped: the field's own sorting software recovers **twenty-two** units in its CA1 zone, only **one** of them well-isolated, against 174 and 32 in a comparable candidate. A neighbourhood that empty is not a fair place to grade anything. And the contract's target for how loud to make the injected spikes (50–200 microvolts) turns out to bracket the real well-isolated neurons in these zones (51–110 microvolts typical, reaching 258) — reassuring, with a caveat I wrote down rather than skipped: the two amplitude numbers may not be measured the same way, and that comparison has to be checked before the target counts as validated.

---

## What is working, what is not

**Working.** The screening approach is holding up remarkably well economically: every result in this report came from reading file *headers* over the network — a few megabytes against recordings that are 18 to 197 gigabytes each. The project has now characterized the anatomy, duration, provenance, label purity, placement capacity and native neuron density of eleven candidate recordings without downloading one.

The review process is also doing its job in both directions. This session Codex's correction of my unsupported claim was upheld and strengthened; last session my objection to Codex's control-group design was upheld and Codex withdrew it. Neither agent is rubber-stamping the other.

**Not working, or not done.** Two gates on host selection still have not run — **drift** (does the probe move relative to the brain during the recording?) and **noise level** — and both need actual recording data and the software stack that Codex's feasibility pilot installs. Until they run, no host is pinned, and pinning a host is what unblocks everything downstream.

I also found and rejected a shortcut: these files contain a column literally named "cumulative drift per hour," which would have been a free answer to the drift question. Its values run to millions of micrometres per hour, which is physically impossible for a probe in a mouse brain, so whatever it accumulates it is not what its name suggests. It is recorded as unusable rather than quietly used.

**Nothing is blocked on you.** There are no open director requests. The two new amendments need Codex's approval, not yours.

---

## Verification artifact

No update. Slot 8's verification artifact — the thing built so you can check the result yourself without reading the technical report — has nothing new this session, because no result exists to verify yet. It gets built as results arrive, not assembled at the end.

---

## What comes next

1. **Measure how far a synthetic neuron's signal spreads.** This decides the placement verdict above, and it is currently the cheapest thing standing between us and a pinned host.
2. **Codex's feasibility pilot** — a 60-second test run that measures whether this desktop can actually sort a 384-channel recording, and which sorting programs it can support. Everything about scale downstream depends on that number.
3. **Drift and noise on the leading candidates**, once that stack exists.
4. **Amendments 3 and 4** through Codex's exact-state review.

The order is deliberate: every one of those is a measurement that could invalidate a plan, and this project's whole posture is to take those measurements before building on top of them rather than after.
