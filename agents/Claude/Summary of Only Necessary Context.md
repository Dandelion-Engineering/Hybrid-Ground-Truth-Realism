# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 3 · 2026-08-11 14:20 PDT**
**Next session will be Claude Session 4.**

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work.** It is the contract and every design decision below actually lives there. This file is the *state*; the Claim Sheet is the *commitments*.

---

## 1. Where the project is

**Phase 1 — Sharpening.** Phase 1 closes when all three are true:

| Requirement | Status |
|---|---|
| Both agents explicitly approve the **same state** of `Claim Sheet.md` | **Not done.** My Session 3 edits sit on top of the state Codex approved; awaiting its response. |
| The **Accessible Claim Sheet** exists and is agreed | **Not done.** Not yet written — deliberately. See §4. |
| The **division of labor** is agreed | **DONE.** Both agents explicitly agreed in Session 3. |

Study Guide Pass 1 is also due at Phase 1 close, is written, and is awaiting Codex's required approval.

## 2. The first thing to do next session

**Check `chats/Claude-Codex/Claim Sheet Review/` for Codex's response to my three Session 3 edits.**

- **If Codex approved them:** the Claim Sheet is converged. **Write the Accessible Claim Sheet immediately** — it is the single most overdue thing I own, it has been deferred twice, and I committed in the chat to writing it the moment convergence happens. Read `Playbooks/accessible-claim-sheet.md` first.
- **If Codex pushed back:** re-review genuinely, per `Playbooks/review-cycle.md`. The one disagreement I predicted is the pilot ceiling — I made the tranche twice as large and kept the 48-sorter-hour ceiling rather than raising it to 96. If that is the dispute and it survives another round-trip, escalate *that specific point* to Randy rather than looping.
- **Also check `chats/Claude-Codex/Study Guide Pass 1 Review/`** for its review of Pass 1. Same discipline: genuinely re-review its edits, do not wave them through.

## 3. What I did in Session 3

| File | What changed |
|---|---|
| `Claim Sheet.md` | Three re-review edits (§5). Approved by me at SHA-256 `d3e75363ebb80a9372ec1f86f0c8bd8f89cda7ef2d1a7128a7cf059dfe1aebc6`, handed back. |
| `Study Guide/Pass 1 - Conceptual Foundation.tex` + `.pdf` | **New.** 13 pages, zero overfull boxes. In review. |
| `chats/…/Claim Sheet Review/…Active.md` | My re-review turn appended. |
| `chats/…/Study Guide Pass 1 Review/…Active.md` | **New channel**, Pass 1 handed off. |
| `director_requests.md` | **New file.** One entry: machine RAM contention. Non-blocking, fallbacks named. |
| `agents/Claude/references.md` | Jun et al. 2017 (Neuropixels) and Efron 1979 (bootstrap) added, both verified this session. |
| `agents/Claude/README.md`, root `README.md` | Labor split recorded; one lean public log entry. |

## 4. Why the Accessible Claim Sheet still is not written

**This is a deliberate deferral for the second time, and it must not become a third.** The reason is sound — the technical sheet is a draft under active edit, the two documents must stay in sync, and writing the companion against a state about to change means writing it twice and risking drift, which the contract names as a defect. Codex agreed the first deferral was sound.

**But two deferrals is the limit of what that reasoning supports.** If the sheet converges next session, write it that session. If Codex pushes back again and the sheet still has not converged by the *end* of Session 4, write the Accessible Claim Sheet anyway against the current state and keep it in sync afterwards — a companion that needs one revision is better than a Phase 1 that cannot close.

## 5. My three Session 3 Claim Sheet edits, so you can defend them

1. **Slot 5 + Slot 9 — the negative control was missing from the compute budget.** Pseudo-arms must be *sorted*, not merely generated. The pilot's admission budget extrapolated from real arms only, understating the Rung 2 load by 2×. Tranche is now `10 min × 2 arms × 5 blocks × 2 contrast types` = **200 recording-minutes per candidate per tier**; pseudo-arm block count equals real block count; **Codex's 48-sorter-hour ceiling kept, not doubled** — deliberately stricter. Panel-level projection (up to 288 sorter-hours) must be recorded, because individually admitted sorters can still not fit as a panel.
2. **Slot 11 — the comparative decision was stated two ways.** `D = |I| − T` with its interval below zero is now authoritative; the `[−T, T]` phrasing is shorthand for it, never a second test. Declared consequence: `|I|` is folded at zero, so a true null resamples upward and **bounded-negative is the harder verdict**. Conservative in the right direction, but it costs us the outcome we think is likelier — hence declared, not discovered.
3. **Slot 7 — one host and injection zone across all tiers, by default.** Cross-tier reasoning (Slot 13.2) and the A+B minimum (Slot 14) both break if the host moves. Deviation = recorded limitation and the cross-tier comparison is dropped.

## 6. The finding worth carrying forward: CA1

