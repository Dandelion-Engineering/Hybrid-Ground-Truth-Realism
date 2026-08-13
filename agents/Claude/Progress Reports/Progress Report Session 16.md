# Progress Report — the word "dataset" was doing a job it could not do

**Claude, Session 16 · 2026-08-13 04:18 PDT**
**Trigger:** regular cadence — my eighth session since the last count-based report.
**Phase:** 2 (Execution). Still no host recording chosen, no data generated, no sorter run.

---

## The short version

The experiment compares two groups of injected fake neurons: one drawn from the same brain region as the place we inject them, one drawn without looking at region at all. For that comparison to mean anything, the two groups have to be alike in every way *except* region. One of the ways we promised to keep them alike is the number of different **source recordings** each group is drawn from.

This session I finally read what the "source recording" label in our donor library actually is, instead of counting it. It is the identifier of **one probe insertion** — the narrowest possible unit. The 37 labels we have been treating as 37 independent sources come from **24 recording sessions and only 12 animals**.

That matters, because it means the balance rule we wrote can be satisfied perfectly and still leave the two groups badly mismatched. Our region-matched group comes from four sources, which happen to be four different animals. A control group could also come from four sources — passing the check exactly — while all four came from **one animal**. Of the 66,045 possible four-source control groups, **28,621 of them (43%) have fewer than four animals in them, and 74 have exactly one.**

The fix is in place and it costs nothing, which is the nice part. I also found a second, unrelated hole: we had carefully pinned down the *rules* of the experiment in advance but not the *dice*.

## The background you need for the rest of this

Spike sorting is the step that takes the electrical noise recorded by a probe in a living brain and decides which blip came from which neuron. There is no answer key for a real recording, so the field grades sorting software using **hybrid recordings**: take a real recording, inject some artificial neurons into it at times you chose yourself, and see how many of your own injections the software finds. The whole project exists to ask whether making those injections more realistic changes the grades — a question the people who built the standard pipeline wrote down as unanswered.

