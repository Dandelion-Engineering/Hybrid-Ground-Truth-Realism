# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 27 · 2026-08-15 03:35 PDT**
**Next session is Claude Session 28. No count-based progress report is due** (the next is Session 32). A phase transition or an approved amendment written in your session would trigger one anyway.

## 0. ⚠️ THE REVIEW METHOD — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

***Convergence in place of escalation* is agreed, written into the playbook, and binding.** `Escalated` is no longer an outcome; the outcomes are **Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required**. At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**: each writes, once, the minimum claim it thinks can ship, the evidence that controls, the strongest evidence against its own position, and one acceptable safe disposition. **Evidence determines what may ship; consensus determines what happens next. Underdetermined evidence is not resolved in favour of approval.** The card closes at a disposition, the owner repairs **outside** review, and may open **one** successor card with a `Supersedes:` line; **a second like-for-like successor is not allowed**. Three readings are in the playbook's operating notes and Codex has agreed to all three: approval stays explicit and state-specific; an unchanged sentence made false by a change elsewhere **is** a regression introduced by the response and so is in scope after Round 1; and a LATE-BLOCKER created by an earlier repair says so.

**RC-001 closed `Approved` at its third round with no Convergence Decision. The method has now survived one full cycle.** Feedback on the method stays an open obligation in `chats/Claude-Codex-Human/Review Method Change/` — Randy asked for it and asked that the chat stay active. Session 27 posted three observations (§9.58).

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six.

**⚠️ This file describes the moment it was written.** Codex has now six times posted a handoff within the hour after a session closed. **Read the active chats before you act on §2.**

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
| `agents/Claude/tools/test_band_drift.py` | **`946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` — same-state approved, closed.** 103 checks, 0 failed at the pinned 200 permutations, 48 s. |
| `Reproducibility Packet/scripts/utils/archive_units.py` | **NEW. `c5c21cb9a2e0f9cedd0f1cff7e98886cb77ccdd21e2ad763422a7b44f3146f12` — open on Codex under RC-002.** |
| `agents/Claude/tools/measure_host_drift.py` | **NEW. `c71a5d9311b0785dcff5469e9c698f0f208946cafb00b32dd4eb0bddbda93cfb` — open on Codex under RC-002.** |
| `agents/Claude/tools/test_measure_host_drift.py` | **NEW. `6ff3d26ce64016efabdf71aaab93c9a0d71526f37fdcbedae457c438f50a3b39` — open on Codex under RC-002.** **163 checks, 0 failed, 10.2 s.** |
| `agents/Claude/tools/probe_band_drift_claims.py` | `4f3b83773156e7f9654f3e080d5adb258658cf500cf741aaea04b5015f07c34f` — closed. 3 of 3 probes pass. |
| `agents/Codex/tools/probe_draft16_safety_claims.py` | `d1c9220dc0f0890744d920638210f501abdc9b53b84256ef89afbc59e6bca6ac`. Digits `7.966`/`8.346 µm` and `27.273`/`11.591 µm` reproduce. **His; do not edit it.** |
| `agents/Codex/tools/probe_rc001_round1.py` | Codex's independent probe, now **13 checks** including a 93,184-case exhaustive bound check. Takes `--repo-root`. **0 failures at Session 27.** Run it; do not read its report. |
| `Reproducibility Packet/` | Eleven numbered-step scripts plus the checker, `DATA.md`, pinned deps, its own `.gitignore`, and `scripts/utils/{band_drift,archive_units}.py`. Runbook checker green at ten steps. |

## 2. The first thing to do next session

**Check the active chats before assuming anything. As of writing, everything open is open on Codex and nothing is open on you.**

- `chats/Claude-Codex/Archive-Reading Drift Command Review/` — **the live review, governed by `Review Cards/RC-002 Archive-Reading Drift Command.md`. Round 1 is open on Codex and is a full pass.** RC-002 is a **new candidate, not a successor** to RC-001.
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active.**
- `chats/Claude-Codex/Tier A Selection Section 16 Review/` · `Tier A Selection Review/` · `Tier A Donor Matching Rule/` · `Reproducibility Packet Review/` — **all concluded.**

**If RC-002 closes `Approved`, the next work is the first real candidate measurement** (§5.2). **Until it closes, do not read a candidate and do not measure one.**

