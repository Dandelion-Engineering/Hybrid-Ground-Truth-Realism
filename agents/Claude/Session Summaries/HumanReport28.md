# Human Report — Claude Session 28

**Current date and time:** 2026-08-15 05:49 PDT
**Phase:** 2 — Execution
**Session type:** Owner response to a review that came back with five blockers

---

## What this session was

Last session I handed Codex a new candidate for review: the command that reads a
real recording out of the archive and turns it into a drift verdict — the piece
that decides which recording this whole experiment runs on. His Round 1 came
back **`Revisions Required`** with five blocking findings and one tracked
follow-up, and he wrote an independent probe that reproduced all seven of his
constructions.

This session is the response. **I accepted all six findings in full and disputed
none of them.** Before editing anything I ran his probe against the unchanged
candidate: seven of seven reproduced on this machine. Every one of his findings
was real.

The short version of what he found: my code checked the *shape* of the archive's
data carefully and its *type* not at all, so an index value of 450.75 was quietly
rounded to 450 and became a well-formed answer; two files from two different
animals were accepted as one recording because their session identifiers
matched; a clock that covered only 999 of its recording's 1,000 samples supplied
the recording's length anyway; a byte budget I described as exact measured the
smallest of the three quantities it could have measured; and one adjustable
setting was still adjustable that should not have been.

---

## What was accomplished

### The five blockers, and what each repair is

**F1 — the cost ceiling did not bound the cost.** I had one number, called
`bytes`, which was how much the spike data occupies inside the file. The reader
fetches the file in fixed-size blocks over the network, so a small scattered
read can cost a whole block; and the arrays are widened to 64-bit floats once in
memory. Codex demonstrated a plan of 57,600 bytes passing a 60,000-byte ceiling
and then transferring 81,360.

There are now **three numbers**, because they are three questions: the stored
payload (exact), an upper bound on the network transfer, and the peak memory
(exact). The ceiling is enforced against **both** of the two that can bind, and
the refusal says which one did. The key called `bytes` is gone rather than
redefined — a key named `bytes` that means one of three things is the defect,
not the name.

The transfer bound is computed from what the file says about itself: where the
columns physically sit when it will say, rounded out to whole chunks when they
are chunked, placed at the worst alignment the block grid allows when the
position is unknown, and capped at the file's own size. It is honest about being
a bound rather than a measurement, including in the report, and it names the one
thing it deliberately does not cover — a network request that fails and retries
re-fetches its block.

**F2 — the structure was converted before it was checked.** Python's `int()`
accepts a float and truncates it. So two boundary offsets 0.75 apart became one
partition, and a fractional electrode reference became a real electrode. Both
reached passing verdicts in Codex's fixtures. The values are now validated as
stored: an integer type passes; a float type passes only if every value is
finite and whole, and the stored type is then reported rather than swallowed;
anything else stops the command by name. Every one-value-per-unit column is also
length-checked, not just the two he named.

**F3 — the two files and the clock were not authenticated.** The command now
requires the raw and processed assets to name the same animal and the same
paired file stem, and requires the timestamp vector to cover the data array
before it accepts the recording's end time as the measurement grid's length.
This is the project's own specification being implemented rather than a new
requirement: section 16.8 asks for "the exact raw and processed assets" to
satisfy a common session clock.

**F4 — a settable number could change which neurons were graded.** I had removed
the ability to type a drift threshold, and left in place a `--max-gap-um` that
decides how far apart two labelled patches of brain tissue can be and still
count as one band. Codex set it to 1000 and merged two separate CA1 islands
across the CA3 rows between them, quietly admitting eight neurons from the wrong
structure — and got a pass. It is now pinned at the 40 µm the selection document
declared, and cannot be typed. The test asserts both halves: the typed value is
rejected, and the same fixture measured through the library at the old value
shows exactly what it would have done.

**F5 — the command was not in the packet and could not be run.** It lived in my
own workspace and only ran because the test harness quietly supplied a path it
needed. It is now in `Reproducibility Packet/scripts/` and runs directly.

That move cost something, and I want it visible rather than buried: the packet's
consistency checker treats any script in that folder without a numbered runbook
step as a hard failure, and Codex and I both hold that the step must wait until
the command has actually been run against a recording. Both cannot hold at once
without a third thing, so the checker gained an explicit *pending* declaration —
checked, not merely exempted: a pending script must exist, must carry exactly
one worked example, and must not claim a step number it does not have. The
packet's README says in plain prose why a script is sitting there without a
step. **I wrote the rule that excuses my own file**, which is the structural
weakness of owner-written review scope that I named to Randy last session, and I
have said so to Codex directly rather than hoping he checks.

**F6 — the follow-up, taken now rather than tracked.** A failed rerun used to
leave the previous run's verdict files sitting at exactly the paths it named.
The two output paths must now differ, both are cleared before the run begins,
and the report only points at the JSON record when one was actually written.

### The part I would keep if I could keep only one thing

**A test suite written after a repair can encode the repair rather than the
property.** Every case would be green, and every case would have been green
against a subtly wrong fix. So I wrote a second harness that **removes each
repair in its own clean copy of the tree and requires the suite to notice**. All
eight mutations were caught and the unmutated control passed.

That harness immediately found something about my own suite that made its totals
less trustworthy than they looked: **a test case that raised an exception used to
abort the whole run**, so the printed total described a smaller suite than the
one that was asked for. A raise is now recorded as a failed check named after
its case, with its traceback, and the run continues.

---

## Challenges, and how they were resolved

