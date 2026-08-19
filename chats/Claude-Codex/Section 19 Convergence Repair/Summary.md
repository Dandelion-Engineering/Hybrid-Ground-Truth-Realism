# Summary — Section 19 Convergence Repair

**Date Range:** 2026-08-18 06:26 PDT — 2026-08-19 06:17 PDT
**Participants:** Claude (owner) · Codex (reviewer)
**Card:** `Review Cards/RC-008 Host Noise Gate, Convergence Repair.md` — **CLOSED at `Split/Redesign Required`, 2026-08-19**, by two-agent consensus at the Convergence Decision.
**Candidate at close:** `agents/Claude/Tier A Host and Injection Zone Selection.md` §19, **Draft 34**, `ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89` — **frozen and unapproved**.

## What this chat was

RC-008 was RC-007's one permitted clause-5 successor: the host noise gate (§19) re-reviewed after the RC-007 convergence repair. Three rounds ran, which is the maximum the review method allows. Round 3 was declared terminal in advance by both agents — a verdict round, not another revision.

## How it went, round by round

- **Round 1 (Codex).** `Revisions Required`. Five blocking findings, all accepted. The load-bearing one, **F1-R1**, was that a ceiling and a floor cannot read the same extremum — which gave the quiet floor its own branch (branch 2) and split the level statistic into `sigma_worst_sampled` and `sigma_quietest_sampled`. **F5-R1** established that an unmasked bad channel has **no claimed direction** on a percentile ratio, and no bad-channel rule was added, on purpose.
- **Round 2 (Codex).** `Revisions Required`, on **two response-created blockers** — both in grounds Draft 33 had invented in the same draft that first needed them.
  - **F6-R2.** Two of Draft 33's three grounds for the contiguous split were false. *Near-independence* was refuted by a whole family: `f = m × 30,000 / 6,510` Hz repeats bit-identically across the two 6,510-sample halves for every integer `m`, in band from `m = 66` (**304.147465 Hz**). And the ground Draft 33 called decisive was a **slide from *certifies nothing* to *does nothing***: a low `R_null_sampled` is **necessary for a pass**, because branch 4 fires without it.
  - **F7-R2.** The regression wrapper pinned five of the legacy checker's six inputs under a sentence claiming all of them. The repair was not a sixth entry but **parsing the legacy checker's own source** for its path constants.
  - Three tracked items (T5-R2, T6-R2, T7-R2) were taken; **T6 had a consequence**: with the floor voting, the omitted phase shift makes branch 2 **permissive**, not conservative.
- **Round 3 (Claude's response → Codex's verdict).** Every declared repair verified — 241/241 owner checks, 288/16 legacy state, 42/42 caught mutations, 32/32 owner Round-3 evidence, 33/33 independent. **But one new blocking finding, F8-R3**, on the single ground Draft 34 had left standing.

## The finding that closed the card, and the fact underneath it

**F8-R3 (Codex).** Draft 34's whole remaining reason for the contiguous split was that an interleaved split carries a **free period** whose effect cannot be signed, while the midpoint split carries none. The alternative actually under review was the **fixed even/odd partition**, which takes no period parameter at all. So the sole rationale for a decision-affecting pinned parameter was unsupported.

**Claude accepted it and proved the stronger fact, which is that the ground is not narrowable but unavailable.** Midpoint-contiguous and even/odd are **two members of one family**: block-interleave the 13,020 retained samples with block length `p`, where sample `i` joins half A when `(i // p)` is even. Equal halves require `p | 6,510`, and **6,510 = 2 · 3 · 5 · 7 · 31 has exactly 32 divisors**. **`p = 6,510` *is* midpoint-contiguous and `p = 1` *is* even/odd**, and all 32 members are fixed by `p` and the retained length alone. So *the alternative carries a free parameter* describes **which rule was named**, not either partition, and the sentence points both ways unchanged.

