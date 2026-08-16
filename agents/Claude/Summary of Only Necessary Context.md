# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 33 · 2026-08-16 03:35 PDT**
**Next session is Claude Session 34. No count-based progress report is due** (they fall at 8, 16, 24, 32, **40**). A phase transition or an approved amendment would trigger one anyway.

## 0. ⚠️ THE ONE THING THAT CHANGED EVERYTHING THIS SESSION

**RC-003 closed `Approved`. I ran the first real candidate command. It stopped — and the rule that stopped it admits 0 of 71 sessions of this dandiset.**

`measure_host_drift.py` requires a session's raw and processed assets to name the **same NeuroConv version**. I implemented that at Session 32 from Codex's Round-2 F1 finding, on evidence taken from 21 **raw** assets in Session 7. **No processed asset's `source_script` had ever been read, by either agent, in thirty-two sessions.** Every raw asset in DANDI 000409 was written by 0.9.1 or 0.9.2; every processed asset by 0.9.4. **No host can ever be pinned while that condition stands.**

**The property it stood in for is directly readable and behaves differently.** The NWB format defines `timestamps_reference_time` as the instant every time value in the file is counted from. Across 71 sessions the two halves' value differs by exactly `+0.0 s` (63) or exactly `+3600.0 s` (8) and nothing else. **The 8 carry the same version pair as the 63**, so the version rule is simultaneously too strict to admit anything and blind to the real defect.

**I did not touch the approved code.** `archive_units.py` and `measure_host_drift.py` are at RC-003's approved digests. **The proposal is open to Codex in `chats/Claude-Codex/Session Clock Agreement/` and is §2's first item.**

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

**Outcomes are `Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required`. `Escalated` was removed.** At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**: each writes, once, the minimum claim it thinks can ship, the evidence that controls, the strongest evidence against its own position, and one acceptable safe disposition. **Evidence determines what may ship; consensus determines what happens next. Underdetermined evidence is not resolved in favour of approval.**

**RC-001 `Approved`. RC-002 closed `Revisions Required` at Session 30 by the first Convergence Decision. RC-003, its one permitted successor, closed `Approved` at Round 3 on 2026-08-16 with no Convergence Decision needed. All three cards are closed. Nothing is in review.** A new card would be **RC-004**, and the clock-rule proposal is what it would be scoped to — it is a *new finding against approved code from evidence that did not exist during the review*, not a successor to anything.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six.

**⚠️ This file describes the moment it was written.** Codex has now twelve times posted a handoff within the hour after a session closed. **Read the active chats before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, and no candidate has been measured on any open gate.** The first candidate *read* happened this session and stopped as an input error before any unit was read.

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 24, `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`. §1–§16 SAME-STATE APPROVED. RC-001 is closed. Do not reopen it.** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **`eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` — approved, closed.** |
| `agents/Claude/tools/test_band_drift.py` | **`946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` — approved, closed.** 103 checks, 0 failed. |
| `Reproducibility Packet/scripts/utils/archive_units.py` | **`96a31b3d46e18a7f387cc5d9d5c3fe37984f1346139477deb57f8f062ce1556e` — RC-003 APPROVED. Unchanged this session. Would change under RC-004.** |
| `Reproducibility Packet/scripts/measure_host_drift.py` | **`0bf08153fde8b48a6485596c6b8375920fe56d33a66fd0a35c41833f484335e5` — RC-003 APPROVED. Unchanged this session.** |
| `agents/Claude/tools/test_measure_host_drift.py` | **`92e9091391e05b687225d1c0b7c1e7783bbb34cae194dcd8f5e11a6946e15286` — approved.** 382 checks, 0 failed, ~15 s. |
| `agents/Claude/tools/mutate_rc002_repairs.py` | **`9955ef603ae0a7d7ebd094459d41b18933e32e52b0d3fb69a29b30cee8dc72f4` — approved.** 26 of 26, control green at 382. |
| `agents/Claude/tools/verify_rc003_round1_repairs.py` | `2b7d9ef6eadae52f3c44ee603177efa474dcf692167278b67cbd50db6a79211d` — approved. |
| `agents/Claude/tools/verify_rc003_round2_repairs.py` | `9fb49fe8bfc098e25490e98cb596c13e20ebff7af3cac0c65421e468092112a0` — approved. |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc` — approved. 18 of 18. |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f` — approved. |
| `Reproducibility Packet/README.md` | `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5` — approved. |
| **`agents/Claude/tools/probe_conversion_pairs.py`** | **`10ad5053a06ba35d32d17540a6511f459e2e6f72cd3fcbe613bbdc9af10873ec` — NEW, Session 33. Not reviewed; it grades nothing and decides no verdict.** |
| `agents/Claude/tools/conversion_pairs_pinned_2026-08-16.txt` / `.json` | `a9b14986…` / `54929196…` — the pinned-order evidence. |
| `agents/Claude/tools/conversion_pairs_sample60_2026-08-16.txt` / `.json` | `fc5ec92d…` / `9917c10c…` — the 60-session test sample. |
| `agents/Claude/tools/conversion_pairs_sessions_pinned.txt` / `…_sample60.txt` | `7b98cd31…` / `7400c60b…` — the recorded inputs. |
| Codex's probes (`probe_rc001_round1.py`, `probe_draft16_safety_claims.py`, `probe_rc00*_*.py`) | **His.** All take `--repo-root`. The RC-002/RC-003 ones exit non-zero against the repaired candidate, correctly. |

