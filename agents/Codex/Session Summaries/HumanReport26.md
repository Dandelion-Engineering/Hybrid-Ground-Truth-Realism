# Human Report 26 — Codex

**Date and time:** 2026-08-15 02:17 PDT
**Phase:** 2 — Execution
**Session type:** RC-001 Round-3 final delta-only review; exact-state approval; first Review Card closeout

---

## Summary

This session completed the final Round-3 review of RC-001, covering §16 of Claude's Tier A host-selection strategy, the band-drift estimator that implements it, and the owner's synthetic harness. The returned bytes resolve the one remaining response regression: Draft 23's universal claim that a displacement affecting fewer than half of a one-minute bin's spikes cannot move the bin median.

Draft 24 correctly withdraws that cutoff instead of moving it. It scopes the old `0/15/30 µm` sweep to the equal-baseline fixture that produced it and states the general boundary in both directions: how much sub-minute movement reaches a bin median depends on the within-bin rank distribution and on where the episode falls on the minute grid. The statistic therefore does not bound sub-minute motion and is not reliably blind to it either. Neither direction is promoted into a safety guarantee.

The exact returned state passed the complete acceptance suite and a new independent exhaustive check of the replacement rank/offset bound. **Codex explicitly approves the same three candidate states Claude approved. RC-001 is closed `Approved`; no Convergence Decision was needed.**

No archive, candidate or raw data was read. No host is pinned, no target manifest or donor exists, no execution authorization moved, and no scientific result exists.

## Exact approved state

| File | SHA-256 |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 24 | `c35987fecc02b020bb393aed1e47a2bbb143a0028ccd759153deea3584b6de09` |
| `Reproducibility Packet/scripts/utils/band_drift.py` | `eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` |
| `agents/Claude/tools/test_band_drift.py` | `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` |

The estimator's Round-2 and Round-3 states have identical docstring-stripped executable syntax trees. Draft 24 changes the module documentation, not a parameter, threshold, seed, return key, verdict path, error string or numerical branch.

## Work completed

### 1. Startup and required context

- `.agent-turn` named Codex and no `.agent-session.lock` existed.
- Created the lock, re-read `.agent-turn`, and confirmed it still named Codex before entering `AgentPrompt.md`.
- Read all project details, Codex continuity, every Codex-including chat summary and active transcript, Claude's latest report, the superseding review playbook, RC-001, the three returned candidate files, the public README playbook, and the relevant live records.
- Verified the three owner-returned SHA-256 values before reviewing the delta.

### 2. Round-3 delta verification

The review stayed within the F1-R1 repair and regressions introduced by it. It did not reopen unchanged §16 material.

The repair is scientifically and mechanically sound:

- the universal half-bin cutoff is removed from §16.4, the status trail, the Draft 23 note, and the estimator docstring;
- the equal-baseline sweep remains a valid fixture result rather than a theorem about medians;
- the heterogeneous construction still reports `29.000 µm` at 2%, 10%, 30% and 49% displaced, and `14.500 µm` for one displaced spike in 100;
- moving the same count of equal-baseline episode spikes inside one bin versus splitting them across two bins reports `30.000 µm` versus `0.000 µm`, demonstrating the grid-placement dependency;
- upward movement cannot lower the median and is bounded by the common offset and the surviving order-statistic ranks; the downward case follows by negation and is also measured directly;
- the text does not claim that either missed or transmitted brief movement has a one-way safety direction.

No repair-created regression, late blocker or new tracked follow-up was found.

### 3. Independent evidence

Codex extended `agents/Codex/tools/probe_rc001_round1.py` with an independent exhaustive check rather than relying only on the owner's randomized fixture. Across sample sizes one through seven, every nondecreasing multiset drawn from four depth levels, every moved subset, and four upward offsets were checked: **93,184 depth/mask/offset cases**, with no negative median move and no violation of the rank/offset bound.

The updated Codex probe passes thirteen checks with zero failures at SHA-256 `491239808ee4cf3b0d04a0858a795a87647fdf16de4779ac3b39248fbdbf59bc`.

### 4. Complete validation

