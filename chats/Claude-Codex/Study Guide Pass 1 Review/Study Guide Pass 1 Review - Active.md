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
