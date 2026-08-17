# Codex Human Report — Session 37

**Date and time:** 2026-08-17 00:16 PDT

**Phase:** Phase 2 — Execution

**Outcome:** Claude's Session-37 missing-depth work was cross-reviewed before
formal review. I accepted his correction to my first counterexample and the
point-estimate sensitivity design, reproduced his 59-check suite at the pinned
200 permutations, but returned the proposed fixed-arrangement null. An
independent 8-check probe demonstrates that the approved completed-data null
has a finite, non-vacuous, assumption-free interval. The strict finite-depth
rule remains operative; ranks 1 and 2 remain paused; RC-005 does not exist.

---

## 1. Startup and controlling workflow

`.agent-turn` named Codex and `.agent-session.lock` did not exist. I created the
lock, re-read `.agent-turn`, and confirmed it still named Codex before doing any
project work. I then completed the context-first workflow from
`AgentPrompt.md`: read `Project Details/Project Details.md` in full, Codex's
continuity, every summary and active transcript involving Codex, Claude's
latest human report and the work it pointed to, and the superseding review
playbook before issuing a design ruling.

The repository began clean and synchronized at `212b88f` (`Claude Session 37`).
No archive, candidate asset, raw voltage, network resource or external source
was read. No dependency was installed and no heavy compute ran. The work was
bounded synthetic numpy testing; the longest owner harness completed in about
11 seconds at 200 null replicates. The next count-based progress report remains
due in Codex Session 40.

## 2. Cross-review: what Claude Session 37 got right

Claude accepted the Session-36 ruling that support counts alone cannot justify
dropping missing depths. His new
`Reproducibility Packet/scripts/utils/missing_depth.py` supplies:

- an exact attainable interval for one unit/bin median from the finite order
  statistics and the missing count;
- an explicit support-invariance condition across the ten-spike bin floor, the
  80%-of-bins unit floor and the five-included-unit bin floor;
- conservative interval propagation through within-unit centring, the
  across-unit median and the excursion statistic;
- exclusion publication per unit, per bin and in total; and
- a decision rule tied to the existing 20/40 µm gate rather than a fitted
  missingness percentage.

I accept those design pieces. I also accept Claude's correction to my Session-36
evidence. My balanced `0/100 µm` construction establishes that the finite-only
`Delta_10min` can be controlled by missing depths even when all support floors
pass. It does **not** establish that the existing two-number gate passes:
permuting a knife-edge bimodal record gives `Q95_null = 100 µm`, so the existing
gate already calls it unmeasurable. Corrections propagate forward; I did not
edit the earlier probe.

Claude's replacement spread fixture establishes the whole-gate property the
first construction did not: its observed record passes with `Delta_10min =
10.367 µm` and a pinned-200 `Q95_null = 14.604 µm`, while the missing-depth
excursion bound reaches `73.45 µm`. The null cannot substitute for the
sensitivity layer because independent per-unit permutation noise can shrink
under the across-unit median while a coherent missing-data shift does not.

## 3. Evidence reproduced

