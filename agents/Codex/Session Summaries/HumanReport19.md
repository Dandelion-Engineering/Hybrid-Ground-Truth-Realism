# Human Report 19 — Codex

**Date and time:** 2026-08-14 00:12 PDT
**Phase:** 2 — Execution
**Session type:** Exact-state review of Claude Draft 12 and repository distribution policy; no candidate measurement

---

## Summary

This session completed Codex's reviewer pass over Claude Session 19. I accepted Claude's new timebase/input-error construction but could not approve Draft 12 unchanged. The new null-scaling paragraph stated a stronger result than its probe established, and the artifact still described the drift estimator as unimplemented after both agents had explicitly approved its code and harness.

I repaired both points without changing any parameter, threshold, candidate order, statistic, gate verdict, or execution authorization. **I explicitly approve Draft 13 at SHA-256 `82d58b4009774adc63817da78be247c137cd5fa105e5553a8fe1c4e775349cc8` and handed it back to Claude for genuine owner re-review.** Section 16 remains open and no candidate may be read meanwhile.

I also accepted Claude's repository-wide `.gitattributes` policy. Its behavior was sound, but its opening explanation incorrectly said every listed file was stored as-is even though the explicit CRLF paths opt into Git text normalization and CRLF checkout. I corrected only that explanation. **I explicitly approve `.gitattributes` at SHA-256 `036c696c3e1ea9cef70925ec8dfedc407ef59bb20e5c00e17ef9b5f88855bfa0` and handed it back for owner review.** A temporary commit cloned under `core.autocrlf=true` reproduced all **153 of 153** tracked files byte for byte.

No host, candidate drift value, target manifest, donor, dependency, raw recording, generator, Rung 0, or sorter was opened or run. There is still no scientific result.

---

## What was accomplished

### 1. Startup gates and context

- Read the automation memory first, then `.agent-turn`; it named `Codex`.
- Confirmed `.agent-session.lock` was absent, created it, and re-read `.agent-turn`; it still named `Codex`.
- Read `AgentPrompt.md`, all of `Project Details/Project Details.md`, Codex's continuity file, every concluded chat summary involving Codex, and the full 1,044-line active Tier A selection transcript before replying.
- Read `Playbooks/review-cycle.md`, `Playbooks/reproducibility-packet.md`, `Playbooks/live-run-readme.md`, Claude's `HumanReport19.md`, and the work that report pointed to.
- Verified the worktree was clean at Claude's pushed `2cb61e6` before making Codex changes.

### 2. Draft 12 exact-state review

I verified Claude's handed-off Draft 12 SHA-256 `e1b93eed32f791acce51bbf5eda7d23ad7e6a175b8492086d99d24a791d6b313` before review, then read §§15–16 whole rather than as a diff.

The timebase diagnosis checks against the tracked records:

- `host_timing_index.jsonl` contains 21 AP series.
- The rank-1 CSHL047 `b52182e7` Probe01 raw series begins at `1.13848929170131 s`; three additional Probe01 series begin at `1.006007200953416 s`, `1.3040165113054096 s`, and `1.002166903429001 s`.
- `duration_s` is `t_last_s - t_first_s` to floating-point tolerance in every series, so it is a span rather than an end time.
- The processed units-table description for `spike_times` says only “the spike times for each unit in seconds” and names no origin.

I therefore accept Draft 12's operative rule: the future archive-reading CLI must reconcile the processed spike-time clock with the raw timing record before computing the bin grid. Failure to reconcile is an input error to resolve, not a failed host, and the pinned first-admissible order must not advance past it.

### 3. Two repairs before approval

**Repair 1 — observable drift bound, not a physical-motion guarantee.**

Draft 12 said a mis-scaled null “can never admit a moving one.” Its supporting probe tests a candidate whose **observed** `Delta_10` is 25 µm against a 20 µm gate and confirms every tested `Q95_null` leaves it failed. That proves the null cannot rescue an observed excursion already above tolerance. It does not prove the IBL center-of-mass depth trace cannot systematically understate physical movement; the next paragraph of the artifact explicitly leaves that bias unbounded.

Draft 13 now states the exact guarantee: no `Q95_null` can change the rejection when observed `Delta_10 > L`; null scaling can only change the resolution verdict among candidates whose observed excursion is already at or below `L`. It explicitly carves out physical movement underestimated by the IBL trace.

The supporting `agents/Claude/tools/probe_band_drift_claims.py` received the same wording repair, with no numerical-code change. I explicitly approve its reviewed SHA-256 `4f3b83773156e7f9654f3e080d5adb258658cf500cf741aaea04b5015f07c34f`; Claude owner re-review remains appropriate because it is Claude's support artifact.

**Repair 2 — current implementation state.**

Draft 12 §16.8 still said “The estimator is defined and not implemented.” That became false when Claude explicitly owner-approved Codex's exact module and harness states in Session 19. Draft 13 now records:

- `Reproducibility Packet/scripts/utils/band_drift.py` — same-state approved at `d8b035968416b335d7ef1bdd0d915c03aec4a64649defa8795c8c013fc70c069`;
- `agents/Claude/tools/test_band_drift.py` — same-state approved at `82aaf77e99f20b158a54b6acfc848fc2626047aa350bebd8b3bd988b7ce48f03`;
- the archive-reading CLI, numbered runbook step, and candidate measurement remain unbuilt.

