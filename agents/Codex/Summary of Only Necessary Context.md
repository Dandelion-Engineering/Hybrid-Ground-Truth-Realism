# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 47 · 2026-08-19.**

**Next Codex session will be Session 48. A count-based director progress report
is due in Session 48.**

## Current phase and controlling boundary

**Phase 2 — Execution and specification review.** RC-008, the sole successor to
RC-007, remains open after **Round-1 and Round-2 `Revisions Required`** verdicts.
Draft 33 SHA-256 `16ee8f801d0a44b99de70c12da7f7d80b32a73325e720ab0236ad2180679f56e`
is frozen and unapproved. Claude owns the **final Round-3 response**.

If Round 3 does not reach explicit same-state approval, the agent-only
Convergence Decision fires. Under clause 5, a non-approval on RC-008 forbids a
second like-for-like successor; the work must then split or redesign with the
changed boundary named.

This remains a specification, not a recording result. No host-noise estimator
exists, no archive sample or candidate noise value has been read, no host is
pinned, and rank 2 is unmeasured. Rank 1 has cleared only the approved strict
drift gate. No host-dependent manifest, donor assignment, generation, Rung 0 or
sorter execution is authorized.

## Draft-33 authentication and reproduced evidence

All nine carded files authenticated:

- selection document `16ee8f80…`;
- specification checker `7574ac52…` and TXT/JSON `8f40c8cc…` / `20aea650…`;
- mutation harness `299be141…` and record `a6c0d943…`;
- owner Round-2 probe `aa6a4371…` and TXT/JSON `5f692ba5…` / `0d185bd3…`.

The frozen spans reproduce: §1–§16 144,664 bytes / `700b3b9a…`; §17 21,864 /
`dc73b87f…`; §18 20,579 / `8af3e62c…`.

Owner evidence reproduced:

- RC-008 checker: **168 / 168**;
- legacy RC-007 baseline: **288 checks, exactly 16 declared failures**;
- mutation harness: **27 / 27 caught**, green control;
- owner Round-2 evidence probe: **36 / 36**.

Codex's `agents/Codex/tools/probe_rc008_round2.py` passes **27 / 27**. Digests:

- probe: `50a57ddb9226bfc608692c3111340671f5c51d27424acbdd180ba4bdade13bc2`;
- text: `e721097e2eb6e8923e74fa1e6440a68af39bff569dfb05a74127171722f9b304`;
- JSON: `06cae35207022b8d1d6d848e6c0e7c70e39f01832b9fa083084d070ede0a4019`.

It reads no archive, candidate sample or network resource.

## Round-2 blocking findings

### F6-R2 — the replacement split rationale contradicts the decision

Draft 33 withdraws the false claim that interleaving always compresses
`R_null_sampled`, but its “decisive” replacement says reducing cancellation is
not a goal the rule can cash. The response's own values refute that. At
`R_space_sampled = 1.5`, `M = 2`:

- contiguous `R_null_sampled = 1` → **passes**;
- interleaved `R_null_sampled = 4` → **unmeasurable**.

The split difference can therefore withhold a would-be pass. The first
replacement ground is also not bounded: a 400.921659 Hz process, wholly above
300 Hz, can repeat exactly across both 6,510-sample halves; across phase the two
half-estimate series have correlation 1.0. High-pass frequency support does not
establish near-independence.

Claude may keep contiguous halves as a predeclared instrument parameter, but
must remove the two false grounds and state the choice at its real boundary, or
provide a bounded rationale that survives the counterexamples.

### F7-R2 — one legacy-checker input remains unauthenticated

`probe_rc007_spec.py` consumes
`Reproducibility Packet/results/host_timing_index.jsonl`. Draft 33's
`RC007_AUTHENTICATED` list pins five paths and omits that file. The mutation
harness copies it but never mutates it.

Codex staged a byte-different synthetic 21-series timing record preserving the
two aggregates the legacy checker consumes. The repaired wrapper still exited
zero at **168 checks, 0 failed**. This is the original F4-R1 defect class on an
unlisted record. Claude must authenticate the timing-index digest and add a
substitution mutation that reaches it.

## Tracked non-blocking delta findings

- **T5-R2:** §19.10 lists four sampled quantities and says a short excursion is
  invisible to “all three.”
- **T6-R2:** §19.3 now gives the lower floor a voting minimum but retains the
  stale sentence that §19.6 “does not lean on the floor.”
- **T7-R2:** the raw AP series declares no sampling rate, but §19.7 asks for the
  candidate's “own declared rate.” Name the whole-span derived timing-index
  rate if that is the intended diagnostic.

## What verified clean in the response

- F1-R1's floor now reads `sigma_quietest_sampled`; the upper ceiling remains
  on `sigma_worst_sampled`; no threshold value moved.
- F2-R1 is honestly declared as a nominal-rate deviation. The design
  coefficients differ by `1.31860735664e-07`; `padlen` remains 18 and the
  automatic margin remains 500 samples under the compared rates. Fixture sample
  effects are explicitly diagnostics, not bounds.
- F5-R1's bad-channel conservatism claim is withdrawn and the per-channel scale
  series is published for every window; no post-hoc detector threshold is added.
- T1-R1's coverage/dilution distinction and corrected 228.718-second number
  reproduce; T2-R1 through T4-R1 are taken on their stated boundaries.

## Immediate owner instructions

**Immediate owner: Claude.** Read RC-008 and the active Section 19 Convergence
Repair chat. Prepare the final Round-3 exact candidate that:

1. removes or bounds the two false split grounds while keeping any parameter
   choice at its honest boundary;
2. authenticates `host_timing_index.jsonl` and mutation-tests its substitution;
3. disposes of T5-R2 through T7-R2;
4. updates candidate digests and owner evidence before handoff.

Codex Session 48 should authenticate only that final delta. Approval requires
explicit same-state approval. If a blocker remains or a new blocker appears,
freeze the state and run the one-time Convergence Decision rather than opening
another repair round.

The Review Method Change chat remains active at Randy's request and has no
outstanding director action.

## Approved foundation and downstream gates

- RC-001: drift definition and estimator closed `Approved`.
- RC-002: closed unapproved; sole successor RC-003 closed `Approved`.
- RC-004: session reference-instant check closed `Approved`.
- RC-005: missing-depth recovery closed `Approved with Follow-Ups`.
- RC-006: rank-1 drift measurement/report closed `Approved`.
- RC-007: closed `Revisions Required`; Draft 31 frozen and unapproved.
- RC-008: open after Round-1 and Round-2 `Revisions Required`; Draft 33 frozen
  and unapproved; final owner response owed.
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

After one host passes all in-force gates, the order remains: approve the
exposure schedule and placement specification; approve matcher implementation
and tests; calibrate footprint/placement; freeze exact matching outputs; obtain
independent balance/manipulation approval; then seek separate generation and
later Rung-0/sorter authorizations.

`agents/Codex/Session Summaries/HumanReport47.md` is the detailed permanent
record. No Session-47 cadence report was due; Session 48 requires one.
