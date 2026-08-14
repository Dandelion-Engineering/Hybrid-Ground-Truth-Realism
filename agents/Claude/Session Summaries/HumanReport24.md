# Human Report 24 — Claude

**Date and time:** 2026-08-14 09:26 PDT
**Phase:** 2 — Execution
**Session type:** Owner re-review of Codex's Draft 21 and its two implementation states; count-based progress report

---

## Summary

Codex handed back three exact states after reviewing my Draft 20: host-selection Draft 21, the band-drift utility, and the synthetic harness. I verified all three SHA-256 digests before opening anything, re-read §§15–16 whole rather than as a diff, read `HumanReport23.md` as the cross-review, and re-ran the shipped validation instead of reading his numbers.

**His blocking correction is accepted in full and kept exactly as written.** Draft 20 had called the band statistic's `Q95_null` "systematically the narrower of the two" against a single unit's noise floor. That was a one-way claim built on one homogeneous noise family, and his heterogeneous counterexample reverses it. The general statement he substituted — the two statistics have no fixed ordering and neither grades the other — is what the evidence supports.

I could not approve Draft 21 unchanged, and the finding follows from his repair rather than objecting to it. **Removing the last yardstick leaves exactly one readable signal in the per-unit audit — a subset separated in magnitude from the rest — and §16.4 was still leaning on that separation to call the label-blind conditional *checkable*.** That claim holds only in the presence direction. I measured the absence direction: a fixture built entirely inside §16.7's own admitted parameters **passes both gate numbers** while ten of its twenty-one units genuinely move 30 µm, their own-worst excursions overlapping the stationary units' and six of the ten sitting inside that range. The masking gets easier as the band grows, and the pinned candidates carry 22 to 267 band units.

Draft 22 narrows the checkability claim to what the values support, states that an absent separation licenses nothing and why, strengthens Codex's own counterexample by showing it does not need its degenerate exactly-flat unit, and makes both new fixtures permanent harness cases at 86 checks. **It edits no utility line at all.**

A count-based progress report was due at Session 24 and is written.

**No host is pinned. No candidate drift, noise or effective-SNR value exists. No target manifest, donor selection, dependency installation, network/archive/raw-data read, Rung 0, generator or sorter run occurred. No scientific result exists.**

---

## Work completed

### 1. Startup and context-first review

- Read `.agent-turn` (named `Claude`), confirmed `.agent-session.lock` absent, created it, re-read `.agent-turn` — still `Claude`.
- Read `AgentPrompt.md` and all of `Project Details/Project Details.md`.
- Read my `Summary of Only Necessary Context.md`, every concluded chat `Summary.md` involving me, and the active Tier A selection transcript's open turns.
- Read `Playbooks/research-progress-report.md` before writing the progress report and `Playbooks/live-run-readme.md` before appending the public log entry.
- Cross-review: read Codex's `HumanReport23.md` and the exact states it names.

### 2. Exact handoff verification, before opening anything

All three digests matched Codex's claim:

- Draft 21: `bd0f678af4d27862d55044be010524782d1d80bb2bccd6a873cc06e70fa3946c`
- `band_drift.py`: `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063`
- `test_band_drift.py`: `fe889703d67b4ee97a9a6a431dbd9dde389216687f07b139db34f0e2df5c317d`

Re-ran rather than read: **79 checks, 0 failed** at the pinned 200 permutations; 3 of 3 claim probes; 10 of 10 runbook steps; Codex's review probe reproducing both counterexamples to the digit (`7.965855925506574` / `8.345705622445344`, and `24.545454545454547` / `11.59090909090909`).

**I also checked his AST claim myself rather than accepting it.** I extracted the Draft 20 module from commit `2dfff44` and compared stripped syntax trees against the working state: identical. His two edits are documentation only, as stated.

### 3. Why Codex was right

`Q95_null` is the permutation noise floor of `D(b)`, a median *across* units. Draft 20 measured, correctly, that on homogeneous no-movement fixtures every per-unit own-worst excursion exceeds it, at 1.62×, 2.13× and 2.76× for the smallest value at 9, 14 and 25 units. Draft 20 then wrote that as a property of the two statistics rather than of that fixture family. Codex's counterexample — one flat unit, four noisy ones — puts a per-unit value at `0 µm` below a `16.598 µm` band null. One counterexample is enough to kill a universal, and the mechanism generalizes: any unit quieter than its neighbours by more than the median's own suppression factor reverses the ordering.

This is the same error I have now made three times in this section: *this mechanism widens it, therefore it always widens*. It is exactly the shape Codex blocked twice in Session 21 and I blocked once in Draft 20.

### 4. The finding — the absence direction was never stated, and it is the direction that matters

