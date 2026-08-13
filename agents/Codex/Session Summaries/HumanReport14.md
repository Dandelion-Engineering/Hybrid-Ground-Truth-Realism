# Human Report 14 — Codex

**Current date and time:** 2026-08-13 01:10 PDT

**Session:** Codex Session 14

**Phase at start:** Phase 2 — Execution. Amendments 1–5 were `In force`; Amendment 6 had been proposed and handed to Codex for exact-state review. No host-specific eligible pool, rendered edge table, selected donor, generator run, Rung 0 or sorter run existed.

**Phase at end:** unchanged. Amendment 6 remains `Proposed`, but Codex has completed its review, repaired two defects and explicitly approved the revised synchronized state. Claude owner re-review is the remaining step before the amendment can enter force. The donor-matching rule remains Draft 2 and intentionally blocked until that convergence.

**Progress-report trigger:** none. Session 14 is not a multiple of eight, no phase closed and no amendment entered force. The next count-based report is Session 16.

---

## Summary

This session reviewed Claude's proposed Amendment 6, which generalizes Tier A from a hard sixteen target donors to the `N = 10…16` CA1 donors that survive host-specific eligibility. The amendment's central choice is correct: the in-force contract already says Tier A survives losing as many as six of sixteen donors, so the arm sizes, exposure schedule, pseudo-arms and claim boundary must remain defined throughout that range rather than failing on the first loss.

I accepted all three design choices Claude specifically asked me to resist: separating per-donor gates from the joint ten-placement host gate; fixing the extra-occurrence identities and donor-to-block deal before the survivors are known; and computing Amendment 5's uniform-draw diagnostic at actual arm size `N`. Independent checks reproduced both SHA-256-derived seeds and verified the quotient/remainder rota for every admissible `N`.

I did not approve Claude's handed-off bytes unchanged. Exact-state review found a circularity between donor eligibility and the later rota, plus one fixed-sixteen description that the technical supersession list missed. I edited both Claim Sheets directly, kept Amendment 6 `Proposed`, explicitly approved the revised hashes and handed them back to Claude for genuine owner re-review. Because same-state convergence is still open, I did not revise the matcher, open a pool or begin implementation.

## 1. Startup and inherited state

`.agent-turn` named Codex and `.agent-session.lock` did not exist. I created the lock, re-read `.agent-turn`, confirmed it still named Codex, and followed `AgentPrompt.md` in order: the full project details, Codex continuity, every summary and active transcript in a Codex-including chat, then Claude's latest report and the playbooks governing Claim Sheet and review-cycle work.

The repository was clean at `2ba6ebb` (`Claude Session 14`), matching `origin/main`. Claude's handed-off hashes reproduced on disk:

- `Claim Sheet.md`: `40d8b0a698ea3dcedb974b9d61d4de1bc773d32006c7fa3d54f4a5ff06a335e6`
- `Accessible Claim Sheet.md`: `cbc3b00660f565ae9ebfd59623fb28e0b9b1b81bb3ae1dd380141ae307208b66`
- Codex matcher Draft 2: `f4ab71c3216d172641706a199d0536520da538aff906eb29d94f06f3d6620310`

The sheet diff from the last in-force contract was addition-only, as Claude reported. The active donor-matching chat asked for exact review of three specific choices; the Tier A Selection Review had nothing new requiring a Codex reply.

## 2. What Amendment 6 gets right

### The contract must support `N = 10…16`

The hard-sixteen matcher would silently tighten Amendment 2's existing failure boundary. Parameterizing the design is the contract-consistent resolution. `N < 10` still triggers Slot 12.3; no threshold, block count, injected-unit count, recording-minute tranche, sorter-hour ceiling or materiality rule moves.

### The donor and host gates are different objects

Whether one donor has an admissible rendered placement is a donor-level question. Whether ten scheduled donors can be placed together without violating the footprint, separation, edge and label rules is joint. Treating the latter as a reason to reduce `N` would make a host-capacity failure masquerade as donor attrition. A joint failure must reject the host.

### The fixed deal is preferable to an unspecified random one

The SHA-256 order plus round-robin deal determines which donors receive the quotient/remainder extras and which blocks contain their appearances before any survivor set is visible. It keeps every block at ten distinct donors for all `N ≥ 10`, while slot-within-block, spike-time and placement seeds remain randomized. The amendment correctly calls this a narrowing of Amendment 2 rather than a clarification.

### Amendment 5's expectation follows actual arm size

The anchor-like uniform-draw expectation describes the arm being built, so it must use `N` when fewer than sixteen targets survive. The already-recorded 0.11 / 1.03 and 0.12 / 1.17 values remain historical sixteen-target diagnostics and are not predictions.

## 3. Repair 1 — donor eligibility and the rota were circular

Claude's first version made `N` depend on realized amplitude, effective host SNR, realized depth and placement feasibility. Those values can vary by site. Point 4, however, creates the donor occurrence rota only after `N` is known and leaves later placement assignment randomized. Read literally, a donor could pass the initial screen, fail at a dealt occurrence, be removed, and cause a new `N` and a new deal. That is an iterative forking path rather than one predeclared measurement.

I edited both sheets so the donor-level screen is independent of the later `N`-dependent rota:

- before any zone donor is evaluated, the tracked configuration pins a finite candidate-site set, every numeric threshold, every per-site predicate and the exact site-to-donor reduction;
- a donor survives if and only if at least one pinned site passes every donor-level hard gate;
- `N` is computed once from those verdicts and is never recomputed in response to a later occurrence;
- after the rota exists, every block's ten donors must admit a jointly feasible ten-placement assignment under the same pinned sites and placement rule;
- a block-level failure rejects the host rather than dropping a donor and redealing.

This preserves Claude's correct donor/host distinction while making it executable without an outcome-dependent loop.

## 4. Repair 2 — one in-force fixed-sixteen sentence remained live

Claude's report correctly noted Amendment 3's point 3 sentence calling P1 a “fixed sixteen,” but the technical supersession paragraph named only Amendment 3 points 1 and 4. Amendment 6 point 5 already makes P1 an `N`-template subset, so the old point 3 sentence would have remained an in-force contradictory description.

I added Amendment 3 point 3 and broadened the technical supersession to cover explanatory sentences in Amendments 2–5 wherever sixteen denotes the current arm, subset, rota or draw size. The Accessible sheet now names the missed P1 sentence explicitly. Both sheets preserve historical status narratives and diagnostics actually computed at sixteen as history rather than silently recalculating them. The three deliberately fixed sixteens remain unchanged: the library's ceiling, the pre-host CA1 pool and the full removal set `Z`.

## 5. Exact-state handoff and gate state

I explicitly approved and handed back:

- `Claim Sheet.md`: `8fa0342279cfe4173ebb605fce4d3434e2647533f4af3a444b78a5f286cfaf48`
- `Accessible Claim Sheet.md`: `c58446d64b58748230f019188812a8eb3b043e95f10151ab1420799cab487d68`

Amendment 6 remains `Proposed` pending Claude's genuine owner re-review of those exact bytes. Amendments 1–5 remain the only in-force amendments. The matcher remains at Draft 2 because the declared gate order is amendment convergence first, revised prose rule second, implementation/test convergence third, and host-specific pool access only after all three.

No host-specific pool was opened. No edge table, donor selection, implementation or synthetic matcher fixture was created. No host, exact configuration, balance verdict, generation authorization, Rung 0 or sorter authorization moved.

## 6. Validation and repository integrity

- Recomputed seed derivations: the exposure-rota phrase gives SHA-256 prefix `71e3ca4a` → `1910753866`; the pseudo-pool phrase gives `2a66865b` → `711362139`.
- Replayed the round-robin arithmetic for every `N = 10…16`: all schedules total fifty; multiplicities equal `floor(50/N)` or `ceil(50/N)` with exactly `50 mod N` extras; every consecutive ten-slot block has ten distinct donor ranks.
- Relative to the last in-force contract at `f4419c4`, the sheets remain pure additions: 60/0 technical and 50/0 accessible.
- `git diff --check` passed after the edits.
- The chat write obeyed the append-only safeguard: the pre-write transcript was exactly 215 lines, the existing file remained an exact prefix, and the Session 14 Codex header occurs exactly once after that boundary.
- Claude's `HumanReport14.md` was read as the required recent-work cross-review. Its numerical and gate-state claims agreed with the live files except for the two exact-state defects repaired above.

The root Live-Run README already carries a public entry for proposed Amendment 6. This review did not move the amendment into force or open a new execution gate, so another public heartbeat would turn the lean log into a session journal; it was deliberately left unchanged.

## 7. Files created or updated

**Created**

- `agents/Codex/Session Summaries/HumanReport14.md`

**Updated**

- `Claim Sheet.md` — repaired proposed Amendment 6; revised hash above.
- `Accessible Claim Sheet.md` — synchronized plain-language repairs; revised hash above.
- `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md` — append-only exact-state review, rationale, approval and handoff.
- `agents/Codex/README.md` — workspace map and live review state.
- `agents/Codex/Summary of Only Necessary Context.md` — complete next-session continuity rewrite.

**Deliberately unchanged**

- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` — blocked until Amendment 6 reaches force.
- Root `README.md` — the proposed amendment was already reflected and no public state changed.
- Reproducibility Packet, `references.md`, `director_requests.md`, dependency files and `.gitignore` — no source, director dependency, dependency, generated artifact or ignore need changed.

## 8. Machine and execution boundary

Measured at 2026-08-13 01:10 PDT: system RAM **9.12 GiB free of 31.67**, GPU memory **1,025 MiB used of 16,311**, and **604.5 GB free on `C:`**.

Nothing heavy ran and no heavy step was contemplated. The session used only tracked text, git diffs, SHA-256 calculations and small in-memory rota checks. No network read, dependency install, raw-recording read, template-array pull, generator, Rung 0 or sorter run occurred.

## 9. Next steps

1. Claude genuinely re-reviews the two revised Amendment 6 hashes and either explicitly approves them or edits and hands back a new state.
2. If Claude approves unchanged, Amendment 6 can enter force in both sheets.
3. Codex then revises the matching rule to enforce source-count equality at every provenance stage, generalize all cardinalities and outputs to `N`, keep `Z` at all sixteen zone keys, and remove the erroneous percentage explanation.
4. Only after the revised prose converges may implementation and deterministic tests begin. Their same-state approval remains required before any host-specific pool or rendered edge table is constructed or opened.
5. No director action is needed. The Phase 1 contract-review request remains open and non-blocking.
