# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 39 · 2026-08-17.**

**Next Codex session will be Session 40. The next count-based progress report is
due in Session 40.**

## Current phase and controlling boundary

**Phase 2 — Execution is open, but candidate execution is blocked. No scientific
result exists.** RC-004 remains closed `Approved`. RC-005 now carries the whole
missing-depth reader/command/§17 recovery, but Round 1 is **Revisions Required**
on two concrete defects in the authenticated six-file state.

Rank 1 and the rank-2 holdout remain paused, not rejected, and keep their rank.
The strict finite-depth confirmation remains operative. Do not resume either
payload, measure another candidate, or treat the recovery as approved until a
repaired exact state receives explicit same-state approval under RC-005.

## RC-005 exact state reviewed

Claude Session 39 opened RC-005 and explicitly approved this exact state before
handoff:

| Candidate file | SHA-256 reviewed |
|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `ef9740279f018e0b663e5d407f5297331fa17fe9042b18f2b477dc6c2233b988` |
| `Reproducibility Packet/scripts/utils/archive_units.py` | `79d8de45abf5d1cb5d177c325deb038067c06e4cfd4227f8fc01755df28aabc8` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `4345f0e3d029f1142a441ee0e777e3f8635ec9aa3223ad31cb2046082df83eb7` |
| `agents/Claude/tools/test_missing_depth.py` | `435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` |
| `agents/Claude/tools/test_measure_host_drift.py` | `c94609a4559cd98da96381f8e686c961f812536359a7cc1940134e981f54fa3a` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` (Draft 25, §17 only) | `f465d02b4df9bcea6be6ce3ba86f4ba7e16d53e08cd94aec2785e2a3985119bd` |

The unchanged approved `band_drift.py`, its harness and the RC-002 mutation
harness also authenticated at the card's recorded digests. No candidate file
was edited during review.

## Round 1 exhaustive ledger

The complete numbered ledger is appended to
`chats/Claude-Codex/Missing Depth Recovery Review/Missing Depth Recovery Review - Active.md`.
Under the superseding review-cycle method, Round 2 is delta-only against these
two findings plus regressions introduced by their repair.

### F1 — final console verdict contradicts the final disposition

On the whole-command support-invariance fixture, the structured record correctly
says `unmeasurable`, `advances=False`; the point gate itself correctly says
`passed=True`. The command prints the completion disposition, writes the report,
and then ends with the unqualified line:

`[drift] verdict: passed=True label=no time-ordered drift resolved`

That line comes from the raw point-gate object rather than `reconciled`. The owner
case asserts the record and report but does not capture or assert stdout. Repair
must make the terminal decision line report the reconciled final disposition,
label any retained point-gate line as diagnostic, and add a whole-command console
assertion that fails on the current state.

### F2 — retained masks are absent from the pre-read memory bound

`plan_transfer` still sizes resident arrays as `total_spikes * 16` plus the
largest stored slice, while the reader now returns and retains one boolean
`missing_depths` array per unit. Those masks are part of the processed-asset read,
which the command expressly places inside `--max-mib`, but they are not named in
`resident_bytes` or `peak_resident_bytes`.

The generated 3,600-spike fixture returns 3,600 omitted mask bytes. At rank-1
size the omitted retained term is 3,160,311 bytes. Repair must include the masks
in the pre-read resident/peak formula and printed decomposition, with exact
formula and just-below/just-above admission tests.

### Nonblocking accounting follow-up

The command's unconditional finite-only split also retains times/depths copies
beside the complete arrays: 57,248 bytes on the generated fixture and 50,561,280
bytes projected at rank-1 size. The current ceiling explicitly limits its scope
to the read, so this is not F2. Avoid the clean-record copy as an implementation
cleanup, and include all downstream copies if a later state claims a whole-command
memory ceiling.

## Evidence reproduced on the exact candidate

- `agents/Codex/tools/probe_rc005_round1.py --repo-root .`: exit 0; reproduces
  F1, F2 and the accounting follow-up from generated local HDF5 only.
- Independent mathematical stress: 120 generated fixtures and 1,080 finite
  completions, with **0 observation-bound escapes and 0 null-bound escapes**.
- `test_missing_depth.py --permutations 200 --completions 200`: **86 checks,
  0 failed**.
- `test_measure_host_drift.py`: **518 checks, 0 failed**; its own output visibly
  reproduces F1.
- unchanged `test_band_drift.py --permutations 200`: **103 checks, 0 failed**.
- `mutate_rc002_repairs.py --repo-root .`: **all 32 mutations detected and the
  unmutated control passes**.
- packet runbook checker: exit 0, ten steps agree and the drift command remains
  pending its first candidate report.
- candidate files plus the new probe compile cleanly.

Green aggregate suites do not override the two independently reproduced defects.
The interval construction itself survived the independent containment stress;
the returned verdict is about the wired command and reader state as a whole.

## Immediate owner and next review step

**Immediate owner: Claude.** Repair F1 and F2 on one exact state, rerun the
acceptance and mutation evidence, update RC-005's candidate table and explicitly
approve the repaired bytes, then hand that state back in the active review chat.

**Next Codex review:** Session 40, Round 2 delta-only. Authenticate every updated
digest, inspect only the F1/F2 repair deltas plus affected tests and regression
surface, reproduce the terminal console decision and mask-bound admission edges,
then issue explicit same-state approval or another bounded verdict. The Session-40
count-based progress report is due regardless of the review outcome.

## Approved foundation and downstream gates

- RC-001: Draft 24 `c35987fe…`, drift utility `eace4cd35…`, owner harness
  `946df906…`, closed `Approved`.
- RC-003: bounded archive reader closed `Approved` at its recorded nine-file
  state.
- RC-004: reference-instant pair check closed `Approved` at its exact five-file
  state.
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

After RC-005 closes, the order remains: resume rank-1 plan/measurement; approve
the exposure schedule and placement specification; approve matcher implementation
and tests; apply noise and effective-SNR host gates; calibrate footprint/placement;
freeze exact matching outputs; obtain independent balance/manipulation approval;
then seek separate generation and later Rung-0/sorter authorizations.

Ranks 5, 7, 9 and 13 remain separately paused on declared-clock disagreement.
The three-way Review Method Change chat remains active by Randy's instruction.
No new director decision is needed.

`agents/Codex/Session Summaries/HumanReport39.md` is the detailed record of the
review, probe, tests, append verification, public heartbeat and boundary.
