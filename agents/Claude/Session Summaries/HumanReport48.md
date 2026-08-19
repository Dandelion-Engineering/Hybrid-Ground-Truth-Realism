# Human Report 48 — Claude

**Date and time:** 2026-08-19 04:45 PDT

**Phase:** Phase 2 — Execution. RC-008 Round 3, the final owner response on the host noise gate specification.

**Session outcome:** **Draft 34 is presented as the Round-3 candidate**, `ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89`. Codex's two Round-2 blockers (F6-R2, F7-R2) and three tracked delta items (T5-R2, T6-R2, T7-R2) are **all accepted, none disputed**, and one further defect was found here — plus a coverage gap that repairing it created in my own harness, which I also found and fixed. **This is the last round the review method allows on this card.** No archive sample was read, no candidate's noise value exists, no estimator was written, no packet file changed, no host is pinned, and rank 2 remains unmeasured.

---

## 1. Startup, and the turn gate

`.agent-turn` named Claude and no `.agent-session.lock` existed. I created the lock, re-read `.agent-turn`, confirmed it still named Claude, then read `AgentPrompt.md`, the whole of `Project Details/Project Details.md`, my `Summary of Only Necessary Context.md`, and the two active chats. Sixteen concluded chats have summaries; the only reply owed by me was Codex's Round-2 delta pass in `chats/Claude-Codex/Section 19 Convergence Repair/`. The three-way `Review Method Change` chat stays open at Randy's instruction with nothing pending.

**Machine reading at 04:08 PDT: 17,075 MiB of 32,425 free.** A second reading at 04:30 gave 16,944 MiB. **Nothing heavy ran this session** — no archive read, no network request. Every construction is synthetic and the whole evidence suite runs in under a minute.

## 2. Cross-review

I read Codex's `HumanReport47.md` in full and his two recorded outputs, `rc008_round2_2026-08-19.txt` and `.json`, and reproduced both of his blocking findings independently before repairing either. His report and the card agree with each other and with the chat message; I found no discrepancy to raise. His §3 and §4 are the two blockers below.

## 3. F6-R2 — two of three grounds for the contiguous split are false

**Background.** Each 0.434-second window is split into two halves so the gate can measure how much of the observed channel-to-channel spread is its own estimation noise rather than the recording's. Draft 32 pinned the split as *contiguous* (first half, second half) rather than *interleaved* (alternate samples), on a claimed direction — interleaving compresses the statistic in the permissive direction. RC-008 Round 1 refuted that direction, and Draft 33 replaced it with three non-directional grounds. **Round 2 refutes two of the three.**

**Ground 1 — near-independence.** Draft 33 said two adjacent stretches give close-to-independent estimates for a signal band-limited above 300 Hz. Codex exhibited a 400.921659 Hz process, wholly in band, that repeats exactly across the two 6,510-sample halves, making them perfectly correlated.

**I did not accept the instance; I derived the family.** A frequency `f = m × 30,000 / 6,510` Hz has a period dividing one half exactly for every integer `m`, and `f > 300 Hz` from **`m = 66`, 304.147465 Hz**, upward. Codex's figure is `m = 87`. I built 135 consecutive members: **all 135 give bit-identical halves, correlation exactly 1 and a half-ratio of exactly 1.** Putting the block through §19.3's own pinned filter chain leaves the agreement at `r_c = 1.000000000000`, so the counterexample is not an artifact of skipping the filter. Generalising the counterexample is what makes the ground unrecoverable rather than merely narrowed.

**One implementation note worth recording, because it looked like a failure and was not.** My first version of the check computed the sine as `sin(2π f k / f_s)` and the two halves differed by `2.7e-13` — floating-point rounding in the phase argument, not a defect in the claim. Evaluating the identical function as `sin(2π m (k mod 6510) / 6510)` — which is exactly what `f = m·f_s/6510` means — makes the identity exact in floating point too. **That is computing the same quantity without avoidable rounding, not relaxing the test**, and I want the distinction on the record because the other resolution (loosening the tolerance) would have looked the same from outside.

