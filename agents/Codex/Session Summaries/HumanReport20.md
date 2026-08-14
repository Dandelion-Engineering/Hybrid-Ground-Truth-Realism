# Human Report 20 — Codex

**Date and time:** 2026-08-14 02:22 PDT
**Phase:** 2 — Execution
**Session type:** Exact-state review and pre-measurement repair of Claude Draft 14; no candidate measurement

---

## Summary

This session completed Codex's reviewer pass over Claude Session 20. I verified the handed-back Draft 14 digest before review and accepted its correction to the null-language boundary, its estimator status, and the already approved implementation state. I could not approve its two new input-confirmation rules.

The endpoint-containment rule cannot identify an unknown clock: first and last spikes need not reach the recording boundaries, and a time compression shorter than one 60-second bin can still move spikes across internal bin boundaries while preserving the total bin count. The proposed coordinate rule had the same inferential shape: a near-zero median residual does not establish that two coordinate systems share scale, shape or band-edge membership.

I repaired both rules before any candidate value was read. First-party conversion provenance pins raw AP timestamps and processed spike times to session time, so the grid begins at session `t = 0` and its extent is `t_last_s`; endpoint containment remains a sanity check, not a clock chooser. Unit membership now uses the finite `rel_y` of each unit's valid same-probe `max_electrode`, exactly as the earlier injection-placement screen did. Per-spike tip distances supply only within-unit depth differences and therefore cannot move the anatomical band.

**I explicitly approve Draft 15 at SHA-256 `3f25a707301c115a6e451721a85ac1c3dc598755e19d8c40b5131591001b7b38` and handed it to Claude for genuine owner re-review.** Section 16 remains open. No archive-reading CLI may be built against Draft 14, and no candidate may be read until the exact-state loop closes.

No host, candidate drift value, target manifest, donor, dependency, raw recording, generator, Rung 0 or sorter was opened or run. There is still no scientific result.

---

## What was accomplished

### 1. Startup gates and context

- Read the automation memory first, then `.agent-turn`; it named `Codex`.
- Confirmed `.agent-session.lock` was absent, created it, and re-read `.agent-turn`; it still named `Codex`.
- Read `AgentPrompt.md`, all of `Project Details/Project Details.md`, Codex continuity, all concluded chat summaries involving Codex, and the full 1,107-line active Tier A selection transcript.
- Read `Playbooks/review-cycle.md`, `Playbooks/live-run-readme.md`, Claude's `HumanReport20.md`, the complete Claim Sheet, and Draft 14 whole rather than as a diff.
- Verified the worktree began clean at Claude's pushed commit `d81eaa7`.

### 2. Draft 14 exact-state review

The handed-off file matched Claude's declared SHA-256 `3b0f89d222f2d3f3a1ce4e904123bbb110cd726ff10f7621010bec6766cdb775`.

Draft 14 correctly repaired the §16.5 wording: above the observed excursion gate, `Q95_null` can change the published failure reason but not the rejection; below it, null scale can change the verdict. It also correctly retained the same-state-approved estimator and harness and kept the archive reader unbuilt.

Two new rules failed review:

1. **Containment is a consistency condition, not clock identification.** Earliest and latest spikes can lie anywhere inside a recording. One or both candidate intervals can therefore contain a clock with the wrong origin or scale. Equal `n_bins` is insufficient because internal boundary assignments can change even when the total bin count does not.
2. **A median residual is not coordinate equivalence.** A depth residual distribution can have median near zero while differing in scale, slope or tails. Those differences can alter which units fall inside either band edge, and merely reporting the IQR does not gate that exposure.

### 3. First-party source resolution

The official DANDI 000409 record identifies `catalystneuro/IBL-to-nwb` as the conversion repository. At pinned repository commit `54030ac4eb40a74978ac1f6ef6e966278b9d3f34`:

- the raw converter aligns AP samples using `SpikeSortingLoader.samples2times`;
- the sorting export preserves IBL `spikes.times`;
- the sorting documentation defines `spike_times` as seconds from session start;
- unit `max_electrode` maps into the electrode table, whose `rel_y` is already the project's pinned anatomical band coordinate.

The source ledger now records the exact documentation and raw-alignment links. No candidate asset or candidate measurement was read to settle the rule.

### 4. Draft 15 direct repair

Draft 15 makes four bounded changes:

- pins the grid anchor at session zero and its extent at `t_last_s`;
- forbids treating `duration_s = t_last_s - t_first_s` as an alternative clock hypothesis;
- requires exact-asset conversion provenance and `[t_first_s, t_last_s]` containment as sanity checks, with a mismatch treated as an input error that pauses the pinned order;
- selects band units through valid same-probe `max_electrode -> rel_y` and uses per-spike tip distance only for centred within-unit displacement.

No threshold, relaxation, candidate order, permutation rule, statistic, null rule or approved estimator byte changed. The repair changes the unit-selection rule before measurement, which is why it requires Claude's owner review on the exact Draft 15 bytes.

### 5. Validation and collaboration record

- `probe_band_drift_claims.py`: **3 of 3 probes passed**.
- `test_band_drift.py --permutations 200`: **57 checks, 0 failed**.
- `check_runbook_consistency.py`: **10 of 10 steps agree** with their script interfaces.
- `git diff --check`: clean.
- Appended the block-and-repair decision to the active Tier A selection transcript. Its prior 157,859 bytes retained SHA-256 `e7040e6f1ebe4d94735faee50494c8062af1df506539ffdff13ae5154a410daf`; exactly one Codex Session 20 header appears after the old 1,107-line boundary; the old prefix is byte-identical; and the strict UTF-8 LF tail is intact.
- Appended a forward correction to the public root README. It replaces neither earlier entry nor the live-state boundary: Draft 15 remains pre-measurement governance, not a result.

---

## Challenges and how they were handled

**The proposed fallback sounded conservative but could silently change the statistic.** A compressed clock does not have to create empty final bins; it can simply move events across internal bin edges. Testing the claim against the actual binning operation exposed the gap.

**The tracked archive description did not name the spike-time origin.** Rather than invent a tolerance or inspect a candidate, I followed the DANDI record to its official conversion repository and pinned the converter's own session-time semantics. Asset-level provenance remains mandatory because repository documentation is not permission to assume a malformed asset conforms.

**The first validation command omitted a required argument.** `probe_band_drift_claims.py` exited immediately because `--module` was absent and changed nothing. I reran it against the approved `band_drift.py`; all three probes passed.

---

## Files created or updated

| Path | Change |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 15 clock and band-membership repair; exact-state approval and owner handoff. |
| `agents/Codex/references.md` | Pinned DANDI conversion, sorting-time and raw-alignment provenance. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only Draft 14 block and Draft 15 handoff. |
| `README.md` | Append-only public forward correction; no-result boundary retained. |
| `agents/Codex/Session Summaries/HumanReport20.md` | This report. |
| `agents/Codex/README.md` | Workspace map and active-state routing refreshed. |
| `agents/Codex/Summary of Only Necessary Context.md` | Rewritten for Codex Session 21. |

No count- or event-triggered progress report was due. The next count-based report remains Codex Session 24.

---

## Next steps

1. Claude must genuinely owner-re-review Draft 15 `3f25a707…`. No candidate is read while §16 remains open.
2. After same-state approval, build and review the archive-reading drift CLI. It must validate ragged time/depth alignment, finite values, exact-asset session-clock provenance and containment, and valid same-probe `max_electrode -> rel_y` mappings before computing.
3. Only after the executable state is approved may the pinned rank-1 host be measured on drift.
4. The schedule/placement specification, matcher implementation/tests, noise/effective-SNR gates, joint placement gate, exact host-dependent configuration, independent balance/manipulation approval, generation, Rung 0 and sorter execution remain separate gates.
