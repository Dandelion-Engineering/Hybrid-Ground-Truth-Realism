# Human Report 17 — Codex

**Current date and time:** 2026-08-13 07:23 PDT

**Session:** Codex Session 17

**Phase at start:** Phase 2 — Execution. Amendments 1–6 were in force. Claude had returned Draft 6 of Codex's pre-pool real-arm donor-matching rule for owner re-review and had handed off Draft 8 of the host-selection artifact with a proposed candidate order and drift gate. No host, manifest, pool, schedule, donor, generator, sorter run, or scientific result existed.

**Phase at end:** unchanged. Donor-matching Draft 6 now has explicit same-state approval from both agents and its prose-review chat is concluded. Codex approves host-selection Draft 9 and has handed it back for Claude owner re-review. No candidate drift value or other open-gate measurement was read.

**Progress report due?** No. Session 16 carried the count-based report; the next count trigger is Session 24, and this session closed no phase or amendment.

---

## Summary

This session completed one exact-state review cycle and repaired another before it could measure anything.

**Completed:** Claude's three Draft 6 edits to the Tier A real-arm donor-matching prose rule are correct. I re-opened the exact bytes, checked them against Amendment 6 and the full artifact, and explicitly approved the same SHA-256 Claude approved. That closes the prose rule at `51adae4b…`. I appended the approval under the chat's physical UTF-8 tail safeguards, concluded the chat, and wrote its summary. This does not approve an implementation or any host-dependent state.

**Repaired and handed back:** Claude's Draft 8 host candidate order is fundamentally sound, and Sections 13–14 are accepted. The proposed drift rule, however, would have rejected a genuinely quiet host simply because its observed statistic looked like its own no-drift null; called a peak-to-peak range “net displacement”; overclaimed that sub-pitch motion is physically invisible; and treated Kilosort-family-derived host selection as neutral to the primary interaction when host-level treatment-effect heterogeneity can make that false. I repaired those points, pinned the permutation and threshold-ladder semantics, and explicitly approved Draft 9 at `3e48873b…`. Claude's owner re-review remains required before implementation or measurement.

No heavy computation, network read, dependency install, raw-data read, template pull, generator run, Rung 0, or sorter run occurred.

## 1. Startup and workflow control

The automation turn gate authorized work:

- `.agent-turn` named `Codex`;
- `.agent-session.lock` was absent;
- I created the lock and re-read `.agent-turn`, which still named `Codex`.

I then followed `AgentPrompt.md`: read `Project Details/Project Details.md`, Codex continuity, every chat summary and active transcript involving Codex, Claude's `HumanReport17.md`, the review-cycle playbook, the relevant Claim Sheet slots and amendments, and the exact handed-off artifacts. The tracked worktree was clean at startup and local `main` matched `origin/main` at Claude Session 17 commit `e9155c3`.

The automation memory supplied the prior run boundary; the live repository and chat tails controlled every current-state decision.

## 2. Donor-matching Draft 6 — owner re-review and close

Handed-off digest, verified from disk before deciding:

`51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`

### 2.1 Placement object — accepted

Amendment 6 leaves placement seeds randomized and separately requires every block's ten scheduled donors to admit a jointly feasible placement assignment. Those clauses do not decide whether:

- each occurrence receives its own independently seeded commanded placement and the joint gate merely verifies the resulting ten; or
- one deterministic block-level algorithm searches/derives the rendered ten jointly.

The difference changes how often a host dies and what a placement seed means. Draft 6 correctly requires the separate exposure-schedule/placement specification to choose and pin one reading, including search order and ties if a joint algorithm is used. The matcher should not take that still-unmeasured decision.

### 2.2 Manifest boundary — accepted

Draft 6 extends the pre-pool boundary so all four implementation steps occur before the target manifest is constructed or opened:

1. schedule/placement specification and synthetic tests;
2. matcher implementation on synthetic inputs;
3. exhaustive/mutation tests;
4. same-state implementation approval.

I accept the stronger boundary. The manifest reveals `N`, `S_T`, `E_T`, and `B_T`, which select schedule and provenance paths. Implementing before those values exist is the timing discipline the prose rule was written to create. Every step is synthetic and the change cannot make a host state infeasible.

### 2.3 Host-order dependency — accepted as external

Draft 6 correctly names that host rejection alone leaves a shopping path unless candidate order is pinned. That order is not the matcher's property; it belongs in Claude's host-selection artifact. Draft 8 proposed the order in the same Claude session, but its separate review state did not alter the exact matching-rule handoff.

### 2.4 Exact-state verdict

I made no edit to Draft 6 and explicitly approved the same SHA-256 Claude approved. The prose loop is closed.

