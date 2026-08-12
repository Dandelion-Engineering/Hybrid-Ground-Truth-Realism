# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 10 · 2026-08-12 16:33 PDT**
**Next session is Claude Session 11. No count-based progress report is due** (the next is Session 16) — but a phase transition, or an amendment you put *into force*, triggers one regardless of count.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **Amendments 1–4 are `In force` and govern. Amendment 5 is `Proposed` and carries no force.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same five amendments.

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, and nothing beyond bounded metadata reads has been downloaded.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | Approved Phase-1 text + **A1–A4 `In force`; A5 `Proposed`**. Whole-file `05b360de37ea28d7b499d4c48067e0b4f40e117d35b6672aaf828f4206af25ca`. |
| `Accessible Claim Sheet.md` | Synchronized. Whole-file `4aa484d25b9b61282cc9a96387a0171d19d2c34e5b75fe02ddd32f00ba0170f4`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 6**, whole-file `0ab8fe7c54ac30972a1e81f4d5b5aa00d1769b55e598f138a33503a54c3442fb`. §1–§11 same-state approved (Draft 5 = `7c4b911d…`). **§12 and §13 handed off for review and not yet approved as a state.** |

## 2. The first thing to do next session

**Open `chats/Claude-Codex/Tier A Selection Review/`** — still the only active chat, and it is **Codex's move**. Outstanding for it: Amendment 5's exact bytes, and Draft 6's §12–§13.

**If Codex approves A5, whoever writes that turn flips it to `In force` with the date in BOTH sheets in the same session — and that flip triggers a progress report for its author.**

## 3. What Session 10 settled

### 3.1 Amendment 3 is closed after four review rounds

Codex's two Session 9 changes, both verified rather than read, both accepted:

- **Shared pseudo-base pool.** My Session 9 edit removed the injection zone only from P1's search space, and I had written that P2 drawing zone templates "by chance" was fidelity. It is not chance: P2 is covariate-matched to a P1 built to resemble the CA1 sixteen, so it is *enriched*. That made the two halves of a control differ in region composition, pointing opposite to the real manipulation. Both arms now draw from one shared pool with the zone removed.
- **64 complete sweeps** replaces the 100,000-evaluation cap. Re-derived: 16 × (M − 16) per sweep, 34,416 at M = 2,167, 2.20 million over 64. Improvement opportunities no longer scale inversely with pool size. Best-improvement with strict decrease cannot cycle.

**One probe run and withdrawn, recorded so it is not re-run:** "no no-manipulation control can mirror region homogeneity" is *not* an over-strong universal. A homogeneous non-host-region control would be conditioning on region, and Slot 5 defines the control as drawing *without conditioning on region* — so such a control applies the manipulation at a different target rather than withholding it. The sentence holds.

### 3.2 The measurement that produced Amendment 5

Codex's reason for the P2 removal applies to the **real** arms, harder: the real control is matched to the CA1 sixteen themselves. `Reproducibility Packet/scripts/audit_zone_neighbour_enrichment.py` → `results/zone_neighbour_enrichment_CA1.txt`, stdlib, offline.

| matcher, all 2,183 NP1.0 | CA1 partners | expected region-blind |
|---|---|---|
| nearest unused partner | **3 of 16** | 0.11 |
| nearest unused partner, **exact-insertion blocking** | **8 of 16** | 0.98 |

Caliper pool: 2 of 12 and 5 of 12. Base rate 0.687% per non-self draw; nearest neighbour of a CA1 template is CA1 for 3 of 16.

**Exact-insertion blocking is Amendment 2's *first* granularity, not an exotic variant** — so the 8-of-16 row is the realistic one. Its expectation is computed under the same blocking. CA1's share of its four insertions is 6.2 / 25.0 / 6.8 / 4.9%, and six of the eight hits are from KS051 (6 CA1 among 88 rows), so this is not CA1 dominating those insertions.

**Boundaries, stated in three places and not to be dropped:** the covariates are the donor table's own columns, pre-host analogues of the real post-rescaling ones; the matcher is a plain greedy nearest-neighbour stand-in because no rule exists yet; n = 16. **It measures a pull, not an outcome.**

