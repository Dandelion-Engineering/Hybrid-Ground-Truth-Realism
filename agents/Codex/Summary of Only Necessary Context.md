# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 43 · 2026-08-18.**

**Next Codex session will be Session 44. The next count-based progress report is
due in Session 48.**

## Current phase and controlling boundary

**Phase 2 — Execution and result review.** RC-007 is open. Codex returned the
authenticated Draft 29 specification at Round 1 with **`Revisions Required`**;
Claude owns the bounded response.

This is not a measurement result. No host-noise estimator exists, no candidate
noise value has been read, no host is pinned, and rank 2 is unmeasured. Rank 1
has cleared only the previously approved strict drift gate. No host-dependent
manifest, donor assignment, generation, Rung 0, or sorter execution is
authorized.

## RC-007 candidate and exact-state evidence

RC-007 covers §19 of `agents/Claude/Tier A Host and Injection Zone
Selection.md` Draft 29 plus the raw-layout probe and the owner specification
checker/mutation instruments. Draft 29 authenticated at SHA-256
`d0fdd4626bc3680313ddbae122a10e157d7b8efbbd9f6847752a1379fabc5bd8`;
all seven accompanying card digests also matched.

The owner checker passed **99/99** and the owner mutation harness caught **11 of
11** mutations with a green control. Codex independently replayed the layout
probe against rank 1: **192 requests, 12,582,912 bytes**, and both recorded
outputs reproduced byte-for-byte. AST inspection and replay found no
Python-level sample slice. These checks authenticate the submitted state; they
do not overcome the specification defects below.

`agents/Codex/tools/probe_rc007_round1.py` authenticates the candidate and
reproduces the counterexamples at **12 checks, 0 failed**, SHA-256
`70fc0a3a1ae8ab916b87329a931aea03b557a89ee5ab768703b11bd612883a15`.

## Round-1 blocking findings

1. **Level rule:** §19 declares
   `1.25 µV ≤ sigma_worst ≤ 10.0 µV`, but the pass rule tests only the upper
   bound. The relaxation prose also says stale `12.5 → 25.0 µV`. The green
   owner checker misses both.
2. **Convention direction:** because `snr_peak ≤ snr_p2p`, a peak-to-peak
   ceiling of 40 is sufficient for a single-sided peak ceiling of 40, not
   necessary. A `+30σ/-20σ` waveform is the direct counterexample.
3. **Verdict precedence:** `R_space > M` and `R_null > M` simultaneously yield
   failed homogeneity and unmeasurable. The owner must reconcile the branches
   and define zero/non-finite denominator handling.
4. **Preprocessing claim:** the official anchor uses a fifth-order Butterworth
   high-pass applied forward and backward with `scipy.filtfilt`; it is not a
   causal recursive comparison. A rectangular DFT high-pass has a global
   periodic impulse response, not contamination confined to the 150 discarded
   edge samples.
5. **Sampling scope:** sixty fixed windows cover 60 of 9,999 full chunks. An
   unsampled one-chunk excursion is invisible, so the result is worst sampled
   window, not a guarantee “wherever the segment lands.”
6. **Supersession:** Claim Sheet Amendment 6 still makes effective host SNR a
   per-donor hard host-specific eligibility gate that determines `N`. Calling
   the rendered quantity donor-level does not remove its host-admissibility
   effect, and aggregate noise does not replace the donor/site predicate.

One nonblocking clarification is tracked: two temporal halves are not known to
have identical true per-channel scale under within-window nonstationarity;
`R_null` can be described as a conservative disagreement diagnostic without
that stronger construction claim.

## Owner response boundary

**Immediate owner: Claude.** Respond inside RC-007 to each numbered finding and
submit one exact repaired candidate. The response should keep the gate fixed
before any candidate value is exposed. In particular it must not measure rank
1 noise, implement the estimator, or advance rank 2 as part of the prose repair.

The current card remains open after Round 1; there is no approval to carry
forward. If the owner changes the decision quantity materially, the full
response-created surface remains reviewable under the card. The Review Method
Change chat remains active but has no outstanding director request.

## Approved foundation and downstream gates

- RC-001: drift definition and estimator closed `Approved`.
- RC-002: closed unapproved; its single successor RC-003 closed `Approved`.
- RC-004: session reference-instant check closed `Approved` at Round 2.
- RC-005: missing-depth recovery closed `Approved with Follow-Ups` at Round 2.
- RC-006: rank-1 drift measurement/report closed `Approved` at Round 2.
- RC-007: host-noise specification open; Round 1 is `Revisions Required`.
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

After one host passes all in-force gates, the order remains: approve the
exposure schedule and placement specification; approve matcher implementation
and tests; calibrate footprint/placement; freeze exact matching outputs; obtain
independent balance/manipulation approval; then seek separate generation and
later Rung-0/sorter authorizations.

`agents/Codex/Session Summaries/HumanReport43.md` is the detailed permanent
record. No Session-43 cadence report was due.
