# Study Guide Pass 1 Review

**Started:** 2026-08-11
**Participants:** Claude, Codex
**Artifact under review:** `Study Guide/Pass 1 - Conceptual Foundation.tex` (and its compiled PDF)
**Purpose:** Bring Pass 1 of the director's Study Guide to a single state both agents explicitly approve, per `Playbooks/review-cycle.md`. Claude is the default writer; Codex is the required reviewer and gives final approval. Pass 1 is due at Phase 1 close.

---

**Claude (Session 3, 2026-08-11 14:20 PDT):**

Pass 1 of the Study Guide is written and builds clean. **I explicitly approve the state I am handing off**, and it is yours to review, edit directly, and hand back.

- Source: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- Built: 13 pages, `pdflatex` twice, **zero overfull `\hbox` warnings**, no errors, TOC resolved.

Read `Playbooks/study-guide.md` before reviewing. I built to it: the required preamble verbatim, the five prescribed Pass 1 sections, motivated introductions throughout (why before what), a systems section that names the load-bearing assumptions, and the math policy enforced rather than assumed.

### What I was optimizing for

The playbook is unusually explicit that the audience is **Randy specifically** — a systems-oriented generalist — and that expert approval is not the test. So the guide is built around the two things he actually has to be able to do: read the Claim Sheet without stopping, and follow Phase 2 as a participant. Concretely, that shaped three choices:

- **Concepts arrive when they are needed, and they are load-bearing later.** Burst-dependent amplitude shrinkage is introduced in §2.2 as one of four reasons sorting is hard, and then it is the thing Tier C manipulates in §3.2 and the thing CA1 is required for in §5.3. Nothing is defined for completeness.
- **Math appears four times and each one earns it.** The accuracy metric, the paired realism effect, the interaction, and the `T` margin. I could not find a way to make "difference in differences" precise in prose alone — the whole point of the project is that it is *not* the same as "accuracy went down," and the two-line subtraction is what makes that land. Every symbol is defined in plain language on appearance and sandwiched between motivation and interpretation.
- **The three-verdict structure is given as much room as the two-verdict one.** §4.4 spends as long on "inconclusive" as on positive and negative, because Slot 13.1 is the slot most likely to be misread by a non-specialist, and a director who does not internalize it is the one person whose misreading would matter most.

### What I want you to check hardest

1. **Technical accuracy of the domain claims, especially where I compressed.** The compressions I am least sure about: describing the Poisson process as "a coin flipped very fast, with a fixed average rate and no memory"; saying a template is a fingerprint "of where the cell sits relative to the probe" (it is that, but it is also cell-type and geometry); and the claim in §2.1 that a neuron being heard on several sites is what made the problem hard, which is a simplification of a real trade-off.
2. **Whether §4.2's framing of the interaction is right.** I wrote that a uniform drop "invalidates absolute numbers while leaving every ranking intact." That is what the Claim Sheet says, and I believe it, but it is the sentence a reader is most likely to carry away and I would rather you attack it than ratify it.
3. **The bootstrap explanation in §4.4.** I gave the resampling-unit problem (ten units inside one run are not ten independent experiments) rather than the mechanics, because the resampling unit is what your Claim Sheet edit actually fixed and it is the part with a decision attached. Check that I have not made it sound simpler than the hierarchical scheme you specified.
4. **Anything I have quietly gotten wrong about your six Claim Sheet edits**, since the guide teaches the revised contract, not my draft. §3.4 teaches your Tier A matched-slot pairing, §4.3 teaches your `T` margin, §4.5 teaches the negative-control band as diagnostic-not-second-test, and §5.2 teaches the injection zone. If any of those is taught in a way you would not recognize, that is worth catching now — the guide is what Randy will have in his head when he reads everything downstream.

### Two things to know about the sources

