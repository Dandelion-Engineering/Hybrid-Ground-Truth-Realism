# Claude Human Report — Session 33

**Date and time:** 2026-08-16 03:30 PDT

**Phase:** Phase 2 — Execution

**Outcome:** The first real candidate command was run. It stopped on a rule added
two sessions ago. Measuring that rule against the dataset shows it admits **0 of
71** sessions, so no host could ever have been pinned while it stood — and the
same measurement found a genuine one-hour clock disagreement on **8 of 71**
sessions that the rule is structurally blind to. The evidence and a proposed
replacement are open to Codex. **No approved code was changed.**

---

## Startup

The automation gate named Claude, no `.agent-session.lock` existed, I created one
and re-read `.agent-turn`, which still named Claude. I then followed
`AgentPrompt.md`: Project Details, my continuity file, every chat summary, the
one active transcript, Codex's Session 32 human report, and the concluded RC-003
transcript.

**RC-003 closed `Approved` at Round 3** while I was away — Codex authenticated
and approved the exact nine-file state I approved, with no Convergence Decision.
I verified the four digests I depend on are unchanged on disk and the worktree
was clean at his commit `51cb436`. That approval was the gate on candidate
measurement, so the pinned next step was reachable.

Nothing in the one active chat (`Review Method Change`) required a reply. I
posted a method observation there at the end of the session instead.

---

## What I did

### 1. The first real candidate read — and it stopped

Machine measured immediately before: **15,262 MB free physical of 32,425;
27,298 MB committed of a 130,415 MB limit.** The read is metadata-only, so this
was headroom checking rather than a constraint.

`--plan-only`, rank 1, CSHL047 Probe01, session
`b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`, run from inside the
packet folder. It got further than I expected and then stopped cleanly:

- raw conversion provenance read and authenticated: `Created using NeuroConv
  v0.9.2`, **22,104 request bytes against a 65,536 budget and 262,144 transfer
  bytes against 327,680** — the two budgets built last session, working on a real
  asset for the first time
- CA1 band derived from the raw electrode table: **320.0–1020.0 µm, 72 channels**
- AP extent read: **`t_first 1.138489 s`, `t_last 4340.732689 s`** — matching the
  recorded timing index exactly, which is the first independent confirmation of a
  number this project has been carrying since Session 15
- then: **`[fatal] input error` — raw states conversion version 0.9.2, processed
  states 0.9.4.**

That is the rule Codex's Round-2 F1 finding produced and that I implemented at
Session 32, doing precisely what it was written to do. My own continuity note
said that if it fired on a real candidate, that is evidence rather than a bug,
and the rule should be amended rather than loosened in place. So I measured it.

### 2. Measuring the rule against the dataset

I wrote `agents/Claude/tools/probe_conversion_pairs.py`, which reads from both
halves of a named session and nothing else: the four provenance paths the archive
reader already declares, under that module's own request and transfer budgets;
and, under a second declared budget, the NWB root values that state the clock
directly — `/session_start_time`, `/timestamps_reference_time`,
`/general/session_id`, and the root `nwb_version` attribute. **No payload, no
electrode table, no spike times.** 74,186,752 bytes in 1,132 requests for
everything below, about a megabyte per session pair.

Two sets, and the second was drawn specifically to test the hypothesis the first
suggested:

- **The eleven distinct sessions of the pinned host order** (ranks 1–13; two
  sessions appear twice under two probes).
- **A deterministic sixty-session sample of the other 448 paired sessions**, rank
  = SHA-256 of a pinned seed plus the session UUID, ascending hex, **excluding
  the eleven the hypothesis came from.**

**Result 1 — the version pair is uniform, and uniformly unequal.** Every raw
asset was written by NeuroConv 0.9.1 (1 of 71) or 0.9.2 (70 of 71); every
processed asset by 0.9.4. **Version agreement holds on 0 of 71 sessions.** The
gate is not a filter that happened to reject rank 1. There is no candidate
anywhere in DANDI 000409 it can pass.

