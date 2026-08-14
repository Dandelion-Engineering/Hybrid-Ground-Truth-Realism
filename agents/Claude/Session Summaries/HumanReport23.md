# Human Report 23 — Claude

**Date and time:** 2026-08-14 07:23 PDT
**Phase:** 2 — Execution
**Session type:** Owner re-review of Codex's Draft 19 and its two implementation states

---

## Summary

Codex handed back three states at the end of his Session 22: host-selection Draft 19, the band-drift utility, and my synthetic harness. I verified all three digests before opening any of them, re-read §§15–16 whole, read his `HumanReport22.md`, and re-ran every piece of shipped validation rather than reading his reported numbers.

**Both of his blocking corrections are accepted in full and kept exactly as written.** His audit-scope defect is real, and it is a mistake I had made twice in the same shape: Draft 18 checked that the per-unit values recover movement the across-unit *median* suppresses, and never asked what happens when that suppressed band then chooses the window the audit is evaluated inside. A flat band trace has no informative argmax, so an audit aligned to it inherits an arbitrary choice. His compatibility correction is also right: Draft 18's "no existing return value changed" was literally false while its vocabulary repair was correct, and the narrower claim he substituted is the accurate one.

**I could not approve Draft 19 unchanged. One finding, and it follows from his repair rather than objecting to it: the per-unit values it requires arrived with no rule for reading them, and both readings a reader would reach for are wrong.** That is now repaired in Draft 20, with both counterexamples measured and both made permanent harness cases. The harness stands at **77 checks, 0 failed**.

**No host is pinned. No candidate drift, noise or effective-SNR value exists. No target manifest, donor selection, dependency installation, archive or raw-data read, Rung 0, generator or sorter run occurred. No scientific result exists.**

---

## Work completed

### 1. Startup, in the order the framework asks for

- Read `.agent-turn` (named Claude), confirmed `.agent-session.lock` was absent, created it, re-read `.agent-turn` — still Claude.
- Read `AgentPrompt.md` and all of `Project Details/Project Details.md`.
- Read my `Summary of Only Necessary Context.md`, then the active chat's most recent turns before acting on anything that file said — which is the rule I wrote for myself after Codex twice posted a handoff inside the hour after a session closed. It had happened again: his Session 22 handoff landed at 06:14 PDT, after my continuity file was written at 05:30.
- Verified the Claim Sheet and Accessible Claim Sheet are unchanged at their recorded whole-file digests.

### 2. Exact-state verification before opening anything

All three handed-off states matched their claimed SHA-256 digests before I read them:

- Draft 19 — `66621494f7aca105cbfd53fd9b170377e2ce6eca911d73547c97d36b95d47890`
- `band_drift.py` — `28154cfff9b8c6b5aaa082de699650b3b11bec3804c155b0886f705bbb3f2c75`
- `test_band_drift.py` — `ff852682ecee5abb45a1419908a114566488bdafdb2094521fdb664baf853a70`

Then I re-ran rather than read: **71 checks with 0 failed** at the pinned 200 permutations, **3 of 3** independent claim probes, **10 of 10** runbook steps, and Codex's own review probe, whose two counterexamples reproduce to the digit against the Draft 19 module.

### 3. The finding: the per-unit audit values had no rule for reading them

Draft 19 requires the archive reader to publish, for every included unit at the injection site, three centred excursions — the whole recording, that unit's own worst ten-bin window, and its excursion inside the band's gating window. That requirement is right and I agree with it. What it did not carry is any statement of what those numbers may be compared against, and §16 publishes exactly two micrometre-scale numbers: `Q95_null`, the permutation null's 95th percentile, and `L`, the gate threshold. A reader holding a per-unit report has both and nothing else.

**Both are the wrong yardstick, and I measured it rather than arguing it.** `Q95_null` is the noise floor of `D(b)`, which is a median *across* units; a single unit's trace has no such suppression. Using the harness's own fixture generator with no movement at all in the recording:

