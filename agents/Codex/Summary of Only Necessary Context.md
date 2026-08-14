# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 20 · 2026-08-14 02:25 PDT**

**Next Codex session will be Session 21.** No count-based progress report is due; the next cadence report is Session 24.

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, rendered edge table, schedule, selected donor, template-array pull, dependency installation, raw-recording read, Rung 0, hybrid generation or sorter run occurred in Codex Session 20.

The public state remains `In Progress`. The host order, drift specification, donor-matching prose, synthetic estimator and repository-distribution policy are pre-measurement governance/implementation, not evidence about whether realism changes sorter accuracy.

## Contract state — Amendments 1–6 are in force

Current synchronized hashes remain:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

Amendment 6 governs Tier A: Z is the full sixteen-key zone universe; one finite donor-level site set and per-site predicates produce T/K once; `N = count(T)` continues for `10 <= N <= 16`; the `1910753866` digest deal assigns fifty occurrences across five ten-distinct-target blocks; joint block-placement failure rejects the host without shrinking T; controls and pseudo-arms follow N while removal stays at full Z.

## Real-arm matching rule — prose closed, implementation absent

Artifact: `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`

Same-state-approved Draft 6 SHA-256:

`51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`

The rule fixes one target manifest, T/K/N once, full-sixteen Z removal, common U-derived scaling, donor-equal cost, deterministic global no-reuse assignment, insertion → session → subject → unrestricted provenance stages, exact count equality before the literal fallback floor, complete outputs and loud failure semantics. Before any real target manifest, host-specific pool or edge table, the separate exposure-schedule/placement specification and matcher implementation/tests must receive same-state approval on synthetic inputs.

## Host order — same-state approved

Artifact: `agents/Claude/Tier A Host and Injection Zone Selection.md`

Section 15 is same-state approved. The pinned order begins:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Ranks 4–13 remain the declared table order. Strict admission evaluates ranks 1–13 sequentially under the 20 µm drift rule and every later gate. If none is fully admissible, the same order restarts once under 40 µm; only then does the tracked asset-cache continuation begin in cached discovery order. No candidate has been measured on any open gate.

## Drift implementation — same-state approved and closed

Both agents approve:

- `Reproducibility Packet/scripts/utils/band_drift.py`: `d8b035968416b335d7ef1bdd0d915c03aec4a64649defa8795c8c013fc70c069`
- `agents/Claude/tools/test_band_drift.py`: `82aaf77e99f20b158a54b6acfc848fc2626047aa350bebd8b3bd988b7ce48f03`
- `agents/Claude/tools/probe_band_drift_claims.py`: `4f3b83773156e7f9654f3e080d5adb258658cf500cf741aaea04b5015f07c34f`

The module implements complete 60-second bins, median-centred per-unit traces, the band median, `Delta_full`, worst-ten-bin `Delta_10`, the deterministic 200-permutation within-unit null, nearest-rank 190th-of-200 `Q95_null`, and the two-number gate. It restricts observation and permutation to complete-bin spikes, fails loudly on mismatched collections and malformed row identifiers, and rejects an unmeasurable observation before constructing its null. The harness passes **57 checks, 0 failed** at the pinned 200 permutations; the claim probe passes **3 of 3**.

## Drift Draft 15 — Codex-approved, Claude owner re-review open

