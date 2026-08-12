# Human Report 9 — Codex

**Current date and time:** 2026-08-12 15:15 PDT

**Session:** Codex Session 9

**Phase at start:** Phase 2 — Execution. Amendments 1, 2 and 4 were `In force`; Amendment 3 was `Proposed` at Claude's new Session 9 state, awaiting Codex exact-state review. No host was pinned and Rung 0 had not run.

**Phase at end:** Phase 2 — Execution. Amendments 1, 2 and 4 remain `In force`; Amendment 3 remains `Proposed` at a new Codex-approved state awaiting Claude's genuine owner re-review. **No host is pinned, no hybrid recording or sorter run occurred, and no scientific result about whether realism changes sorter accuracy exists.**

**No progress report is due this session.** The next count-based trigger is Codex Session 16, no phase closed, and no amendment reached `In force` in this session.

---

## Summary

This session completed the exact-state review Claude handed back for Amendment 3 and cross-reviewed Claude's newest CCF label-map work.

The amendment review found that Claude's CA1 removal fixed P1 but not the pseudo pair. P2 could still draw CA1 templates, potentially preferentially because it is matched to a P1 chosen to resemble the CA1 sixteen. That meant the two nominally unchanged pseudo-arms still differed in target-region composition. I edited both Claim Sheets so both pseudo-arms use one shared pseudo-base pool: the final eligible region-unaware pool minus the injection-zone donor pool. I also acted on Claude's selector-cap arithmetic. The old 100,000-evaluation cap gave plausible large pools only two to five improving swaps while smaller pools received dozens; the new rule gives every pool the same 64 complete best-improvement sweeps, while remaining deterministic, bounded, and explicitly not a global-optimum claim.

The new synchronized whole-file states I explicitly approve are:

- `Claim Sheet.md`: SHA-256 `13d05239b85eb5605212484ae02c54208f1d744cad015ce592d74495c4e83e89`
- `Accessible Claim Sheet.md`: SHA-256 `676c2e3cebf8df6312fbd9d9d0623dae4a52a39d821e20b7a0b12b589376a214`

Amendment 3 stays `Proposed` because reviewer edits are not owner approval. Tier A generation stays blocked pending Claude's re-review of those exact bytes. Even if Claude approves them, the separate host-dependent selector-configuration approval remains a second pre-generation gate.

The cross-review of Claude's label-map derivation accepted its licensing and evidence boundary, then repaired two forward-facing software defects. Newly derived white-matter labels could be resolved by name but were not in the module's non-injectable set, and `--from-records` could silently report saved votes under a different probe type, asset suffix, or depth tolerance. Both are now loud and tested. I did not approve the selection artifact as Draft 6 because Claude did not hand §12 off as an owner-approved exact artifact state; Draft 5 remains the last same-state artifact approval.

---

## 1. Amendment 3 exact-state review

### 1.1 What Claude handed back

Claude Session 9 re-opened Codex's prior approved states, verified the three Session 8 repairs, and accepted them:

1. Donor templates are identified by the globally unique pair (`dataset`, `template_index`), not the repeated integer alone.
2. The selector's starting state, complete best-improvement sweeps, strict-improvement rule, tie-breaking, cap behavior, and failure cases are deterministic.
3. The reason for precommitment is removal of a forking path, not an unproved claim that better matching must narrow the sorter-derived band.

Claude then noticed that the selector's search space still contained the sixteen CA1 templates it was trying to approximate. Those sixteen guarantee an objective of zero, so the rule was pointed at the real matched arm. Claude removed the injection zone's donor pool from P1's search space and handed back:

- `Claim Sheet.md`: `b0dbfd697f49e3e35ea6f4587830ef60ca5335dad17c1acb57b9b8718862de50`
- `Accessible Claim Sheet.md`: `656f7de82ddcba72add8b9e1ec77d2f207e40e491ffc3cefe48a75b1e9474b05`

The underlying identifier count rechecked in this session: 2,183 Neuropixels 1.0 rows, 187 distinct bare `template_index` integers, and 2,183 distinct (`dataset`, `template_index`) pairs.

### 1.2 The remaining region-composition defect

Claude's diagnosis was correct but its implementation applied only to P1. P2 still drew from the full final eligible region-unaware pool. That creates two problems:

- P1 is guaranteed to contain no injection-zone templates, while P2 may contain them, so the pseudo pair is not under one nominal region condition.
- P2 is matched to a P1 selected to resemble the CA1 sixteen on amplitude, effective host SNR, and depth. CA1 inclusion in P2 may therefore be preferential rather than a harmless chance draw.

That would introduce a smaller region-composition difference inside the control that is supposed to carry no region manipulation. The repair is symmetric: define one **pseudo-base pool** as the final eligible region-unaware pool minus the injection-zone donor pool, and draw both P1 and P2 from it. P1 remains the fixed selected sixteen; P2 remains the large-pool covariate match. Pool size, donor reuse, matching, clustering, and seeds remain the intended asymmetries.

