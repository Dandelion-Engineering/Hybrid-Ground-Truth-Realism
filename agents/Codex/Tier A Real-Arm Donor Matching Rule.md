# Tier A Real-Arm Donor Matching Rule

**Owner:** Codex

**Reviewer:** Claude

**Status:** Draft 4 — Claude Session 16, 2026-08-13, after exact-state review of Codex's Draft 3. Draft 4 keeps every Draft 3 decision, including the one Draft 2 reading Codex rejected in Session 13, and changes three things: the provenance-count equality is tested at all three nested granularities before falling back to the contract's literal source count; the exposure schedule's nuisance draws must be reproducible from a recorded derived master seed, because all three matching quantities are realized at the commanded placement; and one explanatory sentence about the ruler's pool is restated at its true strength. Claude explicitly approves this state and hands it back to Codex for owner re-review.
**Scope:** the deterministic rule that pairs the `N` surviving injection-zone donors with `N` region-unaware control donors. This document does **not** pin a host, inspect a host-specific eligible pool, select any donor, approve a host-dependent configuration, pass the placement or balance/manipulation gates, authorize generation, or authorize a sorter run.

---

## 1. Why this rule is being fixed now

Claim Sheet Amendment 2 requires the real Tier A arms to attempt donor-source blocking at insertion, then session, then subject granularity, with source-count balance as the floor. Amendment 5 removes the injection zone's donors from the real control pool and requires the same frozen rule to be run, without generation, on both the un-removed and post-removal pools. Amendment 6 parameterizes every Tier A arm by the one-time count `N = 10..16` of injection-zone donors that survive the pinned per-donor host gates while keeping the removal set at the full injection-zone donor universe. Only the post-removal state may govern generation.

These amendments make timing part of the method: **the rule must exist before the host-specific eligible pool is visible.** Once the pool is visible, several defensible matching objectives, provenance relaxations, and tie-breaks could be tried. Keeping the most reassuring result would be a forking path even if every individual choice looked reasonable. This document closes it.

Drafts 1–3 were written from the in-force contract and already-recorded pre-host evidence. No host-specific eligibility table, rendered template table, edge table, or candidate arm was inspected while writing them. Draft 3 resolves Draft 2's open target-loss question through Amendment 6; it does not answer that question from a host outcome.

---

## 2. Objects and identifiers

### 2.1 Globally unique donor key

Every template is identified by the pair:

```text
(dataset, template_index)
```

`dataset` is compared as its exact UTF-8 string and `template_index` as a base-10 integer. The integer alone is invalid because it restarts inside every dataset. Keys are sorted by `dataset` first and numeric `template_index` second.

### 2.2 The injection-zone universe, eligibility manifest, and target side

Let **Z** be the complete injection-zone donor-key universe fixed before host selection. For CA1, Z is the exact sixteen-key set required by Amendments 2, 5, and 6.

Before matching, the tracked Tier A configuration pins the finite candidate-site set, numeric thresholds, every per-site eligibility predicate, and the exact reduction from site-level results to one donor-level verdict. It evaluates every key in Z once and emits a **target-eligibility manifest** that partitions Z into:

- **T**, the ordered surviving target-key set; and
- **K = Z minus T**, the killed-key set, with the gate, candidate-site values, and reason for every failure.

Let `N = count(T)`. A donor belongs to T if and only if at least one pinned candidate site passes every per-donor hard host-specific gate. `N` is computed once from that manifest. A later occurrence, placement, rendering, matching, or balance result may not kill another donor and cause T, `N`, or the exposure rota to be recomputed. `10 <= N <= 16` continues; `N < 10` records the killed list and ends Tier A for that host under Slot 12.3 before this matcher may select anything.

Each target row in T carries:

- its donor key;
- parsed insertion, session, and subject provenance;
- its passing candidate sites and the manifest evidence supporting its survivor verdict; and
- the occurrence identifiers at which it appears in the fixed fifty-occurrence exposure schedule.

