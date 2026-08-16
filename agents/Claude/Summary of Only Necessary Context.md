# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 36 · 2026-08-16 09:30 PDT**
**Next session is Claude Session 37. No count-based progress report is due** (they fall at 8, 16, 24, 32, **40**). A phase transition or an approved amendment would trigger one anyway.

## 0. WHAT THIS SESSION DID, IN ONE PARAGRAPH

**RC-004 closed `Approved`, the first real drift measurement was attempted, and it stopped on a *different* pre-declared input confirmation.** Codex's Round-2 delta pass came back reviewer-`Approved`; I re-authenticated all five digests from disk, re-ran his Round-2 probe (5 of 5), the acceptance suite (472 / 0) and his Round-1 probe (reproduces neither), explicitly approved the same state, closed the card and concluded the chat with a `Summary.md`. Then rank 1's `--plan-only` **completed for the first time** — the pair condition passes on the real candidate — and the real read stopped at `unit 901 carries 1 non-finite spike depths`. **That is §16.8 working as written, not a bug.** I measured the prevalence on rank 1 *and* on rank 2 as a holdout, opened a new chat with the numbers and a proposed disposition, and **did not rule on it**. **The pinned order is paused at rank 1.**

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

**Outcomes are `Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required`. `Escalated` was removed.** At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**. **Evidence determines what may ship; consensus determines what happens next. Underdetermined evidence is not resolved in favour of approval.**

**RC-001 `Approved`. RC-002 `Revisions Required` (first Convergence Decision, S30). RC-003 `Approved` at Round 3. RC-004 `Approved` at Round 2 (S36). No card is open.** **RC-005 is expected but does not exist yet** — see §2.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six. **Nothing this session needs an amendment**: the non-finite question lives in §16.8 of the selection document, not in the Claim Sheet.

**⚠️ This file describes the moment it was written.** Codex has now fifteen times posted a handoff within the hour after a session closed. **Read the active chat before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, and no candidate has cleared any open gate.** What *does* now exist for the first time: a complete, successful input-authentication pass and read plan on the real rank-1 candidate, and a measured census of non-finite depths on two candidates.

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 24, `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`. §1–§16 SAME-STATE APPROVED and unchanged this session. Do not reopen them.** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | `eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` — approved, closed. |
| `agents/Claude/tools/test_band_drift.py` | `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` — approved, closed. 103 checks. |
| **`Reproducibility Packet/scripts/utils/archive_units.py`** | **`9ef16f58cbd46ece7753406790a1b3d578efaf03df6311024c62e4c0e7b7e6e0` — RC-004 APPROVED, closed.** |
| **`Reproducibility Packet/scripts/measure_host_drift.py`** | **`156f6f0ffb0d13b7b3c871c29e7f516d93da65cadd4cbc742d7113fe132cf450` — RC-004 APPROVED, closed.** |
| **`agents/Claude/tools/test_measure_host_drift.py`** | **`c508233d9c2d5c5567ca6875e8ebd22b1823b3ab7dff2aeac52044847305349a`** — 82 cases, **472 checks, 0 failed, ~16 s.** Approved. |
| **`agents/Claude/tools/mutate_rc002_repairs.py`** | **`97860ad978bf6bd2fd6851033405c7b9e1cf51aacb0c44332344fd64d92bcf49`** — **32 of 32 caught**, ~9–10 minutes. Approved. |
| `agents/Claude/tools/verify_rc003_round2_repairs.py` | `f4ee4ae651a03471c3d8abbd7a3a0e131f2d381219dd6691e113f349a018bf77` — approved. **Exits 1 on exactly two checks by design.** |
| `agents/Claude/tools/verify_rc003_round1_repairs.py` | `2b7d9ef6…` — unchanged, exits 0. |
| `agents/Claude/tools/probe_conversion_pairs.py` | `10ad5053a06ba35d32d17540a6511f459e2e6f72cd3fcbe613bbdc9af10873ec` — the 71-session census. |
| **`agents/Claude/tools/probe_nonfinite_depths.py`** | **`ade3660f3d744e07fae8326f04508c157f47cfbe50313079c983caacc5bb52f1` — NEW this session.** Diagnostic only. Two recorded outputs. |
| `agents/Codex/tools/probe_rc004_round1.py` | `a48b5c5e…` — reproduces neither counterexample against the approved state. |
| `agents/Codex/tools/probe_rc004_round2.py` | `f6b2aa6f13111987f0c3705e877b68d73d4b746d1154ebab4bb1b7341bca429f` — 5 of 5, exit 0. |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `ea85ede2…` — 18 of 18. |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `848e6d03…` — unchanged; 10 steps agree, `measure_host_drift.py` still `PENDING`. |
| `Reproducibility Packet/README.md` | `ae01b1a2…` — **unchanged. No runbook step was added**, because the command produced no report. |

