# Human Report 32 — RC-003 Round 3: the two blockers repaired, and the repair that moved up a level

**Date and time:** 2026-08-16 00:58 PDT
**Session:** Claude Session 32
**Phase:** 2 (Execution). No host pinned, no candidate measured, no archive read, no generator or sorter run, no scientific result.
**Progress report:** count-based report due at this session (8, 16, 24, **32**) — written, at `agents/Claude/Progress Reports/Progress Report Session 32.md`.

---

## 1. What this session was

RC-003 Round 2 returned `Revisions Required` with two blockers still open. This session wrote the **Round 3 owner response**, which is the final response the review method allows on this card: if Round 3 does not reach same-state approval, clause 5 forbids a second like-for-like successor and the work must be split or redesigned with the changed boundary named.

Both blockers were accepted in full and neither was disputed. Before editing anything I ran Codex's `probe_rc003_round2.py` unmodified against the unchanged candidate; it returned his exact figures — `negated_toolchain_reaches_verdict=True`, `mismatched_conversion_values_reach_verdict=True`, `default_block_transfer=2081456 provenance_budget=65536 exceeds_budget=True`, exit 0.

## 2. RC-003-F1 — a search is not authentication

**The finding.** `authenticate_provenance()` required the case-insensitive substring `neuroconv` anywhere in the asset's `general/source_script`. A processed fixture reading `This asset was NOT created using NeuroConv; exported by LocalTool v3` therefore reached a passing drift verdict. Separately, raw `v0.9.2` paired with processed `v0.9.1` reached a verdict with disagreement merely recorded.

**The repair.**

- `CONVERSION_SOURCE_FORM` matches the **whole value** end to end — `^created using neuroconv v<version>$`, case-insensitive, whitespace-stripped — so a value that denies the toolchain is refused although it names it. The version is parsed out by a new `conversion_version()` helper.
- `authenticate_provenance_pair()` requires the two assets of one session to name the **same** converter version, and it runs in preflight (via a new `expect_conversion=` argument to `read_band_units`) rather than after the payload is read.

**The judgement inside it, stated so it can be attacked.** Codex offered two branches: require the values to agree, or justify why the admitted difference still establishes the common clock. I took the strict branch, because the other one needs evidence this project does not have — nothing measured here says a NeuroConv version difference is harmless to the session-time coordinate, and Session 7 read one *raw* asset per subject, so it says nothing about whether a session's two halves are converted together. The failure mode is recoverable: §16.4 makes an input error pause the pinned order rather than reject the candidate.

**What is deliberately not gated.** The version itself. `MEASURED_CONVERSION_VERSIONS = ("0.9.1", "0.9.2")` is reported and never enforced, because that tuple came from 21 *raw* assets and the one reading `v0.9.1` belongs to **NYU-39, a host subject** — the dandiset is demonstrably not uniform, and gating on a sample would reject a file this project has never read on a number it has never measured.

## 3. RC-003-F3 — the repair the measurement moved up a level

**The finding.** `BoundedReader._charge()` checked the length h5py asks for, and then delegated to a reader that fetches whole `--block-kb` blocks. At the 1 MiB default, a two-million-character value refused under a 65,536-byte budget still caused **2,081,456 distinct bytes** to transfer first.

**The first repair, which was correct and insufficient.** The proxy now models the reader's block cache: for every read it computes which blocks that read would *newly* fetch, charges their whole size against a second, transfer-denominated budget, and refuses **before delegating**. The budget is derived rather than chosen, in `provenance_transfer_budget()`: the request budget plus one block per provenance path. The first term is provable — a value of at most `C` bytes at an arbitrary offset spans at most `ceil(C/B)+1` blocks, i.e. at most `C + 2B` — and the second leaves `2B` for the structures that reach the four paths.

**Then I measured where his bytes actually went, and the answer changed the repair.** Instrumenting `source_provenance` on his own construction:

> **2,081,456 spent before the provenance read; 0 spent by it; 2,081,456 in total.**

Every byte belonged to the four preflight reads that precede provenance — the electrode table, the unit scalars, and the two column descriptions. Those reads are *counted*: their cost lands in `spent_bytes` and therefore inside the published plan. But counted is not refused, which is Codex's own Round-1 F3 one level up, and a repair scoped to the provenance read would have made a true statement about a number that was never the problem.

**So the caller's declared ceiling is now held open as a transfer budget for the whole read**, entered before `h5py.File` opens the file. On his construction with his one-byte ceiling, **nothing moves at all — 0 bytes against 2,081,456.**

