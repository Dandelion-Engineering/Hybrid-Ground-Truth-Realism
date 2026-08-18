# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 42 · 2026-08-17.**

**Next Codex session will be Session 43. The next count-based progress report is
due in Session 48.**

## Current phase and controlling boundary

**Phase 2 — Execution and result review.** RC-006 closed **`Approved` at Round
2** on the exact nine-file state both agents approved. Rank 1 has therefore
cleared the strict drift gate, one of five host gates. **No host is pinned.**

Noise, post-rescaling effective SNR, the joint ten-placement condition, and
balance remain open. Rank 2 is unmeasured. No host-dependent target manifest,
donor assignment, generation, Rung 0, or sorter execution is authorized.

## RC-006 approved state

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/results/host_drift_CSHL047_Probe01.txt` | `a2d325088b384f8010a1e398fd58ec759981269e83cb166b7082c3f76ad0cbef` |
| `Reproducibility Packet/results/host_drift_CSHL047_Probe01.json` | `2e125d419eb8ad31ad7824f47dd324b8ed0d54d8230095eb29618436b3c87bd5` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `200709824fb3a5694b12243eb65647d038d1d251df9abfe49a3e90ca3b8bad47` |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `35cea57d67be5e299c036f39312ad821fe193fc3d2cc4d7e1fe6480e04b4ccdb` |
| `Reproducibility Packet/README.md` | `806aefaf9859cc0f391101f205b6e055f9278d5d95ef4d759711ded8762cfaf3` |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `d443ded05bb38662e39dcc9ec8f99ac2b703ab5bb95270bda33ce9108cd83a79` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 28 | `157905c90bfd170cc79f82c045a08e60c7da63c8ed5d5740b431ca24583a16d3` |
| `agents/Claude/tools/probe_rc006_repairs.py` | `512e31fcb1f6eea5832cc678c792cf4f0d224b0c29ba7a8e1fadc04598afc2fc` |
| `agents/Claude/tools/probe_rc006_repairs_2026-08-17.txt` | `745da38a00b07ec3220196d82b43753e13d4c0ac16edcd60b08f2ca1691ba125` |

The §1–§16 span is 144,664 bytes at `700b3b9a…`; §17 is 21,864 bytes at
`dc73b87f…`. Neither moved during RC-006 Round 2. No packet file or result byte
moved in Claude's response.

## Approved rank-1 result

- Candidate: CSHL047 / Probe01, session
  `b52182e7-39f6-4914-9717-136db589706e`, target CA1, strict gate.
- `Delta_10min = 1.8206253051757812 µm`, 11-bin window starting at bin 1.
- `Delta_full = 2.5367050170898438 µm`.
- `Q95_null = 0.5257034301757812 µm`, rank 190 of 200.
- 72 analysed bins, zero invalid, minimum 130 units per bin.
- 140 included of 174 label-blind units or clusters, 3,160,311 spikes.
- 231 missing depths in 11 units; support invariant.
- Completion and reconciliation both `passes`; `advances=True`,
  `conflict=False`.
- Archive cost: 88,599,226 bytes over 93 requests.

This is a pass of the declared per-spike centre-of-mass depth-trace statistic at
one-minute resolution. It is not proof of physical probe stillness. The archive
objects are label-blind units or clusters, not confirmed neurons. `Q95_null` is
a conservative resolution diagnostic under the declared additive
common-movement model, not a universal measurement-noise bound.

## What RC-006 Round 2 settled

All four Round-1 findings are repaired:

1. The 131,985,507-byte plan now names all four terms, including the omitted
   59,040,736-byte retained block-cache bound.
2. The two admission factors are 90.128 and 3.662, not three orders of
   magnitude; the 4 GiB floor binds.
3. The approximately 51 MB working-set increase is only evidence consistent
   with the 50,561,280-byte code-derived projection. The projection remains a
   projection, no whole-command empirical ceiling is claimed, and RC-005
   follow-up 1 remains open.
4. Authenticated `--help` is 164 lines and ASCII-only.

Claude's repair checker passed 61/61. Codex's independent
`agents/Codex/tools/probe_rc006_round2.py` passed 48/48 at SHA-256
`d5b828869b6e137a60ad8c39892bc395ab394637bf918d6432f4aed0858f7ae2`.
The owner prose checker is accepted as the appropriate owner instrument for a
reporting-only response, with the independent record-derived probe providing
the second reading; no Markdown mutation harness was needed.

## Communication and public state

`chats/Claude-Codex/Rank 1 Drift Result/` is concluded and summarized. RC-006
and its index record `Approved at Round 2`.

`chats/Claude-Codex-Human/Review Method Change/` remains active at Randy's
request. The newest exchange agrees that later accessible result writing should
be reviewed sentence-by-sentence beside the technical boundary list, not from
memory. No current message requires a response and no director decision is
needed.

The root public README has a lean closure heartbeat: the corrected rank-1
measurement report is approved, but only one of five host gates is discharged.
The public state remains `In Progress`.

## Immediate next step

**Immediate owner: Claude.** Specify the noise and post-rescaling effective-SNR
gates before reading another candidate value. The quantity, parameters,
thresholds, decision shapes, resource plan, and input confirmations should be
fixed before measurement. Do not add those specifications inside the concluded
RC-006 state; they are a forward section and a separate review boundary.

Rank 2 may be measured only under the still-approved step-11 command and after a
fresh resource check, but it is not a substitute for completing rank 1's next
gates in the declared order. Codex's later lane remains the joint ten-placement
feasibility condition and independent balance/manipulation gate.

## Approved foundation and downstream gates

- RC-001: drift definition and estimator closed `Approved`.
- RC-002: closed unapproved at its Convergence Decision; its single successor
  RC-003 closed `Approved`.
- RC-004: session reference-instant check closed `Approved` at Round 2.
- RC-005: missing-depth recovery closed `Approved with Follow-Ups` at Round 2;
  follow-ups 1, 2, and 4 remain open.
- RC-006: rank-1 measurement/report closed `Approved` at Round 2.
- All six Claim Sheet amendments remain `In force`; contract hashes remain
  `2feda611…` / `679918f7…`.
- The real-arm donor-matching prose remains same-state approved at Draft 6
  `51adae4b…`; implementation and host-dependent states remain separate gates.

After one host passes all five gates, the order remains: approve the exposure
schedule and placement specification; approve matcher implementation and tests;
calibrate footprint/placement; freeze exact matching outputs; obtain independent
balance/manipulation approval; then seek separate generation and later Rung-0/
sorter authorizations.

`agents/Codex/Session Summaries/HumanReport42.md` is the detailed permanent
record. No Session-42 cadence report was due.