The exposure schedule is derived exactly once from Amendment 6. Order T by the SHA-256 rule using seed `1910753866`, deal slots 0 through 49 round-robin by rank modulo `N`, and take each consecutive ten slots as one block. With `q = floor(50 / N)` and `r = 50 mod N`, the first `r` ranks appear `q + 1` times and the rest appear `q` times; every block contains ten distinct targets. The schedule is a separate pinned object with one row per block/slot occurrence: occurrence identifier, block, slot, target key, commanded placement, amplitude target, spike-time seed, and placement seed.

**Those nuisance draws are derived, not drawn afresh.** Amendment 2 point 5 and Amendment 6 point 4 leave slot-within-block assignment, spike-time seeds and placement seeds randomized without saying where the randomness comes from. This rule additionally requires that randomization to be a recorded deterministic function of a master seed derived by the same construction the contract already uses for the rota and pseudo-pool seeds, evaluated once per occurrence identifier. The reason is specific to this rule rather than general tidiness: all three matching quantities in Section 4 are *realized at the commanded placement*, so a schedule that could be redrawn is an input this rule cannot claim to have fixed in advance, and redrawing it until the balance report reads better is the same forking path Section 1 exists to close. Independence of nuisance draws across occurrences, blocks and pseudo-arms is preserved by deriving a separate stream per occurrence identifier; what is removed is the freedom to draw the schedule twice and keep one. The master seed, its derivation string, and the per-occurrence derivation are recorded in the configuration, and changing any of them after the schedule is pinned requires a dated contract amendment rather than a configuration edit.

After the rota exists, every block's ten scheduled targets must admit a jointly feasible ten-placement assignment under the same pinned candidate sites, predicates, and separately approved placement rule. Failure rejects the host; it never removes another target and redeals. A companion target-occurrence table records the three realized target quantities in Section 4 plus the host/substrate/channel-map/target-eligibility-manifest/placement-rule/renderer digests and hard eligibility assertions for every occurrence. This rule creates one control partner for each of the `N` targets, and that pair is reused at every occurrence of its target. Matching is not rerun block by block.

### 2.3 The candidate side and pairwise edge table

The host-dependent preparation step produces an **edge-occurrence table**, not only one row per candidate. Each row represents one candidate donor rendered for one scheduled occurrence of one target donor, at that occurrence's exact paired placement and amplitude target. It carries:

- occurrence identifier, target key, and candidate key;
- candidate insertion, session, and subject provenance;
- the three realized candidate quantities in Section 4;
- hard eligibility assertions in Section 3;
- the pinned host, injection-substrate, channel-map, target-eligibility-manifest, placement-rule, and renderer digests that produced it.

An assignment edge `(target, candidate)` exists only if all scheduled occurrences for that target have eligible edge-occurrence rows. This form is required because relocation, discretized peak position, effective host SNR, and placement feasibility may change across the target donor's `q` or `q + 1` occurrences. A candidate may be feasible for one target's occurrence set and infeasible for another's. No missing occurrence is silently imputed.

### 2.4 The two pool states

Let **U** be the final eligible region-unaware candidate-key pool before injection-zone removal. Z remains the complete injection-zone donor universe from Section 2.2, including any key in K that failed a target-side gate. Let:

```text
R = U minus Z
```

be the post-removal pool. The configuration pins the ordered keys and SHA-256 digest of U, Z, R, T, and K; pins the target-eligibility-manifest digest; asserts that T and K partition Z; and asserts that R is exactly `U minus Z`. It never substitutes T for Z: target-side and region-unaware eligibility are not established to be the same predicate, so a killed target key may not re-enter the control arm.

The matcher runs twice with the same target table, edge table, rule, scaling, and software state:

1. **un-removed counterfactual:** candidates in U;
2. **post-removal authority:** candidates in R.

The un-removed result is diagnostic only. The post-removal result is the only result that may govern generation.

