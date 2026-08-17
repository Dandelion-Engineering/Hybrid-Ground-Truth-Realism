# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 41 · 2026-08-17.**

**Next Codex session will be Session 42. The next count-based progress report is
due in Session 48.**

## Current phase and controlling boundary

**Phase 2 — Execution and result review.** Rank 1 has a reproduced passing result
for the predeclared depth-trace statistic, but **no host is pinned**. RC-006 is
open at **`Revisions Required` after Round 1** because three claims in the §18.2
resource record are unsupported or arithmetically incomplete. Claude owns one
response; Codex Round 2 is delta-only.

The reproduced rank-1 result removes only the drift-statistic gate if RC-006's
reporting state closes. Noise, effective SNR, the joint ten-placement condition,
and balance remain open host gates. Rank 2 is unmeasured. No donor assignment,
Rung 0, generation, or sorter run is authorized.

## RC-006 candidate state

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/results/host_drift_CSHL047_Probe01.txt` | `a2d325088b384f8010a1e398fd58ec759981269e83cb166b7082c3f76ad0cbef` |
| `Reproducibility Packet/results/host_drift_CSHL047_Probe01.json` | `2e125d419eb8ad31ad7824f47dd324b8ed0d54d8230095eb29618436b3c87bd5` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `200709824fb3a5694b12243eb65647d038d1d251df9abfe49a3e90ca3b8bad47` |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `35cea57d67be5e299c036f39312ad821fe193fc3d2cc4d7e1fe6480e04b4ccdb` |
| `Reproducibility Packet/README.md` | `806aefaf9859cc0f391101f205b6e055f9278d5d95ef4d759711ded8762cfaf3` |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `d443ded05bb38662e39dcc9ec8f99ac2b703ab5bb95270bda33ce9108cd83a79` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 27 | `646def951178f76ca2397c34dc46a2b2f0f96c3d77d6658825335aede71b82c3` |

The §1–§16 span is exactly **144,664 physical bytes** at SHA-256
`700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59`
and is byte-identical to the prior state. The command's digest changed for Step
11 documentation only; its docstring-stripped AST is identical to `HEAD~1`.

The RC-005-approved estimator, archive reader, missing-depth layer, and their test
states remain byte-identical and outside this candidate.

## Reproduced rank-1 result

Codex measured live resources immediately before the run: 15,269,576,704 system-
RAM bytes free and 14,899 of 16,311 MiB GPU memory free. Fresh `--plan-only`
returned 131,985,507 bytes and cleared admission. A fresh packet Step-11 run then
produced a byte-identical report and byte-identical JSON record at the two hashes
above; a structured comparison found zero differences.

- `Delta_10min = 1.8206253051757812 µm`, 11-bin window starting at bin 1;
- `Delta_full = 2.5367050170898438 µm`;
- `Q95_null = 0.5257034301757812 µm`, rank 190 of 200;
- 72 analysed bins, zero invalid, minimum 130 units per bin;
- 140 included of 174 label-blind in-band units or clusters, 3,160,311 spikes;
- 231 missing depths in 11 units, support invariant;
- completion `passes`; reconciliation `passes`, `advances=True`, `conflict=False`;
- 88,599,226 archive bytes over 93 requests.

This is a pass of the declared per-spike centre-of-mass depth-trace statistic at
one-minute resolution. It is not proof that the physical probe or tissue stayed
still, and `Q95_null` is a conservative permutation-resolution diagnostic under
the declared additive common-movement model, not a universal noise bound.

## RC-006 Round-1 ledger

1. **RC-006-F1 — blocking:** §18.2 omits the range reader's 59,040,736-byte
   retained block-cache bound from its 131,985,507-byte decomposition. The three
   terms it names total only 72,944,771 bytes. Name all four terms.
2. **RC-006-F2 — blocking:** §18.2's “three orders of magnitude” headroom claim
   is false. With the stated 15,126 MiB free, `(75% × free) / plan` is about
   90.128× and remaining memory divided by the 4 GiB floor is about 3.662×.
3. **RC-006-F3 — blocking:** two rounded process-working-set samples, 162 and
   213 MB, do not isolate the finite-only allocation. The +51 MB observation is
   consistent with the code-derived 50,561,280-byte projection; it does not make
   that term a byte-exact empirical measurement or establish a whole-command
   ceiling.
4. **RC-006-F4 — nonblocking, mechanical:** authenticated help renders 164 lines,
   not the 165 claimed in §18.7; non-ASCII byte count is zero.

Everything else in scope passed Round 1. Every substantive result value in §18
matches the record. The per-unit audit is assembled after reconciliation and is
not consumed by any gate, verdict, label, rank, or ordering. The synthetic
`PENDING_STEP` mutation fixtures are accepted as the correct way to test live
checker properties when no real pending declaration exists.

## Evidence reproduced in Session 41

- Full Step-11 archive replay: byte-identical report and JSON, exit 0.
- `check_runbook_consistency.py`: eleven agreeing steps, nothing pending.
- `test_measure_host_drift.py`: **543 checks, 0 failed**.
- `mutation_test_runbook_checker.py`: green control, **18/18 caught**.
- RC-002 mutation anchors: **32/32** unique.
- `agents/Codex/tools/probe_rc006_round1.py`: **52/52** exact checks.
- Reviewer probe `py_compile`: exit 0.

## Public and communication state

`chats/Claude-Codex/Rank 1 Drift Result/` is active. Codex's exhaustive Round-1
response is appended at physical EOF with the four-item ledger and explicit
`Revisions Required` outcome. Claude owns one response.

The root public `README.md` remains append-only. Codex appended a forward
correction after the first-result entry: 174 label-blind units or clusters are
not 174 confirmed neurons; the result does not prove physical probe stillness;
the permutation diagnostic is not a universal measurement-noise bound; and the
masking fixture was built earlier this week rather than months ago. The exact
reproduced numbers remain unchanged.

`chats/Claude-Codex-Human/Review Method Change/` remains active at Randy's
request. No current message requires a reply and no new director decision is
needed.

## Immediate next step

**Immediate owner: Claude.** Make one RC-006 response that changes reporting
surfaces only:

1. reconcile the 131,985,507-byte peak to all four terms, including the
   59,040,736-byte block cache;
2. replace the false three-orders headroom statement;
3. narrow the working-set observation to evidence consistent with the exact
   code-derived projection, not an isolated byte-exact measurement;
4. correct rendered help from 165 to 164 lines.

Do not move parameters, thresholds, seeds, numerical branches, result artifacts,
rank order, or downstream authorizations. Codex Round 2 must authenticate the
new exact state and inspect only the response delta plus its dependent reporting
surfaces. If repaired without a new blocker, record explicit same-state approval;
silence or use is not approval.

## Approved foundation and downstream gates

- RC-001: drift definition and estimator closed `Approved`.
- RC-002: closed unapproved at its Convergence Decision; its single successor
  RC-003 closed `Approved`.
- RC-004: session reference-instant check closed `Approved` at Round 2.
- RC-005: missing-depth recovery closed `Approved with Follow-Ups` at Round 2.
- RC-006: rank-1 measurement/report is open, `Revisions Required` at Round 1.
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

After a host passes all five gates, the order remains: approve the exposure
schedule and placement specification; approve matcher implementation and tests;
calibrate footprint/placement; freeze exact matching outputs; obtain independent
balance/manipulation approval; then seek separate generation and later Rung-0/
sorter authorizations.

`agents/Codex/Session Summaries/HumanReport41.md` is the detailed permanent
record. No Session-41 cadence report was due.
