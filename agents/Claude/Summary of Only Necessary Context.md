# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 40 · 2026-08-17 05:34 PDT**
**Next session is Claude Session 41. No count-based progress report is due** (they fall at 8, 16, 24, 32, 40, **48**). A phase transition or an approved amendment would still trigger one.

## 0. WHAT THIS SESSION DID, IN ONE PARAGRAPH

**Codex returned RC-005 Round 1 as `Revisions Required` with two blockers, both in the wiring rather than the mathematics; Session 40 repaired both on one state and handed it back for a delta review.** F1: the command's last console line reported the point gate after reconciliation had already paused the candidate. F2: the pre-read resident bound omitted the per-spike positional masks the reader retains — 3,160,311 bytes at rank 1. Evidence: **543 checks 0 failed** (was 518), 86 and 103 unchanged, **32 of 32 RC-002 mutations**, and a new reversion harness at **4 of 4**. **Nothing was measured, no archive was read, and ranks 1 and 2 stay paused and keep their rank until RC-005 closes with same-state approval.**

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

**Outcomes are `Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required`. `Escalated` was removed.** At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**. **Evidence determines what may ship; consensus determines what happens next. Underdetermined evidence is not resolved in favour of approval.**

**RC-001 `Approved`. RC-002 `Revisions Required` (first Convergence Decision, S30). RC-003 `Approved` at Round 3. RC-004 `Approved` at Round 2 (S36). RC-005 is OPEN: Round 1 `Revisions Required` (Codex, 2026-08-17 04:18 PDT), Round 2 handed back S40 and awaiting his delta review.**

**⚠️ RC-005 IS ON ITS SECOND OF AT MOST THREE ROUND-TRIPS.** A third without both approvals freezes the state and triggers a Convergence Decision.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six. **Nothing this session needed an amendment**: both repairs live in §17 of the selection document and in the card.

**⚠️ This file describes the moment it was written.** Codex has now nineteen times posted a handoff within the hour after a session closed. **Read the active chat before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, and no candidate has cleared any open gate.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 26, `3e587874fdce355a4d605861f1ddfd0b1481a766385c2084e37d12db6d44100a`. §17 IS IN RC-005's SCOPE. §1–§16 byte-identical: the 143,890 bytes from `## 1.` to `## 17.` hash to `700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59` in both `HEAD` and the tree. Do not reopen §1–§16.** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **`eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` — approved, closed, untouched and verified so.** |
| `agents/Claude/tools/test_band_drift.py` | `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` — approved. Re-run S40: 103 checks, 0 failed. |
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `ef9740279f018e0b663e5d407f5297331fa17fe9042b18f2b477dc6c2233b988` — **unchanged in Round 2.** |
| **`Reproducibility Packet/scripts/utils/archive_units.py`** | **`ed0766f2d3e6399a4a28f5289159b948cc907ed8ee72055314b0f363d515ec3a` — CHANGED by F2.** |
| **`Reproducibility Packet/scripts/measure_host_drift.py`** | **`26934a6b862be6f0cf7b269346ff85c4c2fd9f5ab056a77d427bc9059d39370e` — CHANGED by F1, F2's printing and the docstring.** |
| `agents/Claude/tools/test_missing_depth.py` | `435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` — unchanged; 86 checks, 0 failed at 200/200. |
| **`agents/Claude/tools/test_measure_host_drift.py`** | **`79c9bb5c3c04bdba66dcbcca9cf092d0b611d19b9ff526edcfeb8ed596c04335` — 543 checks, 0 failed, 18.6 s. Superseded 518.** |
| **`agents/Claude/tools/verify_rc005_round2_repairs.py`** | **NEW. `4f27b70c35f28f715d93ac214aebf0c01f4f4af2f958fb05b373132c8a013bee` — 4 of 4 reversions caught, control green.** |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `97860ad978bf6bd2fd6851033405c7b9e1cf51aacb0c44332344fd64d92bcf49` — **re-run S40: 32 of 32, control passes.** |
| `Reproducibility Packet/README.md` | Unchanged. **10 steps agree, `measure_host_drift.py` still `PENDING`.** Checker re-run S40, exit 0. |
| Root `README.md` | **74 dated log entries**, banner at 2026-08-17. |
| `Review Cards/RC-005 …` | **Open, Round 2 handed back.** Seven files in the candidate table. |

## 2. The first thing to do next session

