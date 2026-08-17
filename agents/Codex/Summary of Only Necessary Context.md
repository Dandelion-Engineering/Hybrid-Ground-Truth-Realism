# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 40 · 2026-08-17.**

**Next Codex session will be Session 41. The next count-based progress report is
due in Session 48.**

## Current phase and controlling boundary

**Phase 2 — Execution is open. No host is pinned and no scientific result
exists.** RC-005 closed `Approved with Follow-Ups` at Round 2 on the exact
seven-file state both agents explicitly approved. The missing-depth
implementation gate is therefore cleared, but the rank-1 drift measurement is a
separate execution step and has not run under the approved state.

Ranks 1 and 2 no longer pause on the old all-finite-depth confirmation. The new
rule is narrower: NaN is retained in position and bounded as missing; either
infinity remains a fatal input error; any support-invariance violation,
unbounded deciding side, threshold-straddling completion interval, or
finite-record/completion-bound disagreement is `unmeasurable` and keeps the
candidate paused. Rank-5/7/9/13 declared-clock disagreements remain separately
paused and keep their rank.

## RC-005 approved exact state

| Candidate file | SHA-256 approved |
|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `ef9740279f018e0b663e5d407f5297331fa17fe9042b18f2b477dc6c2233b988` |
| `Reproducibility Packet/scripts/utils/archive_units.py` | `ed0766f2d3e6399a4a28f5289159b948cc907ed8ee72055314b0f363d515ec3a` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `26934a6b862be6f0cf7b269346ff85c4c2fd9f5ab056a77d427bc9059d39370e` |
| `agents/Claude/tools/test_missing_depth.py` | `435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` |
| `agents/Claude/tools/test_measure_host_drift.py` | `79c9bb5c3c04bdba66dcbcca9cf092d0b611d19b9ff526edcfeb8ed596c04335` |
| `agents/Claude/tools/verify_rc005_round2_repairs.py` | `4f27b70c35f28f715d93ac214aebf0c01f4f4af2f958fb05b373132c8a013bee` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 26 | `3e587874fdce355a4d605861f1ddfd0b1481a766385c2084e37d12db6d44100a` |

The approved estimator remains `band_drift.py` `eace4cd356…` with harness
`946df906943…`. The §1–§16 section-body span is byte-identical between
`219d395` and the approved state: **144,664 physical bytes**, SHA-256
`700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59`.
Draft 26's status line states 143,890 and is retained as tracked follow-up 3.

## Session-40 Round-2 delta review

Claude accepted both Round-1 blockers in full and repaired them on one state.
Codex authenticated all seven digests and closed the card `Approved with
Follow-Ups`.

### F1 — repaired console decision

The point gate can pass while missing-depth reconciliation makes the candidate
`unmeasurable`. The command used to write the correct report/JSON and still end
its console with `passed=True`. It now writes artifacts first, prints the point
gate explicitly labelled `diagnostic, not the decision`, and ends with the
reconciled disposition, `advances`, and `conflict` values.

Codex's fresh paused fixture has a passing point gate and ends exactly:

`[drift] decision: unmeasurable; advances=False; gate and completion bound conflict=False`

The unchanged `reconcile_verdict` rule is explicitly approved rather than
inferred from silence: any finite-record/completion-bound disagreement is
unmeasurable; neither side wins.

### F2 — repaired retained-mask bound

`plan_transfer` now charges `n_spikes * numpy.bool_.itemsize` into
`resident_bytes`, publishes the component as `mask_bytes`, and carries it into
`peak_resident_bytes`, the record, refusal text, report, and console.

On Codex's independent 3,600-spike fixture:

- `mask_bytes = 3,600`;
- `resident_bytes = 68,400`;
- `peak_resident_bytes = 180,337`;
- the old mask-omitting ceiling `176,737` is refused;
- the exact corrected peak is admitted;
- the returned masks occupy exactly the charged 3,600 bytes.

At rank-1 size the repaired term is 3,160,311 bytes.

### Evidence reproduced

- `agents/Codex/tools/probe_rc005_round2.py`: **10/10**, generated local HDF5
  only; positive console equality and exact old/new memory edges.
- `test_measure_host_drift.py`: **543 checks, 0 failed**.
- `verify_rc005_round2_repairs.py`: unmutated control green; **4/4** whole and
  near-miss reversions caught.
- Changed candidate and reviewer Python sources compile.
- Packet consistency: ten agreeing steps and `measure_host_drift.py` still
  pending its first approved candidate report.
- `git diff --check` clean.

No archive, network resource or candidate asset was read during review.

## RC-005 tracked follow-ups

1. The command's unconditional finite-only split retains downstream array copies
   outside the present read-only `--max-mib` scope. Avoid the clean-record copy;
   include every downstream copy if a later state claims a whole-command ceiling.
2. Move `probe_conversion_pairs.py`, `probe_nonfinite_depths.py`, and
   `probe_missing_depth_crossover.py` into the packet before any of their
   load-bearing numbers enters an outward-facing artifact.
3. Correct Draft 26's 143,890-byte §1–§16 status count to the verified 144,664
   physical bytes when that prose next moves; the hash/equality is already right.
4. The report/refusal label calls all of `resident_bytes` “converted arrays,”
   although the safe exact aggregate also includes the maximum stored-width
   slice. Name that slice when the report layout or broader memory accounting
   next moves. The numeric peak and admission boundary are correct.

## Immediate next step

**Immediate execution owner: Claude**, consistent with the existing lane. Run
rank 1 — CSHL047 / Probe01, session
`b52182e7-39f6-4914-9717-136db589706e`, strict gate — under the approved RC-005
state. Immediately before starting, measure free RAM and VRAM, compare free RAM
against the mask-inclusive `peak_resident_bytes`, and do not start if it does
not fit. The expected archive work is a bounded candidate read, not a sorter run.

If a report is produced, make `measure_host_drift.py` packet runbook step 11,
remove its `PENDING_STEP`, and rerun consistency. The report then needs contract-
level interpretation; it does not pin the host merely by existing.

**Next Codex work:** cross-review Claude's newest report and any rank-1 output.
Authenticate the approved command state before interpreting the result. Keep
input errors, `unmeasurable`, drift failure, and drift pass as distinct
dispositions. A pass removes only the drift gate; noise, effective SNR, exact
placement, matcher implementation, balance/manipulation, generation, and sorter
authorization remain separate.

## Approved foundation and downstream gates

- RC-001: Draft 24 `c35987fe…`, drift utility `eace4cd35…`, owner harness
  `946df906…`, closed `Approved`.
- RC-003: bounded archive reader closed `Approved` at its recorded nine-file
  state.
- RC-004: reference-instant pair check closed `Approved` at its exact five-file
  state.
- RC-005: missing-depth recovery closed `Approved with Follow-Ups` at the exact
  seven-file state above.
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

After a candidate passes drift, the order remains: noise and effective-SNR host
gates; approve the exposure schedule and placement specification; approve
matcher implementation and tests; calibrate footprint/placement; freeze exact
matching outputs; obtain independent balance/manipulation approval; then seek
separate generation and later Rung-0/sorter authorizations.

The three-way Review Method Change chat remains active by Randy's instruction.
No new director decision is needed. `agents/Codex/Session Summaries/HumanReport40.md`
is the detailed record of this review and closeout; the Session-40 progress
report is the director-facing account.
