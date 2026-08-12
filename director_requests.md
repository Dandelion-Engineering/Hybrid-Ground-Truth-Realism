# Director Requests

**The single record of work only the director can do.** Append-only. Every entry names what is needed, why, what is blocked, and what the agents are doing meanwhile. The director replies in place; original entries stay as a record.

Randy is asynchronous rather than absent — expect days, not hours. **Nothing in this file blocks a session.** Every entry carries a fallback, and the agents keep working.

---

## 2026-08-11 — Shared-machine memory contention is trending toward blocking the Phase 2 pilot

**Raised by:** Claude, Session 3

**What is needed.** A judgement from Randy about how this project should get access to system RAM on the shared agents desktop — either a rough window when the machine is quieter, an indication of which other projects are running and roughly how long they last, or a decision that this project should simply design around a small memory footprint permanently.

**Why.** Free RAM has been measured at the start of three consecutive sessions and is getting worse, not better:

| When | Free system RAM | Free VRAM |
|---|---|---|
| 2026-08-11 08:22 PDT | 3.46 GiB of 31.67 | 14,269 MiB of 16,311 |
| 2026-08-11 12:07 PDT | 3.96 GiB of 31.67 | 14,389 MiB of 16,311 |
| 2026-08-11 14:16 PDT | **1.01 GiB of 31.67** | 14,286 MiB of 16,311 |

The pre-project feasibility run that proved Kilosort4 works on this machine peaked at **29.3 GiB of system RAM**. Started at any of those three moments it would have failed, and it would have failed slowly rather than cleanly. **VRAM is consistently fine** — the contention is entirely in system RAM, which means whatever else is running is CPU/memory-bound rather than GPU-bound.

This is director-only because `Project Details.md` states the situation plainly: other Dandelion projects run on this machine uncoordinated with this one, and there is no scheduler, no reservation, and no way for an agent here to ask them to wait. The agents can measure the contention and design around it; they cannot resolve it.

**What is blocked.** Nothing yet — but the next scheduled heavy step is Codex's Rung 0 feasibility pilot, which is the first thing in the project that needs real memory, and it is the immediate next step in Phase 2. At 1 GiB free it could not start.

**Fallback the agents are taking, so this does not stall anything.**

1. The Claim Sheet already requires measuring free RAM and VRAM immediately before every heavy step and not starting what does not fit. That rule stands and needs no change.
2. Rung 0 is deliberately small — a 60-second segment — specifically so that it has a chance of fitting into a contended machine. Codex owns its admission budget, which now includes live-headroom guards (no more than 75% of measured free memory, preserving at least 4 GiB RAM and 2 GiB VRAM for everything else).
3. If Rung 0 cannot start, the agents re-measure and retry rather than escalating, and spend the session on work that needs no compute — there is a lot of it, including the Accessible Claim Sheet, the Slot 8 verification artifact's Panel 1, and host/injection-zone selection, which needs only a 2 MB metadata file.
4. If the pilot repeatedly cannot find a window, that becomes a measured finding in its own right and the experiment is re-scoped to a smaller memory footprint through the amendment protocol, rather than waiting.

**What would be most useful in a reply**, in rough order: whether there is a predictable quiet window; whether any other project can be paused for a couple of hours if asked; and whether this project should treat ~4 GiB as its permanent working ceiling, which is a design constraint the agents would rather adopt deliberately than discover.

**Added by Claude, Session 4, 2026-08-11 16:06 PDT — a fourth data point, appended rather than opening a second entry.**

| When | Free system RAM | Free VRAM |
|---|---|---|
| 2026-08-11 16:06 PDT | **0.89 GiB of 31.67** | 14,409 MiB of 16,311 |

Four consecutive measurements, all under 4.5 GiB, and the two most recent are both under 1.1 GiB: 3.46 → 3.96 → 1.01 → 0.89. **VRAM has been fine every single time** (roughly 14 of 16 GB free at every measurement), which continues to say the competing work is memory-bound rather than GPU-bound.

**Nothing changed about what is blocked, and nothing is blocked.** This session did no heavy compute — it closed the Claim Sheet, wrote the Accessible Claim Sheet, and re-reviewed the Study Guide, none of which needs more than a text editor. The measurement is recorded because the contract requires the next session to inherit evidence rather than a hunch, and four points in one direction is now a trend rather than a run of bad luck.

**The third question above has become the practically important one.** If the honest answer is "this machine is busy and will stay busy," the agents would rather adopt a small permanent memory ceiling deliberately — which is a real design decision affecting segment length and the sorter panel, and one the amendment protocol should record — than keep re-measuring and hoping for a window. A reply of "yes, design for ~4 GiB" is more useful than no reply, and is a better outcome than a quiet window nobody can predict.

**Added by Claude, Session 5, 2026-08-11 18:45 PDT — the trend broke, and that is worth recording as carefully as the trend was.**

| When | Free system RAM | Free VRAM |
|---|---|---|
| 2026-08-11 18:14 PDT | **15.27 GiB of 31.67** | 14,416 MiB of 16,311 |
| 2026-08-11 18:45 PDT | **14.39 GiB of 31.67** | 14,405 MiB of 16,311 |

Five and six consecutive measurements now read 3.46 → 3.96 → 1.01 → 0.89 → **15.27 → 14.39**. Whatever was consuming roughly 28 GiB through the afternoon released it some time between 16:06 and 18:14. **VRAM has been flat at ~14 of 16 GB free at every single measurement**, which continues to say the competing work is memory-bound rather than GPU-bound.

