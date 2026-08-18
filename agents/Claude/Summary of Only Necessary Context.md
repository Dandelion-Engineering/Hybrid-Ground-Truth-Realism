# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 43 · 2026-08-18 00:35 PDT**
**Next session is Claude Session 44. No count-based progress report is due** (they fall at 8, 16, 24, 32, 40, **48**). A phase transition or an approved amendment would still trigger one.

## 0. WHAT THIS SESSION DID, IN ONE PARAGRAPH

**RC-006 closed `Approved` at Round 2, so the document was free and I wrote §19 — the host noise gate — as a contract, before any candidate's noise value is known and before any estimator exists.** The gate is three numbers: `sigma_worst` (loudest window's band-median robust scale, gated at **10.0 µV** strict / **25.0 µV** relaxed), `R_space` (worst window's p90/p10 spread across band channels, gated at **2.0** / **4.0**), and `R_null` (the same ratio between disjoint half-windows, which makes a candidate **unmeasurable** if it exceeds the tolerance). **Both thresholds are derived from pinned quantities**, and after a mid-session correction **both multipliers are SpikeForest's own (5 and 8)** rather than mine. **One thing was measured and it is a property of the file, not a candidate:** the raw AP stream is `int16`, gzip-4, chunked **13,020 × 384**. **§19.8 is the structural finding: §15.5's third gate has no host-level content §19.6 does not already decide, so I propose host admissibility is four gates rather than five.** RC-007 is open at Round 1 on Codex.

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

## 1. Where the project is

**Phase 2 — Execution. One host gate of four (formerly five) is discharged for one candidate. No host is pinned, no donor is selected, no generator has run, no sorter has run, and the project's actual question is untouched.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 29, `d0fdd4626bc3680313ddbae122a10e157d7b8efbbd9f6847752a1379fabc5bd8`. §19 IS RC-007's SCOPE and is at Round 1. §1–§18 unedited and proved: §1–§16 144,664 B `700b3b9a…`; §17 21,864 B `dc73b87f…`; §18 body 20,579 B `8af3e62c…` (recorded S43 for the first time). Do not reopen §1–§18.** |
| `Reproducibility Packet/` | **NOTHING CHANGED IN S43.** `results/host_drift_CSHL047_Probe01.txt` `a2d32508…`, `.json` `2e125d41…`, `scripts/measure_host_drift.py` `20070982…`, `check_runbook_consistency.py` `35cea57d…`, `README.md` `806aefaf…`, `utils/band_drift.py` `eace4cd3…`, `archive_units.py` `ed0766f2…`, `missing_depth.py` `ef974027…`. |
| **`agents/Claude/tools/probe_raw_ap_layout.py`** | **NEW. `ddef6e3396b97bf366d3cee16a358d4a407986de4426dcf694cae4c2fc78ac52`.** Reads one raw AP series' layout; **never slices the sample array**. |
| **`…/raw_ap_layout_CSHL047_Probe01_2026-08-18.txt` / `.json`** | **NEW. `f992c394…` / `4896a14f…`.** §19's cost model is built on the JSON. |
| **`…/probe_rc007_spec.py`** | **NEW. `5fb2186545774bad29526f15e8f223572f555c350103f5a0f7ef71cc091ed1b3` — 99 checks, 0 failed.** |
| **`…/probe_rc007_spec_2026-08-18.txt`** | **NEW. `1de3e924…`.** |
| **`…/mutate_rc007_spec.py`** | **NEW. `ae81093ab9d587c5631e3e71ae1840b357ccf4839b16fcfcf9966f7576ac4f1e` — 11 of 11 caught, control green.** |
| **`…/mutate_rc007_spec_2026-08-18.txt`** | **NEW. `e01baea8…`.** |
| `…/probe_rc006_repairs.py` · `test_measure_host_drift.py` · `test_missing_depth.py` · `test_band_drift.py` · `mutation_test_runbook_checker.py` · `mutate_rc002_repairs.py` | `512e31fc…` (61) · `79c9bb5c…` (543) · `435272af…` (86) · `946df906…` (103) · `d443ded0…` (18/18) · `97860ad9…` (32). **None re-run S43 — no code they cover changed.** |
| Root `README.md` | **80 dated log entries**, banner at 2026-08-18. |
| `Review Cards/RC-007 …` | **OPEN at Round 1, full-artifact pass, on Codex.** |

## 2. The first thing to do next session

**Read `chats/Claude-Codex/Host Noise Gate/` before anything else.** My RC-007 Round-1 handoff is the last message; Codex's ledger is what you are waiting on.

- **`chats/Claude-Codex/Host Noise Gate/` — active, on Codex.** RC-007 Round 1.
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active** by Randy's request. Codex agreed at S42 with the accessible-register note and will apply it when an Accessible Piece exists. **Nothing pending.**
- **All fourteen other chats are concluded**, including `Rank 1 Drift Result`.

**What can be done next, in order of readiness:**

1. **Respond to Codex's RC-007 ledger.** Round 1 is the only full-artifact pass; rounds 2+ are delta-only; three round-trips maximum.
2. **Then implement the estimator** against whatever §19 says *after* review — a packet utility plus a synthetic harness, the shape `band_drift.py` took after §16 closed. **Do not write it before RC-007 closes.**
3. **Rank 2 (NYU-12 Probe01) can be measured** for drift — unpaused, unmeasured, command unchanged.

**⚠️ Rank 1's drift command, verbatim, from inside the packet folder — runbook step 11:**

`python scripts/measure_host_drift.py --session b52182e7-39f6-4914-9717-136db589706e --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

Add `--plan-only` for the sizing pass. **Measure free RAM against `peak_resident_bytes`, not `resident_bytes`.** About three minutes, 88.6 MB, 93 requests; `run_in_background`.

## 3. §19 — THE NOISE GATE, AS SPECIFIED

**Nothing has been measured with it. These are symbols with definitions, not values.**

### 3.1 The pinned chain (§19.3), mirroring the anchor pipeline

1. scale `int16 → µV` by the asset's own `conversion`; `offset` must be exactly 0
2. per-channel mean removal over the window
3. **300 Hz high-pass in the frequency domain** (rfft, zero bins below 300 Hz, irfft), then **discard 150 samples (5 ms) at each end** — the DFT wraps
4. **common median reference across all 384 probe channels**, per sample
5. `σ̂_c = MAD / 0.6744897501960817`

**Three declared deviations, each with its direction:** phase shift omitted (needs an assumed converter map) → **σ̂ biased upward**; bad channels not masked → **`R_space` inflated in both directions**; brick-wall filter rather than the pipeline's Butterworth → **no direction claimed**. **§19 does not claim σ̂ equals the σ the sorter will see.**

### 3.2 The quantity (§19.4) and the floor (§19.5)

- `K = 60` disjoint **chunk-aligned** windows at chunk indices `floor(k·C/K)`, `C` = full chunks inside the extent. Deterministic, **seedless**.
- `S(k)` = median over band channels of `σ̂_c(k)`; **`sigma_worst = max_k S(k)`**; `sigma_median` is context.
- **`R_space = max_k (p90/p10 across band channels)`**, nearest-rank.
- **`R_null`** = the same ratio over `σ̂_c^A/σ̂_c^B` from two disjoint halves of each window. **Bounds estimation VARIANCE only; a per-channel bias is identical in both halves and gives a ratio of one.**
- **`max/median` is published and consumed by nothing**, like the per-unit drift excursions. Never compare it to `M`, or a per-channel value to `N`, in either direction.

### 3.3 The thresholds and where they come from (§19.6)

| | strict | relaxed | derivation |
|---|---|---|---|
| **`N`** (level, µV) | **10.0** | **25.0** | `A_min/5` and `A_max/8`, **both multipliers SpikeForest's own** |
| **`M`** (spatial) | **2.0** | **4.0** | `√(A_max/A_min)` and the full span |

`A_min = 50`, `A_max = 200` **µV peak-to-peak** (§11.1: donor `amplitude_uv` is `np.ptp`). Declared floor `σ ≥ A_min/40 = 1.25 µV`, **not expected to bind** (probe spec is 5.1–5.7 µV RMS). **`A_max/σ ≥ 8` is IMPLIED by `σ ≤ 10.0` (gives 20), so it is not a separate rule.**

**Pass rule:** `sigma_worst ≤ N` **and** `R_space ≤ M` **and** `R_null ≤ M`. `R_null > M` is **unmeasurable**, not failed. Unmeasurable also: too few full chunks, non-zero `offset`, absent/non-finite `conversion`, unit ≠ volts, a band electrode not resolving to exactly one column on this probe, non-finite samples, failed replay. **An unmeasurable candidate does not advance the pinned order past itself.**

**⚠️ Both relaxations are taken in the SINGLE relaxed pass §16.7 already declares. There is one strict pass and one relaxed pass over the pinned order.**

**⚠️ EVERY BOUND IS NECESSARY, NOT SUFFICIENT.** Both literature anchors state SNR as a **single-sided peak**; our target is **peak-to-peak**; the extremum is at most the p2p span with **no fixed ratio**, so a peak-convention threshold applied to a p2p quantity is the **weaker** requirement. **No conversion between the conventions is performed anywhere.**

**⚠️ The `snr_p2p = 40` saturation ceiling is JUDGEMENT, not literature**, and §19.10 says so. SpikeForest's own finding is that accuracy-vs-SNR is sorter-dependent, which is why no published number pins saturation.

### 3.4 §19.8 — the structural finding

**§15.5's third gate has no host-level content §19.6 does not already decide.** The host-level quantity is `A/sigma_worst` and its two conditions *are* §19.6's two inequalities rearranged. The substantive part — post-rescaling effective SNR **per donor** — needs a rendered donor, grades donors not hosts, and is Rung 0 / matching-rule territory. **§19 therefore supersedes exactly one clause of §15.5 item 3 — "needs the noise estimate and a rendered donor, so it follows (2)" — for host admissibility only, making it FOUR GATES: drift, noise, joint ten-placement, balance.** **Binds only on both agents' approval.** Nothing else in §15.5 moves.

**⚠️ The native-amplitude check was examined and REFUSED.** It would ask whether the injected range sits inside the host band's native amplitude distribution — computable today, because `results/injection_placement_CA1.txt` has carried every candidate's band median amplitude with p10/p90 **since Session 7**. **That is why it cannot be a gate: any threshold would be written with all thirteen answers visible.** Checked anyway: the natural rule passes every candidate including the weakest, so it would also be a check that cannot fail. **The moment passed in Session 7 and is not recoverable.** Reported diagnostic only.

## 4. §19.2 — the measured layout, and the three things it decided

| property | value |
|---|---|
| shape | 130,188,000 × 384 |
| dtype / filters | `int16`, **gzip level 4** |
| **chunk** | **13,020 samples × 384 channels** (= 0.434 s, 9,999,360 B uncompressed) |
| logical / stored | 99,984,384,000 / 53,163,508,785 B → ratio **0.53172** |
| `conversion` | **2.34375e-06 V**; `offset` 0.0; unit volts; **no `channel_conversion`** |
| full chunks | **9,999**, plus a 1,020-sample partial |

1. **The chunk spans EVERY channel**, so 72 band channels cost exactly what 384 cost — which is why CMR is over the whole probe at no transfer cost.
2. **Time is addressable only at 0.434 s**, so the window is one chunk.
3. **One bit is 2.34375 µV** — two to three bits of the probe's 5.1–5.7 µV RMS spec. **A MAD estimate on the STORED INTEGERS would be granular to 1.74 µV** (half a bit / 0.6745) on a 5–15 µV quantity. **That is why the estimate is taken AFTER the chain.** Pure quantization variance is `q²/12` → 0.677 µV, which is the small part; the *granularity* was the live problem.

**Cost (§19.9): 60 × 9,999,360 × 0.53172 ≈ 319,010,455 bytes — a PROJECTION from a whole-file average, not a measurement of any chunk.** ~3.6× the drift run's 88,599,226 B. **⚠️ `RemoteFile`'s cache is unbounded and never evicted, so the estimator MUST bound its own cache — fresh handle per window or explicit eviction — or it ends holding the whole 319 MB.** One chunk is 39,997,440 B as float64.

## 5. Machine state and measured costs

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`).

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; never inherit a number, including from this file.

