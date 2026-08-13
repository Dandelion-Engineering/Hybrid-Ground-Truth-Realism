# Human Report 15 — Codex

**Current date and time:** 2026-08-13 03:13 PDT

**Session:** Codex Session 15

**Phase at start:** Phase 2 — Execution. Amendments 1–6 were `In force`. Claude had completed genuine owner re-review of Codex's Amendment 6 edits and explicitly unblocked Draft 3 of the Tier A real-arm donor-matching rule. No host, host-specific eligible pool, rendered edge table, selected donor, implementation, generation, Rung 0 or sorter run existed.

**Phase at end:** unchanged. Codex revised the pre-pool prose rule to Draft 3, explicitly approved exact SHA-256 `e63e10317093f37020ad2d184775a3ac696cadb128f885df18928c01f6dd129a`, and handed it to Claude for exact-state review. Implementation and deterministic tests remain a separate approval gate before any host-specific pool may be constructed or opened.

**Progress-report trigger:** none. Session 15 is not a multiple of eight, no phase closed and no amendment entered force during this Codex session. The next count-based report is Session 16.

---

## Summary

This session performed the genuine owner re-review of Claude's Draft 2 matching-rule edits, then generalized and repaired the rule under the now-in-force Amendment 6. The result is a deterministic pre-pool specification that uses a one-time target-eligibility manifest, supports `N = 10..16` surviving injection-zone donors, retains all sixteen zone keys in the removal set, preserves donor-equal matching, and makes exact source-count equality survive every provenance relaxation.

The central correction is not merely replacing “sixteen” with `N`. The design now distinguishes three objects that must never be collapsed: Z, the full sixteen-key injection-zone universe removed from the control pool; T, the `N` targets that survive the pinned host-specific donor gates; and `S_T`, the number of source datasets actually represented in T. T and `N` are computed once. Z never shrinks with them. `S_T`, rather than a hard-coded four, governs source-count equality at insertion, session, subject and unrestricted-edge stages.

No scientific or host-dependent state was opened. The session read only tracked text and already-recorded pre-host evidence, ran small deterministic textual and rota checks, and appended the exact-state handoff. No network read, dependency install, raw-data read, template-array pull, candidate-pool inspection, generator, Rung 0 or sorter run occurred.

## 1. Startup, inherited state and cross-review

`.agent-turn` named Codex and `.agent-session.lock` did not exist. I created the lock, re-read `.agent-turn`, confirmed it still named Codex, and followed `AgentPrompt.md`: read the complete Project Details, Codex continuity, every summary and active transcript in a Codex-participant chat, the review-cycle playbook, both in-force Claim Sheets' governing technical state, Claude's latest continuity, `HumanReport15.md`, and the Amendment 6 progress report.

The tracked repository was clean at `a7a8b18` (`Claude Session 15`). Claude's exact current contract hashes reproduced from the live files:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`
- matching Draft 2: `f4ab71c3216d172641706a199d0536520da538aff906eb29d94f06f3d6620310`

Claude's Session 15 work was the required recent-work cross-review. Its Amendment 6 approval, complete fixed-sixteen audit and stricter block-placement reading agree with the live contract. Its separate drift finding is also correctly bounded: IBL's `cumulative_drift_um_per_hour` is accumulated absolute depth-estimate path length, not net displacement, and its documented correlation with spike count makes it unsuitable as a host gate. That finding remains in Claude's host-selection lane and required no Codex edit this session.

## 2. Genuine owner re-review of Draft 2

I accepted the parts Claude added or clarified in Draft 2:

- one common U-derived ruler for the required un-removed/post-removal comparison, with R-derived standard deviations reported only as a sensitivity diagnostic;
- donor-equal edge cost, with exposure-weighted balance reported separately;
- exact source-count equality rather than a one-sided minimum;
- a provably exact constrained assignment rather than an unconstrained solver plus greedy repair;
- provenance multiplicity/concentration outputs, because equal distinct-source counts do not imply equal concentration;
- a named sampling model beside any zone-count comparator; and
- Claude's `zone_provenance_headroom.py` as bounded review support outside the Reproducibility Packet.

