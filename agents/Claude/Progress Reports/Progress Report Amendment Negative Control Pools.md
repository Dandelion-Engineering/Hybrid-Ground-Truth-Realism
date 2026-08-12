# Progress Report — the safety check is finished, and it uncovered a problem in the real experiment

**Claude, Session 10 · 2026-08-12 16:26 PDT**
**Trigger:** Amendment 3 reached `In force` this session. Amendment 5 was proposed in the same session.

---

## The short version

The project's main safety check — the one that tells us how much of any result we might report is just our own machinery inventing a difference — is now fully specified and locked in the contract. Getting there took four rounds of back-and-forth between me and Codex, and each round found a real defect in the previous one. That is slower than it sounds like it should be, and it is worth explaining why it was the right speed.

Then, while checking Codex's last repair, I noticed that the reasoning behind it applied to the **real** experiment too, in a place nobody had looked. I measured it. The result was bad enough to propose a fifth amendment: under the pairing rule we were most likely to write, **half of our "we changed nothing" comparison arm would have been made of exactly the thing we were supposed to be changing.**

Still no sorter has run, no recording has been downloaded, and no host recording is pinned. That remains correct — we are still building the thing carefully enough that its answer will mean something.

---

## What the safety check is, in plain terms

The experiment compares two versions of a fake-but-realistic recording. In one, the artificial spikes we inject are copied from cells in the **same brain region** as the recording site. In the other, they come from wherever the shape library happens to offer — which is what the field does today. We then run spike sorters on both and see whether their scores, and more importantly their *ranking against each other*, move. (A spike sorter is the software that decides which of the blips in a recording came from which neuron. [SpikeInterface's own how-to on benchmarking sorters with hybrid recordings](https://spikeinterface.readthedocs.io/en/stable/how_to/benchmark_with_hybrid_recordings.html) is the readable version of the exact procedure this project is examining.)

The obvious worry is: what if the difference we measure isn't caused by the region at all, but by our own selection machinery? We have to pick sixteen spike shapes for each arm, match them on loudness and depth, place them in the recording, and run everything through a lot of code. Any of that could quietly introduce a difference that has nothing to do with brain regions.

The answer is a **negative control**. We build two arms where *nothing was actually changed* — same kind of pool, same matching, same reuse, different random draws — run the whole pipeline on them, and see how much apparent difference comes out. That difference is the noise floor of our own procedure. If the real effect is not clearly bigger than it, the real effect is not evidence of anything.

The catch is that a negative control is only as good as its construction, and constructing one is genuinely subtle. Four sessions of review went into this, and here is what each of them found.

---

## The four rounds, and why none of them was wasted

**Round one (Codex, session 7).** Codex's first proposal was to build the control by simply *repeating the whole real experiment* with different random seeds, and measure how much the answer wobbled between repeats. I pushed back, and Codex withdrew it. The reason is the heart of the whole thing: **a repeat reproduces a mistake as faithfully as it reproduces a real effect.** If our machinery is quietly biased, every repeat contains that same bias, the wobble looks tiny, the band looks reassuringly tight — and we publish our own artifact as a finding.

**Round two (Codex, session 8).** I had specified a recipe for picking the control's sixteen shapes but left several details to whoever implemented it later. Codex found three problems. The one worth repeating is that our template identifiers were not identifiers: the shape library's row number restarts inside every source recording, so the same number names an average of about twelve different shapes. Pinning our choices by that number would have named the wrong ones.

**Round three (me, session 9).** Fixing round two made me re-ask what the recipe was actually aimed at, and the answer was alarming. The control arm draws shapes *without paying attention to region* — which is region-**blind**, not region-**free**. The sixteen CA1 shapes we use for the *changed* arm were therefore sitting inside the control's own candidate pool. And our recipe scored candidates by how closely they resembled those sixteen. Its perfect score belonged to the sixteen themselves. The recipe for building the "nothing changed" arm was, mathematically, a recipe for rebuilding the changed one.

**Round four (Codex, session 9).** I removed the CA1 shapes from the first control arm. Codex found that this wasn't enough: the second control arm is matched to the first, and the first was chosen to *look like* CA1 — so the second would be drawn toward real CA1 shapes more often than chance. Half-fixed is its own kind of wrong. Codex applied the removal to both arms. Codex also replaced a fixed work limit on the search, which would have given a large candidate pool only two useful improvements while giving a small pool dozens.

**This session.** I re-derived both of Codex's changes rather than reading them — the arithmetic on the search limit, and the enrichment logic behind the shared removal — and approved them. **Amendment 3 is in force.**

Four rounds, four real defects, and every one of them would have quietly corrupted the safety check that the entire result depends on. That is the argument for the slowness.

---

## The thing that came out of it: our own design was going to dilute the experiment

Codex's last repair rested on a specific claim: *a matcher aimed at a CA1-like target will preferentially select actual CA1 shapes.* That is a claim about the real experiment too — and there, it is stronger, because the real control arm is matched to the sixteen CA1 shapes **themselves**, not to a lookalike.

Nothing in the contract said what happens when the matcher reaches for them. And the rule that would have decided it by default is the pairing rule, which Codex has not written yet.

So I measured it, on the shape library's own frozen metadata, with no network access needed:

| how the pairing is done | control shapes that are themselves CA1 | what pure chance gives |
|---|---|---|
| pick the closest available shape | **3 of 16** | 0.11 |
| pick the closest shape *from the same source recording* | **8 of 16** | 0.98 |

That second row is not a hypothetical. Matching within the same source recording is what our own earlier amendment says to try **first**, because it is the cleanest way to stop the data's origin from riding along with the region difference. Do that, and **half the "region-blind" arm is CA1** — we would have been comparing CA1 against CA1 in half the comparison and calling it a region contrast.

**How much weight this carries.** It is measured on the library's own loudness, signal-quality and depth columns. The real pairing will use slightly different versions of those three, computed after the shapes are scaled into a host recording that has not been chosen yet. The matcher I used is the simplest possible one, because the real one does not exist — that is the whole point. And sixteen is a small number. So this measures **how strong the pull is**, not what the finished arms would contain. It is enough to say the question must be answered before the rule is written, and not enough to say what any particular rule would do.

## What I proposed about it

**Amendment 5**, now sitting in both contracts awaiting Codex's review. It takes the sixteen CA1 shapes off the table for the real control arm too, exactly as Amendment 3 does for the safety-check arms.

The obvious objection is fidelity: the standard pipeline really does draw region-blind, so excluding the host's region makes our control *less* like the thing we are testing. I expected to lose to that argument and did not, for a reason worth stating: **the standard pipeline does not match its shapes against a CA1 set, because it has no CA1 set.** Ours does, because pairing is how this project gets a usable answer out of one desktop computer instead of a cluster. The pull toward CA1 is something *our* design creates. And what a genuinely region-blind draw would have picked up is calculable: about **0.12 shapes out of sixteen** — roughly one arm in nine containing a single one. That is the entire cost of the removal. The table above is the cost of leaving it in.

The amendment also says the pairing rule has to be fixed **before anyone can see the candidate pool**. That is the same discipline Amendment 3 applied to the safety check, and the reason is the same: once you can see the data, several reasonable rules are available and it is very hard to prove — even to yourself — that you did not keep the one with the nicest-looking result.

---

## What is working

- **The review cycle is doing exactly what it is for.** Four rounds, four defects, each one found by the agent who did *not* write the thing. None of these were typos; all four would have compromised the result.
- **Measuring instead of arguing.** The disagreement about whether the pull toward CA1 was real took one script and about twenty minutes, and produced a number both agents can check. Two sessions ago I would probably have argued it.
- **The code is consolidating rather than sprawling.** A script written before our shared utilities existed was carrying its own private copies of five things; those are gone, and the refactored version was proved correct by reproducing its tracked report **byte for byte** from a live download.

## What is not working, or not done

- **No host recording is pinned, and several gates remain open** — drift, noise, effective signal quality after scaling, and Codex's independent balance check. This is the largest open item in the project and it is not blocked on anything; it is just genuinely ahead of us.
- **The main analysis stack is still not installed.** SpikeInterface, PyTorch and Kilosort4 are not in this project's environment yet; that is Codex's first execution step and it has not been reached.
- **Nothing is blocked on you.** `director_requests.md` has no open entry from me. The one licensing question that could have needed you — the Allen Institute brain atlas, whose terms are noncommercial — was resolved last session by deriving what we needed from data we already hold under open licences, so no exception was ever required.

## What is next

Codex reviews Amendment 5 and decides whether to take the removal, a declared ceiling, or a report-only rule. Whatever it chooses, the pairing rule is fixed before the candidate pool is visible. Meanwhile the host-selection gates continue, and the first real machine work — installing the sorting stack and confirming it runs here at a small scale — is Codex's next execution step.

**Nothing to show on your verification picture this session.** It is a Phase 3 artifact and no measured result exists to put in it yet; manufacturing an update would be worse than not having one.
