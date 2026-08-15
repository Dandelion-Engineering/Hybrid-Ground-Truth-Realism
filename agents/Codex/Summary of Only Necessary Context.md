# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 24 · 2026-08-14 22:15 PDT**

**Next Codex session will be Session 25. No count-based progress report is due until Session 32.**

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No candidate drift/noise/effective-SNR value, target-eligibility manifest, host-specific pool, rendered edge table, schedule, selected donor, template-array pull, dependency installation, network/archive/raw-recording read, Rung 0, hybrid generation or sorter run occurred in Codex Session 24.

The public state remains `In Progress`. The next executable step is still blocked on pre-measurement design approval.

## Review method now governing

`Playbooks/review-cycle.md` begins with the director's superseding method, implemented at Claude Session 24 addendum and Codex Session 24:

- the owner opens a Review Card around one stable candidate;
- Round 1 is the only full-artifact pass and records every reasonably discoverable finding in one numbered ledger;
- later rounds are delta-only: recorded findings and regressions introduced by the response;
- the review ends within three owner-reviewer round-trips with a named outcome;
- substantive reviewer edits are findings unless ownership was transferred; approval stays explicit and state-specific.

The old cycle remains in the file only as history.

Randy then asked Claude and Codex to replace human escalation because his asynchronous schedule could strand later sessions. In `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md`, Codex proposed a bounded **agent-only Convergence Decision**:

1. each agent records a minimum shippable claim, controlling evidence, strongest contrary evidence and acceptable safe disposition;
2. evidence controls what may ship; uncertainty on a blocker never becomes approval;
3. both agents explicitly agree on `Revisions Required`, `Split/Redesign Required`, or `Approved with Follow-ups`, even if they retain different substantive beliefs;
4. one successor card names `Supersedes:` and the material pre-review change;
5. a repeated same-purpose non-approval forces a real split/redesign rather than another card reset.

Claude's acceptance or smallest counterproposal is pending. **Do not edit the playbook until consensus is recorded.** Codex agrees with Claude's existing operating readings: explicit same-state approval, response-created regressions in scope, repair-created LATE-BLOCKER language, the evidence test for mechanical edits, and the transition closure of the old chat.

## RC-001 — Round 1 complete, candidate not approved

- **Card:** `Review Cards/RC-001 Tier A Selection Section 16.md`
- **Chat:** `chats/Claude-Codex/Tier A Selection Section 16 Review/Tier A Selection Section 16 Review - Active.md`

Candidate hashes verified before review and unchanged afterward:

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 22 — `5ca2d6ca188d27ad1cfd9352b9078855815b3fc274eb8cc2773a6e11063f4d1a`
- `Reproducibility Packet/scripts/utils/band_drift.py` — `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063`
- `agents/Claude/tools/test_band_drift.py` — `2117983084ceee241273e355077f8c6792ec60c24e6c0ed44813b3481bcd9c89`

Round-1 outcome: **Revisions Required. Codex does not approve the candidate.**

### RC-001-F1 — blocking temporal aggregation mismatch

Ten consecutive 60-second bin medians span only nine minutes between their centres, yet §16 calls their peak-to-peak range the worst movement inside a ten-minute experiment segment and says the host is protected wherever the segment lands.

Permanent independent evidence in `agents/Codex/tools/probe_rc001_round1.py`:

- five units, 61 bins, 100 spikes/unit/bin, common `2.1 µm/min` ramp: true ten-minute movement `21.000 µm`, utility `Delta_10 = 18.900 µm`, deterministic `Q95_null = 18.682 µm`, strict gate **passes**;
- common 30 µm episode occupying fewer than half the spikes in one minute: `Delta_10 = 0`, `Q95_null = 0`, all five per-unit audit values zero, gate **passes**;
- common bin levels `[0, 15 × 9, 30, 15]`: an off-grid segment `[30 s, 630 s)` contains 0 and 30 µm, every aligned ten-bin window is at most 15 µm, null is zero, gate **passes**.

These are not the label-blind conditional: every included unit moves. They are not IBL estimator bias: the movement exists in the utility input and is lost through the utility's own binning/windowing. The response must align the time object with the actual 600-second segment and cover within-bin/off-grid aliasing, or place those cases under another justified pre-measurement gate. Wording alone cannot repair the smooth-ramp wrong verdict.

### RC-001-F2 — blocking unit-count overgeneralization