**Read `chats/Claude-Codex/Missing Depth Recovery Review/` before anything else.** My Round-2 handoff is the last message.

- **`chats/Claude-Codex/Missing Depth Recovery Review/` — active, on Codex.** RC-005 Round 2, delta-only against F1, F2 and repair regressions.
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active** by Randy's request. Nothing pending there.
- **All twelve other chats are concluded.** `Non-Finite Spike Depths`'s `Summary.md` carries four of Codex's rulings and is RC-005's context.

**When RC-005 closes with same-state approval, in order:**

1. **Unpause ranks 1 and 2** and run the rank-1 drift measurement against the archive. §6.2 has the exact command. **Measure free RAM against `peak_resident_bytes` immediately beforehand**; 3–7 minutes and 55–67 MB; `run_in_background`.
2. **When it produces a report, the drift command becomes runbook step 11**: add the README step, **remove its entry from the checker's `PENDING_STEP`** (a script that is both a step and pending is a hard failure, and a mutation proves it), and re-run `check_runbook_consistency.py`.

**If Codex returns `Revisions Required` again:** that is the third round-trip, so a Convergence Decision may follow. **And ask whether the layer should be simpler rather than repairing it a third time** — that commitment is written into `Progress Report Session 40.md`, so it is not only here. **Re-run the mutation harness after every repair** (§11 finding 61) **and `verify_rc005_round2_repairs.py`**; both cover the changed files.

## 3. The design, as it now stands

### 3.1 The per-bin interval is exact — unchanged since S37

Finite depths `x_(1) ≤ … ≤ x_(n)` in a bin, `k` missing whose spikes fall in it. `N = n + k`; the median reads ranks `r1 = ⌊(N+1)/2⌋`, `r2 = ⌈(N+1)/2⌉`.

    lo = ( x_(r1−k) + x_(r2−k) ) / 2      unbounded below when r1 − k < 1
    hi = ( x_(r1)   + x_(r2)   ) / 2      unbounded above when r2 > n

**This is the attainable set, not a bound** — brute-forced over 126 parameter cases at zero endpoint slack. An empty `values` with `k ≥ 1` returns `(−inf, +inf)`; empty with `k = 0` raises.

**A *finite* endpoint is reached by a real completion; an *unbounded* endpoint is reached by NONE**, because no completion places a value at infinity. What an unbounded side asserts is that every finite value on it is attainable — **which is why such a bin propagates as defined-but-unbounded rather than as absent.**

### 3.2 Support invariance — unchanged

**Every unit and bin must have the same inclusion status whether the missing samples are counted toward the floors or not** — all three floors, both ways. A violation makes the candidate **unmeasurable**. An equality, not a fitted tolerance. Both real candidates satisfy it (140/140 and 182/182 units, 0 bins lost).

### 3.3 The null bound is assumption-free — unchanged

`permutation_null` draws `rng.permutation(N)` from a seed derived from asset, probe, unit row and replicate index — and from `N`, which counts *spikes*. A spike whose depth is missing still has a good time, so **`N` and the seed are fixed before any missing value is chosen**, the whole source-to-destination map is known, and the unknown values sit in known source positions. Following them to their destination bins gives a known missing count per bin, where §3.1 applies.

**⚠️ S38's error, which cost a session: I claimed no such bound existed and the argument turned on treating `N` as something a completion could move.** Do not re-derive that argument.

**Two things the module states and must keep stating:** the finite-only null is **not** one of the completions when `k > 0`, and it is not claimed to lie inside the bound; and the bound is **exact per bin, an outer bound above it**.

### 3.4 The propagation above the bin — unchanged

Centring `[lo_ub − hi_cu, hi_ub − lo_cu]`, across-unit median `[median lo, median hi]`, window scan (upper `max hi − min lo`, lower `max(0, max lo − min hi)`, then the max over windows of each). **Interval arithmetic ignores the dependence, so above the bin this is an outer bound. The error runs one way — too wide, never too narrow.**

### 3.5 The decision rule — no fitted number anywhere

At threshold `L`: unbounded side or support-invariance violation → **unmeasurable**; `Dhi ≤ L` **and** `Qhi ≤ L` → **passes under every completion**; `Dlo > L` **or** `Qlo > L` → **fails under every completion**; otherwise → **decision-unstable, unmeasurable, candidate stays paused.**

### 3.6 The reader's disposition — Codex ruled it, S38→S39

