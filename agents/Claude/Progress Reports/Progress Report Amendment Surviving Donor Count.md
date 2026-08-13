# Progress Report — the contract said "carry on," the machinery said "stop"

**Written:** 2026-08-13, Claude Session 15
**Trigger:** Claim Sheet Amendment 6 reached `In force` this session — an approved amendment is a reporting event.
**Phase:** 2 (Execution). No sorter has run. No host recording has been chosen. No scientific result exists yet.

---

## The short version

Back in Amendment 2 we wrote down what happens if the practical checks kill some of our sixteen donor spike shapes: **more than six dead and we drop this part of the study and publish that we dropped it.** Which is also a promise about the other side of that line — one to six dead, and we keep going.

We had never written down *how* to keep going. Every piece of machinery underneath — the pairing rule, the schedule that decides which shape gets injected when, the fake "nothing changed" comparison we use as a sanity check — was written as though the number were always sixteen. So the contract said carry on and the machinery said stop, and nothing reconciled them.

Amendment 6 reconciles them. It gives the surviving count a name, `N`, rewrites the design in terms of it, and leaves the failure line exactly where it already was.

Two things came out of doing that which I did not expect. **The failure line turns out not to have been arbitrary** — it lands exactly where it has to, for a reason nobody wrote down at the time. And checking Codex's repair of my draft turned up **three more sentences that had quietly gone stale**, in amendments nobody was looking at.

---

## A little background, so the rest reads cleanly

**What we are testing.** Spike sorting is the problem of working out which of the electrical blips in a brain recording came from which neuron. A real recording has no answer key, so the field grades sorting software using **hybrid recordings**: take a real recording, inject synthetic spikes at times you chose, and see whether the software finds them. The maintainers of the standard tool for this said in print that they do not know whether their synthetic spikes are realistic enough for the resulting scores to mean what everyone treats them as meaning. We are testing that.

