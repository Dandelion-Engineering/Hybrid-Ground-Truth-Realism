# Codex — Workspace

This directory contains Codex's work for the **Hybrid Ground Truth Realism** project.

## Folder map

```text
agents/Codex/
├── README.md
├── Summary of Only Necessary Context.md
├── Literature Foundation.md
├── Tier A Real-Arm Donor Matching Rule.md
├── references.md
├── tools/
│  └── probe_draft16_safety_claims.py
├── Session Summaries/
│  ├── HumanReport1.md … HumanReport22.md
│  └── HumanReport23.md
└── Progress Reports/
   ├── Progress Report Phase 1 Close.md
   ├── Progress Report Amendment Compute Schedule.md
   ├── Progress Report Session 8.md
   ├── Progress Report Amendment Real Control Donor Exclusion.md
   └── Progress Report Session 16.md
```

## What each file owns

- **`Summary of Only Necessary Context.md`** — authoritative next-session continuity, rewritten at every closeout.
- **`Literature Foundation.md`** — Codex's dated and frozen Phase 0 field survey.
- **`Tier A Real-Arm Donor Matching Rule.md`** — same-state-approved pre-pool specification for the deterministic real-control donor matcher. Claude and Codex explicitly approve Draft 6 SHA-256 `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`. It uses one fixed target manifest, `N = 10…16`, full-sixteen Z removal, two-level provenance-count equality at every stage, and a separate exact exposure-schedule/placement-specification gate before any host-specific manifest or pool. This is not an implementation, pool, configuration, balance verdict, or execution authorization.
- **`references.md`** — Codex's living source ledger and transferable citations.
- **`tools/probe_draft16_safety_claims.py`** — deterministic synthetic review probe showing that label-blind unit expansion and retaining a first bin do not have the one-way safety guarantees claimed in Claude Draft 16. It reads no candidate asset.
- **`Session Summaries/HumanReport<N>.md`** — permanent detailed session reports for the director.
- **`Progress Reports/`** — director-facing reports triggered by phase changes, approved amendments, and the eight-session cadence. The newest is the Session 16 count-based report. The next count-based report is Session 24.

## Shared work outside this folder

- `chats/Claude-Codex/Phase 0 Literature Comparison/`, `Claim Sheet Review/`, `Study Guide Pass 1 Review/`, `Compute Environment Update/`, `Reproducibility Packet Review/`, and `Tier A Donor Matching Rule/` are concluded.
- `chats/Claude-Codex/Tier A Selection Review/` is active. Section 15's thirteen-host order remains same-state approved. Claude Draft 20 correctly denied the per-unit values a unit-level null, but promoted its homogeneous fixtures into the unsupported claim that the band `Q95_null` is systematically narrower than one trace. Codex Draft 21 removes that direction: a quiet heterogeneous counterexample gives one valid flat unit `0 µm` against band `Q95_null = 16.598 µm`, so the statistics have no fixed ordering and cannot grade one another. Codex explicitly approves Draft 21 SHA-256 `bd0f678af4d27862d55044be010524782d1d80bb2bccd6a873cc06e70fa3946c`, utility SHA-256 `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063`, and harness SHA-256 `fe889703d67b4ee97a9a6a431dbd9dde389216687f07b139db34f0e2df5c317d`; Claude genuine owner re-review is open on all three. No archive CLI or candidate value exists.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` are synchronized at SHA-256 `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365` / `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. Amendments 1–6 are `In force`. The matching-rule prose, implementation/tests, host-dependent exact configuration, and manipulation gate remain separate approvals.
- `Study Guide/Pass 1 - Conceptual Foundation.tex` and PDF are approved Phase 1 artifacts. Pass 2 remains a Phase 3 deliverable.
- `director_requests.md` contains one open non-blocking Phase 1 contract-review item. No new director action is needed.
- Root `README.md` is the append-only public live-run page. Codex Session 23 appended a forward correction stating that the band null and individual audit values have no fixed ordering; heterogeneity may expose a limitation but cannot attribute movement, and no audit value reaches a gate or candidate result.
- The Reproducibility Packet is co-owned. Its design-stage runbook remains same-state approved at ten steps. Codex owns Rung 0, the sorter-panel decision, inference/negative-control harness, Tier A's independent balance/manipulation gate, and the two-part placement calibration.

## Current technical boundaries

- Rung 0 must build and pin the host injection substrate before injection because donor templates already carry `phase_shift` and SpikeInterface 0.104.8 does not preprocess inside `generate_hybrid_recording()`.
- Pre-rescaling scale factor is an integrity diagnostic, not a matching covariate.
- Same-state-approved matcher Draft 6 uses common U-derived scaling for amplitude/effective-SNR/depth, donor-equal global no-reuse assignment, and no region term. It computes T and `N` once from a pinned target manifest, preserves the full sixteen-key Z removal, makes joint block-placement failure reject the host, and tests exact insertion/session/subject-count equality before falling back at the same provenance stage to the contract's literal insertion-count floor.
- Before T is measured or any host-specific manifest/pool is opened, an exact exposure-schedule/placement specification and synthetic tests must pin the nuisance seed, amplitude target, and commanded-placement construction. Matcher implementation/test review follows as another same-state gate.
- The derived CCF label layer is opt-in; recognized white-matter/fibre-tract labels remain non-injectable. Any non-CA1 zone change must define the removal set across parent/descendant labels before matching.
- The drift gate's numerical logic remains unchanged and validated; Draft 21's changes are interpretation/documentation plus one permanent counterexample. Claude must owner-approve Draft 21 `bd0f678a…`, utility `3420dec1…`, and harness `fe889703…` before the archive CLI is written. The future reader must confirm ragged time/depth alignment, finite per-spike depths, exact-asset session-time provenance and containment, and valid same-probe `max_electrode -> rel_y` mappings; preserve full unit identifiers/quality labels; and report whole, own-worst-window and band-aligned per-unit excursions with starts/support. Those values have no unit null and cannot be graded against band `Q95_null` or `L`; heterogeneity remains a non-voting limitation flag. The module fails loudly on malformed unit collections, duplicate row IDs and invalid audit windows; 79 synthetic checks pass at all 200 permutations.
- `.gitattributes` makes repository-wide checkout bytes explicit and is same-state approved by both agents. All paths default to `-text`; 17 framework files and 11 legacy packet outputs intentionally reconstruct CRLF. A temporary `core.autocrlf=true` clone matched all 153 reviewed tracked files byte-for-byte.
- No host is pinned, no candidate drift value has been read, and no dependency install, raw-data read, Rung 0, generation, or sorter run has occurred.

For resumption, read `Summary of Only Necessary Context.md`, then the latest human report. Use `references.md` rather than memory for citations.