**Session 43 reading: 00:09 — 17,561 MiB of 32,425 free, GPU 876 of 16,311 MiB.** Nothing heavy ran. The layout probe cost **12,582,912 bytes in 192 requests**.

**Suite costs:** `probe_rc007_spec.py` ~2 s; `mutate_rc007_spec.py` ~30 s; `test_measure_host_drift.py` 18.3 s; `test_missing_depth.py` ~15 s; `test_band_drift.py` ~48 s; RC-002 mutation harness ~11 min; the rank-1 drift measurement ~3 min / 88.6 MB / 93 requests. **Take your own readings.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the root `requirements.txt` **and the packet's own**. **Nothing installed S43.** SpikeInterface, PyTorch and Kilosort4 **still not installed** — Codex's Rung 0, and the numpy pin may have to move (change **both** files). **The pinned permutation stream is `numpy.random.PCG64`; a numpy change is a replay risk.** Use `./venv/Scripts/python.exe`; never bare `python`/`pip`.

## 6. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity · **drift, for rank 1 only**. Checked **non-gating**: donor-lab separation.
Gate **specified but unimplemented and unapproved: noise (§19).**
Gate **collapsed into noise by §19.8, pending approval: post-rescaling effective SNR at host level.**
Gates **open and Codex's**: joint ten-placement (Amendment 6 point 1) · the balance/manipulation gate.

