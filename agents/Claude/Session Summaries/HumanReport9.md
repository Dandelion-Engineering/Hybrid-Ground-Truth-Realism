# Human Report 9 — Claude

**Current date and time:** 2026-08-12 14:36 PDT

**Session:** Claude Session 9

**Phase at start:** Phase 2 — Execution
**Phase at end:** Phase 2 — Execution. Amendments 1, 2 and 4 are `In force`; Amendment 3 is `Proposed` at a new Claude-edited state awaiting Codex. **No host is pinned, no hybrid recording or sorter run has happened, and no scientific result about the project's question exists.**

**No progress report is due this session** — the count-based trigger is Session 16, and this session closed no phase and put no amendment into force.

---

## Summary

Two pieces of work. The first was the owner re-review Codex handed back: I verified its three repairs at the substrate, accepted all three, and then found a hole that its third repair had exposed — the negative-control's selection rule was pointed at the real experimental arm. The second was the largest open item nobody was working on and which was mine: completing the brain-structure label map. That turned into a licensing decision that closed the obvious route, and a derivation that made the obvious route unnecessary.

Both are recorded below in the order they happened.

---

## 1. Amendment 3 — Codex's repairs verified, and a hole they exposed

### 1.1 The three repairs, checked at the substrate rather than read

Codex's Session 8 review repaired three parts of the negative-control selector before approving it. I re-derived each from the tracked data rather than from its summary.

1. **The template key.** Codex found that `template_index` does not identify a donated waveform: the counter restarts inside every source dataset. Confirmed exactly — the tracked Neuropixels 1.0 snapshot has **2,183 rows, 187 distinct integer values, and 2,183 distinct (dataset, template_index) pairs**. A contract pinning waveforms by the integer alone would have named an average of 11.7 different waveforms per identifier. This is the kind of defect that would have survived to the results.

2. **Determinism.** My version named a seed and a search family and left the generator, starting draw, sweep order, improvement rule and cap behaviour to whoever implemented it — which relocates analyst freedom rather than removing it. Codex's replacement uses a SHA-256-ranked starting subset with no random-number generator at all, so the start is a function of the identifiers and survives a library version change. Accepted in full.

3. **The rationale.** I had argued that better covariate matching narrows the safety band and worse matching widens it. I have not measured that relation, and the band is sorter-derived while my objective is not. Codex removed it and replaced it with the argument that stands on its own: the risk being closed is the forking path, where several defensible recipes are tried once the pool is visible and the most reassuring is kept. **Accepted, and logged as a correction** — this is the same error class I made in Session 7, stating a plausible direction as though established.

### 1.2 The hole — the control's selection rule was aimed at the manipulated arm

Removing the monotonic story made me ask what the objective actually points at, and the answer was bad.

The pseudo-control's first arm (P1) is chosen to resemble the sixteen CA1 waveforms on three properties. Its search space was "the final eligible region-unaware pool." But the Claim Sheet defines the region-unaware arm as drawing **without conditioning on region** — region-*blind*, not CA1-free. **So the sixteen CA1 waveforms are themselves inside that pool, and the objective's global minimum is exactly zero, attained by those sixteen.**

The rule for building the "nothing was changed" control was therefore a deterministic search whose optimum is the changed arm, over a space containing it. Every CA1 waveform the search recovered would have put the manipulation inside the control — **precisely the failure for which the earlier replicate-band construction was rejected.** We caught it there when it was structural and obvious; it came back through the objective, where it was neither.

**The fix, made in both sheets:** P1's search space is now the eligible pool **minus the injection zone's own donor pool**. Nothing else moves — not the seed, covariates, objective, sweep rule, tie-breaks, cap, rota or budget. Point 3 no longer asserts "neither pseudo-arm conditions on region" as a bare fact; it now argues it, and distinguishes the removal from an inverse manipulation (P1 is not pushed *away* from CA1; CA1 is simply unavailable to a search that would otherwise walk to it).

Two boundaries I stated rather than let the fix imply: the bounded search would not have recovered all sixteen at any plausible pool size, so the defect is that the rule was *aimed* at the matched arm, not that P1 would have *been* it; and the objective is distributional, so other subsets can also score zero — which does not help, because the CA1 sixteen are the one subset guaranteed to.

### 1.3 One observation raised but deliberately not acted on

A complete search sweep costs 16 × (M − 16) evaluations for a search space of size M, against a 100,000 cap that never allows a partial sweep. At M ≈ 1,149 that affords **five sweeps, so five swaps**; at M ≈ 200 it affords enough to exhaust the subset. So the reported "achieved distances" will read very differently depending on pool size.

I did not edit it. It is declared as a bounded search, the stop reason is reported, and after the §1.2 fix there is no direction the cap can bias the result toward — a weaker search now means a P1 *less* like the CA1 sixteen. I raised it so neither agent meets that number for the first time at the configuration gate, and offered to take whatever cap rule Codex prefers.

### 1.4 Codex's scale-factor ruling — accepted

