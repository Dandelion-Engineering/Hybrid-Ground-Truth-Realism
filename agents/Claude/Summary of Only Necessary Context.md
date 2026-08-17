# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 38 · 2026-08-17 01:30 PDT**
**Next session is Claude Session 39. No count-based progress report is due** (they fall at 8, 16, 24, 32, **40**). A phase transition or an approved amendment would trigger one anyway.

## 0. WHAT THIS SESSION DID, IN ONE PARAGRAPH

**Codex ruled that my impossibility claim was false — an assumption-free bound on the gate's null *does* exist — and he was right. I found the exact word my argument turned on, replaced the counterfactual with the completed-`N` permutation bound, and changed the module's input convention so the missing samples' positions are input rather than reconstruction.** My argument rested on treating `N`, the analysed-bin spike count, as something a completion could move. It cannot: a spike with a missing depth is still a spike with a good time, so `rng.permutation(N)` is fixed by seed and `N` before any missing value is chosen, the unknowns sit in known source positions, and following them to their destination bins gives a finite bound with nothing assumed. **The corrected bound is *wider* than my counterfactual, so the layer bites at roughly half the missingness I reported last session.** 86 checks, 0 failed at the pinned 200 permutations. **Nothing is wired, nothing is carded, and the pinned order is still paused at rank 1.**

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

**Outcomes are `Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required`. `Escalated` was removed.** At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**. **Evidence determines what may ship; consensus determines what happens next. Underdetermined evidence is not resolved in favour of approval.**

**RC-001 `Approved`. RC-002 `Revisions Required` (first Convergence Decision, S30). RC-003 `Approved` at Round 3. RC-004 `Approved` at Round 2 (S36). No card is open.** **RC-005 is expected and still does not exist** — see §2.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six. **Nothing this session needs an amendment**: the non-finite question lives in §16.8 of the selection document, not in the Claim Sheet.

**⚠️ This file describes the moment it was written.** Codex has now seventeen times posted a handoff within the hour after a session closed. **Read the active chat before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, and no candidate has cleared any open gate.** What is new: the missing-depth safety layer now bounds **both** gate numbers with nothing assumed, and the null half of it is a different construction from the one Session 37 shipped.

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 24, `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`. §1–§16 SAME-STATE APPROVED and unchanged. Do not reopen them. §17 does not exist yet and is owed** — see §2. |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **`eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` — approved, closed, untouched this session and verified so.** |
| `agents/Claude/tools/test_band_drift.py` | `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` — approved, closed. **Re-run this session: 103 checks, 0 failed.** |
| `Reproducibility Packet/scripts/utils/archive_units.py` | `9ef16f58cbd46ece7753406790a1b3d578efaf03df6311024c62e4c0e7b7e6e0` — RC-004 APPROVED, closed, unchanged. **Still raises on the first non-finite depth.** |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `156f6f0ffb0d13b7b3c871c29e7f516d93da65cadd4cbc742d7113fe132cf450` — RC-004 APPROVED, closed, unchanged. |
| `agents/Claude/tools/test_measure_host_drift.py` | `c508233d9c2d5c5567ca6875e8ebd22b1823b3ab7dff2aeac52044847305349a` — 82 cases, **472 checks**. **Not re-run this session; nothing it covers changed.** |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `97860ad978bf6bd2fd6851033405c7b9e1cf51aacb0c44332344fd64d92bcf49` — 32 of 32, ~9–10 minutes. **Not re-run this session; it does not cover `missing_depth.py`.** |
| **`Reproducibility Packet/scripts/utils/missing_depth.py`** | **`5a9cfde418069799ce159ce3d25890004bdff6f95f8b8f75fc99ab51833ea17c` — REWRITTEN. Not wired, not carded.** |
| **`agents/Claude/tools/test_missing_depth.py`** | **`435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` — 86 checks, 0 failed; 4.4 s at defaults, 15.0 s at `--permutations 200 --completions 200`.** |
| **`agents/Claude/tools/probe_missing_depth_crossover.py`** | **`57554ac16d8080e52db7afefadad85235baecfc20aecfb20accd611b71685c10` — updated to the new API. Two recorded outputs now; the 2026-08-16 one is superseded and kept.** |
| `agents/Claude/tools/probe_nonfinite_depths.py` | `ade3660f3d744e07fae8326f04508c157f47cfbe50313079c983caacc5bb52f1` — the S36 census. Two recorded outputs. |
| `agents/Codex/tools/probe_missing_depth_actual_null.py` | `d1fdfefae8d9b3f0bdfbc8e9de25c82f7ddae83688855c0a2482d4af8cac09b1` — **his S37 evidence. I ran it unmodified first: 8/8 at 200. Against the new module it now raises a `TypeError` on check 8, because that check compares against the counterfactual and the counterfactual is gone. I did not edit it.** |
| `Reproducibility Packet/README.md` | Unchanged. **10 steps agree, `measure_host_drift.py` still `PENDING`.** Checker re-run this session, exit 0. |
| Root `README.md` | **71 dated log entries**, banner at 2026-08-17. |

