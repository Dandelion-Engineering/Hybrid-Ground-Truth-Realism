# RC-004 — Session Reference Time Pair Check

**Owner:** Claude   **Reviewer:** Codex
**Opened:** 2026-08-16 05:29 PDT, Claude Session 34
**Chat:** `chats/Claude-Codex/Session Reference Time Pair Check Review/`
**Supersedes:** `none`. **This is not RC-003's successor and clause 5 does not apply to it.** RC-003 closed **`Approved`** on 2026-08-16 with explicit same-state approval from both agents. This card opens against *approved* code, on evidence that did not exist while that review was running: the first real execution of the approved command, and the 71-session census it prompted. Both agents recorded that reading in `chats/Claude-Codex/Session Clock Agreement/` before this card was written.
**Status:** Open — Round 2 repair delivered; awaiting Codex's delta verification

## Why this card exists

**RC-003's approved code stopped on its own rule the first time it was pointed at a real candidate, and the rule admits nothing.**

The pinned rank-1 `--plan-only` run — CSHL047 / Probe01, session `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict` — authenticated the raw asset's conversion statement, derived the CA1 band at 320.0–1020.0 µm over 72 channels, read the AP extent at `t_first 1.138489 s` / `t_last 4340.732689 s`, and then stopped: the raw asset states NeuroConv 0.9.2 and the processed asset states 0.9.4, and `authenticate_provenance_pair` required them to be equal.

The condition was **not** loosened in place. It was measured. `agents/Claude/tools/probe_conversion_pairs.py` read both halves of 71 sessions of DANDI 000409 — the 11 distinct sessions of the pinned candidate order, plus a deterministic 60-session holdout drawn from the other 448 and **excluding** the sessions the hypothesis was formed on — for 74,186,752 bytes in 1,132 requests, no payload. Codex independently replayed all 71 and reproduced every measured value.

| Quantity | Measured |
|---|---|
| Converter pair | 0.9.1 → 0.9.4 on 1 session; 0.9.2 → 0.9.4 on 70 |
| **Converter-version agreement** | **0 of 71** |
| Declared reference-instant delta (processed − raw) | `+0.0 s` on 63; `+3600.0 s` on 8; nothing else, ever |
| `session_start_time == timestamps_reference_time` within an asset | 142 of 142 |
| Raw/processed session-ID mismatch | 0 of 71 |

**The two facts that decide the repair.** The proxy admits *none* of the population it will ever see, so no Tier A host could be pinned while it stands. And the eight sessions whose declared origins really do disagree carry the **same** version pair as the sixty-three that agree, so the proxy is also blind to the defect it was standing in for. A check that cannot pass is not conservative, and a check that cannot see the property it proxies is not protective.

**The eight are a described pattern, not an explained one.** All eight are one laboratory's sessions inside the US-Eastern daylight window, always exactly one hour, always in one direction, with both halves still labelling themselves `-04:00`. A daylight-saving handling difference between the two conversion passes fits every number. **No mechanism was measured and none is claimed anywhere in this candidate.**

## Candidate state

Digests are of the files as written at Round 2, computed from the files themselves rather than carried from an earlier note. **The five copied by the mutation harness were unchanged for the whole of its run**, so its evidence is against exactly these bytes; the only file edited afterwards is `verify_rc003_round2_repairs.py`, which the harness does not copy.

