# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 35 · 2026-08-16 07:45 PDT**
**Next session is Claude Session 36. No count-based progress report is due** (they fall at 8, 16, 24, 32, **40**). A phase transition or an approved amendment would trigger one anyway.

## 0. WHAT THIS SESSION DID, IN ONE PARAGRAPH

**RC-004's Round-2 repair is delivered and the card is back on Codex.** He returned Round 1 as **`Revisions Required`** with two blocking findings, each carrying an executable counterexample. **F1:** `datetime.fromisoformat` accepts any character where ISO-8601 puts the `T`, so `2021-05-10Q14:33:49.023776-04:00` on both assets reached a drift verdict. **F2:** the raw asset's provenance and clock read sat outside the caller's `--max-mib` ceiling — 23,920 distinct raw bytes moved, and the clock was printed, under a one-byte ceiling. Both accepted in full, neither disputed. Suite **436 → 472 checks**, mutations **30 → 32**, all caught, control green. **The candidate is NOT approved and the rank-1 command stays blocked until it is.**

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

**Outcomes are `Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required`. `Escalated` was removed.** At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**. **Evidence determines what may ship; consensus determines what happens next. Underdetermined evidence is not resolved in favour of approval.**

**RC-001 `Approved`. RC-002 `Revisions Required` (first Convergence Decision, S30). RC-003 `Approved` at Round 3. RC-004 is OPEN at Round 2, on Codex.** **⚠️ Round 2 is the second of the three round-trips. If Round 3 does not close with both approvals, the Convergence Decision fires.**

**⚠️ RC-004 is NOT a successor and clause 5 does not apply to it.** It is the first card opened against *approved* code, on evidence that did not exist while that review ran.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six. **RC-004 needs no amendment**: §16.4 already makes an unestablished common clock a *pausing input error* and never named converter-version equality as its test. Both agents checked that independently.

**⚠️ This file describes the moment it was written.** Codex has now fourteen times posted a handoff within the hour after a session closed. **Read the active chats before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, and no candidate has been measured on any open gate.** The only real candidate read ever attempted was Session 33's rank-1 `--plan-only`, which stopped as an input error before any unit was read.

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 24, `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`. §1–§16 SAME-STATE APPROVED. RC-001 is closed. Do not reopen it.** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **`eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` — approved, closed.** |
| `agents/Claude/tools/test_band_drift.py` | **`946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` — approved, closed.** 103 checks. |
| **`Reproducibility Packet/scripts/utils/archive_units.py`** | **`9ef16f58cbd46ece7753406790a1b3d578efaf03df6311024c62e4c0e7b7e6e0` — RC-004 ROUND-2 CANDIDATE, unapproved.** ⚠️ `4192f345…` was published in the chat first and then corrected; the addendum on the card explains it. Round 1 was `261d93cc…`; RC-003's approved state was `96a31b3d…`. |
| **`Reproducibility Packet/scripts/measure_host_drift.py`** | **`156f6f0ffb0d13b7b3c871c29e7f516d93da65cadd4cbc742d7113fe132cf450` — RC-004 ROUND-2 CANDIDATE, unapproved.** Round 1 was `c54216f2…`; RC-003's was `0bf08153…`. |
| **`agents/Claude/tools/test_measure_host_drift.py`** | **`c508233d9c2d5c5567ca6875e8ebd22b1823b3ab7dff2aeac52044847305349a`** — 82 cases, **472 checks, 0 failed, ~16 s.** |
| **`agents/Claude/tools/mutate_rc002_repairs.py`** | **`97860ad978bf6bd2fd6851033405c7b9e1cf51aacb0c44332344fd64d92bcf49`** — **32 of 32 caught**, control green at 472, **~9 minutes**. |
| `agents/Claude/tools/verify_rc003_round2_repairs.py` | `f4ee4ae651a03471c3d8abbd7a3a0e131f2d381219dd6691e113f349a018bf77` — unchanged since Round 1. **Exits 1 on exactly two checks by design** (§3.5). |
| `agents/Claude/tools/verify_rc003_round1_repairs.py` | `2b7d9ef6…` — unchanged, exits 0. |
| `agents/Claude/tools/probe_conversion_pairs.py` | `10ad5053a06ba35d32d17540a6511f459e2e6f72cd3fcbe613bbdc9af10873ec` — the 71-session census, authenticated by Codex at this digest. |
| `agents/Codex/tools/probe_rc004_round1.py` | `a48b5c5e500a268d79bab0515f415e34efa428f4459fc8b34cddd1119ded6305` — his Round-1 counterexamples. **Reproduced both before the repair; reproduces neither after.** |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `ea85ede2…` — 18 of 18. |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `848e6d03…` — unchanged; 10 steps agree, `measure_host_drift.py` still `PENDING`. |
| `Reproducibility Packet/README.md` | `ae01b1a2…` — unchanged. **No runbook step changed this session.** |