**NaN is the only missing marker. Both signs of infinity are input errors. A non-finite time is an input error.** `read_band_units` returns the complete record plus `missing_depths` (bool mask) and `n_missing_depths` per unit. **The mask travels rather than being re-derived.**

### 3.7 ⚠️ `reconcile_verdict` IS MINE AND CODEX STILL HAS NOT RULED ON IT

The approved gate decides on the record held; the completion bound decides whether that survives every completion. **They can disagree — only through `Q95_null`.** **The rule: a candidate advances only when both point the same way; any disagreement is `unmeasurable` with `conflict` True.**

**Round 1's ledger is exhaustive by the method and raised nothing about it. I am reading that as UNOBJECTED, NOT as approved**, and I said so in the Round-2 handoff. If he would rather the gate's own number govern and the bound only pause, that is a small change — change the rule, not the report.

### 3.8 The layer engages only when something is missing

With `k = 0` its bounds collapse onto the gate's two numbers, proved elementwise across all 200 replicates by `zero_missing_reproduces_estimator`. **The guard is the reader's mask, not a flag.** The report states in words that the layer did not run and why.

### 3.9 NEW IN S40 — the console contract (RC-005 F1)

**The command writes the report and the JSON record FIRST, then prints exactly two lines and nothing after them:**

    [drift] point gate on the record held (diagnostic, not the decision): passed=... label=...
    [drift] decision: <disposition>; advances=<bool>; gate and completion bound conflict=<bool>

**The last line is the reconciled decision; the point gate says on its own face that it is a diagnostic.** The module docstring carries the contract (so `--help` renders it) and §17.9 carries it as specification. **Do not print anything after the decision** — the `--records` write moved above it for exactly that reason.

**Why this was a blocker and not cosmetics: every check we had read the saved artifacts, and the artifacts were correct.** A defect that lives only in the transcript is invisible to a suite that only opens files, and the host order is first-admissible, so acting on that line advances a candidate the layer refused to certify.

### 3.10 NEW IN S40 — the mask is charged (RC-005 F2)

`plan_transfer` charges `total_spikes * MASK_ITEMSIZE` into `resident_bytes` and publishes it as **`mask_bytes`**. **`mask_bytes` is a COMPONENT of `resident_bytes`, not a further term** — `peak_resident_bytes` is still `cache_bound + resident + structures + library_cache`, and a check asserts that. `MASK_ITEMSIZE = int(np.dtype(np.bool_).itemsize)`, taken from numpy rather than written as 1. The refusal message, the report decomposition, the console decomposition and the JSON record all name it. **3,160,311 bytes at the rank-1 band.**

## 4. The input convention — read this before touching the module

**Every entry point takes the COMPLETE per-unit arrays**: every spike's time, and a depth array of the same length with **NaN at the missing entries**. `measure_missing_depth_sensitivity(spike_times, depths, extent_s, params=None)` and `null_interval(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` mirror `measure_band_drift` and `permutation_null` exactly. **`split_unit` is the one place the record is split**, and the command calls it rather than masking by hand.

## 5. The public surfaces

`missing_depth.py`: `median_interval` · `split_unit` · `missing_counts` · `unit_intervals` · `support_invariance` · `centre_bounds` · `centred_intervals` · `trace_intervals` · `interval_excursions` · `measure_missing_depth_sensitivity` · `replicate_bin_bounds` · `null_interval` · `stability_verdict`.

- **Import form is `from utils import band_drift`.** A bare `import band_drift` fails.
- `centre_bounds(lo, hi)` is the **single definition** of the interval form of the centring step.
- `trace_intervals` and `centre_bounds` count a bin as defined with `~np.isnan`, **not** `np.isfinite`.
- `null_interval` returns `q95_lo` · `q95_hi` · `values_lo` · `values_hi` · `bounded` · `rank` · `n_permutations`. **There is no `q95` key.**
- `measure_missing_depth_sensitivity` returns `observed` · `measurable` (+`reason`) · `support` · `exclusions` and, when measurable, `delta_window_lo/hi` · `delta_full_lo/hi` · `window_start_hi` · `bounded` · `lo_trace` · `hi_trace`. It **raises** if the point estimate falls outside its own bound.
- **`support_invariance` returns numpy arrays** — not JSON-serializable; `summarize_missing` converts them, which is why it exists.

