# Human Report 4 — Codex

**Date and time:** 2026-08-11 17:13 PDT

**Session:** Codex Session 4

**Phase at start:** Phase 1 — Sharpening. The technical Claim Sheet had reached same-state approval. Claude had handed off the first Accessible Claim Sheet and a revised Study Guide Pass 1 source/PDF pair; both still required Codex's exact-state review.

**Phase at end:** Phase 2 — Execution. The technical and Accessible Claim Sheets, Study Guide Pass 1, and initial labor split are all explicitly approved by both agents. Both review chats are concluded. No Phase 2 sorter or generator run has begun.

---

## Summary

This session closed Phase 1 cleanly.

Codex reviewed `Accessible Claim Sheet.md` line by line against the agreed technical contract and approved it without edits. The translation preserves all fifteen slots, the manipulation and balance gates, the host-specific donor boundary, the hierarchical uncertainty scheme, the authoritative `D = |I| - T` rule, the conservative negative call, the 200-recording-minute minimum tranche, the 48-hour per-candidate ceiling, the 288-hour whole-panel projection, and every failure and non-transfer shape. The review-history callouts and final three-sentence reading aid were retained because they make the review process visible without narrowing the contract.

Codex then reviewed Claude's edited Study Guide source/PDF pair. The wrong cross-reference was fixed correctly. The new refractory-period paragraph was accepted because it closes a genuine conceptual gap: the upstream generation interface exposes `refractory_period_ms`, so the baseline is accurately taught as Poisson-like firing plus an enforced refractory period, and the reader can see why refractoriness belongs in the control rather than among the missing realism axes.

The Study Guide was rebuilt twice in a temporary directory, leaving Claude's approved PDF bytes untouched. Both builds exited successfully with no document warnings, unresolved references, or overfull/underfull boxes. Codex rendered all 13 pages and inspected each one; the layout is clean. Text extracted from the approved PDF was byte-identical to text extracted from the independent rebuild. Codex explicitly approved the exact source/PDF pair.

Those two approvals completed the final Phase 1 gates. Codex wrote the phase-transition progress report, appended the contract-ready director request, updated the public Live-Run README to Phase 2, concluded both review chats with summaries, and refreshed its workspace documentation.

## Accessible Claim Sheet review

### Exact state

`Accessible Claim Sheet.md` SHA-256:

`73bff8f81dc2e31b47d4abbe1f61c8106a34dccb8ea6457051c3dba84a589760`

Agreed technical `Claim Sheet.md` SHA-256:

`a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3`

**Codex verdict: APPROVE.** Claude and Codex now approve the same Accessible Claim Sheet bytes, so the Claim Sheet review cycle is closed.

### What was checked

- All fifteen slots are present in the same order.
- Tier A's matched-slot boundary survives translation; the accessible document does not pretend donor identity stays fixed when donor region changes.
- The Session 2 template-audit numbers retain their caveats: seven is a worst-case leave-largest count, not a universal usable-region count; the audit is a pool-size screen, not paired-arm feasibility; CA1 is a candidate and not a selection.
- The manipulation check remains a stop-or-go gate before sorting.
- The bootstrap hierarchy, repeated-donor clustering, and one-host conditional boundary remain explicit.
- `D = |I| - T` remains the only comparative rule. The positive, negative, and inconclusive conditions preserve the technical meaning, including the interaction-interval exclusion required for a bounded positive and the folded-at-zero reason a bounded negative is harder to call.
- The full compute arithmetic remains visible: 5 real blocks plus 5 pseudo blocks, 200 recording-minutes per candidate per tier, a 48-hour admission ceiling, and a 288-hour two-sorter/three-tier ceiling projection.
- The Slot 12 failure modes and all eight Slot 13 non-transfer/inconclusive boundaries remain intact.
- The minimum artifact set, Tier A-plus-B conclusion floor, Tier C generator-failure path, provenance disclosure, and `none identified` monetization position remain intact.

No bound was softened and no edit was needed.

## Study Guide Pass 1 final review

### Exact state

Source SHA-256:

`d33e74d73c41b3ef0b4edbe6de52c0cc4e5597bae2d048618edb5c4523f99819`

PDF SHA-256:

`75e1423294cb3c4695c14920851825d602379d9ffca1aab6bcb93cbd10d998a3`

**Codex verdict: APPROVE.** Claude and Codex now approve the same source/PDF pair, so the Study Guide Pass 1 review cycle is closed.

### Handback edits accepted

1. The forward reference in §3.1 now points to §3.2, the section that actually explains why timing is where most of the missing realism lives.
2. The guide no longer teaches injected spike timing as pure memoryless Poisson firing. It explains that a refractory period is layered on top, cites the upstream generation documentation, and connects that implemented feature to the control-arm decision.

The paragraph earns its space because it explains an absence. Without it, Randy would encounter three realism axes and have no way to know whether refractoriness had been considered or simply missed.

### Build and visual verification

- The approved source built twice with `pdflatex` in a temporary output directory; both exits were 0.
- No document warnings, unresolved references, or overfull/underfull boxes were present.
- The approved PDF is 13 letter-size pages.
- All 13 pages were rendered at 120 DPI and visually inspected for clipping, overlap, broken glyphs, equations, link text, section transitions, and pagination.
- Page 5's new refractory paragraph is clean and readable.
- Page 13 keeps §5.5 complete, with no orphan page.
- The approved PDF and independent rebuild have identical extracted text. Their PDF file hashes differ only because the rebuild has fresh PDF metadata; the approved artifact remained untouched.
- Temporary render/build files were removed after inspection.

The PDF inspection workflow required visual rendering rather than trusting a clean LaTeX log. That confirmed the layout as well as the source-level correction.

