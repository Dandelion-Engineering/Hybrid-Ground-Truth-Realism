# Human Report 20 — Claude

**Date and time:** 2026-08-14 01:26 PDT
**Phase:** 2 — Execution
**Session type:** Owner re-review of Codex's Draft 13; three repairs; no candidate read, no data downloaded, nothing heavy run

---

## Summary

This session was my owner re-review of the state Codex handed back at the end of his Session 19. Under the review cycle I had to do one of two things with his Draft 13: approve those exact bytes, or edit and hand back. I accepted both of his repairs in full, and I could not approve the draft unchanged — the re-review turned up three things, one of which is a second unnamed input to the drift gate and one of which was a defect **in my own first attempt at a repair**, caught before it left the building.

Nothing was measured. No recording was opened, no dependency installed, no sorter run. The machine was at 94% memory in use for the whole session, which is a good illustration of why the "measure before anything heavy" rule exists — nothing heavy could have run tonight even if the work had called for it.

The headline for a non-specialist: **the gate that will decide which recording this project uses was found, twice more, to be quietly depending on numbers nobody had chosen deliberately.** Neither one changes a single value on the recordings already on file. Both change the rule from one that would have worked by luck into one that states what it needs and checks it.

---

## What I did, in order

### 1. Startup gates

- Read `.agent-turn` (named Claude), confirmed `.agent-session.lock` was absent, created it, re-read `.agent-turn` (still Claude).
- Read `AgentPrompt.md` and all of `Project Details/Project Details.md`.
- Read my `Summary of Only Necessary Context.md`.
- Read every `Summary.md` in the Claude-Codex chat folders, then the full active `Tier A Selection Review` transcript.
- Read Codex's `HumanReport19.md` — this session's cross-review obligation — and the work it points to.

### 2. Verified every handed-back state before reading it

Five digests claimed, five matched:

| artifact | SHA-256 | verdict |
|---|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 13 | `82d58b4009…` | re-reviewed, superseded by Draft 14 |
| `.gitattributes` | `036c696c3e…` | **owner-approved** |
| `agents/Claude/tools/probe_band_drift_claims.py` | `4f3b837731…` | **owner-approved** |
| `Reproducibility Packet/scripts/utils/band_drift.py` | `d8b0359684…` | closed, unchanged |
| `agents/Claude/tools/test_band_drift.py` | `82aaf77e99…` | closed, unchanged |

### 3. Re-ran rather than read

- `probe_band_drift_claims.py` against the shipped module: **3 of 3 probes pass.**
- `test_band_drift.py --permutations 200`: **57 checks, 0 failed.**
- `check_runbook_consistency.py`: **green at ten steps.**

### 4. Accepted both of Codex's repairs

**His §16.5 repair.** My Draft 12 said a mis-scaled null could "never admit a moving one." The probe backing that sentence tests a candidate whose *observed* excursion already exceeds the gate — which proves the null cannot rescue it, and proves nothing about a probe that physically moves while IBL's depth trace understates the movement. The section itself leaves that bias unbounded two paragraphs later, so my sentence was contradicted by its own neighbour. Correct catch, kept exactly as written.

**His §16.8 repair.** The section still said the estimator was "defined and not implemented" after both of us had explicitly approved its code and harness. Correct, kept as written.

**His `.gitattributes` repair.** My comment said every path is "stored and checked out as-is." That is false for exactly the files the sentence pointed at: `text eol=crlf` normalizes to LF in the object database and denormalizes on checkout. His replacement says so. Behaviour unchanged; explanation now true. Approved.

---

## The three findings

### Finding 1 — my own repair was wrong in the opposite direction, and I caught it while writing the consumer

The previous session found that `duration_s` in our timing index is a **span** (`t_last_s − t_first_s`) rather than an end time, and that the first timestamp on the rank-1 candidate is 1.138 s rather than zero. Codex accepted that. The obvious follow-through, which is what I wrote first, was: `t_last_s` is recorded in the same record, so take the length from `t_last_s` and never from `duration_s`.

**That is wrong half the time.** If the processed file's spike times are expressed relative to the raw stream's own start rather than on the same absolute clock, then the extent in *their* timebase is the span, and `duration_s` was right all along. Draft 13 named one field unconditionally; my first repair named the other field unconditionally. The same defect, pointing the other way.

