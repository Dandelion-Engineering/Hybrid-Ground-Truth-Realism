# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 8 · 2026-08-12 12:35 PDT**
**Next session is Claude Session 9. No count-based progress report is due** (the next is Session 16), but a phase transition or an approved amendment written in your session still triggers one.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including its `## Amendments` section. Amendments 1, 2 and 4 are `In force` and govern. Amendment 3 is **`Proposed`** and carries no force until Codex approves the exact bytes. `Accessible Claim Sheet.md` is the same content in plain language and carries the same four amendments.

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, and nothing beyond bounded metadata reads has been downloaded.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | Approved Phase-1 text + **A1, A2, A4 `In force`; A3 `Proposed`**. Whole-file `3d9fd72b8321af49f2c737a35d7536f73615982d88424b4cea144dd8ebc45c33`. |
| `Accessible Claim Sheet.md` | Synchronized. Whole-file `a5cf71b76d27886bad12bbae8a90e82f40230cef9ef776627d8257864cf4c8a9`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 5**, `7c4b911df9e53032ae7cd0453cc51ac79b4d65fdfa40abcd41577ad027be69db`. **§1–§10 are same-state approved by both agents.** §11 is new and unreviewed. |

## 2. The first thing to do next session

**Open `chats/Claude-Codex/Tier A Selection Review/`** — still the only active chat. One thing is outstanding and it is Codex's move: **exact-state review of Amendment 3 as I edited it.** If Codex approves, flip the status line to `In force` with the date **in both sheets, same session**. Amendment 3 blocks all Tier A generation until then.

I also asked Codex whether the arm-asymmetric rescaling factors (§4.3 below) belong in its balance gate as a declared covariate. That is a question, not a blocker.

## 3. What Session 8 settled

### 3.1 The owner re-review — I accepted every Codex edit, having checked each one

Codex's Session 7 review edited both sheets and Draft 4. I re-derived every measured claim from `Reproducibility Packet/results/subject_provenance.json` rather than reading the prose. All confirmed:

- Donor labs `{cortexlab}` ×12 (UCL); host `{churchlandlab ×3, angelakilab ×6}` (CSHL, NYU); intersection empty.
- **Protocol versions overlap at exactly `{6.4.2}`.** My Session 7 sentence said they "differ across the two sides" directly above a list sharing 6.4.2. Codex was right.
- `genotype` / `strain` / `description` absent from all 21 files — and I checked `_scalar` really returns `None` only on `key not in node`, so an empty dataset would not read as absent.
- **Codex's Amendment 3 seed verifies:** SHA-256 of `Hybrid Ground Truth Realism|Tier A|pseudo pool|v1` is `2a66865b5504…`; `0x2a66865b` = `711362139`.

**Amendment 4 is `In force`.** Codex's rig narrowing was correct and is the same error class I raised on it in Session 7, running the other way — I inferred rig separation from institution separation and stated it as measured.

### 3.2 The one edit I made to Amendment 3 — and the argument, because it may be contested

Codex pinned the *seed* before the pool exists but left the *objective, scaling, search budget and tie-break* to configuration-approval time, which is after the pool exists. I edited point 1 to fix the whole rule now. **The argument is directional and is the thing to defend if Codex pushes back:**

> A P1 subset matching the CA1 sixteen **worse** widens the negative-control band (conservative). One tuned to match **better** narrows it — and a narrower band makes the real Tier A effect look more decisive. So an objective chosen with the pool in view can only ever flatter us.

The rule now in the contract: three covariates (post-rescaling amplitude, effective host SNR, depth along the injection band), each standardized over the final eligible pool; objective = equally weighted sum of 1-Wasserstein distances against the CA1 sixteen (for equal-sized samples, mean absolute difference of sorted vectors); minimized by seeded start + improving pairwise swaps to convergence or 100,000 evaluations; ties to lowest `template_index`. **Changing it takes its own amendment.** I told Codex I will take its objective if it prefers one — the point is that it is fixed now, not that it is mine.

### 3.3 The amplitude-convention check — the session's real result

`Reproducibility Packet/scripts/audit_amplitude_conventions.py` → `results/amplitude_conventions.txt` / `.json`. 43.5 MB, 42 requests, metadata only, session `sub-KS042/ses-07dc4b76`.

**The two columns are not the same quantity.** Donor `amplitude_uv` = `np.ptp(templates_array, axis=1)` at the best channel — **peak-to-peak of an average waveform** (`hybrid_template_library` @ `0023db29688842f74698bac40c48a86477ea39e7`, `upload_ibl_templates.py:326`, `consolidate_datasets.py:104,118`). Host `median_spike_amplitude_uV` = **median over per-spike single-sided peaks**, per the NWB's own column descriptions.

**Measured conversion**, via the files' own `waveform_mean` (in volts), exact unit identity:

| cohort | n | ratio median | p10–p90 |
|---|---|---|---|
| all | 1,821 | 1.250 | 1.13–1.91 |
| `kilosort2_label == good` | 478 | 1.242 | 1.11–2.50 |
| `ibl_quality_score == 1.0` | 201 | **1.207** | 1.10–1.51 |

**The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only, never unit level.** The p90 forbids per-unit conversion. **Do not pick up "1.2" and apply it to one unit.**

**Session 7's claim is corrected, not deleted.** The direction survives (41–165 still brackets the 51–110 µV `good` medians) but was reached by an undefined comparison. Logged in `references.md`'s corrections table as row 8.

### 3.4 Three facts that came out of it and are not recorded elsewhere

1. **The donor library is good-clusters-only by construction** — `IblSortingExtractor(..., good_clusters_only=True)`, `upload_ibl_templates.py:162`. Tier A's region-matched arm is "region-matched templates *from well-isolated units*." State it that way.
2. **A third best-channel rule.** IBL's `max_electrode` agrees with upstream's peak-to-peak argmax on only **72.6%** of units, usually a near tie between adjacent contacts. Ratios reported at both channels agree to ~0.02 in the median, so the conversion is safe. **But donor `depth_along_probe` and host unit depth use different best-channel rules** — 20 µm in the disagreeing quarter. Handed to Codex as an input to its footprint/placement calibration.
3. **The 50–200 µV target is the donor pool's lower 58%.** All 2,183 NP1.0 templates: median 184.2 µV, none < 50, **42.0% > 200**. The CA1 sixteen: 105, 110, 111, 112, 117, 124, 131, 141, 175, 187, 191, 200, 213, 330, 420, 487; median 158, four above 200. Nobody is cut (the caliper screens, per Amendment 2). But **the CA1 median sits below the pool median, so region-matched templates are scaled *up* on average relative to region-unaware partners** — post-rescaling amplitude is matched, so not a residual confound, but the scale factors differ systematically between arms.

### 3.5 A failed approach, recorded so it is not retried

Matching library templates to file units **by order fails at chance** (0.000–0.023) under both the `kilosort2_label` and `ibl_quality_score` definitions of good, across all four (zarr × probe) pairings. The consolidated metadata carries **no unit id**, only a positional `template_index`. Recovering identity needs the zarr store's `unit_ids` — a separate reader. The §11.2 measurement was deliberately rebuilt not to need it.

**Useful parsing fact learned:** a zarr dataset name is `f"{dandiset_id}_{dandi_name}_{sorting_pid}.zarr"` — the trailing 36-character field is the **IBL probe-insertion id**, which the NWB does not carry. That is why probe assignment is ambiguous for two-probe sessions.

## 4. Host selection: where it stands

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating** property: donor-lab separation.
**Parameterized, not discharged**: placement capacity — edge margin *and* minimum peak separation each need their own justification. **Codex owns that two-part calibration** as part of Rung 0 preparation; do not start it.
Gates **open**: drift · noise · post-rescaling effective SNR · Codex's covariate balance.

**Recommended order** (a recommendation, not a selection — nothing downstream may treat it as one):

1. **CSHL047 Probe01** — 700 µm, 174/32 units, the only band holding ten at every swept parameter up to a 140 µm margin.
2. **NYU-12 Probe01** — 640 µm, 267/60 units, densest native neighbourhood, smallest relative perturbation.
3. **CSHL047 Probe00, session b52182e7** — 560 µm, 182/35, same recording as (1), so the natural depth-specific-zones fallback. **Its two probes carry different clocks** (§4.4 of the artifact).

**NYU-39 Probe00 is deprioritized, not disqualified** (22 units, one `good`). Both agents declined to invent an overcrowding threshold after seeing values.

**First-admissible, never "best"** (Codex ruling 7.3, accepted). Do not resume the 46-of-429 anatomy survey out of tidiness; resume only if every current candidate fails.

## 5. What is still not done — do not let a later session assume otherwise

1. **No host is pinned**, and that is correct.
2. **The CCF label map is materially incomplete** — 296 unmapped host structure names, 650 undefined donor acronyms. Irrelevant to a CA1 search, **blocking for the region-unaware arm's placement**. Needs an Allen ontology and **the licences must be read first** (Allen terms vs `iblatlas` MIT / `brainglobe-atlasapi` BSD-3). Agent work, not a director request, unless the answer needs a named exception. **Now the largest open item nobody is working on, and it is mine. Deprioritized three sessions running; consider doing it next.**
3. **`audit_template_library.py` duplicates `utils/template_metadata.py`.** Resolve before packet assembly. `utils/host_anatomy.py` (Session 7) is the pattern.
4. **The packet still owes its own `requirements.txt`, `.gitignore` and runbook README.** The self-containment test is copying that folder alone to a clean machine.
5. **The preprocessing half of the amplitude question is untouched** and is not metadata-answerable: donor averages use a 1 Hz highpass + CMR over the last 30 minutes; the host column is IBL's number on IBL's preprocessing. Needs the stack — Rung 0 territory.

