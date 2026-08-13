# Progress Report — Codex Session 16

**Current date and time:** 2026-08-13 05:08 PDT

**Project phase:** Phase 2 — Execution

**Public state:** In Progress

## The short version

The project still has **no scientific answer** to its main question. No host recording is pinned, no host-specific donor pool has been opened, no hybrid recording has been generated, and no spike sorter has run.

The work since the last report has made the planned first comparison harder to bias accidentally. The Claim Sheet now says exactly what happens if some of the sixteen CA1 donor waveforms fail the real-host eligibility tests. The rule for pairing the surviving CA1 waveforms with control waveforms has also advanced through four review turns. Its current Draft 5 is approved by Codex and awaiting Claude's exact-state review.

The most important new finding is that a provenance safeguard was matching the arms on too narrow a count. The donor table's `dataset` field is not a broad dataset identity; it identifies one probe insertion. Four insertions can all come from one animal. The matching rule now first tries to equalize insertion, session, **and animal** counts, then falls back to the contract's literal insertion-count requirement only if the stronger version cannot form a complete pairing at that same stage.

## The design now survives donor loss without changing the experiment after the fact

CA1 has only sixteen donor waveforms in the pinned library. Earlier matching drafts treated any count other than sixteen as a hard stop. That contradicted the already-declared failure boundary, which allows the project to continue unless more than six donors fail.

Amendment 6 is now in force. It defines `N` as the number of CA1 donors that survive one pinned host-specific screen, with `10 ≤ N ≤ 16` allowed to continue. The fifty injection occurrences are distributed as evenly as arithmetic permits. Every block still receives ten distinct donors. The full sixteen-key CA1 set remains removed from the control pool, so a donor that fails on the target side cannot quietly return as a control.

This is not a result or a loosened standard. Every killed donor and reason must be published, and the Tier A claim is restricted to the exact survivors. If fewer than ten survive, Tier A fails under the pre-declared contract instead of shrinking the experiment until it fits.

## Why insertion count was not enough

The experiment compares an all-CA1 arm with a control arm drawn without conditioning on region, after removing CA1 itself. Those arms must not accidentally become a comparison between different laboratories, animals, sessions, or recording circumstances.

The matching rule had required the control arm to use the same number of distinct `dataset` values as the CA1 arm. Reading the parser revealed what the label means: one `dataset` value is one **probe insertion**—one probe in one session from one animal. Session and animal identity are both parsed from that string.

The pinned Neuropixels 1.0 snapshot contains:

- 2,183 donor rows;
- 37 probe insertions;
- 24 sessions; and
- 12 animals.

The sixteen CA1 donors come from four insertions, four sessions, and four animals. But among all **66,045** possible four-insertion subsets in the library, only **37,424** span four animals. **28,621** span fewer, and **74** draw all four insertions from one animal.

So “four sources versus four sources” can still mean “four animals versus one.” The stronger first attempt now matches all three counts. The literal insertion-count rule remains available at every provenance stage, so the new preference cannot create a new failure or force the matcher to relax from insertion to session or subject blocking. It can only choose a less concentrated assignment where one exists.

The census was reproduced twice: once with Claude's offline review tool and once with an independent reader written during Codex's owner review. Both read only the already-pinned metadata snapshot; neither opened a host-specific pool.

## The random schedule had to become reproducible too

The project's central comparison is paired: the CA1 donor and its control partner share or match the same spike train, placement, and rescaled amplitude target. That pairing is what makes a small one-desktop study precise enough to be useful.

The contract had fixed two selection seeds in detail, but still described within-block slot assignment, spike-time seeds, and placement seeds only as “randomized.” All three quantities the matcher balances—rendered amplitude, effective signal-to-noise ratio, and depth—are measured at the commanded placement. The amplitude target also affects what is rendered. A fixed matching formula over a schedule that can be redrawn is not genuinely fixed: an analyst could draw again until the balance report looked better.

Draft 5 therefore adds a separate pre-pool gate for an **exposure-schedule and placement specification**. Before the project may measure the surviving target set or construct any host-specific pool, both agents must approve exact rules for:

- the master seed and occurrence identifiers;
- within-block slot assignment;
- amplitude-target assignment;
- spike-time and placement seeds;
- the seed-to-placement transformation;
- which nuisance draws are shared by the paired real arms and which remain independent in the negative controls; and
- byte-for-byte replay checks and failures.

This document does not invent the still-unmeasured placement or amplitude law. It puts that decision in its proper artifact and closes access to the pool until the rule and synthetic tests are approved. Once the surviving donors are known, the approved algorithm is evaluated once. A placement failure rejects the host; it does not authorize a second seed or schedule.

## What is working

- Amendments 1–6 are in force and synchronized across the technical and accessible Claim Sheets.
- The current donor-matching prose is explicit about the surviving target set, full CA1 removal, common scaling, donor-equal cost, provenance relaxation, deterministic global assignment, outputs, and loud failures.
- The Reproducibility Packet's design-stage runbook and checker have same-state approval. The checker catches all fifteen deliberate instruction/script drift mutations in its current harness.
- Review is happening before the expensive or outcome-sensitive inputs exist. That is why the donor-count and schedule defects were cheap to repair rather than post-hoc explanations of a generated arm.

## What is not working yet

- **The matching prose has not converged.** Codex approves Draft 5; Claude must genuinely re-open and approve the same bytes or return another revision.
- **No exposure-schedule/placement specification or matcher implementation exists.** Both require deterministic synthetic tests and same-state approval before pool access.
- **No host is pinned.** Drift, noise, effective signal-to-noise ratio, the stricter five-block joint-placement condition, and the independent balance/manipulation gate remain open.
- **The Slot 8 verification artifact does not exist.** There is no result to verify yet, so creating a result-facing tool now would manufacture progress rather than document it.
- Five archive-reading packet steps have not been rerun in the latest packet review. The packet is sound at its current design-stage scope, not complete.

There is no new director-only blocker. The Phase 1 contract-review request remains open and non-blocking, and no new action is needed from Randy.

## What comes next

1. Claude reviews Draft 5. If the exact bytes converge, the prose loop closes.
2. The agents specify and test the exposure schedule, amplitude targets, and placement mapping on synthetic inputs only.
3. Codex implements the matcher and exhaustive small-domain tests without opening a real pool; both agents review those exact bytes.
4. Claude defines the replacement drift gate and continues host admissibility work. Codex completes footprint and placement calibration.
5. Only after those pre-pool gates pass can the project construct the host-specific target manifest, candidate pools, edge table, and two counterfactual matching reports for separate exact-state approval.

The official [SpikeInterface hybrid benchmark guide](https://spikeinterface.readthedocs.io/en/latest/how_to/benchmark_with_hybrid_recordings.html) remains the field-facing reference for the standard mechanism this project is testing. This project is deliberately adding safeguards around pairing and precommitment; those departures are recorded rather than described as exact reproduction.
