# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 5 · 2026-08-11 19:11 PDT**
**Next session will be Claude Session 6.**

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work.** It is the contract, it is same-state approved by both agents, and changes to it now go through the **amendment protocol**, never the review cycle. `Accessible Claim Sheet.md` is the same content in plain language and is faster to re-load if you need the shape rather than the exact wording — but the technical sheet governs, and the two must stay in sync in the same session as any change.

---

## 1. Where the project is

**Phase 2 — Execution.** Phase 1 closed in Codex's Session 4. Both Claim Sheets and Study Guide Pass 1 are same-state approved; both review chats are concluded with summaries. **No scientific result exists yet, and no sorter has been run.**

| Approved artifact | SHA-256 at approval |
|---|---|
| `Claim Sheet.md` | `a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3` |
| `Accessible Claim Sheet.md` | `73bff8f81dc2e31b47d4abbe1f61c8106a34dccb8ea6457051c3dba84a589760` |
| `Study Guide/Pass 1….tex` / `.pdf` | `d33e74d7…` / `75e14232…` |

**Your progress-report counter: Session 8 is your next count-based trigger.** Codex wrote the Phase-1-close transition report, so you owe nothing extra unless your session closes a phase transition or an approved amendment.

## 2. The first thing to do next session

**Open `chats/Claude-Codex/Tier A Selection Review/`.** Session 5's whole output is a proposal sitting there for Codex's gate. The state I approved and handed over is `agents/Claude/Tier A Host and Injection Zone Selection.md` at SHA-256 `98a168100f8c315eaf0ba47266e0a3026efbe10ac3ed1751c2b0bef509ffd586` — the chat carries an earlier superseded hash above it, left in place per the append-only rule. **Three rulings are asked of Codex:** exclusion granularity, whether the 16-donor pool changes the block scheme, and CA1 versus taking the `SUB` fallback now. If Codex has replied, the review-cycle discipline applies: genuinely re-review, do not wave edits through, and if a disagreement has not converged in about two round-trips, escalate to the director rather than looping.

**Then read `agents/Claude/Tier A Host and Injection Zone Selection.md`.** It is the live artifact for your share of the labor split, and §5 of it is the list of things it deliberately did not do.

## 3. What Session 5 established, and why it matters

### 3.1 The headline finding — the leakage constraint is avoidable, not a matter of degree

**Every Neuropixels 1.0 donor template in the library comes from DANDI 000409 — the same dandiset the hosts come from.** The 37 "source datasets" are 37 probe insertions across **24 sessions and 12 subjects** (`KS042, KS043, KS044, KS046, KS051, KS052, KS055, KS084, KS086, KS091, KS094, KS096`). There is no second source collection for this probe type.

Two consequences, and they are the substance of the session:

1. **"Exclude the host's source dataset" is three exclusions, not one** — insertion, session, subject — and of the 37 areas at ≥10 in-caliper templates, the worst-case survivors are **7 / 6 / 4** respectively. `SUB` (57) and `ENTl5` (31) look healthy at insertion granularity and go to **zero** at subject granularity. **The project has never declared which granularity it uses.**
2. **DANDI 000409 has 139 subjects and only 12 are in the library, so 429 of its 459 raw recordings incur no exclusion at all.** Choosing the host from one of those makes every granularity vacuous simultaneously and each area keeps its **full** pool. **The 37→7 shortlist that has shaped this project since Session 2 only binds if the host is a library recording, and nothing requires that.**

**What it does not fix, and what goes in the limitations:** host and donor still share one consortium, rig design, probe type, acquisition and preprocessing chain, and strain. No available choice fixes that. Do not let a later session present subject-level separation as independence.

### 3.2 The uncomfortable number — CA1's pool has a hard ceiling of 16

| Caliper | CA1 templates |
|---|---|
| 50–200 µV, SNR 5–15 *(provisional)* | 12 |
| unscreened | **16** |

**Sixteen is the entire CA1 Neuropixels 1.0 population of the library.** No caliper produces more. The four outside the provisional caliper are all KS044 `781b35fd` at 2,800 µm with amplitudes 213–488 µV and SNR 10–23 — **high quality, not marginal**, and Slot 7 already says the 50–200 µV figure is a rescaling *target* rather than a donor requirement, so treating them as eligible is contract-compliant. All 16 come from four subjects; 15 sit inside one 280 µm depth band.

**Working pool 16 for a 10-unit arm: six spares.** The second-order consequence, flagged to Codex and not yet resolved: with 5 blocks × 10 slots the **region-matched arm has almost no donor-draw variability across blocks** while the region-unaware arm draws from 1,149. That asymmetry is most likely to surface in the negative-control replicate band, which Codex owns.

### 3.3 The anatomical mapping the Claim Sheet demands already exists

Every 000409 NWB carries `/general/extracellular_ephys/electrodes` with an Allen CCF **long name** per electrode plus `rel_y` (depth along probe), `rel_x`, CCF `x/y/z`, and `group_name` (probe). Raw and processed files for a session carry **identical** tables. **This is Slot 7's pinned channel/trajectory mapping, already published** — do not build one.

