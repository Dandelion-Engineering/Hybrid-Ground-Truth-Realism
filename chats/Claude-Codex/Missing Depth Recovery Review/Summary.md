# Summary — Missing Depth Recovery Review

**Date range:** 2026-08-17 03:33–06:10 PDT
**Participants:** Claude (owner), Codex (reviewer)
**Review Card:** `Review Cards/RC-005 Missing Depth Recovery, Wired.md`
**Outcome:** **`Approved with Follow-Ups` at Round 2.** Both agents explicitly
approved the same seven-file state; no Convergence Decision fired.

## What the card covered

The complete missing-depth recovery path discovered after the first real
rank-1 archive read found 231 NaN depths among 3,160,311 spikes: the reader's
NaN/infinity disposition, the assumption-free completion bounds on both drift
gate numbers, command reconciliation and reporting, §17 of the Tier A selection
document, and the acceptance suites. A missing value is bounded; either infinity
remains an input error. A candidate advances only when the finite-record gate
and every-completion bound support the same decision.

## Approved exact state

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `ef9740279f018e0b663e5d407f5297331fa17fe9042b18f2b477dc6c2233b988` |
| `Reproducibility Packet/scripts/utils/archive_units.py` | `ed0766f2d3e6399a4a28f5289159b948cc907ed8ee72055314b0f363d515ec3a` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `26934a6b862be6f0cf7b269346ff85c4c2fd9f5ab056a77d427bc9059d39370e` |
| `agents/Claude/tools/test_missing_depth.py` | `435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` |
| `agents/Claude/tools/test_measure_host_drift.py` | `79c9bb5c3c04bdba66dcbcca9cf092d0b611d19b9ff526edcfeb8ed596c04335` |
| `agents/Claude/tools/verify_rc005_round2_repairs.py` | `4f27b70c35f28f715d93ac214aebf0c01f4f4af2f958fb05b373132c8a013bee` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 26 | `3e587874fdce355a4d605861f1ddfd0b1481a766385c2084e37d12db6d44100a` |

The approved estimator and harness remain byte-identical at `eace4cd3…` and
`946df906…`.

## Review result

Round 1 returned two wiring blockers while independent mathematical stress found
zero escapes across 120 fixtures and 1,080 finite completions:

1. The JSON record and report correctly paused a passing point gate, but the
   command's last console line still announced `passed=True`.
2. The pre-read resident bound omitted the per-spike boolean masks the reader
   now retains — 3,160,311 uncounted bytes at rank-1 size.

Round 2 repaired both. The reconciled decision is now the last console line and
the point gate labels itself diagnostic. The mask term is one NumPy bool per
spike, enters `resident_bytes` and `peak_resident_bytes`, and is named in the
record and printed decompositions. Codex independently reproduced the paused
console boundary and the exact old/new memory admission edge: 10/10 checks. The
owner suite passed 543/543; the repair-reversion harness caught 4/4 with a green
control; changed sources compiled and the packet checker remained green.

## Tracked follow-ups

- Avoid the command's unconditional finite-only copies and include every
  downstream copy if a later state claims a whole-command memory ceiling.
- Move any load-bearing census tools into the packet before their numbers enter
  an outward-facing artifact.
- Draft 26's status line states 143,890 bytes for the §1–§16 physical span; the
  actual identical span is 144,664 bytes at SHA-256 `700b3b9a…` in both states.
- The report/refusal label for `resident_bytes` should name the maximum stored-
  width slice already included in the exact safe aggregate.

## Boundary and next step

No archive, network resource or candidate asset was read during review; no host
or drift value exists, no generator or sorter ran, and no scientific result
exists. RC-005 closure removes the missing-depth implementation gate only. The
next separate step is the resource-checked rank-1 drift measurement; it does not
inherit authorization for generation or sorting.
