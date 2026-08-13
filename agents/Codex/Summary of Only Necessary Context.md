# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 15 · 2026-08-13 03:13 PDT**

**Next Codex session will be Session 16. A count-based progress report is due.** Complete normal session work first, then write `agents/Codex/Progress Reports/Progress Report Session 16.md` per `Playbooks/research-progress-report.md`. The report is an addition to the session, not a replacement.

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No host-specific eligible pool, target manifest, rendered edge table, selected donor, template-array pull, dependency installation, raw-recording download, Rung 0, hybrid generation or sorter run occurred in Codex Session 15.

The public state remains `In Progress`. Draft 3 of the donor matcher is pre-pool design/governance, not evidence about whether realism changes sorter accuracy.

## Contract state — Amendments 1–6 are in force

Current synchronized hashes:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

Amendment 6 governs Tier A:

- Z is the full sixteen-key injection-zone donor universe.
- A pinned finite candidate-site set, per-site predicates and site-to-donor reduction produce one survivor set T and killed set K.
- `N = count(T)` is computed once. Continue for `10 <= N <= 16`; `N < 10` records Slot 12.3.
- Fifty occurrences use `q = floor(50/N)`, `r = 50 mod N`; the fixed `1910753866` digest order and round-robin deal give exactly `r` extra-occurrence targets and ten distinct targets per block.
- After the rota exists, every block's ten targets must admit a jointly feasible placement under the pinned sites and separately approved placement rule. Failure rejects the host; it never shrinks T or recomputes `N`.
- Real control and pseudo-arms follow `N`; Z remains all sixteen keys; every killed key and reason is published.

## Real-arm matching rule — Draft 3 awaits Claude exact-state review

Artifact: `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`

Codex-approved Draft 3 SHA-256:

`e63e10317093f37020ad2d184775a3ac696cadb128f885df18928c01f6dd129a`

Active chat: `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md`.

Codex genuinely re-reviewed Claude's Draft 2. Accepted: common U-derived scaling with R-derived diagnostic, donor-equal cost, exact source-count equality, provably exact constrained optimization, provenance-concentration outputs, named count comparators and the supporting provenance tool's bounded review role.

Draft 3 fixes the remaining contract reading and incorporates Amendment 6:

1. **Distinct objects:** Z is full sixteen; T is the surviving targets; K is the killed list; `N = count(T)`; `S_T` is T's actual distinct `dataset` count. Do not collapse any two.
2. **One-time eligibility:** the target manifest partitions Z into T/K once. Later placement, matching or balance never changes T, `N` or the rota.
3. **Full-Z control removal:** `U` is the un-removed control pool and `R = U minus Z`. T is never substituted for Z.
4. **Source-count equality at every stage:** insertion+`S_T`, session+`S_T`, subject+`S_T`, then unrestricted hard-eligible edges+`S_T`. Relax only when no complete `N`-pair assignment satisfies both the pairwise rule and exact source count.
5. **Constrained search:** at stages 2–4, enumerating candidate source subsets of size `S_T` is insufficient unless every enumerated source appears at least once in the selected controls. Any alternative method must prove it returns the defined global optimum.
6. **Donor-equal matching:** every target gets `1/N`; exposure weighting is reported separately. Extra-occurrence targets would have `(q + 1)/q` times the exposure influence of the others; the old 22% statement is removed.
7. **Variable outputs/failures:** all pair counts, candidate sufficiency, source multiplicities, reports and failure tests use actual `N`, T and `S_T`. Historical `[6,5,3,2]`, 0.11 and 1.03 remain sixteen-target diagnostics, not predictions.

Codex explicitly approved and handed Draft 3 to Claude. Claude must genuinely re-open the exact bytes and explicitly approve or edit/hand back. If approved unchanged, only the **prose** loop closes.

## Implementation is the next separate gate — no pool access

Even after prose convergence, before any host-specific eligible pool or rendered edge table may be constructed or opened:

1. implement the rule against synthetic inputs only;
2. add exhaustive small-domain and mutation tests covering `N = 10..16`, variable `S_T`, target-manifest partitioning, full-Z removal, rota invariants, all four source-count-preserving stages, no-reuse, self-edge rejection, deterministic objective/tie handling and loud failures; and
3. obtain explicit same-state approval from both agents on implementation and tests.

Do not start implementation until Claude's Draft 3 review resolves. Do not open a real pool during implementation. The implementation/test review, host selection, placement calibration, target eligibility, exact U/Z/R/T/K configuration, matching outputs, balance/manipulation gate, generation and sorter execution are separate approvals.

## Host selection and Rung 0 remain unchanged

`agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 7 at `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01` remains same-state approved for strategy/evidence scope, not as a host selection.

Candidate order remains:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Claude owns drift, noise and post-rescaling effective-SNR host gates. Codex owns footprint/placement calibration, the matching implementation, independent balance/manipulation gate, Rung 0, sorter-panel decision and inference/negative-control harness.

Claude Session 15 confirmed the existing `cumulative_drift_um_per_hour` column is accumulated absolute spike-depth path length, not net displacement, and is documented as scaling with spike count. It is unsuitable and potentially biasing as a host gate. This remains Claude's lane; do not duplicate it.

Rung 0 remains unrun. It must construct and pin the pre-injection host substrate before injection, avoid phase-shifting injected templates twice, pin the exact approximately 60-second segment, resolve dependencies only in the project venv, and take fresh RAM/VRAM immediately before heavy work under Amendment 1's guards. Current venv pins only `h5py==3.16.0` and `numpy==2.5.2`.

## Reproducibility Packet state

The design-stage review is concluded. Same-state approved hashes remain:

- packet `README.md`: `3b07aa5b94203d3f4c826be7aac40e6550c2a13e7d3b45c997399a84af3df4a1`
- checker: `4eb9401825ec2a4561abf46dc7dc82d89ea316722d338bba9e84bd747d83c651`
- mutation harness: `d64134b1485a8550412c1eb7fba7fd98ab509471050cad71a41fc8f704d5acc3`

One command per runbook step/example is a hard error. Ten steps pass and all fifteen mutations are caught. Five archive-reading steps were not re-run in that review. The headline pipeline and Slot 8 `verify_realism.py` do not exist because no result exists. Later packet additions start a new scoped review.

## Gate order — do not collapse

1. Claude exact-state review of Draft 3;
2. Draft 3 same-state prose convergence;
3. matching implementation and deterministic-test convergence on synthetic inputs, before pool access;
4. host selection and Codex's two-part footprint/placement calibration;
5. exact candidate sites, target eligibility manifest, T/K/N, U/Z/R, edge table, two matching outputs, selected IDs and configuration;
6. independent Tier A balance/manipulation approval;
7. generation authorization;
8. Rung 0/sorter execution authorization.

Reviewer edits, downstream use, later commits and silence do not substitute for same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. Its latest log entry already records Amendment 6 entering force, and its working-record section already says the matcher draft awaits review. Draft 3 has not converged, so no new heartbeat was added.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- No progress report was due in Session 15. Session 16 requires the count-based report after normal work.

## Validation and machine record from Session 15

- Draft 3 contract assertions passed, stale Draft 2 phrases were absent, Markdown fences balanced, and `git diff --check` passed.
- Rota multiplicities and ten-distinct-target block membership passed for every `N = 10..16`.
- The artifact contained no malformed Unicode sequence.
- Chat append safeguard passed for the exact 315-line committed prefix and the first handoff header. Read-back caught two mangled range marks in the chat only; an append-only ASCII correction was added. The exact 343-line byte prefix then remained intact and the correction header occurred exactly once. The artifact hash and rules did not change.
- 2026-08-13 03:13 PDT: 8.05 GiB RAM free of 31.67; 1,015 MiB VRAM used of 16,311; 604.0 GB free on `C:`. Nothing heavy ran.

`agents/Codex/Session Summaries/HumanReport15.md` contains the full review rationale, validation evidence and file list.
