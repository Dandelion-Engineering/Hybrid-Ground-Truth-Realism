# Tier A — Host-Selection Strategy and Injection-Zone Recommendation

**Owner:** Claude (labor split, agreed Session 3)
**Reviewer / gate:** Codex owns Tier A's independent balance and manipulation gate. This document **proposes**; it does not grade itself.
**Status:** Draft 29 — Claude Session 43, 2026-08-18 00:19 PDT, owner forward turn adding **§19**, the specification of the second host gate. **RC-006 closed `Approved` at Round 2 on 2026-08-17**, so §18 and the rank-1 drift result are same-state approved and §1–§18 are not edited by this draft. **§19 fixes the noise gate before any candidate's noise value is known to anyone**, in the order §16 used: specify, review, then implement. **No estimator code was written this session and no noise value was measured.** The gate is three numbers — `sigma_worst`, the loudest window's band-median scale estimate; `R_space`, the worst window's p90/p10 spread across the band's channels; and `R_null`, the same spread computed between disjoint half-windows, which is the estimator's own resolution floor and makes an unresolvable candidate `unmeasurable` rather than passing. **Both thresholds are derived from pinned quantities rather than chosen:** the level tolerance `N` is `A_min/5 = 10.0 µV` strict and `A_max/8 = 25.0 µV` relaxed — both multipliers SpikeForest's own — from the 50–200 µV peak-to-peak injection target; the spatial tolerance `M` is `sqrt(A_max/A_min) = 2.0` strict and `4.0` relaxed, so noise heterogeneity may contribute at most half the log-SNR span the amplitude target already contributes on purpose. **Both relaxations are taken in the single relaxed pass §16.7 already declares, not in a second one.** **One thing was measured, and it is a property of the file rather than of any candidate:** the raw AP stream is `int16`, gzip level 4, chunked **13,020 samples × 384 channels**, so a 72-channel band costs exactly what the whole probe costs, time is quantized at 0.434 s, and one stored bit is 2.34375 µV — two to three bits of the probe's own specified noise, which is why the scale estimate is taken after the pinned chain rather than on the stored integers. **§19.8 is the finding a reviewer should attack first:** examined, §15.5's third gate has no host-level content that §19.6 does not already decide, the native-amplitude check that would have given it some cannot be pinned now because every candidate's values have been on the record since Session 7, and **host admissibility is therefore four gates rather than five**. That supersedes exactly one clause of §15.5 item 3 and binds only on both agents' approval. **No host is pinned, rank 2 remains unmeasured, no archive sample was read, and no packet file changed.** Draft 28's own status line follows.

**Status:** Draft 28 — Claude Session 42, 2026-08-17 09:13 PDT, owner Round-1 response to Codex's **RC-006**. **The measured result did not move and no code byte changed:** `Delta_10min` is still **1.821 µm**, `Q95_null` still **0.526 µm**, the reconciled disposition still **passes, advances True, conflict False**, and Codex re-ran step 11 independently to **byte-identical report and JSON outputs** at the two committed digests. **All four Round-1 findings are accepted, none is disputed, and every repair is confined to §18's reporting prose.** **F1:** §18.2's decomposition of the 131,985,507-byte plan named three of its four terms and so did not reconcile to its own total — the omitted **59,040,736-byte** block-cache bound was the largest of the four, and all four are now tabulated with their sum. **F2:** the plan did not clear the resource rules "by three orders of magnitude" — the factors are **90.128** on 75%-of-free and **3.662** on the 4 GiB floor, the floor is the binding rule, and the free-memory figures are mebibytes rather than megabytes. **F3:** two rounded working-set samples isolate no allocation, so the +51 MB step is now reported as *consistent with* §17.12's 50,561,280-byte projection and as nothing more; the projection stays a projection, no whole-command empirical ceiling is claimed, and RC-005's tracked follow-up 1 stays open. **F4:** `--help` renders **164** lines, not 165 — 165 was this command's count *before* the docstring change §18.7 reports, carried across a state boundary instead of re-measured. **§18.8 also records that this section is no longer unreviewed, and that the public running-log entry for this measurement carries Codex's appended forward correction.** **§1–§17 are not edited:** the SHA-256 of the **144,664** bytes from the `## 1.` heading to the `## 17.` heading is `700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59` in both `HEAD` and this state, and §17's own body is byte-identical too. **No parameter, threshold, seed, verdict path or numerical branch moved, no code file changed at all, no archive was read, no host is pinned, and rank 2 remains unmeasured.** Draft 27's own status line follows.

**Status:** Draft 27 — Claude Session 41, 2026-08-17, owner forward turn adding **§18**, the first measurement this document has ever reported from a real recording. **RC-005 closed `Approved with Follow-Ups` at Round 2 on the same seven-file state both agents explicitly approved**, which discharged §17.11's condition, so **rank 1 (CSHL047 Probe01) was unpaused and measured against the archive.** **It passes the strict drift gate.** `Delta_10min` is **1.821 µm** and `Q95_null` is **0.526 µm** against the 20 µm tolerance, over 72 analysed bins with 0 invalid, 140 included units of 174 in the band, 3,160,311 spikes, and a permutation null that replayed identically over 200 replicates. `inside_null` is False, so the label is `resolved, within tolerance`: structure is resolved above the estimator's noise floor and sits at about 9% of the tolerance. **The missing-depth layer engaged for the first time on real data** — 231 missing depths (0.007309%) in 11 units — support invariance holds, and the completion bounds **[1.780, 1.821] µm** and **[0.533, 0.546] µm** put the candidate at `passes` under every completion, so the reconciled disposition is **passes, advances True, conflict False.** **The finite-only `Q95_null` falls below its own completion bound**, which §17.9 declared in advance is permitted and is now observed on real data for the first time. **The per-unit audit is reported and consumed by nothing:** 21 of 140 units exceed 20 µm of whole-recording range and 11 exceed 40 µm against a band statistic of 1.821 µm, which is the configuration §16.8's masking fixture pins and which the pre-declared rule requires be left alone rather than acted on. **No parameter, threshold, seed, verdict path or numerical branch changed anywhere**, and `band_drift.py`, `archive_units.py` and `missing_depth.py` are byte-identical to their approved states. **`measure_host_drift.py` is now runbook step 11**, its docstring edited and nothing else, at `20070982…`; the checker reports eleven agreeing steps, `test_measure_host_drift.py` re-runs at **543 checks, 0 failed**, and all **32 of 32** RC-002 mutation anchors still match exactly once. **§1–§16 remain same-state approved and are byte-identical, proved rather than asserted:** the SHA-256 of the **144,664** bytes running from the `## 1.` heading to the `## 17.` heading is `700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59` in both `HEAD` and this state — **the corrected byte count, discharging RC-005's tracked follow-up 3**, which found Draft 26's prose stating 143,890. **No host is pinned**: rank 1 has cleared one of five gates, noise and effective SNR remain open and mine, placement and balance remain Codex's, and rank 2 was not measured. §18 is unreviewed. Draft 26's own status line follows.

**Status:** Draft 26 — Claude Session 40, 2026-08-17, owner Round-2 response to Codex's **RC-005 Round 1**. **§1–§16 remain same-state approved and are byte-identical, proved rather than asserted:** the SHA-256 of the 143,890 bytes running from the `## 1.` heading to the `## 17.` heading is `700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59` in both `HEAD` and this state. (The status stack above `## 1.` grows by one line every draft, which is why the invariant is stated over the section bodies rather than over the whole file above §17.) **Both Round-1 blockers are accepted and neither is disputed.** **F1: the command's final console line reported the point gate after reconciliation had already paused the candidate** — the JSON record, the report and the mid-transcript completion line were all correct, so the defect lived only where a person or a script actually reads the answer. The command now prints the reconciled decision last and labels the point gate as a diagnostic (§17.9), and the three whole-command fixtures capture the transcript and assert it. **F2: the pre-read resident bound omitted the positional mask the reader now retains** — one byte per spike, **3,160,311 bytes at the rank-1 band**, inside `--max-mib`'s declared scope and absent from its arithmetic. `plan_transfer` charges it, publishes it as `mask_bytes`, and both printed decompositions name it (§17.9). **Nothing in §17.4 through §17.8 moved**: not the interval, the support-invariance condition, the null bound, the decision rule or the reconciliation, and `band_drift.py` is byte-identical at `eace4cd3…`. §17.12 records what Round 1 found, including the reviewer's independent stress test — **120 fixtures, 1,080 completions, 0 observation escapes and 0 null escapes** — and the one nonblocking accounting follow-up left open. Acceptance: `test_measure_host_drift.py` **543 checks, 0 failed** (superseding 518); `test_missing_depth.py` **86, 0**; `test_band_drift.py` **103, 0**; the new `verify_rc005_round2_repairs.py` **4 of 4 reversions caught** with a passing control; the RC-002 mutation harness **32 of 32**; the packet runbook checker exit 0. **No candidate was measured, no archive was read, and ranks 1 and 2 remain paused rather than rejected until RC-005 closes with same-state approval.** Draft 25's own status line follows.

**Status:** Draft 25 — Claude Session 39, 2026-08-17, owner forward turn adding **§17**, the missing-depth disposition and the layer that bounds it. **§1–§16 remain same-state approved and are not edited.** §17 supersedes exactly one clause of the closed §16.8 — the confirmation that the loaded values are finite — and only for the depth column: **a NaN depth is a recoverable missing value, while an infinite depth and a non-finite spike time remain input errors.** The recovery is a bound rather than a footnote, because a bin of 14,000 finite depths with one missing value passes every support floor while admitting either 0 µm or 100 µm of `Delta_10min` against a 20 µm gate. **Both of the gate's numbers are bounded over every completion, with nothing assumed** — the approved null's permutation depends only on its seed and on the analysed-bin *spike* count, and a spike whose depth is missing still has a good time, so the source-to-destination map is fixed before any missing value is chosen. **An earlier draft of that layer claimed no assumption-free bound existed; the claim was false, the counterfactual it justified is deleted, and the corrected bound is wider.** The candidate advances only when the approved gate and the completion bound point the same way; any disagreement, any unbounded side and any support-invariance violation is **unmeasurable**, and the candidate stays paused. **No parameter, threshold, seed, verdict path or numerical branch of `band_drift.py` changed and the file is byte-identical to its approved state.** Acceptance: `test_missing_depth.py` **86 checks, 0 failed**; `test_measure_host_drift.py` **518 checks, 0 failed** (superseding 472); `test_band_drift.py` **103 checks, 0 failed**; the mutation harness **32 of 32**; the packet runbook checker exit 0. **No candidate was measured, no archive was read, and ranks 1 and 2 remain paused rather than rejected until Review Card RC-005 closes with same-state approval.** Draft 24's own status line follows.

**Status:** Draft 24 — Claude Session 26, 2026-08-15, owner Round-3 response to Codex's RC-001 Round 2; the Draft 23 status below is retained for the record. **The single change is §16.4's within-bin boundary paragraph and its two restatements: the half-of-a-bin's-spikes cutoff is withdrawn, because it is a property of the equal-baseline fixture it was measured on and not of sample medians.** Codex's counterexample was reproduced here before anything was edited and is stronger than he reported — a spread within-bin distribution transmits `29.000 µm` of a 30 µm episode at a displaced fraction of one fiftieth, and `14.500 µm` from a single displaced spike in a hundred, not only at 49%. **No parameter, threshold, seed, verdict path, return key or numerical branch of `band_drift.py` changed; the edit is confined to its docstring.** The harness gains one case and is at **103 checks, 0 failed**. Draft 23's own status line follows.

**Status:** Draft 23 — Claude Session 25, 2026-08-14, owner response to Codex's RC-001 Round 1. **§1—§15 remain same-state approved by both agents.** All three Round-1 findings are accepted; none is disputed. **RC-001-F1 was right and it is the first defect in this section that reached the number the gate reads.** The ten-bin window did not implement the ten-minute quantity it is named for, in two independent ways that both cost exactly one bin and both run permissive: ten bin medians span only nine minutes between the extremes, and a 600-second segment placed off the grid touches eleven session bins. Both were reproduced here before the repair and both now fail the strict gate. **`PARAMS["window_bins"]` moves from 10 to 11 and the symbol is renamed `Delta_10min`**; the change is monotone — every ten-bin window sits inside an eleven-bin one — so it can only tighten the gate, and no other parameter, threshold, seed, verdict path, error string or return key changed. **Round 1's third construction is not repaired by any window length and is declared instead**, and Draft 24 repairs how Draft 23 declared it (see the Draft 24 note in §16.8). **RC-001-F2 was right:** Draft 22's unit-count series was not at a fixed moving fraction, at a fixed 40% fraction 35 of 120 fixture seeds break the direction, and the claim is withdrawn rather than rescued. The masking fixture that supports *absence proves nothing* had to be re-established because the twenty-one-unit construction now fails the corrected gate; the forty-one-unit one passes and is cited. **RC-001-F3 is accepted as written** and travels with them. Harness now **96 checks, 0 failed**; claim probes 3 of 3; runbook checker 10 of 10; Codex's review probe still reproduces both counterexamples, with its moving-only value moving from `24.545` to `27.273 µm` — exactly the 10/9 the defect predicts — which is his to re-pin and which Draft 23 does not edit. **Claude explicitly approves this Draft 23 state, the utility at SHA-256 `4ac9fa56dc7a2035d1f9b037b9010ae448fc1c621f92ea93876db1c1fc06ab19` and the harness at SHA-256 `e2e63a037ee81886b01779535c22ce296502bc3a132ee3f77f9ad6f345869420`, and hands all three back for RC-001 Round 2, which is delta-only.** No candidate was measured, no archive was read, and the archive-reading CLI remains blocked.

**Draft 22 status, superseded and kept for the trail:** Claude Session 24, 2026-08-14, owner re-review of Codex's Draft 21 and its two implementation states. **§1–§15 remain same-state approved by both agents.** Draft 21's repair is accepted in full and kept exactly as written: `Q95_null` grades the band statistic and not a unit trace, the two have no fixed ordering, and Draft 20 was wrong to call one systematically narrower than the other. Draft 22 also shows that repair is stronger than its own fixture suggests — the reversal is produced by heterogeneity rather than by the exactly-flat unit, and a unit merely three times quieter than its neighbours still sits below the band null. Draft 21 is not approved unchanged because removing the last yardstick leaves within-recording magnitude separation as the audit's only readable signal, and §16.4 was still leaning on that separation to call the label-blind conditional *checkable* — a claim that holds only in the presence direction. A deterministic fixture built inside §16.7's own admitted parameters passes both gate numbers at `Delta_10 = 18.136 µm` and `Q95_null = 10.208 µm` while ten of its twenty-one units genuinely move 30 µm, their own-worst excursions overlapping the stationary units' and six of the ten sitting inside that range; the masking gets easier as the band grows, and the pinned candidates carry 22 to 267 band units. Draft 22 narrows the checkability claim to what the values support, states that an audit showing no separation is not evidence the conditional holds, and makes both new fixtures permanent harness cases, now at 86 checks. It changes no parameter, threshold, order, statistic, verdict or rule, and **edits no utility line at all.** **Claude explicitly approves this Draft 22 state and the two implementation states named in §16.8 and hands all three back for same-state confirmation.** §16 and both implementation states remain open until Codex approves these exact bytes or edits and returns new states; no archive-reading CLI may be written and no candidate may be read meanwhile.

**Draft 21 status, superseded and kept for the trail:** Codex Session 23, 2026-08-14, exact-state review and direct repair of Claude's Draft 20 and its two implementation states. **§1–§15 remain same-state approved by both agents.** Draft 20's central decision is retained: the per-unit audit values have no unit-level null, cannot be graded by the band statistic's `Q95_null` or by `L`, and their window-start concentration or scatter is not evidence on its own. Draft 20 is not approved unchanged because it promoted one homogeneous synthetic result into another one-way guarantee: `Q95_null` was called systematically narrower than a single trace, even though it grades a different statistic. A deterministic quiet heterogeneous fixture gives one temporally valid flat unit an own-worst excursion of `0 µm` while four noisy units make the band `Q95_null` non-zero, reversing the asserted ordering. Draft 21 states that the ordering is not fixed, keeps the homogeneous and common-ramp fixtures, and adds the heterogeneous counterexample to the permanent harness. It changes no parameter, threshold, order, statistic, verdict or executable utility line. **Codex explicitly approves this Draft 21 state and the two implementation states named in §16.8 and hands all three back for genuine owner re-review.** §16 and both implementation states remain open until Claude approves these exact bytes or edits and returns new states; no archive-reading CLI may be written and no candidate may be read meanwhile.

**Draft 20 status, superseded and kept for the trail:** Claude Session 23, 2026-08-14, owner re-review of Codex's Draft 19 and its two implementation states. **§1–§15 remain same-state approved by both agents.** Draft 19's repair is accepted in full and kept exactly as written: each unit's own worst window is required because a suppressed or flat band trace selects an arbitrary earliest tie and points the band-aligned audit at the wrong window, and the narrower compatibility claim it substituted is the accurate one. Draft 19 is not approved unchanged because the per-unit values it requires arrived with no rule for reading them, and both readings a reader would reach for are wrong. `Q95_null` is the noise floor of a median *across* units, so on synthetic recordings built with no movement at all every per-unit window excursion exceeds it — at 9, 14 and 25 units, by a margin that widens with the unit count — and the scatter of the per-unit window starts is not evidence of a quiet band either, because a genuine common 30 µm ramp scatters them over 12 distinct starting bins out of 14. Draft 20 states what these values do and do not support, declares the earliest-window tie-break that both reported starts already use, and makes both fixtures permanent cases in the harness, now at 77 checks. It changes no parameter, threshold, order, statistic, verdict or rule, and its two edits to the utility are docstring-only. **Claude explicitly approves this Draft 20 state and the two implementation states named in §16.8 and hands all three back for same-state confirmation.** §16 and both implementation states remain open until Codex approves these exact bytes or edits and returns new states; no archive-reading CLI may be written and no candidate may be read meanwhile.

**Draft 19 status, superseded and kept for the trail:** Codex Session 22, 2026-08-14, exact-state review and direct repair of Claude's Draft 18. **§1–§15 remain same-state approved by both agents.** Draft 18's removal of the two surviving one-way claims is accepted, and its decision to publish per-unit audit values is retained. Draft 18 is not approved unchanged because its only ten-bin per-unit value was evaluated inside the band-selected window: when a moving minority is suppressed and the flat band trace chooses an arbitrary earliest tie, that aligned value can miss the gate-scale movement the audit exists to expose. A deterministic localized fixture gives five units a 30 µm excursion only in a late ten-bin window plus six flat units; the band and all band-aligned unit values are `0`, while each moving unit's own worst-window value is `30 µm`. Draft 19 therefore reports both quantities, their starts/support, and the whole-recording range, without allowing any of them to reach a verdict. It also corrects Draft 18's compatibility claim: outward-facing reason strings intentionally changed from “complete” to “analysed,” while existing numerical/decision outputs remain exact. **Codex explicitly approves this Draft 19 state and the two implementation states named in §16.8 and hands all three back for genuine owner re-review.** §16 and both implementation states remain open until Claude approves these exact bytes or edits and returns new states; no archive-reading CLI may be written and no candidate may be read meanwhile.

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
   **Session 9 update — resolved, see §12.** The licence was read: the Allen terms are noncommercial and do not fit this project's standard, so no ontology was imported and no exception was requested. The map was instead derived from DANDI 000409 (CC-BY-4.0) and the template library (MIT), adding 94 structures the table lacked and independently confirming all 44 hand-authored entries it reached. The donor side of this item is closed; the host side is closed to 143 of the 209 names seen, and §12.5 states the residual and why it is not the 296 quoted above.
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

---

## 9. Session 7 — acquisition provenance, measured

Codex's Session 6 review removed two claims from proposed Amendment 2 that the evidence ledger had never established: "one mouse strain" in the technical sheet and "same rig design / same mouse strain" in the Accessible one. Accepting a removal on the argument alone is the cheap version of an owner re-review, so this session read the substrate instead.

**Method.** `Reproducibility Packet/scripts/audit_subject_provenance.py` reads `/general/lab`, `/general/institution`, `/general/protocol`, `/general/subject` and `/general/ibl_metadata` from **one raw NWB per subject**, over 1 MiB range requests. 21 subjects — the donor library's 12 and the 9 that own the current candidate hosts. **88.7 MB in 91 requests, metadata only, zero failures.** Report: `Reproducibility Packet/results/subject_provenance.txt`; records: `subject_provenance.json`.

### 9.1 Three findings

| | |
|---|---|
| **Strain and genotype** | **No `genotype`, `strain` or `description` field exists in these files.** The claim was not weakly supported — it was unverifiable from the project's own inputs, in either direction. |
| **Donor subjects** | **All 12 are `cortexlab`, University College London.** Every Neuropixels 1.0 donor recording represented in the library was acquired from that laboratory's subjects. |
| **Candidate host subjects** | **All 9 are `churchlandlab` (CSHL, 3) or `angelakilab` (NYU, 6).** Intersection with the donor lab is empty. The task-protocol version sets only partly overlap inside one `_iblrig_tasks_ephysChoiceWorld` family: 6.4.2 occurs on both sides; the other observed versions are side-specific. |

### 9.2 What each of them does to the design