**The transfer bound has no tight honest form.** I wanted an exact number and
cannot have one: whether the archive's columns are stored contiguously or in
compressed chunks is not knowable until a real file is opened, and the two cases
have very different costs. I chose a bound that is valid in both and can be
loose in one, and made the plan report the layout facts that explain why it is
loose. A bound that refuses a feasible read is recoverable — the operator raises
the ceiling deliberately after looking at the numbers — while a ceiling that
admits an infeasible read is what F1 was.

**Two numbers in the same report that a reader will compare.** Rendering a
report and reading it as a reviewer — the pass that has produced the last
several sessions' final corrections — showed the transfer bound sitting a few
lines below the total archive transfer, with nothing saying they measure
different things. The bound covers one of the three reads. The report now says
which line to compare it against.

**A timestamp written before the clock was read.** My handoff message's header
said 05:50 PDT when the clock said 05:46. The transcript is append-only, so I
appended the correction rather than editing the header.

---

## Decisions I made that a reviewer should check

1. **A float column whose values are all exactly whole is accepted, not
   rejected**, with its stored type reported. NWB does not require the integer
   type, and an exact whole number is unambiguous about which row it names; what
   was wrong was accepting it *silently*. Codex may overrule this into a hard
   stop and I have said so.
2. **`--target` is still free while `--max-gap-um` is now pinned.** The gap has
   one declared value; the target zone (CA1) is governed by the Claim Sheet and
   is recorded in every report, so changing it is a visible scientific decision
   rather than a knob.
3. **The checker's pending mechanism is new machinery in an approved packet
   script.** It is the smallest thing that lets F5 and the deferred step both
   hold, and it is in scope for Codex's next pass.

---

## Files created or updated

**Moved and repaired**

- `Reproducibility Packet/scripts/measure_host_drift.py` — moved here from
  `agents/Claude/tools/`; F3, F4, F5, F6 repairs and the new report contents.
  SHA-256 `7f99419ee202dd189d9f7a96d36d6d73c31723b5da21ee34cbe889d80c8ca2d5`.
- `Reproducibility Packet/scripts/utils/archive_units.py` — F1 and F2 repairs.
  SHA-256 `19dbcc765cd5a64b41d370c642c318055cfe619cd5d4beb40dc0b69ccac132ea`.
- `agents/Claude/tools/test_measure_host_drift.py` — 17 new cases, a
  block-caching fixture reader, and the crash-is-a-failure fix. 231 checks.
  SHA-256 `ad4985cb83eaa6be135d4e0db88785cfb4aeeb20cd4de03c131aae1c81d5a798`.

**New**

- `agents/Claude/tools/mutate_rc002_repairs.py` — removes each repair in a clean
  copy and requires the suite to notice. SHA-256
  `89785076ffb4856264b761d523a2b897341bc2024b63fa7803bcb4bf4e6f1b12`.

**Changed as a consequence of F5**

- `Reproducibility Packet/scripts/check_runbook_consistency.py` — the checked
  `PENDING_STEP` declaration.
- `Reproducibility Packet/README.md` — the prose section explaining it.

**Record**

- `Review Cards/RC-002 Archive-Reading Drift Command.md` — Round 2 state,
  round log, acceptance evidence, follow-up status.
- `Review Cards/README.md` — index row.
- `chats/Claude-Codex/Archive-Reading Drift Command Review/…Active.md` — the
  Round 2 handoff, appended.
- `README.md` (root) — running-log entry 54.
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`.

**Unchanged, and verified unchanged:** the selection document
(`c35987fe…`), `band_drift.py` (`eace4cd3…`), `test_band_drift.py`
(`946df906…`), and both Claim Sheets.

---

## Evidence

| Test | Result |
|---|---|
| `test_measure_host_drift.py` | **231 checks, 0 failed, 14.1 s** |
| `mutate_rc002_repairs.py --repo-root .` | **8 of 8 repairs caught, control green** |
| `test_band_drift.py` | 103 checks, 0 failed |
| `probe_band_drift_claims.py` | 3 of 3 |
| Codex's `probe_rc001_round1.py --repo-root .` | 0 failures |
| Codex's `probe_draft16_safety_claims.py --repo-root .` | digits unchanged |
| Codex's `probe_rc002_round1.py` | 7 of 7 before the repairs; four now fail and the fifth raises, which is the repair |
| `check_runbook_consistency.py` | 10 steps agree, 1 pending |
| `mutation_test_runbook_checker.py` | 15 of 15, control green |
| Compilation / ASCII / CR bytes | clean on all five files |

**Machine readings.** 05:06 PDT: 0.28 GiB free physical RAM against 7.60 GiB
available including standby, VRAM 1,083 of 16,311 MiB used, `C:` 589 GB free.
The first figure is why the rule says to measure rather than inherit — a
momentary reading during process startup, with the reclaimable figure ten times
larger. This session's whole compute was small local HDF5 fixtures and a numpy
harness needing tens of megabytes, and the mutation harness runs nine copies of
the suite in sequence rather than in parallel for the same reason.

---

## What is still not done

**No archive was read. No candidate was measured. No host is pinned. No
scientific result exists.** Reading the first candidate — CSHL047 Probe01 — is
still gated on RC-002 closing `Approved`.

Everything else in the standing list is unchanged: the capacity gate still needs
re-establishing under Amendment 6's stricter condition, five of the packet's ten
steps have not been re-run, the preprocessing half of the amplitude question is
untouched, and the 66 unmapped host long names remain a licence question rather
than a coding one.

---

## Next steps

1. **Codex's delta-only Round 2** against F1–F6 and against the three states
   this response added.
2. If it closes `Approved`: `--plan-only` on rank 1, measure free memory against
   that exact number, then the first real candidate measurement.
3. If it does not: this is round two of three, and the Convergence Decision
   exists so that a third round is the end of it either way.
