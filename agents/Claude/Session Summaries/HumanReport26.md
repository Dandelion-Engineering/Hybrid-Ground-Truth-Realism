# Human Report 26 — Claude

**Date and time written: 2026-08-15 01:24 PDT**
(read from the machine clock at the moment of writing, not estimated)

**Session type:** Phase 2 execution. Owner Round-3 response to Codex's RC-001 Round-2 review.
**Progress report due?** No. The next count-based one is Session 32, and this session closed neither a phase nor an amendment.

---

## 1. What this session was for, in one paragraph

The drift gate is the first of three remaining screens that decide which real recording becomes the host for the whole experiment. It has been in formal review for three sessions under a review card, RC-001. Last session I repaired three findings Codex raised; this session he verified two of them, verified the third's implementation, and returned **one new blocking finding — a regression my own repair had introduced.** This session accepted that finding, reproduced his counterexample independently, found it was stronger than he had reported, repaired it in all four places the bad claim appeared, added it to the permanent test harness, re-ran every acceptance test, and handed the state back. **This is the third and final round-trip the review method allows.**

## 2. The finding, in plain language

A recording is screened for drift — the probe physically sliding in the brain during the session — by chopping the recording into one-minute bins, taking the **median** depth of each unit's spikes in each bin, and asking how far that moves.

Last session I wrote a sentence about what this measurement *cannot* see: I said that if a displacement moves fewer than half of a bin's spikes, the bin's median does not move at all. I measured that on a test fixture and published `0 µm`, `15 µm`, `30 µm` as the values below, at, and above the halfway point.

**The sentence is false, and the fixture is why.** In that fixture, every spike in a bin had *exactly the same depth*. A median is a rank statistic — it reports the value in the middle of the queue — so when every value in the queue is identical, moving some of them does nothing until you move enough to change which value sits in the middle. That is a property of that queue, not of medians.

Codex built a queue where the depths are spread out instead: 49 spikes at one depth, two just above them, and 49 far above. Now the two values in the middle have a cliff right behind them. Move any of the bottom 49 upward and the middle of the queue falls off the cliff. He reported that displacing 49% of the spikes by 30 µm moves the median 29 µm — well above the gate's 20 µm limit, on a displacement my sentence said was invisible.

**When I rebuilt it, it was worse.** The same fixture gives 29 µm at 30%, at 10%, and at 2%. A **single displaced spike out of a hundred** already moves that bin's median 14.5 µm. So the defect was not that I put the threshold at the wrong fraction — there is no fraction at which that fixture is blind. A cutoff of that shape does not exist, and any repair that just moved the number would have repeated the error.

## 3. What replaced it

A **bound** instead of a cutoff, stated in both directions:

- Displacing `k` of a bin's `n` spikes upward carries that bin's median toward the depths sitting `k` ranks above it. The move is at most the displacement itself, and at most that rank distance.
- The equal-baseline fixture is the corner where the rank distance is **zero** — which is the entire content of the `0/15/30 µm` sweep. That sweep is kept and explicitly scoped to its own fixture rather than deleted.
- Where the episode falls on the bin grid matters too, because the grid is what fixes `k`: the same displaced spikes read `30.000 µm` inside one bin and `0.000 µm` split across two.
- **Conclusion, stated in both directions:** the gate has no guaranteed resolution below the bin width. It is not a bound on sub-minute motion, and it is not reliably blind to it either.

The bound is checked at zero violations and no negative move over 4,000 random cases across four different depth distributions, and the mirrored downward construction is measured rather than assumed — it reports the same 29 µm.

## 4. The decision I want on the record

**I withdrew the safety claim that travelled with the cutoff instead of re-deriving it on the new bound.**

Draft 23 said the blindness was "permissive — it can only understate drift, never invent it." With no universal blindness there is nothing to call permissive. I *could* have argued the replacement: a bin median cannot overstate a uniform shift of a sub-population, and I measured that it does not. I chose not to. **This is the sixth one-way claim this review chain has caught and the third of mine.** Re-arming a directional claim in the same paragraph where one just failed is precisely the pattern that has kept this section in review for nine round-trips under the old method and three under the new one. §16.4 now names both live outcomes and calls neither a safety property:

- an episode the medians do not express **passes a candidate the gate did not actually clear** (the unsafe direction), and
- one they express in full **rejects a candidate over motion that is not sustained drift** (the conservative direction).

I told Codex in the chat that if he thinks this leaves something load-bearing unstated, that is a finding I want now rather than after the card closes.

## 5. Everything that was checked, and the results

Every one was executed this session, not reasoned about or inherited.

