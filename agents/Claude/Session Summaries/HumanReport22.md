# Human Report 22 — Claude

**Date and time:** 2026-08-14 05:30 PDT
**Phase:** 2 — Execution
**Session type:** Owner re-review of Codex's Draft 17; three findings; implementation of the reporting requirement one of them created

---

## Summary

Codex reviewed my Draft 16 last session and blocked it. He was right, and he was right about something larger than the two sentences he named: I had twice reasoned from a mechanism to a guarantee without checking whether that mechanism was the only one operating. This session accepted both of his corrections in full, kept his repairs exactly as written, and then ran the owner re-review pass over edits I already agreed with — which is where all three of this session's findings came from, for the fifth session running.

The findings, in one line each:

1. **Two more sentences of the species Codex repaired**, found by treating his repair's *reason* as a search rather than as a fix. §16.7's parameter table still asserted the load-bearing half of the claim his fixture had just falsified; §16.4 carried a second, unrelated one-way claim about adding bins.
2. **Draft 17's repaired conditional was not checkable from anything the reader reports.** The result is now declared conditional on movement being expressed in enough depth traces — an honest sentence that nothing in the committed output would ever measure. On Codex's own fixture, every published quantity is consistent with a quiet host.
3. **What the fix for (2) consumes was not available to consume.** The per-unit excursion is defined on the *centred* series, and centring lived only inside a private function, so a reader implementing the requirement would have had to restate the centring rule outside the module.

So I specified the reporting requirement, implemented what it consumes, and turned Codex's counterexample into a permanent test case. Draft 18 and two implementation states are handed back for his same-state confirmation.

**No host was pinned, no candidate drift, noise or effective-SNR value was read, no archive-reading CLI was written, and no raw data, template array, Rung 0, generator or sorter was run. No scientific result exists.**

---

## What was accomplished

### 1. Startup and the context-first pass

Read `.agent-turn` (named Claude), confirmed `.agent-session.lock` absent, created it, re-read `.agent-turn` (still Claude). Read `AgentPrompt.md`, the whole of `Project Details/Project Details.md`, my `Summary of Only Necessary Context.md`, every concluded `Summary.md` under `chats/Claude-Codex/`, and the active Tier A selection transcript including both of Codex's Session 21 messages before acting.

For cross-review I read Codex's `HumanReport21.md` in full and responded to it substantively in chat rather than only noting it.

### 2. Verified before opening, and re-ran rather than read

Every handed-off digest matched before I opened the file: Draft 17 at `709be46f…` (his corrected hash, not the superseded `90e5b755…`), the renamed utility at `b2c01605…`, his review probe at `af51fe50…`, and the two closed states plus `.gitattributes` at their approved digests.

I re-ran the shipped validation rather than accepting his numbers — **57 checks / 0 failed at 200 permutations, 3 of 3 claim probes, 10 of 10 runbook steps** — and then ran *his* probe rather than reading its reported output. Both counterexamples reproduced to the digit: `24.545454545454547` / `11.590909090909090` collapsing to `0.0` / `0.0` on the eleven-unit set, and `8.345705622445344` falling to `7.965855925506574` at trial 3.

### 3. Why he was right, stated as the general error rather than the two instances

My Draft 16 claim was that extra scatter from added weaker units must widen `Q95_null`, so the label-blind set could not buy a pass. That covers added units carrying *more* noise and says nothing about added units carrying *less*. A median over eleven series where six are flat is pinned by the flat ones — in the observation *and* in the null — so both numbers go to zero together and the pass is bought exactly as he showed.

The head-bin claim failed the same way: "fewer spikes, therefore noisier, therefore wider" is a statement about expectation that I had written as a statement about every realization.

I also examined his second repair and preferred it to my Draft 16 text on its merits: containment's two margins are **endpoint slack**, not the check's "resolution," because a scale error can keep both endpoints inside the interval while moving spikes across internal bin boundaries. Calling them a resolution would have implied a bound they do not provide.

### 4. Finding 1 — following the repair's reason into sentences it did not reach

Codex's repair reason is general: *this document states one-way directional guarantees about the estimator that were never proved.* Used as a search key, it finds two more.

**§16.7's unit-set basis cell** read "the inclusion rule below already removes the units that cannot carry a displacement." His six flat traces hold 10 spikes in 100% of bins, pass the inclusion rule untouched, and cannot carry a displacement. The prose in §16.4 had been repaired to the correct statement — the rule removes units lacking *temporal support* — and the table cell kept the old one. This is the recurring shape in this project: the repair lands in the paragraph and the table keeps the retired claim.

**§16.4's "adding bins cannot inflate it unless the band genuinely moves further."** A noisy bin can extend a peak-to-peak range with no movement, which is the entire reason §16.5's null exists. The real contrast being drawn is with path length and it survives without the quantifier. Draft 18 says adding bins raises the excursion only by putting a wider pair of levels inside one window, never by summing increments — which is true for both the full-recording and the ten-bin-window quantity, and I checked that second case specifically before writing it, having first written a looser version ("reaches a level it had not already reached") that is false for the windowed statistic.

