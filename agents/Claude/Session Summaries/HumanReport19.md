# Human Report 19 — Claude

**Date and time:** 2026-08-13 10:26 PDT
**Phase:** 2 — Execution
**Session type:** Owner re-review of Codex's Draft 11 and the drift estimator; repository-wide clone-byte repair

---

## Summary

This session did the owner half of a review cycle. Codex had reviewed my Draft 10 of the Tier A host-selection document, repaired three things in it and in the drift estimator, approved its own revised state, and handed all of it back. The review cycle says that handoff is not a decision until the owner genuinely re-opens the artifact and either approves those exact bytes or edits and hands back. I re-opened it.

**Three outcomes.**

1. **Codex's three repairs are accepted in full and kept exactly as written.** I re-derived each rather than reading it — including reproducing the defect behind the largest repair on my own fixture with the pre-repair code restored. **I explicitly approved the estimator and its harness at Codex's exact digests, which closes the implementation loop on those two files.**
2. **I could not approve Draft 11's §16 unchanged, and Draft 12 is handed back.** Two additions, both found in the re-review. The larger one: the bin grid that the whole drift measurement rests on consumes two inputs — its anchor and its length — that no draft had ever pinned, and the number the project was about to use for the length is a *span* on a different asset than the one the spike times come from. On the recording sitting at rank 1 of the pinned candidate order, that span starts at 1.138 s rather than zero.
3. **The Windows clone defect is now repaired repository-wide, not only inside the reproducibility packet.** Codex's packet result reproduced exactly (0 of 42 files differ), but the same measurement showed 81 of 151 tracked files still did not survive a clone — including the Claim Sheet, the document under review, and the harness that validates the packet's drift module. The cost that had justified keeping the fix narrow was measured and turns out to apply to 17 files, all of which can be handled at no cost. **A clone of the finished session state reproduces 152 of 152 tracked files byte for byte.**

**No candidate has been measured, no host is pinned, no donor is selected, no generator or sorter has run, and no scientific result exists.**

---

## What was accomplished

### 1. Verification before reading

All four handed-back states were confirmed at their claimed SHA-256 values before I read a word of them: the Draft 11 document `647743668e…`, `band_drift.py` `d8b0359684…`, `test_band_drift.py` `82aaf77e99…`, and `.gitattributes` `e048236277…`. `Claim Sheet.md` and `Accessible Claim Sheet.md` were also confirmed unchanged at their recorded digests, so nothing in the contract had moved underneath the review.

### 2. Re-deriving Codex's three repairs instead of reading them

Session 18's own lesson was that running the resisting review even on edits you already agree with is what produces the extra findings. I applied it here and wrote the checks into a new probe, `agents/Claude/tools/probe_band_drift_claims.py`. All three pass.

**The partial-bin contamination defect reproduces on an independent fixture.** Codex reported that the pre-repair permutation drew from a unit's *full* depth array, so depths belonging to spikes in the discarded final partial bin could land in complete-bin positions and move the null even though they cannot touch the observed statistic. I restored the pre-repair permutation on a copy of the shipped module and built my own fixture: 8 units, 1,830 s (thirty complete 60 s bins plus a 30 s tail), with 940 tail depths shifted by 9,000 µm. The observed `Delta_10` is identical to four decimals in both arms (0.3199 µm). The pre-repair `Q95_null` moves — 0.5093 µm to 0.5107 µm. The shipped code returns 0.4840 µm in both. Milder than Codex's 0.0-to-6750.0 µm case, and the same defect.

**The repaired permutation pool is exactly the set it is specified to be.** The implementation permutes the contiguous slice `[offsets[0], offsets[-1])` of each unit's depth array. I checked that this equals `{i : 0 ≤ t_i < n_bins × 60}` on 200 randomized fixtures, with durations from 200 s to 4,000 s and spike times deliberately spilling below zero and past the end. It does, on all 200.

**The harness reproduces at 57 checks, 0 failed**, at the pinned 200 permutations.

Codex's third repair — six spike-time arrays and five depth arrays passing through `zip`, returning `n_units_in_band = 6` while computing a measurable verdict from five units — is the one I would least have found on my own, and it is worth naming as the reason the review cycle exists.

### 3. What prevented approving §16 unchanged

**Finding A — the bin grid was consuming two unpinned inputs, and one of them is wrong on the first candidate in the queue.**

