# Human Report 16 — Codex

**Current date and time:** 2026-08-13 05:11 PDT

**Session:** Codex Session 16

**Phase at start:** Phase 2 — Execution. Amendments 1–6 were `In force`. Claude had returned Draft 4 of Codex's Tier A real-arm donor-matching rule for genuine owner re-review at SHA-256 `5dc8022d33045da39ac3cbc4cfa1d667e34ef70629d780de6e6d52fe50d381d7`. No host, manifest, pool, donor, generation, Rung 0, sorter run, or scientific result existed.

**Phase at end:** unchanged. Codex explicitly approves Draft 5 at `23148d2d8896db70f48d13bd712bbf4ba04987b7f348866918a98431fc324cf7` and handed it to Claude for exact-state review. The prose loop remains open. No downstream gate moved.

**Progress-report trigger:** yes — count-based, Codex Session 16. `agents/Codex/Progress Reports/Progress Report Session 16.md` was written after the session's normal work.

---

## Summary

This was an exact-state owner-review session. Claude accepted every decision in Draft 3, then returned Draft 4 with three changes: a stronger two-level provenance-count preference, a requirement to make the schedule's randomized inputs reproducible, and a correction to one common-ruler sentence. I re-opened Draft 4, checked the exact hash, read it against the in-force contract, ran Claude's supporting probe, and independently reproduced its full provenance census.

I accepted the provenance correction and the ruler wording. I also accepted Claude's diagnosis that the matching rule was pinned on top of redrawable nuisance inputs. I did **not** accept Draft 4's implementation of that diagnosis as complete: it required a derived master seed but left the seed string, occurrence grammar, stream mapping, amplitude-target law, and placement transform for a later configuration that would already know the pool.

Draft 5 keeps the diagnosis and places the unresolved choices in a separate exact-state exposure-schedule/placement specification and synthetic-test gate. That gate must close before the target survivors are measured or any host-specific manifest, pool, or edge table may be constructed or opened. The new wording also catches one input the Draft 4 handoff did not name: the amplitude target is part of the schedule and affects the realized quantities being matched, so it cannot remain pool-aware while only the placement seeds are fixed.

No host-specific data was inspected. No dependency was installed. No heavy work ran.

## 1. Startup and workflow control

The turn/session gate authorized work:

1. `.agent-turn` existed and named `Codex`.
2. `.agent-session.lock` did not exist.
3. I created the lock and re-read `.agent-turn`.
4. The second read still named `Codex`.

I then read `AgentPrompt.md`, the complete `Project Details/Project Details.md`, Codex's continuity file, every summary and active chat involving Codex, and the relevant review-cycle, progress-report, and live-run README playbooks. Automation memory and the relevant general memory registry entries were read for continuity; live repo state and chat bytes governed every current-state decision.

The working tree was clean at startup. HEAD and `origin/main` both named Claude Session 16 at `24eac44`.

## 2. Exact-state owner review of Draft 4

The handed-off artifact hash matched the chat before review:

`5dc8022d33045da39ac3cbc4cfa1d667e34ef70629d780de6e6d52fe50d381d7`

### 2.1 Common-ruler correction accepted

Draft 3 had said U includes Z. That was too strong: U is the final region-unaware eligible pool, so it includes only those injection-zone keys that pass region-unaware eligibility. Draft 4's replacement states the actual property: removal takes out exactly the zone rows present in U. The choice to use one U-derived standard-deviation ruler for both the un-removed and post-removal reports, with R-derived standard deviations as diagnostics, is unchanged.

### 2.2 Provenance-count correction accepted

The contract's literal floor matches the number of distinct `dataset` values between the arms. The parser establishes that `dataset` is a probe-insertion identifier and derives session and subject from that string. Matching insertion counts alone therefore says nothing about how concentrated those insertions are across sessions or animals.

Claude's offline probe reports:

- 2,183 NP1.0 donor rows;
- 37 insertions;
- 24 sessions;
- 12 subjects;
- CA1's sixteen across four insertions, four sessions, and four subjects; and
- among 66,045 four-insertion subsets, 37,424 with four subjects, 28,621 with fewer, and 74 with one.

I reran the tool in the project venv and independently parsed the pinned CSV with a separate stdlib reader. The independent enumeration reproduced every `(session_count, subject_count)` census cell exactly, not only the headline totals.

Draft 5 accepts Draft 4's two levels:

- **Level A:** match distinct insertion, session, and subject counts;
- **Level B:** match distinct insertion count only, the contract's literal floor.

At each pairwise provenance stage, Level A is tried first and Level B is tried if Level A fails. The pairwise stage relaxes only if Level B also fails. I judged this to belong in the matching-rule specification rather than require a Claim Sheet amendment because Level B remains reachable at every stage. Level A can change which assignment wins, but it cannot force a coarser provenance stage or create a new failure under Slot 12.3.

## 3. The nuisance-input diagnosis was right; Draft 4's repair was incomplete

The exposure schedule carries the commanded placement, amplitude target, spike-time seed, and placement seed for every occurrence. All three matching quantities—rendered amplitude, effective host SNR, and depth—are realized at that placement. A matcher can therefore be deterministic while its input schedule is repeatedly redrawn until the balance looks favorable.

Draft 4 correctly required a deterministic derived master seed. But it left the exact derivation for the later configuration. That still left material choices open after the pool could be visible:

- master-seed string and digest-to-integer conversion;
- occurrence identifier grammar;
- domain labels and stream separation;
- within-block slot permutation;
- amplitude-target law and occurrence assignment;
- hash or PRNG algorithm/version;
- placement-seed to commanded-site transform; and
- which real/pseudo arms share or separate nuisance streams.

A future configuration approval would not cure the timing problem, because the choices would already have been made with the pool in view.

## 4. Draft 5's repair: a separate exact schedule/placement gate

I did not invent the unmeasured amplitude or placement law inside the donor matcher. Draft 5 instead requires a separate exposure-schedule and placement specification, implementation, synthetic tests, and same-state approval before T is measured and before any host-specific manifest, U/R pool, or rendered edge table is opened.

That specification must pin all choices above, plus byte-for-byte schedule replay, digests, and loud failure semantics. The algorithm is approved against synthetic T/site inputs. It is evaluated once after the real T exists because T supplies the rota members, but no part of its construction may be selected after T is known. A joint placement failure rejects the host; it cannot authorize a second seed or schedule.

The matcher implementation remains another separate gate after prose convergence and after the schedule/placement specification. Both implementations must be reviewed on synthetic inputs before any real pool is visible.

## 5. Exact-state handoff and append-only record

The final artifact hash is:

`23148d2d8896db70f48d13bd712bbf4ba04987b7f348866918a98431fc324cf7`

I explicitly approved those exact bytes as Draft 5 and appended the review, rationale, boundary, hash, and handoff to:

`chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md`

The append used a programmatically verified unique EOF anchor. The pre-write chat had 431 physical LF-terminated lines and SHA-256 `64bbd3bfe7780900fc42bcbf0133b3c9e79d87aec0afc27b3aeeb3e8e12a56cc`. After the append:

- the entire prior file is a byte-exact prefix;
- the new Session 16 header occurs exactly once after that prefix and once total;
- the file ends with the Draft 5 handoff marker; and
- the physical line count is 465.

Claude must genuinely re-open Draft 5 and explicitly approve those bytes or return another edited/approved state. Codex's edit and handoff are not convergence by themselves.

## 6. Cross-review

I read Claude's `HumanReport16.md`, Draft 4, the full review chat, `source_count_granularity_probe.py`, and its recorded output. The report's state description, numerical claims, and boundaries match the artifacts. I independently reproduced the load-bearing provenance numbers.

I found one incompleteness in Claude's proposed implementation—the later seed derivation remained under-specified—and repaired it in Draft 5 rather than treating the diagnosis as approval of its implementation. I found no disagreement with Claude's other Session 16 work.

