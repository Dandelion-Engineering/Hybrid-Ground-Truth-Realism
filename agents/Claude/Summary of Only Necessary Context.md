# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 9 · 2026-08-12 14:40 PDT**
**Next session is Claude Session 10. No count-based progress report is due** (the next is Session 16) — but a phase transition or an amendment you put *into force* in your session triggers one regardless of count.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. Amendments 1, 2 and 4 are `In force` and govern. Amendment 3 is **`Proposed`** and carries no force. `Accessible Claim Sheet.md` is the same content in plain language and carries the same four amendments.

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, and nothing beyond bounded metadata reads has been downloaded.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | Approved Phase-1 text + **A1, A2, A4 `In force`; A3 `Proposed`**. Whole-file `b0dbfd697f49e3e35ea6f4587830ef60ca5335dad17c1acb57b9b8718862de50`. |
| `Accessible Claim Sheet.md` | Synchronized. Whole-file `656f7de82ddcba72add8b9e1ec77d2f207e40e491ffc3cefe48a75b1e9474b05`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 6.** §1–§11 same-state approved by both agents (Draft 5 = `7c4b911d…`). **§12 is new and unreviewed**, and §5.2 carries an appended Session 9 resolution note. |

## 2. The first thing to do next session

**Open `chats/Claude-Codex/Tier A Selection Review/`** — still the only active chat, and it is **Codex's move**. Outstanding for it: exact-state review of my Session 9 edit to Amendment 3 (the search-space removal, §3.2 below), plus the evaluation-cap observation if it wants to act on it.

**If Codex approves, whoever writes that turn flips A3 to `In force` with the date in BOTH sheets in the same session — and that flip triggers a progress report for its author.** Amendment 3 blocks all Tier A generation until then.

## 3. What Session 9 settled

### 3.1 Codex's three Amendment 3 repairs — verified at the substrate, all accepted

- **`template_index` is not an identifier.** Verified: 2,183 NP1.0 rows, **187** distinct integer values, 2,183 distinct (`dataset`, `template_index`) pairs. The contract now pins waveforms by the pair everywhere.
- **Determinism.** A seed alone did not fix the RNG, starting draw, sweep order, improvement rule or cap behaviour. Codex's SHA-256-ranked start uses no RNG at all, so it survives a library version change. Accepted in full.
- **My unproved monotonic claim removed.** I had asserted better matching narrows the band / worse widens it. Not measured; the band is sorter-derived and the objective is not. The forking-path argument carries the precommitment alone. **This is the same error class as Session 7's amplitude comparison — do not make it a third time.**

### 3.2 The hole those repairs exposed — the fix that is now in review

**P1's search space contained the real matched arm.** Slot 5 defines the region-unaware arm as drawing *without conditioning on region* — region-**blind**, not CA1-free. So the sixteen CA1 templates are inside the final eligible pool, and P1's objective (1-Wasserstein distance to the CA1 sixteen) **is minimized at exactly zero by those sixteen**. The rule for building the no-manipulation control was a deterministic search whose optimum is the manipulated arm.

**Fix:** point 1 now defines P1's search space as the eligible pool **minus the injection zone's own donor pool**. Point 3 no longer asserts "neither pseudo-arm conditions on region" as a bare fact — it argues it, and distinguishes withholding the manipulation from applying an inverse one. Nothing else in the amendment moved.

**Two boundaries stated so they are not rediscovered:** the bounded search would not have recovered all sixteen at any plausible pool size (the defect is aim, not outcome); and the objective is distributional, so other subsets can score zero too — which does not help, because the CA1 sixteen are the one subset guaranteed to.

### 3.3 The evaluation-cap arithmetic — raised, not edited

One complete sweep costs **16 × (M − 16)** evaluations for search space M, and a partial sweep is never used, against a 100,000 cap. M ≈ 2,167 → 2 sweeps; **M ≈ 1,149 → 5**; M ≈ 500 → 12; M ≈ 200 → subset exhausted. So "achieved distances" mean very different things at different pool sizes. **Not a defect** — declared bounded, stop reason reported, and after §3.2 there is no direction the cap can bias toward. Codex may re-express the cap in sweeps; I said I would take its rule.

### 3.4 Codex's scale-factor ruling — accepted, do not reopen

Pre-rescaling scale factors are **not** a matching covariate. Rescaling is linear, so the sorter observes rendered amplitude, which is already matched; matching the factor would constrain the donor-amplitude distribution, which is part of what region *is* in this library, and would over-control the manipulation. They are recorded as a **manipulation-check diagnostic** (per-arm distributions, extremes, finite factors, no clipping, achieved amplitudes). Only a Rung 0 finding that scaling is non-linear in practice reopens it, via amendment.

## 4. The CCF label map — closed, and how

### 4.1 The licence answer, which is the load-bearing part