`n_bins = floor(length / 60 s)`. So the grid's anchor and its length are inputs to the gating quantity as surely as the bin width is. §16.7 pins the bin width, the gate window, the inclusion and validity thresholds, the permutation count, the null summary, the master seed, the seed grammar, the 20 µm threshold and the 20→40 µm ladder. It never pinned these two, and §16.4 said only "from `t = 0`".

That is the fifth instance of the same shape in this project — a rule that is only pinned if what it consumes is pinned too — and this one is not hypothetical. `Reproducibility Packet/results/host_timing_index.jsonl` records `duration_s` as `t_last_s − t_first_s` measured on the **raw** AP stream. That is a span, not an end time, and `t_first_s` is not zero:

| series | `t_first_s` |
|---|---|
| `b52182e7` Probe01 — **rank 1 in the pinned order** | **1.138489 s** |
| `034e726f` Probe01 | 1.006007 s |
| `2d5f6d81` Probe01 | 1.304017 s |
| `4b7fbad4` Probe01 | 1.002167 s |
| the other seventeen measured series | within `6.4e-5` s of zero |

A grid anchored at absolute zero and handed a span as its length therefore stops `t_first_s` short of where the data actually ends, and mis-states the reported `discarded_s` by the same amount. Codex's own complete-bin repair widened the consequence: that boundary now decides which depths enter the *null* as well as which enter the observation.

**I have been deliberate about the size of this.** At 1.138 s against a 60-second bin, I expect the effect on `Delta_10` to be negligible, and Draft 12 says so in those words rather than inflating it. The defect is that a carefully pre-declared rule was eating an input nobody had fastened down, on the first candidate we will measure.

The half I could not settle is larger: **the spike times come from the processed asset and `duration_s` was measured on the raw one.** I checked whether this was already answerable from what has been downloaded — `results/amplitude_conventions.json` carries every column's own description, and `spike_times` reads only "the spike times for each unit in seconds", naming no origin. So it is not answerable without reading a candidate, and reading a candidate is exactly what is barred while the specification is open.

Draft 12 therefore does three things: §16.4 point 2 names the timebase the grid is anchored in; a new §16.4 paragraph pins the anchor and the length, records the measurement above, and states the rule that matters more than the arithmetic — **a candidate whose two timebases cannot be reconciled is an input error to resolve, not a drift rejection.** It is not recorded as a failed candidate and the pinned order does not advance past it. §16.8 adds it as a third mandatory pre-computation confirmation alongside Codex's two.

The reason that rule is worth writing down: §15 evaluates *first-admissible* in a fixed order. Under that standard a rejection recorded for the wrong reason hands the host to the next rank and is not recoverable by later work — the relaxation pass only re-runs the order if *nothing* clears at 20 µm.

**Finding B — withdrawing a proof left an exposure unnamed.**

Codex was right that one additive-ramp fixture cannot carry a general monotonic claim that real movement inflates `Q95_null`; my Draft 10 paragraph had promoted a demonstration into a proof, and the repair is correct. But Draft 11 then names only what a *larger* `Q95_null` does. The direction it does not name is the unsafe one: if the assumption fails the other way and `Q95_null` understates the true no-drift floor, then the pass condition `Q95_null ≤ L` certifies a resolution the estimator does not have. That is an *optimistic* failure — the direction this gate exists to avoid.

The reason that is survivable is a bound, and a bound is checkable, so I checked it rather than asserting it. A pass also requires `Delta_10 ≤ L` computed from the real time ordering, which the null cannot touch. In the probe, a candidate at `Delta_10 = 25 µm` against `L = 20 µm` fails for every `q95` in {0, 1, 10, 19.999, 20, 25, 1×10⁶}. **A mis-scaled null can only mislabel a quiet candidate's resolution; it can never admit a moving one.** That is now in §16.5 rather than only in a chat message.

### 4. The clone-byte repair, extended and verified

I reproduced Codex's experiment from scratch before touching anything: fresh clone of `13e9926` at the machine's `core.autocrlf=true`, compared file by file with SHA-256. **His packet result holds exactly — 0 of 42 packet files differ.** His supersession of the repo-wide version was also correct in its diagnosis: `* -text` alone would have fixed thirty packet files and broken eleven others whose tested working bytes are CRLF while their blobs are LF. Independently re-deriving that override list from the working bytes returned his eleven files exactly.

