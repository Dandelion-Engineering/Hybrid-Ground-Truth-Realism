# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 41 · 2026-08-17 07:26 PDT**
**Next session is Claude Session 42. No count-based progress report is due** (they fall at 8, 16, 24, 32, 40, **48**). A phase transition or an approved amendment would still trigger one.

## 0. WHAT THIS SESSION DID, IN ONE PARAGRAPH

**RC-005 closed `Approved with Follow-Ups`, which unpaused ranks 1 and 2, and Session 41 made the project's first real measurement.** Rank 1 (CSHL047 Probe01) was read from the archive and **passes the strict drift gate**: `Delta_10min` **1.821 µm**, `Q95_null` **0.526 µm**, threshold 20 µm, 72 analysed bins with 0 invalid, 140 included units of 174, 3,160,311 spikes, replay identical over 200 replicates. **The missing-depth layer engaged for the first time on real data** — 231 missing depths (0.007309%) in 11 units — support invariance held, and the completion bounds **[1.780, 1.821] µm** and **[0.533, 0.546] µm** made the reconciled disposition **passes, advances True, conflict False**. `measure_host_drift.py` became **runbook step 11**. **No host is pinned: rank 1 cleared one of five gates.** §18 and the promotion are open on Codex as **RC-006**.

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

## 1. Where the project is

**Phase 2 — Execution. One gate of five is discharged for one candidate. No host is pinned, no donor is selected, no generator has run, no sorter has run, and the project's actual question is untouched.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 27, `646def951178f76ca2397c34dc46a2b2f0f96c3d77d6658825335aede71b82c3`. §18 IS IN RC-006's SCOPE. §1–§16 byte-identical: 144,664 bytes from `## 1. ` to `## 17. `, SHA-256 `700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59`, proved against `HEAD`. §17 closed with RC-005. Do not reopen §1–§17.** |
| **`Reproducibility Packet/results/host_drift_CSHL047_Probe01.txt`** | **NEW. `a2d325088b384f8010a1e398fd58ec759981269e83cb166b7082c3f76ad0cbef` — the first measurement.** |
| **`…/host_drift_CSHL047_Probe01.json`** | **NEW. `2e125d419eb8ad31ad7824f47dd324b8ed0d54d8230095eb29618436b3c87bd5`.** |
| **`Reproducibility Packet/scripts/measure_host_drift.py`** | **`200709824fb3a5694b12243eb65647d038d1d251df9abfe49a3e90ca3b8bad47` — MOVED off RC-005's `26934a6b…` on a DOCSTRING-ONLY edit authorized by §17.11.** |
| **`Reproducibility Packet/scripts/check_runbook_consistency.py`** | **`35cea57d67be5e299c036f39312ad821fe193fc3d2cc4d7e1fe6480e04b4ccdb` — `PENDING_STEP` now empty.** |
| **`Reproducibility Packet/README.md`** | **`806aefaf9859cc0f391101f205b6e055f9278d5d95ef4d759711ded8762cfaf3` — ELEVEN steps, nothing pending.** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **`eace4cd3…` — approved, closed, untouched.** |
| `Reproducibility Packet/scripts/utils/archive_units.py` | **`ed0766f2…` — unchanged from RC-005.** |
| `Reproducibility Packet/scripts/utils/missing_depth.py` | **`ef974027…` — unchanged from RC-005.** |
| `agents/Claude/tools/test_measure_host_drift.py` | `79c9bb5c…` — **543 checks, 0 failed, re-run S41 on the changed bytes.** |
| `agents/Claude/tools/test_missing_depth.py` | `435272af…` — 86 checks. Not re-run S41. |
| `agents/Claude/tools/test_band_drift.py` | `946df906…` — 103 checks. Not re-run S41. |
| `agents/Claude/tools/verify_rc005_round2_repairs.py` | `4f27b70c…` — 4 of 4. Not re-run S41. |
| **`agents/Claude/tools/mutation_test_runbook_checker.py`** | **`d443ded05bb38662e39dcc9ec8f99ac2b703ab5bb95270bda33ce9108cd83a79` — CHANGED S41; 18 of 18, control passes.** |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `97860ad9…` — **not re-run S41; all 32 anchors asserted intact instead.** |
| Root `README.md` | **76 dated log entries**, banner at 2026-08-17. |
| `Review Cards/RC-005 …` | **Closed `Approved with Follow-Ups`, Round 2, 2026-08-17.** |
| **`Review Cards/RC-006 …`** | **OPEN, Round 1 handed to Codex 07:20 PDT.** |

## 2. The first thing to do next session

**Read `chats/Claude-Codex/Rank 1 Drift Result/` before anything else.** My RC-006 Round-1 handoff is the last message.

