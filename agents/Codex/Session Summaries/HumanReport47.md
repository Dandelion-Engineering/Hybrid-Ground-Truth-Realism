# Human Report 47 — Codex

**Date and time:** 2026-08-19 03:28 PDT

**Phase:** Phase 2 — Execution. Round-2 specification review of the host noise
gate under RC-008.

**Session outcome:** **Draft 33 returned `Revisions Required` at Round 2 and is
frozen and unapproved.** Claude's five Round-1 repairs and four tracked
dispositions reproduce on their stated numerical boundaries, but the response
created two blockers: the replacement rationale for the contiguous split
contradicts the ordered pass/unmeasurable branches, and the supposedly complete
regression authentication omits the timing-index file consumed by the legacy
checker. Three non-blocking wording repairs are tracked. Claude owns the final
Round-3 response. No archive sample was read, no candidate noise value exists,
no estimator or packet file was written for this gate, no host is pinned, and
rank 2 remains unmeasured.

---

## 1. Startup and review boundary

The automation turn gate named Codex and no `.agent-session.lock` existed. I
created the lock, re-read `.agent-turn`, confirmed it still named Codex, then
read `AgentPrompt.md`, the complete Project Details, Codex continuity, every
Codex-participant chat summary and both active transcripts. The only active
reply owed by Codex was Claude's Draft-33 handoff in
`chats/Claude-Codex/Section 19 Convergence Repair/`. The three-way Review Method
Change chat has no outstanding director request and stays open at Randy's
instruction.

This was a **Round-2 delta pass**, not a new full-artifact review. The binding
scope was Claude's response to F1-R1 through F5-R1, T1-R1 through T4-R1, and any
unchanged sentence made false by those changes. RC-008 is RC-007's sole
like-for-like successor; clause 5 forbids another one after a non-approval.
Round 2 itself does not trigger the Convergence Decision. If the final Round-3
response does not reach explicit same-state approval, the card freezes and the
decision fires.

## 2. Candidate authentication and reproduced owner evidence

All nine Draft-33 handoff digests matched the card:

- selection document `16ee8f80…`;
- extended specification checker `7574ac52…`;
- specification TXT/JSON `8f40c8cc…` / `20aea650…`;
- extended mutation harness `299be141…` and record `a6c0d943…`;
- Round-2 owner probe `aa6a4371…` and TXT/JSON `5f692ba5…` / `0d185bd3…`.

The three closed document spans also reproduced byte-for-byte:

- §1–§16: 144,664 bytes, `700b3b9a…`;
- §17: 21,864 bytes, `dc73b87f…`;
- §18: 20,579 bytes, `8af3e62c…`.

The owner evidence reproduced independently:

- `probe_rc008_spec.py`: **168 checks, 0 failed**;
- closed `probe_rc007_spec.py`: **288 checks, exactly 16 declared failures**,
  exit 1;
- `mutate_rc008_spec.py`: **27 of 27 caught**, control green;
- `probe_rc008_round2.py`: **36 checks, 0 failed**.

The corrected level extrema, nominal-rate deviation diagnostics, interleaving
counterexample, bad-channel pass reversal, and coverage/dilution figures all
match the response. F1-R1, F2-R1 and F5-R1 are accepted on the boundaries Draft
33 now states. The minimum-over-grid floor is deliberately conservative and
auditable through the published `S(k)` series; that design choice did not add a
separate blocker in this delta pass.

## 3. Blocking finding F6-R2 — the split rationale cannot survive the branches

Draft 33 correctly withdraws the claim that interleaving always compresses
`R_null_sampled`, but its replacement gives three grounds for retaining
contiguous halves. Two are false at the strength written.

The document calls it decisive that reducing cancellation is not a goal the
decision rule can “cash,” because a low `R_null_sampled` certifies nothing. Its
own values demonstrate the opposite. At an in-band level with
`R_space_sampled = 1.5` and strict `M = 2`:

- contiguous `R_null_sampled = 1` reaches **passes**;
- interleaved `R_null_sampled = 4` reaches branch 4 and **unmeasurable**.

Reducing cancellation can therefore withhold a would-be pass, which is a direct
decision destination. Saying a low value is not a certificate does not mean the
rule ignores which side of `M` the value lands on.

The first replacement ground says contiguous half-estimates are close to
independent for a signal band-limited above 300 Hz. That frequency condition
does not imply independence. A deterministic 400.921659 Hz process — 87 exact
cycles per 6,510-sample half — repeats across the two halves. Across phase, the
two half-estimate series are identical with correlation 1.0. A narrowband
process can therefore be wholly above 300 Hz and retain perfect cross-half
dependence.

This does not force an interleaved split. Contiguous halves can remain a
predeclared instrument parameter with no optimality or safety claim. It does
block approval of the response's current “decisive” rationale. Claude must
remove the false grounds and state the choice at its actual boundary, or supply
a bounded rationale that survives the counterexamples.

## 4. Blocking finding F7-R2 — one consumed regression input is still unpinned

