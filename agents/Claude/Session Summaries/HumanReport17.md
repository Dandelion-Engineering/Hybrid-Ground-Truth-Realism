# Human Report 17 — Claude

**Current date and time:** 2026-08-13 06:22 PDT

**Session:** Claude Session 17

**Phase at start:** Phase 2 — Execution. Amendments 1–6 all `In force`. Codex had returned Draft 5 of his Tier A real-arm donor-matching rule for my exact-state review. No host pinned, no donor selected, no generator or sorter run, no scientific result.

**Phase at end:** unchanged. Draft 6 of the matching rule is approved by me and back with Codex; Draft 8 of my host-selection document is approved by me and handed to Codex. No host, no measurement, no result.

**Progress report due?** No. My next count-based report is Session 24, and this session closed no phase transition and wrote no approving turn on an amendment.

---

## Summary

Two pieces of work, and the second exists because of the first.

**The review.** I re-opened Codex's Draft 5, verified its digest on disk before reading it, reran my provenance probe and reproduced its recorded output, and reviewed the state against the in-force Claim Sheet rather than against my own last draft. Every Draft 5 decision is accepted. Codex had replaced my Draft 4 repair — a promised master seed — with something stronger: a separate exposure-schedule and placement specification that has to be approved before the pool is visible. He was right that my version pinned the word "deterministic" and left every draw that mattered selectable afterwards. I made three changes and handed back Draft 6.

**The finding.** The most useful of the three came out of noticing that two sentences in Draft 5 describe two different objects, and that the tension is not Codex's — it is in the Claim Sheet. Amendment 6 leaves placement seeds "randomized" while also requiring every block of ten donors to *admit* a jointly feasible placement assignment. Read one way the seeds decide the placements and the gate merely checks them; read the other way the gate searches for placements and the seeds decide nothing. The two readings differ in how often a candidate recording gets rejected. Draft 6 does not choose between them — that is Codex's specification to write — but it now requires the specification to say which one it is.

**The consequence that landed in my own lane.** Reviewing the host-rejection semantics made visible that the project's "take the first recording that passes every check" rule was not a rule. First is a property of a sequence, and the sequence had been sitting in my own document explicitly labelled a *recommendation* since Session 9. A rejected host is followed by another host, which brings its own donors, its own schedule and its own balance report — so an unpinned order is compatible with working down the list until one reads well. **I pinned all thirteen candidates, and what happens when they are exhausted, before any of the remaining gates has been run on any of them.**

**The drift quantity.** The other open piece of my lane. The archive's own drift column is retired on the strength of its own published description, and a replacement is defined — net displacement rather than accumulated path length, spike-count-free by construction, with a within-recording permutation null so that a reading which is really estimation noise is reported as noise rather than as a quiet probe. The threshold and its single pre-declared relaxation are written now, while no candidate's value is known.

Nothing was downloaded. Nothing heavy ran. No dependency was installed.

---

## 1. Startup and workflow control

The turn gate authorized work: `.agent-turn` named `Claude`; `.agent-session.lock` did not exist; I created it and re-read `.agent-turn`, which still named `Claude`. I then read `AgentPrompt.md`, `Project Details/Project Details.md` in full, my continuity file, every `Summary.md` in the chats I am party to, and both active chats.

My continuity file warned that it describes the moment it was written and that Codex had posted after the previous one closed. That was true again: Codex's Session 16 handoff landed at 05:07 PDT, forty-nine minutes after my Session 16 file was written, and it is what opened this session's work.

Working tree clean at startup; HEAD and `origin/main` both at `b3b4311`, Codex Session 16.

## 2. Exact-state review of Draft 5

Handed-off digest `23148d2d8896db70f48d13bd712bbf4ba04987b7f348866918a98431fc324cf7`, confirmed on disk before reading a word.

### 2.1 What I accepted, and why the thing I accepted is better than mine

