# Codex Human Report — Session 33

**Date and time:** 2026-08-16 04:19 PDT

**Phase:** Phase 2 — Execution

**Outcome:** I independently accepted Claude's 71-session clock measurement and
the decision it supports. Raw/processed NeuroConv version equality admits **0 of
71** measured sessions, while the files' directly declared reference instants
agree on **63 of 71** and differ by exactly **+3,600 seconds on 8 of 71**. A new
Claude-owned, Codex-reviewed RC-004 will replace only the pair-version proxy;
RC-003's approved code remains unchanged and candidate execution is blocked
until a new state is explicitly approved.

## Startup and controlling state

The automation gate named Codex and no `.agent-session.lock` existed. I created
the lock, reread `.agent-turn`, and confirmed it still named Codex before doing
project work. I then followed `AgentPrompt.md`: read Project Details, Codex's
continuity, every relevant chat summary, both active Codex-participant chats,
Claude's Session-33 report and continuity, the complete Claim Sheet including
all six in-force amendments, the superseding review method, the card template,
and the relevant implementation and first-candidate evidence.

The tracked worktree was clean at `f48920b` (`Claude Session 33`) before I wrote
the reviewer records. No count-based progress report is due until Codex Session
40.

## What Claude handed back

RC-003's first real use was the pinned rank-1 `--plan-only` command on CSHL047 /
Probe01, session `b52182e7-39f6-4914-9717-136db589706e`, under the strict gate.
It authenticated the raw source statement, derived the CA1 band and raw AP
extent, then stopped before reading any unit because the raw asset names
NeuroConv 0.9.2 and the processed asset names 0.9.4.

Claude preserved both approved files and measured the proxy instead of deleting
the blocking line. His evidence covered the eleven distinct sessions in the
pinned thirteen-candidate order plus a deterministic sixty-session holdout from
the other 448 paired sessions. He proposed keeping whole-positive per-asset
conversion authentication, recording both converter versions, and replacing
version equality with equality of the root `/timestamps_reference_time` values
as timezone-aware instants.

## Independent authentication and reproduction

I authenticated Claude's probe and evidence files:

- `agents/Claude/tools/probe_conversion_pairs.py` — SHA-256
  `10ad5053a06ba35d32d17540a6511f459e2e6f72cd3fcbe613bbdc9af10873ec`;
- pinned report / records — `a9b1498682e616151d72913ccf4c98c2087c5bd611f2040290928251f681e952`
  / `54929196a9c520d9f72c84ce316e1c8121e01e22aa897c2f0b4c2f1a5d609430`;
- holdout report / records — `fc5ec92d60f9b9e2563b57f63a439866254293f3c3d8fbc169af3b13b079d712`
  / `9917c10cd354e15bb5bdc80a46f022adcd1cd05a04ff9ad1d91eb65377950a41`.

From the pinned 2,048-asset cache I independently reconstructed **459** sessions
with exactly one raw and one processed NWB. The recorded holdout list is exactly
the sixty lowest SHA-256 ranks under its declared seed after removing the eleven
pinned sessions. It has sixty unique entries and no overlap with the hypothesis-
forming set.

I then reran the bounded remote probe on all 71 sessions with the project venv.
The replay read **74,186,752 bytes in 1,133 requests**. The pinned report and JSON
reproduced byte-for-byte. The holdout replay reproduced every asset, source
statement, version, clock value, comparison and transferred-byte count. Its only
diff was one processed DY-011 asset using ten HTTP requests rather than the
saved nine while transferring the same 589,824 bytes. That retry count changes
no measured value or bound.

Parsing every saved reference value as a timezone-aware instant reproduced:

| Quantity | Result |
|---|---|
| Raw → processed converter pair | 0.9.1 → 0.9.4 on 1; 0.9.2 → 0.9.4 on 70 |
| Converter-version agreement | **0 / 71** |
| Reference-instant delta | **0 s on 63; +3,600 s on 8** |
| Other delta | **none** |
| Within-asset `session_start_time == timestamps_reference_time` | **142 / 142** |
| Raw/processed session-ID mismatch | **0 / 71** |
| String equality disagreeing with instant equality in this set | **0 / 71** |

