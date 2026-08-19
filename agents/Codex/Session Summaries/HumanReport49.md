# Codex Human Report — Session 49

**Date and time:** 2026-08-19 07:18 PDT

**Phase:** Phase 2 — Execution and specification design

**Outcome:** RC-008 is closed at **`Split/Redesign Required`**, but Claude's
new unreviewed sensitivity sweep over the 32-member split family overstates what
its correct matrix establishes. Codex reproduced both Session-49 owner probes
byte-for-byte, then independently showed **30 strict pairwise dominance
relations** in that matrix. The correction is now in a new open-ended Part-B
design chat. No successor card exists, no estimator or candidate noise value
exists, no host is pinned, and no execution gate moved.

---

## 1. Startup and controlling context

The automation memory was read, then `.agent-turn` named Codex. No
`.agent-session.lock` existed, so I created it atomically with
`.NET FileMode.CreateNew`, re-read `.agent-turn`, and confirmed it still named
Codex before project work.

I read `AgentPrompt.md`, the complete Project Details in ordered chunks, Codex's
continuity file, all seventeen Codex-participant chat summaries, and the only
active three-party transcript in full. No response was due there: its latest
message is already Codex Session 42 and Randy asked that the chat remain active.

Claude Session 49 was the newest unreviewed collaborator work. It closed RC-008
at the terminal disposition Codex proposed, preserved frozen Draft 34, concluded
the card chat, and introduced two synthetic probes as explicitly **unreviewed**
input for the materially changed Part-B design boundary. I also read the
superseding review-cycle playbook before recording a substantive artifact
finding.

No progress report was due. The most recent count-based report is Session 48;
the next is Session 56. No phase transition or approved Claim Sheet amendment
occurred.

## 2. RC-008 closure accepted as concluded state

Claude accepted F8-R3 and explicitly approved `Split/Redesign Required`. The
closed card's stronger family result is sound:

- the 13,020 retained samples have two equal halves of 6,510;
- the 32 divisors of 6,510 define 32 fixed block-interleaved equal partitions;
- `p=6,510` is midpoint-contiguous and `p=1` is even/odd;
- on Draft 34's parity fixture, 16 fixed members produce `passes` and 16 produce
  `unmeasurable`;
- the branch reach remains exactly 9 pass/unmeasurable movements, 6 resolution
  relabels and 57 unchanged states, with no failure-boundary crossing.

The required material change separates split-independent **Part A** from the
resolution-diagnostic **Part B**. Part A alone is strictly more permissive and
cannot certify a host. I did not reopen RC-008, its concluded chat, or Draft 34.

## 3. Reproduction of Claude's Session-49 evidence

Both owner probes were rerun through the project virtual environment into a
temporary directory:

- `probe_rc008_convergence.py`: exit 0, TXT and JSON byte-identical to the
  committed records, **22/22**;
- `probe_split_family_sensitivity.py`: exit 0, TXT and JSON byte-identical to
  the committed records, **12/12**.

The sensitivity matrix itself is therefore reproduced. It has 1,024 finite
member-by-fixture values, all 32 members withhold on their own constructed
fixture, no one member withholds on all 32 fixtures, and no one member withholds
on none.

## 4. Forward correction to the sensitivity interpretation

The source probe equates those last two facts with “the family has no
dominating member.” That inference is invalid. Dominance is a pairwise set
relation, not a requirement that one member withhold on the whole fixture
universe.

I inverted the recorded table. For each member `p`, I computed the set `S_p` of
constructed fixtures on which it withholds. Strict dominance on this matrix is
`S_b` being a proper subset of `S_a`. The exact result is:

- `S_1` is all sixteen odd-target fixtures. `p=1` strictly dominates each of
  the other fifteen odd members.
- `S_2` is all sixteen even-target fixtures. `p=2` strictly dominates each of
  the other fifteen even members.
- Those are exactly the **30** strict dominance relations; there is no
  cross-parity dominance and no pair of equal signatures.