Active chat: `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

Codex verified and blocked Claude's Draft 14 `3b0f89d222f2d3f3a1ce4e904123bbb110cd726ff10f7621010bec6766cdb775` unchanged, then directly repaired it. Codex explicitly approves and handed back:

- host-selection Draft 15: `3f25a707301c115a6e451721a85ac1c3dc598755e19d8c40b5131591001b7b38`

Claude must genuinely owner-re-review those exact bytes before any candidate is read. Section 16 remains open meanwhile.

### Why Draft 14 was blocked

1. Its endpoint-containment chooser could not identify an unknown clock. First and last spikes need not occupy recording boundaries, and an affine compression shorter than one bin can still move spikes across internal boundaries while preserving the total bin count.
2. Its coordinate-equivalence check used only the median of `distance_from_probe_tip_um - rel_y`. A near-zero median does not establish matching scale, shape, tails or band-edge membership; reporting the IQR without gating it does not close that exposure.

### Draft 15 rule

First-party conversion provenance now supplies the timebase. DANDI 000409 identifies `catalystneuro/IBL-to-nwb` as the converter. At pinned repository commit `54030ac4eb40a74978ac1f6ef6e966278b9d3f34`, raw AP samples are aligned through `SpikeSortingLoader.samples2times`, the sorting export preserves IBL `spikes.times`, and the sorting documentation defines `spike_times` as seconds from session start.

Therefore:

- the grid anchor is session `t = 0`;
- its extent is raw `t_last_s`;
- `duration_s = t_last_s - t_first_s` is a span, not an alternative clock;
- exact-asset provenance and `[t_first_s, t_last_s]` containment are sanity checks, not a clock-selection method;
- missing or contradictory clock evidence is an input error that pauses the pinned order rather than rejecting the host;
- band units are selected by valid same-probe `max_electrode -> rel_y`, the same anatomical coordinate used by §10;
- per-spike waveform centre-of-mass depths enter only centred within-unit differences, so their absolute offset cannot move the band.

Draft 14's null-language repair is retained. No threshold, 20/40 µm ladder, candidate order, estimator statistic, permutation rule or approved implementation byte changed.

## Repository checkout bytes — closed

Both agents approve `.gitattributes` SHA-256:

`036c696c3e1ea9cef70925ec8dfedc407ef59bb20e5c00e17ef9b5f88855bfa0`

The policy defaults the repository to `* -text`; 17 framework/workspace paths and 11 legacy packet outputs explicitly use `text eol=crlf` to reproduce their tested CRLF working representation. A temporary commit cloned under `core.autocrlf=true` matched **153 of 153** reviewed tracked files byte-for-byte.

## Reproducibility Packet state

The earlier design-stage review remains concluded at:

- packet README `3b07aa5b94203d3f4c826be7aac40e6550c2a13e7d3b45c997399a84af3df4a1`
- checker `4eb9401825ec2a4561abf46dc7dc82d89ea316722d338bba9e84bd747d83c651`
- mutation harness `d64134b1485a8550412c1eb7fba7fd98ab509471050cad71a41fc8f704d5acc3`

The drift utility is a later same-state-approved addition. The archive-reading drift CLI and runbook Step 11 do not exist. The headline experiment and Slot 8 `verify_realism.py` do not exist because no result exists. The ten-step runbook consistency checker passes.

## Separate gates — do not collapse

1. Claude owner re-review of Draft 15;
2. archive-reading drift CLI, its first scoped packet step/review, and candidate measurement down the pinned order;
3. exposure-schedule/placement specification, implementation, synthetic tests and same-state approval;
4. matcher implementation, exhaustive/mutation tests and same-state approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact candidate sites, T/K/N, U/Z/R, edge table, un-removed/post-removal matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. generation authorization;
10. Rung 0/sorter execution authorization.

Reviewer edits, commits, downstream use and silence are not same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. Codex Session 20 appended a forward correction explaining why both Draft 14 confirmations could certify the wrong input, recorded the provenance/`rel_y` repair, and retained the no-result/no-execution boundary.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- No count- or event-triggered progress report was due in Codex Session 20.

## Validation and append-only boundary

- Draft 14's handed-back digest was verified before review.
- The official DANDI conversion repository and pinned first-party clock semantics were checked without reading a candidate asset.
- The full drift harness passes 57/57 checks at 200 permutations; the review probe passes 3/3.
- The packet checker passes all ten current steps.
- `git diff --check` was clean at the reviewed state.
- Chat append used the verified strict-UTF-8 physical tail, pre-write line count 1,107, one unique EOF anchor, exactly one new Session 20 header after the prior count, an unchanged 157,859-byte prefix with SHA-256 `e7040e6f1ebe4d94735faee50494c8062af1df506539ffdff13ae5154a410daf`, and post-write LF-tail checks.
- No heavy work, dependency install, archive read, raw-data read, template pull, Rung 0, generator or sorter run occurred.

`agents/Codex/Session Summaries/HumanReport20.md` contains the full rationale, source trail, file list and validation evidence.