**The "cannot make anything infeasible" argument**, because a tightening inside a safety check needs one: `peak_resident_bytes` contains `cache_bound_bytes`, which upper-bounds the distinct bytes the read fetches, so any read the later ceiling check admitted had already transferred less than `max_bytes`. Refusing a fetch that would cross `max_bytes` refuses only what the later check would have refused anyway — earlier. The one behaviour it changes: a plan whose `cache_bound_bytes` *under*-bounds the real transfer now fails loudly during the read rather than silently, which is the RC-002 defect class turned into a refusal.

**Two consequences declared rather than left to be found.**

- **Budgets nest now.** `BoundedReader` keeps a scope stack; a read is refused unless it fits in *every* enclosing scope and is charged to all of them only once it has. `ReadBudgetExceeded` carries the refusing scope's label, and `source_provenance` absorbs only its own — an enclosing ceiling refusal recorded as "this value could not be read" would be a failure reporting itself as a success. A case (`ceiling_marker`) requires it to escape, and a mutation (`F3e`) proves the case is load-bearing.
- **The raw asset's provenance read caps its block** at `PROVENANCE_BLOCK_BYTES = 65536`, below whatever the caller passed. It is the one read with no plan behind it, and a block-denominated bound should not scale with a block size chosen for a bulk payload read on a different file: 327,680 bytes instead of 4,259,840.

## 4. RC-003-E1 — closed

The report no longer says the records file carries provenance values "in full". It now says each value is carried exactly as the command holds it — the file's value for a path read whole, a self-describing refusal or truncation marker for one the budgets declined — and that only the required `general/source_script` is necessarily complete on a verdict.

## 5. Three of the six new mutations were wrong before they were right

This is the part I would review hardest if I were the reviewer.

- **`F1g`** (stub authentication) predated the new `version` field, so under the mutation every case died on a `KeyError`. A crashed suite reports every case as failed, so the mutation was scored on something unrelated to what it reverted.
- **`F1h`** removed the provenance budget by passing `None`, which left the published spend `None` and made the new whole-suite invariant compare `None` with `None`. Same failure, different cause.
- **`F3f`** named a check whose name contained a space. The harness matches on the first whitespace-delimited token of a failed check, so that expectation could never match — it reported `MISSED` for a reason unrelated to the repair.

**The general form: a mutation can pass or fail for the wrong reason exactly the way a test can.** All three were found by re-running the harness after the repair, not by reading it. That is the second session running where re-running the mutation harness — rather than trusting a green suite — is what produced the correction.

## 6. Two files changed for reasons that are not repairs, both declared

- **`verify_rc003_round1_repairs.py`** required the Round-2 refusal message after a bounded-but-nonzero spend. The Round-3 repair refuses that construction earlier and spends nothing, so the unchanged script reported an improvement as a failure. It now accepts either bound and still requires the refusal.
- **`test_measure_host_drift.py`** no longer leaves its fixture trees behind. It removed them with `shutil.rmtree(..., ignore_errors=True)` while local readers were still open, which fails silently on Windows; 111 `drift_reader_*` directories had accumulated by Session 31. Readers are closed first and the suite prints a warning if a directory survives. Recorded at Session 31 rather than repaired because the file was mid-review; repaired here because it is a defect in a file this card asks Codex to approve. Verified: 28 leftover directories deleted, and a full suite run now leaves zero.

## 7. Evidence, all on the exact Round 3 state

| Test | Result |
|---|---|
| `test_measure_host_drift.py` | **382 checks, 0 failed, 14.6 s** (325 at Round 2; 57 new) |
| `mutate_rc002_repairs.py --repo-root .` | **26 of 26, control green at 382** (20 of 20 at Round 2) |
| `mutation_test_runbook_checker.py` | **18 of 18, control green** |
| `check_runbook_consistency.py` | 10 steps agree, 1 script pending a step |
| `verify_rc003_round2_repairs.py --repo-root .` | all three Round-2 constructions refused; one-byte ceiling moves **0** bytes |
| `verify_rc003_round1_repairs.py --repo-root .` | all three Round-1 constructions still refused |
| `test_band_drift.py` | 103 checks, 0 failed |
| `probe_band_drift_claims.py` | 3 of 3 |
| `probe_rc001_round1.py --repo-root .` | 0 failures |
| `probe_draft16_safety_claims.py --repo-root .` | digits unchanged: `7.965855925506574` / `8.345705622445344`, `27.272727272727273` / `11.59090909090909` |
| `probe_rc003_round2.py --repo-root .` | **exit 1** — both F1 paths stop as input errors, `default_block_transfer=0` |
| `probe_rc002_round3.py --repo-root .` | exit 1, raising before a plan exists, as at Round 2 |
| Compilation | clean on the five changed files and the new one |
| Console safety | `--help` on all six scripts that have one: 8,059 / 3,585 / 2,413 / 7,130 / 1,673 / 2,696 bytes, zero non-ASCII |

