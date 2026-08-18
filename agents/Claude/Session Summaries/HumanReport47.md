# Human Report 47 — Claude

**Date and time:** 2026-08-18 08:19 PDT

**Phase:** Phase 2 — Execution. Specification review of the host noise gate.

**Session outcome:** Codex's RC-008 Round 1 returned `Revisions Required` with **five blocking findings and four tracked items**. **All nine are accepted; none is disputed.** The Round-2 candidate is **Draft 33** of `agents/Claude/Tier A Host and Injection Zone Selection.md`. **Three of the five change something the gate actually reads**, which makes Draft 33 the first draft of §19 since Draft 30 in which anything executable moves. **No threshold value moved.** No estimator was written, no archive sample was read, no candidate's noise value exists, no packet file changed, no host is pinned, and rank 2 remains unmeasured.

---

## 1. What this session was for

Session 46 closed RC-007 at `Revisions Required` by the Convergence Decision, repaired the surviving defect outside formal review as Draft 32, and opened **RC-008** — the one successor the method allows, with **clause 5 binding**: if this card also reaches a non-approval, no second like-for-like successor is permitted and the work must be split or redesigned.

Codex ran RC-008's Round 1 as a full-artifact pass and returned five blockers and four tracked items. This session is the owner's Round-2 response: accept or dispute each, repair the artifact, strengthen the instruments, and present an exact candidate.

## 2. The five blocking findings, and what each repair was

### F1-R1 — a maximum cannot enforce a floor

§19.6 has declared a `1.25 µV` anti-saturation floor since Draft 29 and gave it a decision branch at Draft 30. Both the declared band and the branch tested it against `sigma_worst_sampled`, the **maximum** band level over the sixty sampled windows. A maximum cannot establish that *no* sampled window is too quiet.

The fixture is exact and I reproduced it independently: fifty-nine sampled windows at `1.0 µV` and one at `5.0 µV` give a maximum of `5.0 µV`, which clears Draft 32's level test in both directions, while fifty-nine of the sixty windows sit below the floor and the quietest injected unit in each would sit at `A_min / S(k) = 50` — past the anti-saturation ceiling of 40 that the floor exists to impose.

**The repair defines a second extremum rather than a second threshold.** §19.4 now defines **`sigma_quietest_sampled = min_{k ∈ G} S(k)`**; §19.6's branch 2, admissible band, pass rule and parameter table route the floor to it and leave the ceiling on `sigma_worst_sampled`; §19.7 publishes it. **The threshold value did not move — what moved is which statistic it is compared to.**

**The repair also found the same defect one layer down.** §19.8 reports two effective-SNR ratios and divided **both** by `sigma_worst_sampled`. One of them is the number condition 3 rearranges, so it was wrong for exactly the same reason. §19.8 now reports three ratios, each on the extremum it actually reads.

This is the second time this section has failed in this family: RC-007's F1 found a declared interval whose decision rule tested only one end, and gave the floor a branch. F1-R1 found that the branch it was given could not fire. **A declared bound is not enforced until both the branch and the statistic it reads can enforce it**, and I recorded that in §19.14 rather than treating it as a one-off.

### F2-R1 — the design rate, and the repair I deliberately did not take

§19.3 designs the Butterworth at the nominal 30,000 Hz and claimed the retained samples **are** `FilterRecording.get_traces`. SpikeInterface designs from the recording's own sampling frequency, so the claim was false in the exact sense it was written in. Codex's coefficient figure reproduces here **to every digit**: `1.31860735664e-07`.

Round 1 permitted either repair — adopt the recording rate, or declare the deviation and narrow the claim. **I took the second, which is the weaker-looking answer, and the reason is evidential rather than aesthetic: there is no unambiguous "recording rate" to adopt on this dataset.**

- Rank 1's raw AP series carries **no `rate` attribute at all**. `Reproducibility Packet/results/host_timing_index.jsonl` records its `timing_source` as `timestamps`.
- The `30,000.039869961383 Hz` figure is therefore **this project's own derivation** over the whole span. The first thousand timestamps give `30,000.03989331282 Hz`.
- **The other probe in the same session declares `29,999.999999999996 Hz`.**
- **Four ranks of the pinned host order are already paused on a declared-clock disagreement** of exactly this kind (§16.4).

