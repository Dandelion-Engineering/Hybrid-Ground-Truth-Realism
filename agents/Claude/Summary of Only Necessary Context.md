# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 21 · 2026-08-14 03:19 PDT**
**Next session is Claude Session 22. No count-based progress report is due** (next is Session 24). A phase transition or an approved amendment written in your session still triggers one.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six.

**⚠️ This file describes the moment it was written.** Codex has more than once posted a handoff within the hour after a session closed. **Read the active chat before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, no candidate has been measured on any open gate, and nothing beyond bounded metadata reads has been downloaded.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 16, `7fed750c8f48420521e2038b32285d72d7b719dfd1490c40dbccc14a6e2204ec`.** §1–§15 same-state approved by both. §16 differs from Codex's approved Draft 15 by three precision repairs (label-blind unit set in §16.4 + a §16.7 table row; the head partial bin in §16.4; containment's resolution and the measured timebase split in §16.4; §16.8's reporting list extended) and the status line — and by nothing else. **Open on Codex.** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **`d8b035968416b335d7ef1bdd0d915c03aec4a64649defa8795c8c013fc70c069` — same-state approved. Closed.** |
| `agents/Claude/tools/test_band_drift.py` | **`82aaf77e99f20b158a54b6acfc848fc2626047aa350bebd8b3bd988b7ce48f03` — same-state approved. Closed.** 57 checks, 0 failed, at the pinned 200 permutations. |
| `agents/Claude/tools/probe_band_drift_claims.py` | **`4f3b83773156e7f9654f3e080d5adb258658cf500cf741aaea04b5015f07c34f` — same-state approved. Closed.** 3 of 3 probes pass. |
| `.gitattributes` | **`036c696c3e1ea9cef70925ec8dfedc407ef59bb20e5c00e17ef9b5f88855bfa0` — same-state approved. Closed.** Repository-wide byte preservation. |
| `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` | **Draft 6, `51adae4b…` — same-state approved. Its chat is concluded.** |
| `Reproducibility Packet/` | Eleven numbered-step scripts plus the checker, `DATA.md`, pinned deps, its own `.gitignore`, and `scripts/utils/band_drift.py`. Runbook checker green at ten steps. |

## 2. The first thing to do next session

**Check the active chat before assuming anything. As of writing, everything open is open on Codex and nothing is open on you.**

- `chats/Claude-Codex/Tier A Selection Review/` — **open on Codex:** Draft 16's exact bytes. Nothing else is open in it.
- `chats/Claude-Codex/Tier A Donor Matching Rule/` — **concluded.** Implementation review starts a new scoped chat.
- `chats/Claude-Codex/Reproducibility Packet Review/` — **concluded.** Later packet additions start a new scoped chat.

**If Draft 16 has come back approved, your lane is the archive-reading drift script** (§5.2) — write it, review it, and only then measure rank 1. **If it has not, do not measure a candidate and do not read one.** You may write, but not run, the archive reader; and note that Sessions 20 and 21 both declined to start it because the specification was still moving under it. §16 has now taken six review round-trips. If Draft 16 comes back with new blocking findings rather than approval, that is the point to consider whether the *specific* remaining disagreement should go to Randy under the playbook's two-round-trip rule — but only a genuine disagreement, which none of Sessions 19–21's findings were.

## 3. What Session 21 did

**Owner re-review of Codex's Draft 15. Accepted both of his blocking corrections in full and kept his repairs exactly as written, then handed back Draft 16 with three additions — none of them a disagreement with Draft 15.**

### 3.1 Accepted from Codex, kept exactly as written — and why he was right

1. **Endpoint containment cannot identify a clock.** My Draft 14 sentence — *"under one bin it escapes both and moves nothing a 60 s grid can see"* — conflated **the total extent differing by less than one bin** with **each spike moving less than one bin.** Those are the same statement for a pure offset and are *not* the same for a scale error, which accumulates along the recording: an affine compression can leave `n_bins` untouched while moving spikes across internal boundaries, changing bin medians, the window excursion and the permutation pool. **Do not revive endpoint-based clock inference.**
2. **A median residual cannot establish coordinate equivalence.** It constrains location and nothing else. Codex's replacement is better than my proposal because it removes the second coordinate entirely: band membership uses `max_electrode -> rel_y`, the coordinate the band's bounds are already written in.

