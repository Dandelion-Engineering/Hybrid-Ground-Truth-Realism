# Codex Human Report — Session 51

**Date and time:** 2026-08-19 11:28 PDT

**Phase:** Phase 2 — Execution (open-ended Part-B specification design,
outside formal review)

**Outcome:** Claude Session 51 supplied the completion-bound proof requested in
Codex Session 50 and asked whether the resulting publication changes belong in
the future successor card's Part-B scope. Codex replayed Claude's 45-check
evidence byte-for-byte, independently closed Claude's stated production-size
gap at the real 72-channel band, found no mathematical blocker, and ruled that
both the Part-B decision vocabulary in section 19.6 and the Part-B-owned
publication fields inside section 19.7 belong in the eventual card. Existing
Part-A publication fields remain frozen regression surface. No split member was
selected, no successor Review Card or section 19 candidate was opened, no
estimator exists, no candidate noise was read, no host was pinned, and no
downstream execution was authorized.

---

## 1. Startup and controlling context

The automation turn gate named Codex and no `.agent-session.lock` existed.
Codex created the lock atomically, re-read `.agent-turn`, confirmed it still
named Codex, and only then began project work.

The required `AgentPrompt.md` workflow was followed in order:

1. read `Project Details/Project Details.md` in full, including the public-run,
   compute, virtual-environment and no-email boundaries;
2. read Codex's `Summary of Only Necessary Context.md` in full;
3. read every `Summary.md` in every Codex-including chat;
4. read both active Codex-including chats in full before replying to either;
5. read Claude's newest collaborator report, `HumanReport51.md`, and the exact
   work it points to.

The three-party `Review Method Change` chat remains active at Randy's standing
request but has no pending Codex response. The only pending response was in
`chats/Claude-Codex/Part B Resolution Diagnostic Design/`.

Codex Session 51 is not a count-based progress-report session. The completed
cadence reports are 8, 16, 24, 32, 40 and 48; the next is Session 56. No phase
transition occurred and no Claim Sheet amendment was approved, so no event
trigger fired.

## 2. Collaborator work cross-reviewed

Claude Session 51 checked the completion-interval criterion Codex proposed in
Session 50. The criterion treats each valid-input `0/0` channel ratio as an
explicit non-value whose completion may occupy `[0,+inf]`, computes the exact
nearest-rank p90/p10 lower and upper endpoints, propagates the endpoints through
the maximum across windows, and lets branch 4 stand down only when the upper
endpoint is at or below `M`.

Claude's owner evidence made four main claims:

- a three-level enumeration agrees with a refined-grid exhaustive search on 36
  small fixtures;
- the maximum is attained at a zero/infinity vertex but the minimum often
  requires an interior placement;
- at the real `n = 72` ranks 8 and 65 give a threshold of eight undefined
  contacts, while seven can still be decision-irrelevant;
- a third branch-3 label is needed when the spatial value falls inside the
  completion enclosure.

The owner report stated its own limitation correctly: exhaustive validation
was at `n = 10..12`, while use at `n = 72` rested on generalization plus samples.
Claude asked for a second independent derivation at `n = 72` if that gap needed
to be closed. Codex treated that as the session's bounded technical task rather
than beginning the later split-member comparison.

## 3. Owner evidence replayed exactly

Codex ran Claude's exact source in the project virtual environment:

`venv/Scripts/python.exe agents/Claude/tools/probe_completion_bounds.py`

The replay passed **45/45** and reproduced both committed records byte-for-byte:

- TXT SHA-256:
  `d14c1471bca1623f7fe6f5280cec225bd5e66ec7f54222178e1caa2495c62b66`;
- JSON SHA-256:
  `bb9465f0657e51b6c9c87d80d8d3b79265e744aa2496ee8dde9ba2d886f8870f`.

This established exact-state determinism. It was not treated as independent
mathematical confirmation, consistent with the distinction both agents have
recorded since Session 50.

## 4. Independent production-size derivation

Codex created:

`agents/Codex/tools/probe_completion_bounds_n72.py`

The script imports none of Claude's source or functions. It derives the full
production-size endpoints directly from the declared nearest ranks, then checks
the derivation by exhausting completion *multisets* rather than ordered tuples.
The order-pattern construction keeps exhaustive `n = 72` checking small without
turning it into another copy of the owner's three-level enumeration.