## 2. The first thing to do next session

**Check the active chats before assuming anything.**

- **`chats/Claude-Codex/Session Reference Time Pair Check Review/` — the live review. Round 2 is on Codex, delta-only.**
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active** by Randy's request.
- **All eight other chats are concluded.**

**If Codex has returned his delta pass:** respond as owner. Every finding gets accepted or disputed explicitly; a dispute is stated with its counterevidence, not deferred. **Round 3 is the last round the method allows**, and a non-approval there fires the Convergence Decision. **Re-run the mutation harness after every repair** — S31, S32 and S35 all proved a repair can silently remove the coverage a mutation depends on.

**If RC-004 closes `Approved`:** run rank 1 (§5.2). That is the first drift number this project will have.

**One question is open to Codex and needs an answer rather than a guess:** whether he wants RC-003-F3's before-the-first-fetch property back at the command level (§3.4). If he does, it costs a second processed-only fixture pair.

## 3. What RC-004 changed

### 3.1 The pair condition (Round 1)

`authenticate_provenance_pair(first, second)` compares `first["reference_instant"]` and `second["reference_instant"]` — timezone-aware `datetime`s parsed from each asset's root `timestamps_reference_time`. Returns `reference_instant_utc` · `reference_instants_agree` · `reference_delta_s` · `raw_version` · `processed_version` · **`versions_agree` (reported, gates nothing, `False` on every real session)** · `versions_are_measured`. **The old keys `version` and `version_is_measured` are gone from the pair dict.**

`authenticate_provenance` requires `timestamps_reference_time` present, complete, ISO-8601 and **timezone-aware**, and returns `reference_path` · `reference_value` · `reference_instant`. **The conversion statement is checked first.** Helpers: `reference_instant(value)` · `instant_text(instant)` · `provenance_record(authentication)` (the JSON-safe projection — **use this, not a hand-written key list**).

`PROVENANCE_PATHS` is **five**: `general/source_script`, `timestamps_reference_time`, `session_start_time`, `general/institution`, `general/lab`. **Transfer budget moved with the path count:** 327,680 → **393,216** at the pinned 64 KiB provenance block. `MEASURED_CONVERSION_VERSIONS = ("0.9.1", "0.9.2", "0.9.4")`, never gated.

### 3.2 The lexical grammar (Round 2, F1)

**`reference_instant` matches the whole stripped value against `REFERENCE_TIME_FORM` before it parses anything.** `fromisoformat` accepts **any single character** where ISO-8601 puts the `T` on the pinned interpreter, CPython 3.12.10 — measured, not read off a changelog — so `2021-05-10Q…-04:00` parsed, carried an offset, agreed with its twin and reached a verdict. The grammar is ISO-8601 **extended**: `T` separator, `hh:mm` with optional `:ss` and optional fraction, optional `Z` or `±hh[:mm]`. `REFERENCE_TIME_FORM_TEXT` is what the error message quotes.

