# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 32 · 2026-08-16 01:05 PDT**
**Next session is Claude Session 33. No count-based progress report is due** (they fall at 8, 16, 24, 32, **40**). A phase transition or an approved amendment would trigger one anyway.

## 0. ⚠️ THE REVIEW METHOD — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

**Outcomes are `Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required`. `Escalated` was removed.** At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**: each writes, once, the minimum claim it thinks can ship, the evidence that controls, the strongest evidence against its own position, and one acceptable safe disposition. **Evidence determines what may ship; consensus determines what happens next. Underdetermined evidence is not resolved in favour of approval.**

**RC-001 closed `Approved`. RC-002 closed `Revisions Required` at Session 30 by the first Convergence Decision. RC-003 is its one permitted successor. Round 1 returned `Revisions Required` (three blockers), Round 2 returned `Revisions Required` (two blockers), and Session 32 wrote the Round 3 response. ⚠️ ROUND 3 IS THE LAST ROUND CLAUSE 5 ALLOWS. If Codex does not approve this exact state, RC-003 closes without approval, no second like-for-like successor may open, and the work must be SPLIT OR REDESIGNED with the changed boundary named — that becomes the first job of the next session, and it is worth taking to the director.**

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six.

**⚠️ This file describes the moment it was written.** Codex has now eleven times posted a handoff within the hour after a session closed. **Read the active chats before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, no candidate has been measured on any open gate, and nothing beyond bounded metadata reads has been downloaded.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 24, `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`. §1–§16 SAME-STATE APPROVED. RC-001 is closed. Do not reopen it.** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **`eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` — same-state approved, closed.** |
| `agents/Claude/tools/test_band_drift.py` | **`946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` — same-state approved, closed.** 103 checks, 0 failed. |
| `Reproducibility Packet/scripts/utils/archive_units.py` | **`96a31b3d…` — open on Codex, RC-003 Round 3. CHANGED in Session 32.** |
| `Reproducibility Packet/scripts/measure_host_drift.py` | **`0bf08153…` — open, RC-003 Round 3. CHANGED.** |
| `agents/Claude/tools/test_measure_host_drift.py` | **`92e90913…` — open, RC-003 Round 3. CHANGED. 382 checks, 0 failed, 14.6 s.** |
| `agents/Claude/tools/mutate_rc002_repairs.py` | **`9955ef60…` — open, RC-003 Round 3. CHANGED. 26 of 26, control green at 382.** |
| `agents/Claude/tools/verify_rc003_round1_repairs.py` | **`2b7d9ef6…` — CHANGED in Session 32** (its F3 check now accepts either bound; see §3). |
| `agents/Claude/tools/verify_rc003_round2_repairs.py` | **`9fb49fe8…` — NEW in Session 32, response-created, in scope for Round 3.** |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | **`ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc` — unchanged since Session 29; open, RC-003. 18 of 18, control green.** |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | **`848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f` — unchanged; open, RC-003.** |
| `Reproducibility Packet/README.md` | **`ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5` — unchanged; open, RC-003.** |
| `agents/Codex/tools/probe_rc003_round2.py` | `d67bf2616b2b10ef6e7f3f34ad324cdfa327787eb8af5b71cb4f7fd1de4e9ef2`. **His.** **Exit 1 against the repaired candidate: both F1 constructions stop as input errors and `default_block_transfer=0`.** |
| `agents/Codex/tools/probe_rc003_round1.py` | `df97e1a0…`. **His.** Still does not run to completion; `verify_rc003_round1_repairs.py` rebuilds its three constructions. |
| `agents/Codex/tools/probe_rc002_round3.py` | `506d7280…`. **His.** Raises the reader's `ValueError` before a plan exists. |
| `agents/Codex/tools/probe_rc001_round1.py` / `probe_draft16_safety_claims.py` | Both take `--repo-root`. 0 failures / digits unchanged at Session 32. |

**The full digests are in `Review Cards/RC-003 ….md` under `### Round 3 response state`. Use the card, not this table, when you need all sixty-four characters.**

## 2. The first thing to do next session

**Check the active chats before assuming anything. As of writing, everything open is open on Codex and nothing is open on you.**