| Check | Result |
|---|---|
| Synthetic harness, pinned 200 permutations | **103 checks, 0 failed** (~48 s). Was 96; the new case adds 7. |
| My three independent claim probes | **3 of 3** |
| **Codex's** `probe_rc001_round1.py` | **0 failures across 12 checks**, including his own heterogeneous construction at `29.000 µm` |
| **Codex's** `probe_draft16_safety_claims.py` | digits unchanged: `7.966`/`8.346 µm`, `27.273`/`11.591 µm` |
| Packet runbook consistency checker | **10 of 10 steps** |
| Encoding invariants | 0 non-ASCII in both code files; document still exactly 8 curly quotes; LF throughout |
| **Docstring-only change to the estimator** | **Proved mechanically.** Syntax trees of the Round-2 and Round-3 states, with every docstring stripped, dump to an identical string. |

That last row matters more than it looks. It is the difference between *saying* the repair cannot move a candidate's measured value and *showing* it: the Round-2 state was recovered from git, both files were parsed, docstrings removed, and the abstract syntax trees compared. They match exactly. No parameter, threshold, seed, verdict path, error string, return key or numerical branch differs.

## 6. Challenges, and how they were handled

**The obvious repair would have been the same error again.** The reported counterexample sat at 49%, one point below my stated cutoff. It would have been easy to read that as "the cutoff is at the wrong place" and move it. Rebuilding the fixture and sweeping it down to a single spike is what showed there is no cutoff to move. **Accepting a finding includes checking whether it is stronger than the person who raised it claimed** — the same lesson Session 24 recorded when I strengthened one of Codex's counterexamples off its degenerate case.

**The bad claim was in four places, not one.** §16.4, the document's status line, §16.8's Draft 23 change note, and the module's own docstring. This project has now been bitten repeatedly by a repaired paragraph leaving its restatements standing; all four were located and repaired in the same edit, and the §16.4 fixture roll-call was moved from eight to nine so the count matches the harness.

**Reading the finished text back as a reviewer caught two more things** before handoff: a number in the status line that still said "one tenth" after I had strengthened the evidence to "one fiftieth and a single spike", and a bound stated without naming which displacement direction it covered. Both were repaired, and the downward direction is now measured rather than assumed. This is the seventh consecutive session in which the read-back pass, not the original edit, produced the last corrections.

## 7. Machine state

Measured at **2026-08-15 01:10 PDT**, immediately before the heaviest step (the 48-second harness):

- **RAM: 0.96 GiB free of 31.67 — 97% in use.** The tightest reading any session in this project has recorded.
- VRAM: 1,086 MiB used of 16,311.
- Disk: 590.6 GB free on `C:`.

The harness needs tens of megabytes and ran without incident, but that reading is worth carrying forward: nothing requiring gigabytes could have been started at that moment. This is exactly the situation the director's compute rule was written for, and it is the reason the rule says to measure at the moment of the step rather than at session start.

## 8. Files created or updated

| Path | What changed |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 24.** §16.4's within-bin boundary paragraph rewritten; the cutoff withdrawn in the status line and §16.8; fixture roll-call eight → nine; Draft 24 change note added. SHA-256 `c35987fe…` |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **Module docstring only** — same correction. SHA-256 `eace4cd3…` |
| `agents/Claude/tools/test_band_drift.py` | New `case_within_bin_transmission_is_distribution_dependent` (7 checks); `common_signal_band` gains an optional within-bin depth distribution and multi-bin episodes, both defaulting to previous behaviour. **103 checks.** SHA-256 `946df906…` |
| `Review Cards/RC-001 Tier A Selection Section 16.md` | Round-3 candidate digests, round log row, full Round-3 response section, acceptance-test count, F1-R1 follow-up entry |
| `chats/Claude-Codex/Tier A Selection Section 16 Review/…Active.md` | Round-3 owner response appended |
| `chats/Claude-Codex-Human/Review Method Change/…Active.md` | Method feedback for Randy and Codex appended |
| `agents/Claude/Session Summaries/HumanReport26.md` | This report |
| `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` | Session closeout |

**The root README's running log was deliberately not touched.** Six consecutive entries already describe this review chain, and this round narrates another round rather than closing anything. The seventh entry should be the one that says the chain closed.

## 9. Next steps

1. **Codex's Round-3 delta-only verification.** This is the last round-trip. If both agents approve the same state, RC-001 closes and the drift gate is settled. If it does not close, the **agent-only Convergence Decision** runs — not a request for Randy's time.
2. **If RC-001 closes:** the archive-reading script (packet step 11) is the next piece of work and gets its own Review Card. Until then, no candidate host may be measured and no archive read.
3. Still open and unchanged: the capacity/ten-placement gate under Amendment 6, the five packet steps that have not been re-run, the preprocessing half of the amplitude question, and the 66 unmapped anatomical long names.

## 10. Nothing scientific happened

No host was pinned, no candidate drift value was measured, no archive or raw data was read, no dependency was installed, no network request was made, no generator or sorter was run, and no Rung 0 work occurred. **The project still has no scientific result, and that remains correct at this stage.**
