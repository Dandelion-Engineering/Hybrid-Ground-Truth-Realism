# Human Report 11 — Codex

**Current date and time:** 2026-08-12 19:11 PDT

**Session:** Codex Session 11

**Phase at start:** Phase 2 — Execution. Amendments 1–4 `In force`; Amendment 5 `Proposed` at Claude's Session 11 owner-re-review state. No host pinned, no Rung 0, no generator or sorter run.

**Phase at end:** Phase 2 — Execution. **Amendment 5 is `In force`.** The real-arm matching-rule lane is open, but no rule, host, exact host-dependent configuration, generation or sorter execution is approved.

**Progress-report trigger:** Amendment 5 entered force in this session, so `Progress Reports/Progress Report Amendment Real Control Donor Exclusion.md` was created in addition to this normal session report.

---

## Summary

This session completed the exact-state review Claude handed back, accepted all three additions unchanged, and put Amendment 5 into force. The amendment removes the injection zone's donors from the real Tier A control before matching, but requires the eventual frozen matching rule to show the cost by running on both the un-removed and post-removal pools. Only post-removal may govern generation.

The review also approved Claude's Draft 7 §14, which independently re-derived the corrected no-reuse expectation and found the contract consequence that made the extra round necessary: Amendment 5 makes one sentence in already-in-force Amendment 3 false. The fix is a narrow dated supersession, not a rewrite of history.

The required recent-work cross-review found one separate defect in the new Reproducibility Packet documentation. Its runbook said a validator checks the newly derived anatomical label map against the donor library. The code intentionally does not do that, because it would be circular. It checks the pre-existing hand-authored core map and the shared depth coordinate. I corrected the runbook and data guide, opened a dedicated packet review chat, and handed the exact states to Claude for genuine owner re-review.

No scientific execution occurred. No result exists.

## 1. Startup and context

`.agent-turn` named Codex and `.agent-session.lock` did not exist. I created the lock, re-read the turn, confirmed Codex still owned it, then followed `AgentPrompt.md` in order: Project Details, Codex continuity, every chat summary including Codex, and every active chat including Codex before replying.

The active Tier A thread ended at Claude Session 11's handoff of:

- `Claim Sheet.md` SHA-256 `d536b7d3f5d0c14015084c0ef5054bd7a5525ad6a22acc4d23f6bdcc480f698a`
- `Accessible Claim Sheet.md` SHA-256 `4eb76bafe4b60abc6af40f7ad3623e61a301386ec9eaaaf9c976ad6e7a84d9a0`
- `agents/Claude/Tier A Host and Injection Zone Selection.md` SHA-256 `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01`

The on-disk hashes matched exactly before review.

## 2. Amendment 5 exact-state verdict

Claude accepted Codex Session 10's two substantive repairs and added three clarifications:

1. caliper counts now carry caliper-specific expectations;
2. paired 0.11 and unpaired 0.12 are identified as different sampling models rather than competing estimates;
3. Amendment 5 explicitly supersedes the one Amendment 3 clause it makes false.

All three pass.

The supersession is load-bearing. Amendment 3 says its pseudo band does not mirror chance injection-zone donors the real control may contain. Amendment 5 removes those donors from the real control, making the real post-removal pool and shared pseudo-base pool the same object on zone membership. Leaving the old sentence operative would imply the opposite of Slot 13.11. The new paragraph retires only that clause from Amendment 5's date; it preserves the rest of Amendment 3's limitation, especially that no no-manipulation control can reproduce the matched arm's region homogeneity.

I explicitly approved the exact handoff hashes in the active chat. After closing the same-state review, I changed only Amendment 5's status/history lines to `In force`. Current synchronized hashes are:

- `Claim Sheet.md`: `ac089232851705be86e8674987f29afd7fa553e0e55e08049868761549465b28`
- `Accessible Claim Sheet.md`: `8bae94bcc84928766214fea64eba234af6a524804afe11bd7eb16504d265c17f`

Amendments 1–5 are now in force.

## 3. Numerical and code verification

The zone-neighbour audit was run offline against the pinned template snapshot. It reproduced:

| pool | zone templates | nearest-unused realized / expected | exact-insertion realized / expected |
|---|---:|---:|---:|
| all NP1.0 | 16 of 2,183 | 3 / 0.11 | 8 / 1.03 |
| provisional caliper | 12 of 1,149 | 2 / 0.12 | 5 / 1.17 |

