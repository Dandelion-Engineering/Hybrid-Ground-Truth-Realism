# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 1 · 2026-08-11 10:23 PDT**
**Next session will be Claude Session 2.**

You are starting with no memory of the last session. This file exists to restore everything you need and nothing you don't. It deliberately omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those at session start anyway.

---

## 1. Where the project is

**Phase 0 — Literature Review. Not closed.**

Phase 0 closes when *both* agents have written their Literature Foundation and the comparison chat is done. Mine is written. **As of the end of Session 1, Codex had not run a session at all** — no session summaries, no literature foundation, empty workspace. So the first thing to check next session is whether that has changed.

Nothing is blocked on the director. `director_requests.md` does not exist yet and did not need to.

## 2. What I produced in Session 1

| File | What it is |
|---|---|
| `agents/Claude/Literature Foundation.md` | The Phase 0 survey. Six sections, 16 ledger-quality sources, all link/DOI-verified by live search. **Frozen** — corrections go forward, not back into it. |
| `agents/Claude/references.md` | The **living** citation ledger. Where it and the Literature Foundation disagree, this governs. Has a *Pending* section of unverified sources that are **not citable**. |
| `agents/Claude/README.md` | Workspace guide. |
| `README.md` (repo root) | The Live-Run README, State A, per `Playbooks/live-run-readme.md`. Replaced the Collaboration Station template README. Run-provenance block **required and present** — this is an agent-selected run. |
| `CITATION.cff`, `LICENSING.md` | Rewritten to describe this project; they were still describing the framework template. |
| `chats/Claude-Codex/Phase 0 Literature Comparison/…Active.md` | Opened by me. Awaiting Codex's first message. |
| `agents/Claude/Session Summaries/HumanReport1.md` | Session report. |

## 3. The findings that should shape Phase 1

These are the reason the Literature Foundation was worth writing. Do not re-derive them.

1. **The maintainers named the *firing-statistics* limitation first, and proposed a fix.** The brief quotes only the brain-region sentence. The sentence before it says spike times were Poisson and "do not necessarily match the overall firing statistics of the original recording," and proposes: *"estimate ongoing population firing rates and inject spike trains that follow the dynamics of nearby neurons."* That is a **third candidate axis — population-coupled firing** — distinct from within-unit bursting, needs no waveform model (just an inhomogeneous Poisson process driven by a locally estimated rate), and is therefore probably cheaper to build. **Raised with Codex; not decided.**

2. **SpikeForest (Magland et al. 2020, ~35,000 GT units) already observed the fingerprint.** Synthetic studies show precision > recall in a way paired ground truth does not, attributed to simulations "not yet duplicating the firing and noise statistics of real-world electrophysiology recordings." **This makes a clean negative less likely than the project assumed.** Plan for the positive branch too.

3. **The yardstick for Slot 7 is the anchor paper's own effect sizes: 0.276 (NP1.0) and 0.408 (NP2.0)** for Kilosort4 over Kilosort2.5. Define "decision-relevant" against those, not against zero.

4. **A Kilosort4-vs-Kilosort2.5-only panel is biased toward the null.** Same family, shared drift-correction lineage; and the companion paper flags that hybrid data injected with motion-corrected templates advantages sorters using the same motion correction. Sorters diverge most on **collision handling**, along template-matching vs density-based lines. A second, mechanistically different sorter is scientifically wanted — **compute feasibility is the open question**, asked of Codex.

5. **The bursting axis has a mechanism, not a story.** Real bursts: ≤6 ms ISIs, extracellular amplitude *decreasing across the burst*, burst probability suppressed by recent firing (Harris et al. 2001). A sorter built around ISI-dependent amplitude decay exists (Pouzat et al. 2004). A fixed average template presents amplitude independent of firing history; a real neuron does not.

6. **The axis ratio, confirmed from the SpikeInterface docs rather than assumed:** `refractory_period_ms` **present** (not a delta); `brain_area` metadata **present** (measurement, no new code); bursting / rate non-stationarity **absent** (must be built). This is what makes part of this project engineering, and the Claim Sheet must be honest about the split.

## 4. Design constraints I committed to in writing

Stated in the Literature Foundation §4.3 and in the chat. Carry them into the Claim Sheet.

- **Match on `amplitude_uv` and `signal_to_noise_ratio` across arms**, or a realism effect is an amplitude effect in disguise.
- **Hold total spike count per unit fixed** across bursting arms, or the comparison is about N, not structure.
- **Factor the axes.** Region-matching (static waveform shape) and bursting (temporal statistics + within-unit dynamics) are mechanistically different; varying them together makes an effect unattributable.
- **Paired designs** — same recording, same units, same seeds, one knob changed — are how a single shared desktop buys statistical power it cannot buy with N.
- **Seeded, pre-declared template selection**, recorded in the packet.
- **A manipulation check as a stop-or-go gate.** Before any sorter time, verify from the injected data that the realism knob actually turned (burst ISI structure and amplitude attenuation present at realistic magnitudes). Without it, a null is a statement about our implementation, not about the field's method.
- **Predeclare a distinct *inconclusive* shape.** A null with a wide interval is not a negative result.

