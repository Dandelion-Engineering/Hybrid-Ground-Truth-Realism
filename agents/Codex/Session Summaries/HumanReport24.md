# Human Report 24 — Codex

**Date and time:** 2026-08-14 22:15 PDT

**Phase:** 2 — Execution

**Session type:** RC-001 Round-1 full-artifact review; count-based progress report; review-method consensus proposal

## Summary

I completed the first formal Round 1 under the director's new bounded review method. The candidate was Review Card RC-001: §16 of Claude's Tier A host-selection artifact, the band-drift estimator, and its synthetic harness. All three handed-off hashes matched before review, and the declared tests all passed. An independently written reviewer probe also confirmed the implementation's ordinary observed, null, mutation-safety, bin-edge and gate behaviour.

The candidate nevertheless receives **Revisions Required, not approval**. The full pass found two blockers and one non-blocking wording issue:

1. Ten one-minute bin medians do not measure the worst excursion inside an actual ten-minute segment. A smooth common ramp moves 21 µm in ten minutes while the implementation reports `Delta_10 = 18.900 µm`, obtains `Q95_null = 18.682 µm`, and passes the 20 µm gate. A common 30 µm within-bin episode passes at `0/0 µm` and vanishes from every audit output; an off-grid ten-minute segment can span 30 µm while all aligned ten-bin windows report at most 15 µm. These are wrong verdicts on inputs inside the declared parameters, not the already-published label-blind limitation.
2. Draft 22's claim that minority masking gets easier with more units overgeneralizes one fixture. Its 11/21/41 series does not hold the moving fraction fixed, and a genuinely fixed 40% construction reverses the claimed monotonic direction at an admitted seed.
3. The sentence that a sample median's realized value does not move with spike count is literally too strong. The correct invariant is that the statistic does not mechanically accumulate a positive term per spike, unlike the retired path length.

I made no candidate edit because both blockers change numerical or scientific meaning. The exact candidate hashes remain unchanged. The archive-reading CLI and every candidate measurement remain blocked.

In the three-way method chat, I agreed with Claude's implementation readings and proposed an agent-only replacement for escalation: a bounded Convergence Decision; evidence determines what can ship; both agents explicitly agree on the safe terminal action even if they retain different substantive beliefs; one declared successor card is allowed; a second like-for-like non-approval forces a real split or redesign rather than another reset. Claude's response is pending, so I did not change the playbook.

Session 24 also triggered the regular eight-session progress report, which is complete.

## Startup and context

- Read `.agent-turn` first; it named `Codex`.
- Confirmed `.agent-session.lock` was absent, created it, and re-read `.agent-turn`; it still named `Codex`.
- Read `AgentPrompt.md`, all of `Project Details/Project Details.md`, Codex's continuity summary, every relevant chat summary, both active chats, Claude's latest human report, the new Review Card, and the superseding review-cycle playbook.
- Read the research-progress and live-run README playbooks before producing their artifacts.
- The working tree began with one modification in the three-way review-method chat: Randy's newly appended instruction. I preserved it byte-for-byte and appended after it.

## Exact candidate state reviewed

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 22 — `5ca2d6ca188d27ad1cfd9352b9078855815b3fc274eb8cc2773a6e11063f4d1a`
- `Reproducibility Packet/scripts/utils/band_drift.py` — `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063`
- `agents/Claude/tools/test_band_drift.py` — `2117983084ceee241273e355077f8c6792ec60c24e6c0ed44813b3481bcd9c89`

The three states were not edited.

## Validation and independent review evidence

The card's acceptance tests:

- full harness: **86 checks, 0 failed** at the pinned 200 permutations;
- claim probes: **3 of 3 passed**;
- Codex's prior safety probe: both label-set and retained-head-bin counterexamples reproduced to the digit;
- packet runbook checker: **10 of 10 steps** agree with their `--help` examples;
- document curly quotes: eight; harness non-ASCII characters: zero;
- both candidate Python files compile.

New reviewer probe: `agents/Codex/tools/probe_rc001_round1.py`.

- forty randomized observations matched a separately written reference calculation exactly;
- one deterministic nine-permutation null matched an independent seed/binning implementation byte-for-byte;
- exact negative-time and final-edge exclusions matched the declared half-open grid;
- null construction did not mutate caller arrays;
- every strict and relaxed decision-boundary combination matched `delta <= L and q95 <= L`;
- all three temporal counterexamples and the fixed-fraction unit-count counterexample reproduced.

The probe uses synthetic arrays only. No candidate asset or network source was opened.

## Round-1 findings and reasoning

### RC-001-F1 — blocking temporal aggregation mismatch

The specification defines `Delta_10` over ten consecutive 60-second bin medians and then interprets that value as the worst movement inside a ten-minute segment, wherever the segment lands. Those are different objects.

The smooth-ramp counterexample is decisive because it does not depend on abrupt motion or a minority of traces. Five units, 61 bins, 100 spikes per unit per bin, and a shared `2.1 µm/min` ramp satisfy every inclusion rule. An actual 600-second interval spans 21 µm. Ten consecutive bin medians are separated by only nine minutes, so the utility returns 18.9 µm. The deterministic null at the recorded asset/row seeds is 18.682 µm. Both fall below 20 and the gate passes.

The within-bin counterexample shows a second loss mechanism. Four of ten regularly spaced spikes in one bin carry a shared 30 µm level in all five units. The per-bin median remains at baseline, so the band trace, null and all per-unit audit values are zero. This is not IBL estimator bias: the 30 µm values enter the utility and are discarded by the utility's aggregation.

