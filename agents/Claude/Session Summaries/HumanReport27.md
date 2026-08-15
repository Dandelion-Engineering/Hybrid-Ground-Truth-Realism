# Human Report 27 — Claude

**Date and time:** 2026-08-15 03:35 PDT
**Phase:** 2 — Execution
**Session type:** New implementation — the archive-reading drift command — written, tested end to end against synthetic recordings, and handed to Codex under a new Review Card

---

## Summary

RC-001 closed `Approved` in Codex's Session 26, which unblocked the piece of work that has been named as "next" for four sessions: the code that actually opens a candidate host recording and produces a drift verdict. This session wrote it, tested it, and opened RC-002 to review it.

Three new files exist and **no existing file changed by a single byte** — the selection document is still `c35987fe…` and the estimator is still `eace4cd3…`, exactly the states RC-001 closed on.

The work has a clear shape. Until now the drift gate was a definition (§16 of my selection document) and a calculator that takes plain arrays (`band_drift.py`). Neither could see a recording. What was missing was the part that reaches into an 18–197 GB file sitting on S3, works out which of its sorted neurons sit inside the target anatomical band, pulls only those neurons' spike times and per-spike depths out of it, checks that what came back is what the gate assumes, and hands it to the calculator. That is what now exists.

**Most of its code is refusal, and that is the design.** The host candidates are tried in a pinned order under a first-admissible rule, so a candidate recorded as *failing* the drift gate is out of the running permanently and the host passes to the next rank. If a recording's file is malformed — its two parallel lists of spike times and spike depths cut into different pieces, a depth column that no longer says what unit it is in, a neuron whose peak contact belongs to the other probe — then the honest answer is "this candidate's inputs are broken", not "this candidate drifts too much". Those two answers have completely different consequences and the code keeps them apart: an input problem exits with a named error and no verdict, and the candidate stays unjudged.

**Nothing was measured.** No archive read, no candidate opened, no host pinned, no scientific result. Every fixture is a local file this session built.

## What was accomplished

### 1. `Reproducibility Packet/scripts/utils/archive_units.py` — new packet module

Reads one probe's band units out of a processed NWB file over HTTP range requests, and performs the input confirmations §16.8 requires:

- **The two ragged columns are partitioned identically.** NWB stores each variable-length column's per-unit end offsets in its own index dataset, and nothing in the format requires two such columns to agree. If they disagree, a unit's times and its depths are not the same spikes — the statistic would be computed from mismatched pairs and would look perfectly ordinary. The module reads both index arrays in full (one integer per unit) and requires them equal.
- **The loaded values are finite, each unit's times ascend, and the depth column still states its micrometre unit** — the last checked against the column's own stored description rather than assumed.
- **Every unit's peak electrode names exactly one contact on that unit's own probe, with a finite depth.** Band membership is decided by this mapping, so an ambiguous mapping is an input error and never permission to shift the band.
- **The raw and processed files' electrode tables agree.** This one is a genuine trap I had not seen stated anywhere: the band is derived from the *raw* file's electrode table, while `max_electrode` indexes the *processed* file's. If those two tables ever differed, a band measured on one would be applied to neurons placed by the other, silently.

It also plans the transfer before spending it. The ragged index arrays are cheap, so the exact byte cost of the band's slices is knowable before a single spike is read — a count, not an estimate, which is what the project's compute rule asks for before any step that needs real memory.

### 2. `agents/Claude/tools/measure_host_drift.py` — the command

Derives the band, validates the clock, reads the units, runs the approved estimator, builds the deterministic permutation null, **replays that null and requires it to reproduce exactly**, applies the gate, and writes a report carrying every quantity §16.4 and §16.8 require — including the ones that exist only so a published limitation stays checkable.

**The threshold cannot be typed.** `--gate` takes `strict` or `relaxed` and resolves to the two values the project declared before any candidate was read. There is no `--threshold-um`. A threshold that can be passed on a command line is a threshold that can be chosen after the values are in, and the pre-declared ladder is the whole reason §16.7 wrote it down first.

### 3. `agents/Claude/tools/test_measure_host_drift.py` — 163 checks, 0 failed, 10.2 s

Every case builds a pair of local HDF5 files shaped like the raw and processed assets and runs the real `main()` against them — the real ragged-index resolution, the real estimator, the real 200-permutation null, the real report. The only substitutions are a local-file object in place of the network reader and a synthetic asset listing.

All four of §16.8's confirmations have at least one fixture that violates them and asserts the command stops without writing a report, plus three more for conditions the command adds on its own account. The case I would point a reader at is `case_grid_extent_is_t_last`: a fixture whose stream starts at 61 s proves the command gives the estimator 15 bins from the session-time extent and not the 13 bins the recording's *span* would give. That is the one error in this file that would silently change a verdict rather than crash, and §16.4 spends a paragraph on it precisely because the two numbers agree on all twenty-one indexed candidate series — agreement that proves nothing, since an offset can move spikes across internal bin boundaries without changing the bin count.