| units | band `Q95_null` | smallest per-unit own-worst excursion | per-unit values above `Q95_null` |
|---:|---:|---:|---:|
| 9 | 2.676 µm | 4.334 µm (1.62×) | 9 of 9 |
| 14 | 2.036 µm | 4.334 µm (2.13×) | 14 of 14 |
| 25 | 1.531 µm | 4.219 µm (2.76×) | 25 of 25 |

Every per-unit value exceeds the band's null on a recording that does not move, and the margin widens with the unit count because that is precisely what the across-unit median is doing. The pinned candidates carry 22 to 267 band units. So the natural reading reports pure depth-estimation noise as suppressed movement, and it does so most confidently on the quietest hosts.

**The obvious repair was also wrong, and I found that out before writing it.** Codex's localized fixture has its five moving units concentrating their own-worst windows in the same late window while the six flat units sit at bin 0 — which invites the rule "starts clustered together means real common movement; starts scattered means noise." I constructed the opposite case first: a genuine common 30 µm ramp running through the whole session **scatters** the per-unit worst windows over **12 distinct starting bins out of 14**, because a near-linear trajectory leaves many windows nearly tied. Had I not checked, I would have shipped a directional rule with the quieter case unexamined — the identical shape to the two claims Codex blocked in Session 21, three sessions after learning it.

**Draft 20 therefore states what these values do and do not support:** no comparison against `Q95_null` or `L`; the failure shape presenting as a subset separated in magnitude from the rest of that same set whose own-worst windows overlap; neither the concentration nor the scatter of the starts being evidence on its own; and the whole thing named explicitly as a reading rule for the published limitation, carrying no threshold, no verdict, and no effect on the pinned order.

### 4. Two smaller repairs found in the same pass

**A stated justification naming a case the code cannot produce.** Draft 19 said the defined-bin counts exist "so a zero based on one observed level is not confused with a supported flat trace" — but the implementation returns `None`, not zero, below two defined levels. What the count actually adds is the difference between a range resting on two levels and one resting on ten, and Draft 20 says that.

**Two reported values produced by an undeclared tie-break.** `excursions` and `unit_excursions` both take the earliest maximum when windows tie; `window_start` and `unit_max_window_start` are both published; and §16 mentioned the earliest-tie behaviour only in passing, as the thing that motivates the own-worst view. A reader re-deriving either start needs the rule, so Draft 20 declares it and the harness pins it on a constructed tie.

### 5. What changed in the implementation, and the check that it changed nothing else

Draft 20's two edits to `band_drift.py` are documentation only: the module docstring's claim that the first two per-unit views "expose" suppressed movement is narrowed to what they actually do — they carry it, together with that unit's own noise, and have no null — and `unit_excursions` gains the no-null note and the tie-break.

**That is checked rather than asserted.** The Draft 19 and Draft 20 modules are identical once every docstring is stripped from both syntax trees, which is a stronger statement than reading the diff. The three claim probes and Codex's review probe both reproduce unchanged, the runbook checker stays at ten steps, every packet source compiles, and `git diff --check` is clean.

### 6. Harness additions

`case_per_unit_audit_has_no_null` is new and permanent: the no-movement fixtures at 9, 14 and 25 units, the assertion that the margin widens with unit count, the shared-ramp counterexample to the start-scatter reading, and a constructed tie that pins the earliest-window rule. Harness at **77 checks, 0 failed**, 34 s wall clock at the pinned 200 permutations.

### 7. Handoff

Appended to `chats/Claude-Codex/Tier A Selection Review/` at 07:17 PDT, approving three exact states for same-state confirmation:

- Draft 20 — `e2cbcd60dd4d13218ad414a4b46e9ef773ee4e4f0b0b596a233e5309f5ebfeb5`
- `band_drift.py` — `228f045c5c94d31cf9faa4ba3fd9391c62a42192a45f23d2842c256414690a47`
- `test_band_drift.py` — `77637e10f0435bfa3d72a97264e15063f9c4afa6b791bd0d678bc4fd5f5560cd`

The append was verified by reading the file back and confirming the prior bytes are an exact prefix.

---

## Challenges, and how they were handled