But the same clone showed **81 of the 151 tracked files still differed** — 80 that are LF in the working tree and get CRLF written on checkout, plus the active review transcript, whose mixed physical form no configuration currently reproduces. The 81 include `Claim Sheet.md`, `Accessible Claim Sheet.md`, the host-selection document under review, and `test_band_drift.py`. That last pairing is the one that decided it for me: **`band_drift.py` survives a clone and the harness that validates it did not.** Every digest this project has published outside the packet was unreproducible by anyone who cloned it on Windows.

The cost that justified keeping the repair narrow was "re-recording CRLF bytes merely to preserve non-packet working representations." I measured that cost instead of arguing about it. Re-recording is only needed for files that are CRLF *in the working tree*, and outside the packet there are **17**: `AgentPrompt.md`, `LICENSE`, `LICENSE-docs`, `LICENSING.md`, all eleven playbooks, `Project Details/Project Details.md`, and `agents/Claude/README.md`. Every one is already LF in its blob, so an explicit `text eol=crlf` override reproduces its tested checkout with no blob re-recorded and no working byte changed. The other 81 are LF in both places, so `-text` costs nothing at all.

The implemented state is `* -text` with `text eol=crlf` overrides for those 17 plus Codex's 11, and the review transcript stored at its true mixed bytes. Verified by cloning a temporary commit of the exact session state at `core.autocrlf=true`: **152 of 152 tracked files byte for byte, 0 differences, packet included.** No working file's SHA-256 changed to achieve it. The temporary branch and both clones were deleted.

---

## Challenges, and how they were handled

**Deciding whether a documentation-only finding was worth another round-trip.** Finding B changes no behaviour — the gate computes the same numbers either way. The pull was to approve and stop, because this artifact has now been in review for several sessions and nothing has been measured. What settled it was that Finding A arrived in the same pass and *does* change a rule (the input-error-versus-rejection distinction), so the round-trip was happening regardless; bundling B into the same handoff costs nothing extra. Had A not existed I would have approved and propagated B forward.

**Not letting Finding A grow into more than it is.** The measured discrepancy is 1.138 s against a 60-second bin. It would have been easy to write it up as a near-miss that would have corrupted the first measurement, and that would not be true. Draft 12 and this report both state the expected effect is negligible and locate the defect in the *unnamed input*, not in the arithmetic.

**Whether to fix the estimator's docstring too.** `measure_band_drift` documents `duration_s` only as "the recording duration in seconds", which is exactly the ambiguity Finding A is about. I chose not to edit it: the module correctly takes the duration from its caller, the obligation belongs to the CLI that does not exist yet, and re-opening an implementation both agents otherwise agree on for a comment would add a third open surface. The obligation lives in §16.4 and §16.8, which the session that writes the CLI must read first.

**A shell trap, recorded because it cost time.** The status line rewrite initially left Draft 11's historical narration stranded mid-paragraph behind my new text, because I replaced the head and tail of a sentence and not its middle. Reading the rendered line back — rather than trusting the six-replacement script's "all applied" — caught it. This is lesson 26 again: a diff will not show you an incoherence that neither side of the diff contains.

---

## Decisions made

1. **Approve `band_drift.py` and `test_band_drift.py` at Codex's exact digests**, closing the implementation loop, while handing back only the document. Minimizing the open surface is the point.
2. **Do not read any candidate.** The timebase question is answerable only by reading a processed asset, and Codex's constraint that no candidate may be measured while §16 is open governs. It becomes the script's first job once the specification is same-state approved.
3. **Rule that a timebase mismatch is an input error, not a drift rejection.** Under first-admissible in a pinned order, the alternative is a silently unrecoverable false rejection.
4. **Extend the clone repair repository-wide** rather than propagating it forward, because the residual defeats the digests both agents exchange in review and the repository is public.
5. **Keep the review probe as a permanent file** in `agents/Claude/tools/`, including its restoration of the pre-repair permutation, so the defect cannot be quietly reintroduced.
6. **No new `director_requests.md` entry.** Nothing this session needed the director.

---

## Reasoning paths explored

**Could the null's bias fail in the deflating direction at all?** I tried to construct a mechanism where real movement *narrows* `Q95_null` and could not find a clean one — under additive common motion the pooled within-unit spread can only grow. That is an argument, not a proof, which is precisely Codex's point, and it is why §16.5 now states the bound rather than a second proof.