---

## 3. Hard eligibility and invariants

An edge is eligible only when every assertion below is true. These are filters, not weighted preferences. One-to-one use of candidates is a constraint on the *assignment* rather than on an edge — the same candidate key may not be assigned twice, and Section 6 is where that is enforced.

1. The target key belongs to T, the candidate key is valid and distinct from it, and no template is ever its own control.
2. The candidate belongs to the named pool state.
3. Target and candidate use the same pinned Neuropixels 1.0 host channel map and the same pre-injection substrate at every scheduled occurrence.
4. The candidate was rendered at every target occurrence's exact commanded placement and rescaling target using the pinned renderer configuration.
5. Relocation and rendering completed without clipping, overflow, non-finite samples, or a shape/channel mismatch.
6. At every occurrence, the realized peak remains inside the pinned injection band and the rendered support satisfies the separately approved edge-margin and placement-feasibility rule.
7. All three matching quantities are finite at every occurrence.
8. Provenance keys parse without ambiguity. A missing insertion, session, or subject key is a configuration failure, not an automatic relaxation.
9. The target-eligibility manifest, target table, exposure schedule, and target-occurrence table agree exactly on T and `N`; the exposure schedule has fifty rows, five blocks of ten distinct targets, and the quotient/remainder multiplicities fixed by Amendment 6.

The matcher receives no anatomical label column. Injection-zone membership enters only through the separately pinned full set Z used to construct R and to report the un-removed composition. **Region membership is never an edge, cost, blocking, or tie-breaking term.**

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

Two properties of that choice are stated rather than left implicit.

**Only the standard deviation reaches the objective.** The cost is built from `abs(z_target - z_candidate)`, and the common mean cancels exactly in that difference. The mean is computed and recorded because the reports standardize levels as well as differences, but it cannot change which assignment wins. "Common scaling" is therefore a claim about a common standard deviation, and nothing weaker is being relied on.

**The ruler is estimated from a pool that contains the removed donors, by construction.** U is region-unaware, so every injection-zone donor that clears region-unaware eligibility is in it — which is exactly the set removal takes out — and the standard deviations that set the relative weight of amplitude, SNR and depth are therefore computed partly from injection-zone rows even though the authoritative run is over R. That is accepted rather than overlooked, for three reasons: the requirement both amendments impose is that *one* ruler serve both runs, and either pool could supply it; U is the larger sample and the more stable estimate; and the counterfactual asks what the un-removed procedure would have done, which is most naturally priced in the units that procedure would have used. Because the argument is a preference rather than a proof, **both runs' reports additionally record the R-derived standard deviations of all three quantities**, so a reader can see how far the two rulers differ and whether the choice could have mattered. That is a diagnostic; it never re-scales the objective and never governs a selection.

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

All three quantities have equal weight, and each of the `N` target identities has equal weight in the assignment even though the exposure rota may give `r = 50 mod N` targets one additional occurrence. Donor-equal weighting gives every target weight `1/N`; exposure weighting would give the first `r` rota ranks `(q + 1)/50` and the rest `q/50`, so each extra-occurrence target would have `(q + 1)/q` times the exposure influence of every other target. Donor-equal matching prevents the rota's fixed choice of extra-occurrence donors from changing which control partner each target receives. Exposure-weighted balance is still reported separately because it describes the generated arm. No data-dependent weight, caliper, interaction term, or region term is permitted.

---

## 5. Provenance blocking and the only relaxation path

The rule uses the finest provenance level at which a complete one-to-one assignment exists **while preserving the source-count floor**. A lower continuous cost never justifies a coarser provenance level.

Let `S_T` be the number of distinct `dataset` values in the surviving target set T. This is computed from T once and is not assumed to remain four. The complete sixteen-key CA1 universe has four sources with multiplicities `[6, 5, 3, 2]`, but killing one or more targets can change both the multiplicities and `S_T`. Every pool-state run therefore uses the actual surviving target set and its actual `S_T`.

