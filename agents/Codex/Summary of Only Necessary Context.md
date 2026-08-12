# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 7 · 2026-08-12 11:21 PDT**

**Next Codex session will be Session 8.** Complete normal session work first, then write the required count-based director progress report. Amendment-triggered reports do not reset this cadence.

## Current phase and execution boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No template-array pull, generator run, sorter run, raw-recording download, dependency installation, or Rung 0 execution occurred in Session 7.

The public state remains `In Progress`. Do not interpret a review handoff, a provisional placement pass, or a low-yield candidate as a result.

## Claim Sheet states

Current synchronized Codex reviewer states:

- `Claim Sheet.md`: SHA-256 `37dcd0f8b20fcee6dc471e1eb396a0f01890a222c5807c70c03fae527a70959a`
- `Accessible Claim Sheet.md`: SHA-256 `696b76e47ad5b4c42038abdeac18426652db8fb1d462804735d26da28d46c267`

Inside those whole-file states:

- **Amendment 1 — compute schedule/corrected memory story: `In force`.**
- **Amendment 2 — Tier A provenance and finite CA1 pool: `In force`.** Claude explicitly approved Codex's Session 6 wording before flipping the status.
- **Amendment 3 — Tier A asymmetric-pool negative control: `Proposed`.** Codex directly edited and explicitly approves the hashes above. Claude's genuine owner re-review is open.
- **Amendment 4 — acquisition-laboratory provenance/non-transfer: `Proposed`.** Codex directly edited and explicitly approves the same hashes. Claude's genuine owner re-review is open.

Do not mark Amendments 3/4 `In force` until Claude approves these exact states or returns a new synchronized state.

### Amendment 3's separate executable gate

Amendment 3 approval does **not** authorize pseudo-arm generation by itself.

- P1 and P2 use the **final eligible region-unaware pool** after host-specific post-rescaling eligibility, not the provisional 1,149-template metadata screen.
- The random seed is fixed before host/subset inspection at **`711362139`**, derived from the first eight hex digits `2a66865b` of SHA-256 over `Hybrid Ground Truth Realism|Tier A|pseudo pool|v1`.
- After a host exists, a tracked selector configuration must pin the eligible-pool digest/filter, covariate scaling, scalar objective, search budget, deterministic tie-break, sixteen selected `template_index` IDs, and achieved spread.
- Both agents must explicitly approve that exact configuration/selected-ID state before any pseudo-arm generation.

This preserves separate construction and executable-configuration approvals.

## Tier A selection artifact

Active chat:

`chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

Artifact:

`agents/Claude/Tier A Host and Injection Zone Selection.md`

Current Codex-approved Draft 4 reviewer state:

`fa5b871e59ac5e07973eee96b02f3de33f385870138c76bf3699ecff3b8b1f75`

Claude owner re-review is open. Draft 3 hash `3ae39913986a1961d674d2ed7b4714f89293fa6f0e8c02f039ebca3c186696cf` remains the last state both agents explicitly approved.

The current Draft 4 approval is bounded to:

- the host-selection strategy and CA1 recommendation;
- measured acquisition provenance;
- discharged anatomy, duration, and label-ambiguity gates;
- native-yield and amplitude context with their evidence limits; and
- a **parameterized**, not decided, placement screen.

It is not a pinned-host approval.

## Provenance evidence and Amendment 4 boundaries

Tracked replay:

- 21/21 subjects;
- 88,650,017 metadata bytes in 91 requests;
- zero failures;
- donor lab set `{cortexlab}`;
- host lab set `{angelakilab, churchlandlab}`; and
- shared protocol exactly `_iblrig_tasks_ephysChoiceWorld6.4.2`.

Claims allowed by the tracked NWBs:

- donor and candidate-host subjects read differ by laboratory and institution;
- different institutions necessarily exclude one shared physical acquisition rig;
- rig hardware and rig design are **not** identified and remain unverified;
- protocol-version sets partly overlap rather than cleanly separating;
- `genotype`, `strain`, and `description` are absent from every NWB read; and
- every donor recording represented was acquired from cortexlab subjects.

Do not attribute downstream IBL sorting or template-library extraction/curation to cortexlab. The Tier A non-transfer statement is conditional on the acquisition laboratory, the downstream shared processing path, and the finite sixteen-template CA1 population.

## Placement evidence and open calibration

Tracked placement replay:

- 13 bands across 11 recordings;
- 170,215,252 metadata bytes in 169 requests;
- zero failures;
- all unit peak-electrode indices valid and on the named probe;
- 13/13 bands CA1-pure;
- 13/13 band/index and raw/processed electrode-table agreement; and
- unchanged provisional 9-pass / 4-fail split at 60 µm edge margin and 40 µm minimum peak separation.

The report now includes session identifiers, so repeated subject/probe rows are auditable. `--from-records` reproduces it byte-for-byte without network reads.

### Placement remains parameterized

The two placement parameters require different evidence:

1. **Edge margin:** calibrate from the real multichannel spatial support of the sixteen CA1 donor templates.
2. **Minimum peak separation:** predeclare a basis from the host's native peak-depth spacing and the generator's relocation constraints.

Codex owns this two-part calibration during Rung 0 preparation. Template footprint alone does not decide the gate.

### Native yield is not a hidden gate

No overcrowding percentage was predeclared. Session 7 therefore declined to turn the observed table into a post-hoc pass/fail rule.

- NYU-39 Probe00 (`22` units, `1` good) is high-risk and deprioritized.
- It is not formally disqualified before the noise/effective-SNR and remaining gates.
- The amplitude table prompts a convention check; it does not validate the 50–200 µV target until IBL `median_spike_amplitude_uV` and donor-library `amplitude_uv` are shown commensurate.

## Current candidate order and remaining host gates

Recommended order for spending the remaining work:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

This is an order, not a selection.

- Discharged gates: anatomy, duration, label ambiguity.
- Checked non-gating property: donor-lab separation.
- Parameterized: placement capacity.
- Open: drift, noise, post-rescaling effective SNR, and Codex's covariate-balance/manipulation gate.

Use first-admissible logic. Do not finish a census to claim “best,” and do not pin a host until every gate passes.

## Rung 0 preparation boundary

Rung 0 remains unrun. It must:

- construct and pin the pre-injection host substrate;
- avoid phase-shifting injected templates twice;
- pin the exact approximately 60-second segment;
- include the two-part placement calibration above;
- resolve dependencies deliberately in the project venv;
- measure live RAM and VRAM immediately before any heavy step;
- obey the 75%-of-free cap plus 4 GiB RAM / 2 GiB VRAM floors; and
- run only in the daytime convention if those fresh guards pass.

The existing venv still pins only `h5py==3.16.0` and `numpy==2.5.2`. Re-run the metadata scripts after any dependency-pin change.

## Public and director state

- Root `README.md` remains State A / `In Progress`.
- Its latest append-only entry forward-corrects the prior rig, NYU-39, and placement-parameter overclaims. The earlier entry was preserved.
- The Phase 1 director contract-review request remains open and non-blocking.
- The shared-memory request is resolved and retired.
- No director action is needed for Amendments 3/4 unless a real agent disagreement emerges.

## What Codex should do next

1. Read Claude's owner response first. Same-state closure requires explicit approval of `37dcd0f8…`, `696b76e4…`, and `fa5b871e…` or a new handoff.
2. If those states converge, preserve Amendment 3 approval and the later selector-config approval as distinct gates.
3. Prepare, but do not launch, the two-part placement calibration and Rung 0 substrate/configuration.
4. Continue the first candidate's drift, noise, effective-SNR, and balance gates without silently adding native-yield thresholds.
5. Run Rung 0 only after fresh daytime RAM/VRAM admission measurements pass.
6. Because the next Codex session is Session 8, write the count-based director progress report after completing normal session work.

`agents/Codex/Session Summaries/HumanReport7.md` contains the full evidence, exact hashes, reasoning, file list, and validation record.
