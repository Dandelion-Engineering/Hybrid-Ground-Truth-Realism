# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 44 · 2026-08-18.**

**Next Codex session will be Session 45. The next count-based progress report is
due in Session 48.**

## Current phase and controlling boundary

**Phase 2 — Execution and result review.** RC-007 remains open. Codex returned
Claude's authenticated Draft 30 owner response at Round 2 with
**`Revisions Required`**. Claude owns the final Round-3 response permitted by
the bounded review method.

This is not a measurement result. No host-noise estimator exists, no candidate
noise value has been read, no host is pinned, and rank 2 is unmeasured. Rank 1
has cleared only the previously approved strict drift gate. No host-dependent
manifest, donor assignment, generation, Rung 0, or sorter execution is
authorized.

## RC-007 Draft-30 exact state

The Round-2 candidate authenticated at all eight carded SHA-256 digests:

- selection Draft 30: `48de3825a6727962fb9e698669eddd2dead5ac5e21362bc90afc69fa69689964`
- filter probe: `ef96ce2120677dc3e1e6ee236b845a962c200f7228ef68dc86b5a6602f3c74ee`
- filter text/JSON: `dfcea89d463808b224355615491bdbfc6007ce6880208d3a16529fdbe4bbae23` /
  `b9f3e089e2b94e2d9e26743133d167bb258e3be169b5ce3f1b3fe625c7b72b15`
- specification checker/output: `9380458b083aca6b6a04ad4c4b665f27532343185d04ca1dc216cc22e7a2facf` /
  `a6027b1a53b1eebe8ae3ee4f88a2a991c2528f5a265518ad82907219146808d9`
- mutation harness/output: `a194d59e81ff8c3eff7e338ac7654b312471a0c82ba257ef53e30e23f3fb4f1b` /
  `9b5ca1647d8d309112a2423e820939c29c98c9fc1e9bb093072bacbecd82c963`

The owner checker passes **214/214**; the owner mutation harness catches
**27/27** with a green control. The recorded filter outputs reproduce. Frozen
selection spans remain §1–§16 `700b3b9a…` over 144,664 bytes, §17 `dc73b87f…`
over 21,864 bytes, and §18 `8af3e62c…` over 20,579 bytes.

Codex's delta probe `agents/Codex/tools/probe_rc007_round2.py` passes
**31/31**, SHA-256
`864c8d56ced613668b88c2104354dc9d5c9fda5b74ad5dc3a4c18cea057904ee`.
It reads no archive, candidate sample or network resource.

## Round-2 disposition

Accepted on their response boundaries:

- F1: lower/upper strict and relaxed verdict rules are explicit and aligned.
- F2: the peak-to-peak ceiling is declared conservative, not necessary.
- F3: input error, failed design and unmeasurable outcomes are reconciled.
- F5: the rounded-endpoint grid and 74.214-second coverage claim are proved.
- Owner-found repair: seven malformed-input conditions stop the queue rather
  than rejecting a host.
- Branch 2: an implausibly quiet result is accepted as a predeclared design
  failure rather than reclassified after measurement.
- F6 withdrawal: the proposed four-gate supersession is withdrawn in full;
  host admissibility remains five gates and no clause of §15.5 is superseded.

Two response-created blockers remain:

1. **F4-R1 — filter isolation is not generally bounded by the owner fixture.**
   Draft 30 correctly adopts the anchor Butterworth and automatic margin, but
   promotes the twelve-fixture `+1e-06` result into “the entire deviation.” A
   valid measured-lattice construction with centre-chunk 6-µV quantized noise
   and neighbouring plateaus at ±29,866 stored counts changes the retained MAD
   scale by **−0.228%** at one pinned seed and **+0.283%** at another when the
   centre chunk is filtered alone rather than in context; retained samples move
   by more than **0.547 µV**. A one-channel effect survives common median across
   384 channels. The final response must obtain real neighbours, prove a
   sufficient input class, or declare the isolation effect unknown/unbounded
   while retaining the owner fixture only as a diagnostic.
2. **F7-R1 — nonstationarity can deflate the split-half spread.** For 72 ratios
   `[0.5]×8, [1]×56, [2]×8`, nearest-rank p10/p90 gives spread 4. Reciprocal
   true temporal factors `[2]×8, [1]×56, [0.5]×8` make every observed ratio one
   and reduce the statistic to **1**. Within-window change can therefore cancel
   disagreement and manufacture a pass; the final response must withdraw the
   one-way claim and narrow what a low value supports.

One nonblocking clarification is tracked as **F6-R1**: §19.8 may state the
conditional aggregate arithmetic under its own thresholds, but Amendment 6
does not define a host-aggregate gate-3 precondition for that arithmetic to
discharge. The real gate-3 conditions remain later-pinned per site/donor.

## Owner response boundary

**Immediate owner: Claude.** Submit one exact final Round-3 response limited to
F4-R1 and F7-R1, while carrying F6-R1 as a clarification. A third non-approval,
a new blocker, or disagreement triggers the card's Convergence Decision; there
is no fourth repair exchange inside RC-007. Explicit same-state approval is
still required before the specification can close approved.

Do not measure rank-1 noise, write the estimator, read candidate samples, or
advance rank 2 as part of this response. The Review Method Change chat remains
active but has no outstanding director request.

## Approved foundation and downstream gates

- RC-001: drift definition and estimator closed `Approved`.
- RC-002: closed unapproved; its single successor RC-003 closed `Approved`.
- RC-004: session reference-instant check closed `Approved` at Round 2.
- RC-005: missing-depth recovery closed `Approved with Follow-Ups` at Round 2.
- RC-006: rank-1 drift measurement/report closed `Approved` at Round 2.
- RC-007: host-noise specification open; Round 2 is `Revisions Required`.
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

After one host passes all in-force gates, the order remains: approve the
exposure schedule and placement specification; approve matcher implementation
and tests; calibrate footprint/placement; freeze exact matching outputs; obtain
independent balance/manipulation approval; then seek separate generation and
later Rung-0/sorter authorizations.

`agents/Codex/Session Summaries/HumanReport44.md` is the detailed permanent
record. No Session-44 cadence report was due.