The donor-matching chat's primary purpose was then complete. I appended the approval, renamed its transcript from `Active` to `Concluded`, and created `Summary.md`. Any matcher implementation and test review begins in a new scoped chat rather than silently reopening a concluded prose review.

**Boundary preserved:** no schedule/placement specification, target manifest, host-specific pool, edge table, matcher implementation, selected donor, balance verdict, generation, Rung 0, or sorter run exists or is approved.

## 3. Host-selection Draft 8 — accepted portions

Handed-off digest, verified from disk before review:

`b104f66596f6a48ad86d5d029ea7be3c437ebbd7b8e83a9d9ea42b748cc4fbef`

### 3.1 Sections 13–14

I explicitly approve Sections 13–14 as handed off:

- the zone-neighbour audit remains a bounded pre-host diagnostic, not a prediction;
- the paired non-self/no-reuse 0.11 expectation and anchor-like unpaired 0.12 expectation are correctly separated as different sampling models; and
- Amendment 5's narrow supersession of Amendment 3 is necessary because the real post-removal pool can no longer contain chance zone donors.

### 3.2 Candidate ranks

The thirteen ranks reproduce their declared construction. Ranks 1–3 preserve the already-published recommendation. Ranks 4–13 are the remaining §4.2 candidates by descending contiguous CA1 channel count, with ASCII `(subject, session, probe)` ties. NYU-39 remains at rank 9 with no hand-written penalty, consistent with its high-risk but not formally disqualified status.

I retained those ranks. I tightened what happens after the list is exhausted: continuation now follows the exact order of the tracked asset cache, whose SHA-256 I verified as `54f8e600ccedf36f2b284a9dacc58277aed24155f9a6915ad60b339437392f70`, rather than wording that could be read as a refreshed live API order.

## 4. Drift rule — defects found and repaired before measurement

Claude's central diagnosis is correct. The archive's own description makes `cumulative_drift_um_per_hour` unusable as this gate: it sums absolute per-spike depth changes, scales with spike count, and explicitly is not electrode displacement. The already-tracked processed-units descriptions expose per-spike depth and time arrays that can support a replacement.

Five repairs were necessary.

### 4.1 A quiet host was turned into a failure

Draft 8 said that if observed `Delta_10` lies inside its permutation null, the host is unmeasurable and rejected. Under a valid no-drift null, a truly quiet host should often lie inside it. The rule therefore inverted its best case.

Draft 9 uses two quantities at active threshold `L`:

- observed worst-window apparent excursion `Delta_10`; and
- the null's nearest-rank empirical 95th percentile `Q95_null`.

The host passes drift only when both are at or below `L`. A low inside-null result passes and is reported as no time-ordered drift resolved with both bounds below the gate. A null bound wider than `L` is the unmeasurable failure.

### 4.2 The statistic was named incorrectly and underspecified

`max D - min D` is a peak-to-peak excursion, not endpoint-to-endpoint net displacement. Draft 9 renames the context quantity from `Delta_net` to `Delta_full` and defines `Delta_10` over ten consecutive complete 60-second bins. A trailing partial bin is discarded and reported. Every complete bin must have at least five valid included-unit medians; an invalid bin rejects the candidate as unmeasurable instead of being omitted and potentially hiding a window maximum.

### 4.3 The threshold rationale overclaimed the probe physics

Twenty micrometres is one Neuropixels contact-row pitch, but sub-pitch motion is not invisible. A unit near a channel boundary can change peak channel, and multichannel waveforms vary continuously with position. Draft 9 retains 20 µm as a declared one-row tolerance chosen before candidate values, not as a physical-resolution fact.

### 4.4 Sorter-derived selection is not guaranteed neutral to the interaction

Using one host across arms means the IBL sorting does not directly define the realism manipulation, so this is not the rejected Tier B circularity. But a Kilosort-family-derived depth trace can select hosts whose features are congenial to that family, and host features can modify a sorter-by-realism treatment effect. The dependence can affect the interaction, not only a constant offset or `G0`. Draft 9 conditions the result on an IBL/Kilosort-family-screened host and leaves transfer to Rung 4 host widening.

### 4.5 Randomization and the threshold ladder were incomplete

Draft 9 pins:

- master seed `3175830281`, independently reproduced from the first eight hex digits `bd4b5309` of SHA-256 over `Hybrid Ground Truth Realism|Tier A|drift permutation null|v1`;
- per-asset/probe/unit-row/permutation domain-separated 64-bit seeds;
- NumPy `Generator(PCG64(seed)).permutation`, with exact NumPy version pinned by implementation;
- 200 permutations and nearest-rank `Q95_null` as the 190th sorted value; and
- byte-for-byte replay before a candidate result is accepted.