Adopting it would exchange a pinned constant for an unpinned derivation, and would leave the identity claim resting on a SpikeInterface estimation rule this project cannot verify without installing the library. So the nominal rate becomes a **third declared deviation**, the identity claim narrows to "in every respect but the filter's design rate", §19.10 carries it as a limitation, and §19.7 publishes both rates per candidate so the deviation is auditable.

**Two things that could have made this worse are computed rather than assumed, and do not:** scipy's default `padlen` is **18** at either rate, and the automatic margin is **500 samples at either rate under truncation, flooring and rounding alike** (500.000000 nominal against 500.000664 derived). The margin, the 14,020-sample block and the retained 13,020 samples are the same objects either way; the deviation is confined to the second-order-section coefficients.

**One disagreement between our two measurements is itself the argument.** Codex's retained-sample difference is `3.56153236218e-05 µV`; mine is `5.80e-06 µV`. Different fixtures. That is precisely why §19.3 labels both as single-fixture diagnostics and refuses to promote either into a bound — the promotion that produced F4-R1 one card ago.

**I flagged this repair as the first thing to attack in Round 2.** If the argument that the recording rate is not a pinned input is wrong, the identity claim is doing less work than §19.3 says, and everything F4-R1 repaired stands on it.

### F3-R1 — a direction that reverses is not a direction

Draft 32 settled the split-half construction as **contiguous halves** and justified it by asserting that interleaving correlates the two half-estimates and **compresses** the spread in the permissive direction. Codex produced a 72-channel periodic construction on which interleaving gives `R_null = 4` against contiguous's `1`.

I reproduced the refutation on a construction that shares nothing with his: seventy-two channels whose scale alternates by **sample parity** — eight at a 2:1 even/odd ratio, fifty-six at 1:1, eight at 1:2. Contiguous halves each hold equal numbers of both parities, so every channel's ratio is exactly 1 and `R_null_sampled` is **exactly 1**; even/odd interleaving separates the parities and it is **exactly 4**. Interleaving expands, and carries the statistic from inside the strict tolerance to outside it.

**The direction claim is withdrawn. The split is not.** §19.5 keeps contiguous halves on three grounds, **none of which is a direction**:

1. The two halves meet at a single boundary, so for a signal band-limited above 300 Hz their estimates are close to independent — which is what a disagreement measurement needs, and which interleaved subsets of the same 434 ms are not.
2. An interleaved split carries a free parameter — the period — whose effect on the decision statistic has no known direction. Pinning a parameter whose effect cannot be signed is how a gate ends up tuned rather than declared.
3. **Decisively: the goal that motivated interleaving is not one the decision rule can cash.** Interleaving was proposed to reduce the cancellation that makes a low `R_null_sampled` uninformative — but under the one-sided reading settled at RC-007, a low value certifies nothing **by declaration**. There is nowhere for the improvement to be spent.

The split rule is now declared a pinned parameter of the instrument, like the chunk boundaries, with **no bound claimed between two split rules**.

### F4-R1 — I authenticated the document and not the instrument reading it

`probe_rc008_spec.py` used the closed card's checker as a regression baseline by running it as a subprocess and reading its printed lines. Codex staged a candidate with the parameter table's `K` changed from 60 to 61 **and** a counterfeit process that printed the six expected failures, and the wrapper still reported 57/57 and exited zero.

**The finding is correct and the design defect is mine.** The repair is on the instrument:

- `probe_rc008_spec.py` now hashes `probe_rc007_spec.py` **and the four carried record files** against pinned digests **before** running anything.
- It requires the subprocess's expected **nonzero** exit rather than ignoring the exit code, and asserts its stderr is clean.
- `mutate_rc008_spec.py` gains three **instrument** mutations that no document mutation can reach: substituting a counterfeit checker that prints the expected list and exits zero, appending one undeclared line to the legacy checker, and tampering with one carried record. All three are caught.

**The generalisation is in §19.14:** a checker that consumes another process's output is only as authenticated as that process, and "I ran the old checker" is a claim about a filename until a digest makes it a claim about a file.

### F5-R1 — a percentile ratio is not monotone in one channel's value

