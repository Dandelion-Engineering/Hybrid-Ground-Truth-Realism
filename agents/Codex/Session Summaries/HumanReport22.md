# Human Report 22 — Codex

**Date and time:** 2026-08-14 06:16 PDT
**Phase:** 2 — Execution
**Session type:** Exact-state review of Claude Draft 18 and direct repair of the per-unit drift audit

---

## Summary

Claude handed back three owner-approved states: host-selection Draft 18, the reopened band-drift utility, and its synthetic harness. I verified all three hashes before opening them, re-read the full active review context and §§15–16, read Claude's `HumanReport22.md`, and reran the implementation evidence instead of accepting the handoff's reported outputs.

Draft 18 correctly removed two remaining one-way safety claims and correctly required per-unit audit values for a limitation the band median can hide. I nevertheless blocked Draft 18 unchanged for two exact-state defects:

1. Its only ten-bin per-unit value was evaluated inside the band-selected worst window. When the band trace is flat because a moving minority is suppressed, that selected window can be an arbitrary earliest tie and can point the audit away from the movement it exists to expose.
2. Draft 18 claimed that no existing return value changed, even though it intentionally changed five outward-facing reason/error strings from “complete” to “analysed.” The vocabulary repair is correct, but those strings are return/error values; the accurate compatibility claim is about numerical and decision outputs.

I directly repaired the artifact, utility and harness and explicitly approved the resulting Draft 19 exact states. No gate parameter, statistic, threshold, seed, ordering, decision branch or verdict changed. Section 16 and both implementation states remain open pending Claude's genuine owner re-review. The archive-reading CLI remains forbidden, and no candidate was read.

**No host is pinned. No candidate drift, noise or effective-SNR value exists. No target manifest, donor selection, dependency installation, network/archive/raw-data read, Rung 0, generator or sorter run occurred. No scientific result exists.**

## Work completed

### 1. Startup and context-first review

- Read the automation memory, then `.agent-turn`; it named `Codex`.
- Confirmed `.agent-session.lock` was absent, created it, and re-read `.agent-turn`; it still named `Codex`.
- Read `AgentPrompt.md` and all of `Project Details/Project Details.md`.
- Read Codex's continuity, every concluded chat summary that includes Codex, and the entire 1,271-line active Tier A selection transcript before replying.
- Read `Playbooks/review-cycle.md` and `Playbooks/reproducibility-packet.md` before reviewing the handed-off artifact and packet utility.
- Read Claude's latest `HumanReport22.md` and its referenced exact states as the required recent-work cross-review.

### 2. Exact handoff verification

The three handed-off digests matched before review:

- Draft 18: `6c0c04886e99e4093474ea3ddf0aa19b86a79eeb2044f4650ce644adb1360618`;
- `band_drift.py`: `7c74c5e8ab6490e1d680edab53624a879522f6d3e4aa8fa595f32ed51f3f8ca9`;
- `test_band_drift.py`: `ab16c0e1606da4416c87185846fe5f43dd795431105d4bc5ff1180d9536f78f2`.

Before making a decision I reran the handed-off 65-check harness, the three-claim probe, Codex's two safety counterexamples and the ten-step packet runbook checker. Every one passed or reproduced exactly as reported.

### 3. The audit-window defect

Draft 18 reports each included unit's whole-recording excursion and its excursion inside the **band-selected** gating window. That aligned value is useful when the band has a unique worst window, but it does not by itself expose the failure shape Draft 18 is supposed to make checkable.

I constructed a deterministic 20-bin fixture:

- five units stay flat for ten bins and then move 30 µm across the last ten;
- six units stay flat throughout;
- all units satisfy the inclusion and bin-validity rules.

The across-unit median is flat in every bin. Consequently:

- band `Delta_10 = 0`;
- the earliest-tie rule selects window 0;
- all eleven Draft 18 band-aligned unit values are `0`;
- each of the five moving units has an own-worst-window excursion of `30 µm`.

The whole-recording values also show 30 µm, but cannot distinguish this ten-minute event from a slow 30 µm change spread across the session. Draft 18 therefore had not yet made the **gating-scale** conditional checkable.

### 4. Draft 19 repair

Draft 19 preserves three per-unit views, all aligned with the temporally included unit indices:

- whole-recording excursion;
- each unit's own worst ten-bin excursion, its starting bin and its defined-bin support;
- each unit's excursion inside the band-selected window and its defined-bin support.

The own-worst view exposes suppressed movement wherever it occurs; the band-aligned view still shows the composition behind the window that produced the band statistic. A per-unit excursion is `None` rather than a misleading zero if fewer than two defined bin medians exist in the relevant span. The helper fails loudly on malformed window arguments.

All per-unit values remain report-only diagnostics. No gate, label, ordering or verdict reads them. They cannot rescue a rejected candidate, reject a passing one, or reopen a verdict after values are visible. Any disagreement is published as a limitation, and any future threshold would require the same recorded-turn governance as the rest of §16.7.

### 5. Compatibility claim corrected

I compared the repaired module against the Codex Session 21 utility state from commit `2642ad1` on randomized fixtures. The comparison deliberately separated numerical/decision values from the known wording change:

- 40 observed fixtures matched on every pre-existing numerical and decision key;
- 4 measurable fixtures reproduced their full deterministic nulls exactly;
- 8 deliberately triggered reason strings differed only by `complete` → `analysed`.

The artifact now states that exact boundary. It no longer says no existing return value changed.

### 6. Exact states approved and handed back

I explicitly approved and handed Claude these exact states:

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 19 — SHA-256 `66621494f7aca105cbfd53fd9b170377e2ce6eca911d73547c97d36b95d47890`;
- `Reproducibility Packet/scripts/utils/band_drift.py` — SHA-256 `28154cfff9b8c6b5aaa082de699650b3b11bec3804c155b0886f705bbb3f2c75`;
- `agents/Claude/tools/test_band_drift.py` — SHA-256 `ff852682ecee5abb45a1419908a114566488bdafdb2094521fdb664baf853a70`.

This does not close the review cycle. Claude must re-open and approve these exact bytes or edit and return new states. The new issue concerns the scope of a newly added audit, not a repeated disagreement over an earlier repair, so no specific dispute exists to escalate.

### 7. Public heartbeat and append-only record

The root public README received one lean forward correction: the earlier per-neuron audit could look in the wrong ten-minute window when the band median is flat, and the repaired report now preserves both each neuron's own worst window and the band-aligned view. It remains explicitly no-result-bounded.

The active chat append passed the physical-tail safeguards:

- pre-write: 184,810 bytes, 1,271 lines, SHA-256 `59dbe4fd1a5243e074f7724226b5dd1e34d83462de1145ab4db5c3bbcf44e9a9`;
- that exact byte sequence remains the prefix after the append;
- the Codex Session 22 header occurs exactly once and only after the old EOF;
- the file decodes as strict UTF-8 and the new tail was read back.

## Validation

- `agents/Claude/tools/test_band_drift.py`: **71 checks, 0 failed** at the pinned 200 permutations.
- `agents/Claude/tools/probe_band_drift_claims.py`: **3 of 3 probes passed**.
- `agents/Codex/tools/probe_draft16_safety_claims.py`: both earlier counterexamples reproduce to the digit against the repaired module.
- Randomized legacy-equivalence probe: **40 observed fixtures exact on prior numerical/decision keys; 4 deterministic nulls exact; 8 reason-only vocabulary updates as declared**.
- `Reproducibility Packet/scripts/check_runbook_consistency.py`: **10 of 10 steps agree**.
- All packet Python sources compile in the project virtual environment.
- `git diff --check` passed before closeout.
- No dependency was installed and no network, archive or raw-data read occurred.

## Challenges and reasoning

**Avoiding an audit that became a post-hoc gate.** The own-worst value is the right quantity for exposing a ten-minute event suppressed outside the band-selected window, but it would become a new selector if a later session interpreted it as a threshold. The repair therefore adds visibility and pins non-consumption in the same change. The result stays governed by the already-declared band statistic; the audit only makes its limitation observable.

**Preserving the useful part of Claude's design.** Replacing the aligned unit value with each unit's own worst window would have lost the decomposition of the band-selected window. Draft 19 keeps both rather than trading one blind spot for another.

**Separating numerical compatibility from textual compatibility.** The earlier reason-string rename was intentional and correct, but “no existing return value changed” was still false. The randomized comparison now establishes the narrower statement the artifact actually needs: numerical and decision outputs are unchanged, and reason strings changed exactly where declared.

## Files created or updated

| Path | Change |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 19 direct repair and exact-state handoff. |
| `Reproducibility Packet/scripts/utils/band_drift.py` | Added own-worst and band-aligned per-unit audit outputs, start/support fields and input validation; no gate change. |
| `agents/Claude/tools/test_band_drift.py` | Added the localized minority-motion fixture and malformed-window check; 71 checks total. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only exact-state review and handoff. |
| `README.md` | Lean forward public correction, no-result-bounded. |
| `agents/Codex/Session Summaries/HumanReport22.md` | This report. |
| `agents/Codex/README.md` | Workspace map and current review state refreshed. |
| `agents/Codex/Summary of Only Necessary Context.md` | Completely rewritten for Codex Session 23. |

No progress report was due: this is Codex Session 22, no phase changed and no Claim Sheet amendment entered force.

## Machine state

Measured at 2026-08-14 06:16 PDT: **0.92 GiB RAM free of 31.67 GiB; 1,036 MiB GPU memory used of 16,311 MiB; 582.8 GiB free on `C:`.** Nothing heavy ran. At 0.92 GiB free, nothing heavy should run; this measurement is a momentary diagnostic and not later authorization.

## Next steps

1. Claude genuinely owner-reviews Draft 19 and both implementation hashes.
2. If Claude approves those exact bytes, §16 and the numerical utility/harness loop close.
3. Only then may Claude write the archive-reading CLI and its scoped packet step/review; the CLI must itself be approved before candidate measurement.
4. Only after that separate approval may rank 1 be read for a drift value.
5. Noise, post-rescaling effective SNR, exposure-schedule/placement, matcher implementation, target manifest, joint placement, balance/manipulation, generation and Rung 0 remain separate gates.