I did not accept Draft 2's claim that session- and subject-blocked assignments could violate the source-count equality until the final fallback. Amendment 2 calls source-count balance the floor. A floor is the property preserved while exact pairwise provenance is relaxed, so it must hold at every stage.

## 3. Draft 3 target state — Z, T, K and `N`

Draft 3 now defines:

- **Z:** the complete injection-zone donor universe, sixteen keys for CA1;
- **T:** the ordered targets surviving the pinned donor-level host gates;
- **K = Z minus T:** every killed key, with gate, site-level values and reason; and
- **`N = count(T)`:** computed once, continuing for `10 <= N <= 16` and recording Slot 12.3 before matching when `N < 10`.

The tracked Tier A configuration must pin the finite candidate-site set, thresholds, every per-site predicate and the exact site-to-donor reduction before evaluating any zone donor. A later occurrence, placement, rendering, matching or balance result may not kill another target and change T, `N` or the rota.

Z remains all sixteen keys even when T is smaller. The real control pools are still `U` before removal and `R = U minus Z` after removal. T is never substituted for Z because target-side and control-side eligibility are not established to be the same predicate; a target killed under one predicate may not silently re-enter the control under another.

## 4. Exposure rota and placement gate

The rule now consumes Amendment 6's exact schedule rather than describing a hard-sixteen special case:

- targets are ordered by the fixed `1910753866` SHA-256 rule;
- fifty slots are dealt round-robin over T;
- `q = floor(50/N)` and `r = 50 mod N`;
- the first `r` ranks appear `q + 1` times and the rest appear `q` times; and
- each consecutive ten-slot block contains ten distinct targets for every admissible `N`.

The joint placement condition remains a separate host gate. After the rota exists, every block's ten scheduled targets must admit a jointly feasible ten-placement assignment under the pinned sites and separately approved placement rule. Failure rejects the host. It does not remove another target and redeal.

## 5. Provenance floor at all four stages

Let `S_T` be the actual number of distinct `dataset` sources in T. It is not assumed to remain four when targets die. Each pool-state run now tests, in order:

1. insertion blocking plus exact use of `S_T` sources;
2. session blocking plus exact use of `S_T` sources;
3. subject blocking plus exact use of `S_T` sources; and
4. unrestricted hard-eligible edges plus exact use of `S_T` sources.

A stage relaxes only when no complete `N`-pair assignment satisfies both its pairwise restriction and the source-count equality. A plain maximum matching of cardinality `N` is insufficient when its selected controls use the wrong number of sources.

At stages 2–4, an implementation that enumerates source subsets must require every source in the enumerated subset to appear at least once in the selected controls. Merely restricting candidates to a subset of size `S_T` is not enough, because a returned assignment could use fewer sources. Any alternative method must prove it returns the Section 6 optimum under the exact global cardinality condition. The full CA1 universe's four-source `[6, 5, 3, 2]` distribution remains historical pre-host context; the matcher uses T's actual sources and multiplicities.

## 6. Weighting, outputs and failure semantics

The erroneous Draft 2 statement that the two objectives differed by “22%” is gone. The invariant is the only statement retained: donor-equal matching gives every target weight `1/N`; exposure weighting gives each extra-occurrence target `(q + 1)/q` times the influence of the others. Donor-equal matching prevents the fixed rota's choice of extra-occurrence donors from deciding their partners, while exposure-weighted balance still describes the generated arm and remains an output.

The required later configuration now includes U/Z/R/T/K, the target manifest and killed list, the candidate sites, block-placement certificates, `q`/`r`, the digest-ranked order, both matching outputs, the actual-`N` uniform expectation, the constrained source-set search proof and all selected pairs. Failure tests use `N`, the actual T distribution and full Z removal. Historical 0.11 / 1.03 values remain explicitly identified as sixteen-target diagnostics, not later predictions.

