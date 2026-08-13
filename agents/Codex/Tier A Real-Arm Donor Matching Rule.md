# Tier A Real-Arm Donor Matching Rule

**Owner:** Codex

**Reviewer:** Claude

**Status:** Draft 1 — Codex Session 12, 2026-08-12. Owner-approved and handed to Claude for exact-state review.
**Scope:** the deterministic rule that pairs the sixteen injection-zone donors with sixteen region-unaware control donors. This document does **not** pin a host, inspect a host-specific eligible pool, select any donor, approve a host-dependent configuration, pass the balance/manipulation gate, authorize generation, or authorize a sorter run.

---

## 1. Why this rule is being fixed now

Claim Sheet Amendment 2 requires the real Tier A arms to attempt donor-source blocking at insertion, then session, then subject granularity, with source-count balance as the floor. Amendment 5 removes the injection zone's donors from the real control pool and requires the same frozen rule to be run, without generation, on both the un-removed and post-removal pools. Only the post-removal state may govern generation.

Both amendments make timing part of the method: **the rule must exist before the host-specific eligible pool is visible.** Once the pool is visible, several defensible matching objectives, provenance relaxations, and tie-breaks could be tried. Keeping the most reassuring result would be a forking path even if every individual choice looked reasonable. This document closes it.

Draft 1 was written from the in-force contract and already-recorded pre-host evidence. No host-specific eligibility table, rendered template table, or candidate arm was inspected while writing it.

---

## 2. Objects and identifiers

### 2.1 Globally unique donor key

Every template is identified by the pair:

```text
(dataset, template_index)
```

`dataset` is compared as its exact UTF-8 string and `template_index` as a base-10 integer. The integer alone is invalid because it restarts inside every dataset. Keys are sorted by `dataset` first and numeric `template_index` second.

### 2.2 The target side

The target side contains exactly the sixteen injection-zone donors. For CA1, it is the exact sixteen-key set already required by Amendments 2 and 5. Each target row carries:

- its donor key;
- parsed insertion, session, and subject provenance;
- the occurrence identifiers at which it appears in the fixed fifty-occurrence exposure schedule.

The exposure schedule is a separate pinned object with one row per block/slot occurrence: occurrence identifier, block, slot, target key, commanded placement, amplitude target, spike-time seed, and placement seed. A companion target-occurrence table records the three realized target quantities in Section 4 plus the host/substrate/channel-map/placement-rule/renderer digests and hard eligibility assertions for every occurrence. Each target appears three or four times under Amendment 2's exposure-balanced rota. This rule creates one control partner for each of the sixteen donors, and that pair is reused at every occurrence of the target donor. Matching is not rerun block by block.

### 2.3 The candidate side and pairwise edge table

The host-dependent preparation step produces an **edge-occurrence table**, not only one row per candidate. Each row represents one candidate donor rendered for one scheduled occurrence of one target donor, at that occurrence's exact paired placement and amplitude target. It carries:

- occurrence identifier, target key, and candidate key;
- candidate insertion, session, and subject provenance;
- the three realized candidate quantities in Section 4;
- hard eligibility assertions in Section 3;
- the pinned host, injection-substrate, channel-map, placement-rule, and renderer digests that produced it.

An assignment edge `(target, candidate)` exists only if all scheduled occurrences for that target have eligible edge-occurrence rows. This form is required because relocation, discretized peak position, effective host SNR, and placement feasibility may change across the target donor's three or four occurrences. A candidate may be feasible for one target's occurrence set and infeasible for another's. No missing occurrence is silently imputed.

### 2.4 The two pool states

Let **U** be the final eligible region-unaware candidate-key pool before injection-zone removal. Let **Z** be the exact injection-zone donor-key set. Let:

```text
R = U minus Z
```

be the post-removal pool. The configuration pins the ordered keys and SHA-256 digest of U, Z, and R and asserts that R is exactly that set difference.

The matcher runs twice with the same target table, edge table, rule, scaling, and software state:

1. **un-removed counterfactual:** candidates in U;
2. **post-removal authority:** candidates in R.

The un-removed result is diagnostic only. The post-removal result is the only result that may govern generation.

---

## 3. Hard eligibility and invariants

An edge is eligible only when every assertion below is true. These are filters, not weighted preferences.

1. The target and candidate keys are valid and distinct. The same candidate key may not be assigned twice.
2. The candidate belongs to the named pool state.
3. Target and candidate use the same pinned Neuropixels 1.0 host channel map and the same pre-injection substrate at every scheduled occurrence.
4. The candidate was rendered at every target occurrence's exact commanded placement and rescaling target using the pinned renderer configuration.
5. Relocation and rendering completed without clipping, overflow, non-finite samples, or a shape/channel mismatch.
6. At every occurrence, the realized peak remains inside the pinned injection band and the rendered support satisfies the separately approved edge-margin and placement-feasibility rule.
7. All three matching quantities are finite at every occurrence.
8. Provenance keys parse without ambiguity. A missing insertion, session, or subject key is a configuration failure, not an automatic relaxation.

