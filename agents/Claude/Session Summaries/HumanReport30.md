# Human Report — Claude Session 30

**Date and time:** 2026-08-15 09:37 PDT (clock read at the moment this file was written)

**Phase:** 2 — Execution

**Session outcome:** RC-002 closed **`Revisions Required`** by the project's first Convergence Decision, with both agents in explicit agreement. The defect was repaired outside review in the same session, the general rule behind it became a whole-suite test, and RC-003 is open on Codex.

---

## What this session was for

Codex's terminal Round-3 verification of the archive-reading drift command found one blocking late defect and, under the review method Randy directed, refused to run a fourth round. He froze the candidate, wrote his one Convergence Decision statement, and left me exactly one move: my own statement and either agreement on the terminal disposition or the smallest counterproposal.

That was the required work. Everything after it — the repair, the new coverage, the successor card — happens *outside* formal review, which is what convergence clause 4 is for.

## The defect, in plain terms

The command sizes a read before it performs it, so the operator can compare the cost against the machine's free memory before spending it. That plan is enforced as a ceiling: if the read would hold more than the ceiling allows, it is refused.

**One read happened after the ceiling had already said yes.** `read_band_units` computed and enforced `peak_resident_bytes`, and then, while assembling its result, called `source_provenance(handle)` — which reads each of the file's conversion-provenance datasets *complete*. None of those bytes, and none of the strings they produce, were in any of the plan's terms.

Codex's counterexample is a generated local file, schema-valid in every respect, whose `general/source_script` holds 4,200,030 characters. The plan reports a `174,368`-byte transfer bound and a `267,001`-byte peak. A run with the ceiling set to exactly that peak is **admitted**, and then transfers and retains **4,232,336 bytes**. The transfer bound is exceeded twenty-four-fold; the admitted memory ceiling more than thirtyfold.

**I reproduced it before writing a word.** His probe, unmodified, at the hash he published, returned his figures to the byte on this machine.

## What I did, in order

### 1. The Convergence Decision statement

Four elements, written once, into both the chat and the card.

- **Minimum shippable claim:** not this state, and not as a bounded reader. The repairs that survive on their tested boundaries — the input confirmations, the pair-identity and clock checks, the pinned anatomy threshold, the packet location, the chunk-index placement, the combined memory figure, both mutation harnesses — should be carried into a successor rather than re-derived. What cannot ship is the *claim* attached to the numbers, because the function whose docstring opens *"Size the band units' read before any of it is spent"* is called from a path that then spends unplanned bytes.
- **Controlling evidence:** his fixture and the source order, `archive_units.py:828` enforcing the ceiling and `:846` reading provenance.
- **Strongest evidence against my own position:** that the real IBL provenance value is probably kilobytes so the defect may never bind — rejected, because "the asset we hope to get" is reasoning this project has refused every time; and that provenance is metadata the ceiling never claimed to cover — rejected on my own Round-3 docstring, which says the combined figure is *"what a free-RAM measurement has to be compared against"*.
- **Disposition:** `Revisions Required`, agreeing with Codex exactly. Not `Split/Redesign` because the mechanisms that fix it already exist in the candidate; not `Approved with Follow-ups` because the defect is demonstrated rather than underdetermined, and clause 2 forbids resolving that in favour of approval.

**I swept the general claim before agreeing**, which produced one thing neither of us had said: the command performs two further reads that no ceiling covers at all — the raw file's electrode table and its AP-series timestamps. I did **not** call them a second blocker, because both are bounded by construction and neither grows with the recording. But they are the same accounting gap, and I said so rather than letting the repair be the narrow one.

### 2. The repair, outside review

**Three parts, and a fourth that matters more than the three.**

