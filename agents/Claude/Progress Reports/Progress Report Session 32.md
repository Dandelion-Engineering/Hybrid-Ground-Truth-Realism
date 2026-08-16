# Progress Report — the difference between counting a cost and refusing it, twice

**Claude, Session 32 · 2026-08-16 (see the session report for the exact clock reading)**
**Trigger:** regular cadence — my eighth session since the last count-based report.
**Phase:** 2 (Execution). Still no host recording chosen, no archive read, no data generated, no sorter run, no result of any kind.

---

## The short version

We are still building the one piece of software that will read a real recording for the first time. It has now been reviewed four times across three review cards, and it has not been approved yet. This session was my last allowed attempt on the current card: if my collaborator returns it again, the method the director set requires us to split the work up or redesign it rather than take another turn.

Two things were still wrong, and both were the same shape as errors this project has made before — a check that looks like it establishes something and does not.

1. **Our provenance check searched for a word.** A recording carries a line saying what software produced it. We required that line to contain "NeuroConv". My collaborator built a file whose line reads *"This asset was NOT created using NeuroConv; exported by LocalTool v3"* — and it passed, because it contains the word. **A file that denies the toolchain names it too.** We now match the whole sentence rather than searching it, and we additionally require the two halves of one recording to name the *same* version, because our claim is that both halves share a clock.

2. **Our safety budget was measured in the wrong currency.** We bounded how many bytes the software *asks for*. What it actually spends is bytes *transferred*, and the reader underneath fetches whole one-megabyte blocks — so a sixteen-byte request for a byte nobody has fetched yet costs a megabyte. On his test file, **2,081,456 bytes moved before a 65,536-byte budget refused anything.** The budget was not merely unenforced; at that block size it was unreachable, because nothing can be read for less than a block.

The fix for the second one is what I want to record, because finding it required disbelieving my own first answer.

## The part worth reading

My first repair was to bound the transfer for the provenance read specifically — the thing his finding named. Before writing the claim, I measured where his 2,081,456 bytes had actually gone.

> **Every single one of them was spent before the provenance read began.** The provenance read itself transferred **zero**.

They were spent by the four ordinary reads that come first — the electrode table, the neuron list, two column descriptions. Those reads are *counted*: their cost lands in the plan the software publishes. But counted is not refused, which is exactly the distinction my collaborator taught me one round earlier, from the other side. A repair aimed only at the provenance read would have made a true statement about a number that was never the problem.

So the repair went one level up. The user of this software declares a memory ceiling. That ceiling used to be checked **once**, against a plan written after all of those reads had already happened — correct, and late. It is now held open for the entire read, so a fetch that would cross it is refused before the bytes move.

On his own construction, with his own one-byte ceiling, the spend goes from **2,081,456 bytes to zero.**

And this is not a case of raising a number until the claim became true. The argument that licenses it is that the ceiling *cannot refuse anything it would otherwise have admitted*: the plan's own combined figure already contains the transfer bound, so any read the old check accepted had, by definition, transferred less than the ceiling. The new refusal is strictly earlier, never stricter.

## What this cost, and what it bought

- The automated test suite went from **325 checks to 382**, all passing.
- The sabotage harness — which removes one repair at a time and requires the tests to notice — went from 20 to **26 sabotages**, all caught, with the unmutated control green.
- Three of those sabotages found something before my collaborator could: two of them made the tests crash rather than fail, which proves nothing about which check was load-bearing, and one was pointed at a test whose name I had written with a space in it so the harness never matched it. **A sabotage that "passes" for the wrong reason is the same failure mode as a test that passes for the wrong reason**, and this is the second session running where re-running the harness after a repair was the only thing that said so.
- A housekeeping defect recorded last session was also repaired: the test suite was leaving its temporary fixture folders behind on Windows, silently, because a file handle was still open when it tried to delete them. 111 of them had accumulated. That is now zero, and the suite says so out loud if a folder survives.

## What's working

- **The bounded review method is doing what the director designed it to do.** Three rounds, three ledgers, no repeated argument. Every round has accepted the previous round's findings in full and then found something new that the repair itself exposed.
- **Reproducing the reviewer's evidence before touching anything.** For the fourth card running, I ran his probe unmodified against the unchanged code first, and it returned his exact figures. That habit is what makes "accepted in full" mean something.
- **Nothing has been spent.** Every fixture in all of this is small and synthetic; the whole suite runs in fifteen seconds. No candidate recording has been read, so the project has not yet spent the ability to make an honest first measurement.

## What isn't working

- **This is the fourth review of the same component and it is still not approved.** Each round has found something real, so I do not think any of them was wasted — but the honest summary is that this piece of software has been harder to get right than the specification it implements was.
- **The measurement still has not started.** No host is pinned, no candidate has been read. The first real drift number is one approval away and has been for several sessions.
- **One thing I now expect to bite on the first real run.** Requiring a recording to state its conversion software, and requiring its two halves to agree, can stop the run on a real file. That is deliberate — it pauses the queue rather than rejecting the recording — but it means the first real attempt has a new way to halt, and I would rather flag it now than explain it afterwards.
- **Three older items remain unresolved**, none new: the placement-capacity check under a recent amendment, the preprocessing half of an amplitude question that metadata cannot answer, and 66 anatomical labels only a brain atlas could resolve, where the atlas we would want carries a non-commercial licence we have declined.
- **No open blockers on you.** `director_requests.md` has nothing waiting.

## Verification artifact

Nothing new. The director-facing verification artifact is a Phase 3 obligation and no work went into it this session; I would rather say that than manufacture an update.

## What's next

If my collaborator approves this state, the next work is the first real measurement of the project: reading one candidate recording out of the public archive and computing its drift number. If he returns it again, the method requires the work to be split or redesigned rather than repaired a fourth time on the same card — and I would come to you with what the changed boundary should be.
