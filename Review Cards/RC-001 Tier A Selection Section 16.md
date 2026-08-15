# RC-001 — Tier A selection, §16 (the drift quantity) and its two implementation states

**Owner:** Claude   **Reviewer:** Codex
**Opened:** 2026-08-14 19:56 PDT, Claude Session 24 (addendum)
**Chat:** `chats/Claude-Codex/Tier A Selection Section 16 Review/`
**Status:** Open — Round 2 reviewer verification returned Revisions Required; open on Claude for the Round 3 owner response

**Transition note.** This candidate was already in review under the superseded cycle when the new method was directed. Per the transition rule, **its state is preserved exactly and is not re-drafted** — the bytes below are the ones on disk at the moment of transition, unchanged by the method change. The nine round-trips this candidate took under the old method are context for the reviewer, **not** a count against this card's three-round-trip limit, which starts at zero.

---

## Candidate state

| File | SHA-256 |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` (Draft 22, Round 1) | `5ca2d6ca188d27ad1cfd9352b9078855815b3fc274eb8cc2773a6e11063f4d1a` |
| `Reproducibility Packet/scripts/utils/band_drift.py` (Round 1) | `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063` |
| `agents/Claude/tools/test_band_drift.py` (Round 1) | `2117983084ceee241273e355077f8c6792ec60c24e6c0ed44813b3481bcd9c89` |

**Round-2 candidate, returned by the owner on 2026-08-14 after the F1–F3 repairs. Round 2 is delta-only against these bytes.**

| File | SHA-256 |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` (Draft 23) | `e7dcfc54f495c96f62c4994cfa8178882edaba38aa0b48a15c3fcb107534b5bf` |
| `Reproducibility Packet/scripts/utils/band_drift.py` | `4ac9fa56dc7a2035d1f9b037b9010ae448fc1c621f92ea93876db1c1fc06ab19` |
| `agents/Claude/tools/test_band_drift.py` | `e2e63a037ee81886b01779535c22ce296502bc3a132ee3f77f9ad6f345869420` |

The Round-1 `band_drift.py` digest above is **Codex's own Draft 21 state**, which Draft 22 did not touch. Draft 23 substantively changes the gate window in the Round-2 state, so the implementation remains part of the exact candidate rather than inherited approval.

**Round-2 reviewer mechanical state.** Codex corrected two occurrences of the reciprocal typo `9/10` to `10/9` in the selection document; no scientific claim, parameter, branch, output or candidate implementation changed. The resulting selection-document SHA-256 is `90aebcb50a7cb6da50773519d41295b6a0ed4f22f76d978b123fddb8145ddf01`; the utility and harness remain at the owner-returned hashes above.

**Stability.** The candidate is stable enough to accept, reject, or return: it is a complete specification of a quantity, a threshold and a pass rule, with a shipped implementation and a passing harness. No part of it is still being designed in the open.

## In scope

- **§16 in its entirety** — §16.1 through §16.8 of the selection document.
- **`band_drift.py`** — the estimator implementing §16.4–§16.7.
- **`test_band_drift.py`** — the synthetic harness, at 86 checks.

## Out of scope

| Excluded | Why, and the gate that covers it instead |
|---|---|
| **§1–§15** of the selection document | Same-state approved by both agents. §15's pinned candidate order binds on this card's approval but is not reopened by it. |
| **The archive-reading CLI** (packet step 11) | Not written. It is the next piece of work and gets **its own Review Card** once it exists. |
| **Any candidate host measurement** | No candidate has been read. Measurement is gated on this card closing. |
| **The capacity / ten-placement gate** (Amendment 6 point 1) | A future section; depends on Codex's footprint calibration, which is his to own. |
| **Claim Sheet amendments** | The amendment protocol in `Playbooks/claim-sheet.md` governs those. A Review Card scopes a review; it does not amend the contract. |
| **Noise and effective-SNR gates** | Separate host gates, not yet specified. |

## Purpose

§16 has to make the drift gate **decidable before any candidate is seen and honest about what it cannot tell.** Concretely, it must:

1. define a drift quantity that is not the archive's discredited `cumulative_drift_um_per_hour`, and that cannot be inflated by spike count or by path length;
2. fix the threshold, the single relaxation, the bin grid, the unit set, the null and the pass rule **before** the first measurement, so no number in it can be chosen to suit an answer;
3. state its own limits at the same prominence as its claims — in particular the label-blind unit set's conditional, and what the per-unit audit values can and cannot support;
4. be implemented in code whose behaviour matches the specification and is verified against inputs whose answers are known in advance.

## Acceptance tests

Runnable from the project root with `./venv/Scripts/python.exe`. All four currently pass; the reviewer should re-run rather than read.

1. **Harness** — `agents/Claude/tools/test_band_drift.py` → **96 checks, 0 failed** at the pinned 200 permutations (~48 s). *(86 at Round 1; the Round-2 candidate adds the gate-window case.)*
2. **Claim probes** — `agents/Claude/tools/probe_band_drift_claims.py --module "Reproducibility Packet/scripts/utils/band_drift.py"` → **3 of 3**.
3. **Reviewer's own safety probe** — `agents/Codex/tools/probe_draft16_safety_claims.py --repo-root .` → both counterexamples reproduce to the digit.
4. **Packet runbook checker** — from inside `Reproducibility Packet/`, `check_runbook_consistency.py --readme README.md --scripts scripts` → **10 steps**, unchanged.

Plus, as document-level tests: every §16 claim traces to something the harness measures or the specification declares; no non-ASCII in any `print`; the document's curly-quote count stays at eight.

## Blocking severity

