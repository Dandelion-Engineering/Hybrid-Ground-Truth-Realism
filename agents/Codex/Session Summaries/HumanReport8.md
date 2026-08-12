# Human Report 8 — Codex

**Current date and time:** 2026-08-12 13:13 PDT

**Session:** Codex Session 8

**Phase at start:** Phase 2 — Execution

**Phase at end:** Phase 2 — Execution. Amendments 1, 2 and 4 are `In force`; Amendment 3 remains `Proposed` at a new Codex-approved reviewer state awaiting Claude owner re-review. **No host is pinned, no hybrid recording or sorter run occurred, and no scientific result about the project's question exists.**

---

## Summary

This session completed the exact-state review Claude handed back in Session 8, independently checked the amplitude-convention evidence, closed same-state review of the Tier A selection artifact through Draft 5, and repaired three defects in the proposed negative-control selector before approving a new synchronized Claim Sheet state.

The most consequential repair was an identifier failure hiding in ordinary-looking metadata. The contract and proposed selector treated `template_index` as though it uniquely named a donor template. It does not: the tracked Neuropixels 1.0 snapshot has 2,183 rows but only 187 distinct integer values because the counter restarts in every source dataset. The pair (`dataset`, `template_index`) is unique across all 2,183 rows. Both sheets now require that two-part key for every real and pseudo donor configuration and explicitly clarify the earlier Slot 7 shorthand.

The selector was also not deterministic despite having a fixed seed. A seed does not specify the random-number generator, starting draw, candidate-swap order, improvement rule, tie rule, or what happens when the evaluation budget expires. The revised Amendment 3 now fixes a hash-ranked starting subset, complete best-improvement swap sweeps, pair-based ties, a no-partial-sweep 100,000-evaluation ceiling, stop-reason reporting, and loud failure for non-finite or zero-variance covariates. It says directly that this is a bounded search rather than a global-optimum claim.

Finally, Claude's rationale said better covariate matching necessarily narrows the sorter-derived diagnostic band and worse matching widens it. That monotonic relationship is plausible but unmeasured and not guaranteed. I replaced it with the evidence-safe reason to precommit: once the pool is visible, multiple defensible objectives or searches could be tried and the most reassuring retained. The rule is fixed early to close that forking path, not because the project already knows how selector score maps to sorter behaviour.

## Context ingested and cross-review performed

I followed the full `AgentPrompt.md` startup workflow after the turn and lock gates:

- read `Project Details/Project Details.md` in full;
- read Codex's continuity summary;
- read every Codex-including chat summary and the full active Tier A transcript before replying;
- read `Playbooks/review-cycle.md`, `claim-sheet.md`, `accessible-claim-sheet.md`, `accessible-piece.md`, `live-run-readme.md`, and `research-progress-report.md` as routed by the current work;
- read Claude's latest `HumanReport8.md`, the exact Claim Sheet states, Draft 5, the new amplitude script, raw JSON, text report, public README entry, and relevant pinned upstream code.

The review response was appended to the live transcript with the append-only safeguards: 426 physical UTF-8 lines before the write, a unique multi-line EOF anchor, exactly one Session 8 Codex header after that boundary, and a re-read showing 457 lines after the append.

## Exact-state decisions

### Tier A selection artifact — approved at its real scope

**I explicitly approved**:

- `agents/Claude/Tier A Host and Injection Zone Selection.md`
- SHA-256 `7c4b911df9e53032ae7cd0453cc51ac79b4d65fdfa40abcd41577ad027be69db`

Claude had already explicitly approved that exact Draft 5 state. The Draft 5 same-state review is therefore closed.

The approval is bounded to the host-selection strategy, CA1 recommendation, measured provenance, anatomy/duration/label findings, parameterized placement screen, native-yield context, and the one-session amplitude-convention audit. It is **not** a pinned-host approval. Drift, noise, post-rescaling effective SNR, placement calibration, and Codex's balance gate remain open.

### Claim Sheets — new reviewer-approved states, owner re-review open

I directly edited and **explicitly approved** synchronized whole-file states:

- `Claim Sheet.md` — SHA-256 `5b6c2ee70f81585fbe291f90e02eb4a312f55eb045356063b34f60c591cb7a09`
- `Accessible Claim Sheet.md` — SHA-256 `d9bb991ba02b8bae8360bbbd565512b873cafc8b0288b8f84aba4557a610ad46`

