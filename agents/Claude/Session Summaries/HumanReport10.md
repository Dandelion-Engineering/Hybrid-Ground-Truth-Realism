# Human Report 10 — Claude

**Session date and time:** 2026-08-12 16:31 PDT (session began 16:05 PDT)
**Phase:** Phase 2 — Execution
**Progress report due?** Yes, and written — Amendment 3 reached `In force` in this session. `agents/Claude/Progress Reports/Progress Report Amendment Negative Control Pools.md`.

---

## What this session did

Four things, in this order:

1. **Closed Amendment 3.** Re-reviewed Codex's two Session 9 changes at the exact bytes, verified each rather than reading it, and put the amendment into force in both Claim Sheets. Tier A's negative-control construction is now agreed after four rounds of review.
2. **Found that the argument behind Codex's last repair applied to the real experiment**, in a place neither of us had asked about — and measured it instead of arguing it. Under the pairing rule the project was most likely to write, **half the region-blind control arm would have been made of injection-zone donors.**
3. **Proposed Amendment 5** in both sheets, which removes the injection zone's donor pool from the real control arm and constrains when the matching rule may be fixed.
4. **Cleared the largest open engineering item that was mine** — `audit_template_library.py` was carrying private copies of five things that live in `utils/template_metadata.py` — and proved the refactor correct by reproducing the tracked report byte for byte from a live fetch.

No host is pinned. No sorter, generator or Rung 0 run occurred. Nothing beyond bounded metadata reads was downloaded, and this session's only network request was the 2 MB template CSV used to prove the refactor.

---

## 1. Amendment 3, verified and put into force

Codex's Session 9 review made two changes and handed back approved bytes. I re-derived both.

**The shared pseudo-base pool.** In Session 9 I had removed the injection zone's donor pool from the first pseudo-arm's search space only, and I had written in the amendment that the second pseudo-arm should still be able to draw zone templates "by chance exactly as the real region-unaware arm can" — treating that as fidelity. Codex found the flaw: P2 is covariate-matched to P1, and P1 is selected to resemble the CA1 sixteen, so the templates that match P1 best include the ones P1 was built to imitate. The draw is not chance; it is enrichment. That left P1 at zero CA1 by construction and P2 enriched — a region difference *between the two halves of a control*, pointing the opposite way to the real manipulation. The correction is right and I accepted it unchanged.

