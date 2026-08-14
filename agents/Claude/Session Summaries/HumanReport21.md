# Human Report 21 — Claude

**Date and time:** 2026-08-14 03:19 PDT
**Phase:** 2 — Execution
**Session type:** Owner re-review of Codex's Draft 15; three precision repairs; no candidate measured

---

## Summary

This session was my owner re-review of Codex's Draft 15 of `agents/Claude/Tier A Host and Injection Zone Selection.md`, under `Playbooks/review-cycle.md`. **I accepted both of his blocking corrections in full and kept his repairs exactly as written**, and then found three further things in the re-review pass. All three are additions to §16 rather than disagreements with Draft 15, and none of them changes a parameter, threshold, candidate order, statistic, verdict or rule. I handed back **Draft 16** at SHA-256 `7fed750c8f48420521e2038b32285d72d7b719dfd1490c40dbccc14a6e2204ec`.

The largest of the three is the one worth reading: the drift gate's unit set was never pinned to a quality filter, and under one of the two available readings the ninth-ranked candidate would have been rejected before a single number was computed — for a sparse-recording reason the project had explicitly decided not to gate on. That is the **seventh** time in this project a carefully pinned rule has turned out to consume an unpinned input.

**Nothing was measured, downloaded, installed or run beyond already-cached metadata.** There is still no host, no candidate drift value, no donor, no generator, no Rung 0 and no sorter run — and no scientific result.

---

## What was accomplished

### 1. Startup gates

- Read `.agent-turn` (named `Claude`), confirmed `.agent-session.lock` absent, created it, re-read `.agent-turn` (still `Claude`).
- Read `AgentPrompt.md`, `Project Details/Project Details.md`, my `Summary of Only Necessary Context.md`, every concluded chat `Summary.md` in `chats/Claude-Codex/`, the tail of the active Tier A selection transcript, `Playbooks/review-cycle.md`, and `director_requests.md`.
- **Cross-review obligation discharged:** read Codex's `HumanReport20.md` and the Draft 15 state it points at.
- Verified seven digests before opening anything: Draft 15 `3f25a707…`, `Claim Sheet.md` `2feda611…`, `Accessible Claim Sheet.md` `679918f7…`, `band_drift.py` `d8b03596…`, `test_band_drift.py` `82aaf77e…`, `probe_band_drift_claims.py` `4f3b8377…`, `.gitattributes` `036c696c…`. All seven matched their approved values.
- Re-ran rather than read Codex's numbers: **3 of 3 claim probes passed; 57 checks, 0 failed at the pinned 200 permutations; 10 of 10 runbook steps agree.**

### 2. Draft 15's two blocks, accepted in full

**Codex was right on both and my Draft 14 was wrong on both.**

His first block killed my endpoint-containment clock chooser. The specific sentence that failed was mine: *"under one bin it escapes both and moves nothing a 60 s grid can see."* That conflated **the total extent differing by less than one bin** with **each spike moving less than one bin**, and those are not the same statement once the error is a scale rather than an offset — an affine compression accumulates along the recording, so it can leave the bin count untouched while moving spikes across internal boundaries, which changes bin medians, the window excursion and the permutation pool alike. Endpoints that need not reach the recording boundaries cannot separate that case, and equal bin counts were never evidence.

His replacement removes the inference rather than bounding it: DANDI 000409's own conversion repository (`catalystneuro/IBL-to-nwb`, pinned commit `54030ac4…`) aligns raw AP samples with `SpikeSortingLoader.samples2times` and exports IBL `spikes.times` unchanged, and the sorting documentation defines that field as seconds from session start. So the grid anchors at session zero, its extent is `t_last_s`, and `duration_s` is a span rather than a rival clock. Containment survives as a consistency check with no inferential job.

His second block killed my median-residual coordinate check on the same logic one level up — a median near zero constrains location and nothing else. His replacement is better than my proposal because it removes the second coordinate entirely: band membership uses `max_electrode -> rel_y`, which is the coordinate the band's bounds are already written in.

### 3. Finding A — the unit set was never pinned, and the reading decides rank 9 by construction

§16.4 selects units by `max_electrode -> rel_y` inside the CA1 band and calls it the same membership rule `screen_injection_placement.py` used for §10's native band yields. **That is true of the rule and silent on the filter.** The processed units table carries `kilosort2_label`; §10 reported band counts both ways; §10.3 gave the two columns explicitly different interpretive jobs. Nothing in §16 said which set the drift gate consumes.

Measured from the already-downloaded `injection_placement_CA1.json`, across the thirteen pinned candidates: **22 to 267 band units, but only 1 to 60 labelled `good`, and six of the thirteen hold 13 or fewer.** NYU-39 Probe00 — rank 9 — holds exactly **one**. §16.7 requires five included units in *every* complete bin, so under a `good`-only reading rank 9 is unmeasurable before a spike is read, and five further candidates enter with 8 to 13 against a floor of five, before the inclusion rule has removed anything.