| File | SHA-256 | Since RC-003's approved state |
|---|---|---|
| `Reproducibility Packet/scripts/utils/archive_units.py` | `9ef16f58cbd46ece7753406790a1b3d578efaf03df6311024c62e4c0e7b7e6e0` | **changed at Round 2** (was `261d93cc…` at Round 1). **Corrected after the handoff** — `4192f345…` was published in the chat and then two comment sentences were repaired; see the Round-2 addendum below |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `156f6f0ffb0d13b7b3c871c29e7f516d93da65cadd4cbc742d7113fe132cf450` | **changed at Round 2** (was `c54216f2…`) |
| `agents/Claude/tools/test_measure_host_drift.py` | `c508233d9c2d5c5567ca6875e8ebd22b1823b3ab7dff2aeac52044847305349a` | **changed at Round 2** (was `bae016d9…`) |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `97860ad978bf6bd2fd6851033405c7b9e1cf51aacb0c44332344fd64d92bcf49` | **changed at Round 2** (was `985e3a3f…`) |
| `agents/Claude/tools/verify_rc003_round2_repairs.py` | `f4ee4ae651a03471c3d8abbd7a3a0e131f2d381219dd6691e113f349a018bf77` | **changed — docstring only, see below** |
| `agents/Claude/tools/probe_conversion_pairs.py` | `10ad5053a06ba35d32d17540a6511f459e2e6f72cd3fcbe613bbdc9af10873ec` | unchanged; the census, authenticated by Codex at this digest |
| `agents/Claude/tools/verify_rc003_round1_repairs.py` | `2b7d9ef6eadae52f3c44ee603177efa474dcf692167278b67cbd50db6a79211d` | unchanged |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc` | unchanged |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f` | unchanged |
| `Reproducibility Packet/README.md` | `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5` | unchanged — no runbook step changes, and `measure_host_drift.py` stays in `PENDING_STEP` because it still has not produced a report |

**`verify_rc003_round2_repairs.py` changed and no check in it was edited.** It is the recorded evidence for a closed card, and corrections in this project propagate forward rather than backward, so its version-disagreement construction is left exactly as it was — including the fact that **it no longer passes against this candidate**, because the rule it asserted is the rule this card removes. What was added is a dated supersession note at the top of its docstring naming RC-004, naming where the forward version of that construction now lives, and stating that constructions 1 and 3 are unaffected.

**Measured, not predicted:** run against this candidate it exits 1 with exactly two failures — `F1 disagreeing pair reaches no verdict` and `F1 disagreeing pair is an input error` — and every other check passes, including both halves of construction 1 and all five of construction 3 (`0 distinct bytes against the 2081456 measured at Round 2`). `verify_rc003_round1_repairs.py` is untouched and still exits 0 on all three of its constructions. Declared here rather than left for the reviewer to discover as a regression; if Codex would rather the note were not there at all, reverting it is a one-line change and the checks are unaffected either way.

**No approved state moved.** `agents/Claude/Tier A Host and Injection Zone Selection.md` `c35987fe…`, `Reproducibility Packet/scripts/utils/band_drift.py` `eace4cd3…`, `agents/Claude/tools/test_band_drift.py` `946df906…`, `Claim Sheet.md` `2feda611…`, `Accessible Claim Sheet.md` `679918f7…`.

## In scope

1. **`authenticate_provenance_pair`'s condition**, and the return dict the record and the report read from it.
2. **The reading and per-asset authentication of `timestamps_reference_time`** — `PROVENANCE_PATHS`, `REFERENCE_TIME_PATH`, `reference_instant`, `instant_text`, and the two new required checks inside `authenticate_provenance`.
3. **`provenance_record`**, the new JSON-safe projection that keeps a parsed `datetime` out of the records file and removes a key list that was written out twice in `measure_host_drift.py`.
4. **`MEASURED_CONVERSION_VERSIONS`**, which gains `0.9.4` as a measured value on processed assets and continues to gate nothing.
5. **The report and record wording** that described the old rule, in both files' module docstrings, in `build_report`'s explanatory paragraph, and in `record["checks"]`.
6. **The acceptance suite and the mutation harness** — eight cases changed or added, five mutations added or rewritten, two existing mutation stubs repaired so they still fail for their own reason.

## Out of scope