## 2. The first thing to do next session

**Read `chats/Claude-Codex/Non-Finite Spike Depths/` before anything else. My Session-38 message is the last thing in it.**

- **`chats/Claude-Codex/Non-Finite Spike Depths/` — active, on Codex.** He owes confirmation that the null replacement is what he asked for, plus a ruling on **two decisions of mine** (§3.4).
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active** by Randy's request. Nothing pending there.
- **All eleven other chats are concluded.**

**Once he confirms**, the remaining work before RC-005, in order —

1. **`archive_units.read_band_units` must stop raising on a non-finite depth** and return the complete record with a **missing-position mask**, not the missing times. Times alone cannot resolve two spikes that share a time, and the null bound reads positions. A non-finite **time** still raises. **If Codex accepts §3.4(a), the reader raises on an infinite depth too.**
2. **`measure_host_drift.py`** publishes exclusions **per unit, per bin and in total**, reports the interval and consumes `stability_verdict`. It already computes the finite-only null for the gate; pass that through rather than recomputing it. Its report gains lines; `--gate` still resolves the threshold and no number that decides a verdict becomes typeable.
3. **Write §17 of the selection document** — the disposition, the support-invariance condition, the **assumption-free** null argument (not a counterfactual), and the outer-bound honesty note. **Do not edit closed §16.8.** The fixture to put in §17 is still `gate_passing_counterexample`.
4. **Open RC-005 with the whole state as the candidate**, not the module alone. Codex asked for that explicitly.
5. **Re-run `mutate_rc002_repairs.py` and `test_measure_host_drift.py` after the reader repair.** S31, S32 and S35 all proved a repair can silently remove the coverage a mutation depends on.

## 3. The design, as it now stands

### 3.1 The per-bin interval is exact — unchanged from S37

Finite depths `x_(1) ≤ … ≤ x_(n)` in a bin, `k` missing whose spikes fall in it. `N = n + k`; the median reads ranks `r1 = ⌊(N+1)/2⌋`, `r2 = ⌈(N+1)/2⌉`.

    lo = ( x_(r1−k) + x_(r2−k) ) / 2      unbounded below when r1 − k < 1
    hi = ( x_(r1)   + x_(r2)   ) / 2      unbounded above when r2 > n

**This is the attainable set, not a bound** — brute-forced over 126 parameter cases at zero endpoint slack. **New in S38:** an empty `values` with `k ≥ 1` returns `(−inf, +inf)`, which is that bin's exact attainable set and is reachable once the null permutes. Empty with `k = 0` still raises.

### 3.2 Support invariance — unchanged

**Every unit and bin must have the same inclusion status whether the missing samples are counted toward the floors or not** — all three floors, both ways. A violation makes the candidate **unmeasurable**. An equality, not a fitted tolerance. Both real candidates satisfy it (140/140 and 182/182 units, 0 bins lost).

### 3.3 ⚠️ THE NULL BOUND IS ASSUMPTION-FREE, AND MY S37 ARGUMENT THAT IT COULD NOT BE WAS WRONG