**Where the injected shapes come from.** They are real waveforms harvested from other recordings, published as [`hybrid_template_library`](https://github.com/SpikeInterface/hybrid_template_library). The recording they get injected into — the "host" — comes from [DANDI 000409](https://dandiarchive.org/dandiset/000409), the International Brain Laboratory's Brain Wide Map.

**The number sixteen.** We inject into CA1, a layer of the hippocampus. The library holds exactly **sixteen** CA1 spike shapes in total. Not sixteen after filtering — sixteen in existence, for this probe type. That was Amendment 2's finding and it is why this report is about a number rather than about a method.

**Why shapes can die.** A donated shape has to survive being dropped into a specific real recording: still loud enough after rescaling, still distinguishable from that recording's background noise, landing at a plausible depth, and with somewhere to physically put it. None of those can be checked until a host recording is chosen, which has not happened yet. So the survivor count is genuinely unknown today, and that is the whole point.

---

## What Amendment 6 settles

**One: the surviving count gets a name and the design is written in terms of it.** `N` is how many of the sixteen survive the checks in the chosen host. Ten through sixteen: carry on. Fewer than ten: this part of the study fails and we publish that, along with a list of exactly which shapes died and which check killed each one.

**Two: the injection schedule is derived rather than assumed.** The study injects ten shapes per run and repeats five times — fifty slots. With sixteen shapes that is fourteen appearing three times and two appearing four times. With ten shapes it is five appearances each. Amendment 6 replaces the hard-coded "three or four times" with the arithmetic that produces it, so it works at every count in between.

**Three, and this is the part with teeth: the schedule is fixed now, not later.** Which shapes get the extra turn, and which round each turn falls in, are settled today by a rule nobody can steer — a fixed scrambling of each shape's identity, dealt out like cards. It has to be settled today, because after the host is chosen we would know *which* shapes survived, and any choice made then is a choice made while looking at the answer. This is the same discipline the last two amendments turned on and it is the single most important habit in the project: **fix the rule while the outcome is still unknown, or the eventual result is a choice dressed as a measurement.**

---

## The unexpected part: the failure line was not arbitrary

Amendment 2 set the line at "more than six of the sixteen." It never said why six.

Sixteen minus six is ten. Ten is exactly how many shapes get injected into each run. So **"at least ten survivors" and "we can still fill a round with ten *different* shapes" are the same condition** — not roughly, but exactly, all the way across the range.

That mattered practically, not just aesthetically. I was about to add a rule saying no shape may be injected twice into the same run. Adding rules to a contract is expensive: each one is a new thing to justify, and a new thing that can conflict with something else. Checking first showed the rule was already implied by the boundary we had. It did not need adding — it needed noticing. And the card-dealing schedule delivers it automatically, so it never had to be argued at all.

I am not claiming that was the original intent. Amendment 2 does not say. But the coincidence is exact, and it converted something I was about to impose on my own authority into a reading of the agreement already in place.

---

## What checking Codex's repairs turned up

This is a two-agent contract: I wrote Amendment 6, Codex reviewed and edited it, and then I had to genuinely re-review Codex's edits rather than wave them through. Both of its repairs were right, and checking them properly was worth more than agreeing with them would have been.

**The first repair closed a loop I had opened.** My version said the checks must be pinned down before any shape is tested against them — cut-offs written in advance so nobody can nudge a threshold until the answer looks better. Codex found that this was not enough, and it is worth being precise about why, because it is not obvious. Several of those checks depend on **where on the probe** a shape is placed. So pinning the cut-off without also pinning the positions is not pinning the check at all: the same shape passes or fails depending on which position you happen to test. Worse, it created a circle — a shape could pass the screen, fail later at a position the schedule assigned it, get removed, change `N`, and change the schedule that assigned it that position in the first place. Codex's edit pins the candidate positions and the exact rule for turning position-level results into one yes-or-no per shape, before anything is tested. The loop closes.

I want to record that my text *looked* rigorous. It said the right-sounding thing about pinning thresholds in advance. It was the unstated half — where they get measured — that carried the defect.

**The second repair was a list I had left one item short**, and checking it found three more. Amendment 6 retires the old fixed "sixteen" wherever it means the size of an arm. I had listed the places. Codex found one I had missed — and, notably, I had *written about* that exact sentence in my handoff note to Codex and then not put it in the document. **A finding described in a message is not a change to the artifact.** That is a new lesson and a slightly embarrassing one.

Codex's fix was to widen the retirement from a list of specific clauses to a general rule. Widening is riskier than it sounds — a blanket "read every sixteen as `N`" would break sentences that are still perfectly true, like "the library holds sixteen CA1 shapes," which stays true no matter how many survive. So I went through every single occurrence of "sixteen" and "16" across four amendments and classified each one. The widening is safe, because Codex paired it with an exemption for measurements actually taken at sixteen. And it earns more than it was written for: **three further sentences had quietly gone stale** under my narrower list — one in Amendment 2, one in Amendment 3, and one in Amendment 4, which is an amendment about an entirely different subject.

That is now the third time in a row that a change to a design property has been found lurking in an amendment whose title has nothing to do with it. It has stopped being a coincidence and is now a standing check.

**Two things I found, checked, and deliberately did not change.** The failure line "more than six of the sixteen" must *not* become "more than six of the `N`," which would be circular nonsense — I confirmed the new rule does not reach it. And the list of shapes removed from the comparison group stays at all sixteen even when fewer survive, which is deliberate: it is not established that "unfit to inject" and "unfit to compare against" are the same test, so shrinking that list could let a shape we have already judged unfit sneak back in through the other side. Both survive on inspection. I recorded the checks rather than editing, because a contract that gets reopened every time someone could *imagine* misreading it stops being stable.

---

## What is working

- **The review discipline is catching real defects, in both directions.** Six amendments in, every single one has been changed by its reviewer before entering force. Not one has gone through unchanged. That is the process working, not the process being slow.
- **Nothing has been decided while looking at the answer.** No host recording is chosen. No pool of candidate shapes has been opened. The pairing rule, the schedule, the seeds and the failure boundaries are all fixed while the outcomes are still unknown.
- **The reproducibility packet is genuinely self-contained.** Someone could copy that folder to a clean machine and follow it without contacting us.

## What is not working, or not done

- **No host recording is pinned, and the next check is awkward on purpose.** The remaining gate I own is **drift** — whether the probe moves relative to the brain over the course of a recording, which matters because a shape injected at a fixed position stops matching a brain that has shifted underneath it. The dataset has a column that claims to measure this, and its values are physically impossible — millions of micrometres per hour, which would be metres. So the quantity has to be *defined* from the raw data before it can be measured, and I have to define it without letting the definition be steered by which recording I would like to win. That is the next real piece of work.
- **Codex's edit made my own job harder, correctly.** The requirement that all ten shapes in a round fit together at fixed positions is now a stricter test than the capacity check I ran back in Session 8. Some candidate recordings that looked fine may not be.
- **The heavy machinery is still not installed.** The sorting software and its dependencies are Codex's lane and have not been set up yet. Nothing has been run on the GPU. That is deliberate sequencing, not a stall — but it does mean the first real compute test is still ahead of us.
- **The one thing pending on you.** `director_requests.md` still carries the Phase 1 entry asking for your review of the contract, from 2026-08-11. It is explicitly non-blocking and we have kept working. One honest update: the contract has moved a fair distance since that request was filed — it now carries six amendments — so if you do read it, the six amendments at the bottom of `Accessible Claim Sheet.md` are where the real decisions of the last two days live. The fifteen slots above them are unchanged.

## Verification artifact

Nothing new. The hands-on artifact that will let you check the result yourself cannot be built until there are results to check, and there are none. The packet's README says so plainly rather than leaving a gap.

## What is next

Drift. Defining the measurement before taking it, and taking it without letting the definition drift toward a convenient answer — which is the same discipline this whole report has been about, applied to a number instead of a contract.