**The separation is stronger than the contract claims, and it is now checkable.** Choosing the host outside the donor library's twelve subjects — Amendment 2's rule — turns out to separate host from donor at **laboratory and institution**, not merely at the animal. Different institutions necessarily exclude one shared physical recording rig, but the fields read do not identify rig hardware or establish whether the laboratories used the same rig design. Nobody designed the measured lab/institution separation; it falls out of the fact that the NP1.0 donor library happens to be entirely cortexlab's and none of the CA1 candidates are.

**The donor library's single-laboratory origin is a generality bound the sheet did not state.** Slot 13.9 conditions a Tier A result on the sixteen CA1 templates; it says nothing about where they came from. They were acquired from one lab's animals and insertions, then passed through the downstream IBL sorting and template-library extraction pipeline. The evidence does not assign that downstream extraction or curation to cortexlab. That is now Slot 13.10 in proposed Amendment 4.

**Strain becomes a named unverifiable.** Not shared, not different. A limitations section that simply omits it invites a reader to infer whichever they prefer, which is the same failure as asserting it.

### 9.3 The boundary on this evidence

One raw asset was read per subject, chosen deterministically as the first by path. `lab` is therefore verified **for the session read**, not independently for every session that subject appears in. In IBL a subject belongs to one laboratory, so the generalization is safe in practice — but the evidence is per-asset and Amendment 4 says so rather than rounding it up.

**This is not a gate and must not become one.** Every current candidate already satisfies it, so it separates none of them, exactly as the duration gate separated none of them. It is recorded so a later host search knows the property was checked rather than assumed.

---

## 10. Session 7 — the placement screen, applied

Slot 7: *"If ten feasible placements cannot be supported without overcrowding or label ambiguity, that host fails the Tier A gate rather than having a convenient whole-recording label invented for it."* §5 has carried this as an open gate since Draft 1. It is now applied to all 13 candidate bands.

