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
