# Claude Human Report — Session 43

**Date and time:** 2026-08-18 00:35 PDT

**Phase:** Phase 2 — Execution. Specification work on the second host gate.

**Outcome:** **§19 of the Tier A selection document is written: the host noise gate, fixed as a contract before any candidate's noise value is known and before any estimator exists.** RC-007 is open at Round 1 on Codex. Nothing was measured except one property of the raw file's storage layout, no estimator was written, no host is pinned, and rank 2 remains unmeasured.

---

## 1. What this session was for

RC-006 closed `Approved` at Round 2 late on 2026-08-17, which discharged rank 1's strict drift gate and — as importantly for this session — freed the selection document. The largest open piece in my lane was the pair of gates §15.5 calls *noise* and *post-rescaling effective SNR*, neither of which had a specification of any kind. Session 42's continuity file said explicitly not to start writing them while RC-006 was open, because adding a section mid-card changes what the reviewer is reviewing. RC-006 closed, so this session started them.

**The sequence matters and it is the sequence §16 used: specify, review, then implement.** The sessions in this project that went the other way — code first, then the sentence describing it — are the ones that produced claims Codex made me withdraw. So no estimator code was written this session. What exists is the contract the estimator will be built and reviewed against.

## 2. What §19 fixes

The gate is **three numbers**, on the pattern §16.7 already established: a gated quantity, a second gated quantity, and a resolution floor that can make a candidate *unmeasurable* rather than passed or failed.

- **`sigma_worst`** — the loudest window's band-median robust scale estimate, in µV. Worst window rather than session median, for the reason §16.4 already settled for drift: the ten-minute injection segment has not been chosen, and a gate evaluated on a favourable stretch would let the segment be chosen after the trace is visible.
- **`R_space`** — the worst window's p90/p10 spread of that estimate across the injection band's channels. This is the project-specific half and it is a real confound rather than a tidiness check. Tier A's two arms place their donors differently by construction, so a noise gradient across the band turns a placement difference into an **effective-SNR difference between arms** — which lands directly in the sorter × realism interaction the project measures, and which no amount of donor-metadata balancing can remove, because it originates in the host.
- **`R_null`** — the same percentile ratio computed between two disjoint halves of each window, where the true per-channel scale is identical by construction, so every difference between the halves is estimation noise. If `R_null` exceeds the tolerance, the candidate is unmeasurable. It does **not** correct or deflate `R_space`, for the same reason §16.5 refuses to correct the drift statistic by its own null.

**Both thresholds are derived from pinned quantities rather than chosen.** The level tolerance is `A_min/5 = 10.0 µV` strict and `A_max/8 = 25.0 µV` relaxed, from the pinned 50–200 µV peak-to-peak injection target. The spatial tolerance is `√(A_max/A_min) = 2.0` strict and `4.0` relaxed, on the rule that noise heterogeneity may contribute at most half the log-SNR span the amplitude target already contributes on purpose. Both relaxations are taken in the **single** relaxed pass §16.7 already declares, not in a second ladder of their own.

## 3. The correction I made to my own draft before handing it over

The first draft of §19 derived its strict level tolerance from "the classic four-sigma detection scale" — `A_min/4 = 12.5 µV`. That multiplier is standard and I believe it is correct, but **I could not verify it from a primary source this session**: the publisher returned 403 on the paper that introduced it, and the review article I could reach confirmed the robust-noise-estimate part without the threshold multiplier. This project's own references rule is that nothing enters from memory.

So I replaced it rather than keeping it with a caveat. **Both rungs of the level ladder now use SpikeForest's own two stated numbers — 5 and 8 — applied to the two ends of the pinned amplitude range**, which I did read directly from the article. No multiplier in the derivation is now this project's. The strict tolerance moves from 12.5 µV to 10.0 µV, which is a tightening, and a tightening is affordable exactly once — before the first measurement, which is where we are.

That change touched five files and was applied by a single script that validated every replacement across every file before writing any of them, then re-asserted afterwards.

## 4. The one thing that was measured, and what it decided

`agents/Claude/tools/probe_raw_ap_layout.py` reads one raw AP `ElectricalSeries` object header and its scaling attributes and **never slices the sample array**, so running it discloses no noise value, no amplitude and no gate quantity. On rank 1's raw asset it cost 192 range requests and 12.6 MB.

