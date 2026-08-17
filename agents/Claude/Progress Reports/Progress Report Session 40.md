# Progress Report — the test that passed in both worlds

**Claude, Session 40 · 2026-08-17 (see the session report for the exact clock reading)**
**Trigger:** regular cadence — my eighth session since the last count-based report.
**Phase:** 2 (Execution). Still no host recording chosen, no drift number, no data generated, no sorter run, no result of any kind.

---

## The short version

The safety layer I have been building for the last four sessions went to my collaborator for review. He returned it with two objections. **Neither was about the mathematics** — he stress-tested that independently, with 120 of his own synthetic recordings and 1,080 different ways of filling in the missing values, and every single one landed inside the range our code promises. Both objections were about the machinery *around* the mathematics, and both were real.

1. **The tool's last printed line contradicted the tool's own decision.** On the test case where the layer correctly pauses a recording that the plain measurement had passed, the saved record said *unmeasurable*, the written report said *unmeasurable*, a line in the middle of the run said *unmeasurable* — and then the run ended with `passed=True`.

2. **The memory estimate had gone stale by exactly one byte per spike.** The reader now keeps a small marker beside every spike saying whether that spike's depth is missing. Those markers are held for the whole read, and the estimate that decides whether a read fits in the machine's free memory had not been updated to count them. On the leading candidate recording that is **3,160,311 bytes held without being counted.**

Both are repaired. The repairs cost 25 new automated checks and one new harness, and the whole state is back with my collaborator for a delta review — under our method, round two only looks at what changed.

## Why the first objection is not a triviality

It would be easy to read objection 1 as cosmetic: the *data* was right, only the *printout* was wrong. That reading is backwards, and it is worth spelling out because it is the kind of mistake that survives a careful review of the wrong artifact.

The record and the report are files. **The console line is the thing a human — or, later, a script — actually acts on.** Our whole selection procedure works down a fixed list of thirteen candidate recordings, taking the first one that clears every gate. A recording our own layer had just refused to certify was, on the last line of the run, announcing itself as passed. Nobody would have to be careless to act on that; they would only have to read the end of the output.

And our test suite could not have caught it, because every check we had written read the saved files. **A defect that lives only in the console is invisible to a check that only reads artifacts.** The three whole-command test cases now capture the console text and require its last line to be the reconciled decision, and require any line that still reports the plain measurement to say on its face that it is a diagnostic.

## The part worth reading: my first repair for objection 2 was untestable

The memory repair itself is two lines. The interesting part is the test I wrote for it, which was wrong in a way I have now made twice in three sessions.

The tool refuses a read whose total memory footprint would exceed a declared ceiling. To prove the markers are counted, the test sets the ceiling to **"the correct total, minus the markers"** and requires the read to be refused. If the markers are counted, that ceiling is one marker-block too small and the read is correctly refused. If they are not counted, the total is *already* that number and the read sails through. A perfect test — except that I computed "the correct total" by asking the very calculation I was testing.

So when I deliberately removed the marker term to check my test would notice, the ceiling moved down with it, and the read was refused anyway. **The test passed in both worlds.** It was measuring nothing at all.

The fix is to build the ceiling out of something the defect cannot move: the fixture's own spike count, which comes from the recording, not from the calculation. With that change, removing the marker term makes the test go red, which is the only evidence that it was ever a test.

I trust this pattern enough now to state it as a rule: **when a test says a quantity is "computed independently," ask independently *of what*.** In three sessions I have found two checks that were comparing two halves of the same idea and reporting the agreement as a result.

## What is new since the last report

- The layer that bounds what a missing depth could have done to the result is now **inside the command that reads the archive**, rather than a module beside it — published three ways (per neuron, per minute, in total), with both of the gate's numbers bounded over every possible completion of the missing values.
- The bound on the *second* of those numbers — the noise floor, which is the harder one — was shown to be possible with **nothing assumed** about the missing values, after an earlier draft of mine claimed it was impossible. That claim was false and the argument turned on a single word.
- Both objections from this round are repaired, and my collaborator's own probe — run unmodified against the repaired code — now reports both of its flags off.
- A new harness undoes each repair in a throwaway copy and requires the test suite to go red: **4 of 4 caught**, plus the 32 older sabotages re-run, because a repair can silently delete the coverage a different test depends on.

## What is not working, honestly

**Four sessions have now produced no measurement.** The first real read of a real recording happened four sessions ago; it reached the data, and stopped on a rule we wrote before we had ever seen a recording, because 231 of 3.16 million spikes carry no depth value. Everything since has been building the thing that lets us proceed *without* quietly dropping those spikes.

I think that was the right call — the cheap version can be wrong by five times the tolerance and no count of dropped values would reveal it — but I want to name the risk plainly, because it is mine to watch: **a project can polish its instrument indefinitely and call it progress.** The specific thing that would tell us this has gone too far is another round of objections that are about our own machinery rather than about the recordings. If the next review returns blockers of that kind again, the honest response is to ask whether the layer should be simpler, not to repair it a third time.

Two smaller open items:

- One accounting follow-up my collaborator raised and deliberately did **not** treat as blocking: the command makes a second copy of the spike arrays even when nothing is missing — about 50 MB on the leading candidate. It is outside what the current memory ceiling claims to cover, so calling it a violation would have quietly widened that claim. It is recorded, and it has to be counted if we ever claim a whole-command memory figure.
- Two entries in `director_requests.md` are still open. The memory-contention one **you already answered** (the day/overnight split between this project and the other one, which is now recorded as Amendment 1). The other is the standing invitation to review the project contract — explicitly non-blocking, and the agents have been working under it the whole time.

## What is next

1. My collaborator's delta review of the repairs. If it closes with both of us approving the same exact state, the two paused candidate recordings unpause and keep their place in the queue.
2. **The first real drift measurement** — about 3 to 7 minutes and 55 to 67 MB of downloading, checked against the machine's free memory immediately beforehand.
3. When that produces a report, the drift command finally becomes a numbered step in the reproducibility packet's runbook instead of the one script still marked "pending its first execution."

No verification-artifact update this time: nothing about the director's verification path changed this session, and I would rather say so than manufacture one.
