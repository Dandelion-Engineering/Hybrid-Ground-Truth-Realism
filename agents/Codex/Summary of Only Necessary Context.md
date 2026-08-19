# Summary of Only Necessary Context - Codex

**Rewritten at the end of Codex Session 52 - 2026-08-19.**

**Next Codex session will be Session 53. The next count-based director progress
report is Session 56; no event-triggered report was due in Session 52.**

## Immediate handoff

**Phase 2 - Execution and specification design. RC-008 remains closed at
`Split/Redesign Required`; Draft 34 remains frozen and unapproved.** The open
work is the materially changed Part-B resolution diagnostic, outside formal
review, in:

`chats/Claude-Codex/Part B Resolution Diagnostic Design/Part B Resolution Diagnostic Design - Active.md`

Claude Session 52 supplied the fixed-member and multi-member comparison Codex
requested. Codex Session 52 replayed it exactly, accepted its constructed-state
findings, and answered Claude's policy question.

**Codex supports one fixed member, `p = 6510`, but only under a narrowed
estimand: early-versus-late disagreement inside the sampled 0.434-second
window.** It is not a generic, partition-invariant estimator-resolution measure.
Codex does not support unanimity or a value-dependent selector as the gate on
the current evidence. Claude's response to this ruling is the next dependency.

Do not edit Section 19, open the successor Review Card, read candidate noise or
measure rank 2 before reading Claude's response.

## Why the completion rule does not select a split

Claude's `probe_member_comparison.py` passes 37/37 and reproduced byte-for-byte
for Codex:

- source `b653bc0c214f6a0c419489bafde244185d4bd61acc882b64e9edd2baa75a6f42`;
- TXT `f0eb1435ec802b93952bb3b155c6d61e0203be8321253c7d4d945b42576b487a`;
- JSON `4a86a090386bedd89f2d176abfdf0652ba3fe7f1bb3e29dd800d73b09e14b4fd`.

The load-bearing constructed result is a 72-contact ramp band with no undefined
or infinite ratio under any family member. Twenty-eight members stand down and
four (`p = 1085, 1302, 2170, 6510`) withhold at strict `M = 2`; reported values
range from 1.8 to 3.343026 and none is on the threshold. The completion rule is
never invoked, so its exactness cannot settle member choice.

Other accepted findings:

- the undefined-member set depends on channel shape, not one parity class;
- finite values are member-dependent as well as undefined identities;
- where finite values are held fixed and one member alone has undefined
  channels, the bounded rule makes the undefined-producing member never more
  permissive;
- unanimity is the verdict of the per-band largest upper bound, existential is
  the smallest, and one member can set unanimity;
- no member is largest on all thirty constructed bands;
- the Session-51 publication endpoints expose the ramp disagreement.

All claims remain bounded to constructed channels and ratio pools. They say
nothing about real-recording frequency.

## Codex Session-52 policy evidence and ruling

`agents/Codex/tools/probe_part_b_policy.py` authenticates Claude's exact source
and JSON record, then independently derives the family masks. It passes 11/11.

Exact states:

- script `9af55db6033d10384b72ffd4493a31b679e1be945806d6cc1531abaa3aaa4360`;
- TXT `c94fd91f2657188c8fe96043979c25b1f050bc6ed684ce9e9c4fe6656d7e8407`;
- JSON `5c9407d14b971c8180893655eb6c2d6916150b5a41efbaf6d71bbfa7b3f3b281`.

The script compiles, exits zero, renders a 15-line ASCII-only help surface and
writes deterministic LF-only records.

It establishes:

- all 32 members divide the 13,020 samples into equal 6,510-sample sets;
- `p = 6510` is uniquely the member whose two sets are both contiguous
  intervals, first half then second half;
- choosing minimum temporal fragmentation therefore selects it from declared
  geometry alone, before any candidate value;
- every other member produces at least four alternating runs;
- on the ramp band, value minimization is existential and stands down, while
  value maximization is unanimity and withholds;
- geometry selects `p = 6510` regardless of the values, and it happens to
  withhold on the ramp, so the rationale is not a convenient passing result.

### Policy ruling

1. **Primary member:** `p = 6510`, because it uniquely answers an interpretable
   temporal question: early-versus-late repeatability.
2. **Narrow the name and claim:** use a name such as
   `R_early_late_sampled`; explicitly state that low values certify nothing,
   periodic blindness remains possible, and no partition-invariance is claimed.
3. **Keep completion semantics:** finite valid `0/0` stays a published non-value;
   exact per-window completion endpoints are computed; branch 4 stands down
   only when the aggregate upper endpoint is at or below `M`.
4. **Reject unanimity as this gate:** it is a worst-member functional over a
   storage-length divisor family and changes the estimand without evidence that
   all 32 contrasts are necessary replicas of one scientific property.
5. **Reject data-dependent selection for now:** if a selector reads member
   values it needs its own scientific target and selection-aware evidence or an
   independent held-out basis; if it reads geometry only, it reduces to a fixed
   pin.
