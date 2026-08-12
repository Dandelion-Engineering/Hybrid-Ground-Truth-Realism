# Progress Report — Claude, Session 8

**Written:** 2026-08-12 12:32 PDT
**Triggers:** the every-eighth-session cadence, and an approved Claim Sheet amendment written in this session.
**Where the project is:** Phase 2 — Execution. Still no sorter run, still no host recording chosen, still no result about the project's actual question.

---

## The short version

This session found that two numbers the project had been comparing to each other were measuring different things. Both were in microvolts. Both were called amplitudes. One is the full trough-to-peak swing of an *averaged* waveform; the other is the typical single-sided peak of *individual* spikes. Nothing had gone wrong yet, because nothing has been built on the comparison — but a conclusion had been drawn from it, and published in the public log, and that conclusion was reached by an operation that wasn't defined.

I measured the conversion between them on 1,821 real neurons, restated the affected number correctly, and wrote the correction into the ledger rather than quietly fixing it.

---

## The thing you'd need to know to follow this

Here is the experiment in one paragraph, because everything below is about a detail inside it.

To grade a spike sorter you need to know the right answer, and real brain recordings don't come with one. So the field takes a real recording and *injects* synthetic spikes into it at times it chooses — now there's an answer key, at least for the injected ones. The synthetic spikes are built from a library of real waveform shapes borrowed from other recordings, called **templates**. Before injection, each template is scaled so it's a realistic loudness for the recording it's going into. Our contract fixes that target loudness at **50 to 200 microvolts**.

A microvolt is a millionth of a volt, and a neuron firing a few tens of micrometres from a recording contact shows up as a blip of roughly that size. ([A short primer on extracellular recording](https://en.wikipedia.org/wiki/Extracellular_recording) if you want the physical picture.)

So: "make the injected spike 50–200 µV loud." Simple enough — until you ask *loud measured how?*

## What the check found

There are at least two reasonable ways to put a number on how loud a spike is.

- **Trough-to-peak of the average.** Take every spike a neuron fired, average them into one clean waveform, and measure the full swing from its lowest point to its highest. One number, from an averaged shape.
- **Typical peak of the individual spikes.** Measure each spike's own peak, one at a time, and take the middle value of all of them.

Both are honest. Both are reported in microvolts. They are not the same number, and neither source labels which one it is using in a way you'd notice.

The waveform library uses the first. The recordings we're injecting into report the second. **In Session 7, I compared one against the other and concluded that the 50–200 µV target looked appropriate for the neurons in our candidate recordings.** That comparison was not a defined operation. My collaborator Codex caught the risk in review and made the rule explicit: until the two are shown to be comparable, *neither* "the target is fine" nor "the target is too loud" is something we get to say.

### How it got settled

Rather than argue about which convention is right, I measured the relationship. The recordings happen to store, for every neuron, the averaged waveform itself. That means the library's definition can be computed directly on the recordings' own neurons — same neurons, both definitions, no guesswork about which neuron is which.

Across 1,821 neurons in one recording, the first measurement is about **1.2 times** the second. On the highest-quality subset the median is 1.207.

But — and this is the part that matters more than the number — the spread is wide. For the middle 80% of neurons the factor runs from about 1.10 to 1.51, and further out it goes past 2. **So the conversion is good enough to restate a population-level target and not good enough to convert any individual neuron.** The target, restated in the recordings' units, is roughly **41 to 165 µV**. I wrote that boundary into the working document explicitly, because the specific failure I could see coming is a future session picking up "1.2" and applying it to one neuron.

### Did the original conclusion survive?

Yes, and the honest thing is to say that it survived *by luck of the numbers, not by the reasoning*. The corrected 41–165 µV band still brackets the real neurons' typical loudness in our candidate zones (51–110 µV). So the practical conclusion is unchanged. The route to it was invalid, and that is logged as a correction with the date, the wrong claim, and the replacement — the same way every other correction in this project is logged.

I want to be plain about why that matters even though the answer didn't move. If we only recorded corrections when the conclusion flips, the ledger would quietly become a record of *lucky* reasoning rather than *sound* reasoning, and the next time an undefined comparison shows up there'd be no habit in place to catch it.

## Two things nobody knew, found on the way

**The borrowed waveforms are all from neurons that passed quality checks.** Reading the library's own build script — rather than its documentation — shows it takes only clusters the field's own quality metrics accepted. That had never been recorded anywhere in this project. It doesn't break anything; it bounds what our eventual result describes. "Region-matched templates" turns out to mean "region-matched templates *from well-isolated neurons*," which is a narrower and more honest claim.

**The target range sits low against the actual library.** Of the 2,183 usable templates, the median loudness is 184 µV and **42% are above 200 µV** — above the top of the target. So rescaling isn't a gentle nudge; for a substantial fraction it's a real reduction. More specifically, for the sixteen hippocampal templates this experiment's first test depends on, four are above 200 µV, the largest at 487. This isn't a problem to fix — the range is a destination, not a filter, and nothing is excluded — but it means the two arms of the comparison get systematically *different amounts* of rescaling, and I've flagged that to Codex as something its balance check may want to watch explicitly rather than inherit.

## What isn't working, and what I got wrong

**My first design for this check was wrong and I threw it away.** I built it around matching the library's templates to the recordings' neurons one-to-one. It failed completely — the library doesn't record a neuron identifier, only a position in a list, and the assumption that the list order matches turned out to be no better than random. The rewrite works on a different principle entirely and is better for it: it needs no matching at all. I've written the failed approach into the document so a later session doesn't spend the same hour rediscovering it.

**A safety check fired and I nearly loosened it.** I'd written the script to abort if its idea of a neuron's strongest recording contact disagreed with the file's own. It aborted on the very first neuron. The tempting move is to relax the check so the script runs. Instead I measured the disagreement: the two rules pick the same contact only 72.6% of the time, usually a near tie between neighbours. It's not a bug — it's a *third* convention difference, and it has a small consequence for how we position injected neurons that I've handed to Codex as an input to work it already owns.

**Nothing is blocked on you.** `director_requests.md` has nothing open that needs an answer.

## Where the contract stands

Four amendments now exist. **Three are in force** — including the one this session closed, which records what the recordings actually prove about where the borrowed waveforms and the host recordings came from (different laboratories and institutions; a claim I'd made about shared rig *design* was not supported and was removed).

**One remains proposed**, and it's mine to defend. Codex had written the negative control's random seed in advance, but left the *recipe* for using it to be settled later, once we can see the data. I pushed back, because that freedom runs in only one direction: a recipe tuned after seeing the data can only make our safety margin look tighter, and a tighter safety margin makes our eventual headline result look more convincing than it is. The recipe is now written out in full, in advance, and changing it later takes a fresh amendment. Codex has that back for review.

## What's next

1. Codex's review of that amendment.
2. The brain-region label map is still materially incomplete — 296 unmapped names on the host side. It doesn't matter for the hippocampal search we're doing, but it does block the comparison arm that ignores region. It needs an external anatomical reference, and the licence terms have to be read before anything is downloaded. It is now the largest open item nobody is working on, and it's mine.
3. The other half of the amplitude question — whether the *processing* the two sides went through matters, on top of the definitions — can't be answered from metadata. It needs the software stack installed, which is Codex's feasibility pilot.

**Still no sorter run, no host chosen, and no scientific result.** Eight sessions in, that is the correct state: everything so far has been making sure the measurement, when it happens, means what we'll say it means.
