# Codex Human Report — Session 31

**Date:** 2026-08-15
**Phase:** Phase 2 — Execution
**Outcome:** RC-003 Round 2 returned **`Revisions Required`**. The exact-name
association repair passes, but provenance authentication and transferred-byte
budgeting remain blocking. Candidate access remains blocked; Claude owns the
final Round 3 response.

## Startup and controlling state

The automation gate named Codex, no `.agent-session.lock` existed, and the lock
was created before project work. I then reread `.agent-turn`, confirmed it still
named Codex, and followed `AgentPrompt.md`. I read Project Details, both agents'
continuity and newest reports, every chat summary, every active chat involving
Codex, the superseding review method, RC-003, the complete Round-2 response
state, and the live-run README playbook.

This was Codex Session 31. No count-based progress report was due; the next one
is due in Session 32.

Claude's Round-2 response declared eight files. I authenticated every digest
before review:

| File | Authenticated SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/archive_units.py` | `787d53ab87069280583f3c4ec0264eb686033535402368d5f2bddfeec0a0d814` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `1941c577b79a7e1d22ab8e25ff41791d1b2852050c980526b6685340bae67ae5` |
| `agents/Claude/tools/test_measure_host_drift.py` | `326314a530355c27b3689919acaa9c7497b7605fa7e0de22d26212afe0b79aee` |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `1e5cffcd6856da215a197528bc66ba62b64d1546d276dcf5d291310bb765525d` |
| `agents/Claude/tools/verify_rc003_round1_repairs.py` | `43402d14245965bfa42d47be1c54a4d80c57b4532e7e677f60e4bfccf20a648c` |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc` |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f` |
| `Reproducibility Packet/README.md` | `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5` |

The first five are the changed or response-created delta. The last three were
explicitly unchanged, so the formal pass did not re-audit their settled content.
Before the substantive reruns, the machine reported **18,089 MiB available of
32,425 MiB physical memory**. No dependency install was needed.

## Round 2 decision

I do not approve the exact Round-2 response state. RC-003-F2 is closed by the
repair, while F1 and F3 remain blocking.

### RC-003-F1 — token presence is not a positive shared provenance state

The new rule requires `general/source_script` on both raw and processed assets,
requires each value to be read whole, and checks for the case-insensitive token
`neuroconv`. That closes the missing-field path but does not authenticate what
the string says or whether the two assets name the same conversion state.

A processed string reading `This asset was NOT created using NeuroConv;
exported by LocalTool v3` reaches a drift verdict because the forbidden
toolchain's name is still present. A raw `Created using NeuroConv v0.9.2` paired
with processed `Created using NeuroConv v0.9.1` also reaches a verdict. The
record correctly says `values_agree = false`, but the owner suite expressly
defines that disagreement as nongating.

This is not the approved §16.4/§16.8 common-clock confirmation. Those sections
require the exact raw and processed assets' provenance and values to establish
the documented common session clock, with absence or failure stopping before
the statistic. A token on each side is necessary evidence, not authentication
of a positive shared conversion state.

### RC-003-F2 — passes

`series_probe()` now decomposes `ElectricalSeries<probe><AP|LF>` and compares
the probe token exactly. `ElectricalSeriesProbe000AP` is refused for requested
`Probe00`. The Round-1 substring ownership construction is closed.

### RC-003-F3 — h5py request bytes do not bound underlying transfer bytes

`BoundedReader` enforces the length h5py requests for a path, but it delegates
that request to `RemoteFile`, whose range cache fetches full blocks. The default
block size is one MiB. A small logical request can therefore cause a much larger
network-equivalent transfer before `BoundedReader` sees the next request.

On a generated local file carrying the two-million-character provenance value,
the default reader transferred **2,081,456 distinct bytes before refusal** under
a claimed **65,536-byte provenance budget**. The owner's 33,456-byte verification
uses a deliberately small block size and proves refusal at the h5py request
boundary; it does not prove the command's default underlying transfer boundary.

RC-003 says cost must be knowable before it is spent, and the module describes
the per-path budget as the most the program may spend. A logical-request budget
that can expand to a full cache block during delegation does not establish that
property.

### RC-003-E1 — non-blocking report wording

The response says the record carries provenance values “in full,” but optional
paths can carry refusal or truncation markers. Only the required authenticated
`source_script` is necessarily complete when a verdict is written. Round 3
should narrow the description.

## Independent evidence

I added `agents/Codex/tools/probe_rc003_round2.py`, SHA-256
`d67bf2616b2b10ef6e7f3f34ad324cdfa327787eb8af5b71cb4f7fd1de4e9ef2`.
It uses generated local HDF5 fixtures only. It reproduced the negated-toolchain
verdict, the mismatched-version verdict, and the default-block transfer
expansion, then exited zero. It reads no archive, network resource, or candidate
asset.

## Verification on the exact response state

| Check | Codex rerun result |
|---|---|
| Owner end-to-end archive-command harness | **325 checks, 0 failed, 13.7 s** |
| Repair-mutation harness | Green 325-check control; **20/20** mutations caught |
| Owner Round-1 repair verifier | All three constructions refused; F3 small-block case at **33,456 bytes** |
| Packet runbook checker | 10 numbered steps agree; 1 command declared pending |
| RC-003 Round-2 probe | Both remaining blockers reproduced; exit 0 |
| Compilation | Clean on all changed, response-created, and reviewer Python files |

The unchanged checker mutation harness and approved estimator suite were not
rerun because the superseding review method makes Round 2 delta-only. Claude's
response records their unchanged green results at 18/18 and 103/103. The broad
green suites are valuable regression evidence, but they do not make the two
remaining boundary claims true.

## Records changed

- Added the independent Round-2 probe.
- Updated RC-003's status, round log, reviewer verification, outcome, and open
  non-blocking wording follow-up.
- Updated the review-card index.
- Appended the exact Round-2 verdict to the bounded review chat after a verified
  UTF-8 physical-tail and line-count check.
- Appended the bounded generalization observation to the active review-method
  chat using the same append-only checks. No Randy decision is needed.
- Added one lean public running-log entry because the default-block transfer
  counterexample and the distinction between token presence and provenance
  authentication are noteworthy before any real read.
- Updated Codex's README and continuity. No progress report was created because
  Session 31 is not a cadence trigger.

## Boundaries and next owner

No archive, network resource, or candidate asset was read. No host is pinned,
no drift value exists, and no donor selection, exposure schedule, placement
configuration, Rung 0, generation, or sorter execution occurred. No scientific
result exists.

Claude owns the final Round 3 response to F1 and F3 plus the E1 wording repair.
The pass is delta-only over the repairs and response-created state. Candidate
access remains blocked until explicit same-state approval. If Round 3 does not
reach approval, method clause 5 forbids another like-for-like successor and
requires a split or redesign with the changed boundary named.
