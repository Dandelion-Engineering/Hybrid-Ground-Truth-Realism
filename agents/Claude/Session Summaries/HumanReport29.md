# Human Report 29 — Claude

**Date and time:** 2026-08-15 07:48 PDT
**Session:** Claude Session 29
**Phase:** Phase 2 — Execution
**Progress report due?** No. The next count-based one is Session 32, and this session closed no phase transition and wrote no approving amendment turn.

---

## What this session was

One thing: **RC-002 Round 3, the final owner response the bounded review method allows.**

Codex's Round 2 returned `Revisions Required` with three blocking defects and two non-blocking items in the archive-reading drift command. Under the method, my response to it is the third round-trip, and Codex's verification of it is terminal — an approval closes the card, and anything short of one sends the card to the agent-only Convergence Decision rather than to a fourth round. Nothing else was worked on and nothing was read from the archive.

All three blockers are repaired. Both non-blocking items are closed rather than carried. One of them turned into the most useful finding of the session, and it was a finding about my own evidence rather than about the code.

---

## The three blockers, and what each repair actually changed

### F1-R1a — the transfer bound assumed a dataset's chunks sit next to each other

The plan's job is to say, before a byte is spent, how much a read will transfer. For a chunked HDF5 column the previous rule rounded the needed element range out to whole chunks and then placed the result as **one contiguous byte span**. HDF5 does not promise that. A file written incrementally alongside other growing datasets interleaves its chunks with unrelated data, and Codex built exactly that file: the plan claimed `241,664` bytes, the block-fetching reader moved `327,680`, and a ceiling of `284,672` was admitted and then exceeded.

The repair asks instead of assuming. `chunk_byte_ranges` reads every touched chunk's own `(byte_offset, size)` out of the chunk index, and the plan unions the fixed blocks covering those real ranges. There are now three placement routes, and `bound_basis` names which were used:

- `dataset offsets` — a contiguous dataset whose file offset h5py gives.
- `chunk offsets` — a chunked one, placed chunk by chunk.
- `whole file` — neither is available, so the only remaining true statement is that a reader cannot fetch more distinct bytes than the file holds.

That third one is deliberately loose, and the reasoning is written down rather than left implicit: a wrong refusal is recoverable by deliberately raising the ceiling against a measurement, and a wrong admission is not. On the fragmented fixture the bound is now `573,440` against an actual `327,680`, and the ceiling that used to be admitted is refused.

One detail that mattered: reading the chunk index costs range requests. Those reads now happen **before** the plan records what the read has already spent, so they are counted rather than invisible.

### F1-R1b — the two memory figures were checked one at a time, and they are alive at the same time

The reader's block cache is unbounded and is not released until the read returns. So while the last neuron's converted arrays are accumulating, every block that fed the first neuron is still resident. The ceiling was being enforced against the block bound and the array bound **separately**, which admitted a ceiling that neither exceeded on its own: `81,361` bytes admitted while `81,360` cached bytes coexisted with `57,600` bytes of arrays.

There is now one quantity, `peak_resident_bytes`, and `max_bytes` is enforced against nothing else. It is the sum of four terms:

1. `cache_bound_bytes` — the retained block cache.
2. `resident_bytes` — the converted arrays plus the largest slice at its stored width.
3. `structures_bytes` — a `sys.getsizeof` walk over the live Python containers, counting a shared object once per reference so it over-counts rather than under-counts.
4. `library_cache_bytes` — HDF5's own per-dataset raw-data chunk cache ceiling.

Because it contains the transfer bound, this is strictly stronger than the two separate checks: nothing refused before is admitted now.

**The fourth term is the part I want on the record as a decision rather than a detail.** My first draft of this repair declared HDF5's internal caches *out of scope* in the docstring. That would have been the same move as the defect — naming the gap instead of closing it — and the number turned out to be readable straight off the dataset's access property list. So it is charged. What remains excluded is now named explicitly instead of left to be discovered: the interpreter's baseline, allocator overhead, and transient h5py allocations outside a chunk cache.

### F2-R1 — a spike index stored as decimals is malformed, however round the values are

`spike_times_index` is an HDMF `VectorIndex`, and the common schema specifies integer storage for it. The previous version accepted a floating-point index whose values happened to be exactly whole, on the reasoning that the conversion was lossless. Codex's point is that this is the project inventing a laxer schema than the format has, on the dataset that decides which spikes belong to which neuron.

Integer storage is now required for the two ragged indices and **not** for `max_electrode`, which is a custom IBL column the schema does not type — a whole-valued float is still accepted there and its dtype reported. The asymmetry is written into the module docstring with its reason, because an unexplained inconsistency reads as an oversight.

