# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 6 · 2026-08-11 21:32 PDT**
**Next session will be Claude Session 7.**

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including its new `## Amendments` section at the end. The text above that section is the same-state-approved contract and still governs; the two amendments below it are **`Proposed`** and carry no force until Codex approves the exact bytes. `Accessible Claim Sheet.md` is the same content in plain language and carries the same two amendments.

---

## 1. Where the project is

**Phase 2 — Execution.** **No scientific result exists, and no sorter has been run.** Nothing has been downloaded beyond bounded metadata range reads.

| Artifact | State |
|---|---|
| `Claim Sheet.md` | Approved text at `a5f5860…` (Session 4) + **Amendments 1 and 2, `Proposed`** (Session 6). Whole-file hash now `e2c352fd34545ac24bdf3ea10fd902262803715cd105045724fcf55b756937a9`. |
| `Accessible Claim Sheet.md` | Same, whole-file hash `1a17b4f33a05cf7ee696bc6a79e0cd299367c4aec7b5dec0294a7b84c2c47958`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 3, **`3ae39913986a1961d674d2ed7b4714f89293fa6f0e8c02f039ebca3c186696cf`**, explicitly approved by me and handed to Codex. Review still open. |

**Your progress-report counter: Session 8 is your next count-based trigger.** Session 6 closed no phase and approved no amendment, so nothing extra is owed yet. **If your session writes the approving turn on Amendment 1 or 2, you owe a progress report** — that is one of the two event triggers.

## 2. The first thing to do next session

**Open `chats/Claude-Codex/Tier A Selection Review/`.** Everything live is there. Three things are outstanding and two of them are Codex's move:

1. **The contested negative-control construction** (see §3 below). If Codex has replied holding its position, **that is two round-trips and it goes to Randy** — scoped to that one question, not the artifact. Do not loop. If Codex has accepted the counter-proposal, write the third amendment (Slot 5's Tier A implementation note) into **both** sheets in the same session.
2. **Exact-state review of Amendments 1 and 2.** If Codex approves, flip both status lines from `Proposed` to `In force` with the date of its approval, in both sheets, same session.
3. **Codex's reply on the injection-stage finding** (§5.3 below).

`chats/Claude-Codex/Compute Environment Update/` needs nothing from you unless Codex disagrees with something; I invited it to conclude that chat itself.

## 3. The one open disagreement — do not soften it and do not let it drift

**Codex proposed replacing Tier A's negative-control band with a replicate-stability band; I accepted the diagnosis and rejected the implementation.** The full argument is §8.3 of the Tier A artifact and the Session 6 chat message. The short form:

- **The problem is real and is originally mine:** the matched arm draws from 16 CA1 donors, the unaware arm from 1,149, so a same-condition pseudo pair drawn from one pool does not resemble the real contrast.
- **Codex's fix:** each pseudo block is an independently seeded replicate of the whole contrast; the band is the difference between real and pseudo interaction estimates.
- **Why I rejected it — the third reason is the load-bearing one.** (1) It stops being a *negative* control: both halves contain the manipulation, so it answers "does it reproduce?" not "can the machinery fake it?", and Slot 8 shows that band to Randy as the second question. (2) It partly duplicates the primary bootstrap. (3) **If the selection/matching machinery itself induces a systematic sorter-by-arm interaction, a replicate band shows the artifact identically in both estimates, the difference is ~0, the band looks tight, and we publish a procedural artifact as a positive result.** Nothing else in the design points at that failure, and Tier A is where it is likeliest because Tier A cannot hold donor identity fixed.
- **My counter, at identical cost:** pseudo-arm P1 draws from a *fixed random 16-template subset of the region-unaware pool* (chosen once, covariate spread approximating the CA1 sixteen, reused across all five pseudo blocks on the same rota); P2 draws from the full unaware pool, covariate-matched to P1. Neither arm conditions on region, so **Slot 5's existing wording is satisfied literally** — an implementation note, not a redefinition of the contract's strongest control. Mirrors pool size, repetition, matching and clustering.
- **The boundary I stated rather than hid:** it does not mirror the matched pool's *region* homogeneity, and no no-manipulation control can, because region homogeneity is the manipulation.

## 4. What Session 6 settled

### 4.1 Two of Codex's three rulings are accepted and are now Amendment 2

- **Host provenance is chosen, not excluded** — the host must be one of the 127 DANDI 000409 subjects absent from the donor library's twelve, which makes insertion/session/subject exclusion vacuous at once. Residual shared-dandiset/consortium/probe/strain boundary stays as a limitation. **Subject separation is not provenance independence; never let a draft imply it is.**
- **Exact donor-source blocking** attempted at insertion → session → subject before falling back to the source-*count* balance, with any relaxation reported per arm.
- **All 16 CA1 donors eligible** (the caliper is a matching diagnostic, not a filter), drawn on a **seeded exposure-balanced rota** — each appears 3–4 times across the 50 matched slots.
- **New Slot 13.9:** Tier A's donor-population statement is conditional on the complete 16-template CA1 library, **reported even if the interval is narrow**, because more blocks buy precision and cannot buy donor diversity.
- **Amendment 1** records the day/overnight machine allocation and withdraws the contention story, preserving every admission rule and moving no capacity commitment.

### 4.2 The duration gate is discharged, and it separated nobody

`screen_host_timing.py`, 11 of 11 candidates, 317.3 MB metadata-only, zero failures. Report: `Reproducibility Packet/results/host_timing_CA1.txt`.

| | |
|---|---|
| Durations | **54.2 – 87.1 min**; all pass the 10-min gate by ≥5× |
| Channels | **384 on every candidate** |
| Rates | 29,999.997 – 30,000.298 Hz, **per probe, not per session** |
| Timestamps | Constant dt to 4 decimals in µs at both ends, strictly increasing |

**Three things to carry forward.** (a) **384 channels is 4× the 96-channel feasibility run** that is the project's only proof this machine sorts anything; the reassuring ratio is that 384 ch × 10 min is 0.65× that run's sample-value count and a 60 s Rung 0 segment is 0.065× — **a data-volume ratio, not a memory measurement**, and it is Codex's pilot that settles it. (b) The two probes in one recording have **different clocks**; irrelevant now, immediate if the depth-specific-zones fallback is taken. (c) **Regular timestamps are also what a generated timestamp vector looks like** — the check shows the clock is usable, not that no samples were dropped. Do not let that get upgraded.

### 4.3 Corrections I accepted after verifying them at the source

- **The 1,401/1 label-map result is internal consistency, not independent validation.** The upstream builder takes `brain_area` from IBL's sorting metadata and the NWB electrode table is another export of the same registration. I read `upload_ibl_templates.py` myself; Codex was right and I was overclaiming.
- **"Host and donor share a preprocessing chain" was unsupported** and is removed. Donor templates come out of `common_reference(highpass_filter(phase_shift(...), freq_min=1.0))`; host raw data has had none of it. The real residual is shared *acquisition*.
- **The fallback order was wrong.** Reducing below ten injected units is not a casual first fallback; it is a contract commitment and would need a scientific amendment.

## 5. What is still not done — do not let a later session assume otherwise

1. **No host is pinned.** The artifact is a *strategy and zone recommendation*. Remaining gates: **drift, noise, post-rescaling effective SNR, ten-placement feasibility, covariate balance.** The last is Codex's and decides whether Tier A runs at all.
2. **The host survey stays at 46 of 429 (10.7%) deliberately.** Codex's ruling 7.3 — accepted — is: gate the current candidates sequentially and pin the **first fully admissible** host, called *admissible*, never *best*. Resume the survey only if all current candidates fail. Do not restart it out of tidiness.
3. **The injection-stage finding is a recommendation, not a fact.** Donor templates already carry `phase_shift` + 1 Hz high-pass + common reference. Injecting into a *raw* host and preprocessing afterwards would apply `phase_shift` twice to injected spikes and once to real ones. **Verify against the pinned SpikeInterface version before relying on it**; the anchor workflow injects into a preprocessed recording, which is presumably why nobody has been bitten.
4. **The CCF label map is materially incomplete** — 296 unmapped host structure names, 650 undefined donor acronyms. Irrelevant to a CA1 search, **blocking for the region-unaware arm's placement.** Needs an Allen ontology; **read the licences first** (Allen terms vs `iblatlas` MIT / `brainglobe-atlasapi` BSD-3). Agent work, not a director request, unless the answer needs a named exception.
5. **`audit_template_library.py` duplicates `utils/template_metadata.py`.** Resolve before packet assembly, not mid-flight.
6. **The packet still owes its own `requirements.txt`, `.gitignore` and runbook README.** The self-containment test is copying that folder alone to a clean machine; the project-root `requirements.txt` does not satisfy it. Scripts are already inside the packet, so this is Phase-3 curation, not relocation.

## 6. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 7. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`, where `G0` is the mean paired sorter gap *in the control arm*** — not the negative-control band. `[−T, T]` is declared shorthand for the `D` rule, never a second test. `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **The manipulation check is a hard stop-or-go gate.** No sorter run starts if the injected data does not demonstrably carry the property at realistic magnitude.
- **One host and injection zone across all tiers by default**; a deviation is a recorded limitation and the cross-tier comparison is dropped rather than made across hosts.
- **CA1 is the approved first zone** (Codex ruling 7.3) on the joint Tier A/Tier C constraint. Do not commission the `SUB` literature task unless CA1 fails a real gate.
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **Equal block counts give equal *nominal replication basis*, not equal precision.** Both achieved widths get reported.
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV rescaling target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first. **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 8. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (Session 4). For the Technical Report, review against a *checklist of what must be present*, not by reading.
2. **Read the column, do not count it** (Session 5). Session 2's audit was correct code answering a question one level too shallow.
3. **A check can be wrong pessimistically, and that is not the safe direction** (Session 5). Verify a self-reported problem before acting on it, to the same standard as a favourable result.
4. **A clean trend invites a causal story you have no way to check** (Session 5 addendum). Report the number; name the inference as an inference.
5. **In an owner re-review, the pull is to accept everything** (Session 6). The reviewer did real work, the edits improve things, and pushing back costs a round-trip — the playbook lists "accepting the diagnosis but silently swallowing the implementation" as a failure mode for exactly this reason. **The question that caught it: for each edit, what failure is this construction pointed at, and does the replacement still point at it?** Two of three rulings survived that question; one did not.
6. **Verify a write to an append-only file by reading it back** (Session 6). A PowerShell append wrote a chat message in the wrong encoding and mangled every em-dash and section symbol without erroring. Restored from git and re-appended with explicit UTF-8. Use `[System.IO.File]::ReadAllText/AppendAllText` with `UTF8Encoding($false)`, not `Get-Content`/`Add-Content`, and always `tail` the file afterwards.

## 9. Machine state

**The memory question is answered and the contention story is withdrawn** (Amendment 1). It was leaked finished Claude automation processes holding ~28 GiB, not competing research work; the director cleared them and a fix is being built rather than landed. **Two projects share the machine on a day/overnight split — this one runs during the day.** Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative and unchanged:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number. If free RAM collapses again with VRAM flat, that signature is known — name it rather than re-derive it.

**Last reading: 2026-08-11 21:16 PDT — RAM 12.38 GiB free of 31.67, VRAM 14,403 of 16,311 MiB. Do not inherit it; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt`. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move when they are. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe`; never bare `python` or `pip`.

## 10. Housekeeping that is easy to get wrong

- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session.** Session 6's timing run was launched in the background and finished inside the session, which is the pattern to copy.
- **`RemoteFile` now validates range responses** (Codex, Session 5) as well as retrying them (me, Session 5): a non-206, a wrong `Content-Range`, or a short body fails loudly rather than caching bad bytes or starting a full-object transfer. Reuse it for any remote NWB read rather than rolling your own.
- **The two resumable indexes (`host_anatomy_index.jsonl`, `host_timing_index.jsonl`) are append-only and tracked**, and `.gitignore` carries a comment saying so. Do not add a blanket rule that catches `Reproducibility Packet/results/`.

## 11. Still-open verification debt

Nothing in `references.md` *Pending* is citable: the regional waveform-duration figures, Steinmetz & Ye 2022, and **Quirk & Wilson** (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed). If Quirk & Wilson clears, it is the natural citation for burst amplitude attenuation in Study Guide §2.2 and §3.2, which currently carry that load on Harris et al. 2001 and Pouzat et al. 2004.

**If the injection zone ever moves off CA1**, Tier C needs primary burst and amplitude-attenuation evidence for the new region and cell class, or it is labelled a synthetic stress test per Slot 13.7. Nothing on subiculum bursting is in `references.md` yet.
