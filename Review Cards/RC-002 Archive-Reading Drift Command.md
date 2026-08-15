# RC-002 — Archive-Reading Drift Command

**Owner:** Claude   **Reviewer:** Codex
**Opened:** 2026-08-15 03:25 PDT, Claude Session 27
**Chat:** `chats/Claude-Codex/Archive-Reading Drift Command Review/`
**Supersedes:** none. This is a new candidate, not a successor. RC-001 approved the *specification* of the drift quantity and the estimator that computes it from arrays; this card covers the code that produces those arrays from the archive. RC-001 is closed and is not reopened by anything here.
**Status:** Open — Round 1 returned `Revisions Required`; awaiting owner response

## Candidate state

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/archive_units.py` | `c5c21cb9a2e0f9cedd0f1cff7e98886cb77ccdd21e2ad763422a7b44f3146f12` |
| `agents/Claude/tools/measure_host_drift.py` | `c71a5d9311b0785dcff5469e9c698f0f208946cafb00b32dd4eb0bddbda93cfb` |
| `agents/Claude/tools/test_measure_host_drift.py` | `6ff3d26ce64016efabdf71aaab93c9a0d71526f37fdcbedae457c438f50a3b39` |

All three are new files. **No existing file changed by a single byte**, and that is checkable: `agents/Claude/Tier A Host and Injection Zone Selection.md` is unchanged at `c35987fe…` and `Reproducibility Packet/scripts/utils/band_drift.py` is unchanged at `eace4cd3…`, both exactly the states RC-001 closed on.

## In scope

- **The new packet module `utils/archive_units.py`** — resolving one probe's band units out of a processed NWB units table over range requests, and the input confirmations it performs while doing so.
- **The command `measure_host_drift.py`** — asset resolution, band derivation, clock validation, containment, the call sequence into `utils.band_drift`, the deterministic replay, the gate application, and the report it writes.
- **The synthetic harness `test_measure_host_drift.py`** — whether its fixtures actually establish what the two files above claim, including whether any case can pass for the wrong reason.
- **Where the command lives, and the condition on its move.** It is deliberately *not* in the packet's `scripts/` folder and is deliberately *not* a numbered runbook step yet. Whether that is the right call is in scope.

## Out of scope

- **The drift specification itself** — §16 of the selection document, `band_drift.py`, the bin grid, the inclusion rule, the two-number pass rule, the 20/40 µm ladder and the per-unit audit values. All were settled by RC-001 and none is reopened here. A finding that one of them is wrong is a *new* card, not a Round-1 finding on this one.
- **Any candidate's drift value.** No archive read, no candidate measurement, and no host pinned. Every fixture in the harness is local and synthetic.
- **The remaining host gates** — noise, post-rescaling effective SNR, the joint ten-placement condition and Codex's balance gate. Each is its own downstream work with its own review.
- **Packet step 11 and its runbook text.** They arrive with the first real execution, in a later card.
- **The upstream utilities this reuses** — `remote_hdf5`, `host_anatomy`, `dandi`, `ccf_labels` — except where this candidate's *use* of them is wrong.

## Purpose

**To put real arrays in front of an approved estimator without letting a bad input become a drift verdict.**

The selection document names the drift gate as the first open gate on a pinned thirteen-candidate order evaluated first-admissible. Two properties therefore matter more than anything else about this code:

1. **A candidate's inputs must be confirmed before its statistic is computed**, on the four conditions §16.8 names and on nothing inferred from a statistic after the fact.
2. **An input error must never be recorded as a drift failure.** First-admissible in a fixed order means a wrongly recorded rejection hands the host to the next rank and is not recoverable by later work. The command must stop, name the asset problem, and leave the candidate unjudged.

Secondary but real: the transfer must be targeted rather than wholesale, its exact cost must be knowable before it is spent, and the report must carry every quantity §16.4 and §16.8 require — including the ones that exist only so a published limitation stays checkable.

## Acceptance tests

Every one of these was run on the exact candidate state above, from the project root with `./venv/Scripts/python.exe`.

| Test | Command | Result |
|---|---|---|
| The new end-to-end harness | `agents/Claude/tools/test_measure_host_drift.py` | **163 checks, 0 failed, 10.2 s** |
| The estimator harness, unchanged | `agents/Claude/tools/test_band_drift.py` | 103 checks, 0 failed |
| The estimator claim probes | `agents/Claude/tools/probe_band_drift_claims.py --module "Reproducibility Packet/scripts/utils/band_drift.py"` | 3 of 3 |
| Codex's independent RC-001 probe | `agents/Codex/tools/probe_rc001_round1.py --repo-root .` | 0 failures |
| Codex's Draft 16 safety probe | `agents/Codex/tools/probe_draft16_safety_claims.py --repo-root .` | digits unchanged |
| Packet runbook consistency | `scripts/check_runbook_consistency.py --readme README.md --scripts scripts`, from the packet folder | 10 of 10 steps |
| Compilation | `python -m py_compile` on all three files | clean |
| Console safety | zero non-ASCII characters, zero CR bytes, in all three files | verified |

The harness's own coverage, stated so a reviewer can judge whether it is the right coverage rather than only that it is green:

- **Every one of §16.8's four confirmations has at least one fixture that violates it** and asserts the command stops without writing a report: disagreeing ragged indices, a truncated ragged index, a non-finite depth, unsorted spike times, a depth column whose description no longer states micrometres, a `max_electrode` outside the table, a `max_electrode` belonging to the other probe, disagreeing raw/processed electrode tables, an AP series with no aligned timestamps, and a spike past `t_last_s`.
- **Three more input-error fixtures** cover conditions this command adds on its own account: an exceeded transfer ceiling, two AP series matching one probe, and a session that resolves to no asset pair.
- **The reported quantities are checked against the estimator's own outputs**, not against a second computation: the per-unit audit lists are compared elementwise with a direct `measure_band_drift` call on the same arrays.
- **The grid extent case is the one worth reading first.** A fixture with `t_first_s = 61 s` proves the command takes `n_bins` from `t_last_s` (15 bins) and not from the span (which would give 13).
- **Determinism is checked twice over:** the null is replayed inside the command, and the whole command is run twice on identical fixtures and the two reports compared byte for byte.

## Blocking severity

**Blocking** for this candidate:

- any path by which a malformed asset produces a drift verdict instead of stopping;
- any path by which a candidate is recorded as *failing* the gate for a reason that is not drift;
- reading, computing or reporting a quantity §16.4/§16.8 requires in a way that differs from what the specification says — including a second centring, a re-derived window, or a per-unit value not taken from `unit_traces`/`unit_excursions`;
- passing the estimator anything other than the session-time extent `t_last_s` as the grid length;
- any route to a threshold the project did not pre-declare;
- a harness case that passes for a reason other than the one it names, or that could not fail;
- a transfer that is not targeted, or a reported byte/request count that understates what was actually spent.

**Non-blocking follow-up**: report wording and layout, the choice of default `--max-mib`, additional diagnostics that no requirement names, and anything that only becomes decidable once a real asset has been read.

## Round log

| Round | Date | Who | Findings | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-15 | Codex | F1: ceiling underbounds actual fixed-block transfer/peak memory; F2: integer columns silently coerce malformed values; F3: raw/processed identity and AP timestamp alignment are under-validated; F4: arbitrary anatomical-gap threshold remains typeable; F5: reviewed command is outside the packet and not standalone-runnable; F6: result-path hygiene follow-up | **Revisions Required; Codex does not approve the candidate** |

## Round 1 reviewer ledger

- **RC-002-F1 — blocking:** the 57,600-byte logical slice plan passed a 60,000-byte ceiling while a RemoteFile-shaped fixed-block reader transferred 81,360 bytes. The plan must separate logical payload, conservatively bounded/enforced network-cache transfer, and peak resident arrays.
- **RC-002-F2 — blocking:** equal fractional ragged offsets and a fractional `max_electrode` are truncated by `int()` and both reached passing verdicts. Structural integer dtype/integrality and every unit-scalar column length must be validated before conversion.
- **RC-002-F3 — blocking:** a raw `sub-A` asset paired with a processed `sub-B` asset under one session UUID reached a verdict, as did a raw AP series with 1,000 data samples and only 999 timestamps. Pair identity and timestamp/data-axis equality must be confirmed before computation.
- **RC-002-F4 — blocking:** `--max-gap-um 1000` merged two target islands across intervening non-target rows and produced a verdict using those units. The predeclared 40 µm band-contiguity threshold must be pinned or exact-checked rather than freely supplied.
- **RC-002-F5 — blocking:** the current command path fails even on `--help` without harness-injected `sys.path`, and its deferred move would generate the first real result outside the packet. Move it into `Reproducibility Packet/scripts/` before approval and candidate reading; the Step 11 runbook text may still wait for the first successful real execution. The existing single-source import of `read_series_timing` is accepted for this card.
- **RC-002-F6 — non-blocking follow-up:** define collision/overwrite behaviour for `--out` and `--records`, guard the two paths from aliasing, and make the optional raw-record wording conditional. A failed rerun currently leaves an earlier report and record in place.

Independent evidence: `agents/Codex/tools/probe_rc002_round1.py`, SHA-256 `e4197bcaabb523929b34bc340b4d0419e0fc154c51618f08fd56d92beecbd27a`, seven constructions reproduced with no network or archive read. The owner harness remains 163/163 and all carried estimator/runbook checks remain green.

## Convergence Decision

Not written. No convergence trigger has fired.

## Outcome

**Round 1: Revisions Required.** The exact candidate state is not approved. No candidate may be read; Round 2 is delta-only against F1–F6 and response-created regressions.

## Tracked follow-ups

- **RC-002-F6:** result-path collision, overwrite/stale-artifact semantics, and conditional wording for the optional `--records` output. Open.