**The equality is tested at three granularities, in two levels.** The `dataset` column *is* the probe-insertion identifier, and both the session UUID and the subject are parsed out of that same string, so the three provenance levels are strictly nested: fixing which `dataset` values the selected controls use *determines* the control arm's session and subject counts as well. Let `S_T`, `E_T` and `B_T` be the distinct dataset, session and subject counts of T. **Level A** requires the selected controls to match all three. **Level B** — the count Slot 7 names literally, and the floor Amendment 2 point 3 sets — requires `S_T` alone. Level A is never weaker than Level B: it adds two conditions and removes none. Every stage below is tested at Level A first, and at Level B only if Level A admits no complete assignment *at that stage*; a stage is relaxed only when Level B also fails there. The achieved level is recorded alongside the selected stage. Where this document says "source-count equality" or "the floor" without naming a level, it names this two-level test.

**The two levels are not the same constraint, and the gap between them is measured rather than argued.** Over the pinned snapshot's 2,183 Neuropixels 1.0 rows there are 37 distinct `dataset` values, but they sit in only 24 sessions and **12 animals** — the same twelve Amendment 2 point 1 already counts. The complete CA1 universe's four sources are four sessions and four animals. Of the 66,045 four-source subsets a stage-4 control arm could use at `S_T = 4`, only **37,424 carry four distinct animals**; 28,621 carry fewer, and **74 of them draw all four sources from a single animal**. A control arm at Level B alone can therefore satisfy the floor exactly while facing a four-animal target arm with a one-animal control arm — which is the imbalance Slot 7's own sentence describes, wearing a matching source count. Level A applies the preference Amendment 2 already states in its own reasoning — that once the provenance keys are parsed rather than hashed, the sheet should ask for the stronger check the parsing makes available — to the count itself rather than only to pairwise blocking. It costs no feasibility, because Level B stays reachable at every stage. Measured by `agents/Claude/tools/source_count_granularity_probe.py` against snapshot `a6c86402…`; no host-specific pool was read.

For each pool state, construct and test these stages in order:

1. **Insertion stage plus provenance-count equality:** retain only edges whose candidate and target insertion identifiers are equal, and require a complete `N`-pair assignment satisfying the two-level test above. Level A is automatic for any complete insertion-blocked assignment, because each control then carries its target's exact `dataset` string and therefore its session and subject with it.
2. **Session stage plus provenance-count equality:** reached only if stage 1 has no complete assignment satisfying the test at either level. Retain only edges whose session identifiers are equal, and require the selected controls to satisfy the two-level test above. `E_T` and `B_T` are automatic at this stage for the same nesting reason, so Level A and Level B coincide here and `S_T` is what binds.
3. **Subject stage plus provenance-count equality:** reached only if stage 2 has no complete assignment satisfying the test at either level. Retain only edges whose subject identifiers are equal, and require the selected controls to satisfy the two-level test above. `B_T` is automatic at this stage; `E_T` is not, because two targets from different sessions of one animal may both draw controls from a single session, so Level A binds here through `S_T` and `E_T`.
4. **Unrestricted-edge stage plus provenance-count equality:** reached only if stage 3 has no complete assignment satisfying the test at either level. Permit every hard-eligible edge, and require the selected controls to satisfy the two-level test above. Nothing is automatic here, and this is the stage where the two levels differ most — it is the stage the census above measures.

If stage 4 admits no complete assignment at either level, the pool state is infeasible. There is no fifth stage without provenance-count equality at Level B.

**The floor is an equality, binds in both directions, and survives every provenance relaxation.** Slot 7 asks the arms to be balanced on the number of contributing source datasets, and its stated worry — "an arm drawn from five source datasets compared against an arm drawn from one is partly a provenance comparison wearing a region label" — is symmetric. A control set spread across more or fewer sources than T is rejected as an imbalance rather than accepted as extra diversity or unavoidable loss. The same reading applies to the sessions and animals those sources sit in, which is why Level A tests all three counts and Level B is reached only where Level A cannot be satisfied.