The eight disagreements are the reported NYU daylight-window cases. I accept
that as a measured pattern and do not treat it as a measured daylight-saving
mechanism.

## Decision

I accepted all three requested decisions in the active Session Clock Agreement
chat:

1. **The measurement is accepted.**
2. **Pair-version equality must lose its voting role.** It admits none of the
   measured population and cannot distinguish the eight direct declared-clock
   disagreements from the sixty-three agreements. Per-asset positive conversion
   authentication remains; both versions remain reportable; 0.9.4 joins the
   measured-version record.
3. **Claude owns the stable candidate and RC-004; Codex reviews it.** RC-004 is a
   new card against new real-input evidence, not a successor to closed RC-003.

I recorded a concrete pre-review acceptance boundary: equal instants must pass
despite unequal versions; different textual offsets denoting one instant must
pass; a one-hour difference must pause before unit payload or verdict; missing,
refused, malformed or timezone-naive values must be input errors; both clock
reads must remain inside declared request/transfer and outer-ceiling accounting;
and the report must not promote reference-time equality into proof of the shared
clock by itself. The card must digest every changed implementation, harness,
mutation and runbook state.

No Claim Sheet amendment is required. The in-force design already says that an
unestablished common clock is a pausing input error and does not name converter-
version equality as its test.

## The affected-candidate diagnostic stays out of order

Claude asked whether to compare the raw AP extent with the processed spike-time
range on NYU-65, one of the one-hour cases. I did **not** authorize it now and
kept it out of RC-004. NYU-65 is rank 5; rank 1 is still unresolved, and the
payload read is unnecessary to repair rank 1's path. Even if the stored numeric
ranges align, the two assets still declare different reference instants, so
admitting them would require a separate evidence-backed recovery rule rather
than an exception hidden inside RC-004. Ranks 5, 7, 9 and 13 remain paused.

## Review-method observation

I appended the result to the active three-way method chat. The lesson is not
that RC-003 needed an unbounded fourth round: another pass over the same
synthetic fixtures would still not reveal that the proxy's real population was
empty. The useful habit is to test what a proxy admits and rejects on real
inputs whenever the represented property is directly readable and the check is
safe and bounded. The review method then did its other job correctly: Claude
preserved the approved bytes, returned the new evidence to the reviewer, and
opened a bounded new-card path instead of silently hotfixing closed work.

## Files changed and validation

- Appended Codex's evidence acceptance and RC-004 boundary to
  `chats/Claude-Codex/Session Clock Agreement/Session Clock Agreement - Active.md`.
- Appended the method observation to
  `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md`.
- Updated `agents/Codex/README.md`, created this report, and rewrote Codex's
  continuity file.
- Both chat appends used the physical-tail, pre-write line-count, unique EOF
  anchor and post-write single-header checks. Their Codex headers occur exactly
  once after the recorded pre-write line counts.
- The public README already carries Claude's accurate 71-session heartbeat, so
  I did not add a duplicate entry.
- No dependency was installed, no unit payload was read, and no heavy compute
  ran. The machine reported 14,388 MB free physical memory of 32,425 MB near
  closeout; the replay was bounded metadata I/O rather than a heavy step.

## Boundary and next owner

No host is pinned. No candidate has a drift, noise or effective-SNR value. No
donor, exposure schedule, placement configuration, Rung 0, generator or sorter
result exists, and no scientific result exists.

Claude's next action is to create a stable RC-004 candidate and Review Card at
the agreed narrow boundary. Until that state receives explicit same-state
approval, the current approved code still gates on converter-version equality
and the first candidate command remains blocked. Codex's next substantive role
is the RC-004 Round-1 full-artifact review after Claude's handoff.
