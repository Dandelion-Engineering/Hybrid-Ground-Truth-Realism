# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 45 · 2026-08-18 04:40 PDT**
**Next session is Claude Session 46. No count-based progress report is due** (they fall at 8, 16, 24, 32, 40, **48**). A phase transition or an approved amendment would still trigger one.

## 0. WHAT THIS SESSION DID, IN ONE PARAGRAPH

**Codex's RC-007 Round 2 returned two blockers the Round-2 response itself created. Both accepted, neither disputed, and Draft 31 is the final Round-3 response the three-round limit allows.** **F4-R1's repair removes the construction rather than bounding it: a window is now filtered as its chunk PLUS THE LAST 500 SAMPLES OF THE PRECEDING CHUNK AND THE FIRST 500 OF THE FOLLOWING ONE**, so the margin is real recorded signal and the retained core is the **full 13,020-sample chunk**. That is `FilterRecording.get_traces` for a 13,020-sample chunk at `margin_ms="auto"` — an *instance* of the anchor pipeline, not an approximation — and **no bound is claimed on what remains.** **F7-R1's one-way claim is withdrawn in full: `R_null_sampled` is ONE-SIDED** — high withholds, low certifies nothing. **F6-R1's "discharged" sentence is withdrawn.** **One defect found here: §19.4's coverage theorem did not follow from its own premise — the tight bound is 170 chunks / 73.780 s, not 171 / 74.214 s.** Transfer triples to 957,031,364 bytes; Draft 30's mean-removal step is dropped. **RC-007 is open on Codex for a verdict, not a revision.**

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

## 1. Where the project is

**Phase 2 — Execution. One host gate of FIVE is discharged for one candidate. No host is pinned, no donor is selected, no generator has run, no sorter has run, and the project's actual question is untouched.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. **Not touched S44 or S45.** |
| `Accessible Claim Sheet.md` | Synchronized, same six. `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 31, `24e78a5ad139245b197286edd1acaf8bea42bc75af3378883b3180d29a923755`. §19 IS RC-007's SCOPE and awaits Codex's Round-3 VERDICT. §1–§18 unedited and proved: §1–§16 144,664 B `700b3b9a…`; §17 21,864 B `dc73b87f…`; §18 body 20,579 B `8af3e62c…`. Do not reopen §1–§18.** |
| `Reproducibility Packet/` | **NOTHING CHANGED IN S43, S44 OR S45.** `results/host_drift_CSHL047_Probe01.txt` `a2d32508…`, `.json` `2e125d41…`, `scripts/measure_host_drift.py` `20070982…`, `check_runbook_consistency.py` `35cea57d…`, `README.md` `806aefaf…`, `utils/band_drift.py` `eace4cd3…`, `archive_units.py` `ed0766f2…`, `missing_depth.py` `ef974027…`. |
| **`agents/Claude/tools/probe_rc007_round3.py`** | **NEW S45. `54aeff57847e7a26cd3c8a80219883500a22c9cf736a5950da195a7f79a531d8` — 27 checks, 0 failed.** Synthetic only, no archive. |
| **`…/rc007_round3_2026-08-18.txt` / `.json`** | **NEW. `b62d667c…` / `51e76266…`.** §19.3 and §19.12's figures are re-derived from the JSON by the checker. |
| **`…/probe_rc007_spec.py`** | **EXTENDED IN PLACE S45. `ef37577e271161677a637b34fcac18a930bb105d544b94992886116140c625dd` — 288 checks, 0 failed.** |
| **`…/probe_rc007_spec_2026-08-18_draft31.txt`** | **NEW. `97346727…`.** The `_draft30` and unsuffixed outputs are Rounds 2 and 1's and are kept. |
| **`…/mutate_rc007_spec.py`** | **EXTENDED IN PLACE S45. `16a5f8832f64d54120a1ba34dd649e09eebc833d8f304f6faff17be9d808aad2` — 52 of 52 caught, control green.** |
| **`…/mutate_rc007_spec_2026-08-18_draft31.txt`** | **NEW. `e42c12bb…`.** |
| `…/probe_filter_chain.py` + its two records | **UNCHANGED S45** `ef96ce21…` / `dfcea89d…` / `b9f3e089…`. |
| `…/probe_raw_ap_layout.py` + its two records | **UNCHANGED** `ddef6e33…` / `f992c394…` / `4896a14f…`. |
| `…/probe_rc006_repairs.py` · `test_measure_host_drift.py` · `test_missing_depth.py` · `test_band_drift.py` · `mutation_test_runbook_checker.py` · `mutate_rc002_repairs.py` | `512e31fc…` (61) · `79c9bb5c…` (543) · `435272af…` (86) · `946df906…` (103) · `d443ded0…` (18/18) · `97860ad9…` (32). **None re-run S43–S45 — no code they cover changed.** |
| Root `README.md` | **84 dated log entries**, banner at 2026-08-18. |
| `Review Cards/RC-007 …` | **OPEN. Round 3 submitted; Codex owes a VERDICT, and the three-round limit is reached.** |

## 2. The first thing to do next session

**Read `chats/Claude-Codex/Host Noise Gate/` before anything else.** My Round-3 handoff is the last message; Codex's verdict is what you are waiting on.

- **`chats/Claude-Codex/Host Noise Gate/` — active, on Codex.** RC-007 Round 3 verdict.
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active** by Randy's request. **Nothing pending.**
- **All fourteen other chats are concluded.**

**What can be done next, in order of readiness:**

1. **Respond to Codex's verdict.** **If it is not an approval, the next step is the agent-only Convergence Decision, NOT a fourth repair.** If it is an approval, RC-007 closes.
2. **Then implement the estimator** against whatever §19 says *after* the card closes — a packet utility plus a synthetic harness, the shape `band_drift.py` took after §16 closed. **Do not write it before RC-007 closes.** **⚠️ The F7-R1 tracked follow-up — contiguous versus interleaved split halves — MUST be settled before the estimator's first run.**
3. **Rank 2 (NYU-12 Probe01) can be measured** for drift — unpaused, unmeasured, command unchanged.

**⚠️ Rank 1's drift command, verbatim, from inside the packet folder — runbook step 11:**

`python scripts/measure_host_drift.py --session b52182e7-39f6-4914-9717-136db589706e --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

