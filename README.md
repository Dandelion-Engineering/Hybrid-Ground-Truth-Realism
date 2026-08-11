# Hybrid Ground Truth Realism

**Does the realism of hybrid ground truth change measured spike-sorting accuracy?**

| | |
|---|---|
| **Current phase** | Phase 0 — Literature Review |
| **Public state** | `In Progress` |
| **Last updated** | 2026-08-11 |

Spike sorting decides which extracellular spikes came from which neuron. Real recordings have no answer key, so the field grades sorters against **hybrid recordings** — a real recording with synthetic spikes injected at times that are known by construction. The maintainers who built the standard hybrid pipeline wrote down, in print, that they do not know whether their synthetic spikes are realistic enough for the resulting accuracy numbers to mean what the field treats them as meaning. This project tests it: vary the realism of injected spikes along axes the maintainers themselves named, hold everything else fixed, and measure whether sorter accuracy — and, more importantly, the *ranking between sorters* — moves.

---

## How this project was run

- **This is an automated exploratory research run.** It investigates one question and reports what it found. It is not a confirmatory study, and it is not meant to settle anything.
- **The work was selected and carried out by AI agents.** Choosing this question, doing the work, and writing it up were all done by AI agents working inside a documented framework.
- **A human director sets direction and reads summaries. He does not review the work in detail.** Dandelion Engineering is one person working with a team of AI agents; his part is direction and judgement about what is worth doing, not line-by-line verification of what was done.
- **Negative findings are published as produced.** If the answer comes back no, or comes back inconclusive, that is what gets published — on the same terms as a positive one, and without waiting to see whether it is flattering.
- **This is not reviewed work.** It has not been peer-reviewed, and it has not been checked in detail by a human. While the status above reads `In Progress` you are reading work in progress rather than a result; once it reads `Concluded` you are reading a finished exploratory run, which is still not a reviewed one. **The way to trust any of it is to check it** — which is what the reproducibility packet is for.

---

## Running log

- **2026-08-11 — Project opened.** Repository created and made public. Phase 0 (literature review) begun.
- **2026-08-11 — Phase 0: first Literature Foundation written.** Survey of the spike-sorting validation field completed by one of the two agents. Two findings worth flagging early, because they cut against the project's own starting assumptions: the pipeline maintainers named the *firing-statistics* limitation before the brain-region one and proposed a specific fix for it, which may mean the project is aiming at the second-priority axis; and a 2020 benchmark of ~35,000 ground-truth units already reported that synthetic ground truth has a systematically different error signature from real ground truth, attributed to firing statistics. Both make a null result less likely than the project assumed at the outset. Phase 0 does not close until the second agent's independent survey exists and the two have been compared.
- **2026-08-11 — Phase 0: second independent Literature Foundation written.** A live audit found that the template library is substantially larger and more region-diverse than the tutorial snapshot, reducing the broad feasibility concern while leaving host-specific matching unresolved. The two agents are comparing interpretations; Phase 0 remains open pending agreement on the decision threshold and how the updated metadata propagates forward.

---

## What this repository will contain

Four artifacts are produced by a completed Dandelion project. None of them exist yet.

| Artifact | Status |
|---|---|
| **Technical Report** — the full account, written for the field | *Pending (Phase 3)* |
| **Accessible Piece** — the same result for a non-specialist | *Pending (Phase 3)* |
| **Reproducibility Packet** — self-contained code, data pointers, and a verification artifact you can run yourself | *Pending (Phase 2–3)* |
| **Study Guide** — director-facing, two passes | *Pending (Phase 1 and Phase 3)* |

In the meantime, the working record is open and readable as it is written:

- `Project Details/Project Details.md` — the project's constitution and the original idea.
- `Playbooks/` — how each artifact gets built.
- `agents/<name>/` — each agent's workspace: literature foundations, session reports, references, and the running summary each session leaves for the next.
- `chats/` — the agents' file-based conversations with each other and with the director, appended and never rewritten.

**A note on how to read work in progress.** Everything above is live. Nothing in it has been checked by a human, nothing in it is a result, and files change between sessions. The running log records phase closes and genuinely noteworthy events — it is not a session-by-session journal, so its silence does not mean nothing happened.

## Licensing and data

Path-scoped: code and software-like materials under `LICENSE` (MIT); prose and narrative artifacts under `LICENSE-docs` (CC BY 4.0). `LICENSING.md` is the authoritative map of which applies where.

**No raw data is redistributed.** The substrate recordings come from [DANDI 000409 — IBL Brain-Wide Map](https://dandiarchive.org/dandiset/000409) (CC-BY-4.0), referenced by identifier and downloaded by the reader. Templates come from [`SpikeInterface/hybrid_template_library`](https://github.com/SpikeInterface/hybrid_template_library) (MIT). [SpikeInterface](https://github.com/SpikeInterface/spikeinterface) is MIT; [Kilosort4](https://github.com/MouseLand/Kilosort) is GPLv3 and is called as an external tool, never vendored or linked into this project's own code. Full per-dataset detail will live in the Reproducibility Packet's `DATA.md`.

---

## About Dandelion Engineering

Dandelion Engineering is a research and technology company with a single purpose: to do real research, and to turn what we learn from it into affordable technology that materially improves the lives of everyday people. It is not venture-scale and not built to maximize profit — it is a small, deliberate, long-running collaboration between one human director and a team of AI agents, pointed at problems that matter for ordinary people.

- **The essay:** [*What to do when Everything Changes*](https://dandelionengineering.substack.com/p/what-to-do-when-everything-changes)

---

## Contact

Dandelion Engineering is run by Randy Crespo. If this work or the way it was made resonates with you — whether you're a researcher, an engineer, someone working on adjacent problems, or just curious — I'd genuinely like to hear from you. Thoughtful questions, critique, and ideas for collaboration are all welcome.

- **LinkedIn:** [linkedin.com/in/randy-crespo](https://www.linkedin.com/in/randy-crespo)
- **Email:** [randy@dandelionengineering.com](mailto:randy@dandelionengineering.com)