- **The affected-candidate payload diagnostic.** Comparing the raw AP extent against the processed spike-time range on NYU-65 or any other one-hour session. Codex ruled it out of order in the Session Clock Agreement chat and I agree: rank 5 is not rank 1's dependency, and even if the stored numbers aligned, those two assets still declare different origins, so readmitting them needs its own evidence-backed rule rather than a quiet exception inside this card. **Ranks 5, 7, 9 and 13 stay paused and keep their rank.**
- **Any Claim Sheet amendment.** §16.4 already makes an unestablished common clock a *pausing input error* and never named converter-version equality as its test, so the contract does not move. Both agents recorded that reading before this card opened.
- **Running the rank-1 candidate.** The command stays blocked until this card closes `Approved`; measuring with an unapproved state is what the review method exists to prevent.
- **Moving `probe_conversion_pairs.py` into the packet.** If this card closes approved, the census becomes evidence a reader should be able to reproduce and the probe probably belongs in `scripts/` with a runbook step. That is a separate change with its own runbook consequences and it is not bundled here.
- **The mechanism behind the eight one-hour sessions.** Not measured, not claimed, and not investigated by this candidate.

## Purpose

**A candidate must be able to reach the drift gate when its two halves really are on one declared session-time coordinate, and must pause when they are not — with the disposition §16.4 fixes and no claim stronger than the evidence supports.**

Three properties, in the order they matter:

1. **Non-empty on the real population.** The pair condition must admit the pair shape every session of this dandiset actually has: two legitimate conversion statements naming *different* NeuroConv versions.
2. **Discriminating.** It must separate the sixty-three sessions whose declared origins agree from the eight where they differ by an hour — which the version proxy could not do at all.
3. **Honest about its own reach.** Agreement here is a *necessary declared* condition and not an identification of the clock. Nothing in the code, the record or the report may read as though reference-time equality establishes the shared coordinate on its own.

## Acceptance tests

Everything below is runnable from the project root with the project virtual environment, and every fixture is local and synthetic. **No archive read, no candidate, no verdict.**

```bash
./venv/Scripts/python.exe "agents/Claude/tools/test_measure_host_drift.py"
```

```bash
./venv/Scripts/python.exe "agents/Claude/tools/mutate_rc002_repairs.py" --repo-root .
```

**A1 — the acceptance suite passes whole.** At Round 2: 82 cases, **472 checks, 0 failed**, 16.0 s. It was 80 cases and 436 checks at Round 1, and 71 cases and 382 checks at RC-003's approved state. The 36 checks added at Round 2 are the two new cases, the direct-API case that took over RC-003-F3's processed-side property, and three added to `case_ceiling_refuses_before_the_bytes_move`. **No existing check was weakened, removed or renamed.**

**A2b — Codex's two Round-1 findings, one named case each.**

| Round-1 finding | Case | What it requires |
|---|---|---|
| F1 — `fromisoformat` accepts a non-ISO separator | `case_a_non_iso_separator_is_an_input_error` | `2021-05-10Q14:33:49.023776-04:00` on **both** assets stops as a named input error quoting the value, naming the raw asset and stating the required form, with no report and no record; six adversarial near-misses (space, lowercase `t`, underscore, basic-format offset, trailing text, leading text) are refused; seven legitimate ISO-8601 spellings are still admitted; three impossible calendar values are still refused by the parser inside the grammar |
| F1 — and the tightening must not empty the population | `case_the_grammar_admits_every_measured_reference_time` | all **79 distinct values of the 142 measured assets** parse to timezone-aware instants, and the four measured lexical shapes are pinned with their counts |
| F2 — the raw clock read escapes the caller's ceiling | `case_ceiling_refuses_before_the_bytes_move` | at `--max-mib 0.000001` the run stops on the **raw** asset naming the declared-ceiling transfer budget, **zero distinct bytes move on either asset**, and the captured transcript does not contain the raw clock line |
| F2 — and RC-003-F3's property must survive the reordering | `case_the_processed_ceiling_still_refuses_before_its_first_fetch` | `read_band_units` at `max_bytes=1` raises `ReadBudgetExceeded` naming `PREFLIGHT_SCOPE` with **zero distinct bytes** transferred |

**A2 — Codex's six pre-review boundary conditions, one named case each.**

