# Human Report 7 — Codex

**Date and time:** 2026-08-12 11:21 PDT
**Session:** Codex Session 7
**Phase at start:** Phase 2 — Execution
**Phase at end:** Phase 2 — Execution. Claim Sheet Amendments 1 and 2 are `In force`; Amendments 3 and 4 remain `Proposed` at a Codex-approved reviewer state pending Claude's exact-state owner re-review. Draft 4 of the Tier A selection artifact is likewise at a Codex-approved reviewer state pending owner re-review. **No host is pinned, no generator or sorter has run, and no scientific result exists.**

---

## Summary

This session reviewed Claude's Session 7 provenance amendments and placement work, reproduced both metadata audits, corrected several claims before they could become execution rules, and handed synchronized exact states back through the active review chat.

The main outcome is not an approval to execute. It is a tighter pre-execution state:

1. **Amendment 3 now distinguishes the provisional 1,149-template metadata screen from the final host-dependent eligible control pool.** Its pseudo-pool random seed is fixed before host or subset inspection, and a separate exact-configuration approval is required before any pseudo-arm generation.
2. **Amendment 4 now stops at what the tracked NWBs establish.** Laboratory and institution separate donor and candidate-host subjects; protocol-version sets partly overlap; rig hardware/design remain unverified; and downstream IBL/library processing is not attributed to the acquisition laboratory.
3. **The placement result remains parameterized.** Donor-template footprint can justify an edge margin but cannot justify the minimum peak-separation rule. Those are now explicitly separate calibration tasks.
4. **Native yield remains diagnostic rather than becoming a post-hoc exclusion threshold.** NYU-39 is a high-risk, lower-priority candidate, not formally disqualified on a rule invented after its value was seen.
5. **The supporting code and reports were hardened and replayed.** Repeated subject/probe rows now carry session IDs, unit-to-electrode probe consistency fails loudly, and both full metadata audits reproduced without error.

## 1. Required context and cross-review

I followed the turn/lock gate, read `AgentPrompt.md`, all of `Project Details/Project Details.md`, Codex continuity, every Codex-including chat summary, and the complete active Tier A selection transcript before replying. I then read the review-cycle, Claim Sheet, Accessible Claim Sheet, Accessible Piece, Reproducibility Packet, and Live-Run README playbooks required by the artifacts touched this session.

The required recent-work cross-review covered:

- `agents/Claude/Session Summaries/HumanReport7.md`;
- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 4;
- synchronized Claim Sheet Amendments 3 and 4;
- the new provenance and placement scripts and their raw/report outputs; and
- the public Live-Run README entry produced by Claude's Session 7.

Claude's core measurements survived replay. The review corrections concern what those measurements license, not whether the measurements occurred.

## 2. Amendment 3 — negative-control construction

Claude's proposed fixed-16-versus-full-pool pseudo contrast remains the right Tier A negative control. It tests whether pool-size, reuse, matching, clustering, and seed asymmetries can manufacture a sorter-by-arm interaction when neither pseudo-arm conditions on region. The earlier replicate-of-the-real-contrast proposal remains withdrawn because it could repeat a systematic matching artifact and make it appear stable.

The handed-off Amendment 3 nevertheless had two unresolved degrees of freedom.

### 2.1 The 1,149 count was provisional, not the final control pool

The amendment described the real region-unaware arm as drawing from 1,149 in-caliper templates. Amendment 2 had already established that the amplitude/SNR caliper is a screening diagnostic rather than an eligibility filter: final eligibility is evaluated after rescaling and relocation in the selected host, including effective host SNR and placement. Treating 1,149 as the final pool would silently reverse that correction.

Both sheets now state that P1 and P2 use the **final eligible region-unaware pool** after the host-specific eligibility gates. The final pool digest, filter, and count must be recorded; the provisional 1,149 screen cannot substitute for them.

### 2.2 The seed was described as pinned but was not named

The seed is now fixed before host selection or subset inspection at **`711362139`**. It is derived reproducibly as the unsigned integer encoded by the first eight hex digits (`2a66865b`) of SHA-256 over the UTF-8 string:

`Hybrid Ground Truth Realism|Tier A|pseudo pool|v1`

The full digest is `2a66865b5504a51fb1390be977e99ac97cb2e0eae9489df687eb318641bdb227`.

The host-dependent selector still cannot be finalized now. Amendment 3 therefore creates a second pre-generation gate: before selection, a tracked configuration must freeze the eligible-pool digest/filter, covariate scaling, scalar objective, search budget, and deterministic tie-break; after selection it must list all sixteen `template_index` IDs and achieved spread. Both agents must explicitly approve that exact configuration and selected-ID state before pseudo-arm generation.

This separates two approvals that must not collapse into one:

- approval of the **construction** in Amendment 3; and
- approval of the later **host-dependent executable configuration**.

