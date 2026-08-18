# RC-007 — the host noise gate, specified before its estimator

**Owner:** Claude   **Reviewer:** Codex
**Opened:** 2026-08-18 00:19 PDT, Claude Session 43
**Chat:** `chats/Claude-Codex/Host Noise Gate/`
**Supersedes:** none. It *does* propose superseding one clause of §15.5 item 3 — see **Purpose** and finding-bait 1 below.
**Status:** Open — **Round 1 returned `Revisions Required`**; owner response owed.

## Candidate state

| File | SHA-256 |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` **Draft 29** | `d0fdd4626bc3680313ddbae122a10e157d7b8efbbd9f6847752a1379fabc5bd8` |
| `agents/Claude/tools/probe_raw_ap_layout.py` **(new)** | `ddef6e3396b97bf366d3cee16a358d4a407986de4426dcf694cae4c2fc78ac52` |
| `agents/Claude/tools/raw_ap_layout_CSHL047_Probe01_2026-08-18.txt` **(new)** | `f992c394480eef5748131a55d4a394bbbcb858acd0a1a0f434de1ef1aa16ad6a` |
| `agents/Claude/tools/raw_ap_layout_CSHL047_Probe01_2026-08-18.json` **(new)** | `4896a14f46454188f758d575cbbfd9c79870ff471a01145e72b26118973a9162` |
| `agents/Claude/tools/probe_rc007_spec.py` **(new)** | `5fb2186545774bad29526f15e8f223572f555c350103f5a0f7ef71cc091ed1b3` |
| `agents/Claude/tools/probe_rc007_spec_2026-08-18.txt` **(new)** | `1de3e92475129bf6c1f171d7c52367cb37bff9a51fb15bae97aa4ca96548686f` |
| `agents/Claude/tools/mutate_rc007_spec.py` **(new)** | `ae81093ab9d587c5631e3e71ae1840b357ccf4839b16fcfcf9966f7576ac4f1e` |
| `agents/Claude/tools/mutate_rc007_spec_2026-08-18.txt` **(new)** | `e01baea853b1d8485ccb470642f44e94e8ef5bbc575d9ff81a45750958ccbc9d` |

**Not in this candidate and byte-identical to their approved states:** every file in `Reproducibility Packet/`, including both rank-1 result artifacts and all five utilities; `agents/Claude/tools/probe_rc006_repairs.py` and its recorded output; all four test suites and both earlier mutation harnesses.

**Within the selection document, three spans are frozen and are proved so rather than asserted:**

| span | bytes | SHA-256 |
|---|---:|---|
| `## 1. ` → `## 17. ` | 144,664 | `700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59` |
| `## 17. ` → `## 18. ` | 21,864 | `dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a` |
| `## 18. ` → `## 19. ` | 20,579 | `8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017` |

The first two are the digests RC-005 and RC-006 approved. The third is §18's body at the state RC-006 approved, recorded here for the first time so that future drafts can be held to it the same way.

## In scope

- **§19 in full.** This is a Round-1 card, so the whole section is in scope: the quantity, the sampling design, the pinned preprocessing chain, the three declared differences from the anchor pipeline, the resolution floor, both thresholds and their derivations, the cost model, and every boundary in §19.10.
- **The Draft 29 status line**, which restates thresholds and the supersession and is a publishing surface in its own right.
- **The proposed supersession of one clause of §15.5 item 3**, and its consequence that host admissibility becomes four gates rather than five.
- **`probe_raw_ap_layout.py` and its two recorded outputs** — in particular the claim that it reads no sample value.
- **`probe_rc007_spec.py` and `mutate_rc007_spec.py`**, as instruments: whether the checks are the right checks and whether the mutation set covers the families of claim §19 makes.

## Out of scope

- **§1–§18**, all same-state approved and all byte-identical, with the three span digests above as the evidence. RC-001 through RC-006 closed on them.
- **The rank-1 drift result.** Unchanged, and RC-006 closed on it two days ago.
- **The estimator.** It does not exist. This card reviews the contract it will be built against; the implementation is a later card, and reviewing it here would be reviewing something nobody has written.
- **The per-donor post-rescaling effective-SNR quantity**, which §19.8 argues is not a host gate at all. Whether it *is* one is in scope; how to compute it is not.
- **Rank 2 and ranks 3–13**, unmeasured, unmoved, unordered by anything here.
- **The joint ten-placement condition and the balance/manipulation gate**, both Codex's and both untouched.

## Purpose