**The one that mattered was resisting my own first repair.** The finding arrived as "these values need a reading rule," and the rule that suggested itself — cluster of starts means movement — came with a ready-made illustration in Codex's own fixture. Writing it would have felt like closing the loop. The reason I did not is a rule already in my continuity file from Session 22: before writing a one-way claim about the estimator, construct the opposite case and run it. The opposite case took four minutes and falsified it. That rule has now paid for itself twice, and the second time it was defending against me rather than catching me after the fact.

**Round-trip count.** §16 has now taken eight review turns. Every one has produced a new finding rather than repeating a disagreement, so the playbook's two-round-trip escalation still does not apply. But I said in the handoff where I think the end is: I see nothing left open in §16 that is not now measured by a fixture, and if what comes back next is a disagreement rather than a finding, I would rather escalate than take a ninth turn.

---

## Decisions I made this session

1. **Accept both of Codex's corrections unchanged**, including keeping his narrower compatibility wording rather than re-deriving my own.
2. **Repair by stating an interpretation rule rather than by adding machinery.** A per-unit permutation null would make the values comparable to something — and would also turn a report-only diagnostic into a second estimator with its own parameters, which §16.4 pins these values *against* becoming. The cheaper honest move is to say what the numbers cannot support.
3. **Leave Draft 19's four curly quotes where they are.** They sit in a status line that is now the superseded-status line; reopening approved bytes for punctuation is not worth a state change. I recorded the count in the handoff so it is on the record rather than discovered later, and my own header uses straight quotes.
4. **Add a running-log entry to the public README.** The log has carried an entry for each substantive turn on this thread, and "the audit could be read exactly backwards" is that kind of turn. The banner date was already 2026-08-14 and needed no change.

---

## Files created or updated

| Path | What changed |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 20. §16.4 gains the reading rule for the per-unit values, the corrected defined-count justification and the declared tie-break; §16.8 records Draft 20 and the new approved digests; the status header is rewritten and Draft 19's is preserved beneath it. |
| `Reproducibility Packet/scripts/utils/band_drift.py` | Two docstrings narrowed — module overview and `unit_excursions`. No executable line changed, verified by stripped-docstring syntax-tree comparison. |
| `agents/Claude/tools/test_band_drift.py` | New permanent case `case_per_unit_audit_has_no_null`; module docstring gains the fifth defect-derived bullet. 71 → 77 checks. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Session 23 handoff appended. |
| `README.md` (repository root) | One running-log entry. Banner unchanged. |
| `agents/Claude/README.md` | Current-state lines advanced from Draft 18 to Draft 20 and to the new implementation digests; check count 65 → 77; the fifth harness case described. |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten for Session 24. |
| `agents/Claude/Session Summaries/HumanReport23.md` | This report. |

Nothing was added to `references.md`: this session consumed no new external source.

---

## Machine state

Measured at **2026-08-14 07:06 PDT, immediately before running anything**: RAM **6.34 GiB free of 31.67**; VRAM **1,034 MiB used of 16,311**; **582.6 GB free on `C:`**.

Nothing heavy ran. The harness operates on small synthetic arrays and takes 34 s wall clock at 200 permutations; the scratch probes are of the same size. For the record of how much the machine moves between sessions, my Session 22 reading two hours earlier was 1.67 GiB free — the reason the rule says to measure immediately before, never to inherit.

---

## Next steps

1. **Codex re-reviews the three Draft 20 states.** Everything open is open on him; nothing is open on me.
2. **If Draft 20 comes back approved, I write the archive-reading CLI** — targeted range reads over the ragged `spike_times` and `spike_distances_from_probe_tip_um` slices for band units only, reusing `remote_hdf5` and `host_anatomy` and calling into `band_drift`, with the four §16.8 confirmations run before it computes anything, and reporting the per-unit values from the estimator's own functions rather than from a second centring. It becomes packet step 11 only once it has actually executed.
3. **Then, and only then, rank 1 is measured** against the drift gate.
4. **Still not discharged:** the joint ten-placement capacity gate under Amendment 6's stricter condition, which waits on Codex's footprint/placement calibration and on `N`.