## 3. Amendment 4 — acquisition provenance

The provenance replay reproduced 21/21 subjects, 88,650,017 bytes in 91 range requests, and zero failures.

The tracked records establish:

- all twelve donor subjects read are `cortexlab` at University College London;
- all nine candidate-host subjects read are `churchlandlab` or `angelakilab`, with no donor-lab overlap;
- `genotype`, `strain`, and `description` are absent from every raw NWB read; and
- donor and host protocol-version sets partly overlap at `_iblrig_tasks_ephysChoiceWorld6.4.2`.

The handed-off amendment overstated two parts of that result.

First, different laboratories and institutions do not make rig hardware or rig design a measured field. Different institutions necessarily exclude one shared physical acquisition rig, but the NWBs do not identify the hardware or establish design equivalence/difference. Second, the donor recordings originate at cortexlab, but the downstream IBL sorting and `hybrid_template_library` extraction/curation pipeline is not thereby cortexlab's pipeline.

Both Claim Sheets and Draft 4 now preserve those distinctions. The new non-transfer boundary is: Tier A is conditional on recordings acquired from one laboratory, the downstream IBL/library processing path, and the finite sixteen-template CA1 population. It does not misattribute the latter two to the acquisition lab.

## 4. Draft 4 — placement and native-yield rulings

The placement audit reproduced 13 bands across 11 recordings, 170,215,252 metadata bytes in 169 requests, and zero failures. Every candidate band remained 100% CA1-pure. The raw and processed electrode tables agreed, each recomputed band matched its index, and the provisional 60 µm margin / 40 µm separation screen remained 9 passes and 4 failures.

### 4.1 Placement has two unmeasured parameters, not one

Claude correctly identified donor-template footprint as important, but footprint alone cannot convert the gate from parameterized to decided:

- **Edge margin** can be calibrated from the real multichannel spatial support of the sixteen CA1 templates.
- **Minimum peak separation** needs its own predeclared basis from native peak-depth spacing and the generator's relocation constraints.

Codex takes ownership of this two-part calibration as part of Rung 0 preparation. No Rung 0 run was authorized or performed. The placement gate remains open until both values are justified and frozen.

### 4.2 No post-hoc overcrowding cutoff

The native-yield table is valuable context, but the Claim Sheet contains no percentage cutoff. Declaring NYU-39 disqualified after observing `22` total / `1` good unit would create a new gate post hoc while simultaneously claiming not to use a threshold.

The reviewer state therefore:

- declines to add a percentage cutoff;
- treats native yield as a candidate-priority and closer-review signal;
- moves NYU-39 behind the stronger candidates; and
- preserves formal admissibility until the predeclared noise/effective-SNR and other open gates run.

The amplitude table received the same discipline. Its apparent overlap with the 50–200 µV target is a reason to verify measurement conventions, not evidence that the target is validated, because IBL's `median_spike_amplitude_uV` and the donor library's `amplitude_uv` have not yet been shown commensurate.

## 5. Engineering review and validation

### Provenance audit

`audit_subject_provenance.py` now:

- reports protocol counts and donor/host overlap explicitly;
- describes laboratory/institution separation without claiming measured rig hardware/design; and
- preserves the one-asset-per-subject evidence boundary.

The full 21-subject live replay completed in 105.9 seconds with the same byte/request totals and zero failures.

### Placement audit

`screen_injection_placement.py` now:

- fails loudly if `max_electrode` is out of range;
- fails loudly if a unit's named probe disagrees with its peak electrode's probe;
- fails on duplicate processed assets for one session rather than silently taking the last one;
- includes short session identifiers in the verdict table, capacity sweep, and per-band headings; and
- distinguishes donor-footprint calibration of edge margin from the separate peak-separation justification.

The full live replay completed in 190.1 seconds. All new unit/electrode consistency assertions passed. A no-network `--from-records` replay reproduced the final text report byte-for-byte.

Structured assertions also passed:

- 13 bands;
- 9 provisional passes;
- 13/13 purity = 1.0;
- 13/13 band/index and raw/processed table agreement;
- 21 provenance records;
- donor lab set exactly `{cortexlab}`;
- host lab set exactly `{angelakilab, churchlandlab}`; and
- shared protocol exactly version 6.4.2.

All changed Python sources compile under the project venv. `git diff --check` passes. No dependency was installed.

## 6. Exact-state handoff

I appended the review to `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` using a verified unique EOF anchor, a pre-write line count of 315, and a post-write assertion that the Session 7 header occurs exactly once after that count.

I explicitly approve and handed back:

- `Claim Sheet.md` SHA-256 `37dcd0f8b20fcee6dc471e1eb396a0f01890a222c5807c70c03fae527a70959a`;
- `Accessible Claim Sheet.md` SHA-256 `696b76e47ad5b4c42038abdeac18426652db8fb1d462804735d26da28d46c267`; and
- `agents/Claude/Tier A Host and Injection Zone Selection.md` SHA-256 `fa5b871e59ac5e07973eee96b02f3de33f385870138c76bf3699ecff3b8b1f75`.

