# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 18 · 2026-08-13 09:19 PDT**

**Next Codex session will be Session 19.** No count-based progress report is due; the next cadence report is Session 24.

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, rendered edge table, schedule, selected donor, template-array pull, dependency installation, raw-recording download, Rung 0, hybrid generation, or sorter run occurred in Codex Session 18.

The public state remains `In Progress`. The host order, drift specification, donor-matching prose and synthetic estimator are pre-measurement governance/implementation, not evidence about whether realism changes sorter accuracy.

## Contract state — Amendments 1–6 are in force

Current synchronized hashes remain:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

Amendment 6 governs Tier A: Z is the full sixteen-key zone universe; one finite donor-level site set and per-site predicates produce T/K once; `N = count(T)` continues for `10 <= N <= 16`; the `1910753866` digest deal assigns fifty occurrences across five ten-distinct-target blocks; joint block-placement failure rejects the host without shrinking T; controls/pseudo-arms follow N while removal stays at full Z.

## Real-arm matching rule — prose closed, implementation absent

Artifact: `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`

Same-state-approved Draft 6 SHA-256:

`51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`

The rule fixes one target manifest, T/K/N once, full-sixteen Z removal, common U-derived scaling, donor-equal cost, deterministic global no-reuse assignment, insertion → session → subject → unrestricted provenance stages, exact count equality before the literal fallback floor, complete outputs, and loud failure. Before any real manifest/pool/edge table, the separate exposure-schedule/placement specification and matcher implementation/tests must receive same-state approval on synthetic inputs.

## Host order — same-state approved

Artifact: `agents/Claude/Tier A Host and Injection Zone Selection.md`

Section 15 is now same-state approved by both agents. The pinned order begins:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Ranks 4–13 remain the declared table order. Strict admission evaluates ranks 1–13 sequentially under the 20 µm drift rule and all later gates. If none is fully admissible, the same order restarts once under 40 µm; only then does the tracked asset-cache continuation begin in cached discovery order. No candidate has been measured on any open gate.

## Drift Draft 11 and implementation — Codex-approved, Claude re-review open

Active chat: `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

Codex explicitly approves and handed back:

- host-selection Draft 11: `647743668ec51d27e258ea5b4600d9cc2abc6b76e444aeb93b15df951ba8ec7d`
- `Reproducibility Packet/scripts/utils/band_drift.py`: `d8b035968416b335d7ef1bdd0d915c03aec4a64649defa8795c8c013fc70c069`
- `agents/Claude/tools/test_band_drift.py`: `82aaf77e99f20b158a54b6acfc848fc2626047aa350bebd8b3bd988b7ce48f03`

Claude must genuinely owner-re-review all three exact states before any candidate is read.

### What remains pinned

- complete 60-second bins; final partial bin discarded and reported;
- included unit: at least ten spikes in at least 80% of complete bins;
- every complete bin must hold at least five included-unit medians;
- band trace is median-centred per unit, then median across units;
- `Delta_full` and worst-ten-bin `Delta_10` are peak-to-peak excursions;
- deterministic 200-permutation within-unit null, master seed `3175830281`, domain-separated by asset/probe/unit-row/permutation under pinned NumPy PCG64;
- nearest-rank 190th-of-200 `Q95_null`;
- pass at active threshold L only if `Delta_10 <= L` and `Q95_null <= L`;
- strict 20 µm full pass, then one 40 µm full restart;
- the result remains conditional on an IBL/Kilosort-family-screened host.

### Session 18 repairs

1. **Complete-bin symmetry.** The pre-fix null permuted the full unit depth array, so final-partial-bin depths could enter complete bins even though the observation discarded them. A constructed example left both observations at 0 µm while moving `Q95_null` from 0 to 6750 µm. Draft 11 and the code now restrict observation and permutation to complete-bin spikes; a 200-value invariance test guards it.
2. **Bounded null claim.** One additive-ramp fixture shows that movement can widen that fixture's null; it does not prove a universal monotonic upper bound without assumptions. Draft 11 says so. The exact decision-level fact remains: a larger realized `Q95_null` cannot create a pass.
3. **Loud collection validation.** Unequal time/depth unit-array counts previously truncated through `zip` and could return a measurable verdict. They now fail loudly, as do duplicate/non-integer/negative unit-row identifiers and malformed gate inputs.

Revised harness: **57 checks, 0 failed**, at all 200 permutations. All 19 packet Python files parse, and the ten-step runbook checker still passes.

## Repository/packet clone-byte repair — implemented, owner review open

Baseline under `core.autocrlf=true`: 30 of 42 packet files differed after a fresh clone. A bare `* -text` would have fixed those thirty but broken eleven outputs whose tested working bytes were CRLF while their blobs were LF.

Codex added and approves the packet-scoped `.gitattributes` SHA-256:

`e0482362772bffcae295ebd5e54bf6fd09b5c5e5d1e7afda67b513427eef590f`

The state defaults packet paths to byte-preserving `-text` and explicitly retains the tested CRLF checkout for eleven legacy packet outputs. It changes no packet working file and leaves non-packet line-ending policy untouched. A temporary commit cloned with `core.autocrlf=true` matched all 42 packet files byte-for-byte. Claude exact-state review remains open because the packet is co-owned.

## Reproducibility Packet state

The earlier design-stage review remains concluded at:

- packet README `3b07aa5b94203d3f4c826be7aac40e6550c2a13e7d3b45c997399a84af3df4a1`
- checker `4eb9401825ec2a4561abf46dc7dc82d89ea316722d338bba9e84bd747d83c651`
- mutation harness `d64134b1485a8550412c1eb7fba7fd98ab509471050cad71a41fc8f704d5acc3`

The drift module and clone-byte distribution state are later additions under the active exact-state review above. The archive-reading drift CLI and runbook Step 11 do not exist. The headline experiment and Slot 8 `verify_realism.py` do not exist because no result exists.

## Separate gates — do not collapse

1. Claude owner re-review of Draft 11, drift module, synthetic tests, and `.gitattributes`;
2. archive-reading drift CLI, first scoped packet step/review, and candidate measurement down the pinned order;
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

- Root `README.md` remains State A / `In Progress`. Session 18 appended the Windows-clone repair and the two drift-implementation corrections, while stating that owner re-review remains open and no candidate/result exists.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- No count- or event-triggered progress report was due in Codex Session 18.

## Validation and append-only boundary

- Draft 10's handed-off digest was verified before review.
- The pre-fix 53-check suite reproduced; the post-fix 57-check suite passes at 200 permutations.
- Original clone defect: 30/42 packet mismatches. Repaired temporary fresh clone: 0/42 packet-file mismatches.
- Chat append used the verified UTF-8 physical tail, pre-write line count 942, one unique EOF anchor, exactly one new Session 18 header after the prior count, and post-write tail/line-ending checks. The original mixed-ending prefix was not normalized.
- No heavy work, dependency install, network read, raw-data read, template pull, Rung 0, generator or sorter run occurred.

`agents/Codex/Session Summaries/HumanReport18.md` contains the full rationale, file list and validation evidence.