### 4. `Review Cards/RC-002` and its chat, both opened

RC-002 is a **new candidate, not a successor** to RC-001 — that distinction matters under the review method, because a successor card on the same candidate is the loophole the three-round limit was closed against. RC-001 approved the specification and the calculator; RC-002 covers the code that feeds it.

## Challenges, and how they were handled

### The two defects I found by reading my own output

I rendered a report from a fixture and read it as a reviewer rather than reading the source. Both findings came from that pass, and both are the same species this review chain keeps producing — a number that describes less than it claims to:

1. **The reported archive transfer was undercounting itself.** It printed only the processed file's bytes and requests, silently omitting the raw electrode-table read and the raw timing read. §16.8 asks for these counts precisely so cost is visible, and a count that omits two of three reads is worse than no count at all. It now reports the total and the three-way split, and a harness case asserts the total equals the sum of its parts.
2. **The permutation null was reported by its endpoints only.** §16.5 says to report the distribution; minimum, maximum and the 95th percentile is not a distribution. It now prints deciles — at nearest rank, the same rule the declared summary uses, so no second convention appears beside it — and a case asserts the decile rule reproduces the declared summary at 95.

This is the seventh consecutive session in which reading the rendered output produced the last corrections. It is the single most reliable habit in this workspace.

### One decision I could not make cleanly, and did not paper over

The bin grid's length is `t_last_s`, the raw AP stream's last aligned timestamp — and packet step 7 already measures exactly that. Writing a second implementation of "read the AP endpoints" is the drift the project's standards forbid, and it would be worse than usual here: if the two ever disagreed, the drift grid would be built on a different clock than the one the timing screen recorded. So the command imports that function from the step-7 script rather than reimplementing it, which means a command importing a sibling command's function — an inverted-looking dependency.

The clean alternative is to lift the function into `utils/`, which edits an already-approved packet script. **I did not do that unilaterally.** Both options are stated in RC-002 and in the review chat as something for Codex to rule on, with my reasoning for the one I took.

### The public README had a structural defect, and I fixed it

The four newest running-log entries — including two of Codex's and one of mine — had been appended into the wrong section. A stranger reading the repository's front page would have seen the log apparently end on 2026-08-14, then a section about what the repository contains, then four orphaned log entries after it. This is the first thing anyone outside the project sees.

The four entries were moved back into the running log, in their existing order, byte for byte, with an assertion that each still appears exactly once and that the section boundaries are clean afterwards. I introduced the defect in Session 25 by appending at a convenient anchor rather than the right one; Codex followed the same anchor twice after me. It is recorded here rather than quietly repaired.

## Decisions made, and the reasoning behind them

**The command stays out of the packet's `scripts/` folder, and is not runbook step 11 yet.** The settled position in this project is that a script becomes a numbered runbook step only once it has actually been executed, because a runbook step nobody has run is a guess. It *has* now been executed — 163 checks — but never against the archive, and it has produced no `results/` report. A step claiming otherwise would claim a result that does not exist. Its module preamble is already the packet's standard one, so the move into `scripts/` when the time comes is a copy with no edit. This is flagged in RC-002 as a decision for Codex to overrule if he disagrees.

**The reading logic goes into the packet now, even though the command does not.** `archive_units.py` is shared logic — the noise gate and the effective-SNR gate read the same units table — and the project's standard is that shared logic lives in `utils/` and is imported rather than copy-pasted. It is also invisible to the runbook checker, which walks `scripts/` non-recursively, so the runbook is untouched. This is the same placement `band_drift.py` already has and for the same reason.

**The per-unit audit values are taken from the estimator, never recomputed.** §16.8 requires this explicitly, and the harness checks it by comparing the reported lists elementwise against a direct estimator call on the same arrays. A second centring inside the reader would be a second definition of the same quantity, and the two would eventually disagree.

## Reasoning paths explored

**Whether to run it against a real candidate this session.** RC-001 closing removes the block on measurement in principle, but Codex's Session 26 report states the condition plainly: the implementation is same-state approved *before* a candidate is read. That is the right order and I did not argue with it — the whole point of the pinned candidate order is that a wrong first read is not recoverable. What I did instead was make the pre-approval testing as strong as it can be without the archive, which is what the 163-case harness is.

**Whether synthetic fixtures are worth the effort when the real files are one command away.** They are, and the transfer-ceiling case is why: a fixture can be malformed on purpose. There is no way to ask the archive for a file whose ragged indices disagree, and that is precisely the failure that would produce a plausible-looking wrong number rather than a crash.

**Whether to add a local-file mode to the command for testing.** Rejected. The harness substitutes the file object from outside instead, so the command has no test-only code path in it. A production command with a testing mode has a mode nobody exercises in production.

