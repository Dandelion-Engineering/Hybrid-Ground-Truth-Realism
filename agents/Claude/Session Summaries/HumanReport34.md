# Claude — Human Report 34

**Date and time:** 2026-08-16 05:35 PDT
**Phase:** Phase 2 — Execution
**Session type:** implementation and handoff. No archive read, no candidate run, no scientific result.

---

## In one paragraph

Last session I found that the safety rule blocking the first real candidate run passes **0 of the 71 recordings** in this dataset, and proposed replacing it rather than deleting it. Codex independently re-read all 71, reproduced every number, agreed, and set six conditions the replacement had to meet before he would look at any code. **This session built it.** The rule now compares the exact instant each half of a recording says its timings are counted from, rather than the version of the conversion software that wrote it. The acceptance suite went from 382 checks to **436**, the sabotage harness from 26 mutations to **30**, and every one of Codex's six conditions has a case named against it. The candidate is handed to him for Round 1 as `RC-004` and **is not approved**; the first candidate measurement stays blocked until it is.

---

## What I did, in order

### 1. Startup and gate

`.agent-turn` named Claude and no `.agent-session.lock` existed. I created the lock, re-read `.agent-turn`, confirmed it still named Claude, and only then started project work. I then read `Project Details/Project Details.md` in full, my continuity file, `Playbooks/review-cycle.md`'s superseding method, the Review Cards template and index, both active chats, and Codex's `HumanReport33.md` — which is this session's cross-review, and which I responded to substantively in the clock chat.

**Machine, measured at 05:09 PDT before any work:** 13,525 MB free physical of 32,425; 30,227 MB committed of a 130,415 MB limit. Nothing this session was heavy — the largest thing that ran was the mutation harness, which is thirty copies of a small synthetic fixture tree, and the peak process footprint was negligible. **No archive read at all.**

### 2. What Codex had decided

He accepted the measurement — authenticating my probe by digest, independently reconstructing the 459-session sampling frame from the pinned asset cache, confirming the 60-session holdout is exactly the sixty lowest hashes under the recorded seed after removing the eleven the hypothesis came from, and replaying all 71 bounded reads. The pinned records reproduced byte for byte; the holdout reproduced every scientific value, with one asset using ten HTTP requests instead of nine for the same 589,824 bytes — a retry counter, and the entire difference.

He agreed that version equality must lose its voting role, agreed I own the repair and he reviews it, and wrote six acceptance conditions **before seeing any code**. He also refused something I had offered to do, and was right to.

### 3. The rule I built

**The condition.** Both halves of a recording must declare the same `timestamps_reference_time` — the instant the NWB format defines as the origin every stored time value is counted from — compared as *instants*, not as text.

Four things about that are deliberate and are the part worth reading:

- **Two spellings of one moment must both pass.** A local time with its offset and the same moment written in UTC are different strings and one instant. A check that compared the text would pause a recording that has no disagreement at all — the pessimistic mirror of the defect being repaired, and a real risk given that the defect being repaired was itself a check that rejected everything.
- **A missing, unreadable, malformed or timezone-less value is a problem with the input**, named per asset, not a disagreement, not an agreement, and not a verdict. A value with no timezone is refused rather than assumed local, because choosing an offset for it would invent the quantity the two halves are being compared on.
- **A real disagreement pauses the candidate rather than rejecting it.** The selection rule picks the first admissible recording in a fixed order, so a rejection recorded for the wrong reason hands the choice to the next candidate irreversibly. Four of the thirteen shortlisted candidates sit on the wrong side of this and keep their rank.
- **The old software-version comparison survives as something reported and never acted on**, and `0.9.4` joined the list of versions this project has actually measured — from 71 sessions rather than the 21 the old list came from.

**Where the value is read is itself part of the answer to one of Codex's conditions.** He required both clock reads to stay inside the declared request and transfer budgets and inside the caller's memory ceiling, with their cost represented in the published plan rather than introduced after it. I read the value inside the existing provenance call rather than in a function of its own, which puts it under the same two budgets, inside preflight, and inside the ceiling — so the whole-suite invariant that already checks every case against both budgets covers it with no new assertion.

### 4. Evidence, as run

| Check | Result |
|---|---|
| Acceptance suite | **436 checks, 0 failed, 17.6 s**, 80 cases (was 382 / 71) |
| Mutation harness | **30 of 30 caught**, control green at 436 (was 26 of 26) |
| Runbook-checker mutations | 18 of 18 |
| Packet runbook consistency | 10 steps agree; `measure_host_drift.py` still pending its first execution |
| `verify_rc003_round1_repairs.py` | exits 0 on all three constructions, untouched |
| `verify_rc003_round2_repairs.py` | exits 1 on exactly two checks, both in the construction this card removes — expected, declared, and explained below |

Five mutations are new or rewritten: remove the pair check; accept a value with no timezone; compare text instead of instants; fill in a missing value instead of refusing it; drop `0.9.4` from the measured list. Each has to make a named case go red.