Draft 21 correctly says the presence of magnitude separation attributes nothing, because heterogeneous noise produces it too. Nothing said what its **absence** means, and §16.4's operative sentences were still leaning on it: *"The conditional has to be checkable from the published record"*, and *"The failure shape the fixture exhibits has a visible signature … and it is visible in quantities the estimator already computes."*

That visibility is a property of the localized fixture, which I checked rather than assumed — it is built from `linspace` and `zeros`, with no noise term at all.

**Measured, inside §16.7's own admitted parameters.** Twenty-one units on a regular grid at twelve spikes per bin (just above the ten-spike inclusion floor), ten of them ramping 30 µm inside one ten-bin window, all clearing inclusion and bin validity:

| quantity | value |
|---|---|
| band `Delta_10` | `18.136 µm` — **under the 20 µm gate** |
| band `Q95_null` | `10.208 µm` — **under the gate** |
| gate verdict | **passes** |
| moving units' own-worst | `[32.5, 54.0] µm` |
| stationary units' own-worst | `[22.1, 35.6] µm` |
| separated? | **no** — six of ten movers sit inside the stationary range |

Four of five seeds pass; all five overlap. So a genuine 30 µm minority movement — half again the disqualifying threshold — passes the gate with no visible signature in the audit built to expose it.

**The direction of the effect is the substantive part.** At fixed per-unit noise and a fixed moving fraction, the same construction gives `Delta_10` of `21.98`, `18.14` and `14.94 µm` at 11, 21 and 41 units. The across-unit median suppresses a moving minority and its noise together, while a single trace keeps both — so masking gets *easier* as the band grows, and the pinned candidates carry 22 to 267 band units. The highest-yield candidates are simultaneously the most likely to pass and the least auditable.

### 5. The repair, and the option I declined

Draft 22 does three things and no more:

1. **Narrows the checkability claim.** "The conditional has to be *as checkable as the published record can make it*"; the signature *can* carry, with how far it reaches settled in the next paragraph rather than assumed.
2. **States the absence direction with its measurement**, names the unit-count asymmetry, and says explicitly that an audit showing no separation is not evidence the conditional holds — the conditional stays a limitation of the drift result.
3. **Strengthens Codex's counterexample.** A reader can dismiss an exactly-flat unit as degenerate, so I checked whether the reversal needs it: a unit merely three times quieter than its neighbours (6 µm against 18 µm) still sits below the band null, at `11.430 µm` against `17.157 µm`. The reversal is produced by heterogeneity, not by the zero.

**The option I declined:** giving the per-unit values their own null. It would have made them comparable and closed the gap directly. I declined it for the reason S23 declined the same offer — it needs a threshold this project has no basis for, and it would turn an unconsumed diagnostic into a second estimator. Saying what the values cannot support was cheaper and more honest.

**This changes no parameter, threshold, order, statistic or verdict, and it cannot, because §16.4 consumes none of these values.**

### 6. Reading it back caught two defects in my own draft

Per the standing habit of re-reading the finished section as a reviewer:

- The new sentence said the visibility question was settled "two paragraphs below" when the reading-rule paragraph is the immediately following one. Fixed.
- The reading-rule heading still said "the **two** readings that would be wrong" when the absence reading makes three. Fixed.

### 7. Validation after the edits

- Harness: **86 checks, 0 failed** at the pinned 200 permutations, 48 s wall clock (up from 34 s).
- Claim probes: 3 of 3. Codex's safety probe: both counterexamples to the digit.
- Runbook checker: 10 of 10 steps.
- Every packet source compiles; `git diff --check` clean; harness is pure ASCII (0 non-ASCII characters anywhere); document is LF with its curly-quote count unchanged at eight.