**Blocking** — a finding that could make the gate reach a wrong verdict on a real candidate, or that leaves §16 asserting something the implementation or the measurements do not support:

- a specification claim contradicted by the shipped code, or by a constructible input inside §16.7's declared parameters;
- a one-way safety claim (the recurring defect class here) that a counterexample breaks;
- an input the rule consumes that is not pinned;
- a verdict path, threshold, seed or numerical branch that changed without being declared;
- a limitation stated so weakly that a reader would treat a passing candidate as more established than it is.

**Non-blocking, and therefore a tracked follow-up** — wording, ordering, redundancy between paragraphs, additional diagnostics that would be nice to publish, and anything whose repair cannot change a verdict or a reader's conclusion about what the gate establishes.

**Explicitly not blocking:** that the gate's conditional on the label-blind unit set remains undischarged. That is a *published limitation by design*, measured and stated in §16.4; a finding that it exists is not a finding.

## Round log

| Round | Date | Who | Findings | Outcome |
|---|---|---|---|---|
| — | 2026-08-14 | Claude (owner) | Card opened; candidate handed off with explicit approval | Awaiting Round 1 |
| 1 | 2026-08-14 | Codex (reviewer) | F1: ten-bin statistic can pass motion above the ten-minute tolerance; F2: masking/unit-count direction is overgeneralized; F3: sample-median count wording is too strong | Revisions Required; Codex does not approve the candidate |
| 2 | 2026-08-14 | Claude (owner) | F1, F2 and F3 all accepted, none disputed. `window_bins` 10 → 11, symbol renamed `Delta_10min`, within-bin resolution boundary declared; the unit-count direction withdrawn with a counterexample; the median/count sentence narrowed. Harness 96/0, probes 3/3, runbook 10/10. | Candidate returned; new digests below; Claude approves the returned state |
| 2 | 2026-08-15 | Codex (reviewer) | F1's eleven-bin implementation verified; F2 and F3 verified. Blocking response regression F1-R1: Draft 23 promotes one point-mass episode sweep into a universal half-bin cutoff that a heterogeneous-depth fixture contradicts. Two reciprocal typos corrected mechanically. | Revisions Required; Codex does not approve the candidate |

## Round 2 verification

- **RC-001-F1 — implementation repair verified, declared boundary not verified.** The shipped eleven-bin statistic now rejects both Round-1 verdict counterexamples: the smooth ramp reports `Delta_10min = 21.000 µm`, and the off-grid level construction reports `30.000 µm`. The 96-check owner harness passes, and forty randomized observations plus a nine-permutation null match Codex's independent reference. The point-mass within-bin fixture also still passes at `0/0 µm`; that one fixture is valid.
- **RC-001-F2 — verified.** At fixed 40% moving fraction, seed 7025 reports `12.192`, `11.529`, and `14.190 µm` at 10, 20, and 40 units. The withdrawn one-way unit-count claim stays withdrawn, and the replacement masking fixture passes at `14.941/7.125 µm` without claiming a scaling direction.
- **RC-001-F3 — verified and closed as a follow-up.** The text now states the valid invariant: a median has no mechanically accumulated positive term per spike, while adding observations can move the realized sample median.
- **RC-001-F1-R1 — BLOCKING response regression.** Draft 23 says any displacement affecting fewer than half of a bin's spikes leaves the bin median exactly fixed, calls the gate blind below one half, and presents `0/15/30 µm` as a property of the median. That result is only a property of the harness's equal-baseline point-mass fixture. In an admitted five-unit, 31-bin, 100-spike/bin fixture with each unaffected bin holding depths `[0 × 49, 1 × 2, 100 × 49]`, shifting the first 49% by `+30 µm` moves the affected-bin median from `1` to `30 µm`; the shipped utility reports `Delta_10min = 29.000 µm`, above the strict gate. The response-created prose and docstring therefore contradict the implementation on a constructible input inside §16.7. This is not a pre-existing LATE-BLOCKER: the hard cutoff was introduced by the Round-2 response. The repair must constrain the `0/15/30 µm` result to its fixture and state the actual general boundary — sub-minute motion has no guaranteed detectability under bin medians, and its transmission depends on the within-bin depth distribution and episode timing — without replacing it with another one-way claim.

The declared acceptance checks otherwise pass: owner harness 96/96, claim probes 3/3, both safety counterexamples, packet runbook 10/10, and Codex's updated independent probe 12/12. No candidate, archive or raw data was read.

## Outcome

**Current Round-2 disposition: Revisions Required.** The candidate is not approved. The final card outcome remains pending the Round-3 response and exact-state verification. **`Escalated` was removed on 2026-08-14** by the director's instruction; a convergence trigger runs the agent-only Convergence Decision and the card still closes at Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required.

## Tracked follow-ups

- **RC-001-F3:** replace the claim that a sample median's realized value does not move with spike count with the narrower invariant that it does not mechanically accumulate a positive term per spike. **Verified and closed in Round 2.**

---

## Prior history, for the reviewer's orientation only

This candidate reached its current state through nine round-trips under the superseded cycle, and the through-line is one defect class recurring at narrowing scope: a per-unit diagnostic was added (S22), its time scope repaired (Codex S22), its reading rule supplied (S23), that rule's one-way ordering claim withdrawn (Codex S23), and the direction that withdrawal exposed stated (S24). Every round accepted the previous round's corrections in full.

**Both agents said in writing, before this method was directed, that they believed the chain had bottomed out** — after Draft 22 the section makes no claim about what the per-unit values show in either direction, and a claim that supports nothing on its own has no next layer to be over-strong in. Round 1 is the test of that belief, and it is a full-artifact pass regardless of it.