This keeps the closed implementation loop closed while accurately naming the still-open executable work.

### 4. Repository distribution review

Claude expanded Codex's packet-scoped `.gitattributes` rule to the full repository. The functional construction is sound:

- all paths default to `* -text`, preserving committed bytes on checkout;
- 17 pre-existing non-packet framework files and 11 legacy packet outputs explicitly use `text eol=crlf` because CRLF is their already-tested working representation;
- the active transcript remains a genuinely mixed-ending file and is preserved byte-for-byte under `-text`.

The only defect was explanatory. Git does not store the explicit CRLF paths as-is: `text eol=crlf` normalizes their object-database representation and reconstructs CRLF on checkout. I corrected the comment to say all paths default to byte-preserving checkout while the named exceptions intentionally opt into normalization plus CRLF checkout. No attribute rule or working file byte changed.

I staged the reviewed state into a temporary commit, cloned it with `core.autocrlf=true`, and compared SHA-256 file by file: **153 tracked files, 0 mismatches**. The temporary ref was removed and the clone was moved to the Recycle Bin after its exact absolute path was verified inside the system temp directory.

### 5. Public and collaboration record

- Appended the Draft 13 and `.gitattributes` exact-state handoff to the active Tier A selection chat. The prior 146,519 transcript bytes retained SHA-256 `4372c9f2300e79b2d25606b4e3f1845b14a7b177cfeff31aa1fb00a956775d7f`; the line count advanced from 1,044 to 1,063; exactly one new Codex Session 19 header occurs after the old line count; and the LF tail remains intact.
- Appended a forward correction to the root public README. It narrows the prior physical-motion claim to observed `Delta_10`, records the 153/153 independent distribution check, and preserves the explicit no-result/no-execution boundary. The earlier entries remain untouched.
- No chat was concluded because Draft 13 and the repository-distribution state still require Claude owner re-review.

---

## Challenges and how they were handled

**A passing probe carried an overbroad English conclusion.** The numerical check was correct, but “moving candidate” silently moved from an observed statistic to physical reality. Reading the next paragraph against the claim exposed the contradiction. The repair scopes the statement to the implemented observable and preserves the systematic-bias limitation.

**A historical status sentence outlived the work it described.** The artifact's “not implemented” sentence had become false while review focused on the new timebase logic. Reading the rendered §16.8 rather than only the Draft 11→12 diff caught it.

**The first runbook-check command used the wrong interface.** I passed an unsupported `--packet` argument; the checker exited immediately and changed nothing. I read its actual usage and reran with `--readme` and `--scripts`; all ten steps passed.

**Temporary-clone cleanup was blocked for permanent recursive deletion.** After verifying the absolute clone path was inside the system temp directory, I used the recoverable Recycle Bin operation instead. No temporary git ref remains.

---

## Validation

- Draft 12 handoff digest verified before review.
- Raw timing facts and the `spike_times` description rechecked from tracked records.
- `test_band_drift.py`: **57 checks, 0 failed**, with all 200 declared permutations.
- `probe_band_drift_claims.py`: **3 of 3 probes passed**.
- Runbook consistency: **10 numbered steps**, all commands agree with script `--help` examples.
- Temporary Windows-style clone: **153/153 tracked files byte-identical**.
- `git diff --check`: clean at the reviewed state.
- Append-only transcript prefix, header-count, line-count, encoding, and tail assertions: passed.

No heavy computation, dependency install, network read, archive read, raw-data download, template pull, Rung 0, hybrid generation, or sorter execution occurred.

---

## Files created or updated

| Path | Change |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 13; observable-bound repair and current estimator/CLI status. |
| `agents/Claude/tools/probe_band_drift_claims.py` | Wording narrowed to the observed-`Delta_10` claim actually tested. |
| `.gitattributes` | Explanation corrected; functional repository-wide byte policy unchanged. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only exact-state review and handoff. |
| `README.md` | Append-only public correction and independent distribution-review result. |
| `agents/Codex/Session Summaries/HumanReport19.md` | This report. |
| `agents/Codex/README.md` | Workspace map and active-state routing refreshed. |
| `agents/Codex/Summary of Only Necessary Context.md` | Rewritten for Codex Session 20. |

No source citation changed, so `agents/Codex/references.md` remains unchanged. No progress report was due: the next count-based report is Codex Session 24, and this session closed neither a phase nor a Claim Sheet amendment.

---

## Next steps

1. Claude must genuinely owner-re-review Draft 13 `82d58b40…`, the supporting probe wording `4f3b8377…`, and `.gitattributes` `036c696c…`. No candidate is read before §16 converges.
2. After same-state approval, build the archive-reading drift CLI. It must confirm the ragged-index layout, finite depth values, and the processed/raw timebase reconciliation before computing anything; then add its numbered packet step and scoped packet review.
3. Only after that executable state is reviewed may the pinned rank-1 candidate be measured on drift.
4. The separate schedule/placement specification, matcher implementation/tests, noise/effective-SNR gates, joint placement gate, exact host-dependent configuration, independent balance/manipulation approval, generation, Rung 0, and sorter execution remain distinct gates.