These are **reviewer approvals**, not same-state closure. Amendments 3/4 remain `Proposed`, and Draft 4 remains open, until Claude genuinely re-opens and explicitly approves those exact states or returns new ones.

## 7. Public heartbeat and claim discipline

Claude's latest public log entry preserved the work honestly but repeated three claims the review narrowed: rig separation as measured, NYU-39 as disqualified, and footprint as sufficient to decide placement. The running log is append-only, so I did not rewrite that entry. I appended a dated forward correction that states the precise reviewer position and reiterates that no host, sorter run, or scientific result exists.

The Live-Run banner remains `Phase 2 — Execution` / `In Progress`. The current artifact pointers now say Amendments 1/2 are in force and Amendments 3/4 are under active same-state review.

## 8. Challenges, decisions, and reasoning

**The largest review issue was a count that looked exact but belonged to an earlier gate.** `1,149` is a real number from the pinned template snapshot, which made it easy to mistake for the final Tier A control pool. The amendment protocol had already demoted it to a provisional screen. Preserving that distinction prevents a tidy number from silently replacing the host-specific eligibility design.

**A measured lab label invited two opposite rig claims.** Earlier work overclaimed a shared rig design; the new draft overcorrected into a verified rig difference. The evidence supports lab/institution separation and an inference that one physical rig cannot occupy two institutions. It does not support hardware/design claims. Naming that middle position is more useful than swapping one unsupported certainty for another.

**The footprint finding solved only half the geometry problem.** A waveform's spatial support can tell us how far its peak must sit inside CA1. It does not tell us how far two neuronal peaks must be from each other. Keeping those questions separate prevents a future template-array measurement from being treated as authority over a parameter it never measured.

**Not using a density threshold required undoing a desired conclusion.** NYU-39's one `good` unit is an important warning. It is not permission to invent a pass/fail rule after the candidate table is visible. Deprioritization preserves the evidence without turning it into retroactive preregistration.

## 9. Files created or updated

| Path | Change |
|---|---|
| `Claim Sheet.md` | Codex reviewer edits to Amendments 3/4; current approved reviewer hash recorded above. |
| `Accessible Claim Sheet.md` | Synchronized plain-language reviewer edits with the same gates and boundaries. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 4 reviewer corrections; owner re-review remains open. |
| `Reproducibility Packet/scripts/audit_subject_provenance.py` | Protocol-overlap reporting and evidence-bounded rig wording. |
| `Reproducibility Packet/results/subject_provenance.txt` | Regenerated from the full 21-subject live replay. |
| `Reproducibility Packet/scripts/screen_injection_placement.py` | Unit/probe assertions, duplicate-asset guard, session identifiers, and two-parameter placement boundary. |
| `Reproducibility Packet/results/injection_placement_CA1.txt` | Regenerated; sessions disambiguate repeated subject/probe rows. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only exact-state handoff and reviewer approvals. |
| `README.md` | Current banner/artifact pointers refreshed; append-only public correction added. |
| `agents/Codex/README.md` | Workspace map and shared-state pointers refreshed. |
| `agents/Codex/Summary of Only Necessary Context.md` | Completely rewritten for Session 8 resumption. |
| `agents/Codex/Session Summaries/HumanReport7.md` | This report. |

The JSON audit outputs were regenerated identically and therefore do not remain modified in git.

## 10. Compute and execution boundary

No heavy compute occurred. Both sustained actions were metadata-only HTTP range audits using the existing `h5py==3.16.0` / `numpy==2.5.2` environment. No raw recording data, template arrays, generator output, sorter output, dependency installation, or Rung 0 execution occurred. Because no heavy step was admitted, no prior RAM/VRAM reading was inherited or treated as authorization.

## 11. Next steps

1. Claude must genuinely re-review the exact Claim Sheet and Draft 4 hashes above. Same-state closure cannot be inferred from this handoff.
2. If Claude approves, mark Amendments 3 and 4 `In force` in both sheets using the established status-line operation and preserve that exact-state record.
3. Codex prepares the two-part placement calibration without launching Rung 0: predeclare template-support and native-spacing/generator rules, then measure them when the exact template/host substrate is available.
4. Before pseudo-arm generation, build and separately cross-approve the Amendment 3 selector configuration and selected sixteen IDs.
5. Continue the remaining host gates in first-admissible order: drift, noise, post-rescaling effective SNR, and covariate balance. Do not treat native yield as a new hidden gate.
6. Run Rung 0 only in the daytime window after fresh RAM/VRAM admission measurements pass all contract guards.

Session 8 is Codex's next session and triggers the count-based director progress report **after normal session work**.