An independent unpaired calculation reproduced expected zone count `0.117270` and P(at least one) `0.111401`, confirming the “about one arm in nine” statement and its distinction from the paired no-self/no-reuse baseline.

All 17 Python files under `Reproducibility Packet/scripts/` parsed with the project venv. No dependency changed. `git diff --check` passed.

## 4. What Amendment 5 authorizes—and does not

The matching-rule lane may begin. Nothing further is implied.

The rule must be fixed before the eligible pool is visible, contain no region term in either direction, and declare its objective, deterministic behavior, provenance blocking/fallbacks, failure cases and relaxation reporting. It must later produce locked results on both un-removed and post-removal pools, with only the latter executable.

Still separate:

- matching-rule same-state approval;
- pinned-host selection;
- host-dependent exact configuration for the real and pseudo selectors;
- immediate Rung 0 RAM/VRAM admission;
- Slot 11.3 manipulation and nuisance-balance approval;
- generation;
- sorter execution.

No host was pinned and no execution authorization was consumed.

## 5. Reproducibility Packet cross-review and correction

Claude Session 11 created the packet's self-contained runbook, data guide, pinned dependency list and packet-local ignore rules. The report states—and the documents preserve—the correct current boundary: five offline design-stage steps reproduced tracked outputs in a copied fresh environment; five archive-reading steps were not re-run; the Slot 8 result verifier does not exist because results do not exist.

One public claim was wrong. The runbook's Step 5 said `validate_ccf_label_map.py` validates the newly derived bridge against the donor library. Reading the code shows it calls `to_acronym(location)` without `include_derived=True`. The validator therefore checks the hand-authored map and whether donor `depth_along_probe` and NWB `rel_y` share a coordinate. The project deliberately avoids claiming that derived entries were validated against the same votes that created them.

I corrected:

- `Reproducibility Packet/README.md` — current SHA-256 `1a32418c7cd3a32ecf4f6ef2960dcbf48beae45e4cd9d3b2ea2e071fdc434cf1`
- `Reproducibility Packet/DATA.md` — current SHA-256 `f8c6ce266f368e0efe6d2ecaafbeca09813d2420acd27999433cd61c0c435e09`

No script, command, result, dependency or licence changed. I opened `chats/Claude-Codex/Reproducibility Packet Review/` and explicitly approved/handed back those exact document states. Claude owner re-review remains open.

## 6. Append-only and public-state handling

Before appending to the Tier A active chat, I read its UTF-8 physical tail and recorded 707 lines. The append used the verified EOF anchor, the Session 11 header occurs exactly once after the old boundary, the old prefix was preserved, and the file now ends at 736 lines.

The root public README received one lean event entry: Amendment 5 is in force, the cost must still be reported under the frozen rule, and the matching rule/host/generation/result remain open. Its orientation now says Amendments 1–5 are in force.

The Amendment 5 event-triggered progress report explains the decision in plain language, the paired-versus-unpaired expectations, the required before/after counterfactual, the explicit supersession and the still-open gates.

## 7. Machine state and execution boundary

Measured at 2026-08-12 19:11 PDT:

- free RAM: 12.59 GiB of 31.67 GiB;
- GPU memory used: 989 MiB of 16,311 MiB;
- free `C:` space: 600.3 GB.

Nothing heavy ran. The only execution was an offline stdlib donor-table audit, arithmetic, source parsing and repository validation. No raw recording, template array, generator, sorter or Rung 0 run occurred.

## 8. Files created or updated

**Created**

- `agents/Codex/Progress Reports/Progress Report Amendment Real Control Donor Exclusion.md`
- `agents/Codex/Session Summaries/HumanReport11.md`
- `chats/Claude-Codex/Reproducibility Packet Review/Reproducibility Packet Review - Active.md`

**Updated**

- `Claim Sheet.md`
- `Accessible Claim Sheet.md`
- `Reproducibility Packet/README.md`
- `Reproducibility Packet/DATA.md`
- `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No packet Python source, tracked numerical result, dependency pin, director request or reference entry changed.

## 9. Next steps

1. Claude should genuinely re-review the packet README/DATA correction and approve the exact hashes or return a new state.
2. Codex can then write the real-arm matching rule under Amendments 2 and 5, before inspecting any host-specific eligible pool.
3. Keep that rule's review separate from host selection, exact configuration, manipulation/balance approval and execution.
4. Do not pin a host or start Rung 0 until every prerequisite and immediate daytime resource guard passes.
