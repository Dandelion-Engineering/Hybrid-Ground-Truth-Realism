# Claude Human Report — Session 37

**Date and time:** 2026-08-16 23:40 PDT

**Phase:** Phase 2 — Execution

**Outcome:** Codex's ruling was accepted, the missing-depth sensitivity layer he
required was designed and built, and building it returned a correction to the
counterexample his ruling rested on. `Reproducibility Packet/scripts/utils/missing_depth.py`
and its 59-check harness exist and pass. **No approved artifact was edited, no
archive was read, no host is pinned, and ranks 1 and 2 remain paused.**

---

## 1. Startup and controlling workflow

`.agent-turn` named Claude and `.agent-session.lock` did not exist. I created
the lock, re-read `.agent-turn`, confirmed it still named Claude, then ran the
`AgentPrompt.md` context-first workflow: `Project Details/Project Details.md` in
full, my `Summary of Only Necessary Context.md`, the chat inventory, both active
chats, and Codex's Session-36 report as the cross-review obligation.

**Machine state at 23:17 PDT: 13,971 MB of 32,425 MB physical free; 38,359 MB
committed; GPU 1,078 of 16,311 MiB used.** Nothing this session was heavy — the
whole test suite runs in 3.7 s at its defaults and 11.0 s at the pinned 200
permutations, all in numpy on synthetic fixtures. **No archive read, so no
network cost at all.**

The next count-based progress report is due at Session 40.

## 2. Cross-review: Codex Session 36

Codex ruled on the non-finite-depth question I opened at the end of Session 36.
**He did not accept my proposed disposition**, and he was right not to. My
proposal was to drop non-finite depths, publish the count, and let §16.7's
pre-declared support floors do the protective work. His objection is exact: the
floors bound how many finite observations *remain*; they say nothing about how
far apart the finite order statistics sit around the median, and that spacing is
what decides how far a missing value can move a bin median.

He backed it with a construction against the approved estimator — five units,
twelve bins, 14,000 finite depths per unit-bin split evenly at 0 µm and 100 µm,
one missing depth per unit-bin. That is 0.00714% missing, slightly *below* rank
1's measured 0.00731%, and it passes every support floor. The complete-case
`Delta_10min` is 0.000 µm; two completions of the same missing entries give
0.000 µm and 100.000 µm against a 20 µm gate.

**I accepted the boundary in full and said so plainly rather than defending the
proposal.** His counterproposal — drop for the point estimate, but compute an
assumption-free missing-depth sensitivity interval, propagate it to the gate,
and let the existing 20/40 µm rule decide stability with no fitted percentage —
is the right shape, and it is what I built.

## 3. What I designed, and the one place I counter-proposed

Posted to `chats/Claude-Codex/Non-Finite Spike Depths/` at 23:19 PDT before
writing any code, so the design was on record as a proposal rather than as a
finished thing.

**(a) The per-bin interval, and it is exact.** For one unit and bin with finite
depths `x_(1) ≤ … ≤ x_(n)` and `k` missing at times known to fall in that bin,
the complete bin holds `N = n + k` values and the median reads ranks
`r1 = ⌊(N+1)/2⌋` and `r2 = ⌈(N+1)/2⌉`. A median is nondecreasing and continuous
in every argument, so:

    lo = ( x_(r1−k) + x_(r2−k) ) / 2      unbounded below when r1 − k < 1
    hi = ( x_(r1)   + x_(r2)   ) / 2      unbounded above when r2 > n

Both endpoints are attained by real finite completions (`x_(1) − 1` and
`x_(n) + 1`), so at the bin level this is the **attainable set**, not an outer
bound. Evaluated on Codex's construction it returns exactly `[0, 100]` — the
rule catches his counterexample from its own definition rather than from having
seen it.

**(b) Support invariance, which I added.** His point 2 varies the missing
*values* and says nothing about the inclusion *sets*, which can also move: a bin
with 9 finite and 2 missing depths is excluded from the record we hold and
included under every completion. Ranging the bound over subsets as well as
values makes it a much larger and less interpretable object, so I proposed a
pre-declared equality instead: **every unit and bin must have the same inclusion
status whether the missing samples are counted toward the three floors or not,
and a violation makes the candidate unmeasurable.** No tolerance is fitted. Both
real candidates already satisfy it — which is what my Session-36 diagnostic was
measuring without knowing that was its use.

**(c) The null, where I counter-proposed.** Codex's point 2 asks for the
interval to be propagated through "the null quantity the gate consumes." **An
assumption-free interval on `Q95_null` does not exist in a non-vacuous form**,
and I showed why rather than producing a number that looks like one: under a
completion the analysed pool holds `n + k` values and the seed-determined
permutation is an arrangement of *that many* elements — a different arrangement,
not a perturbation of ours. Bounding over completions would have to bound over
arrangements, under which any bin can receive any subset of the pool, and the
bound degenerates to the unit's whole observed depth range.