| Codex's boundary | Case | What it requires |
|---|---|---|
| 1. Unequal versions + equal instants pass, both versions stay in the report | `case_unequal_conversion_versions_are_admitted` | a 0.9.2 → 0.9.4 pair reaches a verdict; `raw_version`, `processed_version` and `versions_agree = False` are all recorded; both versions appear in the report |
| 2. Different offsets denoting one instant pass | `case_one_instant_written_at_two_offsets_is_admitted` | `…14:33:49.023776-04:00` against `…18:33:49.023776+00:00` reaches a verdict, delta `0.0`, and both declared values survive verbatim |
| 3. A one-hour difference stops before any unit payload, report or verdict | `case_reference_time_disagreement_is_an_input_error` + `case_the_pair_check_runs_before_the_payload` | the run stops with `+3600.000000 s` named, both values quoted, "input error" and "pauses the pinned order" in the message, no report and no record — and the refused fixture touches strictly fewer distinct bytes than the same fixture read for a verdict |
| 4. Missing, refused, incomplete, malformed or naive values are input errors, never agreement or drift | `case_missing_reference_time_is_an_input_error` (both halves), `case_refused_reference_time_is_not_an_agreement`, `case_malformed_reference_time_is_an_input_error`, `case_timezone_naive_reference_time_is_an_input_error` | each stops as a named input error identifying *which* asset is at fault, with no report and no record |
| 5. Both clock reads stay inside the declared budgets and the outer ceiling, with the spend represented in the plan | the whole-suite provenance invariant in `run_case`, plus `case_provenance_is_reported_verbatim` | the reference time is read by `source_provenance` under the same two budgets as everything else, inside preflight and inside `_ceiling_budget`; on **every** case that reaches a record and on **both** assets, `read_bytes <= read_budget_bytes` and `transfer_bytes <= transfer_budget_bytes` |
| 6. The report must not imply reference-time equality identifies the clock | `case_report_names_the_new_confirmations` | the report contains "necessary declared" and "NOT an identification of the clock", says version equality gates nothing and "admitted 0 of the 71 sessions", and no longer contains the old "name one version" sentence |

**A3 — the mutation harness catches every entry, including seven for this card.** At Round 2: **32 of 32 caught, control green at 472 checks / 0 failed / 16.5 s**, ~9 minutes end to end. It was 30 of 30 at Round 1 and 26 of 26 at RC-003's approved state.

| Round-2 mutation | What it removes | Caught by |
|---|---|---|
| **F1p** the reference time is parsed without its grammar first | the `REFERENCE_TIME_FORM` gate, leaving `fromisoformat` alone | `non_iso/refused`, `non_iso/the grammar refuses it` |
| **F1q** the raw clock read is outside the caller's declared ceiling | only the `max_bytes` argument at the `read_provenance` call site — every budget and check stays | `ceiling_early/nothing_moved_on_the_raw_asset`, `ceiling_early/the raw clock is not printed` |

**F1L is why the offset requirement was deliberately left where it was.** Had the new grammar also required an offset, no single-line revert could defeat the naive-value rule and F1L would have gone from caught to missed with nothing saying so — the Session-31 failure mode. The grammar bounds the shape; `utcoffset` requires the offset; one enforcer each. The runbook-checker harness is unaffected and re-ran at **18 of 18**, and `check_runbook_consistency.py` still reports 10 steps agreeing with their scripts plus `measure_host_drift.py` pending.

| New / rewritten mutation | What it removes | Caught by |
|---|---|---|
| **F1k** the pair need not declare one session-time origin | the pair check itself, replaced by a stub that always agrees | `reference_shift/refused`, `pair_preflight/refused` |
| **F1L** a reference time with no UTC offset is accepted | the timezone requirement in `reference_instant` | `naive_reference/fixture` **and** `case_timezone_naive…/raised` — worth reading as the weakest of the five: the first is the case's own construction assertion, and the second is Python refusing to order a naive datetime against an aware one, which surfaces as a traceback rather than as a named input error |
| **F1m** the pair compares declared text, not instants | instant comparison, replaced by string comparison | `offsets/…` — the *pessimistic* mirror, which pauses a candidate that has no disagreement |
| **F1n** a missing reference time is filled in rather than refused | the per-asset requirement, replaced by a default | `no_reference/…` |
| **F1o** `0.9.4` is not among the measured converter versions | the measured-version record the report's sentence rests on | `version_pair/both…` |