## 2. The first thing to do next session

**Read `chats/Claude-Codex/Non-Finite Spike Depths/` before anything else. It is the only active Claude-Codex chat and the pinned order is paused behind it.**

- **`chats/Claude-Codex/Non-Finite Spike Depths/` — opened this session, on Codex, awaiting his ruling.**
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active** by Randy's request.
- **All ten other chats are concluded**, including the RC-004 review chat.

**If Codex has ruled and accepts the proposal:** implement it, write the disposition as a **new section** of the selection document (§17 — do **not** edit the closed §16), and open **RC-005** with the implementation as the candidate. The loosening needs its mirror-failure cases in the same session: dropping that takes a bin below the floor must still leave the candidate unmeasurable; a unit whose depths are entirely non-finite; and a non-finite *time* that still stops the run. **Re-run the mutation harness after the repair** — S31, S32 and S35 all proved a repair can silently remove the coverage a mutation depends on.

**If he rules the confirmation should stand:** write the pause up as the result, and work out what evidence could recover the paused candidates — which by then is ranks 1 and 2 plus the four already paused on the declared-clock disagreement.

**Do not implement anything before he rules.** This session deliberately did not, and the reason is in §9 finding 67.

## 3. The finding this session's chat is about

### 3.1 What stopped

Rank 1's real read stopped with `[fatal] input error reading …_desc-processed_behavior+ecephys.nwb probe Probe01: unit 901 carries 1 non-finite spike depths`. **No verdict, no output files, exit 1.** An input error **pauses** the candidate; the pinned order has **not** advanced.

**It is not a defect.** §16.8's second input confirmation is *"that those values are finite"*. `archive_units.read_band_units` enforces it (`raise ValueError("unit %d carries %d non-finite spike depths")`) and `band_drift.unit_traces` enforces it again independently. Two layers, one pre-declared rule, both correct against the contract. **What is in question is the confirmation, not the code.**

### 3.2 The measurement, both candidates

`probe_nonfinite_depths.py` reads the same band and reports every non-finite value plus what dropping would cost.

| | **rank 1** CSHL047 Probe01 `b52182e7…` | **rank 2** NYU-12 Probe01 `a8a8af78…` |
|---|---|---|
| band | 320.0–1020.0 µm, 72 ch | 3180.0–3820.0 µm, 66 ch |
| complete 60 s bins | 72 | 82 |
| band units | 174 of 756 | 267 of 1,185 |
| band spikes | 3,160,311 | 4,898,466 |
| **units with non-finite depths** | **11** | **10** |
| **non-finite depths** | **231** (0.00731%) | **222** (0.00453%) |
| worst single unit | 169 of 24,520 = 0.689% | 196 of 49,738 = 0.394% |
| **non-finite spike times** | **0** | **0** |
| NaN / +inf / −inf | 231 / 0 / 0 | 222 / 0 / 0 |
| units meeting support, keeping / dropping | **140 / 140** | **182 / 182** |
| **bins lost by dropping** | **0** | **0** |
| labels of affected units | all `mua` (0 of 32 `good`) | all `mua` (0 of 60 `good`) |
| read cost | 53 requests, 55,210,480 B | 64 requests, 66,771,599 B |

**Rank 1 was read twice by two independent archive reads and gave identical numbers.** **Rank 2 is a holdout** — deliberately the candidate that did not produce the finding.

### 3.3 The four facts, and the one that is recorded but refused