Amendments 1, 2 and 4 remain `In force`. Amendment 3 remains `Proposed` pending Claude's genuine owner re-review of these exact states. Tier A generation remains blocked. Even if Amendment 3 reaches `In force`, a later tracked configuration must separately pin the eligible pool, selected two-part identifiers, achieved distances, evaluated-swap count, and stopping reason; both agents must approve that exact configuration before pseudo-arm generation.

## Amplitude-convention evidence review

Claude's new script correctly distinguishes:

- donor `amplitude_uv`: peak-to-peak range over time of an average waveform at the donor builder's best channel; and
- host `median_spike_amplitude_uV`: the median over per-spike peak amplitudes in the NWB units table.

I checked the claimed donor definitions directly against `SpikeInterface/hybrid_template_library` commit `0023db29688842f74698bac40c48a86477ea39e7`, including the peak-to-peak computation, best-channel rule, good-clusters-only extractor setting, last-30-minute window, and preprocessing chain. I independently recomputed the saved raw JSON summaries rather than trusting the report:

- 1,821 units;
- median peak-to-peak / host-amplitude ratios of 1.250075 for all units, 1.242173 for Kilosort `good`, and 1.206978 for IBL-quality-1 units;
- 72.597% all-unit agreement between the two best-channel conventions;
- 2,183 NP1.0 rows, 187 unique bare indices, 2,183 unique (`dataset`, `template_index`) pairs;
- sixteen CA1 donors with the recorded 105–487 µV amplitudes; and
- 41.96% of the full NP1.0 pool above 200 µV, consistent with the reported 42.0%.

The result remains bounded correctly: it measures a definitional conversion in one session. It does not show that donor and host preprocessing are equivalent, and it does not support a per-neuron conversion factor.

I fixed one stale script docstring discovered during review. It still said the script would fail when its peak-to-peak best channel disagreed with the NWB's named `max_electrode`. The implementation correctly treats that disagreement as a sensitivity result. The docstring and `read_units()` exception contract now say what the code actually does. Numerical code and tracked results were untouched. The script compiles and its CLI help returns successfully in the project venv.

## Scale-factor ruling

Claude asked whether the systematically different pre-rescaling factors should enter Codex's balance gate as a declared covariate.

**Decision: no new matching covariate and no new pass/fail threshold.** In pinned SpikeInterface 0.104.8, template rescaling applies a scalar division to each template array. Once actual rendered post-rescaling amplitude, effective host SNR, footprint/placement, and provenance are gated, the pre-rescaling scalar is not a separate signal property the sorter observes. Matching the scalar would instead constrain original donor amplitude and risk over-controlling a property linked to the intended region manipulation.

The factor still belongs in the record. Rung 0 must report per-arm factor distributions and extremes and verify finite factors, no clipping/overflow, and achieved rendered amplitudes. If the real preprocessing or generator path makes rescaling non-linear, that is new evidence requiring an amendment rather than a reason to add a post-hoc covariate now.

## Public heartbeat and director report

The public README was updated because this was noteworthy rather than routine: it now records that the original identifier repeated across datasets, that the selector's starting/search/tie/cap rules were not fully fixed, and that the unproved monotonic-band rationale was removed. The running log was appended without rewriting prior entries. The current orientation footer was also corrected: Amendments 1, 2 and 4 are in force; only Amendment 3 remains in same-state review.

Codex Session 8 is the mandatory count-based reporting trigger. I wrote `agents/Codex/Progress Reports/Progress Report Session 8.md` at the director-facing, plain-language bar. It explains the negative control, the identifier and selector repairs, the amplitude finding, what is working, what remains open, and the next gate sequence. It deliberately states that the Slot 8 verification artifact has no new state because no experiment or result exists.

## Challenges and reasoning paths

### A fixed seed looked more complete than it was

The first temptation was to accept the selector because it named a seed, objective, search ceiling and tie-break. Reconstructing two independent implementations exposed the missing choices. The fix was not “more prose” in general; it was to name exactly the degrees of freedom that can change selected IDs while leaving the high-level method apparently unchanged.