I found it by starting to write the script that would consume the rule and asking what it would actually do with each field. Draft 14's rule is conditional: `t_last_s` if the spike times are the raw stream's absolute times, `duration_s` if they are stream-relative, **and neither as a default**.

**The test that decides is now pinned, and it needs no new parameter.** Take the earliest and latest spike time over the probe's units and ask which of two windows contains that interval: `[t_first_s, t_last_s]` for the absolute-clock hypothesis, `[0, duration_s]` for the stream-relative one. Exactly one containing it fixes the length. Both containing it — which is automatic on the seventeen series whose first timestamp is zero — goes to a bin-count comparison: if the two lengths give the same number of bins the ambiguity cannot change a result and is published as an ambiguity rather than resolved by preference; if they differ, the candidate is an input error. Neither containing it is an input error too.

I also wrote down what containment **cannot** do, because my first version of that sentence overclaimed as well. It catches a clock that runs long, because such a spike set overruns both windows. It does not catch a clock that runs short — a compressed set sits inside both and would be handed a length longer than its own extent. That case is not silent either: the surplus bins at the end hold no spikes, so they miss the five-included-unit validity rule and the candidate is rejected as unmeasurable with the reason published. A compression under one bin escapes both tests and moves nothing a 60-second grid can see.

**Measured size:** on all twenty-one recorded AP series, `floor(t_last_s / 60)` and `floor(duration_s / 60)` return the identical bin count, rank 1 included at 72 either way. Nothing numerical moves. What moves is that the rule stops naming a field unconditionally.

### Finding 2 — the new exclusivity clause was narrower than the section's own labelling rule

Codex's replacement said a mis-scaled null "can only change the resolution verdict among candidates whose observed excursion is already at or below the gate." But §16.7 says that *above* the gate the report labels a failure *resolved drift* when the observed excursion exceeds the null and *noise-limited* otherwise — so the null moves a verdict on that side too, and the paragraph two above his already says so in those words.

The rejection is untouched either way, which was his point and which stands. What the clause excluded was the published *reason*, and that is not cosmetic: the section requires the reason to be published, and requires the 40 µm relaxation to be published with every value that forced it, so a reader judging whether the relaxation was earned is reading exactly those labels. Draft 14 states both sides.

### Finding 3 — a second input the gate consumes and nobody named

The drift gate selects its unit set as "units whose `distance_from_probe_tip_um` falls inside the pinned CA1 band." **The band's bounds are in the electrode table's `rel_y`. Nothing in this project has shown those two to be the same coordinate.**

- The Session 9 validation established that the donor library's `depth_along_probe` and the host's `rel_y` agree. Different pair.
- `screen_injection_placement.py` selects its band units by `rel_y` at each unit's `max_electrode`, not by tip distance — so the native-yield numbers in §10 do not settle it either. That script *reads* the tip distance and stores it per unit, and no consumer has ever compared the two.

I checked whether it is answerable from what is already downloaded, because that check has paid off twice in the last three sessions. **It is not:** `injection_placement_CA1.json` keeps only aggregates, and `amplitude_conventions.json` keeps per-unit rows carrying neither depth. Recording the empty answer, not just the question.

Draft 14 makes it the gate's fourth pre-computation confirmation, on the same semantics as the timebase: median of `distance_from_probe_tip_um` minus the `rel_y` of the unit's `max_electrode`, with the interquartile range beside it; within one contact row (20 µm — a scale the section already pins, so no new parameter enters) means the same coordinate; outside it is an **input error to resolve, not a drift rejection**. Median rather than mean because Codex's own amplitude audit established that `max_electrode` follows a different best-channel rule and disagrees on near-ties between adjacent rows — about a row of scatter, without a bias.

Translating the band by the measured offset is the obvious repair and is **deliberately not authorized**, because it would let a number derived from the candidate move the zone the gate is evaluated in.

Worth naming precisely what is exposed: every step of the statistic is a difference, so it is immune to a constant offset between the two coordinates. Only the *selection* is not.

---

## Decisions I made, and why

**I edited rather than approved, knowing it keeps the review open and blocks candidate measurement for another round trip.** Findings 1 and 3 both change what the measurement script has to confirm before it computes anything. Fixing them after the script exists costs more than one round trip.

