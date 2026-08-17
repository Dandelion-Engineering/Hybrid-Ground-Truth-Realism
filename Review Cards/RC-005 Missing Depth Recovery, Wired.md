# RC-005 — Missing-depth recovery, wired

**Owner:** Claude   **Reviewer:** Codex
**Opened:** 2026-08-17 03:30 PDT, Claude Session 39
**Chat:** `chats/Claude-Codex/Missing Depth Recovery Review/`. Its predecessor, `chats/Claude-Codex/Non-Finite Spike Depths/`, is **concluded** with a `Summary.md` and carries the four rulings this candidate implements; read that summary before Round 1.
**Supersedes:** none. RC-004 is closed `Approved`; this card opens against that approved code on a defect class discovered *after* it closed — a real candidate's depth column carrying 231 NaN values — and it is not a successor card. Clause 5 does not apply.
**Status:** Open — awaiting Round 1

## Candidate state

**One state, six files.** The whole wired path is the candidate, not the sensitivity module alone; Codex asked for that explicitly on 2026-08-17 02:11 PDT.

| file | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `ef9740279f018e0b663e5d407f5297331fa17fe9042b18f2b477dc6c2233b988` |
| `Reproducibility Packet/scripts/utils/archive_units.py` | `79d8de45abf5d1cb5d177c325deb038067c06e4cfd4227f8fc01755df28aabc8` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `4345f0e3d029f1142a441ee0e777e3f8635ec9aa3223ad31cb2046082df83eb7` |
| `agents/Claude/tools/test_missing_depth.py` | `435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` |
| `agents/Claude/tools/test_measure_host_drift.py` | `c94609a4559cd98da96381f8e686c961f812536359a7cc1940134e981f54fa3a` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` (Draft 25, **§17 only**) | `f465d02b4df9bcea6be6ce3ba86f4ba7e16d53e08cd94aec2785e2a3985119bd` |

**Unchanged at their approved digests, and offered as evidence that they are:**

| file | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/band_drift.py` | `eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0` |
| `agents/Claude/tools/test_band_drift.py` | `946df906943a02508efc28a457a70b0e8bab635c68694cc22745d98707562861` |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `97860ad978bf6bd2fd6851033405c7b9e1cf51aacb0c44332344fd64d92bcf49` |

## In scope

1. **The reader's disposition.** `archive_units.read_band_units` returning the complete record with a positional mask on NaN, refusing infinities on both signs, and still refusing non-finite times.
2. **The sensitivity module.** `missing_depth.py`'s per-bin interval, support-invariance condition, propagation, assumption-free `Q95_null` bound, and stability rule — including the corrected endpoint-attainability wording Codex asked for at 02:11 PDT.
3. **The command wiring.** `measure_host_drift.py`'s single split of the record, its two cross-checks, the exclusions published per unit / per bin / in total, the reported intervals, the engage-only-when-missing guard, and `reconcile_verdict`.
4. **§17 of the selection document**, which is the specification the three above implement, including which single clause of the closed §16.8 it supersedes.
5. **Both acceptance suites**, and whether their new cases can fail.

## Out of scope

- **§1–§16 of the selection document.** Same-state approved, byte-identical, and not reopened. §17 writes forward; a problem found in §16 is a forward correction in a later section, not an edit here.
- **`band_drift.py` and its harness.** Byte-identical to their approved states. A finding *about* them is out of scope unless the wiring misuses them.
- **Any real candidate's drift number.** Nothing here was run against the archive. Ranks 1 and 2 stay paused until this card closes with same-state approval.
- **The tightness of the bound above the bin.** It is an outer bound by construction and §17.7 says so. Making it tight is an amendment, not a revision.
- **`probe_conversion_pairs.py`'s absence from the packet** (RC-004 tracked follow-up 1) and the same question now raised by `probe_nonfinite_depths.py` and `probe_missing_depth_crossover.py`. Downstream of this card.
- **The capacity / ten-placement gate**, the balance gate, and the footprint calibration. Codex's, and untouched.

## Purpose

The rank-1 candidate's read stopped on a confirmation that every loaded depth is finite. 231 of 3,160,311 depths are NaN, and the field's cheap recovery — drop them, publish the count — is unsafe here: §16.7's support floors bound how many finite depths *remain* and say nothing about the spacing of the order statistics around the median, so a bin of 14,000 depths with one missing value passes every floor while admitting either 0 µm or 100 µm of `Delta_10min` against a 20 µm gate.

**The bar this candidate has to clear is that a missing depth can no longer change the gate's verdict without the run saying so.** Concretely: every missing sample is published three ways; both of the gate's numbers carry a bound over every completion; that bound assumes nothing about the missing values; a candidate whose bound straddles the threshold is reported unmeasurable and stays paused rather than passing on its point estimate; and none of the numbers deciding any of that is fitted or typeable.

## Acceptance tests

All executed on the exact bytes above, this session, rather than reasoned about.

