# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 26 · 2026-08-15 01:24 PDT**
**Next session is Claude Session 27. No count-based progress report is due** (the next is Session 32). A phase transition or an approved amendment written in your session would trigger one anyway.

## 0. ⚠️ THE REVIEW METHOD — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**. Reviewers apply **mechanical** corrections directly; substantive ones are findings for the owner.

***Convergence in place of escalation* is agreed, written into the playbook, and binding.** `Escalated` is no longer an outcome; the outcomes are **Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required**. At either trigger (a second LATE-BLOCKER or any new blocker after Round 2; or the third round-trip without both approvals) the disputed state freezes and the agents run **one agent-only Convergence Decision**: each writes, once, the minimum claim it thinks can ship, the evidence that controls, the strongest evidence against its own position, and one acceptable safe disposition. **Evidence determines what may ship; consensus determines what happens next. Underdetermined evidence is not resolved in favour of approval.** The card closes at a disposition, the owner repairs **outside** review, and may open **one** successor card with a `Supersedes:` line; **a second like-for-like successor is not allowed** — the work must be split or redesigned first. Codex accepted both of my recorded applications: the Convergence Decision is written into the Review Card, and director-only questions (licence, outside contact, spend, Claim Sheet amendment) keep their non-blocking `director_requests.md` channel without becoming review outcomes.

**Three readings remain in the playbook's operating notes and Codex has agreed to all three:** approval stays explicit and state-specific; an unchanged sentence made false by a change elsewhere **is** a regression introduced by the response and so is in scope after Round 1; and a LATE-BLOCKER created by an earlier repair says so.

**Feedback on the method stays an open obligation** in `chats/Claude-Codex-Human/Review Method Change/` — Randy asked for it and asked that the chat stay active. Session 26 posted three observations there (§9.57).

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six.

**⚠️ This file describes the moment it was written.** Codex has now five times posted a handoff within the hour after a session closed. **Read the active chats before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, no candidate has been measured on any open gate, and nothing beyond bounded metadata reads has been downloaded.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 24, `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09`.** §1–§15 same-state approved. §16 is the RC-001 **Round-3** candidate. **Open on Codex.** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **`eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` — open on Codex.** Session 26 changed **only its module docstring**, proved by an AST comparison against the Session 25 state. |
| `agents/Claude/tools/test_band_drift.py` | **`946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` — open on Codex.** **103 checks, 0 failed** at the pinned 200 permutations, 48 s. |
| `agents/Claude/tools/probe_band_drift_claims.py` | **`4f3b83773156e7f9654f3e080d5adb258658cf500cf741aaea04b5015f07c34f` — same-state approved. Closed and unchanged.** 3 of 3 probes pass. |
| `agents/Codex/tools/probe_draft16_safety_claims.py` | **`d1c9220dc0f0890744d920638210f501abdc9b53b84256ef89afbc59e6bca6ac`** — Codex's, re-pinned by him after Session 25. Digits `7.966`/`8.346 µm` and `27.273`/`11.591 µm` reproduce. **His; do not edit it.** |
| `agents/Codex/tools/probe_rc001_round1.py` | **`a29144e247ec5a845bb67699b9e8f5d6a4c89ab3d5458743254e2f223dae33cc`.** Codex's independent probe, now 12 checks. Takes `--repo-root`. **0 failures at Session 26.** Run it; do not read its report. |
| `.gitattributes` | **`036c696c3e1ea9cef70925ec8dfedc407ef59bb20e5c00e17ef9b5f88855bfa0` — same-state approved. Closed.** |
| `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` | **Draft 6, `51adae4b…` — same-state approved. Its chat is concluded.** |
| `Reproducibility Packet/` | Eleven numbered-step scripts plus the checker, `DATA.md`, pinned deps, its own `.gitignore`, and `scripts/utils/band_drift.py`. Runbook checker green at ten steps. |

## 2. The first thing to do next session

**Check the active chats before assuming anything. As of writing, everything open is open on Codex and nothing is open on you.**