So I proposed a **declared counterfactual, declared as one in the artifact**:
the counterfactual null permutes the observed depths among the observed-depth
spikes exactly as the actual null does — same seeds, same arrangement — and
leaves each completed value at its own spike's time. I argued this is the
*right* counterfactual and not merely the tractable one: letting the arrangement
change mixes in a nuisance with nothing to do with the missing values, since two
seeds already give two different nulls on data with no missingness at all.

**(d) An honesty note I insisted on.** Above the bin level the propagation is an
**outer bound, not the attainable set**, because the same missing values enter
`d_u(b)` and the centring constant `c_u` and interval arithmetic ignores that
dependence. The error is one-directional — too wide, never too narrow — so the
layer can pause a candidate a dependence-aware treatment would have passed, and
cannot pass one some completion would have failed. That is written into the
module docstring rather than claimed away.

## 4. The correction the build returned

**This is the most important thing in the session and it was not planned.**

The harness case built from Codex's construction failed on its first run —
against `decision-unstable`, it returned `fails`. Chasing that produced the
finding: **`probe_nonfinite_depth_disposition.py` calls `measure_band_drift` and
stops there, and the gate is two numbers.** Run through the whole approved rule
— `permutation_null` at the same 40 replicates, then `apply_gate` at 20 µm —
his construction does not pass:

| | |
|---|---|
| `delta_window` | 0.000 µm (his number, reproduced) |
| `Q95_null` | **100.000 µm** |
| `apply_gate` | `passed=False`, `label=unmeasurable` |

The mechanism is his construction's own. An exactly balanced bin has a
knife-edge median, so permuting a unit's depths among its own spikes swings
every bin median the full 100 µm between the two levels. **A noise floor wider
than the tolerance is precisely the unmeasurable failure the second gate number
exists to catch**, and a bimodal band is the widest one there is.

So the construction does not show that the existing *gate* can accept a
candidate whose missing depths decide it. It shows the *point estimate* can.
That is a real difference and it is the one his ruling rested on. **It does not
overturn the ruling** — see below — but the evidence in the record has to say
what it proves, so the harness case now asserts the rejection rather than the
claim, and the correction is posted in the chat.

## 5. The counterexample that survives, and it is worse

The property Codex was arguing for is real; his fixture was just not the one
that shows it. I built the one that does.

`gate_passing_counterexample`: 15 units, 12 bins, 200 observed depths per unit
and bin drawn **uniformly across 300 µm** so no bin median is knife-edge, and a
block of missing depths in every bin.

| | |
|---|---|
| observed `delta_window` | 10.367 µm |
| observed `Q95_null` | 12.244 µm |
| `apply_gate` at 20 µm | **passes** |
| missing-depth bound on `delta_window` | **[0.00, 73.45] µm** |
| disposition | **decision-unstable** |

**Nothing in the approved pipeline objects to that candidate**, and its verdict
is decided by data nobody has.

**The asymmetry that makes it possible is the general lesson.** `D(b)` is a
median across units, so independent per-unit resampling noise — which is what
the null measures — shrinks with the unit count, while a block of missing depths
shifts every affected unit's median in the same direction at once and does not
shrink. **The null therefore cannot stand in for the bound, and the number of
*units* carrying missing depths matters more than the fraction of *samples*
missing.**

`probe_missing_depth_crossover.py` sweeps that on one fixture: the bound crosses
20 µm between **0.990% and 1.478%** missing while the approved gate keeps
passing. **That number is a property of that fixture, no code reads it, and it
is not a threshold** — the rule is still `L` applied to the bound. I was
explicit about what it does not license: every unit is affected in every bin
there, which is the worst case, while on the real candidates 11 of 140 and 10 of
182 included units carry any missing depth at all. **So I am not predicting the
real candidates are stable.** That is settled by running the bound on them.

## 6. Files created

| file | sha256 | state |
|---|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `2064304cec23621474de8b420d8f20f7e88bc7ace1798811b4682b4b2a2948a5` | new, not yet carded |
| `agents/Claude/tools/test_missing_depth.py` | `73a7c59e4e703f6837f36cd70349ed1836977974b2205857c19cfaa2ffbb46f6` | new, **59 checks, 0 failed** |
| `agents/Claude/tools/probe_missing_depth_crossover.py` | `036c5b8d4ef6df37dbff44b4fc5bfe20b8f3f53e9ce949fa971bae04dd249f10` | new, diagnostic only |
| `agents/Claude/tools/missing_depth_crossover_2026-08-16.txt` | `a53ede7a1d67cd62c4d5d586ce8beef9cfbbdb357d0b19dfb38cd16690a40583` | recorded output |

**`band_drift.py` is untouched at `eace4cd3…`** and all five RC-004 hashes
stand. The module *imports* the approved estimator and takes its point estimate
from `measure_band_drift` rather than computing one, so the two cannot disagree
about what the observation is.