That would have disqualified rank 9 through the drift gate for exactly the yield reason **§10.4 deliberately declined to gate on**, and it would have done it silently, in a session that thought it was measuring drift.

Draft 16 pins the set **label-blind**, in §16.4 point 1 and as a new row in §16.7's parameter table. The reason is step 5's own: real probe movement is common to every unit in the band while depth-estimation noise and unit-specific instability are not, so the across-unit median is sharpened by more contributors; and §16.7's inclusion rule (≥10 spikes in ≥80% of bins) already removes the units that cannot carry a displacement, on the property the quantity needs rather than on a sorter's confidence in a cluster. **The choice cannot smuggle a pass in the other direction, and that argument is stated rather than asserted:** the null is built from the same unit set, so whatever extra depth scatter the weaker units carry widens `Q95_null`, and the pass rule requires `Q95_null <= L` as well as `Delta_10 <= L`. The reader now reports both counts so composition stays auditable.

### 4. Finding B — the session-zero anchor creates a head partial bin, and only the tail was named

Anchoring at `t = 0` and discarding the final partial bin leaves the same situation unhandled at the other end wherever the AP stream starts after session zero: bin 0 spans a full 60 s of clock but less than 60 s of recording, for exactly the reason the tail bin is discarded.

On the pinned candidates this is confined to **rank 1**, whose Probe01 stream begins at `t_first_s = 1.138 s` — its first bin holds 58.86 s of data, 1.9% of one bin out of 72. Five candidate series begin at exactly zero; the remaining seven within `6.4e-5` s of it.

This is small and I have not inflated it: it changes no rule and no number. Draft 16 **retains** the bin and states the argument for retaining it — proportionally fewer spikes make bin 0's medians noisier, which can only widen the observed excursion, and since the null runs over the same bins and counts it widens `Q95_null` alongside, so both numbers in the pass rule move toward rejection and neither toward a pass. What was missing was the record, so the reader now reports `head_partial_s = max(t_first_s, 0)` beside `discarded_s`, and reports how many loaded spikes fall before the grid origin instead of letting `searchsorted` drop them silently (one to two samples' worth on the seven negative series).

### 5. Finding C — containment's resolution was unstated, and the candidate timebases are built two different ways

Draft 15 is right that containment is a consistency check rather than a clock chooser. What it did not say is **how much disagreement containment can miss** — and that is the number a reader needs. It can only catch a mismatch large enough to push the earliest or latest loaded spike outside `[t_first_s, t_last_s]`, so its resolution is exactly the two end margins, and on a real recording neither is zero. Draft 16 requires both reported with the verdict.

I then checked whether that mattered on our actual candidates. It does, in a way worth recording. Computing `(n - 1) / 30000` and the implied sample interval for all twenty-one recorded AP series in `host_timing_index.jsonl` — a file on disk since Session 15 that nobody had compared against the nominal clock — splits them cleanly:

- **Five candidate series are exactly nominal:** `t_first_s` exactly `0.0` and `t_last_s` exactly `(n - 1) / 30000` to the last representable bit, implied interval nominal to twelve decimal places. All five are CSHL Probe00, at ranks **3, 6, 8, 10 and 11**. These arrays are indistinguishable from `arange(n) / 30000`.
- **The other eight carry a fitted alignment:** non-zero offset, and a sample interval departing from nominal by up to about `1e-5` relative — between **0.5 and 49 ms** accumulated across a full run. **Rank 1 is in this group**, at `+1.138489` s and a rate ratio of `0.9999987`, or `-5.8` ms over its run.

**This does not contradict the conversion provenance, and I did not treat it as if it did.** An identity alignment is still an alignment, and tens of milliseconds sit far inside a 60 s bin. What it establishes is that the pinned session clock is a claim about the *converter* rather than a uniform property of the *recorded arrays*, and that the exactly-nominal series are precisely where containment has the least to say. The reported margins are what make that visible on the candidate actually being measured — with no new parameter and no new tolerance.

### 6. Handoff, chat and ledger

- Appended my review turn to `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`. Verified the append by reading it back: the prior 161,800 bytes are byte-identical as a prefix, exactly one Claude Session 21 header exists, the file still decodes as strict UTF-8, and its genuinely mixed line endings (107 CRLF, rest LF) are unchanged.
- Added two entries to `agents/Claude/references.md`: the IBL-to-nwb converter provenance — recorded **with the boundary that I accepted Codex's reading rather than fetching the repository myself** — and this session's own nominal-clock measurement.
- Live-Run README heartbeat: added one running-log entry at the Accessible-Piece bar covering Finding A with the two smaller repairs, and left the banner date unchanged because it already reads 2026-08-14.

---

## Challenges, decisions and reasoning

**The pull to approve, and what resisted it.** Draft 15's two repairs are better than the things they replaced, and I agreed with both before I finished reading them. That is exactly the state in which an owner re-review turns into a rubber stamp. The question I ran instead — for each edit, what does this rule now *eat*, and is all of it pinned? — is what produced all three findings. That has now been the productive question four sessions running.

