# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 51 · 2026-08-19.**

**Next Codex session will be Session 52. The next count-based director progress
report is Session 56; no event-triggered report was due in Session 51.**

## Immediate handoff

**Phase 2 — Execution and specification design. RC-008 remains closed at
`Split/Redesign Required`; Draft 34 remains frozen and unapproved.** The open
work is the materially changed Part-B resolution diagnostic, outside formal
review, in:

`chats/Claude-Codex/Part B Resolution Diagnostic Design/Part B Resolution Diagnostic Design - Active.md`

Claude Session 51 proved the completion semantics Codex proposed in Session 50.
Codex Session 51 replayed Claude's 45/45 evidence byte-for-byte and independently
closed its stated production-size gap at the real 72-channel band. **No
mathematical blocker remains in the completion-bound rule.**

The next design object is the fixed-member or multi-member comparison under the
now-common completion semantics. Do not open a Review Card or edit section 19
until that comparison and the rest of the co-design produce a stable candidate.

## Completion rule now verified

Per-channel `0/0` from finite, structurally valid input is estimator
non-resolution, not an input error. It remains an explicit non-value, published
by channel and window, and is not coerced to `1`, `+inf` or a library NaN order.

Each undefined ratio is completed over `[0,+inf]`. For each window, compute the
exact lower and upper attainable nearest-rank p90/p10 ratio. Propagate both
through the maximum over windows. Branch 4 may stand down only when the
aggregate upper endpoint is at or below `M`; otherwise an otherwise-passing
Part-A state is `unmeasurable`.

For branch 3:

- `R_space_sampled` above the whole completion enclosure → `resolved
  heterogeneity`;
- `R_space_sampled` at or below the whole enclosure → `resolution-limited`;
- `R_space_sampled` inside it, or an unresolved band-level ratio → `unresolved`.

The third label is new vocabulary and must be explicit in the successor
candidate and card.

### Owner evidence

Claude's `probe_completion_bounds.py` passes 45/45. Codex replayed it from
source and reproduced the committed records exactly:

- TXT `d14c1471bca1623f7fe6f5280cec225bd5e66ec7f54222178e1caa2495c62b66`;
- JSON `bb9465f0657e51b6c9c87d80d8d3b79265e744aa2496ee8dde9ba2d886f8870f`.

The owner's key correction is load-bearing: the upper endpoint is attained at
zero/infinity vertices, but the lower endpoint often requires an interior
placement. A vertex-only minimum is wrong in the permissive label direction.

### Independent `n = 72` evidence

`agents/Codex/tools/probe_completion_bounds_n72.py` passes 11/11 without
importing Claude's implementation. It records:

- 24 full-size discrete rank patterns;
- 34,320 exhausted completion multisets;
- 512 continuous positive pools;
- 16,384 sampled interior completions;
- zero endpoint, witness, containment or threshold failures.

Script SHA-256:
`864b6e01dfc8006d22c6a64432e27eadce0117948ba433673735bcb7ede65490`.

For `u <= 7` and positive finite one-based `f[8]`:

- lower = `f[max(65-u, 8)] / f[8]`;
- upper = `max_{a=0..u} f[65-a] / f[8-a]`.

A zero or infinite rank-8 defined value is already withheld. For every
`u = 8..72`, one explicit eight-zero completion makes the band ratio infinite
or undefined, so the effective upper endpoint is unbounded.

The independent records are deterministic:

- `completion_bounds_n72_2026-08-19.txt` — `ce680287736e37f57389cfe61d5b8d75d6e1180a2a3a10e2607a8b418b3571f2`;
- `completion_bounds_n72_2026-08-19.json` — `20c6e963e53d122702e059ff737d08bd82c74f6964ec67eb8f799399545b4a34`.

The exactness claim is over the declared **per-ratio completion space**. It is
not a real-data frequency claim, a physical sample-perturbation model, or a
claim that every interior value is physically attainable.

## Successor-card scope ruling

Claude asked whether section 19.7's publication change stays with Part A or
belongs in Part B. Codex ruled:

**The successor card's Part B covers both section 19.6's decision vocabulary
and the Part-B-owned publication clauses inside section 19.7.** A rule and the
record required to audit it are one review object.

This does not move the whole section 19.7 heading into Part B. The future card
should state:

- in scope: Part-B estimator semantics, branch-3 labels, branch-4 rule,
  band-level `0/0` handling and new/changed publication fields;
- excluded but regression-checked: unchanged Part-A statistics, gates and
  publication fields.

When the candidate is stable, count every current-live Part-B statement in
sections 19.5, 19.6, 19.7 and 19.10 mechanically. Historical draft records stay
historical.

The minimum future publication surface is:

- undefined identities/counts per window;
- per-window lower, upper and undefined-reachable state;
- aggregate endpoints and endpoint-setting window identities;
- the band-level `0/0` state;
- raw per-half scales and defined per-window ratios already promised.

The scalar `R_null_sampled` cannot remain the only reported object.

## What remains open before formal review

1. Compare fixed-member and possible multi-member constructions under the same
   completion semantics.
2. Do not use the 32×32 constructed matrix to claim real-data frequency or to
   defeat a disclosed fixed convention by itself. It establishes decision
   sensitivity; its earlier no-dominance claim is withdrawn.
3. Decide the stable Part-B instrument and count every live surface it changes.
4. Only then open one successor card naming `Supersedes: RC-008` and the
   material Part-A/Part-B boundary. A like-for-like fourth section 19 repair is
   forbidden.

## Exact closed RC-008 state

- Draft 34 selection document:
  `ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89`;
- sections 1–16: 144,664 bytes / `700b3b9a…`;
- section 17: 21,864 bytes / `dc73b87f…`;
- section 18: 20,579 bytes / `8af3e62c…`;
- owner specification evidence: 241/241;
- closed RC-007 baseline: 288 checks with exactly 16 expected failures;
- repair mutations: 42/42 caught with a green control;
- owner Round-3 evidence: 32/32;
- Codex terminal evidence: 33/33;
- Claude Convergence-family evidence: 22/22.

The 9 pass/unmeasurable movements, 6 resolution relabels and 57 unchanged state
pairs remain valid reach evidence. The split rationale failed; the reach proof
did not. The later `0/0` and completion findings belong only to the new Part-B
design boundary and do not reopen RC-008.

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
  in Session 51.

## Director-facing state

`agents/Codex/Progress Reports/Progress Report Session 48.md` is the newest
Codex progress report. No director decision is needed for the immediate
agent-only Part-B redesign. The older nonblocking Phase-1 contract-review
request remains open.

The only three-party active chat,
`chats/Claude-Codex-Human/Review Method Change/`, has no pending Codex response;
its newest entry is Codex Session 42. Randy requested that it remain active.

The root public README's newest forward entry records the independent
production-size completion proof and explicitly preserves the no-measurement
boundary.

For the next Codex session, read this file, then `HumanReport51.md`, the Part-B
design chat and Claude's newest report. Use `references.md` rather than memory
for citations.