1. **The provenance read moved into preflight**, before the reader's spend is captured. Its bytes now land in `spent_bytes`, and therefore inside `cache_bound_bytes` and `peak_resident_bytes`; its returned dict is passed to `held=`, so the retained strings are charged into `structures_bytes`.
2. **A pinned per-value cap**, `PROVENANCE_MAX_BYTES = 65536`, in the module rather than on the command line — a value read from a candidate must not choose the number that decides whether reading it was allowed. It has two halves because HDF5 answers the size question for only one of them. Where the stored size is meaningful, an oversized value is **not read at all**. For a variable-length string it is not meaningful: I measured it rather than assuming, and on h5py 3.16.0 a 4,200,030-character value reports **16 bytes** of storage and **8** of `nbytes`, because the characters live in the global heap. There the value is read in preflight and **retained only up to the cap**, with a marker naming its real length.
3. **The ceiling's scope is stated in the command**, both in the module docstring and in `--max-mib`'s own help: it covers the processed read and every read inside it, and not the two raw-asset reads, whose cost is reported separately as `raw_electrodes` and `raw_timing`. The defect was a read outside a bound whose scope was never written down; writing it down is part of the repair.
4. **The general rule became a test.** `run_case` now requires, on **every** case that reaches a record, that the distinct bytes touched on the processed fixture are inside `plan["cache_bound_bytes"]`, and fails loudly if it matched no reader at all. Two named cases cover the two halves of the cap. Three new mutations cover the repair, and the important one is `F1d`: it sets `spent_bytes` to zero, which is byte-for-byte the state the post-ceiling read created, and it is caught by the whole-suite invariant rather than by any provenance case. **The defect that closed RC-002 would now fail this suite without anyone looking for it.**

### 3. The successor card and the chat

RC-003 is open, `Supersedes: RC-002`, with all seven files in the candidate — the four that changed and the three that carried unchanged — because RC-002 closed unapproved and *nothing in it shipped*. Round 1 is stated as a **full** pass rather than a delta, and the card says why: clause 5 forbids a second like-for-like successor, which creates an incentive to narrow the successor's scope so fewer findings can land in it, and narrowing would be scoping my way to a pass.

## Challenges, and what happened to them

**The invariant caught an error in itself, and that is the part worth reading.** My first version compared `record["io"]["processed_units"]["bytes"]` against `cache_bound_bytes`. Those are not the same quantity: the harness's local reader has no cache and counts a re-read twice, while the bound is on *distinct* bytes. It reported a violation of `84,144` against `81,360` on the standard fixture, on **eighteen cases at once** — and every one of them was double counting. The number that gave it away is that both figures sat at the fixture's own file size.

Had I trusted it, I would have "found" a defect that does not exist and repaired code that is correct. Had I only silenced it, I would have removed the one test that catches the real thing. The fix was to make the comparison real: the readers now record the byte ranges they touch, and the invariant compares the union. **A test written to prevent a false pass produced a false failure, and the second is not the safe direction either.**

**A smaller one:** two mutation anchors I typed from memory did not match the file — one because the argument spans two lines, one because the card's status line uses an em dash where I had typed two hyphens. Both were caught by the assert-exactly-one-match discipline rather than by silently editing nothing, which is what that discipline is for.

## Decisions I made alone

- **Agreeing with Codex's disposition rather than counterproposing.** The alternative worth considering was `Approved with Follow-ups` on the argument that a real IBL provenance value is small. I rejected it, and said why in the statement.
- **Capping rather than declaring the variable-length case out of scope.** My first instinct was to write "there is no pre-read size for a vlen string, so this cannot be bounded". That is true of the *transfer* and false of the *retention*, and the same instinct in Session 29 nearly lost a memory term that turned out to be one API call away.
- **Not bringing the two raw-asset reads under the ceiling.** They are bounded by construction and their cost is already reported. I stated the boundary instead — and flagged it to Codex as the judgement I most want attacked.
- **Making RC-003's Round 1 a full pass.** Costlier for me, and the honest reading of a candidate that has never been approved.

## Evidence, all run on the exact state now on disk

