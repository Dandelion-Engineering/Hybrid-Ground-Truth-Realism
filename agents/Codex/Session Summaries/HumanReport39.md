# Codex Human Report — Session 39

**Date and time:** 2026-08-17 04:18 PDT

**Phase:** Phase 2 — Execution

**Outcome:** RC-005 Round 1 is **Revisions Required**. The authenticated
six-file missing-depth recovery has two independently reproduced blockers: its
last console decision says the raw gate passed after reconciliation has made the
candidate unmeasurable, and its pre-read resident/peak formula omits the boolean
missing-position masks the reader now retains. The mathematical sensitivity
bound itself survived independent completion stress and all owner suites pass,
but the wired reader/command state is not approved. Ranks 1 and 2 remain paused,
the strict finite-depth rule remains operative, and no scientific result exists.

---

## 1. Startup and controlling workflow

The automation memory was read first. `.agent-turn` named Codex and no
`.agent-session.lock` existed, so I created the lock and re-read the turn file;
it still named Codex. Only then did project work begin.

I followed `AgentPrompt.md`'s context-first route: read all of
`Project Details/Project Details.md`, Codex's continuity, every chat summary
involving Codex, both active transcripts, Claude's Session-39 report, RC-005,
the six candidate artifacts and the superseding review-cycle playbook. The
repository began clean and synchronized at `2b95972` (`Claude Session 39`).

No archive or network resource was read, no candidate payload was opened, no
dependency was installed, and no scientific or sorter computation ran. All new
evidence uses deterministic/generated local fixtures.

## 2. Candidate authentication and review boundary

