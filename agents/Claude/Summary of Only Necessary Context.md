# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 2 · 2026-08-11 12:26 PDT**
**Next session will be Claude Session 3.**

You are starting with no memory of the last session. This file restores everything you need and nothing you don't. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those at session start anyway.

**Read `Claim Sheet.md` before doing any work.** It is the contract now, it did not exist before Session 2, and it is where every design decision listed below actually lives. This file is the *state*; the Claim Sheet is the *commitments*.

---

## 1. Where the project is

**Phase 1 — Sharpening. Phase 0 closed in Session 2.**

The Claim Sheet is written and is **in review with Codex**. Phase 1 closes when: (a) both agents explicitly approve the *same state* of the Claim Sheet, (b) the Accessible Claim Sheet exists and is agreed, and (c) the division of labor is agreed. None of the three is done.

Nothing is blocked on the director. **`director_requests.md` still does not exist** and has not needed to.

## 2. The very first thing to do next session

**Check `chats/Claude-Codex/Claim Sheet Review/` for Codex's review.**

- **If Codex has reviewed and edited:** re-open `Claim Sheet.md` and *genuinely* re-review both its feedback and its edits — do not wave them through. Read `Playbooks/review-cycle.md` first. The loop closes only when both agents have explicitly approved the *same* state; approval is never inferred from an edit, a handoff, or silence. **Owning an artifact includes coming back to it** — this is the named failure mode for the position I am now in.
- **If Codex has not yet replied:** do not idle. Do the work in §6 that does not depend on the review.

## 3. What I produced in Session 2

| File | What it is |
|---|---|
| `Claim Sheet.md` | **The contract.** Orientation header, contract-at-a-glance, fifteen slots. Draft under review — not yet an agreed state. |
| `Reproducibility Packet/scripts/audit_template_library.py` | Stdlib-only template feasibility audit with the leave-one-dataset-out stress test. Packet-ready as written. |
| `Reproducibility Packet/results/template_audit_2026-08-11.txt` | Its output, pinned to the metadata snapshot hash. |
| `agents/Claude/Progress Reports/Progress Report Phase 0 Close.md` | Phase-transition report for the director. |
| `chats/…/Phase 0 Literature Comparison/…Concluded.md` + `Summary.md` | Phase 0 chat closed. The `Summary.md` is the fast way back into what was settled. |
| `chats/…/Claim Sheet Review/…Active.md` | Review channel opened; sheet handed off with my explicit approval. |
| `agents/Claude/references.md` | Corrections log added at top; template-library entry rewritten; two `[VERIFY]` cleared; Cohen's *d* use `[SUPERSEDED]`. |
| `README.md` (root) | Banner → Phase 1; three log entries; Claim Sheet listed. |
| `agents/Claude/Session Summaries/HumanReport2.md` | Session report. |

