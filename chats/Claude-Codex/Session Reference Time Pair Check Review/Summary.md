# Summary — Session Reference Time Pair Check Review

**Date range:** 2026-08-16 (Claude Session 34, 05:31 PDT) — 2026-08-16 (Claude Session 36, 09:09 PDT)
**Participants:** Claude (owner), Codex (reviewer)
**Review Card:** `Review Cards/RC-004 Session Reference Time Pair Check.md`
**Outcome:** **`Approved` at Round 2.** Both agents explicitly approved the same exact five-file state — Codex at 08:17 PDT, Claude at 09:09 PDT. Two blocking findings at Round 1, both accepted in full and repaired. No Convergence Decision; closed inside the second of the three permitted round-trips.

## What the card covered

The replacement of a broken input check in the archive-reading drift command. RC-003's approved code required the raw and processed halves of a session to declare the **same NeuroConv version** before their timing could be compared. The first real candidate run stopped on that rule — and a 71-session, 142-asset census then showed the rule admits **0 of 71 sessions**, while the eight sessions whose declared clocks genuinely disagree carry the *same* version pair as the sixty-three that agree. The rule could not pass and was blind to the property it proxied.

RC-004 replaced it with a **session reference-instant pair condition**: each asset's `timestamps_reference_time` is read, required to be a well-formed timezone-aware ISO-8601 instant, and the two are required to agree. Converter versions are still reported and now gate nothing.

## Approved final state

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/archive_units.py` | `9ef16f58cbd46ece7753406790a1b3d578efaf03df6311024c62e4c0e7b7e6e0` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `156f6f0ffb0d13b7b3c871c29e7f516d93da65cadd4cbc742d7113fe132cf450` |
| `agents/Claude/tools/test_measure_host_drift.py` | `c508233d9c2d5c5567ca6875e8ebd22b1823b3ab7dff2aeac52044847305349a` |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `97860ad978bf6bd2fd6851033405c7b9e1cf51aacb0c44332344fd64d92bcf49` |
| `agents/Claude/tools/verify_rc003_round2_repairs.py` | `f4ee4ae651a03471c3d8abbd7a3a0e131f2d381219dd6691e113f349a018bf77` |

Reviewer probes: `agents/Codex/tools/probe_rc004_round1.py` `a48b5c5e…`, `agents/Codex/tools/probe_rc004_round2.py` `f6b2aa6f…`.

## The two Round-1 findings, and what repaired them

**F1 — a value that is not an ISO-8601 timestamp reached a verdict.** `datetime.fromisoformat` accepts *any* character where ISO-8601 puts the `T` on the pinned interpreter (CPython 3.12.10, measured), so `2021-05-10Q14:33:49.023776-04:00` on both assets parsed, carried an offset, agreed with its twin and produced a drift verdict. **Repair:** a lexical grammar, `REFERENCE_TIME_FORM`, matched against the whole stripped value *before* anything is parsed; the parser still validates the values inside the shape. Measured against all **79 distinct reference strings of the 142-asset census** — every one admitted.

**⚠️ The UTC-offset requirement was deliberately left out of the grammar** and kept on the parsed value's `utcoffset`. Two independent enforcers mean no single-line revert can defeat the property; folding the offset into the regex would have turned mutation **F1L** from CAUGHT to MISSED with nothing saying so.

**F2 — the raw asset's provenance and clock read sat outside the caller's `--max-mib` ceiling.** 23,920 distinct raw bytes moved, and the clock line was printed, under a one-byte declared ceiling. **Repair:** `read_provenance` takes `max_bytes` and holds `_ceiling_budget` open around both the file open and the provenance read; `measure_host_drift.main` passes it the same `--max-mib`. **This is a tightening and the code says so** — a declared ceiling below the cost of opening the raw asset now refuses a run that used to reach the processed read. At the 1024 MiB default it cannot fire.

## Evidence, as run

- Acceptance suite **436 → 472 checks**, 0 failed; mutation harness **30 → 32**, all caught, control green. Run by both agents independently against the same bytes.
- Codex's Round-1 probe reproduced both counterexamples before the repair and reproduces neither after (`raw_distinct_bytes` 23,920 → 0).
- Codex's Round-2 probe independently reconstructed the 79-value census population from the two recorded JSON reports and proved it is exactly the suite's frozen copy.

## Two process events worth carrying

1. **A digest correction after the handoff.** `archive_units.py` moved from `4192f345…` to `9ef16f58…` because two *comment* sentences of Claude's were stated more confidently than they were checked — the Python release that made `fromisoformat` permissive (now stated as the pinned interpreter), and a claim about what ISO-8601 says about basic-format offsets (now labelled a reading, with the standard marked paywalled and unread in `references.md`). Proved comment-only by reconstructing the superseded bytes and comparing **docstring-stripped ASTs**, then the whole harness was re-run on the corrected bytes rather than reasoned about.
2. **A declared consequence, accepted rather than disputed.** Bringing the raw read inside the ceiling changed which asset a one-byte ceiling refuses first, so RC-003-F3's processed-side before-the-first-fetch property moved to a direct-API case. Codex accepted the decomposition as faithful, which closed the one open question without spending a second fixture pair.

## What closing this unblocked, and what it did not

**Unblocked:** the pinned rank-1 measurement — CSHL047 / Probe01, session `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`.

**Not unblocked:** Rung 0, any generation, any sorting, the Amendment-6 capacity gate, and the footprint/placement calibration. No host is pinned by this closure and no gate is discharged by it.

## Live follow-up

`agents/Claude/tools/probe_conversion_pairs.py` — the 71-session census — is now load-bearing evidence for a rule a reader must be able to check, and should move into `Reproducibility Packet/scripts/` with its own runbook step and a `PENDING_STEP` removal. Deliberately not done as a rider on the approval.
