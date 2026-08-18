# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 46 · 2026-08-18.**

**Next Codex session will be Session 47. The next count-based progress report is
due in Session 48.**

## Current phase and controlling boundary

**Phase 2 — Execution and specification review.** RC-007 closed
`Revisions Required` by explicit two-agent consensus. RC-008 is its sole
like-for-like successor under `Playbooks/review-cycle.md` clause 5. RC-008
Round 1 returned **`Revisions Required`** on Draft 32 with five blocking and
four tracked findings. Draft 32 is frozen and unapproved; Claude owns the
Round-2 response.

This is not a recording result. No host-noise estimator exists, no archive
sample or candidate noise value has been read, no host is pinned, and rank 2 is
unmeasured. Rank 1 has cleared only the approved strict drift gate. No
host-dependent manifest, donor assignment, generation, Rung 0, or sorter
execution is authorized.

## Draft-32 exact state and reproduced evidence

RC-008 authenticates six files. The selection document is Draft 32, SHA-256
`6933c89ec561a7a9bc3201ea332ed7a6698f179af65cde49621cb0fddaec0db7`.
The other five carded digests matched. Frozen spans remain §1–§16
`700b3b9a…` over 144,664 bytes, §17 `dc73b87f…` over 21,864 bytes, and §18
`8af3e62c…` over 20,579 bytes.

Owner evidence reproduced:

- RC-008 checker: **57 / 57**, exit 0;
- legacy RC-007 baseline: **288 checks with exactly six declared failures**,
  exit 1;
- RC-008 mutation harness: **12 / 12 caught**, green control.

Codex's `agents/Codex/tools/probe_rc008_round1.py` passes **32 / 32**. Digests:

- probe: `7352afab46034dd7057f4aba4dae45a2532729d747287c867ab14acb7eb06f2f`;
- record: `dad99817d0698819fd39f1bf9aa953f9ca19780bff137aa85decb354d5ba4a0d`.

It authenticates Draft 32, invokes the owner checker, and reproduces all five
concrete counterexamples. It reads no archive sample, candidate noise value or
network resource.

## Round-1 blocking findings

### F1-R1 — lower floor uses the loudest sampled window

Section 19 uses `sigma_worst_sampled = max_k S(k)` for both the upper ceiling
and lower anti-saturation floor. A fixture with 59 windows at `1 µV` and one at
`5 µV` passes the strict branch, even though every quiet window violates the
lower floor and gives `A_min / S(k) = 50 > 40`. Use a quietest sampled
statistic for the lower floor, or narrow the guarantee so it does not claim to
protect every sampled placement.

### F2-R1 — nominal-rate design contradicts exact filter identity

Pinned SpikeInterface 0.104.8 designs `FilterRecording` coefficients from
`recording.get_sampling_frequency()`. Draft 32 fixes nominal `30,000 Hz`; the
rank-1 timing index records `30,000.039869961383 Hz`. SOS coefficients differ by
`1.31860735664e-07` and a deterministic retained signal differs by
`3.56153236218e-05 µV`. Use the recording rate, or declare the nominal-rate
deviation and narrow the exact-identity claim.

### F3-R1 — interleaving need not compress the split spread

A periodic 72-channel construction gives contiguous `R_null = 1` and even/odd
interleaved `R_null = 4`. If another interleaving scheme was intended, it was
not pinned. Keep contiguous halves only with a bounded rationale or support a
precisely defined alternative; remove the universal permissive-direction
claim.

### F4-R1 — regression checker can green for the wrong reason

In a staged candidate, change parameter-table `K` from `60` to `61` and replace
the unauthenticated legacy checker with a counterfeit printing the expected six
failures and summary. The outer RC-008 checker still exits zero at **57 / 57**.
Pin the legacy executable and record digests, require its expected process
semantics including nonzero exit, and add substitution/undeclared-change
mutation coverage.

### F5-R1 — an extreme bad channel can make the gate permissive

For a 72-channel vector with 8 values at `1`, 56 at `2`, and 8 at `3`,
`p90/p10 = 3` and strict `M = 2` fails. Replacing one low value with `100`
moves the ratio to `1.5`, flipping failure to pass. Add defensible bad-channel
handling/bounds, or remove the claim that leaving bad channels unmasked is
conservatively directed and account for the permissive failure mode.

## Tracked non-blocking findings

- **T1-R1:** distinguish clustered coverage loss from three-core statistical
  aggregation/dilution in §19.9.
- **T2-R1:** update §19.10's stale current-state sentence from Draft 31.
- **T3-R1:** say stored-code step(s), not stored bit(s).
- **T4-R1:** restrict phase-omission upward bias to the shared-component model
  unless the stronger final nonlinear statistic direction is supported.

No fifth live contradiction was found in the repaired `R_null_sampled` branch
surfaces; those four Draft-32 surfaces agree with the ordered branches.

## Immediate owner instructions

**Immediate owner: Claude.** Read RC-008 and the active Section 19 Convergence
Repair chat. Respond explicitly to F1-R1 through F5-R1 and dispose of T1-R1
through T4-R1. Prepare a fully authenticated exact Round-2 candidate outside
the frozen Draft-32 bytes, update the checker and mutation coverage, and record
the response/digests in RC-008 before handing it back.

Codex Session 47 should authenticate the complete owner response and perform a
Round-2 delta review. Approval requires explicit same-state approval; a green
owner suite or silence is not approval. If RC-008 eventually reaches a
non-approval terminal disposition, clause 5 forbids another like-for-like
successor and requires a named split/redesign.

The Review Method Change chat remains active but has no outstanding director
request.

## Approved foundation and downstream gates

- RC-001: drift definition and estimator closed `Approved`.
- RC-002: closed unapproved; its sole successor RC-003 closed `Approved`.
- RC-004: session reference-instant check closed `Approved`.
- RC-005: missing-depth recovery closed `Approved with Follow-Ups`.
- RC-006: rank-1 drift measurement/report closed `Approved`.
- RC-007: closed `Revisions Required`; Draft 31 frozen and unapproved.
- RC-008: open after Round-1 `Revisions Required`; Draft 32 frozen and
  unapproved; owner Round-2 response owed.
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

After one host passes all in-force gates, the order remains: approve the
exposure schedule and placement specification; approve matcher implementation
and tests; calibrate footprint/placement; freeze exact matching outputs; obtain
independent balance/manipulation approval; then seek separate generation and
later Rung-0/sorter authorizations.

`agents/Codex/Session Summaries/HumanReport46.md` is the detailed permanent
record. No Session-46 cadence report was due.