**Result 2 — the property the rule stood in for is directly readable, and it
behaves differently.** The NWB format defines `timestamps_reference_time` as the
instant every time value in the file is counted from. Across the 71 sessions,
`processed − raw` on that value is either **`+0.0 s` (63 sessions)** or
**`+3600.0 s` (8 sessions)**. Nothing else — never another magnitude, never the
other sign, never a different declared UTC offset between the two halves.
`session_start_time` equals `timestamps_reference_time` on all **142** assets.

**Result 3 — the eight are not scattered.** Cross-tabulated against the raw
asset's declared offset:

| raw offset | agrees | differs |
|---|---|---|
| UTC−08:00 | 5 | 0 |
| UTC−07:00 | 11 | 0 |
| UTC−05:00 | 14 | 0 |
| **UTC−04:00** | **5** | **8** |
| UTC+00:00 | 15 | 0 |
| UTC+01:00 | 13 | 0 |

All eight are NYU subjects whose declared local time falls inside the US-Eastern
daylight window. The two NYU sessions read at −05:00 agree; the five non-NYU
sessions at −04:00 agree. Perfect separation on 71 sessions. Four of them are
pinned candidates: ranks **5, 7, 9 and 13** — NYU-65, NYU-45, NYU-39, NYU-48.

**I am describing that pattern and not explaining it.** A daylight-saving
handling difference between the two conversion passes fits every number, but I
did not measure a mechanism and nothing I write claims one.

### 3. What I proposed, and what I deliberately did not do

Opened `chats/Claude-Codex/Session Clock Agreement/` with the full measurement
and this proposal:

- **Keep** per-asset authentication of the whole conversion statement unchanged —
  that is Codex's finding and it is right — with `0.9.4` now recorded beside
  `0.9.1`/`0.9.2` as a measured value on processed assets.
- **Replace** the pair's converter-version equality with equality of the declared
  reference *instant*, compared as instants rather than strings.
- **Disposition unchanged:** a disagreement is an input error under §16.4 — the
  candidate **pauses**, it is not rejected, and the pinned order does not advance
  past it.
- Ranks 1, 2, 3, 4, 6, 8, 10, 11, 12 would pass; ranks 5, 7, 9, 13 would pause.
  Rank 1 passes, so the first real measurement becomes reachable.

**I did not touch `archive_units.py` or `measure_host_drift.py`.** Both are at the
digests Codex approved hours earlier. The rule I would be changing exists because
of a blocker he raised, the evidence for changing it did not exist during his
review, and one agent should not both discover an input error and decide its
disposition. I proposed RC-004 scoped to the pair condition, owned by me,
reviewed by him.

---

## Challenges, and how they were handled

**The probe's first run left four of eleven processed assets undetermined.** I had
reused the archive reader's own provenance budget for the clock paths, and
reaching a root value in those four files cost a single 61,440-byte structural
read that did not fit in what the scope had left. **An undetermined value is not a
null result here** — it is the absence of the measurement, and the four unread
were four of the seven that would decide the pattern. I gave the clock scope its
own declared budget, re-ran, and all eleven became determinate. Three of the four
newly-read sessions changed the picture: NYU-12 and NYU-37 turned out to *agree*,
and NYU-65 turned out to *disagree*. Had I published the first run's table I would
have published a pattern that was wrong in both directions.

**The hypothesis came from the same data that suggested it.** The eleven pinned
sessions are where I noticed the one-hour shift. Testing it there would have been
circular, so the sixty-session sample explicitly excludes them and is drawn by a
fixed reproducible rule rather than chosen. The separation held on fresh data.

**My first framing of the pattern was too coarse and the data corrected it.** I
initially read it as "sessions in the daylight window disagree." The
cross-tabulation shows five sessions at −04:00 that agree, all non-NYU. The
honest statement is narrower and I wrote the narrower one.

---

## Decisions I made

1. **Measure the rule rather than repair it.** The one-line fix was to drop the
   version condition. Doing that would have produced a working command and no
   knowledge. The measurement is what establishes that the rule admits nothing —
   which is a much stronger reason than "it blocked my candidate" — and what
   found the eight-session defect the version rule cannot see.
