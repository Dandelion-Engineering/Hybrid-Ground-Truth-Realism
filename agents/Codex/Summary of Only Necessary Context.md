# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 3 · 2026-08-11 15:16 PDT**

**Next Codex session will be Session 4.**

## Current phase and gates

The project remains in **Phase 1 — Sharpening**. Phase 0 is closed. The initial labor split is explicitly agreed by both agents.

Two exact-state review loops are active:

1. **Technical Claim Sheet.** Codex explicitly approved an edited current state. Claude must genuinely re-review Codex's edits and either explicitly approve the same bytes or edit and hand it back.
2. **Study Guide Pass 1.** Codex explicitly approved an edited source/PDF pair. Claude must genuinely re-review both the feedback and edited artifact pair and either explicitly approve them or edit and hand them back.

The **Accessible Claim Sheet does not yet exist**. Claude committed to writing it as soon as the technical sheet converges. Phase 1 cannot close until the technical Claim Sheet, Accessible Claim Sheet, and Study Guide Pass 1 each have same-state approval from both agents.

Nothing is blocked on the director. The shared-memory entry in `director_requests.md` is open but explicitly non-blocking.

## Exact states at handoff

### Claim Sheet

Path: `Claim Sheet.md`

SHA-256:

`a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3`

**Codex verdict: APPROVE.** Recorded in:

`chats/Claude-Codex/Claim Sheet Review/Claim Sheet Review - Active.md`

This approval supersedes Codex Session 2's approval hash and Claude Session 3's handoff hash. It applies only to the bytes above.

### Study Guide Pass 1

Source: `Study Guide/Pass 1 - Conceptual Foundation.tex`

Source SHA-256:

`37f724699305a7ae578ed6a8f1550161ed376cabe71b9fc85c6f5dcf5f3468d4`

Compiled PDF: `Study Guide/Pass 1 - Conceptual Foundation.pdf`

PDF SHA-256:

`b42878216a3154c180875d2bea4426bc12b250da22d12e21e0b7e76a669abf55`

**Codex verdict: APPROVE.** Recorded in:

`chats/Claude-Codex/Study Guide Pass 1 Review/Study Guide Pass 1 Review - Active.md`

Final build is 13 pages, two successful `pdflatex` passes, no LaTeX/package warnings, no overfull or underfull boxes, and complete rendered-page visual QA.

## What changed in the technical Claim Sheet

Claude Session 3 added three sound corrections:

- The negative-control pseudo-arms are sorter runs. The minimum Rung 2 tranche is `10 min × 2 arms × 5 blocks × 2 contrast types = 200 recording-minutes per candidate per tier`.
- The admission ceiling stays **≤48 sorter-hours per candidate per tier**. Rung 0 records candidate, tier, and whole-panel projections; at the ceiling, two sorters across three tiers project to 288 sorter-hours.
- `D = |I| − T` is the authoritative comparative decision quantity; a bounded negative is deliberately harder to call because `|I|` is folded at zero.
- One host and injection zone are used across tiers by default. If the host changes, cross-tier comparison is dropped.
- CA1 is the only current joint-screen candidate where Tier C's verified biology and Tier A's donor screen overlap on their face. It is not selected: 12 pre-exclusion templates fall to 6 in the worst case, below the ten-unit budget.

Codex Session 3 then made two direct coherence corrections:

- Equal real and pseudo-arm block counts establish the same **nominal replication basis**, not guaranteed equal precision. Both achieved interval widths must be reported.
- Slot 11's numbered success checklist now uses the same `D` rule as the rest of the sheet: interval below zero for bounded negative; above zero plus interaction interval excluding zero for bounded positive.

The stricter 48-hour ceiling is accepted. There is no open Codex disagreement about Claude's three additions.

## Study Guide Pass 1 review outcome

The guide's structure, audience choice, continuous narrative, and omission of sorter-internal detail were accepted. Codex edited these technical points before approval:

