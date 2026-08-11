# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 4 · 2026-08-11 16:15 PDT**
**Next session will be Claude Session 5.**

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work.** It is the contract and it is now agreed by both agents. This file is the *state*; the sheet is the *commitments*. `Accessible Claim Sheet.md` is the same content in plain language and is faster to re-load if you need the shape rather than the exact wording — but the technical sheet governs.

---

## 1. Where the project is

**Phase 1 — Sharpening, one step from closing.**

| Requirement | Status |
|---|---|
| Both agents approve the **same state** of `Claim Sheet.md` | **DONE (Session 4).** SHA-256 `a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3`. Loop closed, no disagreement survived. |
| The **Accessible Claim Sheet** exists and is agreed | **Written (Session 4), in review.** Awaiting Codex. |
| The **division of labor** is agreed | **DONE (Session 3).** |
| Study Guide Pass 1 agreed (also due at Phase 1 close) | **In review, handed back to Codex (Session 4)** with two of my edits on top of its approved state. |

**Phase 1 closes when Codex approves the Accessible Claim Sheet and the Study Guide pair.** The agent whose session closes it writes the **phase-transition progress report** and logs the *Claim Sheet ready for director review* entry in `director_requests.md`. If that is you, both are required — the progress report is in addition to normal session work, at the Accessible-Piece bar, per `Playbooks/research-progress-report.md`.

**Note on your own progress-report counter:** Session 8 is your next count-based trigger. A phase transition triggers one regardless and does not reset the count.

## 2. The first thing to do next session

**Check both chats in `chats/Claude-Codex/` for Codex's responses.**

- **`Claim Sheet Review/`** — it holds the Accessible Claim Sheet handoff. If Codex edited the Accessible sheet, genuinely re-review per `Playbooks/review-cycle.md` — do not wave edits through. The failure mode to hunt for in your own document is **a bound that got softer in translation**, not an awkward sentence.
- **`Study Guide Pass 1 Review/`** — same discipline. If Codex disagrees that the refractory-period paragraph earns its lines, **take it out rather than argue**; I offered that explicitly in the handoff and the point is not worth a third round-trip.

**If both come back approved, Phase 1 closes in your session.** Do the closing work (progress report + director request) before starting Phase 2 work.

**Then start your Phase 2 job: Tier A host and injection-zone selection.** See §6.

## 3. What I did in Session 4

| File | What changed |
|---|---|
| `Claim Sheet.md` | **Re-reviewed and explicitly approved** at `a5f5860…`. No edits — Codex's two coherence fixes were correct and I found nothing to add. |
| `Accessible Claim Sheet.md` | **New.** All fifteen slots in plain language, every number with its caveat attached. Handed off; SHA-256 at handoff `73bff8f81dc2e31b47d4abbe1f61c8106a34dccb8ea6457051c3dba84a589760`. |
| `Study Guide/…Pass 1….tex` + `.pdf` | Two edits (see §5). Rebuilt: 13 pages, zero overfull/underfull, changed and final pages visually inspected. Handed back at source `d33e74d7…` / PDF `75e14232…`. |
| `agents/Claude/references.md` | SHYBRID entry **superseded** with the source-verified narrower statement; `[VERIFY]` partly closed and retired; Session 4 row in the corrections log. |
| `director_requests.md` | Fourth memory measurement appended under the existing entry. |
| root `README.md`, `agents/Claude/README.md` | Banner, one lean log entry, ownership table. |

## 4. The one finding worth carrying forward: review catches errors, not absences

The Study Guide had been written by me and reviewed page-by-page by Codex against primary sources. Across both reviews, **nine corrections were made and every single one was to a sentence that existed.** Neither agent caught the one real problem, which was that a sentence was *missing* — the guide taught injected spike timing as memoryless and never mentioned that the pipeline already enforces a refractory period, leaving the contract's "refractoriness is part of the control, not an axis" line unexplained and unverifiable by the reader.

**Carry this into Phase 3.** When the artifact under review is the Technical Report, the absent sentence is a limitation nobody wrote down, and the same asymmetry applies. Reviewing against a *checklist of what must be present* catches this; reviewing by reading catches errors but not gaps.

## 5. My two Session 4 Study Guide edits, so you can defend or withdraw them

1. **A forward reference pointed at §3.3 (the manipulation check) when the argument is in §3.2.** Not contestable, just wrong.
2. **Added the refractory period to §3.1**, with the SpikeInterface generation-docs link, and stated why it belongs to the control arm rather than to a realism axis. This is the contestable one. If Codex pushes back, remove it — do not defend it into a third round.

The addition first pushed the build to 14 pages with §5.5 orphaned; I compressed my own paragraph rather than enlarging the page. **If you edit this document again, check the page count and render the last page** — this failure has now happened to both agents.

## 6. Your Phase 2 job, in the state I left it

**Tier A host and injection-zone selection**, mine under the labor split. It needs only the ~2 MB metadata file and no heavy compute, so machine contention does not block it.

**Run it against both constraints at once**, which is the thing Session 3 established and the reason it is not two separate searches:

- **Tier A needs** a zone whose donor pool survives excluding the *exact* host's source dataset — not the worst-case shortlist, the actual host-specific query, which **nobody has run yet.**
- **Tier C needs** a zone whose burst bounds rest on primary evidence, and the current evidence is CA1 (Harris et al. 2001).

**CA1 is the only zone satisfying both on its face**: 12 in-caliper NP1.0 templates across 4 source datasets before host-specific exclusion. **It is a candidate, not a decision** — its worst-case leave-largest count is 6, under the ten-unit budget, so viability turns entirely on which source dataset the chosen host belongs to.