- **The parser still validates the values inside the shape** — month 13, hour 25 and 31 February are refused by `fromisoformat`, not by the expression.
- **⚠️ THE OFFSET REQUIREMENT IS DELIBERATELY NOT IN THE GRAMMAR.** It stays on the parsed value's `utcoffset`. Two independent enforcers of one property mean **no single-line revert can defeat it**, and mutation **F1L** would go from CAUGHT to MISSED with nothing saying so. **Do not "tidy" this by moving the offset into the regex.**
- Deliberately a little wider than the measured population — omitted seconds, any fraction length, `Z`, whole-hour offsets — because those are legitimate ISO-8601 extended forms. **`+hhmm` is refused.** ISO-8601 requires the date and time halves of one representation to use the same format, basic or extended; applying that to the *offset* is a reading rather than a quoted clause, it is labelled as one in the code, and no measured asset spells its offset that way.
- A non-`str` value returns None rather than raising.

### 3.3 The ceiling on the raw clock read (Round 2, F2)

**`read_provenance(url, size, block_bytes, max_bytes=None)`** holds `_ceiling_budget` open around the file open **and** the provenance read, and `measure_host_drift.main` passes it the same `--max-mib`. A refusal becomes `[fatal] input error reading <raw path>: …`.

**It is a tightening and the code says so.** There is no plan behind that read, so `_ceiling_budget`'s "cannot make anything infeasible" argument — which is about `read_band_units` — does not carry. A declared ceiling below the cost of opening the raw asset now refuses a run that used to reach the processed read. At the 1024 MiB default it cannot fire; on the real rank-1 candidate that read spent 22,104 request bytes and 262,144 transfer bytes.

**The narratives were corrected in three places**: the module docstring, `--max-mib`'s help, and `read_provenance`'s docstring. `_ceiling_budget`'s docstring now separates the two callers.

### 3.4 The consequence declared to Codex

**`case_ceiling_refuses_before_the_bytes_move` now stops on the RAW asset**, because that is the read the ceiling meets first. Old assertions all hold; three added (names the raw asset, zero distinct raw bytes, the captured transcript lacks the clock line). **No whole-command ceiling can admit the raw asset's ten kilobytes and still refuse the processed asset's first eight bytes**, so RC-003-F3's processed-side property moved to a direct-API case, `case_the_processed_ceiling_still_refuses_before_its_first_fetch`. Mutation F3d is caught at both layers.

### 3.5 The three things declared at Round 1, still true

1. **`verify_rc003_round2_repairs.py` no longer passes**, by construction — its second construction asserts the removed rule. **No check was edited**; a dated supersession note was added to the docstring. It exits 1 with exactly `F1 disagreeing pair reaches no verdict` and `F1 disagreeing pair is an input error`.
2. **`general/session_start_time` left `PROVENANCE_PATHS`** — a preference, a follow-up on the card.
3. **The comparison resolves to one microsecond.** The measured disagreement is 3,600 s.

### 3.6 What is NOT in RC-004

- **The NYU-65 payload diagnostic.** Codex declined it and I withdrew the question.
- **Moving `probe_conversion_pairs.py` into the packet.** Tracked follow-up 1.
- **Any Claim Sheet amendment**, any archive read, any candidate run.

## 4. The estimator and the readers, as they stand

