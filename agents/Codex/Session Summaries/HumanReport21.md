# Human Report 21 — Codex

**Date and time:** 2026-08-14 04:17 PDT
**Phase:** 2 — Execution
**Session type:** Exact-state review of Claude Draft 16; two safety-claim repairs; no candidate measured

---

## Summary

This session completed the required Codex review of Claude's owner-approved Draft 16 of `agents/Claude/Tier A Host and Injection Zone Selection.md`. I accepted the design choices Draft 16 was trying to pin — the label-blind drift-screen unit set, retention and reporting of rank 1's head-undercovered session-grid bin, and reporting of the endpoint-containment margins — but **blocked Draft 16 unchanged** because two one-way safety arguments were false at the level of the already-approved estimator.

The defects were not theoretical objections. I constructed deterministic synthetic inputs and ran the exact packet implementation at its pinned settings:

- Five units carrying the same 30 µm ramp fail the strict 20 µm gate at `Delta_10 = 24.545 µm`, `Q95_null = 11.591 µm`. Adding six flat traces changes the label-blind eleven-unit median and null to `0/0 µm`, which passes. This disproves Draft 16's statement that added weaker units cannot buy a pass because their scatter must widen `Q95_null`.
- A separate seeded fixture gives `Delta_10 = 8.346 µm` after omitting its first bin and `7.966 µm` when that bin is retained. This disproves the statement that retaining the head-undercovered bin can only move the apparent excursion toward rejection.

These fixtures are **counterexamples to prose guarantees, not predictions about any candidate recording**. I retained both pre-measurement design choices, removed the unsupported directional claims, made their conditionality auditable, and handed back **Draft 17** at SHA-256 `709be46fd0f1d23c7677787410419cf63a7ff5a03945bc88bff2c9db625909eb` for Claude's genuine owner re-review.

I also repaired the numeric utility's public interface before an archive reader could encode the wrong field: its public argument and documentation now say session-time `extent_s`, not recording `duration_s`. The code's numerical branches are unchanged. Codex approves the renamed utility state at SHA-256 `b2c016053b18ffb49b0e9e3c439af22a7ea1d6b1b306857fe9d9b9f0eea9ac66`; Claude owner re-review is required before the implementation loop closes again.

**No host was pinned, no candidate drift/noise/effective-SNR value was read, no archive-reading CLI was written, and no raw data, template array, Rung 0, generator or sorter was run. No scientific result exists.**

---

## What was accomplished

### 1. Startup, continuity and context-first chat pass

- Read `.agent-turn` first; it named `Codex`.
- Confirmed `.agent-session.lock` was absent, created it, and re-read `.agent-turn`; it still named `Codex`.
- Read the automation memory and `AgentPrompt.md`.
- Read the full `Project Details/Project Details.md`, Codex's `Summary of Only Necessary Context.md`, every concluded `Summary.md` under `chats/Claude-Codex/`, and the entire 1,178-line active Tier A selection transcript before replying.
- Read `Playbooks/review-cycle.md`, Claude's `HumanReport21.md`, Draft 16 §§15–16 whole, the Draft 15→16 diff, Claude's new reference entries and the public README heartbeat.
- Verified Draft 16's handed-off SHA-256 `7fed750c8f48420521e2038b32285d72d7b719dfd1490c40dbccc14a6e2204ec` before review.
- Confirmed the repository began clean at Claude Session 21 commit `fdca4f7`, with local `HEAD` matching `origin/main`.

### 2. Independent reproduction of Draft 16's cached facts

I re-read the tracked metadata rather than accepting the report's summary:

- `injection_placement_CA1.json` carries thirteen candidate bands with 22–267 total units and 1–60 `good` units; NYU-39 Probe00 carries one `good` unit.
- `host_timing_index.jsonl` carries twenty-one measured AP series. Five are exactly nominal `i / 30000` timestamp arrays, all the CSHL Probe00 candidates at ranks 3, 6, 8, 10 and 11; the other sixteen measured series carry non-zero/fitted alignments, of which eight are the remaining pinned candidate probes.
- Rank 1's Probe01 stream begins at `t_first_s = 1.138489…`, so session-grid bin 0 has 58.86 seconds of AP coverage inside a full 60-second clock interval.

The counts and timing claims were accepted. The defect was the guarantee attached to them.

