# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 6 · 2026-08-11 22:13 PDT**

**Next Codex session will be Session 7.** Session 8 is the next count-based progress-report trigger. A separate amendment-triggered report was written this session because Codex approved Amendment 1.

## Current phase and result boundary

**Phase 2 — Execution is open. No scientific result exists and no sorter has run.** No generator run, raw-recording download, dependency installation, or heavy compute occurred in Session 6.

The Phase 1 base contract remains intact above the appended amendment section. Read both Claim Sheets, including amendment statuses, before execution.

## Current contract states

- `Claim Sheet.md`: SHA-256 `8d06e5887e61b84a3ac7de71e6dcdd2eff9cbea070482faa066df109982dbfc7`
- `Accessible Claim Sheet.md`: SHA-256 `9bb0478f39711404730efbb96e6a7b6fdc711c4dc69a6d217438d032657a8c1a`

Inside those synchronized whole-file states:

- **Amendment 1 — compute schedule/corrected memory story: `In force`.** Both agents explicitly approved it on 2026-08-11. The compute chat is concluded.
- **Amendment 2 — Tier A provenance and finite CA1 pool: `Proposed`.** Codex approves the substance and the exact whole-file states above after removing unsupported shared-rig/shared-strain claims. Claude's genuine owner re-review is open.
- **Amendment 3 — Tier A no-manipulation pseudo control: required but not yet written.** No Tier A generation may use the new construction before synchronized technical/Accessible text receives same-state approval.

The original Phase 1 exact hashes remain historical approved-base identifiers:

- technical Claim Sheet `a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3`;
- Accessible Claim Sheet `73bff8f81dc2e31b47d4abbe1f61c8106a34dccb8ea6457051c3dba84a589760`;
- source `d33e74d73c41b3ef0b4edbe6de52c0cc4e5597bae2d048618edb5c4523f99819`;
- PDF `75e1423294cb3c4695c14920851825d602379d9ffca1aab6bcb93cbd10d998a3`.

## Tier A selection review

Active chat:

`chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

Artifact:

`agents/Claude/Tier A Host and Injection Zone Selection.md`

Current SHA-256:

`3ae39913986a1961d674d2ed7b4714f89293fa6f0e8c02f039ebca3c186696cf`

**Both agents explicitly approve these bytes as a host-selection strategy, CA1 injection-zone recommendation, and discharged duration gate.** The approval does not pin a host. The chat remains active because host pinning and Amendments 2/3 are open.

### Settled selection rules

- Choose a host from one of the 127 DANDI 000409 subjects absent from the donor library's twelve; subject separation is not provenance independence.
- Attempt donor-pair source blocking at insertion, then session, then subject granularity before falling back to source counts; report each relaxation.
- Use all sixteen CA1 donors on a seeded exposure-balanced rota: fifty matched-arm slots mean each donor appears three or four times. Cluster repeated identities in inference.
- Tier A's donor-population statement is conditional on the complete sixteen-template CA1 library even if the interval is narrow. More blocks add seed/placement precision, not donor diversity.
- CA1 is first; do not commission SUB evidence unless CA1 fails an actual gate.
- Gate current candidates sequentially and pin the first fully admissible host. Resume the wider anatomy survey only if the current set fails. Call the host admissible, never best.
- Reducing below ten injected units is not a casual fallback; it changes anchor comparability/collision load and needs a scientific amendment.

### Accepted no-manipulation control — Amendment 3 owed

Codex withdrew the replicate-stability proposal and accepted Claude's counter-proposal:

- P1 is a fixed, randomly seeded sixteen-template subset of the eligible region-unaware pool, chosen once to approximate the CA1 covariate spread and reused on the same exposure-balanced rota.
- P2 draws from the full eligible region-unaware pool and is matched to P1 using the same covariate procedure as the real control arm.
- Neither arm conditions on region, so the band remains a no-manipulation safety check.
- It mirrors finite-versus-large pool size, reuse, matching, clustering, and seed structure at the existing two-pseudo-arm sorter cost.
- It cannot mirror region homogeneity, because that is the real manipulation; state that boundary.

This is **not merely an implementation note** because current Slot 5 says pseudo-arms use the same selection procedure and P1/P2 intentionally do not. Amendment 3 must pin the subset seed/objective, selected template IDs, rota, matching procedure, no-region-conditioning rule, unchanged budget, and boundary.

## Host timing and remaining gates

Tracked timing index reproduces:

- 11 assets, 21 AP series;
- 54.1527–87.0831 min;
- 29,999.9969–30,000.2984 Hz;
- 384 channels for every series;
- 317,309,738 metadata bytes; and
- zero non-monotonic head/tail edge windows.

Duration passes for every current candidate and separates none. This proves a regular usable time base, not an absence of dropped samples.

**No host is pinned.** Remaining gates: drift, noise, post-rescaling effective SNR, ten-placement feasibility, and covariate balance. Codex owns the balance/manipulation gate.

## Anatomy-index provenance guard

Session 6 found that `survey_host_anatomy.py` and `screen_host_timing.py` could reuse a stored `target_band` while printing a different caller-supplied `--target`. That silent cross-target resume hazard is fixed:

- new anatomy records embed target and maximum gap;
- shared validator: `Reproducibility Packet/scripts/utils/anatomy_index.py`;
- the existing append-only index is legacy and must be asserted with `--legacy-index-target CA1 --legacy-index-max-gap-um 40`;
- a CA1 index replay requested as SUB now fails loudly; and
- compilation and a zero-new-read timing replay passed.

Do not rewrite the tracked append-only indexes to add metadata. The explicit legacy assertion is the provenance bridge.

## Injection/preprocessing order for Rung 0

Verified against SpikeInterface tag `0.104.8`, commit `76c41846f88de3cc9dc5858d5c7f97dd6cb1955f`:

- `generate_hybrid_recording()` passes the caller's recording directly to the injection extractor; it performs no preprocessing.
- The IBL donor builder extracts templates after float conversion → `phase_shift` → 1 Hz high-pass → common reference.
- The official hybrid tutorial injects into a preprocessed host.

**Rung 0 must build and pin the host injection substrate before injection.** Do not phase-shift the combined raw-host-plus-injected recording; that would transform already-phase-shifted donor spikes twice and real host spikes once. Record the exact chain and any later sorter-facing transforms.

SpikeInterface, PyTorch, and Kilosort4 are still not installed in the project venv. Current root pins remain `h5py==3.16.0` and `numpy==2.5.2`; resolve any numpy compatibility deliberately when Rung 0 installs, and re-run the metadata scripts after a pin change.

## Compute environment

Amendment 1 governs:

- target heavy work in the daytime; the other project targets overnight;
- the schedule is a convention, not a reservation;
- the earlier 3.46 → 3.96 → 1.01 → 0.89 GiB series came from leaked finished processes, not competing work;
- the process-leak fix was in progress, not confirmed landed;
- never reason from the shape of that old series.

Live guards are unchanged: measure RAM/VRAM immediately before every heavy step; use no more than 75% of then-free RAM/VRAM; preserve at least 4 GiB system RAM and 2 GiB VRAM; stop if crossed; never inherit a prior measurement.

## Director and public state

- Shared-memory director request: resolved and retired.
- Phase 1 contract review: open and non-blocking.
- No director action is needed for Amendments 2/3; those are agent review work unless a real disagreement recurs.
- `agents/Codex/Progress Reports/Progress Report Amendment Compute Schedule.md` is the required Amendment 1 director update.
- The root README's latest append-only entry corrects the unsupported rig/strain claim, records the accepted pseudo-control pending amendment, pins the injection-order decision, and states no result exists.

## What Codex should do next

1. Read Claude's next owner response before acting. Amendment 2 closes only on explicit approval of whole-file hashes `8d06e588…` / `9bb0478f…` or a new synchronized handoff.
2. Review Amendment 3 exact bytes separately; do not infer approval from the accepted intent.
3. Keep the Tier A chat active until the first fully admissible host is pinned and Amendments 2/3 converge.
4. Prepare Rung 0 without launching: pin the SpikeInterface 0.104.8 source/version decision, construct the pre-injection host substrate, choose the exact ~60 s segment, and write candidate sorter commands/monitoring.
5. Run Rung 0 only in the daytime window after fresh RAM/VRAM measurements pass all guards. Record runtime, peak RAM/VRAM, failures, per-tier 200-recording-minute projection, and whole-panel projection.
6. Keep surviving code inside `Reproducibility Packet/` with argparse, docstrings, no hard-coded paths, loud failures, and dependencies pinned at install.

`agents/Codex/Session Summaries/HumanReport6.md` contains the full evidence, decisions, file list, and reasoning.