6. **The family remains design evidence, not a runtime voting rule.**

This is one agent's design ruling, not same-state approval. Wait for Claude.

## Completion semantics that remain verified

Each valid-input `0/0` per-channel ratio stays undefined and may occupy any
point in `[0,+inf]` in the declared completion space. It is not an input error,
`1`, `+inf`, or a library NaN-order convention.

At `n = 72`, nearest ranks are 8 and 65. For `u <= 7` with positive finite
one-based `f[8]`:

- lower = `f[max(65-u, 8)] / f[8]`;
- upper = `max_{a=0..u} f[65-a] / f[8-a]`.

Eight or more undefined contacts make the effective upper endpoint unbounded.
A zero or infinite defined rank-8 value is already withheld. Branch 4 may stand
down only when the maximum per-window upper endpoint is at or below `M`.

The exactness boundary is the abstract per-ratio completion space, not a
frequency claim, physical sample-perturbation model or claim that every interior
value is physically attainable.

Codex's independent production-size evidence remains:

- `probe_completion_bounds_n72.py` 11/11;
- 24 full-size patterns, 34,320 exhausted completion multisets;
- 512 continuous pools and 16,384 interior completions;
- records `ce680287...` / `20c6e963...`.

## Future candidate and card scope

If Claude accepts the narrowed fixed-member ruling, first mechanically enumerate
every current-live Part-B statement in Sections 19.5, 19.6, 19.7 and 19.10.
The forward rewrite must align the name, claim, branches and publication fields.
Historical draft records remain historical.

The successor card's Part B covers both decision semantics and the Part-B-owned
publication clauses. It should eventually state:

- in scope: the early/late estimator semantics, completion bounds, branch-3
  vocabulary, branch-4 rule, band-level `0/0` disposition and new/changed
  publication fields;
- excluded but regression-checked: unchanged Part-A statistics, gates and
  publication fields.

Minimum Part-B publication remains:

- split member and exact two interval definitions;
- undefined channel identities/counts per window;
- each window's lower, upper and undefined-reachable state;
- aggregate endpoints and endpoint-setting windows;
- band-level `0/0` state;
- raw per-half scales and all defined per-window values.

Do not open the Review Card in the session that first constructs the revised
argument. Let the candidate receive a later stability pass.

## Exact closed RC-008 state

- Draft 34 selection document:
  `ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89`;
- Sections 1-16: 144,664 bytes / `700b3b9a...`;
- Section 17: 21,864 bytes / `dc73b87f...`;
- Section 18: 20,579 bytes / `8af3e62c...`;
- owner specification evidence: 241/241;
- closed RC-007 baseline: 288 checks with exactly 16 expected failures;
- repair mutations: 42/42 with a green control;
- owner Round-3 evidence: 32/32;
- Codex terminal evidence: 33/33;
- Claude Convergence-family evidence: 22/22.

RC-008 stays frozen and unapproved. The later completion and member-policy work
belongs only to the redesigned Part-B boundary and does not reopen it.

## Execution state that must not broaden

No host-noise estimator exists, no candidate noise sample or value has been
read, no host is pinned, and rank 2 remains unmeasured. No host-dependent
manifest, donor assignment, Rung 0, hybrid generation or sorter run is
authorized.

Rank 1 has passed only the same-state-approved strict depth-trace statistic:
`Delta_10min = 1.821 um` against 20 um and `Q95_null = 0.526 um`. Four host
gates remain open: noise, effective SNR, joint ten-placement feasibility and
balance. The result concerns label-blind units or clusters under the declared
common-movement assumption; it is not proof that the physical probe did not
move.

## Durable approved foundations

- Claim Sheet and Accessible Claim Sheet Amendments 1-6 are in force.
- RC-001, RC-003, RC-004 and RC-006 closed `Approved`; RC-005 closed
  `Approved with Follow-Ups`.
- RC-002 closed unapproved at Convergence; RC-007 closed `Revisions Required`;
  RC-008 closed `Split/Redesign Required` and its candidate is frozen.
- Tier A donor matching Draft 6 is same-state approved only as a pre-pool prose
  specification. Schedule/placement, implementation, exact host configuration,
  pool, balance and execution remain separate gates.
- `.gitattributes` remains same-state approved and reproduces reviewed
  cross-platform bytes.
- The Reproducibility Packet remains co-owned. No packet or result file changed
  in Session 52.

## Director-facing and public state

`agents/Codex/Progress Reports/Progress Report Session 48.md` is the newest
Codex progress report. No director decision is needed for immediate Part-B
co-design. The older nonblocking Phase-1 contract-review request remains open.

The three-party `Review Method Change` chat has no pending Codex response and
must remain active at Randy's request.

The root public README's newest forward entry is Claude Session 52's member
comparison. Codex did not add a second entry because the underlying evidence is
already public and the fixed-member ruling still awaits Claude.

For the next Codex session, read this file, then `HumanReport52.md`, Claude's
newest report and the physical tail of the active Part-B chat. Use
`references.md` rather than memory for citations.
