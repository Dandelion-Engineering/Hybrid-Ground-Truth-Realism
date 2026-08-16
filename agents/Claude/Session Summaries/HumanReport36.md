# Claude Human Report — Session 36

**Date and time:** 2026-08-16 09:27 PDT

**Phase:** Phase 2 — Execution

**Outcome:** **RC-004 closed `Approved`**, and the first real drift measurement in
this project's history was attempted. It got further than anything before it — the
whole input-authentication chain passed on the real rank-1 candidate — and then
stopped on a *different* pre-declared input confirmation: one spike in 3,160,311
carries no depth value. I measured how much of that there is, on the candidate
that produced it **and** on a holdout candidate that did not, and handed a
proposed disposition to Codex without ruling on it myself.

---

## 1. What I did first, and why the order mattered

Codex had returned RC-004's Round-2 delta pass as **reviewer `Approved`** at
08:17 PDT, with a boundary correction at 08:21. Under the project's same-state
rule his approval alone does not close a card: the owner has to re-open the
artifact, genuinely re-review, and explicitly approve the *same* state. So that
was the session's first job, and I deliberately did not treat it as a formality.

**What I re-ran rather than re-read.** Codex edited no candidate file, so there
was nothing of his inside the artifact to review. What there *was* to check is
whether the state he approved is the state that exists on disk, and whether his
independent evidence reproduces here:

- All five candidate digests re-computed from disk match his table exactly, as do
  both of his probes.
- **His Round-2 probe, unmodified: 5 of 5 checks, exit 0.** Its independent census
  reconstruction reports `json=79 frozen=79 missing=0 extra=0`; every measured
  reference string is admitted; the malformed `Q` separator is refused; a ceiling
  equal to the whole file admits at 55,920 bytes; one byte short refuses with
  `scope='declared ceiling'` at `distinct_bytes=0`.
- **The acceptance suite: 472 checks, 0 failed, 16.0 s.**
- **His Round-1 probe, unmodified: reproduces neither counterexample.**

**One thing I deliberately did not do, and said so.** I did not re-run the
mutation harness. It had already run twice against these exact bytes — once by me
after the digest correction, once by Codex independently — and nothing moved in
between. Re-running an unchanged harness against unchanged bytes is not evidence,
and I would rather say that than let a number accumulate that nobody used.

**RC-004 therefore closed `Approved` at Round 2**, inside the second of the three
round-trips the method allows, with no Convergence Decision. The card, the index
row and the review chat are all updated; the chat is concluded with a `Summary.md`.

**One open question closed by his answer rather than by my silence.** I had asked
whether he wanted RC-003-F3's before-the-first-fetch property back at the command
level, at the cost of a second fixture pair. He accepted the direct-API layer as
the correct one — the command now meets the raw read first, so no whole-command
ceiling can both admit that larger read and refuse the processed asset's smaller
first fetch. The cost is not spent and the thread is closed.

## 2. The first real measurement

With the card closed, the rank-1 command was unblocked for the first time.

**`--plan-only`, and it completed.** CSHL047 / Probe01, session
`b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`:

- raw asset counts its times from `2020-01-21T13:52:24-05:00`;
- raw conversion provenance `Created using NeuroConv v0.9.2`, spending **23,488**
  request bytes of 65,536 and **262,144** transfer bytes of 393,216;
- CA1 band **320.0–1020.0 µm, 72 channels**;
- AP extent `t_first 1.138489 s`, `t_last 4340.732689 s`;
- **174 band units of 756 on the probe; 3,160,311 spikes**;
- payload 50,564,976 bytes, transfer bounded at 59,040,736, **combined peak
  resident at most 128,825,196 bytes**.

**The pair condition passes on the real candidate** — RC-004 working on the asset
that broke its predecessor.

I measured free RAM (11,721 MB) against `peak_resident_bytes` (0.12 GB) and ran
the real measurement. It stopped:

```
[fatal] input error reading ..._desc-processed_behavior+ecephys.nwb probe Probe01:
        unit 901 carries 1 non-finite spike depths
```

No verdict, no output files, exit 1. That is the correct behaviour: an input error
pauses the candidate rather than recording it as a drift failure, because the host
order is first-admissible and a rejection recorded for the wrong reason hands the
host to the next rank irrecoverably.

## 3. Why this is not a bug, and why that is the interesting part

**The code did exactly what the approved specification told it to do.** §16.8 of
the selection document lists, as its second input confirmation, *"that those
values are finite"*. `archive_units.read_band_units` enforces it and
`band_drift.unit_traces` enforces it again independently. One pre-declared rule,
two layers, both correct against the contract.

