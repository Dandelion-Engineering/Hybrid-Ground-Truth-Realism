# Codex Human Report — Session 48

**Date and time:** 2026-08-19 05:30 PDT

**Phase:** Phase 2 — Execution and specification review

**Outcome:** RC-008 Draft 34 is **frozen and unapproved at the Round-3
limit**. The terminal delta pass reproduced every declared repair, but found
that the only remaining reason offered for the decision-affecting contiguous
split is false for the fixed even/odd alternative actually under review. The
bounded **Convergence Decision is triggered**. Codex has recorded one four-field
statement and explicitly proposes and approves **`Split/Redesign Required`**;
Claude owes the other statement and explicit consensus or the smallest
counterproposal. No fourth repair round, estimator, candidate noise read, host
decision, generation step or sorter run is authorized.

---

## 1. Startup and controlling boundary

The automation turn gate named Codex and `.agent-session.lock` was absent. The
first PowerShell lock attempt used a parameter combination unavailable in this
host; it did not create a file. I then created the lock atomically through
`.NET` with `FileMode.CreateNew`, re-read `.agent-turn`, and confirmed it still
named Codex before any project work.

I read `AgentPrompt.md`, the complete Project Details, Codex continuity, all
Codex-participant chat summaries, both active transcripts, the governing review
playbook, and Claude's Session-48 report. The owed task was the Round-3 terminal
delta review of Draft 34 under RC-008. This is RC-007's one clause-5 successor;
if exact-state approval did not occur here, the method required a Convergence
Decision rather than a fourth candidate repair.

## 2. Candidate authentication and owner evidence

Draft 34 authenticated at the carded selection-document digest
`ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89`.
The specification checker authenticated at `2f20099…`, and every one of the
nine carded files matched its recorded SHA-256 digest. The three frozen
selection-document spans remained unchanged:

- §1–§16: 144,664 bytes, `700b3b9a…`;
- §17: 21,864 bytes, `dc73b87f…`;
- §18: 20,579 bytes, `8af3e62c…`.

The previously omitted timing index remained at `043a4ea4…`, now reached by
the checker's input-discovery authentication rather than a hand-maintained
partial list.

All owner evidence reproduced:

- `probe_rc008_spec.py`: **241 / 241**;
- closed `probe_rc007_spec.py`: **288 checks with exactly the expected 16
  failures**, exit 1;
- `mutate_rc008_spec.py`: **42 / 42 repairs caught**, control green;
- owner `probe_rc008_round3.py`: **32 / 32**.

The Round-3 repairs to F6-R2, F7-R2 and T5-R2 through T7-R2 therefore verify.
The corrected §19.8 ratio sentence and the newly published nonvoting `rho(k)`
series also verify. No new legacy-failure class appeared.

## 3. Independent evidence

I created `agents/Codex/tools/probe_rc008_round3.py` and its TXT/JSON records.
The final probe passes **33 / 33**. It authenticates Draft 34 and the frozen
spans, replays the owner evidence, checks the split's ordered-branch reach, and
derives the wrapper's consumed-input population from the executable syntax
tree rather than trusting a copied list.

SHA-256 digests:

- probe: `75b77dc565de8f17a8425612b3e7a6d78317ed90056249406a3d4340e36d6ff2`;
- TXT record: `136389b0ae5b0e16acdca2bdd4a783c20dc6269aa036be50b9438b4c0ed60352`;
- JSON record: `e41758b9c7e8e7ad9db15c57a855e1dc66ec9075c801471927a5e84a1c1b8ed1`.

The probe reads no archive sample, candidate noise value or network resource.

## 4. Blocking finding F8-R3

Draft 34 says the entire surviving reason to choose midpoint-contiguous halves
is that an interleaved split carries a free period whose unsigned effect could
be tuned, whereas the midpoint split carries no free choice. The concrete
alternative reviewed in F6-R2 is not a tunable-period family. It is the
canonical fixed even/odd partition of all 13,020 retained indices.

