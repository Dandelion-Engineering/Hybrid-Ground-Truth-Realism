# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 1 · 2026-08-11 11:16 PDT**
**Next Codex session will be Session 2.**

## Current state

The project remains in **Phase 0 — Literature Review**. Both independent foundations now exist, and Codex posted the substantive comparison in:

`chats/Claude-Codex/Phase 0 Literature Comparison/Phase 0 Literature Comparison - Active.md`

Phase 0 is not closed. Codex blocked the current synthesis on two precise issues that Claude must answer in its next session:

1. replace the stale 601-template / visual-skew feasibility premise in living context with the live metadata audit; and
2. treat the anchor paper's Cohen's d as contextual scale, not a sufficient ranking-flip threshold.

Claude's Literature Foundation is marked frozen, so corrections should go into Claude's living `references.md`, continuity, and later Claim Sheet—not silently rewrite the dated foundation. Claude must also cross-review Codex's foundation and explicitly accept or object in chat. Nothing is blocked on the director.

## Codex Session 1 outputs

- `agents/Codex/Literature Foundation.md` — six-section Phase 0 evidence survey.
- `agents/Codex/references.md` — living ledger with 13 verified primary or first-party sources and no citation debt for claims retained in the foundation.
- `agents/Codex/Session Summaries/HumanReport1.md` — permanent session report.
- `agents/Codex/README.md` — workspace map and authority guide.
- Root `README.md` — one append-only running-log heartbeat for the second foundation and live metadata audit.

## Findings to preserve

### Experimental structure

- The comparative estimand is the paired sorter-by-realism interaction (difference in differences), not the realism main effect alone.
- With two sorters, ranking stability is only the sign of their paired difference. Rank correlation requires at least three sorters.
- Use a sequential axis ladder: **Tier A region matching**, **Tier B local population-rate coupling**, **Tier C burst plus waveform-history coupling**. Do not start with a full factorial.
- A generator-only manipulation check is a stop-or-go gate before any sorter run.
- A clean negative requires a narrow interval excluding a decision-changing interaction; a wide null is inconclusive.

### Source and verification findings

- Kilosort4's hybrid simulator already couples firing to local population rate in 100 ms bins; this is prior art, not a novel mechanism. Its “non-stationary waveforms” are drift-related, not evidence of within-burst ISI-dependent amplitude attenuation.
- The official eLife v1 XML for Garcia et al. 2026 contains both “key ingredients” and “core features” formulations. The project brief's quotation is verified.
- SHYBRID's abstract confirms relocation of a real unit's spikes, but the narrower snippets-versus-average-template detail remains unresolved and should not be asserted.
- The anchor Cohen's d values 0.276/0.408 are useful context only. The Claim Sheet must predeclare a threshold in raw paired accuracy/rank-interaction units with uncertainty.

### Live template metadata audit

On 2026-08-11, the first-party live CSV contained 7,877 rows, including 2,183 IBL/NP1 rows, 37 IBL source datasets, and 170 IBL area labels. The IBL amplitude range was 52.19–923.15 µV (median 184.22); SNR 2.43–48.44 (median 9.78). CSV SHA-256:

`a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`

This establishes broad template availability, not host-specific feasibility. Host recording and donor rows must be selected jointly under area/probe/amplitude/SNR/placement constraints. Exclude the host's exact source dataset by default and snapshot/hash metadata and row IDs.

## Next actions when Codex gets the turn again

1. Read Claude's new session report, living ledger changes, and appended chat response.
2. Re-read the current chat bytes and issue a direct approve/block verdict on the revised synthesis.
3. If Phase 0 has closed, read the Claim Sheet playbook and review Claude's draft; do not assume closure from a rewrite or silence.
4. Before any compute pilot, measure live RAM and VRAM. The only Python environment allowed is the repository-root `venv`; never use bare `python` or `pip`.

No heavy compute, dependency installation, raw-data download, or sorter run occurred in Session 1.
