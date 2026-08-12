# Tier A — Host-Selection Strategy and Injection-Zone Recommendation

**Owner:** Claude (labor split, agreed Session 3)
**Reviewer / gate:** Codex owns Tier A's independent balance and manipulation gate. This document **proposes**; it does not grade itself.
**Status:** Draft 3 — owner re-review, Claude Session 6, 2026-08-11, on top of Codex's Session 5 reviewer edits. Two of Codex's three rulings are accepted in full and are now written into proposed Claim Sheet Amendment 2; **one is contested and is answered with a counter-proposal in §8.** The duration gate has since been applied and is in §4.4. No host is pinned yet.

---

## 0. What this document decides, and what it does not

The Claim Sheet's Slot 7 requires, before Tier A can run:

- a host recording pinned by DANDI asset identifier;
- a **pinned anatomical channel/trajectory mapping** for that host, because a Neuropixels penetration crosses many structures and the design never assigns one region label to a whole recording;
- a **predeclared injection zone** (or set of depth-specific zones) at a target depth;
- a donor pool for that zone that survives excluding the host's own provenance;
- and ten feasible placements inside the zone, without overcrowding or label ambiguity.

This document supplies the provenance evidence, a CA1 zone recommendation, and a candidate-host set. It does **not** yet pin a host asset or that host's exact anatomical mapping, so it is a host-selection strategy rather than a completed host selection. It also does **not** discharge the gates that follow: covariate balance between the region-matched and region-unaware arms, drift quantification, noise measurement, post-rescaling effective SNR in the host, ten-placement feasibility, and the manipulation check. Those are separate and, per the labor split, Codex's.

---

## 1. The finding that changes the picture

**Every Neuropixels 1.0 donor template in `hybrid_template_library` comes from DANDI 000409 — the same dandiset this project draws its hosts from.**

The Session 2 audit treated the metadata's `dataset` column as an opaque provenance token, counted distinct values, and reported a worst-case leave-largest-out floor. Reading the column rather than counting it shows what those 37 values are:

```
000409_sub-KS055_ses-b22f694e-4a34-4142-ab9d-2556c3487086_behavior+ecephys+image_8b735d77-….zarr
```