**Carry this; it is the session's whole content.** I wrote that bounding over completions "would have to bound over arrangements, under which any bin can receive any subset of the pool." That is false, and the failure is one word: **I treated `N` as a quantity a completion could move.** It is a count of *spikes*, and a spike with a missing depth is still a spike with a perfectly good time. `permutation_null` draws `rng.permutation(N)` from a seed derived from asset, probe, unit row and replicate index — and from `N`. Both are known before any missing value is chosen. **So the whole source-to-destination map is fixed**, the unknown values sit in known source positions, and following them to their destination bins gives a known missing count per bin, where the exact interval of §3.1 applies. Nothing ranges over arrangements.

**Two things the module states and must keep stating:**

- **The finite-only null is not one of the completed records when `k > 0`.** It permutes `n` elements; every completion permutes `N`. It is the point diagnostic the gate itself computes and is **not claimed to lie inside the bound**. `null_interval` deliberately does **not** compute it — the command already has it, and recomputing would double a 200-replicate run.
- **Exact per bin, outer bound above it**, for the same dependence reason as the observation's, with the error one-directional.

### 3.4 Two decisions of mine that Codex has not ruled on

**(a) An infinite depth raises; it is not read as missing.** NaN means missing. `±inf` is a wrong value, not an absent one, and widening a bound around it would treat a corrupt number as unknown. The S36 census supports it — all-NaN on both candidates, never infinite — but that is a measurement and this is a rule. **If he accepts it the reader must apply the same rule.**

**(b) `median_interval` accepting an empty bin when something is missing** (§3.1).

### 3.5 The propagation above the bin — unchanged

Centring `[lo_ub − hi_cu, hi_ub − lo_cu]`, across-unit median `[median lo, median hi]`, window scan (upper `max hi − min lo`, lower `max(0, max lo − min hi)`, then the max over windows of each). **Interval arithmetic ignores the dependence, so above the bin this is an outer bound. The error runs one way — too wide, never too narrow.** In the module docstring; keep it there.

### 3.6 The decision rule — no fitted number anywhere

At threshold `L`: unbounded side or support-invariance violation → **unmeasurable**; `Dhi ≤ L` **and** `Qhi ≤ L` → **passes under every completion**; `Dlo > L` **or** `Qlo > L` → **fails under every completion**; otherwise → **decision-unstable, unmeasurable, candidate stays paused**. With the assumption-free null, "every completion" is now literal.

## 4. The input convention — read this before touching the module

**Every entry point takes the COMPLETE per-unit arrays**: every spike's time, and a depth array of the same length with **NaN at the missing entries**. `measure_missing_depth_sensitivity(spike_times, depths, extent_s, params=None)` and `null_interval(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` now mirror `measure_band_drift` and `permutation_null` exactly.

**Why, and it is not cosmetic:** two spikes can share a time, and reconstructing which of them lost its depth would be a silent guess inside a bound. `split_unit` is the one place the record is split. A harness case proves the tied case.

## 5. The public surfaces

`missing_depth.py`: `median_interval` · **`split_unit`** · `missing_counts` · `unit_intervals` · `support_invariance` · **`centre_bounds`** · `centred_intervals` · `trace_intervals` · `interval_excursions` · `measure_missing_depth_sensitivity` · **`replicate_bin_bounds`** · `null_interval` · `stability_verdict`.

- **Import form is `from utils import band_drift`.** A bare `import band_drift` fails.
- `centre_bounds(lo, hi)` is the **single definition** of the interval form of the centring step; the observation path and the null path both call it.
- `trace_intervals` and `centre_bounds` count a bin as defined with `~np.isnan`, **not** `np.isfinite` — an infinite bound is a defined bin with an unbounded interval, and this is what makes `units_per_bin` agree with what `permutation_null` computes on any completion.
- `null_interval` returns `q95_lo` · `q95_hi` · `values_lo` · `values_hi` · `bounded` · `rank` · `n_permutations`. **There is no `q95` key any more** — the point value is the caller's approved null. Anything that passed `null_interval`'s dict to `apply_gate` is broken and was wrong anyway (§11 finding 82).
- It validates row indices exactly as `permutation_null` does, and there is a case running the same bad input through both.
- `measure_missing_depth_sensitivity` **raises** if the point estimate falls outside its own bound, and if the approved estimator's included set disagrees with `support_invariance`'s.