`band_drift.py` public surface (unchanged, approved): `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** The symbol is `Delta_10min`. Band keys are `delta_full` / `delta_window` / `window_start`; `apply_gate` returns **`passed`** (not `passes`).
- `measure_band_drift(spike_times, depths, extent_s, params=None)` returns `measurable`, `reason` when False, and when True **six** per-unit audit lists aligned with `included`: `unit_delta_full`, `unit_delta_max_window`, `unit_max_window_start`, `unit_max_window_defined_bins`, `unit_delta_band_window`, `unit_band_window_defined_bins`. **`delta_max_window` is the per-unit list's name; the band's is `delta_window`.**
- `permutation_null(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` — **does not take the observation.**
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)`, **anchors at 0**; spikes below zero fall outside every bin and are silently excluded — the reader counts and reports them.
- **A recording needs at least 11 analysed bins.** Candidates carry 54–87.

`archive_units.py` public surface: `ReadBudgetExceeded` (with `.scope`) · **`BoundedReader`** (`.block_bytes`, `.last_spend`, `budget(read_bytes, transfer_bytes=None, label=…)`) · `provenance_transfer_budget` · `ascii_safe` · `read_flat_electrodes` · `column_descriptions` · `source_provenance(handle, reader, max_bytes=PROVENANCE_MAX_BYTES)` · `provenance_is_complete` · `conversion_version` · **`reference_instant`** · **`instant_text`** · `authenticate_provenance(provenance, source)` · **`provenance_record(authentication)`** · **`authenticate_provenance_pair(first, second)`** · **`read_provenance(url, size, block_bytes, max_bytes=None)`** · `read_integer_column` · `read_unit_scalars` · `check_ragged_alignment` · `resolve_unit_electrodes` · `select_band_units` · `chunk_byte_ranges` · `column_layout` · `python_structure_bytes` · `band_slices` · `plan_transfer` · `read_band_units` · `electrode_tables_agree`. Private: `_stored_value_bytes`, `_capped`, `_decode`, `_blocks_covering`, `_slice_blocks`, `_slice_bounds`, `_own_refusal`, `_ceiling_budget`.

- **Constants:** `PROVENANCE_MAX_BYTES = 65536` (request budget, **cumulative over the whole `source_provenance` call**) · `PROVENANCE_BLOCK_BYTES = 65536` · `PROVENANCE_PATHS` (five) · `CONVERSION_SOURCE_FORM` / `…_TEXT` / `…_TOKEN` / `MEASURED_CONVERSION_VERSIONS` · `PROVENANCE_SCOPE` / `PREFLIGHT_SCOPE` · `REQUIRED_PROVENANCE_PATH` · `REFERENCE_TIME_PATH` · **`REFERENCE_TIME_FORM` / `REFERENCE_TIME_FORM_TEXT`**.
- **`read_band_units(..., max_bytes=None, plan_only=False, expect_conversion=None)`** returns `provenance_pair` and `provenance_io` alongside `provenance_authentication`.
- **`read_provenance` returns `provenance`, `provenance_io`, `io`.**
- **A refused read spends neither budget**, so an oversized value does not stop later paths being read; **the two required paths are read first.**
- **`column_layout(dataset, slices=None)`** — pass the slices or a chunked column falls back to `whole file`.
- **`plan_transfer(..., spent_bytes=0, held=())`** — `held` is charged into `structures_bytes`; `read_band_units` passes four objects.
- **Plan keys:** `logical_bytes` · `cache_bound_bytes` · `resident_bytes` · `structures_bytes` · `library_cache_bytes` · `peak_resident_bytes` · `bound_basis` · `block_bytes` · `spent_bytes` · `per_unit` · the two layouts. **There is no key called `bytes`.**

`measure_host_drift.py`: `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`.**
- **`io` has FOUR sources:** `raw_provenance` · `raw_electrodes` · `raw_timing` · `processed_units`. **Since Session 35 the declared ceiling covers `raw_provenance` and `processed_units`; only `raw_electrodes` and `raw_timing` are bounded by construction alone.**
- **`record["provenance_io"]` carries `raw` and `processed`,** each with `read_budget_bytes` / `read_bytes` / `transfer_budget_bytes` / `transfer_bytes` / `block_bytes` / `label`.
- **`record["checks"]` carries `reference_time`**, printed as `session reference time`.

### 4.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires on every case that reaches a record that `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`, and raises if it matched no reader at all. **Do not weaken this into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size** (S31). `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4` for exactly that reason. **Do not change it back.**
3. **The provenance-budget invariant** (S32). On every case that reaches a record and on **both** assets, `read_bytes <= read_budget_bytes` and `transfer_bytes <= transfer_budget_bytes`. **It only has teeth on a block-caching reader**, which is why `case_command_reports_a_block_readers_expansion` runs the whole command with `archive_units.RemoteFile = BlockLocalFile`. **⚠️ It says nothing about reads that never reach a record** — that is exactly the gap Codex's RC-004-F2 walked through, and the answer was the ceiling rather than a wider invariant.
4. **The fixture axes are separate on purpose** (S34). `write_raw` / `write_processed` take `provenance=` **and** `reference_time=` independently, both defaulting to a valid value.
5. **`run_case(..., capture=False)`** (S35). With `capture=True` stdout is collected and `result["stdout"]` is the transcript; otherwise it is **None**, not `""`, so a case cannot assert a phrase is absent from a transcript it never collected.

## 5. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 5.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs are in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`.**

**Do not re-derive the order and do not re-sort it.** Ranks 4–5 outrank rank 3 on channel count deliberately. NYU-39 at rank 9 is deliberate — deprioritized, never disqualified, **and the label-blind unit set is what keeps it that way.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first; cannot change a verdict, only cost): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

