# Codex Human Report — Session 36

**Date and time:** 2026-08-16 10:10 PDT

**Phase:** Phase 2 — Execution

**Outcome:** Claude's proposed treatment of non-finite spike depths is **not
accepted as written**. The real-input evidence justifies a recovery, but the
existing support floors do not bound the influence of missing depths. A new
implementation-level counterexample passes every support floor at 0.00714235%
missingness while admitting `Delta_10min` values of 0 and 100 µm. Rank 1 remains
paused under the strict finite-depth confirmation. Claude owns a pre-card
response to a missingness-sensitivity counterproposal; no RC-005 candidate
exists.

## Startup and controlling workflow

`.agent-turn` named Codex and `.agent-session.lock` did not exist. I created the
lock, reread `.agent-turn`, and confirmed that it still named Codex before doing
project work. I then completed the `AgentPrompt.md` context-first workflow:

- read `Project Details/Project Details.md` and the full governing standards;
- read Codex's Session-35 continuity;
- read every `Summary.md` and both active Codex-participant chats;
- read Claude's Session-36 report and the files it points to;
- read the current review-cycle and Live-Run README playbooks before using them;
- reviewed the clean committed state at `2e09f59` (`Claude Session 36`).

The next count-based progress report remains due in Codex Session 40.

## Cross-review of Claude Session 36

RC-004 is now closed `Approved` at Round 2. Claude explicitly approved the same
five hashes Codex approved in Session 35, concluded the review chat, and then ran
the separately governed rank-1 command.

The rank-1 plan-only read completed. The real drift command stopped before any
verdict or output because unit 901 carries one non-finite spike depth. Claude's
read-only diagnostic then reported:

- rank 1 CSHL047 / Probe01: 231 NaN depths in 11 band units among 3,160,311 band
  spikes; zero non-finite times; 140 units meet the support floor both before and
  after dropping; no qualifying bin is lost;
- rank 2 NYU-12 / Probe01: 222 NaN depths in 10 band units among 4,898,466 band
  spikes; zero non-finite times; 182 units meet support both ways; no qualifying
  bin is lost.

I read `agents/Claude/tools/probe_nonfinite_depths.py`, authenticated its recorded
SHA-256 `ade3660f…`, inspected both JSON/text outputs, and checked the affected
unit/bin distributions. The maximum recorded count is 16 missing depths in one
rank-1 unit/bin and 15 in rank 2; both candidates distribute the affected values
across 50 recording bins. I did **not** repeat an archive read, so the archive
measurements remain Claude-produced rather than independently re-downloaded in
this session. That limitation does not control the disposition below, which is
defeated by a local construction against the approved estimator.

Claude also recorded that every affected unit in both candidates is labelled
`mua` and explicitly refused to use that post-hoc association. I agree. The
selection remains label-blind, and no `good`-only recovery is authorized.

## The blocking gap in the proposed disposition

Claude proposed treating a non-finite depth as a counted/published per-sample
exclusion, keeping a non-finite time fatal, and letting §16.7's predeclared
support floors protect the statistic.

The first and second parts are viable directions. The third is insufficient:
the floors require at least ten finite depths in at least 80% of bins and at
least five included units per analysed bin. They bound the number of finite
observations that remain. They do **not** bound:

- how many depths are missing relative to those finite observations;
- how far apart the finite order statistics around the median are;
- how the within-bin median could change across compatible missing values; or
- the effect of a unit whose depth trace is wholly absent.

Publishing those facts is necessary for audit but does not make the host verdict
decision-stable. The rank-and-offset idea Claude cited is the right foundation,
but it has to be consumed by a gate rather than left as a limitation.

## Independent estimator counterexample

I added `agents/Codex/tools/probe_nonfinite_depth_disposition.py`, SHA-256
`efb03c8e661bba8eabd87010c94cf2fed61bff34a4433b514704e62e5765e729`.
It imports the approved `Reproducibility Packet/scripts/utils/band_drift.py`
`eace4cd356b2618d806227c4be69e3fc0ee8fe1568e68c7ab2be249ce3605ef0`
and exercises `measure_band_drift` directly.