| property | value |
|---|---|
| shape | 130,188,000 × 384 |
| dtype | `int16` |
| chunk | **13,020 samples × 384 channels** |
| filters | gzip level 4 |
| logical / stored | 99,984,384,000 / 53,163,508,785 bytes |
| `conversion` | 2.34375e-06 V, `offset` 0.0, unit volts, no `channel_conversion` |

**Three things follow, and each decided something rather than merely being interesting.**

**The chunk spans every channel**, so reading the 72-channel band costs exactly what reading all 384 costs. The common median reference is therefore computed over the whole probe at no transfer cost — which happens to be what the anchor pipeline does anyway. Had the chunk been channel-split, that choice would have carried a price and would have needed arguing rather than noting.

**Time is addressable only at 0.434 s**, so the sampling window is one chunk rather than a duration someone preferred.

**One stored bit is 2.34375 µV** — two to three bits of the probe's own published 5.1–5.7 µV RMS AP-band noise. A median-absolute-deviation estimate computed on the *stored integers* would therefore be granular to about **1.74 µV** on a quantity whose entire plausible range is roughly 5 to 15 µV. That is not a hypothetical objection, and it is why §19.3's chain is not optional: the estimate is taken after a filter and a reference computed in floating point, on a signal that no longer lives on the integer lattice. **I would not have found this argument without reading the layout**, and it is the clearest case this project has produced of a measurement changing a design rather than confirming one.

## 5. The structural finding — §15.5's third gate

Working out what §15.5's third host gate would actually compute produced a result I did not expect and which is the thing I most want attacked.

**At host level there is nothing left in it that the noise gate does not already decide.** The host-level quantity is the injected amplitude over `sigma_worst`, and the two conditions a host gate could impose on it are the two inequalities §19.6 already rearranged into bounds on `sigma_worst`. Evaluating them again under another name is bookkeeping, not evidence. The substantive part — post-rescaling effective SNR **per donor** — needs a rendered donor, needs the generator, grades donors rather than hosts, and belongs to Rung 0 and the matching rule.

**I looked for a third possibility and refused it, and the refusal is the more interesting half.** A genuinely host-specific check would ask whether the injected amplitude range sits inside the host band's *native* amplitude distribution — a host whose own units were all far quieter would make hybrid units separable for reasons unrelated to sorting. It is computable today with no new reads, because the placement results have carried every candidate's band median amplitude with p10 and p90 since **Session 7**. That is exactly why it cannot become a gate: any threshold written now would be written with all thirteen answers visible. I checked anyway, and the natural rule is satisfied by every candidate including the weakest, so it would also have been a check that cannot fail. **The moment to pin it passed in Session 7 and is not recoverable.** It is carried as a reported diagnostic that no verdict reads.

**Consequence:** §19 proposes superseding exactly one clause of §15.5 item 3, which would make **host admissibility four gates rather than five**. That reduces the number of independent ways a host can be rejected, so it is the first thing in the handoff and the first thing on the review card's attack list. It binds only if Codex approves it.

## 6. Evidence, and the two gaps the mutation harness found in my own checker

Codex settled the instrument question at RC-006: the owner's claim checker guards the exact claims and is not sole evidence. I took that reading, and then went one step further, because at RC-006 I told him a claim checker over prose cannot go red on a real defect — which is a statement about a checker nobody has tried to break.

`agents/Claude/tools/mutate_rc007_spec.py` breaks a clean copy eleven different ways across five families of claim, requires a control to pass, and — after its first run — asserts that the child process **reported failed checks** rather than merely exiting non-zero. That second assertion matters here specifically: the strings under test carry `µ` and `√`, this console is cp1252, and an encoding crash would have looked exactly like a caught mutation.

**Its first pass caught 6 of 9, and both misses were gaps in my instrument rather than in the artifact.**

1. A threshold mutation in the **status line** survived, because the checker was not reading the status line at all — and the status line publishes the same thresholds the section does. It is a publishing surface, and evidence has to come from the exact state you publish.
2. A layout figure mutated in the table survived, because the same number appears elsewhere in the section and a substring search still passed. The checker now validates **whole table rows**. That is §18.2's defect shape — a restatement disagreeing with its siblings — generalised into a check.

