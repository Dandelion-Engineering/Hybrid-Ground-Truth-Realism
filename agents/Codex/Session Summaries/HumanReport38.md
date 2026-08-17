# Codex Human Report — Session 38

**Date and time:** 2026-08-17 02:12 PDT

**Phase:** Phase 2 — Execution

**Outcome:** Claude's corrected completed-`N` missing-depth null design was
authenticated and accepted for pre-card construction. I also accepted the two
open input policies: NaN is the only missing-depth marker while either infinity
remains a fatal input error, and a null destination bin containing only missing
values has the exact unbounded interval `(-inf, +inf)`. The owner harness passes
86/86 and the unchanged approved drift harness passes 103/103 at the pinned 200
permutations. This is a design ruling, not RC-005 approval. The strict finite-
depth confirmation still binds, ranks 1 and 2 remain paused, and no scientific
result exists.

---

## 1. Startup and controlling workflow

The automation memory was read first. `.agent-turn` then named Codex and no
`.agent-session.lock` existed, so I created the lock and re-read the turn file;
it still named Codex. Only then did project work begin.

I completed the context-first workflow in `AgentPrompt.md`: read
`Project Details/Project Details.md`, the current Claim Sheet and all six
in-force amendments, Codex's continuity, all twelve chat summaries involving
Codex, both active transcripts, Claude's Session-38 human report and continuity,
and the superseding review-cycle playbook. The repository began clean and
synchronized at `9c6738b` (`Claude Session 38`).

The machine reading at 02:08 PDT was 17,962 MB available physical RAM of 32,425
and 1,034 of 16,311 MiB GPU memory used. Nothing in this session was heavy: all
execution used deterministic synthetic NumPy fixtures, no archive or network
resource was read, no dependency was installed, and no background process was
left running.

## 2. What Claude corrected

Claude accepted the Session-37 ruling that the proposed fixed-arrangement
counterfactual did not bound the gate's actual null. The corrected module now
uses the complete analysed vector length `N`, the original missing source
positions, and the approved replicate seed to fix the entire permutation before
any missing depth value is chosen. Missing source slots are followed to their
destination bins, the exact per-bin median interval is applied there, and the
result is propagated through the approved centring, across-unit median, window
scan and nearest-rank percentile.

That is the quantity the gate actually consumes on every completed record. The
finite-only null remains a useful point diagnostic, but it permutes `n` observed
values rather than the completed `N` and is correctly not described as one of
the completions when any depth is missing.

The module's API now takes the complete positional record: every spike time and
an aligned depth array with NaN in the missing positions. This removes the
silent ambiguity that would arise if positions were reconstructed from times
when two spikes share a timestamp.

## 3. Evidence authenticated and reproduced

The handed-off hashes reproduce exactly:

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `5a9cfde418069799ce159ce3d25890004bdff6f95f8b8f75fc99ab51833ea17c` |
| `agents/Claude/tools/test_missing_depth.py` | `435272af7a5fc37ba9a83eaaa48e77823c3e1e72e61eb90a818bbc8b8df620f5` |
| `agents/Claude/tools/probe_missing_depth_crossover.py` | `57554ac16d8080e52db7afefadad85235baecfc20aecfb20accd611b71685c10` |

I read the full corrected module, the approved null implementation it wraps,
the relevant owner tests, and the two open design cases. The executed evidence:

- `test_missing_depth.py --permutations 200 --completions 200`: **86 checks,
  0 failed**. Direct completed-record null containment, zero-missing elementwise
  identity, support invariance, unbounded destinations, exclusions and all four
  stability quadrants pass.
- `test_band_drift.py --permutations 200`: **103 checks, 0 failed** against the
  unchanged approved estimator and null.
- Codex's Session-37 probe preserves its first seven completed-data checks:
  `[12.254, 18.618] µm`, non-vacuous width, three actual completions contained,
  and both zero-missing replicate paths identical. It then raises where its
  eighth check calls the now-removed counterfactual signature. That failure is
  the expected forward correction, not a regression.

The owner evidence also corrects the earlier crossover scale. Under the actual
completed-`N` null the synthetic sweep crosses the 20 µm tolerance between
0.498% and 0.990% missing on that fixture, earlier than the superseded
counterfactual estimate. This remains scale on one construction, not a fitted
rule and not a quantity to compare mechanically against the whole-band missing
fraction of a real candidate.

## 4. Design rulings

The complete ruling is appended to the active Non-Finite Spike Depths chat.
This remains open-ended co-design before a stable candidate, not Round 1 of a
formal review.

### Completed-`N` null

**Accepted as the pre-card design requested in Session 37.** The construction
bounds the actual completed-data null, not a substitute quantity. Its exactness
and conservatism are stated at the right levels: exact for each bin's attainable
median set, an outer bound after dependence is discarded above the bin, with
the error only toward pausing a candidate that a tighter treatment might admit.

### Infinite depths

**Accepted as fatal input errors.** The measured recoverable class is NaN with
a finite time. Both candidate censuses found only NaN and no infinities.
Treating infinity as another missing marker would extend the relaxation to an
unmeasured wrong-value class and could re-label corruption as uncertainty. The
reader must reject either sign before exclusion accounting and the command must
write no verdict.

### All-missing null destinations

**Accepted as defined but unbounded.** If a destination bin's complete count
meets the floor but every depth assigned there is unknown, every finite median
is attainable. `(-inf, +inf)` is therefore the exact interval and must propagate
as a defined unbounded bin, producing an unmeasurable disposition. An empty bin
with zero missing values still has no median and correctly raises.

### One forward prose correction

The module broadly says that both interval endpoints are reached by finite
completions. That is true for finite bounded endpoints. An unbounded side has no
completion at infinity, although every finite value on that side is attainable.
Claude should qualify this wording before RC-005. The code and ruling are
already correct.

## 5. Immediate owner and downstream boundary

**Immediate owner: Claude.** The next stable state should include, as one
candidate:

1. reader support for the complete aligned record and missing-position mask;
2. the accepted NaN/infinity distinction;
3. command publication of exclusions per unit, per bin and in total;
4. the point diagnostics, both completed-data sensitivity intervals and the
   stability disposition;
5. forward §17 prose without editing closed §16;
6. rerun acceptance and mutation evidence after the reader/command repair; and
7. a new RC-005 and fresh review chat only after that whole state is stable.

Until same-state approval closes RC-005, the strict finite-depth confirmation
remains operative. Rank 1 and rank 2 remain paused, not rejected. Ranks 5, 7, 9
and 13 remain separately paused on declared-clock disagreement. No host is
pinned; no candidate has a drift, noise, effective-SNR, donor, placement,
generation or sorter value; and no downstream authorization moved.

## 6. Append-only and public-state checks

Before the chat append, the transcript contained 804 physical UTF-8 lines and
no Codex Session-38 header. The patch used the unique physical EOF boundary.
After the append, the transcript contains 865 lines; the new header occurs
exactly once and only after the old line count; `git diff --unified=0` shows a
single 61-line EOF append and no earlier transcript edit.

The root public README already records Claude's corrected completed-`N` design.
This session supplied the private pre-card disposition and did not finish an
artifact, close a phase or produce a new scientific measurement, so a second
public heartbeat would duplicate the existing entry and was not added. No
external source was read, so `agents/Codex/references.md` did not change.

## 7. Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport38.md`

Updated:

- `chats/Claude-Codex/Non-Finite Spike Depths/Non-Finite Spike Depths - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No approved implementation artifact changed and no progress report was due.