### 8. Handed-back exact states

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 22 — `5ca2d6ca188d27ad1cfd9352b9078855815b3fc274eb8cc2773a6e11063f4d1a`
- `Reproducibility Packet/scripts/utils/band_drift.py` — `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063` (**Codex's Draft 21 bytes, unchanged**)
- `agents/Claude/tools/test_band_drift.py` — `2117983084ceee241273e355077f8c6792ec60c24e6c0ed44813b3481bcd9c89`

### 9. Public log and progress report

Appended one running-log entry to the root `README.md` on the safeguard's blind spot and its unit-count direction; the banner already read 2026-08-14 and was not touched. Wrote `agents/Claude/Progress Reports/Progress Report Session 24.md` at the Accessible-Piece bar — the count-based report due at Session 24.

---

## Challenges, and how they were handled

**The finding was nearly not found.** My first pass through Draft 21 produced agreement and nothing else — the repair is correct and the text reads cleanly. What produced the finding was the standing owner-re-review question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* Draft 21 removed the last yardstick, which meant asking what was left, which meant asking what its absence means. Sixth consecutive session in which the extra pass, run on edits I already agreed with, is what produced the finding.

**The first counterexample I built did not establish the claim.** My initial masking fixture (11 units, 28 µm noise) showed the magnitude overlap but *failed* the gate at `Delta_10 = 21.6 µm` — the noise pushed the band over on its own, so it demonstrated nothing about a passing candidate. I swept unit count and noise to find whether the passing regime existed at all rather than reporting the near-miss as if it were the finding. It exists, and it is wide.

**Round-trip count.** This is turn nine on §16. Codex said in Session 23 that a disagreement rather than a finding should go to escalation instead of a tenth turn, and I agree and said so. I also said why I think this one bottoms out: after Draft 22 the section makes no claim about what the per-unit values show in either direction, and a claim that says "this supports nothing on its own" has no next layer to be over-strong in.

---

## Important decisions

1. **Accept Codex's correction whole**, including his wording, and record my own error pattern rather than softening it.
2. **Do not build a per-unit null.** Declare the limit instead.
3. **Edit the earlier operative sentence, not just add a later paragraph.** A governing paragraph does not repair an operative sentence that contradicts it — so §16.4's "checkable" claim itself had to change, not merely be qualified downstream.
4. **Do not touch Codex's utility bytes.** The finding is about the specification's claims, not the code, so the implementation state handed back is his exactly.
5. **Add one public log entry.** The blind spot and its direction are decision-relevant to a stranger reading a future drift result; three prior entries on this chain made me check the bar rather than assume it.

---

## Insights gained

- **A repair that removes a yardstick makes the absence direction load-bearing.** Each repair in this chain created the next layer's gap: a diagnostic, then its time scope, then its reading rule, then that rule's one-way claim, and now the direction the withdrawal exposed. The general lesson is to ask what a repair now *obliges*, not only what it fixed.
- **When a diagnostic's only remaining signal is a pattern, ask what its absence means.** Presence and absence are separate claims and a specification can state one and silently imply the other.
- **A counterexample built on a degenerate case invites dismissal.** Codex's reversal was correct, but resting it on an exactly-flat unit gave a reader an out. Checking whether it needed the degeneracy — it does not — strengthened his finding at the cost of four minutes.
- **The suppression mechanism cuts three ways.** The across-unit median cancels noise (Draft 19's argument), keeps `Q95_null` narrower than a single trace in homogeneous cases (Draft 20's), and hides a moving minority better as the band grows (this session's). Same mechanism, three consequences, and the project had written down two of them as if they were the whole story.

---

## Files created or updated

- `agents/Claude/Tier A Host and Injection Zone Selection.md` — Draft 22 (§16.4 checkability and reading rule; §16.8; status header)
- `agents/Claude/tools/test_band_drift.py` — two new permanent cases, 79 → 86 checks
- `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` — Session 24 handoff appended
- `agents/Claude/Progress Reports/Progress Report Session 24.md` — created
- `agents/Claude/Session Summaries/HumanReport24.md` — this file
- `README.md` — one running-log entry appended
- `agents/Claude/README.md` — updated
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten

**Not touched:** `Claim Sheet.md` and `Accessible Claim Sheet.md` (unchanged, still `2feda611…` / `679918f7…`), `Reproducibility Packet/scripts/utils/band_drift.py` (Codex's Draft 21 bytes), the packet runbook, `references.md` (no external source informed this session).

---

## Machine state

Measured at **2026-08-14 09:07 PDT**, immediately before any work: **RAM 4.47 GiB free of 31.67 (85% in use); VRAM 1,032 MiB used of 16,311; 625.8 GB free on `C:`.** Nothing heavy ran. The harness operates on small synthetic arrays and takes 48 s at 200 permutations; peak footprint is well under a gigabyte. No background job was left running and no temporary directory outside the session scratchpad was created.

---

## Next steps

1. **Codex re-reviews Draft 22 and the two implementation states.** Nothing else is open on either agent.
2. **If it comes back approved, my lane is the archive-reading CLI** — packet step 11, targeted range reads over the ragged `spike_times` and `spike_distances_from_probe_tip_um` slices for band units only, with the four §16.8 confirmations before it computes anything. Only then does rank 1 get measured.
3. **If it comes back as a disagreement rather than a finding, escalate to the director** per the review-cycle playbook rather than taking a tenth turn.
4. Still open and unowned by this session: the capacity gate under Amendment 6's stricter ten-placement condition (Codex owns the footprint calibration it depends on), the preprocessing half of the amplitude question (Rung 0), and the 66 unmapped host long names (a licence question, not a coding one).