- owner synthetic harness: **103/103** checks at the pinned 200 permutations;
- owner claim probes: **3/3**;
- Codex independent probe: thirteen checks, zero failures, including the 93,184-case exhaustive bound check;
- Codex safety probe: prior counterexamples reproduce at `7.966/8.346 µm` and `27.273/11.591 µm`;
- packet runbook consistency checker: **10/10** steps;
- changed Python sources and Codex probes compile;
- Round-2 versus Round-3 utility states: identical docstring-stripped executable ASTs;
- exact candidate hashes match the Review Card;
- `band_drift.py` and the owner harness remain ASCII with LF line endings.

### 5. Review-method result

The first live Review Card closed at its third-round limit without relying on the limit to manufacture approval.

- Round 1's purpose-led full pass found that ten one-minute medians did not implement a ten-minute quantity.
- Round 2's delta focus caught the universal half-bin cutoff created by the repair.
- Round 3 concentrated review on the replacement bound, which survived both the owner suite and independent exhaustive evidence.

The method therefore delivered a bounded review with stronger repair checking and no director dependency. The next archive-reading implementation begins a new card rather than extending RC-001. Feedback was appended to the three-way method chat, which remains active at Randy's request.

### 6. Collaboration and public records

- Updated RC-001's status, round log, exact evidence, final outcome and closed follow-up.
- Updated the Review Cards index to `Approved — closed 2026-08-15`.
- Appended the final exact-state approval to the RC-001 chat, concluded that chat, and created its `Summary.md`.
- Appended the first live-card outcome and method assessment to the active Claude-Codex-Human review-method chat.
- Added a lean public README entry: the bounded review closed, the cutoff is gone, the replacement bound is verified, and no real recording or result exists.

## Challenge and correction

The first RC-001 approval append matched an earlier repeated footer and landed before Claude's final response instead of at the physical end of the transcript. The post-write prefix/header check caught this immediately. Because the transcript is append-only, the misplaced message was not removed or rewritten. A dated physical-EOF correction records the ordering defect, re-states the exact approval after Claude's handoff, and identifies itself as the authoritative chronological response. The current transcript preserves the entire pre-correction prefix and ends with the unique correction header.

This was a workflow error, not a scientific-state change. The concluded chat's summary records it explicitly.

## Machine state

At 02:05 PDT, before the acceptance suite, only **0.03 GiB of 31.67 GiB RAM** was free. A process outside this project held substantial memory, so no Python check was started and no process was terminated. At 02:06 PDT free RAM recovered to **2.26 GiB**, enough for the documented tens-of-megabytes harness but not for any gigabyte-scale work. The complete small synthetic suite then ran successfully.

At the final machine measurement, 02:14 PDT:

- RAM: **2.43 GiB free of 31.67 GiB**;
- GPU memory: **1,097 MiB used of 16,311 MiB**;
- `C:` free space: **548.89 GiB**.

No sorter, recording load, archive batch or other heavy step was attempted.

## Files created or updated

- `agents/Codex/Session Summaries/HumanReport26.md` — this report.
- `agents/Codex/tools/probe_rc001_round1.py` — independent exhaustive rank/offset-bound check.
- `Review Cards/RC-001 Tier A Selection Section 16.md` — final verification and `Approved` outcome.
- `Review Cards/README.md` — closed-card index state.
- `chats/Claude-Codex/Tier A Selection Section 16 Review/Tier A Selection Section 16 Review - Concluded.md` — final approval plus physical-EOF ordering correction.
- `chats/Claude-Codex/Tier A Selection Section 16 Review/Summary.md` — concluded-chat summary.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — first live-card result and method feedback.
- `README.md` — public review-close heartbeat.
- `agents/Codex/README.md` and `agents/Codex/Summary of Only Necessary Context.md` — navigation and next-session continuity.

## Next steps

1. Claude owns the next host-selection implementation: the archive-reading CLI and packet step 11. It requires a new Review Card and chat before any candidate is read.
2. Candidate measurement proceeds only after that implementation is same-state approved; the first-admissible pinned order still binds.
3. Exposure schedule/placement, matcher implementation, noise/effective-SNR gates, placement calibration, exact candidate configuration, independent balance/manipulation approval, generation authorization and Rung 0 remain separate gates.
4. Codex's next role is review of the new card or later execution work within the existing labor split. No count-based progress report is due until Session 32.

Nothing in this session is waiting on Randy.
