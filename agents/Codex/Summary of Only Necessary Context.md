# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 21 · 2026-08-14 04:19 PDT**

**Next Codex session will be Session 22.** No count-based progress report is due; the next cadence report is Session 24.

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, rendered edge table, schedule, selected donor, template-array pull, dependency installation, raw-recording read, Rung 0, hybrid generation or sorter run occurred in Codex Session 21.

The public state remains `In Progress`. Host ordering, drift governance, donor-matching prose, synthetic estimators and review probes are pre-measurement design/implementation work, not evidence about whether realism changes sorter accuracy.

## Contract state — Amendments 1–6 are in force

Current synchronized hashes remain:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

Amendment 6 governs Tier A: Z is the full sixteen-key zone universe; one finite donor-level site set and per-site predicates produce T/K once; `N = count(T)` continues for `10 <= N <= 16`; the `1910753866` digest deal assigns fifty occurrences across five ten-distinct-target blocks; joint block-placement failure rejects the host without shrinking T; controls and pseudo-arms follow N while removal stays at full Z.

## Real-arm matching rule — prose closed, implementation absent

Artifact: `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`

Same-state-approved Draft 6 SHA-256:

`51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`

Before any real target manifest, host-specific pool or edge table, the separate exposure-schedule/placement specification and matcher implementation/exhaustive tests must receive same-state approval on synthetic inputs. The rule fixes T/K/N once, full-sixteen Z removal, a common U-derived ruler, donor-equal global no-reuse assignment, provenance stages, complete counterfactual outputs and loud failure semantics.

## Host order — same-state approved

Artifact: `agents/Claude/Tier A Host and Injection Zone Selection.md`, §15.

The pinned order begins:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Ranks 4–13 remain the declared table order. Strict admission evaluates ranks 1–13 sequentially under the 20 µm drift rule and every later gate. If none is fully admissible, the same order restarts once under 40 µm; only then does tracked asset-cache continuation begin in cached discovery order. No candidate has been measured on any open gate.

## Drift Draft 17 — Codex-approved, Claude owner re-review open

