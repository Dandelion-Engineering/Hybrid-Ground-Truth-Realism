# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 45 · 2026-08-18.**

**Next Codex session will be Session 46. The next count-based progress report is
due in Session 48.**

## Current phase and controlling boundary

**Phase 2 — Execution and result review.** RC-007 is in its bounded
**Convergence Decision** after the final Round-3 review. Draft 31 is frozen and
unapproved. Codex has recorded `Revisions Required`; Claude owns the one
remaining convergence statement and explicit terminal consensus or smallest
safe counterproposal. There is no fourth repair exchange inside RC-007.

This is not a measurement result. No host-noise estimator exists, no candidate
noise value has been read, no host is pinned, and rank 2 is unmeasured. Rank 1
has cleared only the approved strict drift gate. No host-dependent manifest,
donor assignment, generation, Rung 0, or sorter execution is authorized.

## Draft-31 exact state and reproduced evidence

All eight carded candidate digests matched. The selection document is Draft 31,
SHA-256 `24e78a5ad139245b197286edd1acaf8bea42bc75af3378883b3180d29a923755`.
The frozen selection spans remain §1–§16 `700b3b9a…` over 144,664 bytes, §17
`dc73b87f…` over 21,864 bytes, and §18 `8af3e62c…` over 20,579 bytes.

Owner evidence reproduced:

- specification checker: **288/288**;
- mutation harness: **52/52 caught**, green control;
- owner Round-3 probe: **27/27**, regenerated TXT/JSON byte-identical.

Codex's `agents/Codex/tools/probe_rc007_round3.py` passes **39/39**. Digests:

- probe: `e4966b533aa39a506f8768dc8238e6ae547269568e0fe96f4e23bb62e2939feb`;
- record: `9f841c130f5477b488cedc79e61e8677b33f0f5c297e1ffa95f59d69b1c31a1b`.

It authenticates Draft 31, reproduces accepted repairs, and evaluates the
ordered-branch contradiction. It reads no archive, candidate sample, network
resource, or result.

## Accepted Round-3 repairs

- **F4-R1:** each centre chunk is filtered with 500 real samples on both sides,
  then those margins are stripped. The isolated-window construction is gone;
  residual fixture values are diagnostics, not a bound.
- Exact SpikeInterface 0.104.8 source confirms fifth-order SOS Butterworth,
  `sosfiltfilt`, the five-period automatic high-pass margin, real neighbouring
  samples and post-filter stripping. At 300 Hz / 30 kHz the margin is 16.667 ms
  or 500 samples.
- The tight coverage theorem is **170 chunks / 73.780 seconds**; a 169-chunk
  run can miss every sampled centre.
- The 180-chunk transfer projection is **957,031,364 bytes**.
- **F6-R1:** the undefined aggregate gate-3 discharge is withdrawn.
- **F7-R1:** the monotonic nonstationarity claim is withdrawn; low
  `R_null_sampled` certifies nothing.

## New Round-3 blocker F7-R2

Draft 31 says in its status line, §19.5 and §19.10 that high
`R_null_sampled` withholds the measurement. Section 19.5 calls
`R_null_sampled > M` sufficient.

The ordered branches test homogeneity first:

- `R_space_sampled <= M`, `R_null_sampled <= M` → passes;
- `R_space_sampled <= M`, `R_null_sampled > M` → unmeasurable;
- `R_space_sampled > M`, low null → fails on homogeneity;
- `R_space_sampled > M`, high null → also fails on homogeneity.

The high/high state therefore fails rather than being withheld. This changes
whether the host queue advances. The universal high-null claim was introduced
in Draft 31 and was absent from Draft 30.

The defect is narrow: the branch list is explicit and no threshold or
arithmetic is wrong. It is still blocking because the prose and executable
order declare different scientific dispositions and do not tell an implementer
which one to preserve.

## Convergence Decision state

Codex's four-field statement is in RC-007:

- minimum shippable claim: accepted F4-R1, coverage/cost, F6-R1 and low-null
  limits; not the complete disposition;
- controlling evidence: the high/high truth-table case and three universal
  withholding surfaces;
- strongest evidence against: explicit ordered branches make this a local
  prose defect;
- safe disposition: **`Revisions Required`**, freeze Draft 31, close unapproved
  once Claude concurs.

The repair must occur outside RC-007 before a new review. Either condition the
withholding claim on `R_space_sampled <= M`, or give high null precedence and
make high/high unmeasurable. Reconcile status, boundary, branch and checker
surfaces. Also settle the tracked contiguous-versus-interleaved split before
the estimator's first run. At most one successor may name
`Supersedes: RC-007`.

## Immediate owner instructions

**Immediate owner: Claude.** Read the Codex statement in RC-007 and the active
Host Noise Gate chat. Write one convergence statement with the same four
fields, then explicitly concur with `Revisions Required` or state the smallest
safe counterproposal. Do not edit Draft 31 as another response round.

If consensus is reached, record the terminal disposition, close RC-007 and
conclude the chat. Then reconcile the defect outside formal review and, if the
repair will be reviewed, open the sole successor card before any estimator or
candidate-noise run.

The Review Method Change chat remains active but has no outstanding director
request.

## Approved foundation and downstream gates

- RC-001: drift definition and estimator closed `Approved`.
- RC-002: closed unapproved; its sole successor RC-003 closed `Approved`.
- RC-004: session reference-instant check closed `Approved`.
- RC-005: missing-depth recovery closed `Approved with Follow-Ups`.
- RC-006: rank-1 drift measurement/report closed `Approved`.
- RC-007: open only for Convergence Decision consensus; Draft 31 frozen and
  unapproved.
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

After one host passes all in-force gates, the order remains: approve the
exposure schedule and placement specification; approve matcher implementation
and tests; calibrate footprint/placement; freeze exact matching outputs; obtain
independent balance/manipulation approval; then seek separate generation and
later Rung-0/sorter authorizations.

`agents/Codex/Session Summaries/HumanReport45.md` is the detailed permanent
record. No Session-45 cadence report was due.
