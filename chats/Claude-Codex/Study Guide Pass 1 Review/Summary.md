# Summary — Study Guide Pass 1 Review

**Date range:** 2026-08-11 (Claude Session 3, 14:20 PDT) — 2026-08-11 (Codex Session 4, 17:09 PDT)
**Participants:** Claude, Codex
**Outcome:** Converged. Study Guide Pass 1 received explicit same-state source/PDF approval and the review concluded.

## Approved state

- Source `Study Guide/Pass 1 - Conceptual Foundation.tex`: SHA-256 `d33e74d73c41b3ef0b4edbe6de52c0cc4e5597bae2d048618edb5c4523f99819`
- Compiled `Study Guide/Pass 1 - Conceptual Foundation.pdf`: SHA-256 `75e1423294cb3c4695c14920851825d602379d9ffca1aab6bcb93cbd10d998a3`

## What the review settled

- A multichannel template reflects probe-relative position plus cell anatomy, tissue, and probe geometry.
- SHYBRID reuses observed times after a fixed shift and per-spike fitted amplitudes, while the insertion train receives fresh random sub-sample jitter by default; it does not transport arbitrary observed waveform shapes unchanged.
- Tier A needs no new generator mechanism but still requires selection, balance, and analysis work.
- The interaction sign and interpretation were corrected: a near-zero interaction means the between-sorter comparison is stable, not that absolute scores are valid.
- The guide now teaches `D = |I| - T`, the conservative folded-at-zero negative call, the complete hierarchical resampling structure, and the one-host conditional boundary.
- CA1 remains a candidate subject to host-specific feasibility and balance gates; below-range manipulations do not pass the biological-realism gate.
- A wrong section cross-reference was corrected, and the control-arm explanation now includes the refractory period already implemented upstream, explaining why refractoriness is not a missing realism axis.

The final PDF is 13 letter-size pages. It compiled twice with no document warnings or overfull/underfull boxes; Codex rendered and visually reviewed all pages and confirmed that the approved PDF's extracted text matches an independent rebuild. Study Guide Pass 1 is complete.
