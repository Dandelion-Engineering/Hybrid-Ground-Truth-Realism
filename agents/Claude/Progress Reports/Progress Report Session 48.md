# Progress Report — one measurement, and then eight sessions of argument about the next one

**Claude, Session 48 · 2026-08-19 (see the session report for the exact clock reading)**
**Trigger:** regular cadence — my eighth session since the last count-based report.
**Phase:** 2 (Execution). One recording has been measured, on one of five checks. No recording is chosen, no synthetic data exists, no spike sorter has run, and the project's actual question is untouched.

---

## The short version

Since the last report I have done one thing that produced a number and one thing that produced a specification.

**The number.** The leading candidate recording — a 72-minute Neuropixels recording from the International Brain Laboratory's Brain Wide Map — was measured for **drift**, which is the slow physical movement of the probe relative to the brain over the course of a recording. It moved **1.8 micrometres** over its worst ten minutes, against a tolerance of 20. That measurement is done, it was independently replayed by my collaborator, and it is approved. One of five gates, on one of thirteen candidates.

**The specification.** The next gate is **noise** — is the recording's background electrical noise quiet enough, and even enough across the probe, for injected synthetic spikes to be gradeable? I wrote the specification for that gate before writing any code for it, deliberately, and it has now been through **seven rounds of review across two review cards and has never been approved.** This report is mostly about that, because eight sessions is a long time and you are entitled to know whether it is going well or badly.

**My honest answer: it is going well, and it is going slowly for a reason I would defend — but I set myself a tripwire eight sessions ago and I have to report that it is closer than I would like.**

---

## What the noise gate is, in plain terms

Later in this project we take a real recording and inject synthetic spikes into it at times we choose, so that we know the right answer and can grade a spike sorter against it. For that to mean anything, the synthetic spikes have to be neither trivially obvious nor invisible. Whether they land in that band depends on how loud the recording's background noise is.

So before we pick a recording, we measure its noise. Two things matter:

- **Level** — how loud the background is. Too loud and the injected spikes are buried; too quiet and they stand out so far that any sorter finds them and the test measures nothing.
- **Evenness** — whether the noise is roughly the same on every electrode contact along the probe. It matters because our two experimental arms place their synthetic neurons at *different depths* by design. If noise varies steeply with depth, a difference we measure between the two arms could be caused by where the neurons sat rather than by the thing we are testing. That would corrupt the project's central result, so we bound it at the recording rather than trying to correct for it later.

Both are measured on sixty short windows spread across the recording rather than on the whole thing, because downloading the whole thing is expensive and unnecessary. That choice has a cost, and we state it as a guarantee rather than hiding it: **any noisy stretch longer than about 74 seconds is certain to be caught; anything shorter can fall between two windows and be missed.**

---

## What has happened in these eight sessions

Seven review rounds. Every one returned defects; **every defect was accepted and none was disputed.** Here is the shape of them, because the pattern is more informative than the list.

**Three were about a claim being true in one direction but not in general.** We said an unmasked bad electrode always pushes the recording *toward* rejection, so ignoring bad electrodes is safe. It does not: my collaborator built a 72-contact example where replacing **one** contact with an extreme value turned a failing recording into a passing one, because the statistic reads ranked positions rather than values. We said interleaving samples would move an uncertainty measure in the safe direction. It does not; an example moves it the other way, past the tolerance. **In every one of these the right answer was to withdraw the claim rather than narrow it**, and to publish the raw numbers the claim used to stand in for.

**Two were about a rule that could not do the job it was written for.** The check that stops a recording being *too quiet* was being compared against the **loudest** of the sixty windows — which cannot catch a recording that is quiet almost everywhere. It reads the quietest window now. No threshold changed; what changed is which number the threshold is compared to.

**Two were about our own verification machinery rather than about the science.** We built a checker that runs an older, closed checker and requires it to report a specific list of failures. My collaborator demonstrated that a *counterfeit* older checker, printing that list and reporting success, would pass. We fixed it by verifying the older checker cryptographically before running it — and then, this session, he showed the fix listed five of the six files that checker reads, and swapped the sixth for a forgery that we did not notice. **That one is my defect twice over.**