**A consequence worth flagging.** Codex's Round-1 fractional-offsets fixture now stops on dtype rather than on fractionality, because the dtype rule fires first. I kept the case with its assertion changed and its docstring saying so, and integrality on its own is still exercised on `max_electrode`, which is the column where it is the only rule available.

---

## The non-blocking items, and the one that found something

### F6-R1 — path aliases

`same_output_path` now asks `os.path.samefile` when both paths exist and otherwise compares after resolving links and normalizing case. Its test case asserts **what the filesystem under the fixture actually does** rather than assuming: on a case-insensitive filesystem a case-only pair must be refused; on a case-sensitive one those are two real files and must be accepted. A guard that rejected two genuine files would be a different bug of the same size.

### E1 — a coverage claim of mine that was false, and a second one I nearly shipped in its place

Codex found that the harness I built last session — the one that removes each repair in a clean copy and requires the test suite to notice — described itself as covering *every finding's* repair while having no entry for F5. He offered two acceptable responses: add the mutation, or narrow the claim.

I tried to add it. The obvious candidate was the command's `sys.path` line, and the mutation was **missed**. The reason is that CPython puts a directly executed script's own directory on `sys.path` regardless, so removing that line changes nothing observable — the entry would have been a green tick with nothing behind it. F5's repair was never an edit at all: it was *moving the command into the packet* and *declaring it pending in the runbook checker*, and a harness that reverts one anchored string per copy cannot revert either of those.

So the claim is narrowed, in those terms, in the harness's own docstring. But narrowing alone leaves the coverage gap real, so I closed it in two places instead:

- The acceptance suite gained a case that runs the moved command as a **subprocess with `PYTHONPATH` cleared** and requires `--help` to work. Every other case in that file imports it with the packet's folder already on the path — which is precisely the condition that hid the original defect.
- **Here is the part worth reading.** My first draft of the narrowing said the other half was covered by the runbook checker's own mutation harness. I checked before writing it down. It was false — that harness had no pending-related mutation at all. So rather than soften the sentence I made it true: three new mutations there, taking it from fifteen to **eighteen**. Remove the pending declaration and the stepless script must be reported; declare a script that already has a numbered step and that must be an error; delete a declared script and the stale declaration must be caught.

That mechanism was described in Codex's Round 2 as "narrow, checked, and visible." Until this session the *checked* part was not checked. I nearly replaced one false coverage claim with another one while in the act of correcting it.

---

## A correction to my own Round-2 evidence

The Round-2 acceptance table records "zero non-ASCII characters in all five changed/new Python files." That was wider than the check behind it. `check_runbook_consistency.py` has carried a single en dash since Session 13, inside the regular expression that matches the packet README's step headings. It is not a console-safety problem — the character is never printed, and I verified this time by **capturing** each script's `--help` output rather than scanning its source, and all four are ASCII. But the sentence overstated what had been verified, and the file is part of the candidate, so the correction is in the review card and in the chat rather than quietly applied.

---

## Evidence

Every number below was produced this session, on this machine, with `./venv/Scripts/python.exe`.

| Check | Result |
|---|---|
| `agents/Codex/tools/probe_rc002_round2.py --repo-root .`, against the **unchanged** candidate | all four of his constructions reproduced exactly, including his digits |
| `agents/Claude/tools/test_measure_host_drift.py` | **266 checks, 0 failed, 13.8 s** (231 at Round 2) |
| `agents/Claude/tools/mutate_rc002_repairs.py --repo-root .` | **13 of 13 mutations caught, control green** (8 at Round 2) |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | **18 of 18 mutations caught, control green** (15 at Round 2) |
| `check_runbook_consistency.py` from inside the packet | 10 steps agree, 1 script pending a step |
| `agents/Claude/tools/test_band_drift.py` | 103 checks, 0 failed |
| `probe_band_drift_claims.py` | 3 of 3 |
| `agents/Codex/tools/probe_rc001_round1.py --repo-root .` | 0 failures |
| `agents/Codex/tools/probe_draft16_safety_claims.py --repo-root .` | digits unchanged: `7.966` / `8.346`, `27.273` / `11.591` |
| `agents/Codex/tools/probe_rc002_round2.py`, against the **repaired** candidate | raises where it used to demonstrate — the read it needs admitted is refused. That is the repair; the probe is Codex's to re-pin. |
| Compilation, CR bytes | clean on all five changed Python files |
| `--help` output captured and checked | ASCII on the four scripts that have a `--help`. Two candidate files hold never-printed non-ASCII in string literals matching the README step headings, both predating this round; the review card names them. |

---

## Reasoning paths explored, including one abandoned

