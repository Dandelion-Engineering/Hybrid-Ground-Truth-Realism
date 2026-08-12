# Human Report 7 — Claude

**Date and time:** 2026-08-12 10:14 PDT
**Session:** Claude Session 7
**Phase at start:** Phase 2 — Execution
**Phase at end:** Phase 2 — Execution. Claim Sheet **Amendments 1 and 2 are `In force`**; **Amendments 3 and 4 are `Proposed`** and await Codex's exact-state approval. The Tier A selection artifact is at Draft 4. **No host is pinned, no sorter has run, and no scientific result exists.**

---

## Summary

Four things happened this session, and the second one was not planned.

1. **Amendment 2 closed.** I performed the owner re-review of the exact bytes Codex handed back and approved them, flipping the amendment to `In force` in both Claim Sheets.
2. **Checking one sentence in that amendment turned into a finding.** Codex had removed two unverified provenance claims. Rather than accept the removal on the argument, I read the substrate — and found that the claim was not weakly supported but *unverifiable*, that host and donor recordings separate at the **laboratory** level, and that the entire donor library is **one laboratory's work**. That is now proposed Amendment 4.
3. **Amendment 3 was written** to Codex's seven stated requirements, settling the negative-control band construction the previous session left open.
4. **The placement gate was applied** to all thirteen candidate injection zones — the last metadata-only gate standing between the project and a pinned host. Label ambiguity came back clean on every candidate; placement capacity separates nine passes from four failures and turns out to hinge on a number nobody has measured.

Two scripts, one shared module, four result files, one progress report. **170.2 MB + 88.7 MB of network reads, all file metadata, no recording data, no sorter, no dependency installs.**

---

## 1. Amendment 2 — the owner re-review

Codex approved Amendment 2's substance in its Session 6 but edited two claims before doing so, so the amendment stayed `Proposed` pending my re-review of the exact bytes. The edits removed "one mouse strain" from the technical sheet, and "same rig design / same mouse strain" from the Accessible one, on the grounds that the evidence ledger established neither.

The lesson I recorded last session was that in an owner re-review the pull is to accept everything, and the question that resists it is *what failure is this construction pointed at, and does the replacement still point at it?* The construction here is a limitation sentence whose job is to stop any artifact of this project implying that host and donor are independently sourced. Codex's replacement still does that. But a limitation list that stops mentioning strain reads, to a careful reader, as though strain had been checked and found different — **removing an unverified claim can quietly create a new one in the opposite direction.**

So I went and checked, which cost 89 MB and about ten minutes.

**Approved:** both sheets at Codex's handed-back states, `8d06e588…` and `9bb0478f…`. The only change I made to that text is the status line.

---

## 2. What the check found — proposed Amendment 4

`Reproducibility Packet/scripts/audit_subject_provenance.py` reads `/general/lab`, `/general/institution`, `/general/protocol`, `/general/subject` and `/general/ibl_metadata` from one raw NWB per subject, over range requests. 21 subjects — the donor library's 12 and the 9 owning the current host candidates. **88.7 MB in 91 requests, metadata only, zero failures.** Report: `Reproducibility Packet/results/subject_provenance.txt`.

| Finding | Consequence |
|---|---|
| **No `genotype`, `strain` or `description` field exists in these files** | The claim is *unverifiable*, not unsupported. No artifact may report strain as shared or as different, in either direction. |
| **All 12 donor subjects are `cortexlab`, University College London** | The entire Neuropixels 1.0 donor library — both Tier A arms — is one laboratory's work. |
| **All 9 candidate host subjects are `churchlandlab` (CSHL, 3) or `angelakilab` (NYU, 6)** | Zero overlap with the donor laboratory. Task-protocol versions differ across the two sides inside one iblrig family. |

The two consequences point opposite ways and both belong in the record.

**The contract understates the separation.** Amendment 2's rule — pick a host from one of the 127 subjects that contributed no donors — turns out to separate host from donor at **laboratory, institution and rig**, not only at the animal. Nobody designed that; it falls out of the donor library happening to be entirely one lab's and none of the CA1 candidates being from that lab. It is now checkable rather than assertable.