- **`chats/Claude-Codex/Rank 1 Drift Result/` — active, on Codex.** RC-006 Round 1, a full pass over §18 and the step-11 promotion.
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active** by Randy's request. Nothing pending.
- **All thirteen other chats are concluded**, including `Missing Depth Recovery Review`, whose `Summary.md` is RC-005's record.

**What can be done next, in order of readiness:**

1. **Rank 2 (NYU-12 Probe01) can be measured** — unpaused, unmeasured, and the command is unchanged in behaviour. **But consider waiting for RC-006.** Measuring rank 2 before Codex has reviewed *how I reported rank 1* risks committing the same reporting error twice. That is a judgement call, not a rule.
2. **The noise gate and the effective-SNR gate are next in my lane** and **neither is specified yet.** They are §15.5's gates 2 and 3 and there is no §-level specification for either. Writing one is real work and should follow §16's shape: define the quantity and its parameters *before* any candidate is read.
3. **If Codex returns `Revisions Required`**, repair on one state and re-run the anchor check plus the 543-check suite.

**⚠️ Rank 1's command, verbatim, from inside the packet folder — this is now runbook step 11:**

`python scripts/measure_host_drift.py --session b52182e7-39f6-4914-9717-136db589706e --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

Add `--plan-only` for the sizing pass. **Measure free RAM against `peak_resident_bytes`, not `resident_bytes`, and take the figure from `--plan-only` rather than from any number written down.** About three minutes, 88.6 MB, 93 requests; `run_in_background`.

## 3. THE RESULT — rank 1, measured 2026-08-17

| quantity | value |
|---|---|
| `Delta_10min` | **1.821 µm** (11-bin window from bin 1) |
| `Delta_full` | 2.537 µm |
| `Q95_null` | **0.526 µm** (nearest-rank, rank 190 of 200) |
| null range | 0.281–0.761 µm |
| `inside_null` | **False** |
| threshold | 20.0 µm strict |
| bins | 72, **0 invalid**, min 130 units per bin |
| units | 140 included of 174 in band (18 `good`) |
| spikes | 3,160,311 |
| replay | identical over 200 replicates |
| **verdict** | **passed True, `resolved, within tolerance`** |

**Missing-depth layer:** 231 missing (0.007309%) in 11 units; 4 outside grid; **support invariance holds** (140 both ways); `Delta_10min` bound **[1.780, 1.821]**; `Delta_full` [2.537, 2.637]; `Q95_null` bound **[0.533, 0.546]**; **disposition `passes`, advances True, conflict False.**

**Three things about this result that must not be lost:**

1. **`inside_null` is False and `Delta_10min` is ~3.5× `Q95_null`.** Structure is *resolved above the noise floor*, and it is small — about 9% of tolerance. Both halves are the measurement.
2. **The finite-only `Q95_null` (0.526) falls BELOW its own completion bound [0.533, 0.546].** §17.9 declared this permitted in advance and does not claim containment. **This is the first real-data instance, and an asserted containment check would have fired here.** Do not "fix" it.
3. **⚠️ THE PER-UNIT AUDIT IS LOUD AND THE RULE FORBIDS CONSUMING IT.** Whole-recording ranges over the 140 included units: min 1.259, median 9.155, p90 27.146, **max 71.629 µm; 21 exceed 20 µm, 11 exceed 40 µm.** Band-window: median 5.881, 14 above 20, 4 above 40. **This is §16.8's masking-fixture configuration appearing in real data.** The pre-declared rule: per-unit values carry no null, `Q95_null` grades the band trace not any unit, comparison to `L` is undefined **in either direction**. §18.5 reports them and acts on none. **Do not propose a parameter change on the strength of them — §16.7 permits one only by a recorded turn written BEFORE it takes effect, and writing one now is choosing a rule after seeing the answer.**

**Agreement between gate and layer is NOT evidence the layer works.** At 0.007% missingness this is the easy case. The evidence it can disagree is still the synthetic `gate_passing_counterexample`.

## 4. What changed in the packet, and the one digest that moved

**Step 11 exists.** README gains it, the docstring names `**Step 11**` (the *literal* string — the checker's regex needs it) and carries the identical command **including `--records`**, and `PENDING_STEP` is now `{}`. Checker: **eleven agreeing steps, exit 0**.

**`measure_host_drift.py` is off its approved digest.** Docstring only; `git diff` shows no line outside it. Re-run on the changed bytes: **543 checks 0 failed**, `py_compile` clean, `--help` **165 lines 0 non-ASCII**. **The RC-002 mutation harness was NOT re-run** — instead **all 32 anchors were asserted to match their files exactly once (32/32)**, which is finding 61's cheap precaution. Codex may ask for the full pass.

**RC-005 follow-ups:** **3 is discharged** (144,664 verified independently, not inherited). **1 is now a measurement** (§5 below). **2 and 4 remain open** — 2 is the `resident_bytes` "converted arrays" label that should name the stored-width slice; 4 is the same wording issue in the refusal text.

## 5. Machine state and measured costs

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`).

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; never inherit a number, including from this file.

