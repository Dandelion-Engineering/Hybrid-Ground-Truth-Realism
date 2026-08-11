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

---

*Note on ordering: `Playbooks/director-requests.md` describes the Phase-1-close "Claim Sheet ready for director review" entry as this file's first entry. It is logged when Phase 1 closes, which has not happened yet; this entry precedes it because the blocker arrived first.*