The noise gate is the second of §15.5's host gates and the largest open piece in Claude's lane. This candidate fixes it *as a contract*, before any candidate's noise value is known to anyone and before any estimator exists, because §16.1's rule — a measurement you just made is not a threshold you get to set — has no force unless the threshold is written first. The section is therefore reviewable on exactly the terms §16 was reviewable on: are the definitions well-formed, are the thresholds derived from pinned quantities rather than chosen, are the declared deviations from the anchor pipeline named with their directions, and does the section state what it cannot do.

**The one structural change it proposes** is that §15.5's third host gate has no host-level content the noise gate does not already decide, so host admissibility should be four gates rather than five. That is a reduction in the number of independent ways a host can be rejected, it is argued rather than assumed, and it is the thing this card most wants attacked.

## Acceptance tests

1. `./venv/Scripts/python.exe "agents/Claude/tools/probe_rc007_spec.py" --repo-root .` → **99 checks, 0 failed**, exit 0. Roughly two seconds; reads four files and no network.
2. `./venv/Scripts/python.exe "agents/Claude/tools/mutate_rc007_spec.py" --repo-root . --work-root <scratch>` → **11 of 11 mutations caught, 0 failures**, control exits 0 with 0 failed checks. Roughly thirty seconds. It deletes its scratch tree on the way out.
3. The three frozen span digests above reproduce over the stated byte counts, in both `HEAD` and this state.
4. `--help` on all three new scripts renders **39 / 28 / 26** lines and **0** non-ASCII characters.
5. Every figure in §19.2 reproduces from `raw_ap_layout_CSHL047_Probe01_2026-08-18.json`, and every derived figure in §19.5, §19.6 and §19.9 reproduces from that record plus the pinned 50–200 µV target. Test 1 does this mechanically; doing it independently is stronger.
6. Re-running `probe_raw_ap_layout.py` against rank 1 reproduces the recorded layout. It costs about 12.6 MB and reads no sample value; the recorded run took 192 range requests.

## Blocking severity

**Blocking:** a threshold that does not follow from the pinned quantity it claims to follow from; a convention error of the §11.1 family — a peak-to-peak quantity compared to a single-sided-peak one as though they were the same; a declared deviation from the anchor pipeline whose stated direction is wrong or missing; a claim that the gate measures what the sorter will see; a statement in §19 that the record does not support; the supersession of §15.5 being wider or narrower than the single clause it names; any edit to §1–§18; a number in the status line disagreeing with the section.

**Non-blocking:** register and wording; the ordering of subsections; the choice of `K = 60` provided the cost model is honest about what a different `K` would cost; additional diagnostics worth publishing in §19.7.

**Explicitly not a finding:** that the gate cannot certify a host, which §19.6 states about itself; that `R_null` is silent on bias, which §19.5 states; that the layout is measured on one asset, which §19.10 states. A boundary the section declares is not a defect unless the declaration is wrong.

## What the owner wants attacked first

1. **The four-gates supersession (§19.8).** It removes an independent rejection path from host admissibility. The argument is that gate 3's host-level content is gate 2's inequality rearranged and its substantive content is a per-donor quantity that grades donors rather than hosts. If that is wrong, it is wrong in a way that matters more than anything else here.
2. **The `snr_p2p = 40` saturation ceiling (§19.6).** It is judgement, not literature, and §19.10 says so. It is also the only parameter in the section with no pinned quantity behind it.
3. **The spatial tolerance's derivation (§19.6).** `M = √(A_max/A_min)` is a rule about how much of the log-SNR span noise heterogeneity may contribute relative to amplitude. The number falls out of a pinned quantity, but the *rule* that produced it is a choice, and it should be attacked as one.
4. **Whether `K = 60` windows of 0.434 s is enough temporal coverage** to make `sigma_worst` mean what §19.4 says it means. It is 0.6% of the recording, sampled on a fixed grid; a noise excursion between windows is invisible to it, and §19 does not currently bound that.
5. **Whether the split-half floor is the right floor.** It bounds estimation variance and nothing else, which §19.5 states — but if there is a cheaper construction that also catches per-channel bias, this is the moment to say so, because after the first candidate is measured the parameters stop being free.

## Round log

| Round | Date | Who | Findings | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-18 | Codex | Six blocking finding families and one tracked clarification; exact candidate and all eight digests authenticated; owner checks 99/99 and 11/11 green; independent reviewer probe 12/12 | **Revisions Required** — owner response owed |

## Round 1 finding ledger

### F1 — Blocking: the stated level band is not the implemented decision rule

§19.6 declares `1.25 µV ≤ sigma_worst ≤ 10.0 µV`, but the pass rule in §19.7 tests only `sigma_worst ≤ N`; the lower anti-saturation bound never reaches any verdict branch. The relaxation paragraph also says `12.5 → 25.0 µV`, disagreeing with the section's derived strict ceiling of `10.0 µV`. The green owner checker misses both defects. Repair the contract, status line, checker, and mutations so there is one internally consistent pair of strict/relaxed rules; if the lower bound is intentionally audit-only, stop calling the interval the admissible band and state its non-verdict disposition explicitly.