### The objective rationale needed a scientific, not procedural, correction

The early-pinning conclusion was sound, but one argument for it was not. I preserved the conclusion while replacing the unsupported monotonic claim with the correct multiple-analysis-path concern. This keeps the amendment strong without pretending a relation between matching score and sorter-band width has already been measured.

### The identifier bug crossed the real/pseudo boundary

The immediate defect appeared in Amendment 3, but the same shorthand already existed in the in-force Slot 7. Rewriting Slot 7 would violate the amendment discipline. The proposed amendment therefore records the measured repetition, fixes the identifier for its own selector, and explicitly clarifies the earlier shorthand for all subsequent real and pseudo configurations. History stays intact; the operative key becomes unambiguous.

### Scale factor was visible but not automatically a covariate

The observed arm difference is worth reporting, but “different between arms” is not enough to make something a matching variable. I followed the actual transformation path: the scaler changes the array linearly; the sorter observes the final waveform; and the existing gates already measure the output properties. The factor becomes a diagnostic and integrity check, not a balance target that could erase part of the intended donor-population difference.

## Validation performed

- `git diff --check` passed (Git emitted only the repository's existing LF→CRLF working-copy warnings).
- `audit_amplitude_conventions.py` compiled under `./venv/Scripts/python.exe` and its `--help` path succeeded.
- Independent JSON and CSV recomputation reproduced the reported counts, medians, CA1 amplitude list, high-amplitude proportion, and identifier uniqueness.
- Pinned first-party source lines were read live for the donor builder, consolidation path, template scaler, and generator.
- Claim Sheet and Accessible Claim Sheet Amendment 3 states were checked for synchronized meaning.
- The active-chat append was physically re-read and asserted exactly once after the pre-write boundary.
- No dependency was installed, no raw recording was downloaded, no template array was pulled, no hybrid generator or sorter ran, and no Rung 0 work was executed.

## Machine state

Measured at 2026-08-12 13:13 PDT for the session record, not as admission evidence for a future heavy job:

- system RAM: 14.34 GiB free of 31.67 GiB;
- GPU memory: 872 MiB used, 15,091 MiB free of 16,311 MiB.

These values authorize nothing later. Every heavy step still requires an immediate fresh measurement and the Claim Sheet floors/caps.

## Files created or updated

### Created

- `agents/Codex/Progress Reports/Progress Report Session 8.md` — required count-based director progress report.
- `agents/Codex/Session Summaries/HumanReport8.md` — this session record.

### Updated

- `Claim Sheet.md` — Amendment 3 identifier, deterministic bounded selector, failure conditions, configuration outputs, and evidence-safe precommit rationale.
- `Accessible Claim Sheet.md` — synchronized plain-language Amendment 3 changes.
- `Reproducibility Packet/scripts/audit_amplitude_conventions.py` — docstring/exception-contract correction only; numerical logic unchanged.
- `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` — append-only exact-state verdict and scale-factor ruling.
- `README.md` — append-only public heartbeat plus current amendment-status correction.
- `agents/Codex/references.md` — pinned-source links, linear rescaling evidence, unique identifier finding, and how both shaped this review.
- `agents/Codex/README.md` — updated workspace map and ownership/status pointers.
- `agents/Codex/Summary of Only Necessary Context.md` — fully rewritten for Session 9 continuity.

## Next steps

1. Claude must re-open and genuinely review Claim Sheet hashes `5b6c2ee7…` / `d9bb991b…`; Amendment 3 stays proposed until same-state approval exists.
2. Preserve Amendment 3 approval and the later host-dependent selector-configuration approval as separate gates.
3. Prepare the two-part placement calibration: donor multichannel footprint for edge margin, and an independently justified minimum peak separation from native peak depths plus generator constraints.
4. Continue first-admissible host gating in order: drift, noise, post-rescaling effective SNR, placement, then the full balance/manipulation gate. Do not turn native yield or scale factor into silent thresholds.
5. Build and pin the pre-injection Rung 0 host substrate before any injected template can be phase-shifted twice.
6. Measure fresh RAM and VRAM immediately before any heavy step; the daytime convention is not a reservation.
7. Start no Tier A generation until the host, Amendment 3, and exact selector-configuration gates all close explicitly.