## 4. What was settled with Codex — do not relitigate

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates (configuration only) → Tier B local population-rate coupling (the anchor authors' own proposed fix; modest code) → Tier C bursting with spike-history-dependent amplitude attenuation (the genuinely missing mechanism). Combined arm only after component effects are known.
- **Primary comparative estimand is the paired difference in differences** — realism effect for sorter A minus realism effect for sorter B — with thresholds pre-declared in **raw paired accuracy units**, standardized effects secondary and never as thresholds.
- **The manipulation check is a hard stop-or-go gate** with axis-specific criteria. If the injected data does not demonstrably carry the intended property at realistic magnitude, **no sorter run starts.** Otherwise a null is a statement about our implementation, not the field's method, and nothing afterwards can tell the two apart.
- **Refractoriness is already implemented upstream** and is part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus at least one CPU internal sorter (SpyKING CIRCUS 2, TriDesClous 2, or Lupin — all MIT via SpikeInterface). A Kilosort-only panel is biased toward the null.
- **Two corrections Codex raised and I accepted** (details in the Phase 0 `Summary.md`): the stale 601-template premise, and Cohen's *d* as a flip threshold. Both are propagated; my Literature Foundation stays frozen with the errors in it and the ledger governs.

## 5. The numbers and facts that matter, so you don't re-derive them

**Template feasibility — my Session 2 result, and it reversed a decision order.** Caliper amplitude 50–200 µV (from the anchor's own rescaling range) and SNR 5–15 (my judgement, the softer bound): 1,149 of 2,183 NP1.0 templates survive across 149 areas; **37 areas hold ≥10 templates.** After dropping each area's largest contributing source dataset — required by the donor/host leakage rule — **only 7 survive: CP (42), PIR (19), SUB (18), VISa5 (17), AId5 (14), MRN (14), ENTl5 (10).** Thirteen collapse to zero.

→ **Host selection is downstream of donor availability, not parallel to it.** Either pick from the 7-area shortlist, or deliberately pick a host outside the library's 37 IBL source datasets and say why. Re-run the script with different calipers rather than re-deriving by hand.

**Template metadata snapshot, verified independently by both agents:** SHA-256 `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`, 2,032,640 bytes, Last-Modified 2024-09-29 — so the table is mutable but has not actually moved since 2024. Pin it by hash anyway; record selected `template_index` rows.

**The three pre-declared decision events** (Claim Sheet Slot 11): sign **reversal**; **loss of separation** (gap's interval excludes zero in one arm, includes it in the other — distinct from reversal, and likelier); and **magnitude** ≥50% of the control-arm sorter gap. Absolute-score materiality is |Δ accuracy| ≥ 0.05.

**Two uncomfortable pre-declarations that exist to stop this project misleading anyone** (Slot 13): a null with a wide interval is **inconclusive, never reported as evidence realism doesn't matter**; and **Tier A alone cannot conclude the project**, because it is the cheapest axis *and* the least likely to move the interaction.

## 6. Work that does not depend on Codex's review

1. **Study Guide Pass 1** (`Playbooks/study-guide.md`) — due at Phase 1 close, I am the default writer, and it is largely independent of the sheet's final wording.
2. **Clear remaining verification debt.** Everything in `references.md` *Pending* is **not citable**: Quirk & Wilson (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed), the regional waveform-duration figures, Steinmetz & Ye 2022. Also still open: whether SHYBRID transports individual snippets or an average template — both agents failed to resolve it; it is not load-bearing, so it blocks nothing.
3. **Do not re-run the template audit.** It is done, reproduced by both agents, and scripted. Extending it to a *specific* host recording is Phase 2 work and needs host selection first.

## 7. Deliberate departures from the playbooks, so they are not mistaken for omissions

- **The Accessible Claim Sheet is not written**, though `Playbooks/claim-sheet.md` asks for it immediately after. Reason: the two must stay in sync and the technical sheet is a draft a reviewer is about to edit. **I committed in the review chat to writing it in the same session we converge, before Phase 1 closes** — and offered to write it next session instead if Codex would rather review both together. Check the chat for its answer.
- **The `Reproducibility Packet/` folder was created in Phase 1**, slightly ahead of the standard's "early in Phase 2," because a finalized portable script existed and the standard is that packet materials live *inside* the packet rather than being relocated later.

## 8. My open proposal on the division of labor

Posted in the review chat, not yet agreed. I take the Accessible Claim Sheet, Study Guide Pass 1, and Tier A selection/audit work; Codex takes the Rung 0 feasibility pilot and the sorter-panel decision, since that is a compute judgement it has been more careful about; Tiers B and C split after the pilot says what the machine affords. **The part I care most about: the manipulation check for each tier is owned by whoever did *not* write that tier's generator**, so the stop-or-go gate is never graded by its own author.

## 9. Machine state — re-measure, never trust this number

**At 2026-08-11 12:07 PDT: RAM 3.96 GiB free of 31.67 (~87% in use); VRAM 14,389 MiB free of 16,311.**

That is the **second consecutive session** measuring under 4.5 GiB free. The pre-project feasibility run that proved Kilosort4 works here peaked at **29.3 GiB**. Started at either measured moment, it would have failed — slowly and confusingly. Other projects run on this machine uncoordinated with you. **Measure at the moment of the heavy step, against a measured requirement, never from a file — including this one.** The Phase 2 pilot must either find a quiet window or be designed around a fraction of that footprint.

**The venv still contains only `pip`.** SpikeInterface, PyTorch, and Kilosort4 are **not installed**; there is **no `requirements.txt`**. That is correct for now — the first install is the Phase 2 Rung 0 pilot, and versions get pinned *at install time*, not retrofitted. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe`; never bare `python` or `pip`.

## 10. Three housekeeping facts that are easy to get wrong

- **This run is agent-selected**, so the run-provenance block on the public README is **required** and survives unchanged into State B. Do not remove it, soften it, or move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor its source, never link against it. A genuine need to modify it is a `director_requests.md` question *before* writing the modification. For sorter internals, use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** `Literature Foundation.md` is frozen with its Session 1 errors intact; `references.md` governs. Do not go back and fix the foundation — that is the failure mode the rule exists to prevent.
