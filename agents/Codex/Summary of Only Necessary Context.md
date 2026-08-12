# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 5 · 2026-08-11 20:16 PDT**

**Next Codex session will be Session 6.**

## Current phase

**Phase 2 — Execution is open.** No sorter run, generator run, recording download, dependency install, or scientific accuracy measurement occurred in Codex Session 5.

Phase 1 remains closed. The approved technical Claim Sheet, Accessible Claim Sheet, and Study Guide Pass 1 exact states remain the governing contract until dated amendments receive same-state approval.

## Approved Phase 1 exact states

- Technical `Claim Sheet.md`: `a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3`
- `Accessible Claim Sheet.md`: `73bff8f81dc2e31b47d4abbe1f61c8106a34dccb8ea6457051c3dba84a589760`
- Study Guide source: `d33e74d73c41b3ef0b4edbe6de52c0cc4e5597bae2d048618edb5c4523f99819`
- Study Guide PDF: `75e1423294cb3c4695c14920851825d602379d9ffca1aab6bcb93cbd10d998a3`

Do not treat the proposals below as amendments already in force.

## Tier A review state

Active chat:

`chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

Artifact:

`agents/Claude/Tier A Host and Injection Zone Selection.md`

Current SHA-256:

`c7299cea9b8589dfb894c751d7cd402208db9f29b2fd38b18d1f1e969461a9bf`

**Codex explicitly approves these bytes as a host-selection strategy and CA1 injection-zone recommendation. Claude's owner re-review is open.** The review does not close until Claude re-opens the artifact and either approves this exact hash or edits and returns a new state.

**No host is pinned.** The original handoff overstated its scope. The artifact supplies provenance evidence, approves CA1 as the first zone, and gives candidate recordings. A completed selection still needs a DANDI asset identifier, its exact anatomical mapping, adequate duration, drift/noise/effective-SNR checks, ten-placement feasibility, and the independent balance gate.

## Tier A rulings

### Exclusion and balance

- Select a host from a subject absent from the donor library's twelve subjects. This makes insertion/session/subject host leakage exclusions vacuous.
- Report the residual shared-dandiset/IBL/NP1 provenance boundary; subject separation is not independence.
- Within donor pairs, attempt exact provenance blocking at insertion, then session, then subject granularity. Matching only the number of sources is too weak when identities are available.
- The pinned snapshot has non-CA1 candidates in every CA1 source insertion, including inside the provisional caliper; exact blocking is plausible but still subject to waveform/effective-SNR/placement balance.

### Sixteen-donor pool and blocks

- CA1 has exactly 16 NP1 donors, 12 inside the provisional caliper. Fifteen lie from 2,640–2,920 µm; the outlier is at 1,860 µm.
- Keep five blocks as the initial tranche, but use a seeded exposure-balanced donor schedule: 50 matched selections means each CA1 donor appears three or four times.
- Keep repeated donor identities in the same bootstrap cluster.
- The donor-population result is conditional on the complete sixteen-template CA1 library. More blocks add seed/placement precision, not new donor diversity.
- For Tier A only, each pseudo block should independently replicate the full CA1-versus-region-unaware contrast. Form the replicate-stability band from the difference between real-block and pseudo-block interaction estimates. This preserves the small/large pool asymmetry inside the already-budgeted two pseudo-arm runs.
- That band is not the current no-manipulation null diagnostic. It requires a dated Claim Sheet amendment before Tier A execution.

### CA1 and host search

- CA1 is the first zone. Do not commission SUB evidence unless CA1 fails an actual gate.
- Do not finish a 429-recording anatomy census merely to claim “best.” Apply the remaining gates sequentially to the current candidates and pin the first fully admissible host. Call it admissible, not best.
- Resume the survey only if the current set fails.
- Fallback order: SUB plus primary Tier C evidence; depth-specific zones through amendment; then the already-declared Tier A failure.
- Lowering below ten injected units is not a default fallback; ten-unit density is a contract commitment tied to anchor comparability and collision load.

## Supporting evidence and code state

Verified against pinned local artifacts:

- 2,183 NP1 donors; 37 insertions; 24 sessions; 12 subjects;
- 2,048 DANDI assets; 459 raw; 459 processed; 139 subjects;
- 429 raw candidate hosts outside donor subjects; and
- exact 16/12 CA1 total/in-caliper counts.

The CCF bridge check is now bounded correctly. It is an internal consistency check across IBL-derived representations, not independent atlas validation. Thirty-two of 37 donor insertions produced testable assignments; five did not. Among 1,403 testable comparisons: 1,401 agree, 1 disagrees, 1 has an unmapped host label. CA1 is 16/16.

The missing duration metadata lives in each AP series' `timestamps`, not `starting_time`. On pinned NYU-46 asset/session `64e3fb86`, the first two timestamps imply 30,000.1047 Hz and the endpoints imply 4,033.743 s. Read timing only for anatomy-screened candidates rather than transferring timestamp chunks for all 429 assets.

`Reproducibility Packet/scripts/utils/remote_hdf5.py` now rejects ignored, malformed, and short Range responses and retries them. Live post-change test: one 384-channel electrode table, 6 requests, 5,569,540 bytes.

Codex's `references.md` now records the upstream IBL template builder, metadata consolidator, and `IblSortingExtractor`, including the donor high-pass/common-median path and the origin of `brain_area`/depth metadata.

## Open amendment gates

Claude was asked to author synchronized dated amendments to both Claim Sheets for:

1. the Tier A host-exclusion and donor-provenance balance rule;
2. Tier A's full-contrast replicate-stability band; and
3. the compute environment's day/overnight allocation and leaked-process explanation.

Codex has approved the amendment intents, not any exact bytes. Review exact technical and Accessible states before approval. Execution must not silently follow changed rules while the old contract remains authoritative.

## Compute environment

Randy resolved the shared-memory request:

- the earlier 3.46 → 3.96 → 1.01 → 0.89 GiB series came from finished Claude automation processes that had not exited, not active research work;
- those processes were cleared;
- a process-leak fix is being built, not confirmed landed; and
- this project runs during the day, while the other research project runs overnight.

The live guard is unchanged:

- measure free RAM and VRAM immediately before every heavy step;
- use no more than 75% of then-free RAM or VRAM;
- preserve at least 4 GiB system RAM and 2 GiB VRAM;
- stop and record a resource failure if a guard is crossed;
- never inherit an earlier quiet-window measurement; and
- use only `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`, with dependencies pinned at first install.

The active compute chat is:

`chats/Claude-Codex/Compute Environment Update/Compute Environment Update - Active.md`

Codex requested an amendment because Slots 4 and 10 still say projects run simultaneously without coordination or schedule. The amendment should correct those facts without relaxing any guard or changing the capacity ladder.

## Director requests

- Shared-memory request: **resolved and retired** in `director_requests.md`.
- Phase 1 contract review: **open and non-blocking**. Any response is the first amendment cycle.

## What Codex should do next

1. Read Claude's newest report and both active chats before replying.
2. Review Claude's genuine owner response to Tier A hash `c7299cea…`; close only on explicit same-state approval.
3. Review the synchronized technical/Accessible amendment bytes separately. Do not infer approval from intent or edits.
4. Continue Rung 0 preparation independently of Tier A: identify the exact ~60 s host segment and candidate sorter commands before launch.
5. Run Rung 0 only during the daytime window and only after fresh RAM/VRAM measurements pass the admission guards. Record runtime, RAM/VRAM peaks, failures, and projected 200-recording-minute per-tier plus whole-panel cost under the currently approved contract unless an amendment changes that budget.
6. Write surviving code directly inside `Reproducibility Packet/`, with `argparse`, docstrings, no hard-coded paths, loud failures, and pinned dependencies.

`agents/Codex/Session Summaries/HumanReport5.md` contains the full review evidence and reasoning.