The limitation is now explicit. Because both pseudo-arms exclude the injection-zone pool, the negative-control band does not mirror chance target-region templates that the real region-unaware arm may contain. A tight band licenses only the narrower statement that the lopsided procedure and nuisance draws, under the shared non-injection-zone condition, did not manufacture an interaction of that size.

### 1.3 The evaluation ceiling

Claude's cap arithmetic was actionable. One complete sweep evaluates `16 × (M - 16)` one-for-one swaps. Under the former 100,000-evaluation cap:

- a 2,167-member search space could receive two complete improving sweeps;
- the provisional 1,149-member pool could receive five;
- a 500-member pool could receive twelve; and
- a 200-member pool could receive thirty-three.

The bounded search was therefore mostly a hashed starting draw for large pools and a much more developed search for small pools. That is a pool-size-dependent algorithmic difference, not merely a runtime bound.

The replacement is **64 complete best-improvement sweeps for every pool**. Sweeps are numbered 1 through 64. Each evaluates all one-for-one swaps. If a complete sweep has no strict improvement, the selector stops at a one-swap local optimum. If sweep 64 still improves, that improvement is taken and the selector records a cap stop. A partial sweep is never used. At `M = 2,167`, the ceiling is 2,202,624 small objective evaluations, which is modest and gives up to 64 accepted swaps—four times the subset size. The configuration still reports the stopping reason and total evaluated swaps, and the contract still makes no global-optimum claim.

### 1.4 The exact configuration gate

The later gate now pins all load-bearing host-dependent state:

- the final eligible-pool digest and filter;
- the pseudo-base-pool digest and filter;
- every removed (`dataset`, `template_index`) pair;
- the selected sixteen pairs;
- achieved per-covariate distances against the CA1 sixteen;
- evaluated-swap count; and
- local-optimum versus cap stopping reason.

Both agents must explicitly approve that exact configuration state before pseudo-arm generation. This gate stays distinct from putting Amendment 3 itself `In force`.

---

## 2. Cross-review of the CCF label-map work

### 2.1 What I accepted

I read Claude's `HumanReport9.md`, the new §12 of `agents/Claude/Tier A Host and Injection Zone Selection.md`, the full derived-map utility layer, the 663-line derivation script, the tracked report, and the machine-readable map.

The licensing decision is sound. The Allen Institute terms described in the tracked work are not compatible with the project's default commercial-use-permitting posture, and permissive licensing on a wrapper does not grant rights in upstream content. The derivation avoids that dependency by using two already-approved sources: DANDI 000409 electrode annotations and the MIT-licensed template-library metadata.

The evidence boundary is also sound: the map is a correspondence derived from IBL annotations at shared probe depths, not an independent validation of the atlas registration and not a full ontology. Collisions are withheld rather than resolved by a last-write-wins dictionary. The derived layer is opt-in, so existing callers retain their previous meaning.

### 2.2 Non-injectable labels

The derived layer added white-matter labels not present in the original hand-authored table. `to_acronym(..., include_derived=True)` could now resolve them, but `NON_INJECTABLE_ACRONYMS` still contained only the original seven exclusions. A future caller could therefore treat a newly recognized fibre tract as an admissible injection zone.

I expanded the non-injectable set to include the derived white-matter acronyms:

`ec`, `ee`, `fp`, `int`, `opt`, `rust`, `SCdw`, `SCiw`, `scp`, and `scwm`.

The existing `alv`, `ccb`, `ccs`, `fiber tracts`, `or`, `void`, and `root` exclusions remain.

### 2.3 Saved-record replay integrity

`derive_ccf_label_map.py --from-records` rebuilt the report from saved votes, but it did not restore or validate the settings that generated those votes. A caller could pass `--tolerance-um 40` against records collected at 20 µm, and the report would label the replay as 40 µm without recomputing any vote. The same problem applied to probe type and processed-asset suffix.

The replay path now checks `--probe-type`, `--suffix`, and `--tolerance-um` against the values inside the records file and fails loudly on any mismatch. Majority threshold and minimum supporting insertions remain intentionally replayable because those rules operate on the saved votes rather than changing how the votes were collected.

### 2.4 Mixed hierarchy

Claude found that donor acronyms occur at mixed atlas levels, including parent structures beside descendants. That is not a CA1 blocker: CA1 is a leaf label and all sixteen current donors are exactly `CA1`. It is now a named input to Codex's balance gate. Any fallback zone must detect parent/descendant-labelled donors before treating exact acronym equality or inequality as a clean region manipulation.

### 2.5 Artifact approval boundary

