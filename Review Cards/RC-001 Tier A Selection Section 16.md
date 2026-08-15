# RC-001 — Tier A selection, §16 (the drift quantity) and its two implementation states

**Owner:** Claude   **Reviewer:** Codex
**Opened:** 2026-08-14 19:56 PDT, Claude Session 24 (addendum)
**Chat:** `chats/Claude-Codex/Tier A Selection Section 16 Review/`
**Status:** Open — awaiting Round 1

**Transition note.** This candidate was already in review under the superseded cycle when the new method was directed. Per the transition rule, **its state is preserved exactly and is not re-drafted** — the bytes below are the ones on disk at the moment of transition, unchanged by the method change. The nine round-trips this candidate took under the old method are context for the reviewer, **not** a count against this card's three-round-trip limit, which starts at zero.

---

## Candidate state

| File | SHA-256 |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` (Draft 22) | `5ca2d6ca188d27ad1cfd9352b9078855815b3fc274eb8cc2773a6e11063f4d1a` |
| `Reproducibility Packet/scripts/utils/band_drift.py` | `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063` |
| `agents/Claude/tools/test_band_drift.py` | `2117983084ceee241273e355077f8c6792ec60c24e6c0ed44813b3481bcd9c89` |

`band_drift.py` at this digest is **Codex's own Draft 21 bytes**, which Draft 22 does not touch. It is named in the candidate because it is what §16 specifies and cannot be approved apart from it, not because it changed.

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

1. **Harness** — `agents/Claude/tools/test_band_drift.py` → **86 checks, 0 failed** at the pinned 200 permutations (~48 s).
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

## Outcome

*Pending.* One of: Approved · Approved with Follow-ups · Revisions Required · Split/Redesign Required · Escalated.

## Tracked follow-ups

*None yet.*

---

## Prior history, for the reviewer's orientation only

This candidate reached its current state through nine round-trips under the superseded cycle, and the through-line is one defect class recurring at narrowing scope: a per-unit diagnostic was added (S22), its time scope repaired (Codex S22), its reading rule supplied (S23), that rule's one-way ordering claim withdrawn (Codex S23), and the direction that withdrawal exposed stated (S24). Every round accepted the previous round's corrections in full.

**Both agents said in writing, before this method was directed, that they believed the chain had bottomed out** — after Draft 22 the section makes no claim about what the per-unit values show in either direction, and a claim that supports nothing on its own has no next layer to be over-strong in. Round 1 is the test of that belief, and it is a full-artifact pass regardless of it.
