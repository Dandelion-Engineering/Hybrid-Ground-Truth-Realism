# Human Report — Codex Session 29

**Date:** 2026-08-15

**Closeout time:** 08:14 PDT

**Phase:** 2 — Execution

**Review outcome:** RC-002 Round 3 — **not approved; Convergence Decision triggered**

## Executive summary

I performed the terminal delta-only verification of Claude's Round-3 response on RC-002, the archive-reading drift command. All seven handoff hashes matched. Every recorded Round-2 blocker and follow-up passed on its tested boundary: fragmented chunks are placed from their actual byte offsets, the fixed-block cache and converted arrays are combined with Python structures and HDF5's chunk-cache ceiling, ragged indexes require integer storage, output aliases resolve through the filesystem, and the mutation-evidence description now matches its real coverage.

The positive evidence is strong but the candidate is not approvable. The final pass found one blocking late path: `read_band_units` computes and enforces the preflight ceiling, then calls `source_provenance(handle)`, which reads complete stored provenance datasets and returns their strings. Those later bytes and objects are absent from both the transfer bound and the combined resident bound.

An independent generated HDF5 fixture was admitted at a reported `peak_resident_bytes = 267,001` with `cache_bound_bytes = 174,368`. It then transferred and retained 4,232,336 bytes and materialized a 4,200,030-character `general/source_script`. The transfer bound was exceeded more than twenty-fourfold; cached payload plus the loaded string exceeded the admitted peak more than thirtyfold. No archive, network or candidate asset was involved.

Because this is a new blocker after Round 2, the superseding review method forbids another repair round. I froze the exact seven-file state, triggered the agent-only Convergence Decision, and wrote my one required statement. I propose terminal **Revisions Required**: the defect is local and repairable outside formal review, after which Claude may open one successor card naming `Supersedes: RC-002`. Claude's one statement and explicit disposition consensus remain pending. Candidate access remains blocked.

## Exact candidate verified

- `Reproducibility Packet/scripts/utils/archive_units.py` — SHA-256 `2ee891ce7e167edca37f735c6483ba965b7008e4935611e8d38c0177d961fb4a`
- `Reproducibility Packet/scripts/measure_host_drift.py` — SHA-256 `dfbb9cc8620ce85c56350ee2c84b178c0081398aee44513a122db8faeb6607ed`
- `agents/Claude/tools/test_measure_host_drift.py` — SHA-256 `5101d000b3cd803ef53be4930056d0f8608dd9b0736b220519b727e9f2d477b7`
- `agents/Claude/tools/mutate_rc002_repairs.py` — SHA-256 `1e1ed5a9bbda991dc5d2239de05c5cd40510e2a3dcea8fa7713955618d0eceba`
- `agents/Claude/tools/mutation_test_runbook_checker.py` — SHA-256 `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc`
- `Reproducibility Packet/scripts/check_runbook_consistency.py` — SHA-256 `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f`
- `Reproducibility Packet/README.md` — SHA-256 `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5`

I did not edit any candidate file. The candidate is frozen for the Convergence Decision.

## Positive evidence reproduced

- Owner archive-command harness: **266 checks, 0 failed** in 21.9 seconds.
- Repair-mutation harness: unmutated control green and **13/13** mutations caught.
- Packet-checker mutation harness: unmutated control green and **18/18** mutations caught, including all three `PENDING_STEP` cases.
- Packet runbook checker: ten numbered steps plus one explicitly checked pending command.
- Approved estimator harness: **103/103**.
- Estimator claim probes: **3/3**.
- Codex RC-001 probe: zero failures, including the exhaustive 93,184-case rank/offset boundary.
- Codex safety-probe values unchanged at `7.965855… / 8.345705…` and `27.272727… / 11.590909…`.
- All five changed candidate Python files and the new Codex probe compiled.

The checker mutation harness initially failed only because the card's evidence table names the script but not its three required positional arguments. Reading the script and Claude continuity supplied the real interface: packet path, scratch directory and interpreter. With those arguments, all eighteen mutations were caught. The temporary scratch copy was deleted after the run.

## Recorded Round-2 items that now pass

### F1-R1a — fragmented chunks

The new reader obtains every touched chunk's actual `(byte_offset, size)` from the HDF5 chunk index and unions the fixed blocks covering those ranges. The owner's deliberately fragmented fixture now reports a 573,440-byte bound against 327,680 actual bytes and refuses the prior intermediate ceiling. The whole-file fallback remains conservative where placement cannot be obtained.

### F1-R1b — coexisting memory terms

The candidate now enforces one `peak_resident_bytes` quantity containing its retained fixed-block cache bound, converted arrays plus largest stored-width slice, measured Python containers and HDF5 raw-data chunk-cache ceilings. The standard Round-2 construction is refused under the former 81,361-byte admission point.

### F2-R1 — ragged index storage

`spike_times_index` and `spike_depths_index` now require integer storage dtype before conversion. The custom `max_electrode` column retains the narrower compatibility rule: exactly whole floating values may be accepted and their stored dtype is reported.

