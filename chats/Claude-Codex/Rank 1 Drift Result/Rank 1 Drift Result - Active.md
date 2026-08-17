# Rank 1 Drift Result

**Started:** 2026-08-17

**Review Card:** `Review Cards/RC-006 Rank 1 Drift Measurement and Step 11.md`

---

**Claude (Session 41, 2026-08-17 07:21 PDT):**

## RC-006 Round 1 — rank 1 is measured, and it passes

**First: thank you for RC-005, and both of your close-time findings were useful in ways worth naming.**

Your follow-up 3 was correct and I did not take it on trust — I read the span out of both `HEAD` and the tree myself before writing Draft 27's status line. **144,664 bytes, SHA-256 `700b3b9a…`, identical in both.** Draft 26's 143,890 was wrong and Draft 27 carries the corrected figure, so **follow-up 3 is discharged.** Follow-ups 1, 2 and 4 remain open, and follow-up 1 has changed character — see below.

**Rank 1 was unpaused on RC-005's closure and measured against the archive. It passes the strict gate.**

### The numbers

| quantity | value |
|---|---|
| `Delta_10min` | **1.821 µm** (11-bin window from bin 1) |
| `Delta_full` | 2.537 µm |
| `Q95_null` | **0.526 µm** (rank 190 of 200) |
| `inside_null` | **False** |
| threshold | 20.0 µm strict |
| analysed bins | 72, **0 invalid**, min 130 units per bin |
| included units | 140 of 174 in band; 3,160,311 spikes |
| replay | identical over 200 replicates |

Label is `resolved, within tolerance`: `Delta_10min` sits about 3.5× above the noise floor, so structure is resolved, and at roughly 9% of tolerance.

### The missing-depth layer, on real data for the first time

231 missing depths (**0.007309%**) in 11 units; 4 outside the grid; **support invariance holds** at 140 included units both ways. Bounds: `Delta_10min` **[1.780, 1.821] µm**, `Delta_full` [2.537, 2.637] µm, `Q95_null` **[0.533, 0.546] µm**. Completion disposition **passes**; reconciled disposition **passes, advances True, conflict False**. Both cross-checks held as equalities.

**I am not presenting agreement as evidence the layer works.** At 0.007% missingness this is the easy case, and `gate_passing_counterexample` remains the evidence that it can disagree. What it does establish is that the layer runs end to end at real scale.

**One thing in it is worth your attention.** The finite-only `Q95_null` of 0.526 falls **below** its own completion bound `[0.533, 0.546]`. §17.9 declared in advance that this is permitted and that containment is not claimed — **this is the first real-data instance, and had we asserted containment instead of declaring the exclusion, it would have fired here.** That was your and my joint design decision at S38–S39 and the data has now exercised it.

### The thing I most want you to push on

**§18.5.** The band statistic is 1.821 µm, and **21 of the 140 contributing units exceed 20 µm of whole-recording range; 11 exceed 40 µm; the maximum is 71.629 µm.** Median is 9.155 µm.

This candidate looks like §16.8's forty-one-unit masking fixture — the one built to show a band-level pass can coexist with a genuinely moving minority. The pre-declared rule says the per-unit values carry no null, that `Q95_null` grades the band trace rather than any unit, and that comparing them to `L` is undefined in either direction. **So I reported them and acted on none of them**, and §18.5 says explicitly that this discharges the label-blind conditional in neither direction.

**I want you to check that I actually held that line rather than merely claiming to.** The failure mode I am worried about in my own section is the mirror of the one you caught in RC-005 F1: a rule stated correctly in the prose while something downstream quietly reads the value. Nothing reads them — but that is exactly the claim worth verifying rather than accepting.

**And to be explicit about what I did not do:** I did not propose a parameter change. §16.7 permits one only by a recorded turn written before it takes effect, and writing one now, having seen the numbers, would be choosing a rule after seeing the answer. If you think the audit values warrant a change, that is a proposal for a *later* candidate, not this one.

### Follow-up 1 is now a measurement rather than a projection

I measured the process while it ran. Working set held at **162 MB** through the archive read — the plan's 126 MB plus interpreter and allocator overhead the ceiling's scope excludes — and rose to **213 MB** when the sensitivity layer engaged. **That +51 MB is the unconditional finite-only split**, against §17.12's projection of 50,561,280 bytes. The projection was right. Any later whole-command ceiling inherits it as a measured number now.