## 8. Files created or updated

**Changed (the candidate and its harnesses):**

- `Reproducibility Packet/scripts/utils/archive_units.py` — `96a31b3d46e18a7f387cc5d9d5c3fe37984f1346139477deb57f8f062ce1556e`
- `Reproducibility Packet/scripts/measure_host_drift.py` — `0bf08153fde8b48a6485596c6b8375920fe56d33a66fd0a35c41833f484335e5`
- `agents/Claude/tools/test_measure_host_drift.py` — `92e9091391e05b687225d1c0b7c1e7783bbb34cae194dcd8f5e11a6946e15286`
- `agents/Claude/tools/mutate_rc002_repairs.py` — `9955ef603ae0a7d7ebd094459d41b18933e32e52b0d3fb69a29b30cee8dc72f4`
- `agents/Claude/tools/verify_rc003_round1_repairs.py` — `2b7d9ef6eadae52f3c44ee603177efa474dcf692167278b67cbd50db6a79211d`

**Created:**

- `agents/Claude/tools/verify_rc003_round2_repairs.py` — `9fb49fe8bfc098e25490e98cb596c13e20ebff7af3cac0c65421e468092112a0`
- `agents/Claude/Progress Reports/Progress Report Session 32.md`
- `agents/Claude/Session Summaries/HumanReport32.md` (this file)

**Updated (records and coordination):**

- `Review Cards/RC-003 Archive-Reading Drift Command, Bounded-Read Repair.md` — Round 3 state table, round-log row, owner response, owner evidence, outcome, E1 closed
- `Review Cards/README.md` — index status
- `chats/Claude-Codex/Bounded Archive Read Review/Bounded Archive Read Review - Active.md` — Round 3 response
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — method observations
- `README.md` — running-log entry and banner date
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — closeout

**Unchanged and carried:** `agents/Claude/tools/mutation_test_runbook_checker.py`, `Reproducibility Packet/scripts/check_runbook_consistency.py`, `Reproducibility Packet/README.md`, and every approved state (`Claim Sheet.md`, `Accessible Claim Sheet.md`, the Study Guide, `band_drift.py`, `test_band_drift.py`, the Tier A selection document).

## 9. Machine state

Measured at the start of the session's heavy work: **17,104 MB available physical RAM of 32,425**, 18.5% of the commit limit in use, 106,271 of 130,415 MB pagefile available. A quiet machine. Everything this session ran was synthetic; the largest fixture was about 2 MB, and the two mutation harnesses run one small copy of the tree at a time. Both were run with `run_in_background` and collected from their output files, per the standing note that their stdout is buffered when redirected.

## 10. Cross-review

Codex's most recent human report and his Round-2 ledger were read in full, and his `probe_rc003_round2.py` was read line by line and executed unmodified before any edit. Both of his findings were accepted without dispute; the only place I went beyond what he asked was the ceiling, and that was because measuring his own construction said the finding's scope was narrower than the defect.

## 11. What is open, and what happens next

- **RC-003 Round 3 is with Codex, delta-only.** Candidate access stays blocked until it closes `Approved`.
- **Clause 5 is live.** A non-approval disposition closes RC-003 without approval; no second like-for-like successor may open, and the work must be split or redesigned with the changed boundary named. If that happens, the next session's first job is to propose that boundary and take it to the director.
- **If it closes `Approved`,** the next work is the first real candidate measurement: CSHL047 Probe01, session `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`, `--plan-only` first, against a fresh RAM measurement.
- **One thing I now expect to bite on the first real run.** Requiring the conversion statement on both assets and requiring the pair to agree can stop a real candidate as an input error. That is designed behaviour (§16.4 pauses the pinned order), but it is a new way for the first real attempt to halt, and the value should be reported and the rule amended rather than loosened in place.
- **`director_requests.md` has nothing waiting on Randy.**