**Session 41 readings: 07:07 — 15,145 MB of 32,425 available, GPU 1,068 of 16,311 MiB. Immediately pre-read 07:08 — 15,126 MB. At close 07:21 — 14,847 MB, GPU 1,067 MiB.**

**⚠️ NEW — the command's real footprint, measured while it ran.** Working set **162 MB** through the archive read (the plan's 126 MB plus interpreter and allocator overhead the ceiling's scope excludes), rising to **213 MB** when the sensitivity layer engaged. **That +51 MB is RC-005 tracked follow-up 1** — the unconditional finite-only split — against §17.12's projection of **50,561,280 bytes**. **The projection was right and is now a measurement. Any whole-command ceiling claim inherits it as one.**

**The rank-1 `--plan-only` bound is 131,985,507 bytes** (55,120,439 arrays incl. 3,160,311 mask bytes + 1,047,116 structures + 16,777,216 hdf5 cache). **Do not reuse S36's 128,825,196 — it predates the mask term.**

**Suite costs:** `test_measure_host_drift.py` **18.3 s**; `test_missing_depth.py` ~15 s at 200/200; `test_band_drift.py` ~48 s; `verify_rc005_round2_repairs.py` ~1.7 min; RC-002 mutation harness **~11 min**. **The rank-1 measurement: ~3 min, 88,599,226 bytes, 93 requests.** Take your own readings.

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the root `requirements.txt` **and the packet's own**. **Nothing installed S41.** SpikeInterface, PyTorch and Kilosort4 **still not installed** — Codex's Rung 0, and the numpy pin may have to move (change **both** files). **The pinned permutation stream is `numpy.random.PCG64`; a numpy change is a replay risk.** Use `./venv/Scripts/python.exe`; never bare `python`/`pip`.

## 6. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity · **drift, for rank 1 only**. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **noise · post-rescaling effective SNR — NEITHER IS SPECIFIED YET.**
Gates **open and Codex's**: joint ten-placement (Amendment 6 point 1) · the balance/manipulation gate.

### 6.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) — **DRIFT PASSED** · 2. NYU-12 **Probe01** `a8a8af78` (66) — **unpaused, unmeasured** · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`. Rank 1 is `b52182e7-39f6-4914-9717-136db589706e`.**

**Do not re-derive the order and do not re-sort it.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in pinned asset-cache order at 40 µm. **Gate order** (cheapest first): drift → noise → effective SNR → joint ten-placement → balance.

**⚠️ Four ranks — 5, 7, 9, 13 (NYU-65, NYU-45, NYU-39, NYU-48) — remain PAUSED on the declared-clock disagreement, not rejected.** RC-005's closure did not touch them.

**⚠️ First-admissible means rank 1 is only the host if it clears ALL FIVE.** Passing drift orders nothing on its own.

### 6.2 What rank 1's read established

Raw provenance authenticated (`Created using NeuroConv v0.9.2`, 23,488 of 65,536 request bytes, 262,144 of 393,216 transfer bytes); pair condition passes; CA1 band **320.0–1020.0 µm, 72 channels**; AP extent `t_first 1.138489 s`, `t_last 4340.732689 s`; **174 band units of 756; 3,160,311 spikes**; payload 50,564,976 bytes; **231 NaN depths in 11 units; 0 non-finite times** — the S36 census confirmed by a second independent read.

### 6.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Codex owns the footprint/placement calibration**; do not start it.

## 7. What is still not done

1. **No host is pinned**, and that is correct.
2. **Rank 2 has no drift number.** Ranks 3–13 have none either.
3. **The noise and effective-SNR gates have no specification.** This is the largest open piece in my lane.
4. **§18 is written but unapproved.** RC-006 Round 1 is on Codex.
5. **Five of the ten older packet steps still have not been re-run** (the archive-reading ones).
6. **The preprocessing half of the amplitude question is untouched** — Rung 0 territory.
7. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question.
8. **`is_injectable` is a denylist over a partly derived vocabulary.** Latent: no consumer reads it.
9. **`probe_conversion_pairs.py` is not in the packet.** RC-004 tracked follow-up 1, still live, joined by `probe_nonfinite_depths.py` and `probe_missing_depth_crossover.py`, whose numbers §17 cites.
10. **The unconditional finite-only split** — RC-005 tracked follow-up 1, now measured at +51 MB, still unrepaired by choice.

