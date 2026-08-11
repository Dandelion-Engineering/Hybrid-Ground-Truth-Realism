# Human Report 1 — Codex

**Date and time:** 2026-08-11 11:16 PDT
**Session:** Codex Session 1
**Phase:** Phase 0 — Literature Review
**End state:** Both independent foundations exist; Phase 0 comparison is open and blocked on Claude's response to two corrections.

## What I did

I completed Codex's independent Phase 0 literature survey and its reference ledger. The survey was built from live primary-source searches, official documentation/source code, and first-party dataset metadata. It covers the ground-truth landscape, benchmark calibration, resources and licensing, known failure modes, the causal estimand, a staged realism-axis design, and the questions that must be fixed in the Claim Sheet.

I also audited the live SpikeInterface template metadata directly rather than relying on the tutorial's rendered snapshot. The live table is substantially larger and more diverse than Claude's first-pass sources indicated. I recorded the row counts, distributions, high-count areas, response metadata, and SHA-256 checksum so the observation is reproducible and so later work knows the online table is mutable.

Finally, I read Claude's Human Report, Literature Foundation, living reference ledger, continuity summary, and workspace guide. I answered Claude's four questions in the append-only Phase 0 chat, cleared two major verification debts, agreed to the manipulation-check gate, and gave a direct cross-review verdict.

## What matters scientifically

### The primary question is an interaction

The project must distinguish two claims:

- realism changes absolute accuracy; and
- realism changes the comparison between sorters.

The second is tested by a paired difference in differences: the change caused by realism for sorter A minus the change caused by realism for sorter B. A uniform accuracy loss can invalidate absolute scores without changing rank; a concentrated differential loss can change rank while looking small in an aggregate mean.

Claude proposed using the anchor paper's Kilosort4-versus-Kilosort2.5 Cohen's d values (0.276/0.408) as the threshold for whether realism can flip ranking. I blocked that inference. Those standardized effects have their own denominator and sampling structure; they cannot be compared mechanically with a raw accuracy change. They remain useful context, but the decision threshold must be predeclared in raw paired interaction/rank terms with uncertainty.

### The realism axes form a ladder

I recommended:

1. **Region matching** after a joint host/template and covariate-balance gate.
2. **Local population-rate coupling**, which is cheaper than bursting and directly follows the anchor paper's proposed remedy.
3. **Burst plus waveform-history coupling**, including empirically bounded ISI-dependent amplitude attenuation.

These should start as one-axis paired experiments. A combined arm can follow after component effects are understood. The Kilosort4 paper provides prior art for local population-rate coupling, which makes Tier B less speculative; it does not appear to provide the burst-dependent amplitude dynamics proposed for Tier C.

### The sorter panel should span mechanisms

Kilosort4 plus two CPU internal SpikeInterface sorters is a defensible candidate panel. TriDesClous 2 and either SpyKING CIRCUS 2 or Lupin provide more useful mechanism contrast than another Kilosort version. This is not yet a machine-feasibility claim. The chosen candidates must be piloted on the same short segment after a live RAM/VRAM check.

## Live template-library audit

The tutorial's displayed 601-template table is stale. The live first-party CSV contained:

- 7,877 rows total;
- 2,183 IBL/Neuropixels 1.0 rows;
- 37 IBL source datasets and 170 IBL area labels;
- amplitude 52.19–923.15 µV, median 184.22 µV;
- SNR 2.43–48.44, median 9.78.

The CSV SHA-256 was `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`.

This resolves the broad concern that the library is only about 600 mostly visual templates. It does not prove any particular matched/mismatched arm is feasible. The host and donor templates must be co-selected, covariates balanced, and the host recording's exact source dataset excluded by default to prevent leakage.

## Verification debt

Two high-priority items were cleared:

- The official Garcia et al. 2026 XML contains both the “key ingredients” and “core features” formulations. The quote in the project brief is valid.
- Kilosort4's advertised non-stationary waveforms are drift-dependent; I found population-coupled spike timing but no evidence of burst-dependent amplitude attenuation.

One narrow item remains: SHYBRID's abstract confirms spike relocation, but I did not verify from full primary text whether it transports individual spike snippets or re-renders an average template. That detail remains quarantined.

## Cross-review verdict and project state

Claude's foundation is strong on taxonomy, biological mechanism, manipulation checks, pairing, licensing, and sorter diversity. I blocked use of its current exact state as the settled synthesis on two issues:

1. the living record must incorporate the live template audit rather than carry forward the stale 601-template/visual-skew feasibility premise; and
2. the Cohen's d values must be reframed as context rather than a sufficient ranking-flip threshold.

Claude marks its Literature Foundation frozen, so I asked for the corrections to propagate into Claude's living ledger, continuity, and later Claim Sheet. Claude must also read Codex's foundation and explicitly accept or object in chat. Phase 0 remains open. Nothing is blocked on the director.

## Files created or updated

| Path | Change |
|---|---|
| `agents/Codex/Literature Foundation.md` | Created — independent Phase 0 survey |
| `agents/Codex/references.md` | Created — living verified source ledger |
| `agents/Codex/README.md` | Written — workspace map and authority guide |
| `agents/Codex/Summary of Only Necessary Context.md` | Rewritten — next-session continuity |
| `agents/Codex/Session Summaries/HumanReport1.md` | Created — this permanent report |
| `chats/Claude-Codex/Phase 0 Literature Comparison/Phase 0 Literature Comparison - Active.md` | Appended — answers, evidence, and block verdict |
| `README.md` | Appended — public heartbeat for the second foundation and metadata audit |

## Compute and environment

No heavy compute, sorter execution, dependency installation, or raw-data download was needed. Therefore I did not perform a launch-time RAM/VRAM measurement; the standing rule remains to measure both immediately before every heavy job and not launch without headroom. I did not invoke bare Python or modify the repository `venv`.

## Next step

Claude should cross-review Codex's foundation, update its living evidence/continuity for the two corrections, and answer the active comparison chat. If the exact state converges, Claude can close Phase 0, write the phase-transition Progress Report, and begin the Claim Sheet as default writer.
