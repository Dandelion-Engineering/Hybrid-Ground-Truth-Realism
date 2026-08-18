# Codex Human Report — Session 42

**Date and time:** 2026-08-17 23:32 PDT

**Phase:** Phase 2 — Execution and result review

**Outcome:** RC-006 closed **`Approved` at Round 2**. Claude and Codex
explicitly approved the same nine-file state. Rank 1's strict drift gate is now
discharged, and only that gate: no host is pinned, rank 2 is unmeasured, and no
donor, generation, Rung-0, or sorter action is authorized.

---

## 1. What this session was for

Claude Session 42 returned the single owner response to Codex's RC-006 Round-1
ledger. The candidate is the project's first real host-candidate measurement:
the committed rank-1 report and JSON record, §18 of the Tier A host-selection
document, runbook step 11, and the repaired runbook-checker mutation state.

Round 1 had already independently replayed step 11 and reproduced both result
artifacts byte-for-byte. It returned the reporting surface rather than the
measurement: §18.2 omitted one of four resource terms, overstated headroom by
orders of magnitude, and presented two rounded working-set readings as an
isolated allocation measurement; §18.7 carried a stale help-line count. This
session's task was delta-only under the superseding review method: authenticate
Claude's exact response, verify the four recorded findings and response-created
surfaces, and avoid reopening unchanged material.

## 2. Candidate authentication and scope

All nine SHA-256 digests in RC-006's Round-2 table match the physical files:

| State | SHA-256 |
|---|---|
| committed text report | `a2d325088b384f8010a1e398fd58ec759981269e83cb166b7082c3f76ad0cbef` |
| committed JSON record | `2e125d419eb8ad31ad7824f47dd324b8ed0d54d8230095eb29618436b3c87bd5` |
| `measure_host_drift.py` | `200709824fb3a5694b12243eb65647d038d1d251df9abfe49a3e90ca3b8bad47` |
| runbook checker | `35cea57d67be5e299c036f39312ad821fe193fc3d2cc4d7e1fe6480e04b4ccdb` |
| packet README | `806aefaf9859cc0f391101f205b6e055f9278d5d95ef4d759711ded8762cfaf3` |
| mutation checker | `d443ded05bb38662e39dcc9ec8f99ac2b703ab5bb95270bda33ce9108cd83a79` |
| selection document Draft 28 | `157905c90bfd170cc79f82c045a08e60c7da63c8ed5d5740b431ca24583a16d3` |
| owner repair probe | `512e31fcb1f6eea5832cc678c792cf4f0d224b0c29ba7a8e1fadc04598afc2fc` |
| recorded owner-probe output | `745da38a00b07ec3220196d82b43753e13d4c0ac16edcd60b08f2ca1691ba125` |

The carried candidate diff from Codex Session 41 to Claude Session 42 changes
only the selection document. No file inside the Reproducibility Packet changed,
the committed result artifacts are byte-identical, and no result-bearing code
moved. The previously reviewed bodies also remain fixed: §1–§16 is 144,664
bytes at `700b3b9a…`, and §17 is 21,864 bytes at `dc73b87f…`.

## 3. Delta review result

### F1 — complete resource decomposition

The repaired table names all four terms and adds exactly:

- `cache_bound_bytes = 59,040,736`;
- `resident_bytes = 55,120,439`;
- `structures_bytes = 1,047,116`;
- `library_cache_bytes = 16,777,216`;
- sum and `peak_resident_bytes = 131,985,507`.

The resident term's three subparts also close: 50,564,976 bytes for the two
converted float64 arrays, 3,160,311 retained mask bytes, and 1,395,152 bytes for
the largest stored-width slice, which is exactly 87,197 spikes times 16 bytes.
The report and JSON record already carried all four top-level terms; the repair
correctly identifies the defect as prose misreading a correct instrument.

### F2 — actual admission factors

The recorded free-memory reading is 15,126 MiB, or 15,860,760,576 bytes. The
two factors independently reproduce:

- `0.75 × free = 11,895,570,432`; divided by the plan, **90.128×**;
- `free − plan = 15,728,775,069`; divided by 4 GiB, **3.662×**.

Both gates admit the plan, but the 4 GiB floor is the binding rule. Draft 28
states the mebibyte basis and its rounding boundary and removes the false
three-orders claim.

### F3 — working-set claim narrowed to what was observed

The roughly 162 MB to 213 MB working-set step is now described only as
**consistent with** the code-derived 50,561,280-byte projection. Draft 28 says
why the observation does not isolate one allocation: the process working set
contains the interpreter, allocator arenas, libraries, and every other live
allocation; the samples were coarsely rounded; and one pair on one candidate is
not a reproducible ceiling. No whole-command empirical ceiling is claimed.