2. **Draw the test sample deterministically and exclude the training set.**
3. **Do not read payload on an affected candidate this session.** Whether the
   eight sessions' stored *numbers* disagree, or only their declared labels, is
   cheaply testable — the raw AP extent against the processed spike-time range —
   and it decides whether those four candidates are recoverable. It is also a
   payload read on a candidate the command currently refuses. I put the question
   and the method in Codex's hands rather than answering it unilaterally in the
   session that raised it.
4. **Pause, never reject.** §15's first-admissible rule means a candidate rejected
   for the wrong reason hands the host to the next rank irrecoverably. Nothing in
   this session grades any candidate.

---

## Insights worth carrying

1. **A gate that has never been run against real inputs has never been tested.**
   This one was reviewed across three rounds by two agents, defended by 26
   mutations, and passed 382 checks — and it admits nothing in the only dataset it
   will ever see. Every one of those checks ran on fixtures we wrote. **A mutation
   harness proves a check depends on its repair; it cannot tell you the check's
   population is empty.**
2. **A proxy fails in two directions, and the second is the dangerous one.** The
   version rule is too strict — 0 of 71 — and simultaneously blind: the eight
   defective sessions carry the same version pair as the sixty-three sound ones.
   **When a check stands in for a property, ask what it admits and what it rejects
   on the real population, not whether it is conservative.**
3. **Evidence drawn from one half of a paired object says nothing about the
   pair.** `MEASURED_CONVERSION_VERSIONS` came from 21 raw assets in Session 7. No
   processed asset's `source_script` had ever been read, by either agent, in
   thirty-two sessions — and the rule that compared the two halves was written
   from it anyway.
4. **An undetermined value is a missing measurement, not a negative one.** Four
   unread cells nearly became four implicit "no data" entries in a table whose
   whole point was the pattern across cells.
5. **Read what the format says the number means.** The version string is metadata
   about the software; `timestamps_reference_time` is the coordinate itself. The
   project has now made the same class of substitution three times — counted for
   refused, requested for transferred, and now version for instant.

---

## Files created or updated

**Created**

- `agents/Claude/tools/probe_conversion_pairs.py` — the bounded probe
  (`10ad5053a06ba35d32d17540a6511f459e2e6f72cd3fcbe613bbdc9af10873ec`)
- `agents/Claude/tools/conversion_pairs_pinned_2026-08-16.txt` / `.json` — the
  pinned-order evidence
- `agents/Claude/tools/conversion_pairs_sample60_2026-08-16.txt` / `.json` — the
  sixty-session test sample
- `agents/Claude/tools/conversion_pairs_sessions_pinned.txt` /
  `conversion_pairs_sessions_sample60.txt` — the recorded inputs, so both runs
  are reproducible
- `chats/Claude-Codex/Session Clock Agreement/Session Clock Agreement - Active.md`

**Updated**

- `agents/Claude/references.md` — two entries: the NWB format's definition of
  what a timestamp is counted from, and this project's own 71-session census
- `README.md` — one running-log entry (64 dated entries)
- `chats/Claude-Codex-Human/Review Method Change/…Active.md` — one method
  observation
- `agents/Claude/README.md`, `Summary of Only Necessary Context.md` — closeout

**Deliberately unchanged:** `Reproducibility Packet/scripts/utils/archive_units.py`,
`Reproducibility Packet/scripts/measure_host_drift.py`, and every other file in
RC-003's approved state.

---

## Next steps

1. **Codex's answer on the proposal** — accept the measurement, accept that
   pair-version equality has to go, and settle who writes RC-004.
2. **The containment diagnostic on one affected session** (NYU-65), if he agrees
   it is in scope. It decides whether the four paused candidates are recoverable
   or permanently out.
3. **Then rank 1's real measurement**, which is otherwise ready: `--plan-only`
   already reaches the processed read, and the four things to watch are recorded
   in my continuity file.
4. **Still open and unchanged:** the capacity gate under Amendment 6, the five
   packet steps not yet re-run, the preprocessing half of the amplitude question,
   the 66 unmapped host long names.

**Boundary.** No host is pinned. No candidate has a drift, noise or effective-SNR
value. No donor is selected, no generator or sorter has run, and no scientific
result exists. The only candidate payload read attempted was the rank-1
`--plan-only`, which stopped before reading a single unit.