**The substrate understates a limitation.** Slot 13.9 (from Amendment 2) conditions a Tier A result on the sixteen CA1 templates but says nothing about their origin. They are one lab's rigs, one lab's insertions, one lab's curation. Amendment 4 adds **Slot 13.10** for that.

**Boundary, stated in the amendment rather than discovered later:** one asset per subject was read, so `lab` is verified for the session read, not independently for every session that subject appears in. In IBL a subject belongs to one lab, so the generalization is safe in practice — but the evidence is per-asset.

**It is not a gate.** Every current candidate already satisfies it, so it separates none of them, exactly as the duration gate separated none of them. Recorded so a later host search knows the property was checked rather than inherited.

---

## 3. Amendment 3 — the negative-control band

Codex accepted my Session 6 counter-proposal and withdrew its replicate-stability construction, agreeing that a repeat of the real contrast would reproduce a systematic selection artifact as faithfully as a real effect and make the band look reassuringly tight while the project published a procedural artifact. But it disagreed that this was an implementation note: Slot 5 says pseudo-arms use the "same selection and generation procedure," and P1/P2 deliberately use asymmetric pools. It asked for a synchronized amendment with seven specific contents.

Amendment 3 delivers all seven — pinned subset-selection seed and objective, exposed template identifiers, the exposure-balanced rota, P2 matched to P1 by the real-arm procedure, neither arm conditioning on region, the two-pseudo-arm budget preserved, and the region-homogeneity boundary named. It is Tier A-only; Tiers B and C hold donor identity fixed, so their pools are symmetric and Slot 5's original construction still applies to them.

**One thing I added that Codex did not ask for.** Because Tier A's band and Tiers B/C's bands are now built differently, the Slot 8 verification panel's caption and the Technical Report must **name the construction shown** rather than describing all three bands with one sentence. My original objection to the replicate band was that one grey band would come to mean two different things in one report; that failure comes back through the figure caption if nothing blocks it there.

Amendment 3 also states that Amendment 2's generation prohibition is discharged **when Amendment 3 reaches `In force`, and not before.** Amendment 2's text is not rewritten.

---

## 4. The placement gate

The Claim Sheet's Slot 7 has carried this since it was written: *"If ten feasible placements cannot be supported without overcrowding or label ambiguity, that host fails the Tier A gate rather than having a convenient whole-recording label invented for it."* It is now applied to all 13 candidate bands.

`Reproducibility Packet/scripts/screen_injection_placement.py`, **170.2 MB in 169 requests, metadata only, zero failures**. Per band it reads the raw file's electrodes table and the matching processed file's `units` table — IBL's own Kilosort 2.5 sorting, which nobody on this project had opened before.

### Label ambiguity: closed, cleanly

**All 13 bands are 100% pure.** Every contact inside every band's depth range carries the CA1 label; the nearest differently-labelled contact is 20 µm — one contact row — beyond each edge on all of them. The 40 µm gap tolerance never admitted a foreign structure. The recomputed band matched the indexed band exactly in all 13, and the raw and processed electrode tables agree contact-for-contact in all 13 (Session 5 had verified that equality on one session; it now holds on all of them).

### Placement capacity: nine pass, four fail, and the verdict is parameterized

An injected template has spatial extent, so its peak must sit far enough inside the band for its footprint to land in labelled CA1, and peaks must be far enough apart to be ten placements rather than one crowded one. At **60 µm edge margin and 40 µm minimum separation**, nine bands hold ten units and four do not (spans 420–460 µm).

**Both numbers are declared, not measured.** The donor templates' real multichannel footprint needs the template arrays from the upstream zarr store, which this screen does not download. So the report carries a full sweep — and the sweep is the finding: at a 100 µm margin only **five** bands hold ten, and at 140 µm only **two**. **Measuring the donor footprint is now the highest-value remaining piece of Tier A selection work**, because it converts this gate from parameterized to decided. I flagged it to Codex rather than simply taking it, because if Rung 0 pulls templates through SpikeInterface anyway, measuring extent there is nearly free while doing it myself costs a separate zarr reader.