**It reads for ~5–10 MB per recording, not 18–197 GB**, via `utils/remote_hdf5.RemoteFile` (HTTP range requests handed to h5py). That is the technique that makes host screening affordable; reuse it rather than reinventing it.

### 3.4 The two vocabularies, and the check that validated the bridge

Host = Allen long names (`Field CA1`); donors = acronyms (`CA1`). `utils/ccf_labels.py` bridges them and `validate_ccf_label_map.py` checks it against the donor library's own (session, depth, acronym) records — which validates the label map **and** that `depth_along_probe` and `rel_y` are the same coordinate, something nothing else had checked.

Of **1,403 testable comparisons — donor acronyms the table actually defines — 1,401 agree, 1 disagrees, 1 is unmapped.** 44 acronyms confirmed with **zero** disagreements, **`CA1` at 16/16**, plus every large-pool alternative: `CP` 107/107, `SUB` 168/168, `PIR` 94/94, `MRN` 59/59, `AON` 53/53, `ENTl5` 53/53, `VISa5` 49/49, `LP` 47/47. One mixed (`ACAd5` 33/34, a boundary effect). **Zero contradicted.** A further 650 rows carry acronyms the table does not define — that is coverage, not correctness.

**Two corrections were needed to reach those numbers, both in the pessimistic direction.** The first classification condemned an entry on a single disagreement; the second counted *undefined* donor acronyms as disagreements, inventing 49 "contradicted" structures and reporting 92% agreement instead of 99.9%. **A validator can be wrong toward pessimism, and that is no more publishable than optimism.** If you re-run it, check that `undefined` and `disagree` are still kept apart.

## 4. My proposed selection, which is a proposal and not a decision

**Zone: CA1. Host: a 000409 raw recording from a subject absent from the donor library, carrying a contiguous `Field CA1` band.** Rationale: it is the only zone satisfying Tier A and Tier C at once, which Session 3 established as a joint constraint. Moving to `CP` (70) or `SUB` (57) buys Tier A headroom but relocates the work to an unsecured Tier C literature task and risks the exact failure Session 3 named.

Fallbacks, in order, if a gate kills more than six donors: (1) fewer than ten injected units, recorded as a deviation; (2) move to `SUB` and commission Tier C subiculum evidence — **named on pool size and anatomical proximity only; nothing in `references.md` supports subiculum burst parameters yet**, so it is a research task, not a substitution; (3) depth-specific zones — permitted by Slot 7 but weakens the cross-tier comparison, so an amendment rather than a config change; (4) drop Tier A, which Slot 12.3 already pre-declares as a clean publishable failure.

**You are the wrong agent to grade this.** Codex owns Tier A's balance/manipulation gate deliberately. Propose; do not approve.

## 5. What Session 5 did not do — do not let a later session assume otherwise

1. **The host survey is partial.** Coverage is stated in §4 of the selection document and in `host_anatomy_CA1.txt`. The index is append-only and **resumable with the identical command**. Roughly one recording in six carries a usable CA1 band, so it is a **search, not a census** — but a host must not be pinned off a partial ranking without someone explicitly deciding "good enough" beats "best available".
2. **The CCF label map is materially incomplete, and its incompleteness is far larger than its error rate** — the 46 screened recordings produced **296 distinct host structure names with no table entry**. Irrelevant to a CA1-targeted search; **blocking for the region-unaware arm's placement**, whose donors are drawn without conditioning on region. Completing it needs an Allen ontology, and **that carries a licensing question** — Allen Institute terms versus permissively licensed redistributors (`iblatlas` MIT, `brainglobe-atlasapi` BSD-3). Resolve before importing, not after. **This is agent work first, not a director request**: reading the licences is ours to do, and it becomes director-only only if the answer requires a named exception. Session 5 deliberately did not log it in `director_requests.md`, because filing an unscoped question would be handing him our homework.
3. **No non-anatomical host gate has been applied**: drift, noise, duration, post-rescaling effective SNR. All untested.
4. **Ten feasible placements have not been demonstrated**, only made plausible by band width. Slot 7 makes this a gate.
5. **No covariate balance has been evaluated.** Codex's gate, and the one that decides whether Tier A runs.
6. **`audit_template_library.py` duplicates `utils/template_metadata.py`.** Left as-is deliberately rather than refactored mid-flight; recorded in the selection document §5.6 and in `agents/Claude/README.md`. Resolve before packet assembly.
7. **The packet still owes three of its own files.** `Playbooks/reproducibility-packet.md` requires the packet folder to carry its **own** `requirements.txt`, its **own** `.gitignore`, and a runbook `README.md`, because the self-containment test is copying that folder alone to a clean machine. Session 5 created only the **project-root** `requirements.txt` — correct for the venv, not sufficient for the packet. Scripts are already written into `Reproducibility Packet/scripts/` per the write-it-there-first rule, so this is Phase-3 curation rather than relocation, but it is owed and it is not done.

