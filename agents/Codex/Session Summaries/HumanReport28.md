# Human Report — Codex Session 28

**Date:** 2026-08-15

**Closeout time:** 06:30 PDT

**Phase:** 2 — Execution

**Review outcome:** RC-002 Round 2 — **Revisions Required**

## Executive summary

I performed the delta-only Round-2 review of Claude's response to RC-002, the archive-reading drift command. I authenticated the exact six-file response state, reran the owner's 231-check suite, both mutation harnesses, every carried estimator/probe check, direct command startup and compilation. F3, F4 and F5 are repaired, and most of F6 now behaves correctly. The response is still not approvable.

Three blocking defects remain. A valid fragmented HDF5 layout defeats the claimed fixed-block transfer upper bound; the retained block cache and converted arrays coexist even though the ceiling checks their sizes separately; and floating-point ragged index storage remains invalid under the NWB/HDMF schema even when every value is whole. I also recorded two nonblocking items: case-only output aliases evade the Windows path guard, and the mutation-evidence description claims F5 coverage that the mutation list does not contain.

No archive, candidate, or network data was read; no host was selected; no result file was produced. Claude owns the final Round-3 owner response. Candidate measurement remains blocked.

## Exact candidate reviewed

- `Reproducibility Packet/scripts/utils/archive_units.py` — SHA-256 `19dbcc765cd5a64b41d370c642c318055cfe619cd5d4beb40dc0b69ccac132ea`
- `Reproducibility Packet/scripts/measure_host_drift.py` — SHA-256 `7f99419ee202dd189d9f7a96d36d6d73c31723b5da21ee34cbe889d80c8ca2d5`
- `agents/Claude/tools/test_measure_host_drift.py` — SHA-256 `ad4985cb83eaa6be135d4e0db88785cfb4aeeb20cd4de03c131aae1c81d5a798`
- `agents/Claude/tools/mutate_rc002_repairs.py` — SHA-256 `89785076ffb4856264b761d523a2b897341bc2024b63fa7803bcb4bf4e6f1b12`
- `Reproducibility Packet/scripts/check_runbook_consistency.py` — SHA-256 `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f`
- `Reproducibility Packet/README.md` — SHA-256 `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5`

I did not edit any candidate file.

## Positive evidence preserved

- Owner archive-command harness: **231 checks, 0 failed** in 14.8 seconds.
- Repair-mutation harness: unmutated control green and all eight listed mutations caught.
- Packet runbook checker: ten numbered steps plus one explicitly pending script.
- Packet-checker mutation harness: green control and **15/15** mutations caught.
- Approved estimator harness: **103/103**.
- Estimator claim probes: **3/3**.
- Codex RC-001 probe: zero failures.
- Codex safety-probe outputs unchanged at `7.965…/8.345…` and `27.272…/11.590…`.
- Moved packet command runs directly with `--help` and no harness-injected import path.
- Python compilation passed.

The F3 asset-pair and AP-axis checks, F4 pinned 40 µm anatomy check, and F5 packet placement/standalone invocation all pass. The response-created `PENDING_STEP` declaration is explicit, validated and visible in checker output, so it is acceptable until the first real execution creates Step 11. F6's pre-run stale-output clearing and conditional raw-record wording also pass.

## Blocking findings

### F1-R1a — The chunk fallback is not an upper bound

The response computes the fallback cost of a multi-chunk HDF5 slice from the first selected chunk offset through the last and applies fixed-block alignment once. HDF5 does not require successive chunks to occupy one contiguous on-disk span.

I generated a valid local HDF5 fixture, replaced the two ragged columns with chunked datasets, and interleaved large unrelated allocated chunks between each successive ragged-column chunk. The plan reported `cache_bound_bytes = 241,664`; the same fixed-block reader used by the owner harness transferred `327,680` bytes. A deliberately intermediate `284,672`-byte ceiling was admitted, after which the read transferred `327,680` bytes. This directly violates the card's requirement that a planned transfer not understate actual work.

The final repair must enumerate actual per-chunk byte ranges and union their fixed blocks, or apply a genuinely conservative per-chunk bound. The fragmented fixture should become a permanent test.

### F1-R1b — The ceiling omits coexisting live memory

`RemoteFile` and the owner's fixed-block stand-in retain every fetched block until `read_band_units` returns. The returned float64 arrays accumulate during the same interval. The response reports and ceiling-checks `cache_bound_bytes` and `resident_bytes` separately, although both quantities are simultaneously live.

On the standard processed fixture, the function admitted a ceiling of `81,361` bytes. At return, `81,360` cached bytes coexisted with `57,600` bytes of returned float64 times/depths arrays: at least `138,960` live bytes before the other metadata, indexes and conversion temporaries are counted. Each separately checked number fits while their live sum does not.

The final repair needs one conservative combined peak-resident bound whose declared scope includes the block cache, returned arrays, structural metadata/indexes and relevant temporaries. The command must not call a partial array calculation exact process peak memory or compare that partial number with free RAM.

### F2-R1 — Whole-valued floating ragged indexes remain malformed

