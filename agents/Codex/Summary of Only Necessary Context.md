# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 12 · 2026-08-12 21:18 PDT**

**Next Codex session will be Session 13.** No count-based progress report is due until Session 16.

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No host-specific eligible pool or rendered matching edge table exists. No template-array pull, dependency installation, raw-recording download, Rung 0, hybrid generator run, or sorter run occurred in Codex Session 12.

The public state remains `In Progress`. A packet repair and a pre-pool matching-rule draft are design/reproducibility work, not evidence about whether realism changes measured sorter accuracy.

## Claim Sheet state

The synchronized contract remains unchanged:

- `Claim Sheet.md`: SHA-256 `ac089232851705be86e8674987f29afd7fa553e0e55e08049868761549465b28`
- `Accessible Claim Sheet.md`: SHA-256 `8bae94bcc84928766214fea64eba234af6a524804afe11bd7eb16504d265c17f`

Amendments 1–5 are all `In force`. Amendment 5 removes the injection zone's donors from the real Tier A region-unaware pool, requires the frozen matcher to run on both un-removed and post-removal pools, and permits only the post-removal state to govern generation. Its uniform unpaired expectation and fixed-rule counterfactual answer different questions and both must be reported.

No amendment moved this session.

## Packet review — Claude's next move

Active chat: `chats/Claude-Codex/Reproducibility Packet Review/Reproducibility Packet Review - Active.md`.

Claude Session 12 correctly made every packet script's `--help` example packet-relative and added `scripts/check_runbook_consistency.py`. Codex accepted the two design choices:

1. retain runnable examples in every script docstring so `--help` is sufficient;
2. keep the checker as the single hard-coded non-step exception, which is more fail-closed than a self-declared marker.

Codex found and repaired two defects before approval:

- the packet README named an `agents/Claude/...` path, contrary to the outsider-clean packet boundary; the agent path and three older session-history phrases in packet docstrings are gone;
- the checker read only the first line of a runbook command fence and did not enforce unique/contiguous step numbering. It now reads through the closing fence, requires exactly one command line, rejects unclosed fences and duplicate/gapped numbering, validates path kinds, and prints clean parser errors.

The mutation harness now catches 13 of 13 deliberate defects, including a second README command, duplicate step number and numbering gap. All eleven packet scripts compile; all eleven `--help` pages render; the live checker passes ten steps. No result or command changed.

Key handed states awaiting Claude owner re-review:

- packet `README.md`: `00acb8262cee63816a80c9737a0ca1bd3a7a33374347183bcca77b444af4c835`
- checker: `094fbff10b7fa33c441b88926042c494c4a0706b0b41b4e7f9bf25caa6e16c00`
- `audit_template_library.py`: `0f98f195a49498096a1cf24fea6e5492a18cdda50cbc2893f2aaf88d75d2bb87`
- `derive_ccf_label_map.py`: `b0b33ce2515d0504f3ebcbbe8606d9ccfef31d428301314121cecf1769a6cd55`
- `screen_host_timing.py`: `bb6681ca6762139832f204fa3ee0256252c2f9bdb0323f74e6b6b856211f2ab5`
- `audit_amplitude_conventions.py`: `7b82543266f3ea4800a1aeac31733e872106ef3bd46d56c2a6e0b27517629fce`
- Claude mutation harness: `3b5a36a9fa46ef91a5b60ad71cd803e3835bf7cecd925087271e8a7864d91627`

The other six handed step scripts stayed at Claude's hashes and were explicitly approved. `DATA.md` remains already approved and unchanged.

## Real-arm matching rule — Claude's next move

Artifact: `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`

Active chat: `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md`

Draft 1 SHA-256: `1243742131b39dadde8fe86240d718f07d196826186a748e0344085344c1ee3f`

Codex explicitly approves Draft 1 as a **pre-pool prose specification only** and has handed it to Claude for exact-state review. Nothing has been implemented and no data pool has been inspected.

Draft 1 fixes:

- globally unique (`dataset`, `template_index`) keys;
- target pairing once over the sixteen donors, reused across their fixed fifty-occurrence exposure rota;
- an edge-occurrence input because realized amplitude, effective SNR, depth and feasibility can depend on placement;
- U = un-removed eligible pool, Z = zone donors, R = U minus Z;
- one U-derived float64 scaling ruler for both U and R counterfactual runs;
- exactly three equal-weight soft quantities: realized post-rescaling peak-to-peak amplitude, effective host SNR, realized depth along band;
- geometry/placement as hard gates; waveform footprint/shape excluded from matching because they help constitute the manipulation; scale factor diagnostic only;
- no anatomical-label input or region term;
- feasibility-only provenance stages: insertion → session → subject → exact source-count floor; no unrestricted fifth stage;
- global one-to-one assignment, preserving insertion/session/subject matches before total cost, maximum edge cost and lexical key ties;
- loud failure and complete reporting;
- matching output separate from the independent balance/manipulation verdict.

Three choices are explicitly flagged for Claude to resist:

1. whether the source-count floor is exactly the target set's number of distinct `dataset`/insertion sources;
2. donor-equal matching cost over each donor's three/four occurrences while exposure-weighted balance is separately reported;
3. common U-derived scaling for direct un-removed/post-removal comparison.

Critical timing gate: after the prose converges, the implementation and deterministic tests must also receive same-state approval **before** constructing or opening any host-specific pool or edge table. The future matching implementation must become a numbered packet step once finalized; it may not be added as a silent checker exception.

## Host selection and Rung 0 remain unchanged

`agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 7 at `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01` is same-state approved for its declared strategy/evidence scope, not as a host selection.

Candidate order remains:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Claude still owns drift, noise and post-rescaling effective-SNR host gates. Codex still owns the two-part footprint/placement calibration, independent balance/manipulation gate, Rung 0, sorter-panel decision and inference/negative-control harness.

Rung 0 remains unrun. It must construct and pin the pre-injection host substrate, avoid phase-shifting injected templates twice, pin the exact approximately 60-second segment, resolve dependencies in the project venv, and take fresh RAM/VRAM immediately before heavy work under Amendment 1's live resource guards. The current venv still pins only `h5py==3.16.0` and `numpy==2.5.2`.

## Gate order — do not collapse

Keep these distinct:

1. packet review convergence;
2. matching prose-specification convergence;
3. matching implementation/test convergence before pool access;
4. host selection and placement calibration;
5. exact U/Z/R manifests, edge table, two matching outputs and selected IDs;
6. independent Tier A balance/manipulation approval;
7. generation authorization;
8. Rung 0/sorter execution authorization.

Reviewer edits, downstream use, a later commit, or silence do not substitute for same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. The new lean entry says the pre-pool matcher is drafted and under review; no donor/host/generation/result exists.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- No progress report was due in Session 12.

## Validation and machine record from Session 12

- Packet checker: ten steps pass.
- Mutation suite: clean control passes; 13 of 13 mutations caught.
- All eleven packet Python files compiled and rendered `--help`.
- Packet text audit found no agent/Station reference after repair.
- Append-only packet chat preserved its exact 13,223-byte / 127-line prefix and added the Session 12 header exactly once after that boundary.
- `git diff --check` passed before closeout.
- 2026-08-12 21:18 PDT: 11.51 GiB RAM free of 31.67; 981 MiB VRAM used of 16,311; 604.4 GB free on `C:`. Nothing heavy ran.

`agents/Codex/Session Summaries/HumanReport12.md` contains the full review rationale, hashes, matching specification decisions, validation evidence and file list.
