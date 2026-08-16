# Human Report 31 — Claude

**Written 2026-08-15 22:45 PDT** (clock read at the moment of writing, not estimated)
**Session:** Claude Session 31 · **Phase:** 2 — Execution
**No progress report is due this session.** The count-based trigger is every eighth session and the next is Session 32. No phase transition closed and no Claim Sheet amendment was approved here, so neither event trigger fired either.

---

## In one paragraph

Codex returned RC-003 Round 1 with three blocking findings. I reproduced all three with his own probe before editing anything, accepted all three in full, and repaired them: conversion provenance is now *authenticated* rather than recorded, on both halves of the recording; an acquisition stream is matched to its probe by decomposing the name rather than by substring; and a provenance value whose size the file will not state in advance is now **refused at the request** rather than measured after the bytes have moved. That last one is the distinction Codex named and I had missed — moving a read earlier made its cost *accounted*, not *refusable*. Two further things came out of asking whether a check could ever fire: a safety limit I had concluded was dead code turns out to be the only bound left when the file library serves a cached value for sixteen bytes, and a fixture I rewrote at a now-legal size had silently removed an unrelated sabotage check's grip while the suite stayed green. Evidence on the exact response state: **325 checks 0 failed, 20 of 20 repair mutations, 18 of 18 checker mutations**, all carried probes unchanged. RC-003 Round 2 is with Codex. **No archive, network resource or candidate asset was read; no host is pinned; no scientific result exists.**

---

## What I found on arrival

`.agent-turn` named Claude and no `.agent-session.lock` existed, so I created the lock, re-read the turn, and began. The state I inherited:

- **RC-003 was open on Codex, Round 1**, a full seven-file pass over the candidate that RC-002 had frozen unapproved.
- He returned it as **`Revisions Required` with three blockers**, plus an explicit acceptance that the successor's scope had *not* been narrowed — which was the specific thing I had invited him to attack last session.
- His positive evidence reproduced everything I had reported: 279 owner checks, both mutation harnesses green, all carried probes at their expected outputs.

Everything else was concluded. The `Review Method Change` chat stays active by design.

## The three findings, and what I did about each

### RC-003-F1 — provenance was recorded and never authenticated

**The finding.** §16.4 of the selection document says an asset whose conversion provenance and values do not establish the common session clock is an *input error to resolve*, not a drift rejection. The command recorded provenance and gated on none of it, so a schema-valid processed file carrying no statement at all of what produced it reached `passed=True` with an empty provenance record. That is a malformed input becoming a verdict, which is the card's stated purpose inverted.

**The repair.** `general/source_script` must now be present, must have been read whole, and must contain a pinned conversion-toolchain token. A failure raises before any statistic is computed and is reported as an input error, so the pinned order pauses rather than advancing past a candidate that never failed on drift.

**I extended it to the raw asset.** The raw file supplies the grid's extent and the processed file supplies the spikes; the clock claim is that *both* exports share one session-time coordinate, so authenticating one half would leave the claim resting on the unauthenticated one. That cost one more bounded read of the raw asset, reported as `raw_provenance` beside the other three.

**What the rule is checked against — and this is the part I want on the record.** Session 7 read `/general` from one raw NWB per subject across 21 assets of DANDI 000409 and found `general/source_script` on every one, reading `Created using NeuroConv v0.9.2` on twenty and `v0.9.1` on the twenty-first (`Reproducibility Packet/results/subject_provenance.json`). So the token is checked against a measurement this project already holds, not against a guess. **The pinned commit of the conversion repository is not checked, because no asset in that survey carries it** — and the report says so in the same place it reports the check, rather than letting the line imply that the commit was confirmed.

Two limits I declared rather than left implicit: those 21 measured assets are **raw**, so extending the requirement to the processed asset rests on both halves coming off one conversion rather than on a measurement of a processed asset; and the token comparison is case-insensitive, because rejecting a differently-capitalised spelling of the same toolchain would be a rejection on typography. I told Codex these are the two parts of the repair I most want him to attack.

### RC-003-F2 — probe ownership was a substring match

**The finding.** `select_ap_series` used `probe in entry["name"]`. Asked for `Probe00`, a file carrying `ElectricalSeriesProbe000AP` and `ElectricalSeriesProbe01AP` selected the first and reached a passing verdict on a clock belonging to a different probe.

**The repair.** The name is decomposed as `ElectricalSeries<probe><AP|LF>` and the probe token must equal the requested probe exactly. `ElectricalSeriesProbe000AP` yields `Probe000` and no longer answers.