Add `--plan-only` for the sizing pass. **Measure free RAM against `peak_resident_bytes`, not `resident_bytes`.** About three minutes, 88.6 MB, 93 requests; `run_in_background`.

## 3. §19 AT DRAFT 31 — THE NOISE GATE AS IT NOW STANDS

**Nothing has been measured with it. These are symbols with definitions, not values.** **The three gated quantities are `sigma_worst_sampled`, `R_space_sampled`, `R_null_sampled`** — the `_sampled` suffix is load-bearing.

### 3.1 The pinned chain (§19.3) — FOUR steps now, not five

1. scale `int16 → µV` by the asset's own `conversion`; `offset` must be exactly 0
2. **high-pass on a 14,020-SAMPLE BLOCK OF REAL RECORDED SAMPLES** — the window's chunk plus the last 500 samples of chunk `i−1` and the first 500 of chunk `i+1` — fifth-order Butterworth at 300 Hz, `sos`, `sosfiltfilt`, `padtype="odd"`, `padlen=18`, designed at the **nominal 30,000 Hz**; then **discard the 500 margin samples at each end, retaining exactly the chunk's 13,020 samples**
3. **common median reference across all 384 probe channels**, per sample
4. `σ̂_c = MAD / 0.6744897501960817`

**⚠️ DRAFT 30's PER-CHANNEL MEAN REMOVAL IS GONE.** The anchor has no such step, and §19.3's whole force is now that its retained samples ARE the anchor's. It was analytically a no-op (`sosfiltfilt` initializes in steady state, so a constant maps to exactly zero) and measured at most `1.746e-10 µV`.

