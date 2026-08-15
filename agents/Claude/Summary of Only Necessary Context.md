# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 25 · 2026-08-14 23:45 PDT**
**Next session is Claude Session 26. No count-based progress report is due** (the next is Session 32). A phase transition or an approved amendment written in your session would trigger one anyway.

## 0. ⚠️ THE REVIEW METHOD — read this before you review anything, and note what changed again

**Randy directed a new review method after Session 24. It is in `Playbooks/review-cycle.md` as a superseding section and supersedes the rest of that playbook. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

**Session 25 changed one thing inside it, and it is now binding.** Randy said an escalated review parked on his reply would waste sessions, and asked the agents to agree on a replacement. Codex proposed five clauses; I accepted them **as written** and wrote them into the playbook as ***Convergence in place of escalation***:

- **`Escalated` is no longer an outcome of ordinary review**, and *human triage* is no longer a trigger. The outcomes are **Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required**.
- At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**: each writes, once, the minimum claim it thinks can ship, the evidence that controls, the strongest evidence against its own position, and one acceptable safe disposition.
- **Evidence determines what may ship; consensus determines what happens next.** Underdetermined evidence is **not** resolved in favour of approval.
- The card closes at a disposition, the owner repairs **outside** review, and may open **one** successor card with a `Supersedes:` line. **A second like-for-like successor is not allowed** — the work must be split or redesigned first. That is what makes the three-round-trip limit cumulative.

**Two things I added are applications of existing notes, not changes to his five clauses, and Codex may strike either:** the Convergence Decision is written into the Review Card; and a **director-only** finding (licence, outside contact, spend, Claim Sheet amendment) still reaches Randy through `director_requests.md` with a fallback while the card closes at one of the four dispositions. Removing `Escalated` removed a review outcome, not the director's channel.

**Three earlier readings remain in the playbook's operating notes and Codex has now agreed to all three:** approval stays explicit and state-specific; an unchanged sentence made false by a change elsewhere **is** a regression introduced by the response and so is in scope after Round 1; and a LATE-BLOCKER created by an earlier repair says so.

**Feedback on the method stays an open obligation** in `chats/Claude-Codex-Human/Review Method Change/` — Randy asked for it and asked that the chat stay active. What Session 25 reported there, and what to keep watching, is in §9 below.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six.

**⚠️ This file describes the moment it was written.** Codex has now four times posted a handoff within the hour after a session closed. **Read the active chats before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, no candidate has been measured on any open gate, and nothing beyond bounded metadata reads has been downloaded.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 23, `e7dcfc54f495c96f62c4994cfa8178882edaba38aa0b48a15c3fcb107534b5bf`.** §1–§15 same-state approved. §16 is the RC-001 Round-2 candidate. **Open on Codex.** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **`4ac9fa56dc7a2035d1f9b037b9010ae448fc1c621f92ea93876db1c1fc06ab19` — open on Codex.** Session 25 changed `window_bins` 10 → 11 and renamed the symbol; nothing else. |
| `agents/Claude/tools/test_band_drift.py` | **`e2e63a037ee81886b01779535c22ce296502bc3a132ee3f77f9ad6f345869420` — open on Codex.** **96 checks, 0 failed** at the pinned 200 permutations, 48 s. |
| `agents/Claude/tools/probe_band_drift_claims.py` | **`4f3b83773156e7f9654f3e080d5adb258658cf500cf741aaea04b5015f07c34f` — same-state approved. Closed and unchanged.** 3 of 3 probes pass. |
| `agents/Codex/tools/probe_draft16_safety_claims.py` | **`af51fe507be92bcbd0b8b2d7063fcc20e2208f78905b9cceb1d8ef30717bf205`** — Codex's, unchanged. Both counterexamples still reproduce; **its moving-only digit moved from `24.545` to `27.273 µm`** as a consequence of the Session 25 repair. **His to re-pin; do not edit it.** |
| `agents/Codex/tools/probe_rc001_round1.py` | Codex's Round-1 independent probe. Run it; do not read its report. |
| `.gitattributes` | **`036c696c3e1ea9cef70925ec8dfedc407ef59bb20e5c00e17ef9b5f88855bfa0` — same-state approved. Closed.** |
| `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` | **Draft 6, `51adae4b…` — same-state approved. Its chat is concluded.** |
| `Reproducibility Packet/` | Eleven numbered-step scripts plus the checker, `DATA.md`, pinned deps, its own `.gitignore`, and `scripts/utils/band_drift.py`. Runbook checker green at ten steps. |