### F6-R1 and E1 — aliases and evidence scope

Output identity now uses `samefile` where both paths exist and normalized real paths otherwise, respecting the actual filesystem's case behaviour. The repair harness now says explicitly that a text mutation cannot revert F5's file move or checker declaration; standalone command startup and three checker mutations cover those two behaviours directly.

## Blocking late finding: F1-R2

The critical call order is:

1. create `RemoteFile` and open the processed HDF5 file;
2. read electrodes, unit scalars and ragged-column layout;
3. build `plan_transfer` and enforce `max_bytes` against `peak_resident_bytes`;
4. construct the result, including `source_provenance(handle)`;
5. `source_provenance` reads every present path in its provenance allowlist with `node[()]` and returns the resulting strings.

Step 4 occurs after admission. The plan does not include those dataset byte ranges, the retained range-reader blocks they cause, or the Python strings it returns. A schema-valid provenance dataset can therefore make an already admitted read arbitrarily larger than the bound it reports.

Independent evidence: `agents/Codex/tools/probe_rc002_round3.py`, SHA-256 `506d7280f7dbcc98ebc9e0ca544195c9dcfe819eca19e5e6f6b41cfa9adc5e15`.

Observed fixture values:

- processed file size: 4,281,488 bytes;
- planned transfer/cache bound: 174,368 bytes;
- planned combined resident bound and admitted ceiling: 267,001 bytes;
- actual fixed-block transfer and retained cache after provenance: 4,232,336 bytes;
- loaded `general/source_script`: 4,200,030 characters;
- transfer-underbound condition: true;
- resident-underbound condition, even before Python object overhead: true.

This fixture is not evidence about the size of provenance in any real IBL candidate. It is evidence that the command's generic preflight property does not hold. The card makes an understated actual transfer blocking, and the command itself says the combined number is what should be compared with free RAM.

## Why the finding is late and what the method requires

The `source_provenance` call was already present in Round 1. My first pass attacked logical slice payload versus fixed-block reads. Round 2 was correctly delta-only against the new fragmented-chunk calculation and the separately checked cache/array quantities. The existing provenance test used tiny strings and asserted only that they were reported, so it never separated the post-plan read from the plan.

Round 3 expanded the response into a claimed whole-footprint admission number and explicitly asked whether its exclusions were complete. That made the unchanged post-check call contradictory to the repair's own claim. It is therefore both a pre-existing blocker that must be labelled `LATE-BLOCKER` and an unchanged path made false by the response boundary.

The superseding method is unambiguous: any new blocker after Round 2 triggers one Convergence Decision. It does not permit a fourth owner repair and reviewer pass. I therefore made no candidate edit and did not ask Claude for another ordinary response.

## Codex Convergence Decision statement

- **Minimum claim that can ship:** the schema, pairing, clock, anatomy, output-path and estimator-integration repairs may survive into a later candidate, but this state cannot ship as a bounded reader and cannot open a real candidate.
- **Evidence that controls:** the executable post-plan fixture and the call order above; the card defines a transfer undercount as blocking.
- **Strongest evidence against:** every declared suite is green, real provenance may be much smaller, and no real candidate was read. Those facts do not establish the generic admission property.
- **Safe disposition:** **Revisions Required**. Close RC-002 without approval, repair outside formal review, and use one successor card with `Supersedes: RC-002`. A split/redesign is unnecessary because the defect is local.

Claude must write the matching four-part statement once and explicitly agree or counter-propose the smallest terminal disposition. Until then the card is open only for convergence, not for edits.

## Files created or updated

- Created `agents/Codex/tools/probe_rc002_round3.py`.
- Created `agents/Codex/Session Summaries/HumanReport29.md`.
- Updated `Review Cards/RC-002 Archive-Reading Drift Command.md` with the terminal verification and Codex Convergence Decision statement.
- Updated `Review Cards/README.md` status.
- Appended to `chats/Claude-Codex/Archive-Reading Drift Command Review/Archive-Reading Drift Command Review - Active.md`.
- Appended method feedback to `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md`.
- Appended the public forward correction to root `README.md`.
- Updated `agents/Codex/README.md` and completely rewrote `agents/Codex/Summary of Only Necessary Context.md`.

The two active transcript appends were made against UTF-8 physical EOF anchors. Their pre-write line counts were 240 and 250; the new Session-29 header occurs exactly once after each count, at lines 244 and 254 respectively, and both physical tails were re-read after the patch.

## Boundaries and next steps

- No archive, real candidate, raw recording, network source or host value was read.
- No host, target manifest, donor, placement, hybrid, Rung 0 or sorter result exists.
- No dependency was installed and no heavy compute ran.
- RC-002 candidate access remains blocked.
- Claude's next turn should write only the owner Convergence Decision statement and disposition consensus/counterproposal for this card. If `Revisions Required` is agreed, RC-002 closes without approval; repair then occurs outside formal review, followed by at most one successor card.
- Every downstream generation and execution authorization remains separate.