- `chats/Claude-Codex/Tier A Selection Section 16 Review/` — **the live review, governed by `Review Cards/RC-001 Tier A Selection Section 16.md`.** **Round 1 (Codex, S24) returned three findings. Round 2 (my S25 response) accepted all three; Codex's Round-2 verification confirmed them and returned one blocking response regression, F1-R1. Round 3 (my S26 response) accepted F1-R1 and returned Draft 24 plus two changed implementation states. Round 3 is open on Codex, delta-only, and is the THIRD AND FINAL ROUND-TRIP.** If it does not close with both agents approving the same state, run the **agent-only Convergence Decision** — not a request to Randy.
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active.**
- `chats/Claude-Codex/Tier A Selection Review/` · `Tier A Donor Matching Rule/` · `Reproducibility Packet Review/` — **concluded.**

**If RC-001 closes as Approved, your lane is the archive-reading drift script** (§5.2) — and it gets **its own Review Card** before Codex reviews it. **Until RC-001 closes, do not measure a candidate and do not read one.** You may write, but not run, the archive reader.

## 3. What Session 26 did

**Owner Round-3 response to Codex's RC-001 Round 2. The one blocking finding accepted, not disputed, and his counterexample reproduced and strengthened before anything was edited.**

### 3.1 RC-001-F1-R1 — my own Draft 23 repair created a false general claim

Draft 23 declared: *a displacement moving fewer than half of a bin's spikes leaves that bin's median exactly where it was*, published as `0.000`/`15.000`/`30.000 µm` below, at and above one half. **That is the behaviour of the equal-baseline fixture it was measured on — every spike in a bin sharing one depth — and not a property of sample medians.**

Codex's counterexample: ordinary bins holding `[0 × 49, 1 × 2, 100 × 49]`; displacing the first 49% by `+30 µm` moves the bin median `1 → 30` and the shipped utility reports **`Delta_10min = 29.000 µm`**, above the strict gate. **Reproduced here, and it is stronger than he reported:** the same fixture gives `29.000 µm` at 30%, 10% and **2%**, and a **single displaced spike in a hundred** moves that bin's median **`14.500 µm`**. There is no fraction at which that fixture is blind, so the cutoff was not misplaced — a cutoff of that shape does not exist.

### 3.2 The repair — a bound, not a cutoff

- A median tracks rank: displacing `k` of a bin's `n` spikes **upward** carries the median toward the depths sitting `k` ranks above it, so the move is **at most the displacement itself and at most that rank distance**. Verified at **zero violations and no negative move over 4,000 random cases across four depth families**.
- The equal-baseline sweep is **retained and explicitly scoped to its own fixture** — it is the corner where the rank distance is zero.
- **Episode placement matters because the grid fixes `k`:** the same displaced spikes read `30.000 µm` inside one bin and `0.000 µm` split across two.
- **The downward case is the same statement read the other way** (negating depths negates the median) and is **measured**, not assumed: same `29.000 µm`.
- **Conclusion, both directions:** the gate has **no guaranteed resolution below the bin width** — `Delta_10min` is not a bound on sub-minute motion and is **not reliably blind to it either**.

### 3.3 The one-way claim was withdrawn, not re-derived

Draft 23 called the blindness permissive — *"it can only understate drift, never invent it."* With no universal blindness there is nothing to call permissive. **I could have re-armed it on the new bound and chose not to.** §16.4 now names both live outcomes and calls neither a safety property: an episode the medians do not express **passes a candidate the gate did not actually clear**; one they express in full **rejects a candidate over motion that is not sustained drift**. **Sixth one-way claim this chain has caught, third of mine.**

### 3.4 All four restatements repaired

§16.4, the document status line, §16.8's Draft 23 note, and the module docstring. The §16.4 fixture roll-call moved **eight → nine**.

### 3.5 The estimator's behaviour did not move, and that is proved

`git show HEAD:'Reproducibility Packet/scripts/utils/band_drift.py'` recovers the Round-2 state `4ac9fa56…`; parsing both states, stripping every module/function/class docstring and dumping the syntax trees gives an **exact string match**. No parameter, threshold, seed, verdict path, error string, return key or numerical branch differs.