So there was nothing to repair. What is in question is **the confirmation
itself** — written in Session 17, before any candidate had been opened, and now
meeting real data for the first time.

This is the third time this project has hit the same shape, and I think it is the
most important recurring lesson in it: **a rule written from synthetic fixtures
tells you nothing about what it admits on the real population.** Session 33 found
a rule that admitted 0 of 71 sessions after surviving three review rounds and
twenty-six mutations. This is the same class, arriving one layer down.

## 4. The measurement I made instead of a decision

Session 33 left a finding I was determined to obey this time: **do not both
discover an input error and rule on its disposition in the same session.** So I
built a diagnostic instead.

`agents/Claude/tools/probe_nonfinite_depths.py`, SHA-256
`ade3660f3d744e07fae8326f04508c157f47cfbe50313079c983caacc5bb52f1`, reads the same
band the command reads and reports every non-finite value in it, plus what
dropping those samples would do to the pre-declared bin-support floors. It
computes no drift statistic and decides nothing.

**I ran it on rank 1, and then on rank 2 as a holdout** — deliberately the
candidate that had *not* produced the finding, because a rule change fitted to the
asset that suggested it is a rule change fitted to noise.

| | **rank 1** CSHL047 Probe01 | **rank 2** NYU-12 Probe01 |
|---|---|---|
| band | 320.0–1020.0 µm, 72 ch | 3180.0–3820.0 µm, 66 ch |
| complete 60 s bins | 72 | 82 |
| band units | 174 of 756 | 267 of 1,185 |
| band spikes | 3,160,311 | 4,898,466 |
| **units with non-finite depths** | **11** | **10** |
| **non-finite depths** | **231** | **222** |
| fraction of band spikes | 0.00731% | 0.00453% |
| worst single unit | 169 of 24,520 = 0.689% | 196 of 49,738 = 0.394% |
| **non-finite spike *times*** | **0** | **0** |
| NaN / +inf / −inf | 231 / 0 / 0 | 222 / 0 / 0 |
| units meeting support, keeping everything | 140 | 182 |
| units meeting support, dropping them | **140** | **182** |
| **units that lose any bin by dropping** | **0** | **0** |
| **bins lost by dropping** | **0** | **0** |
| read cost | 53 requests, 55,210,480 bytes | 64 requests, 66,771,599 bytes |

**Rank 1 was read twice by two independent archive reads and gave identical
numbers both times.**

### The four facts that matter

**(a) The rule is not discriminating between candidates — it pauses the holdout
too.** Two candidates, two pauses. I have not read the other eleven and will not
assert what they hold, but "the first two both fail on this" is the shape of the
rule that admitted 0 of 71.

**(b) All NaN, never infinite, and never in the spike *times*.** The column is
*"computed from waveform center of mass"* by its own first-party description, and
a centre of mass divides by a sum of weights. All-NaN-no-infinities is what a
degenerate `0/0` looks like rather than what a corrupt file looks like — and the
ragged index, the alignment check and every spike time are intact on both assets.
**That is a described pattern, not a measured mechanism, and the report says so.**

**(c) Dropping the affected samples costs no support at all, measured rather than
argued.** Zero bins and zero units change their inclusion status on either
candidate. And all 21 affected units across the two are *inside* the included set,
so this is not a question about units that were going to be dropped anyway.

**(d) Every affected unit on both candidates is labelled `mua`.** 0 of 32 and 0 of
60 `good` units, against 11 of 142 and 10 of 207 `mua` units — pooled chance about
0.013 at each candidate's own rate. **I recorded this and explicitly refused to use
it.** The unit set is pre-declared label-blind and §16.4 argues that at length,
including that a `good`-only reading would make rank 9 unmeasurable by
construction. Reaching for the quality label here would be re-deriving a filter
that section rejected, using a number I measured after the fact. It is in the
report because omitting a measured pattern would be the worse error.

## 5. What I proposed, and what I refused to propose

Handed to Codex in a new chat, as a proposal rather than a decision:

**Treat a non-finite *depth* as a per-sample exclusion that is counted and
published; keep a non-finite *time* as an input error; let the pre-declared
inclusion floors do the protective work.**

- A missing depth is a missing measurement for one spike. A missing *time* means
  the spike cannot be placed in the recording at all, and the ragged structure is
  not what it claims — that should still stop the run.
- The floors that protect the statistic from thin support (≥10 spikes in ≥80% of
  bins per unit, ≥5 included units per bin, any invalid bin makes the candidate
  unmeasurable) were written before any candidate was read and already govern
  exactly this failure mode.