**The grid is now pinned from first-party conversion provenance**, not inference: DANDI 000409 names `catalystneuro/IBL-to-nwb`; at commit `54030ac4eb40a74978ac1f6ef6e966278b9d3f34` the raw converter aligns AP samples with `SpikeSortingLoader.samples2times`, the sorting export carries IBL `spikes.times` through unchanged, and the docs define that field as **seconds from session start**. So: **anchor = session zero, extent = `t_last_s`, and `duration_s` is a span that the estimator does not consume.** Containment survives as a consistency check only. **I accepted that provenance on Codex's reading and did not fetch the repository myself** — `references.md` records it at that strength.

Re-ran rather than read: **3 of 3 probes, 57 checks / 0 failed at 200 permutations, runbook checker green at ten steps.**

### 3.2 Finding A — the unit set was never pinned, and one reading disqualifies rank 9 by construction

§16.4 says the unit set is the same membership rule `screen_injection_placement.py` used for §10's native band yields. **True of the rule, silent on the filter.** The units table carries `kilosort2_label`; §10 reported band counts *both ways* and §10.3 gave them different interpretive jobs.

**Measured from `injection_placement_CA1.json` across the thirteen candidates: 22–267 band units, but only 1–60 labelled `good`, and six of thirteen hold ≤13.** NYU-39 Probe00 (rank 9) holds **one**. §16.7 requires five included units in *every* complete bin, so a `good`-only reading makes rank 9 unmeasurable before a spike is read — disqualifying it through the drift gate for exactly the yield reason **§10.4 deliberately declined to gate on** — and puts five more candidates in at 8–13 against a floor of five.

**Draft 16 pins it label-blind** (§16.4 point 1 + a new §16.7 table row). Reason: step 5's own — real movement is common to every unit while depth-noise and unit-specific instability are not, so the across-unit median wants more contributors; and the ≥10-spikes-in-≥80%-of-bins rule already removes what cannot carry a displacement, on the property the quantity needs. **It cannot smuggle a pass, and the argument is written down:** the null is built from the *same* unit set, so extra scatter from weaker units widens `Q95_null`, which the candidate must also clear.

### 3.3 Finding B — the head partial bin, named small and kept small

Session-zero anchoring plus tail-bin discarding leaves the head unhandled wherever `t_first_s > 0`: bin 0 spans 60 s of clock but less of recording. **Confined to rank 1** (`t_first_s = 1.138 s` → 58.86 s in bin 0, 1.9% of one bin in 72). Five candidates start at exactly 0.0, seven within `6.4e-5` s.

**The bin is retained**, with the safety argument stated: fewer spikes → noisier bin-0 medians → can only widen the observed excursion, and the null runs over the same bins/counts so it widens `Q95_null` too. Both numbers move toward rejection, never toward a pass. What was missing was the record: the reader reports `head_partial_s = max(t_first_s, 0)` beside `discarded_s`, plus the count of loaded spikes falling before the grid origin (`bin_offsets`' `searchsorted` drops them silently otherwise; one to two samples' worth on the seven negative series).

### 3.4 Finding C — containment's resolution, and a measured split in the raw timebases

Containment can only catch a mismatch big enough to push the earliest or latest spike outside `[t_first_s, t_last_s]`, so **its resolution is the two end margins**, which are never zero on a real recording. Draft 16 requires both reported with the verdict.

Then the measurement that motivated it, from `host_timing_index.jsonl` (on disk since Session 15, never compared against the nominal clock):

- **Five candidate series are exactly nominal** — `t_first_s` exactly `0.0`, `t_last_s` exactly `(n-1)/30000` to the last bit, interval nominal to twelve decimals. All CSHL Probe00, **ranks 3, 6, 8, 10, 11**. Indistinguishable from `arange(n)/30000`.
- **The other eight carry a fitted alignment** — non-zero offset, interval off nominal by up to ~`1e-5` relative, accumulating to **0.5–49 ms** per run. **Rank 1 is here**, at `+1.138489` s and ratio `0.9999987` (−5.8 ms).

**This does not contradict the provenance** — an identity alignment is still an alignment and 49 ms is far inside a 60 s bin. It establishes that the session clock is a claim about the *converter*, not a uniform property of the *arrays*, and that the exactly-nominal series are where containment says least.

## 4. The estimator, as it stands — closed, do not reopen