Active chat: `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

Claude owner-approved Draft 16 at `7fed750c…`. Codex accepted its pre-measurement policies and cached facts but blocked two one-way safety claims with executable counterexamples, directly repaired the artifact and explicitly approved:

- host-selection Draft 17: `709be46fd0f1d23c7677787410419cf63a7ff5a03945bc88bff2c9db625909eb`.

Claude must genuinely owner-re-review those exact bytes before the archive-reading CLI is written or any candidate is read. §16 remains open meanwhile.

### What Draft 16 got right

- The drift-screen unit set must be pinned; a `good`-only interpretation would make rank 9 unmeasurable by construction with one `good` band unit and would leave five additional candidates near the five-unit validity floor.
- The selected set remains label-blind because `kilosort2_label` is a sorter-confidence label rather than a direct temporal-support criterion, and using it as a filter would covertly reinstate the native-yield gate §10.4 declined.
- Rank 1 has `t_first_s = 1.138489…`, so session-grid bin 0 has 58.86 seconds of AP coverage inside a full 60-second clock interval; this treatment must be declared and reported.
- Five pinned candidate series are exactly nominal `i / 30000` timestamp arrays and eight carry fitted alignments; this does not contradict the converter's session-clock semantics.

### Why Draft 16 was blocked

1. **Adding label-blind units is not guaranteed pessimistic.** At the pinned estimator settings, five units sharing a 30 µm ramp fail at `Delta_10 = 24.545 µm`, `Q95_null = 11.591 µm`; adding six flat traces makes the eleven-unit set pass at `0/0 µm`. Same-set null construction does not guarantee that changing the set widens `Q95_null` enough to prevent a pass.
2. **Retaining a head bin is not guaranteed pessimistic.** A deterministic fixture lowers `Delta_10` from `8.346` to `7.966 µm` when its first bin is retained.
3. **Containment margins are endpoint slack, not a general resolution.** They do not bound arbitrary internal offset, scale or time-varying disagreement.

Executable evidence: `agents/Codex/tools/probe_draft16_safety_claims.py`, SHA-256 `af51fe507be92bcbd0b8b2d7063fcc20e2208f78905b9cceb1d8ef30717bf205`. The fixtures are possible failure shapes, not candidate results.

### Draft 17 rule

- Retains the label-blind set but states the result is conditional on movement being expressed in enough IBL depth traces for the across-unit median to carry it; §16.5's systematic-bias boundary remains operative.
- Requires total/`good` counts, unit-table row identifiers and stored labels for both in-band and temporally included sets.
- Retains rank 1's head-undercovered bin as a declared session-grid choice but assigns it no one-way safety guarantee.
- Uses full-width session-grid terminology consistently and calls the clock-containment quantities endpoint slack.
- Changes no threshold, candidate order, statistic, permutation seed, window or verdict rule.

## Drift utility — numerical logic unchanged, exact state reopened

The previously same-state-approved implementation was:

- `Reproducibility Packet/scripts/utils/band_drift.py`: `d8b035968416b335d7ef1bdd0d915c03aec4a64649defa8795c8c013fc70c069`.

Codex Session 21 changed only the public parameter name and documentation from recording `duration_s` to session-time `extent_s`, explicitly defined as raw AP `t_last_s` rather than the timing screen's span. This prevents the future CLI from passing the wrong field while leaving numerical branches untouched. Codex approves:

- renamed utility: `b2c016053b18ffb49b0e9e3c439af22a7ea1d6b1b306857fe9d9b9f0eea9ac66`.

Claude owner re-review is required before this exact-state loop closes. The unchanged supporting states remain:

- `agents/Claude/tools/test_band_drift.py`: `82aaf77e99f20b158a54b6acfc848fc2626047aa350bebd8b3bd988b7ce48f03` — 57 checks at 200 permutations;
- `agents/Claude/tools/probe_band_drift_claims.py`: `4f3b83773156e7f9654f3e080d5adb258658cf500cf741aaea04b5015f07c34f` — 3 of 3 claim probes.

The archive-reading CLI and runbook Step 11 do not exist.

## Repository checkout bytes — closed

Both agents approve `.gitattributes` SHA-256:

`036c696c3e1ea9cef70925ec8dfedc407ef59bb20e5c00e17ef9b5f88855bfa0`

The policy defaults the repository to `* -text`; 17 framework/workspace paths and 11 legacy packet outputs explicitly use `text eol=crlf` to reproduce their tested CRLF representation. The last reviewed fresh clone matched all tracked files byte for byte.

## Reproducibility Packet state

The earlier design-stage review remains concluded at:

- packet README `3b07aa5b94203d3f4c826be7aac40e6550c2a13e7d3b45c997399a84af3df4a1`;
- checker `4eb9401825ec2a4561abf46dc7dc82d89ea316722d338bba9e84bd747d83c651`;
- mutation harness `d64134b1485a8550412c1eb7fba7fd98ab509471050cad71a41fc8f704d5acc3`.

The utility is a later addition whose renamed exact state is under owner review. The archive-reading CLI and runbook Step 11 do not exist. The headline experiment and Slot 8 `verify_realism.py` do not exist because no result exists. The ten-step runbook consistency checker passes.

## Separate gates — do not collapse

1. Claude owner re-review of Draft 17 and renamed utility;
2. archive-reading drift CLI, its scoped packet step/review, and candidate measurement down the pinned order;
3. exposure-schedule/placement specification, implementation, synthetic tests and same-state approval;
4. matcher implementation, exhaustive/mutation tests and same-state approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact candidate sites, T/K/N, U/Z/R, edge table, un-removed/post-removal matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. generation authorization;
10. Rung 0/sorter execution authorization.

Reviewer edits, commits, downstream use and silence are not same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. Codex Session 21 appended a forward correction withdrawing the two false safety guarantees while keeping the policies predeclared and no-result-bounded.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- No count- or event-triggered progress report was due in Codex Session 21.

## Validation and append-only boundary

- Draft 16's handed-back digest was verified before review.
- Cached unit-count and timing claims were independently reproduced.
- The full drift harness passes 57/57 checks at 200 permutations; the existing claim probe passes 3/3; the new Draft 16 safety probe reproduces both counterexamples.
- The packet checker passes all ten current steps.
- `git diff --check` was clean at the reviewed state.
- Chat append preserved the prior 170,082-byte prefix exactly at SHA-256 `094719b5…`, added exactly one Session 21 header after line 1,178 and passed strict UTF-8/tail checks. The terminology-only hash correction preserved the subsequent 173,943-byte prefix at SHA-256 `c61f6de7…` and added exactly one correction header after line 1,209.
- No heavy work, dependency installation, network/archive/raw-data read, template pull, Rung 0, generator or sorter run occurred.

`agents/Codex/Session Summaries/HumanReport21.md` contains the full reasoning, files and validation evidence.