`measure_host_drift.py`: **`reconcile_verdict`** · **`summarize_missing`** · `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. Record carries `missing_depth` and `disposition`; the plan block now also carries **`mask_bytes`**. **No `--max-gap-um`, no `--threshold-um`, and no flag controls the sensitivity layer.**

`archive_units.py`: unchanged surface plus the new constant **`MASK_ITEMSIZE`**. Per-unit dicts carry **`missing_depths`** and **`n_missing_depths`**. **Constants unchanged:** `PROVENANCE_MAX_BYTES = 65536` · `PROVENANCE_BLOCK_BYTES = 65536` · `MEASURED_CONVERSION_VERSIONS = ("0.9.1","0.9.2","0.9.4")`, never gated · `UNITS_PATH = "units"` · `TIME_COLUMN = "spike_times"` · `DEPTH_COLUMN = "spike_distances_from_probe_tip_um"`. Transfer budget **393,216** at the pinned 64 KiB block. **Plan keys** include `peak_resident_bytes` and `mask_bytes`; **there is no key called `bytes`.**

- **`REFERENCE_TIME_FORM` gates the lexical shape before `fromisoformat` parses. ⚠️ THE UTC-OFFSET REQUIREMENT IS DELIBERATELY NOT IN THE GRAMMAR** — two independent enforcers would turn mutation F1L from CAUGHT to MISSED. **Do not "tidy" this.**

`band_drift.py` (unchanged, approved): `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** Symbol `Delta_10min`. Band keys `delta_full` / `delta_window` / `window_start`; `apply_gate` returns **`passed`**. Others: `bin_seconds` 60, `min_spikes_per_bin` 10, `min_bin_fraction` 0.8, `min_units_per_bin` 5, `n_permutations` 200, `null_percentile` 95, `master_seed` 3175830281, thresholds 20/40 µm.
- **`unit_traces` raises on non-finite depths** — which is *why* the command must split the record before calling the estimator.
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)`, **anchors at 0**. **Rank 2's `t_first_s` is −0.000047 s, so sub-zero exclusion is live.** **A recording needs at least 11 analysed bins**; rank 1 has 72, rank 2 has 82.

### 5.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires on every case that reaches a record that `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`. **Do not weaken this into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size** (S31). `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4` for exactly that reason.
3. **The provenance-budget invariant** (S32), on both assets, on every case that reaches a record.
4. **The fixture axes are separate on purpose** (S34): `write_raw` / `write_processed` take `provenance=` **and** `reference_time=` independently.
5. **`run_case(..., capture=False)`** (S35): with `capture=True` `result["stdout"]` is the transcript; otherwise **None**, not `""`. **S40: three whole-command missing-depth cases now pass `capture=True`.**
6. **`_nan_at(units, positions)`** sets NaN at **stated** `(unit, spike)` positions. **Do not switch it to a random draw.**
7. **NEW S40: `check_console_decision(h, prefix, transcript, disposition, advances)`** is the shared console assertion — last non-empty line is the decision, it carries no bare `passed=`, and the single line that does carry one contains `diagnostic`.
8. **NEW S40: `case_the_ceiling_counts_the_retained_masks`** builds its ceilings from the **fixture's spike count**, never from the plan under test. **Do not "simplify" it back to `peak_resident_bytes - mask_bytes`** — that version could not fail (see finding 89).

## 6. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 6.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs are in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`.**

**Do not re-derive the order and do not re-sort it.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

**⚠️ Four ranks — 5, 7, 9, 13 (NYU-65, NYU-45, NYU-39, NYU-48) — are PAUSED on the declared-clock disagreement, not rejected.**

**⚠️ RANKS 1 AND 2 ARE PAUSED UNTIL RC-005 CLOSES WITH SAME-STATE APPROVAL.** Not rejected; they keep their rank.

### 6.2 What rank 1's read established, and what it cost

**Confirmed working against the real asset, end to end up to the payload** (S36): raw provenance authenticated (`Created using NeuroConv v0.9.2`, **23,488** request bytes of 65,536 and **262,144** transfer bytes of 393,216); **the pair condition passes**; CA1 band **320.0–1020.0 µm, 72 channels**; AP extent `t_first 1.138489 s`, `t_last 4340.732689 s`; **174 band units of 756; 3,160,311 spikes**; payload **50,564,976 bytes**, transfer bound **59,040,736**, **`peak_resident_bytes` 128,825,196 (0.12 GB)** — **that figure predates S40's mask term; the new bound is about 3.16 MB higher, so re-read it from `--plan-only` rather than reusing this number.** **231 NaN depths in 11 units; 0 non-finite times.**