My Draft 4 had required the exposure schedule's nuisance draws to come from "a master seed derived by the construction the contract already uses twice." Codex declined to treat that as complete, and he was right. The derivation string, the occurrence-identifier grammar, the stream mapping, the amplitude-target law and the placement transform were all still to be chosen — by a configuration written after the candidate pool was visible. A seed recorded after the fact makes one run reproducible; it does not make the choice precommitted. Draft 5 moves all of it into an artifact that must be approved before the surviving donor set is even measured.

He also caught an input my handoff had not named: the **amplitude target** is part of the schedule and the matched quantities are realized at it, so leaving the amplitude law pool-aware while fixing only the placement seeds would have left two of the three matching quantities selectable.

### 2.2 Change one — which object the block-placement gate evaluates

Draft 5's specification list asked for "the mapping from a placement seed and the pinned candidate-site set to **one commanded placement**." Two paragraphs later, every block's ten targets "must **admit** a jointly feasible ten-placement assignment."

Those describe different objects. The document did not say which one the renderer uses, and neither does the contract:

- Amendment 6 point 4: "Slot-within-block assignment, spike-time seeds and placement seeds remain randomized exactly as before."
- Amendment 6 point 1: "every block's ten scheduled donors must admit a jointly feasible ten-placement assignment... If any block lacks such an assignment, the host is rejected."

If each occurrence is drawn on its own, the joint gate can only verify what the seeds produced, joint feasibility becomes a property of the draw rather than of the rule, and a candidate recording dies whenever ten independent draws happen not to fit together. Strict, but coherent. If a block's ten are derived together, then the algorithm deriving them is the thing that has to be pinned — because a search that can be re-run in a different order is a redraw wearing another name.

Draft 6 requires the specification to state which, and adds one sentence to the block-placement paragraph pointing at that resolution instead of implying a search. **I deliberately did not choose between the two readings.** It is Codex's specification and his placement rule, and the requirement is written so either answer satisfies it. The timing was worth getting right: writing that specification is his next declared step.

### 2.3 Change two — an implementation boundary that did not match its own document

Section 2.2 requires the schedule specification to be approved before "the target-eligibility manifest, U, R, any host-specific eligible pool, or any rendered edge table" is constructed. The status line and the closing sentence of Section 10 both say "manifest, pool, or edge table." Section 9's operative sentence said "any host-specific eligible pool or rendered edge table" and dropped the manifest — so read literally it permitted building the manifest first, which the rest of the document forbids.

A governing sentence elsewhere does not repair an operative sentence that says something weaker. That is precisely the mistake I nearly shipped in Session 16, pointing the other way, and I was not going to leave the shape in place because this time it was not mine.

I aligned it **and extended the boundary from step 1 to all four steps**, which is a tightening and is flagged as one. The manifest is where the surviving donor count and the three provenance counts first become visible, and those are exactly the numbers that decide which matching stage is reached and which level binds inside it; a matcher implemented after they are known is implemented against known values. The no-infeasibility argument is that all four steps are pre-host work on synthetic inputs. I told Codex explicitly that if he wants it to bind only step 1, I will approve the narrowing — it is his artifact.

### 2.4 Change three — the forking path the document does not close

Named in Section 10 as an explicit non-claim rather than fixed there, because it is not that document's to fix. A rejected host is followed by another host with its own sites, its own surviving set, its own schedule and its own balance report; nothing in the matching rule pins which host comes next.

### 2.5 One thing probed and deliberately not edited

Section 8's digest-mismatch failure bullet does not name the schedule/placement-specification digest, although Section 7 requires that digest to be recorded. I was going to add it and then did not: the adjacent bullet already fires when the schedule fails to reproduce byte for byte from the approved specification, which is strictly stronger — a matching digest with a non-reproducing schedule still fails, and a mismatched digest cannot produce a reproducing schedule. Adding the weaker check beside the stronger one would be noise.

I also checked that the ordering the document implies — host, then sites pinned, then specification approved, then manifest, then schedule, then the placement gate, then pool and edge table, then matching — is contradicted by no sentence in it. It is not stated in one place, and I did not add a summary that could drift out of step with the sections it summarizes.

**Handed back: Draft 6, SHA-256 `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282`.**

## 3. Host selection — the candidate order, pinned

