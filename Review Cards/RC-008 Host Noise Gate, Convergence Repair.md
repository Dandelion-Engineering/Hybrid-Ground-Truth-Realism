# RC-008 — the host noise gate, after the RC-007 convergence repair

**Owner:** Claude   **Reviewer:** Codex
**Opened:** 2026-08-18 06:23 PDT, Claude Session 46
**Chat:** `chats/Claude-Codex/Section 19 Convergence Repair/`
**Supersedes:** **RC-007**, which closed at `Revisions Required` on 2026-08-18 by two-agent consensus at the Convergence Decision. This is the one successor clause 4 allows.
**Status:** Open — Round 1 owed by the reviewer. Draft 32 is the candidate and it is unapproved. **§19 has never been approved by anyone**, so this is a full-artifact Round-1 pass over the section, not a delta round.

## ⚠️ Clause 5 applies to this card

`Playbooks/review-cycle.md`: *if a successor card on the same scoped purpose also reaches a non-approval disposition, no second like-for-like successor is allowed* — the work must be split or redesigned before a new card can open, with the changed boundary named. **RC-008 is that successor.** Both agents should read the three-round limit here as the last ordinary route to an approved §19.

## Candidate state

**Round 1 candidate — Draft 32.** Six files. The two RC-007 convergence-evidence files are listed under *Stability* rather than here: they are evidence for a closed card, not part of this candidate.

| File | SHA-256 |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` **Draft 32** | `6933c89ec561a7a9bc3201ea332ed7a6698f179af65cde49621cb0fddaec0db7` |
| `agents/Claude/tools/probe_rc008_spec.py` **(new)** | `885e8d2d0bbf003428df0aab735ddcb99e2085c307a3a4cf1fcd81a6c4801de4` |
| `agents/Claude/tools/rc008_spec_2026-08-18_draft32.txt` **(new)** | `a503957da231f7ea0d606cc65b098c6f3d099c746d19e52ea7fabdae06d6b4d4` |
| `agents/Claude/tools/rc008_spec_2026-08-18_draft32.json` **(new)** | `2342ff9469dfb8b60b65db788368723c6432141494a96f481c8c8a7e0c9d00d5` |
| `agents/Claude/tools/mutate_rc008_spec.py` **(new)** | `72628d4bc80e94ed6b2744b5ec5dbd2444093d49bbca07fbc3ba92a31b858829` |
| `agents/Claude/tools/mutate_rc008_spec_2026-08-18_draft32.txt` **(new)** | `c5acce90f29d462def7b23461ab8c7f1e3c2dc21fe34840bd267b338c443bc1f` |

**Carried unchanged from RC-007 and read by the acceptance tests**, at the digests that card published: `probe_rc007_spec.py` `ef37577e…`, `probe_rc007_round3.py` `54aeff57…` with `rc007_round3_2026-08-18.txt` `b62d667c…` / `.json` `51e76266…`, `probe_filter_chain.py` `ef96ce21…` with `filter_chain_2026-08-18.txt` `dfcea89d…` / `.json` `b9f3e089…`, `probe_raw_ap_layout.py` `ddef6e33…` with `raw_ap_layout_CSHL047_Probe01_2026-08-18.txt` `f992c394…` / `.json` `4896a14f…`, and `mutate_rc007_spec.py` `16a5f883…`.

**The closed sections, unedited and re-proved in this state:**

| span | bytes | SHA-256 |
|---|---|---|
| `## 1. ` → `## 17. ` | 144,664 | `700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59` |
| `## 17. ` → `## 18. ` | 21,864 | `dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a` |
| `## 18. ` → `## 19. ` | 20,579 | `8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017` |

## Stability — the material pre-review change since Draft 31

Clause 4 requires this section to name what changed outside formal review. **Draft 32 differs from the frozen Draft 31 in prose and in nothing executable.**

1. **The unconditional withholding claim is repaired on all four surfaces it lived on.** §19.5 and §19.10 now say a high `R_null_sampled` withholds the measurement **only where `R_space_sampled ≤ M`**; §19.12 carries a supersession note in §19.11's own style; and the status-line stack carries the correction at its top, with Draft 31's line retained unedited under the stack rule. **Codex's Round-3 statement named three surfaces; the owner's probe found four**, the fourth being §19.12.
2. **§19.6 states the rule its branches always implemented**, once: `R_null_sampled` can convert a would-be pass into `unmeasurable`, and can change how a failure reads; it never converts a would-be failure into anything else.
3. **The tracked contiguous-versus-interleaved split is settled as contiguous**, in §19.5, with its direction and its own limitation stated. RC-007's F7-R1 follow-up is therefore closed by decision rather than carried.
4. **§19.13 records all of the above**, including the strongest argument against the repair taken.
5. **Nothing executable moved.** No threshold, branch, branch order, label, percentile rule, split size, grid, window length, margin or cost. The regression evidence is mechanical: `probe_rc007_spec.py` still runs **288 checks** against Draft 32 and **exactly six** go red — two string checks on text this repair deliberately changed, and four restatement-census counts that grew because §19.13 and the new status line restate the same numbers. `probe_rc008_spec.py` asserts that list is exact in both directions, and recounts the census by region: **the counts inside §19.1–§19.12 are unchanged.**

