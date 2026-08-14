# Progress Report — we built a safety net, and this session found the hole in it

**Claude, Session 24 · 2026-08-14 09:25 PDT**
**Trigger:** regular cadence — my eighth session since the last count-based report.
**Phase:** 2 (Execution). Still no host recording chosen, no data generated, no sorter run, no result of any kind.

---

## The short version

We are choosing which real recording to inject our fake neurons into. One of the things that disqualifies a recording is **drift** — the probe and the brain tissue slowly sliding relative to each other during the hour-long recording, so that a neuron's signal migrates across the probe's contacts. We wrote a test for it before looking at any candidate, so that we could not pick the threshold to suit the answer.

The test has a known soft spot, and we have spent the last several sessions building a diagnostic to expose it. This session I measured what that diagnostic can actually see, and the honest answer is: **less than we had been claiming.** A recording can pass our drift test while a substantial minority of its neurons are genuinely moving by more than the amount we said would disqualify it — and the diagnostic we built to catch exactly that case cannot distinguish it from ordinary measurement noise.

The response is not to build a bigger diagnostic. It is to write down plainly that a clean-looking diagnostic is not evidence of a clean recording, and to carry that caveat forward with the result.

## The background you need for the rest of this

A Neuropixels probe is a thin silicon shank with hundreds of tiny recording contacts down its length. It sits in living tissue for an hour or more, and over that time the brain moves — breathing, heartbeat, slow settling of the tissue around the probe. From the software's point of view, this looks like every neuron's signal sliding up or down the probe. Sorting software has to either follow that motion or lose track of the neuron, and there is a whole line of research on handling it ([Garcia et al., 2024, *eNeuro*](https://doi.org/10.1523/ENEURO.0229-23.2023)).

For this project, drift is a nuisance we want to *avoid* rather than study. We are asking whether making injected fake neurons more realistic changes how sorters are graded. If the recording underneath is also drifting, that adds a second thing changing at once. So we screen candidate recordings and use a steady one.

The candidate recordings are the [IBL Brain-Wide Map](https://dandiarchive.org/dandiset/000409), a large public set released under an open licence. Helpfully, they ship not just the raw signal but a processed table that already includes, for every detected spike, an estimate of **how far up the probe that spike appeared**. So we can measure drift without re-doing any of the heavy work: for each neuron, track its estimated depth over time and see whether it wanders.

## What our drift test does, and the soft spot it was always known to have

For each neuron at the injection site, we compute its typical depth in each one-minute slice of the recording. Then we combine the neurons into a single trace by taking the **median** across them — the middle value.

The median is the right choice for a specific reason: real probe movement is *common to every neuron in the neighbourhood*, because they are all being carried by the same tissue. Meanwhile, each individual neuron's depth estimate is noisy for reasons that have nothing to do with the others. Taking the middle value across many neurons cancels the individual noise and keeps the shared movement. Then we ask how far that combined trace wanders inside its worst ten-minute stretch, and compare it to a threshold of 20 µm — one row of contacts on the probe.

**The soft spot is the flip side of that same choice.** A median only reports what the *majority* is doing. If five neurons out of eleven move and six do not, the middle value sits in the group that did not move, and the combined trace reports nothing at all. My collaborator built exactly that counterexample several sessions ago, and it is a permanent test in our code.

So we added a diagnostic: alongside the combined figure, publish **each individual neuron's** wander, so a reader can look at the raw material behind the summary and see whether some neurons were moving while others were not.

## What this session found

The diagnostic has now been through several rounds of correction between the two agents — first because it was measuring the wrong stretch of time, then because it shipped with no instructions for how to read the numbers, then because one of those instructions was stated too strongly. Each round narrowed it. This session asked the question that all of those rounds had left alone:

**When the diagnostic shows nothing interesting, what does that mean?**

It is the question that matters most, because "nothing interesting" is what you see when a recording passes, and it is the moment a reader decides to trust the result.

I built the case that would break it before writing any claim about it — a habit this project has adopted after being wrong in this exact way three times. The result:

> **Twenty-one neurons. Ten of them genuinely move 30 µm — half again our disqualifying threshold — inside one ten-minute window. The recording passes both of our gate's numbers. And the ten movers' individual wander overlaps the eleven steady ones, with six of the ten sitting entirely inside the steady range.**

There is no pattern in the diagnostic for anyone to notice. The reason is that individual neurons' depth estimates are genuinely noisy — much noisier than the combined median, which is the whole point of combining them — so a real 30 µm movement in one neuron does not stand out against another neuron's 35 µm of pure noise.

**The direction of the effect is the part I would most want the director to take away.** The masking gets *easier* as the recording gets better. Holding everything else fixed, the same construction gives a combined figure of 21.98, 18.14 and 14.94 µm at 11, 21 and 41 neurons. More neurons means the median cancels more noise — and also hides a moving minority more effectively — while the individual traces stay exactly as noisy as before. Our candidate recordings hold between **22 and 267** neurons at the injection site. The recordings with the most data, which are the ones we would otherwise most want, are the ones where this is worst.

## What we did about it, and the option we deliberately did not take

There was an obvious fix available: build a second statistical machine that tells you how much wander an individual neuron shows from noise alone, so each neuron's number could be judged against its own yardstick.

We did not do it, for the same reason we have declined similar offers twice before in this project. That machine would need a threshold — how much individual wander is too much — and **we have no basis for one.** A number invented to fill a gap in a diagnostic tends to acquire authority it never earned, and this project's whole method is to avoid setting thresholds after seeing the data.

So the document now says the true thing instead: **an audit showing nothing is not evidence that the recording is steady.** The caveat that our drift result depends on movement being visible to a majority of neurons stays attached to the result rather than being quietly retired by a diagnostic that cannot discharge it. The diagnostic keeps its real job — when it *does* show a separated group, that is worth publishing — and loses the job it could not do.

Both counterexamples are now permanent automated tests, so no future session can re-introduce the claim by accident. The test suite is at 86 checks.

## What's working

- **The review process is doing what it is for.** This section has now taken nine rounds between the two agents. Not one of them has been the same disagreement twice — each round accepted the previous round's corrections in full and then found something *new*, usually as a direct consequence of the repair. This session I accepted my collaborator's correction completely, and then found that his repair had exposed the question above.
- **The habit of building the counterexample first keeps paying.** Twice now in two sessions, the repair I was about to write was falsified in a few minutes by constructing the opposite case before committing to it.
- **Nothing measured, nothing spent.** Every one of these rounds ran on small synthetic data — the full test suite takes 48 seconds. No candidate recording has been read, so none of this has cost the project the ability to make an honest first measurement.

## What isn't working

- **This section has been open a long time.** Nine review rounds on one part of one document is a lot, even granting that each round found something real. Both agents have now independently said in writing where the end is, and we have agreed that if the next round produces a disagreement rather than a new finding, we escalate to you rather than taking a tenth turn.
- **The measurement still has not started.** No candidate recording has been read, no host is pinned, and the script that will read the archive **has not been written** — writing it is blocked until this review closes, because the rules it implements are the thing under review. That is the correct order — the rules have to be fixed before the values are visible — but it does mean the project's visible progress is still all specification.
- **Three things remain genuinely unresolved**, none of them new this session: a capacity check on whether ten fake neurons can be placed in the injection zone under the stricter rule a recent amendment introduced; the preprocessing half of an amplitude question that cannot be answered from metadata; and 66 anatomical labels that only a brain atlas could resolve, where the atlas we would want carries a non-commercial licence we have chosen not to accept.
- **No open blockers on you.** `director_requests.md` has nothing waiting.

## Verification artifact

Nothing new to report. The director-facing verification artifact is a Phase 3 obligation and no work has been done on it this session; I would rather say that than manufacture an update.

## What's next

If my collaborator confirms the current state, the next stretch of work is the script that actually reads the archive — targeted reads of just the neurons at the injection site, checking four specific things about the data before it computes anything, and then producing the first real drift number this project has ever had, for the top-ranked candidate recording. That is the first measurement of the project.
