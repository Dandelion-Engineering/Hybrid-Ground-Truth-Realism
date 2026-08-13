# Human Report 10 — Codex

**Current date and time:** 2026-08-12 17:18 PDT

**Session:** Codex Session 10

**Phase at start:** Phase 2 — Execution. Amendments 1–4 were `In force`; Amendment 5 was `Proposed` at Claude's Session 10 state. Draft 6 §12–§13 and the synchronized Claim Sheets were handed to Codex for exact-state review. No host was pinned and Rung 0 had not run.

**Phase at end:** Phase 2 — Execution. Amendments 1–4 remain `In force`; Amendment 5 remains `Proposed` at a corrected Codex-approved state awaiting Claude's genuine owner re-review. **No host is pinned, no Rung 0 or hybrid generator run occurred, no sorter ran, and no scientific result about realism exists.**

**No progress report is due this session.** The next count-based trigger is Codex Session 16, no phase closed, and no amendment reached `In force` through Codex's work in this session.

---

## Summary

This session closed Codex's review of Draft 6 §12 and repaired Amendment 5 before exact-state approval.

Claude's central finding survives review: a region-blind covariate matcher is strongly pulled toward injection-zone donors because its target is the sixteen CA1 donors themselves. On the frozen pre-host donor snapshot, the simple nearest-unused matcher selects three CA1 partners without blocking and eight under exact-insertion blocking. That makes exclusion a real contract choice rather than an implementation detail, and the choice must be made before the matching rule and eligible pool can be inspected together.

Two parts of the handed-off interpretation needed correction:

1. The exact-insertion expectation assumed independent draws, while the diagnostic matcher never reuses a partner. The audit now uses the exact inclusion-exclusion expectation for injective, non-self assignments: **1.03 rather than 0.98** for the full pool, and **1.17 rather than 1.11** under the provisional caliper. The unblocked expectations remain 0.11 and 0.12.
2. The 0.12 expected CA1 donors under a uniform region-blind draw is not the entire cost of exclusion. CA1 donors include close covariate matches and preferred exact-source matches, so exclusion can worsen balance, require provenance relaxation, or make a host-specific stratum infeasible. Amendment 5 now requires the eventual frozen rule to be run diagnostically on the un-removed pool and executably on the post-removal pool, with both states fully reported.

The synchronized whole-file states Codex explicitly approves are:

- `Claim Sheet.md`: SHA-256 `1a7d3ec689c1a62065b94157d01df6d2282b860fb59bf3162101cd092776e3f2`
- `Accessible Claim Sheet.md`: SHA-256 `7aa34271d07994ad608c3296117d9f631066eb7c2ff82bbb526fd90c6478b302`
- `agents/Claude/Tier A Host and Injection Zone Selection.md`: SHA-256 `7772f4fa65a2093dcbd7e8bb11c76305ab2c0b14d14a1b350e04d08f0652c697`
- `Reproducibility Packet/scripts/audit_zone_neighbour_enrichment.py`: SHA-256 `84dfa2511606e589376fcc2712d5be938e231f2da742c7354df649d444a3ecbf`
- `Reproducibility Packet/results/zone_neighbour_enrichment_CA1.txt`: SHA-256 `d47ff6794dd89d7c0d0e565e12b32ff09356f90f26f254698425025f7d51b16c`

Amendment 5 carries no force until Claude approves the same Claim Sheet bytes. The real-arm donor-matching rule remains blocked while that review is open.

---

## 1. Review of Claude's Session 10 handoff

### 1.1 What is accepted

Claude re-derived Codex's Amendment 3 repairs and approved them on the same exact Claim Sheet bytes. Amendment 3 is therefore `In force`. Its shared non-CA1 pseudo-base pool, globally unique donor identifiers, deterministic 64-sweep selector, and separate host-dependent configuration approval remain intact.

Draft 6 §12 is also approved as handed off. The derived label map's licensing boundary, measured coverage, withheld collisions, opt-in behavior, replay-integrity checks, and mixed-hierarchy warning are all supported by the tracked code and results. Draft 6 §1–§12 are now approved by Codex; §13 is approved only at the corrected hash above and awaits Claude's owner re-review.

The new audit is appropriately bounded. Its amplitude, SNR, and depth values are pre-host analogues. Its greedy matcher is a diagnostic stand-in, not a proposal or a prediction of the final arm. The observed counts establish that the design question is material; they do not prescribe the eventual matching algorithm.

### 1.2 Why the real arm needs the same timing discipline

The anchor pipeline samples region-blind templates but does not match them against a region-matched set. This project adds pairing to gain precision under desktop-scale compute. The resulting pull toward CA1 is therefore manufactured by the project design rather than inherited from the method under test.

Once both the eligible pool and a candidate matching rule are visible, allowing or excluding CA1 can each be defended after seeing the consequences. Amendment 5 closes that forking path. The injection-zone removal decision must enter force before the region-unaware matching rule is written or approved, and the rule itself may not reference region membership in either direction.

---

## 2. Exact no-reuse expectation

The diagnostic matcher assigns one distinct partner to each zone donor and forbids self-pairing. The earlier baseline multiplied per-slot region probabilities as though partners could be reused. That is not the sampling process implemented by `greedy_partners`.

`_injective_zone_expectation(pool_size, zone_count)` now counts admissible injective assignments by inclusion-exclusion and computes the expected number of zone outputs under that same no-reuse, non-self constraint. `region_blind_expectation` applies it either to the full pool or separately inside each exact-insertion block.

Corrected expectations:

| pool | nearest unused observed | no-reuse expectation | exact-insertion observed | no-reuse expectation |
|---|---:|---:|---:|---:|
| all 2,183 NP1.0 templates | 3/16 | 0.11 | 8/16 | 1.03 |
| provisional 50–200 µV / SNR 5–15 caliper | 2/12 | 0.12 | 5/12 | 1.17 |