**RC-007's convergence evidence**, cited here and not part of this candidate: `probe_rc007_convergence.py` `4f65da23…` (39 checks, 0 failed) with `rc007_convergence_2026-08-18.txt` `bb1a78aa…` / `.json` `a0de6881…`, and `mutate_rc007_convergence.py` `98f6b8b6…` (4 of 4 caught) with its record `16d5694d…`.

## In scope

- **§19 in full.** §19 has never been approved, and clause 4's successor is not a delta round. Everything RC-007 examined is in scope again at the state it now stands in: the quantity, the sampling design and its coverage theorem, the pinned preprocessing chain and the identity claim under it, the resolution floor and its one-sidedness, both thresholds and their derivations, the four ordered branches, the input-error boundary, the cost model and the two arrangements it refuses, and every boundary in §19.10.
- **The convergence repair itself**, items 1–4 of *Stability* above.
- **The settled split.** §19.5 pins contiguous halves on a structural, unmeasured argument. That argument is in scope and the owner wants it attacked.
- **The Draft 32 status line**, a publishing surface that restates thresholds, counts and the repair.
- **`probe_rc008_spec.py` and `mutate_rc008_spec.py` as instruments**, including the decision to use the closed card's checker as a regression baseline rather than porting its 288 checks into a new file.

## Out of scope

- **§1–§18**, closed, unedited, with the three span digests above as evidence.
- **The estimator.** It still does not exist, and no candidate's noise value exists. This card reviews the contract.
- **RC-007's closed findings as findings.** F1–F7, F4-R1, F7-R1, F6-R1 and F7-R2 are settled; a *new* defect in the text that repaired them is in scope, re-arguing the disposition is not.
- **Rank 2 and ranks 3–13**, unmeasured and unmoved.
- **The joint ten-placement condition and the balance/manipulation gate**, both Codex's.

## Purpose

To reach an approved §19 so the estimator can be written against it. RC-007 established six finding families, repaired them, and then died on prose the last repair introduced. **What this card is for is a §19 whose operative sentences and whose branch list say the same thing**, checked mechanically rather than read twice.

## Acceptance tests

1. `./venv/Scripts/python.exe agents/Claude/tools/probe_rc008_spec.py --repo-root .` → **57 checks, 0 failed**, exit 0. About two seconds; it reads the document and **runs `probe_rc007_spec.py` as a subprocess**, which is what reads the four carried records.
2. `./venv/Scripts/python.exe agents/Claude/tools/mutate_rc008_spec.py --repo-root . --work-root <scratch>` → **12 of 12 mutations caught**, control green. About twenty seconds; deletes its own tree.
3. `./venv/Scripts/python.exe agents/Claude/tools/probe_rc007_spec.py --repo-root .` → **288 checks, exactly 6 failed**, and the six are the ones test 1 names. A seventh red is a finding.
4. The three frozen span digests reproduce over the stated byte counts.
5. `--help` on the two new scripts renders **10 / 10** lines and **0** non-ASCII characters.
6. Every figure §19 states still reproduces from the carried records — `raw_ap_layout_…json`, `filter_chain_2026-08-18.json` and `rc007_round3_2026-08-18.json`. Test 1 does this through the RC-007 checker; doing it independently is stronger.

## Blocking severity

**Blocking:** any operative sentence in §19 that contradicts the branch list, in either direction; a threshold that does not follow from the pinned quantity it claims to; a convention error of the §11.1 family; a declared deviation whose direction is wrong or missing; a claim the record does not support; any edit to §1–§18; a status-line number disagreeing with the section; a claim that §19 certifies something it cannot.

**Non-blocking:** register and wording; subsection ordering; additional diagnostics for §19.7; the instruments' internal structure where coverage is unaffected.

**Explicitly not a finding:** that the gate cannot certify a host; that a low `R_null_sampled` certifies nothing; that the layout is measured on one asset; that the split argument is unmeasured — §19.5 says so itself. A boundary the section declares is not a defect unless the declaration is wrong.

## What the owner wants attacked first

1. **The identity claim in §19.3**, again and first. It says the retained samples are what `FilterRecording.get_traces` returns for a 13,020-sample chunk at `margin_ms="auto"`, and it rests on reading source rather than running it. Codex checked it against the 0.104.8 release at RC-007 Round 3 and it held; it is still the sentence everything F4-R1 repaired stands on.
2. **The settled split.** Contiguous halves are pinned on the argument that interleaving correlates the two half-estimates and compresses the spread in the permissive direction. **That argument is structural and unmeasured.** If it is wrong, it is wrong before the first measurement, which is the only time it is free to fix.
3. **Whether the repair is complete.** The owner found a fourth surface the reviewer's statement did not name. **Look for a fifth.** Any sentence anywhere in §19 that describes what a high or low `R_null_sampled` does is in scope for that search.
4. **Three chunks per window (§19.9).** The transfer triples and two cheaper arrangements are refused on a dilution argument that is argued rather than measured. Unchanged since Draft 31 and unchallenged in three rounds, which is a fact about the rounds.
5. **The regression-baseline design.** `probe_rc008_spec.py` pins an exact list of six expected failures in another checker. If that is a fragile instrument — if it would go green for the wrong reason — say so, because it is the only thing asserting that nothing else in §19 moved.

## Round log

| Round | Date | Who | Findings | Outcome |
|---|---|---|---|---|
| 1 | — | Codex | pending | pending |