- `S_1` and `S_2` are disjoint and their union covers all 32 constructed
  fixtures. A two-member OR envelope covers this synthetic set.
- The self-target row contains sixteen withholding members for `p_t=1`, one for
  `p_t=2`, and two for every other target. The source report's minimum-one row
  does not establish that every possible pin is nearly isolated on its own
  fixture.

The narrower supported result is still useful: the split parameter is
decision-live; every member has a constructed self-hit; and no single member is
uniformly withholding or uniformly passing on this set. But the sweep does not
establish absence of dominance and, by itself, does not defeat “pin one and
disclose it.” Different decisions on adversarially member-matched fixtures show
sensitivity, not automatically invalidity of an arbitrary disclosed convention.

The `p=1/p=2` envelope is **not** proposed as a real-data diagnostic. It is only
a property of this constructed fixture family and now becomes one piece of
open-ended design evidence.

## 5. Independent witness and communication

I created `agents/Codex/tools/probe_split_family_dominance.py`, a stdlib audit
that consumes the owner JSON through required CLI arguments, reconstructs every
signature, enumerates strict dominance, and records the exact narrower result.
It passed **12/12**, with source-record SHA-256
`f51b4949e8406b7bb237a49ecb3af985ce5127896a680e28c58b67f06a9b4fcb`.
The script's SHA-256 is
`ca7eefeaa5e1fa9bda69059b0ff1b7a30ef7588bc23f2e3e01b574a58dd72d37`.

Because RC-008 is concluded and corrections propagate forward, I opened:

`chats/Claude-Codex/Part B Resolution Diagnostic Design/Part B Resolution Diagnostic Design - Active.md`

The first message gives the complete finding, the exact dominance structure,
the evidence boundary, and the request that Claude narrow the probe/report
claims before using them as successor-card input. The chat is explicitly
open-ended co-design. Formal review begins only after a stable candidate and a
new Review Card exist.

## 6. Challenge and method note

The first replay command was rejected before execution because it combined a
computed temporary path with recursive cleanup. It created nothing. I reran the
same work without destructive cleanup, obtained the byte-identical results,
and used an explicit resolved temporary path for later cleanup.

The substantive method lesson is sharper: a check can be numerically correct
and its verbal conclusion false because the checked condition is not the
definition of the claimed property. Here, “no all-fixture member” was checked;
“no pairwise dominance” was claimed. Turning the matrix around exposed the
gap without changing one source value.

## 7. Files created or updated

**Created**

- `agents/Codex/tools/probe_split_family_dominance.py`
- `chats/Claude-Codex/Part B Resolution Diagnostic Design/Part B Resolution Diagnostic Design - Active.md`
- `agents/Codex/Session Summaries/HumanReport49.md`

**Updated**

- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten

No Claude candidate, Review Card, Claim Sheet, Accessible Claim Sheet, Study
Guide, Reproducibility Packet, result artifact, public README or references
ledger was edited. No new external source was used.

## 8. Resource, public-heartbeat and execution note

No heavy step ran, so no heavy-step RAM/VRAM admission measurement was needed.
The work used local text, JSON and two short synthetic probes; there was no
archive or network read, no candidate sample read, no GPU work, no dependency
installation and no background job.

The public Live-Run README heartbeat was checked and left unchanged. Correcting
an unreviewed design input is important internally but does not change a public
artifact, approved gate, phase, candidate result or execution status.

## 9. Next steps

1. Claude should respond in the new Part-B design chat and narrow the source
   probe/report claims before treating the sweep as successor input.
2. Open formal review only after open-ended co-design yields a stable Part-B
   candidate. Its card must name `Supersedes: RC-008` and the Part-A/Part-B
   material change; a like-for-like fourth §19 repair is forbidden.
3. Test whether any proposed diagnostic has a stated target property and valid
   evidence for it. Do not infer real-data caution or optimality from the 32
   constructed fixtures.
4. Keep rank 2 drift unmeasured unless the pinned first-admissible sequence
   creates a real need. No host-noise estimator or candidate read is authorized.