The change is small numerically and important conceptually: the baseline now describes the actual constraint being compared. Exhaustive enumeration over every `pool_size` from 2 through 7 and every admissible `zone_count` agreed with the helper to floating-point tolerance.

---

## 3. Amendment 5 cost and gate repair

### 3.1 Two different costs

The uniform expectation answers: how far does removing CA1 move the eligible pool away from an anchor-like uniform region-blind draw? For sixteen draws from 2,183 templates containing sixteen CA1 templates, that answer is 0.12 expected CA1 donors.

It does not answer: what does removal do to this project's matched design? The diagnostic itself shows that CA1 donors are unusually attractive under the relevant covariates and exact-source preference. Removing them can increase matching distance, change the provenance-blocking granularity, or leave no post-removal arm satisfying the predeclared balance and placement rules.

Amendment 5 now requires one frozen rule to run in two locked states:

- **Un-removed pool:** diagnostic only; it may never govern generation.
- **Post-removal pool:** the only executable state.

Both configurations report selected (`dataset`, `template_index`) pairs, realized zone count, per-covariate balance/objective, provenance-blocking granularity, all relaxations, and infeasibility. The Technical Report must carry both the uniform-draw expectation and the matched-policy counterfactual.

### 3.2 Composition is not manipulation

The matched arm's 16/16 CA1 and control arm's 0/16 CA1 counts are design-integrity quantities. They verify that the exclusion happened. They do not show that waveform realism changed while amplitude, effective SNR, placement, and provenance stayed balanced. Slot 11.3's manipulation check remains a separate gate.

### 3.3 Failure remains possible

The aggregate donor pool is large, but host-specific and exact-source strata can be small. Amendment 5 now explicitly leaves Slot 12.3 in control: if the post-removal arm cannot satisfy the declared balance, placement, and provenance rules, Tier A fails rather than relaxing the contract silently.

---

## 4. Validation

- All 17 Python files in the Reproducibility Packet parsed successfully.
- The injective expectation matched exhaustive enumeration for pool sizes 2–7.
- Structured assertions confirmed the two Claim Sheets agree on Amendment 5's proposed status, 1.03 baseline, frozen-rule counterfactual, manipulation-check boundary, and open Claude re-review.
- The tracked audit report contains the corrected 0.11/1.03 and 0.12/1.17 expectations.
- `git diff --check` passed.
- The active chat append used a uniquely verified UTF-8 EOF anchor. The transcript had 614 lines before the append and 638 afterward; the new Codex Session 10 header appears exactly once and only after the pre-write boundary.

No network read, dependency installation, template-array pull, raw-data download, Rung 0 step, hybrid generation, or sorter execution occurred.

---

## 5. Decisions

1. **Approve Draft 6 §12.** Its evidence and boundaries survive review.
2. **Accept Amendment 5's exclusion decision.** The pairing-induced CA1 pull is real enough to require a precommitted rule.
3. **Correct the null expectation to the matcher's no-reuse design.** Exact-insertion expectations are 1.03 and 1.17 in the two reported pools.
4. **Measure policy cost with the actual frozen rule.** Uniform sampling arithmetic cannot substitute for matched-policy balance and feasibility.
5. **Keep composition verification separate from the manipulation gate.** Zero CA1 in the control is necessary by construction and not scientific evidence that the realism knob turned.
6. **Preserve Slot 12.3.** A large aggregate pool does not preclude host-specific infeasibility.
7. **Keep Amendment 5 proposed.** Reviewer edits and approval do not replace the owner's same-state review.
8. **Keep the matching-rule lane blocked.** Writing the rule before Amendment 5 closes would settle the open contract choice by omission.

---

## 6. Files created or updated

**Created**

- `agents/Codex/Session Summaries/HumanReport10.md` — this report.

**Updated**

- `Claim Sheet.md` — corrected expectation, matched-policy counterfactual, composition/manipulation distinction, and feasibility boundary.
- `Accessible Claim Sheet.md` — synchronized plain-language Amendment 5 corrections.
- `Reproducibility Packet/scripts/audit_zone_neighbour_enrichment.py` — exact no-reuse expectation.
- `Reproducibility Packet/results/zone_neighbour_enrichment_CA1.txt` — regenerated corrected report.
- `agents/Claude/Tier A Host and Injection Zone Selection.md` — corrected §13 and current review status.
- `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` — append-only exact-state ruling and handoff.
- `README.md` — corrected the orientation footer to the current Amendment 3/5 states.
- `agents/Codex/README.md` — workspace map and current state pointers.
- `agents/Codex/Summary of Only Necessary Context.md` — next-session continuity.

No references entry was added because this session used only tracked first-party project evidence and code.

---

## 7. Machine state

Measured at **2026-08-12 17:18 PDT**:

- RAM: 13.55 GiB free of 31.67 GiB; 18.12 GiB used.
- GPU memory: 14,980 MiB free of 16,311 MiB; 983 MiB used.

These values are continuity only. No heavy step was attempted, and later execution must take a fresh admission measurement.

---

## 8. Next steps

1. Claude must independently re-derive the corrected no-reuse baselines and review the matched-policy counterfactual requirement.
2. If Claude approves Claim Sheet hashes `1a7d3ec…` / `7aa34271…` unchanged, Amendment 5 may enter force and the real-arm matching-rule lane may begin.
3. If Claude edits either sheet, both synchronized states require another Codex exact-state review.
4. Keep the un-removed rule application diagnostic-only and the post-removal state as the sole generation authority.
5. Continue host and Rung 0 prerequisites only after the Amendment 5 gate closes; no host is currently pinned.
