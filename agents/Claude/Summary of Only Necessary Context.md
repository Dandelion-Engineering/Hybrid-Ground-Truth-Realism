# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 7 · 2026-08-12 10:20 PDT**
**Next session will be Claude Session 8 — which is a count-based progress-report trigger. Do the session's work first, then write `Progress Reports/Progress Report Session 8.md`.**

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including its `## Amendments` section. Amendments 1 and 2 are `In force` and govern. Amendments 3 and 4 are **`Proposed`** and carry no force until Codex approves the exact bytes. `Accessible Claim Sheet.md` is the same content in plain language and carries the same four amendments.

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, and nothing beyond bounded metadata range reads has been downloaded.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | Approved Phase-1 text + **A1, A2 `In force`; A3, A4 `Proposed`**. Whole-file `a43eb4f686cb5baed399ef07151cc37dff27b2d983e1bfa1a5d0465a59b96fba`. |
| `Accessible Claim Sheet.md` | Synchronized. Whole-file `71eedf5eee9b3bd64ab93077695cc9c622fd78d8a466c3e35599fa1f065d2134`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 4**, `c3303cf35837120d22af4a992a2e8d1357d983c9243812173f7484bcd3763113`, explicitly approved by me and handed to Codex. §1–§8 are the jointly approved Draft 3 text; §9 and §10 are new. |

## 2. The first thing to do next session

**Open `chats/Claude-Codex/Tier A Selection Review/`** — it is the only active chat and everything live is in it. Three things are outstanding and all three are Codex's move:

1. **Exact-state review of Amendments 3 and 4.** If Codex approves, flip both status lines to `In force` with the date, **in both sheets, same session**. **Amendment 3 blocks all Tier A generation until it is `In force`** — that prohibition comes from Amendment 2 and Amendment 3 discharges it, not before.
2. **Who measures the donor template footprint.** I asked; see §4 below for why it matters more than anything else open.
3. **Whether to set an overcrowding threshold.** I proposed declining. If Codex wants one, that is a contract amendment, not a script parameter.

**If your session writes the approving turn on A3 or A4, you owe a progress report** — and Session 8 owes one anyway on the count.

## 3. What Session 7 settled

### 3.1 Amendment 2 is closed, and checking it produced Amendment 4

Codex removed "one mouse strain" (technical) and "same rig design / same mouse strain" (accessible) from Amendment 2 as unestablished. I verified at the substrate instead of accepting the argument, and found more than the removal claimed. `Reproducibility Packet/scripts/audit_subject_provenance.py` → `results/subject_provenance.txt`, 21 subjects, 88.7 MB metadata:

- **The files carry no `genotype`, `strain` or `description` field at all.** Strain is *unverifiable*, not merely unsupported. **Never report it as shared or as different.**
- **All 12 donor subjects are `cortexlab`/UCL.** The whole NP1.0 donor library is one laboratory's work → new **Slot 13.10** in Amendment 4.
- **All 9 candidate host subjects are `churchlandlab`/CSHL or `angelakilab`/NYU.** Zero overlap. Host/donor separate at **laboratory, institution and rig**, not just animal — stronger than the contract claims.
- Boundary: one asset read per subject, so `lab` is verified per session read. Not a gate; every candidate already satisfies it.

**The transferable lesson: removing an unverified claim can create a new one.** A limitations list that stops mentioning strain reads as though strain were checked and found different.

### 3.2 Amendment 3 settles the negative-control band

Codex accepted my counter-proposal (P1 = fixed seeded 16-template subset of the region-unaware pool; P2 = full unaware pool matched to P1; neither conditions on region) and withdrew its replicate-stability construction — but ruled it a contract change, not an implementation note, because Slot 5 says "same selection ... procedure." Amendment 3 delivers all seven contents Codex specified, Tier A-only, and adds one obligation Codex did not ask for: **Slot 8's Panel 2 caption and the Technical Report must name which band construction is shown**, because otherwise one grey band means two things in one report.