| Test | Result |
|---|---|
| `agents/Claude/tools/test_measure_host_drift.py` | **279 checks, 0 failed, 29.4 s** (266 before) |
| `agents/Claude/tools/mutate_rc002_repairs.py --repo-root .` | **16 of 16 mutations caught, control green** (13 before) |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | **18 of 18, control green** |
| `check_runbook_consistency.py` | 10 steps agree, 1 script pending a step |
| `agents/Claude/tools/test_band_drift.py` | 103 checks, 0 failed |
| `probe_band_drift_claims.py` | 3 of 3 |
| `agents/Codex/tools/probe_rc001_round1.py --repo-root .` | 0 failures |
| `agents/Codex/tools/probe_draft16_safety_claims.py --repo-root .` | digits unchanged: `7.965855925506574` / `8.345705622445344`, `27.272727272727273` / `11.59090909090909` |
| `agents/Codex/tools/probe_rc002_round3.py --repo-root .` | **exit 0 against the frozen state with Codex's exact figures; exit 1 against the repaired state, both underbound flags False** |
| Compilation | clean on the four changed files |
| Console safety | `--help` captured on both scripts that have one: 6,763 and 3,585 bytes, zero non-ASCII |

**Machine readings, taken rather than inherited.** 09:06 PDT — 0.49 GiB free *physical* RAM, **7,067 MiB available** including standby, VRAM 1,078 of 16,311 MiB. 09:26 PDT, with the mutation harness running — **2,521 MiB available**, 41 MiB free physical, and committed memory at **128,194 of 129,385 MB**, which is the tightest commit reading this project has recorded. No single process was large; the largest working set on the machine was 182 MB. I ran the two ~4-minute mutation harnesses one at a time in the background rather than concurrently, and held the light checks until each finished. Nothing heavy was started against that reading.

## Cross-review

I read Codex's `HumanReport29.md` and his Round-3 verification in full, reproduced his probe against the unchanged candidate before touching anything, and accepted his finding without dispute. I also read and answered his method observations in the three-way chat.

## Files created or updated

**Created**
- `Review Cards/RC-003 Archive-Reading Drift Command, Bounded-Read Repair.md`
- `chats/Claude-Codex/Bounded Archive Read Review/Bounded Archive Read Review - Active.md`
- `chats/Claude-Codex/Archive-Reading Drift Command Review/Summary.md`
- `agents/Claude/Session Summaries/HumanReport30.md`

**Updated**
- `Reproducibility Packet/scripts/utils/archive_units.py` — the preflight move, the cap, `_stored_value_bytes`, `_capped`, and the module docstring's statement of the rule
- `Reproducibility Packet/scripts/measure_host_drift.py` — the ceiling's stated scope, in the docstring and in `--max-mib`'s help
- `agents/Claude/tools/test_measure_host_drift.py` — the whole-suite invariant, touched-range recording, and the two new cases
- `agents/Claude/tools/mutate_rc002_repairs.py` — three new mutations and the coverage paragraph
- `Review Cards/RC-002 Archive-Reading Drift Command.md` — Claude's statement, the terminal disposition, the closed status and outcome
- `Review Cards/README.md` — RC-002's terminal row, RC-003's new row
- `chats/Claude-Codex/Archive-Reading Drift Command Review/…` — the convergence statement, then renamed to `- Concluded.md`
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — three method observations
- `README.md` (root) — one running-log entry
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`

## Next steps

1. **RC-003 Round 1 is open on Codex.** Nothing is open on me.
2. **If RC-003 closes `Approved`, the next work is the first real candidate measurement** — rank 1, CSHL047 Probe01, session `b52182e7-…`, `--gate strict`, run `--plan-only` first and compare `peak_resident_bytes` against a *freshly measured* free-RAM figure. Until then, **do not read a candidate**.
3. **If it does not close approved, clause 5 binds:** no second like-for-like successor. The work is split or redesigned, with the changed boundary named.
4. Still outstanding and unchanged: the capacity gate under Amendment 6, the five packet steps not yet re-run, and the preprocessing half of the amplitude question.

## Boundary

**No archive, network or candidate asset was read. No host is pinned, no candidate has been measured, no donor is selected, no generator has run, no sorter has run, and no scientific result exists.** Every fixture in this session was local and synthetic. Nothing is blocked on Randy.
