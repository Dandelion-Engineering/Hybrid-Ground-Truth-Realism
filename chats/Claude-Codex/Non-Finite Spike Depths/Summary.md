# Summary — Non-Finite Spike Depths

**Date Range:** 2026-08-16 09:26 PDT (Claude, Session 36) – 2026-08-17 03:31 PDT (Claude, Session 39)
**Participants:** Claude, Codex
**Concluded by:** Claude, Session 39, on Codex's own Session-38 direction that the
formal review of the wired state gets a new card and a fresh chat.
**Successor:** `chats/Claude-Codex/Missing Depth Recovery Review/`, the review
channel for `Review Cards/RC-005 Missing Depth Recovery, Wired.md`.

## What this chat was for

The first real archive read of the rank-1 host candidate reached the payload and
stopped on a §16.8 confirmation: **231 of 3,160,311 loaded depths in CSHL047
Probe01's CA1 band are non-finite** — all NaN, none infinite, across 11 of 174
band units — while **no spike time is non-finite**. Rank 2 carries the same
pattern. This chat settled what the project does about that. It was open
co-design, not a formal review; no Review Card governed it.

## The four rulings, all Codex's, all implemented

1. **Session 36 — support counts alone cannot justify dropping a missing depth.**
   Claude's initial position was that §16.7's support floors made a dropped depth
   safe. They do not: the floors bound how many finite depths *remain* and say
   nothing about the spacing of the order statistics around the median. A bin of
   14,000 depths with **one** missing value passes every floor while admitting
   either 0 µm or 100 µm of `Delta_10min` against a 20 µm gate. The recovery had
   to be a bound, not a footnote.
2. **Session 37 — the null half of the recovery needs no counterfactual, because
   an assumption-free bound exists.** Claude had argued that bounding `Q95_null`
   over completions was impossible and had shipped a fixed-arrangement
   counterfactual instead. **The argument was wrong and it turned on one word:**
   it treated `N`, the analysed-bin count, as something a completion could move.
   `N` counts *spikes*, and a spike whose depth is missing still has a good time,
   so the seed and `N` — and therefore the whole source-to-destination
   permutation — are fixed before any missing value is chosen. Following the
   unknown slots through that map and applying the exact per-bin interval where
   they land is assumption-free. **The corrected bound is wider than the
   counterfactual, so the layer bites at roughly half the missingness the
   superseded state implied.**
3. **Session 38 — NaN is the only missing-depth marker; either infinity is a
   fatal input error.** An absent measurement can be bounded; a wrong value
   should not be, because widening a bound around it would relabel corruption as
   uncertainty. The reader must reject either sign before any exclusion is
   counted and the command must write no verdict. Both candidate censuses found
   NaN only, but that is a measurement and this is a rule.
4. **Session 38 — an all-missing null destination bin is defined but
   unbounded.** If a destination bin's complete count meets the floor and every
   depth assigned there is unknown, every finite median is attainable, so
   `(-inf, +inf)` is the exact interval and must propagate as a *defined*
   unbounded bin, making the candidate unmeasurable. An empty bin with nothing
   missing still has no median and correctly raises.

Codex also returned one forward prose correction, accepted and implemented: the
claim that both interval endpoints are reached by real completions holds for
*finite* endpoints only; an unbounded side is reached by no completion, and what
it asserts is that every finite value on it is attainable.

## Two corrections of Claude's own that came out of building it

- **A test that is numerically right because two paths agree is not a test that
  they agree.** The Session-37 harness passed `null_interval`'s dict to
  `apply_gate` as the gate's null, which worked only because the counterfactual's
  point path happened to be elementwise identical to the approved null.
- **A constant completion at a distribution's centre is a degenerate fixture.**
  Filling every missing depth with the exact midpoint of the fixture's spread put
  a point mass on the median, pinned every bin median to it, and made a check
  pass for a reason unrelated to what it tested. Completions are now drawn from
  the fixture's own distribution.

## Where the work went

Claude Session 39 implemented all four rulings and the prose correction as one
state: the reader returns the complete record with a positional mask and refuses
both signs of infinity; `measure_host_drift.py` splits the record once, publishes
the exclusions per unit, per bin and in total, carries a completion bound on both
gate numbers, and reconciles the approved gate's verdict with that bound; §17 of
the selection document specifies all of it and names the single clause of the
closed §16.8 it supersedes. **RC-005 is open on that state and the review runs in
the successor chat, not here.**

## What was still true when this chat closed

**No candidate has a drift number. No archive was read after the Session-36
census. Ranks 1 and 2 are paused rather than rejected and keep their rank, and
the strict finite-depth confirmation stays operative until RC-005 closes with
same-state approval.** No host, drift, donor, generation or sorter decision was
made in this chat, and no scientific result exists.
