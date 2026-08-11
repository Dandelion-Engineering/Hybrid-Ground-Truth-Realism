# Human Report 2 — Codex

**Date and time:** 2026-08-11 13:15 PDT

**Session:** Codex Session 2

**Phase at start:** Phase 1 — Sharpening; Claude's first full Claim Sheet draft awaited required Codex review

**Phase at end:** Phase 1 — Sharpening; revised Claim Sheet explicitly approved by Codex and handed back for Claude's same-state re-review

---

## Summary

This session completed the required review of `Claim Sheet.md`. I read the full project constitution, both Phase 0 Literature Foundations, both source ledgers, Claude's latest report and continuity, the active review chat, and the Claim Sheet and review-cycle playbooks before reviewing the draft.

The draft had the right overall question, axis ladder, manipulation gate, and difference-in-differences target, but six parts of the contract were stronger or more definite than the design supported. I edited the sheet directly, validated the resulting state, and explicitly approved the exact reviewed bytes in the append-only Claim Sheet review chat. The approved file's SHA-256 at handoff was:

`67c9503b536de4bc7006e02a7bb25cd01f23e3d5c488c1490435bacdcf758f6e`

The review loop is **not closed**. Claude owns the artifact and must now re-open both the feedback and the edited file, then explicitly approve this same state or edit and hand it back. Phase 1 also still requires the Accessible Claim Sheet, Study Guide Pass 1, and explicit agreement on the labor split.

## What changed in the Claim Sheet

### 1. Tier A now makes an honest pairing claim

The draft said donor/injected-unit identity stayed fixed across realism arms. That is impossible for region matching: changing donor region necessarily changes donor-template identity.

The contract now distinguishes the axes:

- Tier A uses predeclared covariate-matched donor-pair slots, with the same spike train, placement, rescaled amplitude target, unit count, and randomization block inside each pair.
- Tiers B and C keep donor-template identity fixed and change only their intended temporal property while holding total spike count fixed.

The primary estimand is correspondingly defined on a paired donor slot for Tier A rather than on a fictitiously unchanged unit.

### 2. Tier A tests the anchor-like control at the right anatomical scale

The draft's primary Tier A comparison was region-matched versus a maximally distant area. That is a useful possible stress test, but it is not the anchor pipeline's stated default, which draws without conditioning on region. The primary control is now **region-unaware**; a distant-region arm may be added only as a labelled secondary stress test.

The sheet also no longer assigns one brain-region label to an entire Neuropixels recording. A penetration crosses anatomical zones. Tier A must pin the host's channel/trajectory anatomy and define an injection zone or depth-specific zones; donor labels are matched to the local label at each target placement.

### 3. The 37/7 audit is now bounded at its true strength

Claude's leave-one-dataset-out measurement is useful, but the draft interpreted it too strongly. Dropping the largest contributing dataset from each area produces a **worst-case** remaining count. The seven-area result applies only when the selected host corresponds to that largest donor source; excluding a different exact source can leave more templates. The audit also does not test the control pool, anatomical placement, or pairwise covariate balance.

The sheet now calls 37/7 a conservative necessary pool-size screen, not completed paired-arm feasibility. It requires a host-specific exclusion and balance query once a host/injection zone is selected.

I also corrected a more basic calibration issue: the anchor's 50–200 µV figure is an **injection rescaling target**, not evidence that donor templates must already have original amplitudes in that range. The existing amplitude 50–200 and SNR 5–15 filters remain provisional screening values. Final balance is evaluated after rescaling and relocation, including effective SNR against the selected host's measured noise.

### 4. Temporal manipulations no longer inherit hidden comparator or biology assumptions

Tier B's local population driver is now required to come from a sorter-independent host-activity proxy computed once from the untouched host recording. That prevents either comparator from supplying the target used to generate its own test data. Conditional sampling or an equivalent method must preserve total spike count, mean rate, and refractory behaviour across arms.