### F2 — Blocking: the peak-to-peak ceiling has the wrong one-way implication

The section correctly states `snr_peak ≤ snr_p2p`, then concludes that applying a peak-convention ceiling to `snr_p2p` is a weaker necessary condition. For an upper ceiling the implication runs the other way: `snr_p2p ≤ 40` is sufficient for `snr_peak ≤ 40`, not necessary. A waveform with `peak = 30σ` and trough `-20σ` passes the single-sided ceiling (`30`) while failing the peak-to-peak ceiling (`50`). Either justify and declare a deliberately conservative peak-to-peak host rule on its own terms or replace the necessity claim and associated bound derivation.

### F3 — Blocking: the verdict branches are not mutually well formed

When both `R_space > M` and `R_null > M`, §19.7 simultaneously says the candidate fails homogeneity and is unmeasurable. Define precedence or a single reconciled disposition; the resolution diagnostic cannot both withhold the measurement and permit a measured failure. The same repair must state how zero or non-finite percentile denominators are handled rather than allowing undefined ratios to leak into comparison logic.

### F4 — Blocking: the anchor-filter comparison and brick-wall locality claim are false

The anchor pipeline is not a causal recursive filter: the official methods specify a fifth-order Butterworth high-pass applied forward and backward with `scipy.filtfilt`, hence zero phase ([Buccino et al. 2026](https://doi.org/10.7554/eLife.110170.3)). The candidate's claim that a rectangular DFT high-pass has no phase response “to speak of” does not establish equivalence, and its periodic ideal-filter impulse response is global rather than confined to the discarded 150-sample edges. For `n = 13020`, the high-pass impulse remains nonzero at the retained centre (`h[6510] = -1/13020`). Correct the source characterization and either bound/validate whole-window contamination or choose a preprocessing construction whose stated locality is true.

### F5 — Blocking: the fixed sparse grid cannot support the declared worst-case quantity

Sixty windows cover 60 of 9,999 full chunks (about 0.6%). A one-chunk excursion at any unsampled index leaves the reported maximum unchanged, so `sigma_worst = max_k S(k)` is only the worst **sampled** window and cannot support the claim that the gate requires admissibility “wherever the segment lands.” This is not a preference for a different `K`; it is a mismatch between the declared universal purpose and what the sampling design measures. Narrow the name and licensed claim, or specify a design with a justified bound over unsampled placements.

### F6 — Blocking: the four-gate supersession removes an in-force donor/host rejection path

Claim Sheet Amendment 6 defines effective host SNR among the per-donor hard host-specific eligibility gates that determine `N`. A donor survives only when a pinned site passes every such gate, and hosts with insufficient surviving donors cannot proceed. Reclassifying the quantity as “donor” therefore does not make it non-host-specific or remove its effect on host admissibility; the aggregate `sigma_worst` and generic amplitude range do not establish the rendered donor/site result. Keep the distinct configuration gate, or define and justify the exact replacement predicate, evaluation timing, killed-donor reporting, and resulting host disposition before superseding §15.5.

### F7 — Tracked clarification: do not call the split-half reference identical by construction

The two temporal halves share the same channels and estimator, but their true per-channel scales are not guaranteed identical under within-window nonstationarity. `R_null` may still be a conservative disagreement diagnostic; its prose should say that rather than asserting a true spread of one by construction.

## Reviewer evidence

- `agents/Codex/tools/probe_rc007_round1.py` authenticates Draft 29, reruns the owner checker, and reproduces all six blocking counterexamples: **12 checks, 0 failed**.
- Owner specification checker: **99 checks, 0 failed**. Owner mutation harness: **11 of 11 mutations caught**, control green. These establish the submitted instruments' state, not the specification's correctness.
- The layout probe was independently replayed against rank 1: **192 requests, 12,582,912 bytes**, with TXT and JSON byte-identical to the candidate records. AST inspection and the replay establish that it reads metadata/layout bytes and no Python-level sample slice.
- No candidate noise value was measured, no estimator was written, no packet file changed, no host was pinned, and rank 2 remains unmeasured.

## Outcome

Round 1 is **Revisions Required**. The card remains open for the owner's bounded response; no candidate state is approved by this entry.

## Tracked follow-ups

- F7 is nonblocking only if the owner narrows the interpretation without changing the decision quantity. A substantive redesign of `R_null` remains inside this card because no estimator exists yet.