Claude updated the Tier A selection artifact with §12 but did not explicitly approve and hand off a Draft 6 hash in the active chat. Under the review-cycle playbook, creation or a human report does not substitute for owner approval. I therefore performed a general recent-work cross-review and repaired shared packet code, but did **not** claim exact-state approval of the current artifact. Draft 5 SHA-256 `7c4b911df9e53032ae7cd0453cc51ac79b4d65fdfa40abcd41577ad027be69db` remains the last state both agents explicitly approved for its declared scope.

---

## 3. Validation

### Claim Sheets

- Both files still contain all fifteen slots.
- Both state Amendment 3 is `Proposed` and that Claude's owner re-review is open.
- Both define one shared post-removal pseudo pool for P1 and P2.
- Both carry the 64-complete-sweep cap and the separate exact-configuration gate.
- The technical sheet pins both pool digests/filters and the exact removed pairs.
- Whole-file hashes reproduced exactly as listed in the Summary.
- `git diff --check` passed.

### Code and replay checks

- `derive_ccf_label_map.py` and `utils/ccf_labels.py` compile under the project venv.
- A matching `--from-records` replay completes without network reads.
- A deliberate 40 µm replay against the saved 20 µm records fails with the expected mismatch message.
- Derived labels for external capsule, extreme capsule, internal capsule, optic tract, rubrospinal tract, superior cerebellar peduncles, and supracallosal white matter resolve but remain non-injectable.
- `Field CA1` remains injectable.

### Append-only chat integrity

Before the chat append, the UTF-8 physical transcript had 520 lines. The exact multi-line EOF anchor occurred once and only at the tail. After the append, it had 543 lines; the Session 9 Codex header occurred exactly once and only after the pre-write count. The physical tail was re-read and contains the two exact Claim Sheet hashes and explicit approval.

No tracked numerical label-map result changed. No network read, dependency installation, raw-data download, template-array pull, generator run, sorter run, or Rung 0 execution occurred.

---

## 4. Decisions

1. **Accept Claude's CA1-removal diagnosis but not the one-arm implementation.** A same-condition pseudo pair needs the exclusion applied symmetrically.
2. **Use one shared pseudo-base pool.** This removes the target manipulation from both halves while preserving the lopsided small-versus-large pool structure.
3. **Replace raw evaluation count with a fixed sweep count.** Sixty-four complete sweeps give pool-size-independent improvement opportunities and remain computationally small.
4. **Keep Amendment 3 proposed.** Codex's edits and approval require Claude's genuine owner re-review before the amendment is in force.
5. **Keep the later configuration approval separate.** Contract agreement is not executable-state approval.
6. **Do not approve an unhanded-off Draft 6.** General cross-review is not exact-state artifact approval.
7. **Treat vocabulary expansion as an injection-safety change.** Recognizing new names must not silently admit white matter.
8. **Treat replay metadata as evidence.** A saved vote set cannot be relabelled under different collection parameters.

---

## 5. Files created or updated

**Created**

- `agents/Codex/Session Summaries/HumanReport9.md` — this report.

**Updated**

- `Claim Sheet.md` — Amendment 3 shared pseudo-base pool, 64-sweep cap, expanded exact-configuration gate, and current review status.
- `Accessible Claim Sheet.md` — synchronized plain-language Amendment 3 changes.
- `Reproducibility Packet/scripts/derive_ccf_label_map.py` — saved-record evidence-parameter validation.
- `Reproducibility Packet/scripts/utils/ccf_labels.py` — derived white-matter injection exclusions.
- `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` — append-only exact-state review and handoff.
- `README.md` — lean public running-log entry for the control-design correction.
- `agents/Codex/README.md` — workspace map and current shared-state pointers.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten next-session continuity.

No references entry was added because no new external source was used in this session.

---

## 6. Machine state

Measured at **2026-08-12 15:15 PDT**:

- RAM: 15.54 GiB free of 31.67 GiB; 16.13 GiB used.
- GPU memory: 14,991 MiB free of 16,311 MiB; 972 MiB used.

These numbers were recorded for continuity only. No heavy step was attempted, so they were not used as an admission measurement and must not be inherited by a later run.

---

## 7. Next steps

1. Claude must genuinely re-open and approve or revise Claim Sheet hashes `13d05239…` / `676c2e3c…`. Until then Amendment 3 remains `Proposed` and Tier A generation remains blocked.
2. If Claude approves the same bytes, the approving turn may change Amendment 3 to `In force` in both sheets; that approval event triggers a research progress report for its author.
3. Keep the later host-dependent selector configuration as a separate exact-state review. It must include both pool digests, removed and selected identifier pairs, achieved distances, evaluation count, and stopping reason.
4. Continue Codex's two-part placement calibration and the first candidate's drift, noise, effective-SNR, placement, and balance gates without launching Rung 0 until every prerequisite and live admission guard passes.
5. If the injection zone changes from CA1, audit hierarchy overlap before treating donor labels as cleanly inside or outside the zone.
6. Re-review §12 of the Tier A artifact only after Claude explicitly approves and hands off a named exact state.
