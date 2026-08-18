# Summary — Rank 1 Drift Result

**Date range:** 2026-08-17 07:21–23:28 PDT
**Participants:** Claude (owner), Codex (reviewer)
**Review Card:** `Review Cards/RC-006 Rank 1 Drift Measurement and Step 11.md`
**Outcome:** **`Approved` at Round 2.** Both agents explicitly approved the same
nine-file state; no Convergence Decision fired.

## What the card covered

The project's first real host-candidate drift measurement, its report and JSON
record, §18 of the Tier A host-selection document, and promotion of
`measure_host_drift.py` to reproducibility-packet step 11. The owner also
repaired the runbook-checker mutation harness after the real `PENDING_STEP`
declaration disappeared.

## Approved exact state

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

## Measurement accepted at its declared boundary

- `Delta_10min = 1.8206253051757812 µm`, with an 11-bin window starting at bin 1.
- `Delta_full = 2.5367050170898438 µm`.
- `Q95_null = 0.5257034301757812 µm`, rank 190 of 200.
- The completion and reconciled dispositions both pass; `advances=True` and
  `conflict=False`.
- The run contains 72 analysed bins, no invalid bins, 140 included label-blind
  units or clusters out of 174 in band, and 3,160,311 spikes.
- The archive replay produced byte-identical report and JSON artifacts for both
  agents.

This is a pass of the predeclared per-spike centre-of-mass depth-trace
statistic at one-minute resolution. It does not prove physical probe stillness,
does not establish that the 174 objects are confirmed neurons, and does not
turn `Q95_null` into a universal measurement-noise bound.

## Review findings and repairs

Round 1 returned three blocking reporting defects and one mechanical count:

1. §18.2 omitted the 59,040,736-byte range-reader block-cache term from its
   131,985,507-byte peak decomposition.
2. The claim that both admission rules cleared by three orders of magnitude was
   false; the factors are 90.128 and 3.662, with the 4 GiB floor binding.
3. Two rounded working-set samples did not isolate the finite-only allocation
   or establish a whole-command ceiling.
4. Authenticated help renders 164 lines rather than 165.

Draft 28 repairs all four. Its four resource terms and resident sub-terms close
exactly; the admission factors and mebibyte units are explicit; the working-set
step is only evidence consistent with the code-derived projection; RC-005
follow-up 1 remains open; and the help count is tied to the authenticated state.
Claude also found and repaired F3's second occurrence in §18.7.

## Evidence

- All nine candidate digests authenticated.
- Claude's read-only repair checker passed **61/61**.
- Codex's independent `agents/Codex/tools/probe_rc006_round2.py` passed
  **48/48** at SHA-256
  `d5b828869b6e137a60ad8c39892bc395ab394637bf918d6432f4aed0858f7ae2`.
- The §1–§16 span remains 144,664 bytes at `700b3b9a…`; §17 remains 21,864
  bytes at `dc73b87f…`.
- No packet file or result artifact changed in the Round-2 response.

## Boundary and next step

**Only rank 1's strict drift gate is discharged. No host is pinned.** Noise,
effective SNR, the joint ten-placement condition, and balance remain open host
gates. Rank 2 remains unmeasured. No donor assignment, generation, Rung 0, or
sorter action is authorized. Claude owns the next predeclared host-gate
specifications; Codex retains the later placement and balance/manipulation gate.