Files updated: the active chat (two appended messages), the root `README.md`
running log (69 dated entries), this report, `agents/Claude/README.md`, and
`Summary of Only Necessary Context.md`.

## 7. The evidence, case by case

Codex's point 4 asked for four specific things before RC-005. All four exist,
plus two he did not ask for.

- **Exhaustive small-array containment** — `median_interval_matches_brute_force`
  enumerates every completion over a probe set for `n` in 1..11 and `k` in 1..3,
  126 parameter cases. Every completion lands inside the interval and the
  largest endpoint slack is `0.000e+00`, which is the exactness claim.
- **The three mirror failures I named** — `support_invariance_bin_floor`,
  `support_invariance_unit_floor` and
  `dropping_takes_a_bin_below_the_unit_floor`, plus `nonfinite_time_still_stops`
  covering both directions of the time rule.
- **An all-depths-missing unit** — unmeasurable, with all 12 reported bin
  mismatches on that unit and its exclusions counted.
- **His support-passing construction** — §4 above.
- **`zero_missing_reproduces_estimator`** (not asked for) — with nothing missing,
  the null's replicate values must equal `permutation_null`'s **elementwise** and
  the bounds must collapse onto the point estimate. A sensitivity layer that
  changes the answer on data with no missingness is a defect in the layer.
- **`pipeline_bound_contains_every_completion`** (not asked for) — three random
  bands completed 120 times each, including all-missing-at-±5,000 µm, every
  completion run through the approved `measure_band_drift`. **360 completions, 0
  escapes**, and the bounds are 0.00–0.23 µm wide rather than vacuous.
- **`small_missingness_still_passes`** — the same fixture at a twentieth of the
  missingness returns a **stable pass**. A bound that pauses everything is worth
  as much as no bound.

## 8. Decisions I made

1. **Accept the ruling without defending the proposal.** The counterexample was
   correct about the estimator's behaviour and arguing would have cost a round.
2. **Post the design before building it.** Finding 67's shape: the deviation on
   the null is on record as a proposal, not as something discovered after the
   fact in finished code.
3. **Add support invariance rather than interval over inclusion sets.** An
   equality is checkable and pre-declared; a subset-ranging interval is neither.
4. **Declare the null counterfactual rather than pretend to an assumption-free
   one.** Showing the vacuity is more useful than a number that looks rigorous.
5. **Report the correction to Codex's evidence immediately, in the same chat,
   and change the harness case to assert what is true.** Corrections propagate
   forward; his probe is his artifact and I did not touch it.
6. **Do not turn the crossover sweep into a rule.** It is recorded as scale, and
   the probe says in its own printed output that no code consumes it.
7. **Do not start the reader and command wiring this session.** The design has
   one open deviation (the null counterfactual) that Codex has not seen yet, and
   wiring it into `read_band_units` before he rules would build on an unagreed
   foundation.

## 9. Method findings worth carrying

- **A counterexample can be correct about its numbers and wrong about its
  claim.** His fixture proves the point estimate can be decided by missing
  depths. It was offered as proving the *gate* can be. Checking a counterexample
  against the *whole* rule it is aimed at is a distinct step from reproducing it.
- **When a check fires against a fixture you built from someone's evidence, the
  fixture may be right and the expectation wrong.** My harness case failed
  first; the defect was in what I expected, not in the module.
- **An averaging structure and a systematic perturbation scale differently, and
  that difference is where the safety argument lives.** Per-unit noise shrinks
  with unit count; a shared missing-data shift does not. Any argument of the
  form "the noise floor would have caught it" has to check which of the two it
  is talking about.
- **Show the vacuity rather than delivering the vacuous bound.** The
  assumption-free null interval is computable and useless; saying so and
  declaring a counterfactual is the honest move.
- **A conservative bound must be tested in the permissive direction too.** The
  `small_missingness_still_passes` case exists because a layer that pauses every
  candidate would have passed every other test in the file.

## 10. What is still open

1. **`read_band_units` still raises on the first non-finite depth.** It has to
   exclude the sample and return its *time*, since the bin the missing spike
   falls in is what the interval needs.
2. **`measure_host_drift.py` must publish exclusions per unit, per bin and in
   total**, report the interval, and consume `stability_verdict`.
3. **The disposition needs writing as a new section (§17) of the selection
   document** — §16 is closed under RC-001 and corrections propagate forward.
4. **RC-005 cards the whole state**, not the module alone, per Codex's point 4.
5. **Codex has not yet ruled on the declared null counterfactual.** If he
   rejects it, the point-estimate half of the design stands and only the null
   half changes.
6. **No host is pinned, no candidate has a drift number**, ranks 1 and 2 are
   paused on this question and ranks 5, 7, 9, 13 on the declared-clock one.

**Nothing here is waiting on you, Randy.** No archive was read this session and
no scientific result exists.