Tier C's quantitative burst prior is now explicitly region- and cell-class-specific. The current ≤6 ms/history-dependent evidence is grounded in CA1 complex-spike biology. A run in another area requires primary evidence for that host region/cell class; otherwise it is labelled a synthetic stress test rather than a biological-realism test.

### 5. Replication and uncertainty now use the actual independent blocks

The draft treated at least five seed replicates as sufficient to estimate a null band and described a bootstrap over injected units clustered by recording instance. Five blocks cannot be assumed to estimate a tail usefully, and individual spikes or units do not become independent merely because they are numerous inside one sorter run.

The revised contract defines:

- a nested mean over paired unit/donor slots within randomization blocks, blocks within hosts, and hosts equally across the tested set;
- a hierarchical paired bootstrap on those levels, conditional on one host until hosts are widened;
- five blocks as the initial resource tranche, followed by fixed-size batches chosen from interval width rather than a favorable point estimate; and
- a matched pseudo-arm **negative-control replicate band** as a diagnostic for nuisance selection/seed interactions, not a second p-value or a visual truth test. The primary confidence interval already carries between-block variation.

### 6. The decision rule now tests a difference directly

The draft treated “one arm's interval excludes zero and the other's includes zero” as loss of separation. That is not evidence the arm-specific gaps differ.

The revised comparative margin is:

`T = max(0.05, 0.5 × |G0|)`

where `G0` is the mean control-arm sorter gap. The five-point floor prevents a near-zero control gap from making a trivial sign change look important. The hierarchical bootstrap recomputes `G0`, `T`, and `D = |I| − T` in every resample:

- bounded positive: the 95% interval for `D` is wholly above zero and the interaction interval excludes zero;
- bounded negative: the interval for `D` is wholly below zero;
- otherwise: inconclusive at the achieved precision.

Reversal, loss/gain of practical separation, and large non-crossing shifts are descriptions applied only after the direct interaction clears that rule. Practical ties use the declared `[-0.05, 0.05]` equivalence region rather than “includes zero.”

## Verification and pilot changes

Slot 8's manipulation panel previously visualized only the Tier C burst mechanism. It is now tier-specific:

- Tier A shows local anatomy, donor labels/waveforms, and post-rescaling balance;
- Tier B shows host-activity and injected-rate trajectories plus invariance checks; and
- Tier C shows raw snippets, ISI distributions, and history-dependent amplitude.

The Rung 0 sorter admission rule now has actual declared limits: a 60-minute ceiling for the 60-second pilot, monitored live-headroom guards (75% of free resources while retaining at least 4 GiB RAM and 2 GiB VRAM), and a projected minimum-tranche ceiling of 48 sorter-hours per candidate per tier. Changing those numbers requires an amendment.

## Template-audit correction and validation

I updated `Reproducibility Packet/scripts/audit_template_library.py` so its documentation and report say what the computation actually establishes:

- `leave-one-out` is labelled `worst-case LOO`;
- the result for a selected host requires excluding that **specific** source dataset;
- the output is a screening bound, not paired-arm feasibility; and
- the amplitude/SNR values are labelled provisional donor screens.

I reran the script with the required project interpreter. The first-party CSV was still 2,032,640 bytes with the same pinned SHA-256, 7,877 rows, 2,183 Neuropixels 1.0 rows, 37 pre-exclusion viable labels, and 7 labels surviving the worst-case largest-source exclusion. Only the interpretation and report labels changed; the underlying counts reproduced.

Validation performed:

- `git diff --check` — passed (line-ending warnings only);
- `Claim Sheet.md` — exactly 15 numbered slots detected;
- audit script `py_compile` — passed;
- audit script `--help` — passed;
- full live audit rerun — passed and matched the pinned snapshot;
- append-only chat write — physical UTF-8 tail read first, pre-write line count recorded, unique EOF anchor verified, Codex Session 2 header asserted exactly once after the prior tail, and physical tail re-read.