**The 64-sweep cap.** This came out of an observation I raised in Session 9 and deliberately did not act on. One complete best-improvement sweep costs 16 × (M − 16) evaluations, so a 100,000-evaluation ceiling bought two improving swaps at a pool of 2,167 and dozens at a pool of 200 — making "achieved per-covariate distance" mean different things at different pool sizes. Codex replaced it with a fixed 64 complete sweeps for every pool. I re-derived the arithmetic (34,416 per sweep at 2,167 candidates; 2.20 million over 64 sweeps, matching Codex's figure) and confirmed the search cannot cycle, since every accepted swap strictly lowers the objective.

**One probe I ran and withdrew.** I went after the amendment's sentence "no no-manipulation control can [mirror region homogeneity]" as a possible over-strong universal — a control drawing sixteen templates from one *non-host* region would be homogeneous without being region-matched. It fails under the contract's own definitions: Slot 5 defines the control as drawing *without conditioning on region*, so a control that conditions on any region is applying the manipulation at a different target rather than withholding it. The sentence holds. I recorded the probe in the chat so it is not re-run in a later session.

**Amendment 3 is `In force` in both sheets, dated 2026-08-12**, with the full four-round history preserved in the status line. Amendment 2's prohibition on Tier A generation under a changed band is discharged. Two gates remain before any generation: the exact selector-configuration and selected-ID approval, and the manipulation check.

---

## 2. The measurement, and how I got to it

Codex's reason for the P2 removal is a general claim: *a matcher aimed at a zone-like target preferentially selects the zone's own donors.* That claim is about the real contrast too, and there it is stronger, because the real control arm is matched to the sixteen CA1 donors **themselves** rather than to a lookalike. Slot 5's "without conditioning on region" is region-**blind**, not zone-free — the sixteen are eligible to be their own controls — and nothing in the contract decided what happens when the matcher reaches for them.

The rule that would have decided it by default is the donor-matching rule, which is Codex's and is not yet written. So the question would have been answered silently, by whatever that rule turned out to be, at a point where the pool was already visible.

I measured the pull rather than asserting it. New script `Reproducibility Packet/scripts/audit_zone_neighbour_enrichment.py` → `Reproducibility Packet/results/zone_neighbour_enrichment_CA1.txt`. Stdlib only, run against the tracked snapshot, **no network reads**.

| matcher over all 2,183 NP1.0 templates | CA1 partners | expected region-blind |
|---|---|---|
| nearest unused partner, no blocking | **3 of 16** | 0.11 |
| nearest unused partner, exact-insertion blocking | **8 of 16** | 0.98 |

The nearest covariate neighbour of a CA1 template is another CA1 template for 3 of the 16, against a 0.687% base rate per non-self draw. Under the provisional 50–200 µV / SNR 5–15 caliper the two matchers give 2 of 12 and 5 of 12 against 0.11 and 1.11.

**The blocked row is the consequential one.** Exact-insertion blocking is not an exotic variant — Amendment 2 makes it the *first* granularity the balance procedure must attempt, before falling back to session and subject, because it is the cleanest way to stop donor provenance riding along with region. Under it, half the region-blind arm sits inside the injection zone.

The expectation column for that row is computed under the same blocking rather than against a pool-wide rate, which matters: CA1's share of the four CA1-bearing insertions is 6.2%, 25.0%, 6.8% and 4.9%, and six of the eight hits come from the KS051 insertion, which holds six of the sixteen among 88 rows. So the 8 of 16 is not an artifact of CA1 dominating those insertions.

**Three boundaries, written into the script's own report, the amendment, and §13 of my Tier A artifact.** The covariates are the donor table's own columns — pre-host analogues of the post-rescaling amplitude, effective host SNR and depth-along-band the real matching will use, none of which exist until a host is pinned. The matcher is a plain greedy nearest-neighbour, chosen because there is no rule yet, which is the point; it is not a proposal and not a guess at Codex's rule. And n = 16, so the counts are coarse. **It measures the size of a pull, not the composition of an arm.**

**One error I caught in my own draft of that report.** I first wrote that blocking makes the pull stronger "by more than" the unblocked case exceeds its expectation. That is false: the *ratio* to expectation falls (27× to 8×) while the *realized* count rises (3 to 8). The realized count is what dilutes the manipulation, so the sentence now says exactly that and no more. Same error class as the two I have corrected in previous sessions — a direction stated because it was plausible — caught this time before it left the script.

---

## 3. Amendment 5, proposed

Written into both sheets as `Proposed`, carrying no force.

**The proposal.** Remove the injection zone's donor pool from the real region-unaware arm's eligible pool, exactly as Amendment 3 removes it from the shared pseudo-base pool. Report what the removal costs. Fix the matching rule before the eligible pool is visible, with no term referencing region membership in either direction. Report the realized zone-donor count per arm as a manipulation-check quantity.

**The argument I expected to lose and did not.** The obvious objection is fidelity: the anchor pipeline draws region-blind, so a control that excludes the host's region is more mismatched than the field's actual practice — and this project has twice refused constructions that lean the other way. It does not survive the arithmetic. **The anchor pipeline does not covariate-match its templates to a region-matched set, because it has no region-matched set.** Ours does, because pairing is how Slot 4 buys precision from one desktop instead of from N. The pull toward the zone is manufactured by *our* pairing, not inherited from the method under test. What a genuinely region-blind draw would have contained is computable: 16 draws from 2,183 with 16 zone members expects **0.12**, about one arm in nine holding a single one. That is the cost of the removal; the table above is the cost of leaving it in.

**The second reason, which decides the timing.** Once the pool is visible, "admit zone donors" and "exclude them" are both defensible, and the choice could be made — even honestly — with the realized arms in view. That is the forking path Amendment 3 closed for the pseudo selector. The amendment's status line therefore says the matching rule may not be fixed or approved while Amendment 5 is open, because writing the rule first answers the question by omission.

**What I did not do.** I did not write Codex's matching rule, and I said so explicitly in both the amendment and the chat: the amendment constrains *when* the rule is fixed and *what it may not mention*. I also offered to take a different resolution — a declared ceiling on zone donors, or leaving them in and reporting the realized count — since what I am defending is that it is decided before the pool is visible, not that it is decided my way.

**One boundary carried forward from Session 9's §12.7.** "The injection zone's donor pool" is well defined for CA1 because CA1 is a leaf of the atlas hierarchy and all sixteen donors carry exactly that label. The donor library's acronyms sit at mixed levels — `MB` and `OLF` appear alongside their descendants `MRN` and `PIR` — so for any zone whose label has an ancestor or descendant in the library, the removal set must be defined and recorded before the rule is applied. A string match on the acronym is not that definition.

---

## 4. The duplication, cleared and proved

`audit_template_library.py` (Session 2) predated `utils/template_metadata.py` (Session 5) and carried its own `fetch_csv`, `parse_rows`, `as_float`, `in_caliper` and pinned snapshot hash. This was recorded in my own README as a known defect and was the largest open engineering item that was mine.

- The module gained `fetch_metadata_with_headers`, because the audit is the only caller that needs the server's `ETag` and `Last-Modified`. `fetch_metadata` now delegates to it, so the three existing callers keep their two-tuple contract byte for byte unchanged — verified by calling both.
- The audit script imports all five and gained `--cache`, so its group-bys can be re-run offline against the tracked snapshot. 241 lines to 180.
- **Proof it still works: the refactored script, run live, reproduced `Reproducibility Packet/results/template_audit_2026-08-11.txt` byte for byte.** That also re-confirms the upstream S3 object has not moved since 2026-08-11. Offline, the only difference is the two header lines a cached read cannot carry, which the docstring says explicitly.

---

## 5. Cross-review of Codex's Session 9

Read its human report and both code edits to my label-map work.

- **The ten white-matter acronyms it added to `NON_INJECTABLE_ACRONYMS` are correct and complete for the current derived map.** I listed all 138 derived entries against the set: `ec`, `ee`, `fp`, `int`, `opt`, `rust`, `SCdw`, `SCiw`, `scp`, `scwm` are exactly the fibre-tract and white-layer entries and no other derived entry is one. `rust` is the rubrospinal tract, `ee` the extreme capsule; both are real CCF acronyms and both are correctly non-injectable.
- **The `--from-records` guard works and the replay still reproduces.** Replaying against the tracked records is byte-identical in both the report and the map, after Codex's change and after mine.
- **One structural note I raised and did not act on.** `is_injectable` is a denylist over a vocabulary that is now partly derived, so a re-derivation reaching a new fibre tract would default it to injectable. No consumer reads it yet, so the hazard is latent rather than live. I declined to convert it to an allowlist, because doing so would amount to claiming that 84 derived gray-matter acronyms had been reviewed as injectable when they have not. It is recorded as an open item instead.

---

## Files created or changed

| Path | What changed |
|---|---|
| `Claim Sheet.md` | Amendment 3 → `In force` with the Session 10 verification recorded; **Amendment 5 appended as `Proposed`**. SHA-256 `05b360de37ea28d7b499d4c48067e0b4f40e117d35b6672aaf828f4206af25ca` |
| `Accessible Claim Sheet.md` | Same two changes in plain language, same session. SHA-256 `4aa484d25b9b61282cc9a96387a0171d19d2c34e5b75fe02ddd32f00ba0170f4` |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 6** — new §13 (the enrichment measurement and what was done with it); status line records that §12 was never handed off as an approved state and that this draft is that handoff. SHA-256 `0ab8fe7c54ac30972a1e81f4d5b5aa00d1769b55e598f138a33503a54c3442fb` |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Session 10 turn appended (append verified by reading back) |
| `agents/Claude/Progress Reports/Progress Report Amendment Negative Control Pools.md` | **New** — amendment-triggered progress report |
| `agents/Claude/Session Summaries/HumanReport10.md` | **New** — this file |
| `agents/Claude/README.md` | Tree, Tier A description, contract state, chat state, and the two script rows updated |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten |
| `README.md` (Live-Run) | One running-log entry |
| `Reproducibility Packet/scripts/audit_zone_neighbour_enrichment.py` | **New** — the enrichment measurement |
| `Reproducibility Packet/results/zone_neighbour_enrichment_CA1.txt` | **New** — its tracked report |
| `Reproducibility Packet/scripts/audit_template_library.py` | Refactored onto shared utils; `--cache` added; 241 → 180 lines |
| `Reproducibility Packet/scripts/utils/template_metadata.py` | `fetch_metadata_with_headers` added; `fetch_metadata` delegates |

---

## Machine state

Measured at 16:12 PDT, immediately before any work: **RAM 14.28 GiB free of 31.67 (54% in use); VRAM 1,024 MiB used of 16,311.** Nothing this session was heavy — the largest single operation was a 2 MB CSV download and a few group-bys — so no admission gate was exercised. The next session must take its own reading and must not inherit this one.

---

## What is next

1. **Codex reviews Amendment 5's exact bytes**, and reviews Draft 6's §12–§13. The matching rule is blocked until Amendment 5 resolves, by the amendment's own terms.
2. **Host selection continues.** Gates still open: drift, noise, post-rescaling effective SNR, Codex's covariate-balance gate, and the two-part footprint/placement calibration Codex owns.
3. **The packet still owes its own `requirements.txt`, `.gitignore` and runbook README**, and the self-containment test is copying that folder alone to a clean machine.
4. **`is_injectable`'s denylist-over-a-derived-vocabulary hazard** is recorded and unaddressed.
5. **Nothing is blocked on the director.** `director_requests.md` has no open entry from me.
