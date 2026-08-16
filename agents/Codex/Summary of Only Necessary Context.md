# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 35 · 2026-08-16 08:19 PDT**

**Next Codex session will be Session 36. The next count-based progress report is due in Session 40.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned;
no candidate has a drift, noise or effective-SNR value; no donor, host-specific
pool, exposure schedule, placement configuration, template array, Rung 0,
generation or sorter result exists.

RC-001's drift specification and RC-003's bounded archive reader remain closed
`Approved` historical states. RC-004's technical review is complete and Codex
has explicitly approved its corrected exact state, but the card is still open:
Claude has not yet explicitly approved those same hashes. Do not run the rank-1
candidate command until Claude supplies that approval and RC-004 closes
`Approved`.

## RC-004 Round 2 — reviewer Approved, owner approval still required

Claude's repair closes both Round-1 blockers:

1. `reference_instant` now applies a whole-value ISO/NWB lexical gate before
   `datetime.fromisoformat`. The malformed `Q` separator is refused, while all
   79 distinct reference strings recorded across the 142 census assets remain
   admitted as timezone-aware instants.
2. `read_provenance` now holds the caller's declared ceiling around the raw file
   open and provenance read. A below-file ceiling refuses before any distinct
   byte moves or the raw clock is printed.

Codex authenticated and explicitly approved this exact five-file state:

- `Reproducibility Packet/scripts/utils/archive_units.py` — `9ef16f58…`;
- `Reproducibility Packet/scripts/measure_host_drift.py` — `156f6f0f…`;
- `agents/Claude/tools/test_measure_host_drift.py` — `c508233d…`;
- `agents/Claude/tools/mutate_rc002_repairs.py` — `97860ad9…`;
- `agents/Claude/tools/verify_rc003_round2_repairs.py` — `f4ee4ae6…`.

Evidence reproduced against those bytes:

- owner acceptance suite: **472 checks, 0 failed**, 82 cases;
- repair mutation harness: unmutated control 472 / 0, **32 of 32 caught**;
- Round-1 probe no longer reproduces either counterexample;
- new `agents/Codex/tools/probe_rc004_round2.py` at `f6b2aa6f…` passes five
  independent checks: exact census-set reconstruction, full-population
  admission, malformed-separator refusal, exact-ceiling admission and
  one-byte-short pre-transfer refusal;
- RC-003 Round-1 verifier remains green; the Round-2 verifier has only its two
  declared superseded version-equality failures; packet consistency remains ten
  implemented steps agreeing and the drift command pending; changed Python
  sources byte-compile and `git diff --check` is clean.

The processed-side before-first-fetch property is correctly retained at the
direct API layer. The raw read is now earlier and larger, so no whole-command
ceiling can admit it while refusing the processed asset's first smaller fetch.
This is a faithful split of the two boundaries, not a weakening.

## Remaining gate and immediate owner

`chats/Claude-Codex/Session Reference Time Pair Check Review/Session Reference
Time Pair Check Review - Active.md` contains Codex's explicit exact-state
approval and full evidence. The append was hard-gated against the verified
455-line UTF-8 tail; the new header occurs exactly once after that count and the
physical tail ends in the required separator. A boundary correction noting the
official NWB web read was separately hard-gated against the 523-line tail and
also occurs exactly once after it.

**Immediate owner: Claude.** Claude must explicitly approve the same five hashes.
His Round-2 handoff and digest correction publish the candidate but do not count
as same-state approval. Once he approves, RC-004 can close `Approved` without a
third technical round; only then can Claude proceed to the separately governed
rank-1 plan-only measurement. Codex should not redo the technical review unless
the candidate bytes move.

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

## Approved foundation and public state

RC-003 remains historical approval at its recorded exact nine-file state.
RC-001 remains approved on Draft 24 `c35987fe…`, drift utility `eace4cd35…`, and
owner harness `946df906…`. All six Claim Sheet amendments remain `In force`;
contract hashes remain `2feda611…` and `679918f7…`. The real-arm donor-matching
prose remains same-state approved at Draft 6 `51adae4b…`. None authorizes
host-dependent placement or matching, generation or sorting.

No root `README.md` entry was added this session. The reviewer approval is not
yet card closure, so the public heartbeat remains at the Round-1 blockers until
the owner supplies the missing approval and the gate actually closes.

## Downstream gates remain separate

1. Claude's explicit RC-004 same-state approval and card closure;
2. rank-1 candidate plan-only measurement in the pinned order;
3. exposure-schedule/placement specification, implementation, tests and approval;
4. matcher implementation, exhaustive/mutation tests and approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact candidate sites, T/K/N, U/Z/R, edge table, matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. generation authorization;
10. Rung 0/sorter execution authorization.

`agents/Codex/Session Summaries/HumanReport35.md` contains the complete Round-2
review, evidence, append verification, approval distinction and next-owner
boundary.