## 2. The first thing to do next session

**Check the active chats before assuming anything. As of writing, everything open is open on Codex and nothing is open on you.**

- `chats/Claude-Codex/Tier A Selection Section 16 Review/` — **the live review, governed by `Review Cards/RC-001 Tier A Selection Section 16.md`.** **Round 1 (Codex, S24) returned three findings and did not approve. Round 2 (my S25 response) accepted all three and returned Draft 23 plus two changed implementation states. Round 2 is open on Codex and is delta-only.** **Round 3 is the limit; after that it is the Convergence Decision, not Randy.**
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active.** The convergence rule is agreed and written in. Codex may still strike either of my two additions.
- `chats/Claude-Codex/Tier A Selection Review/` · `Tier A Donor Matching Rule/` · `Reproducibility Packet Review/` — **concluded.**

**If RC-001 closes as Approved, your lane is the archive-reading drift script** (§5.2) — and it gets **its own Review Card** before Codex reviews it. **Until RC-001 closes, do not measure a candidate and do not read one.** You may write, but not run, the archive reader.

## 3. What Session 25 did

**Owner Round-2 response to Codex's RC-001 Round 1. All three findings accepted, none disputed. Every one of his constructions was reproduced independently before anything was edited.**

### 3.1 F1 — the gate window did not implement the quantity it names (blocking)

`Delta_10` was the worst window of **ten** consecutive 60 s bins. Two independent errors, each costing exactly one bin, each permissive:

1. **a bin median is a point summary**, so ten of them span only nine minutes between the extremes — a common `2.1 µm/min` ramp travels `21.0 µm` in ten minutes and was reported as `19.032 µm` (my fixture) / `19.145 µm` (the harness fixture), passing the 20 µm gate;
2. **a 600 s segment that does not start on a bin edge touches eleven session bins** — levels `[0, 15×9, 30, …]` gave `15.000 µm` from every aligned ten-bin window while `[30 s, 630 s)` spans `30.000 µm`.

**Repair: `PARAMS["window_bins"]` 10 → 11, symbol renamed `Delta_10min`.** Eleven bins contain every bin any ten-minute segment can touch — checked over 8,572 sub-bin offsets; the touched count is only ever 10 or 11. **The change is monotone** (every ten-bin window sits inside an eleven-bin one; zero violations over 2,000 random traces), so it can only reject more candidates, never fewer. **Nothing else moved** — no other parameter, threshold, seed, verdict path, error string or return key.

### 3.2 The third construction, declared rather than repaired

**No window length fixes within-bin aliasing.** Measured on a 30 µm episode inside one bin: `0.000 µm` at every displaced fraction **below one half**, `15.000 µm` at exactly one half, `30.000 µm` above it. §16.4 now says the gate resolves displacements persisting across at least half of a bin's spikes and is blind below that, **that the blindness is permissive** — it can only understate drift, the unsafe direction for a host gate — and that a passing candidate is admissible against drift *expressed at 60-second resolution*. **A sub-bin statistic was declined for the third time in this section**: the inclusion floor is ten spikes per bin, so any sub-bin split rests on five or fewer centre-of-mass depths for a marginal unit and reintroduces the noise the bin median removes.

### 3.3 F2 — my own one-way claim, withdrawn (blocking)

Draft 22 said masking gets easier as the band grows. **The series was not at a fixed moving fraction** — `5/11`, `10/21`, `20/41` are `0.4545`, `0.4762`, `0.4878`. At a genuinely fixed 40% fraction the direction fails: **35 of the 120 seeds in `7000`–`7119` are not monotone decreasing**, and seed 7025 gives `12.192`, `11.529`, `14.190 µm` at 10, 20, 40 units. Withdrawn, with the counterexample and the seed count as permanent cases. **Fourth one-way claim of mine this class has caught.**

### 3.4 The knock-on the repair created

**The masking fixture that supports *absence proves nothing* stopped passing** — twenty-one units now report `21.614 µm` and fail. A failing fixture proves nothing about a passing candidate. Re-established at **forty-one units, twenty moving: passes at `Delta_10min = 14.941 µm`, `Q95_null = 7.125 µm`**, moving own-worst `[32.5, 57.0] µm` overlapping stationary `[20.9, 37.6] µm`, seven of twenty inside.

### 3.5 F3 — accepted as written

§16.4 step 3 now says a median carries **no spike-count term** — adding observations can move a realized sample median but cannot mechanically accumulate a positive contribution per spike — rather than the false claim that its value does not move with spike count.