- **Deliberately not proposed: any new tolerance.** A "pause if more than X%"
  rule would need an X chosen after seeing 0.0073% and 0.0045%, which is the error
  this project has paid for more than once. The pre-declared floors are the bound.
- The exclusion must be published per unit and in total. A silent exclusion is a
  reproducibility failure by the project's own standard.
- **The bias this admits is real and belongs in the limitation.** If the depth
  estimator fails preferentially at some depths, dropping its failures biases the
  bin median, and I cannot test that from data where the failures have no depth.
  What bounds it is the rank-and-offset bound §16.4 already states for the mirror
  case, read in the other direction — and it is small here only because the count
  is small, which is an argument about these two candidates rather than a general
  safety property.

**I also told him plainly that the opposite ruling is defensible** — keep the
confirmation as written, pause every candidate that carries one, and report that
as the honest answer — and that I would rather hear it now than after building the
alternative.

## 6. Challenges, and how they were handled

**The pull to fix it in the same session.** The obvious move was to change one
line, drop the NaNs, and get the first drift number today. Session 33's finding
exists precisely to stop that, and the reason is sharper here than it was there:
the change is a *loosening* of a safety confirmation, made by the agent who was
inconvenienced by it, on evidence that agent gathered. That is the configuration
in which a wrong call is least likely to be caught.

**Fitting to the asset that produced the finding.** Measuring only rank 1 would
have produced a rule shaped by the one recording that failed. Running the holdout
cost one extra archive read and changed the argument materially: the pattern is
not about rank 1.

**A gap in my own first measurement.** The first probe run reported bin support
only *after* dropping, which cannot show whether dropping costs anything. I
extended the probe to report both counts and re-read rank 1 rather than reasoning
that 231 spikes across 72 bins could not matter. The answer was zero, but it is
now measured.

## 7. Machine state, measured rather than inherited

- 09:06 PDT — 12,099 MB free physical of 32,425; 32,797 MB committed of 130,415.
- Before the plan-only read — 11,705 MB free; GPU 960 of 16,311 MiB used.
- Before the real read — 11,721 MB free, checked against a 0.12 GB peak-resident
  bound.
- During the reads — 11,648–11,786 MB free; the Python process held 77 MB.

Nothing this session was heavy. The largest costs were network: about 178 MB of
archive transfer across five reads, all metadata plus the two ragged band columns.
No raw voltage traces and no waveforms were read.

## 8. Files created or updated

- `Review Cards/RC-004 Session Reference Time Pair Check.md` — closed `Approved`,
  with the owner round-log row and the rewritten outcome.
- `Review Cards/README.md` — index row updated to closed.
- `chats/Claude-Codex/Session Reference Time Pair Check Review/…Active.md` →
  `…Concluded.md`, plus a new `Summary.md`.
- `chats/Claude-Codex/Non-Finite Spike Depths/Non-Finite Spike Depths - Active.md`
  — new chat carrying the finding, the measurement and the proposal.
- `agents/Claude/tools/probe_nonfinite_depths.py` — new diagnostic probe.
- `agents/Claude/tools/nonfinite_depths_CSHL047_Probe01_2026-08-16.{txt,json}` and
  `…NYU-12_Probe01_2026-08-16.{txt,json}` — its recorded outputs.
- `README.md` — running-log entry (67 dated entries).
- `agents/Claude/README.md` and `Summary of Only Necessary Context.md` — updated
  for the next session.
- `agents/Claude/Session Summaries/HumanReport36.md` — this report.

**No packet script changed.** `measure_host_drift.py` produced no report, so it
stays in the runbook checker's `PENDING_STEP` and no runbook step was added.

## 9. Next steps

1. **Codex rules on the disposition.** That is the blocking item; the pinned order
   is paused at rank 1 until it is settled.
2. **If the proposal is accepted:** implement it, write the disposition as a *new*
   section of the selection document rather than editing the closed §16, and open
   RC-005 with the implementation as the candidate — including the mirror-failure
   cases a loosening needs (dropping that takes a bin below the floor must still
   leave the candidate unmeasurable; an all-non-finite unit; a non-finite *time*
   that still stops the run).
3. **If it is rejected:** write up the pause as the result, and work out what
   evidence could recover the paused candidates — which by then would be rank 1,
   rank 2, and the four already paused on the declared-clock disagreement.
4. **Still untouched and still owned elsewhere:** the Amendment-6 capacity gate,
   Codex's footprint/placement calibration, and Rung 0.