The failure mode this ordering forecloses is cheap to fall into: satisfy Tier A, then discover Tier C cannot use the host Tier A picked, leaving Tier C as a labelled synthetic stress test rather than a biological-realism test.

**You are the wrong agent to grade this.** Codex owns Tier A's balance/manipulation gate precisely so the agent proposing the selection is not the agent approving it. Propose; do not grade.

Also remember: **a Neuropixels penetration crosses anatomy.** The deliverable is a pinned channel/trajectory mapping plus a declared injection zone at a target depth — never a whole-recording region label. If ten feasible placements cannot be supported, the host fails the Tier A gate.

## 7. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate**
- **Tiers B and C:** assigned after Rung 0. For each, the manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 8. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates (configuration/selection only) → Tier B population-rate coupling driven by a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation. Combined arm only after component effects are known.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units. Standardized effect sizes are secondary and never thresholds.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)` is the authoritative and only comparative rule.** The `[−T, T]` phrasing is declared shorthand for it, never a second test. Declared consequence: `|I|` is folded at zero, so **bounded-negative is the harder verdict** — conservative in the right direction, but it costs us the outcome we think is likelier.
- **The manipulation check is a hard stop-or-go gate.** If the injected data does not demonstrably carry the property at realistic magnitude, **no sorter run starts.**
- **One host and injection zone across all tiers by default.** Deviation = recorded limitation and the cross-tier comparison is dropped rather than made across hosts.
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 CPU internal sorter (SpyKING CIRCUS 2, TriDesClous 2, or Lupin — MIT via SpikeInterface). Kilosort-only is biased toward the null.
- **Equal block counts give equal *nominal replication basis*, not equal precision.** Both achieved interval widths get reported. (Codex's Session 3 fix to my Session 3 claim.)
- **The 48-sorter-hour ceiling stayed at 48 when the tranche doubled to 200 recording-minutes**, and Codex's reason is the one to reuse: discovering an underestimate is not an argument for approving twice the budget.
- **Errors of mine already corrected and accepted — do not re-argue them:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV rescaling target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim. **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Numbers you should not re-derive

**Template audit (Session 2, corrected by Codex).** Under provisional screens amplitude 50–200 µV and SNR 5–15: 1,149 of 2,183 NP1.0 templates survive across 149 areas; **37 areas hold ≥10**. After dropping each area's largest contributing dataset — the **worst case**, not the binding number — **7 survive:** CP (42), PIR (19), SUB (18), VISa5 (17), AId5 (14), MRN (14), ENTl5 (10). CA1 is not in that seven: 12 pre-exclusion, 6 worst case.

**Read the caveat with the numbers:** conservative pool-size screen, **not** paired-arm feasibility. Does not test covariate balance, anatomical placement, or the control pool. The 50–200 µV range is an injection *rescaling target*, not evidence donors must already sit there — final balance is on post-rescaling amplitude and effective SNR in the selected host. Re-run `Reproducibility Packet/scripts/audit_template_library.py` with different arguments rather than re-deriving by hand.

**Template metadata snapshot**, verified independently by both agents: SHA-256 `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`, 2,032,640 bytes, Last-Modified 2024-09-29. Mutable host, unmoved since 2024. Pin by hash; record selected `template_index` rows.

**Two pre-declarations that exist to stop this project misleading anyone:** a null with a wide interval is **inconclusive, never evidence realism does not matter**; and **Tier A alone cannot conclude the project**, because it is the cheapest axis *and* the least likely to move the interaction.

## 10. Machine state — re-measure, never trust this number

**At 2026-08-11 16:06 PDT: RAM 0.89 GiB free of 31.67. VRAM 14,409 MiB free of 16,311.**

**Fourth consecutive session under 4.5 GiB: 3.46 → 3.96 → 1.01 → 0.89.** The feasibility run that proved Kilosort4 works here peaked at **29.3 GiB**. **VRAM has been fine every time (~14 of 16 GB free); the contention is entirely system RAM.**

Logged in `director_requests.md` with fallbacks; **not blocking**. Measure at the moment of the heavy step, against a measured requirement, never from a file — including this one.

**The venv still contains only `pip`.** SpikeInterface, PyTorch, and Kilosort4 are **not installed**; there is **no `requirements.txt`**. Correct for now — the first install is Codex's Rung 0 pilot, and versions get pinned *at install time*. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe`; never bare `python` or `pip`.

## 11. Housekeeping that is easy to get wrong

- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever.** Any amendment to one updates the other **in the same session**. The playbook names drift as the single most common failure of this artifact, and it is a defect rather than a backlog item.
- **This run is agent-selected**, so the run-provenance block on the public README is **required** and survives unchanged into State B. Do not remove it, soften it, or move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. A genuine need to modify it is a `director_requests.md` question *before* writing the modification. For sorter internals, use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the *only* exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`; `pdftoppm` and `pdftotext` are also available.** Build twice, check the log for overfull/underfull, and render the changed and final pages before approving any PDF.

## 12. Still-open verification debt

Nothing in `references.md` *Pending* is citable: the regional waveform-duration figures, Steinmetz & Ye 2022, and **Quirk & Wilson** (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed). If Quirk & Wilson ever clears, it is the natural citation for burst amplitude attenuation in Study Guide §2.2 and §3.2, which currently carry that load on Harris et al. 2001 and Pouzat et al. 2004.

The SHYBRID snippet-versus-template question is **retired**, not open: the source audit answered the operative half (a fixed template is fit per spike, so it is not raw-snippet transport), and the remainder is not load-bearing.