**⚠️ THE IDENTITY CLAIM IS THE LOAD-BEARING ONE AND IT RESTS ON READING SOURCE, NOT RUNNING IT.** SpikeInterface is **not installed** (Codex's Rung 0). §19.3 says its retained samples are what `FilterRecording.get_traces` returns for a 13,020-sample chunk at `margin_ms="auto"` — established from `filter.py`. **If that is wrong, everything F4-R1 repaired rests on it**, and it is the first thing I asked Codex to attack.

**Two declared deviations, each with its direction, and ONE PINNED PARAMETER:** phase shift omitted → **σ̂ biased upward**; bad channels not masked → **`R_space_sampled` inflated in both directions**; and **the chunk boundaries are pinned to the file's storage chunks — a *parameter* of the anchor pipeline, not a departure from it. NO BOUND IS CLAIMED on the difference between two chunk sizes.** Nominal-rate design costs at most **0.003 Hz** of corner shift.

### 3.2 The grid, the quantities and the coverage bound (§19.4)

- **A window centre needs a FULL CHUNK ON EACH SIDE**, because that is where the margin comes from, so eligible centres are `1 … C − 2` and `K = 60` centres sit at **`i_k = 1 + floor(k·(C−3)/(K−1) + 0.5)`** — explicit `floor(x+0.5)`. Rank 1: `1, 170, 340, …, 9,828, 9,997`.
- **Reading a window transfers THREE chunks and retains ONE.**
- **Largest gap `g = 170`; longest unsampled run `g − 1 = 169`; any interval fully containing `g = 170` consecutive chunks holds a sampled window = 73.780 s at rank 1.** **⚠️ TIGHT IN BOTH DIRECTIONS, verified exhaustively.** Coverage 26.04 s, **0.600%**. `g`, the duration and the fraction are published per candidate.
- `S(k)` = median over band channels of `σ̂_c(k)`; **`sigma_worst_sampled = max_{k∈G} S(k)`**; `sigma_median_sampled` is context.
- **`R_space_sampled = max_{k∈G} (p90/p10 across band channels)`.** **Percentiles nearest-rank: `p10` = rank `ceil(0.10·n)`, `p90` = rank `ceil(0.90·n)`; at n=72 ranks 8 and 65.**
- **`R_null_sampled`** = the same ratio over `σ̂_c^A/σ̂_c^B` from two disjoint halves of the retained 13,020 (**6,510 each**).
- **`max/median` is published and consumed by nothing.**

### 3.3 ⚠️ `R_null_sampled` IS ONE-SIDED — THE MONOTONE CLAIM IS WITHDRAWN

An observed `r_c(k)` is a **product** of an estimation-disagreement factor and a true temporal factor, and products cancel. Codex's construction, reproduced independently: estimation factors `[0.5]×8, [1]×56, [2]×8` give a nearest-rank spread of exactly **4**; reciprocal temporal factors `[2]×8, [1]×56, [0.5]×8` make every observed ratio 1 and the spread exactly **1** — carried from outside `M = 2.0` to the best value the statistic can take.

- **Above `M`: sufficient to withhold the measurement** (branch 4). Sound whatever produced it.
- **At or below `M`: CERTIFIES NOTHING.** Cancellation reaches the same place as a genuinely resolving estimator.
- **A candidate that passes, passes on `R_space_sampled` ALONE.**
- Branch 3's `resolved heterogeneity` label is **a recorded comparison, not a certificate**.
- **An interleaved split is a TRACKED FOLLOW-UP, not taken.** It would reduce but not eliminate the cancellation; the one-sided reading is sound either way; **it must be resolved before the estimator's first run.**

### 3.4 The thresholds (§19.6) — NOTHING MOVED

| | strict | relaxed | derivation |
|---|---|---|---|
| **floor** | **1.25 µV** | **1.25 µV — does not relax** | `A_min/40`, the anti-saturation condition |
| **`N`** (level, µV) | **10.0** | **25.0** | `A_min/5` and `A_max/8`, **both multipliers SpikeForest's own** |
| **`M`** (spatial) | **2.0** | **4.0** | `√(A_max/A_min)` and the full span |

`A_min = 50`, `A_max = 200` **µV peak-to-peak** (§11.1: donor `amplitude_uv` is `np.ptp`). **`A_max/σ ≥ 8` is IMPLIED by `σ ≤ 10.0`.**

**⚠️ THE PASS RULE HAS FOUR ORDERED BRANCHES; THE FIRST THAT FIRES IS THE DISPOSITION.**

1. `sigma_worst_sampled > N` → **fails** on level.
2. `sigma_worst_sampled < 1.25 µV` → **fails** on level, labelled `implausibly quiet`. **A failure, not an input error** — Codex accepted this at Round 2 as a predeclared design failure.
3. `R_space_sampled > M` → **fails** on homogeneity, labelled `resolved heterogeneity` if `> R_null_sampled`, else `resolution-limited`. **The null decides how a failure reads, never whether it is one, and the label certifies nothing.**
4. `R_space_sampled ≤ M` **and** `R_null_sampled > M` → **unmeasurable**.

**Degenerate channels** (exactly zero σ̂) are **counted and published, never masked**; they enter the percentile at their measured value and can drive the ratio to `+inf`, which fires branch 3.

**⚠️ INPUT ERRORS ARE NOT GATE OUTCOMES.** Too few full chunks for the grid (`C ≥ K + 2`), non-zero `offset`, absent/non-finite `conversion`, unit ≠ volts, a band electrode not resolving to one column, non-finite samples, failed replay → **input error: NOT recorded as failed, and the pinned order DOES NOT advance.** An **unmeasurable rejection** (branch 4) **IS a rejection and the order DOES advance.**

**⚠️ THE CONVENTION SUBSTITUTION HAS OPPOSITE DIRECTIONS FOR A FLOOR AND A CEILING.** p2p for single-sided peak **weakens a floor** (conditions 1 and 2 → necessary, not sufficient) and **strengthens a ceiling** (condition 3 → sufficient, not necessary, deliberately conservative). **The `snr_p2p = 40` ceiling is JUDGEMENT, not literature** — neither round challenged it, which is a fact about the rounds.

### 3.5 §19.8 — five gates, and NOTHING of gate 3 is discharged

**Host admissibility is FIVE gates. §15.5 is superseded in no clause.** **⚠️ AND DRAFT 30's SENTENCE CALLING A GATE-3 HOST-AGGREGATE PRECONDITION "DISCHARGED" IS ALSO WITHDRAWN** — Amendment 6 point 1 defines gate 3 through per-site and per-donor predicates a later configuration must pin, and defines **no** host-aggregate precondition. What §19 offers is **conditional arithmetic**: *if* anyone reports `A_min/sigma_worst_sampled` and `A_max/sigma_worst_sampled` under §19's thresholds, they restate §19.6's inequalities and add nothing.

**⚠️ The native-amplitude check was examined and REFUSED, and that stands.** Computable since Session 7 from `results/injection_placement_CA1.txt` — **which is why it cannot be a gate: any threshold would be written with all thirteen answers visible.** It also passes every candidate, so it cannot fail. Reported diagnostic only.

### 3.6 Cost (§19.9) — TRIPLED

**180 chunks × 5,316,841 projected stored bytes ≈ 957,031,364 bytes**, a PROJECTION from a whole-file average. **~10.8× the drift run's 88,599,226 B.** **⚠️ `RemoteFile`'s cache is unbounded and never evicted, so the estimator MUST bound its own cache to ONE WINDOW'S THREE CHUNKS**, not the run's 180. Three chunks are 29,998,080 B as `int16`; the 14,020-sample block across 384 channels is **43,069,440 B as `float64`**, and `sosfiltfilt` needs a comparable temporary.

**Two cheaper arrangements were examined and REFUSED, in §19.9 rather than in a session note.** Twenty windows of five chunks retains the same sixty chunks for 100 transfers — refused because a three-chunk window **dilutes a short excursion in its own MAD**, which is the sensitivity the gate exists for. Twenty single-chunk windows keeps the old 319 MB — refused because it triples the guaranteed duration to ~223 s. **⚠️ THE FIRST REFUSAL IS ARGUED, NOT MEASURED, and I flagged it to Codex as such.**

## 4. §19.2 — the measured layout (UNCHANGED, and no archive was read S44 or S45)

| property | value |
|---|---|
| shape | 130,188,000 × 384 |
| dtype / filters | `int16`, **gzip level 4** |
| **chunk** | **13,020 samples × 384 channels** (= 0.434 s, 9,999,360 B uncompressed) |
| logical / stored | 99,984,384,000 / 53,163,508,785 B → ratio **0.53172** |
| `conversion` | **2.34375e-06 V**; `offset` 0.0; unit volts; **no `channel_conversion`** |
| full chunks | **9,999**, plus a 1,020-sample partial |

1. **The chunk spans EVERY channel**, so 72 band channels cost exactly what 384 cost — which is why CMR is over the whole probe at no transfer cost.
2. **Time is addressable only at 0.434 s**, which is why a margin costs a whole neighbouring chunk.
3. **One bit is 2.34375 µV** — a MAD estimate on the STORED INTEGERS would be granular to 1.74 µV. **That is why the estimate is taken AFTER the chain.**

**§19 converts chunks to seconds at the NOMINAL 30,000 Hz**, consistent with §19.2's own `13,020 / 30,000 = 0.434 s`. Do not switch to the measured rate for a published duration without changing both.

## 5. Machine state and measured costs

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`).

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; never inherit a number, including from this file.

**Session 45 readings: 04:09 — 16,753 MiB of 32,425 free, GPU 956 of 16,311. 04:35 — 16,288 MiB free, GPU 955.** Nothing heavy ran; no archive read.

**Suite costs:** `probe_rc007_round3.py` ~25 s; `probe_rc007_spec.py` ~2 s; **`mutate_rc007_spec.py` ~2 min (52 mutations)**; `probe_filter_chain.py` ~20 s; `test_measure_host_drift.py` 18.3 s; `test_missing_depth.py` ~15 s; `test_band_drift.py` ~48 s; RC-002 mutation harness ~11 min; the rank-1 drift measurement ~3 min / 88.6 MB / 93 requests. **Take your own readings.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2`, `scipy==1.18.0` — all BSD-3-Clause. **`requirements.txt` was NOT touched S45.** **scipy is pinned in the ROOT `requirements.txt` only; the packet's own file gains it when the first packet script imports it.** SpikeInterface, PyTorch and Kilosort4 **still not installed** — Codex's Rung 0. Use `./venv/Scripts/python.exe`; never bare `python`/`pip`.

## 6. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity · **drift, for rank 1 only**. Checked **non-gating**: donor-lab separation.
Gate **specified but unapproved: noise (§19), at RC-007 Round 3, awaiting Codex's verdict.**
Gate **3 — post-rescaling effective SNR — IS IN FORCE, IS NOT SUPERSEDED, AND IS NOT DISCHARGED IN ANY PART.** Its operative content is Amendment 6 point 1's per-donor screen, evaluated after a rendered donor exists.
Gates **open and Codex's**: joint ten-placement (Amendment 6 point 1) · the balance/manipulation gate.

### 6.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) — **DRIFT PASSED** · 2. NYU-12 **Probe01** `a8a8af78` (66) — **unpaused, unmeasured** · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`. Rank 1 is `b52182e7-39f6-4914-9717-136db589706e`.**

**Do not re-derive the order and do not re-sort it.** **Two passes:** the whole order at strict, then — only if nothing clears every gate — the same order restarted once at relaxed. **Gate order** (cheapest first): drift → noise → effective SNR → joint ten-placement → balance.

**⚠️ Four ranks — 5, 7, 9, 13 (NYU-65, NYU-45, NYU-39, NYU-48) — remain PAUSED on the declared-clock disagreement, not rejected.**

**⚠️ First-admissible means rank 1 is only the host if it clears EVERY gate.** Passing drift orders nothing on its own.

### 6.2 What rank 1's read established

Raw provenance authenticated (`Created using NeuroConv v0.9.2`); pair condition passes; CA1 band **320.0–1020.0 µm, 72 channels**; AP extent `t_first 1.138489 s`, `t_last 4340.732689 s`; **174 band units of 756; 3,160,311 spikes**; payload 50,564,976 bytes; **231 NaN depths in 11 units; 0 non-finite times.**

### 6.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Codex owns the footprint/placement calibration**; do not start it.

## 7. THE DRIFT RESULT — rank 1, measured 2026-08-17, replayed by Codex, approved at RC-006

| quantity | value |
|---|---|
| `Delta_10min` | **1.821 µm** (11-bin window from bin 1) |
| `Delta_full` | 2.537 µm |
| `Q95_null` | **0.526 µm** (nearest-rank, rank 190 of 200) |
| `inside_null` | **False**; threshold 20.0 µm strict |
| bins / units / spikes | 72 (0 invalid) / 140 of 174 / 3,160,311 |
| **verdict** | **passed True, `resolved, within tolerance`** |

**Missing-depth layer:** 231 missing (0.007309%) in 11 units; support invariance holds; `Delta_10min` bound **[1.780, 1.821]**; `Q95_null` bound **[0.533, 0.546]**; **disposition `passes`, advances True, conflict False.**

**Three things that must not be lost:**

1. **`inside_null` is False and `Delta_10min` is ~3.5× `Q95_null`.** Structure is resolved above the noise floor, and it is ~9% of tolerance. **Both halves are the measurement.**
2. **The finite-only `Q95_null` (0.526) falls BELOW its own completion bound [0.533, 0.546].** §17.9 declared this permitted in advance. **Do not "fix" it.**
3. **⚠️ THE PER-UNIT AUDIT IS LOUD AND THE RULE FORBIDS CONSUMING IT.** Whole-recording ranges over 140 units: min 1.259, median 9.155, p90 27.146, **max 71.629 µm; 21 exceed 20 µm, 11 exceed 40 µm.** **Per-unit values carry no null; comparison to `Q95_null` or `L` is undefined in either direction.**

## 8. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **footprint/placement calibration** · **real-arm donor-matching rule** · **exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 9. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`**. **Bounded-negative is the harder verdict.**
- **The drift gate is two numbers.** `Delta_10min <= L` **and** `Q95_null <= L`. **Window is ELEVEN 60 s bins.** Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data **except a NaN depth (§17)**, failed replay. **A clock or coordinate mismatch is not one of them** — those pause the pinned order (§16.4).
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** A median tracks rank; on a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`.
- **The drift unit set is blind to `kilosort2_label`.**
- **The per-unit excursions are reported and never consumed.** **The absence of magnitude separation is not evidence either — and NOR IS ITS PRESENCE, which rank 1 demonstrates on real data.**
- **The bin grid anchors at session `t = 0` with extent `t_last_s`.** **`duration_s` is a span, not an alternative clock.** **Endpoint containment cannot identify a clock — and neither can reference-instant agreement.**
- **The permutation pool is analysed-bin spikes only**, for both observation and null.
- **Amendment 6 governs: Tier A is parameterized by `N`.** `10 ≤ N ≤ 16`; `N < 10` is Slot 12.3. `q = ⌊50/N⌋`, `r = 50 mod N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.** **⚠️ AND SO, THROUGH `N`, ARE THE PER-DONOR ELIGIBILITY GATES.**
- **`N ≥ 10` is structural:** `16 − 6 = 10`.
- **The manipulation check is a hard stop-or-go gate**, and the realized zone-donor count is a *composition-integrity* quantity, **not** a substitute for it.
- **Amendment 5:** the injection zone's donors are removed from the **real** region-unaware arm before matching.
- **The matching rule's provenance test is two-level**; **Level A binds only at stages 3 and 4.**
- **0.11 and 0.12 are two sampling models, not two estimates.** Blocked expectations **1.03** and **1.17**.
- **CA1's sixteen donors sit in exactly 4 source datasets, `[6, 5, 3, 2]`**, 4 sessions, 4 animals. Library-wide: **37 insertions, 24 sessions, 12 animals**.
- **The source-count floor binds at *every* relaxation stage** and is an **equality**.
- **One host and injection zone across all tiers by default.**
- **CA1 is the approved first zone.**
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **The donor library is good-clusters-only by construction.**
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.** **§19 uses the RAW 50–200 µV peak-to-peak form for its own derivation.**
- **The Allen CCF ontology is not importable** — noncommercial terms.
- **A one-command-per-side runbook rule is a hard parse error, not a warning.**
- **NaN is the only missing marker. Both signs of infinity are input errors.**
- **`reconcile_verdict`: a candidate advances only when the gate and the completion bound point the same way.**
- **The console contract:** report and record FIRST, then exactly two lines, reconciled decision **last**.
- **`peak_resident_bytes = cache_bound + resident + structures + library_cache` — four terms.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count; S27's five; S28's three plus the Round-2 ASCII claim; S29's one; S30's three; S31's two; S32's own; S34's two; S36's; S38's; S39's; S40's; S41's four; S43's threshold multiplier taken from memory; S43's six that RC-007 Round 1 caught; S43's input-error/unmeasurable conflation found at S44; **and S44's three that RC-007 Round 2 caught — the `+1e-06` isolation figure promoted from twelve fixtures into a bound, the one-way non-stationarity claim, and the gate-3 precondition called discharged — plus S44's loose coverage theorem, which I found myself at S45.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 10. The module surfaces

`missing_depth.py`: `median_interval` · `split_unit` · `missing_counts` · `unit_intervals` · `support_invariance` · `centre_bounds` · `centred_intervals` · `trace_intervals` · `interval_excursions` · `measure_missing_depth_sensitivity` · `replicate_bin_bounds` · `null_interval` · `stability_verdict`.

- **Import form is `from utils import band_drift`.** A bare `import band_drift` fails.
- `null_interval` returns `q95_lo` · `q95_hi` · `values_lo` · `values_hi` · `bounded` · `rank` · `n_permutations`. **There is no `q95` key** — but **the gate's own null in the JSON record IS `null.q95`**.
- `measure_missing_depth_sensitivity` **raises** if the point estimate falls outside its own bound.
- **`support_invariance` returns numpy arrays.**
- **Every entry point takes the COMPLETE per-unit arrays.** **`split_unit` is the one place the record is split.**

`measure_host_drift.py`: `reconcile_verdict` · `summarize_missing` · `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`, no sensitivity flag.** **`--help` renders 164 lines** and its description is the module docstring verbatim.

`archive_units.py`: `MASK_ITEMSIZE` · `PROVENANCE_MAX_BYTES = 65536` · `PROVENANCE_BLOCK_BYTES = 65536` · `MEASURED_CONVERSION_VERSIONS`, never gated · `UNITS_PATH` · `TIME_COLUMN` · `DEPTH_COLUMN`. Transfer budget **393,216**. **There is no plan key called `bytes`.** **`ascii_safe` is here.**

- **Record `plan` keys:** `logical_bytes` · `cache_bound_bytes` · `resident_bytes` · `mask_bytes` · `structures_bytes` · `library_cache_bytes` · `peak_resident_bytes` · `spent_bytes` · `block_bytes` · `bound_basis` · `n_units` · `n_spikes` · `time_layout` · `depth_layout`. **No `per_unit` key.**
- **`REFERENCE_TIME_FORM` gates the lexical shape before `fromisoformat`. ⚠️ THE UTC-OFFSET REQUIREMENT IS DELIBERATELY NOT IN THE GRAMMAR.** **Do not "tidy" this.**

`band_drift.py`: `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** Symbol `Delta_10min`. `apply_gate` returns **`passed`**. Others: `bin_seconds` 60, `min_spikes_per_bin` 10, `min_bin_fraction` 0.8, `min_units_per_bin` 5, `n_permutations` 200, `null_percentile` 95, `master_seed` 3175830281, thresholds 20/40 µm.
- **`unit_traces` raises on non-finite depths.** `complete_bins(extent_s)` **anchors at 0**. **Rank 2's `t_first_s` is −0.000047 s**, so sub-zero exclusion is live.

`screen_host_timing.py` holds `read_series_timing`, which is what `probe_raw_ap_layout.py` mirrors for the layout read.

### 10.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`. **Do not weaken into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size.** `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4`.
3. **The provenance-budget invariant**, on both assets, on every case reaching a record.
4. **The fixture axes are separate on purpose:** `provenance=` **and** `reference_time=` independently.
5. **`run_case(..., capture=False)`** gives `result["stdout"] is None`, not `""`.
6. **`_nan_at(units, positions)`** sets NaN at **stated** positions.
7. **`check_console_decision(...)`** is the shared console assertion.
8. **`case_the_ceiling_counts_the_retained_masks`** builds ceilings from the **fixture's** spike count. **Do not "simplify" it.**

## 11. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). **S33, S36 and S44 are the sharpest instances.**
2. **Read the column, do not count it** (S5, S43, S44).
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30–S33, S36). **⚠️ S45 IS THE CLEANEST PAIR: BOTH of my round-3 probe's failing checks were pessimistic expectations of mine, and correcting them toward the measurement improved the artifact in both cases.**
4. **A clean trend invites a causal story you have no way to check** (S5, S33, S36).
5. **In an owner re-review, the pull is to accept everything** (S6).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **⚠️ A heredoc through the Bash tool mangles nested quotes AND backslash escapes. WRITE SUCH SCRIPTS WITH THE WRITE TOOL.** **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32).
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32, S36). **⚠️ A gate parameter may not be changed after a candidate's value is known.**
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7).
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S33, S42). **S43: two numbers with the same NAME may not be the same quantity.** **S44: the inequality between them can be right while the DIRECTION it propagates through a bound is wrong.**
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32, S33, S36).
13. **A correction is worth logging even when the conclusion survives** (S8, S29, S37, S42, S43).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9, S15).
16. **An audit must use the same key its lookup uses** (S9, S27, S28, S31).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10, S42).
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17, S23, S28, S29).
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11, S27–S29, S33). **S41 is the positive instance.**
24. **Note which direction a correction pushes** (S11, S15, S16, S26, S38, S43, S44).
25. **When a test fails, first ask whether the test or the artifact is broken** (S11, S37, S39, S40, S42). **S43/S44: both mutation misses were gaps in MY CHECKER — a third answer. ⚠️ S45 MAKES IT FIVE FOR FIVE: every mutation the harness missed was a gap in my checker, and every failing check in my own probe was a wrong expectation. The artifact was not the defect in any of the ten.**
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S44).
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29, S40, S43, S44, S45).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27, S36). **S44: two failure semantics with similar names are where it gets made by accident.**
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26, S34). So assert it.
31. **A supersession can be too broad as well as too narrow** (S14). **Say which single clause you supersede** (S39, S43). **S44: OR WITHDRAW IT.** **⚠️ S45: AND CHECK WHETHER A NARROWER CLAIM YOU KEPT IS ALSO WRONG — F6-R1 was exactly that: the four-gate withdrawal was right, and the one sentence I kept from it still had to go.**
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28, S36, S43).
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32, S34–S45). **⚠️ S45: AN APPEND-STYLE EDIT CONTAINS ITS OWN OLD TEXT, so the "old text is gone" post-assertion must expect one occurrence, not zero. Validate every replacement across every file *before* writing any, and re-assert afterwards.**
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Twenty-eight for twenty-eight (S15–S45).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26). **S44's F1 is the sharpest.**
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32, S33, S35).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17, S43). **⚠️ S45: AND THEN CHECK WHETHER THE NULL CAN BE MOVED BY THE THING IT IS SUPPOSED TO CONTROL FOR — a split-half null is a product, and products cancel.**
41. **Read the clock at the moment you write the timestamp** (S17, **S45** — I wrote 04:52 into a status line at 04:21 and had to correct it). **`time.strftime("%Z")` returns the long name on Windows: use a literal `PDT`.**
42. **⚠️ A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24, S34, S35, S37, S38, S42, S44).
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30, S34, S35, S40).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32, S34). **And which *currency* it is denominated in.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26).
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28). **S44 is the positive instance: `_sampled`.**
50. **A counterexample built on a degenerate case invites dismissal** (S24, S26, S37, S38). **⚠️ S45 IS THE MODEL OF THE OPPOSITE: Codex built his on the file's OWN measured 2.34375 µV lattice, inside `int16`, so there was nothing to dismiss.**
51. **A near-miss is not the finding** (S24).
52. **A test can encode the defect it was written to catch** (S25, S28).
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25). **⚠️ STILL OPEN for the noise gate, which is why S45 could change the filter input, the retained count, the grid and the transfer budget at no cost — and why the F7-R1 split-half follow-up MUST be settled before the estimator's first run.**
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32, S35, S38, S39).
56. **Which fixture a published number came from is part of the number** (S25, S26, S37). **⚠️ S45 IS THE HARD VERSION: WHICH FIXTURES A NUMBER CAME FROM IS *ALL* IT IS. Twelve fixtures are not an input class, and calling their worst case "the entire deviation" is the defect.**
57. **A check that cannot fail is not a check** (S27–S32). **S33: nor is one that cannot pass.** **S37: a bound that pauses everything is not a bound.** **S44: a negative check on a string that does not exist is also not a check.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen; S42 posted one on the accessible register.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). RC-003 through RC-006 all closed without another.
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair.** **Assert every mutation's source string still matches its file exactly once** (S39–S41, S44, **S45** — four anchors went stale the moment the section text changed, and the harness hard-failed rather than skipping them, which is the design).
62. **Evidence must come from the exact state you publish digests for** (S31, S34, S35, S37, S41, S42). **S43: the STATUS LINE is a publishing surface.**
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32, S34, S40, S43).
64. **When a reviewer's finding is correct, check whether it is *complete*, and whether its *evidence* proves it** (S32, S37, S38). **RE-DERIVE a handed-over number yourself** (S41, S42, S44, **S45 — the strongest instance: an implementation sharing no code with either the reviewer's or my own earlier one, agreeing to nine decimal places**).
65. **An undetermined value is a missing measurement, not a negative one** (S33, S34, S36, S37).
66. **Test a hypothesis on data that did not suggest it** (S33, S36).
67. **⚠️ Do not both discover an input error and rule on its disposition in the same session** (S33, S36). **Post the design, including where you deviate, before writing the code** (S37–S40, S43).
68. **Separate the fixture's axes before you need them separate** (S34).
69. **A closed card's evidence script may legitimately go red** (S34). **Do not extend a closed card's harness — write a new one** (S40). **S44/S45: an OPEN card's harness is EXTENDED IN PLACE, and each round's recorded output is kept beside the new one rather than overwritten.**
70. **A note added to a docstring is printed surface** (S34, S40, S41).
71. **⚠️ BEFORE ADDING A SECOND ENFORCER OF A PROPERTY, ASK WHAT THE MUTATION FOR THAT PROPERTY REVERTS** (S35).
72. **A whole-command test can have its meaning moved by a change elsewhere while staying green** (S35).
73. **The trusted parser is part of the input surface** (S35).
74. **A diagnostic that answers "how bad is it" must also answer "what would the fix cost"** (S36).
75. **When you refuse to use a measured pattern, record it anyway and say why you refused** (S36, S41, S43). **⚠️ S45: AND PUT THE REFUSAL IN THE ARTIFACT, NOT IN A SESSION NOTE — §19.9 carries both refused cheaper arrangements, because a refusal that is not in the artifact is not reviewable.**
76. **⚠️ AN AVERAGING STRUCTURE AND A SYSTEMATIC PERTURBATION SCALE DIFFERENTLY** (S37).
77. **Show the vacuity rather than delivering the vacuous bound** (S37). **FIRST PROVE THE VACUITY** (S38).
78. **Where a bound is exact and where it is an outer bound are different claims** (S37).
79. **⚠️ AN IMPOSSIBILITY ARGUMENT TURNS ON ONE WORD** (S38).
80. **⚠️ TESTING A BOUND AGAINST A RESTATEMENT OF ITS OWN DEFINITION TESTS ONLY THAT TWO HALVES OF ONE ARGUMENT AGREE** (S38).
81. **The sharpest containment evidence is a completion landing exactly on an endpoint** (S38, S41).
82. **A test that is numerically right because two paths agree is not a test that they agree** (S38).
83. **⚠️ A CONSTANT COMPLETION AT A DISTRIBUTION'S CENTRE IS A DEGENERATE FIXTURE** (S38).
84. **⚠️ A WHOLE-FILE REWRITE OF A TEST SUITE IS A COVERAGE RISK** (S38). `git show HEAD:<path>` recovers the prior implementation. **S44 made the mitigation routine: diff the literal strings the old checker searched for against the new one. S45 avoids the risk entirely by extending in place.**
85. **⚠️ A REVIEWER'S INSTRUCTION CAN HAVE TWO PARTS** (S39). **⚠️ S45: OR THREE OPTIONS — Codex's F4-R1 named three permitted repairs, and the right answer took the FIRST for the part that was ours and the THIRD for the part that was not. Read an option list as a partition of the problem, not as a menu.**
86. **⚠️ AN ASSERTION ABOUT AN EDIT CAN FAIL WHILE THE EDIT IS CORRECT** (S39, **S45** — my chat-append verification line was an operator-precedence bug and the append itself was fine).
87. **⚠️ CONSUMING A DIAGNOSTIC IS WHERE THE POLICY GETS MADE** (S39).
88. **Publish an aggregate and the thing it aggregates** (S39). **PUBLISH A TOTAL AND EVERY TERM OF IT** (S42).
89. **⚠️ A THRESHOLD COMPUTED FROM THE QUANTITY UNDER TEST MOVES WITH THE DEFECT** (S40).
90. **⚠️ A POST-WRITE CHECK CAN FAIL ON ITS OWN STRING RATHER THAN ON THE WRITE** (S40).
91. **A defect that lives only in the console is invisible to a suite that reads only artifacts** (S40).
92. **⚠️ A DESIGN DECISION ARGUED ON FIXTURES GETS EXERCISED BY REAL DATA, AND YOU SHOULD SAY WHEN IT DOES** (S41).
93. **⚠️ THE MOMENT A RULE STOPS BEING FREE TO CHANGE IS THE MOMENT ITS FIRST VALUE IS KNOWN** (S41).
94. **⚠️ REMOVING A DECLARATION REMOVES THE MUTATIONS THAT TESTED IT** (S41).
95. **⚠️ A DIFFERENCE BETWEEN TWO SAMPLES OF A TOTAL DOES NOT MEASURE A PART OF IT** (S42).
96. **⚠️ THE INSTRUMENT CAN BE RIGHT WHILE THE PROSE READING IT IS WRONG** (S42).
97. **⚠️ THE PLAIN-LANGUAGE REGISTER IS WHERE A BOUNDARY GETS LOST** (S42).
98. **⚠️ S43 — READING THE STORAGE LAYOUT CHANGED THE DESIGN, IT DID NOT CONFIRM IT.**
99. **⚠️ S43 — A MULTIPLIER YOU CANNOT TRACE TO A SOURCE THIS SESSION IS A MULTIPLIER FROM MEMORY.**
100. **⚠️ S43/S44 — A GATE'S REAL CONTENT IS WHAT IT CAN REJECT THAT NOTHING ELSE CAN.** Check the *whole* path by which it rejects, including one that runs through a downstream count.
101. **⚠️ S44 — READ THE SOURCE OF A TOOL YOU ARE IMITATING, NOT ITS DOCUMENTATION AND NOT YOUR MEMORY OF IT.** **⚠️ S45 EXTENDS IT: READ IT FOR *EVERYTHING* IT DOES, NOT ONLY THE PART YOU WERE ASKED ABOUT.** S44 read `filter.py` and took the operator and the margin width; the same source says the margin comes from **real neighbouring samples**, and not taking that too is what produced F4-R1 one round later.
102. **⚠️ S44 — WHEN A CLAIM IS FALSE, CHECK WHETHER THE FIX IS TO BOUND IT OR TO REMOVE ITS CAUSE.** **S45 is the second application and it was cheaper because I looked for it.**
103. **⚠️ S44 — A NUMBER RESTATED N TIMES IS N PLACES IT CAN DIVERGE.** The checker carries a **restatement census** — value, expected occurrence count. **S45: when a value changes, RECOUNT the census from the document and inspect where each occurrence lives; do not guess the new number.**
104. **⚠️ S44 — WITHDRAWING A PROPOSAL IS A COMPLETE ANSWER, AND USUALLY A BETTER ONE THAN NARROWING IT.**
105. **⚠️ S44 — A PROPOSAL MADE IN THE SAME DRAFT THAT FIRST CONSTRUCTS ITS ARGUMENT HAS NOTHING CHECKING IT.** **⚠️ S45 APPLIES IT TO A *DESIGN CHANGE* AND DECLINES ONE: the interleaved split is tracked rather than taken, because a change made in a final round has nothing left to check it — and the decision does not depend on it either way.**
106. **⚠️ S45 — "REMOVE THE DEVIATION" AND "BOUND THE DEVIATION" ARE DIFFERENT KINDS OF ANSWER, AND THE FIRST DOES NOT NEED A NUMBER.** What carries §19.3 now is structural: every sample the filter sees is a real recorded sample. The measurements beside it are labelled diagnostics precisely because the section does not need them to be bounds.
107. **⚠️ S45 — A TRUE STATEMENT THAT DOES NOT FOLLOW FROM ITS OWN PREMISE IS STILL A DEFECT.** The `g + 1` coverage bound was correct and conservative, which is exactly why it survived two review rounds. Check that a bound is *tight*, and verify tightness in both directions, or say that you did not.
108. **⚠️ S45 — AN EXPENSIVE REPAIR NEEDS ITS ALTERNATIVES PRICED IN THE ARTIFACT.** Tripling the transfer is a decision a reader is entitled to see argued. Naming the cheaper options and the reason each was refused is what makes it a decision rather than an omission — and it is also where I had to admit one reason is argued rather than measured.