**Tier C's biological prior (CA1 complex-spike bursts) and Tier A's donor-pool requirement intersect in exactly one region.** CA1 holds **12 in-caliper NP1.0 templates across 4 source datasets** before any host-specific exclusion — the only region in the audit satisfying both constraints on its face.

**It is a candidate, not a decision.** CA1's worst-case leave-largest count is **6**, under the ten-unit budget, so viability depends entirely on which source dataset the chosen host belongs to. That is the host-specific exclusion query the Claim Sheet already requires and that **nobody has run yet** — it is Phase 2 work and it is mine under the labor split.

**I am the wrong agent to grade this.** Codex owns Tier A's balance/manipulation gate precisely so the agent proposing the selection is not the agent approving it. Do not drift across that line.

## 7. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate**
- **Tiers B and C:** assigned after Rung 0. For each, the manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention still governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 8. Settled in earlier sessions — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates (configuration only) → Tier B population-rate coupling → Tier C bursting with history-dependent amplitude attenuation. Combined arm only after component effects are known.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units. Standardized effect sizes are secondary and never thresholds.
- **The manipulation check is a hard stop-or-go gate.** If the injected data does not demonstrably carry the property at realistic magnitude, **no sorter run starts.**
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 CPU internal sorter (SpyKING CIRCUS 2, TriDesClous 2, or Lupin — MIT via SpikeInterface). Kilosort-only is biased toward the null.
- **Four errors of mine Codex corrected in Session 2** and I accepted in Session 3: the false "hold everything fixed" claim for Tier A; Tier B's sorter-dependent (circular) rate driver; "significant in one arm, not the other" as a decision event; and the anchor's 50–200 µV rescaling target misused as a donor filter. All are fixed in the sheet. **My `Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 9. Numbers you should not re-derive

**Template audit (Session 2, corrected by Codex in Session 2).** Under provisional screens amplitude 50–200 µV and SNR 5–15: 1,149 of 2,183 NP1.0 templates survive across 149 areas; **37 areas hold ≥10**. After dropping each area's largest contributing dataset — the **worst case**, not the binding number — **7 survive:** CP (42), PIR (19), SUB (18), VISa5 (17), AId5 (14), MRN (14), ENTl5 (10). CA1 is not in that seven: it has 12 pre-exclusion and 6 in the worst case.

**Read the caveat with the numbers:** this is a conservative pool-size screen, **not** paired-arm feasibility. It does not test covariate balance, anatomical placement, or the control pool. The 50–200 µV range is an injection *rescaling target*, not evidence donors must already sit there — final balance is on post-rescaling amplitude and effective SNR in the selected host. Re-run `Reproducibility Packet/scripts/audit_template_library.py` with different arguments rather than re-deriving by hand.

**Template metadata snapshot**, verified independently by both agents: SHA-256 `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`, 2,032,640 bytes, Last-Modified 2024-09-29. Mutable host, but unmoved since 2024. Pin by hash; record selected `template_index` rows.

**Two pre-declarations that exist to stop this project misleading anyone:** a null with a wide interval is **inconclusive, never evidence realism does not matter**; and **Tier A alone cannot conclude the project**, because it is the cheapest axis *and* the least likely to move the interaction.

## 10. Machine state — re-measure, never trust this number

**At 2026-08-11 14:16 PDT: RAM 1.01 GiB free of 31.67. VRAM 14,286 MiB free of 16,311.**

That is the **third consecutive session** under 4.5 GiB free, and by far the worst — 3.46, then 3.96, then 1.01. The feasibility run that proved Kilosort4 works here peaked at **29.3 GiB**. **VRAM has been consistently fine; the contention is entirely system RAM.**

This is now logged in `director_requests.md` with fallbacks, and it is **not blocking**. Measure at the moment of the heavy step, against a measured requirement, never from a file — including this one.

**The venv still contains only `pip`.** SpikeInterface, PyTorch, and Kilosort4 are **not installed**; there is **no `requirements.txt`**. Correct for now — the first install is Codex's Rung 0 pilot, and versions get pinned *at install time*. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe`; never bare `python` or `pip`.

## 11. Three housekeeping facts that are easy to get wrong

- **This run is agent-selected**, so the run-provenance block on the public README is **required** and survives unchanged into State B. Do not remove it, soften it, or move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. A genuine need to modify it is a `director_requests.md` question *before* writing the modification. For sorter internals, use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the *only* exception, and only for artifacts in active review. Do not reopen concluded work.

## 12. Still-open verification debt

Nothing in `references.md` *Pending* is citable: Quirk & Wilson (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed), the regional waveform-duration figures, Steinmetz & Ye 2022. Also open: whether SHYBRID transports individual snippets or an average template — both agents failed to resolve it, it is not load-bearing, and it blocks nothing.

**Study Guide Pass 1 cites none of these**, and if Quirk & Wilson ever clears it is the natural citation for burst amplitude attenuation in that document's §2.2 and §3.2.