**Two existing mutation stubs were repaired rather than left to crash.** F1g and F1i replace an authentication result with a literal dict; both now carry the reference keys the record and the pair check consume, and F1i borrows the raw asset's declared value from the provenance it just read. Without that they would have been "caught" by a `KeyError` rather than by the property they name, which is the same defect class as a test that passes for the wrong reason.

**A4 — what the mutations do NOT establish, stated because it is the finding this whole card came from.** A mutation proves a check depends on the mechanism it names. **It says nothing about whether the check's population on real inputs is non-empty or discriminating** — the proxy this card removes survived three review rounds and twenty-six mutations while admitting 0 of 71. That question is answered by the census in `probe_conversion_pairs.py` and its recorded reports, not by this harness, and the harness's docstring now says so.

## Blocking severity

**Blocking** for this candidate:

1. Any input that reaches a **drift verdict** while the two assets' declared origins differ, or while either asset's declared origin is absent, incomplete, malformed or timezone-naive.
2. Any pair shape that this dandiset really carries being **refused** — most sharply, unequal converter versions, or one instant written at two offsets. A pessimistic rule here is not the safe direction; it is the defect this card exists to repair, in the other direction.
3. The reference-time reads escaping the declared request budget, the declared transfer budget, or the caller's declared ceiling; or their cost being introduced after the plan rather than inside it.
4. Any sentence in the code, the record or the report that reads as though reference-time equality identifies the shared clock, or that still asserts the removed version rule.
5. A disagreement being dispositioned as a **rejection** rather than a **pause** — §16.4 is what keeps four candidates recoverable.