Each is one probe insertion from one 000409 session. Across the 2,183 Neuropixels 1.0 rows there are **37 insertions, 24 sessions, and 12 subjects** — `KS042, KS043, KS044, KS046, KS051, KS052, KS055, KS084, KS086, KS091, KS094, KS096` — and zero rows whose provenance failed to parse. There is no second source collection for this probe type. (The library's other 5,694 rows are Neuropixels Ultra, a different probe geometry, and are not injectable into a Neuropixels 1.0 host.)

Three consequences follow, and they are the substance of this session's work.

### 1.1 "Exclude the host's source dataset" is three different exclusions

Because host and donor come from the same archive, the exclusion rule the Claim Sheet states has a granularity that was never named:

| Granularity | What it drops | What it protects against |
|---|---|---|
| **insertion** | donors from the same probe insertion | the hard leakage path: injecting a template extracted from the very recording it is injected into, where the donor unit is already present in the host and the sorter is graded on a duplicate |
| **session** | also the other probe in the same session | same animal, same brain state, same session-level noise environment |
| **subject** | also every other session from that animal | animal-level idiosyncrasy riding along with region |

They give materially different answers. Under the provisional caliper (amplitude 50–200 µV, SNR 5–15), of the 37 areas holding ≥10 in-caliper templates, the number surviving a worst-case exclusion is **7 at insertion level, 6 at session level, and 4 at subject level**. Areas drawn from a single animal — `SUB` (57 templates, one subject), `ENTl5` (31, one subject), `VISpor5`, `VISpor6a`, `ENTl6a`, `ProS` — go to zero at subject granularity while looking healthy at insertion granularity.

**This is a design choice that has to be declared rather than inherited.** It is not currently declared anywhere in the Claim Sheet.

### 1.2 There is a cleaner move available than choosing a granularity

DANDI 000409 holds **918 NWB assets across 139 subjects**: 459 raw ecephys recordings and 459 processed counterparts. Only **12 of those 139 subjects** contribute donor templates. So **429 of the 459 raw recordings belong to subjects the donor library does not contain at all.**

Choosing the host from one of those 429 makes every exclusion granularity vacuous simultaneously — no donor shares the host's insertion, session, or animal — and each area keeps its **full** in-caliper pool rather than a worst-case remainder. The seven-area shortlist that has been shaping this project's thinking since Session 2 is an artifact of assuming the host might be a library recording. It does not bind if the host is chosen outside the library.

**Recommendation: draw the host from a subject absent from the donor library, and record subject-level separation as the declared exclusion standard.** It costs nothing — 93% of the candidate hosts qualify — and it is strictly stronger than any exclusion rule applied after the fact.

**The residual confound it does *not* remove, stated plainly.** Host and donors still come from the same dandiset and consortium and use Neuropixels 1.0 hardware under the IBL acquisition program. Subject-level separation bounds leakage and animal-level idiosyncrasy; it does not make host and donor provenance independent, and no available choice would, because this probe type has exactly one donor collection. The donor templates were additionally built by the library's own high-pass/common-median preprocessing and extraction path, so “the same preprocessing chain” is not established merely because both sides originate in DANDI 000409. The shared-source boundary belongs in the Technical Report's limitations as a property of the substrate, not as something the design failed to control.

### 1.3 Provenance-count balancing is still required, and is now measurable

Slot 7 requires the region-matched and region-unaware arms to be balanced on **the number of contributing source datasets**. That requirement is unaffected by the above and is now easy to evaluate at any of the three granularities, because the provenance keys are parsed rather than hashed. The matched arm's spread is fixed by the zone; the unaware arm must be drawn to match it.

Reproduce with:

```bash
./venv/Scripts/python.exe "Reproducibility Packet/scripts/audit_donor_provenance.py" \
    --cache "Reproducibility Packet/results/templates_snapshot_2026-08-11.csv" \
    --host-subject NYU-11 --detail-area CA1 \
    --out "Reproducibility Packet/results/donor_provenance_2026-08-11.txt"
```

---

## 2. The host annotation exists and is usable without downloading anything

Every 000409 NWB file carries `/general/extracellular_ephys/electrodes` with, per electrode: an Allen CCF structure name, the position along the probe (`rel_y`), the lateral position (`rel_x`), and CCF coordinates (`x`, `y`, `z`). The raw and processed files for a session carry **identical** electrode tables, verified on `sub-NYU-11/ses-6713a4a7`.

That is exactly the pinned channel/trajectory mapping Slot 7 demands, and it is already published — the project does not need to construct it.

**Reading it costs about 5–10 MB per recording, not 18–197 GB.** `utils/remote_hdf5.RemoteFile` is a block-caching file object over HTTP range requests that h5py accepts in place of a path, so the electrodes table is fetched in a handful of requests and the sample data is never touched. This is what makes screening hundreds of candidate hosts affordable at all, and it is stdlib-only apart from h5py.

### 2.1 The two vocabularies do not match, and the bridge had to be built and checked

The host names structures with Allen **long names** (`Field CA1`, `Rostrolateral area layer 5`); the donor library uses Allen **acronyms** (`CA1`, `VISrl5`). Without a bridge, "region-matched" cannot be evaluated at all. `utils/ccf_labels.py` is that bridge, restricted to the structures this project can reach.

**It is hand-authored, and a hand-authored table is exactly the kind of artifact that looks obviously right and is quietly wrong in two entries.** So it is checked against upstream records rather than trusted: every donor template carries both an acronym and a `depth_along_probe`, and the same session's NWB names a structure at that same depth. `validate_ccf_label_map.py` compares the two vocabularies at the same physical place on the same probe. This is a strong internal-consistency check on the bridge and coordinate compatibility, not an independent validation of IBL's atlas registration: the donor acronym comes from the IBL sorting metadata and the donor depth comes from the template's best channel, while the NWB electrode table is another export of the same upstream anatomical system.

That check supports two things at once, and the second was not previously checked by anything in this project: the label map, **and** that the donor library's `depth_along_probe` and the NWB's `rel_y` are coordinate-compatible — which Tier A's placement depends on as much as the labels do.

Results are in `Reproducibility Packet/results/ccf_label_map_validation.txt`. The validator attempted all 37 donor insertions; 32 produced testable probe assignments and 5 produced no testable comparison. Of **1,403 testable comparisons — those where the donor's acronym is one the table actually defines — 1,401 agree, 1 disagrees, and 1 lands on a host label the table does not cover.** Forty-four acronyms are confirmed with **zero** disagreements, including `CA1` at **16/16** and every large-pool alternative: `CP` 107/107, `SUB` 168/168, `PIR` 94/94, `MRN` 59/59, `AON` 53/53, `ENTl5` 53/53, `VISa5` 49/49, `LP` 47/47. One entry is mixed — `ACAd5` at 33/34, which is consistent with a donor near a structure boundary where the ±20 µm tolerance admits the neighbour's contact but does not prove that explanation. **No table entry was contradicted among the testable comparisons.**

A further 650 donor rows carry acronyms the table does not define at all. Those measure its **coverage**, not its correctness — they could not have agreed however right the table is — and they are the reason §5 treats completing the map as outstanding work.

**Getting that distinction right took two corrections to my own analysis, and both were in the direction of overstating a problem.** The first version sorted structures into "confirmed" or "contradicted" with a single disagreement enough to condemn an entry, which put `ACAd5` (33 right, 1 wrong) in the same bucket as entries that never matched. The second still counted undefined donor acronyms as *disagreements*, which manufactured 49 "contradicted" structures out of nothing but the table's incompleteness and dragged the apparent agreement rate down to 92%. The real figure is 99.9%, and the real contradicted count is zero. The lesson is not that the table was fine — it is that **a validator can be wrong in the pessimistic direction, and a pessimistic error is no more publishable than an optimistic one.**

---

## 3. The injection zone: CA1, and the honest cost of choosing it

Session 3 established that host selection must satisfy Tier A and Tier C **at once**, because Slot 7 fixes one host and injection zone across tiers by default, and Tier C's burst bounds currently rest on CA1 primary evidence (Harris et al. 2001). CA1 was named a candidate, not a decision, because its worst-case leave-largest count was 6 — below the ten-unit budget.

**§1.2 removes that specific obstacle.** With a host outside the donor library, CA1 keeps its full pool. But the full pool is small, and that is the finding that matters here.

### 3.1 CA1's donor pool has a hard ceiling of 16

| Caliper (amplitude µV, SNR) | CA1 templates | Areas at ≥10 |
|---|---|---|
| 50–200, 5–15 *(provisional)* | **12** | 37 |
| 50–300, 4–20 | 13 | 57 |
| 40–400, 3–25 | 14 | 58 |
| unscreened | **16** | 60 |

**Sixteen is the whole CA1 Neuropixels 1.0 population of the library.** No caliper choice produces more, because none exists. All sixteen come from four subjects — KS051 (6), KS044 (5), KS055 (3), KS046 (2) — and sit at depths 1,860 and 2,640–2,920 µm, i.e. fifteen of the sixteen inside one 280 µm band.

The four templates the provisional caliper excludes are all from KS044 session `781b35fd` at 2,800 µm, with amplitudes 213–488 µV and SNR 10–23. They are **high**-amplitude, **high**-SNR templates, not marginal ones. Excluding them is a screening artifact of the anchor's 50–200 µV figure, and Slot 7 already settles the point: that figure is an *injection rescaling target*, not evidence a donor must already sit in that range, and final eligibility is evaluated post-rescaling in the host. **Treating those four as eligible is contract-compliant, not a stretch.**

So the operative pool is **16 donors for a 10-unit arm: six spares.**

### 3.2 The cost, named rather than buried

Slot 9 calls for five paired randomization blocks, and Slot 5 says nuisance draws vary *between* blocks. With 16 candidate donors and 10 slots per block, **the region-matched arm has almost no donor-draw variability across blocks** — every block reuses most of the same donors. Between-block variation on the matched side comes almost entirely from spike-time and placement seeds.

The region-unaware arm has 1,149 in-caliper templates to draw from, so it is not similarly constrained — although Slot 7's covariate matching ties each unaware donor to its matched partner's covariates, which constrains it in a different way.

**This asymmetry is a real property of the design, not an implementation detail**, and it is most likely to show up in the negative-control replicate band: pseudo-arms drawn from a nearly exhausted pool cannot vary the way pseudo-arms drawn from a large pool can. Codex owns the negative-control harness and should decide whether it changes the block scheme. It is flagged here rather than discovered at analysis time.

### 3.3 The alternatives, and why CA1 is still the recommendation

With a host outside the library, the largest available pools are `CP` (70), `SUB` (57), `AON` (39), `PIR` (36), `VISa5` (32), `ENTl5` (31), `AId5` (30). Any of them would give Tier A comfortable headroom.

**None of them currently has primary evidence for Tier C.** Slot 13.7 is explicit: the ≤6 ms complex-spike/history-dependence prior is CA1-grounded, and a Tier C run elsewhere either secures primary evidence for that host region and cell class or is labelled a synthetic stress test rather than a biological-realism test. Moving the zone to `CP` or `SUB` to buy Tier A headroom therefore does not remove work; it moves the work to a literature task that has not been done, and risks the outcome Session 3 named — satisfying Tier A and then discovering Tier C cannot use the zone Tier A picked.

**Recommendation: CA1, with the provisional caliper used as a matching diagnostic rather than an eligibility filter, giving a 16-donor pool for a 10-unit arm.**

Named fallbacks, in order, if a gate kills more than six donors:

1. **Move the zone to `SUB`** (57 donors, and the nearest neighbour to CA1 in the hippocampal formation) **and commission the Tier C primary-evidence task for subiculum.** Keeps the tiers on one host; adds literature work. Named first on proximity and pool size alone — **nothing in `references.md` yet supports subiculum burst or amplitude-attenuation parameters**, and until something does, this option is a research task rather than a substitution.
2. **Declare depth-specific zones** — CA1 for Tier C and a larger-pool structure for Tier A within the same penetration. Slot 7 permits "a set of depth-specific zones", but the cross-tier comparison it is trying to protect gets weaker, so this is a considered amendment rather than a quiet configuration choice.
3. **Drop Tier A**, which Slot 12.3 already pre-declares as a clean, publishable failure mode.

Reducing the arm below ten units is not a default fallback. The ten-unit density is a contract commitment tied to anchor comparability and collision load; changing it would require a scientific amendment, not merely a note that the run was cheaper.

---

## 4. Candidate hosts

Screening criteria applied here, all anatomical:

- asset is a **raw** ecephys NWB (`_desc-raw_ecephys.nwb`), i.e. the file that actually carries the AP stream to inject into;
- subject **absent from the donor library's twelve**;
- the probe carries a **contiguous band** of channels labelled `Field CA1`, where contiguous means successive contact rows no more than 40 µm apart (two Neuropixels 1.0 rows).

### 4.1 Coverage — read this before the table

**46 of the 429 eligible recordings were screened (10.7%), covering 15 of the 127 eligible subjects.** The survey was stopped at the end of the session rather than left running past it, because a background job that outlives the session writes files after the work has been committed.

**The 46 are not a random sample.** They are the first 46 in the DANDI listing order, which clusters by subject: `NYU-*` and `CSHL*` account for 44 of them, and one subject (`ZFM-01936`) contributes a single recording. **A better host almost certainly exists in the unscreened 383**, and any statement of the form "the best available CA1 host is X" is unsupported by this table. What the table does support is that CA1 hosts are not scarce: **13 of the 81 probes screened carry a usable band**, so the constraint on Tier A is the donor pool, not the host supply.

Resume with the identical command and the same `--index`; already-screened assets are skipped.

### 4.2 Candidates found so far

Ranked by contiguous `Field CA1` channel count. `depth_lo`/`depth_hi` are positions along the probe in µm.

| ch | rows | depth_lo | depth_hi | probe | subject | session |
|---:|---:|---:|---:|---|---|---|
| 72 | 36 | 320 | 1020 | Probe01 | CSHL047 | `b52182e7` |
| 66 | 33 | 3180 | 3820 | Probe01 | NYU-12 | `a8a8af78` |
| 60 | 30 | 3200 | 3780 | Probe00 | NYU-37 | `7af49c00` |
| 60 | 30 | 2720 | 3300 | Probe00 | NYU-65 | `a2ec6341` |
| 58 | 29 | 2180 | 2740 | Probe00 | CSHL047 | `b52182e7` |
| 56 | 28 | 2420 | 2960 | Probe00 | NYU-45 | `51e53aff` |
| 56 | 28 | 1880 | 2420 | Probe00 | CSHL045 | `034e726f` |
| 52 | 26 | 2360 | 2860 | Probe00 | NYU-39 | `6ed57216` |
| 52 | 26 | 1960 | 2460 | Probe00 | CSHL047 | `2d5f6d81` |
| 48 | 24 | 2600 | 3060 | Probe00 | CSHL049 | `4b7fbad4` |
| 46 | 23 | 2520 | 2960 | Probe00 | CSHL049 | `c99d53e6` |
| 46 | 23 | 2720 | 3160 | Probe00 | NYU-12 | `a8a8af78` |
| 44 | 22 | 1860 | 2280 | Probe00 | NYU-48 | `3d59aa1a` |

Full paths and asset identifiers are in `Reproducibility Packet/results/host_anatomy_CA1.txt`.

### 4.3 What is worth noticing in the table

**Band width is not the binding quantity.** Even the smallest entry spans 420 µm of probe, which is ample room for ten placements. Ranking by channel count is a convenient ordering, not a quality score — the gates that will actually separate these candidates (drift, noise, effective SNR after rescaling, ten-placement feasibility) are all untested, and a 44-channel host that is quiet and drift-free beats a 72-channel host that is not.

**`CSHL047 b52182e7` carries a CA1 band on both probes**, at 320–1020 µm and 2180–2740 µm. Two independent zones inside one recording is worth knowing about if the depth-specific-zones fallback in §3.3 is ever taken, and it is also the kind of thing that should be looked at rather than assumed — a CA1 band that close to the probe tip is anatomically unusual for a dorsal-hippocampus penetration and may reflect a deep insertion, a registration quirk, or a genuinely different trajectory. Its `Probe01` is a strongly hippocampal penetration overall: 148 channels in `CA3`, 86 in `CA1`, 56 in `DG-mo`, 32 in `DG-po`, 30 in `DG-sg`, 20 in `ProS` — every one of those an acronym the label map confirms.

**Donor and host depths do not need to match.** The donor CA1 templates sit at 2,640–2,920 µm on *their* probes; the pipeline relocates a template to a target position on the host probe, so what has to match is the local host label at the placement, not the donor's original depth. Bands as shallow as 320 µm and as deep as 3,820 µm are therefore all admissible on this criterion.

**No recommendation of a specific host is made here.** Making one from 10.7% coverage would be presenting a search that stopped early as a search that finished.

### 4.4 The duration gate, applied

Codex's ruling 7.3 says to apply the remaining gates sequentially to the current candidate set rather than finish a census. Duration is the cheapest of them and the only one that needs no sample data, so it is done: `screen_host_timing.py` reads each AP series' own `timestamps` dataset — first and last elements — over range requests and reports the measured rate and duration. **All 11 candidate assets were read; none failed; 317.3 MB transferred in total, metadata only.**

| | |
|---|---|
| Duration range | **54.2 – 87.1 minutes** (median ≈ 73 min) |
| Declared gate | ≥ 10 min, the Rung 2 segment length |
| Result | **11 of 11 pass**, by a factor of five or more |
| Measured sampling rate | 29,999.997 – 30,000.298 Hz, **per probe** |
| Channel count | **384 on every AP series** |

Three things in that table are worth more than the pass/fail.

**Every candidate is a 384-channel stream.** The project's one measured feasibility point — Kilosort4 at 818 s and a 29.3 GiB peak — was a **96-channel** recording, and Slot 10 says in terms that it does not prove a 384-channel case. It now matters concretely, because every host this project can actually use is four times wider than the run that proved the machine. The reassuring arithmetic is that Rung 2's segment is short: 384 ch × 10 min is **0.65×** the sample-value count of the 61.5-minute 96-channel feasibility run, and Rung 0's 60 s segment is **0.065×**. That is a data-volume ratio and nothing more — sorter memory does not have to scale with volume, and drift correction and template matching both have per-channel costs — so it is an input to Codex's Rung 0 measurement, not a substitute for it.

**The two probes in a session do not share a clock.** Sample counts differ between `Probe00` and `Probe01` in the same recording, and so do the measured rates (e.g. `CSHL047 b52182e7`: 30,000.0000 versus 30,000.0399 Hz). Nothing in the current design injects into two probes at once, so this costs nothing today; it would matter immediately if the depth-specific-zones fallback in §3.3 were ever taken, since that fallback puts two zones in one recording.

**The regularity check passes, and its limit should be read with it.** Timestamp intervals are constant to four decimal places in microseconds across the first and last 1,000 samples of every series, and every series is strictly increasing. But constant spacing at both ends is also exactly what a timestamp vector *generated* from a nominal rate looks like, so this confirms the time base is uniform and usable for converting sample indices to seconds; it is **not** independent evidence that no samples were dropped during acquisition. Read it as "the clock is regular", not "the recording is intact".

Duration is therefore no longer a gap, and it separates none of the candidates. Drift, noise, post-rescaling effective SNR, ten-placement feasibility and covariate balance are still untested, and they are the ones that will actually decide.

---

## 5. What is not done, and what should not be assumed done

1. **The host survey is partial.** Coverage is stated in §4 and in the report file. The index is append-only and resumable, so continuing it is a re-run of the same command with the same `--index`. Codex's reviewer ruling in §7 explicitly chooses a sequential admissibility search over a full census: screen the current candidates through the remaining gates and pin the first one that passes all of them, without making a “best available” claim. Resume the anatomy survey only if the current set fails.
2. **The CCF label map is materially incomplete, and its incompleteness is much larger than its error rate.** The 46 screened recordings produced **296 distinct host structure names with no table entry**, and 650 donor rows name acronyms it does not define. This does not affect a `CA1`-targeted search — `CA1` is defined and validated at 16/16 — but it does affect the **region-unaware arm**, whose donors are drawn without conditioning on region and whose placement still has to be evaluated against the local host label. Completing the map needs an Allen CCF structure-name↔acronym source, and the obvious ones carry a licensing question: Allen Institute Terms of Use for the atlas data, versus permissively licensed packages that redistribute it (`iblatlas`, MIT; `brainglobe-atlasapi`, BSD-3). **That question should be resolved before importing an ontology, not after.** It is **agent work, not a director request** — reading the licences is ours to do, and it becomes director-only only if the answer requires a named exception. Nothing about it was filed in `director_requests.md`, deliberately: filing an unscoped licence question would be handing the director our homework.
3. **No non-anatomical host gate has been applied *except duration*.** Drift, noise level, and post-rescaling effective SNR are untested, and a recording at the top of §4 can still fail all of them.
   **Duration is now measured rather than missing** — see §4.4. The gap was real: the anatomy index records each AP series' shape but not its sampling rate, because these NWB series carry an explicit `timestamps` dataset rather than `starting_time`, and a sample count without a rate is not a duration. Codex found the path in review and confirmed it on one pinned asset; Session 6 applied it to all 11 candidates, which is the sequential-gate order ruling 7.3 asks for and avoids paying the timestamp-chunk transfer on 429 assets to learn something anatomy has already narrowed.
4. **Ten feasible placements inside the band have not been demonstrated**, only made plausible by band width. Slot 7 makes this a gate: if ten placements cannot be supported without overcrowding or label ambiguity, the host fails.
5. **No covariate balance has been evaluated.** That is Codex's gate and it is the one that decides whether Tier A runs at all.
6. **`audit_template_library.py` duplicates logic now living in `utils/template_metadata.py`.** It is left as-is this session rather than refactored mid-flight, and it is recorded here as a known duplication to resolve before the packet is assembled, not left silent.
7. **The packet does not yet carry its own `requirements.txt`, `.gitignore`, or runbook README.** `Playbooks/reproducibility-packet.md` requires all three, because the self-containment test is copying the packet folder alone to a clean machine. This session created the **project-root** `requirements.txt` — right for the venv, not sufficient for the packet. The scripts are already inside the packet, so this is Phase-3 curation rather than relocation; it is owed, and it is not done.

---

## 6. Artifacts this document rests on

| Path | What it is |
|---|---|
| `Reproducibility Packet/scripts/utils/remote_hdf5.py` | HTTP-range file object; lets h5py read a remote NWB's metadata without downloading it. Retries a failed range request with backoff and rejects ignored, malformed, or short range responses — at hundreds of sequential requests per run a dropped connection is routine, while an ignored range could otherwise start transferring the full 18–197 GB object. |
| `Reproducibility Packet/scripts/utils/dandi.py` | DANDI asset listing, caching, and blob addressing |
| `Reproducibility Packet/scripts/utils/template_metadata.py` | donor CSV fetch, snapshot pinning, caliper, provenance-key parsing |
| `Reproducibility Packet/scripts/utils/ccf_labels.py` | CCF long-name ↔ acronym bridge, and the non-injectable label set |
| `Reproducibility Packet/scripts/audit_donor_provenance.py` | provenance granularity and host-specific exclusion |
| `Reproducibility Packet/scripts/survey_host_anatomy.py` | host anatomy survey and injection-zone band finding |
| `Reproducibility Packet/scripts/validate_ccf_label_map.py` | validates the label map and the depth-coordinate correspondence |
| `Reproducibility Packet/scripts/screen_host_timing.py` | measures each candidate's real sampling rate, duration, and timestamp regularity from its own `timestamps` dataset |
| `Reproducibility Packet/results/donor_provenance_2026-08-11.txt` | provenance audit output |
| `Reproducibility Packet/results/ccf_label_map_validation.txt` | label-map validation output |
| `Reproducibility Packet/results/host_anatomy_index.jsonl` | resumable per-recording anatomy index |
| `Reproducibility Packet/results/host_anatomy_CA1.txt` | ranked CA1 host report |
| `Reproducibility Packet/results/host_timing_index.jsonl` | resumable per-recording timing index |
| `Reproducibility Packet/results/host_timing_CA1.txt` | measured duration and regularity report for the 11 candidates |
| `Reproducibility Packet/results/templates_snapshot_2026-08-11.csv` | the pinned donor metadata snapshot, SHA-256 `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d` |
| `Reproducibility Packet/results/dandi_000409_assets.json` | the pinned DANDI asset listing the survey ran against |

---

## 7. Codex reviewer rulings

These rulings apply to the strategy and recommendation in this document. They do **not** amend the already-approved Claim Sheets by themselves; the contract and Accessible Claim Sheet must receive a synchronized dated amendment before Tier A generation follows any changed commitment.

### 7.1 Exclusion granularity and provenance balance

**Approve subject-level host separation, made vacuous by construction.** The selected host must come from a subject absent from the twelve-subject donor library. The report still names the shared-dandiset boundary.

For the donor arms, balancing only the *number* of provenance sources is too weak now that the keys are parsed. The Tier A balance gate should attempt exact donor-source blocking at the finest feasible level — insertion first, then session, then subject — so a CA1 donor and its region-unaware partner do not carry an avoidable provenance difference. The current snapshot has non-CA1 candidates in every CA1 source insertion, so this is empirically plausible but remains subject to the amplitude, effective-SNR, geometry, and placement gates. Any relaxation is reported and justified rather than silently replacing exact blocking with an equal count.

### 7.2 Sixteen donors, the block scheme, and the negative control

**Keep five blocks as the initial feasibility tranche, but do not use unconstrained random draws.** Use a seeded exposure-balanced schedule over all sixteen CA1 donors: fifty matched-arm selections across five ten-slot blocks means each donor appears three or four times. Randomize slot assignment, spike-time seeds, and placement seeds within that schedule. Keep repeated donor identities in the same bootstrap cluster, as the Claim Sheet already requires.

This changes the interpretation: Tier A's donor-population statement is conditional on the complete sixteen-template CA1 library. More blocks add spike-time and placement precision; they do not create new CA1 donor diversity. The report must say so even if the interval becomes narrow.

The negative-control diagnostic must preserve the same small-pool/large-pool asymmetry. For Tier A, each pseudo block should be an independently seeded **replicate of the full CA1-versus-region-unaware contrast**, and the replicate band should be formed from the difference between the real-block and pseudo-block interaction estimates. That uses the already-budgeted two pseudo-arm sorter runs per block while mirroring both selection pools. It is a replicate-stability diagnostic, not a no-manipulation null band; this tier-specific definition therefore requires a Claim Sheet amendment before execution. Tiers B and C can retain the original same-condition pseudo-arm construction because donor identity is fixed there.

### 7.3 CA1 versus SUB and how far to survey

**Approve CA1 as the first injection-zone choice.** The joint Tier A/Tier C evidence constraint outweighs the donor-headroom advantage of SUB at this point. Do not commission the SUB literature task unless CA1 fails a real gate.

**Do not finish a 429-recording anatomy census merely to claim the best host.** The current screen already establishes that CA1 anatomy is not scarce. Apply duration, drift, noise, effective-SNR, placement, and covariate-balance gates sequentially to the current candidate set and pin the first fully admissible host. Call it a predeclared admissible host, not the best host. Resume the wider survey only if the current candidates fail.

---

## 8. Owner re-review (Claude, Session 6)

This section is the owner's response to §7 and to the reviewer's edits above. It does not rewrite them; the review record stays as it was written.

### 8.1 What I checked rather than accepted

Every reviewer edit that changed a factual claim was re-derived before being accepted:

- **"32 of 37 insertions produced testable assignments."** Confirmed against `ccf_label_map_validation.txt`: the probe-assignment table has exactly 32 rows and the failure list exactly 5. The edit is right and my original prose implied a completeness the run did not have.
- **The narrowed validation claim.** Confirmed at the source rather than taken on the summary. `hybrid_template_library/python/upload_ibl_templates.py` pairs a DANDI 000409 recording with IBL's own sorting from the ONE database and stores that sorting's `brain_area` property; the NWB electrode table is another export of the same IBL registration. **Codex is right and I was overclaiming.** The 1,401/1 result is a strong internal-consistency check on my bridge and on depth-coordinate compatibility; it is not independent validation of the atlas registration, and the artifact now says so.
- **The removed "same preprocessing chain" residual.** Also confirmed at the source: templates are extracted after `common_reference(highpass_filter(phase_shift(...), freq_min=1.0))`. Host raw data has had none of that. The claim as I wrote it was not supported and its removal is correct.
- **The fallback reordering.** Accepted without reservation. Putting "inject fewer than ten units" first was me treating a contract commitment as the cheapest thing to give up, which is exactly backwards — ten-unit density is tied to anchor comparability and collision load, and it should cost an amendment.
- **The `remote_hdf5.py` hardening.** Read the diff. The Range-response validation is right and the failure it prevents is real — a server that ignores `Range` would have begun transferring an 18–197 GB object into a screening loop. Note for the record that `urllib.error.URLError`, `TimeoutError` and `ConnectionError` are all `OSError` subclasses, so the narrowed `except` clause still covers everything the old one did. One cosmetic residue: a retried short response counts its bytes twice in `n_bytes`. Diagnostics only; not worth an edit mid-flight, and recorded here rather than silently left.

### 8.2 Rulings 7.1 and 7.3, accepted in full

Both are accepted as written, and 7.1's substance plus the first half of 7.2 are now proposed as **Amendment 2** to the technical and Accessible Claim Sheets, since they change what the contract commits to rather than only how a step is implemented.

On 7.3 I want to name what I am agreeing to, because it is a real concession and should not read as a formality. I built a survey that covers 10.7% of the eligible hosts and left it resumable, and the instinct that produced it was that more coverage is more rigour. It is not, here: the screen already shows CA1 hosts are common, and a full census would buy a superlative the project has no use for. **"First admissible" is the right standard and "best available" was never a requirement I could have met anyway.** Applying the duration gate (§4.4) rather than resuming the census is that ruling being followed, not merely accepted.

### 8.3 Ruling 7.2 — the schedule is accepted; the replicate band is not, and here is a counter-proposal

**Accepted:** five blocks as the initial tranche, the seeded exposure-balanced schedule over all sixteen CA1 donors, randomisation moved to slot assignment and to spike-time and placement seeds, repeated donors kept in one bootstrap cluster, and the conditional-on-sixteen-templates statement reported even when the interval is narrow. That last point is the one that most changes what a Tier A result means, and it is now a new non-transfer clause (Slot 13.9) in the proposed amendment.

**Not accepted:** replacing Tier A's negative-control construction with a replicate-stability band. I accept the diagnosis completely — the pool asymmetry is real, it is my own §3.2, and a same-condition pseudo pair drawn from one arm's pool measures the wrong thing. I do not accept this implementation of it, for three reasons, the third of which is the one I would not want to lose.

1. **It stops being a negative control.** Slot 5 defines the band as arms generated under the same nominal condition "without any realism manipulation"; Slot 8's Panel 2 shows it to the director as "the apparent interactions produced by matched pseudo-arms where no realism property changed"; Slot 11.5 and Slot 14 both describe it that way. A replicate band contains the manipulation in both halves. Its expectation is zero under stability, so it answers *"does the interaction reproduce?"* — a different question from *"can the machinery invent an interaction of this size on its own?"* Adopting it for one tier means the same grey band in the same report means two different things depending on which figure you are looking at, and the director's one printed sentence names it once. For a project whose Slot 8 is a **non-expert** verification path, that is a real cost.
2. **It partly duplicates the primary interval.** The hierarchical bootstrap already resamples randomization blocks, so between-block instability is already inside the reported uncertainty. Replicate stability is largely a precision statement, and this design is not short of those.
3. **It cannot catch the failure the negative control exists for, and that failure is this project's worst case.** Suppose the selection and matching machinery itself induces a systematic sorter-by-arm interaction — say the covariate matching that pairs each unaware donor to a CA1 partner lands them at systematically different depths or spatial spreads. A replicate band would show that artifact identically in the real estimate and in the pseudo estimate, their difference would be near zero, and **the band would look reassuringly tight while the project reported a positive interaction that was an artifact of its own procedure.** The current construction is the only thing in the design pointed at that failure. Tier A is where it is most likely, because Tier A is the tier that cannot hold donor identity fixed.

**The counter-proposal, at identical cost.** Keep the band a no-manipulation band and mirror the pool asymmetry inside it:

- **Pseudo-arm P1** draws from a **fixed, randomly chosen 16-template subset of the region-unaware pool**, selected once so its amplitude/SNR/depth spread approximates the CA1 sixteen, and used across all five pseudo blocks on the same exposure-balanced rota (each appears three or four times across fifty slots).
- **Pseudo-arm P2** draws from the **full** region-unaware pool and is covariate-matched to P1 exactly as the real control arm is matched to the real matched arm.
- Neither arm conditions on region, so **no realism property changes** — Slot 5's existing definition is satisfied literally, not reinterpreted. What *is* mirrored is everything Codex identified as asymmetric: a nearly exhausted 16-template draw pool against a 1,149-template one, the same repetition structure, the same covariate matching, the same clustering.

Its cost is two pseudo-arms across five blocks — **the same two sorter runs per block already budgeted**, so Slot 9's 200-recording-minute tranche is unchanged. And because it satisfies Slot 5's wording as written, it needs a Tier A implementation note rather than a redefinition of the contract's strongest control, which is the lighter change to make to a pre-registered sheet.

**What it does not mirror, stated so it is not discovered later:** the real matched pool is homogeneous in *region* as well as small, and no no-manipulation control can reproduce that, because region homogeneity is the manipulation. The pseudo band therefore controls pool size, repetition, matching and seeds, and does not control region homogeneity. That boundary is honest and statable; a band that silently changed its own meaning is not.

**If you hold your position after reading this, we are at two round-trips on this specific point and it goes to Randy** — scoped to the band construction alone, not to the artifact. I would rather spend his attention on one well-formed question than loop.

### 8.4 One new finding, for Rung 0 rather than for Tier A

This comes out of Codex's own upstream audit and is the most useful thing I got from the review. The donor templates were extracted **after** `phase_shift` — the Neuropixels ADC sample-shift correction — plus a 1 Hz high-pass and a common reference. So the donor waveforms already carry that chain.

**If injection happens into a raw host and the project's own preprocessing runs afterwards, `phase_shift` is applied twice to the injected spikes and once to the real ones.** That is a systematic difference between injected and real units, present identically in every arm, which means it would not bias the Tier A contrast — but it would smear injected waveforms across channels in a way no real spike is smeared, and it would do it to a benchmark whose whole purpose is to stand in for real units. The anchor's own workflow injects into a **preprocessed** recording, which is presumably why this has not bitten anyone.

**Recommendation, for Rung 0 to verify against the pinned SpikeInterface version rather than take from me:** inject into the preprocessed host, with a preprocessing chain matched to the one the donor templates were built with, and record the chain in the run configuration so the Technical Report can state it. If the pinned version does something different, that is worth knowing before the manipulation check rather than after.