**Ground 3 — the one Draft 33 called decisive.** It said the decision rule cannot "cash" a lower value of this uncertainty statistic, because a low value certifies nothing by declaration. **Codex is right and the error is a slide from *certifies nothing* to *does nothing*.** A low value is *necessary* for a pass: branch 4 rules a candidate `unmeasurable` when the spatial statistic is inside tolerance and the uncertainty statistic is not. **On the parity construction I built for F3-R1 one round ago** — whose spatial statistic is exactly **1.5** against a strict tolerance of **2.0**, with the level in band — the contiguous split reaches **`passes`** and the interleaved split reaches **`unmeasurable`**. The split rule alone changed the disposition.

**What replaces the two grounds is a reach, and it is proved rather than exhibited.** The split enters the decision only through the uncertainty statistic, because the spatial statistic is computed on the retained core and **both split rules are partitions of that identical core** — the probe checks that by sorting rather than asserting it. The uncertainty statistic acts in exactly two places. Evaluated over the whole truth table: **9 state pairs moved between `passes` and `unmeasurable`, 6 relabellings of a homogeneity failure, 57 untouched, and no transition of any other kind.** So a change of split rule can never turn a failure into a non-failure or a non-failure into a failure, and *how much* it can move a value is not bounded anywhere.

**The split stays contiguous on the one surviving ground, and §19.5 says how thin that is.** An interleaved split carries a free period parameter whose effect cannot be signed; the contiguous split at the midpoint has no parameter to choose. **The section explicitly refuses the reading that contiguous halves are the safer of the two**, because nothing here establishes that. I flagged in the handoff that *this choice cannot be pinned* is a disposition I would take over a ground I cannot defend.

## 4. F7-R2 — the regression wrapper authenticated five of six inputs

RC-008's F4-R1 required the wrapper to authenticate the closed card's checker and every record it consumes before trusting its output. Draft 33 pinned five paths and asserted, one line below the list, that *every file the baseline reads is the pinned one*. **The baseline reads six.** Codex replaced `Reproducibility Packet/results/host_timing_index.jsonl` in a staged tree with a byte-different synthetic record preserving the two aggregates the checker consumes, and the wrapper still reported 168 checks, 0 failed and exited zero.

**The finding is correct and the repair is not a sixth entry.** A hand-maintained list cannot make a completeness claim about an input it does not know exists — which is exactly how a five-entry list came to sit under that sentence. `probe_rc008_spec.py` now **parses `probe_rc007_spec.py`'s own source** with Python's `ast` module for every `os.path.join` path constant it defines, and fails if any of them is neither the candidate document nor a pinned digest. It **raises rather than passing quietly** if a `_REL` constant is built from anything other than string literals, because a computed path is one this check cannot see. The timing index is pinned at `043a4ea4…`; **the file itself is unchanged.**

**Two mutations reach the new surface**, and choosing them took some care:

- **Re-serialising the timing index** — byte-different, every value and every aggregate preserved. Nothing but a digest can distinguish it from the original, which is the point.
- **Removing the timing index's entry from the wrapper's own list.** This leaves every pinned digest correct and every file authentic; it can *only* be caught by the derived completeness check. A mutation that damaged the legacy checker instead would have been caught by its digest — for the wrong reason.

**All five instrument mutations now name the check that has to be the one going red**, so a mutation passing on an unrelated failure is visible rather than silent. That is the defect that cost me a real mutation two sessions ago.

## 5. The three tracked items, one of which had a consequence

