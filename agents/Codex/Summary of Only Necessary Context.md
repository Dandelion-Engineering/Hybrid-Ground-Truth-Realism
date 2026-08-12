# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 8 · 2026-08-12 13:17 PDT**

**Next Codex session will be Session 9.** The scheduled Session 8 director progress report exists at `agents/Codex/Progress Reports/Progress Report Session 8.md`.

## Current phase and hard boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No template-array pull, dependency installation, raw-recording download, hybrid generator run, sorter run, or Rung 0 execution occurred in Codex Session 8.

The public state remains `In Progress`. Draft approval, a metadata audit, a selector design, and a provisional placement pass are not results about whether realism changes sorter accuracy.

## Claim Sheet states

Current synchronized Codex reviewer states:

- `Claim Sheet.md`: SHA-256 `5b6c2ee70f81585fbe291f90e02eb4a312f55eb045356063b34f60c591cb7a09`
- `Accessible Claim Sheet.md`: SHA-256 `d9bb991ba02b8bae8360bbbd565512b873cafc8b0288b8f84aba4557a610ad46`

Inside those whole-file states:

- **Amendment 1 — compute schedule/corrected memory story: `In force`.**
- **Amendment 2 — Tier A provenance and finite CA1 pool: `In force`.**
- **Amendment 3 — Tier A asymmetric-pool negative control: `Proposed`.** Codex directly edited and explicitly approves the hashes above. Claude's genuine owner re-review is open.
- **Amendment 4 — acquisition-laboratory provenance/non-transfer: `In force`.** Claude approved Codex's exact Session 7 wording in Session 8 after re-deriving the evidence.

Do not mark Amendment 3 `In force` until Claude approves these exact states or returns a new synchronized state. Tier A generation remains blocked.

## Amendment 3 selector — current exact rule and gates

Amendment 3 fixes a no-manipulation Tier A pseudo contrast:

- P1 uses a fixed sixteen-template subset of the **final host-dependent eligible region-unaware pool**.
- P2 uses that same full eligible pool and is matched to P1 by the real-arm procedure.
- Neither arm conditions on region.
- The fixed seed remains `711362139`, derived from the first eight hexadecimal digits `2a66865b` of SHA-256 over `Hybrid Ground Truth Realism|Tier A|pseudo pool|v1`.

Session 8 repaired three load-bearing points:

1. **Template identity is the pair (`dataset`, `template_index`).** Bare `template_index` is not unique: 2,183 NP1.0 rows contain only 187 distinct integers, while the pair is unique for all rows. Use the pair for every real and pseudo donor configuration; this clarifies the earlier Slot 7 shorthand.
2. **The selector is deterministic and bounded.** Standardize post-rescaling amplitude, effective host SNR, and injection-band depth with the final eligible pool's float64 mean and population SD; apply the same transform to CA1. Non-finite values or zero SD fail the configuration gate. The scalar objective is the equally weighted sum of per-covariate equal-sample 1-Wasserstein distances.
3. **Initialization/search are fixed.** Hash `711362139\n<dataset>\n<template_index>` with SHA-256 for each eligible pair; start with the sixteen smallest unsigned big-endian digests. Each sweep evaluates every one-for-one subset/complement swap; choose the lowest strict-improvement objective, tie-broken by the lexicographically lowest sorted sixteen-pair state. Never run a partial sweep: continue only while a complete next sweep keeps cumulative evaluations at or below 100,000. Report local-optimum versus cap stop. This is not a global-optimum claim.

The rationale is forking-path control, not a monotonic claim. Better covariate matching is **not** known to narrow the eventual sorter-derived band, and worse matching is not known to widen it. The rule is fixed early so multiple plausible recipes cannot be tried after pool inspection and selected for a reassuring band.

Even after Amendment 3 is in force, a **separate executable configuration gate** remains. After the host exists, a tracked configuration must pin the eligible-pool digest/filter, restate the rule, record all sixteen (`dataset`, `template_index`) pairs, per-covariate distances, evaluated-swap count, and stopping reason. Both agents must explicitly approve that exact state before any pseudo-arm generation.

## Tier A selection artifact

Active chat:

`chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

Artifact:

`agents/Claude/Tier A Host and Injection Zone Selection.md`

Draft 5 SHA-256:

`7c4b911df9e53032ae7cd0453cc51ac79b4d65fdfa40abcd41577ad027be69db`

**Both agents explicitly approve this exact Draft 5 state.** The same-state review is closed for Draft 5's declared scope:

- host-selection strategy and CA1 recommendation;
- measured acquisition provenance;
- discharged anatomy, duration, and label-ambiguity gates;
- native-yield and amplitude context with their evidence limits;
- parameterized placement evidence; and
- the one-session amplitude-convention audit.

This is **not** a pinned-host approval. The chat remains active because host selection and Amendment 3 are open.

## Amplitude-convention evidence and scale-factor ruling

Tracked audit:

- `Reproducibility Packet/scripts/audit_amplitude_conventions.py`
- `Reproducibility Packet/results/amplitude_conventions.txt`
- `Reproducibility Packet/results/amplitude_conventions.json`

What it establishes on one processed session (`sub-KS042`, session `07dc4b76`):

- donor `amplitude_uv` is peak-to-peak over time of an average waveform at the donor builder's best channel;
- host `median_spike_amplitude_uV` is the median over per-spike single-sided peak amplitudes;
- they are not the same quantity;
- 1,821-unit ratio medians are 1.250 all / 1.242 Kilosort-good / 1.207 IBL-quality-1;
- best-channel rules agree on 72.6% of all units, with a sensitivity calculation at the file's named channel; and
- a rough population restatement of the 50–200 µV donor target is about 41–165 µV in the host-column convention.

Boundaries:

- one session fixes the definition, not the population;
- the ratio spread forbids per-unit conversion;
- donor and host preprocessing still differ and are not shown equivalent;
- donor templates are good-clusters-only by construction;
- donor depth and host unit depth use different best-channel rules, differing by one 20 µm contact in the disagreeing quarter.

Session 8 fixed a stale script docstring only; numerical code/results were untouched. The script compiles and the raw JSON summaries were independently reproduced.

**Scale factor is diagnostic, not a matching covariate or threshold.** SpikeInterface 0.104.8 rescales each template array linearly. Once actual rendered post-rescaling amplitude, effective host SNR, footprint/placement, and provenance are gated, the scalar itself is not a separate sorter-visible property. Rung 0 must still report per-arm scale-factor distributions/extremes and verify finite factors, no clipping/overflow, and achieved rendered amplitudes. If real execution reveals non-linearity, amend rather than adding a post-hoc covariate.

## Provenance and placement evidence retained

Provenance replay remains:

- 21/21 subjects;
- donor lab `{cortexlab}` and host labs `{angelakilab, churchlandlab}`;
- lab/institution separation measured;
- protocol overlap exactly at 6.4.2;
- different institutions exclude one shared physical rig, but rig hardware/design remain unverified;
- strain/genotype/description absent from all files read; and
- cortexlab is acquisition origin, not attribution for downstream IBL sorting or template extraction.

Placement replay remains:

- 13 bands across 11 recordings;
- 13/13 CA1-pure, band/index and raw/processed electrode tables consistent;
- provisional 9-pass / 4-fail split at the uncalibrated 60 µm edge margin and 40 µm peak separation;
- report reproducible byte-for-byte from saved records.

Placement remains parameterized. Donor multichannel spatial support can calibrate edge margin. Minimum peak separation needs a separate predeclared basis from native peak-depth spacing and generator relocation constraints. Codex owns both in Rung 0 preparation.

## Candidate order and open host gates

Spend remaining work in this order unless new evidence changes admissibility:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

This is an order, not a selection.

- Discharged: anatomy, duration, label ambiguity.
- Checked non-gating property: donor-lab separation.
- Parameterized: placement capacity.
- Open: drift, noise, post-rescaling effective SNR, and covariate-balance/manipulation gate.

Native yield remains diagnostic. NYU-39 Probe00 is high-risk/deprioritized, not formally disqualified without a predeclared threshold and before the noise/SNR gate.

## Rung 0 boundary

Rung 0 remains unrun. It must:

- construct and pin the pre-injection host substrate;
- avoid phase-shifting injected templates twice;
- pin the exact approximately 60-second segment;
- perform the two-part placement calibration;
- deliberately resolve dependencies in the project venv;
- measure fresh RAM and VRAM immediately before any heavy step;
- obey the 75%-of-free cap plus 4 GiB RAM / 2 GiB VRAM floors; and
- run only within the daytime convention if the fresh guards pass.

The existing venv still pins only `h5py==3.16.0` and `numpy==2.5.2`. Re-run metadata scripts after any dependency-pin change.

## Public and director state

- Root `README.md` remains State A / `In Progress` and now records the repeated template index, deterministic-selector repair, and removal of the unproved monotonic-band claim.
- Its orientation footer correctly says Amendments 1, 2 and 4 are in force; Amendment 3 is in active same-state review.
- `agents/Codex/Progress Reports/Progress Report Session 8.md` is the required count-based director update.
- The Phase 1 contract-review request remains open and non-blocking.
- No new director action is needed unless Amendment 3 fails to converge.

## What Codex should do next

1. Read Claude's Amendment 3 owner response first. Same-state closure requires explicit approval of `5b6c2ee7…` / `d9bb991b…` or a new synchronized handoff.
2. Keep Amendment 3 approval and the later selector-configuration approval separate.
3. Prepare the two-part footprint/placement calibration and the pre-injection Rung 0 configuration without launching a heavy run prematurely.
4. Continue the first candidate's drift, noise, effective-SNR, placement, and balance gates without adding native-yield or scale-factor thresholds.
5. Run Rung 0 only after all contract/host prerequisites and immediate daytime RAM/VRAM admission checks pass.

`agents/Codex/Session Summaries/HumanReport8.md` contains the full evidence, reasoning, exact-state decisions, validation record, machine state, and file list.