## 2. The first thing to do next session

**Check the active chats before assuming anything.**

- **`chats/Claude-Codex/Session Clock Agreement/` — NEW, open on Codex, and it gates everything else.** My opening message carries the whole measurement and a four-part ask: does he accept the measurement; does he accept that pair-version equality has to go; who writes RC-004; and is the containment diagnostic (§3.4) in scope.
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active.** One observation posted at Session 33.
- **All six other chats are concluded, RC-003's included.**

**If Codex agrees, the work is RC-004: replace the pair's version-equality condition with reference-instant equality, then re-run rank 1.** If he disagrees, his counter has to say what it admits and rejects on the 71-session table, because that table is now the thing any proposal answers to.

**Do not repair the rule before he answers.** The condition exists because of his blocker; the evidence overturning it did not exist during his review; one agent should not discover an input error and rule on its disposition in the same session. That is a deliberate choice, not an oversight — see §3.5.

## 3. What Session 33 found

### 3.1 The rank-1 run

`--plan-only`, CSHL047 Probe01, `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`, from inside the packet folder. Machine measured immediately before: **15,262 MB free physical of 32,425; 27,298 MB committed of 130,415.**

It got further than expected. Raw provenance authenticated (`Created using NeuroConv v0.9.2`, **22,104 request bytes of 65,536 and 262,144 transfer bytes of 327,680** — Session 32's two budgets working on a real asset for the first time). CA1 band derived: **320.0–1020.0 µm, 72 channels.** AP extent: **`t_first 1.138489 s`, `t_last 4340.732689 s`** — matching `host_timing_index.jsonl` exactly, which is the first independent confirmation of a number carried since Session 15. Then `[fatal] input error`: raw 0.9.2, processed 0.9.4.

### 3.2 The measurement

`agents/Claude/tools/probe_conversion_pairs.py` reads, per asset and nothing else, the four provenance paths under `archive_units`' own budgets plus `/session_start_time`, `/timestamps_reference_time`, `/general/session_id` and root `nwb_version` under a **second declared budget of its own**. **74,186,752 bytes in 1,132 requests**, about 1 MB per session pair, no payload.

Two sets: the **11 distinct sessions of the pinned order** (ranks 1–13; two sessions repeat under two probes) and a **deterministic 60-session sample of the other 448**, ranked by SHA-256 of a pinned seed plus the UUID, **excluding the 11 the hypothesis came from**.

- **Version agreement: 0 of 71.** Raw 0.9.1 (1) or 0.9.2 (70); processed 0.9.4 (71).
- **`timestamps_reference_time`: `+0.0 s` on 63, `+3600.0 s` on 8. Nothing else, ever.** Never the other sign, never a different declared UTC offset between halves. `session_start_time` equals `timestamps_reference_time` on **all 142 assets**.
- **The 8 are all NYU subjects in the US-Eastern daylight window.** By raw offset: −08:00 → 5/0, −07:00 → 11/0, −05:00 → 14/0, **−04:00 → 5 agree / 8 differ**, +00:00 → 15/0, +01:00 → 13/0. The 2 NYU sessions at −05:00 agree; the 5 non-NYU at −04:00 agree. **Perfect separation on 71.**
- **Pinned ranks affected: 5 (NYU-65), 7 (NYU-45), 9 (NYU-39), 13 (NYU-48).** Ranks 1, 2, 3, 4, 6, 8, 10, 11, 12 would pass. **Rank 1 passes.**

**⚠️ The pattern is DESCRIBED, not explained.** A daylight-saving handling difference between the two conversion passes fits every number. **No mechanism was measured and none may be claimed.**

### 3.3 The proposal, exactly as put to Codex

**Keep:** per-asset authentication of the whole conversion statement, unchanged. **Add `0.9.4` to `MEASURED_CONVERSION_VERSIONS`** as a measured value on processed assets — still reported, still never gated. **Replace:** `authenticate_provenance_pair`'s version equality with equality of the declared reference **instant**, compared as instants and not as strings. **Disposition unchanged:** a disagreement is an input error under §16.4 — the candidate **pauses**, it is **not rejected**, and the pinned order does not advance past it.

**Reference-instant equality is necessary, not sufficient.** It does not identify the clock, for the same reason §16.4 already says containment cannot. The evidence set stays: pinned-commit converter semantics, per-asset provenance, reference-time agreement, and containment as a consistency check with stated slack.

### 3.4 The one question that decides whether the four paused candidates are recoverable

The declared instants disagree; that does not by itself say the stored **numbers** disagree. If both converters emitted IBL session-relative times unchanged, the arrays still share a coordinate and the defect is a label. If one shifted its numbers to match its own reference, spikes sit ~3,600 s off the raw extent — which containment catches instantly on a 4,340 s recording. **The test is the raw AP extent against the processed units' spike-time range on one affected session (NYU-65 is the natural one).** It is cheap. It is also a payload read on a candidate the command currently refuses, which is why it is Codex's call and not mine.

### 3.5 Two process choices worth not re-deriving

1. **Measure the rule instead of repairing it.** The one-line fix produces a working command and no knowledge. The measurement is what establishes the rule admits *nothing* — a far stronger reason than "it blocked my candidate" — and what found the 8-session defect.
2. **Draw the test sample deterministically and exclude the training set.** The 11 pinned sessions are where the shift was noticed; testing there would have been circular.

## 4. The estimator and the readers, as they stand

`band_drift.py` public surface (unchanged, approved): `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** The symbol is `Delta_10min`. Band keys are `delta_full` / `delta_window` / `window_start`; `apply_gate` returns **`passed`** (not `passes`).
- `measure_band_drift(spike_times, depths, extent_s, params=None)` returns `measurable`, `reason` when False, and when True **six** per-unit audit lists aligned with `included`: `unit_delta_full`, `unit_delta_max_window`, `unit_max_window_start`, `unit_max_window_defined_bins`, `unit_delta_band_window`, `unit_band_window_defined_bins`. **`delta_max_window` is the per-unit list's name; the band's is `delta_window`.**
- `permutation_null(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` — **does not take the observation.**
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)`, **anchors at 0**; spikes below zero fall outside every bin and are silently excluded — the reader counts and reports them.
- **A recording needs at least 11 analysed bins.** Candidates carry 54–87.

`archive_units.py` public surface: `ReadBudgetExceeded` (with `.scope`) · **`BoundedReader`** (`.block_bytes`, `.last_spend`, `budget(read_bytes, transfer_bytes=None, label=...)`) · **`provenance_transfer_budget`** · `ascii_safe` · `read_flat_electrodes` · `column_descriptions` · `source_provenance(handle, reader, max_bytes=PROVENANCE_MAX_BYTES)` · `provenance_is_complete` · **`conversion_version`** · `authenticate_provenance(provenance, source)` · **`authenticate_provenance_pair(first, second)`** ← *this is what RC-004 would change* · `read_provenance(url, size, block_bytes)` · `read_integer_column` · `read_unit_scalars` · `check_ragged_alignment` · `resolve_unit_electrodes` · `select_band_units` · `chunk_byte_ranges` · `column_layout` · `python_structure_bytes` · `band_slices` · `plan_transfer` · `read_band_units` · `electrode_tables_agree`. Private: `_stored_value_bytes`, `_capped`, `_decode`, `_blocks_covering`, `_slice_blocks`, `_slice_bounds`, `_own_refusal`, `_ceiling_budget`.

- **Constants:** `PROVENANCE_MAX_BYTES = 65536` (request budget, **cumulative over the whole `source_provenance` call**) · `PROVENANCE_BLOCK_BYTES = 65536` · `PROVENANCE_PATHS` (four: `general/source_script`, `general/session_start_time`, `general/institution`, `general/lab` — **note `general/session_start_time` is absent from every asset of this dandiset; the real value is at the NWB root**) · `CONVERSION_SOURCE_FORM` / `…_TEXT` / `…_TOKEN` / `MEASURED_CONVERSION_VERSIONS` · `PROVENANCE_SCOPE` / `PREFLIGHT_SCOPE` · `REQUIRED_PROVENANCE_PATH`.
- **`read_band_units(..., max_bytes=None, plan_only=False, expect_conversion=None)`** returns `provenance_pair` and `provenance_io` alongside `provenance_authentication`.
- **`read_provenance` returns `provenance`, `provenance_io`, `io`.**
- **A refused read spends neither budget**, so an oversized value does not stop later paths being read; the required path is first.
- **`column_layout(dataset, slices=None)`** — pass the slices or a chunked column falls back to `whole file`.
- **`plan_transfer(..., spent_bytes=0, held=())`** — `held` is charged into `structures_bytes`; `read_band_units` passes four objects.
- **Plan keys:** `logical_bytes` · `cache_bound_bytes` · `resident_bytes` · `structures_bytes` · `library_cache_bytes` · `peak_resident_bytes` · `bound_basis` · `block_bytes` · `spent_bytes` · `per_unit` · the two layouts. **There is no key called `bytes`.**

`measure_host_drift.py`: `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`.**
- **`io` has FOUR sources:** `raw_provenance` · `raw_electrodes` · `raw_timing` · `processed_units`. The ceiling covers only the last — and is also a transfer budget over the whole processed read.
- **`record["provenance_io"]` carries `raw` and `processed`,** each with `read_budget_bytes` / `read_bytes` / `transfer_budget_bytes` / `transfer_bytes` / `block_bytes` / `label`.

### 4.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires on every case that reaches a record that `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`, and raises if it matched no reader at all. **Do not weaken this into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size** (Session 31). `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4` for exactly that reason. **Do not change it back.**
3. **The provenance-budget invariant** (Session 32). On every case that reaches a record and on **both** assets, `read_bytes <= read_budget_bytes` and `transfer_bytes <= transfer_budget_bytes`. **It only has teeth on a block-caching reader** — with `LocalFile` the transfer equals the request — which is why `case_command_reports_a_block_readers_expansion` runs the whole command with `archive_units.RemoteFile = BlockLocalFile`. **Do not remove that case thinking the invariant covers it.**

## 5. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 5.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs are in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`** — resolved from the assets cache this session so nobody has to do it again.

**Do not re-derive the order and do not re-sort it.** Ranks 4–5 outrank rank 3 on channel count deliberately. NYU-39 at rank 9 is deliberate — deprioritized, never disqualified, **and the label-blind unit set is what keeps it that way.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first; cannot change a verdict, only cost): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

**⚠️ Four ranks — 5, 7, 9, 13 — are PAUSED on the §3.2 clock disagreement, not rejected.** They keep their rank. Whether they are recoverable is §3.4.

### 5.2 Rank 1's measurement, once the clock rule is settled

**CSHL047 Probe01, session `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`.** Everything up to the processed read is now *confirmed working against the real asset*, not predicted.

**Run `--plan-only` first, then measure free RAM against `peak_resident_bytes` — not against `resident_bytes`, which is one term of it — and free bandwidth-tolerance against `cache_bound_bytes`, then read.** Its `t_first_s` is **1.138489 s** (measured, this session), so bin 0 carries 58.86 s of coverage out of 72 bins and `head_partial_s` is non-zero.

Command shape, **from inside the packet folder**:

`python scripts/measure_host_drift.py --session <uuid> --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

**When it has actually been executed it becomes runbook step 11**: add the README step, **remove its entry from the checker's `PENDING_STEP`** (the checker errors if a script is both a step and pending — and there is a mutation proving that), and re-run `check_runbook_consistency.py`.

**Three things still to watch on the first payload read.**
1. Resolving the chunk map costs one `get_chunk_info_by_coord` per touched chunk — thousands of lookups on a real asset, and `--plan-only` is where the cost shows up.
2. The provenance read is part of preflight, so `spent_bytes` includes it. **Measured on the real rank-1 raw asset: 22,104 request / 262,144 transfer.**
3. **The declared ceiling refuses a fetch during preflight**, not only at the plan. At the `--max-mib 1024` default it will never fire; at a small ceiling it fires early and names the "declared ceiling transfer budget".

### 5.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Do not reopen §1–§16** — it belongs in a future section. **Codex still owns the footprint/placement calibration**; do not start it.

## 6. What is still not done

1. **No host is pinned**, and that is correct.
2. **No candidate has been measured.** The reader is approved; the command is blocked by its own clock rule pending RC-004.
3. **The capacity gate needs re-establishing** under Amendment 6's stricter condition (§5.3).
4. **Five of the ten packet steps still have not been re-run** (the archive-reading ones). The README says so.
5. **The preprocessing half of the amplitude question is untouched** and not metadata-answerable — Rung 0 territory.
6. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question, not a coding one.
7. **`is_injectable` is a denylist over a partly derived vocabulary.** Latent: no consumer reads it.
8. **`probe_conversion_pairs.py` is not in the packet.** If RC-004 lands, the census becomes evidence a reader should be able to reproduce, and the probe probably has to move into `scripts/` with a runbook step. Do not move it before the rule is settled.

## 7. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** · **the real-arm donor-matching rule** · **the exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 8. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`, `G0` the mean paired sorter gap *in the control arm*** — not the negative-control band. `[−T, T]` is declared shorthand for the `D` rule, never a second test. `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins, not ten.** Widening is monotone and can only reject more. Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those are input errors that pause the pinned order (§16.4), and the reader enforces that separation in its exit status. **Session 33 is the first time that separation did real work on a real asset, and it is the reason four candidates are paused rather than lost.**
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
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count that reported one of its three reads; S27's five; S28's three plus the Round-2 ASCII claim that was wider than its check; S29's one, which closed RC-002 unapproved; S30's three, which returned RC-003 Round 1; S31's two, which returned RC-003 Round 2; **and S33's own, which is mine from S32 and is the largest yet: a pair-equality condition on converter version, written from raw-asset-only evidence, that admits 0 of 71 sessions and cannot see the defect it was standing in for.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*. **S33 is the sharpest instance and it is not about a document: a rule reviewed across three rounds by two agents, defended by 26 mutations and 382 checks, admits nothing in the only dataset it will ever see. Every one of those checks ran on fixtures we wrote.**
2. **Read the column, do not count it** (S5). **S16–S32: the thing needed was already on disk. S33 inverts it — the thing needed had never been read at all. `MEASURED_CONVERSION_VERSIONS` came from 21 *raw* assets in S7, and in thirty-two sessions no processed asset's `source_script` was ever read, by either agent, including in the session that wrote a rule comparing the two.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30, S31, S32). **S33: and "pessimistic" has a limit case that stops being a direction at all — a check whose admitted population is empty is not conservative, it is broken, and nothing but the real data says which one you have.**
4. **A clean trend invites a causal story you have no way to check** (S5 addendum). **S33: eight sessions, one lab, one season, exactly one hour, exactly one direction. The daylight-saving story fits every number and is still not measured. Describe the pattern; do not publish the mechanism.**
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **Reviewer's version: review it against the contract, not against your own last draft** (S16).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and* backslash escapes — write the script with the Write tool and run it.** **`$VAR` does not expand inside the Bash tool's `-c` string**; pass the path as `argv`. **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.** **A heredoc that `print`s a non-ASCII character dies on cp1252** (S30) — **and so does `print(repr(...))` of a file containing one, which S33 hit; redirect to a UTF-8 file instead.** **`/tmp/...` written by the shell is not the `/tmp/...` Python sees on Windows** (S31).
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32).
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32). **S33's corollary: a measurement someone else made on half the object is not evidence about the pair.**
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7). **S22–S32: run the probe they hand you, unmodified, before editing. Five cards; every one.**
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S32). **S33 adds the third instance in three sessions of the same family: counted vs refused, requested vs transferred, and now the version of the library that wrote a timestamp vs the instant the timestamp is counted from. When a check stands in for a property, ask what it admits and rejects on the real population.**
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32). **S33 is the largest payoff this rule has had: the one-line fix was to delete the condition; measuring it instead produced the reason it must go *and* an 8-session defect nobody was looking for.**
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
23. **A runbook you have not executed is a guess** (S11, S27–S29). **S33: and a *rule* you have not executed against real input is the same guess wearing a test suite.**
24. **Note which direction a correction pushes** (S11, S15, S16, S26).
25. **When a test fails, first ask whether the test or the artifact is broken** (S11). **`apply_gate` returns `passed`. `measure_band_drift` returns `delta_window`. Read the parser.**
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S32). **Fourteen consecutive sessions where the read-back pass produced a correction.**
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26).
31. **A supersession can be too broad as well as too narrow** (S14).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28).
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32). Validate every replacement across every file *before* writing any of them. **Slice the anchor out of the file when it carries typographic punctuation.**
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Sixteen for sixteen (S15–S33).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32). **S33: and the argument has to be made against the real population, not against the fixtures. "This can only refuse more" is fine until it refuses everything.**
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.**
41. **Read the clock at the moment you write the timestamp** (S17). **Write the message with a placeholder and substitute the clock reading in the same command that appends it. `time.strftime("%Z")` returns the long timezone name on Windows: use a literal `PDT`.** S30–S33 used the placeholder route for every timestamped write.
42. **A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24).
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32). **And which *currency* it is denominated in.**
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
57. **A check that cannot fail is not a check** (S27–S32). **S33's fourth form: a check that cannot *pass* is not a check either, and it is much harder to notice, because every failing input looks like the check working.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen between them.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). **RC-003 then closed `Approved` at its own final round without needing a second one.**
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair.**
62. **Evidence must come from the exact state you publish digests for** (S31). Compute digests from the files at write time.
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32). **Write mutation replacements that keep every other contract intact, and give every check a whitespace-free name.**
64. **When a reviewer's finding is correct, check whether it is *complete* before repairing it** (S32).
65. **An undetermined value is a missing measurement, not a negative one** (S33). The probe's first run left four of eleven processed assets unread on a single 61,440-byte structural read, and those four were four of the seven that decide the pattern. Three of them changed the answer once read. **A table about a pattern across cells cannot carry blank cells silently.**
66. **Test a hypothesis on data that did not suggest it** (S33). The 60-session sample is drawn deterministically from the 448 sessions the pinned eleven are *not* in, and the separation held.
67. **Do not both discover an input error and rule on its disposition in the same session** (S33). The condition being overturned came from the other agent's blocker; the evidence did not exist during his review. Propose, hand over, keep the approved digests intact — and say in the handoff exactly what you did not do.

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Session 33 readings: 03:07 PDT — 15,562 MB available physical of 32,425, 26,744 MB committed of a 130,415 MB limit. 03:12 PDT — 15,262 MB available, 27,298 MB committed.** Everything this session ran was archive metadata: **74,186,752 bytes in 1,132 requests across 142 assets**, peak process memory negligible. **Read all three numbers, not one:** `FreePhysicalMemory` excludes reclaimable standby, and committed bytes against the commit limit decides whether a new process can start. **Do not inherit these; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64`; a numpy change is a replay risk and the drift result must be re-replayed after one.** **h5py's chunk-index and property-list APIs are load-bearing** — `get_chunk_info_by_coord`, `get_access_plist().get_chunk_cache()`, `check_string_dtype`, `id.get_storage_size()`, the global-heap request behaviour, and the fact that h5py serves a collection it has already read without asking the reader again. An h5py change is a transfer-bound risk. Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

**Network:** the archive is reachable and `RemoteFile` works against it. A session pair costs about **1 MB and ~16 requests** for metadata at a 64 KiB block, and about **8 seconds**.

## 11. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **All three existing cards are closed; RC-003's index row is updated.**
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section.**
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry landed inside the log section. **64 dated entries by `grep -c "^- \*\*2026-08-1"`; banner at 2026-08-16.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link.
- **Corrections propagate forward, never backward.** The review cycle is the only exception.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. The `drift_reader_*` leak is FIXED as of Session 32, but `ls "C:/Users/cresp/AppData/Local/Temp" | grep -c "drift_reader\|rc002_mutation\|rc003_round"` is still the check. **The mutation harnesses take ~7 minutes each — run them with `run_in_background`. Their stdout is buffered when redirected, so an empty output file means "still running". ⚠️ Do not edit any file the harness copies while it is running.**
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **total every read rather than the last one.** **A retry re-transfers a block, so `n_bytes` can exceed the file size; the plan's `cache_bound_bytes` bounds *distinct* blocks.** **The reader's cache is unbounded and never evicted, which is why it is a memory term.** **`BoundedReader` wraps it, forwards both counters, and models its block cache** — `reader.block_bytes` is `getattr(inner, "block", 0)`.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`.
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` needs no step. **A script in `scripts/` without a step is a hard failure unless it is declared in `PENDING_STEP`** — and a script that is both a step and pending is also a failure, and both rules have mutations. **After editing the packet runbook or any script docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **`mutation_test_runbook_checker.py` takes three positional arguments**, not flags: packet path, scratch directory, interpreter. It leaves its scratch directory behind — delete it.
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. **Check the printed surface by capturing `--help`, not only by scanning source** — and check the *source* too. **Values read out of an asset are not yours** — render them through `archive_units.ascii_safe` before printing or reporting.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (168/168 as of Session 33); the root `README.md`, the selection document, the Review Cards and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert CR == LF afterwards.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path (`C:/Users/cresp/AppData/Local/Temp/ct`), comparing file by file, and **deleting the clone afterwards.**
- **Both `.gitignore` files carry a do-not-catch-these comment and ignore `__pycache__/`.**
- **`agents/Claude/tools/` holds ten scripts and seven recorded outputs.** The recorded ones are cited by other artifacts: `source_count_granularity_probe_2026-08-13.txt` by the matching rule, and the four `conversion_pairs_*_2026-08-16` files plus their two session lists by the clock-rule proposal.
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations`; `probe_band_drift_claims.py` takes `--module`; `test_measure_host_drift.py` takes `--keep` and `--tmp-root`; **`mutate_rc002_repairs.py`, `verify_rc003_round1_repairs.py` and `verify_rc003_round2_repairs.py` require `--repo-root`**; **`probe_conversion_pairs.py` requires `--assets-cache`, `--out`, and one of `--sessions` / `--sessions-file`**; Codex's probes all require `--repo-root`.
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state — and `git checkout -- <path>` is the clean way to undo a mangled edit script before retrying it properly.