No sorter run, dependency installation, raw-recording download, or other heavy step occurred. The audit downloaded only the 2 MB metadata CSV and used the standard library; no compute-environment measurement was required because no heavy step was launched.

## Division of labor agreed from Codex's side

I explicitly accepted Claude's proposal with one extension:

- **Claude:** Accessible Claim Sheet, Study Guide Pass 1, Tier A host/injection-zone selection.
- **Codex:** Rung 0 feasibility pilot, sorter-panel decision, inference and negative-control harness.
- **Tier A gate:** Codex owns the balance/manipulation check so the selector does not grade its own work.
- **Tiers B/C:** assign implementation after Rung 0; the non-author owns each manipulation check.
- **Shared:** Reproducibility Packet; default Claude-writer/Codex-reviewer convention remains for final narrative artifacts.

Claude still has to explicitly approve this labor split in its next turn; the chat record currently contains Codex's side only.

## Public status decision

The Claim Sheet is not converged, so the phase banner remains `Phase 1 — Sharpening (Claim Sheet in review)`. The review did produce a correction a public reader should see, because the existing log had overstated the 37→7 audit. I appended a lean corrective entry rather than rewriting history: seven is the conservative largest-source worst case, the audit is a pool-size screen, and same-state owner re-review remains open.

## Challenges and reasoning paths

The hardest issue was preserving the value of Claude's seed-replicate idea without turning it into duplicate or informal inference. The useful part is a negative control showing what nuisance draws can mimic. The mistake would be treating a shaded band as an automatic truth threshold while the primary interval already includes the same block variation. Separating the two roles kept the control and removed the double-counting.

The other difficult choice was how much of the numerical decision rule to preserve. The 0.05 and 50% values are judgements, but declaring judgement before results is legitimate. The real defects were a vanishing threshold when the control gap is near zero and a significance-versus-nonsignificance comparison. The five-point floor plus direct joint-bootstrap margin repairs those defects without pretending the values came from literature that did not supply them.

I did not add new sources to `agents/Codex/references.md`. Every edit was a design consequence of the existing verified sources, the live audit, or direct statistical logic; no new external claim was introduced that needed a ledger entry.

## Files created or updated

| Path | Change |
|---|---|
| `Claim Sheet.md` | Direct review edits; explicitly approved by Codex at the handed-off SHA-256 |
| `chats/Claude-Codex/Claim Sheet Review/Claim Sheet Review - Active.md` | Appended Codex's detailed review, explicit approval, labor response, and owner re-review request |
| `Reproducibility Packet/scripts/audit_template_library.py` | Corrected worst-case and screening-bound interpretation; clarified provisional donor screens; retained stdlib-only implementation |
| `Reproducibility Packet/results/template_audit_2026-08-11.txt` | Regenerated from the unchanged pinned live snapshot with corrected labels and interpretation |
| `README.md` | Narrowed the live framing to axis-compatible controls and appended the public correction/review heartbeat |
| `agents/Codex/Session Summaries/HumanReport2.md` | This permanent report |
| `agents/Codex/README.md` | Updated workspace map and current phase/review state |
| `agents/Codex/Summary of Only Necessary Context.md` | Rewritten for Codex Session 3 |

## Next steps

1. Claude re-opens the Claim Sheet and the appended review, then explicitly approves the handed-off state or edits and returns it.
2. If Claude approves, it writes the Accessible Claim Sheet and Study Guide Pass 1 against that exact agreed contract and hands each over for review.
3. Claude explicitly accepts or revises the labor split.
4. Once the Phase 1 artifacts and labor split converge, the closing agent writes the phase-transition progress report and the non-blocking `director_requests.md` Claim Sheet review entry.
5. Phase 2 begins with Codex's Rung 0 pilot, but only after measuring live RAM/VRAM immediately before the heavy step and installing/pinning the stack in the repository-root `venv`.

**Nothing is blocked on the director.**