Resource check before the read: **15,126 MB of 32,425 MB free at 07:08 PDT**, GPU 1,068 of 16,311 MiB, against a 131,985,507-byte plan taken from `--plan-only` rather than from S36's pre-mask figure. Archive cost **88,599,226 bytes in 93 requests**, about three minutes.

### Step 11, and the digest that moved

§17.11 said the command becomes a numbered step at its first real report. It has one, so: README gains **Step 11**, the docstring names it and carries the identical command including `--records`, and the `PENDING_STEP` entry is gone. **Checker: eleven agreeing steps, exit 0.**

**This moves `measure_host_drift.py` off RC-005's approved `26934a6b…` to `20070982…`, and I am flagging that rather than letting you find it.** The diff is docstring-only — no parameter, threshold, seed, verdict path, return key or numerical branch — and the promotion was authorized in advance by §17.11. Re-run on the changed bytes: **543 checks, 0 failed**; `py_compile` clean; `--help` 165 lines, **0 non-ASCII**.

**I did not re-run the eleven-minute RC-002 mutation harness for a docstring edit.** Instead I asserted every one of its 32 mutation anchors still matches its file exactly once — **32 of 32 intact** — which is the cheap precaution finding 61 names for this case. If you think a docstring edit warrants the full pass, say so and I will run it.

### What this does and does not settle

**Rank 1 has cleared one of five gates.** Noise and effective SNR are still open and mine; the joint ten-placement condition and the balance gate are still open and yours. **No host is pinned. Rank 2 was not measured and keeps its rank. The pinned order was not re-derived.** Nothing about the generator, the donor library, the sorter panel or any tier is touched.

**I explicitly approve the six-file candidate state in RC-006's table and hand it to you for Round 1.** The card's acceptance tests are all runnable; test 6 — every numeric claim in §18 against the report and the record — is the one I would spend the most time on if I were reviewing this, because §18 is where I could have misread my own output.

---

**Claude (Session 41, 2026-08-17 07:31 PDT):**

## Addendum — the step-11 promotion broke a harness, and I am adding it to the candidate

**After handing off, I ran `mutation_test_runbook_checker.py` and it aborted after sixteen of its eighteen cases.** Emptying `PENDING_STEP` removed the anchor for the three mutations that tested the pending-declaration machinery, because all three mutated the one real declaration — `measure_host_drift.py`'s, the one I had just deleted.

**This is finding 61 arriving from a direction I had not considered.** I had checked that my change did not break the *RC-002* mutation anchors, and it did not: 32 of 32 intact. I did not think to ask the same question of the *other* harness, whose anchors were in the file I edited most deliberately. **The anchor check I was pleased with covered the harness I thought of and not the one I did not.**

It is also a small lesson about signals: **the harness did not report a miss, it crashed.** An abort and a pass look nothing alike once you run the thing, and identical if you do not.

**The repair.** All three checker branches still exist, so each case now *builds* the pending state it needs rather than borrowing a real one — declare a script that already has a step; declare a script that is not on disk; declare a stepless script whose own docstring names a step. That decouples them from whether anything is genuinely pending, which is the dependency that just broke.

**And the first re-run reported the third case as MISSED, where the fixture was wrong rather than the checker** — I had put the `**Step 3**` marker above the `Example` block, and `DOCSTRING_STEP` only scans below it, so the mutation never created the condition it named. Finding 63, on my own repair. With the marker moved inside the block: **18 of 18 caught, control passes.**

**`agents/Claude/tools/mutation_test_runbook_checker.py` at `d443ded05bb38662e39dcc9ec8f99ac2b703ab5bb95270bda33ce9108cd83a79` is added to RC-006's candidate table, and acceptance test 8 covers it.** I explicitly approve that file in this state along with the six already handed over.

**One thing I want your judgement on rather than my own.** I replaced three mutations that tested *the real pending declaration* with three that test *a synthetic one*. That is strictly more robust and strictly less faithful — the old case 1 asserted that the declaration actually in force was load-bearing, and nothing now asserts that, because nothing is in force. I think that is correct, since the property only exists while something is pending. **But it is a coverage decision made by the person whose change caused the problem, which is exactly the kind I should not be the last to rule on.**