Both rules are fixed before any candidate value is visible:

- midpoint-contiguous: first 6,510 indices versus last 6,510;
- even/odd: even indices versus odd indices.

Claude's own parity fixture uses exactly that fixed even/odd rule and changes
the ordered disposition from `passes` to `unmeasurable`. It varies the data's
periodic pattern, not a split-period parameter. The asserted free parameter is
therefore absent from the reviewed alternative.

This is blocking because the statement is the **whole stated rationale** for a
parameter with a demonstrated decision destination. The strongest facts
against blocking are real but narrower: the chosen split is predeclared, no
safety or optimality claim remains, and all sixty `rho(k)` values are published.
Those safeguards prevent result-dependent tuning and make the convention
auditable. They do not select midpoint-contiguous over fixed even/odd.

## 5. Convergence disposition

The Round-3 non-approval triggers the card's bounded Convergence Decision.
Draft 34 is frozen; no further candidate edit is permitted on RC-008.

Codex's single required statement records:

- **Minimum claim that can ship:** Draft 34 may survive as the frozen record of
  the repairs that verified, but cannot approve §19 or authorize an estimator.
- **Remaining uncertainty or disagreement:** no supported basis selects one
  fixed, complete split from the two decision-affecting alternatives.
- **Strongest evidence against Codex's position:** predeclaration and complete
  `rho(k)` publication eliminate post-result tuning and expose the convention.
- **Acceptable safe disposition:** **`Split/Redesign Required`**, with a changed
  boundary around the split instrument before any new card opens.

Codex explicitly proposes and approves that terminal disposition. Claude owns
the other statement and the consensus exchange. Because RC-008 is the one
allowed like-for-like successor, another §19 repair card with the same boundary
is forbidden.

## 6. Append-only transcript correction

The first verdict append matched an older repeated `---` footer in the active
chat and landed before Claude's final handoff. A first correction repeated that
placement error. In accordance with the append-only rule, neither entry was
deleted or rewritten. I then anchored a dated correction against the verified
physical tail: 503 lines before append, 532 after; the 05:25 PDT header occurs
exactly once after the old EOF and the transcript again ends in `---`. Readers
should treat the physical-EOF 05:25 entry as the controlling Codex handoff.

## 7. Files created or updated

**Created**

- `agents/Codex/tools/probe_rc008_round3.py`
- `agents/Codex/tools/rc008_round3_2026-08-19.txt`
- `agents/Codex/tools/rc008_round3_2026-08-19.json`
- `agents/Codex/Session Summaries/HumanReport48.md`
- `agents/Codex/Progress Reports/Progress Report Session 48.md`

**Updated**

- `Review Cards/RC-008 Host Noise Gate, Convergence Repair.md`
- `Review Cards/README.md`
- `chats/Claude-Codex/Section 19 Convergence Repair/Section 19 Convergence Repair - Active.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No Claude candidate, Claim Sheet, Accessible Claim Sheet, Study Guide,
Reproducibility Packet or result file was edited.

## 8. Resource and execution note

No heavy step ran. Work was limited to local source/text authentication and
short deterministic probes. There was no archive or network access, no GPU
work, no dependency installation, no candidate sample read, and no reason to
perform a heavy-step RAM/VRAM admission measurement.

## 9. Next steps

1. Claude must record exactly one four-field Convergence statement and either
   explicitly agree with `Split/Redesign Required` or name the smallest
   counterproposal on terminal disposition.
2. If consensus is Split/Redesign, close RC-008 and its chat without editing
   Draft 34, then name a materially changed split-instrument boundary.
3. No new host-noise card may be a like-for-like fourth repair. No estimator or
   candidate noise measurement starts until a redesigned specification earns
   explicit same-state approval.
4. Rank 1 remains approved only on its strict drift statistic. Noise, effective
   SNR, joint placement feasibility and balance remain open; rank 2 remains
   unmeasured.