### 3.6 The convergence consensus

Accepted as written and in the playbook. See §0.

## 4. The estimator, as it stands — open on Codex, do not extend

`Reproducibility Packet/scripts/utils/band_drift.py`, `4ac9fa56…`. Public surface unchanged: `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** The symbol in the prose is `Delta_10min`. **The return keys did not change**: the band excursion keys are still `delta_full` / `delta_window` / `window_start`, and `apply_gate` still returns **`passed`** (not `passes`).
- `measure_band_drift` returns `measurable` plus, when False, a `reason` **naming the cause**; when True it also returns **six** per-unit audit lists aligned with `included`: `unit_delta_full`, `unit_delta_max_window`, `unit_max_window_start`, `unit_max_window_defined_bins`, `unit_delta_band_window`, `unit_band_window_defined_bins`. Keep all of them. **`delta_max_window` is the *per-unit* list's name; the band's is `delta_window`.**
- `unit_excursions` returns `None` for a windowed value with fewer than two defined bin medians in its span — **never zero**. Ties resolve to the earliest window, in both it and `excursions`.
- `permutation_null` **raises** on an unmeasurable observation, on malformed unit collections and on duplicate/negative/non-integer row indices. Caller order: measure → if measurable → null → gate. **Its seeds derive from the asset id and probe strings you pass.** Signature: `(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` — it does **not** take the observation.
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)` and **anchors at 0**; `bin_offsets` builds edges as `arange(n_bins+1)*60`, so **spike times below zero fall outside every bin and are silently excluded** — §16.4 requires that count reported. **The CLI passes `t_last_s`.**
- **A recording now needs at least 11 analysed bins**, not 10, or the observation is unmeasurable. Candidates carry 54–87 bins, so this binds only on fixtures.
- The full 200-permutation null on a 14-unit, 61-bin synthetic band takes **3.4 s**; the whole 96-check harness takes **48 s**. Never argue the permutation count on runtime grounds.
- It is in `utils/` because the checker walks `scripts/` **non-recursively**. The archive-reading CLI becomes step 11 **only once it has actually been executed**.

## 5. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 5.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Do not re-derive it and do not re-sort it.** Ranks 4–5 outrank rank 3 on channel count deliberately. NYU-39 at rank 9 is deliberate — deprioritized, never disqualified, **and the label-blind unit set is what keeps it that way.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first; cannot change a verdict, only cost): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

### 5.2 The next piece of work

**The archive-reading script**, which becomes packet step 11. Targeted range reads over the ragged `spike_times` and `spike_distances_from_probe_tip_um` slices for **band units only**, reusing `utils/remote_hdf5` and `utils/host_anatomy`, calling into `utils/band_drift`. Report `n_bytes`/`n_requests` rather than discarding them; 1 MiB blocks beat the 4 MiB default for scattered reads.

**Four things §16.8 requires it to confirm before it computes anything:**

1. the ragged index resolves aligned per-unit `spike_times` / `spike_distances_from_probe_tip_um` slices on these specific assets;
2. those values are finite and the depth column keeps its documented micrometre unit;
3. the exact raw and processed assets satisfy §16.4's **provenance-pinned session clock** and the containment sanity check — **this validates a declared clock, it does not choose one**;
4. every included unit's `max_electrode` resolves unambiguously to a finite `rel_y` **on the same probe** (missing / cross-probe / ambiguous = input error, never a band translation).

**And it must report, not just check** (note the per-unit windowed values are now eleven-bin, like the band's)**:** the two endpoint-slack values, `n_bins`, `discarded_s`, `head_partial_s`, spikes before the grid origin, band unit count, units surviving the inclusion rule, per-set total/`good` counts with row identifiers and stored labels, **and all six per-unit audit lists — from `unit_traces`/`unit_excursions`, never from a second centring of its own.**

### 5.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. Stricter than Draft 7 §10's parameterized sweep. **Do not reopen §1–§14** — it belongs in a future section. **Codex still owns the footprint/placement calibration**; do not start it.

## 6. What is still not done

1. **No host is pinned**, and that is correct.
2. **The archive-reading drift script does not exist** (§5.2). The statistic does.
3. **The capacity gate needs re-establishing** under Amendment 6's stricter condition (§5.3).
4. **Five of the ten packet steps still have not been re-run** (the archive-reading ones). The README says so. The drift script reads the same archive and is the natural place to fold them in.
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
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins, not ten** — ten bin medians span only nine minutes between the extremes and an off-grid 600 s segment touches eleven bins, so ten was permissive in two independent ways (S25/RC-001-F1). Widening is monotone and can only reject more. **The gate is blind to motion moving fewer than half of a bin's spikes**, measured at `0.000`/`15.000`/`30.000 µm` below, at and above one half; that blindness is permissive and is a declared limitation, not a defect to repair. Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those are input errors that pause the pinned order (§16.4).
- **The drift unit set is blind to `kilosort2_label`** and is selected by valid same-probe `max_electrode -> rel_y` inside the band. **That choice carries no one-way safety guarantee** — the result is *conditional* on movement being expressed in enough traces. `distance_from_probe_tip_um` selects nothing; per-spike depths enter only the centred within-unit steps.
- **The per-unit excursions are reported and never consumed, they carry no null, and they do not discharge that conditional in either direction.** `Q95_null` grades a median across units and has **no fixed ordering** against a single trace — narrower on homogeneous fixtures (1.6× to 2.8×), wider on a heterogeneous one, and the reversal does not need an exactly-flat unit (6 µm against 18 µm suffices). **Never compare a per-unit value to `Q95_null` or to `L`.** **Neither the concentration nor the scatter of `unit_max_window_start` is evidence** — a genuine common ramp scatters them over 12 of 14 bins. **And the absence of magnitude separation is not evidence either:** a fixture inside the declared parameters passes both gate numbers with **twenty of forty-one** units genuinely moving 30 µm and no separation visible (`14.941`/`7.125 µm`, moving `[32.5, 57.0]` overlapping stationary `[20.9, 37.6] µm`). **The claim that masking strengthens with band size is WITHDRAWN (S25/RC-001-F2)** — the series behind it was not at a fixed moving fraction, and at a fixed 40% fraction 35 of 120 seeds break the direction. The band statistic has **no fixed direction in the unit count**. A disagreement with the band statistic is a published limitation, not a reopened verdict.
- **The bin grid anchors at session `t = 0` with extent `t_last_s`**, on pinned converter provenance. **`duration_s` is a span and is not an alternative clock hypothesis.** Endpoint containment is a consistency check that cannot identify a clock, and its margins are **endpoint slack** that bounds nothing internal — do not revive either as more than that.
- **The head bin is retained and reported, with no claimed direction.** Confined to rank 1 at 1.9% of one bin in 72.
- **The permutation pool is analysed-bin spikes only**, for both observation and null. Partial-bin depths and pre-origin depths enter neither.
- **`cumulative_drift_um_per_hour` is retired on its own description** — a path length, spike-count-correlated at ~0.79, and "NOT actual electrode displacement" in IBL's words. The count scaling is specifically disqualifying because Tier B's manipulation *is* population-rate coupling.
- **Amendment 6 governs: Tier A is parameterized by `N`**, the zone donors surviving the **per-donor** host gates. `10 ≤ N ≤ 16` continues; `N < 10` is Slot 12.3. Fifty occurrences split `q = ⌊50/N⌋`, `r = 50 mod N`. Control arm and both pseudo-arms follow `N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.**
- **`N ≥ 10` is structural:** `16 − 6 = 10` = the injected-unit count Slot 7 fixes.
- **The manipulation check is a hard stop-or-go gate**, and the realized zone-donor count is a *composition-integrity* quantity, **not** a substitute for it.
- **Amendment 5:** the injection zone's donors are removed from the **real** region-unaware arm before matching. The frozen matching rule runs as a non-generating counterfactual on **both** the un-removed and post-removal pools, with only the post-removal state permitted to govern generation. The rule is fixed **before** the eligible pool is visible and may contain no region term in either direction.
- **The matching rule's provenance test is two-level:** **Level A** matches distinct dataset, session *and* subject counts (`S_T`, `E_T`, `B_T`); **Level B** is the contract's literal `S_T` floor. A stage tries A, then B, and only relaxes when both fail. **Level A binds only at stages 3 and 4.**
- **Before any real target manifest, host-specific pool or edge table exists**, the exposure-schedule/placement specification, the matcher implementation, exhaustive synthetic tests and same-state implementation approval must all be complete. All four steps.
- **0.11 and 0.12 are two sampling models, not two estimates of one number.** Blocked expectations are **1.03** (exact-insertion) and **1.17** (caliper). **Historical diagnostics at sixteen**, never predictions. **Never place the realized count next to a comparator without naming the model.**
- **CA1's sixteen donors sit in exactly 4 source datasets, `[6, 5, 3, 2]`, which are 4 sessions and 4 animals** — subjects KS044/KS046/KS051/KS055. Target-side and host-independent. Library-wide: **37 insertions, 24 sessions, 12 animals**; of 66,045 four-source subsets only 37,424 span four animals and 74 span one.
- **The source-count floor binds at *every* relaxation stage** and is an **equality**, both directions.
- **One host and injection zone across all tiers by default**; a deviation is a recorded limitation and the cross-tier comparison is dropped rather than made across hosts.
- **CA1 is the approved first zone.** Do not commission the `SUB` literature task unless CA1 fails a real gate.
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **The donor library is good-clusters-only by construction.**
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.** Never apply the ~1.2 factor to one unit.
- **Pre-rescaling scale factors are a manipulation-check diagnostic, not a matching covariate.**
- **The Allen CCF ontology is not importable** — noncommercial terms, and `iblatlas` (MIT) / `brainglobe-atlasapi` (BSD-3) do not dissolve them. **No atlas package is installed and that is deliberate.**
- **`validate_ccf_label_map.py` validates the hand-authored core map and the `depth_along_probe`/`rel_y` agreement** — not the derived layer.
- **The donor library's acronyms sit at mixed levels of the CCF hierarchy**, so "same region" is undefined when one label is a parent of the other. CA1 is a leaf and unaffected; **any zone change must check for parent-labelled donors first**.
- **A one-command-per-side runbook rule is a hard parse error, not a warning.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim and the "protocol versions differ" self-contradiction; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity when they are enrichment; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort rather than a floor; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token when it is the insertion identifier; the master-seed requirement that left its derivation and stream mapping to a later configuration; the inside-null rejection that would have failed the quietest possible host; "both net displacements" for a max-minus-min range; the claim that sub-pitch motion is below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins while claiming to preserve bin counts; one additive-ramp fixture promoted into a general monotonicity proof for the null's bias; "take the length from `t_last_s`, never `duration_s`" — the mirror image of the defect it repaired; endpoint containment as a clock chooser and a median residual as a coordinate-equivalence test; the two Draft 16 guarantees Codex blocked in S21; S22's per-unit audit evaluated only inside the band-selected window; **and S23's `Q95_null` "systematically narrower" than a single trace, which is a one-way claim from one homogeneous noise family.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5). **S16–S22: six sessions running where the thing needed was already on disk. S23: the thing needed was already *computed*. S24: and the thing needed was already *stated* — the presence direction was written; only its mirror was missing.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5). **S17 inversion: for a host gate, pessimistic *is* the safe direction. S18 re-inversion: only for a genuinely absent measurement. S19: when a *proof* is withdrawn, ask what the unsafe direction now costs and whether anything bounds it.**
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **Reviewer's version: review it against the contract, not against your own last draft** (S16). **S18–S24: running the pass anyway on edits you already agree with is what produces the extra findings — seven sessions running, and in S20–S24 every finding came from that pass.**
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and backslash escapes*** — write the text with the Write tool and have Python read it in. **`$VAR` does not expand inside the Bash tool's `-c` string passed to python**; pass the path as `argv`. **`.\venv\Scripts\python.exe` does not survive the Bash tool either — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7). **S19: withdrawing an overclaimed proof left the rule's safety argued nowhere. S22: withdrawing it correctly can leave a *conditional* that nothing measures. S23: measuring the conditional can leave numbers with no rule for reading them. S24: and writing that rule in one direction leaves the other direction load-bearing and unstated. Each repair creates the next layer's gap; ask what the repair now obliges.**
8. **A measurement you just made is not a threshold you get to set** (S7). The threshold *and its relaxation ladder* get written before the first measurement (S17), and the ladder has to say whether it re-runs the whole order or only the candidate in hand (S18).
9. **Read a rich first-party table, not one column of it** (S7). Read the column's own `description` too, and check whether you already downloaded it (S15, S17, S19, S21).
10. **Verify a name before trusting it** (S7). **S18: verify a derived constant by re-deriving it. S20: verify a *field* by reading the code that wrote it. S21: when you accept a source second-hand, say so in `references.md`. S22–S23: when the other agent hands you a probe and its output, run the probe. S24: and when they hand you a *proof* — an AST comparison, a digest — re-run that too rather than accepting the sentence.**
11. **Two numbers in the same unit are not the same quantity** (S8); **two numbers that are the same quantity under different sampling models are also not the same number** (S11). **S19: a *span* is not an *end time*. S20: two depth columns in micrometres are not the same coordinate until someone checks. S21: two timestamp arrays with the same nominal rate are not built the same way. S23–S24: two micrometre excursions are not on the same scale when one is a median across units and the other is one unit — and their ordering is not fixed in either direction.**
12. **When a safety check fires, measure it before loosening it** (S8). **S19 inverse: when a cost is cited for *not* doing something, measure the cost before accepting it.**
13. **A correction is worth logging even when the conclusion survives** (S8).
14. **Design the measurement so it does not need the fragile step** (S8). **S20's best repair was Codex's, and this is why it was better than mine: it removed the second coordinate rather than bounding the error between two.**
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9); a *better* reason arriving is also that moment (S15).
16. **An audit must use the same key its lookup uses** (S9).
17. **A pessimistic bug announces itself; a silent one does not** (S9). **S18: that is the argument for rejecting on an invalid bin. S19: loud is not enough if the diagnosis is wrong. S21: a rejection produced by an unpinned reading of "which units" arrives before the measurement rather than after it.**
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10). Eleven for eleven now.
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17). **S23: when it does not survive, the counterexample becomes a permanent case, not a note.**
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11). **S18: keep a finished script out of the runbook until it has run. S19: a distribution fix has a *scope*.**
24. **Note which direction a correction pushes** (S11), including when it makes your own next step harder (S15, S16). **S18: state when a repair cannot cost anything, and prove it. S19–S21: when a repair's effect is nil, measure that and say so. S22–S23: when you claim a repair changed no numerical branch, prove it mechanically. S24: the cheapest such proof is to touch nothing — Draft 22 edits no utility line, so the claim needs no argument.**
25. **When a test fails, first ask whether the test or the artifact is broken** (S11). **S18: `grep -c $''` reports no CRLF in a file that is entirely CRLF. S19: `apply_gate` returns `passed`, not `passes`. S22: an exact float equality between two paths that pick different windows on a linear ramp. S24: `measure_band_drift` returns `delta_window`, not `delta_max_window` — that name belongs to the per-unit list.**
26. **Render the output; do not read the source and assume you know what it prints** (S12). **Read the finished section back as a reviewer** (S16, S18–S24). **S23: reading it back caught a universal quantifier. S24: it caught a cross-reference that counted paragraphs wrong and a heading that still said "two" after a third item was added — headings and cross-references are the last things a writer re-reads and the first a reader trusts.**
27. **Test a checker by breaking things, one breakage per clean copy** (S12). **S18: turn each defect review caught into a permanent test case. S19: reproduce the *defect* as well as the fix. S22–S24: when a counterexample lives only in a review probe or a scratch file, move it into the harness.**
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13). **S19–S20: "unmeasurable" versus "input error" is that choice one level up. S21: so is "which units". S22: so is an unconsumed diagnostic. S23: and its *reading* rule. S24: and the reading rule's silent half — what the diagnostic's null result means is policy whether or not anyone writes it down.**
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16). **S20: the *quantifier* inside it. S22: the table cell restating it. S23: a justification can name a case the code cannot produce. S24: and an operative sentence can survive three rounds of repair to the paragraph below it — a governing paragraph does not repair the sentence above.**
31. **A supersession can be too broad as well as too narrow** (S14). Broaden *and* add the carve-out in the same edit (S15).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17). **S20's inverse: ask whether the scale you need is already pinned somewhere. S21: and whether the check you are adding needs a parameter at all. S23–S24: and whether the repair needs machinery at all — a per-unit null was available twice and declined twice, because saying what the values cannot support is cheaper and more honest than building a second estimator to rescue them.**
33. **Make an edit script assert exactly one match per replacement** (S14). Validate every replacement across every file *before* writing any of them.
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Nine for nine (S15–S23).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17). **S20: nor does a new paragraph repair the *older* sentence above it. S22: nor does a repaired paragraph repair the table cell that restates it. S24: so when the finding is that a claim is too strong, edit the claim — adding a correct paragraph underneath it is what let this one survive from S22 to S24.**
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21). **S22 for an added *diagnostic*: show it cannot reach the verdict in either direction. S23 for an added *reading rule*: say in the text that it carries no threshold and no verdict. S24 for a *narrowed* claim: say that it removes an assurance rather than adding a constraint, so nobody reads it as a new gate.**
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S18: then ask which way its bias points. S19: bound what happens when it goes the other way. S20: state which side of the gate the bound covers. S23: and say what the null does *not* grade. S24: a null built for one statistic has no ordering against another, in either direction — do not substitute one for a missing yardstick.**
41. **Read the clock at the moment you write the timestamp** (S17).
42. **A status sentence doing a rule's job goes stale in the permissive direction** (S18). **S22: so does a *limitation* doing a safeguard's job. S23: and a published number with no reading rule is read against whatever else is on the page. S24: and a diagnostic with no stated null result is read as reassurance.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19). After any repair, ask what else now depends on what it touched.
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20). What caught it was following the rule into its consumer.
46. **State a check's *resolution*, not only its role** (S21) — **and S22's correction: only when the check actually has one. S24: and when it has none in one direction, say that, because silence reads as coverage.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22). **S23: build the case that would break a directional claim before writing it. S24: four claims across three sessions, two of them mine. S25: the fifth, and it was the third of those three consequences — "masking gets easier as the band grows" — killed by Codex checking the arithmetic I had not: the series was not at a fixed moving fraction. `5/11`, `10/21`, `20/41` are `0.4545`, `0.4762`, `0.4878`. **When you cite a series as evidence for a direction, check that the thing you are holding fixed is actually fixed** — and then look for a counterexample at the genuinely fixed value before publishing the direction. There were 35 in 120 seeds.**
49. **Renaming is load-bearing only when the name invites a wrong value** (S22). The same test governs cosmetic edits inside someone else's approved bytes: S23–S24 left the four curly quotes in the superseded status line alone and recorded the count instead.
50. **A counterexample built on a degenerate case invites dismissal** (S24). Codex's ordering reversal was right, but resting it on an exactly-flat unit gave a reader an out. Four minutes established that a merely-quieter unit does it too. **When you accept someone's counterexample, check whether it needs its extreme case — strengthening their finding is part of accepting it.**
51. **A near-miss is not the finding** (S24). My first masking fixture showed the overlap but failed the gate on noise alone, which demonstrated nothing about a *passing* candidate. Sweep the parameters to establish the regime exists before reporting it, rather than presenting the near case as the case.
52. **A test can encode the defect it was written to catch** (S25). `case_known_ramp` asserted `expect_win = ramp × 9 / n_bins` — the nine-minute span was written in as the *expected answer* and passed for eight sessions. **A harness written from the implementation confirms the implementation.** The fix is the same one the Review Card forces: assert against the quantity's stated purpose, not against what the code returns.
53. **Two independent errors can cost the same amount and coincide exactly** (S25). The point-summary span and the off-grid overlap are unrelated arguments and both are repaired at eleven bins. A coincidence like that is a reason to check the covering property directly — 8,572 offsets, touched-bin count only ever 10 or 11 — not a reason to feel good about the number.
54. **A tightening is affordable exactly once: before the first measurement** (S25). Changing a pinned gate parameter was routine here only because no candidate had been read and the 20 — 40 µm relaxation ladder was already declared. After one measurement the same change is a recorded-turn amendment at a far higher bar. **This is the concrete payoff of every earlier session's insistence on writing thresholds before data.**
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25). The window change made the masking fixture *fail*, and a failing fixture demonstrates nothing about what a *passing* candidate hides — which is exactly the near-miss error of S24. After any change to a statistic, **re-run every fixture whose claim depends on its verdict**, not only the ones whose numbers you expect to move.
56. **Which fixture a published number came from is part of the number** (S25). My scratch reproduction and the permanent harness case used different seeds and gave `19.032` versus `19.145 µm`. The document must cite the **permanent case**; the scratch number belongs in the chat, labelled as such.


## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). The old low-memory series was leaked Claude automation processes, not competing research; **do not reason from its shape.** Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Last reading: 2026-08-14 23:10 PDT — RAM 7.57 GiB free of 31.67 (76% in use); VRAM 1,082 MiB used of 16,311; 591.6 GB free on `C:`.** **Do not inherit it; take your own.** (Session 23's reading two hours earlier was 6.34 GiB free, Session 22's 1.67 GiB, Session 21's 6.79 GiB. The machine moves by gigabytes in both directions inside a session gap, which is the whole point of the rule.)

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. `band_drift.py` needs numpy and stdlib `hashlib` only. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64` seeded from a 64-bit integer; a numpy change is a replay risk and the drift result must be re-replayed after one.** Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

## 11. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins** and both agents append the round log and the outcome to it. A card scopes a review; **it does not amend the Claim Sheet** — the amendment protocol still governs that. The public root README carries one orientation line for the folder.
- **`Playbooks/review-cycle.md` is now two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section; do not reach below it to fill a gap** without saying so in the review's own chat.
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session. **Their wording may legitimately differ where their own texts differ.** Sync is of content, not of words.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **The root README's running log is lean and append-only** — entries only for a finished artifact, a phase close, or something genuinely noteworthy. The banner's "Last updated" is the one line that may be overwritten. The log stands at **49 entries**; the banner is at 2026-08-14. Codex added (48) on the gate's temporal aliasing and Session 25 added (49) on its repair — the only reason a sixth consecutive §16 entry was justified is that (48) told a public reader the gate was broken and stopped there. **Six consecutive entries now describe this review chain. The bar for a seventh is high: it needs to close something, not narrate another round.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories, clones and branches before closeout. Sessions 16–24 worked entirely inside the scratchpad.
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **return them from a reader rather than discarding them.** **1 MiB blocks transfer far less than the 4 MiB default** for scattered header reads.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py` (`read_electrode_table`, `contiguous_band` → `depth_lo_um`/`depth_hi_um` in `rel_y`), `anatomy_index.py` (Codex's; pass `--legacy-index-target CA1 --legacy-index-max-gap-um 40` for the existing index, or it *refuses* to extend it), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels` (opt-in derived layer), `band_drift`.
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` modules need no numbered step — **and a new script dropped into `scripts/` without a README step is a hard checker failure.** **After editing either the packet runbook or any script's docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.** Its harness is in `agents/Claude/tools/`. **Invariants: one step per script, one `bash` fence per step, one line in that fence, one indented line per `Example` block, contiguous unique step numbers.**
- **Scripts must not print non-ASCII.** This console's stdout is cp1252 — even a `print` of a path can crash if it carries a µ, and a one-liner that prints a `≥` from a file will crash too. Docstrings are fine; `print` is not. **`test_band_drift.py` is verified at zero non-ASCII characters anywhere, and is now at 96 checks.** **The sheets use straight quotes only** — verify with Python, not `grep`. The host-selection document still carries **eight** curly quotes and no CRLF: four pre-existing in §§1 and 5's approved region, four Codex introduced in Draft 19's status line and now sitting in a superseded-status line, deliberately left alone. Verified again at Draft 23.
- **Line endings are pinned by `.gitattributes` and a clone reproduces the working tree exactly.** `* -text`, with `text eol=crlf` for 17 non-packet framework files and Codex's 11 legacy packet outputs. **`agents/Claude/README.md` is CRLF and must stay CRLF** (149/149 as of Session 24); the root `README.md` and the selection document are LF; the active chat transcript is genuinely mixed (first 107 lines CRLF, rest LF) and is stored that way. A pattern edit over a CRLF file must preserve `\r\n` in the match string, or it will match nothing — **matching a substring inside one line is the safe way to edit a CRLF file.**
- **A clone is not a copy** — but the two now agree. Verify a distribution claim by cloning to a short path (`C:/Users/cresp/AppData/Local/Temp/ct`; the scratchpad path is too long for git), comparing file by file, and **deleting the clone and any temp branch afterwards.** The trick for an uncommitted state: `git add -A`, `git write-tree`, `git commit-tree`, `git branch -f tmp-verify <sha>`, clone `--branch tmp-verify`, then `git branch -D tmp-verify`.
- **The resumable/pinned result files are tracked deliberately.** **Both** `.gitignore` files carry a do-not-catch-these comment.
- **The processed NWB units table is rich** — 31 described columns, and **`results/amplitude_conventions.json` already holds every column's `description` under `descriptions/`.** Read the description before using a column. **`spike_times`' description names no time origin** — which is why §16.4 pins the clock from the converter instead.
- **`results/host_timing_index.jsonl` holds more than it was written for.** Assume the same of the other recorded indices before downloading anything new.
- **`agents/Claude/tools/` holds one recorded output**, `source_count_granularity_probe_2026-08-13.txt`, because the matching rule cites its numbers. Re-running the probe against the pinned snapshot must reproduce it. **The script needs `--cache "Reproducibility Packet/results/templates_snapshot_2026-08-11.csv"`; it has no default.** A shell redirect adds CRLF — compare normalized, or use its `--out`.
- **`test_band_drift.py` takes `--permutations` only** (no `--module`); **`probe_band_drift_claims.py` takes `--module`**; **Codex's `probe_draft16_safety_claims.py` takes `--repo-root` and `--threshold-um` and needs neither.** Read the parser before inventing a flag.
- **Git history is a verification tool, not just a record.** Session 24 checked Codex's "identical syntax trees" claim by pulling the prior module out of commit `2dfff44` with `git show '<sha>:<path>'` and comparing directly. Prior sessions' exact states are all recoverable this way.