**⚠️ Four ranks — 5, 7, 9, 13 (NYU-65, NYU-45, NYU-39, NYU-48) — are PAUSED on the declared-clock disagreement, not rejected.** They keep their rank. **Ranks 1, 2, 3, 4, 6, 8, 10, 11, 12 pass the pair condition. Rank 1 passes.** Recovering the four needs its own evidence and its own recorded gate, and only if the order gets that far.

### 5.2 Rank 1's measurement, once RC-004 closes approved

**CSHL047 Probe01, session `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`.** Everything up to the processed read is *confirmed working against the real asset* (Session 33), not predicted: raw provenance authenticated (`Created using NeuroConv v0.9.2`, **22,104 request bytes of 65,536 and 262,144 transfer bytes** — the transfer budget is now **393,216**, so that measured spend has more headroom, not less), CA1 band **320.0–1020.0 µm, 72 channels**, AP extent **`t_first 1.138489 s`, `t_last 4340.732689 s`** matching `host_timing_index.jsonl` exactly.

**Run `--plan-only` first, then measure free RAM against `peak_resident_bytes` — not against `resident_bytes`, which is one term of it — and free bandwidth-tolerance against `cache_bound_bytes`, then read.** Its `t_first_s` is 1.138489 s, so bin 0 carries 58.86 s of coverage out of 72 bins and `head_partial_s` is non-zero.

Command shape, **from inside the packet folder**:

`python scripts/measure_host_drift.py --session <uuid> --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

**When it has actually been executed it becomes runbook step 11**: add the README step, **remove its entry from the checker's `PENDING_STEP`** (the checker errors if a script is both a step and pending — there is a mutation proving that), and re-run `check_runbook_consistency.py`.

**Three things still to watch on the first payload read.**
1. Resolving the chunk map costs one `get_chunk_info_by_coord` per touched chunk — thousands of lookups on a real asset, and `--plan-only` is where the cost shows up.
2. The provenance read is part of preflight, so `spent_bytes` includes it.
3. **The declared ceiling refuses a fetch during preflight**, not only at the plan — **and since Session 35 it also refuses during the raw provenance read.** At the `--max-mib 1024` default neither will fire.

### 5.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Do not reopen §1–§16** — it belongs in a future section. **Codex still owns the footprint/placement calibration**; do not start it.

## 6. What is still not done

1. **No host is pinned**, and that is correct.
2. **No candidate has been measured.** The command is blocked until RC-004 closes approved.
3. **The capacity gate needs re-establishing** under Amendment 6's stricter condition (§5.3).
4. **Five of the ten packet steps still have not been re-run** (the archive-reading ones). The README says so.
5. **The preprocessing half of the amplitude question is untouched** and not metadata-answerable — Rung 0 territory.
6. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question, not a coding one.
7. **`is_injectable` is a denylist over a partly derived vocabulary.** Latent: no consumer reads it.
8. **`probe_conversion_pairs.py` is not in the packet.** RC-004 tracked follow-up 1.

## 7. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** · **the real-arm donor-matching rule** · **the exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 8. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`, `G0` the mean paired sorter gap *in the control arm*** — not the negative-control band. `[−T, T]` is declared shorthand for the `D` rule, never a second test. `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins, not ten.** Widening is monotone and can only reject more. Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those are input errors that pause the pinned order (§16.4), and the reader enforces that separation in its exit status. **That separation is why four candidates are paused rather than lost.**
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** `0.000`/`15.000`/`30.000 µm` describes the **equal-baseline fixture** only. A median tracks rank, so displacing `k` of a bin's `n` spikes upward moves its median **at most the displacement itself and at most the distance to the depth `k` ranks above it** (0 violations, 4,000 random cases; Codex's exhaustive check: 93,184 cases). On a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`. **The gate has no guaranteed resolution below the bin width in either direction. The old "permissive" claim is WITHDRAWN and must not be re-derived on the new bound.**
- **The drift unit set is blind to `kilosort2_label`** and is selected by valid same-probe `max_electrode -> rel_y` inside the band. **That choice carries no one-way safety guarantee.**
- **The per-unit excursions are reported and never consumed**, they carry no null, and they do not discharge that conditional in either direction. **Never compare a per-unit value to `Q95_null` or to `L`.** **And the absence of magnitude separation is not evidence either.**
- **The bin grid anchors at session `t = 0` with extent `t_last_s`**, on pinned converter provenance. **`duration_s` is a span and is not an alternative clock hypothesis.** Endpoint containment is a consistency check that cannot identify a clock — **and neither can reference-instant agreement; it is a necessary declared condition and the report says so.**
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
- **⚠️ The daylight-saving reading of the 8 disagreeing sessions is DESCRIBED, NOT EXPLAINED.** One lab, one season, exactly one hour, one direction. No mechanism was measured and none may be claimed in any artifact.
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count that reported one of its three reads; S27's five; S28's three plus the Round-2 ASCII claim that was wider than its check; S29's one, which closed RC-002 unapproved; S30's three, which returned RC-003 Round 1; S31's two, which returned RC-003 Round 2; S32's own, the pair-equality condition on converter version that admitted 0 of 71; **and S34's two, which returned RC-004 Round 1: a value that is not an ISO-8601 timestamp reaching a verdict because the parser is broader than the standard, and the raw clock read sitting outside the ceiling the caller declared.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*. **S33 is the sharpest instance: a rule reviewed across three rounds by two agents, defended by 26 mutations and 382 checks, admits nothing in the only dataset it will ever see.**
2. **Read the column, do not count it** (S5). **S33 inverts it — the thing needed had never been read at all.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30–S32). **S33: a check whose admitted population is empty is not conservative, it is broken. S34–S35: when you replace such a check, build the case that catches the *mirror* failure in the same session** — and when you later *tighten* the replacement, measure the tightening against the real population too, because a tightening is the change that can empty one again.
4. **A clean trend invites a causal story you have no way to check** (S5 addendum, S33). Describe the pattern; do not publish the mechanism.
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **Reviewer's version: review it against the contract, not against your own last draft** (S16).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and* backslash escapes — write the script with the Write tool and run it** (confirmed again at S35). **`$VAR` does not expand inside the Bash tool's `-c` string.** **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.** **A heredoc that `print`s a non-ASCII character dies on cp1252** (S30). **Write the message to a scratch file with a `__STAMP__` placeholder, let one script substitute the clock reading, assert the header appears exactly once after the pre-write line count, and assert no CR appeared in an LF transcript** (S34, S35).
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32).
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32).
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7). **S22–S35: run the probe they hand you, unmodified, before editing — and again after.**
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S33). **When a check stands in for a property, ask what it admits and rejects on the real population.**
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32, S33).
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
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S35). **Sixteen consecutive sessions where the read-back pass produced a correction or a confirmation worth having.**
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26, S34). So assert it.
31. **A supersession can be too broad as well as too narrow** (S14).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28).
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32, S34, S35). Validate every replacement across every file *before* writing any of them, and re-assert afterwards.
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Eighteen for eighteen (S15–S35).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32). **S33: made against the real population, not the fixtures. S35's other half: when the argument genuinely does not hold, say the tightening is a tightening and name the class it refuses — do not stretch an argument written for one caller to cover a second.**
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.**
41. **Read the clock at the moment you write the timestamp** (S17). **`time.strftime("%Z")` returns the long timezone name on Windows: use a literal `PDT`.** S30–S35 used the placeholder route for every timestamped write.
42. **A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24, S34). **S35's instance: `agents/Claude/README.md` said the ceiling does not cover the raw-asset reads, which my own repair made false. Grep your changed files for every sentence containing the thing you changed, not just the diff.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30, S34, S35).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32, S34). **And which *currency* it is denominated in.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26).
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28). **S34's inverse: `mutate_rc002_repairs.py` now covers RC-002, RC-003 and RC-004, and the name was *not* changed — three artifacts cite it by path.**
50. **A counterexample built on a degenerate case invites dismissal** (S24). **S26 is the mirror: check whether it is *stronger* than claimed.**
51. **A near-miss is not the finding** (S24). Sweep the parameters to establish the regime exists.
52. **A test can encode the defect it was written to catch** (S25, S28). **A harness written from the implementation confirms the implementation.**
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25).
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32, S35).
56. **Which fixture a published number came from is part of the number** (S25, S26).
57. **A check that cannot fail is not a check** (S27–S32). **S33's fourth form: a check that cannot *pass* is not a check either, and it is much harder to notice.** **S35's corollary: give a "was it absent?" assertion a `None` sentinel rather than an empty string, or a case can assert a phrase is missing from a transcript it never collected.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen between them.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). **RC-003 then closed `Approved` without needing a second one.**
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair.**
62. **Evidence must come from the exact state you publish digests for** (S31, S34, S35). Compute digests from the files at write time. **S35: two comment-only fixes made after the harness had run were enough to re-run the whole harness rather than publish digests it never saw.**
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32, S34).
64. **When a reviewer's finding is correct, check whether it is *complete* before repairing it** (S32).
65. **An undetermined value is a missing measurement, not a negative one** (S33, S34).
66. **Test a hypothesis on data that did not suggest it** (S33).
67. **Do not both discover an input error and rule on its disposition in the same session** (S33). **S34: when the reviewer rules, accept the ruling and say which part of his reason you had underweighted.**
68. **Separate the fixture's axes before you need them separate** (S34).
69. **A closed card's evidence script may legitimately go red** (S34). Do not edit its checks to make it green. Add a dated supersession note, run it, and report the actual failure count.
70. **A note added to a docstring is printed surface** (S34). `--help` renders it, this console is cp1252, and a decorative character there is a crash on a machine detail.
71. **⚠️ BEFORE ADDING A SECOND ENFORCER OF A PROPERTY, ASK WHAT THE MUTATION FOR THAT PROPERTY REVERTS** (S35). Requiring the UTC offset in the new grammar *as well as* on the parsed value would have been ordinary defensive coding and would have turned F1L from CAUGHT into MISSED, silently — two independent enforcers mean no single-line revert can defeat the property. **Redundancy in the code and sensitivity in the harness pull against each other, and the harness is the only thing that says the code still depends on what it claims to.** One enforcer per property, and say in the docstring why.
72. **A whole-command test can have its meaning moved by a change elsewhere while staying green** (S35). Bringing the raw read inside the ceiling changed which asset a one-byte ceiling refuses first; the case would have passed for a reason it was not written to check. **When the arithmetic makes the old meaning unreachable at that layer, move the property down to the layer where it *is* a property rather than leave a green case standing for nothing** — and write the reason into both cases.
73. **The trusted parser is part of the input surface** (S35). `fromisoformat` is deliberately broader than ISO-8601, and "the standard library parsed it" is not "the value is well-formed". When a field's format is specified by an external standard, gate the lexical form yourself and let the parser validate the values inside it.

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Session 35 readings: 07:06 PDT — 13,404 MB available physical of 32,425; 30,683 MB committed of a 130,415 MB limit. 07:25 PDT with the harness running — 12,835 MB free, 32,931 MB committed.** Nothing this session was heavy and **nothing read the archive or the network**: the largest thing that ran was the mutation harness, thirty-two sequential copies of a small synthetic tree, run twice. **Read all three numbers, not one:** `FreePhysicalMemory` excludes reclaimable standby, and committed bytes against the commit limit decides whether a new process can start. **Do not inherit these; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64`; a numpy change is a replay risk.** **h5py's chunk-index and property-list APIs are load-bearing.** **`datetime.fromisoformat` is load-bearing and is now fenced by `REFERENCE_TIME_FORM`** — on CPython 3.12.10 it accepts `Z` and arbitrary fractional digits, truncates below a microsecond, and **accepts any character where ISO-8601 puts the `T`**, which is the defect RC-004-F1 repaired. Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

**Network:** the archive is reachable and `RemoteFile` works against it. A session pair costs about **1 MB and ~16 requests** for metadata at a 64 KiB block, and about **8 seconds**.

## 11. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **RC-001/002/003 are closed; RC-004 is open at Round 2 and its index row says so.**
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section.**
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry landed inside the log section. **66 dated entries by `grep -c "^- \*\*2026-08-1"`; banner at 2026-08-16.** **Session 35 deliberately added none**: the heartbeat check ran, no artifact finished, no phase closed, and four consecutive sessions already have entries — the log is lean by design and a Round-2 repair is expected follow-through, not a noteworthy event.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link.
- **Corrections propagate forward, never backward.** The review cycle is the only exception.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. `ls "C:/Users/cresp/AppData/Local/Temp" | grep -c "drift_reader\|rc002_mutation\|rc003_round\|rc004_round\|rbchk"` is the check. **The mutation harness now takes ~9 minutes for 32 mutations — run it with `run_in_background`. Its stdout is buffered when redirected, so an empty output file means "still running"; `ls "…/Temp"/rc002_mutation_*` shows which mutation it is on. ⚠️ Do not edit any file the harness copies while it is running** — it copies `Reproducibility Packet/scripts/` and `test_measure_host_drift.py` and nothing else, so everything else is safe to edit meanwhile.
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **total every read rather than the last one.** **A retry re-transfers a block, so `n_bytes` can exceed the file size.** **The reader's cache is unbounded and never evicted, which is why it is a memory term.**
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`.
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` needs no step. **A script in `scripts/` without a step is a hard failure unless it is declared in `PENDING_STEP`** — and a script that is both a step and pending is also a failure, and both rules have mutations. **After editing the packet runbook or any script docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **`mutation_test_runbook_checker.py` takes three positional arguments**, not flags: packet path, scratch directory, interpreter. It leaves its scratch directory behind — delete it.
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. **Check the printed surface by capturing `--help`, not only by scanning source.** **Values read out of an asset are not yours** — render them through `archive_units.ascii_safe` before printing.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (176/176 as of Session 35); the root `README.md`, the selection document, the Review Cards and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert CR == LF afterwards.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path (`C:/Users/cresp/AppData/Local/Temp/ct`), comparing file by file, and **deleting the clone afterwards.**
- **Both `.gitignore` files carry a do-not-catch-these comment and ignore `__pycache__/`.**
- **`agents/Claude/tools/` holds ten scripts and seven recorded outputs.** The recorded ones are cited by other artifacts: `source_count_granularity_probe_2026-08-13.txt` by the matching rule, and the four `conversion_pairs_*_2026-08-16` files plus their two session lists by RC-004. **The two census JSON files are also where `MEASURED_REFERENCE_TIMES` in the acceptance suite came from** — the suite carries a frozen copy so it stays self-contained, and Session 35 verified the copy equals the set those files yield.
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations`; `probe_band_drift_claims.py` takes `--module`; `test_measure_host_drift.py` takes `--keep` and `--tmp-root`; **`mutate_rc002_repairs.py`, `verify_rc003_round1_repairs.py` and `verify_rc003_round2_repairs.py` require `--repo-root`**; **`probe_conversion_pairs.py` requires `--assets-cache`, `--out`, and one of `--sessions` / `--sessions-file`**; Codex's probes all require `--repo-root`.
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state — and `git checkout -- <path>` is the clean way to undo a mangled edit script before retrying it properly.
