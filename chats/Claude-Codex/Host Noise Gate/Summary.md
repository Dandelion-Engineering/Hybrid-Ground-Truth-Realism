# Summary — Host Noise Gate

**Date Range:** 2026-08-18 00:19 PDT (Claude Session 43) — 2026-08-18 06:13 PDT (Claude Session 46)
**Participants:** Claude (owner), Codex (reviewer)
**Review Card:** `Review Cards/RC-007 Host Noise Gate Specification.md` — **CLOSED at `Revisions Required`**
**Successor:** `Review Cards/RC-008 Host Noise Gate, Convergence Repair.md`, chat `chats/Claude-Codex/Section 19 Convergence Repair/`

## What this chat was

The whole of RC-007: three owner-reviewer round-trips on §19 of
`agents/Claude/Tier A Host and Injection Zone Selection.md`, the specification
of the **noise gate** — the second of §15.5's five host gates — written as a
contract before any estimator exists and before any candidate's noise value is
known to anyone. Drafts 29 → 30 → 31, then the Convergence Decision.

## How it ended, and why that matters more than a verdict

**Round 3 returned one blocker the Round-3 response itself created, which under
the superseding review method triggers the agent-only Convergence Decision
rather than a fourth exchange.** Both agents wrote their one statement into the
card; **the terminal disposition is `Revisions Required` by explicit two-agent
consensus.** Draft 31 is frozen and unapproved, no candidate byte was edited
after the freeze, and the owner's repair was made **outside formal review** as
Draft 32. That is the method working as designed rather than a review failing:
the loop ended in four sessions with a named disposition, without spending a
single director-day.

## The substance, for anyone picking this up cold

**Round 1** returned six blocking finding families. The largest: §19's proposal
to reduce host admissibility from five gates to four was **withdrawn in full**;
the preprocessing chain moved from a brick-wall DFT high-pass to the anchor
pipeline's own fifth-order Butterworth through `sosfiltfilt`; the three gated
quantities were renamed `sigma_worst_sampled`, `R_space_sampled`,
`R_null_sampled`; the pass rule's branches were ordered; input errors were
separated from unmeasurable rejections.

**Round 2** returned two blockers the Round-1 response created.

- **F4-R1** — twelve synthetic fixtures were not a bound on filtering a chunk in
  isolation, proved by a counterexample built inside `int16` on the file's own
  2.34375 µV lattice. **Repaired by removing the construction rather than
  bounding it:** a window is now filtered as its chunk plus 500 real samples
  from each neighbouring chunk, which makes it an *instance* of
  `FilterRecording.get_traces` at `margin_ms="auto"` rather than an
  approximation. Transfer tripled to 957,031,364 bytes as a result.
- **F7-R1** — the claim that within-window non-stationarity can only inflate the
  split-half statistic is false, because an observed ratio is a *product* and
  products cancel. **Withdrawn in full:** `R_null_sampled` is a **one-sided**
  instrument, and a candidate that passes, passes on `R_space_sampled` alone.

**Round 3** was the final response and it introduced **F7-R2**: the withdrawal
prose said a high `R_null_sampled` is *sufficient* to withhold the measurement,
which §19.6's own ordered branches contradict at the high-space/high-null state
— branch 3 fires first and the candidate **fails on homogeneity**. Claude
concurred, disputed nothing, and added one correction of scope: **the claim was
live on four surfaces, not three** (the fourth is §19.12).

## What the repair is, decided against approved text

Draft 32 makes **the prose yield to the branches**, not the reverse. The
controlling evidence is **§16.7**, approved and closed since Session 17: its
drift rule has the identical asymmetry in the identical cell, and the two rules
— implemented from their own documents — **agree in all four cells**, while
reordering §19.6 would change exactly one, the disputed one. The rule is now
written once: **`R_null_sampled` can convert a would-be pass into
`unmeasurable`, and can change how a failure reads; it never converts a would-be
failure into anything else.** The tracked contiguous-versus-interleaved split is
**settled as contiguous**, before any candidate's value is known.

## State at conclusion

- **No host is pinned.** Rank 1 (CSHL047 Probe01) has passed the drift gate only.
- **Rank 2 remains unmeasured.** Four ranks stay paused on the declared-clock
  disagreement.
- **§19 is unapproved.** No estimator exists, no candidate's noise value exists,
  no archive sample was read in any session of this chat, and no packet file
  changed.
- **Clause 5 now applies:** RC-008 is the one permitted successor. A second
  non-approval on the same scoped purpose requires a split or redesign, not
  another card.

Continue in `chats/Claude-Codex/Section 19 Convergence Repair/`.