**(a) The rule pauses the holdout too** — two candidates, two pauses. Same shape as the converter-version rule that admitted 0 of 71. **(b) All NaN, never infinite, never in the times**; the column is centre-of-mass-derived and a centre of mass divides by a sum of weights — **a described pattern, not a measured mechanism.** **(c) Dropping costs zero bins and zero units on both, measured**; and all 21 affected units are *inside* the included set. **(d) Every affected unit is `mua`** (pooled chance ≈ 0.013 at each candidate's own rate) — **recorded and explicitly refused as a filter**, because the unit set is pre-declared label-blind and §16.4 argues that at length, including that a `good`-only reading would make rank 9 unmeasurable by construction.

### 3.4 The proposal, as posted

**Treat a non-finite *depth* as a per-sample exclusion that is counted and published; keep a non-finite *time* as an input error; let §16.7's pre-declared inclusion floors do the protective work.** Reasons: a missing depth is one missing measurement, while a missing time means the spike cannot be placed at all; the floors (≥10 spikes in ≥80% of bins per unit, ≥5 included units per bin, any invalid bin ⇒ unmeasurable) were set before any candidate was read and already govern thin support; **no new tolerance is proposed**, because an X chosen after seeing 0.0073% is a number fitted to the data; the exclusion must be published per unit and in total; and the bias it admits is real — if the depth estimator fails preferentially at some depths, dropping its failures biases the bin median, bounded by the same rank-and-offset bound §16.4 states for the mirror case, small here only because the count is small.

**Codex was told plainly that the opposite ruling is defensible.**

## 4. The estimator and the readers, as they stand

`band_drift.py` public surface (unchanged, approved): `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** The symbol is `Delta_10min`. Band keys are `delta_full` / `delta_window` / `window_start`; `apply_gate` returns **`passed`** (not `passes`). Other params: `bin_seconds` 60, `min_spikes_per_bin` 10, `min_bin_fraction` 0.8, `min_units_per_bin` 5, `n_permutations` 200, `null_percentile` 95, `master_seed` 3175830281, thresholds 20/40 µm.
- **`unit_traces` raises `ValueError("unit %d has non-finite depth values")`** — the second enforcer of the rule §3 is about.
- `measure_band_drift(spike_times, depths, extent_s, params=None)` returns `measurable`, `reason` when False, and when True **six** per-unit audit lists aligned with `included`: `unit_delta_full`, `unit_delta_max_window`, `unit_max_window_start`, `unit_max_window_defined_bins`, `unit_delta_band_window`, `unit_band_window_defined_bins`.
- `permutation_null(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` — **does not take the observation.**
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)`, **anchors at 0**; spikes below zero fall outside every bin and are silently excluded — the reader counts and reports them. **Rank 2's `t_first_s` is −0.000047 s, so this is live, not hypothetical.**
- **A recording needs at least 11 analysed bins.** Rank 1 has 72, rank 2 has 82.

`archive_units.py` public surface: `ReadBudgetExceeded` (with `.scope`) · **`BoundedReader`** (`.block_bytes`, `.last_spend`, `budget(read_bytes, transfer_bytes=None, label=…)`) · `provenance_transfer_budget` · `ascii_safe` · `read_flat_electrodes` · `column_descriptions` · `source_provenance` · `provenance_is_complete` · `conversion_version` · `reference_instant` · `instant_text` · `authenticate_provenance` · `provenance_record` · `authenticate_provenance_pair` · `read_provenance(url, size, block_bytes, max_bytes=None)` · `read_integer_column` · `read_unit_scalars` · `check_ragged_alignment` · `resolve_unit_electrodes` · `select_band_units` · `chunk_byte_ranges` · `column_layout` · `python_structure_bytes` · `band_slices` · `plan_transfer` · `read_band_units` · `electrode_tables_agree`. Private: `_stored_value_bytes`, `_capped`, `_decode`, `_blocks_covering`, `_slice_blocks`, `_slice_bounds`, `_own_refusal`, `_ceiling_budget`.

- **Unit dicts from `resolve_unit_electrodes` carry `row`, `probe`, `max_electrode`, `rel_y_um`, `label`** — not `rel_y`, not `quality_label`. Reading the wrong key cost a debugging round this session.
- **Constants:** `PROVENANCE_MAX_BYTES = 65536` · `PROVENANCE_BLOCK_BYTES = 65536` · `PROVENANCE_PATHS` (five) · `MEASURED_CONVERSION_VERSIONS = ("0.9.1","0.9.2","0.9.4")`, never gated · `REFERENCE_TIME_FORM` / `…_TEXT` · `UNITS_PATH = "units"` · `TIME_COLUMN = "spike_times"` · `DEPTH_COLUMN = "spike_distances_from_probe_tip_um"`. Transfer budget **393,216** at the pinned 64 KiB block.
- **`REFERENCE_TIME_FORM` gates the lexical shape before `fromisoformat` parses.** **⚠️ THE UTC-OFFSET REQUIREMENT IS DELIBERATELY NOT IN THE GRAMMAR** — it stays on the parsed value's `utcoffset`, because two independent enforcers would turn mutation F1L from CAUGHT to MISSED. **Do not "tidy" this.**
- **The declared ceiling covers `raw_provenance` and `processed_units`; `raw_electrodes` and `raw_timing` are bounded by construction alone.**
- **Plan keys:** `logical_bytes` · `cache_bound_bytes` · `resident_bytes` · `structures_bytes` · `library_cache_bytes` · `peak_resident_bytes` · `bound_basis` · `block_bytes` · `spent_bytes` · `per_unit` · the two layouts. **There is no key called `bytes`.**

`measure_host_drift.py`: `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`.** `io` has FOUR sources: `raw_provenance` · `raw_electrodes` · `raw_timing` · `processed_units`.

### 4.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires on every case that reaches a record that `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`, and raises if it matched no reader. **Do not weaken this into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size** (S31). `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4` for exactly that reason.
3. **The provenance-budget invariant** (S32), on both assets, on every case that reaches a record. **It says nothing about reads that never reach a record** — that gap was closed by the ceiling, not by a wider invariant.
4. **The fixture axes are separate on purpose** (S34): `write_raw` / `write_processed` take `provenance=` **and** `reference_time=` independently.
5. **`run_case(..., capture=False)`** (S35): with `capture=True` `result["stdout"]` is the transcript; otherwise **None**, not `""`.

## 5. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 5.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs are in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`.**

**Do not re-derive the order and do not re-sort it.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first; cannot change a verdict, only cost): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

**⚠️ Four ranks — 5, 7, 9, 13 (NYU-65, NYU-45, NYU-39, NYU-48) — are PAUSED on the declared-clock disagreement, not rejected.** Ranks 1, 2, 3, 4, 6, 8, 10, 11, 12 pass the pair condition.

**⚠️ AND NOW RANKS 1 AND 2 ARE PAUSED ON THE NON-FINITE DEPTH CONFIRMATION**, pending §2's ruling. They are not rejected and they keep their rank.

### 5.2 What rank 1's read established, and what it cost

**Confirmed working against the real asset, end to end up to the payload:** raw provenance authenticated (`Created using NeuroConv v0.9.2`, **23,488** request bytes of 65,536 and **262,144** transfer bytes of 393,216 — the five-path budget holds with room); **the pair condition passes**; CA1 band **320.0–1020.0 µm, 72 channels**; AP extent `t_first 1.138489 s`, `t_last 4340.732689 s` matching `host_timing_index.jsonl`; **174 band units of 756; 3,160,311 spikes**; payload **50,564,976 bytes**, transfer bound **59,040,736**, **`peak_resident_bytes` 128,825,196 (0.12 GB)**.

**The command, from inside the packet folder:**

`python scripts/measure_host_drift.py --session <uuid> --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

Add `--plan-only` for the sizing pass. **Measure free RAM against `peak_resident_bytes`, not `resident_bytes`.** **A full band read costs about 3–7 minutes and 55–67 MB; run it with `run_in_background`.**

**When it has actually produced a report it becomes runbook step 11**: add the README step, **remove its entry from the checker's `PENDING_STEP`** (a script that is both a step and pending is a hard failure, and a mutation proves it), and re-run `check_runbook_consistency.py`. **It has still not produced one.**

### 5.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Do not reopen §1–§16** — it belongs in a future section. **Codex still owns the footprint/placement calibration**; do not start it.

## 6. What is still not done

1. **No host is pinned**, and that is correct.
2. **No candidate has a drift number.** Ranks 1 and 2 are paused on §3's ruling.
3. **The capacity gate needs re-establishing** under Amendment 6's stricter condition.
4. **Five of the ten packet steps still have not been re-run** (the archive-reading ones).
5. **The preprocessing half of the amplitude question is untouched** — Rung 0 territory.
6. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question.
7. **`is_injectable` is a denylist over a partly derived vocabulary.** Latent: no consumer reads it.
8. **`probe_conversion_pairs.py` is not in the packet.** RC-004 tracked follow-up 1, now **live** since the card closed approved — the census is load-bearing evidence a reader should be able to reproduce, so it probably has to move into `Reproducibility Packet/scripts/` with a runbook step and a `PENDING_STEP` removal. **`probe_nonfinite_depths.py` will raise the same question if its numbers end up in an artifact.**

## 7. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** · **the real-arm donor-matching rule** · **the exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 8. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`, `G0` the mean paired sorter gap *in the control arm*.** `[−T, T]` is declared shorthand for the `D` rule, never a second test. `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins, not ten.** Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those are input errors that pause the pinned order (§16.4), and **so is a non-finite value, under §16.8's confirmation, which is what §3 is about.**
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** `0.000`/`15.000`/`30.000 µm` describes the **equal-baseline fixture** only. A median tracks rank, so displacing `k` of a bin's `n` spikes upward moves its median **at most the displacement itself and at most the distance to the depth `k` ranks above it**. On a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`. **The gate has no guaranteed resolution below the bin width in either direction.**
- **The drift unit set is blind to `kilosort2_label`** and is selected by valid same-probe `max_electrode -> rel_y` inside the band. **That choice carries no one-way safety guarantee, and §3.3(d) is not permission to revisit it.**
- **The per-unit excursions are reported and never consumed.** **Never compare a per-unit value to `Q95_null` or to `L`.** **The absence of magnitude separation is not evidence either.**
- **The bin grid anchors at session `t = 0` with extent `t_last_s`**, on pinned converter provenance. **`duration_s` is a span and is not an alternative clock hypothesis.** Endpoint containment is a consistency check that cannot identify a clock — **and neither can reference-instant agreement.**
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
- **⚠️ The daylight-saving reading of the 8 disagreeing sessions is DESCRIBED, NOT EXPLAINED.** **The same discipline now applies to the centre-of-mass reading of the NaN depths in §3.3(b).**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count that reported one of its three reads; S27's five; S28's three plus the Round-2 ASCII claim; S29's one, which closed RC-002 unapproved; S30's three; S31's two; S32's own, the pair-equality condition on converter version that admitted 0 of 71; and S34's two, which returned RC-004 Round 1. **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). **S33 is the sharpest instance; S36 is the second: a confirmation reviewed, approved and never once evaluated against a real asset.**
2. **Read the column, do not count it** (S5). **S33 inverts it — the thing needed had never been read at all.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30–S33). **S36: a check that stops on one sample in three million is pessimistic, and pessimism here pauses the entire pinned order.**
4. **A clean trend invites a causal story you have no way to check** (S5, S33, **S36**). Describe the pattern; do not publish the mechanism. **The all-NaN/never-infinite reading is a description.**
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **S36's version, when the reviewer edited nothing: check that the state approved is the state that exists, and re-run the reviewer's own evidence.**
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and* backslash escapes.** **`$VAR` does not expand inside the Bash tool's `-c` string.** **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.** **Write the message to a scratch file with a `__STAMP__` placeholder, let one script substitute the clock reading, assert the header appears exactly once, and assert no CR appeared in an LF transcript.**
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32).
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32). **⚠️ S36 is the live instance: the obvious repair is "pause if more than X% are non-finite", and every available X was chosen after seeing 0.0073%. The pre-declared floors are the bound instead.**
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7). **Run the probe they hand you, unmodified, before editing — and again after.** **S36: `resolve_unit_electrodes` returns `rel_y_um` and `label`, not `rel_y` and `quality_label`; I read the return contract only after guessing wrong.**
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S33). **When a check stands in for a property, ask what it admits and rejects on the real population.**
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32, S33). **S36 is the cleanest application: the check fired, and the session's whole output is the measurement plus a proposal, with no loosening performed.**
13. **A correction is worth logging even when the conclusion survives** (S8, S29).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9); a *better* reason arriving is also that moment (S15).
16. **An audit must use the same key its lookup uses** (S9, S27, S28, S31).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10).
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17, S23, S28, S29).
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11, S27–S29). **S33: and a *rule* you have not executed against real input is the same guess wearing a test suite.**
24. **Note which direction a correction pushes** (S11, S15, S16, S26).
25. **When a test fails, first ask whether the test or the artifact is broken** (S11). **`apply_gate` returns `passed`. `measure_band_drift` returns `delta_window`. Read the parser.**
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S36).
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27). **S36: "an input error pauses rather than rejects" is a policy that only becomes visible when the input error is one the data always carries.**
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26, S34). So assert it.
31. **A supersession can be too broad as well as too narrow** (S14).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28). **S36's inverse and the core of the proposal: ask whether a constraint you are about to *loosen* is already covered by a pre-declared rule — §16.7's floors already govern thin support.**
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32, S34–S36). Validate every replacement across every file *before* writing any of them, and re-assert afterwards.
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Nineteen for nineteen (S15–S36).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32, S33, S35).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.**
41. **Read the clock at the moment you write the timestamp** (S17). **`time.strftime("%Z")` returns the long timezone name on Windows: use a literal `PDT`.**
42. **A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24, S34, S35). **Grep your changed files for every sentence containing the thing you changed, not just the diff.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30, S34, S35).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32, S34). **And which *currency* it is denominated in.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26).
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28). **S34's inverse: a harness whose name no longer describes its scope was deliberately not renamed, because three artifacts cite it by path.**
50. **A counterexample built on a degenerate case invites dismissal** (S24). **S26 is the mirror: check whether it is *stronger* than claimed.**
51. **A near-miss is not the finding** (S24). Sweep the parameters to establish the regime exists.
52. **A test can encode the defect it was written to catch** (S25, S28). **A harness written from the implementation confirms the implementation.**
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25).
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32, S35).
56. **Which fixture a published number came from is part of the number** (S25, S26).
57. **A check that cannot fail is not a check** (S27–S32). **S33's fourth form: a check that cannot *pass* is not a check either.** **S35's corollary: give a "was it absent?" assertion a `None` sentinel rather than an empty string.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen between them.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). **RC-003 and RC-004 then both closed `Approved` without needing another.**
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair.**
62. **Evidence must come from the exact state you publish digests for** (S31, S34, S35). Compute digests from the files at write time.
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32, S34).
64. **When a reviewer's finding is correct, check whether it is *complete* before repairing it** (S32).
65. **An undetermined value is a missing measurement, not a negative one** (S33, S34). **S36 applies it to a single spike: a NaN depth is a missing measurement, which is exactly why it must be counted and published rather than silently dropped.**
66. **Test a hypothesis on data that did not suggest it** (S33). **S36: rank 2 was read as a holdout for exactly this reason, and it is what turned "rank 1 is unusual" into "the rule is not discriminating".**
67. **⚠️ Do not both discover an input error and rule on its disposition in the same session** (S33). **S36 is the second instance and the sharper one: the change would be a *loosening* of a safety confirmation, proposed by the agent it inconvenienced, on evidence that agent gathered — the configuration in which a wrong call is least likely to be caught.**
68. **Separate the fixture's axes before you need them separate** (S34).
69. **A closed card's evidence script may legitimately go red** (S34). Do not edit its checks to make it green.
70. **A note added to a docstring is printed surface** (S34). `--help` renders it and this console is cp1252.
71. **⚠️ BEFORE ADDING A SECOND ENFORCER OF A PROPERTY, ASK WHAT THE MUTATION FOR THAT PROPERTY REVERTS** (S35). **Redundancy in the code and sensitivity in the harness pull against each other.** One enforcer per property, and say in the docstring why.
72. **A whole-command test can have its meaning moved by a change elsewhere while staying green** (S35).
73. **The trusted parser is part of the input surface** (S35). `fromisoformat` is deliberately broader than ISO-8601.
74. **A diagnostic that answers "how bad is it" must also answer "what would the fix cost"** (S36). The first version of `probe_nonfinite_depths.py` reported bin support only *after* dropping, which cannot show whether dropping costs anything. **Both counts, or the number is unusable for the decision it was gathered for.**
75. **When you refuse to use a measured pattern, record it anyway and say why you refused** (S36). All 21 affected units being `mua` is real, is not strong enough to explain, and is barred by a pre-declared label-blind rule. **Omitting it would be the worse error; using it would be re-deriving a rejected filter from a number measured after the fact.**

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Session 36 readings: 09:06 PDT — 12,099 MB available physical of 32,425, 32,797 MB committed of 130,415. Before the plan-only read — 11,705 MB free, GPU 960 of 16,311 MiB used. Before the real read — 11,721 MB free against a 0.12 GB peak-resident bound. During the reads — 11,648–11,786 MB free; the Python process held 77 MB.** **Nothing was heavy; the cost was network — about 178 MB of archive transfer across five reads.** **Read all three numbers, not one.** **Do not inherit these; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64`; a numpy change is a replay risk.** **h5py's chunk-index and property-list APIs are load-bearing.** **`datetime.fromisoformat` is load-bearing and is fenced by `REFERENCE_TIME_FORM`.** Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

**Network:** the archive is reachable and `RemoteFile` works against it. A session **metadata** pair costs about 1 MB and ~16 requests at a 64 KiB block, about 8 seconds. **A full band payload read costs 55–67 MB in 53–64 requests at the 1 MiB default block, and 3–7 minutes.**

## 11. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **RC-001 through RC-004 are all closed; no card is open.**
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section.**
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry landed inside the log section. **67 dated entries by `grep -c "^- \*\*2026-08-1"`; banner at 2026-08-16.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link.
- **Corrections propagate forward, never backward.** The review cycle is the only exception.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. `ls "C:/Users/cresp/AppData/Local/Temp" | grep -c "drift_reader\|rc002_mutation\|rc003_round\|rc004_round\|rbchk"` is the check; it read 0 at this closeout. **The mutation harness takes ~9–10 minutes for 32 mutations — run it with `run_in_background`.** **⚠️ Do not edit any file the harness copies while it is running.**
- **A long archive read also belongs in the background.** Its stdout is buffered when redirected; `tail` the log or arm a Monitor on the terminal markers rather than polling.
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **total every read rather than the last one.** **A retry re-transfers a block, so `n_bytes` can exceed the file size.** **The reader's cache is unbounded and never evicted.**
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`. **`read_series_timing` lives in `screen_host_timing.py` and is imported by `measure_host_drift.py`.**
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` needs no step. **A script in `scripts/` without a step is a hard failure unless it is declared in `PENDING_STEP`** — and a script that is both a step and pending is also a failure, and both rules have mutations. **After editing the packet runbook or any script docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **`mutation_test_runbook_checker.py` takes three positional arguments**, not flags: packet path, scratch directory, interpreter.
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. **Check the printed surface by capturing `--help`.** **Values read out of an asset are not yours** — render them through `archive_units.ascii_safe`.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (178/178 as of Session 36); the root `README.md`, the selection document, the Review Cards and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert CR == LF afterwards.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path and comparing file by file, then deleting the clone.
- **Both `.gitignore` files carry a do-not-catch-these comment and ignore `__pycache__/`.**
- **`agents/Claude/tools/` holds eleven scripts and eleven recorded outputs.** The recorded ones are cited by other artifacts: `source_count_granularity_probe_2026-08-13.txt` by the matching rule, the four `conversion_pairs_*_2026-08-16` files plus their two session lists by RC-004, and **the four `nonfinite_depths_*_2026-08-16` files by the Non-Finite Spike Depths chat.**
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations`; `probe_band_drift_claims.py` takes `--module`; `test_measure_host_drift.py` takes `--keep` and `--tmp-root`; **`mutate_rc002_repairs.py`, `verify_rc003_round1_repairs.py`, `verify_rc003_round2_repairs.py` and `probe_nonfinite_depths.py` require `--repo-root`**; `probe_conversion_pairs.py` requires `--assets-cache`, `--out`, and one of `--sessions` / `--sessions-file`; Codex's probes all require `--repo-root`.
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state — and `git checkout -- <path>` is the clean way to undo a mangled edit script.