- **T5-R2** — §19.10 lists four sampled quantities and then said a short excursion is invisible to "all three." Now four.
- **T6-R2** — §19.3 explained the phase-omission bias and closed with *which is why §19.6 does not lean on the floor*: true when written, false since Draft 33 gave the floor its own statistic and its own branch. **Deleting the clause is not the whole repair.** Branch 2 rejects on the quietest sampled window now, so under the same shared-component model the omitted phase shift makes that branch **permissive** — an upward-biased quietest window can fail to fire the floor on a genuinely too-quiet host, and cannot fire it on one that is not. §19.3 states it and §19.10 carries it as a boundary. Codex's own report anticipated this reading; I have written it as a limitation rather than as a hedge.
- **T7-R2** — §19.7 asked for "the candidate's own declared rate" beside the nominal one, and rank 1's raw AP series declares no rate at all. **That is the same fact §19.3 uses to refuse F2-R1's other repair, two subsections apart and pulling in opposite directions.** §19.7 now asks for the series' `rate` attribute where one exists and the whole-span figure derived in `host_timing_index.jsonl` where it does not, **labelled as which**.

## 6. One defect found here, and the gap that repairing it opened

**§19.8's conditional sentence still read *if anyone reports `A_min / sigma_worst_sampled` and `A_max / sigma_worst_sampled`*.** Draft 33's F1-R1 repair changed the reported ratios one paragraph above it — `snr_p2p_max` divides by the *quietest* window now — and left the sentence describing them behind. It names the two reported ratios that **are** §19.6's conditions rearranged, `snr_p2p_min` and `snr_p2p_quiet`, and states plainly that `snr_p2p_max` rearranges no condition at all: it is the loud end of a span, reported because a span has two ends. **F1-R1 was reported against §19.6, was found to reach §19.8's ratios as well, and reached one sentence further than that.**

**And repairing it broke one of my own mutations, quietly.** Naming `snr_p2p_max` a second time in §19.8 gave the existing "revert the ratio to the wrong denominator" mutation somewhere to hide: the check looked for the bare string, which the new sentence also contains, so reverting the *definition* left the check green. The harness caught it — the mutation reported `not caught` — because the harness requires every mutation to be caught, not merely to run. The definition check is now anchored on its own clause and the occurrence count is asserted at exactly two.

## 7. One publication no finding asked for

§19.7 now carries the full per-window `ρ(k)` series that the uncertainty statistic is the maximum of, on the same footing as the `S(k)` level series and the per-channel estimates. F6-R2 established that the split rule has a decision destination; a reader can now see sixty numbers rather than one, and the paragraph that used to argue the choice was harmless is gone. This is the same move F5-R1 forced one round ago: **when a direction claim is withdrawn, publish the raw values that would have supported it.**

## 8. Evidence, and what each instrument is for

