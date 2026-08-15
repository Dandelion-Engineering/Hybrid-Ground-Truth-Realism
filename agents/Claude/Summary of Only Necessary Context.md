# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 29 · 2026-08-15 07:50 PDT**
**Next session is Claude Session 30. No count-based progress report is due** (the next is Session 32). A phase transition or an approved amendment written in your session would trigger one anyway.

## 0. ⚠️ THE REVIEW METHOD — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

***Convergence in place of escalation* is agreed, written into the playbook, and binding.** `Escalated` is no longer an outcome; the outcomes are **Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required**. At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**: each writes, once, the minimum claim it thinks can ship, the evidence that controls, the strongest evidence against its own position, and one acceptable safe disposition. **Evidence determines what may ship; consensus determines what happens next. Underdetermined evidence is not resolved in favour of approval.** The card closes at a disposition, the owner repairs **outside** review, and may open **one** successor card with a `Supersedes:` line; **a second like-for-like successor is not allowed**. Three readings are in the playbook's operating notes and Codex has agreed to all three: approval stays explicit and state-specific; an unchanged sentence made false by a change elsewhere **is** a regression introduced by the response and so is in scope after Round 1; and a LATE-BLOCKER created by an earlier repair says so.

**RC-001 closed `Approved` at its third round. RC-002 has now had its Round 3 owner response, so Codex's next pass is TERMINAL** — an approval closes the card, anything short of one goes to the Convergence Decision, and there is no fourth round. Feedback on the method stays an open obligation in `chats/Claude-Codex-Human/Review Method Change/` — Randy asked for it and asked that the chat stay active.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six.

**⚠️ This file describes the moment it was written.** Codex has now eight times posted a handoff within the hour after a session closed. **Read the active chats before you act on §2.**

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
| `Reproducibility Packet/scripts/utils/archive_units.py` | **`2ee891ce7e167edca37f735c6483ba965b7008e4935611e8d38c0177d961fb4a` — open on Codex, RC-002 Round 3.** |
| `Reproducibility Packet/scripts/measure_host_drift.py` | **`dfbb9cc8620ce85c56350ee2c84b178c0081398aee44513a122db8faeb6607ed` — open, RC-002 Round 3.** |
| `agents/Claude/tools/test_measure_host_drift.py` | **`5101d000b3cd803ef53be4930056d0f8608dd9b0736b220519b727e9f2d477b7` — open, RC-002 Round 3. 266 checks, 0 failed, 13.8 s.** |
| `agents/Claude/tools/mutate_rc002_repairs.py` | **`1e1ed5a9bbda991dc5d2239de05c5cd40510e2a3dcea8fa7713955618d0eceba` — open, RC-002 Round 3. 13 of 13, control green.** |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | **NEW to the candidate in Session 29. `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc` — open, RC-002 Round 3. 18 of 18, control green.** |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | **`848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f` — unchanged since Session 28; open, RC-002 Round 3.** |
| `Reproducibility Packet/README.md` | **`ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5` — unchanged since Session 28; open, RC-002 Round 3.** |
| `agents/Codex/tools/probe_rc002_round2.py` | `ea806c590ed5f92764175c3ef798aa15bcea0613386a68c752c58c2ddc070781`. **His; do not edit it.** After the Session 29 repairs it **raises** — the read it must admit is refused. That is the repair, not a regression. |
| `agents/Codex/tools/probe_rc002_round1.py` | `e4197bcaabb523929b34bc340b4d0419e0fc154c51618f08fd56d92beecbd27a`. His. Four constructions FAIL and the fifth raises — the Session 28 repair. |
| `agents/Codex/tools/probe_rc001_round1.py` / `probe_draft16_safety_claims.py` | Both take `--repo-root`; `probe_rc001_round1.py` requires it. 0 failures / digits unchanged at Session 29. |

## 2. The first thing to do next session

**Check the active chats before assuming anything. As of writing, everything open is open on Codex and nothing is open on you.**

- `chats/Claude-Codex/Archive-Reading Drift Command Review/` — **RC-002 Round 3 verification is open on Codex, is delta-only, and is TERMINAL.**
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active.** One method observation from Session 29 is queued for it (§9 note 58).
- All four Tier A / packet chats are **concluded**.

**If RC-002 closes `Approved`, the next work is the first real candidate measurement** (§5.2). **Until it closes, do not read a candidate and do not measure one.**

**If Codex does not approve, do not write a fourth round.** Freeze the disputed state and run the **Convergence Decision**: one statement each, written into the Review Card, ending at one of the four dispositions. It is agent-only — nothing goes to Randy.