**Whether the timebase mismatch would fail loudly.** Mostly it would: spike times starting late leave the first bins empty, which trips the bin-validity rule and rejects. But the rejection carries the *wrong diagnosis* — it reads as a bad candidate rather than a bad input — and one mode is genuinely quiet, where spikes extend past the last edge and are silently dropped from both the observation and now the null. The loud-but-misdiagnosed case is the one that actually costs a host under first-admissible.

**Whether `2,048` assets and other pinned constants needed re-checking.** They were re-derived in Session 18 and nothing this session touched them.

---

## Insights gained

1. **Removing an over-strong claim creates an obligation to state what now rides on the assumption.** Codex's withdrawal of my monotonicity proof was correct; what it left behind was a rule whose safety was no longer argued anywhere. The repair is not to restore the proof but to bound the exposure.
2. **A repair can widen the blast radius of a defect elsewhere.** Restricting the permutation pool to complete bins was right, and it made the bin boundary — set by an unpinned input — matter in one more place than before. Worth asking, after any repair, what else now depends on the thing it touched.
3. **"Fixed" needs a scope, and the scope is the first thing to measure.** The packet clone repair was correct and complete for the packet, and the sentence "the clone defect is fixed" would have been read as covering the repository. Measuring the remainder took one script.
4. **A cost that justifies not doing something should be measured before it is accepted.** The re-recording cost was real in principle and applied to 17 framework files that can be declared explicitly for free. The narrow fix was chosen on an estimate; the wide one survived a measurement.
5. **The validator has to travel as well as the thing it validates.** A packet that reproduces byte for byte alongside a test harness that does not is only half a reproducibility claim.

---

## Files created or updated

| Path | What changed |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 12**, SHA-256 `e1b93eed32f791acce51bbf5eda7d23ad7e6a175b8492086d99d24a791d6b313`. Status rewritten; §16.4 point 2 names the timebase; new §16.4 paragraph pins the grid's anchor and length; §16.5 gains the bounded-exposure paragraph; §16.8 goes from two required confirmations to three. **Open on Codex.** |
| `.gitattributes` | Rewritten repository-wide. SHA-256 `9c18d148995251ab5c242fe4c2cdace5546b27f29956750625bba0cb673e13a8`. **Open on Codex.** |
| `agents/Claude/tools/probe_band_drift_claims.py` | **New.** Three review probes: independent reproduction of the partial-bin defect, randomized complete-bin pool identity, and the pass-rule bound behind §16.5. SHA-256 `e7caeb552e16f3393e4eef563c4e395cc1a9e52b7f7f0a6f76329facbf55c41a`. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Session 19 message appended; file also re-recorded at its true mixed bytes under the new attributes rule. |
| `README.md` | Two running-log entries: the timebase catch, and a correction narrowing the previous entry's clone-fix claim to the packet before reporting the repository-wide result. |
| `agents/Claude/README.md` | Workspace tree updated for the new probe. |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten for Session 20. |
| `agents/Claude/Session Summaries/HumanReport19.md` | This report. |

**Not changed, deliberately:** `Claim Sheet.md`, `Accessible Claim Sheet.md`, `Reproducibility Packet/scripts/utils/band_drift.py`, `agents/Claude/tools/test_band_drift.py`.

---

## Machine state

Measured at **2026-08-13 10:18 PDT**: RAM **5.55 GiB free of 31.67** (82% in use); VRAM **1,092 MiB used of 16,311**; **603.8 GB free on `C:`**. Nothing heavy ran this session — the longest job was the 200-permutation null on synthetic fixtures, a few seconds each. Do not inherit these numbers; measure again.

---

## Next steps

1. **Codex's same-state review of Draft 12 `e1b93eed…` and `.gitattributes` `9c18d148…`.** The estimator and its harness are closed at Codex's digests and need nothing further.
2. **Once §16 is same-state approved: write the archive-reading drift script**, which becomes packet step 11 only after it has actually been executed. It must confirm all three §16.8 preconditions before computing — the ragged index, depth presence and finiteness, and now the timebase — reuse `utils/remote_hdf5` and `utils/host_anatomy`, call into `utils/band_drift`, and report `n_bytes`/`n_requests` rather than discarding them. 1 MiB blocks beat the 4 MiB default for scattered reads.
3. **Then, and only then, measure rank 1 on the drift gate**, and fold in the five archive-reading packet steps that have never been re-run.
4. **Still open and not mine:** the footprint/placement calibration and the covariate-balance gate are Codex's; the capacity gate needs re-establishing under Amendment 6's stricter joint ten-placement condition once `N` and the rota are known.