Claude explicitly asked whether accepting an exactly whole floating column was the right F2 boundary. For the ragged indexes, it is not. NWB defines `Units/spike_times_index` as an HDMF `VectorIndex`; the HDMF common schema specifies unsigned-integer storage for `VectorIndex`. An integrality check prevents lossy coercion but does not make a floating-point index schema-valid.

The final repair must require integer source dtype for `spike_times_index` and `spike_depths_index` before conversion. I did not extend the schema conclusion to the project-specific `max_electrode` column; the command may accept and report a whole-valued floating custom column if the owner deliberately keeps that compatibility choice.

The official NWB and HDMF specification links and their role in this decision are recorded in `agents/Codex/references.md`.

## Nonblocking follow-ups

### F6-R1 — Case-only output aliases on Windows

The repaired guard compares `os.path.abspath` strings. On the case-insensitive workspace filesystem, temporary paths ending in `Verdict.txt` and `verdict.txt` referred to the same file according to `os.path.samefile`, but argument parsing accepted them as distinct. Normalize case and real paths, and use `samefile` when both outputs exist, before first real execution. The normal documented output names differ, so this remains a follow-up rather than a measurement blocker.

### E1 — Mutation coverage wording exceeds the mutation list

The repair-mutation harness contains eight entries: F1; two F2 variants; two F3 variants; F4; and two F6 variants. It contains no F5 mutation even though the response says each finding's repair is removed. Direct F5 checks and the checker mutation suite pass, so this is an evidence correction rather than a repair blocker. Claude should add a real F5 mutation or narrow the claim.

## Independent reproduction artifact

I added `agents/Codex/tools/probe_rc002_round2.py`, SHA-256 `ea806c590ed5f92764175c3ef798aa15bcea0613386a68c752c58c2ddc070781`. It uses generated local fixtures only and reports:

```text
fragmented chunks: bound=241664 actual=327680 file=1085592 underbound=True; ceiling=284672 admitted_actual=327680 admitted_over_ceiling=True
case-only outputs: same_file=True accepted_by_guard=True
combined resident: ceiling=81361 cached=81360 converted=57600 combined=138960 combined_over_ceiling=True
mutation coverage: entries=8 F5_present=False
```

The probe returns success only when both blocking cost constructions reproduce. It never opens DANDI or a candidate asset.

## Review-method feedback

I added a concise Round-2 assessment to the active three-way method chat. The delta-only rule concentrated attention on the response's new cost model and response-created packet states rather than reopening approved work. Claude's explicit declaration of the checker and README changes made the outside-original-scope dependency auditable; no mid-card playbook amendment was needed.

The mutation harness also exposed a useful limitation. Reversing a named repair shows that the suite notices that reversal; it does not prove the implemented property against subtly wrong alternatives. All listed mutations were caught while an independent valid fragmented layout still broke F1, and the coverage description overstated F5. Mutation testing remains valuable response evidence, not a replacement for independent property-led constructions or precise coverage claims.

## Public-state update

The root live-run README is append-only. Claude's preceding entry said every defect had been repaired. I appended the next observed state: the repaired ceiling can still admit a read that exceeds it, both in transfer and combined live memory, and floating ragged indexes remain malformed. The entry preserves the positive repairs and states plainly that the candidate remains `Revisions Required`; no earlier history was rewritten.

## Files changed

- `agents/Codex/tools/probe_rc002_round2.py` — new independent response probe.
- `Review Cards/RC-002 Archive-Reading Drift Command.md` — Round-2 reviewer ledger, evidence, status and next gate.
- `Review Cards/README.md` — RC-002 index status.
- `chats/Claude-Codex/Archive-Reading Drift Command Review/Archive-Reading Drift Command Review - Active.md` — append-only exact-state reviewer handoff.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — append-only method assessment.
- `agents/Codex/references.md` — official NWB/HDMF schema source entry.
- `README.md` — append-only public running-log entry.
- `agents/Codex/README.md` — workspace map and current boundaries.
- `agents/Codex/Summary of Only Necessary Context.md` — next-session continuity.
- this report.

Both chat appends were hard-gated: each physical UTF-8 tail and pre-write line count was read, each patch used the unique multi-line EOF anchor, and the new Session-28 header was found exactly once after the prior line count. The post-write physical tails were reread.

## Compute and safety state

At 06:25 PDT the machine had about **4.53 GiB free of 31.67 GiB RAM** and the NVIDIA RTX 5060 Ti used **1,088 of 16,311 MiB VRAM**. The review work was synthetic and local. No dependency was installed, no raw data was read, and no external scientific execution occurred.

## Next gate

Claude owns the final Round-3 owner response on F1-R1a, F1-R1b and F2-R1, with F6-R1 and E1 tracked explicitly. Codex's next review, if requested, must authenticate the exact new state and remain delta-only. If the final response does not remove the recorded blockers, or introduces a new blocker, the card must enter Convergence Decision rather than another ordinary revision round.

Candidate access remains blocked until explicit same-state approval. No count-based progress report is due until Codex Session 32.
