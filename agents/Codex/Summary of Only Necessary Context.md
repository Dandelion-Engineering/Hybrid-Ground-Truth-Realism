# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 16 · 2026-08-13 05:10 PDT**

**Next Codex session will be Session 17.** No count-based progress report is due. Session 16's required report is `agents/Codex/Progress Reports/Progress Report Session 16.md`.

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No target-eligibility manifest, host-specific eligible pool, rendered edge table, exposure schedule, selected donor, template-array pull, dependency installation, raw-recording download, Rung 0, hybrid generation, or sorter run occurred in Codex Session 16.

The public state remains `In Progress`. Draft 5 of the real-arm donor matcher is pre-pool design/governance, not evidence about whether realism changes sorter accuracy.

## Contract state — Amendments 1–6 are in force

Current synchronized hashes:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

Amendment 6 governs Tier A:

- Z is the full sixteen-key injection-zone donor universe.
- A pinned finite candidate-site set, per-site predicates, and site-to-donor reduction produce one survivor set T and killed set K.
- `N = count(T)` is computed once. Continue for `10 <= N <= 16`; `N < 10` records Slot 12.3.
- Fifty occurrences use `q = floor(50/N)`, `r = 50 mod N`; the fixed `1910753866` digest order and round-robin deal give exactly `r` extra-occurrence targets and ten distinct targets per block.
- After the rota exists, every block's ten targets must admit a jointly feasible placement under the pinned sites and separately approved placement rule. Failure rejects the host; it never shrinks T or recomputes `N`.
- Real control and pseudo-arms follow `N`; Z remains all sixteen keys; every killed key and reason is published.

## Real-arm matching rule — Draft 5 awaits Claude exact-state review

Artifact: `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`

Codex-approved Draft 5 SHA-256:

`23148d2d8896db70f48d13bd712bbf4ba04987b7f348866918a98431fc324cf7`

Active chat: `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md`.

Claude reviewed Draft 3 and explicitly approved Draft 4 `5dc8022d33045da39ac3cbc4cfa1d667e34ef70629d780de6e6d52fe50d381d7`. Codex genuinely owner-re-reviewed those exact bytes, accepted the scientific corrections, edited the nuisance-input repair, explicitly approved Draft 5, and handed it back. **The prose loop remains open:** Claude must genuinely re-open Draft 5 and explicitly approve it unchanged or edit/approve another state.

Draft 5 retains all earlier decisions:

1. **One-time target state:** Z is full sixteen; T/K partition Z once; `N = count(T)`; `S_T` is T's actual distinct insertion count. Later placement, matching, or balance never changes T, N, or the rota.
2. **Full-Z removal:** U is the un-removed control pool and `R = U minus Z`. T is never substituted for Z.
3. **Common ruler and donor-equal cost:** one U-derived float64 ruler standardizes realized amplitude, effective host SNR, and depth for both runs; R-derived standard deviations are diagnostic. Every target has matching weight `1/N`; exposure weighting is separately reported.
4. **No region term:** anatomy is used only for the separately pinned removal set and composition reporting.
5. **Four provenance stages:** insertion, session, subject, and unrestricted hard-eligible edges. A stage relaxes only if no complete assignment satisfies its pairwise restriction and the required provenance-count condition.
6. **Global deterministic assignment:** no reuse, self-edge rejection, exact constrained optimality, lexicographic provenance/cost/tie objective, complete outputs, and loud failures.

## Session 16 correction — provenance counts are two-level

The `dataset` field is the probe-insertion identifier; session and subject are parsed from it. The pinned 2,183-row NP1.0 snapshot has 37 insertions, 24 sessions, and 12 subjects. CA1's sixteen have four insertions, four sessions, and four subjects.

Among all 66,045 four-insertion subsets, 37,424 span four subjects, 28,621 span fewer, and 74 span one. Claude's probe and Codex's independent CSV enumeration reproduce those counts exactly.

Draft 5 therefore tests at each provenance stage:

- **Level A:** selected controls match T's distinct insertion, session, and subject counts;
- **Level B:** selected controls match T's insertion count only, the literal Claim Sheet floor.

Level A is attempted first. Level B remains reachable at the same pairwise stage if Level A fails. The pairwise stage relaxes only if Level B also fails. This can change which assignment wins but cannot force a coarser pairwise stage or create a new Tier A failure. The achieved level and both feasibility results are reported.

## New separate gate — exposure schedule and placement specification

Claude correctly found that the matcher's inputs were not actually pinned: all three matched quantities are realized at the commanded placement, and the schedule carried randomized slot assignment, spike-time seeds, placement seeds, commanded placements, and amplitude targets without an exact construction.

Draft 4 required a derived master seed but left the seed string, occurrence grammar, stream mapping, amplitude-target law, and placement transform for a later pool-aware configuration. Draft 5 replaces that incomplete repair with a separate same-state gate.

Before T is measured or any host-specific manifest, U/R pool, or edge table may be constructed/opened, both agents must approve an exact exposure-schedule/placement specification and synthetic tests that pin:

- master-seed derivation and value;
- occurrence grammar and domain labels;
- within-block unit-slot mapping;
- amplitude-target law and assignment;
- spike-time and placement seed derivations;
- seed/candidate-site to commanded-placement mapping;
- real-arm nuisance sharing and pseudo-arm stream separation; and
- byte-for-byte replay digests and failure semantics.

The approved algorithm is evaluated once after T is known; the schedule is never redrawn. Joint placement failure rejects the host rather than choosing another seed/schedule.

## Matcher implementation remains another separate pre-pool gate

Even after prose convergence:

1. specify, implement, test, and same-state approve the exposure schedule/placement rule on synthetic T/site inputs;
2. implement the matcher against synthetic inputs only;
3. add exhaustive small-domain and mutation tests for `N = 10..16`, variable `S_T/E_T/B_T`, T/K partitioning, full-Z removal, rota invariants, both provenance levels at all four stages, no-reuse, self-edge rejection, deterministic objective/ties, outputs, and loud failures; and
4. obtain explicit same-state approval from both agents before opening a real manifest, pool, or edge table.

Do not start implementation until Claude's Draft 5 review resolves. The schedule/placement specification, matcher implementation, host selection, target eligibility, exact U/Z/R/T/K configuration, matching outputs, balance/manipulation gate, generation, and sorter execution remain separate approvals.

## Host selection and Rung 0 remain unchanged

`agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 7 at `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01` remains same-state approved for strategy/evidence scope, not as a host selection.

Candidate order remains:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Claude owns drift, noise, and post-rescaling effective-SNR host gates. The existing `cumulative_drift_um_per_hour` column is accumulated absolute spike-depth path length and scales with spike count; it is unsuitable as a host gate. Claude must define a replacement quantity and justify its threshold before measuring candidates.

Codex owns footprint/placement calibration, the schedule/placement specification, matching implementation, independent balance/manipulation gate, Rung 0, sorter-panel decision, and inference/negative-control harness.

Rung 0 remains unrun. It must construct and pin the pre-injection host substrate before injection, avoid phase-shifting injected templates twice, pin the exact approximately 60-second segment, resolve dependencies only in the project venv, and take fresh RAM/VRAM immediately before heavy work under Amendment 1's guards. Current venv pins only `h5py==3.16.0` and `numpy==2.5.2`.

## Reproducibility Packet state

The design-stage review is concluded. Same-state approved hashes remain:

- packet `README.md`: `3b07aa5b94203d3f4c826be7aac40e6550c2a13e7d3b45c997399a84af3df4a1`
- checker: `4eb9401825ec2a4561abf46dc7dc82d89ea316722d338bba9e84bd747d83c651`
- mutation harness: `d64134b1485a8550412c1eb7fba7fd98ab509471050cad71a41fc8f704d5acc3`

One command per runbook step/example is a hard error. Ten design-stage steps pass and all fifteen mutations are caught. Five archive-reading steps were not re-run in that review. The headline pipeline and Slot 8 `verify_realism.py` do not exist because no result exists. Later packet additions start a new scoped review.

## Gate order — do not collapse

1. Claude exact-state review of Draft 5;
2. Draft 5 same-state prose convergence;
3. exposure-schedule/placement specification, implementation, synthetic tests, and same-state approval;
4. matcher implementation, deterministic tests, and same-state approval;
5. host selection and Codex's footprint/placement calibration;
6. exact candidate sites, target manifest, T/K/N, U/Z/R, edge table, two matching outputs, selected IDs, and configuration;
7. independent Tier A balance/manipulation approval;
8. generation authorization;
9. Rung 0/sorter execution authorization.

Reviewer edits, downstream use, later commits, and silence do not substitute for same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. Claude Session 16 already added the noteworthy public entry for the provenance-granularity and redrawable-schedule findings. Its working-record section already says the matcher draft awaits same-state review. Draft 5 has not converged, so Codex added no duplicate heartbeat.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- Codex's required count-based Session 16 progress report exists at `agents/Codex/Progress Reports/Progress Report Session 16.md`.

## Validation and machine record from Session 16

- Draft 4's handed-off hash was verified before review.
- Claude's provenance probe reproduced the pinned snapshot and reported 2,183 rows / 37 insertions / 24 sessions / 12 subjects and the full 66,045-subset census.
- An independent stdlib CSV/regex enumeration reproduced every `(session_count, subject_count)` cell, including 37,424 four-subject subsets and 74 one-subject subsets.
- Draft 5 SHA-256 is `23148d2d8896db70f48d13bd712bbf4ba04987b7f348866918a98431fc324cf7`.
- Required/stale-text assertions, Markdown fences, artifact Unicode, append-only transcript prefix/header assertions, and `git diff --check` passed before closeout.
- 2026-08-13 05:10 PDT: 7.31 GiB RAM free of 31.67; 1,021 MiB VRAM used of 16,311; 603.6 GB free on `C:`. No heavy work ran.

`agents/Codex/Session Summaries/HumanReport16.md` contains the full owner-review rationale, verification evidence, and file list.
