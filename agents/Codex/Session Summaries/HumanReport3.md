# Human Report 3 — Codex

**Date and time:** 2026-08-11 15:16 PDT

**Session:** Codex Session 3

**Phase at start:** Phase 1 — Sharpening. Claude had edited and re-approved the Claim Sheet after Codex's Session 2 review, and had handed off Study Guide Pass 1 for its first Codex review.

**Phase at end:** Phase 1 — Sharpening. Codex has explicitly approved an edited exact state of both the Claim Sheet and Study Guide Pass 1. Both review loops remain open only because Claude must re-review Codex's edits and explicitly approve the same states. The Accessible Claim Sheet has not yet been written.

---

## Summary

This session completed two linked exact-state reviews: Claude's three follow-on edits to `Claim Sheet.md`, and the first full review of `Study Guide/Pass 1 - Conceptual Foundation.tex` plus its compiled PDF.

The Claim Sheet's substantive additions were sound. Codex accepted the doubled Rung 2 workload caused by sorting the negative-control pseudo-arms, retained the stricter 48 sorter-hour ceiling per candidate per tier, accepted one host/injection zone across tiers as the default, and accepted CA1 as a joint-screen candidate rather than a selected host. Two coherence defects remained and were corrected directly: equal block counts do not guarantee equal precision, and Slot 11's numbered checklist still described the superseded point-estimated-band rule rather than the authoritative `D = |I| − T` interval rule.

The Study Guide had a strong structure, audience fit, and narrative spine, but its technical compression produced several approval-blocking errors. Codex corrected the sign interpretation of the interaction, taught the now-authoritative `D` rule and hierarchical bootstrap rather than an older approximation, narrowed an unsupported claim about SHYBRID's waveform preservation using the paper and primary source code, and restored the Claim Sheet's candidate, manipulation-gate, and claim-boundary language. The PDF was rebuilt twice, rendered page by page, and visually inspected. An initial edit produced a three-line orphan page; the final layout returns to 13 pages without changing margins globally or typography.

Codex explicitly approved the resulting Claim Sheet and Study Guide source/PDF exact states in their append-only review chats. Neither artifact is same-state closed until Claude genuinely re-reviews the reviewer edits and explicitly approves those exact bytes or edits and hands them back.

## Claim Sheet re-review

### Claude's three edits accepted

1. **Negative-control compute was missing from the pilot extrapolation.** The pseudo-arm contrasts require sorter runs, so the minimum tranche is correctly `10 min × 2 arms × 5 blocks × 2 contrast types = 200 recording-minutes per candidate per tier`. The 48-hour admission ceiling remains unchanged. Doubling the workload exposed an omission; it did not create a reason to double the budget. The panel-level projection is also now required, because individually admitted candidates can still form an unaffordable panel.
2. **The `D` interval is the single authoritative comparative rule.** Claude correctly removed the conflicting instruction to compare the marginal interaction interval against a point estimate of `T`, and correctly declared the folded-at-zero conservatism that makes a bounded negative harder to reach.
3. **The host is fixed across tiers by default.** The cross-tier reasoning in Slots 13 and 14 is not interpretable if the recording changes silently. CA1 is correctly named as the only current joint-screen candidate whose Tier C biology and Tier A donor availability overlap on their face, while its worst-case donor count of six keeps it explicitly short of selection.

### Codex's direct edits

- Replaced the claim that equal real and pseudo-arm block counts imply equal precision. They instead establish the same nominal replication basis; the achieved interval widths can differ and must both be reported.
- Replaced the stale item 4 in Slot 11's success checklist. A bounded negative requires the 95% interval for `D = |I| − T` wholly below zero; a bounded positive requires it wholly above zero plus an interaction interval excluding zero.

### Exact-state verdict

`Claim Sheet.md` SHA-256:

`a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3`

**Codex verdict: APPROVE.** The artifact still contains fifteen slots, retains the stricter 48-hour ceiling, and has no unresolved Codex–Claude disagreement. The loop remains open because these reviewer edits sit on top of Claude's approved state.

## Study Guide Pass 1 review

### What was already strong

- The five required Pass 1 sections are present and form a continuous narrative.
- Concepts arrive because the preceding concept creates a need for them; the guide is not a glossary.
- The focus on interaction, gates, pairing, and uncertainty is appropriate for Randy. Omitting sorter-internal implementation detail is the correct trade at this phase because sorter identity is a variable, not the project's subject.
- The mathematics is motivated, defined in plain language, and interpreted after presentation.
- The system view names the load-bearing assumptions rather than merely recapping sections.

### Corrections made

1. **Template definition.** A multichannel template is not only the cell's position relative to the probe; it also reflects cell anatomy, surrounding tissue, and probe geometry. Multi-site density is now described as part of why the problem became hard, not the whole reason.
2. **SHYBRID evidence boundary.** The prior guide said relocation carries the real spike train and unrestricted real spike-to-spike variability. The primary implementation supports a narrower statement: observed spike times are reused after a fixed shift along with per-spike template-fit amplitudes, while the insertion train receives fresh random sub-sample jitter by default. It does not preserve observed timing jitter or transport each full observed waveform shape. The guide and Codex ledger now say exactly that and link both relevant source files.
3. **Tier A engineering language.** "No new code" became "no new generator mechanism." Tier A still requires constrained selection, balance checks, and analysis. The expectation that Tier A moves absolute scores more readily than the sorter interaction is labelled as the project's prior rather than an established fact.
4. **Interaction sign.** For `I = Δ₁ − Δ₂`, a negative value means realism hurt sorter 1 more, not less. The guide's read-aloud sentence had the sign backwards. It now states both directions correctly and no longer says a near-zero interaction validates absolute scores.
5. **Materiality and decision rule.** The half-gap component of `T` is a declared judgement, not a theorem that every half-gap shift changes a reader's choice. The guide now teaches `D = |I| − T`, the positive/negative/inconclusive interval decisions, and why folding at zero makes the negative call conservative.
6. **Bootstrap hierarchy.** Paired unit/donor-slot observations are resampled within blocks while their arm and sorter pairing remains intact; blocks are resampled within hosts; hosts are resampled at the top when widened; repeated donor identities stay clustered; one-host intervals remain conditional on that host.
7. **Candidate and manipulation boundaries.** CA1 remains a candidate whose exact-host donor exclusion, placement, and balance gates are open. A manipulation present below the declared biological range does not pass the biological-realism gate; any later stress-test result is bounded to the achieved magnitude.

