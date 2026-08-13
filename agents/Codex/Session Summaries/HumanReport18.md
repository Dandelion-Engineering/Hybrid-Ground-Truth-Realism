# Human Report 18 — Codex

**Date and time:** 2026-08-13 09:19 PDT
**Phase:** 2 — Execution
**Session type:** Exact-state host/drift review, synthetic-implementation review, and clone-byte reproducibility repair

---

## Summary

This session reviewed Claude's owner-approved host-selection Draft 10, the newly implemented pure drift estimator, its synthetic test harness, and the reported Windows clone/line-ending defect. The review accepted the pinned thirteen-host order and the new rule that makes the drift parameters bind only after same-state approval. It did **not** approve Draft 10 unchanged.

Two scientific/implementation defects were repaired before any candidate was measured:

1. Draft 10 promoted one synthetic additive-ramp result into a general claim that genuine movement makes the permutation null a monotonic, proved upper bound on the no-drift noise floor. The new Draft 11 keeps the demonstrated direction for that fixture, names the additive common-motion assumption, and states that the no-drift counterfactual and time-dependent depth-estimation errors remain unobserved.
2. The implementation permuted the unit's full depth array, including spikes in the final partial bin that the observed statistic declares discarded. An independent fixture left both observed excursions at `0.0 µm` while changing only five seconds of partial-bin depths moved `Q95_null` from `0.0` to `6750.0 µm`. Draft 11 and the implementation now use complete-bin spikes for both observation and permutation.

A separate malformed-input probe found that six spike-time arrays plus five depth arrays were silently truncated by `zip`, yet the module reported six units in the band and returned a measurable result based on five. The module now fails loudly on unequal unit-array counts, duplicate/non-integer/negative unit-row identifiers, an unmeasurable observation passed to the null builder, and missing/non-finite gate inputs.

The revised exact states are Codex-approved and handed back to Claude for genuine owner re-review. **No candidate may be measured until Claude approves those same bytes or edits and returns a new state.**

The repository-distribution defect was also reproduced and repaired. A baseline fresh clone under the machine's `core.autocrlf=true` setting changed 30 of 42 packet files. Claude's proposed `* -text` diagnosis was correct but incomplete: eleven files that currently survived a clone were CRLF in the tested working tree and LF in the committed blob, so the one-line change alone would have fixed thirty and broken eleven. The implemented `.gitattributes` state is scoped to the packet, preserves raw bytes by default there, and explicitly retains CRLF checkout for those eleven legacy outputs. A temporary commit cloned under `core.autocrlf=true` reproduced all 42 packet working files exactly: **0 byte differences**.

## Exact-state review

### What was accepted unchanged

- `agents/Claude/Tier A Host and Injection Zone Selection.md` §15: the thirteen-candidate order, tracked-cache continuation, gate ordering, strict 20 µm full pass, relaxed 40 µm full restart, and first-admissible semantics.
- Draft 10 §16.8's replacement of a stale status sentence with the actual binding rule.
- The peak-to-peak excursion, complete-bin validity, deterministic seed grammar, 200 PCG64 permutations, nearest-rank `Q95_null`, two-number pass rule, one-row/two-row threshold ladder, and Kilosort-family host-conditioning limitation.

### What prevented unchanged approval

**The null-bias paragraph overclaimed.** One ramp fixture can demonstrate that adding one common ramp widened that fixture's null. It cannot identify the unobserved no-drift version of a real recording, prove monotonicity under arbitrary time-dependent estimator errors, or make `Q95_null` a general upper bound without assumptions. Draft 11 now distinguishes the fixture result from the general claim. The decision-level direction remains exact: once a larger `Q95_null` is realized, it cannot create a pass under the two-number rule.

**The partial-bin interpretation violated the stated discard.** The observation ignored the final partial bin while the null could import its depths into complete-bin positions. The repair restricts each unit's permutation pool to aligned depths whose times lie in complete bins. Partial-bin data now affect neither side.

**Input collections needed structural validation.** Top-level list lengths and row-identifier uniqueness are now checked before any computation. The null builder also checks the observation's inclusion, bin-validity, and window conditions before entering its permutation loop, so a caller receives a specific loud error rather than an accidental `TypeError` or a misleading verdict.

### Approved handoff states

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 11: SHA-256 `647743668ec51d27e258ea5b4600d9cc2abc6b76e444aeb93b15df951ba8ec7d`
- `Reproducibility Packet/scripts/utils/band_drift.py`: SHA-256 `d8b035968416b335d7ef1bdd0d915c03aec4a64649defa8795c8c013fc70c069`
- `agents/Claude/tools/test_band_drift.py`: SHA-256 `82aaf77e99f20b158a54b6acfc848fc2626047aa350bebd8b3bd988b7ce48f03`

Codex explicitly approved all three states in the active Tier A selection chat. Claude owner re-review is open. This does not pin a host, approve a candidate measurement, or discharge any later gate.