## 3. What Session 29 did: the RC-002 Round 3 repairs

**Codex's Round 2 was `Revisions Required` with three blockers and two non-blocking items. I accepted all five in full, disputed none, and reproduced all four of his constructions before editing anything.** Do not re-litigate any of them.

- **F1-R1a — the chunk bound assumed contiguity.** `_slice_block_bytes` rounded the element range out to whole chunks and placed it as one span; HDF5 does not promise successive chunks are adjacent, and a fragmented fixture bounded at `241,664` transferred `327,680`. **Now `chunk_byte_ranges` reads every touched chunk's `(byte_offset, size)` from the chunk index (`get_chunk_info_by_coord`) and the plan unions the blocks covering those real ranges.** Three placement routes, named by `bound_basis`: `dataset offsets`, `chunk offsets`, `whole file`. **The chunk index is read before `spent_bytes` is captured**, so its requests are counted. Bound is now `573,440` against `327,680`.
- **F1-R1b — the memory figures were enforced separately and are live together.** **`max_bytes` is now enforced against one `peak_resident_bytes` and nothing else** = `cache_bound_bytes` + `resident_bytes` + `structures_bytes` + `library_cache_bytes`. It contains the transfer bound, so it is strictly stronger than the old pair. **`library_cache_bytes` is mine, not Codex's ask:** my first draft declared HDF5's chunk cache out of scope, which is the same move as the defect, and the number is readable from `get_access_plist().get_chunk_cache()[1]`. Named exclusions now: interpreter baseline, allocator overhead, transient h5py allocations outside a chunk cache.
- **F2-R1 — integer storage required for the two ragged indices only.** `read_integer_column(..., require_integer_dtype=True)` for `spike_times_index` and `spike_depths_index` (HDMF `VectorIndex`, schema-typed); **unchanged for `max_electrode`**, where a whole-valued float is still accepted and reported. **Consequence: the Round-1 fractional-offsets fixture now stops on dtype, not fractionality** — the case's assertion and docstring say so, and integrality alone is still exercised on `max_electrode`.
- **F6-R1 — `same_output_path`**: `os.path.samefile` when both exist, else `normcase(realpath(...))`. Its case asserts what the filesystem under the fixture actually does, so it does not merge two real files on a case-sensitive one.
- **E1 — both halves.** Harness at 13 mutations, all caught. **It still has no F5 entry and cannot have one**: F5's repair was a file move plus a checker declaration, and a text-mutation harness reverts neither. **The `sys.path` line is not the candidate it looks like — CPython adds a directly executed script's own directory anyway, so the mutation was missed.** Coverage closed instead: a subprocess `--help` case with `PYTHONPATH` cleared, and **three new `PENDING_STEP` mutations in `mutation_test_runbook_checker.py` (15 → 18)** — because my first draft of the narrowing claimed that harness already covered it, and it did not.

**Self-caught evidence correction, already in the card and the chat:** Round 2's "zero non-ASCII in all five changed Python files" was wider than its check. `check_runbook_consistency.py` has held one en dash since Session 13 inside the step-heading regex. Never printed; `--help` on all four scripts is ASCII, verified this time by **capturing the output** rather than scanning source.

## 4. The estimator and the readers, as they stand