## Phase 1 closeout

### Review chats

Codex appended both exact-state approvals using verified unique EOF anchors, asserted each new session header appeared exactly once after the pre-write line count, re-read both physical tails, then concluded the chats:

- `chats/Claude-Codex/Claim Sheet Review/Claim Sheet Review - Concluded.md`
- `chats/Claude-Codex/Study Guide Pass 1 Review/Study Guide Pass 1 Review - Concluded.md`

Each folder now has a `Summary.md` recording the approved hashes and substantive convergence.

### Director progress report

`agents/Codex/Progress Reports/Progress Report Phase 1 Close.md` explains in generalist language:

- what is fixed before results;
- what review corrected;
- what is working;
- what is still unresolved;
- why the shared-memory constraint matters; and
- what Rung 0 and Tier A selection do next.

It states the central honesty boundary directly: no scientific result exists yet.

### Director requests

Codex appended the planned Phase-1-close contract-review entry to `director_requests.md`. Randy is pointed first to `Accessible Claim Sheet.md`, with the Study Guide as its conceptual companion. The request explains that any change becomes a dated amendment and that nothing is blocked while review is pending.

The earlier shared-machine memory request remains open and non-blocking. Its last measured state, from Claude Session 4, was 0.89 GiB free system RAM and 14,409 MiB free VRAM. Nothing in this session overrides the live resource gate.

### Public Live-Run README

The status banner now reads Phase 2 — Execution while keeping the public state `In Progress`. A lean append-only log entry records Phase 1 close and the resource-gated pilot that comes next. The artifact table now marks Study Guide Pass 1 approved, and the Accessible Claim Sheet is listed as an approved plain-language contract rather than as an artifact under review.

## Cross-review and source verification

Codex read Claude's `HumanReport4.md`, both active review transcripts, both handed-off artifacts, the agreed Claim Sheet, and the relevant source ledgers. Claude's report accurately described the open gates and the newly found refractory-period omission.

The refractory claim was checked against SpikeInterface's official generation documentation, which exposes `generate_sorting_kwargs` with `refractory_period_ms`. No new source entry was needed because Claude's ledger already contains the documentation and its project role.

## Challenges and how they were handled

**Exact PDF approval versus independent rebuild.** Rebuilding the source in place would have changed PDF metadata and created new bytes that Claude had not approved. Codex built in a temporary directory instead, reviewed the already approved PDF, and compared extracted text between the two outputs.

**The bundled Poppler wrappers failed to resolve their runtime path.** The workspace dependency resolver then hung and was terminated after repeated waits. Codex located the already-installed Poppler executables directly and used them for metadata and rendering. No dependency was installed or changed.

**An append-only file already contained a pre-Phase-1 director request.** The director-request playbook describes the Claim-Sheet-ready item as structural and normally first. This project had already documented why memory contention arrived earlier. Codex preserved that history and appended the structural entry after it rather than rewriting the file.

**Closing a phase without drifting into execution.** Phase 1 closure itself was a complete, substantive work unit. Rung 0 requires a fresh live resource measurement and a prepared admission run; this session did not casually start it after closeout. Phase 2 opens with that gate intact.

## Files created or updated

| Path | Change |
|---|---|
| `chats/Claude-Codex/Claim Sheet Review/Claim Sheet Review - Concluded.md` | Appended exact Accessible Claim Sheet approval; renamed from Active after convergence. |
| `chats/Claude-Codex/Claim Sheet Review/Summary.md` | New concluded-chat summary with approved hashes and design decisions. |
| `chats/Claude-Codex/Study Guide Pass 1 Review/Study Guide Pass 1 Review - Concluded.md` | Appended exact source/PDF approval; renamed from Active after convergence. |
| `chats/Claude-Codex/Study Guide Pass 1 Review/Summary.md` | New concluded-chat summary with approved hashes and verification evidence. |
| `agents/Codex/Progress Reports/Progress Report Phase 1 Close.md` | New director-facing phase-transition report. |
| `director_requests.md` | Appended the non-blocking contract-ready review entry. |
| `README.md` | Advanced the public banner and log to Phase 2; refreshed artifact statuses. |
| `agents/Codex/Session Summaries/HumanReport4.md` | This report. |
| `agents/Codex/README.md` | Updated workspace map, authority, and shared-state routing. |
| `agents/Codex/Summary of Only Necessary Context.md` | Completely rewritten for Session 5. |

## What did not happen

- No sorter run, generator run, raw-recording load, data download, dependency install, or other heavy compute occurred.
- Live RAM/VRAM was not re-measured because no heavy step was attempted. The contract requires the measurement immediately before a heavy step.
- Rung 0 did not begin. It remains the next Codex-owned execution task.
- Tier A host/injection-zone selection did not begin. It remains Claude's next execution task.
- No scientific result, claim amendment, or verification panel exists yet.

## Next steps

1. Claude begins Tier A host/injection-zone selection against the exact-host donor exclusion, local anatomy, placement, and Tier C evidence constraints.
2. On Codex's next turn, re-read Claude's newest report and any new chats, then prepare Rung 0.
3. Immediately before any admission run, measure free RAM and VRAM. Preserve at least 4 GiB system RAM and 2 GiB VRAM and obey the 75%-of-free guard. If the run does not fit, do not start it.
4. Time and memory-profile Kilosort4 plus the CPU candidate set on the same 60-second segment, record every drop and reason, and project per-tier and whole-panel cost before choosing the panel.
5. Build the inference/negative-control harness inside the Reproducibility Packet under the agreed software standards.
6. Treat any director feedback on the contract as a dated amendment while continuing non-blocked execution.
