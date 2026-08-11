# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 2 · 2026-08-11 13:15 PDT**

**Next Codex session will be Session 3.**

## Current state

The project is in **Phase 1 — Sharpening**. Phase 0 is closed.

Claude owns `Claim Sheet.md`. In Claude Session 2 it handed off a first full draft with explicit approval. In Codex Session 2, Codex read both Literature Foundations and source ledgers, reviewed the draft under `Playbooks/claim-sheet.md` and `Playbooks/review-cycle.md`, edited it directly, and explicitly approved the resulting exact state in:

`chats/Claude-Codex/Claim Sheet Review/Claim Sheet Review - Active.md`

Approved Claim Sheet SHA-256 at handoff:

`67c9503b536de4bc7006e02a7bb25cd01f23e3d5c488c1490435bacdcf758f6e`

**The review loop is still open.** Claude must re-open the file and feedback, then explicitly approve that same state or edit and hand it back. Codex's edit/handoff is not owner approval.

Phase 1 additionally requires an agreed Accessible Claim Sheet, Study Guide Pass 1, and explicit same-state agreement on the initial division of labor. Nothing is blocked on the director.

## What Codex changed in the Claim Sheet

### Tier A

- Region matching cannot hold donor-template identity fixed. Tier A now uses covariate-matched donor-pair slots while reusing spike train, placement, rescaled amplitude target, unit count, and paired randomization block. Tiers B/C retain donor identity.
- The primary control is the anchor-like **region-unaware** draw, not a maximally distant region. A distant arm is secondary only.
- A whole Neuropixels recording is not assigned one region. Each host must pin anatomy and define an injection zone or depth-specific zones; matching uses the local label at placement.
- Final balance is on post-rescaling amplitude and effective SNR in the selected host, plus geometry/placement/provenance. Donor amplitude 50–200 and SNR 5–15 remain provisional pool screens only.

### Template audit interpretation

The live counts still reproduce: 7,877 rows total, 2,183 NP1.0 rows, 37 labels with at least ten templates under the provisional screen, and 7 labels after the **worst-case** largest-source exclusion.

The correction is interpretive and load-bearing:

- 7 is the worst case only when the selected host belongs to that area's largest donor source;
- excluding a different exact source can leave more templates;
- the audit does not test the region-unaware control, pairwise balance, or anatomical placement; and
- the anchor's 50–200 µV value is an injection rescaling target, not a justification for requiring donors' original amplitude to already lie in that range.

`Reproducibility Packet/scripts/audit_template_library.py` and its saved output now state these boundaries. Codex reran the script with the project venv; the snapshot hash and counts matched.

### Temporal tiers

- Tier B must derive its population driver from a sorter-independent host-activity proxy computed once from the untouched host. Total count, mean rate, and refractoriness stay fixed across arms.
- Tier C's current ≤6 ms/history-dependent biological prior is CA1/cell-class-specific. Another host region needs primary evidence or the run is labelled a synthetic stress test rather than biological realism.

### Estimand, replication, and decisions

- Primary mean is nested: paired units/donor slots within randomization blocks, blocks within hosts, hosts equally across the tested set.
- Hierarchical paired bootstrap uses those levels. One-host results are explicitly conditional on that host.
- Five blocks are the initial resource tranche, not a sufficient tail estimate by assertion. Add fixed-size block batches based on interval width, not favorable point estimates.
- The old seed-null band is now a matched pseudo-arm **negative-control replicate band**. It diagnoses nuisance selection/seed interactions and is visualized, but is not a second p-value or a replacement for the primary interval.
- Comparative margin: `T = max(0.05, 0.5 × |G0|)`. Each bootstrap recomputes `G0`, `T`, and `D = |I| − T`. `D` interval above zero plus interaction interval excluding zero = bounded positive; below zero = bounded negative; crossing zero = inconclusive.
- “Significant in one arm, not significant in the other” is not a difference. Practical separation uses the declared `[-0.05, 0.05]` equivalence region after the direct interaction clears the decision rule.

### Verification and compute pilot

Slot 8 Panel 1 is tier-specific (Tier A anatomy/balance, Tier B trajectory/invariance, Tier C ISI/amplitude history). Panel 2 shows the interaction, primary interval/materiality margin, and negative-control band with distinct roles.

Rung 0 now has explicit admission numbers: 60-minute ceiling on the 60-second pilot, monitored use of no more than 75% of live free RAM/VRAM while retaining at least 4 GiB RAM and 2 GiB VRAM, and ≤48 projected sorter-hours per candidate for the minimum five-block Tier-2 tranche. Changing these requires amendment.

## Labor split — Codex's approved proposal

- Claude: Accessible Claim Sheet, Study Guide Pass 1, Tier A host/injection-zone selection.
- Codex: Rung 0 pilot, sorter-panel decision, inference and negative-control harness.
- Codex owns the Tier A balance/manipulation gate.
- Tier B/C implementation is assigned after the pilot; the non-author owns each manipulation check.
- Reproducibility Packet remains co-owned; default Claude-writer/Codex-reviewer convention remains for narrative artifacts.

Claude must explicitly accept or revise this split next session; Codex's acceptance alone does not close it.

## Public record

The root README still correctly says `Phase 1 — Sharpening (Claim Sheet in review)`. Codex appended a corrective running-log entry because the prior public 37→7 statement was too strong. The old entry was preserved; the new entry records the worst-case boundary and that same-state owner review remains open.

## Codex Session 2 outputs

- `Claim Sheet.md` — direct review edits; Codex-approved handoff state.
- `chats/Claude-Codex/Claim Sheet Review/Claim Sheet Review - Active.md` — appended review, approval, labor response, and owner re-review request.
- `Reproducibility Packet/scripts/audit_template_library.py` — corrected interpretation/documentation.
- `Reproducibility Packet/results/template_audit_2026-08-11.txt` — regenerated against the unchanged pinned live snapshot.
- `README.md` — live framing narrowed; append-only public correction/review heartbeat added.
- `agents/Codex/Session Summaries/HumanReport2.md` — permanent detailed report.
- `agents/Codex/README.md` — workspace map/current state refreshed.

Validation passed: `git diff --check` (line-ending warnings only), exactly 15 Claim Sheet slots, script compile/help, full metadata rerun, and append-only chat tail assertions.

No heavy compute, dependency install, raw-recording download, or sorter run occurred. No new source was added to `agents/Codex/references.md`.

## What Codex should do next

1. Read Claude's latest report and the physical tail of the Claim Sheet review chat.
2. Recompute the Claim Sheet hash before relying on the Session 2 approval. If Claude changed it, review the new exact state; do not carry approval forward.
3. If Claude explicitly approves the Session 2 state, review the Accessible Claim Sheet and Study Guide Pass 1 only after their owner handoffs, reading each required playbook first.
4. Do not start Rung 0 until Phase 1 artifacts/labor converge and the turn returns to Codex.
5. Immediately before any heavy pilot, measure live RAM and VRAM. Use only `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; pin dependencies at first install.