The construction uses five identical units across twelve full bins. Each
unit/bin has 14,000 observed finite depths and one missing depth. The finite
values are split at 0 and 100 µm, so their complete-case median is 50 µm in every
bin. Every support and bin-validity floor passes. Missingness is 0.00714235%,
slightly below rank 1's reported aggregate 0.00731%.

The results are:

- complete-case point estimate: `Delta_10min = 0.000000 µm`;
- one compatible completion of the missing entries: `0.000000 µm`;
- another compatible completion, low in the first half and high in the second:
  `100.000000 µm`;
- existing strict gate: 20 µm;
- six checks passed, zero failed.

The construction does not claim that every NaN conceals a meaningful physical
depth. It is a sensitivity proof: the same observed finite record and the same
missingness count do not identify one host-drift disposition. A small fraction
does not imply a small effect when the finite order statistics have a central
gap.

The tool also passes `py_compile`, renders `--help`, and passes at its default
0.09990010% missingness as well as the recorded 0.00714235% run.

## Disposition and counterproposal

I appended the ruling to
`chats/Claude-Codex/Non-Finite Spike Depths/Non-Finite Spike Depths - Active.md`:

**Do not implement the proposal as written. The strict finite-depth confirmation
continues to bind and rank 1 remains paused, not rejected.**

The proposed recovery is:

1. drop non-finite depths only for the point estimate; keep non-finite times as
   input errors;
2. compute an assumption-free sensitivity interval from each unit/bin's missing
   count and finite order statistics;
3. propagate it through within-unit centring, the across-unit band median,
   `Delta_10min`, and the null quantity consumed by the gate;
4. use the already declared 20/40 µm gate to decide stability — no post-hoc
   missingness percentage; a disposition-changing or unbounded interval makes
   the candidate unmeasurable and keeps it paused;
5. publish exclusions and sensitivity outputs per unit, per bin and in total;
6. before RC-005, test Claude's mirror failures, an all-depths-missing unit, this
   support-passing construction, and exhaustive small-array interval
   containment.

This is open-ended co-design before formal review, as the review method requires.
Claude should create RC-005 only after the implementation/documentation state is
stable enough to accept, reject or return.

## Append-only and public-state checks

The active-chat append was hard-gated against the verified 200-line UTF-8 file
at SHA-256 `b56762fd…`. After the append:

- the original 200-line byte prefix has the same SHA-256;
- the Codex Session-36 header occurs exactly once after the old count;
- the physical tail ends with the required separator.

Claude's latest public heartbeat says the sample-count floors already do the
protective work. Because the estimator counterexample directly overturns that
claim, I read the Live-Run README playbook and appended a forward public
correction. Earlier history remains untouched. The new entry records the 0/100
µm construction, the returned pre-implementation proposal, and the unchanged
boundary that no host or scientific result exists.

## Files created or updated

- `agents/Codex/tools/probe_nonfinite_depth_disposition.py` — local six-check
  counterexample against the approved estimator.
- `chats/Claude-Codex/Non-Finite Spike Depths/Non-Finite Spike Depths - Active.md`
  — append-only ruling and counterproposal.
- `README.md` — append-only forward correction to the public live-run log.
- `agents/Codex/README.md` — navigation and current-state update.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for
  Session 37.
- `agents/Codex/Session Summaries/HumanReport36.md` — this report.

No source was added to `references.md`; the session used project artifacts and
local synthetic evidence only. `.gitignore` already excludes bytecode, the
virtual environment, large archive data, scratch outputs and agent lock files;
no ignore change was needed.

## Boundary and next steps

No network or archive resource was read by Codex. No approved packet or selection
artifact changed. No RC-005 candidate exists. No host is pinned; no candidate
drift, null, noise or effective-SNR value exists; no donor, placement, target
manifest, generation, Rung 0 or sorter result exists.

**Immediate owner: Claude.** Accept the missingness-sensitivity boundary or
counter-propose the smallest conservative recovery. Rank 1 remains paused until
that design is implemented, reviewed under a new card, and same-state approved.
