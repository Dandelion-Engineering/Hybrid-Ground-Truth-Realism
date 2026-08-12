# Human Report 5 — Codex

**Date and time:** 2026-08-11 20:16 PDT

**Session:** Codex Session 5

**Phase at start:** Phase 2 — Execution

**Phase at end:** Phase 2 — Execution. Tier A's host-selection strategy and CA1 injection-zone recommendation have Codex's exact-state reviewer approval; Claude's owner re-review and the resulting contract amendments remain open. No host has been pinned.

---

## Summary

This session completed the independent review Claude requested for Tier A host and injection-zone selection. The most important outcome is a narrower and more defensible state than the handoff initially claimed:

- **CA1 is approved as the first injection-zone choice.** Its joint fit with Tier C's existing biological evidence outweighs the extra donor headroom available in SUB. The project should not commission a SUB literature task unless CA1 fails an actual gate.
- **The host is not selected yet.** Claude's document supplied a provenance rule, a CA1 recommendation, and candidate recordings, but it did not pin a DANDI asset or that host's exact trajectory mapping. I retitled and re-scoped the artifact so it no longer presents a strategy as a completed selection.
- **Subject-level host separation is approved.** The host must come from one of the 127 DANDI 000409 subjects absent from the donor library, making insertion-, session-, and subject-level leakage exclusions vacuous simultaneously.
- **The sixteen-donor CA1 ceiling changes the design.** Five blocks remain the initial tranche, but donor exposure must be balanced over the complete sixteen-template CA1 library. The resulting statement is conditional on that finite library; more seed/placement blocks cannot create new donor diversity.
- **Tier A's negative control needs a tier-specific amendment.** Its pseudo block should replicate the full CA1-versus-region-unaware contrast so the diagnostic preserves the small-pool/large-pool asymmetry. The band then measures replicate stability, not the current same-condition no-manipulation null. The agreed Claim Sheets are unchanged until a synchronized dated amendment is written and approved.

The reviewed artifact is now:

`agents/Claude/Tier A Host and Injection Zone Selection.md`

SHA-256 `c7299cea9b8589dfb894c751d7cd402208db9f29b2fd38b18d1f1e969461a9bf`

I explicitly approved those bytes **as the Tier A host-selection strategy and CA1 injection-zone recommendation**, not as a pinned-host selection. The active review remains open until Claude genuinely re-reviews the edits and explicitly approves those exact bytes or returns a new state.

## Verification performed

### Reproduced the central counts

I independently checked the pinned CSV and DANDI asset listing rather than relying on the prose summary:

- 2,183 Neuropixels 1.0 donor rows;
- 37 donor insertions, 24 sessions, and 12 subjects;
- 2,048 DANDI assets, including 459 raw and 459 processed ecephys files across 139 subjects;
- 429 raw host recordings outside the twelve donor subjects;
- 16 total CA1 donors, 12 inside the provisional amplitude/SNR caliper;
- CA1 subject composition: KS044 5, KS046 2, KS051 6, KS055 3;
- fifteen of the sixteen CA1 donor depths lie from 2,640 to 2,920 µm; and
- all four provisional-caliper exclusions are the high-amplitude/high-SNR KS044 donors described in the handoff.

Every CA1 source insertion has non-CA1 control candidates in the pinned snapshot. Even after the provisional caliper, the four CA1 source insertions retain 33, 6, 42, and 30 non-CA1 donors respectively. That makes exact source blocking a real balance strategy rather than an abstract preference, although waveform, effective-SNR, geometry, and placement gates can still reject individual pairs.

### Audited the anatomy-bridge claim against upstream source

The handoff described the 1,401/1 label-map result as independent validation. The result itself is real, but the independence claim was too broad.

The upstream `hybrid_template_library` builder takes `brain_area` from IBL sorting metadata and constructs templates after its own high-pass/common-median preprocessing. Its consolidation code derives `depth_along_probe` from each template's best-channel probe coordinate. The NWB electrode table is another representation of the same IBL anatomical system. Comparing them is therefore a strong internal-consistency test of our hand-authored long-name/acronym bridge and coordinate compatibility, but it is not an independent validation of IBL atlas registration.

I edited the artifact accordingly. I also recorded that the validator attempted 37 insertions but only 32 produced testable probe assignments; five produced no testable comparison. The ACAd5 33/34 outcome is compatible with a boundary effect, not proof of one. CA1 remains clean at 16/16 among testable comparisons.

### Found the duration metadata instead of assuming 30 kHz

The host survey looked only for `starting_time`, but these raw NWB ElectricalSeries use an explicit `timestamps` dataset. On pinned asset `sub-NYU-46/...64e3fb86...`, the first two timestamps imply 30,000.1047 Hz and the endpoints imply 4,033.743 s. That read transferred 19.2 MB because the last timestamp sits in a distant chunk.

The efficient next step is not to add that cost to all 429 anatomy candidates. Read timing only for candidates that survive the anatomy screen, re-index those candidates, and then apply the duration gate. The artifact now records that path.

### Hardened the remote NWB reader

Reviewing `Reproducibility Packet/scripts/utils/remote_hdf5.py` found that retry logic handled connection failures but did not validate the HTTP response. If a server ignored `Range`, the reader could begin transferring an entire 18–197 GB object; if a response was short, it could cache incomplete bytes.

I added pre-read validation for HTTP 206 and the exact `Content-Range` prefix, bounded each body read to the requested length plus one byte, and checked the final payload length, with malformed/short responses entering the existing bounded retry path. I also made the request counter count actual attempts and the byte counter count completed response bodies.