### 3.6 Everything re-run

Harness **103/0**; claim probes **3/3**; **Codex's** `probe_rc001_round1.py --repo-root .` **0 failures / 12 checks**; **Codex's** `probe_draft16_safety_claims.py --repo-root .` digits unchanged; packet runbook **10/10**; 0 non-ASCII in both code files; document still exactly **8** curly quotes, LF throughout.

## 4. The estimator, as it stands — open on Codex, do not extend

`Reproducibility Packet/scripts/utils/band_drift.py`, `eace4cd3…`. **Behaviour is byte-identical to the Session 25 state; only the docstring changed.** Public surface unchanged: `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** The symbol in the prose is `Delta_10min`. **The return keys did not change**: band excursion keys are still `delta_full` / `delta_window` / `window_start`, and `apply_gate` still returns **`passed`** (not `passes`).
- `measure_band_drift` returns `measurable` plus, when False, a `reason` **naming the cause**; when True it also returns **six** per-unit audit lists aligned with `included`: `unit_delta_full`, `unit_delta_max_window`, `unit_max_window_start`, `unit_max_window_defined_bins`, `unit_delta_band_window`, `unit_band_window_defined_bins`. Keep all of them. **`delta_max_window` is the *per-unit* list's name; the band's is `delta_window`.**
- `unit_excursions` returns `None` for a windowed value with fewer than two defined bin medians in its span — **never zero**. Ties resolve to the earliest window, in both it and `excursions`.
- `permutation_null` **raises** on an unmeasurable observation, on malformed unit collections and on duplicate/negative/non-integer row indices. Caller order: measure → if measurable → null → gate. **Its seeds derive from the asset id and probe strings you pass.** Signature: `(spike_times, depths, extent_s, asset_id, probe, unit_row_indices, params=None)` — it does **not** take the observation.
- `complete_bins(extent_s)` returns `(n_bins, discarded_s)` and **anchors at 0**; `bin_offsets` builds edges as `arange(n_bins+1)*60`, so **spike times below zero fall outside every bin and are silently excluded** — §16.4 requires that count reported. **The CLI passes `t_last_s`.**
- **A recording needs at least 11 analysed bins.** Candidates carry 54–87 bins, so this binds only on fixtures.
- The full 200-permutation null on a 14-unit, 61-bin synthetic band takes **3.4 s**; the whole 103-check harness takes **48 s**. Never argue the permutation count on runtime grounds.
- It is in `utils/` because the checker walks `scripts/` **non-recursively**. The archive-reading CLI becomes step 11 **only once it has actually been executed**.
- **The harness helper `common_signal_band` now takes `within_bin_offsets` (a per-bin depth distribution) and `episodes` (a list, for episodes split across bins).** Both default to the previous behaviour; `episode` and `episodes` are mutually exclusive.

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

**And it must report, not just check:** the two endpoint-slack values, `n_bins`, `discarded_s`, `head_partial_s`, spikes before the grid origin, band unit count, units surviving the inclusion rule, per-set total/`good` counts with row identifiers and stored labels, **and all six per-unit audit lists — from `unit_traces`/`unit_excursions`, never from a second centring of its own.**

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
- **The drift gate is two numbers, not one.** `Delta_10min <= L` **and** `Q95_null <= L`. **The gate window is ELEVEN 60 s bins, not ten** — ten bin medians span only nine minutes between the extremes and an off-grid 600 s segment touches eleven bins, so ten was permissive in two independent ways (S25/RC-001-F1). Widening is monotone and can only reject more. Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those are input errors that pause the pinned order (§16.4).
- **⚠️ SUB-BIN RESOLUTION — the S25 statement was WRONG and S26 replaced it (RC-001-F1-R1).** There is **no half-of-a-bin's-spikes cutoff.** `0.000`/`15.000`/`30.000 µm` describes the **equal-baseline fixture** only. A median tracks rank, so displacing `k` of a bin's `n` spikes upward moves its median **at most the displacement itself and at most the distance to the depth `k` ranks above it** (0 violations, 4,000 random cases, four depth families). On a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`, and 2% of them moves it `29.000 µm` — above the gate. Grid placement matters because it fixes `k`: `30.000 µm` in one bin, `0.000 µm` split across two. **The gate has no guaranteed resolution below the bin width in either direction — it neither bounds sub-minute motion nor is reliably blind to it. The old "permissive" claim is WITHDRAWN and must not be re-derived on the new bound.**
- **The drift unit set is blind to `kilosort2_label`** and is selected by valid same-probe `max_electrode -> rel_y` inside the band. **That choice carries no one-way safety guarantee** — the result is *conditional* on movement being expressed in enough traces. `distance_from_probe_tip_um` selects nothing; per-spike depths enter only the centred within-unit steps.
- **The per-unit excursions are reported and never consumed, they carry no null, and they do not discharge that conditional in either direction.** `Q95_null` grades a median across units and has **no fixed ordering** against a single trace — narrower on homogeneous fixtures (1.6× to 2.8×), wider on a heterogeneous one, and the reversal does not need an exactly-flat unit (6 µm against 18 µm suffices). **Never compare a per-unit value to `Q95_null` or to `L`.** **Neither the concentration nor the scatter of `unit_max_window_start` is evidence.** **And the absence of magnitude separation is not evidence either:** a fixture inside the declared parameters passes both gate numbers with **twenty of forty-one** units genuinely moving 30 µm and no separation visible (`14.941`/`7.125 µm`, moving `[32.5, 57.0]` overlapping stationary `[20.9, 37.6] µm`). **The claim that masking strengthens with band size is WITHDRAWN (S25/RC-001-F2)** — 35 of 120 seeds break it at a fixed 40% moving fraction. The band statistic has **no fixed direction in the unit count**.
- **The bin grid anchors at session `t = 0` with extent `t_last_s`**, on pinned converter provenance. **`duration_s` is a span and is not an alternative clock hypothesis.** Endpoint containment is a consistency check that cannot identify a clock, and its margins are **endpoint slack** that bounds nothing internal.
- **The head bin is retained and reported, with no claimed direction.** Confined to rank 1 at 1.9% of one bin in 72.
- **The permutation pool is analysed-bin spikes only**, for both observation and null. Partial-bin depths and pre-origin depths enter neither.
- **`cumulative_drift_um_per_hour` is retired on its own description** — a path length, spike-count-correlated at ~0.79, and "NOT actual electrode displacement" in IBL's words.
- **Amendment 6 governs: Tier A is parameterized by `N`**, the zone donors surviving the **per-donor** host gates. `10 ≤ N ≤ 16` continues; `N < 10` is Slot 12.3. Fifty occurrences split `q = ⌊50/N⌋`, `r = 50 mod N`. Control arm and both pseudo-arms follow `N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.**
- **`N ≥ 10` is structural:** `16 − 6 = 10` = the injected-unit count Slot 7 fixes.
- **The manipulation check is a hard stop-or-go gate**, and the realized zone-donor count is a *composition-integrity* quantity, **not** a substitute for it.
- **Amendment 5:** the injection zone's donors are removed from the **real** region-unaware arm before matching. The frozen matching rule runs as a non-generating counterfactual on **both** the un-removed and post-removal pools, with only the post-removal state permitted to govern generation. The rule is fixed **before** the eligible pool is visible and may contain no region term in either direction.
- **The matching rule's provenance test is two-level:** **Level A** matches distinct dataset, session *and* subject counts (`S_T`, `E_T`, `B_T`); **Level B** is the contract's literal `S_T` floor. A stage tries A, then B, and only relaxes when both fail. **Level A binds only at stages 3 and 4.**
- **Before any real target manifest, host-specific pool or edge table exists**, the exposure-schedule/placement specification, the matcher implementation, exhaustive synthetic tests and same-state implementation approval must all be complete. All four steps.
- **0.11 and 0.12 are two sampling models, not two estimates of one number.** Blocked expectations are **1.03** (exact-insertion) and **1.17** (caliper). **Historical diagnostics at sixteen**, never predictions.
- **CA1's sixteen donors sit in exactly 4 source datasets, `[6, 5, 3, 2]`, which are 4 sessions and 4 animals** — subjects KS044/KS046/KS051/KS055. Library-wide: **37 insertions, 24 sessions, 12 animals**; of 66,045 four-source subsets only 37,424 span four animals and 74 span one.
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
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim and the "protocol versions differ" self-contradiction; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity when they are enrichment; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort rather than a floor; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token when it is the insertion identifier; the master-seed requirement that left its derivation and stream mapping to a later configuration; the inside-null rejection that would have failed the quietest possible host; "both net displacements" for a max-minus-min range; the claim that sub-pitch motion is below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins while claiming to preserve bin counts; one additive-ramp fixture promoted into a general monotonicity proof for the null's bias; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser and a median residual as a coordinate-equivalence test; the two Draft 16 guarantees Codex blocked in S21; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower" than a single trace; **and S25's half-of-a-bin's-spikes cutoff, which was one fixture's behaviour published as a property of medians.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5). **S16–S22: six sessions running where the thing needed was already on disk. S23: already *computed*. S24: already *stated*.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5). **S17 inversion: for a host gate, pessimistic *is* the safe direction. S18 re-inversion: only for a genuinely absent measurement. S19: when a *proof* is withdrawn, ask what the unsafe direction now costs.**
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **Reviewer's version: review it against the contract, not against your own last draft** (S16). **S18–S26: running the pass anyway on edits you already agree with is what produces the extra findings.**
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and backslash escapes*** — write the text with the Write tool and have Python read it in. **`$VAR` does not expand inside the Bash tool's `-c` string passed to python**; pass the path as `argv`. **`.\venv\Scripts\python.exe` does not survive the Bash tool either — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7). **S19–S24: each repair creates the next layer's gap; ask what the repair now obliges. S26 is the inverse and the harder case: my S25 repair created a *new false claim* rather than a gap, because I described a real measurement in words wider than the measurement.**
8. **A measurement you just made is not a threshold you get to set** (S7). The threshold *and its relaxation ladder* get written before the first measurement (S17), and the ladder has to say whether it re-runs the whole order or only the candidate in hand (S18).
9. **Read a rich first-party table, not one column of it** (S7). Read the column's own `description` too.
10. **Verify a name before trusting it** (S7). **S22–S23: when the other agent hands you a probe and its output, run the probe. S24: when they hand you a *proof*, re-run that too. S26: when they hand you a *counterexample*, rebuild it from the description rather than running only their script — rebuilding is what showed it was stronger than reported.**
11. **Two numbers in the same unit are not the same quantity** (S8); **two numbers that are the same quantity under different sampling models are also not the same number** (S11). **S23–S24: a median across units and one unit's excursion are not on the same scale, and their ordering is not fixed.**
12. **When a safety check fires, measure it before loosening it** (S8). **S19 inverse: when a cost is cited for *not* doing something, measure the cost.**
13. **A correction is worth logging even when the conclusion survives** (S8).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9); a *better* reason arriving is also that moment (S15).
16. **An audit must use the same key its lookup uses** (S9).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10). Twelve for twelve now.
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17). **S23: when it does not survive, the counterexample becomes a permanent case.**
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11).
24. **Note which direction a correction pushes** (S11), including when it makes your own next step harder (S15, S16). **S22–S23: when you claim a repair changed no numerical branch, prove it mechanically. S26: the cheapest proof after "touch nothing" is an AST comparison with docstrings stripped — it converts "only the docstring changed" from a promise into a check.**
25. **When a test fails, first ask whether the test or the artifact is broken** (S11). **S19: `apply_gate` returns `passed`, not `passes`. S24: `measure_band_drift` returns `delta_window`, not `delta_max_window`. S26: `probe_rc001_round1.py` takes `--repo-root` and errors without it — read the parser.**
26. **Render the output; do not read the source and assume you know what it prints** (S12). **Read the finished section back as a reviewer** (S16, S18–S26). **S26: it caught a number in the status line that still said "one tenth" after the evidence had been strengthened to "one fiftieth and a single spike", and a bound stated without naming which displacement direction it covered. Seven consecutive sessions where the read-back pass produced the last corrections.**
27. **Test a checker by breaking things, one breakage per clean copy** (S12). **S18: turn each defect review caught into a permanent test case. S22–S26: when a counterexample lives only in a review probe or a scratch file, move it into the harness — S26 moved Codex's heterogeneous fixture in and extended it down to a single spike.**
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16). **S26: and the *fixture* behind it is the thing least likely to be interrogated at all.**
31. **A supersession can be too broad as well as too narrow** (S14).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17). **S23–S24: and whether the repair needs machinery at all. S26 is the counter-case: it *did* need one small piece — a bound — because "it depends on the distribution" without saying what determines it would have invited the next finding.**
33. **Make an edit script assert exactly one match per replacement** (S14). Validate every replacement across every file *before* writing any of them.
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Ten for ten (S15–S23).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17). **S24: when the finding is that a claim is too strong, edit the claim. S26: and edit every restatement of it in the same pass — the cutoff sat in four places, and the paragraph Codex quoted was only one.**
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S24: a null built for one statistic has no ordering against another.**
41. **Read the clock at the moment you write the timestamp** (S17).
42. **A status sentence doing a rule's job goes stale in the permissive direction** (S18). **S24: a diagnostic with no stated null result is read as reassurance.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20).
46. **State a check's *resolution*, not only its role** (S21) — **and S22's correction: only when the check actually has one. S26: and when you state one, state what it is a resolution *of*. "Blind below half a bin's spikes" named a resolution the estimator does not have.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22). **S25: the fifth — check that the thing you are holding fixed is actually fixed. S26: the sixth, and the different one. The first five were directions asserted past their evidence; this one was a *boundary* asserted past its fixture. Same class, different tell: not "is the trend real?" but "is the fixture representative of the object I am describing?"**
49. **Renaming is load-bearing only when the name invites a wrong value** (S22).
50. **A counterexample built on a degenerate case invites dismissal** (S24). **When you accept someone's counterexample, check whether it needs its extreme case. S26 is the mirror: check whether it is *stronger* than claimed. Codex reported 49%; the fixture has no blind fraction at all, and a single spike in a hundred moves the median 14.5 µm. Repairing only what was reported would have left the cutoff in place at a lower number — the same error again.**
51. **A near-miss is not the finding** (S24). Sweep the parameters to establish the regime exists.
52. **A test can encode the defect it was written to catch** (S25). **A harness written from the implementation confirms the implementation.** Assert against the quantity's stated purpose.
53. **Two independent errors can cost the same amount and coincide exactly** (S25). Check the covering property directly.
54. **A tightening is affordable exactly once: before the first measurement** (S25). This is the concrete payoff of writing thresholds before data.
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25). Re-run every fixture whose claim depends on the changed verdict.
56. **Which fixture a published number came from is part of the number** (S25). **S26 generalizes it: a fixture is not just provenance for a number, it is the *scope* of every sentence built on it. An equal-baseline point mass is a degenerate input for a rank statistic — every value identical means every order statistic identical — so it was the worst possible fixture from which to describe what a median does, and that was visible without the counterexample. Before writing a general sentence from a fixture, ask what the fixture makes degenerate.**
57. **Method note (S26, for the Review Method Change chat).** Three observations posted to Randy: delta-only review is *sharper* than full review on repairs, because it concentrates attention exactly where the risk was created — both findings this card produced came from reading the artifact against its stated purpose rather than against the previous draft; **the three-round-trip limit changed how I wrote the response**, because knowing Round 3 was the last one is why I swept the counterexample down to a single spike instead of repairing what was reported; and the honest cost is three of my sessions and three of Codex's on one section, with the Convergence Decision existing precisely so it cannot continue past three.

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Last reading: 2026-08-15 01:10 PDT — RAM 0.96 GiB free of 31.67 (97% in use); VRAM 1,086 MiB used of 16,311; 590.6 GB free on `C:`.** **This is the tightest reading any session here has recorded, and it is two hours after Session 25 measured 7.57 GiB free.** The 48-second numpy harness needs tens of megabytes and ran fine; **nothing needing gigabytes could have started at that moment.** **Do not inherit it; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. `band_drift.py` needs numpy and stdlib `hashlib` only. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64` seeded from a 64-bit integer; a numpy change is a replay risk and the drift result must be re-replayed after one.** Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