### 3. Executable counterexamples to the two safety claims

Created `agents/Codex/tools/probe_draft16_safety_claims.py`, SHA-256 `af51fe507be92bcbd0b8b2d7063fcc20e2208f78905b9cceb1d8ef30717bf205`.

The probe:

- imports the exact packet implementation rather than reimplementing the statistic;
- runs the full pinned 200-permutation null for the unit-set fixture;
- asserts that the five moving units fail and the eleven-unit expansion passes;
- uses a fixed NumPy seed to find and assert the head-bin counterexample;
- accepts its project root and threshold through `argparse`, has no hard-coded machine path, and reads no candidate asset.

The first counterexample exposes the specific gap in Draft 16's reasoning: the same-set permutation null preserves a unit set, but it does not guarantee that *changing* the set affects `Delta_10` and `Q95_null` in a pessimistic direction. The across-unit median can be damped by a majority of movement-insensitive traces. This is consistent with §16.5's existing boundary that systematic depth-estimator bias is not bounded.

The second counterexample exposes the same error shape at the bin boundary: fewer samples can increase variance in expectation, but a realized median, centred unit trace and peak-to-peak window have no deterministic monotonic direction under adding or retaining a bin.

### 4. Draft 17 direct repair

Edited the owner artifact under the review-cycle permission and explicitly approved the handed-back state.

Draft 17:

- retains the label-blind unit policy because `kilosort2_label` is a sorter-confidence label, not a direct measurement-support criterion, and making it a filter would covertly reinstate the native-yield gate §10.4 declined;
- states that the result is conditional on movement being expressed in enough label-blind IBL depth traces for the across-unit median to carry it;
- requires total count, `good` count, unit-table row identifiers and stored quality labels for both the in-band and temporally included sets;
- retains the rank-1 head bin as a declared session-grid choice but states that it can move both gate quantities in either direction;
- distinguishes full-width session-grid intervals from complete AP coverage and aligns the bin/permutation terminology throughout §§16.4–16.8;
- calls the containment values **endpoint slack**, not the check's resolution, and states that they do not bound arbitrary internal offset, scale or time-varying disagreement;
- keeps every threshold, candidate rank, permutation seed, window, statistic and verdict rule unchanged.

Final approved artifact state: `709be46fd0f1d23c7677787410419cf63a7ff5a03945bc88bff2c9db625909eb`.

### 5. Utility interface repair

Edited `Reproducibility Packet/scripts/utils/band_drift.py` without changing numerical behavior:

- `complete_bins`, `measure_band_drift` and `permutation_null` now expose `extent_s` rather than `duration_s`;
- docstrings say the value is raw AP `t_last_s` on the session-time grid, not the timing screen's `t_last_s - t_first_s` span;
- the module states that anatomical/quality-label membership is the archive reader's responsibility and that head undercoverage is retained and reported by the predeclared specification;
- the null and invalid-bin descriptions use the analysed session-grid boundary.

The renaming is load-bearing despite being numerically inert: the old argument name invited the future CLI to pass exactly the span Draft 15 had ruled out.

Final Codex-approved utility state: `b2c016053b18ffb49b0e9e3c439af22a7ea1d6b1b306857fe9d9b9f0eea9ac66`.

### 6. Chat and public forward correction

- Appended the Draft 17 verdict and exact-state handoff to `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`.
- Used the strict append safeguard: pre-write 170,082-byte / 1,178-line transcript at SHA-256 `094719b5…`; the prior bytes remained an exact prefix, exactly one Session 21 header appeared after the prior line count, strict UTF-8 decode passed, and the physical tail was re-read.
- Final readback found two surviving terminology-only uses of “complete bin”; I corrected them in the artifact and appended a dated correction rather than editing the chat history. The second pre-write 173,943-byte prefix at SHA-256 `c61f6de7…` also remained byte-exact, with exactly one correction header after line 1,209.
- Appended a forward public README correction. It preserves the label-blind choice but withdraws the false guarantee and keeps the no-result/no-execution boundary explicit.

---

## Challenges, decisions and reasoning

### Why the label-blind set was retained after its guarantee failed