### 5. Finding 2 — the conditional nothing measures

This is the finding I think matters most, and it is a consequence of Codex's repair rather than an objection to it. Draft 17 states the result is "conditional on movement being expressed in enough of those depth traces for the across-unit median to carry it." I agree with the sentence. But the reader's committed output is `Delta_10`, `Q95_null`, `Delta_full`, bin counts, unit counts, row identifiers and labels — and on his fixture every one of those reads like a quiet host. A conditional that nothing measures is a limitation sentence doing a rule's job.

The failure shape has a visible signature — a minority moving while the median stays flat — and it lives in quantities the estimator already computes on its way to `D(b)`. Draft 18 requires the reader to report, for every included unit, that unit's centred excursion over the whole recording and inside the band's gating window.

**On his fixture the diluted band reports `Delta_10 = 0` while five of the eleven per-unit window excursions read 24.545 µm** — the undiluted band statistic, recovered from the very report that suppressed it.

I spent most of the design effort on making "reported and never consumed" airtight rather than on the quantity itself, because an unconsumed diagnostic is exactly where a specification quietly makes policy. Draft 18 pins: no verdict, label or ordering reads them; they cannot rescue a candidate above `L` or reject one below it; a disagreement with the band statistic is published as a limitation on that host and does **not** reopen the verdict, because a verdict reopened on a diagnostic read after the values are visible is the drift-shopping §15 exists to prevent; and turning them into a gate requires a threshold this project has no basis for, reachable only through §16.7's recorded-turn rule. They end up with exactly the status `Delta_full` already has in this section, which is the precedent I anchored them to rather than inventing a new category.

### 6. Finding 3 — and the implementation, because the requirement had an unpinned input

The per-unit excursion is defined on the *centred* series, and centring lived only inside the private `_trace_from_medians`. Specifying the requirement and leaving it there would have handed the reader a rule whose input it had to restate — a rule is only pinned if what it consumes is pinned too, which is the defect this section has now hit eight times in different clothing. So I implemented it.

`Reproducibility Packet/scripts/utils/band_drift.py` gains:

- **`unit_traces`**, now the module's *single definition* of the centring step, with `_trace_from_medians` rewritten to call it;
- **`unit_excursions`**, which ranges each centred series whole and inside the band's gating window;
- **`unit_delta_full`** and **`unit_delta_window`** on a measurable result, aligned with `included`;
- the across-unit median's modelling assumption stated in the header *as* an assumption, with a pointer to the per-unit values;
- the retired "complete bin" vocabulary replaced in the five rejection-reason and error strings that leave the module in a result file, and the word given a stated meaning in `complete_bins`' docstring — full-width on the session grid, which is what the function counts, not full recording coverage.

Two deliberate non-changes. `_trace_from_medians` keeps its signature and 3-tuple return, because Codex's probe and my `probe_band_drift_claims.py` both call it and neither should have to change for a diagnostic. And `complete_bins` is **not** renamed despite the vocabulary shift: two closed states call it, and a pure rename would reopen both for no safety gain — unlike Codex's `duration_s` → `extent_s` rename, which prevented a future caller from passing a wrong *value*.

### 7. Codex's counterexample is now a permanent test case

`agents/Claude/tools/test_band_drift.py` gains `case_per_unit_audit_values`: five units on a 30 µm ramp plus six flat traces, asserting that the band median reports zero, that the largest per-unit window excursion still carries 24.545 µm, that the two groups separate 5 / 6 at the 20 µm line, that the audit values do not reach the verdict, that every centred series has median zero, that no per-unit whole-recording excursion is below its own window excursion, and that a mismatched mask raises. The harness is at **65 checks, 0 failed** at the pinned 200 permutations.

Its module docstring already named three cases that exist because of specific review defects; this is the fourth and it is listed with the others, with the defect named rather than only the fix.

---

## Challenges and how they were handled

**One test failed on first run, and the test was wrong.** I had asserted exact float equality between the diluted fixture's largest per-unit window excursion and the undiluted band statistic. They differ in the last ulp because the two paths select different windows on a linear ramp — `window_start` 0 versus 2, where every window has the same span up to rounding. The rule here is to ask whether the test or the artifact is broken before touching either; it was the test. It now asserts within 1e-9 and prints both values to twelve places so the reason is visible in the output rather than buried in a tolerance.

**Deciding how much to change in someone else's approved state.** Codex handed back Draft 17 and the renamed utility as approved states. Findings 2 and 3 required editing the utility again, which reopens a loop that has already taken seven turns. The alternative was to specify a requirement whose input did not exist, which is the failure mode this project keeps paying for. I chose the edit and constrained it hard: purely additive to the module's public surface, no numerical branch touched, and — because "no numerical branch changed" is exactly the kind of claim this session was about — verified rather than asserted, by re-running *his* probe against the edited module and confirming both counterexamples reproduce to the same digits.

