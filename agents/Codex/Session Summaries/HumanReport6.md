# Human Report 6 — Codex

**Date and time:** 2026-08-11 22:13 PDT

**Session:** Codex Session 6

**Phase at start:** Phase 2 — Execution

**Phase at end:** Phase 2 — Execution. Claim Sheet Amendment 1 is in force; Amendment 2 remains proposed pending Claude's owner re-review; the Tier A selection strategy is same-state approved for its declared scope; no host is pinned and no sorter has run.

---

## Summary

This session resolved the open Tier A negative-control disagreement, approved the project's first Claim Sheet amendment, corrected two unsupported provenance statements before they became contract facts, fixed a resumable-index configuration hazard, and verified the injection/preprocessing order against SpikeInterface 0.104.8 source.

The most important scientific-design decision is that **Claude's no-manipulation counter-proposal is accepted and Codex's replicate-stability proposal is withdrawn**. A repeated real contrast could reproduce a systematic selection artifact and make a false interaction look stable. The accepted construction instead compares a fixed sixteen-template subset of the region-unaware pool against the full region-unaware pool, with neither arm conditioned on region. It mirrors the real design's finite-versus-large-pool asymmetry, donor reuse, matching, clustering, and seeds while retaining the original safety question: how much interaction can the procedure manufacture when the realism property did not change?

That construction still needs a Claim Sheet amendment. Slot 5 currently says pseudo-arms use the same selection and generation procedure, while the accepted P1/P2 design deliberately uses asymmetric pool construction. I requested synchronized Amendment 3 before any Tier A generation, including a pinned subset-selection seed and objective, exposed template identifiers, the exposure-balanced rota, the real-arm matching procedure, the no-region-conditioning rule, unchanged sorter budget, and the region-homogeneity boundary.

## Exact-state decisions

### Tier A selection artifact

Claude's owner re-review state is:

`agents/Claude/Tier A Host and Injection Zone Selection.md`

SHA-256 `3ae39913986a1961d674d2ed7b4714f89293fa6f0e8c02f039ebca3c186696cf`

**I explicitly approve those exact bytes for the artifact's declared scope:** a host-selection strategy, CA1 injection-zone recommendation, and discharged duration gate. It is not a pinned-host selection. The negative-control construction remains governed by the Claim Sheet rather than by this selection artifact.

### Amendment 1 — compute environment

Amendment 1 passed exact review and is now `In force` in both Claim Sheets as of 2026-08-11. It records the director's daytime/overnight allocation and corrects the earlier low-memory causal story while preserving every live admission guard and every capacity/scientific commitment.

The compute-environment chat was concluded with a summary after explicit approval. No later machine measurement belongs there; Rung 0 owns it.

### Amendment 2 — provenance and the finite CA1 pool

The substance passes, but exact-state owner re-review remains open. I removed two claims not established by the evidence ledger:

- technical: “one mouse strain”; and
- Accessible: “same rig design” and “same mouse strain.”

Both versions now state the verified residual boundary: host and donor share one dandiset/public collection, consortium, IBL acquisition program, and Neuropixels 1.0 probe type. Subject separation still does not make the sources independent.

The synchronized whole-file states I approved and handed back are:

- `Claim Sheet.md`: SHA-256 `8d06e5887e61b84a3ac7de71e6dcdd2eff9cbea070482faa066df109982dbfc7`
- `Accessible Claim Sheet.md`: SHA-256 `9bb0478f39711404730efbb96e6a7b6fdc711c4dc69a6d217438d032657a8c1a`

Amendment 1 is in force inside those files; Amendment 2 remains `Proposed` until Claude genuinely re-reviews the exact bytes.

## Verification performed

### Timing evidence reproduced

The tracked timing index independently yields:

- 11 candidate assets;
- 21 AP series;
- duration range 54.1527–87.0831 minutes;
- measured rate range 29,999.9969–30,000.2984 Hz;
- 384 channels for every series;
- 317,309,738 metadata bytes recorded; and
- zero non-monotonic head/tail timestamp windows.

This supports Claude's duration result at its stated boundary. It shows a regular usable time base and adequate duration; it does not prove no samples were dropped, and it says nothing about drift, noise, effective SNR, placement feasibility, or covariate balance.

### Resumable-index target hazard fixed

`screen_host_timing.py` accepted a `--target` label but selected candidates from a stored `target_band` without proving that the anatomy index was built for that label. `survey_host_anatomy.py` had the deeper form of the same problem: resuming a CA1 index with a different `--target` would reuse prior bands and print the new label. That could silently produce a plausible but mislabeled report.

I added `utils/anatomy_index.py` and changed both scripts so new records embed their target and maximum-gap configuration. The existing append-only CA1/40 µm index is treated as legacy and requires explicit `--legacy-index-target CA1 --legacy-index-max-gap-um 40` assertions. A mismatched CA1→SUB replay now fails loudly before reporting.

Validation completed:

- all three changed Python sources compiled under the project venv;
- the configuration helper accepted matching current and legacy records;
- the helper rejected a mismatched target;
- the actual tracked timing replay found 11 already-timed candidates and performed zero new remote reads; and
- the replay reproduced the 317.3 MB metadata total and zero failures.

### Injection ordering verified against the pinned-version candidate

Claude warned that donor templates were already phase-shifted before extraction, so injecting them into a raw host and phase-shifting the combined recording would transform injected spikes twice and real host spikes once.

I verified the warning against first-party source:

- SpikeInterface tag `0.104.8`, commit `76c41846f88de3cc9dc5858d5c7f97dd6cb1955f`, passes the caller-supplied recording directly into `InjectTemplatesRecording` or `InjectDriftingTemplatesRecording`; `generate_hybrid_recording()` does not preprocess it.
- `hybrid_template_library/python/upload_ibl_templates.py` builds donor templates after float conversion → Neuropixels `phase_shift` → 1 Hz high-pass → common reference.
- The official SpikeInterface hybrid tutorial passes a preprocessed host into the generator.

The consequence for Rung 0 is now explicit: construct and pin the host injection substrate before injection. Do not assume the generator applies preprocessing, and do not phase-shift the raw-host-plus-injected mixture after adding already-phase-shifted donors. Codex's reference ledger records the version, tag commit, source path, and decision.

## Amendment 1 progress report

Approving a Claim Sheet amendment is an event trigger under the project framework, so this session also created:

`agents/Codex/Progress Reports/Progress Report Amendment Compute Schedule.md`

It explains for the director, without technical shorthand, what the memory explanation got wrong, what the daytime/overnight convention changes, what remains unsafe to assume, and why no experiment scale or result rule moved.

## Public log heartbeat

The root Live-Run README required a forward correction because an earlier append-only entry still said host and donor shared one rig design, which the evidence never established. A new lean Phase 2 entry removes rig/strain from the verified limitation, records convergence on the no-manipulation control, records the 0.104.8 injection-order decision, and states that no sorter or scientific result exists. Earlier entries were not rewritten.

## Challenges and reasoning paths

**The safety check had to keep its failure target.** My prior replicate-stability proposal mirrored the real pools but answered whether the interaction reproduced. Claude's counter showed that reproducibility is not enough when the feared failure is systematic: a stable artifact is still an artifact. The accepted control keeps “nothing changed” true while recreating the structural asymmetry that could generate a false interaction.

**A good counter-proposal still needed contract treatment.** The counter satisfies the intended no-region-manipulation meaning, but it does not satisfy the existing literal phrase “same selection procedure.” Treating that as implementation detail would make execution silently diverge from the pre-registered contract. Amendment 3 is the smallest honest fix.

**Exact-state approval and status are different operations.** Amendment 1's text passed and its status was flipped to `In force` in both sheets in the same work unit. Amendment 2 was edited and approved by the reviewer, but it remains proposed because Claude must re-open the exact new bytes. The whole-file hashes make those two states auditable even though both amendments share one file.

**A CLI argument can be more dangerous than a hard-coded value.** The timing script appeared flexible because it accepted `--target`; that flexibility was false because the index did not carry the query that generated `target_band`. Making the legacy assumption explicit is safer than allowing a portable-looking command to mislabel data.

## Files created or updated

| Path | Change |
|---|---|
| `Claim Sheet.md` | Amendment 1 marked `In force`; Amendment 2 residual boundary narrowed; reviewer-approved whole state `8d06e588…`; Amendment 2 owner re-review open. |
| `Accessible Claim Sheet.md` | Synchronized status and residual-boundary correction; reviewer-approved whole state `9bb0478f…`. |
| `Reproducibility Packet/scripts/utils/anatomy_index.py` | New shared validator for anatomy-index target/gap provenance. |
| `Reproducibility Packet/scripts/utils/__init__.py` | Documented the new shared module. |
| `Reproducibility Packet/scripts/survey_host_anatomy.py` | New records embed target/gap provenance; legacy resumes require explicit assertions. |
| `Reproducibility Packet/scripts/screen_host_timing.py` | Validates anatomy-index provenance before selecting candidates and reports the anatomy gap. |
| `Reproducibility Packet/results/host_timing_CA1.txt` | Regenerated with the validated 40 µm anatomy-gap provenance shown in the report header; zero new remote reads. |
| `agents/Codex/references.md` | Recorded SpikeInterface 0.104.8 injection behavior, tag commit, donor preprocessing chain, and Rung 0 implication. |
| `agents/Claude/references.md` | Marked the broad residual-boundary claim superseded and appended the verified boundary. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only response accepting the counter-proposal, approving the selection artifact, handing back Amendment 2, and requesting Amendment 3. |
| `chats/Claude-Codex/Compute Environment Update/Compute Environment Update - Concluded.md` | Appended exact Amendment 1 approval and concluded the resolved transcript. |
| `chats/Claude-Codex/Compute Environment Update/Summary.md` | New concise concluded-chat summary. |
| `README.md` | Appended a public forward correction and pre-execution design update. |
| `agents/Codex/Progress Reports/Progress Report Amendment Compute Schedule.md` | New amendment-triggered director progress report. |
| `agents/Codex/Session Summaries/HumanReport6.md` | This report. |

Codex's `README.md` and `Summary of Only Necessary Context.md` are refreshed after this report as required by closeout.

## Resource and execution boundary

No sorter, generator, raw-recording download, dependency installation, or heavy compute ran. The only network reads were small first-party source pages and a `git ls-remote` tag lookup. The timing replay used the existing local indexes and made zero new NWB requests. Because no heavy step was launched, no RAM/VRAM admission measurement was inherited or used.

## Next steps

1. Claude genuinely re-reviews the exact Amendment 2 whole-file states above and either approves them or edits and returns new synchronized hashes.
2. Claude authors synchronized Amendment 3 for the accepted Tier A no-manipulation pseudo-control; Codex exact-state review remains required before generation.
3. Claude continues the first-admissible host path through drift, noise, effective-SNR, placement, and balance gates; no wider anatomy census unless current candidates fail.
4. Codex prepares Rung 0 with SpikeInterface 0.104.8/tag provenance, a pinned pre-injection host substrate, exact candidate sorter commands, and live resource monitoring.
5. Rung 0 starts only during the daytime window and only after fresh RAM/VRAM measurements pass every existing guard.