Every digest in RC-005's candidate table reproduced before review:

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `ef9740279f018e0b663e5d407f5297331fa17fe9042b18f2b477dc6c2233b988` |
| `Reproducibility Packet/scripts/utils/archive_units.py` | `79d8de45abf5d1cb5d177c325deb038067c06e4cfd4227f8fc01755df28aabc8` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `4345f0e3d029f1142a441ee0e777e3f8635ec9aa3223ad31cb2046082df83eb7` |
| `agents/Claude/tools/test_missing_depth.py` | `435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` |
| `agents/Claude/tools/test_measure_host_drift.py` | `c94609a4559cd98da96381f8e686c961f812536359a7cc1940134e981f54fa3a` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` (§17 only) | `f465d02b4df9bcea6be6ce3ba86f4ba7e16d53e08cd94aec2785e2a3985119bd` |

The unchanged approved drift utility, its harness and the RC-002 mutation
harness also matched the card. I made no edit to any candidate artifact.

This was Round 1, so I performed one full-artifact pass and recorded one
exhaustive numbered ledger. Per `Playbooks/review-cycle.md`, Round 2 is now
delta-only against F1/F2 plus regressions introduced by their repairs.

## 3. F1 — terminal console decision contradicts reconciliation

The owner suite contains the right decisive fixture: missing depths violate
support invariance while the raw point gate passes. The record correctly says:

- completion disposition `unmeasurable`;
- reconciled disposition `unmeasurable`;
- `advances=False`; and
- point gate `passed=True`.

The command prints the completion disposition correctly, writes the report, then
ends with `[drift] verdict: passed=True label=no time-ordered drift resolved`.
That line reads the raw `verdict` object at `measure_host_drift.py:1320-1321`,
not the `reconciled` state built at line 1184. The owner case asserts JSON and
report fields but does not capture or assert stdout.

This is blocking because the last unqualified command decision authorizes the
opposite action from §17 and the structured record. The repair must make the
terminal decision line report the reconciled disposition, identify any retained
point-gate line as diagnostic, and add a whole-command stdout assertion that
fails on the current paused fixture.

## 4. F2 — returned masks are absent from the resident bound

The reader's plan still computes `resident_bytes` as `total_spikes * 16` plus
the largest stored slice at `archive_units.py:1833-1834`. The new reader retains
one boolean `missing_depths` array beside every unit at lines 2039-2040, but the
mask bytes do not enter `resident_bytes` or `peak_resident_bytes`.

Those masks are inside the documented scope: the command says the processed-
asset read and the arrays it returns are covered by `--max-mib`. They are not
allocator overhead and they are not transient outside the read. My 3,600-spike
fixture therefore returns 3,600 retained bytes absent from the formula. At the
rank-1 size, the omitted term is **3,160,311 bytes**.

The repair must include all returned mask arrays in the pre-read resident and
peak formulas and the printed decomposition, then exercise exact formula and
just-below/just-above admission tests.

The probe separately records the command's finite-only times/depths copies:
57,248 bytes on the generated fixture and 50,561,280 bytes projected at rank 1.
Because the present ceiling explicitly claims only the read footprint, I logged
this as a nonblocking accounting follow-up rather than broadening F2. A later
whole-command memory claim must include them; the no-missing copy can be avoided
now as a cleanup.

## 5. Independent probe and mathematical stress

I added `agents/Codex/tools/probe_rc005_round1.py`. It imports the owner harness,
constructs only local generated HDF5, captures the decisive whole-command stdout,
and compares the reader's planned resident arrays with every retained returned
array. Its successful run reports:

- `disposition_console_contradiction=True`;
- record final disposition `unmeasurable`, `advances=False`, while the final
  console line says `passed=True`;
- `retained_mask_unbudgeted=True`;
- 3,600 omitted mask bytes on 3,600 synthetic spikes; and
- the rank-1 projections above.

I also stress-tested the missing-depth math independently over 120 small generated
fixtures and 1,080 finite completions. Every actual observation and approved
completed-data null landed inside the proposed outer interval: **0 observation
escapes and 0 null escapes**. This is positive evidence for the mathematical
layer, not approval of the wiring around it.

## 6. Reproduced suites

- `test_missing_depth.py --permutations 200 --completions 200`: **86 checks,
  0 failed**.
- `test_measure_host_drift.py`: **518 checks, 0 failed**; its output visibly
  reproduces F1.
- unchanged `test_band_drift.py --permutations 200`: **103 checks, 0 failed**.
- `mutate_rc002_repairs.py --repo-root .`: **all 32 mutations detected and the
  unmutated control passes**.
- packet runbook checker: **exit 0**, ten steps agree and the drift command
  remains pending its first candidate report.
- all six candidate Python files and the new probe compile cleanly.

The green suites do not clear F1 or F2 because neither current acceptance surface
asserts the contradictory terminal decision or the new returned-mask memory term.

## 7. Review record, public state and closeout files

I appended the complete Round-1 verdict to the active Missing Depth Recovery
Review chat. Before the append, the transcript contained 93 physical UTF-8 lines;
the exact multi-line EOF anchor occurred once. After the append it contained 165
lines, the new Codex Session-39 header occurred exactly once and only after the
old line count, and the physical tail ended at the new separator.

RC-005 now records `Round 1 — Revisions Required`, the two findings, the delta-
only Round-2 boundary and the nonblocking downstream-copy follow-up. The public
root README received one lean append-only heartbeat because a formal review
return before execution is a noteworthy state change. It states both defects and
preserves the boundary that no candidate was read, no drift value exists, no
sorter ran and no scientific result exists.

Created:

- `agents/Codex/tools/probe_rc005_round1.py`
- `agents/Codex/Session Summaries/HumanReport39.md`

Updated:

- `chats/Claude-Codex/Missing Depth Recovery Review/Missing Depth Recovery Review - Active.md`
- `Review Cards/RC-005 Missing Depth Recovery, Wired.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No progress report was due in Session 39. The Session-40 count-based progress
report is due next, regardless of RC-005's Round-2 outcome.

## 8. Immediate owner and authorization boundary

**Immediate owner: Claude.** Repair F1 and F2 on one exact state, update RC-005's
candidate table, rerun the affected acceptance and mutation surfaces, explicitly
approve the repaired bytes, and hand them back in the active review chat.

Until Codex explicitly approves that same repaired state, ranks 1 and 2 remain
paused and the strict finite-depth confirmation remains operative. No host is
pinned, no candidate has a drift/noise/effective-SNR value, and no donor,
placement, generation, Rung-0 or sorter authorization moved.
