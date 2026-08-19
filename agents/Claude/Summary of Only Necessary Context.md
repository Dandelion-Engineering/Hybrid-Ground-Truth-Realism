# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 52 · 2026-08-19 12:30 PDT**
**Next session is Claude Session 53. NO count-based progress report is due** (8, 16, 24, 32, 40, 48 are done; the next is **56**). A phase transition or an approved Claim Sheet amendment would still trigger one. **A review card closing is NOT a trigger.**

## 0. WHAT THIS SESSION DID, IN ONE PARAGRAPH

**I built Codex's named next object — the split-member comparison under the verified completion semantics — and it found that the semantics DOES NOT SETTLE THE SPLIT.** `probe_member_comparison.py`, 37 checks, 0 failed, ~1.5 s. **On a band where NO member's ratio is undefined at all, 28 of 32 members stand down and 4 withhold on byte-identical data** — eight copies of an amplitude-ramp channel holding the p10 rank above a pool of 64 at 1.8, so each member reports exactly `1.8 / (its own ramp ratio)` and stands down exactly when that ratio is at or above `0.9`. Mechanism checked 32/32; closest value to `M` is 0.029806, so **not a knife edge**; and the withholding set `{1085, 1302, 2170, 6510}` is **NOT the four longest block lengths** (3255 stands down at 0.944598, shorter 2170 withholds at 0.818169), so no monotonicity story is claimed. **Second result, and it costs an assumption I was carrying: the undefined set is a property of the CHANNEL, not of the family.** A step channel is undefined under exactly the 16 EVEN members; an amplitude-parity channel under exactly the 16 ODD ones; a three-segment channel under exactly `{6510}`; amplitude-block channels under exactly `{1, p}`. Seven distinct patterns over 12 shapes. **Third: Codex's criterion holds one-way for a statable reason** — the non-undefined member's value is itself a completion, so it lies inside the enclosure (49 cells, 0 escapes) — **while the FROZEN scalar rule's member disagreement has NO DIRECTION** (permissive on 14 cells, conservative on 1). **I again proposed no Part B design** and put three grounds to Codex as a question. **Four of my own errors, all caught by me except the last:** a withdrawn straddle expectation, a tautological check whose underlying claim was also FALSE, a note contradicted by its own numbers, and **a duplicate chat append caused by an idempotence guard keyed on a timestamp.**

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**.

**⚠️ *Convergence in place of escalation*, five clauses, binding since 2026-08-14:**

1. **A second LATE-BLOCKER, or ANY new blocker after Round 2, freezes the candidate and runs ONE agent-only Convergence Decision.** Each agent writes, once: minimum claim that can ship · controlling evidence · **strongest evidence against its own position** · one acceptable safe disposition.
2. **Evidence determines what may ship; consensus determines what happens next.** An in-scope executable counterexample defeats a universal or one-way safety claim. **Underdetermined evidence is NOT resolved in favour of approval.**
3. Safe dispositions: local repairable blocker → **`Revisions Required`**; purpose-level → `Split/Redesign Required`; non-blocking → `Approved with Follow-ups`. **Both agents approve the DISPOSITION, not the belief.**
4. **Close the card, repair OUTSIDE formal review, then ONE successor card naming `Supersedes:`**, whose stability section identifies the material pre-review change.
5. **⚠️ CLAUSE 5 WAS CONSUMED ON RC-008.** RC-008 was RC-007's one successor and it closed at a non-approval. **NO SECOND LIKE-FOR-LIKE SUCCESSOR IS ALLOWED.** The successor must carry the **Part A / Part B** boundary in section 3.0 below, and its stability section must say so.

**⚠️ THREE ROUNDS IS THE LIMIT AND ROUND 3 IS A VERDICT, NOT A REVISION.** RC-008 is the worked example of what happens when it is not reached.

## 1. Where the project is

**Phase 2 — Execution. One host gate of FIVE is discharged for one candidate. No host is pinned, no donor is selected, no generator has run, no sorter has run, and the project's actual question is untouched.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. **Not touched S44–S52.** |
| `Accessible Claim Sheet.md` | Synchronized, same six. `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 34, `ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89`, 343,106 bytes. FROZEN AND UNAPPROVED. NOT EDITED S49–S52.** **§1–§16 144,664 B `700b3b9a…`; §17 21,864 B `dc73b87f…`; §18 body 20,579 B `8af3e62c…`. Do not reopen §1–§18.** |
| `Reproducibility Packet/` | **NOTHING CHANGED IN S43–S52.** `results/host_drift_CSHL047_Probe01.txt` `a2d32508…`, `.json` `2e125d41…`, `scripts/measure_host_drift.py` `20070982…`, `check_runbook_consistency.py` `35cea57d…`, `README.md` `806aefaf…`, `utils/band_drift.py` `eace4cd3…`, `archive_units.py` `ed0766f2…`, `missing_depth.py` `ef974027…`, `results/host_timing_index.jsonl` `043a4ea4…`. |
| **`agents/Claude/tools/probe_member_comparison.py`** | **NEW S52. `b653bc0c214f6a0c419489bafde244185d4bd61acc882b64e9edd2baa75a6f42` — 37 checks, 0 failed, ~1.5 s.** Records `f0eb1435…` (TXT) / `4a86a090…` (JSON). Requires `--out`, takes `--records`. **⚠️ NO REVIEW HAS SEEN THIS** — and its docstring says so. **⚠️ IT AUTHENTICATES `probe_completion_bounds.py` AND `probe_null_ratio_undefined.py` BY PINNED DIGEST AND REFUSES TO RUN IF EITHER MOVED** — so editing either of those breaks this probe by design. **The digest published in the chat was corrected once (`87ee771a…` → `b653bc0c…`); the records did NOT change.** |
| **`…/probe_completion_bounds.py`** | **S51. `2c1c78beaf7345edf91e8393df70b8d049bfa0b462684c3463053b5431afddec` — 45 checks, 0 failed, ~0.4 s.** Records `d14c1471…` / `bb9465f0…`. **⚠️ PINNED BY DIGEST INSIDE `probe_member_comparison.py`. DO NOT EDIT IT.** Codex replayed it at 45/45 byte-identical. |
| **`…/probe_null_ratio_undefined.py`** | **S50. `4d21c7578011c0f01b956fbed10a670ff78cbc34c46d6c3c061dbcc8fc63eb66` — 20 checks, 0 failed, ~2 s.** Records `5ff8e2fa…` / `5cc4d438…`. **⚠️ ALSO PINNED BY DIGEST INSIDE `probe_member_comparison.py`. DO NOT EDIT IT.** Codex replayed it 20/20. |
| `…/probe_split_family_narrowing.py` | **S50. `37c864618bbe5ddbdfc1d438357fc643461239ca42542d48a99e942904a399d4` — 24 checks, 0 failed, ~19 s.** Records `4375175f…` / `1b9b3bd1…`. Requires `--source --out`, takes `--records`. **The withdrawal of the S49 overclaim lives here.** |
| `…/probe_split_family_sensitivity.py` | **UNCHANGED S50–S52 AND MUST STAY SO — Codex audited its record `f51b4949…` by digest and editing it breaks that chain.** `331f9e9f…`. **⚠️ ITS DOCSTRING AND ONE DETAIL STRING STILL CARRY THE WITHDRAWN CLAIM.** The withdrawal lives in the narrowing probe, in `agents/Claude/README.md` and here. |
| `…/probe_rc008_convergence.py` | **UNCHANGED.** `6bbdf3bd…` — 22 checks, 0 failed. |
| `…/probe_rc008_spec.py` · `mutate_rc008_spec.py` · `probe_rc008_round2.py` · `probe_rc008_round3.py` | **UNCHANGED — RC-008 IS CLOSED, SO NONE MAY BE EXTENDED AGAIN.** `2f20099b…` (241) · `2b19e1ec…` (42/42) · `aa6a4371…` (36) · `6210e7d2…` (32). |
| `…/probe_rc007_spec.py` + `mutate_rc007_spec.py` + `probe_rc007_round3.py` + `probe_rc007_convergence.py` + `mutate_rc007_convergence.py` | **UNCHANGED — RC-007 closed.** `ef37577e…` · `16a5f883…` · `54aeff57…` · `4f65da23…` · `98f6b8b6…`. `probe_rc007_spec.py` returns **288 checks with EXACTLY 16 expected reds** against Draft 34 — a deliberate instrument, not rot. |
| `…/probe_filter_chain.py` · `probe_raw_ap_layout.py` + records | **UNCHANGED** `ef96ce21…` / `dfcea89d…` / `b9f3e089…` · `ddef6e33…` / `f992c394…` / `4896a14f…`. |
| `…/probe_rc006_repairs.py` · `test_measure_host_drift.py` · `test_missing_depth.py` · `test_band_drift.py` · `mutation_test_runbook_checker.py` · `mutate_rc002_repairs.py` | `512e31fc…` (61) · `79c9bb5c…` (543) · `435272af…` (86) · `946df906…` (103) · `d443ded0…` (18/18) · `97860ad9…` (32). **None re-run S43–S52 — no code they cover changed.** |
| **`agents/Codex/tools/probe_split_family_dominance.py`** | **Codex's S49 audit, `ca7eefee…`, 12/12.** Reads my record by `--records`, writes `--out`/`--json`. |
| **`agents/Codex/tools/probe_completion_bounds_n72.py`** | **Codex's S51 independent full-size derivation, `864b6e01dfc8006d22c6a64432e27eadce0117948ba433673735bcb7ede65490`, 11/11.** Records `ce680287…` / `20c6e963…`. **Requires `--out --records`, takes `--random-fixtures`.** I read it at S52 and confirmed it imports nothing of mine. |
| Root `README.md` | **96 dated log entries** (95 at S52 open, +1 from S52), banner at 2026-08-19. **COUNT THEM, do not increment.** |
| `agents/Claude/README.md` | **338 CRLF lines, 0 bare LF** (326 at S52 open). |
| `Review Cards/RC-008 …` | **CLOSED at `Split/Redesign Required`, 2026-08-19.** `d2a8051061a8d7fc0f632e4d32c3eef84816e48bfd2cab47a8369a00349ef175`. **NOT reopened S50–S52.** |

## 2. The first thing to do next session

**`chats/Claude-Codex/Part B Resolution Diagnostic Design/…- Active.md` is the live channel and THE BALL IS WITH CODEX.** My S52 turn publishes the member comparison, states its honest limit, and puts **three grounds** to him as a question:

- **(a) pin one member and disclose it**, accepting that a differently disclosed convention could reach a different verdict on the same host **from defined values alone**;
- **(b) unanimity**, whose cost is now measured and is set by the single most withholding member;
- **(c) something that reads the data to choose a member**, which is a new kind of object and would need its own defence.

**I asked which the evidence now supports and whether the ramp band changes his view of (a). Read his reply before doing anything else in §19.** A forward correction follows my turn, naming the corrected script digest.

- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active** by Randy's request. **Nothing pending.**
- **All eighteen other chats are concluded**, each with a `Summary.md`. `Host Noise Gate/Summary.md` carries RC-007's arc; `Section 19 Convergence Repair/Summary.md` carries RC-008's.

**What can be done next, in order of readiness:**

1. **Codex's answer on the three grounds, then whatever it licenses.** **⚠️ Do NOT write the successor card in the same session that first constructs its argument — my most repeated error, now six sessions running.** The five S49–S52 probes are the evidence; consume them.
2. **Count every current-live Part-B surface mechanically — §19.5, §19.6, §19.7, §19.10 — before any candidate is called stable.** Codex's S51 scope ruling requires this and it has not been done.
3. **Rank 2 (NYU-12 Probe01) drift can be measured** — unpaused, unmeasured, command unchanged. **S49–S52 deliberately did NOT do this**: the pinned order is first-admissible and rank 1 has not been rejected, so it is speculative compute against the *Efficiency* standard.
4. **The estimator remains unwritable** until Part A and Part B are both settled. **Part A alone cannot certify a host** (see 3.0).

**⚠️ Rank 1's drift command, verbatim, from inside the packet folder — runbook step 11:**

`python scripts/measure_host_drift.py --session b52182e7-39f6-4914-9717-136db589706e --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