## 6. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate**
- **Tiers B and C:** assigned after Rung 0. For each, the manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 7. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation. Combined arm only after component effects are known.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units. Standardized effect sizes are secondary and never thresholds.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)` is the authoritative and only comparative rule.** `[−T, T]` is declared shorthand for it, never a second test. Declared consequence: `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **The manipulation check is a hard stop-or-go gate.** If injected data does not demonstrably carry the property at realistic magnitude, **no sorter run starts.**
- **One host and injection zone across all tiers by default.** Deviation = recorded limitation and the cross-tier comparison is dropped rather than made across hosts.
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 CPU internal sorter (SpyKING CIRCUS 2, TriDesClous 2, or Lupin — MIT via SpikeInterface). Kilosort-only is biased toward the null.
- **Equal block counts give equal *nominal replication basis*, not equal precision.** Both achieved interval widths get reported.
- **The 48-sorter-hour ceiling stayed at 48 when the tranche doubled to 200 recording-minutes.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV rescaling target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim. **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 8. Two findings about *how to work* worth carrying

1. **Review catches errors, not absences** (Session 4). Nine corrections across two Study Guide reviews, every one to a sentence that existed; the real defect was a missing sentence, and neither agent caught it. **Carry this into Phase 3:** for the Technical Report, the absent sentence is a limitation nobody wrote down. Review against a *checklist of what must be present*, not by reading.
2. **Read the column, do not count it** (Session 5). Session 2's audit was correct code answering a question one level too shallow, and the number it produced was carried into the Claim Sheet, the Study Guide, and the public log before anyone opened a cell. When a field is treated as an opaque token, check what is actually in it before building on the count.
3. **A check can be wrong pessimistically, and that is not the safe direction** (Session 5). The label-map validator reported 49 broken structures and 92% agreement when the truth was zero and 99.9%, twice in a row, because it conflated *undefined* with *wrong*. We are both calibrated to watch for overstated successes; an overstated failure misleads a reader exactly as much, and it is harder to notice because it feels like rigour. **When a self-check reports a problem, verify the problem before acting on it** — the same standard applied to a favourable result.

## 9. Machine state — re-measure, never trust this number

**2026-08-11 18:14 PDT: RAM 15.27 GiB free of 31.67, VRAM 14,416 of 16,311 MiB.**
**2026-08-11 18:45 PDT: RAM 14.39 GiB free, VRAM 14,405 MiB.**

**The four-session downward trend broke.** The series is now 3.46 → 3.96 → 1.01 → 0.89 → **15.27 → 14.39**. Something released ~28 GiB between 16:06 and 18:14. **VRAM has been flat at ~14 of 16 GB free at every measurement**, so the competing work is memory-bound, not GPU-bound. Logged in `director_requests.md` as a data point, explicitly not as an answer.

**Venv state changed this session.** It now holds `h5py==3.16.0` and `numpy==2.5.2` (both BSD-3-Clause), pinned in a **new `requirements.txt`**. SpikeInterface, PyTorch, and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the requirements file carries a note that the numpy pin may have to move when they are. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe`; never bare `python` or `pip`.

## 10. Housekeeping that is easy to get wrong

- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever.** Any amendment updates both **in the same session**. Drift is a defect, not a backlog item.
- **This run is agent-selected**, so the run-provenance block on the public README is **required** and survives unchanged into State B. Do not remove, soften, or move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. A genuine need to modify it is a `director_requests.md` question *before* writing the modification. For sorter internals, use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the *only* exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`; `pdftoppm` and `pdftotext` are also available.** Build twice, check the log for overfull/underfull, and render the changed and final pages before approving any PDF.
- **Two concurrent network jobs roughly halve each other.** Run the anatomy survey alone, or add parallel workers, if you want it to finish.
- **Do not leave a background job running past the end of a session.** Stop it, regenerate its report from whatever it produced, and state the coverage.
- **`RemoteFile` now retries a failed range request four times with backoff** (added Session 5, after one transient S3 disconnect discarded a whole recording's result). At hundreds of sequential requests per run, a dropped connection is routine — if you write another screening loop, use `RemoteFile` rather than rolling your own reader.

## 11. Still-open verification debt

Nothing in `references.md` *Pending* is citable: the regional waveform-duration figures, Steinmetz & Ye 2022, and **Quirk & Wilson** (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed). If Quirk & Wilson ever clears, it is the natural citation for burst amplitude attenuation in Study Guide §2.2 and §3.2, which currently carry that load on Harris et al. 2001 and Pouzat et al. 2004.

**New debt from Session 5:** if the injection zone moves off CA1, Tier C needs primary burst and amplitude-attenuation evidence for the new region and cell class, or it is labelled a synthetic stress test per Slot 13.7. For `SUB` that means subiculum bursting pyramidal cells; nothing on it is in `references.md` yet.
