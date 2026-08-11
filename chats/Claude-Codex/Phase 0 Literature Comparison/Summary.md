# Summary — Phase 0 Literature Comparison

**Date range:** 2026-08-11 (Claude Session 1, 10:24 PDT) — 2026-08-11 (Claude Session 2, 12:10 PDT)
**Participants:** Claude, Codex
**Outcome:** Converged. **Phase 0 closed.** Discussion continues in `chats/Claude-Codex/Claim Sheet Review/`.

---

## What the chat was for

Both agents wrote independent Phase 0 Literature Foundations. This channel compared them, surfaced disagreements, and settled what was load-bearing before Phase 1 drafted the Claim Sheet.

## What was settled

**The realism axis ladder — agreed, one axis at a time.**

- **Tier A — region-matched templates.** Configuration and selection, no new generator code. Gated on a joint host/template feasibility and covariate-balance audit.
- **Tier B — local population-rate coupling.** The anchor paper's *own* proposed remedy: drive injected spike trains with a locally estimated population rate while holding mean rate and refractory behaviour fixed. Cheaper than bursting and with prior art in the Kilosort4 hybrid simulator.
- **Tier C — burst plus spike-history-dependent waveform attenuation.** The genuinely missing mechanism; the most direct stress test of short-ISI and collision handling; the easiest to implement unrealistically.

A combined/factorial arm is interpretable only after component effects are known, so it is not part of the initial design.

**The primary comparative estimand is a paired difference in differences** — the realism-induced accuracy change for sorter A minus the change for sorter B — with the decision threshold predeclared in raw paired accuracy units, not in standardized effect sizes.

**The manipulation check is a stop-or-go gate**, with axis-specific pass criteria (region: waveform-feature separation with amplitude/SNR/probe/placement balanced; population coupling: injected-versus-local rate trajectory agreement with mean rate and refractory violations controlled; burst: short-ISI distribution and history-dependent amplitude attenuation inside predeclared biological bounds). If the check fails, no sorter run starts, because a sorter null would then be a statement about the implementation rather than about the field's method.

**Nothing was blocked on the director at any point.**

## The two corrections Codex raised, and Claude accepted

1. **The stale template-library premise.** Claude's Session 1 work carried a 601-template, visual-cortex-skewed picture of `hybrid_template_library`, taken from the SpikeInterface tutorial's rendered snapshot. Codex audited the live first-party CSV and found 7,877 rows — 2,183 Neuropixels 1.0 across 37 source datasets and 170 area labels. Claude independently re-downloaded and reproduced the audit byte-for-byte (same SHA-256), and marked the stale claim superseded in `agents/Claude/references.md`. Claude's Literature Foundation stays frozen with the stale premise in it, per the forward-propagation rule; the ledger governs.

2. **Cohen's *d* as a ranking-flip threshold.** Claude had proposed using the anchor paper's Kilosort4-versus-Kilosort2.5 effect sizes (0.276 NP1.0, 0.408 NP2.0) as the bar for whether realism could flip a ranking. Codex blocked it: the two quantities are standardized over different denominators and sampling structures, so the comparison is not a defined operation. Accepted. The anchor's *d* values are retained as **contextual calibration** — they establish that sorter-versus-sorter differences in this domain are small-to-moderate, which sets the precision the study needs — while the decision threshold is measured inside the experiment as the paired sorter gap in raw accuracy units.

## What Claude added on top of the convergence

- **Sign reversal is not the only decision-relevant comparative event.** A sorter gap that goes from clearly separated to statistically indistinguishable changes a reader's conclusion as much as one that reverses, and is the likelier outcome. Both are predeclared.

- **Tier B carries a circularity confound in Kilosort4's favour.** Because the Kilosort4 hybrid benchmark already modulates ISIs by local population rate, adding population coupling to the SpikeInterface pipeline moves the test data toward Kilosort4's home benchmark. A Kilosort4-favouring Tier B interaction therefore cannot cleanly separate robustness from familiarity, and is predeclared as inconclusive-on-attribution rather than as a clean positive.

- **Tier A has the weakest mechanistic prior for moving rankings.** Region mismatch changes static waveform shape, which sorter front ends consume similarly; the temporal tiers hit collision handling, where sorter families are documented to diverge. So a Tier A null licenses no conclusion about the temporal tiers, and the project is not concludable on Tier A alone.

- **Dataset provenance must be balanced across arms, not merely excluded.** Codex's rule excluded the host recording's own source dataset from donor templates. Claude extended it: also balance the *number* of contributing source datasets across the matched and mismatched arms, or provenance rides along with region as a confound.

- **The sorter-panel pilot needs a predeclared budget and a named fallback**, so a marginal pilot result does not become a mid-Phase-2 negotiation.

## The new empirical result

Claude ran a leave-one-dataset-out stress test on the template library, which is what Codex's own leakage rule implies. Under a caliper of amplitude 50–200 µV (the anchor paper's rescaling range) and SNR 5–15, 1,149 of 2,183 Neuropixels 1.0 templates survive across 149 areas, and **37 areas hold ≥10 in-caliper templates**. But after dropping each area's single largest contributing source dataset, **only 7 areas keep ≥10: CP (42), PIR (19), SUB (18), VISa5 (17), AId5 (14), MRN (14), ENTl5 (10)** — and 13 of the 37 collapse to zero, because one dataset supplied all their templates.

The consequence is a conditional, not a count: a host recording outside the library's 37 source datasets leaves region selection essentially unconstrained; a host inside them constrains the region axis to a 7-area shortlist. Either way, **host selection is now downstream of donor availability rather than parallel to it.** Both numbers move with the caliper, which is a declared parameter.

Script: `Reproducibility Packet/scripts/audit_template_library.py` (stdlib only). Output: `Reproducibility Packet/results/template_audit_2026-08-11.txt`.

## Verification debt

**Cleared by Codex:** the anchor companion paper's "key ingredients" quotation is real and appears in the official eLife v1 XML alongside the "core features" formulation; Kilosort4's advertised "non-stationary spike waveforms" are drift-dependent, and it has population-coupled spike timing but no within-burst ISI-dependent amplitude attenuation — so Tier C remains a genuinely missing mechanism.

**Still open:** whether SHYBRID transports individual spike snippets or re-renders an average template (quarantined, not citable); plus the items in Claude's `references.md` *Pending* section (Quirk & Wilson, the regional waveform-duration figures, Steinmetz & Ye 2022).

## Where to go next

The Claim Sheet is where every design commitment above now lives, and where the contestable ones should be argued. Claude wrote the draft as default writer; Codex is the required reviewer and gives final approval. The review runs in `chats/Claude-Codex/Claim Sheet Review/` under `Playbooks/review-cycle.md`.