| instrument | result |
|---|---|
| `probe_rc008_spec.py` (extended in place) | **241 checks, 0 failed** |
| `mutate_rc008_spec.py` (extended in place) | **42 of 42 caught**, control green |
| `probe_rc007_spec.py` (closed card's, untouched, run as a regression baseline) | **288 checks, exactly 16 failed** — **the same sixteen as Round 2, by name** |
| `probe_rc008_round3.py` (new) | **32 checks, 0 failed** |

**That the legacy baseline's red list is unchanged is itself the finding**: Draft 34 caused no new class of legacy red. Four of the sixteen are counts that grew further, and the wrapper's own census — now six regions, because §19.15 is a new one — is what carries those. The census asserts that its regions **partition the file**, so a restatement appearing somewhere no region covers has nowhere to hide.

**Nothing that decides anything moved.** `N` is 10.0 and 25.0 µV, `M` is 2.0 and 4.0, the floor is 1.25 µV and does not relax, `K` is 60, the retained core is 13,020 samples with 6,510 in each half, the split is still contiguous, the grid and the 170-chunk / 73.780-second coverage theorem are untouched, the transfer projection is still 957,031,364 bytes, and §1–§18 are byte-identical at their three published span digests.

## 9. An error of my own, recorded rather than smoothed over

**I wrote the timestamp `2026-08-19 04:40 PDT` into the Draft 34 status line, the review card and the chat message before reading the clock.** The actual readings that bracket those writes are 04:08 and 04:30. The figure falls inside this session's real span and misorders nothing — Codex's Round-2 message is 03:22, and the previous entries are from 2026-08-18 — but it was written from an estimate, which is exactly the practice my own notes tell me to avoid. **I have not cascaded a correction**, because the status line's digest is published in the card, the chat and two record files, and rewriting all four over a ten-minute offset would be a worse trade than recording it here. **The rule stands: read the clock at the moment you write the timestamp.**

## 10. Files created or updated

**Updated**

- `agents/Claude/Tier A Host and Injection Zone Selection.md` — **Draft 34**, 343,106 bytes, `ecccfa56…`. §19.3, §19.5, §19.7, §19.8, §19.10 edited; §19.14 gains a supersession note; **§19.15 is new**; the status stack gains Draft 34's line above Draft 33's, which is retained unedited with its own now-superseded claim.
- `agents/Claude/tools/probe_rc008_spec.py` — extended in place, `2f20099b…`, **241 checks**.
- `agents/Claude/tools/mutate_rc008_spec.py` — extended in place, `2b19e1ec…`, **42 mutations**.
- `Review Cards/RC-008 Host Noise Gate, Convergence Repair.md` — Round-3 candidate, response, and round-log addendum appended.
- `chats/Claude-Codex/Section 19 Convergence Repair/Section 19 Convergence Repair - Active.md` — my Round-3 response appended.
- `README.md` — one new dated log entry; **90 dated entries**, counted rather than incremented. The banner already read 2026-08-19.

**Created**

- `agents/Claude/tools/probe_rc008_round3.py` — `6210e7d2…`, the Round-3 evidence probe. Every number Draft 34 publishes about F6-R2 is computed in it.
- `agents/Claude/tools/rc008_round3_2026-08-19.txt` / `.json` — `4edf5eb0…` / `3ca619e4…`.
- `agents/Claude/tools/rc008_spec_2026-08-19_draft34.txt` / `.json` — `94277e0e…` / `7deafd99…`.
- `agents/Claude/tools/mutate_rc008_spec_2026-08-19_draft34.txt` — `83b15d93…` (CRLF, like every captured-stdout mutation record).
- `agents/Claude/Progress Reports/Progress Report Session 48.md` — the count-based progress report this session owes.

**Not touched:** the Claim Sheet, the Accessible Claim Sheet, the Study Guide, and every file in `Reproducibility Packet/`. The timing index is authenticated but unmodified.

## 11. What is next

1. **Codex's Round-3 delta pass. It is a verdict, not another revision.** If it does not reach same-state approval, the card freezes and the Convergence Decision fires; clause 5 forbids a third like-for-like successor, so the work would have to be split or redesigned with the changed boundary named.
2. **Then the estimator** — a packet utility plus a synthetic harness, the shape `band_drift.py` took after §16 closed. Deliberately not written before the specification closes.
3. **Rank 2 (NYU-12 Probe01) drift measurement** — unblocked, cheap, and waiting behind this.

## 12. Reflections

**The sharpest lesson this session is about the shape of my own error rather than its content.** F6-R2's decisive ground was a slide between two sentences that look alike — *this value certifies nothing* and *this value does nothing* — and the first is a declaration the specification makes on purpose while the second contradicts its own branch order. I have now made a version of this mistake twice in three sessions: **withdraw a false claim, then fill the gap with an argument invented in the same draft, with nothing checking it.** The repair I am adopting is not another rule but a habit: an argument constructed in the draft that first needs it should be labelled as untested, or the withdrawal should stand alone.

**The second lesson is about counterexamples.** Codex handed me one frequency. Generalising it to a family with a stated lower bound, and building 135 members, converted "here is an awkward case" into "this reasoning cannot be rescued." That is a better outcome for both of us than a narrowed claim, and it took ten minutes.

**The third is that a repair can open a hole in the instrument that was watching it.** Fixing §19.8's stale sentence gave an existing mutation a second string to hide behind. The only reason it surfaced is that the harness requires each mutation to be *caught* rather than merely to *run*.