- **A conservative per-chunk arithmetic bound instead of reading the chunk index.** Codex offered this as an acceptable alternative. I chose the chunk index because it makes the common case *exact* rather than merely safe, and because a bound loose enough to be safe without knowing where the chunks are is loose enough to refuse reads that would have fit. The loose route still exists as the third branch, for files that will not answer.
- **Whether to charge for HDF5's internal cache or declare it out of scope.** Described above. Declaring it would have been defensible and would have been worse.
- **Whether a mutation can be written for F5.** Tried, measured, abandoned with the reason recorded. The measurement — that CPython adds a script's own directory to `sys.path` — is why the entry would have been theatre.
- **Whether to reopen the fractional-offsets case or leave it.** Left, with its assertion and docstring updated, because it still establishes the thing it exists to establish and re-deriving it would have been re-litigating a closed finding.

---

## What is still true, and what is not done

- **No archive or candidate asset has been read.** Every fixture in this session was local and synthetic.
- **No host is pinned, no sorter has run, and no scientific result exists.**
- **Candidate access stays blocked until RC-002 closes.** If Codex approves, the next work is the first real candidate measurement — rank 1, CSHL047 Probe01, `--plan-only` first, with free RAM measured against `peak_resident_bytes` rather than against the array term alone. If he does not, the card goes to the Convergence Decision, which is agent-only and does not reach the director.
- The four other open items from the previous session are unchanged: the capacity gate under Amendment 6, the five packet steps not yet re-run, the preprocessing half of the amplitude question, and the 66 unmapped host long names.

---

## Files created or updated

| Path | What changed |
|---|---|
| `Reproducibility Packet/scripts/utils/archive_units.py` | `chunk_byte_ranges`, `band_slices`, `python_structure_bytes` added; `column_layout` takes slices and reports `chunk_map` and `library_cache_bytes`; `_slice_block_bytes` replaced by `_slice_blocks` with three placement bases; `plan_transfer` reports `structures_bytes`, `library_cache_bytes` and `peak_resident_bytes`; `read_integer_column` gained `require_integer_dtype`; the ceiling is enforced on one combined quantity |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `same_output_path` added and used by the output-collision guard; report and record carry the new cost terms; the module docstring and `--max-mib` help describe the combined bound |
| `agents/Claude/tools/test_measure_host_drift.py` | 231 → 266 checks. New: fragmented-chunk fixture writer and case, combined-resident case, unplaceable-column case, float ragged index case, path-alias case, standalone `--help` case; three existing cost cases rewritten; new check names given single-token prefixes so the mutation harness can match them |
| `agents/Claude/tools/mutate_rc002_repairs.py` | 8 → 13 mutations; coverage claim narrowed with F5's reason stated |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | 15 → 18 mutations; the three new ones test the `PENDING_STEP` exemption |
| `Review Cards/RC-002 Archive-Reading Drift Command.md` | Round 3 candidate hashes, round-log row, owner-response section, outcome, follow-ups closed, Round-2 evidence correction |
| `Review Cards/README.md` | index row status |
| `chats/Claude-Codex/Archive-Reading Drift Command Review/…Active.md` | the Round 3 response, appended, plus an appended format correction to its own timestamp |
| `README.md` (root) | running-log entry 56 |
| `agents/Claude/README.md` | tool and artifact rows updated for this session |
| `agents/Claude/Summary of Only Necessary Context.md` | rewritten |
| `agents/Claude/Session Summaries/HumanReport29.md` | this file |

---

## Machine state, measured rather than inherited

- **07:06 PDT:** `FreePhysicalMemory` 0.61 GiB, `\Memory\Available MBytes` **2,234 MiB**, VRAM 1,079 of 16,311 MiB used, `C:` 589 GB free.
- **07:20 PDT:** available **7,154 MiB**, taken before starting a second concurrent process.

Both readings were taken at the moment they were needed, not at session start. This session's heaviest step was the mutation harness, which builds one small copy of the packet scripts at a time and runs a suite whose whole compute is tens of megabytes; nothing came close to either reading. **No candidate read was attempted, so no `peak_resident_bytes` was compared against free RAM.** That comparison is the first thing the next session does, and it must take its own reading.

---

## One methodological note for the review-method chat

The Review Method Change chat stays active at Randy's request, and this session produced one observation worth adding there next session. **The method's delta-only rule interacted well with a response that closed a finding by proving it could not be closed the expected way.** Codex's E1 offered two options; the honest answer turned out to be a third — narrow *and* build the coverage somewhere the harness can reach. Because the rule scopes Round 3 to the recorded findings and to regressions my response introduces, that answer is checkable in a bounded pass rather than opening a new argument about what the harness ought to be. I want to see whether Codex agrees before writing it into the chat as a method observation rather than a session opinion.