§19.3 has said since Draft 29 that an unmasked bad channel inflates `R_space_sampled` whichever kind it is, so the spatial check is conservative in their presence; §19.10 carried the same claim. **The two premises are true and the conclusion does not follow.** Reproduced independently: a 72-channel band of eight contacts at 1, fifty-six at 2 and eight at 3 gives `p90/p10 = 3` and fails the strict `M = 2`; replacing **one** quiet contact by an extreme 100 moves the tenth percentile's rank off a 1 and onto a 2, leaves the ninetieth at 3, and the ratio **falls to 1.5 and the candidate passes**.

**The claim is withdrawn on both surfaces.** The direction is declared **unknown**, because the comparison is against a counterfactual value for the same contact that this gate never observes.

**No bad-channel handling rule is added, and that is deliberate.** Acquiring a detector to run a screen is what §19.3 refuses; a threshold on outlier count or size would be a parameter invented **after** the failure mode was known, which is the failure §15 and §16.1 exist to prevent. What replaces the claim is a record: §19.7 now publishes the per-channel `σ̂_c` **for every window** rather than for one, so a displaced percentile rank is visible in the JSON rather than argued about in prose.

## 3. The four tracked items, one of which found a wrong number of mine

- **T1-R1 — coverage and dilution are different defects.** §19.9 attributed both to "dilution". It now names three refused arrangements and two distinct failures: keeping three cores of a five-chunk read as three windows costs **coverage** (largest gap 170 → **524**, guarantee 73.780 s → **227.416 s**); aggregating them adds **dilution** on top (a 3× one-chunk excursion reads 3.02 alone and **1.33** inside three chunks, 44% of it). **And Draft 32's figure for the third arrangement was wrong: "about 223 s" is actually 527 chunks and 228.718 s**, carried over from an earlier grid. Every number is computed rather than estimated.
- **T2-R1 — the stale current-state sentence.** §19.10 still said "This Draft 31 state is not approved by anyone yet". Replaced with the current state, including that RC-008 is the clause-5 successor.
- **T3-R1 — terminology.** "one stored bit" → "one stored code step"; "least-significant bits" → "code steps"; "half-bit" → "half a code step". 2.34375 µV is a quantization increment, not a bit depth.
- **T4-R1 — the phase-omission direction.** Narrowed to the shared-component model and to the **level** statistic alone. The same fixture shows where it stops: all 72 channels rise, and the *spatial* statistic moves the other way (1.0418 → 1.0406). **No direction is claimed for `R_space_sampled`.**

## 4. Evidence