**The command, from inside the packet folder:**

`python scripts/measure_host_drift.py --session <uuid> --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

Add `--plan-only` for the sizing pass. **Measure free RAM against `peak_resident_bytes`, not `resident_bytes`.** **A full band read costs about 3–7 minutes and 55–67 MB; run it with `run_in_background`.** **It has still not produced a report.**

### 6.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Do not reopen §1–§16.** **Codex still owns the footprint/placement calibration**; do not start it.

## 7. What is still not done

1. **No host is pinned**, and that is correct.
2. **No candidate has a drift number.** Ranks 1 and 2 are paused on RC-005.
3. **§17 is written but unapproved.** It is RC-005's specification half, now at Draft 26.
4. **The capacity gate needs re-establishing** under Amendment 6's stricter condition.
5. **Five of the ten packet steps still have not been re-run** (the archive-reading ones).
6. **The preprocessing half of the amplitude question is untouched** — Rung 0 territory.
7. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question.
8. **`is_injectable` is a denylist over a partly derived vocabulary.** Latent: no consumer reads it.
9. **`probe_conversion_pairs.py` is not in the packet.** RC-004 tracked follow-up 1, still live, now joined by `probe_nonfinite_depths.py` and `probe_missing_depth_crossover.py`, whose numbers §17 cites.
10. **NEW: the command's unconditional finite-only split** retains a second pair of copies (≈50 MB projected at rank 1) even with nothing missing. **RC-005 tracked follow-up 1**, deliberately unrepaired: fixing it inside this round would widen `--max-mib`'s declared scope in the same round a term was found missing from it. **It must enter any later whole-command memory claim.**

## 8. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** · **the real-arm donor-matching rule** · **the exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 9. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`**, `G0` the mean paired sorter gap *in the control arm*. **Bounded-negative is the harder verdict.**
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins.** Inside-null is **not** a failure. **A claim that "the estimator would have caught it" must say *which of the two numbers*.** Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data **except a NaN depth (§17)**, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those pause the pinned order (§16.4).
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** A median tracks rank, so displacing `k` of a bin's `n` spikes upward moves its median **at most the displacement itself and at most the distance to the depth `k` ranks above it**. On a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`. **The gate has no guaranteed resolution below the bin width in either direction.**
- **The drift unit set is blind to `kilosort2_label`** and is selected by valid same-probe `max_electrode -> rel_y` inside the band. **The `mua` association among affected units is recorded and refused.**
- **The per-unit excursions are reported and never consumed.** **Never compare a per-unit value to `Q95_null` or to `L`.** **The absence of magnitude separation is not evidence either.**
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
- **⚠️ The daylight-saving reading of the 8 disagreeing sessions is DESCRIBED, NOT EXPLAINED. The same discipline applies to the centre-of-mass reading of the NaN depths** — and §17 says so in its own text.
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count; S27's five; S28's three plus the Round-2 ASCII claim; S29's one, which closed RC-002 unapproved; S30's three; S31's two; S32's own, the pair-equality condition that admitted 0 of 71; S34's two; S36's, that §16.7's support floors are sufficient to make a dropped depth safe; S38's, that no assumption-free bound on `Q95_null` exists; S39's, naming the wrong chat as RC-005's review channel; **and S40's, a memory-ceiling check whose threshold was computed from the quantity it was testing.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Session 40 readings: 05:08 PDT — 16,291 MB available physical of 32,425 (50% in use); GPU 1,056 of 16,311 MiB. At close 05:34 PDT — 16,004 MB, GPU 1,055 MiB.** **Nothing this session was heavy and no archive was read.** Suite costs: `test_missing_depth.py` ~15 s at 200/200; `test_measure_host_drift.py` 18.6 s; `verify_rc005_round2_repairs.py` ~1.7 minutes for 4 reversions plus a control; the RC-002 mutation harness **~11 minutes** for 32. **Do not inherit these; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. **Nothing was installed this session.** SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64`; a numpy change is a replay risk.** Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

**Network:** the archive is reachable and `RemoteFile` works against it. A session **metadata** pair costs about 1 MB and ~16 requests at a 64 KiB block, about 8 seconds. **A full band payload read costs 55–67 MB in 53–64 requests at the 1 MiB default block, and 3–7 minutes.**