**Judging whether the per-unit diagnostic was worth its own risk.** An unconsumed diagnostic can become a post-hoc threshold, and I have added requirements before that needed later repair. What settled it: the diagnostic costs no extra data, no extra permutations and no new parameter; it is computed by the same code path as the gate; and the alternative is a published conditional that nobody can ever check. I wrote the non-consumption rule and its disagreement semantics into the specification in the same edit rather than leaving them to a later session, because failure semantics are where a specification quietly makes policy.

---

## Insights worth carrying

**An unproved one-way claim is a species, not an instance.** Codex found two; the same reason found two more in sentences he had read past. The general form is worth stating: whenever this document says a choice can only make the gate stricter, someone has to have checked the case where the added thing is *quieter* rather than noisier, not only the case where it is noisier.

**A limitation is not a safeguard.** Draft 17's conditional was honest and correct and did nothing, because no committed output could ever exhibit it. The useful question after writing a limitation is: *what number would have to move for a reader to notice this had happened?* If the answer is "none," the limitation is a sentence.

**The fix for a masked signal was already in the pipeline.** The per-unit centred series exist for one line inside a private function on the way to the median that discards them. This is the fourth time this section has found what it needed in something already computed or already downloaded — after the drift replacement in a column description, the nominal-clock split in a tracked JSON file, and the unit counts in a cached placement file.

**Renaming is load-bearing only when the name invites a wrong value.** Codex's `duration_s` → `extent_s` prevented a caller from passing the span. My "complete bins" → "analysed bins" only affects what a reader is *told* — so it belongs in the strings that leave the module, and does not justify reopening two closed states to rename a function.

---

## Validation

- `agents/Claude/tools/test_band_drift.py`: **65 checks, 0 failed** at the pinned 200 permutations (57 before this session's new case).
- `agents/Claude/tools/probe_band_drift_claims.py`: **3 of 3 probes passed**, unchanged at `4f3b8377…`.
- `agents/Codex/tools/probe_draft16_safety_claims.py`: **both counterexamples reproduce to the digit** against the edited module — `24.545454545454547` → `0.0` and `8.345705622445344` → `7.965855925506574`.
- Packet runbook checker: **10 of 10 steps agree**.
- `band_drift.py` compiles in the project venv; no non-ASCII, no CRLF, no lines longer than the file's pre-existing maximum.
- The chat append was verified by reading the file back: the prior bytes remain an exact prefix, and the file's 107 CRLF line endings are unchanged.

---

## Files created or updated

| Path | Change |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 18 — three findings repaired; SHA-256 `6c0c04886e99e4093474ea3ddf0aa19b86a79eeb2044f4650ce644adb1360618`. Open on Codex. |
| `Reproducibility Packet/scripts/utils/band_drift.py` | `unit_traces` / `unit_excursions` added, per-unit keys returned, vocabulary repaired; SHA-256 `7c74c5e8ab6490e1d680edab53624a879522f6d3e4aa8fa595f32ed51f3f8ca9`. Open on Codex. |
| `agents/Claude/tools/test_band_drift.py` | Codex's counterexample kept as a permanent case; SHA-256 `ab16c0e1606da4416c87185846fe5f43dd795431105d4bc5ff1180d9536f78f2`. Open on Codex. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only owner re-review, three findings, exact-state handoff. |
| `README.md` | One running-log entry: the limitation that nothing measured, and the per-neuron report that now would. |
| `agents/Claude/Session Summaries/HumanReport22.md` | This report. |
| `agents/Claude/README.md` | Workspace map refreshed. |
| `agents/Claude/Summary of Only Necessary Context.md` | Completely rewritten for Claude Session 23. |

No progress report was due — the next count-based one is Session 24, and this session closed no phase and approved no amendment. No new director request is needed; nothing is blocked on Randy.

---

## Machine state

Measured at 2026-08-14 05:06 PDT: **1.67 GiB RAM free of 31.67 GiB; 1,039 MiB VRAM used of 16,311 MiB; 582.8 GB free on `C:`.** Nothing heavy ran — the whole session's computation is small synthetic arrays, and the full 200-permutation harness takes 23 seconds. This reading describes the moment it was taken and is not permission for a later heavy step; every one of those needs its own fresh measurement.

Worth noting against Session 21's reading of 6.79 GiB free two hours earlier: the machine gave back five gigabytes in that gap. That is the entire reason the rule forbids inheriting a number.

---

## Next steps

1. **Codex owner-reviews the three exact states** handed back this session. §16 stays open until he approves those bytes or edits and returns new ones.
2. **If Draft 18 comes back approved, I write the archive-reading CLI** against that state — targeted range reads for band units only, the four §16.8 confirmations before it computes anything, and the per-unit excursions in what it reports. It becomes packet step 11 only once it has actually been executed.
3. **Only after the CLI itself is approved may rank 1 be read** for a drift value.
4. Noise, post-rescaling effective SNR, the joint ten-placement gate, and Codex's balance/manipulation gate remain separate and unstarted. Five archive-reading packet steps still await a re-run, and the drift reader is the natural place to fold them in.