The off-grid counterexample shows why aligned windows do not justify “wherever the segment lands.” A segment beginning 30 seconds into bin 0 and ending 30 seconds into bin 10 contains both a 0 µm and 30 µm level, while every aligned ten-bin window contains at most a 15 µm range. The gate passes at `15/0 µm`.

Any acceptable response must align the estimator's time object with the actual 600-second experiment segment and cover or explicitly gate within-bin and off-grid motion. Merely relabelling `Delta_10` cannot repair the smooth-ramp wrong verdict under the stated purpose.

### RC-001-F2 — blocking unit-count overgeneralization

Draft 22 says masking becomes easier as the band grows “at fixed per-unit noise and a fixed moving fraction,” citing 5/11, 10/21 and 20/41 moving units. Those fractions are 0.4545, 0.4762 and 0.4878, not fixed. More importantly, at an actually fixed 40% fraction and admitted seed 7013, the same construction gives `Delta_10 = 14.891`, `15.532`, and `8.182 µm` at 10, 20 and 40 units. The first transition goes in the opposite direction.

The underlying limitation remains real: a moving minority can be suppressed. What does not survive is a deterministic ordering across candidate unit counts based on one nested fixture. This is the same one-way-overclaim class that dominated the earlier review history.

### RC-001-F3 — tracked wording follow-up

A realized sample median can change when observations are added. The intended distinction is narrower and valid: it does not add each absolute increment, so it has no mechanical positive accumulation with spike count. This wording should travel with the substantive revision.

## Review-method feedback and consensus proposal

I accepted Claude's five relevant judgement calls:

- explicit same-state approval remains required;
- an unchanged sentence made false by a repair is an in-scope regression;
- a repair-created LATE-BLOCKER says it did not previously exist;
- mechanical status is established by effect-preserving evidence, not assertion;
- concluding the superseded in-flight chat was a reasonable application of the transition rule.

Randy asked the agents to replace human escalation because his asynchronous schedule could strand several sessions. I proposed:

1. one agent-only Convergence Decision at an escalation trigger, with each side recording its minimum shippable claim, controlling evidence, strongest contrary evidence and acceptable disposition;
2. evidence rules that prevent an executable counterexample or unresolved blocker from being waved through;
3. terminal action by consensus: `Revisions Required`, `Split/Redesign Required`, or `Approved with Follow-ups`, rather than waiting on the director;
4. one lineage-declared successor card after repair;
5. mandatory split/redesign if a same-purpose successor also closes without approval, preventing infinite card resets.

The playbook remains unchanged until Claude and Codex agree on exact text.

## Public and director communication

- Appended the complete Round-1 ledger to the RC-001 chat using a verified byte-exact prior prefix.
- Updated the Review Card's round log and tracked-follow-up section.
- Appended the convergence proposal to the three-way method chat after preserving Randy's uncommitted message exactly.
- Appended a forward public correction: the prior larger-band direction is one fixture, not a general ordering, and the more important new blocker is the gate's temporal aliasing.
- Wrote `Progress Reports/Progress Report Session 24.md` at the director-facing readability bar.
- No new `director_requests.md` entry is needed; Randy's request already lives in the active three-way chat and has an agent fallback in motion.

## Files created or updated

- `agents/Codex/tools/probe_rc001_round1.py` — created; independent numerical and counterexample probe.
- `Review Cards/RC-001 Tier A Selection Section 16.md` — Round 1 and F3 metadata only.
- `chats/Claude-Codex/Tier A Selection Section 16 Review/Tier A Selection Section 16 Review - Active.md` — Round-1 ledger appended.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — consensus proposal appended after Randy's message.
- `README.md` — one forward public running-log correction appended.
- `agents/Codex/Progress Reports/Progress Report Session 24.md` — created.
- `agents/Codex/Session Summaries/HumanReport24.md` — created.
- `agents/Codex/README.md` — workspace map and current state updated.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten.

## Append-only safeguards

Before appending, the RC-001 transcript was 3,757 bytes with SHA-256 `ac11eeb075fc3e3458eda9d4a1685e476f9d6d0c195290eda58c47c93f5368ef`; the new file's exact first 3,757 bytes reproduce that hash and exactly one Codex Session 24 header was added.

The three-way transcript was 11,295 bytes with SHA-256 `6fc8a3850b6bdff5bb1a2c8c96ed7fe61fb9a20e1a6408cb12d12f0d0be0b96f`; the new file's exact first 11,295 bytes reproduce that hash and exactly one Codex Session 24 header was added. This explicitly preserves Randy's pre-session append.

The public README's prior running log was preserved and extended forward rather than corrected backward.

## Boundaries

No host was pinned. No candidate drift, noise or effective-SNR value was read. No target manifest, donor, host-specific pool, edge table, placement schedule or exact configuration was opened. No dependency was installed. No network or archive/raw-recording read occurred. No Rung 0, generator or sorter run occurred. No scientific result exists.

## Next steps

1. Claude responds to RC-001 F1–F3 as owner. Round 2 is delta-only and verifies those findings plus response-introduced regressions.
2. Claude accepts or minimally revises the convergence proposal. Only after agreement does the accepting agent update the superseding review-cycle playbook.
3. The archive-reading CLI and first candidate measurement remain blocked until RC-001 closes on an explicitly same-state-approved candidate.
4. All later host, placement, matching, balance, generation and execution gates remain separate.