### Overcrowding: measured for the first time, deliberately not gated

The Claim Sheet caps injected units at ten because more of them change the recording's own collision and density statistics. That is a density argument, and the project had no density measurement. IBL's sorting of the same bands supplies one: ten injected units are **+3.7% to +45.5%** of the native cluster count, or **+17% to +1000%** of the `good`-labelled count.

I did not gate on it. The Claim Sheet fixes no overcrowding threshold, and a screening script is not the place to invent one — a design parameter buried in code is exactly the failure mode this project's review discipline exists to catch. I proposed to Codex that we decline to set a fixed percentage and instead treat native yield as a named admission consideration alongside drift and noise.

### Two things that fell out sideways

**NYU-39 Probe00 should be dropped, and the placement gate is not the reason.** Its CA1 band holds 22 sorted units, **one** labelled `good`, against 174 and 32 in a comparable CSHL047 band. It passes the geometric gate at exactly ten sites. A zone where the field's own sorter recovers one well-isolated unit is not a zone where ten injected units can be judged against a realistic neighbourhood. That is *yield* evidence, not a noise measurement — but it arrived free and it is decisive.

**The 50–200 µV rescaling target survives contact with the host, for well-isolated units.** Median amplitude across all sorted units in these bands runs 20–60 µV; across `good` units only it runs 51–110 µV with p90 reaching 258 µV. **The caveat is load-bearing:** that column is IBL's `median_spike_amplitude_uV` computed on IBL's preprocessed data, and whether its convention matches the donor library's `amplitude_uv` has not been verified. It is a flag telling us to run that check, not the check.

### One shortcut found and rejected

The processed files carry a column named `cumulative_drift_um_per_hour`, which would have been a free answer to the open drift gate. Its values reach ~6.5 × 10⁶ µm/hour, which is not physically possible for a probe in a mouse brain, so whatever it accumulates it is not net drift. It is recorded as uninterpreted and used for nothing. **Drift remains open**, and a later session that rediscovers the column will find the note rather than trusting the name.

---

## 5. Engineering

**A refactor, because the alternative was a second copy.** `read_electrode_table` and `contiguous_band` moved out of `survey_host_anatomy.py` into a new `utils/host_anatomy.py`. The placement screen must compute the band with the *same* implementation as the survey that ranked it, or it measures a different band than the one under consideration. **Validation: the anatomy survey replayed from its index with `--limit 0`, zero new remote reads, and reproduced `host_anatomy_CA1.txt` byte-for-byte.** Codex's `anatomy_index` provenance assertions still fire; I passed the legacy flags.

**A `--from-records` mode** on the placement screen rewrites the report from saved JSON with no network reads, so a presentation change never costs another 170 MB. I used it once already, to add a column.

**One bug caught in a smoke test**, which is why the smoke test existed: the screen initially built its asset reference from the anatomy index's record, which carries no blob identifier, so the first candidate failed loudly at the URL construction rather than silently reading nothing. Fixed by looking the asset up in the pinned listing and failing hard if the index and the listing disagree.

---

## 6. Challenges and reasoning paths

**Deciding not to gate on the density number was harder than computing it.** Having measured something genuinely new, the pull is to use it — to declare a threshold and let the screen return a cleaner verdict. But the Claim Sheet does not fix an overcrowding threshold, and putting one inside a script would make a design parameter invisible to review. Reporting the measurement and asking for the decision is slower and correct.

**The "sideways" findings were the most valuable per byte, and neither was the point of the screen.** NYU-39's single well-isolated unit and the amplitude comparison both fell out of a table opened for a different reason. Worth noticing as a pattern: reading a rich first-party table costs about the same as reading one column of it.

**I nearly used a column because of its name.** `cumulative_drift_um_per_hour` would have discharged an open gate for free. Checking the magnitude took thirty seconds and showed the name does not describe the values. This is the third time in this project that a plausible-looking shortcut failed a cheap verification, and the pattern is worth carrying: verify a favourable result to the same standard as an unfavourable one.

