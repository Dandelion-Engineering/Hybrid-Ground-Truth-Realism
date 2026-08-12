# Human Report 8 — Claude

**Date and time:** 2026-08-12 12:30 PDT
**Session:** Claude Session 8
**Phase at start:** Phase 2 — Execution
**Phase at end:** Phase 2 — Execution. Claim Sheet Amendments 1, 2 and **4** are `In force`; Amendment 3 is `Proposed` at a Claude-edited state awaiting Codex. **No host is pinned, no sorter has run, and no scientific result about the project's question exists.**

---

## Summary

Two things happened this session. I completed the owner re-review Codex handed back — accepting all of its corrections and adding one of my own to Amendment 3 — and then ran the check that Codex's review had made load-bearing: whether the donor template library's amplitude column and the host recordings' amplitude column are the same measurement.

They are not. That is the session's substantive result, and it invalidates the *reasoning* behind an observation I published in Session 7 and in the public log, though not its direction.

---

## 1. The owner re-review, and why I accepted everything Codex changed

Codex reviewed my Session 7 amendments and the Tier A selection draft, edited them, and handed back three approved states. My job this session was to genuinely re-review the edits rather than accept them — which, per my own Session 6 note, is the moment where the pull is to approve everything and move on.

I re-derived every measured claim from the tracked JSON rather than reading Codex's prose:

- **Laboratories and institutions:** donor `{cortexlab}` ×12 at UCL; host `{churchlandlab ×3, angelakilab ×6}` at CSHL and NYU. Intersection empty. Confirmed.
- **Task-protocol versions:** the two sides overlap at exactly `{6.4.2}`. **Codex was right and I had been self-contradictory** — my Session 7 sentence said the versions "differ across the two sides" directly above a list in which both sides carry 6.4.2.
- **Strain:** I re-read my own script to check that a `None` really means an absent HDF5 dataset rather than an empty one. It does. "No field at all" holds across all 21 files.
- **The seed Codex pinned into Amendment 3:** SHA-256 of the named phrase is `2a66865b5504…` and `0x2a66865b` is `711362139`. It checks out. This was a newly-inserted checkable claim in the contract, so it needed checking rather than trusting.

Codex's most important correction was that Amendment 3 had promoted a *provisional* 1,149-template metadata screen into the final control pool. The real region-unaware arm draws from the pool that survives host-specific eligibility, and the negative control must mirror the arm that actually exists. I should have caught that.

Its rig correction is the same class of error I raised on *it* in Session 7, running the other way: I inferred rig separation from institution separation and stated it as measured. Its replacement keeps both directions explicit — different institutions cannot share one physical rig, rig design remains unverified — so it fixes the overclaim without creating the silence problem I had warned about.

**Amendment 4 is now `In force` in both sheets.**

## 2. The one edit I made, and the argument for it

Codex's Amendment 3 fixes the *seed* for the negative control's sixteen-template subset before the pool exists, but leaves the *objective, covariate scaling, search budget and tie-break* to be frozen later, at configuration-approval time — which is after the pool exists. It guards that with a requirement that both agents approve the configuration.

I do not think approval closes it, because the freedom is directional:

> A subset that matches the real CA1 sixteen **worse** widens the safety band, which is the conservative error. One tuned to match them **better** narrows it — and a narrower safety band makes the real result look more decisive.

So an objective chosen with the pool in view can only ever flatter us, and two agents approving it afterwards would be approving a choice already contaminated by the view. Codex's own argument for pinning the seed early applies unchanged to the rule.

Amendment 3's point 1 now fixes the whole rule, all of which is determinable without the pool: three named covariates standardized over the eligible pool; an equally weighted sum of 1-Wasserstein distances against the CA1 sixteen; a seeded start plus improving pairwise swaps to convergence or 100,000 evaluations; ties to the lowest template index. Changing any of it takes its own amendment. What the configuration still freezes is the genuinely host-dependent part — which templates are eligible — plus the realized outputs.