Codex ruled that the systematically different pre-rescaling scale factors must **not** become a matching covariate: rescaling is a linear multiplication, so the sorter observes rendered amplitude, which is already matched; matching the factor would instead constrain the donor-amplitude distribution, which is part of what region *is* in this library, and would over-control the manipulation. That reasoning is better than my question and I accepted it without reservation. The factors are recorded as a manipulation-check diagnostic instead.

---

## 2. The CCF label map — a licence decision, then a derivation

This was the largest open item nobody was working on, it was mine, and it had been deprioritized three sessions running.

**The problem.** Two vocabularies name the same structures. The host recordings spell them out — "Field CA1", "Rostrolateral area layer 5". The donated waveform library abbreviates — `CA1`, `VISrl5`. The hand-authored bridge between them covered the CA1 target but not the rest, which is what the region-unaware comparison arm needs.

### 2.1 The licence, read rather than inferred — and it closed the obvious route

I read the **Allen Institute Terms of Use** directly. The Content may be used "for research or other noncommercial purposes," and "You may not redistribute the Content or Improvements for commercial purposes without our written permission."

That is a real conflict with this project's standard, not a technicality. Dandelion requires commercial-use-permitting licences by default and allows a restrictive input only under an explicitly approved, named exception stating the downstream limits. Importing the ontology would have put a noncommercial restriction on a component of a shipped artifact — a decision about what Dandelion may release, which is the director's, not mine.

I also checked the tempting shortcut and declined it. `iblatlas` is MIT (read at its own licence file: "MIT License", "Copyright (c) 2023 International Brain Laboratory") and `brainglobe-atlasapi` is BSD-3. Both are honest about their own code. **Neither is the Allen Institute, and a third party's permissive licence over a redistribution is not a grant of rights in the upstream content it redistributes.** Treating an MIT wrapper as laundering the terms would have been exactly the "import on the assumption that it will be fine" the standard forbids.

**Nothing was filed in `director_requests.md`, and that was the right call** — because the ontology turned out to be unnecessary, so the director was never the dependency.

### 2.2 The bridge is derivable from data the project already holds

Both sides annotate the same physical places on the same probes, and the project holds both under commercial-use-permitting licences: DANDI 000409 electrode tables (CC-BY-4.0) carry the long name and depth; the template library (MIT) carries the acronym and depth. A donor at 2,900 µm labelled `CA1`, next to a host electrode at 2,900 µm labelled "Field CA1", *is* the correspondence. This is the evidence the existing validator uses to **check** the table, run in the other direction to **build** it.

`Reproducibility Packet/scripts/derive_ccf_label_map.py`. **146.6 MB in 150 range requests, metadata only, no recording data read.** 32 of 37 donor insertions assigned a probe; 2,053 donor rows placed.

**138 entries emitted — 94 of them structures the hand-authored table did not contain.** 119 acronyms saw exactly one host name, 23 cleared a two-thirds majority, 2 were ambiguous and were not emitted.

### 2.3 The audit — the part I did not plan, and the part I got wrong first

Every emitted entry is compared against the hand-authored table. This is a check nobody had run and the existing validation *could not* give: that run could only test names the table already contained, so it could confirm the acronyms but never the long-name spellings.

**44 agree. 0 disagree.** Every hand-authored entry the derivation reached independently reproduced both name and acronym.

**That number depended on getting the comparison right, and my first version got it wrong.** Comparing raw strings reported 31 disagreements. **Thirty of them were punctuation** — the NWB export strips the commas the canonical names carry, and the lookup already resolves both spellings through its normaliser. An audit that does not use the same key its lookup uses is not auditing the lookup. Fixed; the one real finding survived as a collision below. Logged as a correction, because it was reasoning that would have published thirty false alarms about a table that was in fact correct.

### 2.4 Two entries thrown away rather than guessed at

A map keyed by long name can have two acronyms win the same name. My first version wrote them into a dictionary and **silently kept whichever came last** — the quiet-failure mode the software standard exists to prevent. Collisions are now refused outright and reported:

- `'Periaqueductal gray'` — claimed by `PAG` (50 votes, 4 insertions) and `IVn` (2 votes, 1 insertion). `IVn` is the trochlear nerve.
- `'posteromedial visual area layer 6a'` — claimed by `VISpm6a` (12 votes) and `VISpm5` (2 votes).

Both are boundary contamination and in both cases the majority claimant is obviously right. **Neither is emitted anyway**, because the rule is not "prefer the better-supported claim": this evidence establishes which claim is more common, not which is correct, and a rule that resolves these by vote count would resolve a genuinely ambiguous case with the same confidence.

### 2.5 The ceiling, published with the result

A host structure holding no donated waveform cannot be derived by this method. Of **209 distinct host long names** seen on the assigned probes, **143 are mapped and 66 remain unmapped**. Those 66 would need the ontology — so the licence question returns if the region-unaware arm's placement ever lands in one.

I also flagged a denominator trap for later sessions: **do not read the 66 against the 296 quoted in earlier work.** The 296 came from 46 screened recordings; the 209 come from the 32 donor-session probes. Different recording sets, different denominators.

### 2.6 How it is wired, and what was verified rather than asserted

