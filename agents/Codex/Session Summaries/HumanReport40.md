# Codex Human Report — Session 40

**Date and time:** 2026-08-17 06:15 PDT

**Phase:** Phase 2 — Execution

**Outcome:** RC-005 closed **`Approved with Follow-Ups` at Round 2** on the exact
seven-file missing-depth state both agents explicitly approved. The repaired
command now ends with the reconciled decision, and the reader's pre-read bound
charges the per-spike missing-depth masks it retains. Codex independently
verified both boundaries at 10/10, reproduced the changed owner suite at 543/543
and the repair-reversion harness at 4/4 with a green control. No archive or
candidate asset was read; no host, drift value, sorter run, or scientific result
exists.

---

## 1. Startup and controlling workflow

`.agent-turn` named Codex and `.agent-session.lock` did not exist. I created the
lock, re-read the turn file, and confirmed it still named Codex before reading
project materials or doing any project work.

I then followed `AgentPrompt.md` in order: read `Project Details/Project
Details.md` in full; read Codex's continuity summary; ingested every chat summary
and both active transcripts without replying; read the superseding review-cycle
playbook, RC-005, Claude's `HumanReport40.md`, and the complete Round-2 delta.
The repository began clean at `9e2feb1` (`Claude Session 40`), matching
`origin/main`.

This was a review/verification session, not a heavy scientific run. At close,
15,440 MB of 32,425 MB system RAM was available and GPU use was 1,056 of 16,311
MiB. No dependency was installed, no archive/network resource was opened, and no
sorter or generator was run.

## 2. Exact state authenticated

Every digest in RC-005's Round-2 candidate table matched disk:

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `ef9740279f018e0b663e5d407f5297331fa17fe9042b18f2b477dc6c2233b988` |
| `Reproducibility Packet/scripts/utils/archive_units.py` | `ed0766f2d3e6399a4a28f5289159b948cc907ed8ee72055314b0f363d515ec3a` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `26934a6b862be6f0cf7b269346ff85c4c2fd9f5ab056a77d427bc9059d39370e` |
| `agents/Claude/tools/test_missing_depth.py` | `435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` |
| `agents/Claude/tools/test_measure_host_drift.py` | `79c9bb5c3c04bdba66dcbcca9cf092d0b611d19b9ff526edcfeb8ed596c04335` |
| `agents/Claude/tools/verify_rc005_round2_repairs.py` | `4f27b70c35f28f715d93ac214aebf0c01f4f4af2f958fb05b373132c8a013bee` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 26 | `3e587874fdce355a4d605861f1ddfd0b1481a766385c2084e37d12db6d44100a` |

The approved `band_drift.py` and its harness remained at `eace4cd3…` and
`946df906…`. A raw-byte comparison of the selection document's §1–§16 span
against parent state `219d395` found both spans identical at **144,664 physical
bytes**, SHA-256 `700b3b9a…`.

## 3. Round-2 delta review

### F1 — final console decision

Round 1 found a whole-command contradiction: the report and JSON correctly
paused a candidate whose point gate passed, while the command's final console
line still announced `passed=True`. Claude's repair writes the artifacts first,
then prints the point gate labelled `diagnostic, not the decision`, and ends with
the reconciled disposition.

I independently reconstructed the paused local fixture. Its point gate passes,
its final record is `unmeasurable` with `advances=False`, and its exact last
non-empty line is:

`[drift] decision: unmeasurable; advances=False; gate and completion bound conflict=False`

The only line carrying `passed=` is the diagnostic line above it. F1 is repaired
on the consumer-visible console boundary rather than only in saved artifacts.

### F2 — retained masks in the memory bound

Round 1 also found that the reader returns and retains one boolean mask per
spike while the pre-read formula counted only the two float64 arrays and largest
stored-width slice. Claude's repair derives `MASK_ITEMSIZE` from NumPy, charges
`n_spikes * MASK_ITEMSIZE` into `resident_bytes`, publishes that component as
`mask_bytes`, and carries it into the combined peak and printed/structured
records.

My independent 3,600-spike fixture derived the boundary from fixture properties,
not from the plan under test:

- mask term: 3,600 bytes;
- resident term: 68,400 bytes;
- combined peak: 180,337 bytes;
- former mask-omitting peak: 176,737 bytes, refused;
- corrected peak: admitted exactly;
- masks returned: 3,600 bytes, exactly the amount charged.

This closes the unsafe direction. At rank-1 size the repaired retained term is
3,160,311 bytes.

### Reconciliation rule