## 6. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** (taken Session 7)
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 7. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`, `G0` the mean paired sorter gap *in the control arm*** — not the negative-control band. `[−T, T]` is declared shorthand for the `D` rule, never a second test. `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **The manipulation check is a hard stop-or-go gate.**
- **One host and injection zone across all tiers by default**; a deviation is a recorded limitation and the cross-tier comparison is dropped rather than made across hosts.
- **CA1 is the approved first zone.** Do not commission the `SUB` literature task unless CA1 fails a real gate.
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **Equal block counts give equal *nominal replication basis*, not equal precision.** Both achieved widths get reported.
- **The negative-control band construction is settled in substance** (Amendment 3); only its selection-rule paragraph is in review. The argument that won it is §8.3 of the Tier A artifact.
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV rescaling target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim and the "protocol versions differ" self-contradiction (S7, corrected S8); the amplitude-convention comparison (S7, corrected S8). **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 8. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5).
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5).
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The question that resists it: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* Applied in S8: all Codex edits passed it, which is a real answer, not a rubber stamp — the check was re-deriving the measurements, not re-reading the prose.
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`, and `tail` the file afterwards. **A heredoc through the Bash tool mangles nested quotes and doubles `%`** — write the text with the Write tool to a scratch file and have Python read it in. **Also: matching a long literal against a file with box-drawing characters and column-aligned padding fails on whitespace** — edit such blocks line-by-line by index, not by whole-string replace.
7. **Removing an unverified claim can create a new one** (S7).
8. **A measurement you just made is not a threshold you get to set** (S7).
9. **Read a rich first-party table, not one column of it** (S7).
10. **Verify a name before trusting it** (S7). `cumulative_drift_um_per_hour` reaches ~6.5 × 10⁶, which is impossible; **it is not used and drift is still open.** Do not rediscover this column and trust it.
11. **Two numbers in the same unit are not the same quantity** (S8). Both amplitude columns were in microvolts, which is exactly why nobody noticed for six sessions. When two sources are compared, read both definitions from primary sources before comparing, not after.
12. **When a safety check fires, measure it before loosening it** (S8). The best-channel assertion aborted on the first unit. Measuring the disagreement rate turned an apparent bug into the session's third finding. Loosening it to make the script run would have destroyed the finding and kept the bug.
13. **A correction is worth logging even when the conclusion survives** (S8). Otherwise the ledger records lucky reasoning as sound reasoning.
14. **Design the measurement so it does not need the fragile step** (S8). The first script needed unit-level matching and died with it. The rewrite needed no matching and worked anywhere.

## 9. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). The old low-memory series was leaked Claude automation processes, not competing research; **do not reason from its shape**. Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Last reading: 2026-08-12 12:07 PDT — RAM 15.53 GiB free of 31.67 (50% in use); VRAM 810 MiB used of 16,311. Do not inherit it; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt`. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe`; never bare `python` or `pip`.

## 10. Housekeeping that is easy to get wrong

- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session.**
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests`. Reuse it for any remote NWB read rather than rolling your own. **1 MiB blocks transfer far less than the 4 MiB default** for scattered header reads.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py` (band finding), `anatomy_index.py` (Codex's target/gap provenance assertions — pass `--legacy-index-target CA1 --legacy-index-max-gap-um 40` for the existing index), `remote_hdf5`, `dandi` (`list_assets`, `blob_url`, `subject_of`, `session_of`, `RAW_SUFFIX`, `PROCESSED_SUFFIX`), `template_metadata`, `ccf_labels`.
- **When you refactor a script another agent hardened, prove it still works.**
- **The three resumable/pinned result files are tracked deliberately** (`host_anatomy_index.jsonl`, `host_timing_index.jsonl`, and the two upstream snapshots), and `.gitignore` carries a comment saying so. Do not add a blanket rule catching `Reproducibility Packet/results/`.
- **`screen_injection_placement.py --from-records`** rewrites its report from saved JSON with no network reads. Use it for any presentation change.
- **The processed NWB units table is rich** — 32 columns including `waveform_mean` (volts, `(units, time, channels)`, NaN-padded), `spike_amplitudes_uV`, `cluster_uuid`, `ibl_quality_score`, `max_spike_amplitude_uV`. **Every column carries a `description` attribute.** Read the description before using a column; that is what settled the amplitude question.

## 11. Still-open verification debt

Nothing in `references.md` *Pending* is citable: the regional waveform-duration figures, Steinmetz & Ye 2022, MEArec, and **Quirk & Wilson** (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed). If Quirk & Wilson clears, it is the natural citation for burst amplitude attenuation in Study Guide §2.2 and §3.2, which currently carry that load on Harris et al. 2001 and Pouzat et al. 2004.

**If the injection zone ever moves off CA1**, Tier C needs primary burst and amplitude-attenuation evidence for the new region and cell class, or it is labelled a synthetic stress test per Slot 13.7. Nothing on subiculum bursting is in `references.md` yet.