## 7. Public heartbeat and director state

Claude Session 16 already appended a lean public README entry describing both noteworthy findings: provenance concentration and redrawable schedule inputs. The root README's working-record section already says the matcher remains under same-state review. Draft 5 has not converged and adds no public result, phase close, or separate noteworthy finding beyond the repair already logged, so I left the public README unchanged.

The Phase 1 director contract-review request remains open and non-blocking. No new director-only action is needed.

The required count-based progress report was created at:

`agents/Codex/Progress Reports/Progress Report Session 16.md`

It explains Amendment 6, the provenance finding, the schedule/placement gate, current blockers, and next work at the Accessible-Piece bar. The Slot 8 verification artifact has no new state because no result exists.

## 8. Validation and repository integrity

Validation performed:

- Draft 4 hash verified before review.
- Claude's provenance probe rerun in `venv` against the pinned CSV.
- Independent CSV/regex enumeration reproduced the full four-insertion census.
- Draft 5 hash computed from disk.
- Required new terms and removed stale terms inspected.
- Markdown fences balanced.
- Zero curly double quotes, U+FFFD replacement characters, or malformed `Ã`/`Â` sequences in Draft 5.
- `git diff --check` clean before closeout.
- Append-only chat prefix/header/tail assertions passed.
- `.gitignore` reviewed; the session introduced only tracked Markdown changes and no new ignore need.

Machine at 05:10 PDT:

- RAM: 7.31 GiB free of 31.67 GiB;
- VRAM: 1,021 MiB used of 16,311 MiB;
- `C:` free: 603.6 GB.

Nothing heavy ran. The only execution was metadata parsing, hashing, Markdown checks, and the 66,045-subset stdlib enumeration.

## 9. Files created or updated

| Path | What changed |
|---|---|
| `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` | Draft 4 → Draft 5. Accepted the two-level provenance rule and ruler correction; replaced the incomplete later-seed promise with a separate exact pre-pool schedule/placement specification and tests; recorded Codex approval. |
| `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md` | Append-only Session 16 owner review and Draft 5 exact-state handoff. |
| `agents/Codex/Progress Reports/Progress Report Session 16.md` | New count-based director progress report. |
| `agents/Codex/README.md` | Workspace tree, Draft 5 state, chat status, and technical boundaries updated. |
| `agents/Codex/Summary of Only Necessary Context.md` | Completely rewritten for Session 17. |
| `agents/Codex/Session Summaries/HumanReport16.md` | This report. |

## 10. Next steps

1. Claude exact-state reviews Draft 5. Implementation remains blocked until the prose loop converges.
2. Codex drafts the exposure-schedule/placement specification against synthetic T/site inputs, including the amplitude-target and nuisance-stream construction, then hands it to Claude for same-state review.
3. Codex implements and tests the matcher on synthetic inputs only after the prose rule converges; no host-specific pool may be opened.
4. Claude continues the replacement drift-gate definition and host-admissibility work. Codex continues footprint/placement calibration in its own lane.
5. After all pre-pool gates, the host-specific target manifest, U/Z/R/T/K state, edge table, two matching outputs, selected IDs, balance/manipulation verdict, generation, and sorter execution remain sequential approvals.

## 11. Challenge and decision record

The main judgement was whether to approve Draft 4's seed requirement as sufficient. The diagnosis and the implementation had to be separated. A future recorded seed would make one run reproducible, but if its derivation were chosen after the pool was visible it would not make the choice precommitted. The repair therefore had to govern *when and where* the schedule rule is approved, not merely require that the eventual number be written down.

The second judgement was whether Level A required a Claim Sheet amendment. I kept it in the matching specification because its Level B fallback preserves the exact contract floor at the same pairwise stage and its timing is clean: the preference was written and measured before any host-specific candidate state existed. If Level A had been allowed to create infeasibility or force a coarser stage, I would have treated it as contract work instead.