The gates remain separate. Draft 3 is not an implementation, pool, matching result, balance verdict, placement approval, exact configuration, generation authorization or sorter authorization.

## 7. Exact-state handoff and validation

I explicitly approved and handed to Claude:

- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`: SHA-256 `e63e10317093f37020ad2d184775a3ac696cadb128f885df18928c01f6dd129a`

Validation performed before handoff:

- required-text assertions covered the manifest partition, `N` boundary, full-Z removal, all four source-count-preserving stages, exact source-subset use, exposure invariant and actual-`N` expectation;
- stale-text assertions rejected the 22% claim, hard-sixteen target/candidate failures, the former “floor only at stage 4” reading and the unresolved Section 11;
- Markdown code fences were balanced;
- the round-robin schedule reproduced quotient/remainder multiplicities and ten distinct target ranks per block for every `N = 10..16`;
- `git diff --check` passed; and
- the artifact contained no malformed Unicode sequence.

The first appended handoff message contained two console-mangled range marks even though the artifact was clean. The mandatory read-back caught them. I preserved the original transcript and appended a dated correction in plain ASCII, changing no rule, hash, result, gate or approval. Append-only verification then proved the exact 315-line committed prefix survived the handoff, and the exact 343-line byte prefix survived the correction; each new Codex header appeared exactly once after its respective boundary.

## 8. Public heartbeat, files and ignore review

The root Live-Run README already records Amendment 6 entering force and already says the pre-pool matching-rule draft awaits same-state review. Draft 3 is a handoff, not a converged artifact or execution event, so another public running-log entry would turn the lean heartbeat into a session journal. The root README was deliberately left unchanged.

**Created**

- `agents/Codex/Session Summaries/HumanReport15.md`

**Updated**

- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` — Draft 3 at the approved hash above.
- `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md` — append-only owner review, exact-state handoff and append-only rendering correction.
- `agents/Codex/README.md` — workspace map and current gate state.
- `agents/Codex/Summary of Only Necessary Context.md` — complete next-session continuity rewrite.

**Deliberately unchanged**

- Claim Sheets — Amendment 6 was already in force and no contract defect was found.
- root `README.md` — no converged public state changed.
- Reproducibility Packet and dependencies — implementation is still blocked on prose convergence.
- `references.md`, `director_requests.md` and `.gitignore` — no new source, director dependency, dependency, generated artifact or ignore need arose.

The `.gitignore` already excludes the coordination lock and turn files, virtual environment, raw electrophysiology inputs, large generated arrays, sorter outputs, secrets, logs and build artifacts while preserving the packet's small pinned snapshots. No update was needed.

## 9. Machine and execution boundary

Measured at 2026-08-13 03:13 PDT: system RAM **8.05 GiB free of 31.67**, GPU memory **1,015 MiB used of 16,311**, and **604.0 GB free on `C:`**.

Nothing heavy ran and no heavy step was contemplated. The session used tracked text, git history/diffs, SHA-256, small in-memory rota checks and append-only integrity checks. No network read, dependency install, raw recording, template array, eligible pool, edge table, generator, Rung 0 or sorter run was opened.

## 10. Next steps

1. Claude genuinely re-opens Draft 3 at `e63e103…`, reviews the actual bytes and either explicitly approves them unchanged or edits and hands back a new state.
2. If Claude approves unchanged, the pre-pool prose loop closes.
3. Codex then implements the rule only against synthetic inputs and builds exhaustive small-domain and mutation tests covering `N = 10..16`, variable `S_T`, all four source-count-preserving stages, target-manifest partitioning, full-Z removal, schedule invariants, no-reuse and deterministic ties/failures.
4. Both agents must explicitly approve the implementation and tests before any host-specific eligible pool or rendered edge table may be constructed or opened.
5. Host selection, placement calibration, target eligibility, exact U/Z/R/T/K configuration, matching outputs, balance/manipulation approval, generation and sorter execution remain later separate gates.
6. No director action is needed. The Phase 1 contract-review request remains open and non-blocking.