**Three decisions in RC-002 are flagged for Codex to overrule rather than accept.** If he returns a finding on any of them, it is not a defect you missed — it is a decision you deliberately surfaced:
1. the command lives in `agents/Claude/tools/`, not the packet's `scripts/`, and is not step 11 yet;
2. it imports `read_series_timing` from `screen_host_timing.py` rather than reimplementing it or lifting it into `utils/` (lifting edits an approved packet script, which you did not do unilaterally);
3. there is no `--threshold-um`; `--gate` resolves to the pre-declared strict/relaxed values only.

## 3. What Session 27 built

**The archive-reading layer. Three new files, and no existing file changed by a byte.**

### 3.1 `utils/archive_units.py` — reads and refuses

Targeted range reads over the ragged `spike_times` and `spike_distances_from_probe_tip_um` slices for band units only. It performs §16.8's four confirmations and **raises `ValueError` on every violation**, which the command converts into a named non-zero exit with no verdict:

1. **the two ragged columns are partitioned identically** — read both `_index` arrays in full and require equality, plus non-decreasing and ending at the column length;
2. **values finite, times ascending, and the depth column's own stored description still contains `micrometers`** — the description is reported verbatim, and the check is a substring so punctuation cannot cause a rejection;
3. **each unit's `max_electrode` names one electrode on that unit's own probe with a finite `rel_y`** — validated for every unit whose `probe_name` is the requested probe;
4. **the raw and processed electrode tables agree** — *this one is not in §16.8 and is a real trap*: the band comes from the **raw** table while `max_electrode` indexes the **processed** one.

It also **plans the transfer before spending it**: the ragged index gives the exact byte cost, `plan_only=True` returns it without reading spikes, and `max_bytes` refuses to exceed a declared ceiling.

### 3.2 `measure_host_drift.py` — the command

Resolve session → raw+processed assets · read raw electrode table · `contiguous_band` · `read_series_timing(n_edge=2)` → require `timing_source == "timestamps"` and finite increasing endpoints · read band units · require electrode-table agreement · containment + the two slack values · `complete_bins(t_last_s)` · `measure_band_drift` · `permutation_null` **twice, requiring exact reproduction** · `apply_gate` · report.

- **A failed replay sets the result unmeasurable** rather than raising — that is §16.7's rule.
- **`--gate {strict,relaxed}` only.** No typed threshold exists.
- **`record["io"]` totals all three reads** (raw electrodes, raw timing, processed units) and reports the split.
- The report prints the null's **deciles at nearest rank**, the same rule `Q95_null` uses.
- Per-unit audit values come from the estimator's own `unit_traces`/`unit_excursions`, never a second centring — asserted elementwise in the harness.

### 3.3 The harness — 163 checks

Local HDF5 fixtures shaped like the two assets; the real `main()` runs against them with `RemoteFile` substituted in `archive_units`, `host_anatomy` and `screen_host_timing`, and `dandi.list_assets`/`blob_url` substituted. **Every confirmation has at least one deliberately broken fixture.** `case_grid_extent_is_t_last` is the one to read first: `t_first_s = 61 s` proves the grid takes 15 bins from `t_last_s` and not the 13 the span would give.

**Sessions must use UUID-shaped session ids** — `utils.dandi` matches `ses-<36 chars>` only. `session_id()` derives one from the case name.

### 3.4 Two defects found by rendering the report and reading it

- **The reported transfer omitted two of its three reads.** Fixed and asserted.
- **The null was reported by endpoints only**, where §16.5 asks for the distribution. Deciles added.

### 3.5 A structural defect fixed in the public README

The four newest running-log entries had been appended into the **wrong section** — after the working-record bullet list in *What this repository will contain*. Moved back into the running log, in order, byte for byte, with assertions. **I introduced it in Session 25 by appending at a convenient anchor; Codex followed it twice.** The log now stands at **52 entries, all inside `## Running log`**; the banner is at 2026-08-15. **Append new entries before the `---` that closes the Running log section, not at the end of the file.**

## 4. The estimator and the reader, as they stand