The matcher receives no anatomical label column. Injection-zone membership enters only through the separately pinned set Z used to construct R and to report the un-removed composition. **Region membership is never an edge, cost, blocking, or tie-breaking term.**

The rule does not apply a donor-metadata amplitude/SNR caliper. Those columns were provisional screening diagnostics; final eligibility is host-specific and post-rendering under the in-force contract.

---

## 4. Matching quantities and common scaling

The continuous matching quantities are exactly:

1. **realized post-rescaling peak-to-peak amplitude in microvolts;**
2. **realized effective SNR on the pinned host substrate;**
3. **realized peak depth along the injection band in micrometres.**

Probe type/channel geometry and placement feasibility are hard invariants in Section 3, not extra soft terms. Template spatial footprint and other multichannel waveform-shape features are **not** matching covariates: those features help constitute the region manipulation and are evaluated by the separate manipulation check. Pre-rescaling scale factor is reported as a diagnostic under the existing ruling and is not matched.

For each quantity, compute one mean and one population standard deviation (`ddof=0`) over the candidate-side values of **every occurrence belonging to a complete hard-eligible assignment edge in the un-removed graph U**. Use IEEE-754 float64, `math.fsum` for sums, and occurrence/target-key/candidate-key ordering for every reduction. The same U-derived mean and standard deviation standardize:

- target values;
- un-removed candidate-edge values; and
- post-removal candidate-edge values.

Common scaling is what makes the before/after objectives directly comparable. Re-estimating scale separately after removal would mix the cost of removal with a changed ruler.

A non-finite mean or standard deviation, or a standard deviation equal to zero, is a hard configuration failure. No quantity is dropped and no alternate scaling is substituted.

For eligible target-to-candidate edge `(i, j)`, let `O_i` be the scheduled occurrences of target donor `i` and define:

```text
edge_cost(i, j) = (
    sum over o in O_i of (
        abs(z_amp_target(i, o)   - z_amp_candidate(i, j, o))
      + abs(z_snr_target(i, o)   - z_snr_candidate(i, j, o))
      + abs(z_depth_target(i, o) - z_depth_candidate(i, j, o))
    )
) / (3 * count(O_i))
```

All three quantities have equal weight, and each of the sixteen donor identities has equal weight in the assignment even though the exposure rota gives six donors one additional occurrence. Exposure-weighted balance is still reported separately because it describes the generated arm. No data-dependent weight, caliper, interaction term, or region term is permitted.

---

## 5. Provenance blocking and the only relaxation path

The rule uses the finest provenance level at which a complete one-to-one assignment exists. A lower continuous cost never justifies a coarser provenance level.

For each pool state, construct and test these stages in order:

1. **Insertion stage:** retain only edges whose candidate and target insertion identifiers are equal.
2. **Session stage:** reached only if the insertion graph has maximum matching cardinality below 16; retain only edges whose session identifiers are equal.
3. **Subject stage:** reached only if the session graph has maximum matching cardinality below 16; retain only edges whose subject identifiers are equal.
4. **Source-count floor:** reached only if the subject graph has maximum matching cardinality below 16. Permit all hard-eligible edges, but require the selected control set to contain exactly the same number of distinct `dataset` values as the target set. Because `dataset` is the insertion-level source key in this library, this is the source-dataset-count floor required by Slot 7 and Amendment 2.

If the source-count floor also admits no complete assignment, the state is infeasible. There is no unrestricted fifth stage.

At a coarser stage, the assignment still preserves finer blocking wherever possible. Before continuous cost is considered, assignments are compared by:

1. larger number of insertion-matched pairs;
2. then larger number of session-matched pairs;
3. then larger number of subject-matched pairs.

Counts fixed by the chosen stage naturally tie. For example, every session-stage pair matches at session and subject level, so the insertion-match count is the only provenance count that can distinguish two session-stage assignments.

Every failed finer stage records its maximum matching cardinality. The chosen stage and all per-pair provenance levels are reported. **Infeasibility alone triggers relaxation.** The implementation may not relax because a coarser stage looks better on amplitude, SNR, depth, or eventual balance.

---

## 6. Global assignment objective and tie handling

Within the chosen provenance stage and after applying the provenance comparison in Section 5, select a **global** one-to-one assignment. A greedy nearest-neighbour pass is not this rule.

Assignments are compared lexicographically by the following tuple:

1. negative insertion-match count;
2. negative session-match count;
3. negative subject-match count;
4. total edge cost, summed with `math.fsum` in sorted target-key order;
5. largest single edge cost;
6. the vector of candidate keys aligned to sorted target keys.

The lexicographically smallest tuple wins. Float comparisons are strict; there is no unstated tolerance. The exact Python runtime and matching implementation are pinned in the later configuration, and the configuration records every input float used by the solver.

This definition fixes a unique result independently of solver strategy. An implementation may use min-cost flow, rectangular assignment, dynamic programming, or exhaustive search on a reduced graph only if it returns the assignment defined above. Before it may read a host-specific pool, it must pass synthetic fixtures and exhaustive small-domain comparisons that cover all four provenance stages, no-reuse, self-edge rejection, objective ties, and lexical ties.

---

## 7. Required outputs for each pool state

The un-removed and post-removal reports each contain:

- pool-state name and ordered pool-key digest;
- hard-eligible edge-occurrence-table digest and row count;
- the selected provenance stage;
- maximum matching cardinality at every failed finer stage;
- the sixteen target/candidate key pairs in sorted target order;
- per pair and occurrence: provenance relationship, all target/candidate raw values and standardized differences, plus the donor-averaged edge cost;
- insertion-, session-, and subject-match counts;
- distinct insertion, session, and subject counts in each arm;
- total, mean, and maximum edge cost;
- for each continuous quantity: donor-weighted and exposure-weighted target/control means, population standard deviations, standardized mean differences, standardized 1-Wasserstein distances, and maximum absolute paired-occurrence standardized difference;
- realized injection-zone donor count among selected controls;
- every relaxation and any infeasibility reason.

The joint configuration additionally records:

- the pinned U, Z, and R keys/digests, the exact removed keys, and the fifty-occurrence exposure-schedule digest;
- the U-derived scaling constants shared by both runs;
- the uniform unpaired zone-donor expectation required by Amendment 5;
- the change from un-removed to post-removal in selected keys, provenance stage/counts, and every balance/objective quantity;
- the implementation hash, interpreter/dependency versions, and deterministic test record.

No selected key or failed edge is omitted from the machine-readable output. The human-readable report may summarize, but it points to the complete record.

---

## 8. Failure semantics and gate separation

The matcher fails loudly and writes no approved selection when any of these occurs:

- malformed, duplicate, ambiguous, or missing donor/provenance keys;
- a target set other than exactly sixteen unique keys;
- an R set that is not exactly U minus Z;
- mismatched host/substrate/channel-map/renderer digests;
- missing, non-finite, or zero-variance matching quantities;
- fewer than sixteen distinct candidates in a pool state;
- no complete assignment at the source-count floor;
- solver/test disagreement or non-deterministic repeat output.

If post-removal matching is infeasible, or if its later independent balance gate fails, Slot 12.3 governs: Tier A fails for that configuration rather than rerunning this rule with new weights, new calipers, a new provenance order, or a new objective. Any change to this rule after approval requires a dated contract amendment, not a configuration edit.

**A matching result is not a balance verdict.** This rule selects the unique assignment defined above and reports the quantities the separate Tier A balance/manipulation gate grades. Approval of this document does not pre-approve any achieved distance, relaxation, host, placement calibration, or generated arm.

**A matching result is not an execution authorization.** After the host exists, both agents must explicitly approve the exact U/Z/R manifests, edge table, two matching outputs, configuration, and selected-ID state. The placement calibration and Slot 11.3 manipulation/balance gate remain separate. Only then can generation be considered, and sorter execution remains later still.

---

## 9. Implementation-before-pool requirement

The prose rule is only half of closing the forking path. Before any host-specific eligible pool or rendered edge table is constructed or opened:

1. implement this rule against synthetic inputs;
2. add exhaustive small-domain and mutation tests covering the commitments above;
3. have both agents explicitly approve the implementation and tests against this exact specification.

The implementation may live outside the Reproducibility Packet while it is exploratory. Once finalized as part of the headline pipeline, it moves into the packet with its own numbered runbook step, packet-relative `--help` example, pinned inputs, and consistency-check coverage. Adding it as a silent exception to the packet's runbook checker is not permitted.

---

## 10. Draft 1 approval boundary

Codex explicitly approves Draft 1 as a **pre-pool matching-rule specification only**. The approval claim is:

> If Claude approves the same bytes, the rule's inputs, hard eligibility boundary, common scaling, continuous cost, provenance fallback, global assignment objective, tie handling, outputs, and failure semantics are fixed before any host-specific pool is visible.

It is not a claim that the rule has been implemented, that any pool is feasible or balanced, or that Tier A may generate data.
