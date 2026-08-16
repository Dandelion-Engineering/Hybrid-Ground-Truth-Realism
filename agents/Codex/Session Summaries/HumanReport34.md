# Codex Human Report — Session 34

**Date and time:** 2026-08-16 06:20 PDT

**Phase:** Phase 2 — Execution

**Outcome:** RC-004 Round 1 is **Revisions Required**. I authenticated and
reviewed Claude's complete five-file candidate, reproduced its 436-check suite
and 30-of-30 mutation result, and found two independent blocking
counterexamples. A non-ISO/NWB timestamp separator reaches a drift verdict, and
the raw reference-time read happens before the caller's outer transfer ceiling.
Claude owns the Round-2 repair; the first candidate measurement remains blocked.

## Startup and controlling state

The automation gate named Codex and no `.agent-session.lock` existed. I created
the lock, reread `.agent-turn`, and confirmed it still named Codex before doing
project work. I followed `AgentPrompt.md`: read Project Details, Codex continuity,
all active Codex-participant chats and their summaries, Claude's Session-34
report, the complete RC-004 card and candidate, the superseding review method,
and the live-run README playbook. The tracked worktree was clean at `db8e8ca`
(`Claude Session 34`) before reviewer records were written. The next count-based
progress report remains due in Codex Session 40.

## Candidate authenticated

I recomputed all five SHA-256 digests and matched the card exactly:

- `Reproducibility Packet/scripts/utils/archive_units.py` —
  `261d93ccd94707bd0ee2d5eb418bec4281574dd46546ce0a98a4dd0fdf6491cc`;
- `Reproducibility Packet/scripts/measure_host_drift.py` —
  `c54216f28dcb9065dcd8953e05a39429a68ad6c00fbd389c6bffdc4ab5041ddf`;
- `agents/Claude/tools/test_measure_host_drift.py` —
  `bae016d9b7c8fd67279f79d9f8ffbdf7adfa01d7b96a27c7b9c68aeef6c9486f`;
- `agents/Claude/tools/mutate_rc002_repairs.py` —
  `985e3a3fdb5ba1c513c00c43508aea6a626ee42002cd8e70e4c3751c9e67b7b7`;
- `agents/Claude/tools/verify_rc003_round2_repairs.py` —
  `f4ee4ae651a03471c3d8abbd7a3a0e131f2d381219dd6691e113f349a018bf77`.

I reviewed the full changed surface from RC-003's approved `51cb436` state:
760 insertions and 148 deletions across those five files. I did not edit them.

## Owner evidence reproduced

- Acceptance suite: **436 checks, 0 failed**.
- Repair mutation harness: unmutated control green at 436; **30 of 30 caught**.
- Runbook-checker mutation harness: **18 of 18 caught**.
- Packet consistency: all ten implemented steps agree with their scripts;
  `measure_host_drift.py` remains pending as declared.
- RC-003 Round-1 verifier: exits 0 on all three constructions.
- RC-003 Round-2 verifier: the declared two failures are exactly the removed
  version-equality assertions; every other check passes, including the repaired
  block-expansion construction.
- Python byte-compilation: all five candidate files and the independent probe
  compile cleanly.

This is strong internal evidence. It does not establish approval because neither
independent construction is represented by the owner suite.

## Round-1 blocker RC-004-F1 — timestamp grammar

`reference_instant` claims to accept a complete ISO-8601/NWB timestamp and calls
`datetime.datetime.fromisoformat(value.strip())` directly. Python 3.12 documents
that this parser deliberately accepts any one Unicode character in place of the
ISO date/time `T` separator. The NWB schema specifies an ISO-8601 extended
date-time with offset for root `timestamps_reference_time`.

My generated local fixture places
`2021-05-10Q14:33:49.023776-04:00` on both assets. Both per-asset checks accept
it; the pair compares equal; the command exits 0 and writes a drift record. A
malformed declared origin has therefore become a verdict. This violates RC-004
A2.4 and blocking-severity item 1.

The repair must enforce the strict external grammar before parsing and add
adversarial near-miss coverage, including a non-ISO separator, that requires a
named input error with no report or record.

## Round-1 blocker RC-004-F2 — caller ceiling

The pre-review condition and card require both clock reads inside the caller's
outer transfer ceiling. The candidate instead calls raw `read_provenance` before
passing `--max-mib` only to processed `read_band_units`. `read_provenance` has no
outer-ceiling argument; its docstring says it runs before any ceiling exists,
and the CLI help and module narrative tell the operator that the raw reads are
not covered.

My generated local fixture uses `--max-mib 0.000001 --plan-only`. The raw clock
is read and printed and **23,920 distinct raw bytes move** before the processed
side refuses the one-byte ceiling. The whole-suite provenance invariant checks
the per-provenance sub-budgets only on cases that reach a record, so it cannot
catch this pre-record escape. This violates pre-review condition 5, card A2.5,
and blocking-severity item 3.

The repair must hold the caller's ceiling before the raw reference-time read,
correct the CLI/help narrative, and prove under a below-minimum ceiling that the
raw value is neither read nor printed before refusal.

## Independent probe and source check

I created `agents/Codex/tools/probe_rc004_round1.py`, SHA-256
`a48b5c5e500a268d79bab0515f415e34efa428f4459fc8b34cddd1119ded6305`.
It exits 0 after reproducing both blockers and uses local synthetic HDF5 fixtures
only. It reads no archive, network resource or candidate asset.

I checked the relevant semantics against the official NWB schema and Python
3.12 documentation and added both primary-source entries to
`agents/Codex/references.md`.

## Exact-state verdict and records

The complete numbered ledger is appended to
`chats/Claude-Codex/Session Reference Time Pair Check Review/Session Reference
Time Pair Check Review - Active.md`. The append used the UTF-8 physical tail,
recorded the 189-line pre-write count, matched a unique multi-line EOF anchor,
and then verified the Session-34 header occurs exactly once after the old line
count and that the physical tail ends in the new separator.

I changed RC-004's status to Round 1 `Revisions Required`, added the Round-1 row,
and left the card open. I added one lean public README heartbeat because the two
permission failures are genuinely noteworthy and preserve the no-result
boundary. The microsecond comparison resolution and root
`session_start_time` substitution remain nonblocking follow-up/preference items.
I found no third blocker in the full pass.

## Boundary and next owner

No candidate implementation file was edited. No archive, network resource or
candidate asset was read. No host is pinned; no candidate drift, noise or
effective-SNR value exists; no donor, exposure schedule, placement
configuration, Rung 0, generator or sorter result exists; and no scientific
result exists.

**Immediate owner:** Claude answers the numbered Round-1 ledger delta-only,
repairs F1 and F2, updates the tests/mutations and exact candidate hashes, and
hands the stable state back for Round 2. Candidate execution remains blocked
until explicit same-state approval.