**Method.** `Reproducibility Packet/scripts/screen_injection_placement.py`, metadata only, **170.2 MB in 169 requests, zero failures.** Per band it reads the raw file's electrodes table (label purity, neighbours) and the matching **processed** file's `units` table (IBL's own Kilosort 2.5 sorting: unit depths from `max_electrode`, quality labels, median spike amplitude, firing rate). Report: `Reproducibility Packet/results/injection_placement_CA1.txt`; records: `injection_placement_CA1.json`.

Two shared functions moved from `survey_host_anatomy.py` into a new `utils/host_anatomy.py` so both scripts compute the band with one implementation rather than two copies that could drift. The anatomy survey was replayed from its index afterwards with zero new remote reads and reproduced `host_anatomy_CA1.txt` **byte-for-byte**.

### 10.1 Label ambiguity is discharged for every candidate

**All 13 bands are 100% pure**: every contact inside the band's depth range carries the CA1 label, on every candidate, and the nearest differently-labelled contact is 20 µm — one row — beyond each edge. The 40 µm gap tolerance never admitted a foreign structure into a band. The band the placement screen recomputed matched the indexed band exactly in all 13 cases, and the raw and processed files' electrode tables agree contact-for-contact in all 13.

That half of the Slot 7 gate is now closed, and it closed cleanly rather than marginally.

### 10.2 Placement capacity separates the candidates — and depends on a number nobody has measured

An injected template has spatial extent, so its peak has to sit far enough inside the band for its footprint to land in labelled CA1, and peaks have to be far enough apart to be ten placements rather than one crowded one. At the declared parameters — **60 µm edge margin, 40 µm minimum separation** — **9 of 13 bands hold ten units and 4 do not.**

| band | span µm | max sites | verdict |
|---|---|---|---|
| CSHL047 Probe01 | 700 | 15 | PASS |
| NYU-12 Probe01 | 640 | 14 | PASS |
| NYU-37 Probe00 | 580 | 12 | PASS |
| NYU-65 Probe00 | 580 | 12 | PASS |
| CSHL047 Probe00 (b52182e7) | 560 | 12 | PASS |
| NYU-45 Probe00 | 540 | 11 | PASS |
| CSHL045 Probe00 | 540 | 11 | PASS |
| NYU-39 Probe00 | 500 | 10 | PASS (exactly) |
| CSHL047 Probe00 (2d5f6d81) | 500 | 10 | PASS (exactly) |
| CSHL049 Probe00 (4b7fbad4) | 460 | 9 | FAIL |
| CSHL049 Probe00 (c99d53e6) | 440 | 9 | FAIL |
| NYU-12 Probe00 | 440 | 9 | FAIL |
| NYU-48 Probe00 | 420 | 8 | FAIL |

**Read the parameters with the verdict.** 60 µm and 40 µm are *declared*, not measured. The donor templates' real multichannel footprint has not been measured, because that needs the template arrays from the upstream zarr store and this screen downloads nothing; that measurement can calibrate the **edge margin**. It cannot by itself justify the **minimum peak separation**, which needs its own predeclared basis from the host's native peak-depth distribution and the generator's relocation constraints. The report therefore carries a full sweep, and the sweep shows the verdict is genuinely sensitive to both parameters — at a 100 µm margin only **5** bands hold ten, and at 140 µm only **2** do. Codex takes ownership of this two-part footprint/placement calibration as part of Rung 0 preparation. The gate stays parameterized until both values are justified and frozen.

### 10.3 The overcrowding half, and why this screen does not gate on it

The Claim Sheet caps injected units at ten because "more simultaneous injections change the collision and density statistics of the recording itself." That is a statement about density, so density is what overcrowding has to be judged against — and until now the project had no measurement of the host's own unit density anywhere.

It does now. Ten injected units against IBL's own sorting of the same band:

| band | native units | 'good' | +10 vs all | +10 vs 'good' |
|---|---|---|---|---|
| NYU-12 Probe01 | 267 | 60 | +3.7% | +17% |
| CSHL047 Probe00 (b52182e7) | 182 | 35 | +5.5% | +29% |
| CSHL047 Probe01 | 174 | 32 | +5.7% | +31% |
| NYU-65 Probe00 | 123 | 27 | +8.1% | +37% |
| NYU-45 Probe00 | 90 | 20 | +11.1% | +50% |
| CSHL047 Probe00 (2d5f6d81) | 74 | 22 | +13.5% | +45% |
| NYU-37 Probe00 | 86 | 12 | +11.6% | +83% |
| CSHL045 Probe00 | 108 | 10 | +9.3% | +100% |
| **NYU-39 Probe00** | **22** | **1** | **+45.5%** | **+1000%** |

Both columns are reported because they answer different questions: injected units are well-isolated single units by construction, so "vs good" is what is actually being added, while "vs all" is closer to what a sorter's clustering sees.

**The screen does not gate on either, deliberately.** The Claim Sheet fixes no overcrowding threshold, and a screening script is not the place to invent one — that is a contract decision. What the numbers do is make the consideration visible. Codex's review declines to add a post-hoc percentage cutoff: native yield can change candidate priority and trigger closer noise/SNR review, but it cannot silently become a new pass/fail gate after the values are known.

### 10.4 Two things fell out that were not the point of the screen

**NYU-39 Probe00 is a high-risk host candidate, and the placement screen is not why.** Its CA1 band holds **22 sorted units, one of them 'good'**, against 174 and 32 in a comparable CSHL047 band. It passes the geometric screen at exactly ten sites. That makes it reasonable to move behind the stronger candidates in the order of further work, but — without a predeclared yield threshold and before the noise/effective-SNR gate — it is **not formally disqualified**. This is a *yield* observation, not a noise measurement, and the distinction is preserved.

**The host amplitude table makes the 50–200 µV rescaling target worth checking; it does not validate it.** Median amplitude across all sorted units in these bands runs 20–60 µV. Across **'good'** units only it runs **51–110 µV with p90 up to 258 µV**. But the units table's `median_spike_amplitude_uV` is IBL's number on IBL's preprocessed data, and whether its convention matches the donor library's `amplitude_uv` column has **not** been verified. Until that convention check is done, the apparent bracketing cannot support a claim that the target is defensible or too loud for another population.

### 10.5 What this does not touch

**Drift and noise remain open, and this screen deliberately does not pretend otherwise.** The processed files carry a `cumulative_drift_um_per_hour` column whose values reach millions of micrometres per hour; whatever it accumulates it is not net probe drift at that magnitude, so it is recorded as uninterpreted and used for nothing. Post-rescaling effective SNR and Codex's covariate-balance gate are also untouched.

### 10.6 Where host selection now stands

Gates discharged: **anatomy** (Draft 1), **duration** (§4.4), and **label ambiguity** (§10.1). Checked non-gating property: **donor-lab separation** (§9). Parameterized but not discharged: **placement capacity** (§10.2), because the edge margin and minimum peak separation still need separate justification. Gates open: **drift**, **noise**, **post-rescaling effective SNR**, and **Codex's covariate balance**.

Still no pinned host, and that is correct — first-admissible means first to clear *every* gate, and the remaining gates have not all run. The ordering that has emerged, and that I would carry into the remaining work rather than re-derive:

1. **CSHL047 Probe01** (700 µm, 174/32 units) — the only band that holds ten at every swept parameter up to a 140 µm margin.
2. **NYU-12 Probe01** (640 µm, 267/60 units) — the densest native neighbourhood by a wide margin and the smallest relative perturbation from ten injected units.
3. **CSHL047 Probe00, session b52182e7** (560 µm, 182/35) — same recording as (1), which makes it the natural depth-specific-zones fallback; note the two probes carry **different clocks**, per §4.4.

That is a recommendation about which order to spend the remaining gates in. It is not a selection, and nothing downstream may treat it as one.

---

## 11. Session 8 — the amplitude-convention check, run

§10.4 flagged that the 50–200 µV rescaling target and the host amplitude table might not be measuring the same thing, and said so was a prompt to check rather than a check. Codex's review sharpened it: until the conventions are shown commensurate, *neither* "the target is defensible" nor "the target is too loud" is supportable. This section runs the check.

`Reproducibility Packet/scripts/audit_amplitude_conventions.py` → `results/amplitude_conventions.txt` and `.json`. **43.5 MB in 42 range requests, metadata only.** One session, `sub-KS042/ses-07dc4b76`, chosen because it is a donor session, so both sides of the question are present in one file.

### 11.1 They are not the same quantity, and the upstream source says so plainly

Read from `SpikeInterface/hybrid_template_library` at pinned commit `0023db29688842f74698bac40c48a86477ea39e7`:

| Side | What the number is | Where |
|---|---|---|
| **Donor `amplitude_uv`** | `np.ptp(templates_array, axis=1)` at the best channel — the **peak-to-peak range, over time, of the average waveform** | `upload_ibl_templates.py:326`, `consolidate_datasets.py:104,118` |
| **Host `median_spike_amplitude_uV`** | *"Median spike amplitude in microvolts"*, over a per-spike column the same file describes as *"Peak amplitude of each spike"* | the NWB's own column descriptions |

One is a trough-to-peak span of an average; the other is a median over per-spike single-sided peaks. **The comparison in §10.4 was not a valid comparison as stated.**

Three further differences are in the upstream source and survive any unit conversion: the donor averages come from a **1 Hz highpass plus common median reference** (not IBL's preprocessing), from the **last 30 minutes only**, and — this one had not been recorded anywhere in the project — from **`IblSortingExtractor(..., good_clusters_only=True)`**. The donor library is a *good-clusters-only* population by construction.

### 11.2 The conversion, measured rather than argued

The processed NWB carries `waveform_mean` per unit, in volts. That makes the donor column's *definition* computable on host units with exact unit identity and no matching problem: peak-to-peak over time, on the channel maximising it, ×10⁶.

| cohort | n | p2p of mean waveform | `median_spike_amplitude_uV` | ratio (median) | ratio p10–p90 |
|---|---|---|---|---|---|
| all units | 1,821 | 87.2 µV | 65.9 µV | **1.250** | 1.13–1.91 |
| `kilosort2_label == good` | 478 | 124.4 µV | 91.7 µV | **1.242** | 1.11–2.50 |
| `ibl_quality_score == 1.0` | 201 | 164.6 µV | 128.3 µV | **1.207** | 1.10–1.51 |

**Read the spread with the median.** A central factor near 1.2 supports a population-level restatement; the p90 does not support converting a single unit. So the target may be restated in host-column terms as *roughly* 41–165 µV, and no unit-level equivalence may be claimed.

**What that does to §10.4.** The direction of the observation survives — the restated 41–165 µV band still brackets the host bands' `good`-unit medians of 51–110 µV — but it survives on different numbers than the ones that were used to reach it, and the earlier statement was reasoning from an undefined comparison. The corrected statement replaces it going forward; §10.4 is a recorded turn and stays as written.

### 11.3 A third convention difference, found on the way

The file's own `max_electrode` — *"the electrode with maximum spike amplitude for this unit"* — agrees with the upstream peak-to-peak best-channel rule on only **72.6%** of units, usually a near tie between adjacent contacts. Every ratio above is therefore reported twice, at each side's chosen channel; the two agree to within about 0.02 in the median, so the conversion does not rest on the channel choice.

It matters elsewhere: **donor `depth_along_probe` and host unit depth are computed at best channels chosen by different rules.** Both are used for placement. The difference is one contact — 20 µm — in the disagreeing quarter, which is small against a 60 µm edge margin but is not zero, and belongs in the placement calibration Codex owns rather than being discovered inside it.

### 11.4 What the donor pool actually looks like against the target

Local computation over the tracked snapshot, no reads:

- **All 2,183 NP1.0 templates:** median `amplitude_uv` **184.2 µV**. **None** below 50 µV; **42.0% above 200 µV**. The 50–200 µV target is not centred on the donor population — it is its lower 58%.
- **The CA1 sixteen:** 105, 110, 111, 112, 117, 124, 131, 141, 175, 187, 191, 200, 213, 330, 420, 487 µV. Median **158 µV**; **four sit above 200 µV**, the largest at 487.

The target is a rescaling destination, not a filter — Amendment 2 settled that the caliper screens rather than excludes — so this cuts nobody. What it does say is that **rescaling is not a light touch on this arm**: four of the sixteen are scaled down by up to ~2.4×, and the CA1 median sits *below* the pool median, so region-matched templates are on average scaled *up* relative to region-unaware partners. Post-rescaling amplitude is a matched covariate, so this is not a residual confound after matching — but the scale factors themselves differ systematically between arms, and that belongs in the record before the manipulation check meets it.

### 11.5 A pairing that failed, recorded so nobody retries it

The obvious way to compare the two columns is to match library templates to file units. It does not work: the consolidated metadata carries **no unit identifier**, only a positional `template_index`, and the hypothesis that template order follows the file's unit order scores **at chance** (0.000–0.023) under both the `kilosort2_label` and the `ibl_quality_score` definitions of a good cluster, across all four (zarr × probe) pairings. Recovering unit identity would need the zarr store's own `unit_ids`, which is a separate reader. **The §11.2 measurement deliberately does not depend on that pairing** — which is why it was built the other way round.

### 11.6 What this closes and what it leaves

**Closed:** the convention question raised in §10.4. The two columns are different quantities; the conversion between their definitions is measured; the restated target is on the record.

**Left open, and named so it is not mistaken for closed:** whether the *preprocessing* difference matters. The donor averages are built on a 1 Hz highpass plus CMR; the host column is IBL's number on IBL's destriped data. This report measures the definitional difference and does not touch the preprocessing one. That second difference can only be measured once the stack is installed and a donor template can be rendered through the host's own preprocessing — which is Rung 0 territory, not metadata.

---

## 12. Session 9 — the CCF label map, completed without importing an ontology

§5.2 named the largest open item nobody was working on: the hand-authored label map is materially incomplete, completing it appears to need an Allen CCF ontology, and the ontology carries a licensing question that had to be read rather than assumed. This section resolves both halves. The licence answer turned out to be the interesting one, because it closed the obvious path and forced a better one.

### 12.1 The licence, read rather than inferred

**Allen Institute Terms of Use — read at `https://alleninstitute.org/terms-of-use/`, 2026-08-12.** The Content may be used, copied, distributed and built on "for research or other noncommercial purposes," and "You may not redistribute the Content or Improvements for commercial purposes without our written permission." Attribution is required, and commercial exceptions are granted only by written permission from the Institute.

**That is a genuine conflict with this project's standard, not a technicality.** *Project Details* requires commercial-use-permitting licences by default and allows a restrictive input only under an explicitly approved and named exception that states the downstream limits it creates. Importing the CCF ontology would have put a noncommercial restriction on a component of a shipped artifact — the Reproducibility Packet's label map — which is a decision about what Dandelion may release, not an implementation detail. That is a director-level call.

**The permissive redistributions do not dissolve it.** `iblatlas` is MIT (read at `https://raw.githubusercontent.com/int-brain-lab/iblatlas/main/LICENSE`: "MIT License", "Copyright (c) 2023 International Brain Laboratory") and `brainglobe-atlasapi` is BSD-3. Both are honest about their own code. Neither is the Allen Institute, and a third party's permissive licence on a redistribution is not a grant of rights over the upstream content it redistributes. Treating an MIT wrapper as laundering the terms on the data inside it would be exactly the "import on the assumption that it will be fine" that the standard forbids.

**No exception was requested and none is needed, because the ontology turned out not to be necessary.** Nothing was filed in `director_requests.md`: a request should be filed when the director is the dependency, and after §12.2 he is not.

### 12.2 The bridge is derivable from data the project already holds

The two vocabularies annotate the same physical places on the same probes, and the project holds both sides under commercial-use-permitting licences:

| side | source | licence | what it carries |
|---|---|---|---|
| host | DANDI 000409 electrodes table | CC-BY-4.0 | CCF **long name** + `rel_y` depth, per electrode |
| donor | `hybrid_template_library` rows | MIT | CCF **acronym** + `depth_along_probe`, per template |

So the correspondence can be *read off* rather than imported: a donor at 2,900 µm in session S carrying `CA1`, next to a host electrode at 2,900 µm in session S labelled "Field CA1", is direct evidence that those two strings name the same structure. This is the evidence `validate_ccf_label_map.py` already uses to **check** the hand-authored table, run in the other direction to **build** the entries it lacks.

`Reproducibility Packet/scripts/derive_ccf_label_map.py` → `results/ccf_label_map_derived.txt`, `results/ccf_label_map_derived_records.json`, and the map itself at `scripts/utils/ccf_label_map_derived.json`. **146.6 MB in 150 range requests, metadata only, no recording data read**; 32 of 37 donor insertions assigned a probe; 2,053 donor rows placed, none outside the 20 µm tolerance.

**Result: 138 entries emitted, 94 of them structures the hand-authored table did not contain.** By tier: 119 acronyms saw exactly one host name, 23 cleared the two-thirds majority, 2 were ambiguous and are not emitted.

### 12.3 The audit, which is the part that was not planned

Every emitted entry is compared against the hand-authored table. This is a check nobody had run and the existing validation could not give: that run could only test names the table already contained, so it could confirm the table's *acronyms* but never its *long-name spellings*.

**44 AGREE. 0 DISAGREE.** Every hand-authored entry the derivation reached independently reproduced its long name and acronym. The hand-authored table has now been checked from both directions and has no known error.

**That result depended on getting the comparison right, and the first version got it wrong.** Comparing raw strings reported 31 disagreements; 30 were punctuation. The NWB export strips the commas the canonical Allen names carry, so `"Primary motor area Layer 5"` and `"Primary motor area, layer 5"` are the same structure and `to_acronym` already resolves them identically through `normalise`. **An audit that does not use the same key its lookup uses is not auditing the lookup.** The comparison now runs on the normalised key and the 30 false alarms are gone; the one real finding survived as a collision (§12.4).

### 12.4 Two entries withheld, and why the withholding matters more than the entries

A map keyed by long name can have two acronyms win the same name. The first version wrote them into a dict and **silently kept whichever came last** — the classic quiet failure the *Software engineering* standard exists to prevent. Collisions are now refused outright and reported:

- `'Periaqueductal gray'` — claimed by `PAG` (50 votes, 4 insertions) and `IVn` (2 votes, 1 insertion). `IVn` is the trochlear nerve; it is not PAG. One donor sat one contact outside its own structure.
- `'posteromedial visual area layer 6a'` — claimed by `VISpm6a` (12 votes) and `VISpm5` (2 votes). A layer-5 donor nearest a layer-6a electrode.

Both are boundary contamination, and in both cases the majority claimant is obviously right. **Neither is emitted anyway.** The rule is not "prefer the better-supported claim" — this evidence cannot establish which claim is correct, only which is more common, and a map that resolves collisions by vote count would resolve a genuinely ambiguous one the same confident way. Two structures lost is a small price for a rule that cannot quietly guess.

### 12.5 What this closes, and the ceiling it does not cross

**Closed:** the donor side, completely. Every acronym the donor library uses in these 32 insertions is now either defined or explicitly reported as unresolvable, and the licence question in §5.2 is answered without an exception.

**The ceiling, stated plainly:** a host structure that holds no donor template cannot be derived by this method, however common it is in the host. Across the 209 distinct host long names seen on the assigned probes, **143 are mapped and 66 remain unmapped**. Those 66 are not resolvable from this evidence and would need the ontology — which means the licence question returns if the region-unaware arm's placement ever lands in one of them.

**Do not read the 66 against §5.2's 296.** The 296 came from the 46 screened recordings; the 209 here are the host names on the 32 donor-session probes. Different denominators over different recording sets. The honest statement is the one in the report: the derivation reached 143 of the 209 names it saw.

### 12.6 How it is wired, and what it deliberately does not change

`utils/ccf_labels.py` gains the derived layer as **opt-in on every call**. `to_acronym(label)` keeps its original hand-authored-only behaviour; `to_acronym(label, include_derived=True)` consults the derived layer, with the hand-authored entry always winning where both define a label. `provenance(label)` reports which layer answered — `hand-authored`, `derived:unanimous`, or `derived:majority` — so a region assignment can be reported with the strength of the evidence behind it rather than presenting a validated entry and a derived one as equally established.

**The default was chosen so no existing consumer changes meaning underneath itself, and that was verified rather than asserted:** `validate_ccf_label_map.py` was re-run after the module change and reproduced `results/ccf_label_map_validation.txt` **byte for byte**.

**The validation report was deliberately not regenerated against the derived map.** Validating derived entries with the evidence they were derived from would agree trivially and would look like independent confirmation. The 44 AGREE rows in §12.3 are the non-circular part — they test the table that was written before the data was consulted — and they are the only confirmation claimed here.

### 12.7 One structural fact about the donor vocabulary, found on the way

**The donor library's acronyms sit at mixed levels of the CCF hierarchy.** `MB` (Midbrain) and `OLF` (Olfactory areas) are parent structures, and they appear alongside `MRN` and `PIR`, which are their descendants. `MB` in particular is a majority entry precisely because host electrodes near `MB` donors are sometimes labelled with a child structure.

This matters for the region-unaware arm and belongs in Codex's balance gate rather than here: **"same region" is not a well-defined test when one label is a parent of the other.** A donor labelled `MB` is not region-matched to a `MRN` injection zone in the sense Tier A means, and it is not cleanly mismatched either. CA1 is unaffected — it is a leaf structure and its sixteen donors are all labelled `CA1` — so this is not a Tier A blocker, but any zone change should check whether the candidate region has parent-labelled donors before assuming the region axis is clean there.

### 12.8 Replay

`derive_ccf_label_map.py --from-records` rebuilds the report and the map from `results/ccf_label_map_derived_records.json` with **no network reads at all**, the same pattern `screen_injection_placement.py --from-records` established. Verified: the replayed report and JSON are byte-identical to the tracked ones. Any later change to a tier rule, the majority fraction, or the presentation costs nothing and touches no remote file.
---

## 13. Session 10 — how hard a region-blind matcher pulls toward the injection zone

This section exists because of something Codex found in Amendment 3 and neither of us then asked about the real arms.

### 13.1 Where the question came from

Codex's Session 9 review removed the injection zone's donor pool from **both** negative-control pseudo-arms, not just from P1. Its reason: P2 is covariate-matched to P1, and P1 is chosen to resemble the CA1 sixteen, so a P2 that could still draw CA1 templates would draw them *preferentially* rather than by chance — leaving the two pseudo-arms under different region conditions. That reasoning is correct and I accepted it.

It also applies to the **real** contrast, where it is stronger, because there the matching target is not a CA1 lookalike but the CA1 sixteen themselves. Slot 5's control draws "without conditioning on region," which is region-*blind*, not zone-free: the sixteen are eligible to be their own controls. Nothing in the contract said what happens if the matcher reaches for them — and the matching rule has not been written yet, so nothing was going to say until it was too late to say it cleanly.

### 13.2 What was measured

`Reproducibility Packet/scripts/audit_zone_neighbour_enrichment.py` → `Reproducibility Packet/results/zone_neighbour_enrichment_CA1.txt`. Stdlib only, run against the tracked snapshot, **no network reads**.

Over all 2,183 Neuropixels 1.0 templates, standardizing `amplitude_uv`, `signal_to_noise_ratio` and `depth_along_probe` over the pool:

| quantity | value | region-blind expectation |
|---|---|---|
| CA1 templates whose nearest covariate neighbour is also CA1 | 3 of 16 | 0.687% per non-self draw |
| control partners that are CA1, nearest-unused-partner matching | **3 of 16** | 0.11 |
| control partners that are CA1, **exact-insertion blocking** | **8 of 16** | 1.03 |

Under the provisional 50–200 µV / SNR 5–15 caliper the same two matchers give 2 of 12 and 5 of 12 against 0.12 and 1.17.

The blocked row is the one that matters, because exact-insertion blocking is not an exotic variant: Amendment 2 makes it the **first** granularity the balance procedure must attempt, before falling back to session and subject. Under this simple diagnostic matcher and its pre-host covariates, half of the selected control partners are injection-zone donors.

Two denominators are worth having in view so the blocked number is not over-read. CA1's share of its own insertions is 6.2%, 25.0%, 6.8% and 4.9% (80, 8, 88 and 61 templates respectively), so 8 of 16 is far above what CA1's presence in those insertions would give on its own — which is what the corrected 1.03 no-reuse expectation computes. Six of the eight come from the KS051 insertion, which holds six of the sixteen.

### 13.3 The boundary, which is wide

- The covariates are the donor table's own columns. The real matching uses **post-rescaling** amplitude, **effective host** SNR, and depth along the injection band, none of which exist until a host is pinned. These are their pre-host analogues.
- The matcher is a plain greedy nearest-neighbour. It is not a proposal, and it is not Codex's rule; it is a stand-in chosen because there is no rule yet, which is the point.
- Sixteen is small. Three-of-sixteen and eight-of-sixteen are coarse counts, not estimates with useful precision.

**So this measures the size of a pull, not the composition of an arm.** It is evidence that the question has to be answered before the rule is written, not evidence about what any particular rule would produce.

### 13.4 What I did with it

Wrote **Amendment 5** (Proposed, Session 10) rather than edited anything. It proposes removing the injection zone's donor pool from the real region-unaware arm's eligible pool, on the argument that the pull is manufactured by *our* pairing rather than inherited from the anchor pipeline: the anchor does not covariate-match its templates to a region-matched set, because it has no such set. A genuinely uniform region-blind draw would contain 0.12 zone donors in expectation, but Codex's review found that this is only the anchor-policy component of the removal's cost. Because zone donors can also be the closest covariate matches and satisfy preferred provenance blocks, the amendment now requires the same frozen matching rule to be reported on the eligible pool both before and after removal. The un-removed run is diagnostic only; the post-removal run is the sole executable state.

The amendment also requires the matching rule to be fixed before the eligible pool is visible and to contain no term referencing region membership in either direction. **It does not write that rule** — that is Codex's under the labor split. It constrains when the rule is fixed and what it may not mention.

### 13.5 One thing this does not settle

Amendment 5's removal set is well defined for CA1 because CA1 is a leaf and all sixteen donors carry that exact label. §12.7's mixed-hierarchy finding says that is not general: for a zone whose label has an ancestor or descendant in the donor library, "the injection zone's donor pool" has to be defined before the rule can be applied to it, and a string match on the acronym is not that definition. That is written into the amendment as a stated boundary rather than left for a future session to rediscover.

---

## 14. Session 11 — the no-reuse baseline re-derived, and two things it exposed in the contract

Codex's Session 10 review corrected §13's expectation column and added a requirement to Amendment 5. This section records what re-deriving that correction found, because two of the three findings are about the contract rather than about the arithmetic.

### 14.1 The corrected baseline is right, checked three ways rather than read

Codex replaced §13's expectation with the exact inclusion–exclusion expectation for **injective, non-self** assignments — the null that carries the diagnostic matcher's own constraints, since `greedy_partners` never reuses a control partner and never partners a template with itself. I re-derived it by three routes that share no code with the audit script:

| route | what it does |
|---|---|
| exhaustive enumeration | every injective non-self assignment, pool sizes 2–8, every zone count |
| a counting DP | inclusion–exclusion over self-pairs, then splitting free slots between zone and non-zone targets |
| Monte Carlo | rejection sampling, 400,000 accepted assignments per case |

All three agree with the formula to floating-point equality on every enumerated case (**0 mismatches over 28 (pool, zone) pairs**), and the Monte Carlo agrees to within 0.002 at n = 20/88/60. Recomputing the aggregate from the pinned snapshot through a separate CSV path reproduces Codex's numbers exactly: full pool **0.1100**, exact-insertion blocking **1.0321**, and inside the provisional caliper **0.1151** and **1.1694**. The superseded independent-slot baseline gives **0.9837** for the blocked case, which is the 0.98 that was there before — so the correction moves the blocked expectation up by about 5%, and the realized 8-of-16 is now compared against a slightly *more* permissive null. **The correction makes the diagnostic weaker, not stronger, which is the direction that should be trusted.**

The per-insertion decomposition is worth keeping, because it shows where the blocked expectation comes from: KS051 contributes 0.349 of the 1.032 (6 CA1 among 88), KS044 0.256 (5 among 80), KS042 0.326 (2 among **8** — a tiny block, so a large per-slot rate), and KS055 0.102 (3 among 61). The eight-template insertion is doing disproportionate work in the *expectation*, while KS051 is doing it in the *realized* count.

### 14.2 The two expectations in Amendment 5 were two models wearing one label

Amendment 5's table gives **0.11** as the region-blind expectation, and four paragraphs later its rationale gives **0.12** for "a genuinely uniform region-blind draw." Both numbers are correct and they are not the same quantity:

- **0.110** is the paired matcher's null: sixteen control slots, one distinct partner each, no template partnered with itself.
- **0.117 → 0.12** is an anchor-like pipeline's null: sixteen donors drawn region-blind with no pairing at all, so nothing is excluded as a self. Hypergeometric, `16 × 16 ⁄ 2,183`. Its P(at least one) is 0.1114, which is the "about one arm in nine" the amendment states — confirmed, not inherited.

The gap between them is exactly the pairing's self-exclusion. Nothing was wrong; two numbers in the same unit were carrying the same label with no note, which is the failure this project logged as its own lesson after the Session 8 amplitude work. Both sheets now say which model each number belongs to, and why the unpaired one is the right answer to the fidelity objection: the fidelity objection is a claim about *the anchor's* policy, and the anchor does not pair.

### 14.3 Amendment 5 makes a sentence in Amendment 3 false, and nothing said so

This is the finding that mattered most and it is not a numerical one.

Amendment 3's boundary paragraph — `In force` — says the negative-control band "does not mirror the chance injection-zone templates that the real region-unaware arm may contain." Amendment 5's point 1 removes the injection zone's donor pool from the real region-unaware arm, which makes that arm's post-removal eligible pool **the same object** as Amendment 3's shared pseudo-base pool. After that, the real region-unaware arm contains no zone templates by construction, so there are no chance zone templates for the band to fail to mirror.

Left alone, the contract would have carried two `In force` clauses pointing opposite ways, and the stale one implies the real control arm may contain zone donors — which is the direct negation of Slot 13.11. A reader reconstructing the design from the amendment stack would have had no way to tell which clause won.

The fix respects append-never-overwrite: Amendment 3's text is untouched, and Amendment 5 now carries a **What this supersedes** paragraph naming the clause and dating its retirement. The supersession is deliberately narrow — the rest of that paragraph still holds, including that the band cannot mirror the matched pool's region homogeneity, which no no-manipulation control can. Amendment 3 point 3's "control-only safeguard" is scoped in the same paragraph rather than called false, because it describes Amendment 3's own removal accurately.

**The general lesson, since this is the second amendment in a row where the finding came from a neighbour rather than from the thing under review:** an amendment that changes a design property must be checked against every in-force sentence that *describes* that property, not only against the slots it lists as affected. Amendment 5's header names Slots 5, 7, 11.3 and 13. The sentence it falsified is in Amendment 3.

### 14.4 What is still open in this document

Unchanged by this session: no host is pinned; drift, noise, post-rescaling effective SNR, the footprint/placement calibration and Codex's covariate-balance gate remain open; the recommendation order in §10.6 stands as a recommendation and not a selection.

---

## 15. Session 17 — the candidate order, pinned

### 15.1 Why this is a section and not a preference

Codex's ruling 7.3 settled the standard: apply the remaining gates sequentially to the current candidate set and pin the **first fully admissible** host, labelled admissible rather than best. I accepted it in the same exchange and have repeated it in every continuity file since. What neither of us noticed is that **first-admissible is not a rule until the order is fixed.** "First" is a property of a sequence, and the sequence has lived in §10.6 as an explicit recommendation — "That is a recommendation about which order to spend the remaining gates in. It is not a selection" — which means that until now, a host that failed a gate would have been followed by whichever host the next session thought was worth trying next.

The defect is the same shape as the one Codex closed in the matching rule this week. A pinned threshold evaluated at an unpinned site is not a pinned threshold; a pinned matching rule over redrawable placements is not a pinned matching; and a first-admissible rule over an unpinned candidate order is not a rule at all. In each case the machinery is precise and the input it consumes is free. Here the free input is consequential in a specific way: every host brings its own candidate sites, its own surviving target set `T`, its own exposure schedule and therefore its own balance report, so an unpinned order is compatible with working down the list until one of them reads well.

This section pins the order. It is the closure of the non-claim recorded in §10 of `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`, where the host-rejection semantics that make the ordering load-bearing are written down.

**The timing claim, stated so it can be checked rather than trusted: as of this section, no drift, noise, or post-rescaling effective-SNR value has been measured for any candidate.** The gates that will decide have not been run on anyone. The order below is therefore fixed before its consequences are visible, which is the only property that makes it worth fixing at all.

### 15.2 The rule that produces the order

Two inputs, both already recorded, and no new machinery:

1. **The three hosts §10.6 named, in the order it named them.** That ordering came out of the placement-capacity sweep (§10.2) and the native-yield table (§10.3), both measured and published before any open gate existed, and the reasoning behind it is in the document. Judgment already exercised and recorded in public is not the thing that needs constraining; judgment exercised later, after a gate outcome, is.
2. **Every remaining candidate in the §4.2 table, ordered by descending contiguous `Field CA1` channel count, ties broken by ascending `(subject, session, probe)` as ASCII strings.** This carries no judgment at all: §4.3 already says channel count is "a convenient ordering, not a quality score," which is exactly what recommends it here. A tail order that expressed a preference would reintroduce the freedom the section exists to remove.

A digest ranking of the kind Amendments 3 and 6 use was considered and rejected. It would be equally deterministic and strictly more machinery, and the table's own column already determines a total order once the tie-break is stated.

### 15.3 The pinned order

| rank | probe | subject | session | CA1 ch | source of rank |
|---:|---|---|---|---:|---|
| 1 | Probe01 | CSHL047 | `b52182e7` | 72 | §10.6 recommendation, first |
| 2 | Probe01 | NYU-12 | `a8a8af78` | 66 | §10.6 recommendation, second |
| 3 | Probe00 | CSHL047 | `b52182e7` | 58 | §10.6 recommendation, third |
| 4 | Probe00 | NYU-37 | `7af49c00` | 60 | tail rule |
| 5 | Probe00 | NYU-65 | `a2ec6341` | 60 | tail rule |
| 6 | Probe00 | CSHL045 | `034e726f` | 56 | tail rule |
| 7 | Probe00 | NYU-45 | `51e53aff` | 56 | tail rule |
| 8 | Probe00 | CSHL047 | `2d5f6d81` | 52 | tail rule |
| 9 | Probe00 | NYU-39 | `6ed57216` | 52 | tail rule |
| 10 | Probe00 | CSHL049 | `4b7fbad4` | 48 | tail rule |
| 11 | Probe00 | CSHL049 | `c99d53e6` | 46 | tail rule |
| 12 | Probe00 | NYU-12 | `a8a8af78` | 46 | tail rule |
| 13 | Probe00 | NYU-48 | `3d59aa1a` | 44 | tail rule |

Two consequences of the construction are worth naming rather than leaving to be noticed.

**Ranks 4 and 5 carry more CA1 channels than rank 3.** That is the recommendation being honoured over the mechanical key, and it is deliberate: §10.6's third entry is the depth-specific-zones fallback for the recording at rank 1, which is a structural reason the channel count does not see.

**NYU-39 Probe00 lands at rank 9 with no special handling.** §10.4 recorded it as a high-risk candidate on native yield — 22 sorted units in the band, one of them `good` — and said in terms that it is "not formally disqualified" without a predeclared yield threshold. Moving it by hand would be applying a gate the contract does not have, under the name of ordering. The mechanical key puts it in the back half anyway, which is what §10.4 asked for.

### 15.4 What happens when the list is exhausted

If the strict and relaxed passes in §16.7 both fail to produce a fully admissible host from the thirteen above, the anatomy survey resumes with the identical command and the same recorded `--index`, exactly as §4.1 says it can. The continuation order is the order of the tracked asset cache `Reproducibility Packet/results/dandi_000409_assets.json`, SHA-256 `54f8e600ccedf36f2b284a9dacc58277aed24155f9a6915ad60b339437392f70`; **newly discovered candidates are appended in that cached discovery order** and evaluated under the already-in-force relaxed threshold.

Cached discovery order, not channel count, and the reason is timing rather than taste. By the time the survey resumes, the gates' behaviour on the first thirteen will be known, and any re-sort of the new candidates would be a sort informed by that knowledge. Pinning the cache bytes makes the continuation order reproducible rather than dependent on a later live API listing. It is also, by §4.1's own account, clustered by subject and lab, so it is not a random sample and this document does not claim it is one; it claims only that it is fixed independently of anything this project will learn.

### 15.5 The gate order, and why it does not change the verdict

A host is admissible only if it clears **every** gate, so the order in which the gates run cannot change which host is admissible. It changes only what the project spends to find out. Cheapest-informative-first, and the last two entries are ordered by necessity rather than by cost:

1. **drift** — §16, computable from the processed units table over targeted range reads;
2. **noise** — needs raw sample data and is therefore the first gate with a real transfer cost;
3. **post-rescaling effective SNR** — needs the noise estimate and a rendered donor, so it follows (2);
4. **the joint ten-placement gate** — cannot run until the target-eligibility manifest and the exposure rota exist, which per Amendment 6 point 1 is after `N` is known, and per Draft 6 of the matching rule is after the schedule/placement specification and the matcher have both been approved on synthetic inputs;
5. **Codex's covariate-balance and manipulation gate** — last by construction, and it is a stop-or-go on the configuration rather than on the host alone.

A host is carried forward only while it is passing. The strict pass evaluates ranks 1–13 sequentially under the 20 µm rule in §16.7; the first host to clear (1) through (5) is pinned, and the ones below it are never evaluated. If none clears all five gates, the single predeclared 40 µm relaxation restarts the same order at rank 1. Threshold-independent results may be reused, but admissibility is recomputed under the relaxed rule and no rank changes. Only after all thirteen fail that relaxed pass does §15.4 resume the survey and append new candidates. This two-pass order is what makes the relaxation compatible with first-admissible selection rather than an exception applied only to whichever candidate happened to fail last.

### 15.6 The boundary on this section

This pins an **order**, not a host. No candidate has been selected, no gate has been discharged by this section, and the recommendation in §10.6 keeps its recorded status as a recommendation — this section is what converts it into a commitment, and the conversion is dated here rather than backdated there.

The order binds from the moment both agents have approved this state. Changing it afterwards is not a working decision: it requires a recorded turn in `chats/Claude-Codex/Tier A Selection Review/` naming what changed and why, written before the change takes effect, and if the reason is anything a gate outcome told us, the honest answer is that it cannot be changed at all.

---

## 16. Session 17 — the drift quantity, defined before anything is measured

### 16.1 The order of operations, and why it is this way round

The rule this section obeys is one this project has already paid for: *a measurement you just made is not a threshold you get to set*. So the quantity and the basis of its threshold are written now, while no candidate's value is known, and the measurement session inherits them rather than choosing them. Everything below is falsifiable against the archive; none of it is a result.

### 16.2 The column that looks like the answer, and is not

The processed files carry `cumulative_drift_um_per_hour`, and it has been sitting in the units table since §10.5 recorded it as uninterpreted. Its own first-party description settles what it is:

> "Sum of absolute depth changes between consecutive spikes, normalized to um/hour. Formula: `sum(abs(diff(spike_depths)))/duration*3600`. High values indicate either electrode drift or depth estimation noise. Scales with spike count (~0.79 correlation). NOT actual electrode displacement."

Three disqualifications, and the third is IBL's own.

**It is a path length, not a displacement.** A summed absolute difference grows with every wiggle, so a probe that moves 5 µm down and 5 µm back scores the same as one that moves 10 µm and stays. What the sorter has to survive is the displacement, because that is what moves a unit's waveform across contacts; the path length is the wrong functional entirely.

**It scales with spike count**, at a correlation IBL reports as ~0.79. That makes it a partly a measure of how busy the band is, and this project cannot afford that particular contamination: **Tier B's whole manipulation is population-rate coupling**, so a host chosen for scoring low on a spike-count-correlated quantity is a host chosen partly for being quiet, which biases the tier before it starts. This is the reason the replacement had to be built rather than the column re-scaled — a per-spike normalization would remove the count scaling and leave the path length.

**The description says outright that it is "NOT actual electrode displacement."** The correct reading of `cumulative_drift_um_per_hour` is that it is a contamination flag whose two causes — movement and depth-estimation noise — it does not separate. It stays uninterpreted and it gates nothing. The ~0.79 correlation is IBL's reported figure and is cited as theirs; this project has not reproduced it and does not need to.

### 16.3 What the archive actually exposes

The processed units table carries **`spike_distances_from_probe_tip_um`** — "Distance from the probe tip for each spike in micrometers, computed from waveform center of mass" — as a ragged per-unit array with its own index, alongside `spike_times` on the same structure. Per-spike depth and per-spike time are therefore both available without raw data and without re-sorting, and the ragged index means only the units in the CA1 band need to be read.

That is the whole reason a replacement is possible at all, and it was already downloaded and described in `Reproducibility Packet/results/amplitude_conventions.json` before this session — the same lesson as §9's, arriving again: read the rich first-party table's own column descriptions before deciding a quantity is unavailable.

### 16.4 The quantity

For one probe, one band, and one recording:

1. **Unit set.** Units whose valid same-probe `max_electrode` resolves to a finite electrode-table `rel_y` inside the pinned CA1 band. The gate is about drift *at the injection zone*, and drift along a Neuropixels shank is not uniform. This is the same anatomical coordinate and the same unit-membership rule `screen_injection_placement.py` used for §10's native band yields, and it is **blind to `kilosort2_label`**: every unit whose peak electrode lands in the band contributes, exactly as that script's in-band set did, and the `good`-only counts §10 reported beside it are not a filter here. `distance_from_probe_tip_um` does **not** select the unit set. The per-spike `spike_distances_from_probe_tip_um` values enter only steps 3–6, where each unit is centred on itself and the result is an excursion; a constant offset between waveform centre-of-mass depth and electrode `rel_y` therefore cannot move the band or alter the statistic.
2. **Bins.** The recording is partitioned into fixed 60-second session-grid intervals `[60b, 60(b + 1))` from session `t = 0`, the documented origin of the processed asset's `spike_times`, identical for every unit and every candidate. The recorded extent is the raw AP stream's final aligned timestamp `t_last_s`; `n_bins = floor(t_last_s / 60 s)`. Every analysed interval is a full 60 seconds on that clock; a final underlength grid interval is discarded and its duration is reported. This does **not** assert a full 60 seconds of AP coverage in bin 0 when `t_first_s > 0`; the declared head-coverage exception is recorded below. Sixty seconds is IBL's own `presence_ratio` bin and gives 54 to 87 analysed bins across the measured extents in §4.4 — enough to resolve a slow ramp, coarse enough that a bin holds many spikes for a typical unit.
3. **Per-unit, per-bin depth.** `d_u(b)` is the **median** of `spike_distances_from_probe_tip_um` over unit `u`'s spikes in bin `b`. A median, because a center-of-mass depth estimate on a single spike is noisy and occasionally wild, and because a median carries no spike-count term: adding observations can move a realized sample median, but it cannot mechanically accumulate a positive contribution per spike the way the path-length column §16.2 retires does, and what more spikes buy here is a smaller sampling error rather than a larger value.
4. **Centring.** `delta_u(b) = d_u(b) - median_b' d_u(b')`. Each unit is expressed as a displacement from its own typical depth, so units at different depths in the band can be pooled. The reference is the unit's own median across bins rather than its first bin, because the first bin is an arbitrary and equally noisy choice.
5. **The band trace.** `D(b) = median over available included units of delta_u(b)`. A median across units, because real probe movement is common to every unit in the band while depth-estimation noise and unit-specific instability are not. Every analysed bin must contain valid medians from at least five included units; an invalid bin makes the candidate unmeasurable rather than being omitted from a window.
6. **The reported quantities, both peak-to-peak band excursions:**
   - `Delta_full = max_b D(b) - min_b D(b)`, over the whole recording;
   - `Delta_10min = max over every eleven-consecutive-analysed-bin window of (max_b D(b) - min_b D(b)) within that window`.

**Why the ten-minute window is eleven bins.** A bin median is a point summary, so ten of them span only nine minutes between the extremes; and a 600-second segment that does not begin on a bin edge touches eleven session bins rather than ten. Both errors cost exactly one bin, both are permissive, and eleven consecutive bins fix both at once, because eleven bins contain every bin any ten-minute segment can touch. `Delta_10min` therefore bounds the range of the bin-median levels across a ten-minute segment wherever it lands on the grid. The two failures the ten-bin definition permitted are permanent harness cases rather than an argument. A common `2.1 µm/min` ramp displaces `21.0 µm` in ten minutes and reported `19.145 µm` over ten bins — under the strict tolerance — against `21.258 µm` over eleven, which fails it. Common bin levels `[0, 15×9, 30, ...]` report `15.000 µm` from every aligned ten-bin window while the off-grid segment `[30 s, 630 s)` spans `30.000 µm`, which the eleven-bin window reports in full. **Widening the window can only raise the statistic** — every ten-bin window sits inside an eleven-bin one, checked at zero violations over 2,000 random traces — so this is a tightening: it can turn a pass into a rejection but never the reverse, and §16.7's pre-declared 40 µm relaxation is what covers the case where it rejects the whole order.

**What no window length repairs is motion confined below the bin width — and how much of it reaches the bin medians is not fixed, which Draft 23 got wrong.** A median tracks rank, so displacing `k` of a bin's `n` spikes upward carries that bin's median toward the depths sitting `k` ranks above it, and how far away those are is a property of the within-bin depth distribution rather than of medians. Where every spike in a bin shares a depth, a 30 µm episode confined to one bin reports `0.000 µm` at every displaced fraction below one half, `15.000 µm` at exactly one half and `30.000 µm` above it — **that sweep is the behaviour of that fixture and of nothing wider.** Where the depths are spread, the same episode passes almost entirely through: on Codex's RC-001 Round-2 construction, each bin holding 49 spikes at one depth, two just above them and 49 far above, displacing the first 49% by 30 µm moves the bin median `29.000 µm` and fails the strict gate — and it does so at a displaced fraction as low as one fiftieth, while a single displaced spike in a hundred already moves that bin's median `14.500 µm` — so there is no fraction at which this fixture is blind, let alone one half. Where the episode falls on the bin grid matters for the same reason, because the grid is what fixes `k`: the same displaced spikes report `30.000 µm` inside one bin and `0.000 µm` split across two. What holds across all of them is a bound rather than a cutoff — a bin median moves by at most the displacement itself and at most the distance to the depth `k` ranks above it, checked at zero violations over 4,000 random cases across four depth families — and the equal-baseline sweep is simply the corner where that distance is zero. A downward displacement is the same statement read the other way, because negating every depth negates the median; the harness measures the mirrored construction rather than assuming it, and it reports the same `29.000 µm`. **So the gate has no guaranteed resolution below the bin width in either direction: `Delta_10min` is not a bound on sub-minute motion, and it is not reliably blind to it either.** Both directions are live and neither is stated here as a safety property: an episode the medians do not express passes a candidate the gate did not actually clear, and one they express in full rejects a candidate over motion that is not sustained drift. It is declared rather than repaired because §16.7's inclusion floor is ten spikes per bin, so any sub-bin statistic would rest on five or fewer centre-of-mass depths for a marginal unit and would reintroduce exactly the per-spike noise the bin median exists to remove. A candidate that passes this gate is admissible against drift *expressed at 60-second resolution*, and none of the per-bin numbers above bounds `Delta_10min` itself, which composes a second median across units on top of them.

**Why the unit set is quality-label-blind, what the alternative would cost, and what is not guaranteed.** The processed units table carries `kilosort2_label`, and §10 reported its band yields both ways, so "the units in the band" is not self-interpreting and the choice belongs here rather than in whoever writes the reader. It is made in the label-blind direction because `kilosort2_label` is a sorter's cluster-confidence label rather than a direct criterion for whether a unit's depth trace can carry common movement. §16.7's inclusion rule — at least 10 spikes in at least 80% of bins — removes units on the temporal support this quantity actually needs. **The stakes are measured, not hypothetical.** Across the thirteen pinned candidates §10 counted 22 to 267 band units but only 1 to 60 labelled `good`, and six of the thirteen hold 13 or fewer; NYU-39 Probe00 holds exactly one. Under a `good`-only reading, §16.7's requirement of five included units in every analysed bin would make rank 9 unmeasurable by construction — disqualifying it through the drift gate for the yield reason §10.4 deliberately declined to gate on — and would leave five further candidates holding 8 to 13 `good` units against that floor of five, before the inclusion rule has removed anything.

The label-blind choice does **not** carry a one-way mathematical safety guarantee. Adding units changes both the across-unit median trace and the permutation null; weaker, biased or movement-insensitive traces can damp an apparent common excursion without necessarily widening `Q95_null`. The deterministic review fixture in `agents/Codex/tools/probe_draft16_safety_claims.py` demonstrates the permitted failure shape without claiming it occurs in IBL data: five units sharing a 30 µm ramp fail the 20 µm gate at `Delta_10min = 27.273 µm`, `Q95_null = 11.591 µm`, while adding six flat traces makes the label-blind eleven-unit set pass at `0/0 µm`. The result is therefore conditional on the predeclared label-blind IBL unit set and on movement being expressed in enough of those depth traces for the across-unit median to carry it; the systematic-bias boundary in §16.5 remains operative. The reader reports, for both the in-band and temporally included sets, total count, `good` count, every unit-table row identifier and its stored quality label so that composition is auditable without turning the label into a hidden threshold.

**The conditional has to be as checkable as the published record can make it, so the reader also reports the per-unit excursions.** A conditional that nothing measures is a limitation sentence doing a rule's job. The failure shape the fixture exhibits *can* carry a visible signature — a minority of units moving while the across-unit median stays flat — in quantities the estimator already computes on its way to `D(b)`. How far that visibility reaches is settled in the next paragraph rather than assumed here, and it does not reach as far as certifying the conditional. For every included unit, the reader therefore reports three centred excursions beside `Delta_full` and `Delta_10min`: the whole-recording range, that unit's own worst gate-window range, and its range inside the band-selected gating window. The own-worst value carries its starting bin; both windowed values carry their count of defined bin medians. A windowed value is *undefined* rather than zero when fewer than two bin medians are defined inside its span, so what the count adds is the difference between a range resting on two levels and one resting on ten. Where several windows tie — for a unit's own worst or for the band's — the earliest is taken. That is the shipped behaviour, and it is declared here rather than left to the code because `window_start` and `unit_max_window_start` are both reported and a reader re-deriving either needs the rule. The band-aligned value shows what contributed in the window selected from `D(b)`; the own-worst value is also required because a suppressed or flat band trace can select an arbitrary earliest tie and thereby point its aligned audit at the wrong window. A deterministic localized fixture makes that boundary concrete: five units move 30 µm only across a late ten-bin span and six remain flat; the band reports `Delta_10min = 0`, selects window 0, and all eleven band-aligned unit values are `0`, while the five own-worst unit values remain `30 µm`. The whole-recording values alone do not settle the ten-minute question because the same range could have accumulated slowly across the session.

**How these values may be read, and the three readings that would be wrong.** They carry no null of their own. `Q95_null` grades `D(b)`, which is a median *across* included units, so it is the noise floor of the band statistic and not of any single trace. The ordering is not fixed. In homogeneous independent-noise fixtures with no movement, every included unit's own-worst window excursion exceeds the band's `Q95_null` at 9, 14 and 25 units, with the smallest per-unit value sitting at about 1.6 times `Q95_null` at nine units and about 2.8 times it at twenty-five. But a quiet heterogeneous fixture reverses the ordering: one temporally valid flat unit has an own-worst excursion of `0 µm` while four noisy units make the band `Q95_null` non-zero. What produces that reversal is the heterogeneity rather than the exact flatness of that one unit, which matters because a degenerate construction invites a reader to dismiss it: a unit merely three times quieter than its neighbours — 6 µm against their 18 µm — still sits below the band null, at `11.430 µm` against `Q95_null = 17.157 µm`. Reading a per-unit excursion against `Q95_null` — or against `L`, the only other micrometre-scale number this section publishes — is therefore undefined in either direction, because neither number grades the per-unit statistic. What these values can do is flag within-recording heterogeneity consistent with the failure shape the audit exists to expose: a subset separated in magnitude from the rest of that same set whose own-worst windows overlap one another. That pattern is not attribution to movement; heterogeneous depth-estimation noise can also produce it, so it is published only as a limitation on the band result. **And its absence licenses nothing either, which is the direction that matters, because it is the one a reader reaches for when a candidate passes.** The separation is visible only while per-unit depth noise stays small against the movement, and that is a property of the noiseless localized fixture rather than a guarantee. A deterministic fixture built entirely inside the parameters §16.7 already admits — forty-one units firing just above the ten-spike inclusion floor, twenty of them ramping 30 µm inside one gate window — **passes both gate numbers** at `Delta_10min = 14.941 µm` and `Q95_null = 7.125 µm`, while the moving units' own-worst excursions of `[32.5, 57.0] µm` overlap the stationary units' `[20.9, 37.6] µm` and seven of the twenty sit inside the stationary range. **That fixture is one construction and licenses nothing about how the masking scales.** Draft 22 said here that the masking gets easier as the band gets larger, citing `21.98`, `18.14` and `14.94 µm` at 11, 21 and 41 units. That series was not at a fixed moving fraction — `5/11`, `10/21` and `20/41` are `0.4545`, `0.4762` and `0.4878` — and at a genuinely fixed 40% moving fraction the direction does not hold: at fixture seed 7025 the same construction reports `12.192`, `11.529` and `14.190 µm` at 10, 20 and 40 units, and **35 of the 120 seeds in `7000`—`7119` are not monotone decreasing.** The band statistic has no fixed direction in the unit count, and no inference from the pinned candidates' 22 to 267 band units follows from this fixture. Both the fixture and the counterexample are permanent harness cases so that no later draft re-derives a direction from a single series. A published audit showing no separation is therefore not evidence that the conditional in the paragraph above holds; the conditional stays a limitation of the drift result and these values narrow it only in the direction where they do separate. This narrows what the audit is claimed to do and changes no verdict, because nothing consumes these values. Neither the concentration nor the scatter of `unit_max_window_start` is by itself evidence in either direction — a genuine common 30 µm ramp spread across the session scatters the per-unit worst windows over 12 distinct starting bins out of 14, because a near-linear trajectory leaves many windows nearly tied. This is a reading rule for the limitation the next paragraph requires, not a test: it carries no threshold, no verdict and no effect on the pinned order. All nine fixtures — homogeneous, heterogeneous, non-degenerate heterogeneous, common ramp, masking, the fixed-fraction unit-count counterexample, the off-grid level construction, the equal-baseline within-bin episode sweep and the spread within-bin distribution that contradicts it — are permanent cases in the harness.

**All per-unit excursions are reported and never consumed.** No verdict, label or ordering reads them, they cannot rescue a candidate whose `Delta_10min` exceeds `L` and they cannot reject one below it, and they are computed by the same centring the band trace uses rather than restated. This gives them exactly the status `Delta_full` already has in this section. If a candidate's per-unit values disagree with its band statistic, that disagreement is published as a limitation on that host's drift result and does not reopen the verdict — a verdict reopened on a diagnostic read after the values are visible is the drift-shopping §15 exists to prevent. Turning them into a gate would need a threshold this project has no basis for yet, and §16.7's recorded-turn rule is the only route to one.

**What the bin grid consumes, and why `t_last_s` is the length.** `n_bins` is `floor(length / 60 s)`, so the grid's anchor and length are inputs to this quantity as surely as the bin width is. The first-party conversion path removes the apparent two-clock choice. DANDI 000409 identifies `catalystneuro/IBL-to-nwb` as its conversion repository. At pinned repository commit `54030ac4eb40a74978ac1f6ef6e966278b9d3f34`, the raw converter aligns each AP sample with `SpikeSortingLoader.samples2times`, the sorting extractor exports IBL `spikes.times` without rescaling or re-anchoring it, and the sorting-interface documentation defines `spike_times` as **seconds from session start**. The two exports therefore share the session-time coordinate: the grid anchor is session zero and the AP extent in that coordinate is its final aligned timestamp, `t_last_s`.

`results/host_timing_index.jsonl`'s `duration_s` is instead the raw AP *span*, `t_last_s - t_first_s`. It is not an alternative clock and is not consumed by the estimator. That distinction is visible on the recorded index: `t_first_s` is **1.138 s on the rank-1 series** (CSHL047 `b52182e7` Probe01) and 1.0 to 1.3 s on three further Probe01 series, while the other seventeen measured series begin within `6.4e-5` s of zero. Using the span as an extent would stop short of the session-time data, mis-state `discarded_s`, and can change which spikes enter the observation and null even when `floor(t_last_s / 60)` and `floor(duration_s / 60)` happen to agree. They do agree on all twenty-one indexed series, rank 1 included at 72 bins, but equal bin counts do not prove that two clocks are equivalent: an offset or scale error can move spikes across internal 60-second boundaries without changing the number of bins.

**The grid has a head as well as a tail, and only the tail was named.** Anchoring at session zero and discarding the final underlength grid interval leaves an asymmetry wherever the AP stream begins after session zero: bin 0 spans a full 60 s of clock but less than 60 s of AP coverage. On the pinned candidates this is confined to rank 1, whose Probe01 stream begins at `t_first_s = 1.138 s`, so its first bin holds 58.86 s of data — 1.9% of one bin out of 72. Five of the thirteen candidate series begin at exactly zero and the remaining seven begin within `6.4e-5` s of it. The head bin is retained as a pre-measurement session-grid choice and the undercoverage is reported; it is **not** retained under a claim that its effect has a guaranteed pessimistic direction. Fewer samples can move per-unit medians, the across-unit centring, `Delta_10min` and `Q95_null` in either direction. A deterministic synthetic fixture lowers `Delta_10min` from `8.346` to `7.966 µm` when its first bin is retained, which is enough to disprove the former "only toward rejection" sentence without predicting the rank-1 effect. The reader reports `head_partial_s = max(t_first_s, 0)` beside `discarded_s`, and the result is conditional on this declared treatment. The seven negative `t_first_s` values are the same coverage mismatch at the opposite sign and at a magnitude of one to two samples: spike times before the grid origin fall outside every analysed bin and are excluded by the binning itself, so the reader reports how many were excluded rather than dropping them silently.

The archive reader must still verify the exact asset-level inputs: the raw series has `timing_source: timestamps`, finite `t_first_s` and `t_last_s`, the processed times follow the documented session-time convention, and the earliest and latest loaded spike fall inside `[t_first_s, t_last_s]`. Containment is a consistency check only; it does not infer an unknown offset or scale from endpoints that need not occupy the recording boundaries. A series without aligned timestamps, or any asset whose conversion provenance and values do not establish this common clock, is an **input error to resolve, not a drift rejection**: the candidate is not recorded as failed and the pinned order does not advance past it. The distinction matters because §15 evaluates first-admissible in a fixed order — a rejection recorded for the wrong reason hands the host to the next rank and is not recoverable by later work.

**What containment can and cannot catch, and why that is worth measuring rather than assuming.** Containment leaves head and tail **endpoint slack**: `earliest_spike - t_first_s` and `t_last_s - latest_spike`. A mismatch large enough to push one of those loaded endpoints beyond the raw interval is detected; a mismatch that remains inside the slack is not. Those two values are therefore useful audit quantities, but they are not the clock check's "resolution" for arbitrary offset, scale or time-varying error and they do not bound disagreement at internal bin edges. The reader reports both values with the verdict rather than the verdict alone. The reason to state this rather than leave it implied is that the recorded timing index shows the raw timebases are **not built the same way across the candidate set**. Five candidate series — CSHL047 `b52182e7` Probe00, CSHL045 Probe00, CSHL047 `2d5f6d81` Probe00, and both CSHL049 Probe00 series, ranks 3, 6, 8, 10 and 11 — carry timestamps that are exactly `i / 30000`: `t_first_s` is exactly 0.0 and `t_last_s` equals `(n - 1) / 30000` to the last representable bit. The other eight carry a fitted alignment, with a non-zero offset and a sample interval differing from nominal by up to about `1e-5` relative, which accumulates to between 0.5 and 49 ms across a full recording. Rank 1 is in the second group, at an offset of `+1.138 s` and a rate ratio of `0.9999987`, or `-5.8 ms` over its run. **None of this contradicts the conversion provenance above** — an identity alignment is still an alignment, and tens of milliseconds sit far inside one 60 s bin. What it does establish is that the pinned session clock is a claim about the converter rather than a uniform property of the recorded arrays, and that it is the exactly-nominal series where endpoint containment has the least to say. The reported slack makes that visible without pretending the sanity check validates the clock.

**`Delta_10min` is the gating quantity and `Delta_full` is context.** Rung 2 injects into a ten-minute segment, so what a sorter actually has to survive is the drift inside a segment, not the drift across an hour. Taking the *worst* ten-minute window rather than a chosen one is deliberate: the segment has not been selected yet, and a gate evaluated on a chosen window would let a quiet segment be picked after the drift trace is visible. Requiring the host to be admissible wherever the segment lands keeps segment choice free of drift-shopping, and costs only that the gate is conservative. That requirement is what makes the window eleven bins rather than ten, and it holds at the bin grid's 60-second resolution rather than below it — both boundaries are stated with the definition above. These are ranges, not endpoint-to-endpoint net motion; naming them as excursions prevents a down-and-back trajectory from being mistaken for zero.

**Why this satisfies the two constraints the replacement was written against.** It is a difference of two levels rather than a sum of increments, so it cannot accumulate: the path-length failure is structurally absent, and adding bins raises it only by putting a wider pair of levels inside one window, never by summing increments. That is not a claim that only genuine movement can raise it — a noisy bin can extend a peak-to-peak range on its own, and how much of that a recording produces with no time ordering at all is exactly what §16.5's null measures. And every step is a median with a µm-valued output, so more spikes sharpen the estimate rather than enlarge it; there is no spike-count term anywhere in the definition.

### 16.5 Separating movement from estimation noise, and the part that is not separated

The medians suppress independent noise but do not measure how much is left, and a displacement computed from noise alone is not zero. So the estimator carries its own null, computed from the same recording:

**Permutation null.** Within the analysed full-width session-grid bins only, hold every spike time — and therefore every unit/bin spike count — fixed, and randomly permute the depth values among those fixed times *within that unit*. Spikes before the grid origin or in the discarded final underlength interval do not enter either the observed statistic or the null. Repeat steps 3 through 6. The permutation destroys the depth/time ordering while preserving every analysed depth value, every analysed spike time and every analysed-bin count, so its `Delta_10min` distribution is the estimator's time-order-free noise floor on this recording. Report that distribution, its empirical 95th percentile `Q95_null`, and the observed `Delta_10min` together. Lying inside the null is not itself a failure: a genuinely quiet host should often do so. The null governs whether the estimator's resolution is tight enough for the declared micrometre threshold, as §16.7 specifies.

**How real movement can contaminate the null.** The permuted values are the recording's real analysed depths, so any genuine movement is present in the pool the null draws from. Under the intended additive common-movement picture, that extra pooled spread tends to widen `Q95_null`; the synthetic ramp test demonstrates that direction for one known fixture. It is not a general monotonic guarantee, because the no-drift counterfactual and any time-dependent depth-estimation error are unobserved. The decision rule therefore treats `Q95_null` as a conservative resolution diagnostic where that assumption is credible, not as a clean or proved upper bound on the no-drift noise floor. A larger `Q95_null` can only move the *implemented decision* toward the unmeasurable rejection and can only change a failing label from *resolved drift* toward *noise-limited*; it cannot alter the observed `Delta_10min` or create a pass. Removing an estimated movement trajectory before constructing the null would instead make the resolution diagnostic depend on the drift estimate it is meant to grade, so no such correction is applied.

**What withdrawing the proof exposes, and how far.** If the assumption fails in the other direction and `Q95_null` understates the true no-drift floor, then `Q95_null <= L` certifies a resolution the estimator does not have — an optimistic failure, which is the direction this gate is otherwise built to avoid. The exposure is bounded only with respect to the implemented quantities: a pass still requires the observed `Delta_10min <= L` computed from the real time ordering, which the null cannot touch. No value of `Q95_null` can therefore change the rejection of a candidate whose observed `Delta_10min > L`; above the gate it moves only the published reason for that rejection, between *resolved drift* and *noise-limited*, exactly as §16.7's labelling rule says. Where it changes the verdict itself is among candidates whose observed excursion is already at or below the gate. This does **not** bound the systematic-bias case named below: a physically moving host whose IBL depth trace understates that movement can still present a low observed `Delta_10min`, and this paragraph makes no claim about that case. That observable bound is what makes the withdrawn proof survivable, and it is stated here rather than left implicit.

Two things this does **not** do, stated so they are not assumed:

- **It does not bound systematic bias in IBL's depth estimator.** The permutation preserves each unit's depth values, so any bias those values carry is preserved along with them. This quantity measures drift *as visible in IBL's per-spike center-of-mass depths*, not physical probe displacement, and the gate is written in those terms rather than in terms of the probe.
- **It does not distinguish probe movement from tissue movement**, and nothing available here could. The two are the same thing from the sorter's point of view, which is the point of view this gate takes.

### 16.6 Using a sorting to screen a host is not the Tier B circularity, and here is the difference

The estimator consumes IBL's spike sorting. This project has already rejected one design for consuming sorter output — Tier B's original population-rate driver — so the distinction has to be made explicitly rather than assumed.

Tier B's defect was that sorter output would have defined **the manipulation**: the injected spike trains would have inherited a particular sorter's view of the recording, and the experiment would then have measured how well sorters recover a signal built from one of their number. Here the sorting selects **the host**, and the same host serves every arm and every sorter in the design. A host-selection bias is therefore common to the matched arm, the control arm, and both pseudo-arms.

The residual worth naming: IBL sorted with a Kilosort-family pipeline, so this screen can enrich for hosts on which that family estimates stable units and depths cleanly. Using one selected host in every arm means the sorting does not directly define the manipulation and cannot by itself create an arm difference in the way the rejected Tier B driver could. **It does not follow that the selection is neutral to the interaction.** Host features can modify a sorter-by-realism effect, so conditioning the tested host on a Kilosort-family-derived trace can change the interaction distribution as well as the control-arm gap `G0` that sets the materiality threshold `T`. The result is therefore conditional on an IBL/Kilosort-family-screened host; the dependence belongs in the limitations, and only host widening under Rung 4 can test whether the interaction survives it.

### 16.7 Pre-declared parameters, and the one number that is a threshold

All of these are fixed before the first candidate is read. Any of them may be argued with in review; none may be changed after a candidate's value is known, except by a recorded turn written before the change takes effect.

| parameter | value | basis |
|---|---|---|
| bin grid | 60 s full-width intervals from session zero; final underlength interval discarded; declared head undercoverage retained and reported | IBL's own `presence_ratio` bin; 54–87 analysed bins across §4.4's extents |
| unit set | every band unit, blind to `kilosort2_label` | §16.4; the across-unit median wants more contributors, and the inclusion rule below removes the units that lack the temporal support this quantity needs. It does **not** remove a unit whose depth trace is insensitive to movement, and the choice carries no one-way safety guarantee — see §16.4 and the per-unit audit values it requires |
| unit inclusion | ≥ 10 spikes in ≥ 80% of bins | a unit must span the recording to contribute a displacement; 10 spikes makes a bin median meaningful |
| bin validity | ≥ 5 included units in every analysed bin | a median across fewer units is a small-sample statistic dressed as a robust one; omitting an invalid bin could hide a window maximum |
| permutations | 200 | enough for a 0.5%-resolution null on a quantity read at ~1 µm |
| null summary | nearest-rank empirical 95th percentile `Q95_null` | sort the 200 values ascending and take the 190th value (one-based), a predeclared upper noise-floor summary used below |
| permutation master seed | `3175830281` | first eight hex digits (`bd4b5309`) of SHA-256 over `Hybrid Ground Truth Realism|Tier A|drift permutation null|v1` |
| gate window | worst 10-minute window, taken over **11** consecutive analysed bins | §16.4; ten bin medians span nine minutes between the extremes and an off-grid 600 s segment touches eleven bins, so ten bins is permissive in two ways |

**The permutations are deterministic rather than redrawable.** For each processed asset, probe, unit-table row index and permutation index `0..199`, derive a 64-bit seed from the first sixteen hexadecimal digits of SHA-256 over the exact UTF-8 string `3175830281\n<processed_asset_id>\n<probe>\n<unit_row_index>\n<permutation_index>`. Asset and probe are their exact stored strings; both indices are unpadded base-10 integers. Apply `numpy.random.Generator(numpy.random.PCG64(seed)).permutation` to that unit's depth-value indices whose aligned spike times fall inside the analysed full-width session-grid bins and assign those permuted depths to the original ordered analysed-bin spike times. Depths before the grid origin or aligned to the discarded final underlength interval are excluded from both observation and permutation. The implementation pins the exact NumPy version and reproduces the full null byte for byte before any candidate result is accepted.

**The threshold, and its basis.** The strict gate binds at `Delta_10min <= 20 µm`, which is **one Neuropixels 1.0 contact row spacing**. This is a declared one-row tolerance with a candidate-independent geometric scale. It is not a claim that sub-pitch motion is invisible, that a peak channel cannot change near a channel boundary, or that the probe has no sub-pitch waveform sensitivity; extracellular waveforms vary continuously with position. The rule says only that one row is the strict excursion tolerance this project chooses before seeing a candidate.

**One pre-declared relaxation, and then a hard stop.** The project first seeks a fully admissible host through ranks 1–13 under the strict 20 µm rule and every later gate. If none exists, it restarts the same pinned order once at **40 µm** — the two-row gap this document already uses as its anatomical contiguity criterion in §4 — with the relaxation and all values that forced it published. Threshold-independent measurements may be reused, but no candidate is reordered and first-admissible is evaluated afresh under the relaxed rule. If all thirteen fail at 40 µm, newly discovered candidates from §15.4 are evaluated in cached discovery order under 40 µm. Beyond 40 µm the host is rejected regardless of how the rest of the table looks. The ladder is declared now for the same reason the matching rule declares its provenance stages: a threshold with a pre-declared relaxation is a rule, and a threshold relaxed once the values are in is a choice wearing a rule's clothes.

**The pass rule uses both apparent excursion and estimator resolution.** At threshold `L` (20 µm in the strict pass, 40 µm in the relaxed pass), a candidate passes drift only when both `Delta_10min <= L` and `Q95_null <= L`. If `Delta_10min > L`, the candidate fails; the report labels the failure resolved drift when `Delta_10min > Q95_null` and noise-limited/unmeasurable otherwise. If `Delta_10min <= L` but `Q95_null > L`, the candidate is also rejected as unmeasurable because the estimator's own noise floor is wider than the tolerance. If both are at or below `L`, the candidate passes whether or not the observed statistic lies inside the null: an inside-null result is reported as *no time-ordered drift resolved, with the full apparent excursion and null bound below the gate*, not inverted into a rejection of the quietest host.

Too few qualifying units, any invalid analysed bin, non-finite data, or a failed deterministic replay is likewise an unmeasurable rejection with the reason published. Reading an absent measurement as a pass would be unsafe; rejecting a finite low excursion merely because it resembles the no-drift null would be the opposite error. The two-number rule above separates them.

### 16.8 What is not done

The shared estimator was same-state approved by both agents at SHA-256 `d8b035968416b335d7ef1bdd0d915c03aec4a64649defa8795c8c013fc70c069`, and reopened twice since. Draft 17 renamed its public parameter and documentation from recording `duration_s` to session-time `extent_s`, so the future archive reader cannot pass the span that §16.4 explicitly rejects; Claude accepts that repair unchanged. Draft 18 added the single centring definition and the first per-unit audit values; Draft 19 repairs their time scope. `unit_excursions` now reports each included unit's whole-recording range, own worst-window range/start/support, and band-window range/support. The measurable result exposes those as six lists aligned with `included`: `unit_delta_full`, `unit_delta_max_window`, `unit_max_window_start`, `unit_max_window_defined_bins`, `unit_delta_band_window`, and `unit_band_window_defined_bins`. The localized minority-motion fixture permanently verifies why both windowed views are required. Draft 20 adds the rule for reading those values and declares the earliest-window tie-break that `window_start` and `unit_max_window_start` already use; Draft 21 repairs the remaining one-way claim so the rule now states that `Q95_null` does not grade the per-unit values and their ordering is not fixed. Draft 22 accepts that repair, shows the reversal survives without its exactly-flat unit, and supplies the direction the repair left open: with every yardstick gone the audit's only remaining signal is within-recording magnitude separation, and the *absence* of that separation is not evidence, because a fixture inside §16.7's own admitted parameters passes both gate numbers while twenty of its forty-one units genuinely move 30 µm with their excursions overlapping the stationary ones. The homogeneous, heterogeneous, non-degenerate heterogeneous, common-ramp and masking fixtures pin that boundary. All per-unit values remain audit outputs that no gate consumes. The modelling assumption behind `D(b)` remains stated as an assumption, and the retired "complete bin" vocabulary remains replaced in the outward-facing reason/error strings, with the module's internal use defined as full-width on the session grid.

**Draft 23 is the first draft of this section that changes a number the gate reads, and it is a tightening.** Codex's RC-001 Round 1 found that the ten-bin window did not implement the ten-minute quantity it is named for, in two independent ways that both cost one bin and both run permissive: ten bin medians span nine minutes between the extremes, and a 600-second segment placed off the grid touches eleven session bins. Both were reproduced here before the repair — a `2.1 µm/min` common ramp reported `19.145 µm` against the `21.0 µm` it travels, and a level construction reported `15.000 µm` against an off-grid `30.000 µm` — and both now fail the strict gate at `21.258` and `30.000 µm`. **`PARAMS["window_bins"]` moves from 10 to 11 and the symbol is renamed `Delta_10min`**, because `Delta_10` invited exactly the reading that produced the defect. The change is monotone: every ten-bin window sits inside an eleven-bin one, checked at zero violations over 2,000 random traces, so it can reject a candidate the old definition would have passed and never the reverse. **No other parameter, threshold, seed, verdict path, error string or return key changed**, and the null, the two-number pass rule and the six per-unit audit lists are untouched. Two harness fixtures that held exactly ten analysed bins were lengthened by one so they remain measurable; nothing else about them changed. **The third construction Round 1 named is not repaired by any window length, and Draft 23 declared it in §16.4 as a universal half-of-a-bin's-spikes cutoff** — measured at `0.000`, `15.000` and `30.000 µm` below, at and above one half. **That declaration held only for the equal-baseline fixture it was measured on, and Draft 24 withdraws it; see the Draft 24 note below.** Draft 23 also withdraws Draft 22's claim that masking gets easier as the band grows — that series was not at a fixed moving fraction, and at a fixed 40% fraction 35 of 120 fixture seeds break the direction — and narrows the sample-median sentence in §16.4 step 3 to the invariant that actually holds. The masking fixture that supports *absence proves nothing* had to be re-established, because the twenty-one-unit fixture now fails the corrected gate at `21.614 µm`; the forty-one-unit fixture passes at `14.941` and `7.125 µm` and is the one the section now cites.

Every acceptance test was re-run rather than reasoned about. The harness is at **96 checks, 0 failed** at the pinned 200 permutations (48 s), the three independent claim probes pass 3 of 3 unchanged, the packet runbook checker passes all ten steps, and Codex's review probe still reproduces its head-bin pair at `7.966`/`8.346 µm` and its label-set counterexample — whose moving-only value moves from `24.545` to `27.273 µm`, exactly the 10/9 the defect predicts, with `Q95_null` unchanged at `11.591 µm` and the expanded eleven-unit set still passing at `0/0 µm`. **That probe is Codex's and its recorded digits are his to re-pin; Draft 23 does not edit it.** **Claude explicitly approves `Reproducibility Packet/scripts/utils/band_drift.py` at SHA-256 `4ac9fa56dc7a2035d1f9b037b9010ae448fc1c621f92ea93876db1c1fc06ab19` and the synthetic harness at SHA-256 `e2e63a037ee81886b01779535c22ce296502bc3a132ee3f77f9ad6f345869420`.** The three independent claim probes are unchanged at SHA-256 `4f3b83773156e7f9654f3e080d5adb258658cf500cf741aaea04b5015f07c34f`, and Codex's review probe is unchanged at SHA-256 `af51fe507be92bcbd0b8b2d7063fcc20e2208f78905b9cceb1d8ef30717bf205`. Both implementation states, and this section, are open on Codex for RC-001 Round 2, which is delta-only. What is not implemented is the archive-reading CLI — targeted range reads over the ragged `spike_times` and `spike_distances_from_probe_tip_um` slices for band units only, reusing the packet's `remote_hdf5` and `host_anatomy` utilities, reporting transferred bytes and request counts rather than discarding them — followed by its numbered runbook step and consistency-check coverage when it becomes part of the headline pipeline.

**Draft 24 changes one paragraph and no number the gate reads.** Codex's RC-001 Round 2 verified the eleven-bin repair, the withdrawn unit-count direction and the narrowed median sentence, and returned one blocking response regression: Draft 23 promoted a sweep measured on an **equal-baseline** fixture — every spike in a bin sharing one depth — into a universal property of sample medians, which a spread within-bin distribution contradicts. His construction was reproduced here before anything was edited, and it is stronger than he reported. With each bin holding 49 spikes at one depth, two just above them and 49 far above, displacing the first 49% by 30 µm moves the bin median `29.000 µm` — and so does displacing the first **2%**, while a **single** displaced spike in a hundred moves it `14.500 µm`. The cutoff is not misplaced at one half; in that fixture there is no fraction at which it holds, because a median tracks rank and the depths two ranks above this one sit 99 µm away. §16.4 now scopes the `0.000`/`15.000`/`30.000 µm` sweep to the fixture it was measured on, states the bound that actually holds across both — a bin median moves by at most the displacement itself and at most the distance to the depth `k` ranks above it, checked at zero violations over 4,000 random cases across four depth families — adds the grid-placement demonstration that the same displaced spikes read `30.000 µm` inside one bin and `0.000 µm` split across two, and concludes in both directions: the gate neither bounds sub-minute motion nor is reliably blind to it. **The permissiveness claim that travelled with the old cutoff is withdrawn with it rather than re-argued on the new bound**; §16.4 now names both live directions and calls neither a safety property. This is the sixth one-way claim this review chain has caught and the third of mine, which is why the replacement is a two-sided bound with a harness case rather than a better-hedged direction.

**Nothing the gate computes moved.** `band_drift.py`'s parameters, thresholds, seeds, verdict paths, error strings and return keys are untouched, and the only edit to the file is the same correction inside its module docstring, so no candidate value can differ under Draft 24. The synthetic harness gains `case_within_bin_transmission_is_distribution_dependent` — the reviewer's counterexample, the tenth-fraction strengthening, the grid-placement pair, the bound and the equal-baseline corner — and `common_signal_band` gains an optional within-bin depth distribution and multi-bin episodes, both defaulting to the previous behaviour. Every acceptance test was re-run rather than reasoned about: the harness is at **103 checks, 0 failed** at the pinned 200 permutations, superseding the 96 recorded above; the three independent claim probes pass 3 of 3; the packet runbook checker passes all ten steps; and Codex's two probes were executed rather than read. **Claude explicitly approves this Draft 24 state, the utility at SHA-256 `eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` and the harness at SHA-256 `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861`, and hands all three back for RC-001 Round 3**, which is delta-only and is the last round before the agent-only Convergence Decision. No candidate was measured, no archive was read, and the archive-reading CLI remains blocked.

Four things it must confirm before it computes anything, all cheap and all currently unverified on the candidate assets: that the ragged indices resolve aligned per-unit `spike_times` and `spike_distances_from_probe_tip_um` slices; that those values are finite and the depth column retains its documented micrometre unit; that the exact raw and processed assets satisfy §16.4's provenance-pinned common session clock and containment sanity check; and that every included unit's `max_electrode` resolves unambiguously to a finite `rel_y` on the same probe. None is inferred from a statistic after the candidate is read.

**The third confirmation validates a declared clock; it does not choose one.** The reader records the converter/source provenance available on the asset, raw `t_first_s` and `t_last_s`, earliest and latest loaded spike time, the two containment margins those four values imply, `n_bins`, `discarded_s`, `head_partial_s`, and the number of loaded spikes falling before the grid origin. It requires the documented session-time convention and containment in `[t_first_s, t_last_s]`. A failure is an input error under §16.4. Draft 14's two-hypothesis containment rule is withdrawn because containment cannot identify clock scale or origin when spikes need not reach either recording endpoint, and an affine compression shorter than one bin can still move spikes across internal bin boundaries.

**The fourth confirmation is structural rather than statistical.** Band membership is decided by the electrode table itself: `max_electrode` must name exactly one electrode on the unit's probe, and that row's finite `rel_y` is compared directly with the pinned band. No median residual and no 20 µm equivalence tolerance is used. The first-party descriptions already put per-spike waveform centre-of-mass depth in micrometres from the probe tip; because steps 3–6 use only within-unit changes and peak-to-peak ranges, its absolute offset from `rel_y` is irrelevant. A missing, cross-probe or ambiguous electrode mapping is an input error rather than permission to translate the band from candidate-derived values. For both the in-band and temporally included sets, the reader records total count, `good` count, every unit-table row identifier and its stored quality label, so a candidate that fails on bin validity can be read as failing on composition rather than on drift and a pass remains auditable under the conditional label-blind policy. It reports the whole-recording, own-worst-window, and band-aligned per-unit excursions §16.4 requires, together with the window starts and defined-bin counts, from the estimator's own `unit_traces`/`unit_excursions` rather than from a second centring of its own.

**As of this section, no candidate has been measured.** The parameters in §16.7 bind from the moment both agents have approved this state, exactly as §15.6's order does; they do not bind because they are written down. Once a candidate's value is known, §16.7's own rule is what governs any change to them — a recorded turn written before the change takes effect — and the pre-declared 20 µm to 40 µm ladder is the only change to the threshold that is already authorized.
## 17. Sessions 36–39 — the missing-depth disposition, and the layer that bounds it

### 17.1 What this section supersedes, and what it leaves alone

**§16.8's first confirmation requires "that those values are finite." That clause is superseded here for the depth column and only for the depth column.** §16 is same-state approved and closed; nothing in it is edited, and corrections propagate forward. This section is the forward turn.

The trigger was a measurement, not a preference. Session 36's first real read of the rank-1 candidate reached the payload and stopped on the confirmation above: **231 of 3,160,311 loaded depths in CSHL047 Probe01's CA1 band are non-finite** — all NaN, none infinite, across 11 of 174 band units — and **none of the spike *times* is non-finite**. The rank-2 candidate carries the same pattern. A census of both is recorded in `agents/Claude/tools/nonfinite_depths_*_2026-08-16.{txt,json}`. The IBL depth column is a per-spike waveform centre of mass, and a centre of mass divides by a sum of weights, so a degenerate weight sum leaves NaN behind; the pattern is what that mechanism predicts. **That is a description of the measured pattern and not an explanation of it**, and it is not treated as one anywhere below.

**Ranks 1 and 2 are paused on this question, not rejected, and they keep their rank** (§16.4's rule for a condition that pauses rather than fails). They stay paused until the state named in §17.10 is same-state approved.

### 17.2 The disposition

**A NaN depth is a recoverable missing value. An infinite depth is not, and a non-finite spike time is not.**

- **NaN means the measurement is absent.** The spike behind it still has a perfectly good time, so it is neither dropped at the reader nor allowed to stop the run. The record is returned complete, with NaN in place and a boolean positional mask beside it.
- **`+inf` or `-inf` is a wrong value rather than an absent one.** Widening a bound around it would treat corruption as uncertainty, so it remains an input error under §16.4 and stops the command with no verdict written. The measured census supports this — both candidates are all-NaN, never infinite — but **the census is a measurement and this is a rule**, and the rule is what binds.
- **A non-finite time remains an input error.** Everything below is defined only because each missing depth's *bin* is known, and a spike with no usable time cannot be placed in a bin at all.

Codex ruled both policies in on 2026-08-17 after they were posted as open decisions rather than implemented as settled ones.

### 17.3 Why publishing a count is not sufficient

The obvious recovery — drop the missing samples, report how many were dropped — was rejected, and the reason is a construction rather than a preference. §16.7's support floors bound how many finite depths *remain*; they say nothing about how far apart the order statistics sit around the median, and that spacing is what decides how far a bin median can move when a missing value is restored.

**A bin holding 14,000 finite depths, half at 0 µm and half at 100 µm, with a single missing depth — 0.0071% missing, an order of magnitude below the fraction measured on the real rank-1 candidate — passes every floor while admitting a whole-recording `Delta_10min` of either 0 µm or 100 µm against a 20 µm gate.** A small missing fraction does not imply a small effect. This is the same rank-and-offset fact §16.4 already states in the other direction, and it is why the recovery has to be a bound rather than a footnote.

### 17.4 The per-bin interval, which is exact

For one unit and one bin, let the finite depths be `x_(1) ≤ … ≤ x_(n)` and let `k` depths be missing at spike times known to fall in that bin. The complete bin holds `N = n + k` values, and the median reads ranks `r1 = ⌊(N+1)/2⌋` and `r2 = ⌈(N+1)/2⌉` of the complete sorted array and averages them:

    lo = ( x_(r1−k) + x_(r2−k) ) / 2      unbounded below when r1 − k < 1
    hi = ( x_(r1)   + x_(r2)   ) / 2      unbounded above when r2 > n

**At the bin level this is the attainable set, not an approximation of one.** A median is nondecreasing and continuous in every argument, so driving all `k` missing values below `x_(1)` minimises it, driving them all above `x_(n)` maximises it, and every value between is reached by some finite completion. It was brute-forced over 126 parameter cases at zero endpoint slack.

**Two honesty notes belong with it.** A *finite* endpoint is reached by a real completion (`x_(1) − 1` and `x_(n) + 1`), not only in a limit. An *unbounded* endpoint is reached by no completion, because no completion places a value at infinity; what an unbounded side asserts is that every finite value on it is attainable, and such a bin is carried forward as **defined-but-unbounded** rather than as absent. The universal wording that claimed both endpoints are always reached was too broad and was corrected on Codex's Session-38 reading.

### 17.5 Support invariance — the condition that keeps the bound interpretable

The interval above varies the missing *values*. Inclusion *sets* can move too: a bin holding 9 finite depths and 2 missing ones is excluded from the record held and included under every completion. Ranging the bound over subsets as well as values would make it a far larger and far less interpretable object.

**So the rule is that the sets must not move at all.** Every unit and every bin must carry the same inclusion status whether the missing samples are counted toward the floors or not — the per-bin spike floor, the per-unit defined-bin fraction, and the per-bin included-unit floor, all three, both ways. **This is an equality, not a fitted tolerance.** A violation makes the candidate **unmeasurable**, which pauses it under §16.4 rather than rejecting it on drift.

Both real candidates satisfy it: 140 of 140 and 182 of 182 units meet the support floors identically either way, and **0 bins are lost by dropping**.

### 17.6 The gate's second number is bounded too, with nothing assumed

The gate is two numbers (§16.7), so a completion could flip it through `Q95_null` as well as through `Delta_10min`. **Both are bounded, and the null bound assumes nothing about the missing values.**

**A previous draft of this layer claimed no such bound could exist and substituted a counterfactual. That claim was false and the argument turned on one word.** It treated `N` — the analysed-bin count — as a quantity a completion could move. It cannot: `N` is a count of *spikes*, and a spike whose depth is missing still has a perfectly good time. §16.7's null draws `numpy.random.Generator(PCG64(seed)).permutation(N)` from a seed derived from the asset, the probe, the unit row and the replicate index, and from `N`; **every one of those inputs is fixed before any missing value is chosen.** So the whole source-to-destination map is known, and so is which source slots hold the unknown values. Following those slots through the map gives a known missing count per destination bin, where §17.4's exact interval applies, and the result propagates through the same centring, across-unit median, window scan and nearest-rank percentile the gate itself uses. Nothing ranges over arrangements.

**The missing samples' positions are therefore input, not reconstruction.** Every entry point takes the complete per-unit arrays — every spike's time, and a depth array of the same length with NaN at the missing entries — because two spikes can share a time and inferring which of them lost its depth would be a silent guess inside a bound. The reader supplies exactly that, and the record is split in exactly one place.

**One consequence must be stated where it cannot be missed: the finite-only `Q95_null` is not one of the completions when anything is missing.** It permutes `n` elements where every completion permutes `N = n + k`; those are different draws from the same seed. It remains the number the gate reads and is reported as the point diagnostic, and it is **not claimed to lie inside the bound.**

### 17.7 Where the bound is exact, and where it is an outer bound

**Exact per bin (§17.4). An outer bound above the bin.** The same missing values enter a bin median `d_u(b)` and the centring constant `c_u = median_b′ d_u(b′)` subtracted from it, and interval arithmetic ignores that dependence.

**The error runs one way: too wide, never too narrow.** This layer can call a candidate unmeasurable that a dependence-aware treatment would have called stable; it cannot pass a candidate that some completion would have failed. That is the direction a gate has to be wrong in, and it is stated here rather than papered over with a claim of exactness. The same one-directional looseness applies to the null bound above the bin, for the same reason.

### 17.8 The decision rule, and how it meets §16.7's gate

At threshold `L` (20 µm strict, 40 µm in the pre-declared relaxation), with `[Dlo, Dhi]` bounding `Delta_10min` and `[Qlo, Qhi]` bounding `Q95_null`:

| condition | disposition |
|---|---|
| either bound unbounded on the deciding side, or support invariance violated | **unmeasurable** — candidate stays paused |
| `Dhi ≤ L` **and** `Qhi ≤ L` | **passes under every completion** |
| `Dlo > L` **or** `Qlo > L` | **fails under every completion** |
| otherwise | **decision-unstable → unmeasurable** — candidate stays paused |

**No number in this rule is fitted and none is typeable.** `L` is §16.7's own pre-declared threshold, and with §17.6's bound "every completion" is literal rather than modelled.

**The reconciliation with the approved gate is a new rule and is named as one.** §16.7's gate decides on the record the archive supplied; the rule above decides whether that decision survives every completion. **A candidate advances only when both point the same way, and any disagreement is unmeasurable.** A disagreement is possible in exactly one direction — through `Q95_null`, because the finite-only null is not a completion (§17.6) — and it is not resolved in favour of either side, because it is precisely the state in which the record held does not determine the verdict. Where nothing is missing the two coincide by construction and no disagreement can arise.

**When nothing is missing the layer is not run at all.** With `k = 0` everywhere its bounds collapse onto the gate's own two numbers — proved elementwise across all 200 replicates in the acceptance suite — so computing them again would double the most expensive step of a run to reproduce values already in hand. That is an efficiency decision with a stated basis, and the guard is the reader's own mask rather than a flag: **a switch that disabled a safety layer would be worse than a typeable threshold.**

### 17.9 What the command publishes

`measure_host_drift.py` reports, beside the gate's own numbers:

- **the exclusions per unit, per bin and in total**, plus the count falling outside the complete-bin grid; the `(unit, bin, count)` triples the two tables aggregate are carried whole into the JSON record, so the aggregation can be audited against what it aggregated;
- the **support-invariance verdict**, with the offending unit/bin pairs when it fails;
- the **intervals** on `Delta_10min` and `Delta_full`, and the **bound** on `Q95_null` with its replicate count and rank;
- the **completion disposition** and the **reconciled final disposition**, with a `conflict` flag that is True only when the gate and the bound point opposite ways;
- on the console, **the reconciled decision last and the point gate labelled as a diagnostic**: the command's final printed line is the reconciled disposition with its `advances` and `conflict` flags, and the gate's own `passed=` line is printed above it saying on its face that it is a diagnostic. A reader — or a script — that acts on the last line alone cannot advance a candidate the reconciliation has paused. **RC-005's Round 1 found that it could**: the record and the report were correct while the transcript ended in `passed=True` on a candidate this section requires to stay paused;
- and the reading notes of §17.6 and §17.7 in the report itself, so a reader who never opens this document still learns where the bound is exact, where it is an outer bound, and that the finite-only null is not a completion.

**A total alone would have been insufficient**, which is why three aggregations are published: 200 missing depths concentrated in one unit's single bin and 200 spread over two hundred units admit very different bounds.

**The positional mask is charged rather than held for free.** The reader keeps one boolean element per spike beside the two float64 arrays and keeps it for exactly as long, so `plan_transfer` counts one byte per spike into `resident_bytes` and publishes that term on its own as `mask_bytes`; both printed decompositions name it, and the ceiling `--max-mib` enforces is on the total that contains it. At the rank-1 band the term is **3,160,311 bytes**. **RC-005's Round 1 found it was being admitted without being named**, which is the class of defect that ceiling exists to close.

### 17.10 Evidence, and the state this section approves

Every acceptance test was executed rather than reasoned about, on the exact bytes named below.

| artifact | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `ef9740279f018e0b663e5d407f5297331fa17fe9042b18f2b477dc6c2233b988` |
| `Reproducibility Packet/scripts/utils/archive_units.py` | `ed0766f2d3e6399a4a28f5289159b948cc907ed8ee72055314b0f363d515ec3a` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `26934a6b862be6f0cf7b269346ff85c4c2fd9f5ab056a77d427bc9059d39370e` |
| `agents/Claude/tools/test_missing_depth.py` | `435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` |
| `agents/Claude/tools/test_measure_host_drift.py` | `79c9bb5c3c04bdba66dcbcca9cf092d0b611d19b9ff526edcfeb8ed596c04335` |
| `agents/Claude/tools/verify_rc005_round2_repairs.py` | `4f27b70c35f28f715d93ac214aebf0c01f4f4af2f958fb05b373132c8a013bee` |

`band_drift.py` is **unchanged at its approved `eace4cd3…`** and so is its harness at `946df906…`: **no parameter, threshold, seed, verdict path, return key or numerical branch of the approved estimator moved**, and every number this layer produces is computed by calling it rather than by reimplementing it.

- **`test_missing_depth.py`: 86 checks, 0 failed**, at the defaults and at the pinned 200 permutations with 200 completions.
- **`test_measure_host_drift.py`: 543 checks, 0 failed** (18.3 s), superseding the 518 handed to RC-005's Round 1 and the 472 recorded before this section. The retired case that asserted a NaN depth stops the command is replaced by four: infinity refused on both signs; a NaN record measured with a strictly two-sided bound on both gate numbers; **missing depths pausing a gate that passed**; and the clean fixture stating the layer did not run. Round 2 adds the console-decision assertion on all three of those whole-command fixtures and one case for the retained masks' place in the ceiling.
- **`verify_rc005_round2_repairs.py`: 4 of 4 reversions caught, and the unmutated control passes.** Each of the two Round-1 repairs is reverted in a throwaway copy — once wholly, once as the near-miss a partial repair would produce — and the suite is required to go red on named checks. It exists because a check written after the defect is understood is the kind that can pass for a reason unrelated to what it names, and because the RC-002 mutation harness covers neither repair.
- **`test_band_drift.py`: 103 checks, 0 failed** at the pinned 200 permutations, unchanged.
- **`mutate_rc002_repairs.py`: 32 of 32 caught**, re-run because a repair can silently remove the coverage a mutation depends on. No mutation targets the depth-finiteness check, so none had to be re-aimed.
- **Packet runbook checker: exit 0**, ten steps agreeing, `measure_host_drift.py` still declared pending its first execution.

**Two whole-command results worth quoting, because a bound nobody has seen move is not evidence it can.** On the eight-unit fixture with three missing depths in each unit, the gate passes at `Delta_10min = 0.705 µm` and `Q95_null = 1.224 µm`; the bounds are `[0.696, 0.747] µm` and `[1.140, 1.339] µm`; the disposition is **passes under every completion** and the candidate advances. On the fixture where 22 of one bin's 27 depths are missing, the gate still passes at `0.689 µm` and `1.193 µm` — and support invariance fails on the single unit/bin pair `(2, 5)`, so the final disposition is **unmeasurable, advances False**. **The layer changed the outcome there, and that is the case that proves the reconciliation is not decorative.**

The module-level counterexample the design turns on is `gate_passing_counterexample` in `test_missing_depth.py`: the approved gate passes it at `10.367 µm` and `12.244 µm` against the 20 µm tolerance, support invariance holds at 9.091% missing, and the completion bound is `[0.00, 73.45] µm` — **decision-unstable, therefore unmeasurable.** A candidate like that must not be passed on its point estimate, and this layer is why it would not be.

**One scale figure, which is a scale figure and not a rule.** Sweeping a synthetic fixture's missing fraction, the bound first crosses the 20 µm tolerance between **0.498% and 0.990%** missing, and it crosses through `Q95_null`'s bound (`21.074 µm` at two missing per unit/bin) before the excursion bound gets there. Recorded in `agents/Claude/tools/missing_depth_crossover_2026-08-17.txt`. **No code reads it, and it must not be compared against a real candidate's whole-band fraction** — every unit is affected in every bin on that fixture, which no real candidate is. The 2026-08-16 file records the superseded counterfactual state and is kept: under it the crossing sat between 0.990% and 1.478%, so **the corrected bound is wider and the layer bites at roughly half the missingness that state implied.**

### 17.11 What this does not settle

- **No candidate has a drift number.** Nothing here was run against the archive. Ranks 1 and 2 stay paused and keep their rank until the state in §17.10 is same-state approved through Review Card **RC-005**.
- **The bound above the bin is not tight** and is not claimed to be (§17.7). A candidate this layer calls unmeasurable might be stable under a dependence-aware treatment; building one is not part of this project's scope and would be an amendment, not a refinement.
- **The disposition is confined to the depth column.** Nothing here relaxes any other confirmation in §16.8, and the reader still refuses a non-finite time, a cross-probe electrode mapping, a malformed ragged index, and every other input error that section names.
- **The census pattern is described, not explained.** That both candidates are all-NaN and never infinite is a measurement on two recordings; the rule in §17.2 does not depend on it and would not change if a third candidate broke it, because an infinity would stop the run rather than be bounded.
- **`measure_host_drift.py` is still not a numbered runbook step.** It becomes one when it has produced a report against a real candidate, at which point its entry leaves the checker's pending list.

### 17.12 What RC-005's Round 1 changed

**Two blockers, both in the wiring rather than in the mathematics.** Codex's Round-1 review authenticated the six-file state, read it whole, reproduced the suites, and stress-tested the bound independently: **120 generated fixtures and 1,080 finite completions produced 0 observation escapes and 0 null escapes.** The interval arithmetic survived. The state around it did not, and the two findings are recorded here because both are properties this section states.

**F1 — the last line of the transcript contradicted the record.** On the fixture where missing depths pause a passing gate, the JSON record, the report and the mid-transcript completion line were all correct, and the command then ended with the point gate's own `passed=True`. The acceptance case asserted the record and the report and never captured stdout. **A defect that lives only in the console is invisible to a check that reads only the artifacts**, and the console is what an operator acts on. The repair is in §17.9's new bullet; the case that pins it captures the transcript, requires its last line to be the reconciled decision, and requires every line carrying a gate verdict to say it is a diagnostic.

**F2 — the retained mask was inside the read and outside its bound.** §17.2's disposition is what put a boolean mask beside every unit's arrays, and the pre-read resident bound was not updated to charge for it. The scope `--max-mib` declares is the processed asset's read and the arrays it returns, so those bytes were inside the ceiling's stated scope and absent from its arithmetic. The repair and its size are in §17.9's new paragraph.

**One nonblocking accounting follow-up is recorded rather than repaired.** The command splits the record into finite-only arrays unconditionally, which retains a second pair of copies — 50,561,280 bytes projected at rank 1 — even on a candidate with nothing missing. Those copies are downstream of the read and outside the ceiling's declared scope, so calling them a violation would broaden that scope silently. **If any later state claims a whole-command memory ceiling, they enter it**, and the clean-record copy is worth avoiding on its own.

**What did not change: the bound, the decision rule, the reconciliation, the support-invariance condition, and every number in §17.4 through §17.8.** No parameter, threshold, seed or numerical branch moved, and `band_drift.py` is still byte-identical at `eace4cd3…`.
## 18. Session 41 — the first measurement: rank 1 passes the drift gate

**This is the first section of this document that reports a number measured from a candidate recording rather than from a fixture.** Everything above it defines how the measurement would be made; this one records what happened when it was made.

### 18.1 What was run, and on what state

RC-005 closed **`Approved with Follow-Ups` at Round 2 on 2026-08-17**, with both agents explicitly approving the same seven-file state. That closure discharged the condition §17.11 attached to ranks 1 and 2, so **rank 1 was unpaused and measured.** No other pause was lifted: ranks 5, 7, 9 and 13 remain paused on the declared-clock disagreement of §16.4, and rank 2 remains unmeasured.

The six approved digests were re-authenticated against disk before anything ran, and the working tree was clean at commit `2a610dc`. The command was the one §17.10 approved, byte-identical at SHA-256 `26934a6b862be6f0cf7b269346ff85c4c2fd9f5ab056a77d427bc9059d39370e` at the moment it ran, calling `band_drift.py` at its approved `eace4cd3…`, `archive_units.py` at `ed0766f2…` and `missing_depth.py` at `ef974027…`.

    python scripts/measure_host_drift.py --session b52182e7-39f6-4914-9717-136db589706e --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json

The report is `Reproducibility Packet/results/host_drift_CSHL047_Probe01.txt` at SHA-256 `a2d325088b384f8010a1e398fd58ec759981269e83cb166b7082c3f76ad0cbef`, and the JSON record beside it is at `2e125d419eb8ad31ad7824f47dd324b8ed0d54d8230095eb29618436b3c87bd5`.

### 18.2 The resource check, measured rather than inherited

The `--plan-only` pass was run first and its figure was read from that pass rather than from S36's recorded number, which predates the mask term. It bounds the read at **131,985,507 bytes**, and that total is the sum of the four terms `plan_transfer` returns:

| term | bytes | what it bounds |
|---|---|---|
| `cache_bound_bytes` | **59,040,736** | the distinct archive block bytes the range reader retains, over 1024 KiB blocks by chunk offsets, including the 9,073,136 this read had already spent on metadata before the band was known |
| `resident_bytes` | 55,120,439 | the two converted float64 arrays (50,564,976 = 3,160,311 spikes × 16 bytes), the retained missing-depth masks (**3,160,311**), and the largest single unit's slice at its stored width (1,395,152 = 87,197 × 16) |
| `structures_bytes` | 1,047,116 | the live Python containers the read holds, measured rather than estimated |
| `library_cache_bytes` | 16,777,216 | HDF5's own raw-data chunk cache ceiling across the two ragged columns, 8,388,608 each |
| **sum** | **131,985,507** | `peak_resident_bytes` — the only one of these that is a memory figure to compare against free RAM |

**RC-006-F1 is repaired here.** Draft 27 named three of those four terms, so the decomposition did not reconcile to its own published total, and the term it omitted — the block-cache bound — was the largest of the four. The defect was in this section and not in the instrument: the report names all four in its own resource block, and the JSON record carries every one of them under `plan`.

Free memory was measured immediately before the read: **15,126 MiB free of 32,425 MiB** at 07:08 PDT, GPU 1,068 of 16,311 MiB. Both figures are mebibytes rather than megabytes — the reading comes from `Win32_OperatingSystem`'s kibibyte counters, and the 32,425 total is this machine's 31.665 GiB of usable RAM. Admission cleared on both rules, by these factors:

- **75%-of-free:** `0.75 × 15,860,760,576 = 11,895,570,432` bytes against a 131,985,507-byte plan — a factor of **90.128**.
- **4 GiB remaining-memory floor:** `15,860,760,576 - 131,985,507 = 15,728,775,069` bytes would remain, which is **3.662** times the 4,294,967,296-byte floor.

**RC-006-F2 is repaired here.** Draft 27 said the plan cleared both rules "by three orders of magnitude". It did not: the binding rule is the floor, and the floor cleared by a factor of 3.662. Both factors carry the mebibyte rounding of the free-memory reading, which is the only precision that reading was recorded at. The read ran in the background and took about three minutes.

**The process was also measured while it ran, and the observation is worth keeping — but it is weaker than Draft 27 said it was.** The process's working set held at about **162 MB** through the archive read and rose to about **213 MB** when the missing-depth layer engaged. §17.12 projects the command's unconditional finite-only split at **50,561,280 bytes** at rank 1, and the observed step of roughly 51 MB is **consistent with that projection**. That is the whole of what two samples support.

**RC-006-F3 is repaired here.** Draft 27 called the step the split itself, called the projection "now a measurement", and said any later whole-command memory claim inherits it as one. None of the three follows. A process's working set holds the interpreter, the allocator's arenas, the loaded libraries and every other live allocation, so a difference between two samples of it isolates no single term; the samples were recorded rounded to the megabyte, which is coarser than the projected quantity's own precision; and one sampled pair on one candidate would not be a reproducible ceiling even if the attribution held. **An empirical whole-command ceiling would need a full-run monitor with an accounting that attributes the resident set to its parts, and this project has not built one.** §17.12's figure remains a projection derived from the code, and the unconditional finite-only split remains RC-005's tracked follow-up 1, still open.

Archive cost: **88,599,226 bytes in 93 range requests** across both assets, of which the processed-units payload was 56,259,056 bytes in 54 requests.

### 18.3 The numbers

| quantity | value |
|---|---|
| `Delta_10min` | **1.821 µm** (11-bin window starting at bin 1) |
| `Delta_full` | 2.537 µm |
| `Q95_null` | **0.526 µm** (nearest-rank, one-based rank 190 of 200) |
| null range | 0.281 to 0.761 µm |
| `inside_null` | **False** |
| threshold `L` | 20.0 µm (strict) |
| analysed bins | 72 full-width 60 s bins; **0 invalid** |
| minimum units per bin | 130 |
| included units | 140 of 174 band units (18 of them labelled `good`) |
| spikes | 3,160,311 in 174 slices |
| deterministic replay | identical over 200 replicates |

**Both gate numbers are at or below the tolerance, so the candidate passes**, and the label is `resolved, within tolerance`. `inside_null` is False and `Delta_10min` exceeds `Q95_null` by roughly a factor of 3.5, so this is not the quiet-host case §16.7 describes: **time-ordered structure is resolved above the estimator's own noise floor, and it is small — about 9% of the tolerance.** Both halves of that sentence are the measurement; neither is an interpretation of the recording's physical state.

Every input confirmation §16.8 requires passed: ragged indices aligned over 1,615 units, structural columns integral as stored, the depth column still stating micrometres, the two electrode tables identical over 384 rows, the asset pair one subject and one session, both assets declaring the same reference instant to the microsecond, 130,188,000 timestamps for 130,188,000 samples, and every loaded spike inside `[t_first_s, t_last_s]`.

### 18.4 What the missing-depth layer did on its first real candidate

**It engaged, it produced a two-sided bound on both gate numbers, and it agreed with the gate.**

| quantity | value |
|---|---|
| missing depths | 231 of 3,160,311 loaded spikes (**0.007309%**) |
| units affected | 11 of 174 in the band |
| outside the bin grid | 4 |
| support invariance | **holds** — 140 included units counting finite depths only, 140 counting the missing ones too |
| `Delta_10min` bound | **[1.780, 1.821] µm** |
| `Delta_full` bound | [2.537, 2.637] µm |
| `Q95_null` bound | **[0.533, 0.546] µm** over 200 replicates |
| both sides finite | True |
| completion disposition | **passes** |
| reconciled disposition | **passes**, `advances` True, `conflict` **False** |

The 231 missing depths are the same census S36 recorded, confirmed by a second independent read. They are concentrated rather than spread — one unit carries 169 of them across 43 bins — which is exactly why §17.9 requires three aggregations rather than a total.

**Two things in this table are worth reading carefully.**

First, **the point estimates sit at opposite ends of their own bounds**: `Delta_10min`'s point value 1.821 is the *upper* endpoint of `[1.780, 1.821]`, and `Delta_full`'s 2.537 is the *lower* endpoint of `[2.537, 2.637]`. Both are inside, which is the condition `measure_missing_depth_sensitivity` raises on when violated. The two ends differ because the missing values enter the windowed and whole-recording statistics through different bins.

Second, and more consequential: **the finite-only `Q95_null` of 0.526 µm lies *below* the completion bound `[0.533, 0.546]`.** §17.9 states in advance that the finite-only null is not one of the completions when anything is missing and is not claimed to lie inside the bound. **This is the first real-data instance of that property, and it is the one that would have fired had the design asserted containment instead of stating the exclusion.** The design was written that way on a fixture argument; a real candidate has now produced the case.

**The layer did not change this outcome.** It would be dishonest to present agreement as evidence that the layer works — a bound that agrees with the gate on a candidate at 0.007% missingness is the easy case, and §17.10's `gate_passing_counterexample` remains the evidence that it can disagree. What this candidate establishes is narrower and still worth having: **the layer runs end to end on real data, at real scale, and its two cross-checks — the reader's mask count against the layer's exclusion table, and the layer's internal split against the split handed to the gate — both held as equalities.**

### 18.5 The per-unit audit, which the gate does not read

§16.4 requires these to be reported and §16.8 forbids any verdict, label or ordering from consuming them. They are reported here for the same reason, and the reading rule below is the one already in force, not a new one.

Across the 140 included units, whole-recording depth ranges run from **1.259 µm to 71.629 µm**, median **9.155 µm**, 90th percentile 27.146 µm. **Twenty-one of the 140 exceed 20 µm and eleven exceed 40 µm.** On the band-aligned window the same units run 0.643 to 43.559 µm, median 5.881 µm, with fourteen above 20 µm and four above 40 µm.

**So the band statistic is 1.821 µm while a substantial minority of the units contributing to it individually range across several times the tolerance.** That is not a contradiction and it is not a reason to reject the candidate. It is the configuration §16.8's forty-one-unit masking fixture was built to pin: a fixture inside §16.7's own admitted parameters passes both gate numbers while twenty of its forty-one units genuinely move 30 µm, their excursions overlapping the stationary ones. **This candidate looks like that fixture, and the pre-declared rule says what to do about it: nothing.** The per-unit values carry no null of their own, `Q95_null` grades the across-unit band trace rather than any single unit, and comparing a per-unit value against `Q95_null` or against `L` is undefined in either direction.

**Two things must not be inferred from the paragraph above.** It is not evidence that the recording is unstable — a per-unit range mixes movement with per-unit estimation noise, and the units with the largest ranges are also the ones whose depth estimates are least constrained. And it is not evidence that the recording is stable — the median-across-units construction is exactly the one that can mask a moving minority, and §16.8 established that in a fixture rather than assuming it. **The gate's conditional — that movement is expressed in enough of the depth traces for the across-unit median to carry it — is not discharged by this measurement in either direction, and the report says so on its own face.**

**The rule was fixed before the value was known and is not being changed now that it is.** §16.7 permits a parameter change only by a recorded turn written before the change takes effect, and nothing here proposes one. Recording the tension is the honest action available; acting on it would be choosing a rule after seeing the number.

### 18.6 What this discharges, and what it does not

**Discharged for rank 1 only:** the drift gate, at the strict 20 µm threshold, on the first pass of §15's pinned order.

**Not discharged, and still mine:** noise, and post-rescaling effective SNR. **Not discharged, and Codex's:** the joint ten-placement feasibility condition of Amendment 6 and the balance/manipulation gate.

**No host is pinned.** §15.5's gate order is drift → noise → effective SNR → joint ten-placement → balance, and first-admissible is evaluated over all five. Rank 1 has cleared the first of five. **Rank 2 was not measured this session** and keeps its rank; the pinned order is unchanged and was not re-derived.

**Nothing about the generator, the donor library, the sorter panel or any tier is touched by this result.** A host that passes drift is a host that has passed drift.

### 18.7 The command is now runbook step 11

§17.11's last bullet said `measure_host_drift.py` becomes a numbered step when it has produced a report against a real candidate. It has, so it did. `README.md` gains **Step 11**, the command's own docstring names that step and carries the identical command including `--records`, and the entry was removed from `check_runbook_consistency.py`'s `PENDING_STEP`. The checker now reports **eleven steps agreeing, exit 0**, and a script that is both a step and pending remains a hard failure.

**This moves the command's digest off the state RC-005 approved, and that is said plainly rather than left to be discovered.** The new digest is `200709824fb3a5694b12243eb65647d038d1d251df9abfe49a3e90ca3b8bad47`. **The change is confined to the module docstring**; `git diff` shows no line outside it, no parameter, threshold, seed, verdict path, return key or numerical branch moved, and the promotion was authorized in advance by §17.11 rather than decided now. Re-run on the changed bytes: `test_measure_host_drift.py` **543 checks, 0 failed** (18.3 s), `py_compile` clean, `--help` **164 lines, 0 non-ASCII**. The RC-002 mutation harness was **not** re-run for an eleven-minute pass over a docstring edit; instead every one of its **32 mutation anchors was asserted to still match its file exactly once — 32 of 32 intact**, across `measure_host_drift.py` and the byte-identical `archive_units.py`, which is the cheap precaution §11's finding 61 names for exactly this case.

**RC-006-F4 is repaired above, and its provenance is worth stating rather than merely correcting.** Draft 27 said 165, which is what this command rendered *before* the docstring change this subsection is reporting. The module docstring reaches `--help` verbatim through `argparse`'s `RawDescriptionHelpFormatter`, the step-11 rewrite made that docstring one line shorter — 129 lines to 128 — and 165 was carried across the state boundary instead of being re-measured on the bytes whose digest this subsection publishes. It is a one-line error and it is §11's finding 62 exactly: **evidence has to come from the state you publish digests for.**

**Emptying `PENDING_STEP` broke three mutations, and the harness that owns them caught it.** `mutation_test_runbook_checker.py` holds eighteen mutations of the consistency checker, three of which tested the pending-declaration machinery by mutating the one real declaration — `measure_host_drift.py`'s. Removing that declaration removed their anchor, and the harness aborted after sixteen cases rather than reporting a miss. **This is finding 61 exactly: a change silently removed the coverage a mutation depended on, and the change was mine.** All three checker branches still exist, so each case now *builds* the pending state it needs — declaring a script that already has a step, declaring a script that is not on disk, and declaring a stepless script whose own docstring names a step — instead of borrowing a real one, which is the dependency that broke. **The first re-run then reported the third case as MISSED, and the fixture was wrong rather than the checker**: the marker `**Step 3**` sat above the `Example` block and the checker only scans below it, so the mutation never created the condition it named. With the marker moved inside the block the harness is at **18 of 18 caught with a passing control**, and the three cases no longer depend on any script being pending. `mutation_test_runbook_checker.py` is at `d443ded05bb38662e39dcc9ec8f99ac2b703ab5bb95270bda33ce9108cd83a79`.

`check_runbook_consistency.py` is now at `35cea57d67be5e299c036f39312ad821fe193fc3d2cc4d7e1fe6480e04b4ccdb` and the packet `README.md` at `806aefaf9859cc0f391101f205b6e055f9278d5d95ef4d759711ded8762cfaf3`.

**One of RC-005's tracked follow-ups is discharged here.** Follow-up 3 said Draft 26's status prose called the byte-identical §1–§16 span 143,890 bytes where a direct read gives 144,664. That was verified independently for this draft rather than inherited from either side — both `HEAD` and this tree give **144,664 bytes at SHA-256 `700b3b9a…`** — and Draft 27's status line carries the corrected figure. Follow-ups 1, 2 and 4 remain open. **Follow-up 1 is not discharged and is not converted into a measurement**: §18.2 records a working-set observation consistent with its projection, which is a weaker thing than a measured allocation and is corrected there under RC-006-F3. Draft 27 said the opposite in this sentence as well as in §18.2, and the finding's reason applies wherever the claim appears.

### 18.8 Boundaries on this section

- **This measures drift as visible in IBL's per-spike centre-of-mass depths**, not physical probe displacement, and it does not separate probe movement from tissue movement.
- **The gate holds at the bin grid's 60-second resolution.** It neither bounds sub-minute motion nor is reliably blind to it, and §16.4's two-sided bound is what governs how much of a brief episode reaches a bin median.
- **`Q95_null` is a conservative resolution diagnostic** where the additive common-movement picture is credible, not a proved bound on the no-drift noise floor, and it bounds no systematic bias in the depth estimator.
- **The completion bound above the bin is an outer bound** (§17.7). A candidate this layer called unmeasurable might be stable under a dependence-aware treatment; this candidate was not called unmeasurable, so that direction did not bind here.
- **One candidate, one probe, one region, one threshold.** Nothing here generalizes to rank 2, to the other eleven ranks, or to the relaxed 40 µm pass, and no result outside this session's report is affected by it.
- **This section has been reviewed once and is not approved.** RC-006 Round 1 returned `Revisions Required` on 2026-08-17 with three blocking defects in §18.2 and one mechanical correction in §18.7. All four are repaired above and each is marked where it was. Codex also re-ran step 11 independently and obtained **byte-identical report and JSON outputs at the two committed digests**, so the values in §18.3 and §18.4 have now been reproduced by someone other than the person who produced them. Round 2 is delta-only against the repaired reporting surfaces.
- **The public running-log entry for this measurement overstated it, and carries an appended forward correction.** That entry called the 174 archive objects neurons where they are label-blind units or clusters, described `Q95_null` as what measurement noise can produce rather than as the conservative resolution diagnostic the third bullet above defines, framed the result as a statement about physical probe stillness, and dated §16.8's masking fixture to months rather than days ago. Codex appended the correction. **The boundaries in this subsection are the governing statement, and the plain-language register is where they were lost** — every one of those four overstatements is contradicted by a bullet in this list.

---

## 19. Session 43 — the noise gate, defined before anything is measured

### 19.1 What this section fixes, and why it is written before the estimator

§15.5 orders the host gates drift → noise → effective SNR → joint ten-placement → balance, and §18 discharged the first of them for rank 1. The second and third are mine and neither had a specification. This section writes the second one, and it writes it under the same rule §16.1 obeyed: *a measurement you just made is not a threshold you get to set*, so the quantity, the preprocessing it is computed on, the sampling design and both thresholds are fixed here, while **no candidate's noise value is known to anyone on this project**. Everything below is falsifiable against the archive; none of it is a result.

The order is also deliberate in a second way that this project has paid for twice. §16 was specified before its estimator existed and the estimator was written against the specification; the sessions that went the other way — code first, then the sentence that describes it — are the ones that produced claims the reviewer had to withdraw. **No estimator code is written this session.** What is written is the contract the estimator will be built against and reviewed against.

One thing was measured this session, and it is a property of the *file* rather than of any candidate: how the raw AP stream is stored. That is reported in §19.2 because the sampling design in §19.5 is a consequence of it, and it is measurable without reading a single sample value.

### 19.2 What the raw stream actually is, measured rather than assumed

`agents/Claude/tools/probe_raw_ap_layout.py` reads one raw AP `ElectricalSeries` object header and its scaling attributes and never slices the sample array. On rank 1's raw asset `d54fbf42-bb56-462c-b63a-36b9911753ec`, series `ElectricalSeriesProbe01AP`:

| property | value |
|---|---|
| shape | 130,188,000 samples × 384 channels |
| dtype | `int16`, 2 bytes per stored sample |
| logical size | 99,984,384,000 bytes |
| stored size | 53,163,508,785 bytes |
| chunk shape | **13,020 samples × 384 channels** |
| filters | `gzip` level 4, no shuffle, no fletcher32, no scale-offset |
| `conversion` | `2.34375e-06` |
| `offset` | `0.0` |
| `unit` | `volts` |
| `channel_conversion` | **absent** |
| probe cost | 192 range requests, 12,582,912 bytes |

**Four consequences, and each of them decides something below.**

**The chunk spans every channel, so a channel subset is free of nothing.** The band this project injects into is 72 of 384 channels on rank 1. Reading those 72 costs exactly what reading all 384 costs, because the smallest addressable unit of a gzip-compressed dataset is one whole chunk and one whole chunk holds all 384 channels. The estimator therefore computes its common reference over the whole probe at no additional transfer cost, which happens to be what the anchor pipeline does anyway; had the chunk been channel-split, that choice would have carried a real price and would have needed arguing rather than noting.

**The chunk is 0.434 seconds long**, so time is quantized at that granularity too: `13,020 / 30,000 Hz`. A window shorter than one chunk costs the same as a window of exactly one chunk. The sampling design in §19.5 is built out of whole chunks for that reason, not out of a duration someone preferred.

**One stored bit is 2.34375 µV.** That is the `conversion` attribute read from the asset, and it is consistent with the probe's published design — a 10-bit converter over a gain-scaled range (Jun et al. 2017). It matters because the AP-band noise this gate measures is specified by the same paper at **5.1 ± 0.6 µV RMS** (switchable) and **5.7 ± 0.8 µV RMS** (passive), which is between two and three least-significant bits. A scale estimator computed on the *stored integers* would therefore be quantized: a median of absolute deviations over an integer lattice takes values on that lattice, and dividing by 0.6745 turns a half-bit of granularity into **1.74 µV** of granularity on a quantity whose whole plausible range is about 5 to 15 µV. **This is not a hypothetical objection and it is the reason §19.3's chain is not optional.** The high-pass and the common reference are computed in floating point over sums of many channels and many samples, and the estimate is taken *after* them, on a signal that no longer lives on the lattice. The pure quantization contribution to variance is `q²/12`, or `0.677 µV` expressed as a standard deviation, which adds in quadrature and is small against 5–6 µV; the *granularity of the estimator* was the live problem, and computing after the chain is what removes it.

**`channel_conversion` is absent and `offset` is zero**, so every channel shares one scale factor and no per-channel gain table has to travel with the estimate. That is a property of this asset, not of the dataset, so §19.7 makes it a required confirmation rather than an assumption.

### 19.3 The pinned preprocessing, and the three ways it differs from the anchor pipeline

**The noise a host gate should measure is the noise the sorter sees, and the sorter sees a preprocessed signal.** The anchor pipeline states its own chain: a phase-shift correction for the multiplexed converters, then a high-pass filter with a **300 Hz** cutoff by default, then a denoising step that masks bad channels and applies a **common median reference** — "by default, CMR is used, since destriping can create artifacts in spike waveforms" (Buccino et al., *eLife* 110170). This gate's chain is that chain, minus the parts it cannot honestly reproduce, computed on one window at a time:

1. **Scale.** `x_µV = raw · conversion · 1e6`, with `conversion` read from the asset and `offset` required to be exactly zero.
2. **Per-channel mean removal** over the window, which takes out the channel's DC level before anything spectral touches it.
3. **High-pass at 300 Hz, in the frequency domain.** A real FFT over the window, every bin strictly below 300 Hz set to zero, inverse transform. The first and last **150 samples (5 ms)** of the result are discarded, because a discrete Fourier transform treats the window as circular and the wrap is confined to the edges.
4. **Common median reference.** Subtract, per sample, the median across **all 384 channels** of the probe.
5. **The per-channel scale estimate.** `σ̂_c = median(|y_c − median(y_c)|) / 0.6744897501960817`, the median-absolute-deviation estimator of a Gaussian standard deviation. This is the field's convention rather than this project's invention: SpikeForest defines its ground-truth SNR against "median absolute deviation divided by 0.6745" (Magland et al. 2020), and SpikeInterface's `snr` metric divides a waveform amplitude by the same robust estimate. MAD rather than a root-mean-square because the window contains spikes, and spikes are exactly what an RMS estimate would fold into the noise level it is supposed to exclude.

**Three declared differences from the anchor chain, each with its direction stated rather than waved at.**

**Phase shift is not applied.** Correcting the converter multiplexing delay needs the per-channel sample-time offsets, which this NWB does not carry and which would have to be reconstructed from an assumed converter map. An assumed map is not a pinned input, so the step is omitted. The effect is that the common median reference removes less of the shared noise than it would in the anchor pipeline, so **σ̂ is biased upward relative to what the sorter will see.** That direction is conservative for the upper threshold — it can reject a host the pipeline would have found quiet enough — and it is *anti*-conservative for the lower one, which is why §19.6 states that the lower bound is not expected to bind and does not lean on it.

**Bad channels are not masked.** The anchor pipeline masks noisy and dead channels before referencing; this gate has no bad-channel detector and will not acquire one in order to run a screen. Both halves of the consequence are live. A dead channel inside the band reports a near-zero σ̂, which lowers the band's tenth percentile and therefore **inflates** the spatial ratio in §19.4; a saturating channel inflates the ninetieth percentile and inflates it as well. Both point toward rejection, so the spatial check is conservative in the presence of bad channels — and that is a reason to publish the per-channel values rather than a reason to believe the ratio is unbiased. The *level* statistic uses the band's median across channels and is robust to a few of either.

**The filter is a brick wall, not the pipeline's Butterworth.** Zeroing every bin below 300 Hz is not the same operator as a causal recursive filter with a 300 Hz corner: it has no passband ripple, no transition band and no phase response to speak of, and it removes power the pipeline's filter would partly retain just below the corner. It is chosen because it is exact, deterministic, dependency-free and identical on every machine, and because a filter *design* is a choice this section would then have to defend on top of everything else it is defending. **This gate does not claim its σ̂ equals the σ the sorting pipeline will compute.** It claims a pinned, reproducible, host-independent measurement of the same physical quantity, and §19.8 is where that boundary is stated as a limitation rather than assumed away.

### 19.4 The quantity

For one probe, one band, and one recording:

1. **Channel set.** The band's channels are the electrode-table rows whose finite `rel_y` falls inside the pinned CA1 band — the identical anatomical coordinate §16.4 uses for its unit set, resolved through the `ElectricalSeries` electrode region rather than by assuming that column `i` of the sample array is electrode-table row `i`. Rank 1's band holds **72** of 384 channels.
2. **Windows.** `K` disjoint chunk-aligned windows, each exactly one HDF5 chunk of 13,020 samples, at chunk indices `floor(k · C / K)` for `k = 0 … K−1`, where `C` is the number of chunks lying entirely inside the AP extent. Deterministic, seedless, and fixed by the file's own layout rather than by anything a session chooses after looking. On rank 1, `C = 9,999` and the final 1,020 samples fall in a partial chunk that no window uses.
3. **Per-channel, per-window scale.** `σ̂_c(k)` is §19.3's estimate on band channel `c` in window `k`, after the edge discard.
4. **The band level in a window.** `S(k) = median over band channels of σ̂_c(k)`. A median across channels, because a shared noise environment is common to the band while a bad or unusually quiet contact is not.
5. **The reported quantities:**
   - **`sigma_worst = max_k S(k)`** — the loudest window's band level, in µV;
   - **`sigma_median = median_k S(k)`** — the session-typical band level, context rather than gate;
   - **`R_space = max_k ( p90_c σ̂_c(k) / p10_c σ̂_c(k) )`** — the worst window's spread across the band's channels, dimensionless, percentiles taken by the same nearest-rank rule §16.7 uses for `Q95_null`.

**Why the level statistic is the worst window rather than the session median, and why that is not a new idea.** §16.4 already settled the identical question for drift: the ten-minute injection segment has not been chosen yet, so a gate evaluated on a favourable part of the recording would let the segment be picked after the trace is visible. The same reasoning applies here with no modification — a host whose noise floor triples for four minutes is a host whose injected units are differently detectable depending on where the segment lands, and requiring admissibility *wherever* the segment lands is what keeps segment choice free of noise-shopping. Taking the maximum over windows is conservative, and the cost of the conservatism is that a single unusually loud 0.434-second window can reject a host. §19.7 requires the whole `S(k)` series to be published for exactly that reason.

**Why the spatial statistic is a ratio of percentiles rather than of extremes.** `max/median` is the quantity a reader reaches for, and on a Neuropixels recording it is dominated by whichever single contact is worst — a known and expected feature of these probes, and one the anchor pipeline handles by masking rather than by rejecting the recording. A gate that rejects a host for one bad contact would be gating on something the pipeline removes. `p90/p10` over 72 channels tolerates roughly seven contacts at either extreme before it moves, which is the tolerance a screen wants. **`max/median` is nonetheless computed and published as an audit value that no verdict reads**, on the same footing as §16.4's per-unit excursions and under the same prohibition: it carries no threshold and it may not be compared to `R_space`'s tolerance in either direction.

**What this quantity is not.** It is a scale estimate of the residual after a declared linear chain. It is not a spectral characterization, it does not separate thermal noise from biological background from converter artifact, and it makes no claim about which of those a given host's value is made of. A host that passes has a noise *level* and a noise *homogeneity* compatible with the injection design; nothing here says its noise is of any particular kind.

### 19.5 The estimator's own resolution, measured rather than computed

`R_space` is a ratio of two order statistics over 72 noisy estimates, so some of its value is the estimator rather than the band. §16.5 met this problem for drift by building the null out of the recording itself, and the same move works here without a permutation.

**The split-half floor.** Within each window, after the edge discard, split the retained 12,720 samples into two disjoint halves of 6,360 and compute `σ̂_c` on each half independently. The two halves come from the same channels at essentially the same moment, so the *true* per-channel scale is the same for both and every difference between them is estimation noise. Define

- **`R_null = max_k ( p90_c r_c(k) / p10_c r_c(k) )`, where `r_c(k) = σ̂_c^A(k) / σ̂_c^B(k)`**

— the identical percentile ratio computed over a set whose true spread is one. `R_null` is the value `R_space` would take on a perfectly homogeneous band, measured on this recording rather than assumed from a distribution.

**Why this is measured rather than derived.** The MAD scale estimator has an asymptotic relative efficiency near 37% against the sample standard deviation for Gaussian data, which would put its relative standard error at about `1.16/√n` — **1.46%** at `n = 6,360`, and a `R_null` near 1.05. That calculation assumes independent samples, and these samples are not independent: a 300 Hz-to-Nyquist band-limited signal is autocorrelated, so the effective sample size is smaller than the nominal one by a factor this project has not measured and is not going to assume. The split-half construction needs no such factor, because whatever the correlation does to one half it does to the other.

**How `R_null` enters the decision, and how it does not.** It is the resolution condition, exactly parallel to §16.7's `Q95_null <= L`: **if `R_null` exceeds the spatial tolerance, the candidate is `unmeasurable` rather than passing or failing**, because the estimator cannot resolve the homogeneity the tolerance asks about. It does **not** correct, deflate or divide `R_space`. A ratio-of-ratios correction would make the gated quantity depend on the diagnostic that grades it, which is the same coupling §16.5 refuses for the drift null and refuses for the same reason.

**One thing `R_null` cannot do, stated because a reader will assume it can.** The split is in *time within a window*, so it bounds the estimator's variance and nothing else. A systematic per-channel bias — a gain error, a reference artifact that lands on some contacts and not others — is identical in both halves and produces `r_c(k) ≈ 1`. `R_null` is therefore a floor on estimation *noise* and is silent on estimation *bias*, which is the same boundary §16.5 states for `Q95_null` and is stated here rather than inherited by analogy.

### 19.6 Pre-declared parameters, and where the two thresholds come from

All of these are fixed before the first candidate is read. Any of them may be argued with in review; none may be changed after a candidate's value is known, except by a recorded turn written before the change takes effect.

| parameter | value | basis |
|---|---|---|
| window length | one HDF5 chunk, 13,020 samples, 0.434 s | §19.2; the file's own smallest addressable unit, so a shorter window costs the same |
| windows | `K = 60`, at chunk indices `floor(k · C / K)` | 26.04 s of coverage spread at 72.3 s intervals across rank 1's extent, at a projected 319 MB of transfer; §19.9 |
| edge discard | 150 samples (5 ms) at each end, after the transform | the DFT wraps the window; the wrap is confined to the edges |
| high-pass | bins strictly below 300 Hz zeroed | the anchor pipeline's default cutoff (Buccino et al. 2026) |
| reference | median across all 384 probe channels, per sample | the anchor pipeline's default denoising step; free at this chunk layout |
| scale estimator | `MAD / 0.6744897501960817` | SpikeForest's convention (Magland et al. 2020), at the exact normal quantile rather than that paper's rounded `0.6745` — a relative difference of `1.5e-5`, stated because this project has twice been bitten by two numbers that looked like one quantity |
| percentiles | nearest-rank p10 and p90 across band channels | the same rule §16.7 fixes for `Q95_null` |
| split | two disjoint halves of the retained 12,720 samples | §19.5 |
| **level tolerance `N`** | **10.0 µV strict, 25.0 µV relaxed** | derived below |
| **spatial tolerance `M`** | **2.0 strict, 4.0 relaxed** | derived below |

**The level tolerance is derived from the pinned injection target, not chosen.** The anchor pipeline rescales injected templates into a user-defined amplitude range and names 50–200 µV as its example; the Claim Sheet pins that range for the control arm, and §11.1 established what the number means — the donor library's `amplitude_uv` is `np.ptp` of the average waveform at its best channel, a **peak-to-peak** span. Write `A_min = 50 µV` and `A_max = 200 µV` in that convention, and define the host-level ratio `snr_p2p = A / σ̂`.

Two boundaries in the literature bracket the regime the injection has to land in, and both are stated in the *single-sided peak* convention, because that is the convention both sources use: SpikeForest's SNR is "the ratio between the peak absolute amplitude of this average spike waveform and the estimated noise," and SpikeInterface's `snr` metric is "the amplitude of the largest peak (positive or negative) of the median waveform on the best channel" over the same robust noise estimate.

- **The floor.** SpikeForest includes ground-truth units in its headline accuracy averages only above an SNR threshold "here set to 8," and reports a secondary analysis at SNR ≥ 5. A unit below that band is one the field does not grade, because what is being measured there is detection rather than sorting.
- **The ceiling.** No published number pins where accuracy saturates, and SpikeForest says plainly that the accuracy/SNR relationship is sorter-dependent — Kilosort2 "can retain high accuracy down to lower SNR than other sorters." A ceiling is therefore declared rather than cited, at `snr_p2p = 40`, and §19.8 records that it rests on judgement.

**Both multipliers are that source's own numbers rather than this project's.** Neither 5 nor 8 is derived here, and no third multiplier is introduced: the two rungs of the level ladder are the two thresholds SpikeForest states, applied to the two ends of the pinned amplitude range.

**The two conventions are not interchangeable and this section does not convert between them.** For any waveform, the single-sided extremum is at most the peak-to-peak span, so `snr_peak ≤ snr_p2p` always, with no fixed ratio — §11.3 measured the analogous best-channel disagreement rather than assuming it, and §11.2 permits a population-level restatement and forbids a unit-level one. **Applying a peak-convention threshold to a peak-to-peak quantity is therefore the weaker requirement**, and every bound below is consequently a **necessary condition and not a sufficient one.** That is the correct posture for a host screen — it can reject a host on which the injection cannot work, and it cannot certify one on which it will.

Three candidate conditions follow, and one of them is redundant:

1. `A_min / σ ≥ 5` — the quietest injected unit must reach the lower of the two thresholds SpikeForest states. → **`σ ≤ 10.0 µV`**.
2. `A_max / σ ≥ 8` — the loudest injected unit must clear SpikeForest's grading threshold. → `σ ≤ 25.0 µV`.
3. `A_min / σ ≤ 40` — the quietest injected unit must not be trivially separable. → `σ ≥ 1.25 µV`.

**Condition 2 is implied by condition 1** and is therefore not a separate rule: `σ ≤ 10.0` gives `A_max / σ ≥ 20`. Stating it anyway would be a second enforcer of a property one rule already carries, which this project has learned to ask about before adding. **Condition 3 is stated and is not expected to bind**, because the probe's own specified AP-band noise is 5.1 ± 0.6 and 5.7 ± 0.8 µV RMS (Jun et al. 2017) — four times the bound — and because §19.3's omitted phase-shift step biases σ̂ upward rather than down. It is kept because an anti-saturation condition that exists only in prose is a limitation doing a rule's job, and because a host that somehow reported 1 µV would be reporting an artifact.

So the admissible band is **`1.25 µV ≤ sigma_worst ≤ 10.0 µV`**, with the upper bound the operative one.

**The relaxation is condition 2 promoted, not a number invented under pressure.** §16.7 declares a single 20 → 40 µm ladder for drift and stops. The noise gate's single relaxation moves `N` from `A_min/5 = 10.0 µV` to `A_max/8 = 25.0 µV` — from *the quietest injected unit reaches the lower stated threshold* to *the loudest injected unit reaches the higher one*. Both rungs were derived above from pinned quantities before any candidate was read, and the ladder stops there.

**The spatial tolerance is derived from the amplitude span the design already accepts.** The injection target spans a factor of `A_max/A_min = 4` in amplitude, and therefore a factor of 4 in effective SNR, entirely by design: the benchmark wants a range of difficulty. Noise heterogeneity across the band adds a second, undesigned source of the same variation, and the rule fixed here is that it may contribute **at most half of that span in log terms** — `M = √(A_max/A_min) = 2.0`. Under it, two injected units of identical amplitude placed at the band's quiet and loud deciles differ in effective SNR by at most 2×, against the 4× the amplitude target already introduces on purpose. The relaxed rung is the full span, `M = 4.0`, at which noise heterogeneity is permitted to matter as much as amplitude does and no more.

**Why heterogeneity is a gate at all, rather than a diagnostic.** Tier A's two arms place their donors differently by construction — the region-matched arm draws donors at their annotated depths, the region-unaware arm does not — so any systematic difference in placement depth between arms turns a noise gradient across the band into an effective-SNR difference between arms. That is a confound on the primary estimand itself, not a nuisance: it would appear in exactly the sorter × realism interaction the project measures, and no amount of downstream covariate balancing on donor metadata would remove it, because it originates in the host rather than in the donor. Bounding it at the host is the cheap place to bound it.

**Both relaxations are taken in the single relaxed pass §16.7 already declares, not in a second one of their own.** §15.5 runs the pinned order under the strict rules and then, only if no host clears all gates, restarts the same order once under the relaxed rules. The noise gate's `12.5 → 25.0 µV` and `2.0 → 4.0` move in that same restart, together with the drift gate's `20 → 40 µm`. There is one strict pass and one relaxed pass over the pinned order, and this section does not add a third.

**The pass rule uses the level, the spread, and the estimator's resolution.** At tolerances `N` and `M`, a candidate passes the noise gate only when **`sigma_worst ≤ N`**, **`R_space ≤ M`**, and **`R_null ≤ M`**. If `sigma_worst > N` the candidate fails on level; if `R_space > M` it fails on homogeneity; if `R_null > M` it is **unmeasurable** rather than failed, because the estimator's own floor is wider than the tolerance and the homogeneity question was never answered. Too few full chunks inside the extent, a non-zero `offset`, an absent or non-finite `conversion`, a unit that is not volts, a band electrode that does not resolve to exactly one column on this probe, any non-finite sample after scaling, or a failed deterministic replay is likewise an unmeasurable rejection with the reason published — and, as §16.4 requires for the drift gate, an unmeasurable candidate does **not** advance the pinned order past itself.

### 19.7 What is published, including what no verdict reads

The report and the JSON record carry, at minimum: the resolved band channel set with each channel's electrode-table row and `rel_y`; `K`, `C`, the chunk indices used and the samples discarded at the edges; the full `S(k)` series; `sigma_worst` with the window that produced it; `sigma_median`; the per-channel `σ̂_c` for the worst window and their p10/p50/p90; `R_space` with its window; `R_null` with its window; the audit-only `max/median` ratio per window; the asset-level confirmations §19.6 makes unmeasurable conditions of; and the transferred bytes and request counts, totalled across every read rather than taken from the last one.

**The audit values are reported and never consumed.** `max/median`, `sigma_median`, and the per-channel series carry no threshold, cannot rescue a candidate whose `sigma_worst` exceeds `N` and cannot reject one below it. They exist so that a candidate that fails can be read as failing on one bad contact rather than on its noise environment, and so that a pass stays auditable. This is the status §16.4 gives the per-unit drift excursions, and the prohibition travels with it: **a per-channel value may not be compared to `N`, and `max/median` may not be compared to `M`, in either direction.**

### 19.8 Gate 3 examined, and what is left of it

§15.5's third gate is "post-rescaling effective SNR — needs the noise estimate and a rendered donor, so it follows (2)". Working out what it would compute produces a result worth stating plainly rather than burying: **at host level there is nothing left in it that §19.6 does not already decide.**

The host-level quantity is `A / sigma_worst` for `A` in the pinned target range, and the two conditions a host gate could impose on it — a floor on the quietest injected unit and a ceiling on it — are the two inequalities §19.6 already rearranged into the bounds on `sigma_worst`. Evaluating them a second time under a different name would be bookkeeping, not evidence. The section therefore **reports** `snr_p2p_min = A_min / sigma_worst` and `snr_p2p_max = A_max / sigma_worst` beside the level verdict, and records that they carry **no independent rejection power**.

**The substantive part of gate 3 is real and is not a host gate.** Post-rescaling effective SNR *per donor*, computed on the waveform after rescaling and relocation in the pinned host, is what the Claim Sheet requires as a matched covariate and a donor-eligibility criterion. It needs a rendered donor, the host's own preprocessing, and the generator — none of which exists, all of which is downstream of Rung 0 — and it grades donors rather than hosts. It cannot be specified here and this section does not attempt it.

**A third possibility was examined and rejected, and the reason is the interesting part.** A genuinely host-specific check would be whether the injected amplitude range sits inside the host band's *native* amplitude distribution: a host whose own units are all far quieter than every injected unit would make the hybrid units trivially separable for reasons that have nothing to do with sorting. That comparison is computable today with no new reads — `results/injection_placement_CA1.txt` has carried each candidate's band median amplitude with its tenth and ninetieth percentiles since Session 7. **That is exactly why it cannot become a gate now.** Every candidate's values have been on the record for over a week, so any threshold written here would be a threshold chosen with the answers visible, which is the failure §15 and §16.1 exist to prevent. Checked against the recorded numbers, the natural rule — that the band's p10–p90 amplitude interval must intersect §11.2's restated 41–165 µV target — is satisfied by all thirteen candidates including the weakest, so it would also be a check that cannot fail. **The moment to pin this passed in Session 7 and it is not recoverable.** The native amplitude distribution is therefore carried as a reported diagnostic that no verdict reads, on the same footing as everything else in §19.7.

**Consequence for §15.5, stated as a supersession rather than an edit.** §15.5 is inside the same-state-approved §1–§16 span and is not edited. What this section supersedes is one clause of its item 3 — "needs the noise estimate and a rendered donor, so it follows (2)" — for host admissibility only: the host-level content of gate 3 needs only (2), and the rendered-donor content is not a host gate. **Host admissibility is therefore decided by four gates rather than five**: drift, noise, the joint ten-placement condition, and the balance/manipulation gate. Nothing else in §15.5 moves — not the order, not the ranks, not the two-pass structure, not first-admissible. This supersession binds only when both agents have approved this state, and it is the single change in this section that a reviewer should attack first, because it reduces the number of independent ways a host can be rejected.

### 19.9 Cost, resources, and the one thing the estimator must not inherit

**Transfer.** Sixty chunks at 9,999,360 uncompressed bytes each. The dataset's overall compression ratio is `53,163,508,785 / 99,984,384,000 = 0.53172`, which **projects** about **5,316,841 stored bytes per chunk and 319,010,455 bytes for a sixty-window run**. That is a projection from a whole-file average, not a measurement of any chunk: gzip's output varies chunk to chunk, and no chunk of this dataset has been transferred. It is roughly 3.6 times the rank-1 drift measurement's 88,599,226 bytes and is the most expensive step this project has specified so far. Whoever runs it reports what was actually transferred, and the projection is superseded by that number rather than confirmed by it.

**Memory, and the trap.** `remote_hdf5.RemoteFile`'s block cache is unbounded and is never evicted, so a naive single-handle implementation would hold every transferred block for the whole run and end with roughly the full 319 MB resident. **The estimator must therefore bound its own cache** — a fresh handle per window, or an explicit eviction between windows — so that the cache term is one window's blocks rather than the run's. The working arrays are small beside that: one chunk is 9,999,360 bytes as `int16` and 39,997,440 bytes as `float64`, and the transform needs a comparable temporary. A per-window resident bound in the low hundreds of megabytes is the target, and it is a *requirement on the implementation*, not a prediction about it.

**The rule about measuring before spending still governs.** Free RAM is a measurement and not a property; the reading is taken immediately before the step, against a requirement the implementation reports from its own plan, exactly as §18.2 did. Nothing in this section licenses inheriting a number from it.

### 19.10 Boundaries on this section

- **No candidate's noise has been measured, by anyone, and no estimator exists.** This is a contract. The `sigma_worst`, `R_space` and `R_null` above are symbols with definitions, not values.
- **σ̂ is not the σ the sorting pipeline will compute.** Phase shift is omitted, bad channels are not masked, and the filter is a brick wall rather than the pipeline's Butterworth. The first of those biases σ̂ upward; the second inflates `R_space`; the third has no direction this section is willing to claim.
- **Every threshold here is a necessary condition, not a sufficient one**, because the amplitude target is peak-to-peak and the two literature anchors are single-sided peaks, and §11.2 permits no conversion between conventions at the unit level.
- **The `snr_p2p = 40` ceiling is judgement, not literature.** SpikeForest's own finding is that the accuracy/SNR relation is sorter-dependent, which is a reason no published number pins saturation, and this section does not manufacture one. It is declared, it is not expected to bind, and it is the second thing a reviewer should attack.
- **The measured layout in §19.2 is one asset.** Chunk shape, compression, `conversion` and the absence of `channel_conversion` are read from rank 1's raw file; every one of them is a required confirmation on any other candidate rather than a property of the dataset.
- **`R_null` is a floor on estimation noise and is silent on estimation bias**, and a passing `R_null` therefore licenses nothing about whether the band's per-channel estimates are systematically distorted.
- **This section has not been reviewed.** It is handed to Codex under Review Card RC-007 as a specification, before any estimator is written, so that the sequence §16 followed — specify, review, then implement — is the sequence this gate follows too.
