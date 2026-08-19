# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 50 · 2026-08-19.**

**Next Codex session will be Session 51. The next count-based director progress
report is Session 56; no event-triggered report was due in Session 50.**

## Immediate handoff

**Phase 2 — Execution and specification design. RC-008 remains closed at
`Split/Redesign Required`; Draft 34 remains frozen and unapproved.** The open
work is the materially changed Part-B resolution diagnostic, outside formal
review, in:

`chats/Claude-Codex/Part B Resolution Diagnostic Design/Part B Resolution Diagnostic Design - Active.md`

Claude Session 50 accepted Codex's dominance correction and independently
rebuilt all 1,024 split-family cells. The matrix contains 30 strict pairwise
dominance relations; the source claims *the family has no dominating member*
and *none dominates* are withdrawn. The rebuild also found 450 exact
`M = 2.0` ties, all on the passing side, so the constructed family cannot
support near-threshold claims.

Claude then found a separate frozen-specification defect: a constructed finite
retained-channel array can vary across the whole core while both chosen halves
have zero MAD. Its half-ratio is `0/0`, not `+inf`. On the constructed midpoint
step channel, exactly the sixteen even split-family members are undefined and
all sixteen odd members return 1.0. With eight undefined channels of 72,
NumPy produces `R_null_sampled = NaN`, `NaN > M` is false and Draft 34's branch
logic permissively returns `passes`. Python and NumPy sorts also disagree on
the nearest-rank position of NaN, so “sort ascending” does not define the case.

## Session-50 ruling and evidence

Codex reproduced both Claude probes and their TXT/JSON records byte-for-byte:

- `probe_split_family_narrowing.py`: **24/24**, records `4375175f…` /
  `1b9b3bd1…`;
- `probe_null_ratio_undefined.py`: **20/20**, records `5ff8e2fa…` /
  `5cc4d438…`.

Codex's reply agrees that failure semantics precede member choice, with three
separate layers:

1. finite, structurally valid input that yields `0/0` is **not an input error**;
2. the per-channel ratio remains explicitly **undefined**, published by
   channel/window, and is not coerced to 1, `+inf` or a library NaN order;
3. the band-level decision must be bounded without letting a non-value silently
   become non-voting, because Part A alone cannot certify a host.

The next design object is an **exact completion interval**. Treat each
undefined ratio as able to occupy `[0,+inf]`, derive the exact lower/upper
attainable nearest-rank `rho(k)`, and propagate the bounds through the maximum
over windows. Current design criterion, not yet a candidate:

- upper bound `<= M`: undefined entries are decision-irrelevant for branch 4,
  but remain published;
- upper bound above `M` or unbounded: an otherwise-passing Part A state is
  `unmeasurable`;
- Part-A homogeneity failure remains a failure; its Part-B label is `resolved`
  or `resolution-limited` only if the whole interval supports that comparison,
  otherwise the label remains unresolved.

The exact order-statistic bounds still need a proof and adversarial fixtures.
Only after that should any member or multi-member construction be compared
under one common semantics. Do not open a Review Card or new §19 draft yet.

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
split rationale fell. The later `0/0` finding belongs to the new Part-B design
boundary and does not reopen Draft 34 or RC-008.

## Next actions

1. Prove or refute exact completion bounds for nearest-rank `p90/p10` with
   `[0,+inf]` per-channel unknowns, including nonuniform finite ratios and the
   maximum over sixty windows.
2. Specify how those bounds grade both branch 4 and branch 3's label.
3. Grade every later fixed-member or multi-member proposal under that same
   semantics, before any candidate noise read.
4. Open formal review only after co-design yields a stable candidate. Its card
   must name `Supersedes: RC-008` and the Part-A/Part-B material change. A
   like-for-like fourth §19 repair is forbidden.
5. Keep rank 2 drift unmeasured; rank 1 has not been rejected.

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
  in Session 50.

## Director-facing state

`agents/Codex/Progress Reports/Progress Report Session 48.md` is the newest
Codex progress report. No new director decision is needed for the immediate
agent-only Part-B redesign. The older nonblocking Phase-1 contract-review
request remains open.

The only three-party active chat,
`chats/Claude-Codex-Human/Review Method Change/`, has no pending Codex response;
its newest entry is Codex Session 42. Randy requested that it remain active.

For the next Codex session, read this file, then `HumanReport50.md`, the Part-B
design chat and Claude's newest report. Use `references.md` rather than memory
for citations.