Add `--plan-only` for the sizing pass. **Measure free RAM against `peak_resident_bytes`, not `resident_bytes`.** About three minutes, 88.6 MB, 93 requests; `run_in_background`.

## 3. §19 AT DRAFT 34 — FROZEN, UNAPPROVED, AND SPLIT IN TWO

**Nothing has ever been measured with any of it. These are symbols with definitions, not values.** **The gated quantities are FOUR: `sigma_worst_sampled`, `sigma_quietest_sampled`, `R_space_sampled`, `R_null_sampled`** — the `_sampled` suffix is load-bearing on all four.

### 3.0 ⚠️ THE PART A / PART B BOUNDARY — THE CLAUSE-5 MATERIAL CHANGE

- **Part A — the split-independent gate.** §19.3's chain and its three declared deviations; §19.4's grid, `K = 60`, and the 170-chunk / 73.780-second coverage theorem; `sigma_worst_sampled`, `sigma_quietest_sampled`, `R_space_sampled`; §19.6's thresholds and **branches 1–3 with branch 3's LABEL excluded**; §19.7's publication set; §19.8's five gates and three ratios; §19.9's cost and cache bound. **No sentence in Part A reads a split rule.**
- **Part B — the resolution diagnostic.** **`R_null_sampled`, branch 4, and branch 3's label.**

**⚠️ CODEX'S S51 SCOPE RULING, ACCEPTED BY ME AT S52.** The successor card's Part B covers **both** §19.6's decision vocabulary **and** the Part-B-owned publication clauses inside §19.7 — a decision rule is not reviewable if the record needed to audit it sits outside the card. **The split is semantic, not heading-wide:** existing Part-A fields in §19.7 stay frozen regression surface; the new or changed fields that publish undefined `r_c(k)` identities, completion endpoints and the aggregate diagnostic are in scope; **the directly affected current-live Part-B statements in §19.5, §19.6, §19.7 and §19.10 must be counted MECHANICALLY when a candidate is stable.** The card must say *in scope: Part B's estimator semantics, branches/labels and publication fields; excluded but regression-checked: the unchanged Part A statistics, gates and publication fields.*

**⚠️ PART A ALONE CANNOT CERTIFY A HOST.** Branch 4 is the only thing between `R_space_sampled ≤ M` and `passes`, so a Part-A-only gate is **STRICTLY MORE PERMISSIVE** than the specified one.

**⚠️ AND AT S52 PART B'S QUESTION CHANGED SHAPE.** It is no longer only *what does the diagnostic do when it cannot be computed* — the completion rule answers that and Codex found no mathematical blocker at production size. It is now **what licenses pinning one split rule when the rule choice changes the verdict on FULLY DEFINED data.** See 3.1d.

### 3.1 ⚠️ THE 32-MEMBER FAMILY — THE FACT THAT CLOSED RC-008

**Block-interleave the 13,020 retained samples with block length `p`: sample `i` joins half A when `(i // p)` is even.**

- **Equal halves require `p | 6,510`. `6,510 = 2·3·5·7·31`, so there are EXACTLY 32 members** — 16 odd, 16 even.
- **`p = 6,510` IS midpoint-contiguous. `p = 1` IS even/odd.** Every member is fixed by `p` and the retained length alone; **none reads the data to be defined.**
- **So *the alternative carries a free parameter* is a statement about WHICH RULE WAS NAMED**, not about either partition. A category error, **not narrowable, unavailable.**
- **On the parity fixture: `R_space_sampled` = 1.5 for ALL 32; `R_null_sampled` takes exactly 1.0 and 4.0; 16 reach `passes` and 16 reach `unmeasurable` on BYTE-IDENTICAL DATA.**
- Evidence: **`probe_rc008_convergence.py`, 22 checks, 0 failed.**

### 3.1a ⚠️ THE SENSITIVITY SWEEP — WHAT SURVIVES AND WHAT IS WITHDRAWN

`probe_split_family_sensitivity.py` (S49, 12 checks) built a 32 × 32 sweep: fixtures at each member's own block length, all 32 members run against each.

**SURVIVES:** 0 of 1,024 non-finite; `R_space_sampled` 1.000–1.667, inside strict `M`, so **branch 4 is what decides**; 32 of 32 members withhold on the fixture at their own block length; 0 withhold on every fixture; 0 on no fixture; smallest withholding set on any fixture is **1**.

**⚠️ WITHDRAWN: "the family has no dominating member" and "none dominates."** Codex's `probe_split_family_dominance.py` (12/12) and my `probe_split_family_narrowing.py` (24 checks) independently give **30 strict pairwise dominance relations**; `p = 1` withholds on exactly the 16 ODD-target fixtures and dominates every other odd member (signatures `{1, p}`); `p = 2` on exactly the 16 EVEN-target fixtures and dominates every other even member (signatures `{p}`); `p = 1` and `p = 2` are incomparable, disjoint, and their union covers all 32; 32 distinct signatures. **⚠️ SO THE SWEEP DOES NOT DEFEAT "PIN ONE MEMBER AND DISCLOSE IT."**

**⚠️ AND TWO FURTHER BOUNDARIES ON THAT MATRIX:**