### 3.3 The placement gate is applied — Slot 7's last metadata-only gate

`Reproducibility Packet/scripts/screen_injection_placement.py` → `results/injection_placement_CA1.txt` / `.json`. 13 bands, **170.2 MB metadata, zero failures.**

- **Label ambiguity: closed.** All 13 bands **100% pure**; nearest other structure exactly 20 µm beyond each edge; recomputed band matches the index on all 13; raw and processed electrode tables agree contact-for-contact on all 13.
- **Placement capacity: 9 of 13 pass** at 60 µm edge margin / 40 µm separation. **Both are declared, not measured** — at 100 µm only 5 pass, at 140 µm only 2. **The verdict is parameterized, not decided.**
- **Overcrowding measured, not gated.** Ten injected units = +3.7%…+45.5% of native clusters, +17%…+1000% of `good` units. The Claim Sheet fixes no threshold and a script is not where one gets invented.

### 3.4 Two findings that arrived sideways

- **NYU-39 Probe00 should be dropped on yield, not geometry.** 22 sorted units in its CA1 band, **one** `good`, versus 174/32 in a comparable CSHL047 band. It passes the geometric gate at exactly ten sites.
- **The 50–200 µV rescaling target brackets `good` units** (51–110 µV median, p90 to 258) and is too loud for the MUA population (all-unit medians 20–60 µV). **Caveat is load-bearing:** IBL's `median_spike_amplitude_uV` convention versus the donor library's `amplitude_uv` is **unverified**. Run that check before treating the target as validated.

### 3.5 A shortcut found and rejected

`cumulative_drift_um_per_hour` exists in the processed files and would have discharged the drift gate for free. Its values reach ~6.5 × 10⁶, which is impossible for a probe in a mouse brain, so the name does not describe the values. **Not used. Drift is still open.** Do not rediscover this column and trust it.

## 4. Host selection: where it stands, and the one thing that unblocks it

Gates **discharged**: anatomy · duration · donor-lab separation · label ambiguity · placement capacity *at declared parameters*.
Gates **open**: **donor template footprint measurement** (re-decides placement) · **drift** · **noise** · **post-rescaling effective SNR** · **Codex's covariate balance**.

**The footprint measurement is the highest-value remaining piece of my share.** It converts the placement gate from parameterized to decided, and it needs the template arrays from the upstream zarr store (`s3://spikeinterface-template-database/…`, paths in `results/templates_snapshot_2026-08-11.csv`). If Codex's Rung 0 pulls templates through SpikeInterface anyway, measuring extent there is nearly free; doing it myself costs a separate zarr reader. **Do not start writing that reader before reading Codex's answer in the chat.**

**Recommended order for spending the remaining gates** (a recommendation, not a selection — nothing downstream may treat it as one):

1. **CSHL047 Probe01** — 700 µm, 174/32 units, the only band holding ten at every swept parameter up to a 140 µm margin.
2. **NYU-12 Probe01** — 640 µm, 267/60 units, densest native neighbourhood and smallest relative perturbation.
3. **CSHL047 Probe00, session b52182e7** — 560 µm, 182/35, same recording as (1), so the natural depth-specific-zones fallback. **Its two probes carry different clocks** (§4.4 of the artifact).

**First-admissible, never "best"** (Codex ruling 7.3, accepted). Do not resume the 46-of-429 anatomy survey out of tidiness; resume only if every current candidate fails.

## 5. What is still not done — do not let a later session assume otherwise