## 11. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins** and both agents append the round log and the outcome to it. A card scopes a review; **it does not amend the Claim Sheet**.
- **`Playbooks/review-cycle.md` is two documents in one file:** a superseding method at the top and the retained superseded cycle below it. **Read the top section; do not reach below it to fill a gap** without saying so in the review's own chat.
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session. Sync is of content, not of words.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **The root README's running log is lean and append-only.** The banner's "Last updated" is the one line that may be overwritten. **The log stands at 49 entries; the banner is at 2026-08-14. Session 26 deliberately added nothing** — six consecutive entries already describe this review chain, and a seventh should be the one that says the chain **closed**, not another round. **If RC-001 closes next session, that is the entry to write.**
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories, clones and branches before closeout. Sessions 16–26 worked entirely inside the scratchpad.
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **return them from a reader rather than discarding them.** **1 MiB blocks transfer far less than the 4 MiB default** for scattered header reads.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py` (`read_electrode_table`, `contiguous_band` → `depth_lo_um`/`depth_hi_um` in `rel_y`), `anatomy_index.py` (Codex's; pass `--legacy-index-target CA1 --legacy-index-max-gap-um 40` for the existing index, or it *refuses* to extend it), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels` (opt-in derived layer), `band_drift`.
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` modules need no numbered step — **and a new script dropped into `scripts/` without a README step is a hard checker failure.** **After editing either the packet runbook or any script's docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.**
- **Scripts must not print non-ASCII.** This console's stdout is cp1252. Docstrings are fine; `print` is not. **`test_band_drift.py` is verified at zero non-ASCII characters anywhere, and is now at 103 checks.** **The sheets use straight quotes only** — verify with Python, not `grep`. The host-selection document still carries **eight** curly quotes and no CRLF; verified again at Draft 24.
- **Line endings are pinned by `.gitattributes`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (154/154 as of Session 26); the root `README.md` and the selection document are LF; the §16 review transcript is genuinely mixed (first 107 lines CRLF, rest LF) and is stored that way. **A pattern edit over a CRLF file must preserve `\r\n` in the match string** — matching a substring inside one line is the safe way, and an edit script should assert the CRLF count equals the newline count after editing.
- **A clone is not a copy** — verify a distribution claim by cloning to a short path (`C:/Users/cresp/AppData/Local/Temp/ct`; the scratchpad path is too long for git), comparing file by file, and **deleting the clone and any temp branch afterwards.**
- **The resumable/pinned result files are tracked deliberately.** **Both** `.gitignore` files carry a do-not-catch-these comment.
- **The processed NWB units table is rich** — 31 described columns, and **`results/amplitude_conventions.json` already holds every column's `description` under `descriptions/`.** **`spike_times`' description names no time origin** — which is why §16.4 pins the clock from the converter instead.
- **`results/host_timing_index.jsonl` holds more than it was written for.** Assume the same of the other recorded indices before downloading anything new.
- **`agents/Claude/tools/` holds one recorded output**, `source_count_granularity_probe_2026-08-13.txt`, because the matching rule cites its numbers. **The script needs `--cache "Reproducibility Packet/results/templates_snapshot_2026-08-11.csv"`; it has no default.**
- **Read the parser before inventing a flag.** `test_band_drift.py` takes `--permutations` only; `probe_band_drift_claims.py` takes `--module`; **both of Codex's probes take `--repo-root` and `probe_rc001_round1.py` requires it**; `probe_draft16_safety_claims.py` also takes `--threshold-um`.
- **Git history is a verification tool, not just a record.** `git show '<sha>:<path>'` recovers any prior exact state — Session 24 used it to check an AST claim, and Session 26 used it to *make* one.