**Finding A is a decision about failure semantics wearing the clothes of a definition.** "The units in the band" reads like a description. It is actually a policy about which candidates get to be measured at all, because the five-units-per-bin validity rule converts a sparse unit set into an *unmeasurable rejection*, and under §15's first-admissible rule an unmeasurable rejection advances the pinned order irrecoverably. This is the same shape as Sessions 19 and 20's findings and the reason I now check what a rule consumes before approving it.

**I chose the label-blind direction rather than leaving it to the implementer, and I did not choose it on convenience.** The deciding argument is that the failure mode label-blindness could introduce — weak units diluting a real common movement — is the exact failure the permutation null is built to detect, because dilution requires those units to be scattered and scatter widens `Q95_null`, which the candidate must also clear. That makes the choice safe rather than merely convenient, and it is written into the document as an argument rather than an assertion.

**Finding B is deliberately reported small.** 1.9% of one bin in 72 is not a result and I did not dress it as one. Its value is that the document's stated reason for discarding the tail bin applied at the head too, on the exact series ranked first, and nothing said so. Inflating that would be its own dishonesty; omitting it would leave the same class of gap the last three sessions were spent closing.

**On the round-trip count, named rather than left to accumulate.** §16 has now been open across three review turns and I have added findings on each. None of this session's three disputes Draft 15, so nothing here meets the playbook's escalation bar — but I said so in the chat rather than letting the section quietly become permanent. If Draft 16 comes back approved, the archive-reading CLI is the next thing I write.

---

## Insights worth carrying

1. **A repair can be wrong in the mirror image of the defect it repairs** (Session 20) has a sequel: *and the correct repair can still leave the rule eating something else.* Draft 15 fixed the clock and the coordinate correctly, and the unit set was sitting underneath both, unpinned the whole time.
2. **"Which units" is a failure-semantics decision, not a definition**, whenever a validity rule can convert a small set into a rejection.
3. **A file on disk for six sessions can still hold an unread finding.** `host_timing_index.jsonl` has been tracked since Session 15; nobody had divided `t_last_s` by the nominal clock until this session. Third consecutive session in which the answer was already downloaded.
4. **State a check's resolution, not just its role.** Draft 15 correctly said containment is a sanity check. A sanity check whose sensitivity is unstated is still an unpinned input.
5. **When you accept a reviewer's source second-hand, record that you did.** The converter provenance is load-bearing for the whole bin grid and I did not fetch it myself; the references entry says so.

---

## Files created or updated

| Path | Change |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 16** — label-blind unit set (§16.4 point 1, §16.7 table row, new justification paragraph), head-partial-bin naming and reporting (§16.4), containment-resolution paragraph with the measured timebase split (§16.4), expanded reader reporting list (§16.8). Status line rewritten. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only: acceptance of Draft 15's two repairs, the three findings, explicit Draft 16 approval and handoff. |
| `agents/Claude/references.md` | Two new entries: IBL-to-nwb converter provenance (second-hand, boundary stated) and the nominal-clock measurement. |
| `README.md` | One running-log entry at the Accessible-Piece bar. Banner unchanged. |
| `agents/Claude/Session Summaries/HumanReport21.md` | This report. |
| `agents/Claude/README.md` | Workspace map refreshed. |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten for Claude Session 22. |

No count- or event-triggered progress report was due; the next count-based one is Claude Session 24.

---

## Machine state

Measured at 2026-08-14 03:15 PDT: **RAM 6.79 GiB free of 31.67; VRAM 1,089 MiB used of 16,311; 583.1 GB free on `C:`.** Nothing heavy ran and nothing heavy was planned; the session's only compute was three stdlib/numpy validation runs and offline reads of already-cached JSON. The reading is recorded so the next session inherits evidence rather than a hunch, and it must not be inherited as a number.

---

## Next steps

1. **Codex re-reviews Draft 16** at `7fed750c8f48420521e2038b32285d72d7b719dfd1490c40dbccc14a6e2204ec`. §16 stays open until both approvals name the same state; no candidate is read meanwhile.
2. **On approval, I write the archive-reading drift CLI** — packet step 11 — against Draft 16: targeted range reads over the ragged `spike_times` and `spike_distances_from_probe_tip_um` slices for band units only, reusing `utils/remote_hdf5` and `utils/host_anatomy`, calling `utils/band_drift`, reporting bytes and requests, and discharging §16.8's four pre-computation confirmations plus the new reporting fields before it computes anything.
3. Only then may rank 1 be measured on drift.
4. Still open and unchanged: the noise and post-rescaling effective-SNR gates; the capacity gate under Amendment 6's stricter joint-ten-placement condition; Codex's footprint/placement calibration, schedule/placement specification, matcher implementation and balance/manipulation gate; Rung 0; and the five packet steps that have not been re-run.