Script SHA-256:
`864b6e01dfc8006d22c6a64432e27eadce0117948ba433673735bcb7ede65490`.

At `n = 72`, the declared ranks are `i10 = 8` and `i90 = 65`. For `u <= 7`
undefined ratios and a positive finite eighth defined value, with `f` one-based
and sorted, the direct endpoints are:

- lower: `f[max(65-u, 8)] / f[8]`;
- upper: `max_{a=0..u} f[65-a] / f[8-a]`, where `a` unknowns are placed below
  every defined value and the remaining `u-a` above every defined value.

The evidence passed **11/11**:

- **24 full-size discrete rank patterns**;
- **34,320 exhausted completion multisets**;
- **zero endpoint mismatches**;
- **512 continuous positive finite pools**, zero endpoint-witness mismatches;
- **16,384 sampled interior completions**, zero enclosure escapes;
- **16 zero/infinity rank-8 edge fixtures**, zero failures;
- every undefined count from **8 through 72** has one explicit completion that
  makes the band ratio infinite or undefined, zero failures across 65 counts.

The independent check reproduced the two examples whose contrast makes the
policy nontrivial:

- seven undefined values with finite ratios `[1.0]×7 + [3.0]×58` give exact
  enclosure `[1.0, 3.0]`, changing the current scalar-convention pass into
  `unmeasurable` at strict `M = 2`;
- seven undefined values over the homogeneous finite ramp give
  `[1.049652, 1.057000]`, so branch 4 may stand down and the unknowns are proved
  decision-irrelevant rather than automatically rejected.

It also independently exercises reachability of all three branch-3 labels:
`resolved heterogeneity` above the whole enclosure, `resolution-limited` at or
below the whole enclosure, and `unresolved` inside it.

The final deterministic records are:

- `agents/Codex/tools/completion_bounds_n72_2026-08-19.txt`, SHA-256
  `ce680287736e37f57389cfe61d5b8d75d6e1180a2a3a10e2607a8b418b3571f2`;
- `agents/Codex/tools/completion_bounds_n72_2026-08-19.json`, SHA-256
  `20c6e963e53d122702e059ff737d08bd82c74f6964ec67eb8f799399545b4a34`.

Two runs produced identical hashes. The script compiles, exits zero, renders an
11-line ASCII-only help surface, and both records contain LF line endings with
zero CR bytes.

**Ruling:** no mathematical blocker remains in the completion-bound rule at the
production band size.

## 5. Exactness boundary retained

The word *exact* is bounded to the declared per-ratio completion space. Each
`0/0` channel ratio is independently allowed to occupy `[0,+inf]`; the reported
endpoints are exact over that abstract space.

That does not establish how often real recordings produce undefined ratios,
that every interior value is attainable from a physical perturbation of the
underlying samples, or that the independent per-window completion choices form
a physical generative model. The rule is an assumption-free conservative
decision envelope, not a measured frequency statement. Claude's message already
respected this boundary; Codex made it explicit in the reply so it travels into
the eventual specification.

## 6. Scope ruling posted to Claude

Codex answered Claude's question directly:

**The successor card's Part B must cover both section 19.6's decision vocabulary
and the Part-B-owned publication clauses inside section 19.7.** A decision rule
cannot be reviewed independently of the record needed to audit it.

The heading boundary does not move wholesale. The eventual card should state:

- **in scope:** Part B's estimator semantics, branch-3 labels, branch-4 rule,
  second-order band-level `0/0` disposition, and new/changed publication fields;
- **excluded but regression-checked:** unchanged Part-A statistics, gates and
  publication fields already assigned to the split-independent side by RC-008.

The current-live Part-B statements in sections 19.5, 19.6, 19.7 and 19.10 must
be counted mechanically once a stable candidate exists. Historical draft
records remain historical rather than repair targets.

The future Part-B publication set needs at least:

- undefined channel identities and counts per window;
- each window's lower, upper and undefined-reachable state;
- the aggregate maximum's endpoints and the window or windows setting them;
- the second-order band-level `0/0` state;
- the raw per-half scale estimates and defined per-window values already
  promised.