Claude also searched for the general defect rather than only the sentence named
in Round 1 and repaired the second occurrence in §18.7. RC-005 follow-up 1 is
explicitly not discharged and not converted into a measurement in both places.

### F4 — state-bound rendered help

The authenticated command renders 164 lines and zero non-ASCII bytes. Draft 28
also records why 165 appeared: it was correct for the pre-promotion command and
was carried across the docstring state change instead of being re-measured on
the published digest.

## 4. Evidence and the owner-probe judgement

Claude's read-only `probe_rc006_repairs.py` reproduced at **61 checks, 0
failed**. Claude explicitly asked whether a prose claim checker was sufficient
or whether the response needed a document mutation harness.

The decision was to accept the claim checker as the appropriate *owner*
instrument because this response changes no executable behaviour. That did not
make it sole evidence. I added
`agents/Codex/tools/probe_rc006_round2.py`, SHA-256
`d5b828869b6e137a60ad8c39892bc395ab394637bf918d6432f4aed0858f7ae2`.
It independently authenticates all nine states, proves that only the selection
document moved in the carried candidate, re-derives the resource and admission
arithmetic from the committed JSON record, checks both fixed earlier-section
spans, verifies the narrowed and retired prose claims, rechecks the unchanged
result disposition, renders help, and compiles the owner probe. It passed
**48/48**.

A mutation harness over Markdown would not establish a new executable
property. The useful pair here is exact instrument output plus an independent
reading of every claim made from it.

## 5. Review decision and communication

I appended an exact-state approval to the RC-006 chat naming Draft 28's full
digest and approving the complete nine-file card table. The card and index now
record `Approved at Round 2`; the chat is concluded and carries a summary.

The root public README received one lean append-only closure entry. It says that
the corrected report is approved while keeping the result narrow: a pass of the
declared depth-trace statistic at 1.821 µm against 20 µm, not proof of physical
probe stillness. Four host gates remain open and no downstream action is
authorized.

Claude's new method observation in the three-way chat was also answered. I
agree that accessible result sentences should later be reviewed directly beside
the technical boundary list, sentence by sentence, rather than translated from
memory. I kept that as recorded practice for now; the applicable artifact
playbook can absorb it when an Accessible Piece actually exists for review.

## 6. Challenges and reasoning paths

The substantive question was not the arithmetic; it was the evidence standard
for prose-only repairs. A green owner checker can still encode its author's
reading, while a behavioural mutation harness has no natural target when no
behaviour changed. The resolution was to separate roles: the owner checker
guards the exact repaired claims, while an independent reviewer probe derives
the numbers from the record and authenticates the no-code-movement boundary.

I also checked whether the response introduced a new claim by decomposing
`resident_bytes`. The source already defines `structures_bytes` as a measured
container bound and `resident_bytes` as the converted arrays, masks, and largest
stored-width slice; Draft 28's wording matches that existing approved contract.
No new blocker or tracked RC-006 follow-up was found.

## 7. Files created or updated

**Created**

- `agents/Codex/tools/probe_rc006_round2.py`
- `agents/Codex/Session Summaries/HumanReport42.md`
- `chats/Claude-Codex/Rank 1 Drift Result/Summary.md`

**Updated**

- `Review Cards/RC-006 Rank 1 Drift Measurement and Step 11.md`
- `Review Cards/README.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md`

**Lifecycle move**

- `chats/Claude-Codex/Rank 1 Drift Result/Rank 1 Drift Result - Active.md`
  → `Rank 1 Drift Result - Concluded.md`, byte-identical at SHA-256
  `ebaaeb569f2ee7873fd7cd5b55c96dcff9633463361170ad4cb768673ee1d353`.

No archive, candidate asset, or network resource was read this session. No
heavy computation or dependency installation occurred.

## 8. Next steps

**Immediate owner: Claude.** Define the noise and post-rescaling effective-SNR
gates before reading another candidate value. The host order remains pinned and
rank 2 remains unmeasured. Codex's later lane remains the joint ten-placement
feasibility condition and independent balance/manipulation gate.

The four-gate remainder is not a host approval. Until all five gates pass on one
candidate, no host-dependent target manifest, donor assignment, generation,
Rung 0, or sorter execution is authorized. RC-005 follow-ups 1, 2, and 4 remain
open outside RC-006.

No count-based progress report was due. Codex's next session is Session 43; the
next cadence report is due in Session 48.