| Instrument | Result |
|---|---|
| `probe_rc008_spec.py` (extended in place) | **168 checks, 0 failed** |
| `mutate_rc008_spec.py` (extended in place) | **27 of 27 caught**, control green — three of them instrument mutations |
| `probe_rc007_spec.py` (closed card's, unedited) | **288 checks, exactly 16 failed**; the list is pinned in both directions |
| `probe_rc008_round2.py` (new, this session's evidence) | **36 checks, 0 failed** |
| Frozen spans §1–§16 / §17 / §18 | **byte-identical**: 144,664 / 21,864 / 20,579 |

Every number Draft 33 publishes is computed in `probe_rc008_round2.py`, which reads no archive and touches no candidate.

**The sixteen expected reds are named against the finding that required each.** Six are Draft 32's; ten are Draft 33's — six sentences RC-008 required to change, and four census counts. **One of the four is a false positive worth recording:** the legacy census is a *substring* census, and Draft 33 quotes the other probe's declared rate `29,999.999999999996 Hz`, which contains `9,999`. No restatement of the chunk count changed. The new census counts that occurrence explicitly rather than waving at it.

## 5. Challenges, and how they were handled

**A mutation that had been passing for the wrong reason.** After extending the mutation harness, the control run was red — the staged tree was missing the new Round-2 record. Once that was fixed, a mutation that had reported `caught=True red=1` turned out to have been catching **the control's own failure** rather than anything it broke: its anchor lived in §19.14, and no check read §19.14 for that sentence. I added the check and it is caught properly now. This is the third session in which "a mutation can pass for the wrong reason exactly the way a test can" has fired, and the first in which a *green control* was the thing hiding it.

**A check of mine that could not fail.** My first version of the Round-2 evidence probe contained `not bool(...) or True` — a check with no failing branch. I found it reading my own output, replaced it with two checks that can fail, and both pass. That is the failure mode I keep a numbered lesson about, written into my own instrument in the same session.

**Deciding which of two permitted repairs to take, twice.** F2-R1 and F5-R1 both offered "fix it" or "declare it". For F2-R1 I took the declaration, on the evidence that the alternative's input is not pinned. For F5-R1 I took the withdrawal and refused to add a rule, on the ground that any rule would be a parameter chosen with the failure visible. **In both cases the weaker-looking answer is the honest one, and in both cases the artifact now says why rather than leaving the choice to be inferred.**

## 6. Insights worth carrying

1. **A declared bound is not enforced until the branch *and* the statistic it reads can enforce it.** RC-007's F1 gave the floor a branch; RC-008's F1-R1 found the branch could not fire. Two rounds, one bound, two different halves of the same failure.
2. **When a repair fixes a defect, go and check the other places the same arithmetic appears.** F1-R1 was reported against §19.6; §19.8 had the identical defect and was not named.
3. **A direction that reverses between two models of the thing it is a direction about is not a direction.** The right response is to withdraw it and find grounds that do not need one — not to narrow it.
4. **A checker that consumes another process's output is only as authenticated as that process.** A digest is what turns "I ran the old checker" from a claim about a filename into a claim about a file.
5. **A green control is not a clean control.** A red control inflates every case's failure count and can make a mutation look caught. Fix the control first, then re-read every "caught" line.
6. **Prefer the answer that does not need a number.** F5-R1's repair is a published record instead of a threshold; F2-R1's is a declaration instead of an unpinned input. Both are smaller than the alternative and neither invents a parameter after the answer was visible.

## 7. Files created or updated

**Created**

- `agents/Claude/tools/probe_rc008_round2.py` — the Round-2 evidence probe (36 checks)
- `agents/Claude/tools/rc008_round2_2026-08-18.txt` / `.json`
- `agents/Claude/tools/rc008_spec_2026-08-18_draft33.txt` / `.json`
- `agents/Claude/tools/mutate_rc008_spec_2026-08-18_draft33.txt`
- `agents/Claude/Session Summaries/HumanReport47.md`

**Updated**

- `agents/Claude/Tier A Host and Injection Zone Selection.md` — **Draft 33**, `16ee8f80…`, 325,190 bytes; §19.14 added; §19.13 marked superseded in one claim; Draft 33's status line pushed onto the stack
- `agents/Claude/tools/probe_rc008_spec.py` — extended in place (57 → 168 checks, plus the F4-R1 authentication)
- `agents/Claude/tools/mutate_rc008_spec.py` — extended in place (12 → 27 mutations, three of them instrument mutations)
- `Review Cards/RC-008 Host Noise Gate, Convergence Repair.md` — Round-2 candidate and response
- `Review Cards/README.md` — index row
- `chats/Claude-Codex/Section 19 Convergence Repair/Section 19 Convergence Repair - Active.md` — appended
- `README.md` — one running-log entry (88 dated entries)
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`

**Not touched:** the Claim Sheet, the Accessible Claim Sheet, the Study Guide, every file in `Reproducibility Packet/`, §1–§18 of the selection document, and every closed review card.

## 8. Machine state

RAM available **13,296 MiB of 32,425 MiB** at 08:05 PDT. Nothing heavy ran: no archive read, no network request, no GPU work. The heaviest step was the mutation harness at roughly forty seconds. Temporary trees are deleted by the harness itself.

## 9. Next steps

1. **Codex owes RC-008's Round-2 delta pass.** Under clause 1 of the convergence rule, **any new blocker after Round 2 freezes the candidate and triggers a Convergence Decision** — and under clause 5, a non-approval on this card forbids a third like-for-like successor.
2. **The estimator is still not written and must not be**, until §19 reaches explicit same-state approval. When it is, it is a packet utility plus a synthetic harness, in the shape `band_drift.py` took after §16 closed.
3. **Rank 2 (NYU-12 Probe01) can be measured for drift** at any time; the command is unchanged and the gate is discharged for rank 1 only.
4. **No count-based progress report was due.** The next falls at Session 48.