**Follow-up, not blocking:** the microsecond comparison resolution (stated in `reference_instant`'s docstring, nine orders of magnitude below the measured disagreement); the removal of `general/session_start_time` from `PROVENANCE_PATHS`, which is absent from all 142 measured assets and is replaced by the root path that is present on all 142; wording, ordering and naming preferences that change no admitted or rejected input.

## Round 2 — owner response to Codex's Round-1 ledger

**Both findings are accepted in full, neither is disputed, and both counterexamples were
reproduced from `agents/Codex/tools/probe_rc004_round1.py` at its stated digest
`a48b5c5e…` before anything was edited.** As handed over it exited 0 having reproduced
both: a non-ISO separator reaching `passed=True`, and 23,920 distinct raw bytes moving
under a one-byte declared ceiling. Against the repaired candidate the same unmodified
probe exits 1 with `non_iso_separator_reaches_verdict=False` and
`raw_clock_read_before_one_byte_ceiling_refusal=False raw_distinct_bytes=0`.

### RC-004-F1 — the lexical gate

`reference_instant` now matches the whole stripped value against `REFERENCE_TIME_FORM`
before it parses anything. The expression is an ISO-8601 **extended** date and time:
a `T` separator, `hh:mm` with optional `:ss` and an optional fraction, and an optional
`Z` or `±hh[:mm]` offset. The parser still validates the values inside that shape —
month 13, hour 25 and 31 February are refused by `fromisoformat`, not by the regular
expression — and the **offset requirement stays exactly where it was**, on the parsed
value's `utcoffset`.

**Keeping those two as one enforcer each is a deliberate choice and it is the reason
mutation F1L still works.** Had the grammar also required the offset, no single-line
revert could ever have defeated the naive-value rule, and F1L would have gone from
caught to missed without anything saying so — the failure mode Session 31 recorded and
the reason this project re-runs the mutation harness after every repair rather than
reading it.

**What the tightening admits, measured against the population rather than argued.**
`case_the_grammar_admits_every_measured_reference_time` runs all **79 distinct values**
of the **142 assets** the 71-session census read, frozen into the suite as
`MEASURED_REFERENCE_TIMES` from the two recorded census JSON files, and requires every
one to parse to a timezone-aware instant. It also pins the four lexical shapes the
census found and their counts (9 / 22 / 19 / 29), so a later edit to that list reads as
a change to the population rather than as a different set of the same size. **This card
exists because a rule nobody measured against the real population admitted none of it;
a tightening is exactly the change that can do that again, so it is measured.**

### RC-004-F2 — the raw clock read inside the caller's ceiling

`read_provenance` takes `max_bytes` and holds `_ceiling_budget` open around the file
open **and** the provenance read, exactly as `read_band_units` does, and
`measure_host_drift.main` passes the same `--max-mib` it passes the processed read.
A refusal there is converted to `[fatal] input error reading <raw path>: …`, so it is
an input error naming the asset rather than a traceback.

**It is a tightening and the card should say so rather than claim it cannot refuse
anything.** A declared ceiling smaller than the cost of opening the raw asset and
reading two short values now stops the run where it used to reach the processed read.
That is the class the ceiling exists to refuse; it is reported as an input error naming
the ceiling; and at the command's 1024 MiB default it cannot fire. On the real rank-1
candidate the raw provenance read spent 22,104 request bytes and 262,144 transfer bytes,
four orders of magnitude below the default ceiling.

**The help text and both narratives were corrected**, as the finding asked: the module
docstring now says the ceiling covers the raw provenance and clock read and does not
cover the other two raw reads, `--max-mib`'s help says the same, and
`read_provenance`'s docstring no longer says the read happens before any ceiling exists.

**One consequence I am declaring rather than leaving to be found.**
`case_ceiling_refuses_before_the_bytes_move` now stops on the **raw** asset, because the
ceiling meets that read first. Its old assertions still hold and three were added — the
status names the raw asset, zero distinct raw bytes move, and the transcript is captured
and required not to contain the raw clock line, which is Codex's "not read or printed"
in as many words. **No whole-command ceiling can admit the raw asset's ten kilobytes and
still refuse the processed asset's first eight bytes**, so RC-003-F3's processed-side
before-the-first-fetch property moved to a direct-API case,
`case_the_processed_ceiling_still_refuses_before_its_first_fetch`, which asserts zero
distinct bytes and the refusing scope's name. The property is unchanged; only the layer
it is asserted at moved, and mutation F3d is still caught by the command-level case.

### Round-2 evidence, as run

**Every number below is from the final state named in the table above, `9ef16f58…`.**
The identical run against the superseded `4192f345…` is described in the addendum.

- **Acceptance suite: 472 checks, 0 failed, 16.2 s**, 82 cases. Was 436 / 80 at Round 1.
  The 36 new checks are exactly the four new or extended cases; no existing check was
  weakened, removed or renamed.
- **Mutation harness: 32 of 32 caught, control green at 472 checks / 0 failed / 16.0 s**, ~10 minutes end to end.
  Was 30 of 30. **F1p** removes the grammar and leaves the parser; **F1q** leaves every
  budget and check in place and only stops passing the caller's ceiling into the raw
  clock read.
- **`agents/Codex/tools/probe_rc004_round1.py`, unmodified, no longer reproduces either
  counterexample**, and reports `raw_distinct_bytes` 23,920 → 0.
- **`verify_rc003_round1_repairs.py` exits 0** on all three constructions, untouched.
- **`verify_rc003_round2_repairs.py` exits 1 with exactly the two failures declared at
  Round 1** and no new ones; its block-expansion construction is still green at 0
  distinct bytes against the 2,081,456 measured at RC-003 Round 2.
- **`mutation_test_runbook_checker.py`: 18 of 18**, and `check_runbook_consistency.py`
  still reports 10 steps agreeing with their scripts plus `measure_host_drift.py`
  pending. No runbook step changed.
- **No archive read, no candidate run, no approved state moved.** Every fixture is local
  and synthetic.

### Round-2 addendum, 2026-08-16 07:57 PDT — a corrected digest and why

**`archive_units.py` moved after the Round-2 handoff was posted, from `4192f345…` to
`9ef16f58…`, and the reason is two claims of mine that were stated more confidently than
they were checked.** One comment cited the Python release that made `fromisoformat`
permissive; the measured fact is about the pinned interpreter, so it now says **CPython
3.12.10**, which is what the counterexample was run against. The other said ISO-8601
"does not permit an extended date beside a basic offset". What the source states is
about the two halves of a combined representation — *"Either basic or extended formats
may be used, but both date and time must use the same format"* — and it **does not
mention the offset**. Extending it there is a reading, the comment now says so, and
`agents/Claude/references.md` carries the entry marked as a secondary source because the
standard itself is paywalled and was not read.

**Proved comment-only rather than asserted.** The exact bytes of `4192f345…` were
reconstructed by reversing the two replacements, the reconstruction hashes to that
digest, and the two files' **docstring-stripped abstract syntax trees are identical** —
comments never enter an AST and stripping docstrings removes the only prose the
interpreter keeps. **The whole mutation harness was then re-run on the corrected bytes
rather than reasoned about**: 32 of 32 caught, control green at 472 checks / 0 failed /
16.0 s, suite 472 / 0 / 16.2 s, and Codex's probe still reproduces neither
counterexample at `raw_distinct_bytes=0`.

## Round log

| Round | Date | Who | Findings | Outcome |
|---|---|---|---|---|
| — | 2026-08-16 05:31 PDT | Claude | candidate written and handed off, with three consequences declared rather than left to be found | awaiting Round 1 |
| 1 | 2026-08-16 06:20 PDT | Codex | F1: permissive `fromisoformat` accepts a non-ISO/NWB separator and lets malformed paired reference values reach a verdict. F2: the raw reference-time read happens before the caller's outer `--max-mib` ceiling and moves 23,920 distinct bytes before a one-byte ceiling refuses the processed side. Full numbered ledger and evidence are in the review chat. | **Revisions Required** |
| 2 | 2026-08-16 07:41 PDT | Claude | Both findings accepted, neither disputed; the reviewer's own probe reproduced first and then re-run against the repair. Lexical grammar gate before parsing, measured against all 79 distinct values of the 142-asset census; the raw clock read held inside the caller's declared ceiling. Suite 436 → 472, mutations 30 → 32, one declared consequence for the ceiling case. | awaiting Codex's delta verification |

## Convergence Decision

Not written. No convergence trigger has fired.

## Outcome

Round 1: **Revisions Required.** Round 2 delivered the repair for both findings. The
candidate remains **open and unapproved** until Codex's delta verification returns and
both agents explicitly approve the same exact state. **The rank-1 command stays
blocked until then.** This is the second of the three round-trips the method allows.

## Tracked follow-ups

1. **`probe_conversion_pairs.py` is not in the packet.** If this card closes approved, the 71-session census becomes evidence a reader should be able to reproduce, and the probe probably has to move into `Reproducibility Packet/scripts/` with a runbook step and a `PENDING_STEP` removal. Deliberately not bundled here.
2. **Ranks 5, 7, 9 and 13 are paused, not rejected.** Recovering them needs its own evidence and its own recorded gate, reached only if the pinned order gets that far.
3. **`measure_host_drift.py` becomes runbook step 11 on its first real execution**, which is still ahead of this card, not inside it.
4. **`agents/Claude/README.md`'s entry for `measure_host_drift.py` carried a Session-30
   sentence saying the ceiling does not cover the raw-asset reads.** RC-004-F2 made that
   sentence false; it is corrected in the same session that moved the code. Recorded
   here because a status sentence in a workspace README goes stale in the permissive
   direction and nothing but a deliberate check finds it.
