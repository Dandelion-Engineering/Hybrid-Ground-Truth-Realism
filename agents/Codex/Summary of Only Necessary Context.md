# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 34 · 2026-08-16 06:20 PDT**

**Next Codex session will be Session 35. The next count-based progress report is due in Session 40.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned;
no candidate has a drift, noise or effective-SNR value; no donor, host-specific
pool, exposure schedule, placement configuration, template array, Rung 0,
generation or sorter result exists.

RC-001's drift specification and RC-003's bounded archive reader are closed
`Approved` historical states. RC-004's candidate is open and **not approved**.
Do not run the rank-1 candidate command until RC-004 receives explicit same-state
approval.

## RC-004 Round 1 — Revisions Required

Claude handed off a five-file candidate that keeps affirmative per-asset
conversion authentication, replaces raw/processed converter-version equality
with equality of their declared root `timestamps_reference_time` instants, and
keeps both versions reportable but non-voting.

Codex authenticated the candidate hashes recorded in RC-004 and reviewed the
full 760-insertion / 148-deletion surface from RC-003's approved `51cb436` state.
The owner evidence reproduces:

- acceptance suite: **436 checks, 0 failed**;
- repair mutation harness: **30 of 30 caught**, unmutated control green;
- runbook-checker mutation harness: **18 of 18 caught**;
- packet consistency: ten implemented steps agree, drift measurement pending;
- RC-003 Round-1 verifier green; Round-2 verifier has exactly the two declared
  version-equality failures and no others.

The full Round-1 pass found two blockers.

### RC-004-F1 — permissive timestamp grammar

`archive_units.reference_instant` calls `datetime.fromisoformat` directly.
Python intentionally accepts any one Unicode character in place of the ISO
date/time separator. A local synthetic pair carrying
`2021-05-10Q14:33:49.023776-04:00` on both assets is accepted and reaches a drift
record. NWB requires an ISO-8601 extended date-time with an offset, so a malformed
input becomes a verdict. This violates A2.4 and blocking-severity item 1.

Required repair boundary: validate the strict NWB/ISO lexical form before
parsing and add adversarial near-miss coverage, including the non-ISO separator,
that requires a named input error with no report or record.

### RC-004-F2 — raw reference time outside caller ceiling

`measure_host_drift.main` reads and prints raw provenance/reference time before
passing `--max-mib` only to the processed `read_band_units` call.
`read_provenance` has no caller-ceiling argument and explicitly runs before any
outer ceiling exists. Under `--max-mib 0.000001 --plan-only`, a local synthetic
fixture reads and prints the raw clock and moves **23,920 distinct raw bytes**
before the processed side refuses the one-byte ceiling. This violates the exact
pre-review condition 5, A2.5 and blocking-severity item 3.

Required repair boundary: hold the caller's ceiling before the raw
reference-time read, correct the help/narrative, and add a below-minimum refusal
test proving the raw reference value is not read or printed before refusal.

Both constructions live in `agents/Codex/tools/probe_rc004_round1.py`, SHA-256
`a48b5c5e500a268d79bab0515f415e34efa428f4459fc8b34cddd1119ded6305`.
The probe is local and synthetic; it reads no archive, network resource or
candidate asset. No third blocker was found. The microsecond resolution and root
`session_start_time` substitution remain follow-up/preference class.

## Active review and immediate owner

`chats/Claude-Codex/Session Reference Time Pair Check Review/Session Reference
Time Pair Check Review - Active.md` contains the complete numbered Round-1
ledger. RC-004's status is `Revisions Required` and its exact five-file candidate
is unapproved.

**Immediate owner:** Claude responds to F1 and F2 delta-only under the superseding
review method, updates the stable candidate, tests, mutations and hashes, and
hands the exact state back. **Immediate Codex role:** perform the Round-2 delta
review only after that handoff. Candidate execution stays blocked in the
meantime.

`chats/Claude-Codex-Human/Review Method Change/` remains active by Randy's
instruction. No new Randy decision is needed.

## Real-input context that must not be lost

The first RC-003 rank-1 plan-only attempt stopped before unit payload because raw
names NeuroConv 0.9.2 and processed names 0.9.4. Claude and Codex independently
measured 71 paired sessions:

- converter-version agreement: **0 / 71**;
- declared-reference-instant delta: **0 seconds on 63; +3,600 seconds on 8**;
- no other delta; within-asset `session_start_time == timestamps_reference_time`
  on all 142 assets; no session-ID mismatch.

The eight one-hour cases are a descriptive NYU daylight-window pattern, not a
measured daylight-saving mechanism. Pinned ranks 5, 7, 9 and 13 remain paused,
not rejected. Do not read their spike payload or run the proposed containment
diagnostic out of order; recovering that class needs separate evidence if the
pinned order reaches it.

## Approved foundation

RC-003 remains historical approval at its recorded exact nine-file state. RC-001
remains approved on Draft 24 `c35987fe…`, drift utility `eace4cd35…`, and owner
harness `946df906…`. All six Claim Sheet amendments remain `In force`; contract
hashes remain `2feda611…` and `679918f7…`. The real-arm donor-matching prose
remains same-state approved at Draft 6 `51adae4b…`. None of those approvals
authorizes host-dependent placement or matching, generation or sorting.

Root `README.md` now carries one lean public heartbeat for the two RC-004 Round-1
blockers. No public result is claimed.

## Downstream gates remain separate

1. RC-004 implementation approval;
2. rank-1 candidate plan-only measurement in the pinned order;
3. exposure-schedule/placement specification, implementation, tests and approval;
4. matcher implementation, exhaustive/mutation tests and approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact candidate sites, T/K/N, U/Z/R, edge table, matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. generation authorization;
10. Rung 0/sorter execution authorization.

`agents/Codex/Session Summaries/HumanReport34.md` contains the complete Round-1
review, evidence, append verification and next-owner boundary.
