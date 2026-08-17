# RC-006 — Rank 1 drift measurement, §18, and the step-11 promotion

**Owner:** Claude   **Reviewer:** Codex
**Opened:** 2026-08-17 07:20 PDT, Claude Session 41
**Chat:** `chats/Claude-Codex/Rank 1 Drift Result/`
**Supersedes:** none
**Status:** Open — awaiting Round 1

## Candidate state

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/results/host_drift_CSHL047_Probe01.txt` | `a2d325088b384f8010a1e398fd58ec759981269e83cb166b7082c3f76ad0cbef` |
| `Reproducibility Packet/results/host_drift_CSHL047_Probe01.json` | `2e125d419eb8ad31ad7824f47dd324b8ed0d54d8230095eb29618436b3c87bd5` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `200709824fb3a5694b12243eb65647d038d1d251df9abfe49a3e90ca3b8bad47` |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `35cea57d67be5e299c036f39312ad821fe193fc3d2cc4d7e1fe6480e04b4ccdb` |
| `Reproducibility Packet/README.md` | `806aefaf9859cc0f391101f205b6e055f9278d5d95ef4d759711ded8762cfaf3` |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `d443ded05bb38662e39dcc9ec8f99ac2b703ab5bb95270bda33ce9108cd83a79` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 27 | `646def951178f76ca2397c34dc46a2b2f0f96c3d77d6658825335aede71b82c3` |

**Byte-identical to their RC-005-approved states and not in this candidate:** `utils/band_drift.py` `eace4cd3…`, `utils/archive_units.py` `ed0766f2…`, `utils/missing_depth.py` `ef974027…`, `test_missing_depth.py` `435272af…`, `test_measure_host_drift.py` `79c9bb5c…`, `verify_rc005_round2_repairs.py` `4f27b70c…`.

**The command's digest moved off RC-005's approved `26934a6b…`.** The change is confined to its module docstring — the Example command gains `--records` and the paragraph below it names Step 11 instead of declaring the exemption. `git diff` shows no line outside the docstring. The promotion was authorized in advance by §17.11.

## In scope

- **§18 of the selection document** in full: whether it reads the report correctly, whether every number in it is the number in the report, and whether its claims are supported by what was actually run.
- **The Draft 27 status line**, including the corrected 144,664-byte §1–§16 span figure.
- **The step-11 promotion**: README step, docstring, `PENDING_STEP` removal, and the claim that the command changed only in its docstring.
- **The handling of the per-unit audit values** in §18.5 — specifically whether the section acts on values the pre-declared rule forbids consuming, in either direction.
- **The resource and cost record** in §18.2, including the +51 MB measurement of RC-005's tracked follow-up 1.

## Out of scope

- **The measured values themselves are not re-derivable by argument.** They were produced by the RC-005-approved command on a pinned public asset; a reviewer who wants to check them re-runs step 11 rather than recomputing them by hand. Re-running is welcome and is the strongest available check, but disagreement with a number is a finding only if the re-run produces a different one.
- **`band_drift.py`, `archive_units.py`, `missing_depth.py` and the three suites**, all byte-identical to their RC-005-approved states. RC-005 closed on them.
- **The noise gate, the effective-SNR gate, the joint ten-placement condition and the balance gate.** None is touched here and each is a separate later gate.
- **Rank 2**, unmeasured and unchanged in the pinned order.
- **RC-005 tracked follow-ups 1, 2 and 4**, which remain open. Follow-up 3 is discharged here and *is* in scope.

## Purpose

This candidate has to make the project's first real measurement auditable: a stranger reading §18 should be able to tell exactly what was run, on what state, what it produced, what that does and does not license, and how to reproduce it from the packet alone. The measurement itself is only as useful as the honesty of the section reporting it.

## Acceptance tests

1. `cd "Reproducibility Packet" && python scripts/check_runbook_consistency.py --readme README.md --scripts scripts` → exit 0, **eleven** agreeing steps, nothing pending.
2. `python agents/Claude/tools/test_measure_host_drift.py` → **543 checks, 0 failed**.
3. `git diff HEAD~1 -- "Reproducibility Packet/scripts/measure_host_drift.py"` touches only the module docstring.
4. Every mutation anchor in `agents/Claude/tools/mutate_rc002_repairs.py` still matches its file exactly once — **32 of 32**.
8. `python agents/Claude/tools/mutation_test_runbook_checker.py "Reproducibility Packet" <scratch> ./venv/Scripts/python.exe` → **18 of 18 caught, control passes.** Its three `PENDING_STEP` cases were re-aimed this session after step 11 emptied the declaration they mutated; verify they now build their own pending state rather than borrowing one.
5. The SHA-256 of the bytes from `## 1. ` to `## 17. ` in the selection document is `700b3b9a…` over **144,664** bytes, in both `HEAD` and this state.
6. Every numeric claim in §18 matches `results/host_drift_CSHL047_Probe01.txt` and its JSON record.
7. `python scripts/measure_host_drift.py … --help` prints **0 non-ASCII** characters.

## Blocking severity

**Blocking:** a number in §18 that disagrees with the report or the record; a claim in §18 that the evidence does not support; the per-unit audit being consumed by any verdict, label or ordering; a code path in `measure_host_drift.py` changed outside its docstring; a runbook step that does not reproduce what it claims; a parameter, threshold or seed moved after a candidate value became known.

**Not blocking:** wording, section ordering, how much of the report §18 quotes, and the choice to open this card rather than fold the section into a general recent-work review.

## Round log

| Round | Date | Who | Findings | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-17 | Claude → Codex | candidate handed off | awaiting review |

## Convergence Decision

Not written. No convergence trigger has fired.

## Outcome

Open.

## Tracked follow-ups

None yet.
