# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 9 · 2026-08-12 15:15 PDT**

**Next Codex session will be Session 10.** No progress report was due in Session 9; the next count trigger is Session 16 unless a phase transition or approved amendment triggers one earlier.

## Current phase and hard boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No template-array pull, dependency installation, raw-recording download, hybrid generator run, sorter run, or Rung 0 execution occurred in Codex Session 9.

The public state remains `In Progress`. Contract repair, metadata derivation, and host screening are not evidence about whether realism changes sorter accuracy.

## Claim Sheet states

Current synchronized Codex reviewer states:

- `Claim Sheet.md`: SHA-256 `13d05239b85eb5605212484ae02c54208f1d744cad015ce592d74495c4e83e89`
- `Accessible Claim Sheet.md`: SHA-256 `676c2e3cebf8df6312fbd9d9d0623dae4a52a39d821e20b7a0b12b589376a214`

Inside those whole-file states:

- **Amendment 1 — compute schedule/corrected memory story: `In force`.**
- **Amendment 2 — Tier A provenance and finite CA1 pool: `In force`.**
- **Amendment 3 — Tier A asymmetric-pool negative control: `Proposed`.** Codex directly edited and explicitly approves the hashes above. Claude's genuine owner re-review is open.
- **Amendment 4 — acquisition-laboratory provenance/non-transfer: `In force`.**

Do not mark Amendment 3 `In force` until Claude approves these exact states or returns a new synchronized state. Tier A generation remains blocked.

## Amendment 3 selector — current exact rule and gates

The Tier A no-manipulation diagnostic now uses one shared pseudo-base pool:

- The full final eligible region-unaware pool is computed after a host is pinned.
- Remove the injection zone's donor pool from it. For the current CA1 recommendation, the removed set is exactly the sixteen real matched-arm templates.
- P1 is a fixed sixteen-template subset of this pseudo-base pool.
- P2 draws from the same full pseudo-base pool and is matched to P1 by the real-arm procedure.
- Both arms therefore share the same non-injection-zone condition. This avoids the prior defect where P1 excluded CA1 but P2 could draw it, potentially preferentially because P2 is matched to the CA1-like P1.
- The diagnostic does not mirror chance target-region donors in the real region-unaware arm; that limitation is stated explicitly.

Every template is identified by the globally unique pair (`dataset`, `template_index`). Bare `template_index` is invalid: 2,183 NP1.0 rows contain 187 distinct integers but 2,183 distinct pairs.

The fixed seed remains `711362139`, derived from the first eight hexadecimal digits `2a66865b` of SHA-256 over `Hybrid Ground Truth Realism|Tier A|pseudo pool|v1`.

Selection remains deterministic:

1. Standardize post-rescaling amplitude, effective host SNR, and injection-band depth with the final eligible pool's float64 mean and population SD; apply the same transform to CA1. Non-finite values or zero SD fail the gate.
2. Minimize the equally weighted sum of per-covariate equal-sample 1-Wasserstein distances.
3. Hash `711362139\n<dataset>\n<template_index>` for each pseudo-base pair and start with the sixteen smallest unsigned big-endian SHA-256 digests.
4. Each complete sweep evaluates every one-for-one subset/complement swap; take the lowest strict improvement with the lexicographically lowest sorted pair-state as the exact tie-break.
5. Run at most **64 complete sweeps**. Stop earlier at a one-swap local optimum; if sweep 64 improves, take it and record a cap stop. No partial sweep and no global-optimum claim.

The former 100,000-evaluation cap was removed because plausible large pools received only two to five improvement opportunities while small pools received dozens. At `M = 2,167`, 64 sweeps are about 2.20 million small objective evaluations.

Even after Amendment 3 becomes `In force`, a **separate executable configuration gate** remains. It must pin:

- final eligible-pool digest/filter;
- pseudo-base-pool digest/filter;
- exact removed (`dataset`, `template_index`) pairs;
- selected sixteen pairs;
- per-covariate distances;
- evaluated-swap count; and
- local-optimum versus cap stop.

Both agents must approve that exact state before pseudo-arm generation.

## Tier A selection artifact

Active chat:

`chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

Artifact:

`agents/Claude/Tier A Host and Injection Zone Selection.md`

Draft 5 SHA-256:

`7c4b911df9e53032ae7cd0453cc51ac79b4d65fdfa40abcd41577ad027be69db`

**Draft 5 is the last artifact state both agents explicitly approved.** It covers the host-selection strategy and CA1 recommendation, measured provenance, anatomy/duration/label evidence, parameterized placement, native-yield context, and the one-session amplitude-convention audit. It is not a pinned-host approval.

Claude added §12 in Session 9, but did not hand off an owner-approved Draft 6 hash in chat. Codex reviewed the new work generally and fixed shared packet code; do not call the current artifact same-state approved until Claude explicitly hands it off and the review cycle closes.

## CCF label-map state

Claude derived 138 long-name/acronym entries from DANDI 000409 electrode annotations plus the MIT template metadata instead of importing the Allen ontology under its noncommercial terms. The tracked derivation reports 44/44 agreements with the independently hand-authored table, two name collisions withheld, and 66 of 209 host names still unmapped on the assigned donor probes.

Codex Session 9 fixed two forward-facing defects:

- derived white-matter/fibre-tract acronyms `ec`, `ee`, `fp`, `int`, `opt`, `rust`, `SCdw`, `SCiw`, `scp`, and `scwm` remain non-injectable; and
- `derive_ccf_label_map.py --from-records` fails if probe type, asset suffix, or depth tolerance differs from the evidence-generation settings saved with the votes.

Compilation, a matching replay, a deliberate tolerance mismatch, and injectability assertions passed. No tracked numerical result changed.

The derived layer is opt-in. Mixed parent/descendant donor labels are an input to Codex's balance gate: CA1 is a leaf and unaffected, but any zone change must audit hierarchy overlap before exact acronym equality/inequality is treated as a clean region contrast.

## Amplitude and placement evidence retained

Amplitude convention remains:

- donor `amplitude_uv` is peak-to-peak over an averaged waveform at the donor builder's best channel;
- host `median_spike_amplitude_uV` is median per-spike single-sided peak;
- the one-session ratio medians are 1.250 all / 1.242 Kilosort-good / 1.207 IBL-quality-1;
- best-channel rules agree on 72.6% of all units; and
- roughly 41–165 µV in host-column terms corresponds at population level to the 50–200 µV donor target.

The pre-rescaling scale factor remains diagnostic, not a matching covariate or threshold. Report per-arm distributions/extremes, verify finite factors, no clipping/overflow, and achieved rendered amplitudes. If execution reveals nonlinear scaling, amend.

Placement remains parameterized:

- 13/13 CA1 bands were label-pure and raw/processed electrode tables agreed;
- the provisional screen was 9 pass / 4 fail at 60 µm edge margin and 40 µm peak separation;
- donor multichannel spatial support must calibrate edge margin; and
- minimum peak separation needs a separate predeclared basis from native peak-depth spacing and generator relocation constraints.

Codex owns both placement calibrations during Rung 0 preparation.

## Candidate order and open host gates

Continue in this order unless new evidence changes admissibility:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

This is an order, not a selection.

- Discharged: anatomy, duration, label ambiguity, donor-lab separation as a recorded property.
- Parameterized: placement capacity.
- Open: drift, noise, post-rescaling effective SNR, and covariate-balance/manipulation gate.
- Native yield remains diagnostic. NYU-39 Probe00 is deprioritized/high risk, not formally disqualified without a predeclared threshold.

## Rung 0 boundary

Rung 0 remains unrun. It must:

- construct and pin the pre-injection host substrate;
- avoid phase-shifting injected templates twice;
- pin the exact approximately 60-second segment;
- complete the two-part placement calibration;
- deliberately resolve dependencies in the project venv;
- measure fresh RAM and VRAM immediately before any heavy step;
- obey the 75%-of-free cap plus 4 GiB RAM / 2 GiB VRAM floors; and
- run only within the daytime convention if the fresh guards pass.

The current venv still pins only `h5py==3.16.0` and `numpy==2.5.2`. Re-run metadata scripts after any dependency-pin change.

## Public and director state

- Root `README.md` remains State A / `In Progress`; its latest entry records the shared-pseudo-pool and 64-sweep corrections.
- Its orientation footer correctly says Amendments 1, 2 and 4 are in force; Amendment 3 is in active same-state review.
- The Phase 1 contract-review request remains open and non-blocking.
- No new director action is needed unless Amendment 3 fails to converge.
- No progress report was triggered in Codex Session 9.

## What Codex should do next

1. Read Claude's owner response to hashes `13d05239…` / `676c2e3c…` first. Same-state closure requires explicit approval or a new synchronized handoff.
2. Keep Amendment 3 approval and the later selector-configuration approval separate.
3. If Claude puts Amendment 3 `In force`, confirm both sheets changed together and that the author created the event-triggered progress report.
4. Re-review §12 only after Claude explicitly approves and hands off a named artifact state.
5. Continue the footprint/edge-margin calibration and independent peak-separation basis, then the first candidate's drift, noise, effective-SNR, placement, and balance gates.
6. Do not launch Rung 0 until all contract/host prerequisites and immediate daytime RAM/VRAM admission checks pass.

`agents/Codex/Session Summaries/HumanReport9.md` contains the full evidence, reasoning, exact-state decision, code fixes, validation record, machine state, and file list.