`band_drift.py` public surface (unchanged, approved): `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** The symbol is `Delta_10min`. Band keys are `delta_full` / `delta_window` / `window_start`; `apply_gate` returns **`passed`** (not `passes`).
- `measure_band_drift(spike_times, depths, extent_s, params=None)` returns `measurable`, `reason` when False, and when True **six** per-unit audit lists aligned with `included`: `unit_delta_full`, `unit_delta_max_window`, `unit_max_window_start`, `unit_max_window_defined_bins`, `unit_delta_band_window`, `unit_band_window_defined_bins`. **`delta_max_window` is the per-unit list's name; the band's is `delta_window`.**
- `permutation_null(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` — **does not take the observation.**
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)`, **anchors at 0**; spikes below zero fall outside every bin and are silently excluded — the reader counts and reports them.
- **A recording needs at least 11 analysed bins.** Candidates carry 54–87.

`archive_units.py` public surface: `read_flat_electrodes` · `column_descriptions` · `source_provenance` · `read_integer_column` · `read_unit_scalars` · `check_ragged_alignment` · `resolve_unit_electrodes` · `select_band_units` · **`chunk_byte_ranges`** · `column_layout` · **`python_structure_bytes`** · **`band_slices`** · `plan_transfer` · `read_band_units` · `electrode_tables_agree`.
- **`column_layout(dataset, slices=None)`** — pass the slices or the chunk map is not resolved and a chunked column falls back to `whole file`.
- **`plan_transfer(band_units, scalars, time_layout, depth_layout, block_bytes, file_size, spent_bytes=0, held=())`** — `held` is charged into `structures_bytes`; `read_band_units` passes `(electrodes, unit_electrodes, descriptions)`.
- **Plan keys:** `logical_bytes` · `cache_bound_bytes` · `resident_bytes` · `structures_bytes` · `library_cache_bytes` · `peak_resident_bytes` · `bound_basis` · `block_bytes` · `spent_bytes` · `per_unit` · the two layouts. **There is no key called `bytes`.**

`measure_host_drift.py`: `GATES` · `BAND_MAX_GAP_UM` · `resolve_assets` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · **`same_output_path`** · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`.**

## 5. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 5.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Do not re-derive it and do not re-sort it.** Ranks 4–5 outrank rank 3 on channel count deliberately. NYU-39 at rank 9 is deliberate — deprioritized, never disqualified, **and the label-blind unit set is what keeps it that way.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first; cannot change a verdict, only cost): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

### 5.2 The next piece of work, once RC-002 closes

**Measure rank 1 — CSHL047 Probe01, session `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`.**

**Run `--plan-only` first, then measure free RAM against `peak_resident_bytes` — not against `resident_bytes`, which is one term of it — and free bandwidth-tolerance against `cache_bound_bytes`, then read.** The raw file's `t_first_s` for this series is **1.138 s**, so its bin 0 carries 58.86 s of coverage out of 72 bins and `head_partial_s` will be non-zero.

Command shape, **from inside the packet folder**:

`python scripts/measure_host_drift.py --session <uuid> --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

**When it has actually been executed it becomes runbook step 11**: add the README step, **remove its entry from the checker's `PENDING_STEP`** (the checker errors if a script is both a step and pending — and since Session 29 there is a mutation proving that), and re-run `check_runbook_consistency.py`.

**One thing to watch on the first real read.** Resolving the chunk map costs one `get_chunk_info_by_coord` per touched chunk. On a real processed asset that is thousands of lookups, and `--plan-only` is where the cost shows up. If it is slow, that is a measurement to report, not a reason to revert to the loose bound.

### 5.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Do not reopen §1–§16** — it belongs in a future section. **Codex still owns the footprint/placement calibration**; do not start it.

## 6. What is still not done

1. **No host is pinned**, and that is correct.
2. **No candidate has been measured.** The reader exists but is unapproved.
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
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count that reported one of its three reads; S27's five (a ceiling on the stored payload described as bounding the transfer, structural columns coerced before validation, a raw/processed pair authenticated by session UUID alone, an AP clock accepted without covering its data, a band-contiguity tolerance left typeable); **and S28's three: a chunk bound that assumed contiguous chunks, two memory figures enforced separately when they are live together, and a whole-valued float ragged index accepted against its own schema — plus the Round-2 ASCII claim that was wider than its check.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5). **S16–S22: six sessions where the thing needed was already on disk. S23: already *computed*. S24: already *stated*. S29: already *readable* — the HDF5 chunk-cache ceiling was one property-list call away from a number I was about to declare unknowable.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5). **S17: for a host gate, pessimistic *is* the safe direction. S19: when a *proof* is withdrawn, ask what the unsafe direction now costs. S28: when the safe bound is loose, ask what a wrong refusal costs — here it is recoverable by a deliberate raise, which is why the loose-but-valid bound wins. S29 keeps that as the third branch and makes the first two exact, which is the better answer where the file will answer.**
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **Reviewer's version: review it against the contract, not against your own last draft** (S16).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and backslash escapes*** — write the script with the Write tool and run it. **S29 hit this again**: a heredoc holding a long markdown block died with a bash parse error; the Write-tool route worked first time. **`$VAR` does not expand inside the Bash tool's `-c` string passed to python**; pass the path as `argv`. **`.\venv\Scripts\python.exe` does not survive the Bash tool either — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7). **S26: a repair can create a *new false claim* by describing a real measurement in words wider than the measurement. S29 is the sharpest case: while correcting a false coverage claim I wrote a replacement coverage claim that was also false, and only checking it before writing it down caught it.**
8. **A measurement you just made is not a threshold you get to set** (S7, S17). **S27 made it mechanical: if the threshold cannot be typed, it cannot be chosen after the values are in. S28 generalizes it: anything that changes *which data is graded* is the same kind of number.**
9. **Read a rich first-party table, not one column of it** (S7). Read the column's own `description` too — **and S27: make the code read it.**
10. **Verify a name before trusting it** (S7). **S22–S23: run the probe they hand you. S24: re-run the *proof*. S26: rebuild the *counterexample*. S28–S29: run the whole probe against the unchanged candidate before editing — seven of seven, then four of four.**
11. **Two numbers in the same unit are not the same quantity** (S8); **two numbers that are the same quantity under different sampling models are also not the same number** (S11). **S28: one name for three quantities is how a ceiling ends up enforced on the smallest. S29 is the inverse and it is the harder direction: three quantities that are the same resource at the same moment must be ONE number, or a ceiling each of them clears is exceeded by their sum.**
12. **When a safety check fires, measure it before loosening it** (S8). **S19 inverse: when a cost is cited for *not* doing something, measure the cost.**
13. **A correction is worth logging even when the conclusion survives** (S8). **S29: including a correction to your own published evidence table when the defect it overstated is harmless.**
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9); a *better* reason arriving is also that moment (S15).
16. **An audit must use the same key its lookup uses** (S9). **S27: when an index in file A is used against a table in file B, check that A's and B's tables are the same table. S28: and that the two files are the same recording.**
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10). Thirteen for thirteen.
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17). **S23: when it does not survive, the counterexample becomes a permanent case. S28: when the reviewer's counterexample is repaired, keep it as a case from the *other* side. S29: and rebuild the superseded rule inside the case, so "the old figure would not have covered it" is recomputed on the fixture rather than quoted from a review message.**
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11, S27). **S28: when that collides with "the artifact must live in the packet", the answer is a third mechanism that is *checked*. S29: and "checked" has to mean a mutation exists — the `PENDING_STEP` mechanism was called checked for a whole round before anything tested it.**
24. **Note which direction a correction pushes** (S11), including when it makes your own next step harder (S15, S16). **S26: prove a no-numerical-branch claim with an AST comparison with docstrings stripped.**
25. **When a test fails, first ask whether the test or the artifact is broken** (S11). **`apply_gate` returns `passed`. `measure_band_drift` returns `delta_window`. Read the parser.**
26. **Render the output; do not read the source and assume you know what it prints** (S12). **Read the finished section back as a reviewer** (S16, S18–S29). **Ten consecutive sessions where the read-back pass produced the last correction — S29's was a ragged wrapped line and, more importantly, the realization that the memory scope I had just *declared* was one API call from being *closed*.**
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27). **S28 turned it on the tests themselves. S29 turned it on the harness's own claim: a mutation that gets MISSED is information, not a nuisance — the missed F5 mutation is what proved the repair was a file move rather than an edit.**
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16). **S26: and the *fixture* behind it is least likely to be interrogated at all.**
31. **A supersession can be too broad as well as too narrow** (S14).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17). **S28: §16.8 already required "the exact raw and processed assets".**
33. **Make an edit script assert exactly one match per replacement** (S14). Validate every replacement across every file *before* writing any of them. **S29: and read the anchor out of the file rather than from your own memory of it — two anchors differed from what I typed by one word.**
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Twelve for twelve (S15–S29).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17). **S26: edit every restatement in the same pass.**
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.**
41. **Read the clock at the moment you write the timestamp** (S17). **S28 got it wrong twice; the fix is mechanical — write the message with a placeholder and substitute the clock reading in the same command that appends it. S29 did exactly that and got the *format* wrong instead: `time.strftime("%Z")` returns the long timezone name on Windows, not the abbreviation. Use a literal `PDT`, or `%Y-%m-%d %H:%M` plus the abbreviation.**
42. **A status sentence doing a rule's job goes stale in the permissive direction** (S18). **S24: a diagnostic with no stated null result is read as reassurance.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20).
46. **State a check's *resolution*, not only its role** (S21) — **and only when the check actually has one** (S22). **S26: state what it is a resolution *of*. S28: when a bound cannot be exact, say it is a bound, say what it excludes, and report the facts that explain its looseness. S29: and before writing "out of scope", check whether the thing is measurable — a declared exclusion is a promise you stopped looking.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26). Six caught.
49. **Renaming is load-bearing only when the name invites a wrong value** (S22). **S28: `bytes` was that name.**
50. **A counterexample built on a degenerate case invites dismissal** (S24). **S26 is the mirror: check whether it is *stronger* than claimed.**
51. **A near-miss is not the finding** (S24). Sweep the parameters to establish the regime exists.
52. **A test can encode the defect it was written to catch** (S25). **A harness written from the implementation confirms the implementation.** **S28: mutate the implementation and require the harness to notice.**
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25).
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25).
56. **Which fixture a published number came from is part of the number** (S25, S26).
57. **A check that cannot fail is not a check** (S27). **S28: a suite that cannot report a failure is worse. S29: and a check name whose first token is not unique is a check the mutation harness cannot match on — `re.findall(r"^  FAILED (\S+)")` captures one token, so name checks `family/single_token`.**
58. **Method notes for the Review Method Change chat.** S26 and S27 each posted three; S28 posted the observation that a response to F5 required me to write the checker rule that excuses my own file. **S29's queued note:** the delta-only rule handled well a response that closed a finding by *proving it could not be closed the expected way* — Codex offered two options, the honest answer was a third (narrow *and* build the coverage where a harness can reach), and the bounded scope kept that checkable instead of opening a fresh argument about what the harness ought to be. Post it only if Codex agrees it is a method observation rather than a session opinion.
59. **A mutation that is platform-conditional must say so where it is counted** (S29). The path-alias mutation is only observable on a case-insensitive filesystem; the harness's docstring says the total is a statement about this machine for that entry, and the acceptance case asserts the *correct* opposite behaviour on a case-sensitive one.

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Session 29 readings: 07:06 PDT — 0.61 GiB free *physical* RAM but 2,234 MiB *available* including standby, VRAM 1,079 of 16,311 MiB used, `C:` 589 GB free; 07:20 PDT — 7,154 MiB available.** **Read both numbers, not one:** `Win32_OperatingSystem.FreePhysicalMemory` excludes reclaimable standby memory and can read near zero while `\Memory\Available MBytes` reads gigabytes at the same moment. **Do not inherit these; take your own.** **The candidate read is sized by `--plan-only`, and the number to compare against free RAM is `peak_resident_bytes`**, not `resident_bytes`.

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64`; a numpy change is a replay risk and the drift result must be re-replayed after one.** **h5py's chunk-index API is now load-bearing** — `get_chunk_info_by_coord` and `get_access_plist().get_chunk_cache()`; an h5py change is a transfer-bound risk. Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

## 11. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins** and both agents append the round log and the outcome to it. **RC-002's index row must be updated when it closes.**
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section.**
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry landed inside the log section. **56 entries; banner at 2026-08-15.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link.
- **Corrections propagate forward, never backward.** The review cycle is the only exception.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. Sessions 16–29 worked entirely inside the scratchpad. **The mutation harnesses take ~3.5 minutes each — run them with `run_in_background` and collect the output file, not with a 120 s foreground timeout.**
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **total every read rather than the last one.** **1 MiB blocks transfer far less than the 4 MiB default** for scattered reads. **A retry re-transfers a block, so `n_bytes` can exceed the file size; the plan's `cache_bound_bytes` bounds *distinct* blocks and says so.** **The reader's cache is unbounded and is never evicted, which is why it is a memory term and not only a transfer term.**
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py` (`read_electrode_table`, `contiguous_band`), `anatomy_index.py` (Codex's), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`.
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` needs no step. **A script in `scripts/` without a step is a hard failure unless it is declared in `PENDING_STEP`** — and a script that is both a step and pending is also a failure, and both rules now have mutations. **After editing the packet runbook or any script docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **`mutation_test_runbook_checker.py` takes three positional arguments**, not flags: packet path, scratch directory, interpreter. It leaves its scratch directory behind — delete it.
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. **Check the printed surface by capturing `--help`, not only by scanning source** — `check_runbook_consistency.py` legitimately holds one en dash inside a regex that is never printed, and a source scan alone reports it as a violation.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (161/161 as of Session 29); the root `README.md`, the selection document and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert CR == LF afterwards.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path (`C:/Users/cresp/AppData/Local/Temp/ct`), comparing file by file, and **deleting the clone afterwards.**
- **Both `.gitignore` files carry a do-not-catch-these comment and ignore `__pycache__/`.**
- **`agents/Claude/tools/` holds seven scripts and one recorded output**, `source_count_granularity_probe_2026-08-13.txt`, because the matching rule cites its numbers.
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations`; `probe_band_drift_claims.py` takes `--module`; `test_measure_host_drift.py` takes `--keep` and `--tmp-root`; **`mutate_rc002_repairs.py` requires `--repo-root`**; Codex's probes take `--repo-root` (`probe_rc001_round1.py` requires it; `probe_rc002_round1.py` and `probe_rc002_round2.py` — the latter requires it).
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state, and it is how the en-dash claim in §3 was dated to Session 13 rather than guessed at.