A live post-change read against the pinned NYU-46 asset succeeded: 384 electrodes, 6 range requests, 5,569,540 bytes transferred. No recording data was loaded.

## The three review rulings

### 1. Exclusion and provenance

Choose a host subject absent from the donor library and report the remaining shared-dandiset limitation. Within the donor arms, attempt exact source blocking at insertion, then session, then subject granularity. Merely matching the number of contributing source datasets is too weak when the source identities are known. Any relaxation must be explicit and justified.

### 2. Blocks and negative control

Keep the five-block initial tranche, but replace unconstrained donor draws with a seeded exposure-balanced schedule: fifty CA1 selections across five ten-slot blocks means each of sixteen donors appears three or four times. Randomize slot assignment, spike-time seeds, and placement seeds inside that schedule; keep repeated donors in one bootstrap cluster.

For Tier A, make each pseudo block an independently seeded replicate of the complete CA1-versus-region-unaware contrast, then form the diagnostic band from differences between real and pseudo interaction estimates. That preserves both pool sizes inside the already budgeted two pseudo-arm runs. It is a replicate-stability diagnostic and therefore needs an explicit tier-specific Claim Sheet amendment.

### 3. Zone and search strategy

Use CA1 first. Apply the remaining duration, drift, noise, effective-SNR, placement, and covariate-balance gates sequentially to the current candidate set. Pin the first host that passes every gate and call it an admissible host, not the best host. Resume the 429-recording anatomy survey only if the current candidates fail. This is the smaller sufficient search and avoids paying for a census that changes no decision.

The fallback order is now SUB plus primary Tier C evidence, then depth-specific zones through amendment, then the already-declared Tier A failure. Lowering the arm below ten injected units is not a casual first fallback because ten-unit density is part of the anchor comparison and collision load.

## Compute-environment decision

Claude relayed Randy's answer: the earlier low-memory series came from leaked finished Claude automation processes, not active research contention. Randy cleared them and set a day/overnight schedule: this project runs during the day and the other project overnight. The process-leak fix is being built, not yet established.

I agreed that the live admission rules remain unchanged and disagreed that no amendment is needed. Slots 4 and 10 currently state that other projects run at the same time, are uncoordinated, and have no schedule. I requested a synchronized factual amendment to the technical and Accessible Claim Sheets that records the day/overnight allocation and leak explanation while preserving the 75%-of-free and 4 GiB RAM / 2 GiB VRAM floors. Exact-state approval is open until those bytes exist.

No sorter, generator, recording download, dependency install, or heavy compute ran this session. The only remote data reads were bounded NWB metadata range reads. Because no heavy step was launched, no inherited memory measurement was used as an admission decision.

## Challenges and reasoning paths

**The document's evidence was better than its status.** The provenance and CA1 work was substantive, but a candidate list is not a pinned host. The fix was not to reject the evidence; it was to approve it at its true scope and leave host pinning open.

**The negative control could not ignore the finite-pool asymmetry.** A same-condition pseudo pair drawn only from one arm would measure one pool's instability while the real contrast uses two radically different pools. Replicating the full contrast keeps the two pseudo sorter runs already budgeted and directly measures whether the interaction reproduces under independent nuisance draws.

**More anatomy screening was not automatically more rigor.** Once the current screen showed many usable CA1 bands, a 429-recording census would mostly buy a “best” claim the project does not need. Sequential admissibility is cheaper and more honest.

**A successful validator can still overclaim what it validates.** The label bridge agrees impressively with upstream records, but the upstream construction path shows why that is not independent biological truth. The result remains useful after the claim is narrowed.

## Files created or updated

| Path | Change |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Reviewer edits, scope correction, validation boundary, fallback correction, duration finding, and three explicit rulings; approved by Codex at hash `c7299cea…`; owner re-review open. |
| `Reproducibility Packet/scripts/utils/remote_hdf5.py` | Added strict Range-response validation and bounded retry of malformed or short responses; live metadata read passed. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only review handoff with exact hash, edits, rulings, approval, and remaining owner gate. |
| `chats/Claude-Codex/Compute Environment Update/Compute Environment Update - Active.md` | Append-only reply requesting a synchronized factual environment amendment. |
| `agents/Codex/references.md` | Added upstream IBL template-construction, consolidation, and extractor sources and how they bounded the review claim. |
| `agents/Codex/README.md` | Updated workspace tree, active review states, and director-request status. |
| `agents/Codex/Summary of Only Necessary Context.md` | Completely rewritten for Session 6. |
| `agents/Codex/Session Summaries/HumanReport5.md` | This report. |

The root Live-Run README was checked and left unchanged. This session did not finish the Tier A selection, close a phase, or approve an amendment; publishing a heartbeat entry would overstate an open review.

## Next steps

1. Claude genuinely re-reviews the exact Tier A strategy bytes and either approves hash `c7299cea…` or edits and returns a new state.
2. Claude authors synchronized dated technical/Accessible Claim Sheet amendments for the Tier A provenance rule, Tier A replicate-band construction, and the day/overnight compute context. Codex exact-state review remains required.
3. After those gates, Claude pins the first fully admissible CA1 host from the current candidate set; Codex independently applies the balance and manipulation gates.
4. Codex prepares and runs Rung 0 separately, during the daytime window and only after a fresh RAM/VRAM measurement satisfies the existing guards.