Claude explicitly asked not to let Round-1 silence become approval of the
unchanged `reconcile_verdict` rule. I approved it directly in the closing review
message. The card defines it as blocking for a finite-record/completion-bound
disagreement to be resolved in favour of either side; the implementation instead
returns `unmeasurable`, non-advancing, with `conflict=True`. That is the required
safe rule.

## 4. Evidence executed

- New `agents/Codex/tools/probe_rc005_round2.py`: **10 checks, 0 failed**;
  generated local HDF5 only.
- `agents/Claude/tools/test_measure_host_drift.py`: **543 checks, 0 failed**.
- `agents/Claude/tools/verify_rc005_round2_repairs.py`: unmutated control passes;
  **4 of 4** whole/near-miss reversions caught.
- Changed candidate, owner-test, reversion, and reviewer-probe Python files:
  `py_compile` exit 0.
- Packet runbook checker: exit 0, ten agreeing steps and the drift command still
  explicitly pending its first approved candidate report.
- `git diff --check`: clean.

The unchanged missing-depth and estimator suites were authenticated at their
recorded digests; Round 2 did not re-audit their unchanged material. No heavy
eleven-minute RC-002 mutation rerun was repeated by Codex because Claude had run
it on the authenticated state and the new four-mutation harness directly covers
the two changed repairs.

## 5. Two nonblocking close-time findings

The exact safe behavior is approved. Two record/label problems were tracked
rather than silently absorbed into another owner round:

1. Draft 26 and the owner handoff call the byte-identical §1–§16 span 143,890
   bytes. Direct physical-byte reads of both states give **144,664**, with the
   stated identical SHA-256. The review card's close record was corrected; the
   document count remains tracked for its next status-prose change.
2. The report and refusal text call all of `resident_bytes` “converted arrays,”
   while the exact formula also includes the maximum slice at its stored width.
   The total, mask subterm, peak and admission boundary are correct. The label
   should name the slice when report layout or broader memory accounting next
   moves.

Both fall under the card's nonblocking wording/report-layout boundary. The
outcome is therefore `Approved with Follow-Ups`, not a softened blocker and not
an undocumented clean approval.

## 6. Review closure and public state

I appended the exact-state approval to the active review transcript using a
unique physical-EOF anchor: 310 pre-write lines, one Session-40 header after that
count, one header total, and the expected new physical tail. The transcript was
then renamed `Missing Depth Recovery Review - Concluded.md` and a `Summary.md`
was created. RC-005 and the Review Card index now record the closed outcome.

The root public README gained one lean append-only heartbeat. It says what the
closure does and does not mean: the missing-depth implementation gate is clear;
no candidate was read during review and no drift or sorter result exists.

The three-way Review Method Change chat remains active at Randy's instruction.
No message there required a reply this session.

## 7. Count-based progress report

Session 40 triggers Codex's eight-session progress-report cadence. I read
`Playbooks/research-progress-report.md` and created `agents/Codex/Progress
Reports/Progress Report Session 40.md`. It explains in plain language the two
real-input failures since Session 32, why sample-count floors could not make
missing medians safe, how the completed-data null became assumption-free, what
review found, and why approval is still not a scientific result. No verification
artifact update was manufactured; `verify_realism.py` still waits on results.

## 8. Files created or updated

**Created**

- `agents/Codex/tools/probe_rc005_round2.py`
- `agents/Codex/Progress Reports/Progress Report Session 40.md`
- `agents/Codex/Session Summaries/HumanReport40.md` (this report)
- `chats/Claude-Codex/Missing Depth Recovery Review/Summary.md`

**Updated**

- `Review Cards/RC-005 Missing Depth Recovery, Wired.md`
- `Review Cards/README.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
- `chats/Claude-Codex/Missing Depth Recovery Review/Missing Depth Recovery Review - Concluded.md` — appended exact-state decision, then renamed from Active

No source or candidate file owned by Claude was edited. The approved seven-file
candidate remains byte-identical to the state Claude handed off.

## 9. Next steps

1. Claude owns the resource-checked rank-1 measurement under the approved RC-005
   state. Measure current memory immediately before starting and compare it with
   the mask-inclusive peak.
2. If the command produces a report, add it as packet runbook step 11 and remove
   the pending declaration, then assess the report under the strict gate.
3. A report is not a host pin by itself. Drift, noise, effective SNR, placement,
   matcher implementation, balance/manipulation, generation, and sorter
   authorization remain separate gates.
4. Codex's next session is 41; the next cadence progress report is Session 48.

No new director decision is needed. The existing Phase-1 contract-review request
remains open and nonblocking.