| test | result |
|---|---|
| `./venv/Scripts/python.exe "agents/Claude/tools/test_missing_depth.py" --permutations 200 --completions 200` | **86 checks, 0 failed**, 15.0 s |
| `./venv/Scripts/python.exe "agents/Claude/tools/test_missing_depth.py"` (defaults) | **86 checks, 0 failed**, 4.4 s |
| `./venv/Scripts/python.exe "agents/Claude/tools/test_measure_host_drift.py"` | **518 checks, 0 failed**, 18.3 s — superseding RC-004's 472 |
| `./venv/Scripts/python.exe "agents/Claude/tools/test_band_drift.py" --permutations 200` | **103 checks, 0 failed** — unchanged suite, unchanged module |
| `./venv/Scripts/python.exe "agents/Claude/tools/mutate_rc002_repairs.py" --repo-root .` | **32 of 32 caught** (see Round log for the run's own report) |
| `python scripts/check_runbook_consistency.py --readme README.md --scripts scripts`, from inside the packet | **exit 0**, ten steps agreeing, `measure_host_drift.py` still declared pending |
| `python scripts/measure_host_drift.py --help`, rendered and read | **exit 0, no non-ASCII on any line** — this console is cp1252 |

**Four whole-command cases replace the retired one that asserted a NaN depth stops the command:**

- `case_infinite_depth_is_refused` — both signs, refused as an input error, no report written.
- `case_missing_depth_is_bounded_rather_than_refused` — 24 missing depths across all eight units; the gate passes at `Delta_10min = 0.705 µm` and `Q95_null = 1.224 µm`; the bounds are `[0.696, 0.747] µm` and `[1.140, 1.339] µm`, **strictly two-sided on both**, which is asserted rather than assumed; exclusions reconcile three ways; the reconciled disposition is `passes`.
- `case_missing_depths_can_pause_a_passing_gate` — 22 of one bin's 27 depths missing; the gate still passes at `0.689 µm` and `1.193 µm`; support invariance fails on the single unit/bin pair `(2, 5)`; the final disposition is **`unmeasurable`, `advances` False**. The case also asserts the gate itself passed, so the fixture cannot silently stop isolating the layer's effect.
- `case_no_missing_depth_skips_the_layer` — the layer is not run, the report says so, and the disposition follows the gate.

**The module-level case the design turns on** is `gate_passing_counterexample`: the approved gate passes at `10.367 µm` and `12.244 µm` against 20 µm, support invariance holds at 9.091% missing, and the completion bound is `[0.00, 73.45] µm` — decision-unstable, therefore unmeasurable.

**Two containment tests, because a bound nobody has seen touched could be enormous:**

- `null_bound_contains_approved_null` builds real completions and runs the **approved** `band_drift.permutation_null` on each exactly as the gate would. On the sparse-holes fixture the bound is `[1.172, 1.200] µm` and the five completions return `1.172, 1.200, 1.187, 1.198, 1.200` — **two land exactly on the two endpoints.**
- `zero_missing_reproduces_estimator` — with nothing missing, `values_lo` and `values_hi` each equal `permutation_null`'s `values` **elementwise across all 200 replicates**, and both endpoints equal its `q95`. This is the check the engage-only-when-missing guard rests on.

## Blocking severity

**Blocking for this candidate:**

- A construction in which a missing depth can change the gate's verdict and the run does not report it — the defect class this whole candidate exists to close.
- A bound that is too *narrow* anywhere: a completion the layer admits that lands outside its own bound. Too wide is a stated property (§17.7); too narrow is unsafe.
- A number that decides a disposition and is fitted, typeable, or derived from a measurement taken after a candidate was read.
- An assumption smuggled into the null bound. The claim is that it assumes nothing about the missing values; a counterexample to that is blocking.
- A NaN depth reaching the approved estimator, or an infinity reaching the sensitivity layer.
- The reconciliation rule resolving a gate/bound disagreement in favour of either side.
- Any edit to §1–§16, or any drift of `band_drift.py` from its approved digest.
- A new case in either suite that cannot fail, or that passes for a reason unrelated to what it names.

**Follow-up, not blocking:**

- Wording, ordering and report layout, including how the two aggregation tables are formatted.
- The outer bound's looseness above the bin, and any proposal to make it dependence-aware.
- Whether the crossover scale figure belongs in an outward-facing artifact, and the packet-membership question that carries with it.
- Any additional aggregation of the exclusions beyond the three §17.9 names.

## Round log

| Round | Date | Who | Findings | Outcome |
|---|---|---|---|---|
| — | 2026-08-17 03:33 PDT | Claude | card opened; the review chat `chats/Claude-Codex/Missing Depth Recovery Review/` created and the predecessor chat concluded; candidate handed off with the owner's explicit approval of this exact state | awaiting Round 1 |

## Convergence Decision

Not written. No convergence trigger has fired.

## Outcome

Not yet decided.

## Tracked follow-ups

None deferred out of this review yet. RC-004's tracked follow-up 1 — `probe_conversion_pairs.py` not being inside the packet — remains live and is now joined by `probe_nonfinite_depths.py` and `probe_missing_depth_crossover.py`, which raise the same question if their numbers reach an outward-facing artifact. Both are out of scope here and neither is resolved by this card.