## Insights gained

**Writing the Review Card's `Purpose` field first changed what I built, not just how it gets reviewed.** Stating the bar before writing the code produced two sentences — *a bad input must never become a drift verdict*, and *an input error must never be recorded as a drift failure* — and those two sentences then decided the code's shape. Eleven of the harness's cases exist because of the second one. Under the old review cycle I would have written the code first and discovered the bar during review.

**The card's weakest field is the one the owner writes about their own work.** RC-002 opens with a `Blocking severity` section written by the person who wrote the candidate. An owner who writes a narrow one has narrowed the review before it starts. I do not think there is a fix inside the method, but it is the field I would read most sceptically as a reviewer, and I have said so to Codex in the chat rather than hoping he notices.

**A trap worth carrying forward: two copies of the same table in two files, with an index pointing into one of them.** The raw/processed electrode-table agreement check exists because I went looking for what the `max_electrode` index actually indexes, and found that the band comes from a different file than the index does. Nothing in the specification said to check it. The general form: *when an index in file A is used against a table in file B, the check is not that the index is in range — it is that A's and B's tables are the same table.*

## Files created or updated

**Created**

- `Reproducibility Packet/scripts/utils/archive_units.py` — SHA-256 `c5c21cb9a2e0f9cedd0f1cff7e98886cb77ccdd21e2ad763422a7b44f3146f12`
- `agents/Claude/tools/measure_host_drift.py` — SHA-256 `c71a5d9311b0785dcff5469e9c698f0f208946cafb00b32dd4eb0bddbda93cfb`
- `agents/Claude/tools/test_measure_host_drift.py` — SHA-256 `6ff3d26ce64016efabdf71aaab93c9a0d71526f37fdcbedae457c438f50a3b39`
- `Review Cards/RC-002 Archive-Reading Drift Command.md`
- `chats/Claude-Codex/Archive-Reading Drift Command Review/Archive-Reading Drift Command Review - Active.md`
- `agents/Claude/Session Summaries/HumanReport27.md` — this report

**Updated**

- `Review Cards/README.md` — RC-002 added to the index
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — session feedback appended
- `README.md` — one running-log entry, and the four misplaced entries moved back into the running log
- `agents/Claude/README.md` — new files, new chat, and the RC-001 close reflected in every status row that named it as open
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten

**Unchanged, and verified so**

- `agents/Claude/Tier A Host and Injection Zone Selection.md` at `c35987fe…`
- `Reproducibility Packet/scripts/utils/band_drift.py` at `eace4cd3…`

## Validation run this session

| Check | Result |
|---|---|
| New end-to-end harness | **163 checks, 0 failed, 10.2 s** |
| Estimator harness (unchanged file) | 103 checks, 0 failed |
| Estimator claim probes | 3 of 3 |
| Codex's independent RC-001 probe | 0 failures |
| Codex's Draft 16 safety probe | digits unchanged |
| Packet runbook consistency checker | 10 of 10 steps |
| `py_compile` on all three new files | clean |
| Non-ASCII characters in the three new files | zero |
| CR bytes in the three new files | zero |
| `agents/Claude/README.md` line endings | CRLF preserved, 159/159 |

## Machine state

Measured at the start of the session and again at the end, per the project's compute rule; no number was inherited.

- **03:08 PDT** — RAM 2.00 GiB free of 31.67; VRAM 1,077 MiB used of 16,311; `C:` 549.4 GB free.
- **03:30 PDT** — RAM 6.65 GiB free of 31.67; VRAM 1,077 MiB used of 16,311; `C:` 549.4 GB free.

Nothing heavy was run. The whole session's compute was small local HDF5 fixtures and a numpy harness needing tens of megabytes, which fit comfortably at both readings. **The 2.00 GiB reading at session start is worth carrying:** the archive read this command will eventually perform is a few hundred megabytes of spike arrays held in memory at once, and that is exactly the kind of step the `--plan-only` and `--max-mib` options exist to size before starting.

## Next steps

1. **Codex's RC-002 Round 1** — a full pass against the card's `Purpose`. Three decisions are flagged for him to overrule rather than accept: keeping the command outside `scripts/`, importing `read_series_timing` from a sibling script rather than lifting it into `utils/`, and removing every command-line route to an undeclared threshold.
2. **When RC-002 closes `Approved`, the first candidate can be read** — rank 1, CSHL047 Probe01, at the strict 20 µm gate, with `--plan-only` run first and the machine's free memory measured against that exact number before the real read starts.
3. **The remaining host gates stay open**: noise, post-rescaling effective SNR, the joint ten-placement condition under Amendment 6, and Codex's balance gate.
4. **No count-based progress report is due**; the next is my Session 32.

**Nothing in this session is waiting on Randy.**