## 12. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **RC-001–RC-006 closed; RC-007 open awaiting a Round-3 verdict.** **A new card gets a new chat.**
- **`Playbooks/review-cycle.md` is two documents in one file:** read the superseding top section.
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry is the last dated line inside the log. **84 dated entries; banner at 2026-08-18.** **⚠️ Corrections propagate forward; do not "fix" an earlier entry.**
- **Status lines in the selection document are a stack.** Draft N's line goes above Draft N−1's and ends "Draft N−1's own status line follows." **Retained lines keep their errors.** **⚠️ The status line is a publishing surface and `probe_rc007_spec.py` checks sixteen of its strings.**
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. `ls "C:/Users/cresp/AppData/Local/Temp" | grep -c "drift_reader\|rc002_mutation\|rc005_reversion\|rbchk\|rc007_mutation"` — **0 at S45 close**; `mutate_rc007_spec.py` deletes its own tree.
- **A long archive read belongs in the background.**
- **`RemoteFile` validates and retries range responses.** Counters `n_bytes` / `n_requests` — **total every read**. **A retry re-transfers a block.** **⚠️ ITS CACHE IS UNBOUNDED AND NEVER EVICTED** — which §19.9 turns into a hard requirement on the noise estimator, now for **three chunks per window**.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py`, `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`, `missing_depth`. **`read_series_timing` lives in `screen_host_timing.py`.**
- **The runbook checker walks `scripts/` non-recursively.** **A script in `scripts/` without a step is a hard failure unless declared in `PENDING_STEP`**; **`PENDING_STEP` is empty.** **None of S43's, S44's or S45's tools is in the packet, so none needs a step.**
- **Scripts must not print non-ASCII.** cp1252. **Check by capturing `--help`** — `measure_host_drift.py` **164**; `probe_rc007_round3.py` **46**; `probe_rc007_spec.py` **38**; `mutate_rc007_spec.py` **39**; `probe_filter_chain.py` **49**; `probe_raw_ap_layout.py` **39**; all 0 non-ASCII. **⚠️ A failure DETAIL string can carry non-ASCII even when the labels do not** — escape at the printer, not the call site.
- **Line endings are pinned by `.gitattributes`, which sets `* -text`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (233/233 at S45 close); the root `README.md`, the packet README, the selection document, the Review Cards and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert the ratio afterwards.
- **Both `.gitignore` files ignore `__pycache__/`.** **`Reproducibility Packet/results/` is NOT ignored.**
- **`agents/Claude/tools/` holds twenty scripts and twenty-seven recorded outputs.** `raw_ap_layout_*_2026-08-18.json`, `filter_chain_2026-08-18.json` and `rc007_round3_2026-08-18.json` are all cited by §19 and read by `probe_rc007_spec.py`. **The two `_draft31` outputs are current; the `_draft30` and unsuffixed ones are Rounds 2 and 1's and are kept.**
- **Read the parser before inventing a flag.** `probe_rc007_round3.py` requires `--out` and takes `--records --seeds`; `probe_filter_chain.py` requires `--repo-root --out` and takes `--records --margins --excursions`; `probe_raw_ap_layout.py` requires `--repo-root --session --probe --assets-cache --out` and takes `--records --band-channels --block-kb`; `probe_rc007_spec.py` requires only `--repo-root`; `mutate_rc007_spec.py` requires `--repo-root --work-root` and takes `--python`. Older probes: `test_band_drift.py` `--permutations`; `test_measure_host_drift.py` `--keep`/`--tmp-root`; `test_missing_depth.py` `--permutations`/`--completions`; the `verify_rc00*` and `probe_*` scripts require `--repo-root`.
- **Git history is a verification tool.** `git show '<sha>:<path>'` recovers any prior exact state. **To prove a closed section of a growing document is byte-identical, hash the section body between two headings** — §19's checker does this for three spans at once.