**Allen Institute Terms of Use permit "research or other noncommercial purposes" and forbid commercial redistribution without written permission.** Under this project's standard that makes the CCF ontology a restrictive input needing a named exception — which would put a noncommercial restriction on part of a shipped artifact, a director-level call.

**`iblatlas` (MIT) and `brainglobe-atlasapi` (BSD-3) do not dissolve it.** Both licences are honest about their own code; neither party is the Allen Institute, and a permissive licence over a redistribution is not a grant of rights in the upstream content. **Do not "just pip install iblatlas" to get a structure tree.**

**No exception was requested and none is needed** — the ontology proved unnecessary, so the director was never the dependency. Nothing was filed in `director_requests.md`.

### 4.2 What was built instead

`Reproducibility Packet/scripts/derive_ccf_label_map.py` reads the correspondence off DANDI 000409 (CC-BY-4.0) electrode long names and template-library (MIT) acronyms at the same probe depth. **146.6 MB in 150 range requests, metadata only.** 32/37 insertions assigned, 2,053 donor rows placed.

- **138 entries emitted; 94 are structures the hand-authored table lacked.** 119 unanimous, 23 majority, 2 ambiguous.
- **Audit vs the hand-authored table: 44 agree, 0 disagree.** This is the first independent check of its *long-name spellings* — the old validation could only test names the table already had. **It is also the only non-circular confirmation available**, because validating derived entries against the evidence they came from would agree trivially. That check was deliberately not run; do not run it and call it confirmation.
- **2 collisions withheld entirely**, not resolved by vote: `PAG`/`IVn` on `'Periaqueductal gray'`, `VISpm6a`/`VISpm5` on `'posteromedial visual area layer 6a'`. Both boundary contamination.
- **Ceiling:** of **209** distinct host long names on the assigned probes, **143 mapped, 66 still unmapped.** Those need the ontology, so **the licence question returns if a placement lands in one of the 66.**
- **Do not read the 66 against the old 296.** The 296 came from 46 screened recordings; the 209 from 32 donor-session probes. Different denominators.

### 4.3 How it is wired

`utils/ccf_labels.py` gained an **opt-in** derived layer. `to_acronym(label)` is unchanged; `to_acronym(label, include_derived=True)` consults it, hand-authored always winning; `provenance(label)` returns `hand-authored` / `derived:unanimous` / `derived:majority` / `None`. **Verified, not assumed: re-running `validate_ccf_label_map.py` after the change reproduced its tracked report byte for byte.**

`derive_ccf_label_map.py --from-records "Reproducibility Packet/results/ccf_label_map_derived_records.json"` replays the whole report and map with **zero network reads**; verified byte-identical. Use it for any rule or presentation change.

### 4.4 One structural finding to hand to Codex

**The donor library's acronyms sit at mixed levels of the atlas hierarchy** — `MB` (Midbrain) and `OLF` (Olfactory areas) appear alongside their descendants `MRN` and `PIR`. **"Same region" is not well defined when one label is a parent of the other**, which belongs in Codex's balance gate. CA1 is a leaf and all sixteen donors are labelled `CA1`, so Tier A is unaffected — but **any zone change must check for parent-labelled donors first.**

## 5. Host selection: where it stands (unchanged this session)

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
**Parameterized, not discharged**: placement capacity — edge margin *and* minimum peak separation each need their own justification. **Codex owns that two-part calibration**; do not start it.
Gates **open**: drift · noise · post-rescaling effective SNR · Codex's covariate balance.

**Recommended order** (a recommendation, not a selection):

1. **CSHL047 Probe01** — 700 µm, 174/32 units, the only band holding ten at every swept parameter up to a 140 µm margin.
2. **NYU-12 Probe01** — 640 µm, 267/60 units, densest native neighbourhood.
3. **CSHL047 Probe00, session b52182e7** — 560 µm, 182/35, same recording as (1). **Its two probes carry different clocks** (§4.4 of the artifact).

**NYU-39 Probe00 is deprioritized, not disqualified** (22 units, one `good`). Both agents declined to invent an overcrowding threshold after seeing values. **First-admissible, never "best"** (Codex ruling 7.3). Do not resume the 46-of-429 anatomy survey out of tidiness.

## 6. What is still not done

1. **No host is pinned**, and that is correct.
2. **`audit_template_library.py` duplicates `utils/template_metadata.py`.** Resolve before packet assembly. `utils/host_anatomy.py` is the pattern. **This is now the largest open item that is mine.**
3. **The packet still owes its own `requirements.txt`, `.gitignore` and runbook README.** The self-containment test is copying that folder alone to a clean machine.
4. **The preprocessing half of the amplitude question is untouched** and not metadata-answerable — Rung 0 territory.
5. **The 66 unmapped host long names** (§4.2) — resolvable only by an ontology, so they are a licence question, not a coding one.

