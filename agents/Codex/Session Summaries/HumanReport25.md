# Human Report 25 — Codex

**Date and time:** 2026-08-15 00:15 PDT
**Phase:** 2 — Execution
**Session type:** RC-001 Round-2 delta-only review; cross-review of Claude Session 25; review-method follow-through

---

## Summary

This session completed Codex's Round-2 review of RC-001, covering §16 of the Tier A host-selection strategy, the shipped band-drift utility, and its synthetic harness. The review stayed inside the new method's delta-only boundary: the three Round-1 findings and regressions introduced by Claude's response.

Claude's main numerical repair is correct. Moving the gate from ten to eleven consecutive one-minute summaries now covers both failures Codex found in Round 1: ten bin medians span only nine minutes between their extremes, and an off-grid 600-second segment can touch eleven grid bins. The repaired utility rejects the 21 µm smooth ramp and the 30 µm off-grid level construction that the old state passed. Claude also correctly withdrew the unsupported unit-count direction and repaired the sample-median wording.

RC-001 nevertheless remains **Revisions Required**. Claude's response turned one valid point-mass synthetic fixture into a universal statement that any displacement affecting fewer than half of a bin's spikes leaves the sample median exactly fixed. That is false when the spike depths already present in the bin are heterogeneous. In a deterministic admitted fixture, shifting 49% of the spikes by 30 µm moves the median by 29 µm and puts the implemented statistic above the strict gate. This is a blocking response regression because the prose and module docstring now contradict the shipped implementation on a constructible input inside the declared parameter space. It is not a pre-existing LATE-BLOCKER: the hard cutoff was introduced by the Round-2 response.

No candidate or archive was read. No host is pinned, no donor is selected, no execution authorization moved, and no scientific result exists.

## Work completed

### 1. Startup and required context

- `.agent-turn` named Codex and no `.agent-session.lock` existed.
- Created the lock atomically, re-read `.agent-turn`, and confirmed it still named Codex before opening `AgentPrompt.md`.
- Read all of `Project Details/Project Details.md`, Codex's continuity summary, every Codex-including chat summary and active transcript, Claude's latest report, the superseding review-cycle playbook, and RC-001.
- Read Claude's returned exact states and verified the owner-handoff SHA-256 values before reviewing them.

### 2. Review-method cross-review

Accepted both of Claude's applications of the agreed convergence rule:

1. both agents' Convergence Decision statements and terminal disposition belong in the Review Card;
2. director-only questions retain the existing non-blocking `director_requests.md` route and do not become ordinary review outcomes.

One stale quality-checklist line still said that a second late blocker or post-Round-2 blocker went to “human triage or a split,” contradicting the new agent-only rule. Corrected it mechanically to the Convergence Decision. No consensus clause changed.

RC-001 also carried a stale statement immediately after the Round-2 table saying the utility was unchanged Draft 21 bytes. Corrected it to distinguish the unchanged Round-1 state from Draft 23's substantive eleven-bin implementation.

### 3. RC-001 Round-2 findings

#### RC-001-F1 — numerical repair verified; declared boundary not verified

The implementation's only executable change is `PARAMS["window_bins"] = 11`; the remainder of the utility change is documentation. Independent results:

- common 2.1 µm/min ramp: `Delta_10min = 21.000 µm`, `Q95_null = 18.717 µm`; strict gate now fails;
- off-grid levels `[0, 15 × 9, 30, 15]`: `Delta_10min = 30.000 µm`, `Q95_null = 0`; strict gate now fails;
- forty randomized measurable observations matched an independently written reference exactly;
- a nine-permutation null matched an independently replayed seed/binning implementation byte-for-byte;
- caller arrays remained unchanged and every decision-boundary quadrant matched the declared two-number rule.

The owner's equal-baseline within-bin fixture remains valid: a 30 µm episode affecting 49% of identical depths is erased and passes at `0/0 µm`. What fails is the response's promotion of that result into a general property.

#### RC-001-F1-R1 — blocking response regression

Constructed five identical unit traces with 31 full bins and 100 spikes per unit/bin. Every ordinary bin used depths:

`[0 × 49, 1 × 2, 100 × 49]`

In one bin, the first 49 depths were shifted by `+30 µm`. The unaffected median is `1 µm`; the affected median is `30 µm`; the shipped utility reports `Delta_10min = 29.000 µm`. All units and bins satisfy the declared floors.

This directly contradicts Draft 23's statements that a sub-half-bin displacement leaves the median exactly fixed, that the gate is categorically blind below one half, and that the `0/15/30 µm` transition is a property of the median rather than of the specific point-mass fixture. The safe general statement is narrower: sub-minute movement has no guaranteed detectability under bin medians, and how much is transmitted depends on the within-bin depth distribution and episode timing. `Delta_10min` remains not a bound on sub-minute motion.

#### RC-001-F2 — verified

At a genuinely fixed 40% moving fraction and seed 7025, the admitted construction reports `12.192`, `11.529`, and `14.190 µm` at 10, 20, and 40 units. The direction is not monotone. Claude's withdrawal is therefore correct. The replacement 41-unit masking fixture passes at `Delta_10min = 14.941 µm` and `Q95_null = 7.125 µm` while making no unit-count claim.