Our injected neurons are copied from a public library of about 2,183 real recorded neuron shapes, published under an open licence by the [SpikeInterface team](https://github.com/SpikeInterface/hybrid_template_library), all extracted from the [IBL Brain-Wide Map](https://dandiarchive.org/dandiset/000409) recordings.

The first realism axis we test is **region matching**: does it matter whether the injected neurons come from the same brain area we are injecting into? So we build two arms — one matched, one drawn blind to region — and compare them.

**The danger with any two-arm comparison is that something else differs between the arms and gets credited to the thing you were testing.** Where the neurons were *originally recorded* is one of those something-elses. If the matched arm comes from four different animals and the control arm comes from one, then some of what we measure is the difference between four animals and one animal, wearing a "region" label. That is the specific failure the balance rule exists to prevent — and it is quoted in the contract in almost those words.

## What I found

Every donor neuron in the library carries a `dataset` label. Since the very first week of this project we have used the number of distinct `dataset` values as the measure of "how many independent sources is this arm drawn from," and the rule Codex and I have been drafting makes matching that number a hard requirement.

I opened the parser that reads that column. **The `dataset` string *is* one probe insertion** — one probe, one time, in one animal. The session identifier and the animal identifier are both pulled out of that same string.

Two things follow, and I checked both by making the computer assert them across all 2,183 rows rather than by reading the code and believing it:

1. **The three levels nest perfectly.** Choose which `dataset` values a group uses, and you have automatically also decided how many sessions and how many animals it spans. There is no freedom left.
2. **Matching the narrowest count does not match the wider ones.** Here is the census, by group size — how many groups of that size span that many distinct animals:

| Group size | Possible groups | Groups spanning that many animals | Share |
|---|---|---|---|
| 1 | 37 | 37 | 100% |
| 2 | 666 | 608 | 91% |
| 3 | 7,770 | 5,884 | 76% |
| **4** | **66,045** | **37,424** | **57%** |

Our region-matched arm is a four-source group. So at the size that actually applies, **43% of the control groups that would pass our check are drawn from fewer animals than the arm they are being compared against** — and 74 of them come from a single animal.

## The fix, and why it was free

The rule now checks the count at all three levels — insertions, sessions, animals — and only falls back to the original single-level check if no valid pairing exists at the stronger one. Three things make this comfortable rather than risky:

- **Nothing can become impossible.** The original rule is still available as a fallback at every step, so no configuration that would have worked before can now fail.
- **The search got smaller, not bigger.** Because the wider counts are *determined* by the narrow one, the stronger check simply throws out 28,621 of the 66,045 candidate groups before any work is done on them. Stronger and cheaper at the same time.
- **It only bites in two places.** At the tightest pairing level the stronger check is automatic; at the loosest it does all its work.

## The second hole: we pinned the rules but not the dice

This is a different kind of problem and worth explaining, because it is the failure mode this whole slow, contract-first way of working is built to prevent.

The reason Codex and I write these rules *before* looking at any data is a well-known trap: when you can see the results, every choice you make afterwards — which method, which threshold, which tie-breaker — can be defended individually while the collection of them quietly steers you to the answer you liked. The defence is to fix every choice in writing beforehand, so there is nothing left to steer with.

We have been thorough about that. The order the injected neurons are scheduled in is fixed by a published formula. The random seed for it is fixed, and the contract even records the exact sentence the seed was computed from.

**But the physical placements — where on the probe each injected neuron actually goes — are only described as "randomized."** Nowhere does it say where that randomness comes from. And every single quantity the matching rule compares the two arms on — how big the injected spike is, how far above the noise it sits, how deep it is — is measured *at that placement*.

So the rule was pinned on top of an input that was not. Nothing stopped someone from drawing the placements, disliking the balance report, and drawing again. The fix is small: the placements now have to come from a recorded formula and a recorded seed, derived the same way the two seeds we already pin were derived, one stream per injection. The randomness the experiment needs is unaffected; what is removed is the ability to roll twice and keep one roll.

Codex owns that part of the project, so I have flagged it as its call whether the requirement lives where I put it or somewhere it owns. What I did not do is leave the finding in a message — a note about a change is not the change.

## What is working

- **The review loop keeps catching real things.** Codex's last pass caught a genuine circularity in something I wrote; this pass caught two things in something Codex wrote. Neither of us is finding these in our own work.
- **Every number in this report was measured offline** against a snapshot we pinned in week one, in under a second, with no network access and no data download. The project has not yet spent a meaningful amount of compute, and it has not needed to.
- **The contract has held under six amendments.** Nothing has had to be quietly rewritten; every change is dated and appended.

## What is not working, or is simply not done yet

- **We still have no host recording chosen**, and therefore no result of any kind. That is correct for where we are, but it is the honest headline: the project is still building the ruler.
- **The drift gate in my own lane is still open.** Last session I found that the drift measurement the public data ships with is unusable for our purpose — it accumulates measurement jitter rather than measuring real movement, and it rises with how often a neuron fires. I now need to define a replacement, and I have to define it before measuring any candidate recording, or I will be choosing the threshold to fit the answer.
- **The stricter placement requirement I described above may push back on me.** It makes the host-selection job in my lane harder, not easier. That is the right direction for the science and the wrong direction for my convenience, and it is worth saying which of those I noticed first.
- **Nothing is blocked on you.** `director_requests.md` has one open non-blocking item — your review of the Claim Sheet, whenever you get to it.

## Verification artifact

No change this session. The hands-on artifact that will let you check the result yourself cannot be built before there are results to check; the packet that will hold it is in place and its runbook is approved.

## What is next

Codex re-reviews the rule I handed back. In my own lane, the drift definition is the next real piece — the quantity first, the threshold's justification second, and only then any measurement of a candidate recording. That order is the whole point.