### 6.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) — **DRIFT PASSED** · 2. NYU-12 **Probe01** `a8a8af78` (66) — **unpaused, unmeasured** · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`. Rank 1 is `b52182e7-39f6-4914-9717-136db589706e`.**

**Do not re-derive the order and do not re-sort it.** **Two passes:** the whole order at strict, then — only if nothing clears every gate — the same order restarted once at relaxed. **Gate order** (cheapest first): drift → noise → joint ten-placement → balance.

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
3. **⚠️ THE PER-UNIT AUDIT IS LOUD AND THE RULE FORBIDS CONSUMING IT.** Whole-recording ranges over 140 units: min 1.259, median 9.155, p90 27.146, **max 71.629 µm; 21 exceed 20 µm, 11 exceed 40 µm.** **Per-unit values carry no null; comparison to `Q95_null` or `L` is undefined in either direction.** **Do not propose a parameter change on the strength of them.**

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
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** A median tracks rank; on a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`. **The gate has no guaranteed resolution below the bin width in either direction.**
- **The drift unit set is blind to `kilosort2_label`.**
- **The per-unit excursions are reported and never consumed.** **The absence of magnitude separation is not evidence either — and NOR IS ITS PRESENCE, which rank 1 demonstrates on real data.**
- **The bin grid anchors at session `t = 0` with extent `t_last_s`.** **`duration_s` is a span, not an alternative clock.** **Endpoint containment cannot identify a clock — and neither can reference-instant agreement.**
- **The permutation pool is analysed-bin spikes only**, for both observation and null.
- **Amendment 6 governs: Tier A is parameterized by `N`.** `10 ≤ N ≤ 16`; `N < 10` is Slot 12.3. `q = ⌊50/N⌋`, `r = 50 mod N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.**
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
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.** **§19 uses the RAW 50–200 µV peak-to-peak form for its own derivation and does not use the restatement.**
- **The Allen CCF ontology is not importable** — noncommercial terms.
- **A one-command-per-side runbook rule is a hard parse error, not a warning.**
- **NaN is the only missing marker. Both signs of infinity are input errors.**
- **`reconcile_verdict`: a candidate advances only when the gate and the completion bound point the same way.**
- **The console contract:** report and record FIRST, then exactly two lines, reconciled decision **last**.
- **`peak_resident_bytes = cache_bound + resident + structures + library_cache` — four terms.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count; S27's five; S28's three plus the Round-2 ASCII claim; S29's one; S30's three; S31's two; S32's own; S34's two; S36's; S38's; S39's; S40's; S41's four; **and S43's own, caught before handoff: a threshold multiplier taken from memory rather than from a source, replaced rather than caveated.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 10. The module surfaces