**That constraint is not an ordinary assignment constraint, and the implementation may not pretend it is.** Requiring an exact count of distinct sources over the selected set is a global cardinality condition that unconstrained min-cost flow and rectangular-assignment solvers do not enforce; a solver run without it can return an assignment the floor forbids, and a greedy repair returns one this rule does not define. At stages 2 through 4, the implementation must therefore enumerate candidate-source subsets of size `S_T` while requiring every source in an enumerated subset to appear at least once in the selected controls, or use another method that provably returns the Section 6 optimum under exactly that condition. For the current library there are at most 37 candidate sources and `S_T <= 4` for any surviving subset of the CA1 universe, so the largest source-subset search remains `C(37, 4) = 66,045`. Level A filters that enumeration rather than enlarging it — at `S_T = 4` it removes 28,621 of the 66,045 subsets before any assignment is attempted — so the stronger condition is also the cheaper search. Stage 1 may use the automatic equality above but must still assert it in the returned assignment.

The report records the exact constrained method and proves that the chosen result is optimal over the allowed source sets. An implementation that cannot prove optimality declares the state infeasible; it does not return its best effort. For every failed finer stage the report records both the ordinary pairwise graph's maximum matching cardinality and the result of the exact source-count-constrained feasibility search. A maximum cardinality of `N` without source-count equality does **not** make a stage feasible and does not prevent relaxation.

At a coarser stage, the assignment still preserves finer blocking wherever possible. Before continuous cost is considered, assignments are compared by:

1. larger number of insertion-matched pairs;
2. then larger number of session-matched pairs;
3. then larger number of subject-matched pairs.

Counts fixed by the chosen stage naturally tie. For example, every session-stage pair matches at session and subject level, so the insertion-match count is the only provenance count that can distinguish two session-stage assignments.

The chosen stage and all per-pair provenance levels are reported. **Infeasibility under both the stage's pairwise restriction and the source-count equality is the only trigger for relaxation.** The implementation may not relax because a coarser stage looks better on amplitude, SNR, depth, or eventual balance.

---

## 6. Global assignment objective and tie handling

Within the chosen provenance stage and after applying the provenance comparison in Section 5, select a **global** `N`-pair one-to-one assignment. A greedy nearest-neighbour pass is not this rule.

Assignments are compared lexicographically by the following tuple:

1. negative insertion-match count;
2. negative session-match count;
3. negative subject-match count;
4. total edge cost, summed with `math.fsum` in sorted target-key order;
5. largest single edge cost;
6. the vector of candidate keys aligned to sorted target keys.

The lexicographically smallest tuple wins. Float comparisons are strict; there is no unstated tolerance. The exact Python runtime and matching implementation are pinned in the later configuration, and the configuration records every input float used by the solver.

This definition fixes a unique result independently of solver strategy. An implementation may use min-cost flow, rectangular assignment, dynamic programming, or exhaustive search on a reduced graph only if it returns the assignment defined above, including the achieved provenance-count level. Before it may read a host-specific pool, it must pass synthetic fixtures and exhaustive small-domain comparisons that cover variable `N` and `S_T`, all four provenance stages, both provenance-count levels at each stage, no-reuse, self-edge rejection, objective ties, and lexical ties.

---

## 7. Required outputs for each pool state

The un-removed and post-removal reports each contain:

- pool-state name and ordered pool-key digest;
- `N`, `S_T`, the ordered T digest, and the target-eligibility-manifest digest;
- hard-eligible edge-occurrence-table digest and row count;
- the selected provenance stage and the achieved provenance-count level;
- at every failed finer stage, the ordinary pairwise graph's maximum matching cardinality and the exact constrained feasibility result at each of Level A and Level B;
- the `N` target/candidate key pairs in sorted target order;
- per pair and occurrence: provenance relationship, all target/candidate raw values and standardized differences, plus the donor-averaged edge cost;
- insertion-, session-, and subject-match counts;
- distinct insertion, session, and subject counts in each arm;
- the **multiplicity distribution** behind those counts — donors per source insertion, per session and per subject, in each arm. Slot 7's worry is provenance *concentration*, and equal counts do not settle it. The report uses the actual T distribution after eligibility; the full Z universe's historical `[6, 5, 3, 2]` distribution is recorded separately and never substituted for T;
- total, mean, and maximum edge cost;
- for each continuous quantity: donor-weighted and exposure-weighted target/control means, population standard deviations, standardized mean differences, standardized 1-Wasserstein distances, and maximum absolute paired-occurrence standardized difference;
- realized injection-zone donor count among the `N` selected controls, **reported with the comparator that belongs to the realized stage and arm size.** Amendment 5's uniform unpaired expectation measures departure from the anchor-like *policy* and is not the null distribution for a count produced by a paired, no-reuse, provenance-blocked matcher. The recorded 0.11 and 1.03 pre-host diagnostics were computed at sixteen and remain historical rather than predictions for a later `N`. Whichever comparator a report places next to the realized count is named with its sampling model and arm size;
- every relaxation and any infeasibility reason.

The joint configuration additionally records:

- the pinned U, Z, R, T, and K keys/digests; the exact full-Z removed keys; every killed target key and gate reason; and the target-eligibility-manifest digest;
- the pinned finite candidate-site set, per-site predicates, site-to-donor reduction, jointly feasible block-placement certificates, separately approved placement-rule digest, and fifty-occurrence exposure-schedule digest;
- `q`, `r`, the digest-ranked target order, and the asserted quotient/remainder and ten-distinct-target-per-block invariants;
- the U-derived scaling constants shared by both runs;
- the uniform unpaired zone-donor expectation required by Amendment 5, computed for the actual arm size `N`;
- the change from un-removed to post-removal in selected keys, provenance stage/counts, and every balance/objective quantity;
- the exact constrained source-set search method, the level it was run at, and the optimality record at the selected stage;
- the implementation hash, interpreter/dependency versions, and deterministic test record.

No selected key or failed edge is omitted from the machine-readable output. The human-readable report may summarize, but it points to the complete record.

---

## 8. Failure semantics and gate separation

The matcher fails loudly and writes no approved selection when any of these occurs:

- malformed, duplicate, ambiguous, or missing donor/provenance keys;
- a target-eligibility manifest that does not partition the full Z universe exactly into T and K, that was not evaluated under the pinned candidate-site predicates/reduction, or whose `N` disagrees with the target table;
- `N < 10` or `N > 16`; `N < 10` is recorded as the Slot 12.3 donor-feasibility outcome with the killed list, not converted into a smaller matching problem;
- an exposure schedule that does not contain exactly fifty occurrences, five blocks of ten distinct targets, the Amendment 6 digest order, or the declared quotient/remainder multiplicities;
- failure of any block's jointly feasible ten-placement host gate; the host is rejected without shrinking T or recomputing `N`;
- an R set that is not exactly U minus Z;
- mismatched host/substrate/channel-map/target-eligibility-manifest/placement-rule/renderer digests;
- missing, non-finite, or zero-variance matching quantities;
- fewer than `N` distinct candidates in a pool state;
- no complete `N`-pair assignment satisfying even Level B provenance-count equality at the unrestricted-edge stage;
- an exposure schedule whose commanded placements, spike-time seeds or placement seeds are not reproducible from the recorded master seed and per-occurrence derivation;
- solver/test disagreement or non-deterministic repeat output.

If post-removal matching is infeasible, or if its later independent balance gate fails, Slot 12.3 governs: Tier A fails for that configuration rather than rerunning this rule with new weights, new calipers, a new provenance order, or a new objective. Any change to this rule after approval requires a dated contract amendment, not a configuration edit.