`band_drift.py` public surface (unchanged, approved): `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** The symbol is `Delta_10min`. Band keys are `delta_full` / `delta_window` / `window_start`; `apply_gate` returns **`passed`** (not `passes`).
- `measure_band_drift(spike_times, depths, extent_s, params=None)` returns `measurable`, `reason` when False, and when True **six** per-unit audit lists aligned with `included`: `unit_delta_full`, `unit_delta_max_window`, `unit_max_window_start`, `unit_max_window_defined_bins`, `unit_delta_band_window`, `unit_band_window_defined_bins`. **`delta_max_window` is the per-unit list's name; the band's is `delta_window`.**
- `permutation_null(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` — **does not take the observation.** Raises on unmeasurable observations, malformed collections, duplicate/negative/non-integer rows.
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)`, **anchors at 0**; spikes below zero fall outside every bin and are silently excluded — the reader counts and reports them.
- **A recording needs at least 11 analysed bins.** Candidates carry 54–87.

`archive_units.py` public surface: `read_flat_electrodes` · `column_descriptions` · `source_provenance` · `read_unit_scalars` · `check_ragged_alignment` · `resolve_unit_electrodes` · `select_band_units` · `plan_transfer` · `read_band_units` · `electrode_tables_agree`. Constants `UNITS_PATH`, `ELECTRODES_PATH`, `TIME_COLUMN`, `DEPTH_COLUMN`, `DEPTH_UNIT_PHRASE`, `PROVENANCE_PATHS`.

## 5. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 5.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Do not re-derive it and do not re-sort it.** Ranks 4–5 outrank rank 3 on channel count deliberately. NYU-39 at rank 9 is deliberate — deprioritized, never disqualified, **and the label-blind unit set is what keeps it that way.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first; cannot change a verdict, only cost): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

### 5.2 The next piece of work, once RC-002 closes

**Measure rank 1 — CSHL047 Probe01, session `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`.**

**Run `--plan-only` first, then measure free RAM against that exact number, then read.** The plan is a count, not an estimate. Expect a few hundred megabytes of spike arrays for a 22–267-unit band; the raw file's `t_first_s` for this series is **1.138 s**, so its bin 0 carries 58.86 s of coverage out of 72 bins and `head_partial_s` will be non-zero.

Command shape (from the packet folder, with `scripts/` on `sys.path`; see the module docstring):

`measure_host_drift.py --session <uuid> --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

**When it has actually been executed, the command moves into `Reproducibility Packet/scripts/` unchanged and becomes runbook step 11**, with the README step added and `check_runbook_consistency.py` re-run. **A script dropped into `scripts/` without a README step is a hard checker failure.**

### 5.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. Stricter than Draft 7 §10's parameterized sweep. **Do not reopen §1–§16** — it belongs in a future section. **Codex still owns the footprint/placement calibration**; do not start it.

## 6. What is still not done

1. **No host is pinned**, and that is correct.
2. **No candidate has been measured.** The reader exists but is unapproved.
3. **The capacity gate needs re-establishing** under Amendment 6's stricter condition (§5.3).
4. **Five of the ten packet steps still have not been re-run** (the archive-reading ones). The README says so.
5. **The preprocessing half of the amplitude question is untouched** and not metadata-answerable — Rung 0 territory.
6. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question, not a coding one.
7. **`is_injectable` is a denylist over a partly derived vocabulary**, so a re-derivation reaching a new fibre tract defaults it to injectable. Latent: no consumer reads it.

## 7. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** · **the real-arm donor-matching rule** · **the exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 8. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`, `G0` the mean paired sorter gap *in the control arm*** — not the negative-control band. `[−T, T]` is declared shorthand for the `D` rule, never a second test. `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins, not ten.** Widening is monotone and can only reject more. Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those are input errors that pause the pinned order (§16.4), and the reader now enforces that separation in its exit status.
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** `0.000`/`15.000`/`30.000 µm` describes the **equal-baseline fixture** only. A median tracks rank, so displacing `k` of a bin's `n` spikes upward moves its median **at most the displacement itself and at most the distance to the depth `k` ranks above it** (0 violations, 4,000 random cases; Codex's independent exhaustive check: 93,184 cases). On a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`, and 2% moves it `29.000 µm`. Grid placement matters because it fixes `k`: `30.000 µm` in one bin, `0.000 µm` split across two. **The gate has no guaranteed resolution below the bin width in either direction. The old "permissive" claim is WITHDRAWN and must not be re-derived on the new bound.**
- **The drift unit set is blind to `kilosort2_label`** and is selected by valid same-probe `max_electrode -> rel_y` inside the band. **That choice carries no one-way safety guarantee.** `distance_from_probe_tip_um` selects nothing; per-spike depths enter only the centred within-unit steps.
- **The per-unit excursions are reported and never consumed**, they carry no null, and they do not discharge that conditional in either direction. **Never compare a per-unit value to `Q95_null` or to `L`.** **Neither the concentration nor the scatter of `unit_max_window_start` is evidence.** **And the absence of magnitude separation is not evidence either** (`14.941`/`7.125 µm` fixture, twenty of forty-one units moving 30 µm). **The claim that masking strengthens with band size is WITHDRAWN** — 35 of 120 seeds break it at a fixed 40% moving fraction.
- **The bin grid anchors at session `t = 0` with extent `t_last_s`**, on pinned converter provenance. **`duration_s` is a span and is not an alternative clock hypothesis.** Endpoint containment is a consistency check that cannot identify a clock, and its margins are **endpoint slack** that bounds nothing internal.
- **The head bin is retained and reported, with no claimed direction.** Confined to rank 1 at 1.9% of one bin in 72.
- **The permutation pool is analysed-bin spikes only**, for both observation and null.
- **`cumulative_drift_um_per_hour` is retired on its own description** — a path length, spike-count-correlated at ~0.79, and "NOT actual electrode displacement" in IBL's words.
- **Amendment 6 governs: Tier A is parameterized by `N`.** `10 ≤ N ≤ 16` continues; `N < 10` is Slot 12.3. Fifty occurrences split `q = ⌊50/N⌋`, `r = 50 mod N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.**
- **`N ≥ 10` is structural:** `16 − 6 = 10` = the injected-unit count Slot 7 fixes.
- **The manipulation check is a hard stop-or-go gate**, and the realized zone-donor count is a *composition-integrity* quantity, **not** a substitute for it.
- **Amendment 5:** the injection zone's donors are removed from the **real** region-unaware arm before matching. The frozen matching rule runs as a non-generating counterfactual on **both** the un-removed and post-removal pools, with only the post-removal state permitted to govern generation.
- **The matching rule's provenance test is two-level:** **Level A** matches distinct dataset, session *and* subject counts; **Level B** is the contract's literal `S_T` floor. **Level A binds only at stages 3 and 4.**
- **Before any real target manifest, host-specific pool or edge table exists**, the exposure-schedule/placement specification, the matcher implementation, exhaustive synthetic tests and same-state implementation approval must all be complete. All four steps.
- **0.11 and 0.12 are two sampling models, not two estimates of one number.** Blocked expectations are **1.03** (exact-insertion) and **1.17** (caliper). **Historical diagnostics at sixteen**, never predictions.
- **CA1's sixteen donors sit in exactly 4 source datasets, `[6, 5, 3, 2]`, which are 4 sessions and 4 animals** — KS044/KS046/KS051/KS055. Library-wide: **37 insertions, 24 sessions, 12 animals**.
- **The source-count floor binds at *every* relaxation stage** and is an **equality**, both directions.
- **One host and injection zone across all tiers by default**; a deviation is a recorded limitation and the cross-tier comparison is dropped rather than made across hosts.
- **CA1 is the approved first zone.** Do not commission the `SUB` literature task unless CA1 fails a real gate.
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **The donor library is good-clusters-only by construction.**
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.** Never apply the ~1.2 factor to one unit.
- **Pre-rescaling scale factors are a manipulation-check diagnostic, not a matching covariate.**
- **The Allen CCF ontology is not importable** — noncommercial terms, and `iblatlas` (MIT) / `brainglobe-atlasapi` (BSD-3) do not dissolve them. **No atlas package is installed and that is deliberate.**
- **The donor library's acronyms sit at mixed levels of the CCF hierarchy**, so "same region" is undefined when one label is a parent of the other. CA1 is a leaf and unaffected; **any zone change must check for parent-labelled donors first**.
- **A one-command-per-side runbook rule is a hard parse error, not a warning.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity when they are enrichment; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection that would have failed the quietest possible host; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins while preserving bin counts; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser and a median residual as a coordinate-equivalence test; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower" than a single trace; S25's half-of-a-bin's-spikes cutoff; **and S27's archive-transfer count that reported one of its three reads.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5). **S16–S22: six sessions running where the thing needed was already on disk. S23: already *computed*. S24: already *stated*.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5). **S17: for a host gate, pessimistic *is* the safe direction. S18: only for a genuinely absent measurement. S19: when a *proof* is withdrawn, ask what the unsafe direction now costs.**
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **Reviewer's version: review it against the contract, not against your own last draft** (S16).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and backslash escapes*** — write the text with the Write tool and have Python read it in. **`$VAR` does not expand inside the Bash tool's `-c` string passed to python**; pass the path as `argv`. **`.\venv\Scripts\python.exe` does not survive the Bash tool either — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7). **S26 is the harder case: a repair can create a *new false claim* rather than a gap, by describing a real measurement in words wider than the measurement.**
8. **A measurement you just made is not a threshold you get to set** (S7). The threshold *and its relaxation ladder* get written before the first measurement (S17). **S27 makes it mechanical: if the threshold cannot be typed on the command line, it cannot be chosen after the values are in.**
9. **Read a rich first-party table, not one column of it** (S7). Read the column's own `description` too — **and S27: make the code read it, so the unit is checked rather than assumed.**
10. **Verify a name before trusting it** (S7). **S22–S23: when the other agent hands you a probe and its output, run the probe. S24: when they hand you a *proof*, re-run that too. S26: when they hand you a *counterexample*, rebuild it from the description.**
11. **Two numbers in the same unit are not the same quantity** (S8); **two numbers that are the same quantity under different sampling models are also not the same number** (S11).
12. **When a safety check fires, measure it before loosening it** (S8). **S19 inverse: when a cost is cited for *not* doing something, measure the cost.**
13. **A correction is worth logging even when the conclusion survives** (S8).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9); a *better* reason arriving is also that moment (S15).
16. **An audit must use the same key its lookup uses** (S9). **S27 generalizes it: when an index in file A is used against a table in file B, the check is not that the index is in range — it is that A's and B's tables are the same table.**
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10). Twelve for twelve.
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17). **S23: when it does not survive, the counterexample becomes a permanent case.**
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11). **S27's application: a script does not enter the runbook until the command in it has actually been run and produced the result the step claims.**
24. **Note which direction a correction pushes** (S11), including when it makes your own next step harder (S15, S16). **S26: when you claim a repair changed no numerical branch, prove it with an AST comparison with docstrings stripped.**
25. **When a test fails, first ask whether the test or the artifact is broken** (S11). **`apply_gate` returns `passed`. `measure_band_drift` returns `delta_window`. `probe_rc001_round1.py` requires `--repo-root`. Read the parser.**
26. **Render the output; do not read the source and assume you know what it prints** (S12). **Read the finished section back as a reviewer** (S16, S18–S27). **S27: eight consecutive sessions where the read-back pass produced the last corrections — this time an archive-transfer count that omitted two of its three reads, and a null reported by its endpoints where the specification asks for its distribution.**
27. **Test a checker by breaking things, one breakage per clean copy** (S12). **S18: turn each defect review caught into a permanent test case. S27: when the failure you need cannot be requested from the real source, build a fixture that has it on purpose — there is no way to ask the archive for a file whose ragged indices disagree.**
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13). **S27: the policy here is that an input error is not a gate failure, because the order is first-admissible and a wrong rejection is not recoverable.**
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16). **S26: and the *fixture* behind it is the thing least likely to be interrogated at all.**
31. **A supersession can be too broad as well as too narrow** (S14).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17).
33. **Make an edit script assert exactly one match per replacement** (S14). Validate every replacement across every file *before* writing any of them.
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Ten for ten (S15–S23).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17). **S26: edit every restatement in the same pass.**
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.**
41. **Read the clock at the moment you write the timestamp** (S17).
42. **A status sentence doing a rule's job goes stale in the permissive direction** (S18). **S24: a diagnostic with no stated null result is read as reassurance.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20).
46. **State a check's *resolution*, not only its role** (S21) — **and only when the check actually has one** (S22). **S26: and state what it is a resolution *of*.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26). Six caught. **S26's is the different one: not a direction asserted past its evidence but a *boundary* asserted past its fixture.**
49. **Renaming is load-bearing only when the name invites a wrong value** (S22).
50. **A counterexample built on a degenerate case invites dismissal** (S24). **S26 is the mirror: check whether it is *stronger* than claimed.**
51. **A near-miss is not the finding** (S24). Sweep the parameters to establish the regime exists.
52. **A test can encode the defect it was written to catch** (S25). **A harness written from the implementation confirms the implementation.** Assert against the quantity's stated purpose.
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25).
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25).
56. **Which fixture a published number came from is part of the number** (S25, S26). **Before writing a general sentence from a fixture, ask what the fixture makes degenerate.**
57. **A check that cannot fail is not a check** (S27). The harness briefly carried an assertion whose condition was the literal `True`. It read as coverage and was noise; it was deleted rather than left to inflate a count.
58. **Method notes for the Review Method Change chat.** S26 posted three (delta-only review is sharper on repairs; the round-trip limit changed how the response was written; the honest cost is three sessions each). **S27 posted three more:** writing the card's `Purpose` field *before* the code changed what got built — eleven harness cases exist because of one sentence in it; the `Acceptance tests` field is what forced the render-and-read pass that caught both of this session's defects; and the method's structural weakness is that the owner writes the `Blocking severity` field for their own work, which narrows the review before it starts. **That last one is stated to Codex directly rather than left for him to notice.**

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Session 27 readings: 03:08 PDT — RAM 2.00 GiB free of 31.67; VRAM 1,077 MiB used of 16,311; `C:` 549.4 GB free. 03:30 PDT — RAM 6.65 GiB free.** The session's whole compute was small HDF5 fixtures and a numpy harness needing tens of megabytes. **The 2.00 GiB reading matters for what comes next:** the first real candidate read holds a few hundred megabytes of spike arrays at once, which is exactly what `--plan-only` and `--max-mib` exist to size first. **Do not inherit these; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. `band_drift.py` needs numpy and stdlib `hashlib`; `archive_units.py` needs numpy and h5py. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64` seeded from a 64-bit integer; a numpy change is a replay risk and the drift result must be re-replayed after one.** Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

## 11. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins** and both agents append the round log and the outcome to it. A card scopes a review; **it does not amend the Claim Sheet**. **RC-002's index row must be updated when it closes.**
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section; do not reach below it to fill a gap** without saying so in the review's own chat.
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session. Sync is of content, not of words.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **The root README's running log is lean and append-only, and it ends at a `---` before `## What this repository will contain`.** **Append new entries before that separator** — Session 27 found four entries (two of Codex's, two mine) that had been appended after the *next* section's bullet list, and moved them back. **The log stands at 52 entries; the banner is at 2026-08-15.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories, clones and branches before closeout. Sessions 16–27 worked entirely inside the scratchpad.
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **return them from a reader rather than discarding them, and total every read rather than the last one.** **1 MiB blocks transfer far less than the 4 MiB default** for scattered reads.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py` (`read_electrode_table`, `contiguous_band` → `depth_lo_um`/`depth_hi_um` in `rel_y`), `anatomy_index.py` (Codex's; pass `--legacy-index-target CA1 --legacy-index-max-gap-um 40`), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels` (opt-in derived layer), `band_drift`, **`archive_units`**.
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` modules need no numbered step — **and a new script dropped into `scripts/` without a README step is a hard checker failure.** **After editing either the packet runbook or any script's docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. Docstrings are fine; `print` is not. All three Session 27 files are verified at zero non-ASCII and zero CR bytes. **The sheets use straight quotes only** — verify with Python, not `grep`. The host-selection document carries **eight** curly quotes and no CRLF.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (159/159 as of Session 27); the root `README.md`, the selection document and all chat files are LF. **A pattern edit over a CRLF file must preserve `\r\n` in the match string** — matching a substring inside one line is the safe way, and an edit script should assert the CR count equals the LF count after editing.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path (`C:/Users/cresp/AppData/Local/Temp/ct`; the scratchpad path is too long for git), comparing file by file, and **deleting the clone and any temp branch afterwards.**
- **The resumable/pinned result files are tracked deliberately.** **Both** `.gitignore` files carry a do-not-catch-these comment, and both ignore `__pycache__/`.
- **The processed NWB units table is rich** — 31 described columns, and **`results/amplitude_conventions.json` already holds every column's `description` under `descriptions/`.** **`spike_times`' description names no time origin** — which is why §16.4 pins the clock from the converter instead. The ragged columns are `spike_times` / `spike_distances_from_probe_tip_um` with `_index` siblings.
- **`results/host_timing_index.jsonl` holds more than it was written for** — AP series names are `ElectricalSeries<Probe>AP`, and rank 1's Probe01 has `t_first_s = 1.13848929170131`, `t_last_s = 4340.732688643263`. **The reader re-measures these from the asset rather than consuming the index**, deliberately: a number in a file is inherited, a number read from the asset is measured.
- **`agents/Claude/tools/` holds seven files and one recorded output**, `source_count_granularity_probe_2026-08-13.txt`, because the matching rule cites its numbers. **That script needs `--cache "Reproducibility Packet/results/templates_snapshot_2026-08-11.csv"`; it has no default.**
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations`; `probe_band_drift_claims.py` takes `--module`; **both of Codex's probes take `--repo-root` and `probe_rc001_round1.py` requires it**; `probe_draft16_safety_claims.py` also takes `--threshold-um`; `test_measure_host_drift.py` takes `--keep` and `--tmp-root`.
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state.
