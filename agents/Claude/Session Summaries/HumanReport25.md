# Human Report 25 — Claude

**Date and time:** 2026-08-14 23:40 PDT
**Phase:** 2 — Execution
**Session type:** RC-001 Round-2 owner response (all three Round-1 findings accepted and repaired); acceptance of the convergence consensus and its writing into the review-cycle playbook

---

## Summary

Two pieces of work, both of them handed to me by the previous session's close.

**The first is the one that matters scientifically.** Codex's RC-001 Round 1 — the first review run under Randy's new method — found that the drift gate does not implement the quantity it is named for. The gate is supposed to bound how far the probe moves inside the ten-minute segment this experiment will inject into. It was implemented as the worst window of ten consecutive one-minute bins. Ten one-minute bin medians span only *nine* minutes between their extremes, and a ten-minute segment that does not begin on a bin edge touches *eleven* session bins rather than ten. Both errors cost exactly one bin and both run permissive, so the gate reported less drift than there was and would have accepted a recording moving 21 µm in ten minutes against a 20 µm tolerance.

**I accepted all three findings, disputed none, and reproduced every one of his constructions independently before touching anything.** The repair moves `PARAMS["window_bins"]` from 10 to 11 and renames the symbol `Delta_10min`. It is provably a tightening — every ten-bin window sits inside an eleven-bin one — so it can reject a candidate the old definition would have passed and never the reverse. His third construction is not repairable by any window length and is now a declared, measured boundary instead. His second finding killed a one-way claim of mine from Session 24, and I withdrew it with a counterexample rather than rescuing it.

**The second is procedural.** Randy asked the two agents to agree on what happens instead of escalating a stuck review to him, since he is asynchronous by design and a parked review costs sessions. Codex proposed a five-clause replacement at the end of his Session 24. **I accepted it as written**, and it is now in `Playbooks/review-cycle.md` as a new section inside the superseding method, with his instruction quoted verbatim.

**No host was pinned, no candidate was measured, no archive was read, and no scientific result exists.** The archive-reading CLI remains blocked until RC-001 closes.

---

## What was accomplished

### 1. RC-001-F1 — the gate window (blocking, accepted, repaired)

**Verified before repaired.** Finding 10 in my own carried notes says that when the other agent hands you a probe or a proof, you run it rather than reading it. I wrote an independent script with my own fixtures — not his — and all three of his constructions reproduced:

| construction | ten-bin result | truth | verdict at 20 µm |
|---|---|---|---|
| common `2.1 µm/min` ramp, 5 units, 61 bins | `19.032 µm` | `21.000 µm` in ten minutes | **passed** |
| 30 µm episode inside 40% of one bin's spikes | `0.000 µm` | 30 µm | **passed** |
| levels `[0, 15×9, 30, …]`, off-grid `[30 s, 630 s)` | `15.000 µm` | `30.000 µm` | **passed** |

**The repair, and why eleven is the right number rather than a guess.** The two aliasing mechanisms are different arguments that cost the same one bin and coincide exactly at eleven:

- a bin median is a *point summary*, so `k` of them span `k − 1` bin widths — ten span nine minutes;
- a 600-second half-open segment placed anywhere on a 60-second grid touches **10 or 11 bins and never more**, which I checked over 8,572 sub-bin offsets rather than asserting.

Eleven consecutive bins therefore contain every bin any ten-minute segment can touch, so the reported value bounds the range of the bin-median levels across that segment wherever it lands. That is a provable covering statement, not a directional intuition — which matters, because directional intuitions are the exact defect class that has produced four corrections in this section.

**The change is monotone, and I proved it rather than argued it.** Every ten-bin window is contained in an eleven-bin window, so the statistic is non-decreasing; measured at zero violations over 2,000 random traces. Consequences, stated in the document:

- it can turn a pass into a rejection, or into an *unmeasurable* rejection when `Q95_null` rises above the tolerance, and **never the reverse**;
- §16.7's pre-declared 20 → 40 µm relaxation ladder is what covers the case where it rejects the whole pinned order. The ladder was written before any measurement, which is precisely why this tightening is affordable now.

**Nothing else moved.** No other parameter, threshold, seed, verdict path, error string or return key changed. The permutation null, the two-number pass rule and the six per-unit audit lists are untouched.

### 2. The within-bin boundary — declared, not repaired

Codex's third construction is not fixed by any window length, and he explicitly allowed the alternative: move it to a declared boundary with a justification. I did, with a measurement rather than a hand-wave. Sweeping a 30 µm episode confined inside one bin:

| fraction of the bin's spikes displaced | reported excursion |
|---|---|
| 0.30, 0.49 | `0.000 µm` |
| 0.50 | `15.000 µm` |
| 0.51, 0.90, 1.00 | `30.000 µm` |

So the gate resolves displacements persisting across at least half of a bin's spikes — half a bin's duration where firing is locally uniform — and is blind below that. **§16.4 now states that the blindness is permissive: it can only understate drift, never invent it**, which is the unsafe direction for a host gate, and that a passing candidate is admissible against drift *expressed at 60-second resolution* rather than against sub-minute motion.

**Why I declined to build a sub-bin statistic** — the third time I have declined machinery in this section for the same reason. §16.7's inclusion floor is ten spikes per bin, so any sub-bin split rests on five or fewer centre-of-mass depths for a marginal unit and reintroduces exactly the per-spike noise the bin median exists to remove. It would also need a threshold this project has no basis for. Saying what the gate cannot see is cheaper and more honest than building a second estimator to rescue it.

### 3. RC-001-F2 — my own one-way claim, withdrawn (blocking, accepted)

Draft 22 said masking gets *easier* as the band grows, citing `21.98`, `18.14`, `14.94 µm` at 11, 21 and 41 units. Codex's arithmetic is exact and I had not checked it: `5/11`, `10/21`, `20/41` are `0.4545`, `0.4762`, `0.4878`, so **the series was not at a fixed moving fraction** and I presented it as though it were.

I then checked whether the direction survives at a genuinely fixed fraction under the corrected window. It does not. **35 of the 120 fixture seeds in `7000`–`7119` are not monotone decreasing at a fixed 40% moving fraction**; seed 7025 reports `12.192`, `11.529`, `14.190 µm` at 10, 20 and 40 units. The claim is withdrawn, the arithmetic that killed it is in the text, and both the counterexample and the seed count are permanent harness cases.

**This is the fourth one-way claim of mine this defect class has caught, and the second in two sessions.**

### 4. The knock-on the F1 repair created — the closest thing to a regression this session

The masking fixture that supports *absence of separation proves nothing* **no longer passes the corrected gate**: the twenty-one-unit construction now reports `21.614 µm` and fails. A failing fixture demonstrates nothing about what a *passing* candidate hides — that is exactly the near-miss error I logged last session. So I re-established it:

- forty-one units, twenty of them ramping 30 µm, **passes** at `Delta_10min = 14.941 µm` and `Q95_null = 7.125 µm`;
- the moving units' own-worst excursions `[32.5, 57.0] µm` overlap the stationary `[20.9, 37.6] µm`;
- **seven of the twenty** moving units sit inside the stationary range.

§16.4 and §16.8 now cite that fixture, and say plainly that it is one construction that licenses nothing about how masking scales — which is F2's whole point.

### 5. RC-001-F3 — accepted as written (non-blocking)

§16.4 step 3 said a median's value does not move with the number of spikes underneath it. That is literally false; adding an observation can move a realized sample median. It now says a median carries no spike-count term — it cannot mechanically accumulate a positive contribution per spike the way the retired path-length column does — and that more spikes buy a smaller sampling error rather than a larger value.

### 6. Acceptance tests, all re-run

| test | result |
|---|---|
| `test_band_drift.py` at the pinned 200 permutations | **96 checks, 0 failed**, 48 s (86 at Round 1) |
| `probe_band_drift_claims.py` | **3 of 3** |
| Codex's `probe_draft16_safety_claims.py` | both counterexamples reproduce; one digit moved (below) |
| packet runbook checker | **10 of 10** steps |

**Codex's probe is the interesting one.** Its head-bin pair is unchanged at `7.966`/`8.346 µm`. Its label-set counterexample's moving-only value moves from `24.545` to `27.273 µm` — which is exactly `10/9` of the old value, since `24.545 = 30 × 9/11` and `27.273 = 30 × 10/11`. That is the defect's own signature appearing in his fixture. `Q95_null` is unchanged at `11.591 µm` and the expanded eleven-unit set still passes at `0/0 µm`, so his counterexample is intact and only the recorded digit moved. **His probe is his to re-pin and Draft 23 does not edit it**; §16.4 carries the new number.

### 7. The convergence consensus, accepted and written into the playbook

Codex's five clauses are in `Playbooks/review-cycle.md` under *Convergence in place of escalation*, unaltered, with Randy's instruction quoted verbatim. `Escalated` is removed as an outcome of ordinary review and *triggers human triage or a split* becomes *triggers the Convergence Decision*. The quality checklist, the failure-modes list, the precedence note against `Project Details.md`, the Review Cards template and index, and RC-001's own outcome line all follow it.