Both sheets carry the change. **Amendment 3 is therefore back to `Proposed`, awaiting Codex.** It continues to block all Tier A generation, which costs nothing in practice because several other gates are open anyway.

## 3. The amplitude-convention check — the session's real work

### What was wrong

The Claim Sheet rescales every injected template into a 50–200 µV band, stated in the donor library's `amplitude_uv`. In Session 7 I compared that band against the host recordings' `median_spike_amplitude_uV` and reported that it brackets the well-isolated units. I flagged that the conventions were unverified; Codex sharpened the flag into a rule: until they are shown commensurate, *neither* "the target is defensible" nor "the target is too loud" is supportable.

### What the sources actually say

Reading the upstream build scripts at pinned commit `0023db29688842f74698bac40c48a86477ea39e7`, and the NWB files' own column descriptions:

| | What the number is |
|---|---|
| Donor `amplitude_uv` | `np.ptp(templates_array, axis=1)` at the best channel — the **peak-to-peak swing, over time, of the average waveform** |
| Host `median_spike_amplitude_uV` | the **median over spikes** of a column the file describes as *"Peak amplitude of each spike"* |

A trough-to-peak span of an average, versus a median of per-spike single-sided peaks. Both are in microvolts, which is exactly why the mismatch was invisible.

### The conversion, measured rather than argued

The processed NWB carries `waveform_mean` per unit, in volts. That let me evaluate the donor column's *definition* on host units with exact unit identity and no matching problem — take the peak-to-peak over time on the channel maximising it, convert, and divide by the host column.

| cohort | n | ratio, median | p10–p90 |
|---|---|---|---|
| all units | 1,821 | 1.250 | 1.13–1.91 |
| Kilosort `good` | 478 | 1.242 | 1.11–2.50 |
| all IBL quality metrics passed | 201 | **1.207** | 1.10–1.51 |

A central factor near 1.2 supports restating the target as roughly **41–165 µV** in host-column terms at the population level. The p90 does **not** support converting any single unit, and I wrote that boundary into the artifact so the median is not quietly reused later as a per-unit factor.

**The direction of my Session 7 observation survives** — 41–165 still brackets the host bands' 51–110 µV good-unit medians — but it survives on different numbers than the ones it was reached with, and it had been reached by an undefined comparison. That is logged as a correction rather than silently fixed.

### Three things the check turned up on the way

1. **The donor library is good-clusters-only by construction.** `IblSortingExtractor(..., good_clusters_only=True)`. Nothing in the project had recorded this. It bounds what any Tier A result describes and it belongs in the manipulation check's framing.

2. **A third best-channel rule exists.** IBL's `max_electrode` agrees with the upstream peak-to-peak rule on only **72.6%** of units, usually a near tie between adjacent contacts. Every ratio is reported at both channels and they agree to ~0.02 in the median, so the conversion is safe. But donor depth and host unit depth are computed at best channels chosen by *different rules* — one contact, 20 µm, in the disagreeing quarter. Small against a 60 µm margin, not zero, and it is an input to the placement calibration Codex owns rather than a surprise to be found inside it.

3. **The 50–200 µV target is the donor pool's lower 58%.** All 2,183 Neuropixels 1.0 templates: median 184.2 µV, none below 50, **42% above 200**. The CA1 sixteen run 105 to 487 µV, median 158, four above 200. Nobody is excluded — the caliper screens rather than filters — but rescaling is not a light touch, and because the CA1 median sits *below* the pool median, region-matched templates get scaled **up** on average relative to their region-unaware partners. Post-rescaling amplitude is a matched covariate, so this is not a residual confound after matching; the *scale factors themselves* differ systematically between arms, which is something Codex's balance gate may want declared rather than inherited.

### A negative result, recorded so nobody repeats it

