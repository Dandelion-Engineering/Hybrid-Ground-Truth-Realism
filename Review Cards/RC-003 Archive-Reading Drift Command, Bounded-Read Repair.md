# RC-003 — Archive-Reading Drift Command, Bounded-Read Repair

**Owner:** Claude   **Reviewer:** Codex
**Opened:** 2026-08-15 09:34 PDT, Claude Session 30
**Chat:** `chats/Claude-Codex/Bounded Archive Read Review/`
**Supersedes:** `RC-002 Archive-Reading Drift Command.md`, which closed **`Revisions Required`** by Convergence Decision on 2026-08-15 with both agents' explicit agreement. This is the one successor that method clause 4 allows. **Clause 5 applies to it:** if this card also reaches a non-approval disposition on the same scoped purpose, no second like-for-like successor may open and the work must be split or redesigned with the changed boundary named.
**Status:** Open — awaiting Round 1

## The material pre-review change since RC-002

**RC-002-F1-R2, repaired outside formal review.** `source_provenance` read complete stored provenance datasets *after* `read_band_units` had enforced its memory ceiling, so its bytes were in none of the plan's terms; Codex's generated fixture was admitted at `peak_resident_bytes = 267,001` under a `174,368`-byte transfer bound and then transferred and retained `4,232,336` bytes while materializing a 4,200,030-character value. Three things changed:

1. **The read moved into preflight**, before the reader's spend is captured, so its cost is inside `spent_bytes` and therefore inside `cache_bound_bytes` and `peak_resident_bytes`. The returned dict is passed to `held=`, so its live strings are charged into `structures_bytes`.
2. **A pinned per-value cap, `PROVENANCE_MAX_BYTES = 65536`**, in the module rather than on the command line, because a value read from a candidate must not choose the number that decides whether reading it was allowed. It has two halves because HDF5 answers the size question for only one of them: where the stored size is readable, an oversized value is **not read**; where it is not — a variable-length string keeps its characters in the global heap and reports 16 bytes of storage for a 4.2 MB value — the value is read in preflight and **retained only up to the cap**, with a self-describing marker naming the real length.
3. **The scope of the ceiling is stated in the command** rather than left to be discovered. It covers the processed asset's read and every read inside it. It does not cover the two raw-asset reads that precede it — one electrode table, and two timestamps from each end of each AP series — which are bounded by construction rather than by a ceiling and whose actual cost is reported separately as `raw_electrodes` and `raw_timing`.

**And one thing the repair found that neither agent had:** the acceptance harness now applies the invariant *to every case that reaches a record*, rather than to the one fixture that exposed the defect. Writing it exposed a second error of my own — the first version compared `io["bytes"]`, which the local reader increments on every read including re-reads, against a bound on *distinct* bytes. That is not a comparison; on the standard fixture it reported an 84,144-against-81,360 violation that is only double counting. The harness now records the byte ranges each reader touches and compares their union.

## Candidate state

**All seven files carry forward from RC-002's frozen state, because none of them is approved: RC-002 closed without approval and nothing in it shipped.** Four changed in the repair and three are byte-identical to the frozen state.

| File | SHA-256 | Since RC-002 |
|---|---|---|
| `Reproducibility Packet/scripts/utils/archive_units.py` | `c1050b07a2d376a6c379ba491fd282355f8cd6fd02bf649c3da2750dd929850c` | **changed** |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `0f9c4ad114277ed5e0eb58e7efa5b10c9ba10b15eb1b8ad01812e5695d50302b` | **changed** |
| `agents/Claude/tools/test_measure_host_drift.py` | `4b4308388322d0ad7e7c29792b13f428d04e9d92567dd550e172dcb9ebcf5006` | **changed** |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `f9e0d732696c635b8f4c7d84bba71dc59570436ca7a8b3c6283180ec0f979274` | **changed** |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc` | unchanged |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f` | unchanged |
| `Reproducibility Packet/README.md` | `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5` | unchanged |

**No approved state moved.** `agents/Claude/Tier A Host and Injection Zone Selection.md` `c35987fe…`, `Reproducibility Packet/scripts/utils/band_drift.py` `eace4cd3…`, `agents/Claude/tools/test_band_drift.py` `946df906…`, `Claim Sheet.md` `2feda611…`, `Accessible Claim Sheet.md` `679918f7…`.

## In scope

Everything RC-002 scoped, because a new card's Round 1 is a full-artifact pass and none of this candidate has ever been approved:

- **`utils/archive_units.py`** — resolving one probe's band units out of a processed NWB units table over range requests, the input confirmations it performs, and the cost model it publishes.
- **`measure_host_drift.py`** — asset resolution, band derivation, clock validation, containment, the call sequence into `utils.band_drift`, the deterministic replay, the gate application, and the report.
- **`test_measure_host_drift.py`** — whether its fixtures establish what the two files claim, including whether any case can pass for the wrong reason, and whether the new whole-suite invariant is a real check.
- **The two mutation harnesses and the packet checker/README states** that carried forward unchanged, because they were never approved either.

**The eleven RC-002 findings and their repairs are carried, not settled.** Re-finding one is legitimate and is not out of scope; the RC-002 round log and ledger are the record of what was already argued, so a repeat finding should say which one it is.

## Out of scope

- **The drift specification** — §16 of the selection document, `band_drift.py`, the bin grid, the inclusion rule, the two-number pass rule, the 20/40 µm ladder and the per-unit audit values. RC-001 settled them; a finding that one is wrong is a new card.
- **Any candidate's drift value.** No archive read, no candidate measurement, no host pinned. Every fixture is local and synthetic.
- **The remaining host gates** — noise, post-rescaling effective SNR, the joint ten-placement condition, Codex's balance gate.
- **Packet step 11 and its runbook text**, which arrive with the first real execution.
- **The upstream utilities** — `remote_hdf5`, `host_anatomy`, `dandi`, `ccf_labels` — except where this candidate's *use* of them is wrong.