`Reproducibility Packet/scripts/utils/band_drift.py`, `d8b03596…`. Public surface: `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- `measure_band_drift` returns `measurable` plus, when False, a `reason` **naming the cause**. Keep that.
- `permutation_null` **raises** on an unmeasurable observation, on malformed unit collections and on duplicate/negative/non-integer row indices. Caller order: measure → if measurable → null → gate.
- `apply_gate` returns key **`passed`** (not `passes`), plus `label`, `reason`, `delta_window`, `q95_null`, `threshold_um`, `inside_null`.
- `complete_bins(duration_s)` returns `(n_bins, discarded_s)` and **anchors at 0**; `bin_offsets` builds edges as `arange(n_bins+1)*60`, so **spike times below zero fall outside every bin and are silently excluded** — §16.4 now requires that count reported. **Its docstring still calls the argument "the recording duration in seconds"; the CLI must pass `t_last_s`** (§16.4 pins this — do not read the module as pinning the timebase).
- The full 200-permutation null on a 14-unit, 61-bin synthetic band takes **3.4 s**. Never argue that parameter on runtime grounds.
- It is in `utils/` because the checker walks `scripts/` **non-recursively**. The archive-reading CLI becomes step 11 **only once it has actually been executed**.

## 5. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 5.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Do not re-derive it and do not re-sort it.** Ranks 4–5 outrank rank 3 on channel count deliberately. NYU-39 at rank 9 is deliberate — deprioritized, never disqualified, **and Session 21's Finding A is what keeps it that way.** **Two passes:** the whole order at 20 µm, then — only if nothing clears all five gates — the same order restarted at 40 µm, then the survey continuation in the pinned asset-cache order at 40 µm. **Gate order** (cheapest first; cannot change a verdict, only cost): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

### 5.2 The next piece of work

**The archive-reading script**, which becomes packet step 11. Targeted range reads over the ragged `spike_times` and `spike_distances_from_probe_tip_um` slices for **band units only**, reusing `utils/remote_hdf5` and `utils/host_anatomy`, calling into `utils/band_drift`. Report `n_bytes`/`n_requests` rather than discarding them; 1 MiB blocks beat the 4 MiB default for scattered reads.

**Four things §16.8 requires it to confirm before it computes anything:**

1. the ragged index resolves aligned per-unit `spike_times` / `spike_distances_from_probe_tip_um` slices on these specific assets;
2. those values are finite and the depth column keeps its documented micrometre unit;
3. the exact raw and processed assets satisfy §16.4's **provenance-pinned session clock** and the containment sanity check — **this validates a declared clock, it does not choose one**;
4. every included unit's `max_electrode` resolves unambiguously to a finite `rel_y` **on the same probe** (missing / cross-probe / ambiguous = input error, never a band translation).

**And it must report, not just check:** the two containment margins, `n_bins`, `discarded_s`, `head_partial_s`, spikes before the grid origin, band unit count, and units surviving the inclusion rule.

Layout facts, all confirmed from already-downloaded metadata: the units table carries `spike_times` + `_index`, `spike_distances_from_probe_tip_um` + `_index`, `spike_amplitudes_uV` + index, `probe_name`, `distance_from_probe_tip_um` (per-unit scalar, **not** the selector), `max_electrode`, `electrodes` + `_index`, `kilosort2_label`. `results/host_timing_index.jsonl` carries per-series `t_first_s`, `t_last_s`, `duration_s`, `rate_hz`, `timing_source` — **all twenty-one measured series are `timestamps`**; the `starting_time` branch of `screen_host_timing.py` writes only `n_samples / rate_hz` and records no `t_last_s` and no origin.

### 5.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. Stricter than Draft 7 §10's parameterized sweep. **Do not reopen §1–§14** — it belongs in a future section. **Codex still owns the footprint/placement calibration**; do not start it.

## 6. What is still not done

1. **No host is pinned**, and that is correct.
2. **The archive-reading drift script does not exist** (§5.2). The statistic does and is closed.
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
- **The drift gate is two numbers, not one.** `Delta_10 <= L` **and** `Q95_null <= L`. Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid complete bin, non-finite data, failed deterministic replay. **A clock or coordinate mismatch is not one of them** — those are input errors that pause the pinned order (§16.4).
- **The drift unit set is blind to `kilosort2_label`** (Session 21) and is selected by valid same-probe `max_electrode -> rel_y` inside the band. `distance_from_probe_tip_um` selects nothing; per-spike depths enter only the centred within-unit steps.
- **The bin grid anchors at session `t = 0` with extent `t_last_s`**, on pinned converter provenance. **`duration_s` is a span and is not an alternative clock hypothesis.** Endpoint containment is a consistency check that cannot identify a clock — do not revive it as one.
- **The permutation pool is complete-bin spikes only**, for both observation and null. Partial-bin depths enter neither.
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
- **`validate_ccf_label_map.py` validates the hand-authored core map and the `depth_along_probe`/`rel_y` agreement** — not the derived layer. The tip-distance-versus-`rel_y` question that Session 20 raised is **moot**: Draft 15 removed tip distance from unit selection entirely.
- **The donor library's acronyms sit at mixed levels of the CCF hierarchy**, so "same region" is undefined when one label is a parent of the other. CA1 is a leaf and unaffected; **any zone change must check for parent-labelled donors first**.
- **A one-command-per-side runbook rule is a hard parse error, not a warning.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim and the "protocol versions differ" self-contradiction; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity when they are enrichment; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort rather than a floor; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token when it is the insertion identifier; the master-seed requirement that left its derivation and stream mapping to a later configuration; the inside-null rejection that would have failed the quietest possible host; "both net displacements" for a max-minus-min range; the claim that sub-pitch motion is below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins while claiming to preserve bin counts; one additive-ramp fixture promoted into a general monotonicity proof for the null's bias; "take the length from `t_last_s`, never `duration_s`" — the mirror image of the defect it repaired; **and the two Draft 14 rules Codex blocked in Session 20: endpoint containment as a clock chooser, and a median residual as a coordinate-equivalence test. Both were inference from a statistic that does not constrain the thing being inferred. Do not revive either.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5). **S16: eleven sessions of a weaker-than-intended constraint because a provenance token was counted and never read. S17: the drift replacement existed the whole time in a column description already downloaded. S19–S21: recording that a check came back *empty* is worth as much as recording one that came back full — and S21's biggest finding came out of a JSON file tracked since S15 that nobody had divided by the nominal clock. Four sessions running.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5). **S17 inversion: for a host gate, pessimistic *is* the safe direction. S18 re-inversion: only for a genuinely absent measurement. S19: when a *proof* is withdrawn, ask what the unsafe direction now costs and whether anything bounds it.**
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **Reviewer's version: review it against the contract, not against your own last draft** (S16). **S18–S21: running the pass anyway on edits you already agree with is what produces the extra findings — four sessions running, and in S20 and S21 every finding came from that pass.**
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and backslash escapes*** — write the text with the Write tool and have Python read it in. **`$VAR` does not expand inside the Bash tool's `-c` string passed to python**; pass the path as `argv`. **`.\venv\Scripts\python.exe` does not survive the Bash tool either — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7). **S19: withdrawing an overclaimed proof was right and left the rule's safety argued nowhere.**
8. **A measurement you just made is not a threshold you get to set** (S7). The threshold *and its relaxation ladder* get written before the first measurement (S17), and the ladder has to say whether it re-runs the whole order or only the candidate in hand (S18).
9. **Read a rich first-party table, not one column of it** (S7). Read the column's own `description` too, and check whether you already downloaded it (S15, S17, S19, S21).
10. **Verify a name before trusting it** (S7). **S18: verify a derived constant by re-deriving it, and a round number by finding out what produced it. S20: verify a *field* by reading the code that wrote it. S21: when you accept a source second-hand from the other agent, say so in `references.md` rather than recording it as if you had read it.**
11. **Two numbers in the same unit are not the same quantity** (S8); **two numbers that are the same quantity under different sampling models are also not the same number** (S11). **S19: a *span* is not an *end time*. S20: two depth columns in micrometres are not the same coordinate until someone checks. S21: and two timestamp arrays with the same nominal rate are not built the same way.**
12. **When a safety check fires, measure it before loosening it** (S8). **S19 inverse: when a cost is cited for *not* doing something, measure the cost before accepting it.**
13. **A correction is worth logging even when the conclusion survives** (S8).
14. **Design the measurement so it does not need the fragile step** (S8). **S20's best repair was Codex's, and this is why it was better than mine: it removed the second coordinate rather than bounding the error between two.**
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9); a *better* reason arriving is also that moment (S15).
16. **An audit must use the same key its lookup uses** (S9).
17. **A pessimistic bug announces itself; a silent one does not** (S9). **S18: that is the argument for rejecting on an invalid bin rather than omitting it. S19: loud is not enough if the diagnosis is wrong — under first-admissible a wrong-reason rejection costs the host. S21: and a rejection produced by an unpinned reading of "which units" is exactly that, arriving before the measurement rather than after it.**
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10). Nine for nine now.
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17).
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11). **S18: keep a finished script out of the runbook until it has run. S19: a distribution fix has a *scope* — measure what it does not cover before calling it fixed.**
24. **Note which direction a correction pushes** (S11), including when it makes your own next step harder (S15, S16). **S18: state when a repair cannot cost anything, and prove it. S19–S21: when a repair's effect is nil, measure that and say so — inflating a real finding is its own dishonesty, and S21's head-bin finding is reported at 1.9% of one bin for that reason.**
25. **When a test fails, first ask whether the test or the artifact is broken** (S11). **S18: `grep -c $''` reports no CRLF in a file that is entirely CRLF. S19: `apply_gate` returns `passed`, not `passes`.**
26. **Render the output; do not read the source and assume you know what it prints** (S12). **Read the finished section back as a reviewer** (S16, S18, S19, S20). **S21: reading it back is what caught three loose quantifiers in text I had just written — "close to that floor", a bound quoted at the wrong end, and an inconsistent tolerance figure.**
27. **Test a checker by breaking things, one breakage per clean copy** (S12). **S18: turn each defect review caught into a permanent test case. S19: reproduce the *defect* as well as the fix.**
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13). **S19–S20: "unmeasurable" versus "input error" is that choice one level up. S21: so is "which units" — whenever a validity rule can convert a small set into a rejection, the set's definition is a policy, not a description.**
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16). **S20: and the *quantifier* inside it is the least checked part of that.**
31. **A supersession can be too broad as well as too narrow** (S14). Broaden *and* add the carve-out in the same edit (S15).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17). **S20's inverse: ask whether the scale you need is already pinned somewhere. S21: and whether the check you are adding needs a parameter at all — reporting a margin beats gating on one you cannot yet justify.**
33. **Make an edit script assert exactly one match per replacement** (S14). Validate every replacement across every file *before* writing any of them.
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Threshold at an unpinned measurement point (S15); matching rule over unpinned placements (S16); "first-admissible" over an unpinned order (S17); a null test with no stated summary (S18); a bin grid with unpinned anchor and length (S19); a unit set compared across two depth coordinates never shown to be one (S20); **a unit set whose quality filter was never named (S21)**. Seven for seven. **When you approve a rule, ask what it eats — and ask it again after someone else repairs the rule, because a correct repair can leave a different input exposed.**
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17). **S20: nor does a new paragraph repair the *older* sentence above it.**
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16, S17, S18). **S21's version for a *choice between readings*: show that the reading you pin cannot manufacture a pass. Here the null is computed on the same unit set, so weaker units widen `Q95_null` and cannot buy admission.**
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). **S18: then ask which way its bias points. S19: if you cannot prove the direction, bound what happens when it goes the other way. S20: and state which side of the gate the bound covers.**
41. **Read the clock at the moment you write the timestamp** (S17).
42. **A status sentence doing a rule's job goes stale in the permissive direction** (S18).
43. **A repair can widen the blast radius of a defect somewhere else** (S19). After any repair, ask what else now depends on what it touched.
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20). What caught it was following the rule into its consumer.
46. **State a check's *resolution*, not only its role** (S21). Draft 15 correctly called containment a sanity check; a sanity check whose sensitivity is unstated is still an unpinned input. The fix was to report the margins, not to invent a threshold for them.
47. **An error of inference does not become sound by being made more carefully** (S21). Both rules Codex blocked were attempts to infer a fact from a statistic that does not constrain it. The repair in both cases was to find a source that *states* the fact, or to remove the need for it.

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). The old low-memory series was leaked Claude automation processes, not competing research; **do not reason from its shape.** Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Last reading: 2026-08-14 03:15 PDT — RAM 6.79 GiB free of 31.67; VRAM 1,089 MiB used of 16,311; 583.1 GB free on `C:`.** **Do not inherit it; take your own.** (Session 20's reading two hours earlier was 1.84 GiB free — the machine moves by gigabytes within a session gap, which is the whole point of the rule.)

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. `band_drift.py` needs numpy and stdlib `hashlib` only. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). **The pinned permutation stream is `numpy.random.PCG64` seeded from a 64-bit integer; a numpy change is a replay risk and the drift result must be re-replayed after one.** Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

## 11. Housekeeping that is easy to get wrong

- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session. **Their wording may legitimately differ where their own texts differ.** Sync is of content, not of words.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **The root README's running log is lean and append-only** — entries only for a finished artifact, a phase close, or something genuinely noteworthy. The banner's "Last updated" is the one line that may be overwritten. **Session 21 added one entry** covering the unit-set finding with the two smaller repairs, and left the banner at 2026-08-14.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories, clones and branches before closeout. Sessions 16–21 worked entirely inside the scratchpad.
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **return them from a reader rather than discarding them.** **1 MiB blocks transfer far less than the 4 MiB default** for scattered header reads.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py` (`read_electrode_table`, `contiguous_band` → `depth_lo_um`/`depth_hi_um` in `rel_y`), `anatomy_index.py` (Codex's; pass `--legacy-index-target CA1 --legacy-index-max-gap-um 40` for the existing index, or it *refuses* to extend it), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels` (opt-in derived layer), `band_drift`.
- **The runbook checker walks `scripts/` non-recursively**, so `utils/` modules need no numbered step — **and a new script dropped into `scripts/` without a README step is a hard checker failure.** **After editing either the packet runbook or any script's docstring, run `check_runbook_consistency.py --readme README.md --scripts scripts` from inside the packet folder.** Its harness is in `agents/Claude/tools/`. **Invariants: one step per script, one `bash` fence per step, one line in that fence, one indented line per `Example` block, contiguous unique step numbers.**
- **Scripts must not print non-ASCII.** This console's stdout is cp1252 — even a `print` of a path can crash if it carries a µ. Docstrings are fine; `print` is not. **The sheets use straight quotes only** — verify with Python, not `grep`. (The host-selection document carries exactly four pre-existing curly quotes in its approved region; leave them, and check the count is still four after an edit.)
- **Line endings are pinned by `.gitattributes` and a clone reproduces the working tree exactly.** `* -text`, with `text eol=crlf` for 17 non-packet framework files and Codex's 11 legacy packet outputs. **`agents/Claude/README.md` is CRLF and must stay CRLF** (144/144 as of Session 21); the active chat transcript is genuinely mixed (first 107 lines CRLF, rest LF) and is stored that way. A pattern edit over either must preserve `\r\n` in the match string, or it will match nothing. **If you add a file that must be CRLF, add it to `.gitattributes`.**
- **A clone is not a copy** — but the two now agree. Verify a distribution claim by cloning to a short path (`C:/Users/cresp/AppData/Local/Temp/ct`; the scratchpad path is too long for git), comparing file by file, and **deleting the clone and any temp branch afterwards.** The trick for an uncommitted state: `git add -A`, `git write-tree`, `git commit-tree`, `git branch -f tmp-verify <sha>`, clone `--branch tmp-verify`, then `git branch -D tmp-verify`.
- **The resumable/pinned result files are tracked deliberately.** **Both** `.gitignore` files carry a do-not-catch-these comment.
- **The processed NWB units table is rich** — 31 described columns, and **`results/amplitude_conventions.json` already holds every column's `description` under `descriptions/`.** Read the description before using a column. **`spike_times`' description names no time origin** — which is why §16.4 pins the clock from the converter instead.
- **`results/host_timing_index.jsonl` holds more than it was written for.** Session 21 got the nominal-clock split out of `n_timestamps`, `t_first_s` and `t_last_s` alone. Assume the same of the other recorded indices before downloading anything new.
- **`agents/Claude/tools/` holds one recorded output**, `source_count_granularity_probe_2026-08-13.txt`, because the matching rule cites its numbers. Re-running the probe against the pinned snapshot must reproduce it. **The script needs `--cache "Reproducibility Packet/results/templates_snapshot_2026-08-11.csv"`; it has no default.** A shell redirect adds CRLF — compare normalized, or use its `--out`.
- **`test_band_drift.py` takes `--permutations` only** (no `--module`); **`probe_band_drift_claims.py` takes `--module`**. Read the parser before inventing a flag.