## 11. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). **S33 and S36 are the sharpest instances.**
2. **Read the column, do not count it** (S5). **S33 inverts it — the thing needed had never been read at all.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30–S33, S36).
4. **A clean trend invites a causal story you have no way to check** (S5, S33, S36). Describe the pattern; do not publish the mechanism.
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?*
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and* backslash escapes, and breaks on a Python file containing `'''`. ⚠️ S40 adds backticks: a `` ` `` inside a double-quoted Bash string is command substitution, and it silently deleted "`Revisions Required`" from a file I wrote that way. Write such scripts with the Write tool instead.** Write the message to a scratch file with a `__STAMP__` placeholder, substitute the clock reading at write time, assert the header appears exactly once, and assert no CR appeared in an LF transcript. **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32).
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32, S36).
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7). **Run the probe they hand you, unmodified, before editing — and again after.** **S40 did the "after" half and had to read its result carefully: one of its two flags flipped because the defect's *home* was deleted, not because the replacement was inspected.**
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S33).
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32, S33, S36).
13. **A correction is worth logging even when the conclusion survives** (S8, S29, S37). **S38 is the inverse: S37 kept his conclusion and killed his evidence; S38 kept my design and killed my *reason*.**
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9, S15).
16. **An audit must use the same key its lookup uses** (S9, S27, S28, S31).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10).
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17, S23, S28, S29).
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11, S27–S29). **S33: and a *rule* you have not executed against real input is the same guess wearing a test suite.**
24. **Note which direction a correction pushes** (S11, S15, S16, S26, S38).
25. **When a test fails, first ask whether the test or the artifact is broken** (S11) — **S37's third possibility, that the *expectation* is broken; S39's fourth, that the *assertion about the edit* is broken while the edit is fine; and S40's fifth, that the *checker's own string* is wrong** (finding 90).
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S40).
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29, **S40**).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27, S36). **S38–S39: NaN is missing, `±inf` is an input error — that is a policy, it is flagged as one, and it is enforced at the reader as well as in the layer.**
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26, S34). So assert it.
31. **A supersession can be too broad as well as too narrow** (S14). **S39: so say which single clause you supersede, not which section.**
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28, S36).
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32, S34–S40). Validate every replacement across every file *before* writing any of them, and re-assert afterwards.
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Twenty-three for twenty-three (S15–S40).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32, S33, S35).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.** **S37: a null built by averaging across units cannot bound a perturbation common to those units.**
41. **Read the clock at the moment you write the timestamp** (S17). **`time.strftime("%Z")` returns the long timezone name on Windows: use a literal `PDT`.**
42. **⚠️ A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24, S34, S35, S37, S38). **Check the chat rows every session.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30, S34, S35). **S40's application: the paused fixture would be satisfied by a decision line hard-coded to `unmeasurable`, so the clean and bounded fixtures assert the other two outcomes.**
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32, S34). **And which *currency* it is denominated in.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26).
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28).
50. **A counterexample built on a degenerate case invites dismissal** (S24, S26, S37, S38).
51. **A near-miss is not the finding** (S24). Sweep the parameters to establish the regime exists.
52. **A test can encode the defect it was written to catch** (S25, S28). **A harness written from the implementation confirms the implementation.**
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25).
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32, S35, S38, S39).
56. **Which fixture a published number came from is part of the number** (S25, S26, S37).
57. **A check that cannot fail is not a check** (S27–S32). **S33: a check that cannot *pass* is not a check either.** **S37: a bound that pauses everything is not a bound.** **S39: a safety layer nobody has seen change an outcome is not evidence it can.** **⚠️ S40 is the sharpest instance yet — see finding 89.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen between them.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). **RC-003 and RC-004 then both closed `Approved` without needing another.**
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair.** **Cheap precaution before spending eleven minutes: assert every mutation's source string still matches its file exactly once** (S39, S40 — and S40 built that check into the new harness as `check_anchors`).
62. **Evidence must come from the exact state you publish digests for** (S31, S34, S35, S37). **S40: this is why an in-flight mutation run was killed and restarted after a docstring edit rather than reported against superseded bytes.**
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32, S34). **S40: the new harness's first run reported 4 MISSED against a suite that had genuinely gone red, because its expectation matcher captured `\S+` and our check names contain spaces.**
64. **When a reviewer's finding is correct, check whether it is *complete*, and whether its *evidence* proves it** (S32, S37, S38).
65. **An undetermined value is a missing measurement, not a negative one** (S33, S34, S36, S37).
66. **Test a hypothesis on data that did not suggest it** (S33, S36).
67. **⚠️ Do not both discover an input error and rule on its disposition in the same session** (S33, S36). **S37–S40: post the design, including where you deviate, before writing the code — and do not build the candidate on a decision the reviewer has not ruled on.**
68. **Separate the fixture's axes before you need them separate** (S34).
69. **A closed card's evidence script may legitimately go red** (S34). Do not edit its checks to make it green. **S40's corollary: do not extend a closed card's harness either — write a new one.**
70. **A note added to a docstring is printed surface** (S34, **S40**). `--help` renders it and this console is cp1252.
71. **⚠️ BEFORE ADDING A SECOND ENFORCER OF A PROPERTY, ASK WHAT THE MUTATION FOR THAT PROPERTY REVERTS** (S35).
72. **A whole-command test can have its meaning moved by a change elsewhere while staying green** (S35).
73. **The trusted parser is part of the input surface** (S35).
74. **A diagnostic that answers "how bad is it" must also answer "what would the fix cost"** (S36).
75. **When you refuse to use a measured pattern, record it anyway and say why you refused** (S36).
76. **⚠️ AN AVERAGING STRUCTURE AND A SYSTEMATIC PERTURBATION SCALE DIFFERENTLY** (S37).
77. **Show the vacuity rather than delivering the vacuous bound** (S37). **⚠️ S38's qualification: FIRST PROVE THE VACUITY.**
78. **Where a bound is exact and where it is an outer bound are different claims and both have to be stated** (S37).
79. **⚠️ AN IMPOSSIBILITY ARGUMENT TURNS ON ONE WORD — FIND IT BEFORE YOU PUBLISH THE ARGUMENT** (S38). **Most of the inputs to a seeded computation are not the adversary's to vary.**
80. **⚠️ TESTING A BOUND AGAINST A RESTATEMENT OF ITS OWN DEFINITION TESTS ONLY THAT TWO HALVES OF ONE ARGUMENT AGREE** (S38). **Whenever a test says "computed independently", ask independently *of what*.** **S40 is the second instance and it is in a memory bound rather than a statistical one — see finding 89.**
81. **The sharpest containment evidence is a completion landing exactly on an endpoint** (S38).
82. **A test that is numerically right because two paths agree is not a test that they agree** (S38).
83. **⚠️ A CONSTANT COMPLETION AT A DISTRIBUTION'S CENTRE IS A DEGENERATE FIXTURE** (S38).
84. **⚠️ A WHOLE-FILE REWRITE OF A TEST SUITE IS A COVERAGE RISK** (S38). `git show HEAD:<path>` recovers the exact prior implementation.
85. **⚠️ A REVIEWER'S INSTRUCTION CAN HAVE TWO PARTS, AND IMPLEMENTING THE FIRST WELL IS NOT EVIDENCE YOU READ THE SECOND** (S39). **When a handoff names a deliverable, enumerate its parts before starting and check them off at the end.**
86. **⚠️ AN ASSERTION ABOUT AN EDIT CAN FAIL WHILE THE EDIT IS CORRECT** (S39). **Assert `written.count(old) == new.count(old)`, never `== 0`.**
87. **⚠️ CONSUMING A DIAGNOSTIC IS WHERE THE POLICY GETS MADE** (S39). **A layer that only reports has not yet made its hard decision.**
88. **Publish an aggregate and the thing it aggregates, in the same artifact** (S39).
89. **⚠️ S40 — A THRESHOLD COMPUTED FROM THE QUANTITY UNDER TEST MOVES WITH THE DEFECT.** The mask-ceiling case set `max_bytes = plan["peak_resident_bytes"] - plan["mask_bytes"]` and required a refusal. Revert the mask term and the plan's own peak drops by the same amount, so the ceiling drops with it and the read is refused anyway: **the check passed in both worlds and was measuring nothing.** The boundary must come from the fixture — here the spike count and the column item sizes — which no defect in the code under test can move. **General form: any "just below / just above" test must build its boundary out of inputs, never out of the output it is bounding.** It was caught by the reversion harness on its first run, not by reading the code.
90. **⚠️ S40 — A POST-WRITE CHECK CAN FAIL ON ITS OWN STRING RATHER THAN ON THE WRITE.** The chat-append script built its heading as `"## RC-005 Round 2 - both …".replace("-", "—", 1)`, which replaced the hyphen inside `RC-005`; the append was correct and the verification reported zero occurrences. **Build a checker's expected string as a literal, not by transforming another string**, and when a post-write check fails, read the file before touching anything.
91. **S40 — a defect that lives only in the console is invisible to a suite that reads only artifacts.** Every check for the missing-depth layer opened the JSON record or the report, all of which were correct, while the transcript ended in the opposite verdict. **When a command's output has two surfaces, the acceptance evidence has to cover both**, and `run_case(capture=True)` is how this suite does it.

## 12. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **RC-001–RC-004 closed; RC-005 open at Round 2.** **A new card gets a new chat** (finding 85).
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section.**
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry landed inside the log section. **74 dated entries by `grep -c "^- \*\*2026-08-1"`; banner at 2026-08-17.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link.
- **Corrections propagate forward, never backward.** The review cycle is the only exception.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. `ls "C:/Users/cresp/AppData/Local/Temp" | grep -c "drift_reader\|rc002_mutation\|rc005_reversion\|rbchk"` is the check — **0 at S40 close.** **The RC-002 mutation harness takes ~11 minutes for 32 mutations — run it with `run_in_background`, and its stdout is buffered when redirected so the log stays empty until it finishes.** **⚠️ Do not edit any file the harness copies while it is running** — `measure_host_drift.py`, `archive_units.py`, `test_measure_host_drift.py`. **S40 killed a run rather than edit under it, and cleaned the abandoned tree by hand.**
- **`test_measure_host_drift.py` takes `--keep` and `--tmp-root`**, which is how to get a real report out of a fixture case. **Delete the kept tree afterwards.**
- **A long archive read also belongs in the background.** `tail` the log or arm a Monitor rather than polling.
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **total every read rather than the last one.** **A retry re-transfers a block, so `n_bytes` can exceed the file size.** **The reader's cache is unbounded and never evicted.**
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`, `missing_depth`. **`read_series_timing` lives in `screen_host_timing.py`.**
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` needs no step. **A script in `scripts/` without a step is a hard failure unless it is declared in `PENDING_STEP`**, and a script that is both a step and pending is also a failure. **After editing the packet runbook or any script docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **`mutation_test_runbook_checker.py` takes three positional arguments**, not flags: packet path, scratch directory, interpreter.
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. **Check the printed surface by capturing `--help`** — 165 lines at S40, 0 non-ASCII. **Values read out of an asset are not yours** — render them through `archive_units.ascii_safe`.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (197/197 at S40 close, five rows added); the root `README.md`, the selection document, the Review Cards and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert the CRLF/LF ratio afterwards.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path and comparing file by file, then deleting the clone.
- **Both `.gitignore` files carry a do-not-catch-these comment and ignore `__pycache__/`.**
- **`agents/Claude/tools/` holds fourteen scripts and thirteen recorded outputs.** The recorded ones are cited by other artifacts: `source_count_granularity_probe_2026-08-13.txt` by the matching rule, the four `conversion_pairs_*_2026-08-16` files plus their two session lists by RC-004, the four `nonfinite_depths_*_2026-08-16` files **and both `missing_depth_crossover_*` files by §17.**
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations`; `probe_band_drift_claims.py` takes `--module`; `test_measure_host_drift.py` takes `--keep` and `--tmp-root`; `test_missing_depth.py` takes `--permutations` (default 40) and `--completions` (default 120); `mutate_rc002_repairs.py`, `verify_rc003_round1_repairs.py`, `verify_rc003_round2_repairs.py`, **`verify_rc005_round2_repairs.py`** (also `--work-root`, `--python`, `--keep`), `probe_nonfinite_depths.py` and `probe_missing_depth_crossover.py` require `--repo-root`; `probe_conversion_pairs.py` requires `--assets-cache`, `--out`, and one of `--sessions` / `--sessions-file`; Codex's probes all require `--repo-root`.
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state. `git checkout -- <path>` is the clean way to undo a mangled edit script. **To prove a closed section of a growing document is byte-identical, hash the section body between two headings** — `git diff --numstat` alone cannot, because a status line prepended above §1 counts as an insertion in the same file.
