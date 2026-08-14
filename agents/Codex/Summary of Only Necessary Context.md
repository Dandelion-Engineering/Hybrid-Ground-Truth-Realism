# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 19 · 2026-08-14 00:14 PDT**

**Next Codex session will be Session 20.** No count-based progress report is due; the next cadence report is Session 24.

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, rendered edge table, schedule, selected donor, template-array pull, dependency installation, raw-recording read, Rung 0, hybrid generation, or sorter run occurred in Codex Session 19.

The public state remains `In Progress`. The host order, drift specification, donor-matching prose, synthetic estimator, and repository-distribution policy are pre-measurement governance/implementation, not evidence about whether realism changes sorter accuracy.

## Contract state — Amendments 1–6 are in force

Current synchronized hashes remain:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

Amendment 6 governs Tier A: Z is the full sixteen-key zone universe; one finite donor-level site set and per-site predicates produce T/K once; `N = count(T)` continues for `10 <= N <= 16`; the `1910753866` digest deal assigns fifty occurrences across five ten-distinct-target blocks; joint block-placement failure rejects the host without shrinking T; controls and pseudo-arms follow N while removal stays at full Z.

## Real-arm matching rule — prose closed, implementation absent

Artifact: `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`

Same-state-approved Draft 6 SHA-256:

`51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`

The rule fixes one target manifest, T/K/N once, full-sixteen Z removal, common U-derived scaling, donor-equal cost, deterministic global no-reuse assignment, insertion → session → subject → unrestricted provenance stages, exact count equality before the literal fallback floor, complete outputs, and loud failure semantics. Before any real target manifest, host-specific pool, or edge table, the separate exposure-schedule/placement specification and matcher implementation/tests must receive same-state approval on synthetic inputs.

## Host order — same-state approved

Artifact: `agents/Claude/Tier A Host and Injection Zone Selection.md`

Section 15 is same-state approved. The pinned order begins:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Ranks 4–13 remain the declared table order. Strict admission evaluates ranks 1–13 sequentially under the 20 µm drift rule and every later gate. If none is fully admissible, the same order restarts once under 40 µm; only then does the tracked asset-cache continuation begin in cached discovery order. No candidate has been measured on any open gate.

## Drift implementation — same-state approved and closed

Claude owner-approved Codex's exact repaired states, so the implementation loop is closed:

- `Reproducibility Packet/scripts/utils/band_drift.py`: `d8b035968416b335d7ef1bdd0d915c03aec4a64649defa8795c8c013fc70c069`
- `agents/Claude/tools/test_band_drift.py`: `82aaf77e99f20b158a54b6acfc848fc2626047aa350bebd8b3bd988b7ce48f03`

The module implements complete 60-second bins, median-centred per-unit traces, the band median, `Delta_full`, worst-ten-bin `Delta_10`, the deterministic 200-permutation within-unit null, nearest-rank 190th-of-200 `Q95_null`, and the two-number gate. It restricts observation and permutation to complete-bin spikes, fails loudly on mismatched collections and malformed row identifiers, and rejects an unmeasurable observation before constructing its null. The harness passes **57 checks, 0 failed** at the pinned 200 permutations.

## Drift Draft 13 — Codex-approved, Claude owner re-review open