**Two things I added, both marked in the chat as applications of existing notes rather than changes to his proposal, and both explicitly strikeable by him:**

1. the Convergence Decision is written **into the Review Card**, since the card is already required to be readable as the review's whole history without the transcript;
2. **a director-only finding is not a review outcome and never was** — a licence question, outside contact, a spend, or a Claim Sheet amendment still reaches Randy through `director_requests.md` with a fallback. Removing `Escalated` removes a review outcome, not the director's channel. I wanted that written down so nobody later reads the removal as closing it.

I also folded his `Supersedes:` field into the card template, because his clause 4 depends on it.

---

## Challenges, and how they were handled

**The repair invalidated numbers scattered across the document.** Changing the window changed the value of every quoted fixture in §16 — nine separate numbers across four paragraphs, plus two harness fixtures that held exactly ten bins and became unmeasurable. There was no way to reason about which ones moved; each had to be re-measured. Every quoted number in Draft 23 comes from a harness run in this session, and the two ten-bin fixtures each gained one bin with nothing else about them changed.

**One number I nearly got wrong.** My scratch reproduction of the ramp reported `19.032`/`21.173 µm`; the permanent harness fixture, on a different seed, reports `19.145`/`21.258 µm`. I had already written the scratch numbers into the module docstring before noticing that the document must cite the *permanent case*, not the throwaway. Fixed before anything was handed off, and the chat says explicitly which numbers came from which.

**Deciding whether to accept or counter-propose the convergence rule.** Codex asked me to accept as written or counter-propose the smallest change I need. I wanted two things added, and rather than spend a round-trip on it, I checked whether either actually changes his clauses. Neither does — both apply notes the playbook already carries. So I wrote all of it in, labelled which parts are his consensus and which two are mine, and said plainly that he can strike either. That gets the method binding this session instead of next, which is what Randy asked for.

---

## Decisions made, and the reasoning behind them

1. **Eleven bins rather than a redesign of the statistic.** The architecture — bin, centre, median across units, peak-to-peak over windows, permutation null, two-number gate — is not what failed. One parameter and its justification were wrong. A redesign would have been a `Split/Redesign Required` disposition and would have cost the project a section it has spent nine round-trips on, for a defect that is one bin wide.
2. **Rename `Delta_10` to `Delta_10min`.** Renaming is load-bearing only when the name invites a wrong value. `Delta_10` invited "ten bins" and that reading is what produced the defect. The result keys (`delta_window`, `window_start`) were already neutral and are unchanged.
3. **Declare the within-bin limit rather than measure it.** Reasoning in §2 above. This is the third time in this section that the cheaper and more honest repair was to say what a quantity cannot support rather than build a second estimator to rescue it.
4. **Re-establish the masking fixture rather than drop the claim.** The claim — that an audit showing no separation is not evidence the gate's conditional holds — is still true and still load-bearing. What broke was its supporting fixture, and a passing one exists inside the same admitted parameters.
5. **Add one public running-log entry despite four consecutive entries already describing this review chain.** Codex's entry told a public reader that the steadiness check can pass movement larger than its own limit, and stopped there. Leaving that open with no resolution is worse than a fifth entry. Mine says it was fixed, that fixing it made it stricter, and what it still cannot see.
6. **Do not edit Codex's probe.** Its recorded digits are his. I reported the moved digit and the arithmetic behind it instead.

---

## Reasoning paths explored and not taken

- **Narrower bins instead of a wider window.** Halving to 30-second bins would address sub-bin motion directly. Rejected: it halves the spikes per bin against a ten-spike inclusion floor, which would remove units the gate needs and would degrade every bin median. The bin width is the noise-suppression mechanism the whole quantity rests on.
- **A within-bin dispersion diagnostic.** Rejected for the same reason a per-unit null was rejected twice before: it would be an unconsumed diagnostic needing a threshold this project has no basis for, and unconsumed diagnostics with no reading rule are what generated the last three review rounds.
- **Sweeping seeds until the masking direction held.** Explicitly not done. Finding a seed where the direction survives would be exactly the error F2 identifies. I swept to find whether counterexamples exist, found 35 in 120, and reported that.

---

## Insights gained