- A multichannel template reflects probe-relative position plus cell anatomy, tissue, and probe geometry.
- SHYBRID reuses observed spike times after a fixed shift and a fixed template's per-spike fitted amplitudes; the insertion train receives fresh random sub-sample jitter by default. It does not preserve observed timing jitter or transport arbitrary full per-spike waveform shapes unchanged. Both relevant implementation files are linked in `agents/Codex/references.md`.
- Tier A needs no new **generator mechanism**, but still needs selection, balance, and analysis code. Its expected weak interaction is explicitly the project's prior.
- For `I = Δ₁ − Δ₂`, a negative value means realism hurt sorter 1 more. The original guide's read-aloud sentence had the sign backwards.
- A near-zero interaction says the between-sorter comparison is stable; it does not validate the absolute scores.
- The guide now teaches `D = |I| − T`, the folded-at-zero conservative negative call, and the full resampling hierarchy: paired slots within blocks, blocks within hosts, hosts at the top, repeated donors clustered, and one-host intervals conditional on that host.
- The 50%-of-gap component is a declared judgement, not a theorem about reader decisions.
- CA1 is a candidate with open host-specific feasibility and balance gates.
- A manipulation below the declared biological range does not pass the biological-realism gate; any later stress-test result is bounded to the achieved magnitude.

## Labor split — agreed by both agents

- **Claude:** Accessible Claim Sheet, Study Guide Pass 1 owner, Tier A host/injection-zone selection.
- **Codex:** Rung 0 feasibility pilot, sorter-panel decision, inference and negative-control harness.
- **Codex owns Tier A's balance/manipulation gate**, so Claude does not grade its own host/zone selection.
- Tier B and Tier C implementation are assigned after Rung 0; the non-author owns each manipulation check.
- Reproducibility Packet remains co-owned. The default Claude-writer/Codex-reviewer convention remains for narrative artifacts.

## Compute and director state

`director_requests.md` records three early free-memory measurements: 3.46 GiB, 3.96 GiB, and 1.01 GiB free system RAM, while VRAM stayed broadly free. The known full Kilosort4 run peaked at 29.3 GiB RAM. Randy was asked for a quiet window, information about other workloads, or a decision to design around a small permanent ceiling.

This request is non-blocking. Before any heavy step:

- measure live free RAM and VRAM immediately beforehand;
- preserve at least 4 GiB system RAM and 2 GiB VRAM;
- use no more than 75% of then-free RAM or VRAM;
- stop and record a resource failure if a guard is crossed;
- use only `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`;
- install nothing without pinning it at first install.

No heavy compute ran in Codex Session 3, so no live memory measurement was needed.

## Public record and closeout state

The root Live-Run README was checked and intentionally left unchanged. No artifact or phase completed because Claude's same-state re-reviews are still open. Do not log a review as closed until those explicit approvals exist.

No progress report was due in Codex Session 3. A phase-transition progress report and the structural Claim-Sheet-ready `director_requests.md` entry are required from whichever session actually closes Phase 1.

Codex Session 3 created `agents/Codex/Session Summaries/HumanReport3.md`. Read it for full review reasoning and validation evidence.

## What Codex should do next

1. Read Claude's newest report and the physical tails of both active review chats.
2. Recompute all relevant hashes before relying on the approvals above.
3. If Claude explicitly approves the Claim Sheet hash above, treat the technical sheet review as closed. If Claude edits, review the new exact state; do not carry approval forward.
4. If Claude explicitly approves the Study Guide source/PDF pair above, treat Pass 1 as closed. If Claude edits or rebuilds, review both new hashes and render the PDF again.
5. Review the Accessible Claim Sheet only after Claude hands off an explicitly approved state, reading `Playbooks/accessible-claim-sheet.md` and `Playbooks/review-cycle.md` first.
6. Do not start Rung 0 until Phase 1 artifacts and labor have converged and the turn returns to Codex.
7. Immediately before Rung 0, measure live RAM/VRAM and obey the exact admission/headroom rules. A repeated inability to find a safe window is handled through the existing fallback/amendment path, not by bypassing the gate.
