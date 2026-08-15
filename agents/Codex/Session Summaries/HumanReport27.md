# Human Report — Codex Session 27

**Date:** 2026-08-15

**Closeout time:** 04:20 PDT

**Phase:** 2 — Execution

**Review outcome:** RC-002 Round 1 — **Revisions Required**

## Executive summary

I performed the one exhaustive Round-1 review of Claude's archive-reading drift command under `Review Cards/RC-002 Archive-Reading Drift Command.md`. The submitted owner harness passes all 163 checks, and the approved RC-001 estimator evidence remains green. That positive evidence is real but insufficient for approval: seven independent synthetic constructions reached boundaries that the submitted tests did not cover.

The review returned one complete ledger with five blocking findings and one tracked nonblocking follow-up. No archive, candidate, or network data was read; no host was selected; no command output was accepted as a project result. Candidate measurement remains blocked. Claude owns the response, and any Codex Round 2 is delta-only against the recorded ledger and response-created regressions.

## Exact candidate reviewed

- `Reproducibility Packet/scripts/utils/archive_units.py` — SHA-256 `c5c21cb9a2e0f9cedd0f1cff7e98886cb77ccdd21e2ad763422a7b44f3146f12`
- `agents/Claude/tools/measure_host_drift.py` — SHA-256 `c71a5d9311b0785dcff5469e9c698f0f208946cafb00b32dd4eb0bddbda93cfb`
- `agents/Claude/tools/test_measure_host_drift.py` — SHA-256 `6ff3d26ce64016efabdf71aaab93c9a0d71526f37fdcbedae457c438f50a3b39`

I did not edit any of these candidate files.

## Positive evidence preserved

- Claude's archive-command harness: **163 checks, 0 failures**.
- Approved drift-estimator harness: **103/103**.
- Claim probes: **3/3**.
- Codex RC-001 probe: **13/13**, including **93,184** exhaustive small constructed cases with zero violations.
- Packet runbook checker: **10/10**.
- Python compilation of the reviewed Python files and Codex's new probe is clean.
- RC-001's authenticated selection-document and estimator hashes remain unchanged.

The accepted parts of the RC-002 design include the explicit `--gate {strict,relaxed}` switch and the use of the approved estimator rather than a second drift implementation. The deferred packet-runbook Step 11 text is not itself a Round-1 blocker. The card's Purpose controls the review boundary, so the written scope did not excuse failures that could admit an invalid measurement or undermine refusal/resource guarantees.

## Blocking findings

### F1 — The byte preflight does not bound actual work

The plan sums logical HDF5 array payload. The reader fetches fixed-size blocks, caches whole fetched blocks, and later materializes peak arrays as `float64`. In a synthetic plan with 57,600 logical bytes, the 60,000-byte ceiling passed while fixed-block reads transferred 81,360 bytes. The submitted ceiling therefore does not establish its stated network, cache, or peak-memory safety boundary. The revision must separately define and enforce logical payload, actual block transfer/cache, and peak-memory limits.

### F2 — Integer structure is coerced before it is validated

Ragged offsets and `max_electrode` are converted to integer dtype before the command checks them. Fractional values are silently truncated and can reach a passing verdict. The command also does not prove all unit-indexed scalar arrays have the same unit count. The revision must validate original dtype/integrality and exact scalar-array lengths before coercion or indexing.

### F3 — Pair and AP-clock identity are incomplete

The command accepts a raw file for one subject and a processed file for another when their session UUIDs match. It also accepts AP data with 1,000 samples and only 999 timestamps. Both constructions reached a verdict. The revision must bind raw and processed assets by the declared subject/session/stem identity and prove AP timestamp length equals the AP data time axis before using clock bounds.

### F4 — A typeable anatomy threshold changes the population being graded

`--max-gap-um` is an arbitrary runtime threshold, not a predeclared scientific gate. With `--max-gap-um 1000`, two CA1 islands separated by CA3 rows merge and eight intervening/non-target units enter the graded span, producing a passing verdict. The candidate must implement the declared exact 40 µm finite CA1 step check without exposing a new scientific tuning knob.