The strict pass evaluates ranks 1–13 under 20 µm through every gate. If no fully admissible host exists, the one declared 40 µm relaxation restarts the same rank order. Only after all thirteen fail at 40 µm does cached discovery-order extension begin, at 40 µm. This prevents the relaxation from becoming an exception applied only to the last failure.

## 5. Exact-state host handoff

I explicitly approve and hand back:

`agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 9, SHA-256 `3e48873b03f60fa1cc59a0940ac8f79a8e91521203b8a88f1689e96c9cb27a8c`.

Claude must genuinely owner-re-review the exact bytes. Drift implementation and candidate measurement remain blocked until that same-state step. The implementation must still confirm aligned ragged indices, finite values, exact dependency version, and deterministic null replay before producing any candidate result.

## 6. Public heartbeat

Claude Session 17 had already added public entries for the candidate order and the proposed drift replacement. The drift entry said the replacement measured net displacement and described an inside-null reading as noise rather than quiet. Because those were now forward-facing defects, I did not rewrite the append-only log. I appended a correction entry recording:

- peak-to-peak excursion rather than net displacement;
- the two-number observed/null pass rule;
- the bounded one-row threshold rationale;
- the Kilosort-family selection limitation; and
- same-state approval of the donor-matching prose while implementation remains absent.

The README working-record sentence was updated from “matching draft awaits review” to the current approved-prose/open-implementation state. Public status remains `In Progress` and no result claim was added.

## 7. Append-only safeguards

Both active-chat appends followed the physical-tail protocol:

- read the strict UTF-8 physical tail;
- recorded pre-write counts: 526 donor-matching lines and 794 selection-review lines;
- patched only against unique multi-line EOF anchors;
- asserted exactly one new Codex Session 17 header after each prior count;
- re-read the physical tail after the write.

The donor-matching transcript was renamed only after the final approval append passed those assertions. No transcript content was rewritten or truncated.

## 8. Validation performed

- Verified Draft 6 and Draft 8 handed-off SHA-256 values from disk before review.
- Verified Draft 9 SHA-256 `3e48873b…` after the edits.
- Re-derived the drift master-seed SHA-256 phrase and integer using the project venv.
- Verified the tracked DANDI asset-cache SHA-256 before pinning it in §15.4.
- Read the first-party processed-units column descriptions for `cumulative_drift_um_per_hour`, per-spike depths, their ragged index, spike times and their index.
- Reviewed the Draft 8 candidate table against the declared sort/tie rule.
- `git diff --check` was clean during the review; final closeout validation is recorded in the session commit.
- Reviewed `.gitignore`; the coordination lock remains ignored and this session introduced no secret, large binary, build output or new dependency.

## 9. Machine state and resource boundary

Measured at 2026-08-13 07:19 PDT:

- **RAM:** 6.37 GiB free of 31.67 GiB
- **VRAM:** 1,020 MiB used of 16,311 MiB
- **`C:` free:** 603.5 GiB

No heavy step was attempted. The measurement is a session record, not an inherited admission measurement for future work.

## 10. Files created, updated or moved

| Path | Change |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 8 → Codex-approved Draft 9; host-order continuation and drift decision rule repaired. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only Session 17 exact-state review and Draft 9 handoff. |
| `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Concluded.md` | Final same-state approval appended, then active transcript renamed after convergence. |
| `chats/Claude-Codex/Tier A Donor Matching Rule/Summary.md` | Created with the approved Draft 6 state and downstream boundary. |
| `README.md` | Append-only correction/heartbeat and current matching-rule working-record state. |
| `agents/Codex/README.md` | Workspace map and current review states. |
| `agents/Codex/Summary of Only Necessary Context.md` | Fully rewritten for Session 18. |
| `agents/Codex/Session Summaries/HumanReport17.md` | This report. |

`agents/Codex/Tier A Real-Arm Donor Matching Rule.md` was reviewed and approved unchanged; its bytes remain Claude Session 17's Draft 6 state.

## 11. Next steps

1. Claude genuinely owner-re-reviews Draft 9 and either approves it unchanged or edits/returns another exact state.
2. Only after drift prose convergence, Claude implements the targeted-range drift estimator and confirms ragged-index/finite-column/replay invariants before reading a candidate result.
3. Host gates proceed in the pinned strict/relaxed order: drift, noise, post-rescaling effective SNR, joint placement, then Codex's balance/manipulation gate.
4. In Codex's lane, the next pre-manifest artifact is the exposure-schedule/placement specification and synthetic tests, followed separately by matcher implementation/tests.
5. No host-specific manifest, pool or edge table may be opened until all Draft 6 pre-pool implementation approvals are complete.

Nothing is blocked on the director. The Phase 1 Claim Sheet review request remains open and non-blocking.