This is §15 of `agents/Claude/Tier A Host and Injection Zone Selection.md`.

Codex's ruling 7.3 settled the standard in Session 7: apply the remaining gates sequentially and pin the first fully admissible host, labelled admissible rather than best. I accepted it and then wrote the three-host order into §10.6 as an explicit recommendation — "It is not a selection" — and every continuity file since has repeated the word. Reviewing Draft 5 is what turned that from untidy into consequential.

**The order is now thirteen deep.** Ranks 1–3 are §10.6's three, in the order it named them, because that judgment was exercised and published before any open gate existed. Ranks 4–13 are the rest of the §4.2 table by descending contiguous CA1 channel count, ties broken by ascending `(subject, session, probe)`. The tail key carries no judgment on purpose — §4.3 already calls channel count "a convenient ordering, not a quality score," which is exactly what recommends it for a tail. A digest ranking of the kind two amendments already use was considered and rejected as more machinery for an order the table already determines.

**Exhaustion is pinned too.** If all thirteen fail, the anatomy survey resumes from its recorded index and new candidates are appended in **discovery order**, not re-sorted — because by then the gates' behaviour on the first thirteen is known and any re-sort would be informed by it. The listing order is the one ordering that cannot be. It is clustered by subject and lab, and the section says so rather than pretending otherwise.

**The gate order is also pinned**, though it cannot change any verdict — a host must clear every gate — only the cost of reaching it: drift, then noise, then post-rescaling effective SNR, then the joint ten-placement gate (which cannot run until the manifest and rota exist), then Codex's balance and manipulation gate.

Two consequences I named rather than let be discovered. Ranks 4 and 5 carry more CA1 channels than rank 3, because the recommendation is honoured over the mechanical key and rank 3 is the depth-specific-zones fallback for the recording at rank 1. And NYU-39 Probe00 lands at rank 9 with no special handling: it was recorded in Session 10 as high-risk on native yield and explicitly *not* disqualified, so moving it by hand would be applying a gate the contract does not have under the name of ordering.

**The timing claim is checkable rather than asserted: no drift, noise or effective-SNR value has been measured for any candidate.**

## 4. Host selection — the drift quantity, defined before measuring

§16 of the same document. The rule it obeys is one this project already paid for: a measurement you just made is not a threshold you get to set.

### 4.1 The column that looks like the answer

`cumulative_drift_um_per_hour` has been sitting in the units table, recorded as uninterpreted since Session 10. Its own first-party description settles it: *"Sum of absolute depth changes between consecutive spikes... Scales with spike count (~0.79 correlation). NOT actual electrode displacement."*

Three disqualifications. It is a **path length**, so a probe that moves 5 µm down and back scores like one that moves 10 µm and stays — but what a sorter has to survive is the displacement, because that is what moves a waveform across contacts. It **scales with spike count**, which this project specifically cannot afford: Tier B's whole manipulation is population-rate coupling, so a host chosen for scoring low on a count-correlated quantity is a host chosen partly for being quiet, which biases that tier before it starts. And IBL says outright that it is not electrode displacement.

### 4.2 What the archive actually exposes, and where the evidence already was

`spike_distances_from_probe_tip_um` is per-spike depth from waveform centre of mass, ragged, with its own index, alongside `spike_times` on the same structure. Per-spike depth and time are therefore both available without raw data and without re-sorting, and the ragged index means only the units in the band need reading.

That description was already downloaded and stored in `Reproducibility Packet/results/amplitude_conventions.json` in Session 8. The lesson from Session 7 arrived again unchanged: read the rich first-party table's own column descriptions before concluding a quantity is unavailable.

### 4.3 The quantity

Sixty-second bins; per unit per bin the **median** per-spike depth; each unit centred on its own across-bin median; the band trace is the **median across units**; and the reported numbers are net displacement over the whole recording and over the **worst** ten-minute window. The worst window gates, because Rung 2 injects into a ten-minute segment and the segment has not been chosen — a gate on a chosen window would let a quiet segment be picked after the trace is visible.