A single scalar `R_null_sampled` can no longer be the only published object
after the rule stops treating every channel as scalar.

This was posted as Codex Session 51 in the active Part-B chat. The append was
made only after a physical UTF-8 tail read, a pre-write line count and a unique
multi-line EOF-anchor check. The post-write read found the new header exactly
once after the old line count, retained LF-only bytes and retained the trailing
newline.

## 7. Public heartbeat

The root Live-Run README was checked under `Playbooks/live-run-readme.md`. Its
newest entry explicitly identified small-size exhaustion as the proof's open
limitation. The independent production-size derivation closes that stated gap,
which met the playbook's genuinely-noteworthy threshold.

One forward-only entry was appended. It states the 34,320 multiset exhaustion,
512 additional patterns, the seven-versus-eight distinction, and the unchanged
execution boundary. The banner date already read 2026-08-19 and was not changed.
The running log now has 95 dated entries; the new entry occurs exactly once and
is the last dated line before the log separator. No earlier entry was edited.

## 8. Challenges and corrections

The main technical challenge was avoiding a second implementation of Claude's
argument disguised as independent evidence. The solution was to derive closed
rank-index formulas at the production size, then exhaust completion multisets
over full-size rank patterns. This checks a different object from the owner's
small-n refined-grid enumeration while retaining exact endpoint witnesses.

One edge remained outside the positive-finite closed form: rank 8 itself can be
zero or infinite. The final independent tool handles that explicitly and shows
both states are already withheld for every `u = 0..7`, so the formula covers
the only branch-4-live case. It separately supplies a universal eight-zero
witness for every `u >= 8` rather than inferring the claim from one uniform
pool.

During the README pre-write check, one initial anchor-count expression used a
PowerShell single-quoted string containing literal `` `n `` characters and
therefore returned zero. No write occurred. The anchor was reconstructed with
real newline characters, verified unique, and only then used. This was a
validation-command correction, not a project-file repair.

## 9. Files created or updated

**Created**

- `agents/Codex/tools/probe_completion_bounds_n72.py`
- `agents/Codex/tools/completion_bounds_n72_2026-08-19.txt`
- `agents/Codex/tools/completion_bounds_n72_2026-08-19.json`
- `agents/Codex/Session Summaries/HumanReport51.md` (this report)

**Updated**

- `chats/Claude-Codex/Part B Resolution Diagnostic Design/Part B Resolution
  Diagnostic Design - Active.md` — one verified append-only Codex reply
- `README.md` — one forward-only public running-log entry
- `agents/Codex/README.md` — Session-51 navigation and tool description
- `agents/Codex/Summary of Only Necessary Context.md` — rewritten at closeout

**Not changed**

- every Review Card;
- `agents/Claude/Tier A Host and Injection Zone Selection.md` (Draft 34 remains
  frozen and unapproved);
- every file in `Reproducibility Packet/`;
- both Claim Sheets, Study Guide, requirements and references;
- the three-party Review Method Change chat.

No new external source was read, so `agents/Codex/references.md` did not need an
entry.

## 10. Resource and execution boundary

No heavy step ran. The owner replay and independent synthetic check each took
well under one second and used no GPU. No archive, network resource, candidate
sample, raw recording, template asset or external data was read. No dependency
was installed, no background job was started, and no temporary replay artifact
remained after verification.

No candidate noise value exists. No host-noise estimator exists. Rank 1 remains
discharged on drift alone; rank 2 remains unmeasured; no host is pinned; and no
donor, manifest, Rung 0, generation or sorter action is authorized.

## 11. Next steps

1. Read Claude's response to the Session-51 scope ruling before changing the
   Part-B design.
2. Compare the fixed-member and possible multi-member constructions under the
   now-verified common completion semantics. Do not use the earlier fixture
   matrix to claim real-data frequency or to defeat a disclosed fixed
   convention by itself.
3. Count every current-live Part-B surface mechanically before a stable
   candidate is declared, especially sections 19.5, 19.6, 19.7 and 19.10.
4. Open a successor Review Card only after co-design yields a stable candidate.
   It must name `Supersedes: RC-008`, the material Part-A/Part-B split, and the
   exact in-scope publication fields.
5. Keep rank 2 and all downstream execution blocked. Rank 1 has not been
   rejected.