**I did not start the archive-reading script.** It is the next piece of work in my lane and I had the session time for a first version, but two of the three findings changed its contract mid-session. A script written against a specification that is still moving encodes a draft nobody approved. It is the first thing after this loop closes.

**I corrected my own repair inside the same session instead of shipping it and correcting it later.** The wrong version was written, rendered, read back and replaced before the handoff. The report says so because the near-miss is the useful part.

**I updated the public running log** with one entry covering both corrections, at the plain-language bar, and moved the banner's "Last updated" to 2026-08-14.

---

## Reasoning paths explored and abandoned

- **Approving Draft 13 as-is and folding the exclusivity-clause wording into a later draft.** Rejected: Finding 3 arrived while checking Finding 1, and it is a genuine unnamed input rather than a wording preference. Once one edit is required, holding back a second one to save bytes is not a real economy.
- **Selecting band units by `rel_y` at `max_electrode` instead**, which would make the coordinate question disappear because the band bounds are in that same coordinate. Rejected as a unilateral rule change inside an artifact under active review, and because the per-spike depths the statistic actually consumes live in the tip-distance coordinate; naming the dependency is the honest move, switching the rule under review is not.
- **Translating the band by the measured coordinate offset if the two disagree.** Rejected on principle: it would let a candidate-derived number move the zone the candidate is then judged in.
- **Pinning a numeric tolerance for the timebase reconciliation.** Rejected once I found the containment formulation, which decides the same question with no free parameter at all — and a tolerance would have been exactly the class of unpinned input this session is about.

---

## Insights worth carrying

1. **Following a repair into its consumer is what caught the over-correction.** Reading the rule was not enough; asking what the script would do with each field is what exposed that both fields are correct under different clocks.
2. **A repair can be wrong in the mirror image of the defect it repairs.** "Never `duration_s`" and "always `duration_s`" are the same mistake.
3. **Sixth instance of the same shape:** a pinned rule eating an unpinned input. Threshold at an unpinned measurement point; matching rule over unpinned placements; first-admissible over an unpinned order; a null test with no stated summary; a bin grid with unpinned anchor and length; and now a unit set compared across two depth coordinates never shown to be one. When you approve a rule, ask what it eats.
4. **Recording that a check came back empty is worth as much as recording one that came back full.** Third session running.
5. **A "can only" clause is a quantifier, and a quantifier is a claim.** Both of the last two sessions' findings in §16.5 were exclusivity clauses that excluded something real.

---

## Files created or updated

| path | what changed |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 13 → **Draft 14**, SHA-256 `3b0f89d222f2d3f3a1ce4e904123bbb110cd726ff10f7621010bec6766cdb775`. §16.4 conditional length rule and the coordinate input; §16.5 exclusivity clause; §16.8 containment test and fourth confirmation; status line. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Session 20 message appended (append-only, prefix verified byte-identical afterwards). |
| `README.md` | One running-log entry; banner "Last updated" → 2026-08-14. |
| `agents/Claude/Session Summaries/HumanReport20.md` | This report. |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten for Session 21. |
| `agents/Claude/README.md` | Refreshed status pointers. |

Nothing was added to `references.md`: no new external source informed this session's work.

---

## Machine state, measured

**2026-08-14 01:20 PDT — RAM 1.84 GiB free of 31.67 GiB (94% in use); VRAM 1,087 MiB used of 16,311 MiB; 583.8 GB free on `C:`.**

Nothing heavy was run and nothing heavy could have been. Recorded so the next session inherits evidence rather than a hunch — and so that the reading is not inherited: take your own.

---

## Next steps

1. **Codex's same-state confirmation of Draft 14** at `3b0f89d222…`. §16 stays open until then and no candidate may be read.
2. **The archive-reading CLI** — the first thing after the loop closes. Targeted range reads over the ragged `spike_times` and `spike_distances_from_probe_tip_um` slices for band units only, reusing `remote_hdf5` and `host_anatomy`, calling into the approved `band_drift`, reporting bytes and requests. It must now discharge **four** pre-computation confirmations, not three.
3. **Then the first candidate measurement**, rank 1 of the pinned order, under the strict 20 µm rule.
4. Still open and unchanged: the capacity/ten-placement gate under Amendment 6, the noise and effective-SNR gates, and the five packet steps that have not been re-run.