- `chats/Claude-Codex/Bounded Archive Read Review/` — **RC-003 Round 3 is open on Codex and is delta-only** over the two repairs, the response-created verification script, and the report's provenance wording.
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active.** Two observations were posted at Session 32.
- **All five Tier A / packet / RC-002 chats are concluded.**

**If RC-003 closes `Approved`, the next work is the first real candidate measurement** (§5.2). **Until it closes, do not read a candidate and do not measure one.**

**If it does not close `Approved`, clause 5 fires: no third like-for-like card. The work is split or redesigned and the changed boundary is named.** The natural split, if it comes to that, is between the *reader* (`archive_units.py` — resolving band units under bounded cost) and the *command* (`measure_host_drift.py` — asset resolution, clock validation, gate application); they have been reviewed as one candidate three times and their findings have never overlapped. **That is a suggestion, not a decision, and it should go to the director rather than being adopted unilaterally.**

## 3. What Session 32 did — RC-003 Round 2's two blockers, repaired

**Both accepted in full, neither disputed. His probe reproduced unmodified before anything was edited: `negated_toolchain_reaches_verdict=True`, `mismatched_conversion_values_reach_verdict=True`, `default_block_transfer=2081456`.**

- **F1 — a search is not authentication.** `neuroconv` as a substring admitted `This asset was NOT created using NeuroConv; exported by LocalTool v3`. Now `CONVERSION_SOURCE_FORM = ^created using neuroconv v(?P<version>\d+(?:\.\d+)*)$` matches the **whole** value, case-insensitively, whitespace-stripped, via the helper `conversion_version(value)`. `authenticate_provenance_pair(first, second)` then requires both assets of one session to name the **same** version, run in preflight through `read_band_units(..., expect_conversion=raw_auth)`. **`MEASURED_CONVERSION_VERSIONS = ("0.9.1", "0.9.2")` is reported and NEVER gated on** — that tuple is from 21 *raw* assets and the one `v0.9.1` belongs to **NYU-39, a host subject**, so the dandiset is not uniform.
- **F3 — a request is not a transfer, and then the measurement moved the repair up a level.** `BoundedReader` now models the reader's block cache and charges each read the **distinct bytes it would newly fetch**, refusing before delegating, against `provenance_transfer_budget(block) = PROVENANCE_MAX_BYTES + len(PROVENANCE_PATHS) * block` (None for a reader with no block, where transfer == request). **But instrumenting his own construction showed all 2,081,456 of his bytes were spent by preflight BEFORE `source_provenance` was called; the provenance read itself transferred 0.** So the caller's **declared ceiling** is held open as a transfer budget for the whole read, entered before `h5py.File` opens the file (`_ceiling_budget`). His one-byte ceiling now moves **0 bytes**. **The licensing argument: `peak_resident_bytes ⊇ cache_bound_bytes ⊇ distinct transfer`, so this cannot refuse anything the later check would have admitted.**
- **Budgets nest.** `BoundedReader._scopes` is a stack; a read must fit **every** enclosing scope and is charged to all only once it fits. `ReadBudgetExceeded` carries `.scope`; `PROVENANCE_SCOPE` / `PREFLIGHT_SCOPE` are the two labels, and `_own_refusal(exc)` re-raises anything that is not the provenance scope's own — otherwise a ceiling refusal would be recorded as a per-path marker, a failure reporting itself as a success.
- **`read_provenance` caps the raw asset's block** at `PROVENANCE_BLOCK_BYTES = 65536`: 327,680-byte bound instead of 4,259,840.
- **E1 closed.** The report no longer says provenance values are carried "in full".
- **Two non-repair changes, both declared in the card and the chat.** `verify_rc003_round1_repairs.py`'s F3 check required the Round-2 message after a nonzero spend, so it reported the improvement as a failure; it now accepts either bound. And `test_measure_host_drift.py` closes its readers before `rmtree`, fixing the silent Windows leak (111 leftover directories by Session 31, 28 more deleted this session, zero after a full run).

## 4. The estimator and the readers, as they stand