**Read this as a data point, not as an answer.** It tells us the machine is *not* permanently at 1 GiB free, which is the more optimistic of the two hypotheses in the original request and argues against adopting a hard ~4 GiB design ceiling on the evidence available. It does **not** tell us the contention is over, when it returns, or whether a window is predictable — six measurements taken opportunistically in one day cannot support that, and the contract's rule stands unchanged either way: measure immediately before the heavy step, against a measured requirement, and do not start what does not fit.

**Nothing was blocked and nothing changed.** This session's work was metadata-only — a 2 MB table and HTTP range reads of NWB headers, a few megabytes per recording — and never approached the memory floor. **The most useful reply is still the third question**, and this measurement slightly changes what would be useful about it: not "how little should we design for" but "is there a pattern to when this machine frees up."

---

### ✅ RESOLVED — Randy's reply, 2026-08-11, relayed by Claude (Session 5 addendum, 19:40 PDT)

**Randy answered this in conversation rather than in the file.** It is recorded here so the record is complete and so neither agent has to find it in a chat. **The words below are my summary of what he said, not a quotation of something he wrote here** — the original entry above stays as the record of the question.

**The memory was not another project's work. It was leftover processes from Claude automations that had finished and never exited**, holding roughly 28 GiB while doing nothing. Randy cleared them. He and Dandelion Station are building a fix so processes are not left running after they complete. He noted that killing them accidentally closed the Claude app.

**One correction to my own inference, made here rather than left standing.** Four sessions of this file present a worsening trend — 3.46 → 3.96 → 1.01 → 0.89 GiB free — and I described it as contention with work "we cannot see" and "cannot ask to wait." That framing was wrong. It was measuring accumulated dead processes, not competition. The measurements were accurate; the story I attached to them was not, and anything either agent inferred from the *shape* of that series should be discarded.

**Answers to the three questions I asked, in order:**

1. **Is there a predictable quiet window?** Yes, and it is now a schedule rather than a hope. **Two research projects share this machine. Randy has decided this one runs during the day and the other runs overnight.** Heavy steps should be aimed at daytime.
2. **Can another project be paused if asked?** Effectively moot — the thing that needed stopping was not a project, and it has been stopped.
3. **Should this project treat ~4 GiB as a permanent working ceiling?** **No.** That was the practically important question and the answer is that we should not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds. If the sorter panel narrows, it narrows because Rung 0 measured it narrow.

**What does not change.** Free memory is still a measurement rather than a property: the other project genuinely runs overnight, the process-leak fix is in progress rather than landed, and a session starting near a boundary can still meet a busy machine. **The Claim Sheet's rule stands unchanged — measure free RAM and VRAM immediately before every heavy step, against a measured requirement, and do not start what does not fit.**

**Reading at the time of this reply: 2026-08-11 19:40 PDT — 13.85 GiB free of 31.67; VRAM 14,413 of 16,311 MiB.** Do not inherit it.

**This request is retired.** It is left in place rather than deleted, per the append-only rule. Codex has been informed in `chats/Claude-Codex/Compute Environment Update/`, including my read that this needs **no Claim Sheet amendment** — Slots 4 and 10 already describe a shared machine and a live-measurement gate, and no commitment was written because of the contention — with the one arguable exception, recording the day/overnight schedule in Slot 10, left open for Codex to propose if it disagrees.

---

*Note on ordering: `Playbooks/director-requests.md` describes the Phase-1-close "Claim Sheet ready for director review" entry as this file's first entry. It is logged when Phase 1 closes, which has not happened yet; this entry precedes it because the blocker arrived first.*

---

## 2026-08-11 — Phase 1 contract is ready for director review

**Raised by:** Codex, Session 4

**What is needed.** Randy's review of the agreed project contract. The preferred entry point is `Accessible Claim Sheet.md`, which carries the same fifteen slots, commitments, numbers, and honesty bounds as the technical `Claim Sheet.md` in plain language. `Study Guide/Pass 1 - Conceptual Foundation.pdf` is the conceptual companion. If anything should change, reply beneath this entry with the point and the reason; the agents will treat it as the first amendment cycle.

**Why.** Phase 1 is closed: both agents explicitly approved technical Claim Sheet SHA-256 `a5f586041b074ff4a86fec2bac88f02f76a6e79cce1d7d2a859e4c24a92c91f3`, Accessible Claim Sheet SHA-256 `73bff8f81dc2e31b47d4abbe1f61c8106a34dccb8ea6457051c3dba84a589760`, and the Study Guide source/PDF pair. This is the planned point where the director can inspect the question, method, compute ladder, verification path, and pre-declared success/failure/inconclusive shapes before substantial execution.

**What is blocked.** Nothing. Director review is explicitly non-blocking, and Phase 2 begins under the agreed contract while the review is pending.

**Fallback the agents are taking.** Codex proceeds to the resource-gated Rung 0 feasibility pilot and inference harness; Claude proceeds to Tier A host/injection-zone selection. Any later director feedback is handled through a dated amendment rather than by quietly rewriting the agreed contract, and the Accessible Claim Sheet is updated in the same work unit if the technical sheet changes.

**What would be most useful in a reply.** Any commitment that feels wrong, any boundary that feels too weak or too strict, or an explicit “no amendment requested.” No technical markup is required.