Both constraints are satisfied structurally rather than by tuning. It is a difference of two levels rather than a sum of increments, so adding bins cannot inflate it. Every step is a median with a micrometre output, so more spikes sharpen the estimate rather than enlarge it.

### 4.4 Separating movement from estimation noise

The medians suppress independent noise but do not measure what is left, so the estimator carries a **within-recording permutation null**: re-assign each unit's spikes to bins at random within that unit, preserving every depth value and every bin count while destroying time order, and recompute. That is what the estimator reports on this recording when nothing moves. A candidate whose observed value sits inside its own null is **not** a quiet host — it is a host whose drift this estimator cannot resolve, and it is recorded as that.

Two things it does not do, stated rather than assumed: it does not bound systematic bias in IBL's depth estimator, because the permutation preserves the depth values; and it does not distinguish probe movement from tissue movement, which nothing available could and which are the same thing from a sorter's point of view.

### 4.5 The circularity question, answered explicitly

The estimator consumes IBL's sorting, and this project has already killed one design for consuming sorter output, so the distinction is written out rather than assumed. Tier B's defect was that sorter output would have defined **the manipulation**. Here it selects **the host**, and one host serves every arm and every sorter, so the bias is common to all of them.

The residual I did not want left unstated: IBL sorted with a Kilosort-family pipeline, so a host whose IBL sorting is clean may be congenial to Kilosort-family sorters. A constant per-sorter offset cancels from the paired difference in differences, which is the estimand — but it does **not** cancel from the control-arm sorter gap that sets the materiality threshold. Neutral for the estimand, not neutral for the threshold that grades it, and it belongs in the limitations rather than in a claim of cleanliness. I flagged it to Codex as the judgement in §16 I am least sure of.

### 4.6 The threshold and its ladder

The gate binds at **20 µm** of net displacement in the worst ten-minute window — one Neuropixels 1.0 contact row spacing. The basis is geometric and candidate-independent: a displacement below the inter-row pitch cannot systematically move a unit's peak channel during the segment.

**One pre-declared relaxation, to 40 µm** — the two-row gap the document already uses as its anatomical contiguity criterion — published with the values that forced it, and beyond that the host is rejected regardless. Declaring the ladder now is the same discipline the matching rule uses for its provenance stages: a threshold with a pre-declared relaxation is a rule; a threshold relaxed once the values are in is a choice wearing a rule's clothes.

**A failure to measure is not a pass.** Too few qualifying units, or an observed value inside its own null, rejects the host as unmeasurable with the reason published.

## 5. Cross-review

I read Codex's `HumanReport16.md` in full, along with Draft 5 and the complete review chat. Its state description, hashes and numbers match the artifacts; I reran his independently reproduced provenance census myself and it matches too. I have no disagreement with it. His Session 16 next-step list correctly names the drift-gate definition and host-admissibility work as mine, which is what this session did.

## 6. A mistake of my own, corrected in place

The header on my first message in the selection-review chat reads `06:30 PDT`. It was written at `06:20` and quotes a machine reading taken at `06:13`. I wrote the time forward instead of reading the clock — which is the one thing a chat header exists to get right, because the timestamps are what let the director audit the order work was created in. The file is append-only, so the header stands and a correction entry follows it naming the real times. No hash, threshold, ordering or approval changed.

## 7. Validation performed

- Draft 5's digest computed from disk before it was read.
- `source_count_granularity_probe.py` rerun in the venv against the pinned snapshot: byte-identical to the recorded output after normalizing the shell redirect's line endings. Snapshot digest still matches its pinned value; 2,183 rows; 37 insertions / 24 sessions / 12 subjects; CA1 at 4/4/4 with multiplicities `[6, 5, 3, 2]`; the full k=4 census including the 74 single-animal subsets.
- Amendment 6 points 1 and 4 re-read from `Claim Sheet.md` rather than from my continuity file. Change one came out of that reading.
- Both edit scripts asserted **exactly one match per replacement across the whole file before any write** — 7 replacements on the matching rule, 2 on the host document — and every changed section was re-read as a reviewer afterwards rather than trusted from the diff.
- Matching rule after edit: 6 fences balanced, zero curly quotes, zero replacement characters, no CRLF, no trailing whitespace.
- Host document after edit: 4 fences balanced, no CRLF, no trailing whitespace; the four curly quotes it contains were verified to be pre-existing in the approved region of Draft 7 and were left alone.
- Both chat appends verified by reading the file back: prior content is a byte-exact prefix, the new header occurs exactly once, the file ends with the new message.
- The selection-review transcript's first 107 lines are CRLF and the rest LF. Pre-existing, from the file's creation in Session 5; noted because my continuity file had claimed my own README was the project's only CRLF file.
- `git diff --check` clean.
- `.gitignore` reviewed: this session added only tracked Markdown and two scratchpad-only scripts that live outside the repository. No new ignore rule needed.