## 7. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 8. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`, `G0` the mean paired sorter gap *in the control arm*** — not the negative-control band. `[−T, T]` is declared shorthand for the `D` rule, never a second test. `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **The manipulation check is a hard stop-or-go gate.**
- **One host and injection zone across all tiers by default**; a deviation is a recorded limitation and the cross-tier comparison is dropped rather than made across hosts.
- **CA1 is the approved first zone.** Do not commission the `SUB` literature task unless CA1 fails a real gate.
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **The donor library is good-clusters-only by construction** (`IblSortingExtractor(..., good_clusters_only=True)`). Tier A's matched arm is "region-matched templates *from well-isolated units*."
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.** Never apply the ~1.2 factor to one unit.
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim and the "protocol versions differ" self-contradiction; the amplitude-convention comparison; **the unproved monotonic matching-quality/band-width claim (S8, corrected S9); the raw-string label audit that reported 30 punctuation differences as anatomical disagreements (S9, caught in-session).** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5).
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5).
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?*
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes and doubles `%`** — write the text with the Write tool to a scratch file and have Python read it in. **Matching a long literal against a file with box-drawing characters fails on whitespace** — edit such blocks line-by-line.
7. **Removing an unverified claim can create a new one** (S7).
8. **A measurement you just made is not a threshold you get to set** (S7).
9. **Read a rich first-party table, not one column of it** (S7).
10. **Verify a name before trusting it** (S7). `cumulative_drift_um_per_hour` reaches ~6.5 × 10⁶, which is impossible; **it is not used and drift is still open.**
11. **Two numbers in the same unit are not the same quantity** (S8). Both amplitude columns were in microvolts, which is why nobody noticed for six sessions.
12. **When a safety check fires, measure it before loosening it** (S8).
13. **A correction is worth logging even when the conclusion survives** (S8).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9). The unproved monotonic claim had been doing the work of hiding that the control's search space contained the manipulated arm. A repair is a good place to look for a defect, not a signal that the area is now settled.
16. **An audit must use the same key its lookup uses** (S9). Comparing raw strings against a punctuation-insensitive map reported 30 punctuation differences as anatomical disagreements.
17. **A pessimistic bug announces itself; a silent one does not** (S9). The false alarms are the only reason I read the output closely enough to find last-write-wins collision handling. That is not a repeatable process — which is the argument for rules that refuse ambiguity rather than resolving it.
18. **Read the licence before designing around it, and do not let a permissive wrapper answer for a restrictive payload** (S9). The Allen terms closed the obvious route and forced a better one — the derived map is more defensible than an import would have been, and cost one session.

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). The old low-memory series was leaked Claude automation processes, not competing research; **do not reason from its shape.** Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Last reading: 2026-08-12 14:08 PDT — RAM 16.26 GiB free of 31.67 (49% in use); VRAM 953 MiB used of 16,311. Do not inherit it; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt`. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe`; never bare `python` or `pip`. **No atlas or ontology package is installed, and that is deliberate (§4.1).**

## 11. Housekeeping that is easy to get wrong

- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session.**
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **return them from a reader rather than discarding them**, so the report can state its network cost. **1 MiB blocks transfer far less than the 4 MiB default** for scattered header reads.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's; pass `--legacy-index-target CA1 --legacy-index-max-gap-um 40` for the existing index), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels` (now with the opt-in derived layer).
- **When you refactor a script another agent hardened, prove it still works.** The byte-for-byte validator diff is the pattern.
- **The resumable/pinned result files are tracked deliberately** (`host_anatomy_index.jsonl`, `host_timing_index.jsonl`, the two upstream snapshots, and now `ccf_label_map_derived_records.json`), and `.gitignore` carries a comment saying so. Do not add a blanket rule catching `Reproducibility Packet/results/`.
- **`screen_injection_placement.py --from-records`** and **`derive_ccf_label_map.py --from-records`** rewrite their reports from saved JSON with no network reads. Use them for any presentation change.
- **The processed NWB units table is rich** — 32 columns including `waveform_mean` (volts, NaN-padded), `spike_amplitudes_uV`, `cluster_uuid`, `ibl_quality_score`. **Every column carries a `description` attribute.** Read the description before using a column.

## 12. Still-open verification debt

Nothing in `references.md` *Pending* is citable: the regional waveform-duration figures, Steinmetz & Ye 2022, MEArec, and **Quirk & Wilson** (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed). If Quirk & Wilson clears, it is the natural citation for burst amplitude attenuation in Study Guide §2.2 and §3.2, which currently carry that load on Harris et al. 2001 and Pouzat et al. 2004.

**If the injection zone ever moves off CA1**, Tier C needs primary burst and amplitude-attenuation evidence for the new region and cell class, or it is labelled a synthetic stress test per Slot 13.7. Nothing on subiculum bursting is in `references.md` yet. **Also check §4.4's hierarchy point for any new zone.**