1. **No host is pinned**, and that is correct: first-admissible means first to clear *every* gate, and two have not run.
2. **The CCF label map is materially incomplete** — 296 unmapped host structure names, 650 undefined donor acronyms. Irrelevant to a CA1 search, **blocking for the region-unaware arm's placement**. Needs an Allen ontology and **the licences must be read first** (Allen terms vs `iblatlas` MIT / `brainglobe-atlasapi` BSD-3). Agent work, not a director request, unless the answer needs a named exception. **Still open after Session 7 — deliberately deprioritized behind the placement gate, not forgotten.**
3. **`audit_template_library.py` duplicates `utils/template_metadata.py`.** Resolve before packet assembly. Session 7 did the analogous refactor for the anatomy functions (`utils/host_anatomy.py`), so the pattern is established.
4. **The packet still owes its own `requirements.txt`, `.gitignore` and runbook README.** The self-containment test is copying that folder alone to a clean machine.
5. **The amplitude-convention check** (§3.4) has not been run.

## 6. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate**
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
- **The negative-control band construction is settled** (Amendment 3, pending approval). Do not reopen it; the argument that won it is §8.3 of the Tier A artifact.
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV rescaling target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first. **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 8. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5).
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5).
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The question that resists it: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?*
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`, and `tail` the file afterwards. **Also: a heredoc through the Bash tool mangles nested quotes and doubles `%`** — write the text with the Write tool to a scratch file and have Python read it in.
7. **Removing an unverified claim can create a new one** (S7). A limitations list that stops mentioning something reads as though it was checked and found absent. Going and looking cost ten minutes.
8. **A measurement you just made is not a threshold you get to set** (S7). Having measured native unit density, the pull was to gate on it. The Claim Sheet fixes no overcrowding threshold, and a design parameter buried in a script is invisible to review. Report it; ask for the decision.
9. **Read a rich first-party table, not one column of it** (S7). The two most valuable findings — NYU-39's single `good` unit and the amplitude comparison — fell out of a table opened for a different reason, at no extra cost.
10. **Verify a name before trusting it** (S7). `cumulative_drift_um_per_hour` would have answered an open gate for free; thirty seconds on its magnitude showed it does not mean what it says.

## 9. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). The old low-memory series was leaked Claude automation processes, not competing research; **do not reason from its shape**. Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Last reading: 2026-08-12 09:51 PDT — RAM 17.19 GiB free of 31.67; VRAM 826 MiB used of 16,311. Do not inherit it; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt`. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe`; never bare `python` or `pip`.

## 10. Housekeeping that is easy to get wrong

- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session.**
- **`RemoteFile` validates and retries range responses.** Reuse it for any remote NWB read rather than rolling your own. **1 MiB blocks transfer far less than the 4 MiB default** for scattered header reads — 2–4 MB per file instead of 12.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py` (band finding), `anatomy_index.py` (Codex's target/gap provenance assertions — pass `--legacy-index-target CA1 --legacy-index-max-gap-um 40` for the existing index), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`.
- **When you refactor a script another agent hardened, prove it still works.** Session 7's proof was replaying the anatomy survey with `--limit 0` (zero remote reads) and diffing the report byte-for-byte.
- **The three resumable/pinned result files are tracked deliberately** (`host_anatomy_index.jsonl`, `host_timing_index.jsonl`, and the two upstream snapshots), and `.gitignore` carries a comment saying so. Do not add a blanket rule catching `Reproducibility Packet/results/`.
- **`screen_injection_placement.py --from-records`** rewrites its report from saved JSON with no network reads. Use it for any presentation change.

## 11. Still-open verification debt

Nothing in `references.md` *Pending* is citable: the regional waveform-duration figures, Steinmetz & Ye 2022, MEArec, and **Quirk & Wilson** (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed). If Quirk & Wilson clears, it is the natural citation for burst amplitude attenuation in Study Guide §2.2 and §3.2, which currently carry that load on Harris et al. 2001 and Pouzat et al. 2004.

**If the injection zone ever moves off CA1**, Tier C needs primary burst and amplitude-attenuation evidence for the new region and cell class, or it is labelled a synthetic stress test per Slot 13.7. Nothing on subiculum bursting is in `references.md` yet.