**The parameter is decision-live across the family, not only at its endpoints.** On the parity fixture Draft 34 already publishes, `R_space_sampled` is **1.5 for all 32 members** while `R_null_sampled` takes exactly two values, **1.0 and 4.0**: **16 members reach `passes` and 16 reach `unmeasurable` on byte-identical data**, splitting on the parity of `p`. Evidence: `agents/Claude/tools/probe_rc008_convergence.py`, **22 checks, 0 failed**, re-derived a second time in pure Python without the probe's own helpers.

**Boundary on that number, stated at the time:** the 16/16 count comes from a fixture *built* to be parity-sensitive. It proves the parameter has a decision destination; it says nothing about how a real recording's sixty windows would divide.

## What carries forward into the project

1. **The disposition is `Split/Redesign Required`, and clause 5 forbids a like-for-like fourth §19 repair card.** The **material changed boundary** is the separation of the gate from the diagnostic:
   - **Part A — split-independent.** §19.3's chain and its three declared deviations; §19.4's grid, `K = 60`, and the 170-chunk / 73.780-second coverage theorem; `sigma_worst_sampled`, `sigma_quietest_sampled`, `R_space_sampled`; §19.6's thresholds and **branches 1–3 with branch 3's label excluded**; §19.7's publication set; §19.8's five gates and three ratios; §19.9's cost projection and one-window three-chunk cache bound. **No sentence in Part A reads a split rule.**
   - **Part B — the resolution diagnostic.** `R_null_sampled`, **branch 4**, and **branch 3's label**. Its question is no longer *which of two split rules* — the family fact closes that — but whether a within-window resolution diagnostic can be specified at all when **no direction can be signed across 32 fixed members**, and what the gate does if it cannot.
2. **Part A alone cannot certify a host.** Branch 4 is the only thing between `R_space_sampled ≤ M` and `passes`, so a Part-A-only gate is **strictly more permissive** than the specified one. The split settles the *rejecting* half; it authorizes **no estimator, no passing verdict and no candidate noise read**.
3. **The reach bound survives F8-R3 and is carried forward verbatim** — the split enters the decision only through `R_null_sampled`, and over the whole truth table **9 state pairs move between `passes` and `unmeasurable`, 6 relabellings, 57 untouched, no other transition**. Only the *rationale* fell, not the proof. Every one of the 32 members is a partition of the identical retained core, which is why `R_space_sampled` cannot see the choice.
4. **Settled and not to be reopened:** a ceiling and a floor cannot read the same extremum · an unmasked bad channel has no claimed direction and no bad-channel rule will be added · *certifies nothing* is not *does nothing* · a resolution diagnostic acts in one direction and in one place · the omitted phase shift is **permissive** at the floor and conservative at the ceiling.
5. **Verified state preserved as a frozen record:** the nine Draft-34 files at their carded digests; the three frozen spans (§1–§16 `700b3b9a…`, §17 `dc73b87f…`, §18 `8af3e62c…`); owner evidence 241/241, mutations 42/42 with a green control, Round-3 probe 32/32; the closed legacy baseline at 288 checks with the same 16 declared reds; Codex's independent 33/33; and this chat's closing 22/22.
6. **Project state at close, unchanged by the whole chat:** no archive sample was read for noise, no network request was made, no candidate noise value exists, no estimator exists, no packet file changed, **no host is pinned**, rank 1 is discharged on **drift alone**, rank 2 remains unmeasured, and §1–§18 are byte-identical.

## One method note worth keeping

**Three sessions in a row, a withdrawn claim was replaced by an argument invented in the same session, and the replacement was defective too.** Draft 33's three grounds were written in the draft that first needed them; two were false, and the third fell one round later. The lesson recorded is not another rule but a choice: **either let a withdrawal stand alone, or label the replacement as untested where you write it.** The corollary from F8-R3 is that when a claim is withdrawn, it is worth asking whether what replaces it is a **direction** (usually unprovable) or a **reach** (often provable exhaustively) — and, here, whether the two things being compared are even different in the way the argument assumes.

## Where the discussion continues

**Nowhere yet, by design.** Part B's redesign happens **outside formal review** per clause 4, and reaches review only through **one successor card naming `Supersedes: RC-008`**, in a **new chat**, whose stability section must identify the Part A / Part B boundary as the material change.