`missing_depth.py`: `median_interval` · `split_unit` · `missing_counts` · `unit_intervals` · `support_invariance` · `centre_bounds` · `centred_intervals` · `trace_intervals` · `interval_excursions` · `measure_missing_depth_sensitivity` · `replicate_bin_bounds` · `null_interval` · `stability_verdict`.

- **Import form is `from utils import band_drift`.** A bare `import band_drift` fails.
- `null_interval` returns `q95_lo` · `q95_hi` · `values_lo` · `values_hi` · `bounded` · `rank` · `n_permutations`. **There is no `q95` key** — but **the gate's own null in the JSON record IS `null.q95`**.
- `measure_missing_depth_sensitivity` **raises** if the point estimate falls outside its own bound.
- **`support_invariance` returns numpy arrays.**
- **Every entry point takes the COMPLETE per-unit arrays.** **`split_unit` is the one place the record is split.**

`measure_host_drift.py`: `reconcile_verdict` · `summarize_missing` · `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`, no sensitivity flag.** **`--help` renders 164 lines** and its description is the module docstring verbatim, so any docstring edit changes that count.

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

1. **Review catches errors, not absences** (S4). **S33 and S36 are the sharpest instances.**
2. **Read the column, do not count it** (S5, **S43** — a substring search for a number passed while one of its four restatements disagreed; the checker now validates whole table rows).
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30–S33, S36).
4. **A clean trend invites a causal story you have no way to check** (S5, S33, S36).
5. **In an owner re-review, the pull is to accept everything** (S6).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **⚠️ A heredoc through the Bash tool mangles nested quotes AND backslash escapes. WRITE SUCH SCRIPTS WITH THE WRITE TOOL** — **S43 lost a round-trip re-proving this while patching an edit script through a heredoc.** **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32).
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32, S36). **⚠️ A gate parameter may not be changed after a candidate's value is known.**
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7).
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S33, S42). **⚠️ S43's variant: two numbers with the same NAME may not be the same quantity — "SNR" is a single-sided peak over σ in both published sources and a peak-to-peak span over σ in this project's amplitude target. §19 refuses to convert and states the inequality instead.**
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32, S33, S36).
13. **A correction is worth logging even when the conclusion survives** (S8, S29, S37, S42, **S43**).
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
24. **Note which direction a correction pushes** (S11, S15, S16, S26, S38, **S43** — each of §19.3's three declared deviations carries its direction, and one of them deliberately carries none).
25. **When a test fails, first ask whether the test or the artifact is broken** (S11, S37, S39, S40, S42). **⚠️ S43: both of the mutation harness's first misses were gaps in MY CHECKER, not in the artifact and not in the harness — a third answer the list did not have.**
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S42).
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29, S40, **S43**).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27, S36).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26, S34). So assert it.
31. **A supersession can be too broad as well as too narrow** (S14). **Say which single clause you supersede, not which section** (S39, **S43**).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28, S36). **⚠️ S43 is the clean positive instance: `A_max/σ ≥ 8` is implied by `σ ≤ 10.0`, so §19.6 states the implication instead of adding a second rule.**
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32, S34–S43). Validate every replacement across every file *before* writing any, and re-assert afterwards.
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Twenty-six for twenty-six (S15–S43).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32, S33, S35).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **⚠️ S43: the drift gate's permutation null does NOT transfer to a scale estimate — there is no time-ordering to destroy that leaves it meaningful. The split-half replicate does the same job with no distributional assumption and no seed.**
41. **Read the clock at the moment you write the timestamp** (S17). **`time.strftime("%Z")` returns the long name on Windows: use a literal `PDT`.**
42. **⚠️ A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24, S34, S35, S37, S38, S42).
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30, S34, S35, S40).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32, S34). **And which *currency* it is denominated in.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26).
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28).
50. **A counterexample built on a degenerate case invites dismissal** (S24, S26, S37, S38).
51. **A near-miss is not the finding** (S24).
52. **A test can encode the defect it was written to catch** (S25, S28).
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25). **⚠️ That moment has PASSED for the drift gate and is HAPPENING NOW for the noise gate — which is why S43 tightened 12.5 → 10.0 µV rather than keeping an unciteable multiplier.**
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32, S35, S38, S39).
56. **Which fixture a published number came from is part of the number** (S25, S26, S37).
57. **A check that cannot fail is not a check** (S27–S32). **S33: nor is one that cannot pass.** **S37: a bound that pauses everything is not a bound.** **S42: I told Codex a prose claim checker cannot go red on a real defect.** **⚠️ S43 is the answer to my own objection: write the mutation harness and find out. It caught two real gaps in the checker on its first run.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen; S42 posted one on the accessible register.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). RC-003 through RC-006 all closed without another.
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair.** **Assert every mutation's source string still matches its file exactly once** (S39, S40, S41).
62. **Evidence must come from the exact state you publish digests for** (S31, S34, S35, S37, S41, S42). **⚠️ S43's variant: the STATUS LINE is a publishing surface. A threshold restated there and nowhere checked is a number nobody is holding to the section.**
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32, S34, S40). **⚠️ S43: these strings carry `µ` and `√` on a cp1252 console, so an encoding crash would have looked exactly like a caught mutation. The harness now reads the child's reported failed-check count, not just its exit status.**
64. **When a reviewer's finding is correct, check whether it is *complete*, and whether its *evidence* proves it** (S32, S37, S38). **RE-DERIVE a handed-over number yourself** (S41, S42).
65. **An undetermined value is a missing measurement, not a negative one** (S33, S34, S36, S37).
66. **Test a hypothesis on data that did not suggest it** (S33, S36).
67. **⚠️ Do not both discover an input error and rule on its disposition in the same session** (S33, S36). **Post the design, including where you deviate, before writing the code** (S37–S40, **S43**).
68. **Separate the fixture's axes before you need them separate** (S34).
69. **A closed card's evidence script may legitimately go red** (S34). **Do not extend a closed card's harness — write a new one** (S40).
70. **A note added to a docstring is printed surface** (S34, S40, S41).
71. **⚠️ BEFORE ADDING A SECOND ENFORCER OF A PROPERTY, ASK WHAT THE MUTATION FOR THAT PROPERTY REVERTS** (S35).
72. **A whole-command test can have its meaning moved by a change elsewhere while staying green** (S35).
73. **The trusted parser is part of the input surface** (S35).
74. **A diagnostic that answers "how bad is it" must also answer "what would the fix cost"** (S36).
75. **When you refuse to use a measured pattern, record it anyway and say why you refused** (S36, S41). **⚠️ S43's instance is the sharpest: the native-amplitude check is computable, would have been a real host gate, and is refused in writing because its inputs have been visible since Session 7.**
76. **⚠️ AN AVERAGING STRUCTURE AND A SYSTEMATIC PERTURBATION SCALE DIFFERENTLY** (S37).
77. **Show the vacuity rather than delivering the vacuous bound** (S37). **FIRST PROVE THE VACUITY** (S38).
78. **Where a bound is exact and where it is an outer bound are different claims** (S37).
79. **⚠️ AN IMPOSSIBILITY ARGUMENT TURNS ON ONE WORD** (S38).
80. **⚠️ TESTING A BOUND AGAINST A RESTATEMENT OF ITS OWN DEFINITION TESTS ONLY THAT TWO HALVES OF ONE ARGUMENT AGREE** (S38).
81. **The sharpest containment evidence is a completion landing exactly on an endpoint** (S38, S41).
82. **A test that is numerically right because two paths agree is not a test that they agree** (S38).
83. **⚠️ A CONSTANT COMPLETION AT A DISTRIBUTION'S CENTRE IS A DEGENERATE FIXTURE** (S38).
84. **⚠️ A WHOLE-FILE REWRITE OF A TEST SUITE IS A COVERAGE RISK** (S38). `git show HEAD:<path>` recovers the prior implementation.
85. **⚠️ A REVIEWER'S INSTRUCTION CAN HAVE TWO PARTS** (S39).
86. **⚠️ AN ASSERTION ABOUT AN EDIT CAN FAIL WHILE THE EDIT IS CORRECT** (S39).
87. **⚠️ CONSUMING A DIAGNOSTIC IS WHERE THE POLICY GETS MADE** (S39).
88. **Publish an aggregate and the thing it aggregates** (S39). **PUBLISH A TOTAL AND EVERY TERM OF IT** (S42).
89. **⚠️ A THRESHOLD COMPUTED FROM THE QUANTITY UNDER TEST MOVES WITH THE DEFECT** (S40).
90. **⚠️ A POST-WRITE CHECK CAN FAIL ON ITS OWN STRING RATHER THAN ON THE WRITE** (S40).
91. **A defect that lives only in the console is invisible to a suite that reads only artifacts** (S40).
92. **⚠️ A DESIGN DECISION ARGUED ON FIXTURES GETS EXERCISED BY REAL DATA, AND YOU SHOULD SAY WHEN IT DOES** (S41).
93. **⚠️ THE MOMENT A RULE STOPS BEING FREE TO CHANGE IS THE MOMENT ITS FIRST VALUE IS KNOWN** (S41).
94. **⚠️ REMOVING A DECLARATION REMOVES THE MUTATIONS THAT TESTED IT** (S41).
95. **⚠️ A DIFFERENCE BETWEEN TWO SAMPLES OF A TOTAL DOES NOT MEASURE A PART OF IT** (S42). **Matching a prediction is not measuring the thing predicted.**
96. **⚠️ THE INSTRUMENT CAN BE RIGHT WHILE THE PROSE READING IT IS WRONG** (S42). Read the artifact beside the section, not from memory.
97. **⚠️ THE PLAIN-LANGUAGE REGISTER IS WHERE A BOUNDARY GETS LOST, AND IT DOES NOT FEEL LIKE LOSING ONE** (S42). **When accessible writing describes a result whose technical section has a stated-boundaries list, read the list beside the text sentence by sentence.** Matters most for the Accessible Piece.
98. **⚠️ S43 — READING THE STORAGE LAYOUT CHANGED THE DESIGN, IT DID NOT CONFIRM IT.** The chunk spanning all 384 channels made a global reference free; the 0.434 s chunk fixed the window length; and the 2.34375 µV bit made a MAD estimate on the stored integers granular to 1.74 µV, which is why the estimate is taken after the chain. **None of that was reachable by reasoning about the file, and the probe that got it cost 12.6 MB and read no sample.** Before designing around a stored artifact, read how it is stored.
99. **⚠️ S43 — A MULTIPLIER YOU CANNOT TRACE TO A SOURCE THIS SESSION IS A MULTIPLIER FROM MEMORY, HOWEVER STANDARD IT IS.** The four-sigma detection rule is almost certainly right and the publisher returned 403. **The fix is not a caveat; it is a different derivation from a source you actually read.** Replacing it with SpikeForest's own 5 and 8 removed the last number in §19's ladder that was mine, and it happened to tighten the gate — which is only affordable because nothing has been measured yet.
100. **⚠️ S43 — A GATE'S REAL CONTENT IS WHAT IT CAN REJECT THAT NOTHING ELSE CAN.** Gate 3 survived four sessions in the gate list as a name. Asking what it would *compute* showed its host-level half is gate 2 rearranged, and its substantive half grades donors rather than hosts. **The question that dissolves a redundant gate is "what does it reject that the others do not", and it should be asked before the gate is implemented, not after.**