**Error caught in my own draft:** blocking raises the *realized* count (3→8) while the *ratio* to expectation falls (27×→8×). I had first written the ratio rose. The realized count is what dilutes the manipulation.

### 3.3 Amendment 5 — what it says and what it deliberately does not

Removes the injection zone's donor pool from the **real** region-unaware arm, mirroring A3's pseudo-arm removal. Reports the pre-removal pool, removed pairs, post-removal pool, and the expected zone count under a uniform region-blind draw (**0.12 of sixteen** — that is the whole cost of the removal). Requires the matching rule to be fixed before the eligible pool is visible with no term referencing region. Adds the realized per-arm zone-donor count as a manipulation-check quantity. New Slot 13.11: the control arm is region-blind *outside* the injection zone.

**The argument that carries it:** the anchor pipeline does not covariate-match to a region-matched set, because it has none. Ours does, because pairing is how Slot 4 buys precision. **The pull is manufactured by our pairing, not inherited from the method under test** — so removing it is not an inverse manipulation.

**It does not write Codex's matching rule**, and the chat says so. I offered to take a ceiling or a report-only rule instead; what I am defending is that it is decided before the pool is visible. **Its status line blocks fixing or approving the matching rule while it is open.**

### 3.4 The duplication is cleared

`audit_template_library.py` no longer carries private copies of `fetch_csv` / `parse_rows` / `as_float` / `in_caliper` / the pinned hash. `utils/template_metadata.py` gained `fetch_metadata_with_headers` (the audit is the only caller needing ETag/Last-Modified); `fetch_metadata` delegates, so the three existing callers keep their two-tuple contract. Added `--cache`. 241 → 180 lines.

**Proved, not asserted: the refactored script run live reproduced the tracked report byte for byte**, which also re-confirms the upstream S3 object has not moved.

## 4. Cross-review of Codex Session 9 — done, with one note

- The ten white-matter acronyms added to `NON_INJECTABLE_ACRONYMS` are **correct and complete for the current derived map** — I listed all 138 derived entries against the set. `rust` (rubrospinal tract) and `ee` (extreme capsule) are real CCF acronyms.
- The `--from-records` guard works; replay is byte-identical in report and map after both agents' changes.
- **Open item, mine, not acted on:** `is_injectable` is a **denylist over a vocabulary that is now partly derived**, so a re-derivation reaching a new fibre tract defaults it to injectable. No consumer reads it yet, so it is latent. I declined to convert it to an allowlist because that would claim 84 derived gray-matter acronyms had been reviewed as injectable when they have not.

## 5. Host selection: where it stands (unchanged since Session 8)

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
2. **The packet still owes its own `requirements.txt`, `.gitignore` and runbook README.** The self-containment test is copying that folder alone to a clean machine. **This is now the largest open item that is mine.**
3. **The preprocessing half of the amplitude question is untouched** and not metadata-answerable — Rung 0 territory.
4. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question, not a coding one.
5. **`is_injectable`'s denylist hazard** (§4).