**And this session's headline is the one I find most instructive.** Last session I withdrew a claim and replaced it with three reasons. This session the review showed **two of the three reasons are false** — including the one I had labelled decisive, which said that a certain measure being good "buys the decision nothing." It buys it a great deal: on our own worked example, a recording that passes under one setting is ruled *unmeasurable* under the other. **I had slid from "this value is not a certificate" to "this value does nothing," and those are different sentences.**

---

## What was unexpected, and worth your time

**Withdrawing a reason is not the same as fixing a claim, and can leave a worse hole.** Twice now I have correctly removed a false claim and then filled the gap with a *new* argument invented in the same session — with nothing checking it. Both times the new argument was itself defective. The discipline I am taking from this is that an argument built in the same draft that first needs it has had nothing testing it, and should be labelled that way rather than presented as settled.

**A counterexample is worth more when you generalise it.** My collaborator found one frequency whose two window-halves are identical, which defeated our "the halves are nearly independent" reasoning. Rather than accept the single instance, I worked out the whole family it belongs to — **there are infinitely many, starting at 304 Hz** — and built 135 of them. That turns "here is an awkward case" into "this reasoning cannot be rescued," which is a cleaner outcome for both of us than a narrowed claim.

**The most valuable thing our review method produces is not the defects; it is the record of what we refused to do.** Twice this stretch the obvious fix was to add a rule — a bad-electrode rule, a rate-adopting rule — and both times we declined, on the same ground: **a rule invented after you have seen how something fails is a rule chosen with the answer visible.** That is the specific failure the whole pre-declaration structure exists to prevent. The refusals are written into the document, not into a private note.

---

## What is working

- **The review method is catching real things at a real rate**, and the things it catches are getting more subtle rather than more numerous. This round's two defects are both about the *relationship between* correct statements, not about incorrect ones.
- **The evidence discipline holds.** Every number the specification publishes is computed by a script that is handed over with a cryptographic fingerprint, and my collaborator recomputes them independently. Twice now our two figures for the same quantity have *disagreed*, and both times that disagreement was the useful finding — it showed the number was a property of the example rather than a general bound, and we relabelled it accordingly.
- **Nothing has been quietly loosened.** Across seven rounds, no threshold value has moved. That matters more than it sounds: the moment a threshold moves after a candidate's number is known, the gate stops being a gate.

## What is not working

**I said this last time and I have to say it more sharply now.** In the Session 40 report I wrote that the specific signal that instrument-polishing had gone too far would be "another round of objections that are about our own machinery rather than about the recordings," and that the honest response would be to ask whether the thing should be simpler rather than repair it a third time.

**Two of this stretch's defects were exactly that**, on the checker that verifies our own checker. I do not think we have crossed the line — both were genuine holes in a genuine safeguard, and the second repair replaced a hand-maintained list with something derived automatically, so that class of defect should not recur. But I am recording the tripwire rather than quietly moving it.

The structural fact underneath it: **this specification has consumed eight of my sessions and produced no measurement.** The counterweight is that the specification governs a measurement that costs about **950 MB of downloading per candidate recording** and may have to run thirteen times, so getting it wrong is not cheap either. Still, I would rather state the ratio than let it pass unremarked.

**The method has now run out of room on this specification.** Our review rules allow a bounded number of rounds; **this session's response is the last revision permitted.** What comes back next is a verdict, not another repair. If it is not an approval, the rules require us to split the work or redesign it with the changed boundary named — not to open another round. I think that is the right constraint and I am glad it exists.

**Open items needing you:** two entries in `director_requests.md`. Both are non-blocking and neither has changed since the last report — the standing invitation to review the project contract, and the compute-contention question you already answered, which is recorded as Amendment 1 and is working.

---

## What is next

1. **My collaborator's verdict on the specification.** Approval or a bounded terminal decision; not another revision.
2. **Then the estimator gets written** — the actual code that measures a recording's noise — against whatever the specification says once it closes. It is deliberately not written yet, so that no line of it can quietly become the specification.
3. **The second candidate recording's drift measurement**, which is unblocked and cheap and has simply been waiting behind this.

No verification-artifact update this time. Nothing about your verification path changed this stretch, and I would rather say so than manufacture one.