## Clone-byte reproducibility repair

The baseline was independently reproduced from a local fresh clone:

- system Git configuration: `core.autocrlf=true`;
- 42 packet files compared;
- 30 working-tree/clone byte mismatches;
- the mismatch set included every packet script, the frozen upstream CSV, and recorded placement outputs.

The proposed one-line `* -text` rule needed an inverse-edge repair. Eleven outputs had LF blobs but CRLF tested working bytes and were stable only because Git converted them during checkout. Under `* -text` alone, those eleven would have changed. The final packet-scoped approach:

- adds `.gitattributes` SHA-256 `e0482362772bffcae295ebd5e54bf6fd09b5c5e5d1e7afda67b513427eef590f`;
- defaults packet paths to `-text`, so their committed bytes are not rewritten on checkout;
- overrides the eleven legacy CRLF packet outputs with `text eol=crlf`, preserving their already-tested checkout bytes without changing their committed content;
- leaves every non-packet path under its prior line-ending policy.

The line-ending repair itself changed no packet working file. A temporary tree/commit was cloned under `core.autocrlf=true`; all 42 packet files matched the current tested working tree byte-for-byte. The temporary ref and clone were removed after verification.

## Validation

- Original Claude harness: 53 checks passed before review.
- Revised harness: **57 checks passed, 0 failed**, using all 200 declared permutations.
- New permanent tests cover top-level unit-array count mismatch, duplicate row IDs, and complete-bin null invariance under extreme partial-bin changes.
- An independent pre-fix probe reproduced the two defects: silent unit-list truncation and `Q95_null` movement from 0 to 6750 µm with unchanged observation.
- All 19 Python files under `Reproducibility Packet/scripts/` parsed successfully.
- `check_runbook_consistency.py` passed all ten existing runbook steps.
- `git diff --check` passed.
- Append-only chat safeguards passed twice: the substantive review used pre-write line count 942 and ended at 980; the distribution-state correction used pre-write line count 980 and ended at 990. Each used one unique EOF anchor and produced exactly one new timestamped header after the prior count. The original 107 CRLF sequences and 835 original lone-LF sequences remained intact; both appends added only new LF lines.
- Fresh-clone verification passed at 0 differences across all 42 packet files; the full packet check is repeated during final staging.

No network read, dependency installation, template pull, raw-recording read, candidate measurement, host selection, Rung 0, generator, sorter, or heavy computation occurred. The longest check was the lightweight synthetic permutation suite.

## Public heartbeat

The root `README.md` received one append-only running-log entry because both events are public-reproducibility-relevant: the Windows clone path now preserves the tested bytes, and implementation review found the partial-bin and malformed-collection defects before any candidate result existed. The entry retains the `In Progress` state and says explicitly that Claude owner re-review is still required.

## Files created or updated

- `.gitattributes` — new repository byte-preservation rules.
- `agents/Claude/Tier A Host and Injection Zone Selection.md` — Draft 10 to Codex-approved Draft 11.
- `Reproducibility Packet/scripts/utils/band_drift.py` — complete-bin null, loud structural validation, and bounded null-bias wording.
- `agents/Claude/tools/test_band_drift.py` — 57-check harness with the new regression cases.
- `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` — the append-only Codex Session 18 review/handoff and a later correction narrowing `.gitattributes` to the packet; existing physical prefix preserved.
- `README.md` — one lean public-log entry.
- `agents/Codex/README.md` — workspace map and active-review state refreshed.
- `agents/Codex/Summary of Only Necessary Context.md` — fully rewritten for Session 19.
- `agents/Codex/Session Summaries/HumanReport18.md` — this report.

## Decisions and boundaries

- The final partial bin is discarded from both observation and null. A statistic cannot declare data discarded on one side and use it on the other.
- The additive-ramp null-widening result is a fixture result, not a universal monotonic theorem.
- Exact row identifiers are part of deterministic randomization; duplicates are malformed input, not two legitimate units sharing a stream.
- Working-file hashes remain the approved scientific states. The packet-scoped line-ending repair changes checkout behavior, not measured content or non-packet policy.
- Draft 11, the estimator, its test harness, and the repository-distribution state await Claude's exact-state owner re-review. Reviewer edits and the eventual commit do not substitute for that approval.

## Next steps

1. Claude genuinely re-opens Draft 11, `band_drift.py`, `test_band_drift.py`, and `.gitattributes`, then explicitly approves the same states or edits and returns new states.
2. Only after that approval may the archive-reading CLI and its packet step be completed and a candidate read.
3. The first candidate measurement must confirm the ragged index and finite depth column before computing a verdict.
4. Noise, post-rescaling effective SNR, schedule/placement specification, matcher implementation, joint placement, balance/manipulation, generation, Rung 0, and sorter execution remain separate gates.

No new director action is required.
