# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 11 · 2026-08-12 19:11 PDT**

**Next Codex session will be Session 12.** No count-based progress report is due until Session 16. Session 11 put Amendment 5 into force, so the required event-triggered report exists at `agents/Codex/Progress Reports/Progress Report Amendment Real Control Donor Exclusion.md`.

## Current phase and hard boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No template-array pull, dependency installation, raw-recording download, Rung 0 execution, hybrid generator run or sorter run occurred in Codex Session 11.

The public state remains `In Progress`. Contract repair, donor-pool diagnostics, packet self-containment and host screening are not evidence about whether realism changes measured sorter accuracy.

## Claim Sheet state

Current synchronized states after Amendment 5 entered force:

- `Claim Sheet.md`: SHA-256 `ac089232851705be86e8674987f29afd7fa553e0e55e08049868761549465b28`
- `Accessible Claim Sheet.md`: SHA-256 `8bae94bcc84928766214fea64eba234af6a524804afe11bd7eb16504d265c17f`

Amendments 1–5 are all `In force`.

Claude's Session 11 handoff states `d536b7d3f5d0c14015084c0ef5054bd7a5525ad6a22acc4d23f6bdcc480f698a` / `4eb76bafe4b60abc6af40f7ad3623e61a301386ec9eaaaf9c976ad6e7a84d9a0` received explicit Codex same-state approval. The current hashes differ only because the status/history lines were then changed from `Proposed` to `In force`.

## Amendment 5 — executable meaning

The real Tier A control excludes the injection zone's donor pool before matching. For the current CA1 recommendation, remove all sixteen matched-arm (`dataset`, `template_index`) pairs.

The eventual real-arm matching rule must:

1. be fully fixed before the eligible host-specific pool is visible;
2. contain no term referencing region in either direction;
3. run once without generation on the un-removed pool and once on the post-removal pool;
4. report for both states the selected pairs, realized zone count, per-covariate balance/objective, provenance-blocking granularity, relaxations and infeasibility;
5. permit only the post-removal state to govern generation.

The uniform unpaired region-blind expectation (0.117 zone donors, P at least one 0.111) prices departure from the anchor-like sampling policy. The fixed-rule before/after counterfactual will price removal under this project's matched policy. Both must be reported.

The composition check is 16/16 CA1 in the matched arm and 0/16 in the control. It does not replace Slot 11.3's waveform-separation and nuisance-balance manipulation gate. Slot 12.3 still controls: if post-removal matching cannot satisfy balance, placement and provenance inside required strata, Tier A fails.

Amendment 5 explicitly supersedes only Amendment 3's now-false statement that the pseudo band does not mirror chance zone donors the real control may contain. Both the real control and pseudo-arms now use the final eligible region-unaware pool minus the zone donor pool on this property. The remainder of Amendment 3's boundary still holds, especially that the pseudo control cannot mirror the matched arm's region homogeneity.

## Tier A selection artifact

Active chat: `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`.

Artifact: `agents/Claude/Tier A Host and Injection Zone Selection.md`.

Draft 7 SHA-256 `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01` has explicit same-state approval from Claude and Codex for its declared strategy/evidence scope. Sections 1–13 retain the previously reviewed strategy and diagnostics; §14 carries Claude's independent re-derivation of the no-reuse baseline, the paired-versus-unpaired expectation distinction, and the contract supersession finding.

This is still **not** a pinned-host selection. Candidate order remains:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Drift, noise, post-rescaling effective SNR, placement calibration and the independent balance/manipulation gate remain open.

## Matching-rule and configuration gates stay separate

Amendment 5 approval opens the real-arm matching-rule lane. It does not approve a rule. The rule must be deterministic, provenance-aware and host-blind at the time it is fixed, with explicit objective, blocking/fallback order, tie handling, failure semantics and relaxation reporting.

After a host exists, a separate exact-state configuration approval remains required for the real arms and for Amendment 3's pseudo selector. Pool digests/filters, removed pairs, selected pairs, achieved distances, evaluated swaps and stop reason must be pinned before generation. None of this is authorized by the Amendment 5 close.

## Reproducibility Packet review

Claude Session 11 added `Reproducibility Packet/README.md`, `DATA.md`, `requirements.txt` and `.gitignore`, then tested a copy of the packet alone in a fresh environment. Five offline steps reproduced tracked outputs; five archive-reading steps are explicitly labelled not re-run. The Slot 8 verifier is correctly described as absent because no results exist.

Codex's general recent-work review found one public-boundary defect: the runbook/data guide said `validate_ccf_label_map.py` validates the newly derived map, but the code deliberately calls the hand-authored layer only. It validates the pre-existing core long-name/acronym table and the `depth_along_probe` / NWB `rel_y` coordinate agreement. Scoring derived entries against their own source votes would be circular.

Codex corrected and explicitly approved:

- `Reproducibility Packet/README.md`: SHA-256 `1a32418c7cd3a32ecf4f6ef2960dcbf48beae45e4cd9d3b2ea2e071fdc434cf1`
- `Reproducibility Packet/DATA.md`: SHA-256 `f8c6ce266f368e0efe6d2ecaafbeca09813d2420acd27999433cd61c0c435e09`

Claude owner re-review is open in `chats/Claude-Codex/Reproducibility Packet Review/Reproducibility Packet Review - Active.md`. The packet script docstrings still use project-root-relative examples rather than packet-root-relative commands; Claude already recorded that as a later handoff item.

## Rung 0 boundary retained

Rung 0 remains unrun. It must construct and pin the pre-injection host substrate, avoid phase-shifting injected templates twice, pin the exact approximately 60-second segment, finish both placement calibrations, resolve dependencies deliberately in the project venv, take fresh RAM/VRAM immediately before heavy work, and obey the 75%-of-free cap plus 4 GiB RAM / 2 GiB VRAM floors within the daytime convention.

The current project venv still pins only `h5py==3.16.0` and `numpy==2.5.2`. Re-run metadata utilities after any dependency change.

## Public and director state

- Root `README.md` remains State A / `In Progress`; its latest log records Amendment 5 entering force and says the matching rule, host, generation and result remain open.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- The Amendment 5 event-triggered progress report is complete.

## Validation record from Session 11

- Exact handoff hashes matched before review.
- Offline zone-enrichment replay reproduced 2,183/16 and 1,149/12 pool counts plus realized/expected 3/0.11, 8/1.03, 2/0.12 and 5/1.17.
- Independent unpaired arithmetic reproduced expectation 0.117270 and P(at least one) 0.111401.
- All 17 packet Python sources parsed.
- The Tier A chat append preserved the 707-line prefix, added the Session 11 header exactly once after that boundary, and ended at 736 lines.
- `git diff --check` passed before closeout.

## What Codex should do next

1. Read Claude's owner response to the packet README/DATA hashes first; keep that packet review open until the same exact state is approved.
2. Begin the real-arm matching-rule artifact only after re-reading Amendments 2 and 5 together. Fix the complete rule before inspecting any host-specific eligible pool.
3. Keep matching-rule approval, host selection, host-dependent exact configuration, Rung 0 resource admission, manipulation/balance approval, generation and sorter execution as separate gates.
4. Do not pin a host or launch Rung 0 until all prerequisites and immediate daytime resource guards pass.

`agents/Codex/Session Summaries/HumanReport11.md` contains the full review evidence, packet correction, validation record and file list.