## 5. Open questions — mine to resolve or to settle with Codex

**Asked of Codex in the chat, awaiting reply:**
1. Is population-coupled firing a real third axis, and is it cheaper than bursting?
2. Can this machine afford a non-Kilosort sorter? (I asked for a feasibility read, not a preference.)
3. Which axis first? I lean **region-matching first** — no new code, settles the cheap axis before we build the expensive one.
4. Who runs the template-library feasibility query.

**Empirical, unanswered, and the biggest feasibility risk:**
**Does `hybrid_template_library` hold enough templates in the specific brain regions of the DANDI 000409 recordings we'd use, at comparable amplitude and SNR, to build both a matched and a mismatched arm?** The confirmed `brain_area` values skew heavily to visual cortex. **This is a cheap database query — `fetch_templates_database_info()`, group by area, cross against candidate recordings' regions — and it must be answered before Phase 1 commits to the region axis.** If matched templates are scarce, redesign the axis (e.g. matched vs maximally-distant) rather than quietly weaken it.

## 6. Verification debt — do not let these harden into fact

Full list in `Literature Foundation.md` §5.4; the two that matter:

- **The "key ingredients" quote.** The project brief quotes eLife 110588 as saying the hybrid pipeline *"already has the key ingredients to challenge spike sorting algorithms."* The version I reached renders the equivalent claim as "core features needed to properly challenge modern spike sorters." **The negative-result framing leans on this quote. Do not publish the brief's wording until it is confirmed against the PDF.**
- **Kilosort4's simulator** advertises "non-stationary spike waveforms." If that already includes ISI-dependent amplitude attenuation, part of the axis we call missing exists inside a comparator's own benchmark — which would materially change the framing. bioRxiv rate-limited me.

Also pending and **not citable** until verified: Quirk & Wilson on activity-dependent amplitude attenuation (only PMC6762418 located, full citation unconfirmed); the regional waveform-duration figures; SHYBRID's exact injection mechanism; Steinmetz & Ye 2022.

## 7. Machine state — re-measure, never trust this number

**At 2026-08-11 10:23 PDT: RAM 4.42 GiB free of 31.67 GiB (~86% in use); VRAM 14,731 MiB free of 16,311 MiB.**

The pre-project feasibility run that proved Kilosort4 works here peaked at **29.3 GiB of system RAM**. Started at that moment, it would have failed. Other projects run on this machine uncoordinated with you. **Measure at the moment of the heavy step, not at session start, and never from a file — including this one.**

**The project venv contains only `pip==25.0.1`.** SpikeInterface, PyTorch, and Kilosort4 are **not installed**. There is **no `requirements.txt` yet**. Creating it and pinning versions at install time is a Phase 2 task and is a hard standard, not a nicety. Use `.\venv\Scripts\python.exe` and `.\venv\Scripts\pip.exe` — never bare `python` or `pip`.

## 8. Next session, in order

1. **Check whether Codex has run.** If its Literature Foundation exists, read it properly and reply in the comparison chat — that also discharges the cross-review obligation. If it does not exist, Phase 0 still cannot close; do useful non-blocking work instead (items 2 and 3).
2. **Run the template-library feasibility query.** Cheap, de-risks an axis, needs only a light install (`spikeinterface` + pandas, no GPU stack) — but check free RAM first and pin whatever you install into `requirements.txt` the moment you install it.
3. **Clear verification debt**, prioritising the quoted sentence and the Kilosort4 simulator question.
4. **Once Phase 0 closes, begin the Claim Sheet.** I am the default writer; Codex is the required reviewer and gives final approval. Read `Playbooks/claim-sheet.md` before starting it. Phase 0 close is a **phase transition**, which triggers a Progress Report from whichever agent's session closes it — if that is me, `Playbooks/research-progress-report.md` and `agents/Claude/Progress Reports/`.
5. **Live-Run README heartbeat.** Check at the end of every session whether anything is worth a log entry — a finished artifact, a phase close, or a genuinely noteworthy finding. Phase 0 closing would be one. Routine sessions are not.

## 9. Two housekeeping facts that are easy to get wrong

- **This run is agent-selected**, so the run-provenance block is **required** on the public README and survives unchanged into State B. Do not remove it, soften it, or move it below the result.
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor its source, never link against it. If a genuine need to modify it appears, that is a `director_requests.md` question *before* writing the modification. For sorter internals, use SpikeInterface's MIT `sortingcomponents` instead.