The derived layer is **opt-in on every call**: `to_acronym(label)` keeps its original hand-authored-only behaviour, `to_acronym(label, include_derived=True)` consults the derived layer with hand-authored entries always winning, and a new `provenance(label)` reports which layer answered and at what tier. The default was chosen so no existing consumer changes meaning underneath itself — and **that was verified: re-running the existing validator after the module change reproduced its tracked report byte for byte.**

**One check I deliberately did not run.** Regenerating the validation report against the derived map would have agreed trivially — it would validate entries with the evidence they were derived from. The 44 agreements in §2.3 are the only non-circular confirmation claimed, because they test a table written before the data was consulted.

### 2.7 A structural finding on the way

**The donor library's acronyms sit at mixed levels of the atlas hierarchy.** `MB` (Midbrain) and `OLF` (Olfactory areas) are parent structures appearing alongside their own descendants `MRN` and `PIR`. That matters for the region-unaware arm and belongs in Codex's balance gate: **"same region" is not well defined when one label is a parent of the other.** CA1 is unaffected — it is a leaf and all sixteen donors are labelled `CA1` — so this is not a Tier A blocker, but any zone change should check for parent-labelled donors before assuming the region axis is clean there.

---

## Challenges, and how they were handled

**A repair that exposed a defect rather than closing one.** Codex's removal of my unproved monotonic claim is what made me look at what the objective points at. The lesson worth keeping: removing a bad reason for a rule is a good moment to re-derive whether the rule is right, because the bad reason was doing the work of hiding it.

**My own script was wrong twice, in opposite directions.** The audit was wrong pessimistically (30 false alarms) and the collision handling was wrong silently (last-write-wins). The pessimistic one announced itself; the silent one would not have. I found the silent one only because the false alarms made me read the output line by line. That is not a repeatable process, and it is the argument for the withholding rule I ended up with.

**Deciding not to file a director request.** The licence question looked director-shaped. It was not — reading the terms was mine to do, and only a *named exception* would have been his. Filing it before doing the reading would have handed him homework and stalled the item for days.

---

## Decisions I made

1. **Edit Amendment 3 rather than approve it**, on a defect rather than a preference. Everything else in it is Codex's text and I reopened none of it.
2. **Raise the evaluation-cap arithmetic without editing it.** It is not a defect and the cap is Codex's rule; surfacing the number now is worth more than a third round-trip over it.
3. **Do not import the Allen ontology, and do not request an exception.** Derive instead.
4. **Withhold colliding entries entirely** rather than resolve them by vote count.
5. **Make the derived layer opt-in**, so no existing consumer silently changes meaning, and prove it by byte-for-byte reproduction.
6. **Do not re-run the validation against the derived map**, because it would be circular and would look like confirmation.
7. **Add a `--from-records` replay path**, matching the pattern already in the packet, so future rule or presentation changes cost no network reads.

---

## Files created or updated

**Created**
- `Reproducibility Packet/scripts/derive_ccf_label_map.py`
- `Reproducibility Packet/results/ccf_label_map_derived.txt`
- `Reproducibility Packet/results/ccf_label_map_derived_records.json` (replay records)
- `Reproducibility Packet/scripts/utils/ccf_label_map_derived.json` (the derived map)
- `agents/Claude/Session Summaries/HumanReport9.md` (this file)

**Updated**
- `Claim Sheet.md` — Amendment 3 points 1 and 3, and its status line
- `Accessible Claim Sheet.md` — same, synchronized in the same session
- `Reproducibility Packet/scripts/utils/ccf_labels.py` — opt-in derived layer, `provenance()`
- `agents/Claude/Tier A Host and Injection Zone Selection.md` — new §12; §5.2 marked resolved
- `agents/Claude/references.md` — three new entries, plus correction row 9
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md` (rewritten)
- `README.md` — one running-log entry
- `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md`

---

## Machine state measured this session

**2026-08-12 14:08 PDT — RAM 16.26 GiB free of 31.67 (49% in use); VRAM 953 MiB used of 16,311.** Every step this session was metadata-only over HTTP range requests with no recording data loaded, so no heavy-step admission gate applied. Total network reads: 146.6 MB in 150 range requests for the derivation, plus a validator re-run of comparable size for the no-regression check.

---

## Next steps

1. **Codex's exact-state review of Amendment 3's search-space removal.** Tier A generation stays blocked until both agents approve the same bytes. If Codex approves, whoever writes that turn flips the status to `In force` in **both** sheets in the same session — and that flip triggers a progress report for its author.
2. **§12 of the Tier A artifact is unreviewed.** It is Draft 6 in substance; §1–§11 remain same-state approved.
3. **The 66 unmapped host names** are the residual. If a candidate zone's placement lands in one, the licence question returns and would then need a director request for a named exception.
4. **The hierarchy finding (§2.7)** is an input to Codex's balance gate, not a claim on it.
5. Still untouched and still mine to resolve before packet assembly: `audit_template_library.py` duplicates `utils/template_metadata.py`, and the packet still owes its own `requirements.txt`, `.gitignore` and runbook README.
