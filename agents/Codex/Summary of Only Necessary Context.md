# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 49 · 2026-08-19.**

**Next Codex session will be Session 50. The next count-based director progress
report is Session 56; no event-triggered report was due in Session 49.**

## Immediate handoff

**Phase 2 — Execution and specification design. RC-008 is closed at
`Split/Redesign Required`; Draft 34 remains frozen and unapproved.** Claude's
Session-49 Convergence statement accepted Codex F8-R3 and proved the stronger
family fact: midpoint-contiguous (`p=6,510`) and even/odd (`p=1`) are two fixed
members of one 32-member block-interleaved family over the 13,020 retained
samples. On Draft 34's parity fixture, 16 family members produce `passes` and
16 produce `unmeasurable`. The failed parameter-count rationale cannot be
narrowed.

Clause 5 requires a material boundary change before another card:

- **Part A — split-independent gate:** the pinned preprocessing chain, sampling
  grid and coverage theorem, loud/quiet level extrema, `R_space_sampled`,
  branches 1–3 without branch 3's resolution label, thresholds, publication
  set and cost model.
- **Part B — resolution diagnostic:** `R_null_sampled`, branch 4, and branch
  3's resolution label.

**Part A alone cannot certify a host.** It is strictly more permissive than the
specified gate and authorizes no estimator, passing verdict, candidate noise
read or host decision.

## Session-49 cross-review finding

Claude's unreviewed `probe_split_family_sensitivity.py` reproduced byte-for-byte
at 12/12, and the separate Convergence probe reproduced byte-for-byte at 22/22.
The sensitivity probe's matrix is correct, but its interpretation is too
strong.

The probe infers “the family has no dominating member” because no member
withholds on all 32 constructed fixtures and no member withholds on none. Codex
inverted the same recorded matrix by member and found **30 strict pairwise
dominance relations**:

- `p=1` withholds on exactly the 16 odd-target fixtures and dominates every
  other odd member;
- `p=2` withholds on exactly the 16 even-target fixtures and dominates every
  other even member;
- `p=1` and `p=2` are incomparable, their signatures are disjoint, and their
  union covers all 32 constructed fixtures;
- each other odd member withholds on `{1,p}`; each other even member withholds
  only on `{p}`.

The self-target rows have sizes 16 for `p_t=1`, one for `p_t=2`, and two for
every other target. Therefore the sweep establishes decision sensitivity, all
32 self-hits, and the absence of one globally withholding/passing member. It
does **not** establish absence of dominance or, by itself, defeat the “pin one
and disclose it” reading. The two-member `p=1 OR p=2` envelope covers this
constructed fixture set, but that says nothing yet about real recordings.

Independent evidence is
`agents/Codex/tools/probe_split_family_dominance.py`: **12/12** against source
record SHA-256
`f51b4949e8406b7bb237a49ecb3af985ce5127896a680e28c58b67f06a9b4fcb`.
The correction is posted in
`chats/Claude-Codex/Part B Resolution Diagnostic Design/Part B Resolution Diagnostic Design - Active.md`.
This is open-ended pre-card design, not formal review. Claude should narrow the
source probe/report claims before using them as successor-card input.

## Exact closed RC-008 state

- Draft 34 selection document:
  `ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89`;
- §1–§16: 144,664 bytes / `700b3b9a…`;
- §17: 21,864 bytes / `dc73b87f…`;
- §18: 20,579 bytes / `8af3e62c…`;
- owner specification evidence: 241/241;
- closed RC-007 baseline: 288 checks with exactly 16 expected failures;
- repair mutations: 42/42 caught with a green control;
- owner Round-3 evidence: 32/32;
- Codex terminal evidence: 33/33;
- Claude Convergence-family evidence: 22/22.

The exact branch reach survives: 9 pass/unmeasurable movements, 6 resolution
relabels and 57 unchanged states, with no failure-boundary crossing. Only the
split rationale fell.

## Next actions

1. Claude should respond in the Part-B design chat, narrow the unreviewed
   sensitivity claims, and decide what evidence actually bears on whether a
   resolution diagnostic can be specified.
2. Open formal review only after open-ended co-design yields a stable candidate.
   The new Review Card must name `Supersedes: RC-008` and identify the
   Part-A/Part-B split as the material change. A like-for-like fourth §19 repair
   is forbidden.
3. Do not treat the `p=1/p=2` two-member envelope as a proposal or real-data
   result. It is a property of Claude's 32 constructed fixtures only.
4. Rank 2 drift remains available but unmeasured. Do not run it speculatively
   while rank 1 has not been rejected.

## Execution state that must not be broadened

No host-noise estimator exists, no candidate noise sample or value has been
read, no host is pinned, and rank 2 remains unmeasured. No host-dependent
manifest, donor assignment, Rung 0, hybrid generation or sorter run is
authorized.

Rank 1 has passed only the same-state-approved strict depth-trace statistic:
`Delta_10min = 1.821 µm` against 20 µm and `Q95_null = 0.526 µm`. Four host
gates remain open: noise, effective SNR, joint ten-placement feasibility and
balance. The result concerns label-blind units or clusters under the stated
common-movement assumption; it is not proof that the physical probe did not
move.

## Durable approved foundations

- Claim Sheet and Accessible Claim Sheet Amendments 1–6 are in force.
- RC-001, RC-003, RC-004 and RC-006 closed `Approved`; RC-005 closed
  `Approved with Follow-Ups`.
- RC-002 closed unapproved at Convergence; RC-007 closed `Revisions Required`;
  RC-008 closed `Split/Redesign Required` and its candidate is frozen.
- Tier A donor matching Draft 6 is same-state approved only as a pre-pool prose
  specification. Schedule/placement, implementation, exact host configuration,
  pool, balance and execution remain separate gates.
- `.gitattributes` remains same-state approved and reproduces the reviewed
  cross-platform bytes.
- The Reproducibility Packet remains co-owned. No packet or result file changed
  in Session 49.

## Director-facing state

`agents/Codex/Progress Reports/Progress Report Session 48.md` is the newest
Codex progress report. No new director decision is needed for the immediate
agent-only Part-B redesign. The older nonblocking Phase-1 contract-review
request remains open.

The only three-party active chat,
`chats/Claude-Codex-Human/Review Method Change/`, has no pending Codex response;
its newest entry is Codex Session 42. Randy requested that it remain active.

For the next Codex session, read this file, then `HumanReport49.md`, the Part-B
design chat, and Claude's newest report. Use `references.md` rather than memory
for citations.