### Build and visual verification

- `pdflatex` ran twice successfully.
- No errors, unresolved LaTeX/package warnings, overfull boxes, or underfull boxes.
- Final PDF: 13 letter-sized pages.
- Every final page was rendered to PNG and inspected for clipping, overlap, broken glyphs, margins, section transitions, equations, links, and pagination.
- One intermediate 14-page build left only a few closing lines on the final page. The closing paragraph was tightened and the last page adjusted locally; the final 13-page rendering is clean.

### Exact-state verdict

Source SHA-256:

`37f724699305a7ae578ed6a8f1550161ed376cabe71b9fc85c6f5dcf5f3468d4`

PDF SHA-256:

`b42878216a3154c180875d2bea4426bc12b250da22d12e21e0b7e76a669abf55`

**Codex verdict: APPROVE.** The review loop remains open only because Claude must re-review this edited source/PDF pair.

## Cross-review and source work

Codex read Claude's `HumanReport3.md`, both active review chats, the Claim Sheet, the Study Guide source, the compiled PDF, both Literature Foundations, both source ledgers, and `director_requests.md`. That satisfied the general recent-work cross-review as well as both artifact-specific review cycles.

The SHYBRID correction was checked against the primary article and the public implementation in `hybridizer/spikes.py`. Codex updated its living `references.md` rather than rewriting the dated Phase 0 Literature Foundation.

## Challenges and how they were handled

**The two artifacts had to teach one statistical rule.** Claude had corrected the Claim Sheet's prose to make `D` authoritative, but one numbered checklist item and the Study Guide still taught older approximations. Codex reviewed them as a coupled system and propagated one exact rule across both.

**The Study Guide's simplifications were plausible enough to survive a superficial review.** The SHYBRID claim, interaction read-aloud, and bootstrap explanation all sounded reasonable. Each was checked against either primary source/code or the exact contract rather than against tone. This separated useful compression from false compression.

**The PDF was technically valid before it was visually polished.** The first revised build had zero LaTeX warnings yet produced an orphaned 14th page. Rendering every page caught what the log could not. The final PDF is both technically and visually clean.

**The workspace dependency locator hung.** It was terminated after repeated waits. The already-installed Poppler executables were located directly and used for PDF metadata and rendering; no dependency was installed or changed.

## Files created or updated

| Path | Change |
|---|---|
| `Claim Sheet.md` | Clarified nominal replication versus achieved precision; made the numbered success checklist use the authoritative `D` rule. |
| `Study Guide/Pass 1 - Conceptual Foundation.tex` | Corrected technical compression, interaction sign, decision rule, bootstrap hierarchy, and candidate/gate boundaries; refined final pagination. |
| `Study Guide/Pass 1 - Conceptual Foundation.pdf` | Rebuilt final approved 13-page artifact and visually verified every page. |
| `agents/Codex/references.md` | Added primary SHYBRID source-code evidence and narrowed the preserved-variability claim. |
| `chats/Claude-Codex/Claim Sheet Review/Claim Sheet Review - Active.md` | Appended exact-state review, edits, reasons, and explicit approval. |
| `chats/Claude-Codex/Study Guide Pass 1 Review/Study Guide Pass 1 Review - Active.md` | Appended first Codex review, exact source/PDF hashes, and explicit approval. |
| `agents/Codex/Session Summaries/HumanReport3.md` | This report. |
| `agents/Codex/README.md` | Workspace map and active review state refreshed. |
| `agents/Codex/Summary of Only Necessary Context.md` | Completely rewritten for Session 4. |

## What did not happen

- No sorter run, generator run, raw-recording load, raw-data download, dependency install, or other heavy compute occurred.
- Live RAM/VRAM was not measured because no heavy step was attempted; the contract requires measurement immediately before a heavy step, not as session decoration.
- The root Live-Run README was checked and left unchanged. No artifact or phase finished: both reviews still require Claude's same-state re-approval.
- No progress report was due: this was Codex Session 3 and no phase transition or approved amendment occurred.
- Nothing is blocked on the director. The shared-memory request remains open but non-blocking.

## Next steps

1. Claude genuinely re-reviews `Claim Sheet.md` at hash `a5f586…` and either explicitly approves it or edits and hands it back.
2. Claude genuinely re-reviews the Study Guide source/PDF pair at hashes `37f7246…` / `b428782…` and either explicitly approves them or edits and hands them back.
3. Claude writes the Accessible Claim Sheet against the converged technical state and hands it over for its own review.
4. Phase 1 closes only after same-state approval of the technical Claim Sheet, Accessible Claim Sheet, and Study Guide Pass 1. The closing agent then writes the phase-transition progress report and the Claim-Sheet-ready director request.
5. Rung 0 remains downstream of Phase 1 close. Immediately before it, Codex measures live RAM and VRAM and obeys the declared headroom/admission gates.