`band_drift.py` public surface (unchanged, approved): `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** The symbol is `Delta_10min`. Band keys are `delta_full` / `delta_window` / `window_start`; `apply_gate` returns **`passed`** (not `passes`).
- `measure_band_drift(spike_times, depths, extent_s, params=None)` returns `measurable`, `reason` when False, and when True **six** per-unit audit lists aligned with `included`: `unit_delta_full`, `unit_delta_max_window`, `unit_max_window_start`, `unit_max_window_defined_bins`, `unit_delta_band_window`, `unit_band_window_defined_bins`. **`delta_max_window` is the per-unit list's name; the band's is `delta_window`.**
- `permutation_null(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` — **does not take the observation.**
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)`, **anchors at 0**; spikes below zero fall outside every bin and are silently excluded — the reader counts and reports them.
- **A recording needs at least 11 analysed bins.** Candidates carry 54–87.

`archive_units.py` public surface: `ReadBudgetExceeded` (now with `.scope`) · **`BoundedReader`** (`.block_bytes`, `.last_spend`, `budget(read_bytes, transfer_bytes=None, label=...)`) · **`provenance_transfer_budget`** · `ascii_safe` · `read_flat_electrodes` · `column_descriptions` · `source_provenance(handle, reader, max_bytes=PROVENANCE_MAX_BYTES)` · `provenance_is_complete` · **`conversion_version`** · `authenticate_provenance(provenance, source)` · **`authenticate_provenance_pair(first, second)`** · `read_provenance(url, size, block_bytes)` · `read_integer_column` · `read_unit_scalars` · `check_ragged_alignment` · `resolve_unit_electrodes` · `select_band_units` · `chunk_byte_ranges` · `column_layout` · `python_structure_bytes` · `band_slices` · `plan_transfer` · `read_band_units` · `electrode_tables_agree`. Private: `_stored_value_bytes`, `_capped`, `_decode`, `_blocks_covering`, `_slice_blocks`, `_slice_bounds`, `_own_refusal`, `_ceiling_budget`.

- **Constants:** `PROVENANCE_MAX_BYTES = 65536` (request budget, **cumulative over the whole `source_provenance` call**) · `PROVENANCE_BLOCK_BYTES = 65536` · `CONVERSION_SOURCE_FORM` / `CONVERSION_SOURCE_FORM_TEXT` / `CONVERSION_SOURCE_TOKEN` / `MEASURED_CONVERSION_VERSIONS` · `PROVENANCE_SCOPE` / `PREFLIGHT_SCOPE` · `REQUIRED_PROVENANCE_PATH`.
- **`read_band_units(..., max_bytes=None, plan_only=False, expect_conversion=None)`** returns `provenance_pair` and `provenance_io` alongside `provenance_authentication`.
- **`read_provenance` returns `provenance`, `provenance_io`, `io`.**
- **A refused read spends neither budget**, so an oversized value does not stop later paths being read; the required path is first.
- **`column_layout(dataset, slices=None)`** — pass the slices or a chunked column falls back to `whole file`.
- **`plan_transfer(..., spent_bytes=0, held=())`** — `held` is charged into `structures_bytes`; `read_band_units` passes four objects.
- **Plan keys:** `logical_bytes` · `cache_bound_bytes` · `resident_bytes` · `structures_bytes` · `library_cache_bytes` · `peak_resident_bytes` · `bound_basis` · `block_bytes` · `spent_bytes` · `per_unit` · the two layouts. **There is no key called `bytes`.**

`measure_host_drift.py`: `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`.**
- **`io` has FOUR sources:** `raw_provenance` · `raw_electrodes` · `raw_timing` · `processed_units`. The ceiling covers only the last — but it is now *also* a transfer budget over the whole processed read.
- **`record["provenance_io"]` carries `raw` and `processed`,** each with `read_budget_bytes` / `read_bytes` / `transfer_budget_bytes` / `transfer_bytes` / `block_bytes` / `label`.

### 4.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires on every case that reaches a record that `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`, and raises if it matched no reader at all. **Do not weaken this into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size** (Session 31). `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4` for exactly that reason. **Do not change it back.**
3. **The provenance-budget invariant (new, Session 32).** On every case that reaches a record and on **both** assets, `read_bytes <= read_budget_bytes` and `transfer_bytes <= transfer_budget_bytes`. **It only has teeth on a block-caching reader** — with `LocalFile` the transfer equals the request — which is why `case_command_reports_a_block_readers_expansion` runs the whole command with `archive_units.RemoteFile = BlockLocalFile`. **Do not remove that case thinking the invariant covers it.**

## 5. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 5.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Do not re-derive it and do not re-sort it.** Ranks 4–5 outrank rank 3 on channel count deliberately. NYU-39 at rank 9 is deliberate — deprioritized, never disqualified, **and the label-blind unit set is what keeps it that way.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first; cannot change a verdict, only cost): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

### 5.2 The next piece of work, once RC-003 closes

**Measure rank 1 — CSHL047 Probe01, session `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`.**

**Run `--plan-only` first, then measure free RAM against `peak_resident_bytes` — not against `resident_bytes`, which is one term of it — and free bandwidth-tolerance against `cache_bound_bytes`, then read.** The raw file's `t_first_s` for this series is **1.138 s**, so its bin 0 carries 58.86 s of coverage out of 72 bins and `head_partial_s` will be non-zero.

Command shape, **from inside the packet folder**:

`python scripts/measure_host_drift.py --session <uuid> --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

**When it has actually been executed it becomes runbook step 11**: add the README step, **remove its entry from the checker's `PENDING_STEP`** (the checker errors if a script is both a step and pending — and there is a mutation proving that), and re-run `check_runbook_consistency.py`.

**Four things to watch on the first real read.**
1. Resolving the chunk map costs one `get_chunk_info_by_coord` per touched chunk — thousands of lookups on a real asset, and `--plan-only` is where the cost shows up.
2. The provenance read is part of preflight, so `spent_bytes` includes it.
3. **If a real asset's `general/source_script` is absent, oversized, or is not the measured conversion statement, the run STOPS as an input error at zero spike cost — on the raw asset too.** §16.4 says that pauses the pinned order rather than rejecting the candidate. **New and stricter since Session 32: it also stops if the raw and processed assets name DIFFERENT converter versions.** If either fires on a real candidate, that is evidence, not a bug; report the values and amend the rule rather than loosening it in place.
4. **New since Session 32: the declared ceiling now refuses a fetch during preflight**, not only at the plan. At the `--max-mib 1024` default that will never fire; at a small ceiling it fires early and the message names the "declared ceiling transfer budget" rather than listing the plan's parts.

### 5.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Do not reopen §1–§16** — it belongs in a future section. **Codex still owns the footprint/placement calibration**; do not start it.

## 6. What is still not done

1. **No host is pinned**, and that is correct.
2. **No candidate has been measured.** The reader exists but is unapproved — three times now.
3. **The capacity gate needs re-establishing** under Amendment 6's stricter condition (§5.3).
4. **Five of the ten packet steps still have not been re-run** (the archive-reading ones). The README says so.
5. **The preprocessing half of the amplitude question is untouched** and not metadata-answerable — Rung 0 territory.
6. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question, not a coding one.
7. **`is_injectable` is a denylist over a partly derived vocabulary.** Latent: no consumer reads it.

## 7. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** · **the real-arm donor-matching rule** · **the exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 8. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`, `G0` the mean paired sorter gap *in the control arm*** — not the negative-control band. `[−T, T]` is declared shorthand for the `D` rule, never a second test. `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins, not ten.** Widening is monotone and can only reject more. Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those are input errors that pause the pinned order (§16.4), and the reader enforces that separation in its exit status.
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** `0.000`/`15.000`/`30.000 µm` describes the **equal-baseline fixture** only. A median tracks rank, so displacing `k` of a bin's `n` spikes upward moves its median **at most the displacement itself and at most the distance to the depth `k` ranks above it** (0 violations, 4,000 random cases; Codex's exhaustive check: 93,184 cases). On a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`. **The gate has no guaranteed resolution below the bin width in either direction. The old "permissive" claim is WITHDRAWN and must not be re-derived on the new bound.**
- **The drift unit set is blind to `kilosort2_label`** and is selected by valid same-probe `max_electrode -> rel_y` inside the band. **That choice carries no one-way safety guarantee.**
- **The per-unit excursions are reported and never consumed**, they carry no null, and they do not discharge that conditional in either direction. **Never compare a per-unit value to `Q95_null` or to `L`.** **And the absence of magnitude separation is not evidence either.** **The claim that masking strengthens with band size is WITHDRAWN.**
- **The bin grid anchors at session `t = 0` with extent `t_last_s`**, on pinned converter provenance. **`duration_s` is a span and is not an alternative clock hypothesis.** Endpoint containment is a consistency check that cannot identify a clock.
- **The head bin is retained and reported, with no claimed direction.**
- **The permutation pool is analysed-bin spikes only**, for both observation and null.
- **`cumulative_drift_um_per_hour` is retired on its own description.**
- **Amendment 6 governs: Tier A is parameterized by `N`.** `10 ≤ N ≤ 16` continues; `N < 10` is Slot 12.3. Fifty occurrences split `q = ⌊50/N⌋`, `r = 50 mod N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.**
- **`N ≥ 10` is structural:** `16 − 6 = 10` = the injected-unit count Slot 7 fixes.
- **The manipulation check is a hard stop-or-go gate**, and the realized zone-donor count is a *composition-integrity* quantity, **not** a substitute for it.
- **Amendment 5:** the injection zone's donors are removed from the **real** region-unaware arm before matching. The frozen matching rule runs as a non-generating counterfactual on **both** pools, with only the post-removal state permitted to govern generation.
- **The matching rule's provenance test is two-level:** **Level A** matches distinct dataset, session *and* subject counts; **Level B** is the contract's literal `S_T` floor. **Level A binds only at stages 3 and 4.**
- **Before any real target manifest, host-specific pool or edge table exists**, the exposure-schedule/placement specification, the matcher implementation, exhaustive synthetic tests and same-state implementation approval must all be complete.
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
- **The donor library's acronyms sit at mixed levels of the CCF hierarchy.** CA1 is a leaf and unaffected; **any zone change must check for parent-labelled donors first**.
- **A one-command-per-side runbook rule is a hard parse error, not a warning.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count that reported one of its three reads; S27's five; S28's three plus the Round-2 ASCII claim that was wider than its check; S29's one, which closed RC-002 unapproved; S30's three, which returned RC-003 Round 1; **and S31's two, which returned RC-003 Round 2: a substring token search treated as authentication, and a read budget denominated in requested bytes treated as a bound on transfer.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5). **S16–S22, S23, S24, S29, S30, S31: the thing needed was already on disk, already computed, already stated, already readable. S32 is the version that changed a repair rather than confirming one: `results/subject_provenance.json` held not just the token but the *whole measured sentence* and the fact that its one outlier version belongs to a host subject — which is what made "match the form, report the version, gate the pair" derivable instead of chosen.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5). **S17: for a host gate, pessimistic *is* the safe direction. S28: when the safe bound is loose, ask what a wrong refusal costs. S30: an invariant that fires falsely on eighteen good cases is indistinguishable from a broken test. S31: requiring provenance can stop the whole pinned order. S32 adds a rule for choosing: when the strict branch's failure mode is a *pause* and the permissive branch needs evidence you do not have, take the strict branch and say what would resolve it.**
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **Reviewer's version: review it against the contract, not against your own last draft** (S16).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and backslash escapes* — S32 proved it twice in one session, both times on a `\n` inside a mutation string. Write the script with the Write tool and run it.** **`$VAR` does not expand inside the Bash tool's `-c` string**; pass the path as `argv`. **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.** **A heredoc that `print`s a non-ASCII character dies on cp1252** (S30). **`/tmp/...` written by the shell is not the `/tmp/...` Python sees on Windows** (S31).
7. **Removing an unverified claim can create a new one** (S7). **S26: a repair can create a *new false claim*. S29–S30: a new *false check*. S31: it can silently *delete* a true check. S32: and it can silently invalidate a *sibling script* — `verify_rc003_round1_repairs.py` began reporting an improvement as a failure because its assertion encoded which bound was expected to refuse.**
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30, S31). **S32: and when you cannot avoid a number, derive it. `provenance_transfer_budget` is "the request budget plus one block per provenance path", with the first term provable (`C + 2B` covers any legal value at any offset) — not a value that worked on the fixtures.**
9. **Read a rich first-party table, not one column of it** (S7). Read the column's own `description` too — **and S27: make the code read it.**
10. **Verify a name before trusting it** (S7). **S22–S32: run the probe they hand you, unmodified, against the unchanged candidate, before editing. Five cards running; three of three, and this session two of two plus his exact byte count.**
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S31). **S32 is the sharpest instance: a request and the transfer that serves it are both "bytes", and at a 1 MiB block they differ by five orders of magnitude.**
12. **When a safety check fires, measure it before loosening it** (S8). **S19 inverse: when a cost is cited for *not* doing something, measure it. S30: when a *new* check fires on everything at once, suspect the check. S32 third inverse: when a reviewer hands you a number, measure where it actually came from before repairing what you assume produced it — all 2,081,456 of his bytes were spent before the read his finding named.**
13. **A correction is worth logging even when the conclusion survives** (S8, S29).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9); a *better* reason arriving is also that moment (S15).
16. **An audit must use the same key its lookup uses** (S9, S27, S28, S31).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10). Fifteen for fifteen.
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17, S23, S28, S29).
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11, S27–S29).
24. **Note which direction a correction pushes** (S11, S15, S16, S26).
25. **When a test fails, first ask whether the test or the artifact is broken** (S11). **`apply_gate` returns `passed`. `measure_band_drift` returns `delta_window`. Read the parser.**
26. **Render the output; do not read the source and assume you know what it prints** (S12). **Read the finished section back as a reviewer** (S16, S18–S32). **Thirteen consecutive sessions where the read-back pass produced a correction — S32's was "at a 0-byte block", which is how a reader with no block cache was being described.**
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26).
31. **A supersession can be too broad as well as too narrow** (S14).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28).
33. **Make an edit script assert exactly one match per replacement** (S14). Validate every replacement across every file *before* writing any of them. **S29: read the anchor out of the file rather than from your own memory of it. S32 got that wrong once and the assert caught it: the card's E1 paragraph uses typographic dashes and quotes, and an anchor typed with the ASCII forms matched nothing. The fix was to slice the anchor out of the file.** **And an anchor that is unique in one row can appear in two: two table rows ended with the same sentence, which the count assert caught before anything was written.**
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Fifteen for fifteen (S15–S32).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21). **S32: and so does a tightening inside your own safety check. Holding the declared ceiling open is licensed by `peak_resident_bytes ⊇ cache_bound_bytes ⊇ distinct transfer`, which is why it can only refuse earlier and never more.**
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.**
41. **Read the clock at the moment you write the timestamp** (S17). **Write the message with a placeholder and substitute the clock reading in the same command that appends it. `time.strftime("%Z")` returns the long timezone name on Windows: use a literal `PDT`.** S30–S32 used the placeholder route for every timestamped write.
42. **A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24).
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S31). **S32: and state which of two *currencies* it is denominated in, because a bound in the wrong one is not a bound at all.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26). Six caught.
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28).
50. **A counterexample built on a degenerate case invites dismissal** (S24). **S26 is the mirror: check whether it is *stronger* than claimed.**
51. **A near-miss is not the finding** (S24). Sweep the parameters to establish the regime exists.
52. **A test can encode the defect it was written to catch** (S25, S28). **A harness written from the implementation confirms the implementation.**
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25).
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32).
56. **Which fixture a published number came from is part of the number** (S25, S26).
57. **A check that cannot fail is not a check** (S27–S30). **S31's inverse: a check you *believe* cannot fire may still fire — construct the thing that reaches it before deleting it. S32's third form: an invariant can be live and still toothless. The new provenance-budget invariant compares transfer against request, and on the default local reader those are the same number; only a block-caching reader gives it teeth, which is why one end-to-end case installs one.**
58. **Method notes for the Review Method Change chat.** S26–S32 posted thirteen between them.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30).
61. **⚠️ A repair can silently remove the coverage a mutation depends on, and a green suite is not sensitive to it** (S31). **Re-run the mutation harness after every repair, not only after adding a mutation.**
62. **Evidence must come from the exact state you publish digests for** (S31). Compute digests from the files at write time rather than typing them.
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32). Three of six new ones did: two made the suite *crash* rather than fail (a stub missing a new field; a budget removed by passing `None`, which made an invariant compare `None` with `None`), and one named a check whose name contained a space, which the harness's first-token prefix matching can never match. **Write mutation replacements that keep every other contract intact, and give every check a whitespace-free name.**
64. **When a reviewer's finding is correct, check whether it is *complete* before repairing it** (S32). His F3 was right about the budget and pointed at a read that spent nothing. The repair that mattered was one level up, and the only way to know was to measure the decomposition rather than the total.

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Session 32 reading: 00:1x PDT — 17,104 MB available physical RAM of 32,425, 18.5% of the commit limit in use, 106,271 of 130,415 MB pagefile available.** Everything this session ran was synthetic; the largest fixture was about 2 MB. **Read all three numbers, not one:** `FreePhysicalMemory` excludes reclaimable standby, and committed bytes against the commit limit is the one that decides whether a new process can start. **Do not inherit these; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64`; a numpy change is a replay risk and the drift result must be re-replayed after one.** **h5py's chunk-index and property-list APIs are load-bearing** — `get_chunk_info_by_coord`, `get_access_plist().get_chunk_cache()`, `check_string_dtype`, `id.get_storage_size()`, the fact that h5py requests a global-heap collection's bytes through the file object before materializing a variable-length value, **and — new at Session 32 — the fact that h5py serves a collection it has already read without asking the reader again, so a value read whole can cost the request budget almost nothing.** An h5py change is a transfer-bound risk. Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

## 11. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins** and both agents append the round log and the outcome to it. **RC-003's index row must be updated when it closes.**
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section.**
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry landed inside the log section. **62 dated entries by a `grep -c "^- \*\*2026-08-1"` count; banner at 2026-08-16.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link.
- **Corrections propagate forward, never backward.** The review cycle is the only exception.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. **The `drift_reader_*` leak is FIXED as of Session 32** — the suite closes its readers before `rmtree` and warns if a directory survives — but `ls "C:/Users/cresp/AppData/Local/Temp" | grep -c "drift_reader\|rc002_mutation\|rc003_round"` is still the check, because other agents' probes leave their own. **The mutation harnesses take ~7 minutes each — run them with `run_in_background` and collect the output file. Their stdout is buffered when redirected, so an empty output file means "still running". ⚠️ Do not edit any file the harness copies while it is running: it copies `Reproducibility Packet/scripts/**` and `agents/Claude/tools/test_measure_host_drift.py` afresh per mutation. `mutate_rc002_repairs.py` itself is NOT copied, so editing that file mid-run is safe.**
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **total every read rather than the last one.** **A retry re-transfers a block, so `n_bytes` can exceed the file size; the plan's `cache_bound_bytes` bounds *distinct* blocks.** **The reader's cache is unbounded and never evicted, which is why it is a memory term.** **`BoundedReader` wraps it, forwards both counters, and now also models its block cache** — `reader.block_bytes` is `getattr(inner, "block", 0)`, so a stand-in reader that declares no block is treated as fetching exactly what it is asked for.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`.
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` needs no step. **A script in `scripts/` without a step is a hard failure unless it is declared in `PENDING_STEP`** — and a script that is both a step and pending is also a failure, and both rules have mutations. **After editing the packet runbook or any script docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **`mutation_test_runbook_checker.py` takes three positional arguments**, not flags: packet path, scratch directory, interpreter. It leaves its scratch directory behind — delete it.
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. **Check the printed surface by capturing `--help`, not only by scanning source** — and check the *source* too: a `§` typed into a docstring failed `report/sources are ascii` in Session 32. **Values read out of an asset are not yours** — render them through `archive_units.ascii_safe` before printing or reporting.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (168/168 as of Session 32); the root `README.md`, the selection document, the Review Cards and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert CR == LF afterwards.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path (`C:/Users/cresp/AppData/Local/Temp/ct`), comparing file by file, and **deleting the clone afterwards.**
- **Both `.gitignore` files carry a do-not-catch-these comment and ignore `__pycache__/`.**
- **`agents/Claude/tools/` holds ten scripts and one recorded output**, `source_count_granularity_probe_2026-08-13.txt`, because the matching rule cites its numbers.
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations`; `probe_band_drift_claims.py` takes `--module`; `test_measure_host_drift.py` takes `--keep` and `--tmp-root`; **`mutate_rc002_repairs.py`, `verify_rc003_round1_repairs.py` and `verify_rc003_round2_repairs.py` require `--repo-root`**; Codex's probes take `--repo-root` (`probe_rc001_round1.py`, `probe_rc002_round2.py`, `probe_rc002_round3.py`, `probe_rc003_round1.py` and `probe_rc003_round2.py` require it).
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state — and `git checkout -- <path>` is the clean way to undo a mangled edit script before retrying it properly.
