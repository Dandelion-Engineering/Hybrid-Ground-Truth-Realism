# Hybrid Ground Truth Realism

**Does the realism of hybrid ground truth change measured spike-sorting accuracy?**

| | |
|---|---|
| **Current phase** | Phase 2 — Execution (contract and Phase 1 companions agreed; feasibility pilot next) |
| **Public state** | `In Progress` |
| **Last updated** | 2026-08-11 |

Spike sorting decides which extracellular spikes came from which neuron. Real recordings have no answer key, so the field grades sorters against **hybrid recordings** — a real recording with synthetic spikes injected at times that are known by construction. The maintainers who built the standard hybrid pipeline wrote down, in print, that they do not know whether their synthetic spikes are realistic enough for the resulting accuracy numbers to mean what the field treats them as meaning. This project tests it: vary the realism of injected spikes along axes the maintainers themselves named, hold every axis-compatible nuisance variable fixed or matched, and measure whether sorter accuracy — and, more importantly, the *ranking between sorters* — moves.

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
- **2026-08-11 — Phase 0 closed. Both corrections accepted; one of them was a bad success bar caught before it reached the contract.** The second agent blocked the first agent's synthesis on two points and both were upheld: a stale template-library figure taken from a tutorial snapshot rather than the live data, and — the more consequential one — a proposal to use another paper's standardized effect sizes as the threshold for whether a result matters here. Those are scaled over a different sample and are not commensurable with a raw accuracy change; the decision threshold is now measured inside this experiment instead. A success bar written wrong quietly determines the answer, so it is worth recording that this one was caught in review rather than after results.
- **2026-08-11 — A feasibility check reversed a design decision before it was made.** Enforcing the rule that donor waveforms may not come from the host recording's own source dataset — otherwise the test is partly rigged — cuts the usable brain regions from 37 to **7**, with 13 of the 37 collapsing to zero because a single dataset had supplied all their templates. So the templates constrain which recording can be used, not the other way round, which is the reverse of the assumed order. The audit script is already in the reproducibility packet and the filter is a command-line argument, so the numbers can be re-derived at other thresholds. Both agents reached the same measurement of the live metadata independently, matching to the byte.
- **2026-08-11 — Phase 1 opened: the Claim Sheet is drafted and in review.** The contract now names three realism axes tested one at a time, a stop-or-go gate requiring the manipulation to be demonstrably real before any sorter time is spent, and pre-declared shapes for success, failure, and *inconclusive*. Two of those pre-declarations are deliberately uncomfortable: a null result with a wide interval will not be reported as evidence that realism does not matter, and the cheapest axis — the only one needing no new code — cannot conclude the project on its own, because it is the least likely of the three to move the thing the project is actually asking about.
- **2026-08-11 — Claim Sheet review corrected the feasibility and decision rules before execution.** The earlier 37→7 log entry was too strong: seven is the conservative worst case after removing each area's largest donor source, not the usable count for every represented host, and the audit is a pool-size screen rather than proof that balanced paired arms exist. The reviewed contract now uses an anchor-like region-unaware control, anatomical injection zones instead of a whole-recording region label, a hierarchical paired-block estimand, and a direct interaction/equivalence rule rather than treating “significant in one arm, not significant in the other” as a difference. Codex explicitly approved the revised bytes; the Claim Sheet remains in review until Claude re-opens and approves or revises that same state.
- **2026-08-11 — The re-review found the experiment's compute budget was missing half the work, and one brain region turned out to satisfy two separate constraints at once.** The design's strongest control generates "pretend" comparisons where nothing was actually changed, to see how much apparent effect the machinery invents on its own. Those have to be *sorted* like everything else, and the pre-declared compute budget had counted only the real comparisons — understating the cost of the primary run by a factor of two, before anything was spent. Separately, the requirement that the burst parameters rest on real biology (which currently means hippocampal CA1) and the requirement that enough donor waveforms survive the anti-leakage rule intersect in exactly one region in the audit: **CA1**, which is now the leading candidate and not yet a decision. The Claim Sheet is still in review; the director-facing Study Guide's first pass is drafted and awaiting review.

- **2026-08-11 — The contract is agreed. Both agents have now approved the same version of the Claim Sheet, after four rounds of review in which each of them blocked the other.** The question, the method, the three realism axes, the stop-or-go gate, and the pre-declared shapes of success, failure and *inconclusive* are now fixed before any measurement exists — which is the whole point of writing them down first. Worth recording what the review actually cost, because it is the case for doing it: seven substantive errors were caught and corrected before execution, four of them by the reviewing agent and three by the writing agent re-reading its own approved text. Three were the kind that quietly decide an answer — a threshold borrowed from another study that was not comparable to anything measured here, a design in which one of the sorters being graded would have supplied the target used to generate its own test data, and a decision rule that treated "significant in one arm, not the other" as evidence the two arms differ. The plain-language companion to the contract is now written and under review, and the director-facing study guide is on its second round.
- **2026-08-11 — Phase 1 closed; Phase 2 begins.** The Accessible Claim Sheet and Study Guide Pass 1 have now passed same-state review alongside the technical contract and labor split. No result exists yet. Execution starts with a resource-gated 60-second feasibility pilot that decides which sorter panel this shared machine can actually support; live system memory has been the binding constraint, so no candidate run starts unless the declared headroom survives a measurement taken immediately beforehand.

---

## What this repository will contain

Four artifacts are produced by a completed Dandelion project. Study Guide Pass 1 now exists and is approved; the outward-facing artifacts remain in progress or pending.

| Artifact | Status |
|---|---|
| **Technical Report** — the full account, written for the field | *Pending (Phase 3)* |
| **Accessible Piece** — the same result for a non-specialist | *Pending (Phase 3)* |
| **Reproducibility Packet** — self-contained code, data pointers, and a verification artifact you can run yourself | *Pending (Phase 2–3)* |
| **Study Guide** — director-facing, two passes | *Pass 1 approved at Phase 1 close · Pass 2 pending (Phase 3)* |

In the meantime, the working record is open and readable as it is written:

- `Claim Sheet.md` — the project's contract: the question, the method, the baselines, and the pre-declared shapes of success, failure, and inconclusive. Both agents have now approved the same state of it. If you read one file here, read Slots 11–13.
- `Accessible Claim Sheet.md` — the same approved contract in plain language, written for a reader with no background in the field. Same commitments, same numbers, no jargon wall. **If you would rather read one file than two, read this one instead of the sheet above.**
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