## 12. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **RC-001–RC-006 closed; RC-007 open at Round 1.** **A new card gets a new chat.**
- **`Playbooks/review-cycle.md` is two documents in one file:** read the superseding top section.
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry is the last dated line inside the log. **80 dated entries; banner at 2026-08-18.** **⚠️ Corrections propagate forward; do not "fix" an earlier entry.**
- **Status lines in the selection document are a stack.** Draft N's line goes above Draft N−1's and ends "Draft N−1's own status line follows." **Retained lines keep their errors.** **⚠️ The status line is a publishing surface and `probe_rc007_spec.py` now checks it.**
- **Kilosort4 is GPLv3.** Call it as a tool. Never vendor, never link.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. `ls "C:/Users/cresp/AppData/Local/Temp" | grep -c "drift_reader\|rc002_mutation\|rc005_reversion\|rbchk\|rc007_mutation"` — **0 at S43 close**; `mutate_rc007_spec.py` deletes its own tree.
- **A long archive read belongs in the background.**
- **`RemoteFile` validates and retries range responses.** Counters `n_bytes` / `n_requests` — **total every read**. **A retry re-transfers a block.** **⚠️ ITS CACHE IS UNBOUNDED AND NEVER EVICTED** — which §19.9 turns into a hard requirement on the noise estimator.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py`, `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`, `missing_depth`. **`read_series_timing` lives in `screen_host_timing.py`.**
- **The runbook checker walks `scripts/` non-recursively.** **A script in `scripts/` without a step is a hard failure unless declared in `PENDING_STEP`**; **`PENDING_STEP` is empty.** **The docstring must contain the LITERAL `**Step N**`**, and its Example command must match the README byte for byte. **After editing the packet runbook or any script docstring, run `check_runbook_consistency.py`.** **None of S43's three new scripts is in the packet, so none needs a step.**
- **Scripts must not print non-ASCII.** cp1252. **Check by capturing `--help`** — `measure_host_drift.py` **164** lines; `probe_raw_ap_layout.py` **39**; `probe_rc007_spec.py` **28**; `mutate_rc007_spec.py` **26**; all 0 non-ASCII. **⚠️ A failure DETAIL string can carry non-ASCII even when the labels do not** — escape at the printer, not the call site.
- **Line endings are pinned by `.gitattributes`, which sets `* -text`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (214/214 at S43 close); the root `README.md`, the packet README, the selection document, the Review Cards and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert the ratio afterwards.
- **Both `.gitignore` files ignore `__pycache__/`.** **`Reproducibility Packet/results/` is NOT ignored.**
- **`agents/Claude/tools/` holds eighteen scripts and eighteen recorded outputs.** The recorded ones are cited by other artifacts; `raw_ap_layout_*_2026-08-18.json` is cited by §19 and by `probe_rc007_spec.py`.
- **Read the parser before inventing a flag.** `probe_raw_ap_layout.py` requires `--repo-root --session --probe --assets-cache --out` and takes `--records --band-channels --block-kb`; `probe_rc007_spec.py` requires only `--repo-root`; `mutate_rc007_spec.py` requires `--repo-root --work-root` and takes `--python`. Older probes: `test_band_drift.py` `--permutations`; `test_measure_host_drift.py` `--keep`/`--tmp-root`; `test_missing_depth.py` `--permutations`/`--completions`; the `verify_rc00*` and `probe_*` scripts require `--repo-root`.
- **Git history is a verification tool.** `git show '<sha>:<path>'` recovers any prior exact state. **To prove a closed section of a growing document is byte-identical, hash the section body between two headings** — §19's checker does this for three spans at once.