I read the full 772-line module, the full 890-line owner harness, the crossover
probe and its recorded output. The recorded hashes reproduce:

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/missing_depth.py` | `2064304cec23621474de8b420d8f20f7e88bc7ace1798811b4682b4b2a2948a5` |
| `agents/Claude/tools/test_missing_depth.py` | `73a7c59e4e703f6837f36cd70349ed1836977974b2205857c19cfaa2ffbb46f6` |
| `agents/Claude/tools/probe_missing_depth_crossover.py` | `036c5b8d4ef6df37dbff44b4fc5bfe20b8f3f53e9ce949fa971bae04dd249f10` |

The owner harness passes **59/59** at the pinned 200 permutations and 360
random/extreme completed-record point-estimate checks. All four changed/new
Python files compile. This is positive pre-card evidence, not approval: the
whole reader/command/§17 candidate does not yet exist.

## 4. Why the proposed null counterfactual was returned

Claude argued that an assumption-free interval for the gate's `Q95_null` is
necessarily vacuous because restoring `k` missing values changes a unit's
permutation from length `n` to length `N = n + k`. He therefore proposed a
counterfactual that permutes only the observed `n` depths among observed-depth
times and leaves each completed value at its original time.

The premise is wrong. Once the reader preserves the original all-spike order or
missing-position mask:

1. the completed length `N` is known;
2. the missing source positions are known;
3. the replicate seed is known; and
4. `rng.permutation(N)` is therefore fixed before any missing value is chosen.

A completion changes the values in unknown source slots; it does not change the
permutation. Each unknown slot can be followed to its destination bin, where
the existing exact median interval applies. Propagating those bin intervals
through the approved null gives an assumption-free bound on the actual
completed-data quantity. No range over arbitrary arrangements is required.

This matters semantically. The proposed `null_interval` computes a different
quantity from `band_drift.permutation_null` on a completed record, yet
`stability_verdict` says every completion leaves both gate numbers on one side
of `L`. That statement cannot be licensed by a counterfactual number. The
counterfactual may remain as a clearly labelled, nonvoting diagnostic if it
earns a separate purpose.

## 5. Independent completed-data-null probe

I added `agents/Codex/tools/probe_missing_depth_actual_null.py`, SHA-256
`d1fdfefae8d9b3f0bdfbc8e9de25c82f7ddae83688855c0a2482d4af8cac09b1`.
It is synthetic reviewer evidence, not packet code. At the pinned 200
permutations it passes **8/8**:

- the actual completed-data null interval is finite: `[12.254, 18.618] µm`;
- its width is non-vacuous at `6.365 µm`;
- actual approved-null runs for all-low, all-high and mixed finite completions
  give `15.609`, `15.311` and `15.739 µm`, all inside the bound;
- with zero missing values, the lower and upper replicate paths each reproduce
  all 200 approved-null replicate values element-for-element; and
- the actual interval is distinct from the proposed counterfactual interval,
  `[12.758, 18.440] µm`.

The production design should preserve original missing positions directly.
Missing times alone cannot reconstruct exact source order when two spikes share
a timestamp, even though the synthetic probe deliberately uses distinct times.

## 6. Ruling and next owner

The full ruling is appended to
`chats/Claude-Codex/Non-Finite Spike Depths/Non-Finite Spike Depths - Active.md`.
This remains open-ended co-design under the superseding review method, not a
formal review round.

**Immediate owner: Claude.** Before RC-005:

1. replace the voting fixed-arrangement counterfactual with the completed-`N`
   permutation bound, preserving original missing positions;
2. keep the finite-only approved null as a point diagnostic but do not treat it
   as a completed record when `k > 0`;
3. add direct containment tests against the approved full-`N` null, zero-missing
   elementwise identity, unbounded cases, and exact row-index validation parity;
4. then complete the reader, command, new §17 prose and exclusion/sensitivity
   publication as one stable pre-card state; and
5. only then create RC-005 and its fresh review chat.

The strict finite-depth confirmation remains operative. Rank 1 and rank 2 are
paused, not rejected. Ranks 5, 7, 9 and 13 remain separately paused on declared
clock disagreement. No host, donor, placement, generation, Rung 0 or sorter
gate moved.

## 7. Append-only and public-state checks

Before the chat append, the transcript contained 546 physical UTF-8 lines and
had SHA-256
`0A89D5E36EA8D3F24643C03EE78B66D777114557B7BDBE84F839BAE01F5FFFDE`.
The chosen multiline EOF anchor occurred exactly once. After the append, the
first 546 lines reproduce that SHA-256 byte-for-byte, the Session-37 Codex
header occurs exactly once after the old EOF, and the physical tail ends at the
new boundary marker.

The public README heartbeat was warranted because the null design changed
before implementation: it now records the finite, non-vacuous actual-null
bound and preserves the no-result boundary. The banner date is updated to
2026-08-17. No source was read, so `agents/Codex/references.md` did not change.

## 8. Files created or updated

Created:

- `agents/Codex/tools/probe_missing_depth_actual_null.py`
- `agents/Codex/Session Summaries/HumanReport37.md`

Updated:

- `chats/Claude-Codex/Non-Finite Spike Depths/Non-Finite Spike Depths - Active.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No approved candidate artifact changed. No progress report was due.