**I did not resolve the CCF label-map gap**, which was one of the open items I inherited. It is blocking for the region-unaware arm's placement and needs an Allen ontology whose licence has to be read before it is imported. It stayed open because the placement gate was on the critical path and the ontology question is not. Recorded rather than quietly dropped.

---

## 7. Machine state

Measured immediately before the only sustained step: **RAM 17.19 GiB free of 31.67 (45% in use); VRAM 826 MiB used of 16,311.** Nothing this session was heavy — the peak working set was a few thousand table rows — but the measurement is recorded so the next session inherits evidence rather than a hunch. No dependency was installed; the venv still holds only `h5py==3.16.0` and `numpy==2.5.2`.

---

## 8. Files created or updated

| Path | Change |
|---|---|
| `Claim Sheet.md` | Amendment 2 → `In force`; **Amendments 3 and 4 appended** as `Proposed`. New whole-file SHA-256 `a43eb4f686cb5baed399ef07151cc37dff27b2d983e1bfa1a5d0465a59b96fba`. |
| `Accessible Claim Sheet.md` | Synchronized in the same session. SHA-256 `71eedf5eee9b3bd64ab93077695cc9c622fd78d8a466c3e35599fa1f065d2134`. |
| `Reproducibility Packet/scripts/audit_subject_provenance.py` | **New.** Reads acquisition provenance for named subjects from their own NWB headers. |
| `Reproducibility Packet/scripts/screen_injection_placement.py` | **New.** Applies the Slot 7 placement and label-ambiguity gate; reports capacity sweeps and native unit density. |
| `Reproducibility Packet/scripts/utils/host_anatomy.py` | **New.** Shared electrode-table reader and contiguous-band finder. |
| `Reproducibility Packet/scripts/survey_host_anatomy.py` | Refactored onto the shared module; replay reproduces its report byte-for-byte. |
| `Reproducibility Packet/scripts/utils/__init__.py` | Documented the new module. |
| `Reproducibility Packet/results/subject_provenance.txt` · `.json` | **New.** 21 subjects' lab/institution/protocol, and the absent-field finding. |
| `Reproducibility Packet/results/injection_placement_CA1.txt` · `.json` | **New.** 13 bands, purity, capacity sweep, native density and amplitude. |
| `Reproducibility Packet/results/host_anatomy_CA1.txt` | Regenerated identically by the refactor validation. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 4** — new §9 (provenance) and §10 (placement gate). §1–§8 unchanged. SHA-256 `c3303cf35837120d22af4a992a2e8d1357d983c9243812173f7484bcd3763113`. |
| `agents/Claude/references.md` | New entry for the processed files' `/units` table and `/general` metadata, with the drift-column negative and the amplitude-convention caveat. |
| `agents/Claude/Progress Reports/Progress Report Amendment Provenance and Finite Donor Pool.md` | **New.** Amendment-triggered director report. |
| `chats/Claude-Codex/Tier A Selection Review/…Active.md` | Two appended messages: the amendment turn, and the placement result with the Draft 4 handoff. |
| `README.md` (Live-Run) | Banner date updated; one appended log entry covering the provenance finding and the placement gate. |
| `agents/Claude/Session Summaries/HumanReport7.md` | This report. |

`agents/Claude/README.md` and `Summary of Only Necessary Context.md` are refreshed after this report, as closeout requires.

---

## 9. Next steps

1. **Codex's exact-state review of Amendments 3 and 4.** Amendment 3 blocks Tier A generation until it is `In force`.
2. **Measure the donor templates' multichannel footprint.** It decides the placement verdict and is the cheapest thing standing between the project and a pinned host. Ownership is an open question I put to Codex.
3. **Whether to set an overcrowding threshold or decline to.** My proposal is to decline and treat native yield as a named admission consideration.
4. **Drift and noise on the leading candidates**, which need Rung 0's stack.
5. **The CCF ontology licence question**, still open, still not blocking CA1.
6. **Verify the amplitude convention** between IBL's `median_spike_amplitude_uV` and the donor library's `amplitude_uv` before the rescaling target is treated as validated.

Nothing is blocked on the director. There are no open items in `director_requests.md` that need him.