1. **450 of the 1,024 cells sit EXACTLY at `M = 2.0`, every one on the passing side** (branch 4's `>` is strict). The 77 withholding cells are all at 4.0 or 25/9. **THIS FIXTURE FAMILY SUPPORTS CLAIMS ABOUT CLEARLY SEPARATED VALUES AND MUST NOT BE USED TO ARGUE ANYTHING NEAR `M`.**
2. **The fixtures are CONSTRUCTED to be visible to one member.** Nothing in the matrix is a claim about real recordings.

### 3.1b ⚠️ THE RESOLUTION DIAGNOSTIC HAS AN UNDEFINED CASE — S50

**Draft 34 §19.6 says the half-window ratio is "handled identically" to `sigma_hat_c`, that "a channel with a zero denominator contributes `+inf`", and that "No undefined ratio enters a comparison." THE LAST SENTENCE IS FALSE.** The degenerate test §19.6 imports — *a channel literally constant across the retained core* — is right for `R_space_sampled` and **wrong for `r_c(k)`, which reads the two halves.** A channel can vary across the core and still be constant **within each half**, giving 0/0.

`probe_null_ratio_undefined.py`, **20 checks, 0 failed**, constructed channels:

- A **mid-window step channel** has whole-core `σ̂_c = 1.482602` — **not degenerate by §19.6's test** — and both contiguous halves have exactly zero MAD. **Ratio is NaN, not `+inf`.**
- **Mechanism, checked not asserted: `6,510` carries exactly one factor of 2, so `p` is even ⟺ `6,510/p` is odd**; an odd block count leaves each half holding a **strict majority** of one step value (smallest observed share **0.500154**); and **a MAD is exactly zero whenever a strict majority share the median value.**
- **⚠️ THE UNHANDLED BEHAVIOUR IS PERMISSIVE ON THESE FIXTURES.** 7 undefined of 72 → NaNs sort above rank 65, never reach the comparison → **`passes`**. 8 of 72 → `R_null_sampled` is itself NaN, `NaN > M` is **False** → **`passes` again**. **CONTRAST: 8 zero-denominator channels at the same count and rank are `unmeasurable`.**
- **"Sort ascending" does not determine an answer with a NaN.** `numpy.sort` sinks NaN to the end — a convention §19.4 does not state — while Python's `sorted` returns different rank-65 values for two permutations of the SAME multiset.
- **⚠️ THE DOCUMENTED `+inf` HALF IS SOUND AND WAS NOT DISTURBED. Do not "fix" it.**

**⚠️ AND S52 BOUNDS THE PERMISSIVENESS CLAIM — SEE 3.1d POINT 3. It is true on these fixtures and does NOT generalise to every pool.**

### 3.1c ⚠️ THE COMPLETION BOUNDS ARE EXACT — S51, CLOSED AT PRODUCTION SIZE BY CODEX

**Codex's criterion, proved rather than assumed.** `n` band channels; `u` of them have an undefined ratio; the other `m = n − u` are finite (possibly including exact `0` and exact `+inf`). A **completion** gives each undefined channel a value in `[0, +inf]`.

- **Ranks: `i10 = ceil(n/10)`, `i90 = ceil(9n/10)`, 1-based. At n = 72 that is 8 and 65.** **⚠️ AND `i10 = n − i90 + 1 = 8` AT n = 72**, which is why ONE count governs both ends.
- **MAXIMUM: attained at a VERTEX** — every unknown at `0` or at `+inf`. Checked, 36 of 36 fixtures.
- **⚠️ MINIMUM: NOT attained at a vertex.** On **24 of 36 fixtures** an interior placement strictly beats every vertex. Mechanism: an unknown placed between the two ranks lowers the p90 rank's value by one finite position while leaving the p10 rank's alone; `0` lowers both, `+inf` lowers neither. Worked case: `n = 10`, finite `1..9` — both vertices give **9.0**, an interior placement gives **8.0**. **Closed form `f[max(i90 − u, i10)] / f[i10]`.** **A vertex-only minimum is TOO HIGH, which is PERMISSIVE for the branch-3 label.**
- **⚠️ THE PRODUCTION-SIZE CLOSED FORM, NOW DERIVED THREE TIMES INDEPENDENTLY** (Codex's prose, his code, and my S52 re-implementation from his prose): at n = 72, for `u ≤ 7` and a positive finite rank-8 value, **lower = `f[max(65−u, 8)] / f[8]`; upper = `max_{a=0..u} f[65−a] / f[8−a]`**, with `a` unknowns below every defined value and the rest above. **My S52 probe agrees with the S51 enumeration on both endpoints over 48 full-size pools, 0 mismatches.**
- **⚠️ MY S51 SMALL-n LIMITATION IS CLOSED.** Codex's `probe_completion_bounds_n72.py` (11/11) exhausts **34,320 completion multisets across 24 full-size rank patterns**, 512 continuous pools, 16,384 sampled interior completions, zero mismatches; handles the zero/infinite rank-8 edge; and supplies an eight-zero witness for every `u = 8..72`. **He finds no mathematical blocker.** I read the source and confirmed it imports nothing of mine.
- **COUNT THRESHOLD: `u ≥ 8` of 72 → upper bound UNBOUNDED whatever the finite values are → withheld.** That is **exactly** §19.6's documented zero-denominator count. **`u ≤ 7` leaves a finite bound the finite values decide** — 65 homogeneous ratios plus 7 undefined give `[1.049652, 1.057000]`, so branch 4 STANDS DOWN and the unknowns are *proved* irrelevant. **Not a blanket rejection.**
- **CONSERVATIVE EXTENSION.** With `u = 0` the endpoints collapse to the single value (24/24), branch 4 fires exactly when Draft 34 says, and the third label is unreachable across 72 spatial values.
- **ONE-WAY.** Every scalar convention (`0`, `1`, `+inf`, the finite median) is itself a completion and lands inside the enclosure, as do 2,400 random mixed completions; **no completion withholds while the bounded rule stands down.**
- **IT BITES.** 65 finite ratios (seven at 1.0, fifty-eight at 3.0) plus 7 undefined: NumPy gives **1.0** and today `passes`; the upper bound is **3.0** and the bounded rule returns `unmeasurable`.
- **⚠️ NUMPY'S NaN ORDERING *IS* THE ALL-AT-`+inf` VERTEX.** The divergence is in the COMPARISON, not the ordering.
- **MAX OVER WINDOWS PROPAGATES EXACTLY**, both endpoints, because placements are independent across windows. **One unbounded window carries the whole diagnostic.**
- **⚠️ THE WORD *EXACT* IS BOUNDED TO THE DECLARED PER-RATIO COMPLETION SPACE**, where each `0/0` ratio ranges independently over `[0, +inf]`. **Not a frequency claim about real recordings and not a claim that every interior value is physically attainable.** Codex's wording boundary, accepted.

**THREE COSTS, all recorded:** (1) **the third label is a change to PUBLISHED VOCABULARY** — §19.6 publishes exactly TWO labels; (2) **interior attainment is OPEN and NOT load-bearing** — both endpoints are attained by exhibited witnesses, and the enclosure can COLLAPSE TO A POINT; (3) **a SECOND-ORDER 0/0 exists one level up** — if both selected order statistics are `0` the band ratio is itself 0/0 with no channel undefined; at n = 72 that needs 65 channels at exactly zero, and the bound already treats it as unbounded.

**⚠️ AND ONE EXPECTED DEFECT THAT MEASUREMENT REFUTED — WITHDRAWN.** §19.4's own `ceil(0.10 n)` / `ceil(0.90 n)` in binary floating point **agrees with exact integer arithmetic at EVERY n from 1 to 200,000.** **Do not re-raise it.**

### 3.1d ⚠️ THE MEMBER COMPARISON — S52, NEW, UNREVIEWED. THE SEMANTICS DOES NOT SETTLE THE SPLIT

`probe_member_comparison.py`, **37 checks, 0 failed**, ~1.5 s, all constructed. **It authenticates and imports the two probes above rather than re-implementing them, so it is graded by exactly the proved semantics.**

**1. ⚠️ THE MEMBERS DISAGREE WITH NO UNDEFINED CHANNEL PRESENT. THIS IS THE FINDING.**
A band of 72: **eight copies of an amplitude-ramp channel** (alternating sign scaled by a linear ramp 1.0 → 4.0 across the retained core) **above a pool of 64 channels at 1.8**. The eight copies occupy exactly the p10 rank and the pool the p90 rank.

- **0 members undefined; 29 distinct reported values; 28 members stand down and 4 withhold** — `{1085, 1302, 2170, 6510}`.
- **Mechanism checked 32/32:** the reported value is exactly `1.8 / (the member's own ramp ratio)`, and branch 4 stands down exactly when that ratio is at or above `1.8 / M = 0.9`.
- **NOT a knife edge: closest reported value is 0.029806 from `M`.** The pool is **1.8 and not 2.0 on purpose** — a pool at exactly `M` would repeat the S50 450-ties problem.
- **⚠️ THE WITHHOLDING SET IS NOT THE FOUR LONGEST BLOCK LENGTHS.** 3255 stands down at ramp ratio **0.944598**; the shorter 2170 withholds at **0.818169**. The ratio is **not monotone in block length** and **no causal story beyond the measured ratio is claimed.**
- **CONSEQUENCE: `R_null_sampled` remains decision-relevant to the split after the undefined case is fully handled.** Part B cannot be closed as a corollary of the completion rule.
- **HONEST LIMIT: the band is constructed to separate members, and 28 of 32 agreed.** Nothing says a real band does this.

**2. ⚠️ THE UNDEFINED SET IS A PROPERTY OF THE CHANNEL, NOT OF THE FAMILY.** Measured over 12 shapes × 32 members = 384 cells:

| shape | undefined under |
|---|---|
| two-segment step | **exactly the 16 EVEN members** |
| amplitude-parity | **exactly the 16 ODD members** |
| three-segment | **exactly `{6510}`** |
| amplitude blocks at 7 / 31 / 105 | exactly `{1, 7}` / `{1, 31}` / `{1, 105}` |
| four-, five-, six-segment; alternating; ramp | none |
| dead half | none undefined; **`+inf` under exactly the 16 EVEN members** |

**Seven distinct undefined patterns. NEITHER PARITY CLASS IS THE UNRELIABLE HALF.** **Mechanism checked on all 384 cells and 768 halves:** the ratio is undefined ⟺ both halves have zero MAD, and a half has zero MAD ⟺ a strict majority of its samples equal its own median. **The ramp channel has 29 distinct DEFINED ratios (0.538434 – 1.000000) with no undefined and no infinite member**, which is what makes point 1 possible.

**3. ⚠️ DIRECTION: THE BOUNDED RULE IS ONE-WAY; THE FROZEN SCALAR RULE HAS NO DIRECTION AT ALL.**
Where two members see the same finite values and differ only in which channels are undefined, **the member WITHOUT the undefined channels reports a value that is itself one legal completion, so it lies inside the other's enclosure** — 49 cells, **0 escapes**. Therefore:

- **bounded rule: the undefined-producing member is NEVER the more permissive** (0 of 49), and is **strictly more conservative on 14 of 49**;
- **frozen scalar rule: the same member is permissive on 14 cells and CONSERVATIVE on 1** — the `('onetail', 7)` cell, a pool of 64 ones plus a single 10.0 with seven undefined, where sinking the NaNs displaces the finite values **into** the p90 rank instead of occupying it. **So S50's permissiveness result is true ON ITS FIXTURES and does NOT generalise to every pool.**
- **⚠️ 14 AND 14 IS A COINCIDENCE AND THE TWO CELL SETS ARE DISJOINT — 0 IN COMMON.** The probe asserts this so no reader infers a correspondence.
- On the biting fixture the two members **disagree under the scalar rule and AGREE under the bounded one**; at `k ≥ 8` the disagreement becomes **total and value-independent** (the undefined-producing member is withheld whatever the pool; the other can pass).

**4. THE THREE MULTI-MEMBER CONSTRUCTIONS**, over 30 bands × 32 members:

- **Strictly ordered.** unanimity ⟹ every pinned member ⟹ existential; **0 order violations**; 121 cells strict against unanimity, 71 against existential.
- **Unanimity is EXACTLY the verdict of the member with the largest upper bound on that band**, and existential exactly the smallest. **0 mismatches over 30 bands.** So unanimity is not a new statistic; it is a per-band selection.
- **⚠️ NO MEMBER HAS THE LARGEST UPPER BOUND ON EVERY BAND** — 6 distinct maximizing sets, **empty intersection**. **Unanimity CANNOT be replaced by pinning one member chosen in advance.**
- **⚠️ ITS COST: UNANIMITY IS WITHHELD BY AS FEW AS ONE MEMBER OF 32.** On the three-segment band at k = 7 over a one-tailed pool, `p = 6510` alone withholds and 31 stand down. **Its rejection rate is set by the single most withholding convention.**

**5. THE PUBLICATION SET IS SUFFICIENT TO AUDIT THIS CASE — A POINT IN CODEX'S FAVOUR.** On the ramp band the **undefined-specific** fields (identity count, reachable-undefined state) are **identical under all 32 members**, while the **published endpoint pair differs under 29**. So the disagreement is auditable from the record rather than hidden by it. **Keeping the raw per-half scales is what makes another member's value recomputable.**

**⚠️ AND FOUR ERRORS OF MINE FROM THIS SESSION, ALL RECORDED:** a **withdrawn** expectation that some shape's defined ratio would straddle 1.0 (none does; every varying shape has 1.0 as one endpoint, now asserted as a fixture property, and the negative result stays in the suite); **a tautological check whose underlying claim was ALSO FALSE** (I asserted the publication set would hide the disagreement; the endpoints reveal it); **a note contradicted by its own numbers** (the "four longest block lengths"); and **a duplicate chat append** (see section 11 item 129).

### 3.2 The pinned chain (§19.3) — FOUR steps

1. scale `int16 → µV` by the asset's own `conversion`; `offset` must be exactly 0
2. **high-pass on a 14,020-SAMPLE BLOCK OF REAL RECORDED SAMPLES** — the window's chunk plus the last 500 samples of chunk `i−1` and the first 500 of chunk `i+1` — fifth-order Butterworth at 300 Hz, `sos`, `sosfiltfilt`, `padtype="odd"`, `padlen=18`, **designed at the NOMINAL 30,000 Hz**; then **discard the 500 margin samples at each end, retaining exactly the chunk's 13,020 samples**
3. **common median reference across all 384 probe channels**, per sample
4. `σ̂_c = MAD / 0.6744897501960817`

**THREE DECLARED DEVIATIONS:**

1. **phase shift omitted** → **σ̂ biased upward UNDER THE SHARED-COMPONENT MODEL and FOR THE LEVEL STATISTIC ONLY.** **⚠️ CONSERVATIVE at the ceiling and PERMISSIVE at the floor** (T6-R2). **No direction is claimed for `R_space_sampled`.**
2. **bad channels not masked** → **DIRECTION UNKNOWN (F5-R1).** **NO BAD-CHANNEL RULE IS ADDED, ON PURPOSE.**
3. **nominal design rate** → SpikeInterface designs from the recording's rate; **rank 1's series carries NO `rate` attribute at all** (`timing_source: timestamps`). `padlen` is 18 at either rate; the margin is 500 samples at either rate under truncation, flooring AND rounding. SOS coefficients differ by at most **1.31860735664e-07**.

### 3.3 The grid, the quantities and the coverage bound (§19.4)

- **A window centre needs a FULL CHUNK ON EACH SIDE**, so eligible centres are `1 … C − 2` and `K = 60` centres sit at **`i_k = 1 + floor(k·(C−3)/(K−1) + 0.5)`**. Rank 1: `1, 170, 340, …, 9,828, 9,997`.
- **Reading a window transfers THREE chunks and retains ONE.**
- **Largest gap `g = 170`; longest unsampled run `169`; any interval fully containing `170` consecutive chunks holds a sampled window = 73.780 s at rank 1. TIGHT IN BOTH DIRECTIONS.** Coverage 26.04 s, **0.600%**.
- `S(k)` = median over band channels of `σ̂_c(k)`. **`sigma_worst_sampled = max_k S(k)`** (ceiling); **`sigma_quietest_sampled = min_k S(k)`** (floor).
- **`R_space_sampled = max_k (p90/p10 across band channels)`.** **Nearest-rank: `p10` = rank `ceil(0.10·n)`, `p90` = rank `ceil(0.90·n)`; at n=72 ranks 8 and 65.**
- **`R_null_sampled`** = the same ratio over `σ̂_c^A/σ̂_c^B` from two disjoint halves of the retained 13,020 (**6,510 each**). **The split rule is Part B and is NOT settled.**
- **`max/median` is published and consumed by nothing.**

### 3.4 `R_null_sampled` IS ONE-SIDED AND ACTS IN ONE PLACE

> **`R_null_sampled` can convert a would-be pass into `unmeasurable`, and can change how a failure reads; it never converts a would-be failure into anything else.**

- **Above `M` withholds the measurement ONLY WHERE `R_space_sampled ≤ M`.**
- **At or below `M`: CERTIFIES NOTHING.** A candidate that passes, passes on `R_space_sampled` **alone**.
- **⚠️ BUT *certifies nothing* IS NOT *does nothing*.** A low `R_null_sampled` is **necessary for a pass** — branch 4 fires without it. **It gates without certifying.**
- **That asymmetry is §16.7's, transposed** — the two rules agree cell for cell in all four states.

### 3.5 ⚠️ THE SPLIT'S REACH IS EXACT — ONLY THE RATIONALE FELL

The split enters the decision **only** through `R_null_sampled`, because `R_space_sampled` is computed on the retained core and **every one of the 32 members is a partition of that identical core** (`R_space_sampled` recomputes to the same value from all 32, max deviation exactly 0). Over the whole truth table: **9 state pairs moved between `passes` and `unmeasurable`, 6 relabellings, 57 untouched, no transition of any other kind.** **A change of split rule can NEVER turn a failure into a non-failure or a non-failure into a failure. How much it can move a value is not bounded anywhere** — and S52's ramp band is the sharpest instance yet. **Carry this forward verbatim.**

### 3.6 ⚠️ AN UNMASKED BAD CHANNEL HAS NO CLAIMED DIRECTION (F5-R1)

Eight contacts at 1, fifty-six at 2, eight at 3 → `p90/p10 = 3`, fails strict `M = 2`. Replace **one** quiet contact by 100 → p10's rank moves off a 1 and onto a 2, p90 stays at 3 → **ratio 1.5, and it passes.** **Direction UNKNOWN. NO BAD-CHANNEL RULE IS ADDED, ON PURPOSE.** §19.7 publishes the per-channel `σ̂_c` FOR EVERY WINDOW.

### 3.7 The thresholds (§19.6) — NOTHING HAS EVER MOVED

| | strict | relaxed | derivation |
|---|---|---|---|
| **floor** (reads `sigma_quietest_sampled`) | **1.25 µV** | **1.25 µV — does not relax** | `A_min/40`, the anti-saturation condition |
| **`N`** (level, reads `sigma_worst_sampled`) | **10.0** | **25.0** | `A_min/5` and `A_max/8`, **both multipliers SpikeForest's own** |
| **`M`** (spatial) | **2.0** | **4.0** | `√(A_max/A_min)` and the full span |

`A_min = 50`, `A_max = 200` **µV peak-to-peak** (§11.1: donor `amplitude_uv` is `np.ptp`). **`A_max/σ ≥ 8` is IMPLIED by `σ ≤ 10.0`.**

**⚠️ THE PASS RULE HAS FOUR ORDERED BRANCHES; THE FIRST THAT FIRES IS THE DISPOSITION.**

1. `sigma_worst_sampled > N` → **fails** on level.
2. **`sigma_quietest_sampled < 1.25 µV`** → **fails** on level, labelled `implausibly quiet`. A predeclared design failure, not an input error.
3. `R_space_sampled > M` → **fails** on homogeneity, labelled `resolved heterogeneity` if `> R_null_sampled`, else `resolution-limited`. **⚠️ THIS FIRES AT HIGH/HIGH AND THE MEASUREMENT IS NOT WITHHELD.** **The LABEL is Part B; the BRANCH is Part A.**
4. `R_space_sampled ≤ M` **and** `R_null_sampled > M` → **unmeasurable**. **Wholly Part B.**

**Degenerate channels** (exactly zero σ̂) are **counted and published, never masked**; **if enough of them reach the p10 rank** the ratio is `+inf`, which fires branch 3. **⚠️ "ENOUGH" IS LOAD-BEARING — at n = 72 the p90 rank is 65, so fewer than 8 extreme channels never reach it.**

**⚠️ INPUT ERRORS ARE NOT GATE OUTCOMES.** Too few full chunks (`C ≥ K + 2`), non-zero `offset`, absent/non-finite `conversion`, unit ≠ volts, a band electrode not resolving to one column, non-finite samples, failed replay → **input error: NOT recorded as failed, and the pinned order DOES NOT advance.** An **unmeasurable rejection** (branch 4) **IS a rejection and the order DOES advance** — as does a branch-3 failure. **⚠️ AND CODEX'S S50 RULING, WHICH I ACCEPT: a valid, structurally sound sample that makes the estimator return 0/0 is NOT an input error** — nothing about the asset is malformed, and calling it one would pause the pinned order on a condition no data repair can cure.

**⚠️ THE CONVENTION SUBSTITUTION HAS OPPOSITE DIRECTIONS FOR A FLOOR AND A CEILING.** p2p for single-sided peak **weakens a floor** and **strengthens a ceiling**. **The `snr_p2p = 40` ceiling is JUDGEMENT, not literature** — **no round of either card challenged it.**

### 3.8 §19.7 and §19.8 — what is published, and the three ratios

**§19.7 publishes:** the full `S(k)` series; **the per-channel `σ̂_c` FOR EVERY WINDOW** (F5-R1); **the full per-window `ρ(k)` series that `R_null_sampled` is the maximum of**; and the filter's design parameters including **the nominal rate AND the candidate's own sampling rate WITH ITS SOURCE labelled** (T7-R2; **rank 1 declares none**, so the whole-span `host_timing_index.jsonl` derivation is named instead).

**⚠️ CODEX'S S51 MINIMUM FOR THE PART-B PUBLICATION SURFACE**, once the rule stops treating every channel as a scalar: **undefined channel identities and counts per window; each window's lower, upper and undefined-reachable state; the aggregate maximum's two endpoints and the window(s) that set them; the second-order band-level 0/0 state; and the raw per-half scales and defined per-window values already promised.** **A single scalar `R_null_sampled` cannot remain the only reported object.** **S52 confirms this set is sufficient to audit the ramp band's member disagreement, and that the RAW PER-HALF SCALES are the field that makes another member's value recomputable.**

**§19.8 — host admissibility is FIVE gates; §15.5 is superseded in no clause; NOTHING of gate 3 is discharged.** It reports **three** ratios: `snr_p2p_min = A_min/sigma_worst_sampled`, `snr_p2p_max = A_max/sigma_quietest_sampled`, `snr_p2p_quiet = A_min/sigma_quietest_sampled`. **`snr_p2p_max` rearranges no condition at all.** **The native-amplitude check was examined and REFUSED and that stands.**

### 3.9 Cost (§19.9) — UNCHANGED AT 957,031,364 BYTES

**180 chunks × 5,316,841 projected stored bytes ≈ 957,031,364 bytes**, a PROJECTION from a whole-file average, **~10.8× the drift run's 88,599,226 B**. **⚠️ `RemoteFile`'s cache is unbounded, so the estimator MUST bound its own cache to ONE WINDOW'S THREE CHUNKS.** Three chunks are 29,998,080 B as `int16`; the 14,020-sample block across 384 channels is **43,069,440 B as `float64`**, and `sosfiltfilt` needs a comparable temporary.

**THREE refused arrangements, TWO distinct defects:** three cores of a five-chunk read kept as three windows → **COVERAGE** (gap 170 → 524, guarantee 73.780 s → **227.416 s**); the same aggregated → that plus **DILUTION** (3.02 → **1.33**, 44%); twenty single-chunk windows → **COVERAGE** (gap 527, guarantee **228.718 s**).

## 4. §19.2 — the measured layout (UNCHANGED; no archive read S44–S52)

| property | value |
|---|---|
| shape | 130,188,000 × 384 |
| dtype / filters | `int16`, **gzip level 4** |
| **chunk** | **13,020 samples × 384 channels** (= 0.434 s, 9,999,360 B uncompressed) |
| logical / stored | 99,984,384,000 / 53,163,508,785 B → ratio **0.53172** |
| `conversion` | **2.34375e-06 V**; `offset` 0.0; unit volts; **no `channel_conversion`** |
| full chunks | **9,999**, plus a 1,020-sample partial |

1. **The chunk spans EVERY channel**, so 72 band channels cost exactly what 384 cost — which is why CMR is over the whole probe at no transfer cost.
2. **Time is addressable only at 0.434 s**, which is why a margin costs a whole neighbouring chunk.
3. **One stored CODE STEP is 2.34375 µV.** A MAD estimate on the STORED INTEGERS would be granular to 1.74 µV. **That is why the estimate is taken AFTER the chain.**

**§19 converts chunks to seconds at the NOMINAL 30,000 Hz.** Do not switch to the measured rate for a published duration without changing both.

## 5. Machine state and measured costs

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`).

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; never inherit a number, including from this file.

**Session 52 readings: 12:09 — 12,438 MiB of 32,425 free, VRAM 14,906 of 16,311; 12:30 — 11,955 MiB, VRAM 14,909.** Nothing heavy ran; no archive read, no network request, no GPU work.

**Suite costs:** **`probe_member_comparison.py` ~1.5 s**; `probe_completion_bounds.py` ~0.4 s; `probe_split_family_narrowing.py` ~19 s; `probe_null_ratio_undefined.py` ~2 s; `probe_rc008_convergence.py` ~2 s; `probe_split_family_sensitivity.py` ~15 s; `probe_rc008_spec.py` ~2 s; `mutate_rc008_spec.py` ~70 s; `probe_rc008_round2.py` ~3 s; `probe_rc008_round3.py` ~4 s; `probe_rc007_convergence.py` <1 s; `mutate_rc007_convergence.py` ~5 s; `probe_rc007_round3.py` ~25 s; `probe_rc007_spec.py` ~2 s; `mutate_rc007_spec.py` ~2 min; `probe_filter_chain.py` ~20 s; `test_measure_host_drift.py` 18.3 s; `test_missing_depth.py` ~15 s; `test_band_drift.py` ~48 s; RC-002 mutation harness ~11 min; the rank-1 drift measurement ~3 min / 88.6 MB / 93 requests. **Take your own readings.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2`, `scipy==1.18.0` — all BSD-3-Clause. **`requirements.txt` was NOT touched S45–S52.** **scipy is pinned in the ROOT `requirements.txt` only.** SpikeInterface, PyTorch and Kilosort4 **still not installed** — Codex's Rung 0. Use `./venv/Scripts/python.exe`; never bare `python`/`pip`.

## 6. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity · **drift, for rank 1 only**. Checked **non-gating**: donor-lab separation.
Gate **specified but UNAPPROVED and now SPLIT: noise (§19). Part A verified but not approved; Part B unresolved and its question reshaped at S52.**
Gate **3 — post-rescaling effective SNR — IS IN FORCE, IS NOT SUPERSEDED, AND IS NOT DISCHARGED IN ANY PART.** It consumes the noise estimate, so it is downstream of §19.
Gates **open and Codex's**: joint ten-placement (Amendment 6 point 1) · the balance/manipulation gate.

### 6.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) — **DRIFT PASSED** · 2. NYU-12 **Probe01** `a8a8af78` (66) — **unpaused, unmeasured** · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`. Rank 1 is `b52182e7-39f6-4914-9717-136db589706e`.**

**Do not re-derive the order and do not re-sort it.** **Two passes:** the whole order at strict, then — only if nothing clears every gate — the same order restarted once at relaxed. **Gate order** (cheapest first): drift → noise → effective SNR → joint ten-placement → balance.

**⚠️ Four ranks — 5, 7, 9, 13 (NYU-65, NYU-45, NYU-39, NYU-48) — remain PAUSED on the declared-clock disagreement, not rejected.** **That pause is load-bearing twice: it is also the evidence §19.3 cites for refusing to adopt the recording's sampling rate.**

**⚠️ First-admissible means rank 1 is only the host if it clears EVERY gate — and it also means measuring rank 2 before rank 1 is settled is speculative compute.**

### 6.2 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Codex owns the footprint/placement calibration**; do not start it.

## 7. THE DRIFT RESULT — rank 1, measured 2026-08-17, replayed by Codex, approved at RC-006

| quantity | value |
|---|---|
| `Delta_10min` | **1.821 µm** (11-bin window from bin 1) |
| `Delta_full` | 2.537 µm |
| `Q95_null` | **0.526 µm** (nearest-rank, rank 190 of 200) |
| `inside_null` | **False**; threshold 20.0 µm strict |
| bins / units / spikes | 72 (0 invalid) / 140 of 174 / 3,160,311 |
| **verdict** | **passed True, `resolved, within tolerance`** |

**Missing-depth layer:** 231 missing (0.007309%) in 11 units; support invariance holds; `Delta_10min` bound **[1.780, 1.821]**; `Q95_null` bound **[0.533, 0.546]**; **disposition `passes`, advances True, conflict False.**

**Three things that must not be lost:**

1. **`inside_null` is False and `Delta_10min` is ~3.5× `Q95_null`.** Structure is resolved above the noise floor, and it is ~9% of tolerance. **Both halves are the measurement.**
2. **The finite-only `Q95_null` (0.526) falls BELOW its own completion bound [0.533, 0.546].** §17.9 declared this permitted in advance. **Do not "fix" it.**
3. **⚠️ THE PER-UNIT AUDIT IS LOUD AND THE RULE FORBIDS CONSUMING IT.** Whole-recording ranges over 140 units: min 1.259, median 9.155, p90 27.146, **max 71.629 µm; 21 exceed 20 µm, 11 exceed 40 µm.** **Per-unit values carry no null; comparison to `Q95_null` or `L` is undefined in either direction.**

## 8. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **footprint/placement calibration** · **real-arm donor-matching rule** · **exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 9. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`**. **Bounded-negative is the harder verdict.**
- **⚠️ A RESOLUTION DIAGNOSTIC ACTS IN ONE DIRECTION AND IN ONE PLACE.** `Q95_null` for drift and `R_null_sampled` for noise can convert a would-be pass into `unmeasurable`, and can change how a failure reads; **neither ever converts a would-be failure into anything else.** Settled at the RC-007 Convergence Decision.
- **⚠️ AND *CERTIFIES NOTHING* IS NOT *DOES NOTHING*.** A low `R_null_sampled` is necessary for a pass. Settled at Draft 34 by F6-R2.
- **⚠️ THE TWO SPLIT RULES ARE MEMBERS OF ONE 32-MEMBER FAMILY** (`p | 6,510`). **No parameter-count argument can select between them; the split is UNSETTLED and is Part B.** Draft 32's direction, Draft 33's near-independence and cannot-cash grounds, and Draft 34's free-parameter ground are **all withdrawn**. Settled at the RC-008 Convergence Decision.
- **⚠️ AND THE FAMILY *DOES* HAVE DOMINATING MEMBERS — 30 STRICT RELATIONS.** My S49 claim to the contrary is **withdrawn**, and with it the argument that the sweep defeats "pin one and disclose it." **It does not.**
- **⚠️ AND CODEX'S COMPLETION BOUNDS ARE EXACT, WITH THE MINIMUM NOT AT A VERTEX.** Proved at S51 by exhaustion, closed at n = 72 by Codex at S51; see 3.1c. **A vertex-only minimum is permissive for the branch-3 label.** **`u ≥ 8` of 72 is unbounded; `u = 0` reduces to Draft 34 exactly; every scalar convention is a completion, so the rule is one-way.**
- **⚠️ AND THE COMPLETION SEMANTICS DOES NOT SETTLE THE SPLIT.** S52: 28 of 32 members stand down and 4 withhold with **no undefined channel present**. See 3.1d. **Part B's question is now what licenses pinning one rule when the rule choice moves the verdict on fully defined data.**
- **⚠️ AND THE UNDEFINED SET IS A PROPERTY OF THE CHANNEL, NOT THE FAMILY.** S52: one shape fails under exactly the 16 EVEN members, another under exactly the 16 ODD, a third under exactly one. **Neither parity class is privileged.**
- **⚠️ AND S50's PERMISSIVENESS RESULT IS FIXTURE-SCOPED.** The frozen scalar rule's member disagreement has **no direction**: permissive on 14 cells, conservative on 1. Settled at S52.
- **⚠️ AND §19.4's FLOATING-POINT RANK FORM IS NOT A DEFECT.** It agrees with integer arithmetic at every n from 1 to 200,000. **Withdrawn at S51. Do not re-raise it.**
- **⚠️ A 0/0 ON A VALID SAMPLE IS NOT AN INPUT ERROR.** Codex, S50; accepted. It would pause the pinned order on a condition no data repair can cure.
- **⚠️ A CEILING AND A FLOOR CANNOT READ THE SAME EXTREMUM.** Settled at Draft 33 by F1-R1.
- **⚠️ AN UNMASKED BAD CHANNEL HAS NO CLAIMED DIRECTION**, and no bad-channel rule will be added.
- **The drift gate is two numbers.** `Delta_10min <= L` **and** `Q95_null <= L`. **Window is ELEVEN 60 s bins.** Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data **except a NaN depth (§17)**, failed replay. **A clock or coordinate mismatch is not one of them** — those pause the pinned order (§16.4).
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** A **single** displaced spike in a hundred moves the median `14.500 µm`.
- **The drift unit set is blind to `kilosort2_label`.**
- **The per-unit excursions are reported and never consumed.** **The absence of magnitude separation is not evidence either — and NOR IS ITS PRESENCE.**
- **The bin grid anchors at session `t = 0` with extent `t_last_s`.** **`duration_s` is a span, not an alternative clock.** **Endpoint containment cannot identify a clock — and neither can reference-instant agreement.**
- **The permutation pool is analysed-bin spikes only**, for both observation and null.
- **Amendment 6 governs: Tier A is parameterized by `N`.** `10 ≤ N ≤ 16`; `N < 10` is Slot 12.3. `q = ⌊50/N⌋`, `r = 50 mod N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.** **⚠️ AND SO, THROUGH `N`, ARE THE PER-DONOR ELIGIBILITY GATES.**
- **`N ≥ 10` is structural:** `16 − 6 = 10`.
- **The manipulation check is a hard stop-or-go gate**, and the realized zone-donor count is a *composition-integrity* quantity, **not** a substitute for it.
- **Amendment 5:** the injection zone's donors are removed from the **real** region-unaware arm before matching.
- **The matching rule's provenance test is two-level**; **Level A binds only at stages 3 and 4.**
- **0.11 and 0.12 are two sampling models, not two estimates.** Blocked expectations **1.03** and **1.17**.
- **CA1's sixteen donors sit in exactly 4 source datasets, `[6, 5, 3, 2]`**, 4 sessions, 4 animals. Library-wide: **37 insertions, 24 sessions, 12 animals**.
- **The source-count floor binds at *every* relaxation stage** and is an **equality**.
- **One host and injection zone across all tiers by default.** **CA1 is the approved first zone.**
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **The donor library is good-clusters-only by construction.**
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.** **§19 uses the RAW 50–200 µV peak-to-peak form.**
- **The Allen CCF ontology is not importable** — noncommercial terms.
- **A one-command-per-side runbook rule is a hard parse error, not a warning.**
- **NaN is the only missing marker. Both signs of infinity are input errors.** *(This is §17's rule for the DEPTH column. It is NOT a rule for `r_c(k)`, whose 0/0 case is handled by the completion bound — see 3.1c.)*
- **`reconcile_verdict`: a candidate advances only when the gate and the completion bound point the same way.**
- **The console contract:** report and record FIRST, then exactly two lines, reconciled decision **last**.
- **`peak_resident_bytes = cache_bound + resident + structures + library_cache` — four terms.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count; S27's five; S28's three plus the Round-2 ASCII claim; S29's one; S30's three; S31's two; S32's own; S34's two; S36's; S38's; S39's; S40's; S41's four; S43's threshold multiplier taken from memory; S43's six that RC-007 Round 1 caught; S43's input-error/unmeasurable conflation found at S44; S44's three that RC-007 Round 2 caught plus S44's loose coverage theorem; S45's one that RC-007 Round 3 caught; S46's two wrong expectations in my OWN new checker; S43–S46's five that RC-008 Round 1 caught plus the "about 223 s" figure and the 33-vs-32 tool-output count; S47's two that RC-008 Round 2 caught; S48's free-parameter ground, caught as F8-R3; S49's three — a tautological check in my own convergence probe, a README write that landed before its assertion, and an inherited tool-output count wrong by one; S49's "NO DOMINATING MEMBER", caught by Codex's audit; S50's two, both wrong expectations in my OWN new probes; S51's four, all caught by my own first run. **⚠️ AND NOW S52's FOUR: a withdrawn straddle expectation; a TAUTOLOGICAL CHECK WHOSE UNDERLYING CLAIM WAS ALSO FALSE; a note contradicted by its own numbers; and A DUPLICATE CHAT APPEND from an idempotence guard keyed on a timestamp.** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 10. The module surfaces

`missing_depth.py`: `median_interval` · `split_unit` · `missing_counts` · `unit_intervals` · `support_invariance` · `centre_bounds` · `centred_intervals` · `trace_intervals` · `interval_excursions` · `measure_missing_depth_sensitivity` · `replicate_bin_bounds` · `null_interval` · `stability_verdict`.

- **Import form is `from utils import band_drift`.** A bare `import band_drift` fails.
- `null_interval` returns `q95_lo` · `q95_hi` · `values_lo` · `values_hi` · `bounded` · `rank` · `n_permutations`. **There is no `q95` key** — but **the gate's own null in the JSON record IS `null.q95`**.
- `measure_missing_depth_sensitivity` **raises** if the point estimate falls outside its own bound.
- **`support_invariance` returns numpy arrays.**
- **Every entry point takes the COMPLETE per-unit arrays.** **`split_unit` is the one place the record is split.**

`measure_host_drift.py`: `reconcile_verdict` · `summarize_missing` · `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`, no sensitivity flag.** **`--help` renders 164 lines.**

`archive_units.py`: `MASK_ITEMSIZE` · `PROVENANCE_MAX_BYTES = 65536` · `PROVENANCE_BLOCK_BYTES = 65536` · `MEASURED_CONVERSION_VERSIONS`, never gated · `UNITS_PATH` · `TIME_COLUMN` · `DEPTH_COLUMN`. Transfer budget **393,216**. **There is no plan key called `bytes`.** **`ascii_safe` is here.**

- **Record `plan` keys:** `logical_bytes` · `cache_bound_bytes` · `resident_bytes` · `mask_bytes` · `structures_bytes` · `library_cache_bytes` · `peak_resident_bytes` · `spent_bytes` · `block_bytes` · `bound_basis` · `n_units` · `n_spikes` · `time_layout` · `depth_layout`. **No `per_unit` key.**
- **`REFERENCE_TIME_FORM` gates the lexical shape before `fromisoformat`. ⚠️ THE UTC-OFFSET REQUIREMENT IS DELIBERATELY NOT IN THE GRAMMAR.** **Do not "tidy" this.**

`band_drift.py`: `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** Symbol `Delta_10min`. `apply_gate` returns **`passed`**. Others: `bin_seconds` 60, `min_spikes_per_bin` 10, `min_bin_fraction` 0.8, `min_units_per_bin` 5, `n_permutations` 200, `null_percentile` 95, `master_seed` 3175830281, thresholds 20/40 µm.
- **`unit_traces` raises on non-finite depths.** `complete_bins(extent_s)` **anchors at 0**. **Rank 2's `t_first_s` is −0.000047 s**, so sub-zero exclusion is live.

`screen_host_timing.py` holds `read_series_timing`, which is what `probe_raw_ap_layout.py` mirrors for the layout read.

### 10.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`. **Do not weaken into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size.** `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4`.
3. **The provenance-budget invariant**, on both assets, on every case reaching a record.
4. **The fixture axes are separate on purpose:** `provenance=` **and** `reference_time=` independently.
5. **`run_case(..., capture=False)`** gives `result["stdout"] is None`, not `""`.
6. **`_nan_at(units, positions)`** sets NaN at **stated** positions.
7. **`check_console_decision(...)`** is the shared console assertion.
8. **`case_the_ceiling_counts_the_retained_masks`** builds ceilings from the **fixture's** spike count. **Do not "simplify" it.**

### 10.2 The S49–S52 probe surfaces

- **`probe_rc008_convergence.py`** — requires `--out`, takes `--records`. **No project input.** `divisors(6510)` → 32; `block_mask(p, n)`; `parity_core(...)`; `disposition(...)`. **22 checks.** `--help` 8 lines.
- **`probe_split_family_sensitivity.py`** — requires `--out`, takes `--records`. `core_at(...)`, `sweep(...)`. **12 checks plus one `NOTE`.** `--help` 8 lines. **⚠️ UNREVIEWED, AND ITS DOCSTRING CARRIES THE WITHDRAWN CLAIM. DO NOT EDIT IT.**
- **`probe_split_family_narrowing.py`** — **requires `--source --out`, takes `--records`.** ⚠️ `--source` is the ONLY input flag of mine that names an INPUT. `divisors` · `median_by_sort` · `sigma_by_sort` · `nearest_rank_index` · `spread_by_rank` · `mask_by_repeat` · `core_by_tile` · `disposition` · `recompute` · `signatures` · `strict_dominance`. **Pins `SOURCE_SHA256 = f51b4949…` and authenticates before reading.** **24 checks plus 4 `NOTE`s.** `--help` 10 lines.
- **`probe_null_ratio_undefined.py`** — requires `--out`, takes `--records`. `divisors` · `sigma_hat` · `block_mask` · `ratio_under` (**deliberately unguarded**) · `step_channel` · `alternating_channel` · `dead_half_channel` · `majority_share` · `nearest_rank` · `spread` · `disposition` · `band_with`. **20 checks plus 5 `NOTE`s.** `--help` 8 lines. **⚠️ UNREVIEWED. ⚠️ PINNED BY DIGEST INSIDE THE S52 PROBE — DO NOT EDIT.**
- **`probe_completion_bounds.py`** — requires `--out`, takes `--records --fixtures`. **No project input.** `nearest_ranks` (INTEGER arithmetic) · `nearest_ranks_float` · `rho` (returns **None** for a band-level 0/0 or ∞/∞) · `bounds_exact` (three-level (a, b, j) enumeration; returns `lo`, `hi`, `undefined_reachable`, **`upper_effective`**) · `bounds_vertex_only` · `lo_closed` · `refined_grid` · `bounds_brute` · `max_over_windows` · `max_over_windows_brute` · `stands_down` · `branch3_label` · `disposition` · **`frozen_disposition`** (Draft 34's four branches with a SCALAR `R_null_sampled`, NaN included) · `numpy_nan_rho` · `random_finite`. **45 checks plus 8 `NOTE`s.** `--help` 11 lines. **⚠️ UNREVIEWED. ⚠️ PINNED BY DIGEST INSIDE THE S52 PROBE — DO NOT EDIT.** **⚠️ `upper_effective` is `+inf` whenever an undefined ratio is REACHABLE — read that, never `hi`, for a decision.**
- **`probe_member_comparison.py`** — **NEW S52.** Requires `--out`, takes `--records`. **No project input.** `sha256_of` · `authenticate_sources` · `median_share` · `segment_channel(n)` · `amplitude_parity_channel` · `amplitude_block_channel(block)` · `amplitude_ramp_channel` · `finite_pool(shape, m)` (shapes `flat` `tight` `biting` `onetail` `spread` `highlow` `withzero` `eighteens`) · `closed_form_n72` (**my own re-derivation of Codex's formula, valid for `u ≤ 7` and a positive finite rank-8 value**) · `jsonable`. Inside `main`: local `describe_set` and `band_readings`. **37 checks plus 40 `NOTE`s.** `--help` 9 lines. **⚠️ UNREVIEWED, and its docstring says so.** **⚠️ IT EXITS 1 WITHOUT RUNNING A CHECK IF EITHER PINNED SOURCE DIGEST HAS MOVED — verified by breaking it on a clean copy, both for a mutated source and a missing one.**

## 11. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). **S33, S36, S44, S47, S48 are the sharpest instances.**
2. **Read the column, do not count it** (S5, S43, S44). **AND COUNT THE FILES RATHER THAN INCREMENTING A COUNT** (S47–S52). **S52 counted 32 scripts and 52 outputs from the directory; the workspace README's own paragraph still carried "thirty scripts and fifty outputs" from S50, and the correction is appended forward rather than edited backward.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30–S33, S36, S45).
4. **A clean trend invites a causal story you have no way to check** (S5, S33, S36). **AND SO DOES A CLEAN NUMBER** (S49). **WHEN THE CLEAN NUMBER SURVIVES, GO AND FIND THE MECHANISM AND CHECK *THAT*** (S50). **⚠️ S52: AND WHEN THE PATTERN LOOKS ORDERED, CHECK THE ORDER.** "The four withholding members are the four longest block lengths" was false; 3255 stands down while the shorter 2170 withholds.
5. **In an owner re-review, the pull is to accept everything** (S6).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **⚠️ A heredoc through the Bash tool mangles nested quotes AND backslash escapes. WRITE SUCH SCRIPTS WITH THE WRITE TOOL.** **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32, S47–S49).
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32, S36). **NOR MAY A RULE BE ADDED AFTER ITS FAILURE MODE IS KNOWN.** **DO NOT ASSERT AN INVENTED MARGIN — MEASURE THE DISTRIBUTION** (S50).
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7).
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S33, S42–S44).
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32, S33, S36).
13. **A correction is worth logging even when the conclusion survives** (S8, S29, S37, S42, S43).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9, S15, S47–S49).
16. **An audit must use the same key its lookup uses** (S9, S27, S28, S31).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10, S42). **A REVIEWER'S FINDING IS TOO** (S47, S48).
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17, S23, S28, S29).
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11, S27–S29, S33). **S41 is the positive instance.**
24. **Note which direction a correction pushes** (S11, S15, S16, S26, S38, S43, S44). **AND WHEN AN UNHANDLED CASE HAS A DIRECTION, SAY IT** (S50). **⚠️ S52: AND CHECK WHETHER IT HAS ONE AT ALL.** The frozen scalar rule turned out to move in **both** directions, which is a different and worse finding than "it is permissive."
25. **When a test fails, first ask whether the test or the artifact is broken** (S11, S37, S39, S40, S42–S45, S47, S48, S50–S52). Say which resolution you took.
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S52).
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29, S40, S43–S45, S47, S48). **S52: the digest guard was verified by a one-byte mutation AND by a missing file, each on a fresh copy.**
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27, S36, S44, S50).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26, S34). So assert it.
31. **A supersession can be too broad as well as too narrow** (S14, S39, S43–S45).
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28, S36, S43).
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32, S34–S52). **⚠️ AN APPEND-STYLE EDIT CONTAINS ITS OWN OLD TEXT.** **⚠️ AND SEE 118: VALIDATE BEFORE WRITING, NOT AFTER.**
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Thirty-two for thirty-two (S15–S52).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26, S44).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32, S33, S35).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17, S43) — **and then check whether the null can be moved by the thing it controls for** (S45).
41. **⚠️ READ THE CLOCK AT THE MOMENT YOU WRITE THE TIMESTAMP** (S17, S45, S48–S52). **`time.strftime("%Z")` returns the long name on Windows: use a literal `PDT`.** **⚠️ AND SEE 129 — A TIMESTAMP READ AT WRITE TIME MUST NOT BE WHAT AN IDEMPOTENCE GUARD KEYS ON.**
42. **⚠️ A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24, S34, S35, S37, S38, S42, S44, S47, S48).
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30, S34, S35, S40).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32, S34). **And which *currency* it is denominated in.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26, S47).
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28, S44, S47).
50. **A counterexample built on a degenerate case invites dismissal** (S24, S26, S37, S38). **GENERALISE THE COUNTEREXAMPLE YOU ARE HANDED** (S48). **AND CHECK WHETHER YOUR OWN POSITION IS INSIDE THE GENERALISATION** (S49).
51. **A near-miss is not the finding** (S24).
52. **A test can encode the defect it was written to catch** (S25, S28).
53. **Two independent errors can cost the same amount and coincide exactly** (S25). **⚠️ S52 IS THE SHARPEST INSTANCE AND IT IS ABOUT RESULTS, NOT ERRORS: 14 bounded-conservative cells and 14 scalar-permissive cells, DISJOINT.** When two counts match, check whether the sets do, and assert the answer either way.
54. **A tightening is affordable exactly once: before the first measurement** (S25). **⚠️ STILL OPEN for the noise gate.**
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32, S35, S38, S39).
56. **Which fixture a published number came from is part of the number** (S25, S26, S37, S45, S47, S49). **STATE WHERE THE FIXTURE'S VALUES SIT RELATIVE TO THE THRESHOLD** (S50). **⚠️ S52 ACTED ON IT IN ADVANCE:** the ramp band's pool is **1.8 and not 2.0** precisely so the passing side is not sitting on `M`, and the probe asserts the 0.029806 clearance.
57. **A check that cannot fail is not a check** (S27–S33, S37, S44, S47–S49). **A CHECK WHOSE BODY IS SOUND CAN CARRY A DETAIL STRING THAT CLAIMS SOMETHING ELSE** (S50). **⚠️ S52 IS THE SIXTH VARIANT AND THE WORST: A TAUTOLOGICAL CHECK WHOSE UNDERLYING CLAIM WAS ALSO FALSE.** I wrote `round(x,12) == round(x,12)` to "prove" the publication set hides the member disagreement — and it does not hide it; the endpoint pair reveals it. **A check that cannot fail cannot tell you your claim is wrong, which is exactly when you need it to.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen; S42 posted one.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). **Three for three.**
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair.**
62. **Evidence must come from the exact state you publish digests for** (S31, S34, S35, S37, S41–S43). **⚠️ S52: AND IF YOU EDIT THE ARTIFACT AFTER PUBLISHING ITS DIGEST, POST A FORWARD CORRECTION NAMING THE NEW ONE.** I added an unreviewed-status line to a docstring after publishing the digest; the records were byte-identical but the script digest was not, and a replay against the old digest would have failed.
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32, S34, S40, S43, S47, S48).
64. **When a reviewer's finding is correct, check whether it is *complete*, and whether its *evidence* proves it** (S32, S37, S38). **RE-DERIVE a handed-over number yourself** (S41–S45, S47–S52). **⚠️ S52: AND RE-DERIVE A HANDED-OVER FORMULA FROM ITS PROSE, NOT FROM ITS CODE.** Implementing Codex's closed form from his chat message rather than his script is what makes agreement evidence instead of a copy.
65. **An undetermined value is a missing measurement, not a negative one** (S33, S34, S36, S37).
66. **Test a hypothesis on data that did not suggest it** (S33, S36).
67. **⚠️ Do not both discover an input error and rule on its disposition in the same session** (S33, S36). **Post the design, including where you deviate, before writing the code** (S37–S40, S43).
68. **Separate the fixture's axes before you need them separate** (S34).
69. **A closed card's evidence script may legitimately go red** (S34). **Do not extend a closed card's harness — write a new one** (S40). **An OPEN card's harness is EXTENDED IN PLACE** (S44, S45, S47, S48). **⚠️ RC-007 AND RC-008 ARE BOTH CLOSED, SO ALL NINE OF THEIR SCRIPTS ARE FROZEN.**
70. **A note added to a docstring is printed surface** (S34, S40, S41).
71. **⚠️ BEFORE ADDING A SECOND ENFORCER OF A PROPERTY, ASK WHAT THE MUTATION FOR THAT PROPERTY REVERTS** (S35).
72. **A whole-command test can have its meaning moved by a change elsewhere while staying green** (S35).
73. **The trusted parser is part of the input surface** (S35). **SO IS A TRUSTED SUBPROCESS** (S47). **AND SO IS EVERY FILE THAT SUBPROCESS OPENS** (S48). **⚠️ S52: AND SO IS EVERY MODULE YOU IMPORT — WHICH IS WHY THE NEW PROBE PINS BOTH OF ITS IMPORTS BY DIGEST AND REFUSES TO RUN IF EITHER MOVED.**
74. **A diagnostic that answers "how bad is it" must also answer "what would the fix cost"** (S36). **⚠️ S52 PRICED UNANIMITY: one dissenting member of 32 is enough to reject.**
75. **When you refuse to use a measured pattern, record it anyway and say why you refused** (S36, S41, S43, S45).
76. **⚠️ AN AVERAGING STRUCTURE AND A SYSTEMATIC PERTURBATION SCALE DIFFERENTLY** (S37).
77. **Show the vacuity rather than delivering the vacuous bound** (S37). **FIRST PROVE THE VACUITY** (S38).
78. **Where a bound is exact and where it is an outer bound are different claims** (S37).
79. **⚠️ AN IMPOSSIBILITY ARGUMENT TURNS ON ONE WORD** (S38).
80. **⚠️ TESTING A BOUND AGAINST A RESTATEMENT OF ITS OWN DEFINITION TESTS ONLY THAT TWO HALVES OF ONE ARGUMENT AGREE** (S38, S49).
81. **The sharpest containment evidence is a completion landing exactly on an endpoint** (S38, S41).
82. **A test that is numerically right because two paths agree is not a test that they agree** (S38).
83. **⚠️ A CONSTANT COMPLETION AT A DISTRIBUTION'S CENTRE IS A DEGENERATE FIXTURE** (S38). **A DEGENERATE FIXTURE ANNOUNCES ITSELF AS `NaN`, WHICH A `> M` COMPARISON SILENTLY READS AS A PASS** (S49). **S50 FOUND THE SAME HOLE IN THE SPECIFICATION ITSELF.**
84. **⚠️ A WHOLE-FILE REWRITE OF A TEST SUITE IS A COVERAGE RISK** (S38). `git show HEAD:<path>` recovers the prior implementation. **⚠️ S52: AND IT RECOVERS A BOTCHED APPEND TOO — see 129.**
85. **⚠️ A REVIEWER'S INSTRUCTION CAN HAVE TWO PARTS — OR THREE OPTIONS** (S39, S45, S47, S48). **AND WHEN A SURVIVING GROUND IS THIN, THE NEXT ROUND WILL BREAK IT** (S49).
86. **⚠️ AN ASSERTION ABOUT AN EDIT CAN FAIL WHILE THE EDIT IS CORRECT** (S39, S45, S48). **⚠️ S52 IS THE CLEANEST INSTANCE: MY POST-WRITE ASSERTION WAS BROADER THAN MY PRE-WRITE ONE** — it checked the whole file for ASCII where the pre-write check covered only my addition, so it tripped on Codex's em dashes. **The two assertions must cover the same region or the failure tells you nothing.**
87. **⚠️ CONSUMING A DIAGNOSTIC IS WHERE THE POLICY GETS MADE** (S39).
88. **Publish an aggregate and the thing it aggregates** (S39, S42). **WHEN A DIRECTION CLAIM IS WITHDRAWN, PUBLISH THE RAW VALUES** (S47, S48).
89. **⚠️ A THRESHOLD COMPUTED FROM THE QUANTITY UNDER TEST MOVES WITH THE DEFECT** (S40).
90. **⚠️ A POST-WRITE CHECK CAN FAIL ON ITS OWN STRING RATHER THAN ON THE WRITE** (S40, S52).
91. **A defect that lives only in the console is invisible to a suite that reads only artifacts** (S40).
92. **⚠️ A DESIGN DECISION ARGUED ON FIXTURES GETS EXERCISED BY REAL DATA** (S41).
93. **⚠️ THE MOMENT A RULE STOPS BEING FREE TO CHANGE IS THE MOMENT ITS FIRST VALUE IS KNOWN** (S41).
94. **⚠️ REMOVING A DECLARATION REMOVES THE MUTATIONS THAT TESTED IT** (S41, S48).
95. **⚠️ A DIFFERENCE BETWEEN TWO SAMPLES OF A TOTAL DOES NOT MEASURE A PART OF IT** (S42).
96. **⚠️ THE INSTRUMENT CAN BE RIGHT WHILE THE PROSE READING IT IS WRONG** (S42). **S50 IS THE INVERSE: MY OWN SUMMARY OF A DOCUMENT WAS LOOSER THAN THE DOCUMENT.** Read the source before writing the claim, including when the "source" is this file's own paraphrase.
97. **⚠️ THE PLAIN-LANGUAGE REGISTER IS WHERE A BOUNDARY GETS LOST** (S42).
98. **⚠️ S43 — READING THE STORAGE LAYOUT CHANGED THE DESIGN, IT DID NOT CONFIRM IT.**
99. **⚠️ S43 — A MULTIPLIER YOU CANNOT TRACE TO A SOURCE THIS SESSION IS A MULTIPLIER FROM MEMORY.**
100. **⚠️ S43/S44 — A GATE'S REAL CONTENT IS WHAT IT CAN REJECT THAT NOTHING ELSE CAN.**
101. **⚠️ S44 — READ THE SOURCE OF A TOOL YOU ARE IMITATING, NOT ITS DOCUMENTATION AND NOT YOUR MEMORY OF IT** (S45, S47).
102. **⚠️ S44 — WHEN A CLAIM IS FALSE, CHECK WHETHER THE FIX IS TO BOUND IT OR TO REMOVE ITS CAUSE.**
103. **⚠️ S44 — A NUMBER RESTATED N TIMES IS N PLACES IT CAN DIVERGE.**
104. **⚠️ S44 — WITHDRAWING A PROPOSAL IS A COMPLETE ANSWER, AND USUALLY A BETTER ONE THAN NARROWING IT.**
105. **⚠️ S44/S48/S49 — A PROPOSAL MADE IN THE SAME DRAFT THAT FIRST CONSTRUCTS ITS ARGUMENT HAS NOTHING CHECKING IT. THIS IS MY MOST REPEATED ERROR.** **S50 was the first session that acted on the fix; S51 and S52 did the same — evidence plus a question, no candidate.** **Keep doing it unless Codex's reply supplies the missing check.**
106. **⚠️ S45 — "REMOVE THE DEVIATION" AND "BOUND THE DEVIATION" ARE DIFFERENT KINDS OF ANSWER.** **S47 ADDS "DECLARE THE DEVIATION."**
107. **⚠️ S45 — A TRUE STATEMENT THAT DOES NOT FOLLOW FROM ITS OWN PREMISE IS STILL A DEFECT.**
108. **⚠️ S45 — AN EXPENSIVE REPAIR NEEDS ITS ALTERNATIVES PRICED IN THE ARTIFACT** (S47).
109. **⚠️ S46 — WHEN TWO SENTENCES IN YOUR OWN DOCUMENT DISAGREE, LOOK FOR AN ALREADY-APPROVED SECTION THAT ANSWERS THE SAME QUESTION.**
110. **⚠️ S46 — A REVIEWER'S FINDING CAN BE RIGHT AND ITS SCOPE STILL SHORT.** **Count the surfaces mechanically.**
111. **⚠️ S46/S47 — A CLOSED CARD'S CHECKER IS A REGRESSION BASELINE, NOT DEAD WEIGHT, AND YOU MUST AUTHENTICATE IT BY DIGEST FIRST** (S48). **⚠️ S52 GENERALISED THIS INTO CODE: AUTHENTICATE BEFORE IMPORTING, AND FAIL CLOSED.**
112. **⚠️ S46 — STATE THE HONEST REACH OF A BLOCKER ALONGSIDE ACCEPTING IT.**
113. **⚠️ S46 — SETTLE A DEFERRED DESIGN QUESTION AT THE FIRST MOMENT THERE IS SOMETHING NEW TO CHECK IT.**
114. **⚠️ S47 — A DECLARED BOUND IS NOT ENFORCED UNTIL THE BRANCH *AND* THE STATISTIC IT READS CAN ENFORCE IT.**
115. **⚠️ S48 — *CERTIFIES NOTHING* IS NOT *DOES NOTHING*.**
116. **⚠️ S48/S49 — WHEN A CLAIM IS WITHDRAWN, ASK WHETHER WHAT REPLACES IT IS A *DIRECTION*, A *REACH*, OR A *CATEGORY ERROR*.**
117. **⚠️ S48 — WRITE THE TIMESTAMP FROM A READING, NOT FROM AN ESTIMATE.**
118. **⚠️ S49 — VALIDATE AN EDIT BEFORE WRITING IT, NOT AFTER.** **Compose the new text in memory, run every structural assertion against the COMPOSED text, then write, then re-run the same assertions against the read-back.** **⚠️ S52 ADDS THE MISSING HALF: THE TWO SETS OF ASSERTIONS MUST COVER THE SAME REGION — see 86.**
119. **⚠️ S49 — SAY WHICH READING YOU COULD NOT REFUTE.**
120. **⚠️ S49 — WORK PRODUCED OUTSIDE FORMAL REVIEW MUST SAY SO WHERE IT LIVES, NOT ONLY WHERE IT IS ANNOUNCED.** **⚠️ S52: AND IF A README ASSERTS THAT A DOCSTRING SAYS SO, GO AND CHECK THAT IT DOES.** Mine did not; adding it cost a digest correction, which was the right price.
121. **⚠️ S50 — A BYTE-FOR-BYTE REPRODUCTION PROVES DETERMINISM, NOT CORRECTNESS.** **When a result matters, rebuild it along a deliberately different code path and require cell-by-cell agreement.**
122. **⚠️ S50 — WHEN YOU CORRECT AN OVERCLAIM, PUT THE WITHDRAWAL WHERE THE CLAIM LIVES, EVEN WHEN THE FILE ITSELF MUST NOT BE EDITED.**
123. **⚠️ S51 — AN EXTREME OVER A BOX IS NOT ALWAYS AT A VERTEX, AND WHICH ENDPOINT FAILS DEPENDS ON WHICH DIRECTION EACH COORDINATE HELPS.**
124. **⚠️ S51 — WHEN A PROPOSED RULE REPRODUCES A THRESHOLD THE EXISTING SPECIFICATION ALREADY HAS, THAT IS EVIDENCE ABOUT THE RULE.**
125. **⚠️ S51 — A LIBRARY'S DEFAULT ORDERING CAN BE EXACTLY ONE COMPLETION OF MANY.**
126. **⚠️ S51 — A CHECK YOU WROTE EXPECTING IT TO FAIL, WHICH PASSES, IS A RESULT AND STAYS IN THE SUITE.** **⚠️ S52 IS THE MIRROR AND IT PAID BETTER: A CHECK YOU WROTE EXPECTING IT TO PASS, WHICH FAILS, IS ALSO A RESULT — AND REPLACING IT WITH THE CLAIM THE MEASUREMENT DOES SUPPORT IS WHERE THE SESSION'S HEADLINE CAME FROM.** The straddle check failed; what replaced it was *member dependence needs no undefined case*, which led directly to the ramp band.
127. **⚠️ S51 — A TEST THAT SILENTLY CHANGES A DERIVED CONSTANT IS BROKEN EVEN WHEN ITS FINDING IS SOUND.** **When a fixture has a size, pass the size, do not recompute it from a subtraction.**
128. **⚠️ S51 — A SAMPLING SWEEP CANNOT PROVE A GAP AND CANNOT PROVE A BOUND.** **State the open question as open, and name the check that would close it.** **S52 note: Codex closed exactly the check I named.**
129. **⚠️ S52 — AN IDEMPOTENCE GUARD MUST NOT KEY ON A VALUE THE CLOCK CHANGES.** My chat-append guard tested for the full timestamped header. The first run wrote a `12:24` header and then failed on an unrelated post-write assertion; the second run built a **`12:25`** header, did not find it, and appended the **entire message twice**. **The repair: `git show HEAD:<path>` recovered the exact pre-append state, verified byte-for-byte at 25,553 bytes; the guard was re-keyed on the session-stable `**Claude (Session 52,` marker; the append was made once and the guard verified to refuse a second run.** **Key an idempotence guard on the thing that identifies the WRITE, never on the thing that identifies the MOMENT.**
130. **⚠️ S52 — A CETERIS PARIBUS COMPARISON MUST SAY SO IN ITS OWN OUTPUT, NOT ONLY IN THE HANDOFF.** Section 3's decision comparison holds the finite ratios fixed across members while section 2 of the same probe measures that assumption to be false in general. **The probe prints that contradiction as a `NOTE` above the section it limits**, so a reader of the record cannot take the comparison for more than it is.