### F5 — The command is outside the packet and is not standalone

The reviewed command lives under `agents/Claude/tools/` while the card and packet require the executable archive reader to be part of the Reproducibility Packet. Invoking it directly from the repository root fails with `ModuleNotFoundError: screen_host_timing` because the owner harness supplies a path that the command itself does not. The approved candidate must be placed in the packet and run from its documented location before any candidate read. A sibling packet-module import is acceptable for this card; the issue is artifact placement and standalone invocation, not a demand to duplicate code.

## Tracked nonblocking follow-up

### F6 — Output collision and stale-artifact semantics

A successful run followed by an input-error rerun against the same output paths leaves the previous report and JSON unchanged. Report and record paths can also collide. This does not need to block the corrected measurement candidate if the revised command and Step 11 define safe output ownership clearly, but it remains recorded and cannot disappear silently.

## Independent reproduction artifact

I added `agents/Codex/tools/probe_rc002_round1.py`, SHA-256 `e4197bcaabb523929b34bc340b4d0419e0fc154c51618f08fd56d92beecbd27a`. It uses only locally generated synthetic HDF5 fixtures and reuses the owner's fixture writers; it does not open DANDI or any candidate asset. It deterministically reproduces seven constructions:

1. fractional ragged offsets truncated to integers;
2. fractional `max_electrode` values truncated to integers;
3. AP data/timestamp length mismatch accepted;
4. raw/processed subject mismatch accepted under one session UUID;
5. logical byte plan below a ceiling while fixed-block transfer exceeds it;
6. stale prior outputs surviving an input-error rerun;
7. a large anatomy gap merging CA1 islands and admitting intervening units.

## Review-method feedback

Randy asked that the three-way review-method chat remain active. I added a concise assessment there: the first bounded cards are improving review completeness and making closure conditions explicit, but Round 1 is still expensive and card authors must not narrow scope so far that stated purpose and executable refusal boundaries escape review. RC-002 demonstrates both sides: one exhaustive pass produced one finite ledger, and the ledger still treated the card Purpose as controlling.

## Public-state correction

The prior root `README.md` entry said the command counted the exact number of bytes it was about to transfer. That is no longer supportable after F1. I appended a forward correction rather than rewriting history: the 163 tests remain green, but the command has been returned before archive access because independent constructions exposed transfer-accounting, structural, identity, clock, anatomy and standalone-execution defects.

## Files changed

- `agents/Codex/tools/probe_rc002_round1.py` — new independent synthetic probe.
- `Review Cards/RC-002 Archive-Reading Drift Command.md` — Round-1 status, full ledger, tracked follow-up and delta-only next gate.
- `chats/Claude-Codex/Archive-Reading Drift Command Review/Archive-Reading Drift Command Review - Active.md` — append-only reviewer handoff.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — append-only method assessment.
- `README.md` — append-only public forward correction.
- `agents/Codex/README.md` — workspace map and current boundaries.
- `agents/Codex/Summary of Only Necessary Context.md` — next-session continuity.
- this report.

The two chat appends were guarded by pre-write line counts, unique physical-EOF anchors, byte-prefix hashes and post-write occurrence/tail checks. Both original byte prefixes remained exact.

## Compute and safety state

At 04:20 PDT the machine had about **0.03 GiB free of 31.67 GiB RAM** and the NVIDIA RTX 5060 Ti used **1,085 of 16,311 MiB VRAM**. I performed no heavy work after observing that pressure. All review evidence was synthetic and local; no dependency was installed, no raw data was read, and no external scientific execution occurred.

## Next gate

Claude should respond to F1–F6 and submit an exact revised candidate state. Codex should then authenticate that state and perform only the recorded delta review plus regression checks caused by the response. Until explicit same-state approval, candidate measurement remains blocked. Reviewer edits, a green aggregate harness, downstream use, silence, or this handoff are not approval.

No count-based progress report is due until Codex Session 32.
