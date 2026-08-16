# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 33 · 2026-08-16 04:19 PDT**

**Next Codex session will be Session 34. The next count-based progress report is due in Session 40.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned;
no candidate has a drift, noise or effective-SNR value; no donor, host-specific
pool, exposure schedule, placement configuration, template array, Rung 0,
generation or sorter result exists.

RC-001's drift specification and RC-003's bounded archive reader are closed
`Approved` historical states. The first real plan-only use of RC-003 exposed a
new real-input defect in one approved pair condition. **Do not run the candidate
command again until a new RC-004 state has explicit same-state approval.**

## The Session-33 finding

Claude ran the pinned rank-1 plan-only command on CSHL047 / Probe01, session
`b52182e7-39f6-4914-9717-136db589706e`, under `--gate strict`. It authenticated
the raw source statement, derived the CA1 band and raw AP extent, then stopped
before reading any unit: raw names NeuroConv 0.9.2, processed names 0.9.4.

Claude measured the pair-version condition on the eleven distinct pinned-order
sessions plus a deterministic sixty-session holdout from the other 448 paired
sessions. Codex independently reconstructed the 459-session sampling frame,
verified the sixty-session draw exactly, and reran all 71 bounded remote reads.
The pinned report/records reproduced byte-for-byte. The holdout reproduced every
scientific and metadata value; one asset used one extra HTTP request while
transferring the same bytes.

Accepted combined result:

- raw → processed converter pair: 0.9.1 → 0.9.4 on 1; 0.9.2 → 0.9.4 on 70;
- converter-version agreement: **0 / 71**;
- parsed reference-instant delta: **0 seconds on 63; +3,600 seconds on 8**;
- no other delta, no session-ID mismatch, and
  `session_start_time == timestamps_reference_time` on all 142 assets;
- the eight differences are all NYU daylight-window sessions, but that pattern
  is descriptive and no daylight-saving mechanism was measured.

Evidence hashes:

- `agents/Claude/tools/probe_conversion_pairs.py` —
  `10ad5053a06ba35d32d17540a6511f459e2e6f72cd3fcbe613bbdc9af10873ec`;
- pinned report / records — `a9b1498682e616151d72913ccf4c98c2087c5bd611f2040290928251f681e952`
  / `54929196a9c520d9f72c84ce316e1c8121e01e22aa897c2f0b4c2f1a5d609430`;
- holdout report / records — `fc5ec92d60f9b9e2563b57f63a439866254293f3c3d8fbc169af3b13b079d712`
  / `9917c10cd354e15bb5bdc80a46f022adcd1cd05a04ff9ad1d91eb65377950a41`.

## Agreed RC-004 direction — pre-review, not approval

Claude owns the stable candidate and RC-004; Codex reviews it. RC-004 is a new
card based on evidence unavailable during RC-003, not a successor to closed
RC-003. **No RC-004 candidate or card exists yet.**

The agreed direction:

- keep whole-positive per-asset `general/source_script` authentication;
- keep both converter versions in the report and add 0.9.4 to the measured
  record;
- remove only converter-version equality's voting role;
- directly read both root `/timestamps_reference_time` values under bounded
  I/O and compare them as timezone-aware instants;
- a disagreement, missing/refused/malformed value or timezone-naive value is a
  pausing input error before any unit payload, report or drift verdict;
- equal instants written with different UTC offsets must pass;
- reference-time equality remains one necessary declared condition, not proof
  of the shared clock by itself; per-asset source authentication and later
  containment remain distinct evidence;
- clock reads must be inside the request/transfer budgets and the caller's outer
  transfer ceiling, and their spend must be represented in the plan/report.

The card must digest every changed implementation, test, mutation and runbook
state. No Claim Sheet amendment is needed: §16.4 already makes an unestablished
common clock a pausing input error and does not commit to version equality.

## Do not read the later affected candidates now

The one-hour declared-reference disagreements include pinned ranks 5, 7, 9 and
13: NYU-65, NYU-45, NYU-39 and NYU-48. **They remain paused, not rejected.**

Claude proposed comparing raw AP extent with processed spike-time range on
NYU-65 to learn whether the stored arrays align despite the metadata. Codex did
not authorize that read now. It is rank 5, rank 1 remains unresolved, and the
diagnostic is unnecessary to repair rank 1. Even aligned numeric ranges would
not erase the files' declared reference-instant disagreement; recovering that
class would need a separate evidence-backed rule when the pinned order reaches
it. Do not reveal later-candidate payload out of order and do not place this
diagnostic inside RC-004.

## Approved foundation and current code state

RC-003 remains closed `Approved` at its recorded exact nine-file state. The two
primary approved hashes are unchanged:

- `Reproducibility Packet/scripts/utils/archive_units.py` —
  `96a31b3d46e18a7f387cc5d9d5c3fe37984f1346139477deb57f8f062ce1556e`;
- `Reproducibility Packet/scripts/measure_host_drift.py` —
  `0bf08153fde8b48a6485596c6b8375920fe56d33a66fd0a35c41833f484335e5`.

That state still gates on pair-version equality. Treat it as authenticated
history, not as authorization to continue candidate execution after the new
evidence. RC-001 remains approved on Draft 24 `c35987fe…`, drift utility
`eace4cd35…`, and owner harness `946df906…`.

All six Claim Sheet amendments remain `In force`. Contract hashes remain:

- `Claim Sheet.md` — `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`;
- `Accessible Claim Sheet.md` — `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`.

The real-arm donor-matching prose remains same-state approved at Draft 6
`51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`.
Sections 1–16 of Claude's selection document remain approved. None of those
approvals authorizes exact host-dependent placement or matching, generation or
sorting.

## Active records and next action

- `chats/Claude-Codex/Session Clock Agreement/Session Clock Agreement -
  Active.md` holds Claude's measurement and Codex's independent acceptance,
  RC-004 boundary and no-NYU-65 ruling.
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change -
  Active.md` remains active by Randy's instruction. Its newest observation says
  a synthetic review can prove dependence on a proxy without showing the proxy
  has a nonempty or discriminating real population. No Randy decision is needed.
- Root `README.md` already carries Claude's accurate public heartbeat for the
  0/71 proxy failure and 8/71 declared-clock disagreements. Do not duplicate it.
- The Phase-1 director contract-review request remains open and nonblocking.

**Immediate owner:** Claude creates a stable RC-004 candidate and card, then
hands it to Codex with explicit approval. **Immediate Codex role:** perform the
Round-1 full-artifact review only after that handoff. Until then there is no
formal review and no executable candidate state.

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

`agents/Codex/Session Summaries/HumanReport33.md` contains the complete replay,
decision, card boundary, append checks and next-owner reasoning.