## 12. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **RC-001–RC-008 are ALL CLOSED.** **⚠️ RC-008 consumed clause 5.** **A new card gets a new chat.**
- **`Playbooks/review-cycle.md` is two documents in one file:** read the superseding top section.
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator.** **⚠️ MEASURE the separator's position from the file rather than trusting a line number or an inherited claim about trailing newlines — S52's insertion script located it by finding the last `---` above the anchor heading and asserted the new entry was the last dated line immediately above it.** **96 dated entries — COUNT THEM.** **⚠️ Corrections propagate forward; do not "fix" an earlier entry.**
- **Status lines in the selection document are a stack.** Draft N's line goes above Draft N−1's. **Retained lines keep their errors**, and `probe_rc008_spec.py` asserts that they do.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. **S52's mutation copies were deleted after verification.**
- **A long archive read belongs in the background.**
- **`RemoteFile` validates and retries range responses.** Counters `n_bytes` / `n_requests` — **total every read**. **⚠️ ITS CACHE IS UNBOUNDED AND NEVER EVICTED.**
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py`, `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`, `missing_depth`. **`read_series_timing` lives in `screen_host_timing.py`.**
- **The runbook checker walks `scripts/` non-recursively.** **A script in `scripts/` without a step is a hard failure unless declared in `PENDING_STEP`**; **`PENDING_STEP` is empty.** **None of S43–S52's tools is in the packet, so none needs a step.**
- **Scripts must not print non-ASCII.** cp1252. **Check by capturing `--help`** — `measure_host_drift.py` **164**; `probe_completion_bounds.py` **11**; `probe_split_family_narrowing.py` **10**; `probe_member_comparison.py` **9**; `probe_rc008_convergence.py`, `probe_split_family_sensitivity.py` and `probe_null_ratio_undefined.py` **8 each**; `probe_rc008_spec.py`, `mutate_rc008_spec.py`, `probe_rc008_round2.py` **10 each**; `probe_rc008_round3.py` **11**; `probe_rc007_round3.py` **46**; `probe_rc007_spec.py` **38**; `mutate_rc007_spec.py` **39**; `probe_rc007_convergence.py` and `mutate_rc007_convergence.py` **11 each**; `probe_filter_chain.py` **49**; `probe_raw_ap_layout.py` **39**; all 0 non-ASCII. **⚠️ A failure DETAIL string can carry non-ASCII even when the labels do not.**
- **Line endings are pinned by `.gitattributes`, which sets `* -text`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (**338/338 at S52 close**); the root `README.md`, the packet README, the selection document, the Review Cards and all chat files are LF. **⚠️ `grep -c $'\r'` THROUGH THE BASH TOOL REPORTS 0 ON THAT CRLF FILE — Git Bash translates. CHECK LINE ENDINGS FROM PYTHON, on bytes.** **A pattern edit over a CRLF file must carry `\r\n` in the match string**, and assert the ratio afterwards. **⚠️ AND PRINTING THAT FILE FROM PYTHON NEEDS `sys.stdout.reconfigure(encoding='utf-8')` — its box-drawing characters crash a cp1252 console.**
- **⚠️ THE CHAT FILES CONTAIN NON-ASCII IN CODEX'S TURNS** (em dashes, curly quotes — 11 characters in the Part B chat at S52 close). **They are his and the append-only rule forbids touching them. Scope any ASCII assertion to YOUR OWN appended region.**
- **⚠️ THE WORKSPACE README'S TREE HAS A FIXED DESCRIPTION COLUMN AT 36 CHARACTERS.** Build rows with `ljust(36)` and assert `row[35] == " "` before writing.
- **Both `.gitignore` files ignore `__pycache__/`.** **`Reproducibility Packet/results/` is NOT ignored.**
- **`agents/Claude/tools/` holds THIRTY-TWO scripts and FIFTY-FOUR non-script files** (fifty-two recorded outputs and two pinned session lists), counted from the directory this session, **not inherited**; `__pycache__/` is ignored. **⚠️ RC-007's AND RC-008's SCRIPTS ALL BELONG TO CLOSED CARDS — do not extend any of them.**
- **Read the parser before inventing a flag.** **`probe_member_comparison.py` requires `--out` and takes `--records`.** `probe_split_family_narrowing.py` requires `--source --out` and takes `--records` — `--source` is an INPUT and is the only one of its kind of mine. `probe_completion_bounds.py` requires `--out` and takes `--records --fixtures`; `probe_null_ratio_undefined.py`, `probe_rc008_convergence.py` and `probe_split_family_sensitivity.py` require `--out` and take `--records`; `probe_rc008_round3.py` and `probe_rc008_round2.py` require `--repo-root --out` and take `--records`; `probe_rc008_spec.py` requires `--repo-root` and takes `--out --records`; `mutate_rc008_spec.py`, `mutate_rc007_spec.py` and `mutate_rc007_convergence.py` require `--repo-root --work-root` and take `--python`; `probe_rc007_round3.py` requires `--out` and takes `--records --seeds`; `probe_filter_chain.py` requires `--repo-root --out` and takes `--records --margins --excursions`; `probe_raw_ap_layout.py` requires `--repo-root --session --probe --assets-cache --out` and takes `--records --band-channels --block-kb`; `probe_rc007_spec.py` requires only `--repo-root`; `probe_rc007_convergence.py` requires `--repo-root --out` and takes `--records`. **Codex's `probe_split_family_dominance.py` requires `--records --out` and takes `--json`, where `--records` is its INPUT** — the opposite of my convention. **Codex's `probe_completion_bounds_n72.py` requires `--out --records` and takes `--random-fixtures`.**
- Older probes: `test_band_drift.py` `--permutations`; `test_measure_host_drift.py` `--keep`/`--tmp-root`; `test_missing_depth.py` `--permutations`/`--completions`; the `verify_rc00*` and `probe_*` scripts require `--repo-root`.
- **Git history is a verification tool.** `git show '<sha>:<path>'` recovers any prior exact state. **To prove a closed section of a growing document is byte-identical, hash the section body between two headings.** **⚠️ AND IT IS THE REPAIR PATH FOR A BOTCHED APPEND — see section 11 item 129.**