#### RC-001-F3 — verified and closed as a follow-up

The document now says that adding observations can move a realized sample median, while a median cannot mechanically accumulate one positive term per spike as the retired path-length quantity does. That is the required narrower invariant.

### 4. Mechanical candidate and probe maintenance

Corrected two reciprocal typos in Claude's selection document from `9/10` to `10/9`; this cannot change a consumer, scientific claim, parameter, branch or output. The reviewer-state selection-document SHA-256 is:

- `90aebcb50a7cb6da50773519d41295b6a0ed4f22f76d978b123fddb8145ddf01`

The returned implementation states remain:

- `band_drift.py`: `4ac9fa56dc7a2035d1f9b037b9010ae448fc1c621f92ea93876db1c1fc06ab19`
- `test_band_drift.py`: `e2e63a037ee81886b01779535c22ce296502bc3a132ee3f77f9ad6f345869420`

Updated Codex's two independent probes from the retired `Delta_10` name/ten-bin expectations to `Delta_10min`/eleven-bin behavior. `probe_rc001_round1.py` now permanently carries the heterogeneous 49% counterexample and passes all twelve independent checks at SHA-256 `a29144e247ec5a845bb67699b9e8f5d6a4c89ab3d5458743254e2f223dae33cc`. The safety probe uses the renamed output labels and remains behaviorally unchanged at SHA-256 `d1c9220dc0f0890744d920638210f501abdc9b53b84256ef89afbc59e6bca6ac`.

### 5. Validation

- owner harness: **96/96** checks at the pinned 200 permutations;
- claim probes: **3/3**;
- Codex safety counterexamples: both reproduce, with the moving-only value now `27.273 µm` and the expanded set still passing at `0/0 µm`;
- packet runbook checker: **10/10** steps;
- updated Codex independent probe: **12/12** checks;
- append-only RC-001 chat: prior 17,708-byte prefix preserved exactly, one Codex Session 25 header after the prior 104 lines;
- append-only three-way method chat: prior 20,453-byte prefix preserved exactly, one Codex Session 25 header after the prior 154 lines.

### 6. Public and collaboration records

- Updated RC-001 with the Round-2 verification, exact mechanical state, blocking response regression, and current `Revisions Required` disposition.
- Appended the exact verdict to the RC-001 chat.
- Appended acceptance of the two convergence applications and the live method evidence to the three-way chat.
- Added a lean forward correction to the public README: the eleven-summary repair holds, but the public entry's universal half-minute cutoff is withdrawn. The project remains `In Progress` and has no result.

## Challenges and reasoning

The main challenge was separating a valid fixture from a valid theorem. Claude's `0/15/30 µm` sweep is correct for the arrays it constructs, where all unaffected within-bin depths are identical. But a sample median depends on order statistics, not only on what fraction of values is shifted. A counterexample had to preserve the declared unit/bin/spike floors and change only the baseline depth distribution; doing so produced a verdict-changing 29 µm response at a 49% shifted fraction.

The finding belongs in Round 2 because the hard cutoff was introduced by the response. It is not a new full-artifact issue and not a missed Round-1 blocker. That distinction is important evidence that the new review method is working as intended: the review stayed delta-only and still caught a regression created by the repair.

## Machine state

Measured at 2026-08-15 00:15 PDT, after the checks:

- system RAM: **0.98 GiB free of 31.67 GiB**;
- GPU memory: **1,089 MiB used of 16,311 MiB**.

No heavy work ran. The low free RAM would have forbidden any sorter, full recording, batch, archive load or other heavy step under the project's admission rule. This session used only documentation reads, small deterministic NumPy fixtures, the existing 48-second harness, and short probes.

## Files created or updated

- `agents/Codex/Session Summaries/HumanReport25.md` — this report.
- `agents/Codex/tools/probe_rc001_round1.py` — eleven-bin reference update plus the permanent response-regression counterexample.
- `agents/Codex/tools/probe_draft16_safety_claims.py` — `Delta_10min` naming update.
- `agents/Claude/Tier A Host and Injection Zone Selection.md` — two mechanical reciprocal corrections only.
- `Review Cards/RC-001 Tier A Selection Section 16.md` — Round-2 evidence and disposition.
- `Playbooks/review-cycle.md` — one mechanical convergence-checklist correction.
- `chats/Claude-Codex/Tier A Selection Section 16 Review/Tier A Selection Section 16 Review - Active.md` — append-only Round-2 verdict.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — append-only method response.
- `README.md` — current public forward correction and date.
- `agents/Codex/README.md` and `agents/Codex/Summary of Only Necessary Context.md` — closeout navigation and continuity refresh.

## Next steps

1. Claude performs the Round-3 owner response, constraining the half-bin sweep to its fixture and replacing the universal cutoff in the selection document, module docstring, harness labels, Review Card, and public wording as needed.
2. Codex performs the final exact-state delta verification. If both agents do not approve the same state at that limit, run the agent-only Convergence Decision; do not park on Randy.
3. Keep the archive-reading CLI and every candidate measurement blocked until RC-001 closes with explicit same-state approval.
4. After RC-001 closes, the archive-reading CLI receives its own Review Card before any candidate is read.
5. No count-based progress report is due until Codex Session 32.

Nothing in this session is waiting on Randy.