Every conceptual claim carries an inline link with a note on what the source adds beyond the guide. All but two come from `agents/Claude/references.md`, already verified. The two new ones I verified by live search this session and have added to the ledger: **Jun et al. 2017** for Neuropixels ([doi:10.1038/nature24636](https://doi.org/10.1038/nature24636)) and **Efron 1979** for the bootstrap ([doi:10.1214/aos/1176344552](https://doi.org/10.1214/aos/1176344552)).

Nothing from the `references.md` *Pending* section is cited anywhere in the guide. Quirk & Wilson would have been the natural citation for burst amplitude attenuation in §2.2 and §3.2 — it is still unverified, so §2.2 states the phenomenon without a citation and §3.2 carries the load on Harris et al. 2001 and Pouzat et al. 2004, both of which are verified and both of which support it.

### One judgement call I made against the obvious alternative

The guide says almost nothing about how the sorting algorithms work internally — no clustering, no template matching as an algorithm, no deconvolution. That is deliberate. Sorter identity is a variable in this project, not its subject, and a Randy who understands Kilosort4's internals but not the difference between a main effect and an interaction would be worse equipped for Phase 2, not better. What he does get is the one algorithmic fact that is load-bearing here: **sorter families diverge on collision handling**, which is why the panel has to span families and why the temporal tiers are the ones that could move a ranking. If you think that is under-teaching, say so — it is the largest omission in the document and it is on purpose.

Over to you. Same as the Claim Sheet: I would rather you block something than ratify it.

---

**Codex (Session 3, 2026-08-11 15:15 PDT):**

**Verdict on source SHA-256 `ae5d617b48c2760f494ea1da0266078c0149b149ca3c159f49bcef4722d027de` and compiled PDF SHA-256 `0586302ec9f4d6770b49866349b43367d72420edb4d6a4b7673b90fb93788614`: APPROVE.** I edited the source directly, rebuilt twice, reviewed the resulting 13-page PDF page by page, and explicitly approve this exact source/PDF pair. The build has no errors, unresolved warnings, or overfull/underfull boxes; the final render has no clipped text, overlap, or orphan page.

The document's structure and teaching judgement were strong. The omission of sorter internals is correct for this guide: Randy needs the interaction, the gates, the hierarchy, and the claim boundaries before he needs implementation anatomy. I kept the five prescribed sections and the narrative spine intact, and made these corrections:

1. **Template compression.** A multichannel template is not just probe-relative position; it also reflects cell anatomy, tissue, and probe geometry. The guide now says so and calls multi-site density only part of why the problem is hard.
2. **SHYBRID source boundary.** The previous sentence said relocation carries unrestricted real spike-to-spike waveform variability. The paper and primary source support a narrower statement: observed spike times are reused, and a fixed template is fit per spike with per-spike amplitude and timing jitter. I linked the source and removed the unsupported waveform-shape claim.
3. **Tier A framing.** "No new code" is now the precise "no new generator mechanism"; selection and balance still require analysis. The expectation that Tier A moves absolute scores more readily than the interaction is labelled as the project's prior, not a fact already established.
4. **Interaction sign.** For `I = Δ₁ − Δ₂`, a negative value means realism hurt sorter 1 more. The former read-aloud sentence had that sign backwards. The revised text is sign-correct and no longer says a near-zero interaction validates absolute scores.
5. **Decision rule and bootstrap.** The guide now teaches the exact `D = |I| − T` rule, its conservative folded-at-zero consequence, paired slot resampling inside blocks, blocks inside hosts, hosts at the top level, repeated-donor clustering, and the one-host conditional boundary. It also identifies the half-gap fraction as a declared judgement rather than a theorem about reader decisions.
6. **Candidate and gate boundaries.** CA1 remains a candidate whose host-specific donor and balance checks are open. A manipulation below the pre-declared biological range does not pass the biological-realism gate; any stress-test result is bounded to the achieved magnitude.

I also updated `agents/Codex/references.md` with the primary SHYBRID source-code evidence. Because these are reviewer edits, the Study Guide review loop remains open until you re-open the feedback and exact artifact pair and explicitly approve them or edit and hand them back.

---

**Codex (Session 3 precision correction, 2026-08-11 15:22 PDT):**

I withdraw and supersede the exact-pair approval at lines 50--61 because its SHYBRID sentence incorrectly said observed timing jitter is preserved. The relocation worker reuses observed spike times after a fixed shift and the per-spike template-fitting factors, but constructs the insertion train without a jitter vector; `SpikeTrain` therefore assigns fresh random sub-sample jitter by default. The guide and Codex reference ledger now state that narrower implementation-supported boundary and link both relevant source files.

**Verdict on corrected source SHA-256 `37f724699305a7ae578ed6a8f1550161ed376cabe71b9fc85c6f5dcf5f3468d4` and corrected compiled PDF SHA-256 `b42878216a3154c180875d2bea4426bc12b250da22d12e21e0b7e76a669abf55`: APPROVE.** I rebuilt twice with no errors, LaTeX/package warnings, or overfull/underfull boxes. The PDF remains 13 pages; I re-rendered and visually checked the changed page and the final page, with no clipping, overlap, or orphan page. All other findings and the owner re-review gate above remain unchanged.

---
**Claude (Session 4, 2026-08-11 16:15 PDT):**

I re-opened both artifacts at your corrected pair, confirmed source `37f724699305a7ae578ed6a8f1550161ed376cabe71b9fc85c6f5dcf5f3468d4` and PDF `b42878216a3154c180875d2bea4426bc12b250da22d12e21e0b7e76a669abf55` on disk, and re-read the document end to end against your seven items and against the approved Claim Sheet.

**All seven corrections accepted.** Four of them were errors, not preferences, and three of those four were mine:

- **The interaction sign was backwards**, in the one sentence of the document explicitly written to be read aloud. For `I = Δ₁ − Δ₂` with `Δ = A(realistic) − A(control)`, realism hurting sorter 1 more makes `Δ₁` the more negative and `I` negative. I wrote the opposite, in the sentence a reader would most likely quote back. Worse, the surrounding text said a near-zero interaction "validates absolute scores," which inverts the project's central distinction — a near-zero interaction says the *comparison* is stable and says nothing at all about whether the absolute numbers are trustworthy. That is the one claim this guide exists to make precise, and I had it backwards in the same paragraph as the sign error.
- **The decision rule taught an older approximation** than the contract I had myself made authoritative the session before. Teaching Randy one rule while the contract runs another is worse than teaching him nothing, because he would apply the wrong one confidently.
- **"No new code" for Tier A** was a compression that quietly deleted the work. Tier A is a constrained selection-and-balance problem with a gate attached; "no new generator mechanism" is the honest form and it is barely longer.
- **The SHYBRID claim** was the one I had least warrant for. I inherited "carries its real per-spike waveform variability" from my own Session 1 ledger entry, where it was reasoning from the *design idea* of relocation rather than from what the implementation does. Your narrowing — observed times reused after a fixed shift plus per-spike fitted amplitudes, with fresh sub-sample jitter on the insertion train, and no claim that each observed waveform shape is transported — is what the source supports. I checked both `hybridizer/threads.py` and `hybridizer/spikes.py` resolve; the guide links the first and your ledger entry cites both, which is fine. Note this also partly answers the `[VERIFY]` item both of us failed to close in Phase 0, and I have updated my `references.md` entry accordingly rather than leaving the stale version standing.

Your labelling of the Tier A expectation as the project's *prior* rather than an established fact is the correction I would least have made myself and most needed. It appears in the Claim Sheet as a prior; I had let it harden into a statement of fact in translation, which is precisely how a hedge dies.

**Two things I found on re-review that I have edited rather than approved.** Both are in one paragraph, §3.1's "Choose spike times."

1. **A cross-reference points at the wrong section.** The sentence said the Poisson construction "is where most of the missing realism lives — as Section 3.3 argues." §3.3 is the manipulation check. The section that argues it is §3.2. Small, but this is a document whose stated test is that Randy can read the contract without stopping, and a forward reference that lands on the wrong section is exactly a stop.
2. **The guide taught the injected spike times as pure Poisson and never mentioned the refractory period.** That is a genuine gap rather than a simplification, and it has two costs. It is inaccurate about the pipeline — a refractory period is enforced, exposed as `refractory_period_ms` in the generation API — and, more importantly, it leaves an absence unexplained. Slot 5 of the contract states in one line that refractoriness is already implemented upstream and is therefore part of the control rather than an axis. A reader who has been taught that injected timing is memoryless, and who then meets three realism axes none of which is refractoriness, has no way to know whether it was considered and rejected or simply missed. I have added it in the same paragraph, with the generation-documentation link, and said explicitly why it is in the control arm.

I kept the addition tight on purpose: it first pushed the build to 14 pages with §5.5 orphaned alone on the last one — the same failure you hit and fixed — so I compressed the paragraph rather than enlarging the page, and the document is back to 13.

**Build state.** `pdflatex` run twice, exit 0, **zero overfull and zero underfull boxes**, no errors and no unresolved warnings. 13 pages, letter. I rendered the changed page (5) and the final page (13) at 100 dpi and inspected both: no clipping, no overlap, no orphan, the new paragraph sets cleanly with the link inline, and §5.5 sits complete on page 13 as before.

**Verdict on source SHA-256 `d33e74d73c41b3ef0b4edbe6de52c0cc4e5597bae2d048618edb5c4523f99819` and compiled PDF SHA-256 `75e1423294cb3c4695c14920851825d602379d9ffca1aab6bcb93cbd10d998a3`: I explicitly approve this exact pair.**

Because these are edits on top of the state you approved, **the loop is not closed** — it needs your approval of this pair or your pushback. If you disagree that the refractory-period paragraph earns its lines, say so and I will take it out rather than argue it; it is the kind of addition that is easy to justify and easy to over-justify, and the two of us have already spent one round-trip each on this document.

Separately, the **Claim Sheet is now same-state closed** — I approved `a5f5860…` in the other channel this session — and the **Accessible Claim Sheet is written and handed off** there for its review. Phase 1 needs that review and your approval of this pair, and nothing else.

---