## 8. Machine state

Measured at 06:13 PDT, before any work that could have needed it:

- **RAM:** 7.02 GiB free of 31.67 (77% in use)
- **VRAM:** 1,029 MiB used of 16,311
- **`C:` free:** 648.0 GB

Nothing heavy ran and nothing was downloaded. The only execution was stdlib parsing, hashing, Markdown checks and a 66,045-element enumeration. The reading is recorded so the next session inherits evidence, not a hunch — and it takes its own.

## 9. Files created or updated

| Path | What changed |
|---|---|
| `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` | Draft 5 → Draft 6. Three reviewer changes; approved and handed back. |
| `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md` | Append-only Session 17 exact-state review and Draft 6 handoff. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 7 → Draft 8. New §15 (pinned candidate order) and §16 (drift quantity and threshold basis). |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only Session 17 handoff of Draft 8, plus a timestamp correction. |
| `README.md` | Two running-log entries: the unpinned candidate order, and the retired drift column with its replacement. |
| `agents/Claude/README.md` | Session 17 state. |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten for Session 18. |
| `agents/Claude/Session Summaries/HumanReport17.md` | This report. |

## 10. Next steps

1. **Codex owner-re-reviews Draft 6**, including whether Section 9's manifest boundary should bind all four steps or only the first.
2. **Codex reviews Draft 8's §15 and §16**, in particular the exhaustion rule, the pre-declared drift parameters, and the sorter-family residual in §16.6.
3. **I implement the drift estimator** — targeted range reads over the ragged per-unit slices for band units only, reusing the packet's remote-HDF5 and anatomy utilities — after §16 is approved, and confirm first that the ragged index resolves as expected on these assets and that the depth column is present and finite on every candidate.
4. **Then the drift gate runs down the pinned order**, first-admissible, and the noise and effective-SNR gates follow it.
5. Codex continues the exposure-schedule/placement specification and the footprint/placement calibration in his lane.

Nothing is blocked on the director. The Phase 1 Claim Sheet review request remains open and non-blocking.

## 11. Decisions and the reasoning behind them

**Not choosing between the two placement readings.** I could have picked one and written it into Draft 6. I did not, because the choice determines how often a candidate recording dies and it belongs to the person writing the placement rule. A reviewer who resolves an ambiguity in the owner's favour is still taking the decision.

**Extending the manifest boundary to all four steps.** This is the one edit that tightens rather than clarifies, and I made it only after establishing that it cannot make anything infeasible — every step is synthetic pre-host work. I said so explicitly and offered to approve the narrower version, because a tightening inside someone else's artifact without that argument is a decision taken from them.

**Pinning the tail of the candidate order mechanically rather than by judgement.** A judgement-based tail would have reintroduced exactly the freedom §15 exists to remove. The cost is that ranks 4 and 5 look out of place next to rank 3, which is a cost worth paying and is explained in the section.

**Setting the drift threshold from probe geometry rather than from anything measurable about the candidates.** Twenty micrometres is one contact row. It is not a number the data suggested, because no data has been read. The single pre-declared relaxation exists so that a failure to find any passing host produces a recorded relaxation rather than a negotiation.

**Declaring an unmeasurable host a failure rather than a pass.** The safe direction here is the pessimistic one, and choosing it deliberately is different from arriving at it by accident.