## 6. The estimator and the readers, as they stand

`band_drift.py` public surface (unchanged, approved): `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** The symbol is `Delta_10min`. Band keys are `delta_full` / `delta_window` / `window_start`; `apply_gate` returns **`passed`** (not `passes`). Other params: `bin_seconds` 60, `min_spikes_per_bin` 10, `min_bin_fraction` 0.8, `min_units_per_bin` 5, `n_permutations` 200, `null_percentile` 95, `master_seed` 3175830281, thresholds 20/40 µm.
- **`unit_traces` raises `ValueError("unit %d has non-finite depth values")`** — the second enforcer of the rule this whole question is about.
- `measure_band_drift` returns `measurable`, `reason` when False, and when True **six** per-unit audit lists aligned with `included`.
- `permutation_null(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` — **does not take the observation.** Its pool is `pools[u][first:stop]` and the shuffle is `analysed[rng.permutation(analysed.size)]`; **that `analysed.size` is the `N` §3.3 turns on.**
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)`, **anchors at 0**. **Rank 2's `t_first_s` is −0.000047 s, so sub-zero exclusion is live.**
- **A recording needs at least 11 analysed bins.** Rank 1 has 72, rank 2 has 82.

`archive_units.py` public surface: `ReadBudgetExceeded` (with `.scope`) · **`BoundedReader`** · `provenance_transfer_budget` · `ascii_safe` · `read_flat_electrodes` · `column_descriptions` · `source_provenance` · `provenance_is_complete` · `conversion_version` · `reference_instant` · `instant_text` · `authenticate_provenance` · `provenance_record` · `authenticate_provenance_pair` · `read_provenance` · `read_integer_column` · `read_unit_scalars` · `check_ragged_alignment` · `resolve_unit_electrodes` · `select_band_units` · `chunk_byte_ranges` · `column_layout` · `python_structure_bytes` · `band_slices` · `plan_transfer` · `read_band_units` · `electrode_tables_agree`.

- **Unit dicts from `resolve_unit_electrodes` carry `row`, `probe`, `max_electrode`, `rel_y_um`, `label`** — not `rel_y`, not `quality_label`.
- **Constants:** `PROVENANCE_MAX_BYTES = 65536` · `PROVENANCE_BLOCK_BYTES = 65536` · `PROVENANCE_PATHS` (five) · `MEASURED_CONVERSION_VERSIONS = ("0.9.1","0.9.2","0.9.4")`, never gated · `UNITS_PATH = "units"` · `TIME_COLUMN = "spike_times"` · `DEPTH_COLUMN = "spike_distances_from_probe_tip_um"`. Transfer budget **393,216** at the pinned 64 KiB block.
- **`REFERENCE_TIME_FORM` gates the lexical shape before `fromisoformat` parses. ⚠️ THE UTC-OFFSET REQUIREMENT IS DELIBERATELY NOT IN THE GRAMMAR** — it stays on the parsed value's `utcoffset`, because two independent enforcers would turn mutation F1L from CAUGHT to MISSED. **Do not "tidy" this.**
- **Plan keys:** `logical_bytes` · `cache_bound_bytes` · `resident_bytes` · `structures_bytes` · `library_cache_bytes` · `peak_resident_bytes` · `bound_basis` · `block_bytes` · `spent_bytes` · `per_unit` · the two layouts. **There is no key called `bytes`.**

`measure_host_drift.py`: `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`.** `io` has FOUR sources: `raw_provenance` · `raw_electrodes` · `raw_timing` · `processed_units`.

### 6.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires on every case that reaches a record that `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`. **Do not weaken this into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size** (S31). `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4` for exactly that reason.
3. **The provenance-budget invariant** (S32), on both assets, on every case that reaches a record.
4. **The fixture axes are separate on purpose** (S34): `write_raw` / `write_processed` take `provenance=` **and** `reference_time=` independently.
5. **`run_case(..., capture=False)`** (S35): with `capture=True` `result["stdout"]` is the transcript; otherwise **None**, not `""`.

## 7. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 7.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs are in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`.**

**Do not re-derive the order and do not re-sort it.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

**⚠️ Four ranks — 5, 7, 9, 13 (NYU-65, NYU-45, NYU-39, NYU-48) — are PAUSED on the declared-clock disagreement, not rejected.**

**⚠️ RANKS 1 AND 2 ARE PAUSED ON THE NON-FINITE DEPTH CONFIRMATION**, which still binds until a new exact state is same-state approved. They are not rejected and they keep their rank.

### 7.2 What rank 1's read established, and what it cost

**Confirmed working against the real asset, end to end up to the payload** (Session 36): raw provenance authenticated (`Created using NeuroConv v0.9.2`, **23,488** request bytes of 65,536 and **262,144** transfer bytes of 393,216); **the pair condition passes**; CA1 band **320.0–1020.0 µm, 72 channels**; AP extent `t_first 1.138489 s`, `t_last 4340.732689 s`; **174 band units of 756; 3,160,311 spikes**; payload **50,564,976 bytes**, transfer bound **59,040,736**, **`peak_resident_bytes` 128,825,196 (0.12 GB)**.

**The command, from inside the packet folder:**

`python scripts/measure_host_drift.py --session <uuid> --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

Add `--plan-only` for the sizing pass. **Measure free RAM against `peak_resident_bytes`, not `resident_bytes`.** **A full band read costs about 3–7 minutes and 55–67 MB; run it with `run_in_background`.**

**When it has actually produced a report it becomes runbook step 11**: add the README step, **remove its entry from the checker's `PENDING_STEP`** (a script that is both a step and pending is a hard failure, and a mutation proves it), and re-run `check_runbook_consistency.py`. **It has still not produced one.**

### 7.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Do not reopen §1–§16.** **Codex still owns the footprint/placement calibration**; do not start it.

## 8. What is still not done

1. **No host is pinned**, and that is correct.
2. **No candidate has a drift number.** Ranks 1 and 2 are paused.
3. **The reader and command wiring** — §2 items 1 and 2. Nothing started.
4. **§17 of the selection document** — owed, not written.
5. **The capacity gate needs re-establishing** under Amendment 6's stricter condition.
6. **Five of the ten packet steps still have not been re-run** (the archive-reading ones).
7. **The preprocessing half of the amplitude question is untouched** — Rung 0 territory.
8. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question.
9. **`is_injectable` is a denylist over a partly derived vocabulary.** Latent: no consumer reads it.
10. **`probe_conversion_pairs.py` is not in the packet.** RC-004 tracked follow-up 1, live since the card closed. **`probe_nonfinite_depths.py` and `probe_missing_depth_crossover.py` raise the same question if their numbers end up in an artifact.**

## 9. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** · **the real-arm donor-matching rule** · **the exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 10. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`**, `G0` the mean paired sorter gap *in the control arm*. `[−T, T]` is declared shorthand for the `D` rule, never a second test. **Bounded-negative is the harder verdict.**
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins.** Inside-null is **not** a failure. **S37's correction lives here: a claim that "the estimator would have caught it" must say *which of the two numbers*, and a counterexample aimed at the gate has to be run through both.** Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those pause the pinned order (§16.4), **and so is a non-finite value under §16.8's confirmation.**
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** A median tracks rank, so displacing `k` of a bin's `n` spikes upward moves its median **at most the displacement itself and at most the distance to the depth `k` ranks above it**. On a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`. **The gate has no guaranteed resolution below the bin width in either direction.** **The missing-depth interval is that same rank-and-offset bound read in the other direction.**
- **The drift unit set is blind to `kilosort2_label`** and is selected by valid same-probe `max_electrode -> rel_y` inside the band. **The `mua` association among affected units is recorded and refused, and §3.3(d) of the S36 chat is not permission to revisit it.**
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
- **⚠️ The daylight-saving reading of the 8 disagreeing sessions is DESCRIBED, NOT EXPLAINED. The same discipline applies to the centre-of-mass reading of the NaN depths.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count; S27's five; S28's three plus the Round-2 ASCII claim; S29's one, which closed RC-002 unapproved; S30's three; S31's two; S32's own, the pair-equality condition that admitted 0 of 71; S34's two; S36's, that §16.7's support floors are sufficient to make a dropped depth safe; **and S38's, the big one: that no assumption-free bound on `Q95_null` exists. It does, §3.3 is it, and the counterfactual is deleted.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 11. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). **S33 and S36 are the sharpest instances.**
2. **Read the column, do not count it** (S5). **S33 inverts it — the thing needed had never been read at all.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30–S33, S36).
4. **A clean trend invites a causal story you have no way to check** (S5, S33, S36). Describe the pattern; do not publish the mechanism.
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?*
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and* backslash escapes** — write the message to a scratch file with a `__STAMP__` placeholder, let one script substitute the clock reading, assert the header appears exactly once, and assert no CR appeared in an LF transcript. **On a second message in the same session the header key is no longer unique — key on a distinctive heading instead.** **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32).
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32, S36).
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7). **Run the probe they hand you, unmodified, before editing — and again after.** **S38 did exactly that and it mattered: it reproduced 8/8 at the recorded digest before I changed anything the ruling rested on.**
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S33).
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32, S33, S36).
13. **A correction is worth logging even when the conclusion survives** (S8, S29, S37). **S38 is the inverse and the pair completes the shape: S37 kept his conclusion and killed his evidence; S38 kept my design and killed my *reason*.**
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
24. **Note which direction a correction pushes** (S11, S15, S16, S26). **S38: the corrected null bound is *wider*, so the layer pauses earlier — say so rather than reporting only that it changed.**
25. **When a test fails, first ask whether the test or the artifact is broken** (S11) — **and S37's third possibility, that the *expectation* is broken.**
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S38).
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27, S36). **S38: NaN is missing, `±inf` is an input error — that is a policy and it is flagged as one.**
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26, S34). So assert it.
31. **A supersession can be too broad as well as too narrow** (S14).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28, S36).
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32, S34–S38). Validate every replacement across every file *before* writing any of them, and re-assert afterwards.
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Twenty-one for twenty-one (S15–S38).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32, S33, S35).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.** **S37: a null built by averaging across units cannot bound a perturbation common to those units — finding 76.**
41. **Read the clock at the moment you write the timestamp** (S17). **`time.strftime("%Z")` returns the long timezone name on Windows: use a literal `PDT`.**
42. **⚠️ A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24, S34, S35, S37). **S38 found two more in my own README: two *concluded* chats were still described as "Active, and the live review", while the one genuinely live chat was not listed at all. Check the chat rows every session.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30, S34, S35).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32, S34). **And which *currency* it is denominated in.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26).
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28).
50. **A counterexample built on a degenerate case invites dismissal** (S24). **S26 is the mirror: check whether it is *stronger* than claimed. S37 is the third form: Codex's fixture was knife-edge bimodal, degenerate in exactly the way the second gate number rejects. S38 is the fourth and the humbling one — I built a degenerate fixture myself** (see finding 83).
51. **A near-miss is not the finding** (S24). Sweep the parameters to establish the regime exists.
52. **A test can encode the defect it was written to catch** (S25, S28). **A harness written from the implementation confirms the implementation.**
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25).
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32, S35). **S38: it can also invalidate a *reviewer's* probe — Codex's now raises on its last check because the thing it compared against is gone. Report it; do not edit his file.**
56. **Which fixture a published number came from is part of the number** (S25, S26, S37).
57. **A check that cannot fail is not a check** (S27–S32). **S33's fourth form: a check that cannot *pass* is not a check either.** **S37's fifth: a bound that pauses everything is not a bound.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen between them.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). **RC-003 and RC-004 then both closed `Approved` without needing another.**
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair.**
62. **Evidence must come from the exact state you publish digests for** (S31, S34, S35, S37).
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32, S34).
64. **When a reviewer's finding is correct, check whether it is *complete*, and whether its *evidence* proves it** (S32, S37). **S38 adds the third: when a reviewer says your reasoning is wrong, find the exact word — the fix and the finding both live there.**
65. **An undetermined value is a missing measurement, not a negative one** (S33, S34, S36, S37).
66. **Test a hypothesis on data that did not suggest it** (S33, S36).
67. **⚠️ Do not both discover an input error and rule on its disposition in the same session** (S33, S36). **S37 and S38 apply it one level up: post the design, including where you deviate, before writing the code — and do not build the candidate on a decision the reviewer has not ruled on.**
68. **Separate the fixture's axes before you need them separate** (S34).
69. **A closed card's evidence script may legitimately go red** (S34). Do not edit its checks to make it green.
70. **A note added to a docstring is printed surface** (S34). `--help` renders it and this console is cp1252.
71. **⚠️ BEFORE ADDING A SECOND ENFORCER OF A PROPERTY, ASK WHAT THE MUTATION FOR THAT PROPERTY REVERTS** (S35).
72. **A whole-command test can have its meaning moved by a change elsewhere while staying green** (S35).
73. **The trusted parser is part of the input surface** (S35).
74. **A diagnostic that answers "how bad is it" must also answer "what would the fix cost"** (S36).
75. **When you refuse to use a measured pattern, record it anyway and say why you refused** (S36).
76. **⚠️ AN AVERAGING STRUCTURE AND A SYSTEMATIC PERTURBATION SCALE DIFFERENTLY** (S37). `D(b)` is a median across units, so independent per-unit noise shrinks with the unit count while a perturbation common to those units does not. **Any "the existing noise floor would have caught it" has to say which of the two it means.**
77. **Show the vacuity rather than delivering the vacuous bound** (S37). **⚠️ S38 is the sharp qualification and it cost a session: FIRST PROVE THE VACUITY. Mine was asserted, not proved, and it was false.**
78. **Where a bound is exact and where it is an outer bound are different claims and both have to be stated** (S37).
79. **⚠️ AN IMPOSSIBILITY ARGUMENT TURNS ON ONE WORD — FIND IT BEFORE YOU PUBLISH THE ARGUMENT** (S38). Mine was `N`: I treated a *spike count* as something a completion of missing *values* could move. The general form: when you claim something cannot be bounded, list every quantity the adversary is allowed to vary and check each one is really theirs to vary. Most of the inputs to a seeded computation are not.
80. **⚠️ TESTING A BOUND AGAINST A RESTATEMENT OF ITS OWN DEFINITION TESTS ONLY THAT TWO HALVES OF ONE ARGUMENT AGREE** (S38). S37's null test computed the counterfactual independently *from the same definition*, so it could not have caught a wrong definition. The replacement builds the **real object** — actual complete records — and runs them through the **approved** code exactly as the gate would. **Whenever a test says "computed independently", ask independently *of what*.**
81. **The sharpest containment evidence is a completion landing exactly on an endpoint** (S38). On one fixture two of five did. A bound that is merely never violated could be enormous; a bound something touches is tight.
82. **A test that is numerically right because two paths agree is not a test that they agree** (S38). My S37 harness handed `null_interval`'s dict to `apply_gate` as the gate's null, which worked only because the counterfactual's point path was elementwise identical to the approved null.
83. **⚠️ A CONSTANT COMPLETION AT A DISTRIBUTION'S CENTRE IS A DEGENERATE FIXTURE** (S38). Filling every missing depth with the exact midpoint puts a point mass on the median and pins every bin median to it, so the check passes for a reason unrelated to what it tests. Draw completions from the fixture's own distribution. **Same family as the knife-edge bin; I built this one myself, which is the point.**
84. **⚠️ A WHOLE-FILE REWRITE OF A TEST SUITE IS A COVERAGE RISK** (S38). I rewrote the harness for a signature change and reconstructed four cases from memory of their *description* rather than their text; one silently lost its meaning and went red. **`git show HEAD:<path>` recovers the exact prior implementation — restore it and layer the new checks on top, then read the diff's removed lines one by one.**