**Why I could check the tightening rather than guess at it.** The thirteen candidates in the pinned order carry exactly two series names between them — `ElectricalSeriesProbe00AP` and `ElectricalSeriesProbe01AP` — recorded in `results/host_timing_index.jsonl` from an earlier session. So the decomposition is verified against every asset the pinned order can reach, which is the difference between a rule and a hopeful pattern.

**What it does not do, written beside it in the code.** It authenticates the *name*. A stream labelled for this probe but carrying another's channels is not caught, and closing that would mean resolving each series' electrode region inside a script outside this card that has already produced a recorded index. I also declared a branch that can no longer fire: with an exact decomposition, two matches cannot arise from one HDF5 group, so the `!= 1` form is a guard and the live failure is zero.

### RC-003-F3 — accounted is not refused

**The finding, and it is the one I had genuinely got wrong.** RC-002 closed because a provenance read happened *after* the memory ceiling was enforced. I repaired that by moving the read into preflight, where its cost lands inside the plan. Codex's Round 1 showed that this makes the spend **visible** without making it **preventable**: with a two-million-character value and a one-byte ceiling, `2,028,208 distinct bytes are touched before the promised refusal`. The plan honestly reports a spend that has already happened.

**The repair.** HDF5 will not state a variable-length string's size in advance — its characters live in the global heap and the dataset stores 16 bytes of references. But h5py asks *this project's own reader* for the heap collection's bytes before they move. So a `BoundedReader` now sits above the range reader and checks the requested length against a pinned per-path budget, raising instead of delegating. On Codex's own construction: **33,456 distinct bytes against his 2,028,208**, and the smaller figure includes the electrode table, the unit scalars and the descriptions, not only the refused read.

## Two things that came from asking whether a check could fire

**The first saved a check I was about to delete.** After the budget was in, the older retention cap looked unreachable: nothing oversized can arrive to be capped if the read is refused first. Before deleting it I built the case that would reach it — and it exists. The budget bounds what h5py asks *the reader* for; it does not bound what HDF5 hands back from its own cache. After one read of a 2,000,000-character value, a second read costs **sixteen bytes** through the reader, so a 1,000-byte budget does not refuse it and the retention cap is the only bound left. That is not reachable through this command's own call sequence, but a bound that holds only because of a layout accident is not a bound. There is now a case for it.

**The second was a regression I created and caught.** Repairing F3 meant rewriting an existing test case at a size the budget admits — legitimate, because the old 4.2 MB fixture is now refused. That silently removed the whole-suite invariant's ability to detect mutation `F1d`, which had been catching it since RC-002: at 32 KB under 1 MiB blocks, one block covers the whole fixture, so the invariant's comparison is true whatever the plan says about preflight spend. **Nothing in the acceptance suite said so.** It was green at 321 checks and nineteen of twenty mutations were still caught. The only reason I know is that I re-ran the mutation harness after the repair instead of trusting the green suite. The case now runs at 4 KiB blocks and `F1d` is caught by the invariant again.

## One defect the read-back pass caught

Rendering the report and reading it as a reader — the habit that has produced the last correction in twelve consecutive sessions — found that provenance keys were clipped to nine characters, so `general/source_script` and `general/source_script@file_name` both printed as `source_sc` and two different values sat under one label. Keys are printed whole now and a case requires each of four to appear by its full name.

## What I told Codex about his own probe

`probe_rc003_round1.py` no longer runs to completion, and both reasons are the repair rather than a disagreement. Its first construction built a provenance-free processed asset by omitting the harness's `provenance` argument, and that default is now a valid mapping — a fixture that omits provenance must do so deliberately. Its second calls `select_ap_series` directly on an impostor name, which is now a `SystemExit` rather than a return value, so the probe raises there and its temporary-directory cleanup fails behind it on Windows. Rather than leave him to work that out, I wrote `agents/Claude/tools/verify_rc003_round1_repairs.py`, which rebuilds all three constructions **explicitly** with every fixture written in the script, and requires each to be refused. It is response-created, declared in the card, and is not a replacement for his re-pin.

`probe_rc002_round3.py` also changed behaviour and I reported it precisely rather than by its old expected wording: its 4.2 MB fixture is now refused during preflight, so the probe raises the reader's `ValueError` before a plan exists to test. Exit 1, but no longer by its own assertions.

## Evidence, on the exact response state

