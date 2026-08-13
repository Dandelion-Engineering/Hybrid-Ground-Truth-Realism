# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 17 · 2026-08-13 07:23 PDT**

**Next Codex session will be Session 18.** No count-based progress report is due; the next cadence report is Session 24.

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate drift value, target-eligibility manifest, host-specific eligible pool, rendered edge table, schedule, selected donor, template-array pull, dependency installation, raw-recording download, Rung 0, hybrid generation, or sorter run occurred in Codex Session 17.

The public state remains `In Progress`. The approved donor-matching prose and Draft 9 host/drift proposal are pre-measurement governance, not evidence about whether realism changes sorter accuracy.

## Contract state — Amendments 1–6 are in force

Current synchronized hashes remain:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

Amendment 6 governs Tier A: Z is the full sixteen-key zone universe; a pinned finite site set and per-site predicates produce T/K once; `N = count(T)` continues for `10 <= N <= 16`; the `1910753866` digest deal assigns fifty occurrences across five ten-distinct-target blocks; joint block-placement failure rejects the host without shrinking T; control and pseudo-arms follow N while removal stays at full Z.

## Real-arm matching rule — prose loop closed

Artifact: `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`

**Same-state-approved Draft 6 SHA-256:**

`51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`

Claude's Session 17 review accepted Draft 5 and added three clarifications. Codex genuinely owner-re-reviewed those exact bytes and accepted all three unchanged:

1. The separate schedule/placement specification must choose whether each occurrence's placement is independently derived and jointly verified, or one deterministic block-level algorithm derives all ten rendered placements. Amendment 6 leaves both readings open; the specification must choose and pin one.
2. The target manifest is behind all four pre-pool implementation steps, not only behind the schedule specification. The matcher and its tests must be fixed on synthetic inputs before `N`, `S_T`, `E_T`, or `B_T` is visible.
3. Host candidate order is an external dependency of the host-rejection semantics and belongs to Claude's selection artifact rather than this matcher.

The matching-rule chat is concluded at `chats/Claude-Codex/Tier A Donor Matching Rule/`. `Summary.md` records the exact approved state; any implementation/test review starts in a new scoped chat.

Draft 6 still fixes:

- one target manifest; T/K partition full Z once; N never recomputed;
- U un-removed and `R = U minus Z`, with only R executable;
- one U-derived float64 ruler for realized amplitude, effective host SNR and depth, plus R-derived diagnostic standard deviations;
- donor-equal cost and separate exposure-weighted balance reporting;
- insertion → session → subject → unrestricted provenance stages, with Level A insertion/session/subject-count equality attempted before Level B's literal insertion-count floor at every stage;
- deterministic global no-reuse assignment, self-edge rejection, strict lexicographic objective/ties, complete outputs and loud failures.

## Host selection Draft 9 — Codex-approved, Claude owner re-review open

Artifact: `agents/Claude/Tier A Host and Injection Zone Selection.md`

**Codex-approved Draft 9 SHA-256:**

`3e48873b03f60fa1cc59a0940ac8f79a8e91521203b8a88f1689e96c9cb27a8c`

Active chat: `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`.

Codex explicitly approved Sections 13–14 as handed off: the zone-neighbour audit remains bounded, the paired 0.11 and unpaired 0.12 expectations are distinct models, and Amendment 5 correctly supersedes Amendment 3's stale chance-zone clause.

Draft 8's thirteen-host rank list was correct. Draft 9 preserves ranks 1–13, beginning:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Ranks 4–13 remain the rest of the existing table by descending CA1 channel count and ASCII `(subject, session, probe)` ties. If both threshold passes fail on all thirteen, extensions follow the tracked asset-cache order at SHA-256 `54f8e600ccedf36f2b284a9dacc58277aed24155f9a6915ad60b339437392f70`, never a refreshed live listing or a gate-informed re-sort.

### Drift rule repaired before measurement

Draft 8 correctly retired `cumulative_drift_um_per_hour`: its first-party description says it is summed absolute per-spike depth path length, scales with spike count, and is not electrode displacement. It correctly found that the processed units table already carries aligned ragged `spike_times` and `spike_distances_from_probe_tip_um` inputs.

Codex repaired five decision-rule defects before approving Draft 9:

1. `max D - min D` is a peak-to-peak band excursion, not net displacement. The context quantity is now `Delta_full`; `Delta_10` is the maximum range over ten consecutive complete 60-second bins.
2. A final partial minute is discarded and reported. Included units require at least ten spikes in at least 80% of complete bins; every complete bin needs at least five valid included-unit medians, otherwise the candidate is unmeasurable rather than silently omitting the bin.
3. The null holds times/bin counts fixed and permutes depth values within each unit. The 200 permutations are deterministic: master seed `3175830281` from SHA-256 phrase `Hybrid Ground Truth Realism|Tier A|drift permutation null|v1`, domain-separated per asset/probe/unit-row/permutation, using pinned NumPy `PCG64`. `Q95_null` is the nearest-rank 190th of 200 sorted values.
4. At threshold L, drift passes only if both `Delta_10 <= L` and `Q95_null <= L`. An observed value inside its null is not automatically rejected: a quiet host may look like no drift. A noise bound wider than L is the unmeasurable failure.
5. Twenty micrometres is a declared one-row tolerance, not a claim that sub-pitch motion is invisible or peak-channel-invariant. Kilosort-family-derived host screening does not directly define an arm, but can condition treatment-effect heterogeneity and therefore the interaction as well as `G0`; the result is conditional on that screened host.

The strict pass evaluates ranks 1–13 sequentially under L = 20 µm and all later gates. If no fully admissible host exists, the single predeclared L = 40 µm relaxation restarts the same rank order; threshold-independent results may be reused, but admissibility is recomputed. Only after all thirteen fail at 40 µm does the cached discovery-order extension begin at 40 µm.

**Claude must genuinely owner-re-review Draft 9 before the drift implementation or any candidate measurement.** The implementation must still confirm the ragged index, finite aligned columns, exact NumPy version and byte-for-byte null replay.

## Separate gates — do not collapse

1. Claude exact-state owner re-review of host-selection Draft 9;
2. host-order/drift prose convergence;
3. drift implementation and targeted metadata-only candidate measurements down the pinned order;
4. exposure-schedule/placement specification, implementation, synthetic tests and same-state approval;
5. matcher implementation, exhaustive/mutation tests and same-state approval;
6. noise and post-rescaling effective-SNR host gates;
7. footprint/placement calibration;
8. exact candidate sites, target manifest, T/K/N, U/Z/R, edge table, two matching outputs and selected IDs;
9. independent Tier A balance/manipulation approval;
10. generation authorization;
11. Rung 0/sorter execution authorization.

Reviewer edits, downstream use, later commits and silence do not substitute for same-state approval.

## Reproducibility Packet state

The design-stage packet review remains concluded. Same-state-approved hashes remain:

- packet `README.md`: `3b07aa5b94203d3f4c826be7aac40e6550c2a13e7d3b45c997399a84af3df4a1`
- checker: `4eb9401825ec2a4561abf46dc7dc82d89ea316722d338bba9e84bd747d83c651`
- mutation harness: `d64134b1485a8550412c1eb7fba7fd98ab509471050cad71a41fc8f704d5acc3`

Later matcher/schedule/drift additions begin new scoped reviews and must keep one command per numbered runbook step/example. The headline experiment and Slot 8 `verify_realism.py` do not exist because no result exists.

## Public and director state

- Root `README.md` remains State A / `In Progress`. Session 17 appended a forward correction for the unmeasured drift rule and recorded that the donor-matching prose is now same-state approved while implementation remains absent.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- No count- or event-triggered progress report is due in Codex Session 17.

## Validation and machine boundary

- Draft 6's handed-off digest was verified before owner approval.
- Draft 8's handed-off digest was verified before review; Draft 9 is `3e48873b…`.
- The asset-cache digest and drift master-seed derivation were independently checked.
- Both append-only chat writes used verified UTF-8 physical tails, pre-write line counts, unique EOF anchors, exactly one new Session 17 header after the prior count, and post-write tail reads.
- The donor-matching transcript was renamed to `Concluded` only after the approval append; its summary was then created.
- No heavy work, dependency install, network read, raw-data read, template pull, Rung 0, generator or sorter run occurred.

`agents/Codex/Session Summaries/HumanReport17.md` contains the full review rationale, file list and validation evidence.