**And two existing mutations had to be repaired before they meant anything.** Both replace an authentication result with a hand-written stand-in, and both stand-ins were now missing keys the new code reads — so they would have been "caught" by a crash rather than by the property they name. That is the same defect as a test that passes for the wrong reason, and it is the second session running in which the mutation harness needed fixing before its result could be trusted.

### 5. Three things I declared rather than let the reviewer discover

**A. One of my own earlier verification scripts no longer passes, by construction.** `verify_rc003_round2_repairs.py` rebuilds the reviewer's constructions from the previous review and requires each to be refused. Its second construction asserts exactly the rule this session removes. **I edited no check in it** — it is the recorded evidence for a closed review, and this project fixes things forward rather than by reopening the past. I added a dated note to the top of its documentation saying what superseded it and where that construction's forward version now lives, then ran it and reported the actual outcome: two failures, both in that construction, everything else passing. I offered to revert even the note if Codex would rather it were untouched.

**B. A path left the provenance read and a better one replaced it.** The command was reading `general/session_start_time`, which is absent from all 142 files we have read, and is now reading the root `session_start_time`, which is present on all 142 and equal to the reference time on all 142. It is recorded and gates nothing. This is a preference rather than a requirement and it is on the card as a follow-up, not as part of the repair.

**C. The comparison resolves to one microsecond**, because that is where Python's ISO-8601 parser truncates. The disagreement being detected is 3,600 seconds. I stated the resolution rather than argued it away — a check's resolution is part of what the check is, and this project has been caught before stating a check's role without its resolution.

### 6. What I did not do, and why

- **I did not run the candidate.** Approved code still carries the old rule; measuring with an unapproved state is precisely what the review method exists to prevent.
- **I did not run the diagnostic I proposed last session.** I had offered to test whether one affected recording's stored spike times are actually shifted or only its label is. Codex declined it: it is a rank-5 recording, rank 1 does not depend on it, and even if the numbers aligned, those two halves still declare different origins — so readmitting them needs its own evidence-backed rule rather than an exception smuggled inside a card scoped to something else. I accepted that and withdrew the question. **He was right, and the part I had underweighted was the second half of his reason.**
- **I did not amend the Claim Sheet.** Section 16.4 already makes an unestablished shared clock a pausing input error and never named software-version equality as its test, so the contract does not move. Both of us checked that independently.

---

## Challenges, and how they were handled

**The temptation to make the old evidence green.** The obvious tidy-up was to rewrite the superseded construction in `verify_rc003_round2_repairs.py` so everything passes. That would have quietly rewritten what a closed review established. Leaving it red and explaining why is uglier and honest, and the note points a future reader forward instead of pretending the past was different.

**Making sure the new rule can be caught being wrong in *both* directions.** The failure this whole card comes from was a check that rejected everything. It would have been easy to build a replacement that is merely less strict and equally untested against the pessimistic failure. The two-spellings-of-one-instant case exists for exactly that, and there is a mutation whose only effect is to compare text instead of instants — so if the rule ever regresses into over-refusing, a named case says so.

**A non-ASCII character in a docstring, caught by checking the printed surface.** My supersession note started with a warning emoji. This project's console is cp1252 and the script prints its own documentation under `--help`, so that would have died on a machine detail rather than on anything real. Found by scanning for non-ASCII and re-running `--help`, which is the habit this project already carries and which paid again.

---

## Files created or updated

**The candidate**
- `Reproducibility Packet/scripts/utils/archive_units.py` — the rule, the per-asset authentication, the two new helpers, the JSON-safe projection, the constants
- `Reproducibility Packet/scripts/measure_host_drift.py` — the record, the report, the new confirmation line, the rewritten explanatory paragraph
- `agents/Claude/tools/test_measure_host_drift.py` — eight cases changed or added; 436 checks
- `agents/Claude/tools/mutate_rc002_repairs.py` — five mutations added or rewritten, two repaired; 30 entries
- `agents/Claude/tools/verify_rc003_round2_repairs.py` — supersession note only; no check edited

**The review**
- `Review Cards/RC-004 Session Reference Time Pair Check.md` — new
- `Review Cards/README.md` — index row
- `chats/Claude-Codex/Session Reference Time Pair Check Review/…- Active.md` — new chat, handoff posted
- `chats/Claude-Codex/Session Clock Agreement/…- Concluded.md` + `Summary.md` — closing message posted, chat concluded

**Everything else**
- `README.md` — one running-log entry
- `agents/Claude/references.md` — two entries updated forward
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`, this report

---

## Next steps

1. **Codex's Round 1 on RC-004** — the only full-artifact pass, one numbered ledger.
2. **If it closes `Approved`: run rank 1.** CSHL047 / Probe01, `b52182e7-39f6-4914-9717-136db589706e`, `--plan-only` first, then free memory measured against the plan's combined peak before the real read. That is the first drift number this project will have.
3. **Then the runbook step**, which the command earns only by having actually been executed.
4. Tracked follow-ups: moving the 71-session census into the reproducibility packet if the rule stands; and, much later and only if the shortlist gets that far, whatever rule would be needed to recover the four paused recordings.

**Boundary, stated the same way every session.** No recording is chosen. No candidate has a drift, noise or effective-SNR value. No donor is selected, no generator or sorter has run, and no scientific result exists.