| Test | Result |
|---|---|
| `test_measure_host_drift.py` | **325 checks, 0 failed, 13.3 s** (279 at Round 1; 46 new) |
| `mutate_rc002_repairs.py --repo-root .` | **20 of 20, control green at 325** (16 of 16 at Round 1) |
| `mutation_test_runbook_checker.py` | **18 of 18, control green** |
| `check_runbook_consistency.py` | 10 steps agree, 1 script pending a step |
| `verify_rc003_round1_repairs.py --repo-root .` | all three Round-1 constructions refused; F3 at 33,456 bytes |
| `test_band_drift.py` | 103 checks, 0 failed |
| `probe_band_drift_claims.py` | 3 of 3 |
| `probe_rc001_round1.py --repo-root .` | 0 failures |
| `probe_draft16_safety_claims.py --repo-root .` | digits unchanged |
| `probe_rc002_round3.py --repo-root .` | exit 1, refused during preflight |
| Compilation | clean on four changed files and the new one |
| Console safety | `--help` on all three scripts that have one: 7,390 / 3,521 / 1,646 bytes, zero non-ASCII |

**One honesty note about that table.** I edited the mutation harness's own docstring *after* its first run had started, which meant the reported evidence no longer matched the file's hash. Rather than explain the mismatch I re-ran it against the exact final state; the 20-of-20 figure above is from that second run.

## Machine state, measured rather than inherited

- **2026-08-15 22:2x PDT, before the first heavy step:** **18,522 MiB available physical RAM, 42% memory load**, 108,426 of 130,415 MB pagefile available. Everything this session runs is synthetic and small — the largest fixture is about 2 MB — so nothing came close to the guards.
- The two mutation harnesses were run one at a time in the background, ~4-5 minutes each, with their output collected from a file rather than a foreground timeout.
- **A housekeeping defect found at closeout and deliberately not repaired.** The acceptance suite removes its fixture directory with `ignore_errors=True`, and on Windows that silently fails whenever an h5py handle is still open. **111 leftover `drift_reader_*` directories had accumulated in the system temp folder across sessions.** I deleted them and wrote the fix into the continuity file rather than applying it: the harness is a file I had just published digests for and told Codex I approve, and changing it after that handoff would make the evidence describe a state that no longer exists. It is a five-line fix for the session after RC-003 closes.
- **Do not inherit these numbers.** Take your own immediately before any heavy step.

## Files created or updated

**Changed (the RC-003 Round 2 response state):**
- `Reproducibility Packet/scripts/utils/archive_units.py` — `787d53ab87069280583f3c4ec0264eb686033535402368d5f2bddfeec0a0d814`
- `Reproducibility Packet/scripts/measure_host_drift.py` — `1941c577b79a7e1d22ab8e25ff41791d1b2852050c980526b6685340bae67ae5`
- `agents/Claude/tools/test_measure_host_drift.py` — `326314a530355c27b3689919acaa9c7497b7605fa7e0de22d26212afe0b79aee`
- `agents/Claude/tools/mutate_rc002_repairs.py` — `1e5cffcd6856da215a197528bc66ba62b64d1546d276dcf5d291310bb765525d`

**Created:**
- `agents/Claude/tools/verify_rc003_round1_repairs.py` — `43402d14245965bfa42d47be1c54a4d80c57b4532e7e677f60e4bfccf20a648c`
- `agents/Claude/Session Summaries/HumanReport31.md` — this file

**Updated (documentation and record):**
- `Review Cards/RC-003 Archive-Reading Drift Command, Bounded-Read Repair.md` — Round 2 response state, round log, owner response and evidence
- `Review Cards/README.md` — RC-003's index row
- `chats/Claude-Codex/Bounded Archive Read Review/Bounded Archive Read Review - Active.md` — the Round 2 response, appended
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — three method observations, appended
- `README.md` — one running-log entry, inside the log section (60 dated entries by my own count; the previous session recorded 58 by a slightly different counting method, and I have not reconciled the two because nothing depends on the number)
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — closeout

**Unchanged and still approved:** both Claim Sheets, the selection document, `band_drift.py`, `test_band_drift.py`, the Study Guide, the packet README and the runbook checker.

## What is still not done

1. **No host is pinned and no candidate has been measured.** Candidate access stays blocked until RC-003 closes `Approved`.
2. **The capacity / ten-placement gate** is still not discharged under Amendment 6's stricter condition. It is Codex's calibration and belongs in a future section.
3. **Five of the ten packet steps** — the archive-reading ones — still have not been re-run.
4. **The preprocessing half of the amplitude question** is untouched; it is Rung 0 territory.
5. **The 66 unmapped host long names** remain an ontology/licence question rather than a coding one.

## Next steps

- **Codex owns RC-003 Round 2**, delta-only over the three repairs, the response-created verification script and the report's key rendering.
- If it closes `Approved`, the next work is the **first real candidate measurement** — rank 1, CSHL047 Probe01, session `b52182e7`, `--gate strict`, with `--plan-only` run first and free RAM measured against `peak_resident_bytes`.
- If it does not, **clause 5 binds**: no second like-for-like successor, and the work is split or redesigned with the changed boundary named.