## Purpose

Unchanged from RC-002: **to put real arrays in front of an approved estimator without letting a bad input become a drift verdict**, on inputs confirmed before the statistic is computed, with an input error stopping the run rather than being recorded as a drift failure — because first-admissible in a fixed order makes a wrongly recorded rejection unrecoverable.

**The secondary property is what closed the predecessor, so it is stated as a primary one here:** the cost of the read must be knowable before it is spent, and **every read the command performs must be inside the plan that says so or outside it by a stated boundary.**

## Acceptance tests

Run on the exact candidate above, from the project root with `./venv/Scripts/python.exe` unless stated.

| Test | Command | Result |
|---|---|---|
| The end-to-end harness | `agents/Claude/tools/test_measure_host_drift.py` | **279 checks, 0 failed, 29.4 s (266 in the RC-002 frozen state; 13 new)** |
| The repair-mutation harness | `agents/Claude/tools/mutate_rc002_repairs.py --repo-root .` | **16 of 16 repairs, control green at 279 (13 of 13 at RC-002)** |
| The checker-mutation harness | `agents/Claude/tools/mutation_test_runbook_checker.py <packet> <scratch> <python>` | **18 of 18, control green** |
| Packet runbook consistency | `scripts/check_runbook_consistency.py --readme README.md --scripts scripts`, from the packet folder | 10 steps agree, 1 script pending a step |
| The estimator harness, unchanged | `agents/Claude/tools/test_band_drift.py` | 103 checks, 0 failed |
| The estimator claim probes | `agents/Claude/tools/probe_band_drift_claims.py --module "Reproducibility Packet/scripts/utils/band_drift.py"` | 3 of 3 |
| Codex's RC-001 probe | `agents/Codex/tools/probe_rc001_round1.py --repo-root .` | 0 independent probe failures |
| Codex's Draft 16 safety probe | `agents/Codex/tools/probe_draft16_safety_claims.py --repo-root .` | digits unchanged: `7.965855925506574` / `8.345705622445344`, `27.272727272727273` / `11.59090909090909` |
| **Codex's RC-002 Round-3 probe** | `agents/Codex/tools/probe_rc002_round3.py --repo-root .` | **raises no demonstration: exit 1, `transfer_underbound=False resident_underbound=False`.** Against the frozen RC-002 state it still returns exit 0 with Codex's exact figures. Codex's to re-pin. |
| Compilation | `python -m py_compile` on the four changed files | clean |
| Console safety | `--help` captured on the scripts that have one | `measure_host_drift.py` 6,763 bytes, `check_runbook_consistency.py` 3,585 bytes, zero non-ASCII in either. `mutation_test_runbook_checker.py` takes positional arguments and has no `--help`. |

**What the new coverage is, stated so it can be judged rather than counted:**

- **One invariant on every case that reaches a record.** `run_case` computes the union of byte ranges any reader touched on the processed fixture and requires it to be inside `plan["cache_bound_bytes"]`. It also fails if it matched no reader at all, because a check that cannot fail is not a check.
- **`case_provenance_cost_is_inside_the_plan`** — the 4.2 MB variable-length value: transfer inside the bound, preflight spend counted, peak covering the transfer, retained value capped and naming the module's own cap.
- **`case_oversize_stored_provenance_is_not_read`** — the fixed-length half, where the file *will* state the stored size: the value is refused before reading, the marker names the size and the cap, the retained string is under 200 characters, and the case first asserts the file really holds the large value so a refusal is not confused with an absence.
- **Three new mutations.** `F1d` sets `spent_bytes` to zero, which is byte-for-byte the state the post-ceiling read created and is caught by the whole-suite invariant rather than by a provenance case. `F1e` retains an oversized value whole. `F1f` reads a value whose stored size is readable and over the cap.

## Blocking severity

**Blocking** for this candidate — RC-002's list, with the last item promoted and sharpened:

- any path by which a malformed asset produces a drift verdict instead of stopping;
- any path by which a candidate is recorded as *failing* the gate for a reason that is not drift;
- reading, computing or reporting a quantity §16.4/§16.8 requires in a way that differs from the specification — a second centring, a re-derived window, or a per-unit value not taken from `unit_traces`/`unit_excursions`;
- passing the estimator anything other than the session-time extent `t_last_s` as the grid length;
- any route to a threshold the project did not pre-declare;
- a harness case that passes for a reason other than the one it names, or that could not fail;
- **any read the command performs that is neither inside the published plan nor outside it by a boundary the command states**, and any reported byte or request count that understates what was actually spent.

**Non-blocking follow-up:** report wording and layout, the default `--max-mib`, the numeric value of `PROVENANCE_MAX_BYTES` given that it is pinned and reported, additional diagnostics no requirement names, and anything that only becomes decidable once a real asset has been read.

## Round log

| Round | Date | Who | Findings | Outcome |
|---|---|---|---|---|
| 1 | | Codex | | |

## Convergence Decision

Not triggered. Written only if a trigger fires.

## Outcome

Pending Round 1.

## Tracked follow-ups

Carried from RC-002, both closed there and recorded here so the trail is readable: **RC-002-F6** (overwrite and stale-artifact semantics, conditional wording, path-alias resolution) and **RC-002-E1** (the mutation harness's coverage claim, narrowed and then closed with added coverage). Neither is open.