## 8. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **footprint/placement calibration** · **real-arm donor-matching rule** · **exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 9. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`**, `G0` the mean paired sorter gap *in the control arm*. **Bounded-negative is the harder verdict.**
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins.** Inside-null is **not** a failure. **A claim that "the estimator would have caught it" must say *which of the two numbers*.** Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data **except a NaN depth (§17)**, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those pause the pinned order (§16.4).
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** A median tracks rank, so displacing `k` of a bin's `n` spikes upward moves its median **at most the displacement itself and at most the distance to the depth `k` ranks above it**. On a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`. **The gate has no guaranteed resolution below the bin width in either direction.**
- **The drift unit set is blind to `kilosort2_label`** and is selected by valid same-probe `max_electrode -> rel_y` inside the band. **The `mua` association among affected units is recorded and refused.**
- **The per-unit excursions are reported and never consumed.** **Never compare a per-unit value to `Q95_null` or to `L`.** **The absence of magnitude separation is not evidence either — and NOR IS ITS PRESENCE, which rank 1 now demonstrates on real data.**
- **The bin grid anchors at session `t = 0` with extent `t_last_s`**, on pinned converter provenance. **`duration_s` is a span and is not an alternative clock hypothesis.** Endpoint containment cannot identify a clock — **and neither can reference-instant agreement.**
- **The head bin is retained and reported, with no claimed direction.**
- **The permutation pool is analysed-bin spikes only**, for both observation and null.
- **`cumulative_drift_um_per_hour` is retired on its own description.**
- **Amendment 6 governs: Tier A is parameterized by `N`.** `10 ≤ N ≤ 16` continues; `N < 10` is Slot 12.3. Fifty occurrences split `q = ⌊50/N⌋`, `r = 50 mod N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.**
- **`N ≥ 10` is structural:** `16 − 6 = 10` = the injected-unit count Slot 7 fixes.
- **The manipulation check is a hard stop-or-go gate**, and the realized zone-donor count is a *composition-integrity* quantity, **not** a substitute for it.
- **Amendment 5:** the injection zone's donors are removed from the **real** region-unaware arm before matching. The frozen matching rule runs as a non-generating counterfactual on **both** pools, with only the post-removal state permitted to govern generation.
- **The matching rule's provenance test is two-level:** **Level A** matches distinct dataset, session *and* subject counts; **Level B** is the contract's literal `S_T` floor. **Level A binds only at stages 3 and 4.**
- **0.11 and 0.12 are two sampling models, not two estimates of one number.** Blocked expectations are **1.03** and **1.17**. **Historical diagnostics at sixteen**, never predictions.
- **CA1's sixteen donors sit in exactly 4 source datasets, `[6, 5, 3, 2]`**, 4 sessions, 4 animals — KS044/KS046/KS051/KS055. Library-wide: **37 insertions, 24 sessions, 12 animals**.
- **The source-count floor binds at *every* relaxation stage** and is an **equality**, both directions.
- **One host and injection zone across all tiers by default**; a deviation is a recorded limitation and the cross-tier comparison is dropped.
- **CA1 is the approved first zone.** Do not commission the `SUB` literature task unless CA1 fails a real gate.
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **The donor library is good-clusters-only by construction.**
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.**
- **Pre-rescaling scale factors are a manipulation-check diagnostic, not a matching covariate.**
- **The Allen CCF ontology is not importable** — noncommercial terms. **No atlas package is installed and that is deliberate.**
- **A one-command-per-side runbook rule is a hard parse error, not a warning.**
- **⚠️ The daylight-saving reading of the 8 disagreeing sessions is DESCRIBED, NOT EXPLAINED. The same discipline applies to the centre-of-mass reading of the NaN depths**, and §17 says so in its own text.
- **NaN is the only missing marker. Both signs of infinity are input errors. A non-finite time is an input error.** The reader returns the complete record plus `missing_depths` and `n_missing_depths`; **the mask travels rather than being re-derived.**
- **`reconcile_verdict`: a candidate advances only when the gate and the completion bound point the same way; any disagreement is `unmeasurable` with `conflict` True.** **Codex explicitly approved this at RC-005 Round 2 — it is no longer merely unobjected.**
- **The console contract:** the command writes the report and record FIRST, then prints exactly two lines — the point gate marked `diagnostic, not the decision`, then the reconciled decision **last, with nothing after it.**
- **`mask_bytes` is a COMPONENT of `resident_bytes`, not a further term.** `peak_resident_bytes = cache_bound + resident + structures + library_cache`.
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count; S27's five; S28's three plus the Round-2 ASCII claim; S29's one, which closed RC-002 unapproved; S30's three; S31's two; S32's own, the pair-equality condition that admitted 0 of 71; S34's two; S36's, that §16.7's support floors are sufficient to make a dropped depth safe; S38's, that no assumption-free bound on `Q95_null` exists; S39's, naming the wrong chat as RC-005's review channel; **and S40's, a memory-ceiling check whose threshold was computed from the quantity it was testing.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 10. The module surfaces

`missing_depth.py`: `median_interval` · `split_unit` · `missing_counts` · `unit_intervals` · `support_invariance` · `centre_bounds` · `centred_intervals` · `trace_intervals` · `interval_excursions` · `measure_missing_depth_sensitivity` · `replicate_bin_bounds` · `null_interval` · `stability_verdict`.

- **Import form is `from utils import band_drift`.** A bare `import band_drift` fails.
- `null_interval` returns `q95_lo` · `q95_hi` · `values_lo` · `values_hi` · `bounded` · `rank` · `n_permutations`. **There is no `q95` key.**
- `measure_missing_depth_sensitivity` **raises** if the point estimate falls outside its own bound.
- **`support_invariance` returns numpy arrays** — `summarize_missing` converts them, which is why it exists.
- **Every entry point takes the COMPLETE per-unit arrays** — every spike's time, and a depth array of the same length with NaN at the missing entries. **`split_unit` is the one place the record is split.**

`measure_host_drift.py`: `reconcile_verdict` · `summarize_missing` · `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`, and no flag controls the sensitivity layer.**

`archive_units.py`: `MASK_ITEMSIZE` · `PROVENANCE_MAX_BYTES = 65536` · `PROVENANCE_BLOCK_BYTES = 65536` · `MEASURED_CONVERSION_VERSIONS = ("0.9.1","0.9.2","0.9.4")`, never gated · `UNITS_PATH = "units"` · `TIME_COLUMN = "spike_times"` · `DEPTH_COLUMN = "spike_distances_from_probe_tip_um"`. Transfer budget **393,216** at the pinned 64 KiB block. **There is no plan key called `bytes`.**

- **`REFERENCE_TIME_FORM` gates the lexical shape before `fromisoformat` parses. ⚠️ THE UTC-OFFSET REQUIREMENT IS DELIBERATELY NOT IN THE GRAMMAR** — two independent enforcers would turn mutation F1L from CAUGHT to MISSED. **Do not "tidy" this.**

`band_drift.py`: `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** Symbol `Delta_10min`. Band keys `delta_full` / `delta_window` / `window_start`; `apply_gate` returns **`passed`**. Others: `bin_seconds` 60, `min_spikes_per_bin` 10, `min_bin_fraction` 0.8, `min_units_per_bin` 5, `n_permutations` 200, `null_percentile` 95, `master_seed` 3175830281, thresholds 20/40 µm.
- **`unit_traces` raises on non-finite depths** — which is *why* the command splits the record first.
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)`, **anchors at 0**. **Rank 2's `t_first_s` is −0.000047 s, so sub-zero exclusion is live.** **A recording needs at least 11 analysed bins**; rank 1 has 72, rank 2 has 82.

### 10.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires on every case reaching a record that `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`. **Do not weaken into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size** (S31). `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4` for that reason.
3. **The provenance-budget invariant** (S32), on both assets, on every case reaching a record.
4. **The fixture axes are separate on purpose** (S34): `write_raw`/`write_processed` take `provenance=` **and** `reference_time=` independently.
5. **`run_case(..., capture=False)`** (S35): with `capture=True` `result["stdout"]` is the transcript; otherwise **None**, not `""`.
6. **`_nan_at(units, positions)`** sets NaN at **stated** positions. **Do not switch it to a random draw.**
7. **`check_console_decision(h, prefix, transcript, disposition, advances)`** is the shared console assertion.
8. **`case_the_ceiling_counts_the_retained_masks`** builds its ceilings from the **fixture's spike count**, never from the plan under test. **Do not "simplify" it** (finding 89).

## 11. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). **S33 and S36 are the sharpest instances.**
2. **Read the column, do not count it** (S5). **S33 inverts it — the thing needed had never been read at all.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30–S33, S36).
4. **A clean trend invites a causal story you have no way to check** (S5, S33, S36). Describe the pattern; do not publish the mechanism.
5. **In an owner re-review, the pull is to accept everything** (S6). Ask: *for each edit, what failure is this pointed at, and does the replacement still point at it?*
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **⚠️ A heredoc through the Bash tool mangles nested quotes AND backslash escapes; a backtick inside a double-quoted Bash string is command substitution; and `%` in a URL-encoded string collides with `%`-formatting (S41). WRITE SUCH SCRIPTS WITH THE WRITE TOOL — S41 lost two round-trips relearning this.** Write with a `__STAMP__` placeholder, substitute the clock at write time, assert the header appears exactly once. **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32).
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32, S36). **⚠️ S41's application: a gate parameter may not be changed after a candidate's value is known — §16.7 requires the recorded turn to precede the change. Seeing a loud per-unit audit is not permission to act on it.**
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7). **Run the probe they hand you, unmodified, before editing — and again after.**
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S33).
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32, S33, S36).
13. **A correction is worth logging even when the conclusion survives** (S8, S29, S37).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9, S15).
16. **An audit must use the same key its lookup uses** (S9, S27, S28, S31).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10).
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17, S23, S28, S29).
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11, S27–S29). **S33: and a *rule* you have not executed against real input is the same guess wearing a test suite.** **⚠️ S41 is the positive instance — step 11 exists only because the command finally ran.**
24. **Note which direction a correction pushes** (S11, S15, S16, S26, S38).
25. **When a test fails, first ask whether the test or the artifact is broken** (S11) — **S37's third possibility, the *expectation*; S39's fourth, the *assertion about the edit*; S40's fifth, the *checker's own string*.**
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S41).
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29, S40).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27, S36).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26, S34). So assert it.
31. **A supersession can be too broad as well as too narrow** (S14). **S39: say which single clause you supersede, not which section.**
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28, S36).
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32, S34–S41). Validate every replacement across every file *before* writing any, and re-assert afterwards. **⚠️ S41: this caught a real defect — the docstring said `**The command above is Step 11**`, so the literal `**Step 11**` the checker's regex needs never appeared, and the step would have been rejected as unnamed.**
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Twenty-four for twenty-four (S15–S41).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32, S33, S35).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.** **S37: a null built by averaging across units cannot bound a perturbation common to those units.**
41. **Read the clock at the moment you write the timestamp** (S17). **`time.strftime("%Z")` returns the long name on Windows: use a literal `PDT`.** **S41: I wrote a card stamp before reading the clock and had to correct it — write the placeholder, then substitute.**
42. **⚠️ A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24, S34, S35, S37, S38). **Check the chat rows every session.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30, S34, S35, S40).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32, S34). **And which *currency* it is denominated in.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26).
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28).
50. **A counterexample built on a degenerate case invites dismissal** (S24, S26, S37, S38).
51. **A near-miss is not the finding** (S24). Sweep the parameters to establish the regime exists.
52. **A test can encode the defect it was written to catch** (S25, S28). **A harness written from the implementation confirms the implementation.**
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25). **⚠️ S41: that moment has now PASSED for the drift gate. Rank 1 is measured.**
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32, S35, S38, S39).
56. **Which fixture a published number came from is part of the number** (S25, S26, S37).
57. **A check that cannot fail is not a check** (S27–S32). **S33: a check that cannot *pass* is not a check either.** **S37: a bound that pauses everything is not a bound.** **S39: a safety layer nobody has seen change an outcome is not evidence it can.** **⚠️ S40 finding 89 is the sharpest instance.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen between them.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). **RC-003, RC-004 and RC-005 then all closed without needing another.**
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair.** **Cheap precaution before spending eleven minutes: assert every mutation's source string still matches its file exactly once** (S39, S40). **⚠️ S41 used the anchor check ALONE on a docstring-only edit — 32 of 32 — and told Codex he may demand the full pass. That judgement is his to overrule.**
62. **Evidence must come from the exact state you publish digests for** (S31, S34, S35, S37, S41).
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32, S34, S40).
64. **When a reviewer's finding is correct, check whether it is *complete*, and whether its *evidence* proves it** (S32, S37, S38). **⚠️ S41's variant: when a reviewer hands you a corrected number, RE-DERIVE IT YOURSELF. Codex's 144,664 was right, and I read it out of `HEAD` and the tree before publishing it.**
65. **An undetermined value is a missing measurement, not a negative one** (S33, S34, S36, S37).
66. **Test a hypothesis on data that did not suggest it** (S33, S36).
67. **⚠️ Do not both discover an input error and rule on its disposition in the same session** (S33, S36). **S37–S40: post the design, including where you deviate, before writing the code.**
68. **Separate the fixture's axes before you need them separate** (S34).
69. **A closed card's evidence script may legitimately go red** (S34). Do not edit its checks to make it green. **S40: do not extend a closed card's harness either — write a new one.**
70. **A note added to a docstring is printed surface** (S34, S40, **S41**). `--help` renders it and this console is cp1252. **S41 changed a docstring and re-captured `--help`: 165 lines, 0 non-ASCII.**
71. **⚠️ BEFORE ADDING A SECOND ENFORCER OF A PROPERTY, ASK WHAT THE MUTATION FOR THAT PROPERTY REVERTS** (S35).
72. **A whole-command test can have its meaning moved by a change elsewhere while staying green** (S35).
73. **The trusted parser is part of the input surface** (S35).
74. **A diagnostic that answers "how bad is it" must also answer "what would the fix cost"** (S36).
75. **When you refuse to use a measured pattern, record it anyway and say why you refused** (S36). **⚠️ S41 is the largest instance: the per-unit audit is loud, the rule forbids consuming it, and §18.5 publishes it beside the pass with the refusal stated.**
76. **⚠️ AN AVERAGING STRUCTURE AND A SYSTEMATIC PERTURBATION SCALE DIFFERENTLY** (S37).
77. **Show the vacuity rather than delivering the vacuous bound** (S37). **⚠️ S38: FIRST PROVE THE VACUITY.**
78. **Where a bound is exact and where it is an outer bound are different claims and both have to be stated** (S37).
79. **⚠️ AN IMPOSSIBILITY ARGUMENT TURNS ON ONE WORD — FIND IT BEFORE YOU PUBLISH THE ARGUMENT** (S38).
80. **⚠️ TESTING A BOUND AGAINST A RESTATEMENT OF ITS OWN DEFINITION TESTS ONLY THAT TWO HALVES OF ONE ARGUMENT AGREE** (S38). **Whenever a test says "computed independently", ask independently *of what*.**
81. **The sharpest containment evidence is a completion landing exactly on an endpoint** (S38). **⚠️ S41: rank 1's `Delta_10min` point estimate LANDS ON the upper endpoint of its own bound, and `Delta_full` on the lower — real data, not a fixture.**
82. **A test that is numerically right because two paths agree is not a test that they agree** (S38).
83. **⚠️ A CONSTANT COMPLETION AT A DISTRIBUTION'S CENTRE IS A DEGENERATE FIXTURE** (S38).
84. **⚠️ A WHOLE-FILE REWRITE OF A TEST SUITE IS A COVERAGE RISK** (S38). `git show HEAD:<path>` recovers the exact prior implementation.
85. **⚠️ A REVIEWER'S INSTRUCTION CAN HAVE TWO PARTS** (S39). **When a handoff names a deliverable, enumerate its parts before starting and check them off at the end.**
86. **⚠️ AN ASSERTION ABOUT AN EDIT CAN FAIL WHILE THE EDIT IS CORRECT** (S39). **Assert `written.count(old) == new.count(old)`, never `== 0`.**
87. **⚠️ CONSUMING A DIAGNOSTIC IS WHERE THE POLICY GETS MADE** (S39). **A layer that only reports has not yet made its hard decision.**
88. **Publish an aggregate and the thing it aggregates, in the same artifact** (S39).
89. **⚠️ S40 — A THRESHOLD COMPUTED FROM THE QUANTITY UNDER TEST MOVES WITH THE DEFECT.** The boundary must come from the fixture — inputs no defect in the code under test can move. **General form: any "just below / just above" test must build its boundary out of inputs, never out of the output it is bounding.**
90. **⚠️ S40 — A POST-WRITE CHECK CAN FAIL ON ITS OWN STRING RATHER THAN ON THE WRITE.** **Build a checker's expected string as a literal, not by transforming another string**, and when a post-write check fails, read the file before touching anything.
91. **S40 — a defect that lives only in the console is invisible to a suite that reads only artifacts.** **When a command's output has two surfaces, the acceptance evidence has to cover both.**
92. **⚠️ S41 — A DESIGN DECISION ARGUED ON FIXTURES GETS EXERCISED BY REAL DATA, AND YOU SHOULD SAY WHEN IT DOES.** The finite-only `Q95_null` fell *below* its own completion bound on the first real candidate. §17.9 declared in advance that containment is not claimed; an asserted containment check would have fired on measurement one. **When real data exercises a boundary you argued abstractly, record that it did — it is the strongest evidence the argument was needed.**
94. **⚠️ S41 — REMOVING A DECLARATION REMOVES THE MUTATIONS THAT TESTED IT.** Emptying `PENDING_STEP` for step 11 stripped the anchor from three mutations, and the harness **aborted after 16 rather than reporting a miss** — an abort and a pass are not the same signal, and only running it distinguished them. **A mutation that borrows real state is coupled to that state; one that builds its own is not.** All three were rewritten to construct their own pending declaration. **And the first re-run reported the replacement as MISSED because the fixture was wrong, not the checker** (finding 63): the step marker sat above the `Example` block and the parser only scans below it.
93. **⚠️ S41 — THE MOMENT A RULE STOPS BEING FREE TO CHANGE IS THE MOMENT ITS FIRST VALUE IS KNOWN.** The per-unit audit on rank 1 is loud enough to invite a rule change, and §16.7 forecloses one. **The discipline is not "resist the temptation" but "recognize which side of the measurement you are on."** Report the tension, refuse to act on it, and say in the artifact that you refused.

## 12. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **RC-001–RC-005 closed; RC-006 open at Round 1.** **A new card gets a new chat** (finding 85).
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below. **Read the top section.**
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry landed inside the log section. **76 dated entries by `grep -c "^- \*\*2026-08-1"`; banner at 2026-08-17.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link.
- **Corrections propagate forward, never backward.** The review cycle is the only exception.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. `ls "C:/Users/cresp/AppData/Local/Temp" | grep -c "drift_reader\|rc002_mutation\|rc005_reversion\|rbchk"` is the check — **0 at S41 close.** **⚠️ Do not edit any file the mutation harness copies while it is running** — `measure_host_drift.py`, `archive_units.py`, `test_measure_host_drift.py`.
- **`test_measure_host_drift.py` takes `--keep` and `--tmp-root`**, which is how to get a real report out of a fixture case. **Delete the kept tree afterwards.**
- **A long archive read belongs in the background.** `tail` the log or arm a Monitor rather than polling. **A `run_in_background` Bash `until` loop is the right shape for a one-shot wait.**
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **total every read rather than the last one.** **A retry re-transfers a block, so `n_bytes` can exceed the file size.** **The reader's cache is unbounded and never evicted.**
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`, `missing_depth`. **`read_series_timing` lives in `screen_host_timing.py`.**
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` needs no step. **A script in `scripts/` without a step is a hard failure unless declared in `PENDING_STEP`**, and a script that is both a step and pending is also a failure. **`PENDING_STEP` is now empty.** **The docstring must contain the LITERAL `**Step N**`** and its Example command must match the README's byte for byte. **After editing the packet runbook or any script docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **`mutation_test_runbook_checker.py` takes three positional arguments**, not flags: packet path, scratch directory, interpreter. **⚠️ S41 emptied `PENDING_STEP` and broke the three mutations that tested it — the harness aborted after 16. All three were re-aimed to BUILD their own pending state rather than mutate a real declaration, and it is back to 18 of 18 with a passing control. Digest `d443ded0…`. Do not re-couple them to a real pending script.**
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. **Check the printed surface by capturing `--help`** — 165 lines at S41, 0 non-ASCII. **Values read out of an asset are not yours** — render them through `archive_units.ascii_safe`.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (199/199 at S41 close, two rows added); the root `README.md`, the packet README, the selection document, the Review Cards and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert the ratio afterwards.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path and comparing file by file, then deleting the clone.
- **Both `.gitignore` files carry a do-not-catch-these comment and ignore `__pycache__/`.** **`Reproducibility Packet/results/` is NOT ignored and the two new drift outputs are tracked.**
- **`agents/Claude/tools/` holds fourteen scripts and thirteen recorded outputs.** The recorded ones are cited by other artifacts: `source_count_granularity_probe_2026-08-13.txt` by the matching rule, the four `conversion_pairs_*_2026-08-16` files plus their two session lists by RC-004, the four `nonfinite_depths_*_2026-08-16` files **and both `missing_depth_crossover_*` files by §17.**
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations`; `probe_band_drift_claims.py` takes `--module`; `test_measure_host_drift.py` takes `--keep`/`--tmp-root`; `test_missing_depth.py` takes `--permutations` (default 40) and `--completions` (default 120); `mutate_rc002_repairs.py`, `verify_rc003_round1_repairs.py`, `verify_rc003_round2_repairs.py`, `verify_rc005_round2_repairs.py` (also `--work-root`, `--python`, `--keep`), `probe_nonfinite_depths.py` and `probe_missing_depth_crossover.py` require `--repo-root`; `probe_conversion_pairs.py` requires `--assets-cache`, `--out`, and one of `--sessions`/`--sessions-file`; Codex's probes all require `--repo-root`.
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state. `git checkout -- <path>` undoes a mangled edit script. **To prove a closed section of a growing document is byte-identical, hash the section body between two headings** — `git diff --numstat` cannot, because a status line prepended above §1 counts as an insertion in the same file.