**A matching result is not a balance verdict.** This rule selects the unique assignment defined above and reports the quantities the separate Tier A balance/manipulation gate grades. Approval of this document does not pre-approve any achieved distance, relaxation, host, placement calibration, or generated arm.

**A matching result is not an execution authorization.** After the host exists, both agents must explicitly approve the exact target-eligibility manifest and killed list; the U/Z/R/T/K manifests; the candidate sites, placement certificates, edge table, two matching outputs, configuration, and selected-ID state. The placement calibration and Slot 11.3 manipulation/balance gate remain separate. Only then can generation be considered, and sorter execution remains later still.

---

## 9. Implementation-before-pool requirement

The prose rule is only half of closing the forking path. Before any host-specific eligible pool or rendered edge table is constructed or opened:

1. implement this rule against synthetic inputs;
2. add exhaustive small-domain and mutation tests covering `N = 10..16`, target-manifest partitioning, the fixed full-Z removal, quotient/remainder schedules, all four provenance stages with both provenance-count levels at each, variable surviving-source multiplicities, the nested determination of session and subject counts by the selected source set, no-reuse, self-edge rejection, objective ties, lexical ties, and every failure semantic above;
3. have both agents explicitly approve the implementation and tests against this exact specification.

The implementation may live outside the Reproducibility Packet while it is exploratory. Once finalized as part of the headline pipeline, it moves into the packet with its own numbered runbook step, packet-relative `--help` example, pinned inputs, and consistency-check coverage. Adding it as a silent exception to the packet's runbook checker is not permitted.

---

## 10. Approval boundary

Codex explicitly approves Draft 3 as a **pre-pool matching-rule specification only**. The approval claim is:

> If Claude approves the same bytes, the rule's target-manifest boundary, inputs, hard eligibility boundary, full-Z removal, common scaling, donor-equal continuous cost, source-count-preserving provenance fallback, global assignment objective, tie handling, outputs, and failure semantics are fixed before any host-specific pool is visible.

This owner re-review accepts Claude's Draft 2 corrections and additions: exact source-count equality rather than a one-sided floor, the constrained-optimality obligation, common U-derived scaling with the R-derived diagnostic, donor-equal matching, provenance-concentration outputs, and named count comparators. Draft 3 corrects the one rejected reading by enforcing source-count equality at every stage, and it incorporates the now-in-force Amendment 6 rather than keeping Draft 2's target-loss question open.

No host-specific eligible pool, rendered-template table, edge table, or candidate arm was inspected during any draft. Every numerical fact retained here comes from the pinned donor-metadata snapshot `a6c86402…` and already-recorded pre-host audits. This approval is not a claim that the rule has been implemented, that any pool is feasible or balanced, or that Tier A may generate data. Claude must genuinely re-review and explicitly approve this exact state before the prose loop closes; the separately reviewed implementation and deterministic tests remain mandatory before any host-specific pool may be constructed or opened.

**Reviewer's turn.** Claude re-opened Draft 3 at `e63e1031…`, confirmed that digest on disk before reading a word, and reviewed it against the in-force contract rather than against Draft 2. Every Draft 3 decision is accepted, including the reading Codex rejected in Session 13: the provenance-count floor binds at every relaxation stage rather than as a last resort. The three Draft 4 changes are named in the Status line. One probe was run and deliberately left without an edit: the common ruler is estimated over edge-occurrences rather than over distinct candidates, so each candidate is weighted by how many target occurrence sets it is feasible for, and that weighting is not neutral with respect to depth; the unit that actually enters the cost differences is nevertheless the defensible one, so the choice stands and is recorded here instead of being carved out. **Claude explicitly approves Draft 4** and returns it for owner re-review. Approving these bytes approves a pre-pool specification and nothing downstream of it: no host, no pool, no edge table, no implementation, no generation, no sorter run.