F4-R1 required the wrapper to authenticate the legacy checker and the records
it consumes before trusting its output. Draft 33 adds five paths to
`RC007_AUTHENTICATED` and the checker announces that every legacy input is
pinned. The legacy checker also reads:

`Reproducibility Packet/results/host_timing_index.jsonl`

That file is absent from the digest list. The mutation harness copies it into
every staged case, which confirms it is required, but none of the 27 mutations
changes it.

The independent probe staged a byte-different timing record containing 21
synthetic series while preserving the two aggregate properties the legacy
checker consumes: series count 21 and maximum relative rate deviation
`9.946e-06`. The wrapper still exited zero at **168 checks, 0 failed**. This is
the original F4-R1 failure class on an unlisted record, not a new concern about
internal style. The final response must pin the timing-index digest and add a
substitution mutation that reaches it.

## 5. Tracked non-blocking delta findings

Three wording surfaces should be repaired with the blockers:

1. **T5-R2:** §19.10 lists four sampled quantities —
   `sigma_worst_sampled`, `sigma_quietest_sampled`, `R_space_sampled` and
   `R_null_sampled` — then says a short excursion is invisible to “all three.”
2. **T6-R2:** §19.3 now gives the lower floor a voting minimum but retains the
   stale sentence that §19.6 “does not lean on the floor.” The actual boundary
   is that the omitted phase correction can bias the level upward under the
   stated model and therefore can make the floor permissive relative to the
   anchor pipeline.
3. **T7-R2:** §19.3 establishes that the raw series declares no sampling rate,
   while §19.7 asks the record to publish the candidate's “own declared rate.”
   If the intended diagnostic is the whole-span endpoint derivation already
   recorded in `host_timing_index.jsonl`, name that derivation.

## 6. Independent evidence and challenges

Created `agents/Codex/tools/probe_rc008_round2.py`, SHA-256 `50a57ddb…`, with
text/JSON records `e721097e…` / `06cae352…`. It passes **27 / 27** and:

- authenticates all nine carded files and all three frozen spans;
- replays the owner and legacy fast probes;
- implements the relevant ordered decision cells directly;
- constructs the above-300-Hz repeated-half counterexample;
- imports the wrapper's own authentication list rather than retyping it;
- stages the counterfeit timing index and proves the wrapper stays green;
- detects the three tracked wording surfaces.

The probe's first run stopped before producing evidence because its span guard
counted section-heading text quoted inside the status stack. I changed it to
match physical Markdown headings (`\n## …`) and reran it. The final record is
green and the preliminary failed run wrote no tracked evidence file. A separate
attempt to wrap the owner mutation harness in shell-side recursive cleanup was
rejected before execution; rerunning with the harness's own self-cleaning temp
tree produced the declared 27/27 result. Neither event changed a candidate or
packet file.

## 7. Decisions and project boundary

- **Review verdict:** `Revisions Required` on Draft 33.
- **Approval:** none; Draft 33 remains frozen and unapproved.
- **Next owner:** Claude, for the final Round-3 response.
- **Convergence:** not triggered by this Round-2 return; mandatory if Round 3
  does not close on explicit same-state approval.
- **Clause 5:** still binding; a non-approval on RC-008 cannot be followed by a
  second like-for-like successor.
- **Execution:** no estimator, candidate noise read, host pin, donor state,
  generation, Rung 0 or sorter run is authorized.

The public Live-Run README receives a forward correction because Claude's prior
entry said the checker now verifies every file it reads and presented the split
as supported by three reasons. The new entry narrows both claims and keeps them
explicitly separate from any recording result.

## 8. Files created or updated

**Created**

- `agents/Codex/tools/probe_rc008_round2.py`
- `agents/Codex/tools/rc008_round2_2026-08-19.txt`
- `agents/Codex/tools/rc008_round2_2026-08-19.json`
- `agents/Codex/Session Summaries/HumanReport47.md`

**Updated**

- `Review Cards/RC-008 Host Noise Gate, Convergence Repair.md`
- `Review Cards/README.md`
- `chats/Claude-Codex/Section 19 Convergence Repair/Section 19 Convergence Repair - Active.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No Claim Sheet, Accessible Claim Sheet, Study Guide, Reproducibility Packet or
Claude candidate file was edited.

## 9. Resource and execution note

No heavy step ran. There was no archive or network access, no GPU work, no
dependency installation and no candidate sample read. The longest validation
was the local mutation harness at under five seconds in this run, so no
heavy-step RAM/VRAM admission measurement was required.

## 10. Next steps

1. Claude should respond explicitly to F6-R2 and F7-R2 and dispose of T5-R2
   through T7-R2 in the final Round-3 candidate.
2. Codex should authenticate only the final delta. If it is acceptable, both
   agents must explicitly approve the same state. If it is not, the
   Convergence Decision fires and RC-008 closes at a terminal disposition.
3. The host-noise estimator remains blocked until §19 closes approved.
4. Codex Session 48 will require the next count-based director progress report;
   no cadence report was due in Session 47.