1. **Two independent errors can cost the same one bin and coincide exactly.** The point-summary span and the off-grid overlap are unrelated arguments; both are fixed at eleven. When two independent corrections land on the same number, that is worth checking rather than celebrating — I checked the covering property over 8,572 offsets rather than trusting the coincidence.
2. **A test can encode the defect it was written to catch.** `case_known_ramp` asserted `expect_win = ramp × 9 / n_bins` — it had the nine-minute span written into it as the expected answer, and passed for eight sessions. A harness written from the implementation confirms the implementation.
3. **The most productive part of the new review method is not the round cap.** It is the Review Card's `Purpose` field. Nine rounds of the old cycle compared each draft to the previous draft; nothing compared the artifact to what it was for, because nothing had written down what it was for. F1 is a purpose mismatch and that is why a purpose-directed pass found it first time.
4. **A repair that changes a pinned number is affordable exactly once — before measurement.** Every prior session's discipline about writing thresholds and ladders before seeing data is what made this repair a routine tightening rather than a crisis. Had one candidate been measured, changing `window_bins` would have been a recorded-turn amendment with a much higher bar.

---

## Files created or updated

- `agents/Claude/Tier A Host and Injection Zone Selection.md` — **Draft 23**, SHA-256 `e7dcfc54f495c96f62c4994cfa8178882edaba38aa0b48a15c3fcb107534b5bf`. §16.4 definition, two new paragraphs, the F3 sentence, the masking paragraph, the gating-quantity paragraph, §16.7's parameter table, §16.8's status narrative, and the header status stack. §1–§15 untouched.
- `Reproducibility Packet/scripts/utils/band_drift.py` — SHA-256 `4ac9fa56dc7a2035d1f9b037b9010ae448fc1c621f92ea93876db1c1fc06ab19`. `window_bins` 10 → 11, symbol renamed, docstring records both aliasing mechanisms and the within-bin boundary.
- `agents/Claude/tools/test_band_drift.py` — SHA-256 `e2e63a037ee81886b01779535c22ce296502bc3a132ee3f77f9ad6f345869420`. New `case_gate_window_covers_the_segment` (nine checks), F2's counterexample and seed sweep, two lengthened fixtures, one withdrawn check. **96 checks, 0 failed.**
- `Playbooks/review-cycle.md` — the convergence consensus, the checklist, the precedence note, the failure-modes list.
- `Review Cards/README.md` — outcome list, `Supersedes:` field, Convergence Decision section, index row.
- `Review Cards/RC-001 Tier A Selection Section 16.md` — Round-2 candidate table, round log, status, acceptance test 1, follow-up entry, outcome list.
- `chats/Claude-Codex/Tier A Selection Section 16 Review/Tier A Selection Section 16 Review - Active.md` — Round-2 owner response appended (append verified by reading the file back and comparing the prior prefix byte for byte).
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — acceptance and method feedback appended, same verification.
- `README.md` — one running-log entry.
- `agents/Claude/Session Summaries/HumanReport25.md` — this report.
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — closeout.

---

## Cross-review

Read Codex's `HumanReport24.md` and his Round-1 ledger in full, ran his `probe_draft16_safety_claims.py` rather than reading its recorded output, and responded to every finding substantively in the review chat. No problem was found in his work: F1 and F2 are both correct and F3 is correctly classified. His Round 1 is the first full-artifact pass under the new method and it behaved as the method intends — one numbered ledger, no stopping at the first blocker.

---

## Machine state, measured

**2026-08-14 23:10 PDT: RAM 7.57 GiB free of 31.67 (76% in use); VRAM 1,082 MiB used of 16,311; 591.6 GB free on `C:`.** Taken fresh at session start, not inherited. Nothing heavy ran: the whole session's compute is the 48-second harness and a few short probes, all numpy and stdlib.

---

## Next steps

1. **Codex runs RC-001 Round 2, delta-only** — F1, F2, F3 and regressions introduced by this response. The place I flagged for him is the §16.4 paragraph pair about what the gate guarantees, since my repair made several unchanged sentences false and the delta rule puts those in scope.
2. **If Round 2 closes as Approved, the archive-reading CLI is the next piece of work** and gets its own Review Card. It is written but not run; it becomes packet step 11 only once executed.
3. **Codex may strike either of my two additions** to the convergence section. Nothing depends on them.
4. **Round 3 is the limit.** If Round 2 does not close it, the next stop is the Convergence Decision the two of us just agreed, not Randy.
5. Still open and unchanged: the capacity/ten-placement gate under Amendment 6, the five packet steps not yet re-run, the preprocessing half of the amplitude question, and the 66 unmapped host long names.

**Nothing in this session is waiting on Randy.**
