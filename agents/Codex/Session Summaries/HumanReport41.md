# Codex Human Report — Session 41

**Date and time:** 2026-08-17 08:19 PDT

**Phase:** Phase 2 — Execution and result review

**Outcome:** RC-006 is **`Revisions Required` at Round 1**. The rank-1 drift
measurement itself reproduced exactly and passes its predeclared statistic, but
§18.2 contains three blocking resource-report claims: an omitted 59,040,736-byte
cache term, false headroom scale language, and an unsupported conversion of two
working-set samples into an isolated byte-exact allocation measurement. A fourth,
nonblocking correction changes the rendered-help count from 165 to 164 lines.
No host is pinned; the remaining host gates and all generation/sorter gates stay
open.

---

## 1. Startup and controlling workflow

`.agent-turn` named Codex and `.agent-session.lock` did not exist. I created the
lock atomically, re-read the turn file, and confirmed it still named Codex before
doing project work.

I followed `AgentPrompt.md`: read the full project brief and Codex continuity,
ingested every Codex-including chat summary and both active transcripts, read the
superseding review-cycle and live-run playbooks, read Claude's latest report, and
reviewed RC-006's complete seven-file candidate. The repository began clean at
`c884b9b` (`Claude Session 41`), matching `origin/main`.

## 2. Candidate authentication and unchanged boundaries

All seven RC-006 digests matched disk. The two committed result artifacts are:

- report: `a2d325088b384f8010a1e398fd58ec759981269e83cb166b7082c3f76ad0cbef`;
- JSON: `2e125d419eb8ad31ad7824f47dd324b8ed0d54d8230095eb29618436b3c87bd5`.

The §1–§16 span is exactly **144,664 bytes** at SHA-256 `700b3b9a…` and is
byte-identical to the preceding state. The drift command's digest moved to
`20070982…`, but its docstring-stripped abstract syntax tree is identical to
`HEAD~1`; the executable program did not move. The previously approved estimator,
reader, missing-depth layer, and their suites retain their recorded digests.

## 3. Independent full replay

Immediately before the network run, I checked live resources in the same shell:
15,269,576,704 bytes of system RAM were free and 14,899 of 16,311 MiB GPU memory
was free. A fresh `--plan-only` run returned the committed **131,985,507-byte**
peak, so admission cleared before any archive read.

I then ran packet Step 11 to temporary outputs. It exited zero and produced a
byte-identical report and byte-identical JSON record at the two committed hashes
above. A structured comparison found zero differences. The reproduced result is:

- `Delta_10min = 1.8206253051757812 µm`, 11-bin window beginning at bin 1;
- `Delta_full = 2.5367050170898438 µm`;
- `Q95_null = 0.5257034301757812 µm`, rank 190 of 200;
- 72 analysed bins, zero invalid, minimum 130 units per bin;
- 140 included of 174 label-blind in-band units or clusters, 3,160,311 spikes;
- 231 missing depths affecting 11 units, with support invariance;
- completion `passes`; reconciliation `passes`, `advances=True`, `conflict=False`.

This is one passing host-selection gate, not a host pin and not proof that the
physical probe stayed still.

## 4. Executable and numerical evidence

- Packet runbook checker: eleven agreeing steps, nothing pending, exit 0.
- Owner suite: **543 checks, 0 failed**.
- Repaired runbook mutation checker: control passes, **18/18 caught**.
- RC-002 mutation anchors: **32/32** still occur exactly once.
- New `probe_rc006_round1.py`: **52 exact checks passed**.
- Changed reviewer Python: `py_compile` clean.
- Rendered drift-command help: **164 lines**, zero non-ASCII bytes.

Independent record derivation reproduced the whole-unit range summary (minimum
1.259 µm, maximum 71.629 µm, median 9.155 µm, 21 above 20 µm, 11 above 40 µm)
and aligned-window summary (minimum 0.643 µm, maximum 43.559 µm, median 5.881 µm,
14 above 20 µm, 4 above 40 µm). The code assembles this audit only after verdict
reconciliation and copies it to the record/report; no gate, label, verdict,
ranking, or ordering consumes it.

## 5. Complete Round-1 finding ledger

1. **RC-006-F1 — blocking:** §18.2 names only resident arrays, structures, and
   the HDF5 library cache as the 131,985,507-byte peak decomposition. Those terms
   total 72,944,771 bytes. The omitted **59,040,736 bytes** is the range reader's
   retained block-cache bound and must be named.
2. **RC-006-F2 — blocking:** the same section says the plan clears both resource
   rules “by three orders of magnitude.” With its own 15,126 MiB free value,
   `(75% × free) / plan` is about **90.128×**, while remaining memory divided by
   the 4 GiB floor is about **3.662×**. Admission passed, but the scale claim is
   false.
3. **RC-006-F3 — blocking:** two rounded process-working-set samples, 162 and
   213 MB, cannot isolate one allocation. The +51 MB observation is consistent
   with the code-derived 50,561,280-byte finite-only-copy projection; it does not
   turn the projection into a byte-exact empirical measurement or establish a
   later whole-command ceiling.
4. **RC-006-F4 — nonblocking, mechanical:** authenticated help renders 164 lines,
   not the 165 claimed in §18.7.

The repaired mutation checker's synthetic pending declarations are accepted.
With no real declaration in force, locally constructing each pending state tests
the live rejection properties without creating a false project state.

## 6. Public forward correction

Claude's newest root running-log entry described 174 objects as neurons, treated
the permutation diagnostic as a universal measurement-noise floor, framed the
result as answering physical probe drift, and dated the masking fixture to months
ago. I preserved the append-only record and added a lean forward correction. It
states the supported boundary: 174 label-blind units or clusters, a conservative
permutation-resolution diagnostic under the declared model, a pass of the depth-
trace statistic rather than proof of physical stillness, and a fixture built
earlier this week. The exact reproduced measurement remains visible.

This correction is general recent-work review, outside RC-006, and does not alter
the candidate or its result.

## 7. Files created or updated

**Created**

- `agents/Codex/tools/probe_rc006_round1.py`
- `agents/Codex/Session Summaries/HumanReport41.md` (this report)

**Updated**

- `Review Cards/RC-006 Rank 1 Drift Measurement and Step 11.md`
- `Review Cards/README.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
- `chats/Claude-Codex/Rank 1 Drift Result/Rank 1 Drift Result - Active.md` — one
  append-only Round-1 response

No Claude-owned candidate file was edited.

## 8. Next steps

1. Claude owns the single RC-006 response: repair §18.2's decomposition,
   headroom language, and working-set attribution, and change the help count to
   164 without moving any parameter or result-bearing code.
2. Codex Round 2 is delta-only against those repaired reporting surfaces and the
   candidate authentication boundary.
3. Even after RC-006 closes, noise, effective SNR, the joint ten-placement
   condition, and balance remain separate host-selection gates. Rank 2 remains
   unmeasured. No generator, donor assignment, Rung 0, or sorter authorization is
   implied.
4. Codex's next session is 42; the next cadence progress report is Session 48.

No new director decision is needed. The three-way review-method observation chat
remains active by the director's instruction.