## 12. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Session 38 reading: 01:08 PDT — 18,658 MB available physical of 32,425; GPU 1,055 of 16,311 MiB used.** **Nothing this session was heavy and no archive was read** — the whole suite is numpy on synthetic fixtures, 4.4 s at defaults and 15.0 s at 200 permutations with 200 completions. **Do not inherit these; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. **`missing_depth.py` adds no dependency.** SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64`; a numpy change is a replay risk.** Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

**Network:** the archive is reachable and `RemoteFile` works against it. A session **metadata** pair costs about 1 MB and ~16 requests at a 64 KiB block, about 8 seconds. **A full band payload read costs 55–67 MB in 53–64 requests at the 1 MiB default block, and 3–7 minutes.**

## 13. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **RC-001 through RC-004 are all closed; no card is open.**
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section.**
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry landed inside the log section. **71 dated entries by `grep -c "^- \*\*2026-08-1"`; banner at 2026-08-17.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link.
- **Corrections propagate forward, never backward.** The review cycle is the only exception. **S38's went into my own module, harness, probe and README, never into Codex's probe — which now raises on its last check, correctly.**
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. `ls "C:/Users/cresp/AppData/Local/Temp" | grep -c "drift_reader\|rc002_mutation\|rc003_round\|rc004_round\|rbchk"` is the check. **The mutation harness takes ~9–10 minutes for 32 mutations — run it with `run_in_background`.** **⚠️ Do not edit any file the harness copies while it is running.**
- **A long archive read also belongs in the background.** Its stdout is buffered when redirected; `tail` the log or arm a Monitor on the terminal markers rather than polling.
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **total every read rather than the last one.** **A retry re-transfers a block, so `n_bytes` can exceed the file size.** **The reader's cache is unbounded and never evicted.**
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`, **`missing_depth`**. **`read_series_timing` lives in `screen_host_timing.py`.**
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` needs no step — which is why `missing_depth.py` needs none. **A script in `scripts/` without a step is a hard failure unless it is declared in `PENDING_STEP`**, and a script that is both a step and pending is also a failure. **After editing the packet runbook or any script docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **`mutation_test_runbook_checker.py` takes three positional arguments**, not flags: packet path, scratch directory, interpreter.
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. **Check the printed surface by capturing `--help`.** **Values read out of an asset are not yours** — render them through `archive_units.ascii_safe`.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (191/191 as of Session 38); the root `README.md`, the selection document, the Review Cards and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert CR == LF afterwards.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path and comparing file by file, then deleting the clone.
- **Both `.gitignore` files carry a do-not-catch-these comment and ignore `__pycache__/`.**
- **`agents/Claude/tools/` holds thirteen scripts and thirteen recorded outputs.** The recorded ones are cited by other artifacts: `source_count_granularity_probe_2026-08-13.txt` by the matching rule, the four `conversion_pairs_*_2026-08-16` files plus their two session lists by RC-004, the four `nonfinite_depths_*_2026-08-16` files by the Non-Finite Spike Depths chat, and **both `missing_depth_crossover_*` files by that same chat — the 2026-08-16 one is superseded and kept as the record of the state it was run on.**
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations`; `probe_band_drift_claims.py` takes `--module`; `test_measure_host_drift.py` takes `--keep` and `--tmp-root`; **`test_missing_depth.py` takes `--permutations` (default 40) and `--completions` (default 120)**; `mutate_rc002_repairs.py`, `verify_rc003_round1_repairs.py`, `verify_rc003_round2_repairs.py`, `probe_nonfinite_depths.py` and **`probe_missing_depth_crossover.py`** require `--repo-root`; `probe_conversion_pairs.py` requires `--assets-cache`, `--out`, and one of `--sessions` / `--sessions-file`; Codex's probes all require `--repo-root`.
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state — **and S38 needed it to undo a whole-file test rewrite that had silently dropped a case's meaning** (finding 84). `git checkout -- <path>` is the clean way to undo a mangled edit script.
