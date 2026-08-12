# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 4 · 2026-08-11 17:13 PDT**

**Next Codex session will be Session 5.**

## Current phase

**Phase 1 is closed. Phase 2 — Execution is open.** No sorter run, generator run, data download, dependency install, or scientific measurement has occurred in Codex Session 4.

The Phase 1 requirements are all same-state agreed:

- technical Claim Sheet;
- Accessible Claim Sheet;
- Study Guide Pass 1 source/PDF pair; and
- initial labor split.

Both review chats are concluded and have `Summary.md` files. Later changes to either Claim Sheet use the dated amendment protocol, not the review cycle, and both sheets must remain in sync.

## Approved exact states

### Technical Claim Sheet

Path: `Claim Sheet.md`

SHA-256:

`a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3`

Both agents explicitly approve these bytes.

### Accessible Claim Sheet

Path: `Accessible Claim Sheet.md`

SHA-256:

`73bff8f81dc2e31b47d4abbe1f61c8106a34dccb8ea6457051c3dba84a589760`

Both agents explicitly approve these bytes. It preserves all fifteen slots, decision rules, compute budgets, failure shapes, and non-transfer boundaries without softening the technical contract.

### Study Guide Pass 1

Source: `Study Guide/Pass 1 - Conceptual Foundation.tex`

Source SHA-256:

`d33e74d73c41b3ef0b4edbe6de52c0cc4e5597bae2d048618edb5c4523f99819`

PDF: `Study Guide/Pass 1 - Conceptual Foundation.pdf`

PDF SHA-256:

`75e1423294cb3c4695c14920851825d602379d9ffca1aab6bcb93cbd10d998a3`

Both agents explicitly approve this exact pair. The final guide is 13 pages. Codex independently rebuilt the source twice in a temporary directory, confirmed clean logs, rendered and visually inspected all pages, and verified that approved/rebuilt extracted text is identical.

## Concluded review records

- `chats/Claude-Codex/Claim Sheet Review/Claim Sheet Review - Concluded.md`
- `chats/Claude-Codex/Claim Sheet Review/Summary.md`
- `chats/Claude-Codex/Study Guide Pass 1 Review/Study Guide Pass 1 Review - Concluded.md`
- `chats/Claude-Codex/Study Guide Pass 1 Review/Summary.md`

Do not reopen these review cycles. Corrections discovered later propagate through amendments or later artifacts.

## Labor split

- **Claude:** Tier A host/injection-zone selection; Accessible Claim Sheet owner; Study Guide owner.
- **Codex:** Rung 0 feasibility pilot; sorter-panel decision; inference and negative-control harness; Tier A balance/manipulation gate.
- **Tier B and Tier C:** implementation assigned after Rung 0; the non-author owns each manipulation check.
- **Reproducibility Packet:** co-owned. Surviving scripts are written directly into it.
- Default Claude-writer/Codex-reviewer convention remains for later narrative artifacts.

## Phase 2 design commitments that are easiest to violate

- Tier A pairs covariate-matched donor slots; donor identity cannot stay fixed when donor region changes.
- Use a pinned anatomical injection zone, not one region label for a whole penetration.
- Exclude the exact host source dataset before claiming donor feasibility. The 37/7 audit is a conservative pool screen, not paired-arm feasibility.
- CA1 is the only current joint-screen candidate on its face, not a selection. Its worst-case donor count is six, below the ten-unit budget.
- Tier B's population driver is computed once from the untouched host without sorter output.
- Every manipulation check passes at biologically justified magnitude before any sorter time is spent on that tier.
- The primary comparative decision uses the hierarchical-bootstrap interval on `D = |I| - T`; `[−T,T]` is only within-resample shorthand.
- A bounded positive additionally requires the interaction interval to exclude zero. A wide interval is inconclusive, never negative.
- Five real blocks plus five pseudo blocks form the initial tranche. Pseudo-arms are sorter runs. Minimum load: 200 recording-minutes per candidate per tier.
- Admission ceiling stays 48 sorter-hours per candidate per tier. Report per-candidate, per-tier, and whole-panel projections; two sorters × three tiers at the ceiling is 288 sorter-hours.
- Equal real/pseudo block counts give equal nominal replication basis, not equal precision; report both achieved widths.
- Use one host/injection zone across tiers by default. If the host changes, drop cross-tier comparison.

## Compute state and open director requests

Four measured free-memory points exist in `director_requests.md`:

- 3.46 GiB RAM / 14,269 MiB VRAM;
- 3.96 GiB RAM / 14,389 MiB VRAM;
- 1.01 GiB RAM / 14,286 MiB VRAM; and
- 0.89 GiB RAM / 14,409 MiB VRAM.

The known full Kilosort4 run peaked at 29.3 GiB system RAM. The shared-memory request asks for a predictable quiet window or a decision to design around a permanent small-memory ceiling. It is non-blocking.

Immediately before every heavy step:

- measure free RAM and VRAM at that moment;
- use no more than 75% of then-free RAM or VRAM;
- preserve at least 4 GiB system RAM and 2 GiB VRAM;
- stop and record a resource failure if a guard is crossed;
- use only `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; and
- pin dependencies at first install.

A second director entry now asks Randy to review the agreed contract, preferably through `Accessible Claim Sheet.md`. It is also non-blocking. Feedback becomes a dated amendment; execution continues meanwhile.

## Phase-transition records

- `agents/Codex/Progress Reports/Progress Report Phase 1 Close.md` is the director-facing transition report.
- Root `README.md` now shows Phase 2 — Execution, remains `In Progress`, records Phase 1 close in the append-only log, and marks Study Guide Pass 1 approved.
- `agents/Codex/Session Summaries/HumanReport4.md` contains the full session evidence.

## What Codex should do next

1. Read Claude's newest report and every new Codex-including active chat before replying.
2. Confirm whether Claude has begun or completed Tier A host/injection-zone selection; cross-review it if present.
3. Prepare Rung 0 without assuming a resource window. Identify the exact host segment/data inputs and candidate sorter commands before any heavy launch.
4. Immediately before the first candidate run, measure live RAM and VRAM and enforce the admission/headroom rules. If it does not fit, do not start it; record the failure and work on the inference/negative-control harness or other non-heavy packet work.
5. Time and memory-profile Kilosort4 plus the declared CPU candidate set on the same ~60 s segment, one admission run each, with the 60-minute wall-time ceiling.
6. Record measured peaks, runtime, drops, and projected 200-recording-minute per-tier plus whole-panel cost before selecting the panel.
7. Write surviving code directly into `Reproducibility Packet/`, with `argparse`, docstrings, no hard-coded paths, loud failures, and pinned dependencies.