The obvious way to compare the two columns is to match library templates to file units. It does not work. The consolidated metadata carries no unit identifier, only a position, and the hypothesis that template order follows the file's unit order scores **at chance** (0.000–0.023) under both definitions of a good cluster, across all four dataset×probe pairings. Recovering identity needs the zarr store's own `unit_ids`, which is a separate reader. I rebuilt the measurement so it does not need the pairing at all — which is why there is a result despite the failure.

## 4. Challenges, and how they went

**A cross-check fired and it was not a bug.** My first version treated disagreement between my best channel and the file's `max_electrode` as a fatal integrity error. It fired on the first unit. Rather than loosen the check to make the script run, I measured the disagreement rate across all 1,821 units and against three different criteria. It is a real difference between two definitions — finding (2) above. The check became a reported diagnostic plus a sensitivity computation at both channels, so the result no longer depends on which rule is right.

**The first design of the whole script was wrong.** I built it around matching donor templates to host units by order. That failed at chance, and the failure was informative but not useful. The rewrite — evaluate the donor *definition* on host data using the file's own mean waveforms — is strictly better: exact unit identity, no assumption to validate, and it works on any session rather than only donor sessions. The failed approach is documented in the artifact so a later session does not spend the same hour.

## 5. Files created or updated

| Path | What changed |
|---|---|
| `Claim Sheet.md` | Amendment 4 → `In force`; Amendment 3 point 1 rewritten to fix the selection rule now, with the directional argument stated. → `3d9fd72b…` |
| `Accessible Claim Sheet.md` | Both changes mirrored in plain language. → `a5cf71b7…` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 5: §1–§10 same-state approved by both agents; new **§11** (the amplitude-convention check). → `7c4b911d…` |
| `Reproducibility Packet/scripts/audit_amplitude_conventions.py` | **New.** argparse, docstrings, no hard-coded paths, metadata-only. |
| `Reproducibility Packet/results/amplitude_conventions.txt` / `.json` | **New.** The report and its raw records. |
| `agents/Claude/references.md` | New entries for the upstream build scripts (pinned commit, six specific findings) and for this project's own measurement; new corrections-log row for the Session 7 amplitude claim. |
| `chats/Claude-Codex/Tier A Selection Review/…Active.md` | Session 8 turn appended. |
| `README.md` (Live-Run) | One running-log entry. |
| `agents/Claude/README.md`, `Summary of Only Necessary Context.md` | Updated / rewritten for the next session. |

## 6. Machine state

Measured directly rather than inherited. **2026-08-12 12:07 PDT: RAM 15.53 GiB free of 31.67 (50% in use); VRAM 810 MiB used of 16,311.** The session's only remote work was metadata: 43.5 MB in 42 range requests, plus a handful of small exploratory reads. No heavy step was taken and none was needed.

## 7. Next steps

1. **Codex's exact-state review of Amendment 3** as edited. If it approves, both sheets flip in the same session. If it prefers a different objective, I take its version — the point I am defending is that the rule is fixed now, not that it is mine.
2. **The CCF label map remains incomplete** — 296 unmapped host structure names, 650 undefined donor acronyms. Irrelevant to a CA1 search, blocking for the region-unaware arm's placement. It needs an Allen ontology and the licences must be read before anything is downloaded. This is now the largest thing on my list that nobody is doing.
3. **The packet still owes its own `requirements.txt`, `.gitignore` and runbook README**, and `audit_template_library.py` still duplicates `utils/template_metadata.py`.
4. **The preprocessing half of the amplitude question is untouched** and is not metadata-answerable: donor averages are built on a 1 Hz highpass plus common median reference over the last 30 minutes, while the host column is IBL's number on IBL's own preprocessing. Measuring that needs the stack installed, which is Rung 0.

**A progress report for the director accompanies this session** — Session 8 is a count-based trigger, and this session also wrote the approving turn on an amendment, which is a second trigger. `agents/Claude/Progress Reports/Progress Report Session 8.md`.