Final state: the checker is at **99 checks, 0 failed**; the harness at **11 of 11 caught, 0 failures**, control green. `--help` on the three new scripts renders 39 / 28 / 26 lines with **0** non-ASCII characters. The three frozen document spans reproduce exactly: §1–§16 at `700b3b9a…` over 144,664 bytes, §17 at `dc73b87f…` over 21,864, and §18's body at `8af3e62c…` over 20,579 — the last recorded for the first time, so later drafts can be held to it the way the first two are.

## 7. Challenges and reasoning paths

**The hardest question was not the statistic; it was what a host gate is entitled to claim.** The faithful version of a noise gate measures what the sorter sees, which needs the pinned sorting preprocessing, which needs SpikeInterface, which is Rung 0 and does not exist. The honest resolution was to pin a chain that *mirrors* the anchor pipeline's — 300 Hz high-pass, global common median reference — declare the two steps it omits with the direction each omission pushes the answer, and state plainly in the section that the resulting estimate is **not** the σ the pipeline will compute.

**The second hard question was the convention trap.** Both literature anchors state SNR as a single-sided peak over the noise estimate; this project's amplitude target is peak-to-peak. §11 taught this project what happens when two numbers in the same unit are treated as one quantity. I refused to convert: the extremum is at most the peak-to-peak span with no fixed ratio, so applying a peak-convention threshold to a peak-to-peak quantity is the **weaker** requirement, and every bound in §19.6 is therefore stated as a necessary and not a sufficient condition. A host screen can reject a host the injection cannot work on; it cannot certify one it will work on.

**A path I considered and dropped:** building a permutation null for the noise statistic, by analogy with the drift gate. It does not transfer — there is no time-ordering to destroy that leaves the scale estimate meaningful. The split-half construction does the same job with no distributional assumption, and it needs no seed. Its limit is stated rather than discovered later: it bounds estimation *variance* and is silent on estimation *bias*, because a per-channel gain error is identical in both halves.

## 8. Files created or updated

**Created**

- `agents/Claude/tools/probe_raw_ap_layout.py` and its two recorded outputs, `raw_ap_layout_CSHL047_Probe01_2026-08-18.{txt,json}`
- `agents/Claude/tools/probe_rc007_spec.py` and `probe_rc007_spec_2026-08-18.txt`
- `agents/Claude/tools/mutate_rc007_spec.py` and `mutate_rc007_spec_2026-08-18.txt`
- `Review Cards/RC-007 Host Noise Gate Specification.md`
- `chats/Claude-Codex/Host Noise Gate/Host Noise Gate - Active.md`
- `agents/Claude/Session Summaries/HumanReport43.md`

**Updated**

- `agents/Claude/Tier A Host and Injection Zone Selection.md` — **Draft 29**, adding §19 and the Draft 29 status line. §1–§18 unedited and proved so.
- `agents/Claude/references.md` — five new entries
- `Review Cards/README.md` — RC-007 index row
- `README.md` — one running-log entry, banner to 2026-08-18
- `agents/Claude/README.md` — tools tree and counts
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten

**No file inside `Reproducibility Packet/` changed.** No archive sample was read. No dependency was installed.

## 9. Machine state

Measured at 00:09 PDT: **17,561 MiB of 32,425 free; GPU 876 of 16,311 MiB used.** The only network work was the layout probe at 12.6 MB, and the only compute was three short read-only scripts. Nothing heavy ran, so nothing needed a second reading against a requirement. Temporary directories: `0` at close.

## 10. Next steps

**Immediate: Codex's RC-007 Round 1.** The five things I asked him to attack, in order, are the four-gates supersession, the declared `snr_p2p = 40` saturation ceiling (judgement, not literature, and labelled as such), the rule behind the spatial tolerance, whether 60 windows of 0.434 s is enough temporal coverage, and whether the split-half floor is the right floor.

**Then, in my lane:** implement the estimator against whatever §19 says after review, as a packet utility with its own synthetic harness — the same shape `band_drift.py` took after §16 was approved. That is the next substantial build.

**Unchanged:** no host is pinned; rank 2 (NYU-12 Probe01) is unmeasured with its command unchanged; ranks 5, 7, 9 and 13 stay paused on the declared-clock disagreement; Codex retains the joint ten-placement condition and the balance/manipulation gate; and no donor assignment, generation, Rung 0 or sorter execution is authorized.

**No count-based progress report was due.** Mine fall at sessions 8, 16, 24, 32, 40 and next at **48**; no phase transition and no approved amendment closed in this session.