Active chat: `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

Codex explicitly approves and handed back:

- host-selection Draft 13: `82d58b4009774adc63817da78be247c137cd5fa105e5553a8fe1c4e775349cc8`
- supporting review probe: `4f3b83773156e7f9654f3e080d5adb258658cf500cf741aaea04b5015f07c34f`

Claude must genuinely owner-re-review both exact states before any candidate is read.

### Draft 12 content Codex accepted

The bin grid consumes an anchor and an extent in the processed `spike_times` clock. The existing `host_timing_index.jsonl` value is a raw-stream span (`t_last_s - t_first_s`), not an endpoint. Rank-1 CSHL047 Probe01 begins at 1.138489 s; three other Probe01 series begin about 1.0–1.3 s after zero. The processed `spike_times` description names no origin.

The future archive CLI must reconcile the clocks before computing. An unreconciled clock is an **input error to resolve**, not a host rejection, and the pinned first-admissible order does not advance past it.

### Codex Session 19 repairs

1. **Observable bound only.** Draft 12's statement that a mis-scaled null “can never admit a moving one” overclaimed its probe. Draft 13 says only that no `Q95_null` can change the rejection when observed `Delta_10 > L`; null scaling can change only the resolution verdict among candidates whose observed excursion is already at or below the gate. It explicitly leaves physical movement underestimated by IBL's depth trace outside that guarantee.
2. **Current implementation state.** Draft 12 still said the estimator was unimplemented. Draft 13 records the same-state-approved module and harness and correctly identifies the archive-reading CLI, runbook step, and candidate measurement as the unbuilt work.

The supporting probe received the same wording correction with no numerical change and passes **3 of 3** checks.

## Repository checkout bytes — Codex-approved, Claude re-review open

Codex approves `.gitattributes` SHA-256:

`036c696c3e1ea9cef70925ec8dfedc407ef59bb20e5c00e17ef9b5f88855bfa0`

The policy defaults the repository to `* -text`; 17 framework/workspace paths and 11 legacy packet outputs explicitly use `text eol=crlf` to reproduce their tested CRLF working representation. Codex changed only the explanation: the named exceptions opt into Git text normalization and CRLF checkout, so saying every file was stored as-is was inaccurate.

A temporary commit cloned under `core.autocrlf=true` matched **153 of 153** reviewed tracked files byte-for-byte. The temporary ref was removed and the clone was sent to the Recycle Bin. Claude owner re-review remains open on the exact comment-corrected state.

## Reproducibility Packet state

The earlier design-stage review remains concluded at:

- packet README `3b07aa5b94203d3f4c826be7aac40e6550c2a13e7d3b45c997399a84af3df4a1`
- checker `4eb9401825ec2a4561abf46dc7dc82d89ea316722d338bba9e84bd747d83c651`
- mutation harness `d64134b1485a8550412c1eb7fba7fd98ab509471050cad71a41fc8f704d5acc3`

The drift utility is a later same-state-approved addition. The archive-reading drift CLI and runbook Step 11 do not exist. The headline experiment and Slot 8 `verify_realism.py` do not exist because no result exists. The ten-step runbook consistency checker passes.

## Separate gates — do not collapse

1. Claude owner re-review of Draft 13, the review-probe wording, and `.gitattributes`;
2. archive-reading drift CLI, its first scoped packet step/review, and candidate measurement down the pinned order;
3. exposure-schedule/placement specification, implementation, synthetic tests, and same-state approval;
4. matcher implementation, exhaustive/mutation tests, and same-state approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact candidate sites, T/K/N, U/Z/R, edge table, un-removed/post-removal matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. generation authorization;
10. Rung 0/sorter execution authorization.

Reviewer edits, commits, downstream use, and silence are not same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. Session 19 appended a forward correction narrowing the drift guarantee to observed `Delta_10`, recorded the 153/153 independent clone check, and retained the no-result/no-execution boundary.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- No count- or event-triggered progress report was due in Codex Session 19.

## Validation and append-only boundary

- Draft 12 and `.gitattributes` handoff digests were verified before review.
- The raw timing records and processed `spike_times` description were rechecked.
- The full drift harness passes 57/57 checks at 200 permutations; the review probe passes 3/3.
- The packet checker passes all ten steps.
- The reviewed temporary distribution commit cloned with 153/153 byte-identical files.
- Chat append used the verified UTF-8 physical tail, pre-write line count 1,044, one unique EOF anchor, exactly one new Session 19 header after the prior count, an unchanged 146,519-byte prefix, and post-write LF-tail checks.
- No heavy work, dependency install, network read, archive read, raw-data read, template pull, Rung 0, generator, or sorter run occurred.

`agents/Codex/Session Summaries/HumanReport19.md` contains the full rationale, file list, and validation evidence.
