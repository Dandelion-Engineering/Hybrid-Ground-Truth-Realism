# Codex Human Report — Session 35

**Date and time:** 2026-08-16 08:21 PDT

**Phase:** Phase 2 — Execution

**Outcome:** RC-004's Round-2 technical review is **`Approved` by the reviewer**.
Both Round-1 blockers are repaired, the authenticated state passes 472 checks,
all 32 repair mutations, and five new independent delta checks. The card remains
open only because Claude has not explicitly approved the same exact five-file
state. The rank-1 candidate remains blocked until he does and the card closes.

## Startup and controlling state

The automation gate named Codex and no `.agent-session.lock` existed. I created
the lock, reread `.agent-turn`, and confirmed it still named Codex before doing
project work. I followed `AgentPrompt.md`: read Project Details, Codex
continuity, all active Codex-participant chats and their summaries, Claude's
Session-35 report, the complete RC-004 card, the Round-2 candidate delta, and the
superseding review method. The tracked worktree was clean at `525d25e` (`Claude
Session 35`) before reviewer records were written. The next count-based progress
report remains due in Codex Session 40.

## Exact candidate authenticated

I recomputed and matched the five current candidate digests:

- `Reproducibility Packet/scripts/utils/archive_units.py` —
  `9ef16f58cbd46ece7753406790a1b3d578efaf03df6311024c62e4c0e7b7e6e0`;
- `Reproducibility Packet/scripts/measure_host_drift.py` —
  `156f6f0ffb0d13b7b3c871c29e7f516d93da65cadd4cbc742d7113fe132cf450`;
- `agents/Claude/tools/test_measure_host_drift.py` —
  `c508233d9c2d5c5567ca6875e8ebd22b1823b3ab7dff2aeac52044847305349a`;
- `agents/Claude/tools/mutate_rc002_repairs.py` —
  `97860ad978bf6bd2fd6851033405c7b9e1cf51aacb0c44332344fd64d92bcf49`;
- `agents/Claude/tools/verify_rc003_round2_repairs.py` —
  `f4ee4ae651a03471c3d8abbd7a3a0e131f2d381219dd6691e113f349a018bf77`.

The first digest is Claude's corrected post-handoff digest, not the superseded
`4192f345…` value. I reviewed the corrected comments and executable delta; no
candidate file was edited in this session.

## Round-2 finding verification

### F1 — strict external grammar before parsing

`reference_instant` now matches the whole stripped value against
`REFERENCE_TIME_FORM` before calling `datetime.fromisoformat`. The exact
Round-1 `Q` construction is refused, the named error boundary remains intact,
and impossible calendar values remain parser refusals inside the lexical form.

I independently reconstructed the reference-string population from
`conversion_pairs_pinned_2026-08-16.json` and
`conversion_pairs_sample60_2026-08-16.json`. It contains exactly 79 distinct
values and is exactly equal to the frozen owner-suite tuple: no missing and no
extra values. All 79 parse to timezone-aware instants under the repaired code.

I also checked the external boundary against the official version-pinned NWB
2.9 root schema. It defines `timestamps_reference_time` as ISO-8601 extended
date-time with an offset and gives `Z` and colon-offset examples. I added that
version-pinned source to `agents/Codex/references.md`. No stricter rule was
inferred from the measured population.

### F2 — raw provenance inside the caller ceiling

`read_provenance` now enters `_ceiling_budget` before the raw file is opened and
holds it through provenance extraction. `measure_host_drift.main` passes the
same `--max-mib` ceiling used for the processed read and turns refusal into a
named raw-input error.

My independent block-caching construction admits a ceiling exactly equal to the
local synthetic file's size and, one byte below that size, refuses in
`PREFLIGHT_SCOPE` before any distinct byte transfers. Claude's extended
whole-command case separately proves that the below-minimum refusal prints no
raw clock and moves zero bytes on either asset.

I accept the processed-side before-first-fetch check at the direct API layer.
The raw read is now encountered first and is larger, so no whole-command ceiling
can admit it while refusing the processed asset's first smaller fetch. The two
tests now isolate the two layers honestly; this is not weakened coverage.

## Evidence reproduced

- Acceptance suite: **472 checks, 0 failed**, 82 cases, 16.7 s.
- Repair mutation harness: unmutated control **472 / 0**; **32 of 32 caught**,
  including Round-2 mutations F1p and F1q.
- Round-1 reviewer probe: neither counterexample reproduces;
  `raw_distinct_bytes=0`.
- New `agents/Codex/tools/probe_rc004_round2.py`, SHA-256
  `f6b2aa6f13111987f0c3705e877b68d73d4b746d1154ebab4bb1b7341bca429f`:
  **5 checks green** using recorded census JSON and local synthetic HDF5 only.
- RC-003 Round-1 verifier: exits 0. Round-2 verifier: exactly the two declared,
  superseded version-equality failures and no others; block expansion remains
  zero distinct bytes.
- Packet runbook consistency: ten implemented steps agree; the drift command
  remains pending its first real execution.
- Python byte-compilation and `git diff --check`: clean.

No blocking finding remains, and the delta review found no new blocker.

## Exact-state verdict and the remaining gate

I appended the full evidence and an explicit **reviewer `Approved`** verdict to
`chats/Claude-Codex/Session Reference Time Pair Check Review/Session Reference
Time Pair Check Review - Active.md`. The append was hard-gated against the
verified 455-line UTF-8 tail; the Session-35 header occurs exactly once after
that count and the physical tail ended in the required separator.

I then corrected one overly broad boundary sentence by append only: this session
did read the official NWB schema over the web, although no computational probe
made a network request. That correction was separately hard-gated against the
523-line tail, occurs exactly once after it, and leaves the physical tail at the
required separator.

The Review Card and its index now say **Open — Round 2 reviewer `Approved`;
awaiting Claude's explicit same-state approval**. I did not close or rename the
chat. Claude's handoff and digest correction publish the candidate, but neither
is explicit approval under the project's gate. Once he approves the same five
hashes, the card can close without another technical round. Candidate execution
remains blocked until then.

## Public heartbeat and boundary

I did not add a root `README.md` entry. Reviewer approval without owner approval
is not card closure, so the public heartbeat should not imply that the gate has
closed.

The independent probe read only the two recorded census JSON reports and
generated local HDF5. I read the official NWB schema over the web for the source
check, but no DANDI archive asset, candidate asset or spike payload was read. No
host is pinned; no candidate drift, noise or effective-SNR value exists; no
donor, exposure schedule, placement configuration, Rung 0, generator or sorter
result exists; and no scientific result exists.

## Files created or updated

- `agents/Codex/tools/probe_rc004_round2.py` — five-check independent delta
  probe.
- `agents/Codex/references.md` — version-pinned NWB 2.9 root-schema link and
  clarified timestamp boundary.
- `chats/Claude-Codex/Session Reference Time Pair Check Review/…Active.md` —
  exact-state reviewer approval and boundary correction appended.
- `Review Cards/RC-004 Session Reference Time Pair Check.md` and
  `Review Cards/README.md` — reviewer-approved/open-owner-gate status.
- `agents/Codex/README.md` and `Summary of Only Necessary Context.md` — current
  state and next-owner continuity.
- `agents/Codex/Session Summaries/HumanReport35.md` — this report.

**Immediate owner:** Claude explicitly approves the same five hashes, closes
RC-004, and only then decides the separately governed rank-1 plan-only step.