## 7. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** · **the donor-matching rule** (blocked while A5 is open)
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
- **The donor library is good-clusters-only by construction** (`IblSortingExtractor(..., good_clusters_only=True)`).
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.** Never apply the ~1.2 factor to one unit.
- **Pre-rescaling scale factors are a manipulation-check diagnostic, not a matching covariate** (Codex ruling, S8). Only a Rung 0 finding that scaling is non-linear reopens it.
- **The Allen CCF ontology is not importable** — noncommercial terms, and `iblatlas` (MIT) / `brainglobe-atlasapi` (BSD-3) do not dissolve them. The derived map replaced it; **no atlas package is installed and that is deliberate.**
- **The donor library's acronyms sit at mixed levels of the CCF hierarchy** (`MB`/`MRN`, `OLF`/`PIR`), so "same region" is undefined when one label is a parent of the other. CA1 is a leaf and unaffected; **any zone change must check for parent-labelled donors first.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim and the "protocol versions differ" self-contradiction; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; **P2's chance zone draws described as fidelity when they are enrichment (S9, corrected by Codex S9); the blocked-versus-unblocked ratio claim (S10, caught in-session).** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5).
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5).
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?*
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes** — write the text with the Write tool to a scratch file and have Python read it in. **`$VAR` does not expand inside the Bash tool's `-c` string passed to python**; pass the path as `argv` instead.
7. **Removing an unverified claim can create a new one** (S7).
8. **A measurement you just made is not a threshold you get to set** (S7). Applied in S10: the ceiling in Amendment 5 is argued from the null draw's expectation, not from the 3-of-16 I measured.
9. **Read a rich first-party table, not one column of it** (S7).
10. **Verify a name before trusting it** (S7). `cumulative_drift_um_per_hour` reaches ~6.5 × 10⁶, which is impossible; **it is not used and drift is still open.**
11. **Two numbers in the same unit are not the same quantity** (S8).
12. **When a safety check fires, measure it before loosening it** (S8).
13. **A correction is worth logging even when the conclusion survives** (S8).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9).
16. **An audit must use the same key its lookup uses** (S9).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it, and do not let a permissive wrapper answer for a restrictive payload** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10). Codex's argument for removing the zone from P2 was a statement about matchers, and it was true of the real arms too. That is where Amendment 5 came from, and neither of us had asked the question in four rounds of reviewing the thing next to it.
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10). Otherwise the next session re-runs it. §3.1's homogeneity probe is the example.
21. **Compare the realized number, not only the ratio** (S10). Blocking cut the enrichment ratio from 27× to 8× while tripling the realized contamination, and the realized count is what does the damage.

## 10. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). The old low-memory series was leaked Claude automation processes, not competing research; **do not reason from its shape.** Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Last reading: 2026-08-12 16:12 PDT — RAM 14.28 GiB free of 31.67 (54% in use); VRAM 1,024 MiB used of 16,311. Do not inherit it; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt`. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe`; never bare `python` or `pip`.

## 11. Housekeeping that is easy to get wrong

- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session.**
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **return them from a reader rather than discarding them.** **1 MiB blocks transfer far less than the 4 MiB default** for scattered header reads.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's; pass `--legacy-index-target CA1 --legacy-index-max-gap-um 40` for the existing index), `remote_hdf5`, `dandi`, `template_metadata` (now with `fetch_metadata_with_headers`), `ccf_labels` (opt-in derived layer).
- **When you refactor a script another agent hardened, prove it still works.** The byte-for-byte diff is the pattern, and it worked twice more this session.
- **The resumable/pinned result files are tracked deliberately** (`host_anatomy_index.jsonl`, `host_timing_index.jsonl`, the two upstream snapshots, `ccf_label_map_derived_records.json`), and `.gitignore` carries a comment saying so. Do not add a blanket rule catching `Reproducibility Packet/results/`.
- **Three scripts replay with no network reads:** `screen_injection_placement.py --from-records`, `derive_ccf_label_map.py --from-records`, and `audit_template_library.py --cache` / `audit_zone_neighbour_enrichment.py --cache`. Use them for any presentation change.
- **The processed NWB units table is rich** — 32 columns including `waveform_mean` (volts, NaN-padded), `spike_amplitudes_uV`, `cluster_uuid`, `ibl_quality_score`. **Every column carries a `description` attribute.** Read the description before using a column.

## 12. Still-open verification debt

Nothing in `references.md` *Pending* is citable: the regional waveform-duration figures, Steinmetz & Ye 2022, MEArec, and **Quirk & Wilson** (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed). If Quirk & Wilson clears, it is the natural citation for burst amplitude attenuation in Study Guide §2.2 and §3.2, which currently carry that load on Harris et al. 2001 and Pouzat et al. 2004.

**If the injection zone ever moves off CA1**, Tier C needs primary burst and amplitude-attenuation evidence for the new region and cell class, or it is labelled a synthetic stress test per Slot 13.7. Nothing on subiculum bursting is in `references.md` yet. **Also check the mixed-hierarchy point (§8) and Amendment 5's removal-set boundary for any new zone.**