The counterexample proves that label-blind inclusion is not one-way safe; it does not establish that `good`-only filtering is superior. A `good`-only rule would condition the screen on one sorter's confidence label, make rank 9 unmeasurable by construction for the exact yield reason the project declined to gate on, and leave five more candidates close to the validity floor before temporal inclusion. The honest decision is therefore to pin the label-blind set before measurement, state its unbounded failure shape, and preserve the full composition so the result can be audited. That is a conditional measurement design, not a theorem about weaker units.

### Why the head bin was retained

Draft 16 had already made the choice before any drift value existed, and the implementation already uses the session-zero grid. The rank-1 undercoverage is 1.138 seconds of one 60-second bin in a 72-bin trace. I retained the choice rather than reopening the grid, but removed the false monotonic rationale and made the result conditional on it. The fixture proves only that no one-way guarantee exists.

### Why this was not escalated despite the long §16 review

The review-cycle playbook escalates a specific disagreement that fails to converge after roughly two round-trips. This session did not repeat an unresolved disagreement with Claude: it accepted Draft 16's policy and found new, executable counterexamples to two claims attached to it. Draft 17 is therefore a new exact-state handoff, not another unsupported vote on the same contested point. Claude's owner re-review is still mandatory.

---

## Validation

- `agents/Claude/tools/test_band_drift.py`: **57 checks, 0 failed** at the pinned 200 permutations after the `extent_s` rename.
- `agents/Claude/tools/probe_band_drift_claims.py`: **3 of 3 probes passed**.
- `agents/Codex/tools/probe_draft16_safety_claims.py`: both deterministic counterexamples reproduced.
- Packet runbook checker: **10 of 10 steps agree** with their scripts' `--help` examples.
- Both changed Python files compiled successfully in the project venv.
- `git diff --check`: clean at the reviewed state.
- Draft 17 SHA-256: `709be46fd0f1d23c7677787410419cf63a7ff5a03945bc88bff2c9db625909eb`.
- Renamed utility SHA-256: `b2c016053b18ffb49b0e9e3c439af22a7ea1d6b1b306857fe9d9b9f0eea9ac66`.
- Review probe SHA-256: `af51fe507be92bcbd0b8b2d7063fcc20e2208f78905b9cceb1d8ef30717bf205`.

No network request, dependency installation, candidate/archive/raw-data read, template pull, heavy computation, Rung 0, generator or sorter run occurred.

---

## Files created or updated

| Path | Change |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Direct review repair to Draft 17; exact-state owner re-review open. |
| `Reproducibility Packet/scripts/utils/band_drift.py` | Renamed public extent argument and aligned documentation; numerical logic unchanged. |
| `agents/Codex/tools/probe_draft16_safety_claims.py` | New deterministic synthetic counterexample probe. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only verdict, exact-state handoff and hash correction. |
| `README.md` | Forward public correction of the withdrawn safety claims. |
| `agents/Codex/Session Summaries/HumanReport21.md` | This report. |
| `agents/Codex/README.md` | Workspace map and current shared-state routing refreshed. |
| `agents/Codex/Summary of Only Necessary Context.md` | Completely rewritten for Codex Session 22. |

No count- or event-triggered progress report was due. The next count-based Codex report is Session 24. No new director request is needed.

---

## Machine state

Measured at 2026-08-14 04:17 PDT: **1.89 GiB RAM free of 31.67 GiB; 1,086 MiB VRAM used of 16,311 MiB; 582.8 GiB free on `C:`.** Nothing heavy ran. This reading is evidence about the closeout moment, not permission for a future heavy step; every such step still requires a fresh admission measurement.

---

## Next steps

1. Claude genuinely owner-reviews Draft 17 SHA-256 `709be46fd0f1d23c7677787410419cf63a7ff5a03945bc88bff2c9db625909eb` and the renamed utility SHA-256 `b2c016053b18ffb49b0e9e3c439af22a7ea1d6b1b306857fe9d9b9f0eea9ac66`.
2. If Claude approves both exact states unchanged, §16 and the implementation loop close again.
3. Only after that may Claude write the archive-reading drift CLI and its scoped packet step/review.
4. Only after the CLI itself is approved may rank 1 be read for a drift value.
5. Noise, post-rescaling effective SNR, footprint/placement calibration, the exposure-schedule/placement specification, matcher implementation, exact host-dependent configuration, independent balance/manipulation approval, generation and sorter execution remain separate gates.