Draft 22 says masking gets easier with more units at a fixed moving fraction, citing 5/11, 10/21 and 20/41. Those fractions are `0.4545`, `0.4762`, `0.4878`, not fixed. At a genuinely fixed 40% moving fraction and seed 7013, the admitted construction gives `Delta_10 = 14.891`, `15.532`, `8.182 µm` at 10, 20, 40 units; the first transition reverses the claimed direction.

The valid limitation is that a moving minority can be suppressed. The evidence does not order candidate recordings by unit count. The owner must constrain the claim to the one pinned fixture or support a conditioned probabilistic/expected claim.

### RC-001-F3 — non-blocking tracked follow-up

Replace the sentence that a sample median's realized value cannot move with spike count. The valid invariant is that it does not mechanically accumulate a positive term per spike like the retired path length.

### Round-2 boundary

Round 2 is delta-only. Verify F1–F3 and regressions introduced by the response; do not re-audit unchanged §16 from scratch. Any unchanged sentence made false by the repair counts as a response regression. The archive reader and candidate measurement remain blocked until both agents explicitly approve the same exact state.

## Validation state

All RC-001 declared acceptance tests passed:

- 86/86 synthetic harness checks at 200 permutations;
- 3/3 claim probes;
- both prior safety counterexamples to the digit;
- 10/10 packet runbook steps;
- eight document curly quotes, ASCII harness, candidate Python compilation.

New independent probe also passed:

- forty randomized observations against a separate reference implementation;
- one nine-permutation null replayed byte-for-byte against a separate seed/binning implementation;
- exact grid-edge exclusion, caller-array immutability, and every gate boundary;
- all F1/F2 counterexamples.

The implementation matches its written ten-bin algorithm. The blocker is the algorithm's interpretation and purpose, not an accidental code divergence.

## Contract and other approved state

Amendments 1–6 remain in force. Current synchronized hashes:

- `Claim Sheet.md`: `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`
- `Accessible Claim Sheet.md`: `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`

The real-arm donor-matching prose remains closed and same-state approved:

- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` Draft 6 — `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`

§1–§15 of Claude's host-selection document remain outside RC-001 and same-state approved. The thirteen-candidate order remains pinned. The packet's earlier design-stage review remains closed at ten steps; the archive-reading CLI/Step 11 does not exist.

## Separate gates — do not collapse

1. Claude's response to RC-001 F1–F3 and Codex's delta-only verification;
2. archive-reading drift CLI, its own Review Card/packet step, then candidate measurement down the pinned order;
3. exposure-schedule/placement specification, implementation, synthetic tests and same-state approval;
4. matcher implementation, exhaustive/mutation tests and same-state approval;
5. noise and post-rescaling effective-SNR host gates;
6. footprint/placement calibration and joint ten-placement gate;
7. exact candidate sites, T/K/N, U/Z/R, edge table, un-removed/post-removal matching outputs and IDs;
8. independent Tier A balance/manipulation approval;
9. generation authorization;
10. Rung 0/sorter execution authorization.

Reviewer edits, commits, downstream use and silence are not same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. Session 24 appended the temporal-alias blocker and withdrew forward the unsupported claim that larger candidate bands are necessarily easier to fool.
- `agents/Codex/Progress Reports/Progress Report Session 24.md` is the count-based director report. The next cadence report is Session 32.
- The Phase 1 director contract-review request remains open and non-blocking.
- Randy's new method request is active in the three-way chat; no separate `director_requests.md` entry is needed.
- No Slot 8 verification-artifact update exists because there is no result.

## Append-only evidence

- RC-001 transcript pre-write: 3,757 bytes, SHA-256 `ac11eeb075fc3e3458eda9d4a1685e476f9d6d0c195290eda58c47c93f5368ef`; the new file's exact first 3,757 bytes match and one Codex Session 24 header exists.
- Three-way transcript pre-write: 11,295 bytes, SHA-256 `6fc8a3850b6bdff5bb1a2c8c96ed7fe61fb9a20e1a6408cb12d12f0d0be0b96f`; the new file's exact first 11,295 bytes match and one Codex Session 24 header exists. Randy's user-authored append is preserved.
- Root README pre-entry SHA-256 `9bd3e40a63753416b280f748762964904c9fe2ac8ab97891c19b4d4241162996`; removing exactly the one new running-log entry and its insertion newline reconstructs that hash.

`agents/Codex/Session Summaries/HumanReport24.md` contains the full work and reasoning.
