# Human Report 18 — Claude

**Date and time:** 2026-08-13 08:22 PDT
**Phase:** 2 — Execution
**Session type:** Owner re-review of a reviewed artifact, then implementation of the specification it settles.

---

## What this session was

Two pieces of work, in the order they had to happen.

**First, the owner re-review that closes a review cycle.** Codex reviewed my Session 17 draft of the host-selection document, accepted its candidate order, repaired five things in its drift specification, and handed the document back as Draft 9. The review cycle only closes when both agents have explicitly approved the *same* bytes, and that requires the owner to genuinely re-open the artifact rather than accept the handoff on trust. I did that, accepted all five repairs, verified the two constants Codex's edits introduced by re-deriving them rather than reading them, added two things, and handed back Draft 10.

**Second, the implementation of the thing the specification specifies.** The drift estimator now exists, is tested, and passes 53 synthetic checks at the exact permutation count the gate is pinned to. **It has not been pointed at a single real recording**, and it will not be until Codex confirms Draft 10.

**No host is pinned, no candidate has been measured on any open gate, no donor is selected, no generator or sorter has run, and no scientific result exists.**

---

## Part one: the review

### What Codex found, and the one that matters

The specification defines a drift measurement and then a rule that decides, from that measurement, whether a candidate recording is admissible. The measurement survived review nearly intact. The decision rule did not, and the central defect is worth stating plainly because it was mine.

The estimator carries a *null* — a version of the same computation run on the same recording with the time ordering destroyed, which answers the question "what does this estimator return here when nothing moves?" That is a good construction and Codex kept it. My decision rule then said: if the observed value sits inside its own null, the host is rejected as unmeasurable.

**That inverts the best possible outcome.** A recording that genuinely does not drift, measured by an estimator sharp enough to say so, will land inside its null — that is what "no drift" looks like. My rule made the cleanest available result the one outcome that could not pass. The quantity that separates "quiet" from "cannot tell" was in my hands the whole time and I did not use it: it is the threshold. A small excursion inside a *tight* null is a quiet host; the same excursion inside a null wider than the tolerance is a host we cannot speak about at the resolution the gate is written in.

Codex's replacement requires **both** the observed worst-window excursion **and** the null's declared 95th percentile to sit at or below the tolerance. Lying inside the null is explicitly not a failure. That is correct and I approved it unchanged.

### The check I ran on the repair, and why it is worth recording

This project has a standing rule that a tightening made inside someone else's artifact owes a "this cannot make anything infeasible" argument. Codex's repair is not a tightening, but I worked out whether it could be one, because the argument is cheap and the answer turned out to be clean:

**The new rule is never stricter than the one it replaces.** If a candidate passed under my Draft 8 — excursion at or below the tolerance, and outside its null, which can only mean the excursion exceeded the null's summary — then the null's summary was below the excursion, which was below the tolerance, so the new rule passes it too. The set of admissible candidates strictly grows, by exactly the quiet hosts my rule inverted. It is a repair that cannot cost a host, and that is a stronger statement than "it looks better."

### The other four repairs, all accepted

- **The statistic is a peak-to-peak excursion, not a net displacement.** I labelled `max − min` a displacement in the same section that argued a path-length measure is the wrong functional. Codex renamed it. I verified the rename is complete — no occurrence of the old name survives anywhere in the file.
- **The geometric justification of the 20 µm threshold was too strong.** I had written that motion below one contact-row pitch is "below the spatial resolution at which the probe records at all." That is not true of a continuously varying waveform sampled at 20 µm rows. What survives is what the threshold actually is: a one-row tolerance chosen before any candidate was seen, on a scale that does not depend on the candidate. That is enough, and it is all we can claim.
- **The Kilosort-family conditioning lands harder than I wrote it.** I had reduced the residual risk to a constant per-sorter offset and then shown where a constant cancels — which assumed the thing at issue. A host feature can *moderate* a sorter-by-realism effect, not merely shift each sorter's level, and a moderator does not cancel from the study's primary comparison. This was the one judgement in the section I had flagged as least certain and explicitly asked Codex to push on. It pushed, and it was right.
- **The relaxation ladder needed to be a whole-pass rule.** My draft said the threshold relaxes once from 20 µm to 40 µm if nothing passes, which left it ambiguous whether the relaxation applied to the whole candidate order or to whichever candidate happened to be in hand when the list ran out. The second reading is a relaxation aimed at one candidate, which is exactly what a pre-declared ladder exists to prevent. Codex's version runs the entire pinned order at 20 µm and only then restarts the same order at 40 µm.

### The two constants I re-derived rather than read

Codex's edits introduced two values that other things now depend on. Both reproduce:

- The permutation master seed `3175830281` is claimed to be the first eight hexadecimal digits of the SHA-256 of a specific string. Computed: `bd4b5309074646d5…`, and `0xbd4b5309 = 3175830281`. It derives from its stated input.
- The exhaustion rule now binds the continuation order to a tracked asset-listing file at a stated SHA-256. The file is on disk at exactly that digest, 734,388 bytes, 2,048 assets. **I also checked what 2,048 means**, because a round power of two is the shape of a page cap rather than a total — reading the listing utility shows it follows the archive's pagination until exhausted, so the file is a complete listing of the dataset as of 2026-08-11 and not a truncation. That matters: binding the continuation to those bytes closes the candidate universe at a reproducible snapshot, which is stronger than what my draft said.

### One probe I ran on a tightening Codex *did* make, and what I did instead of arguing

Codex changed bin validity from a per-bin criterion to "every complete bin must be valid, or the candidate is unmeasurable." That one genuinely can reject a candidate my draft would have measured, and the two criteria are not jointly guaranteed: a unit is allowed to be absent from up to 20% of bins and still count as included, so five included units whose gaps happen to align leave a bin short and the candidate dies on alignment rather than on drift.

I did not ask for it to be loosened. A hole inside a ten-bin window can hide that window's maximum, which is a *silent* failure; a rejection is a loud one, and loud is the safe direction for a gate. The cost is bounded by thirteen candidates plus a defined continuation.

What it needs is that a rejection says which cause it had, so **I took that on as an implementation obligation rather than a specification change**: the estimator reports the per-bin included-unit count and its minimum across bins, and a bin-validity rejection names the offending bins and how many units each held. That is now tested.

Worth noting in the same breath: Codex's revised null holds every spike time fixed and permutes depth values, which preserves each unit's per-bin spike counts exactly — so bin validity is identical under permutation and observation, and no replicate can be invalid where the observation is valid. My own formulation re-assigned spikes to bins while claiming to preserve counts, which is two descriptions of two different objects in one sentence. That is the second time this week I have written that particular defect, once in Codex's document and once in my own.

### What Draft 10 adds

Nothing that changes a parameter, threshold, order, verdict or rule. Two additions:

**1. Which way the null's own residual bias points (§16.5).** The permuted values are the recording's real depths, so if the band genuinely moves, that movement is inside the pool the null draws from, and the null's summary is an *inflated* estimate of a no-drift noise floor rather than a clean one. The inflation reaches the statistic only through each unit's pooled depth spread divided by the square root of its per-bin spike count, so it is second order wherever bins are well populated — but the direction matters more than the size, and it is safe in both places it acts. A wider null can only push a candidate toward an unmeasurable rejection and never toward a pass, because the observed value never touches the null; and it can only push a failing candidate's label from *resolved drift* toward *noise-limited*, never the reverse. So the null summary reads as an upper bound on the noise floor rather than an estimate of it. I state explicitly that this is not a reason to correct it: removing drift from the values before building the null against which drift is judged would be circular. **The implementation then measured this claim rather than leaving it as an argument** — see below.

**2. A status sentence replaced by the rule it was standing in for (§16.8).** The section closed with "the parameters above are a proposal until Codex has reviewed them." That is a sentence which goes stale the moment Codex reviews them, and it goes stale in the *permissive* direction: a later session reads "proposal" and treats pre-declared parameters as adjustable, which is the exact failure the section exists to prevent. The neighbouring section already had the right shape — "the order binds from the moment both agents have approved this state" — so the drift parameters now say the same thing, keep the existing rule for changing them afterwards, and name the 20 µm to 40 µm ladder as the only change to the threshold that is already authorized.

---

## Part two: the implementation

### What was built

`Reproducibility Packet/scripts/utils/band_drift.py` implements the specification and nothing else: the per-unit per-bin median depths, the centring, the across-unit band trace, the whole-recording and worst-window peak-to-peak excursions, the deterministic within-unit permutation null with its nearest-rank 95th-percentile summary, and the two-number pass rule.

`agents/Claude/tools/test_band_drift.py` is its test battery. **53 checks, 0 failed**, run at the pinned 200 permutations rather than at a faster number, so what is tested is what will run.

### Why the tests are the interesting part

Every input is synthetic and constructed so the right answer is known before the test runs:

- **A ramp of a stated size** is recovered at both scales — a 60 µm linear drift returns 58.76 µm whole-recording against 59.02 µm expected, and 9.45 µm in-window against 8.85 µm expected.
- **A trajectory that goes away and comes back** returns to within 0.33 µm of where it started and reports 44.13 µm of its 45 µm excursion. This is the property the rename protects: a net-displacement statistic would have scored this recording as clean.
- **A trace whose worst window is deliberately not its first** is found correctly, so the gate takes the worst window rather than a convenient one.
- **A band deliberately left one unit short during a single minute** is refused as unmeasurable, names bin 20, and reports that it held four units against the required five.
- **Malformed input raises rather than returning a verdict.** A non-finite depth or a mismatched array length is a bug, not an unmeasurable candidate, and the two must not be confused.

**Three of the cases exist specifically because review caught the corresponding defects**, and those are the ones most worth keeping: a flat band passes the 20 µm gate and is labelled *no time-ordered drift resolved* (observed 1.24 µm against a null bound of 1.81 µm — exactly the inside-null case my draft would have rejected); a down-and-back trajectory reports its excursion; an invalid bin rejects and names itself. A future session cannot quietly restore any of the three without something going red.

### The claim I added to the specification, then measured

The null-inflation direction is not left as an argument. The harness builds two bands identical in every respect except that one carries a 240 µm ramp, and compares their nulls: quiet 1.73 µm, drifting 9.30 µm. Real movement does widen a candidate's own null, as claimed — and the drifting band still fails on its excursion (36.80 µm) rather than on its resolution, which is the direction the paragraph says it should.

### One reading of the specification the code forced into the open

The specification says to permute "that unit's depth-value indices." I implemented the pool as the unit's **full loaded depth array**, which includes any spikes falling in the discarded final partial bin — so a depth belonging to a partial-bin spike can land in a complete bin under permutation. That is the literal reading. The alternative, restricting the pool to spikes inside complete bins, is defensible and is a one-line change. The partial bin is under 60 seconds of a 54-to-87-minute recording, so I expect no practical difference, but **I would rather have the choice named than have it be an accident of implementation**, so it is in the module's docstring and it has been handed to Codex to confirm or change.

### Where it lives, and why not in the packet's runbook yet

The module is inside the Reproducibility Packet, in `scripts/utils/`, because shared computation belongs there under the project's own software standard and because a reader who copies the packet gets it. It is deliberately **not** a numbered runbook step yet. The packet's consistency checker requires every runnable script to have exactly one numbered step, and a numbered step is a promise that the command was run. The archive-reading command that becomes step 11 cannot be run until Codex confirms Draft 10, and five of the ten existing steps already carry an honest "not re-run" caveat. Adding a sixth to save a session would be the wrong trade. The checker still passes at ten steps, verified after the addition.

---

## Part three: a defect found on the way out, in the claim this repository rests on

The session's work was committed and pushed before this turned up, which is worth saying plainly because it is why it appears here rather than woven into the account above.

**What it is.** This repository has no `.gitattributes`, and git on this machine is configured to convert line endings on checkout. **The bytes a reader gets from `git clone` are therefore not the bytes we tested.**

I did not reason about how much that matters; I cloned the repository to a short local path and compared every packet file against its working-tree twin. **Thirty of forty-two differ after a clone.** Two of those matter:

- **The pinned upstream input** — the frozen copy of the waveform library's metadata, whose entire purpose is to be byte-identical to what was downloaded on 2026-08-11 — is 2,032,640 bytes here and 2,040,518 bytes after a clone. Three of the packet's steps read it, and its published checksum does not survive the trip.
- **One of the five steps the packet claims reproduces byte for byte offline** has recorded outputs in the group that changes. A reader on Windows who clones this repository and runs that step would find the comparison failing, through no fault of their own.

**Why the earlier validation missed it.** The self-containment test copied the packet folder to an isolated location, which preserves bytes exactly. A reader does not copy the folder; they clone the repository, and a clone is a different operation. The test was correct about what it tested, and the claim it was taken to support is wider than what it tested. The project already had the lesson in a narrower form — a runbook you have not executed is a guess — and this is the same thing one level up: **a distribution path you have not exercised is a guess.**

**The scope, stated honestly.** On Linux and macOS the conversion is normally off, so a clone there yields the committed bytes and the problem does not arise. It affects Windows readers specifically. It affects nothing either agent has measured or approved: every checksum the two agents have exchanged is a working-tree checksum in this one clone, and all of them are still correct.

**What I did about it, and what I deliberately did not.** I did not fix it. The fix is a one-line repository-wide file that changes what every future checkout produces, in a repository whose packet is co-owned and whose review is concluded — that belongs in a review, not in a session's closing minutes. So it is measured, written up in full in the agents' review channel with the proposed fix and the verification procedure attached, and recorded in the continuity file so it cannot quietly drop. The proposed fix is chosen for a specific property: it changes nothing in the current working tree, so no already-published checksum is invalidated by fixing it.

**Nothing about the drift work or any approved state changes because of this.**

---

## Challenges, and how they were handled

**The temptation in an owner re-review is to accept everything.** The reviewer has done real work, the edits look better than what they replaced, and agreeing is faster than checking. The discipline this project uses is to ask, for each edit, what failure the original construction was pointed at and whether the replacement still points at it. Applying that produced the monotonicity argument for the pass rule, the completeness check on the rename, and the pagination check on the asset listing — none of which I would have run if I had accepted the handoff on trust.

**Three of my tests failed on the first run, and all three were the tests.** One expected the wrong bin boundary because I had miscounted which bins a three-bin partition contains; one asserted a consequence of that same miscount; and one built a drift fixture too small to exceed the threshold it was asserting the candidate would exceed (a 240 µm ramp over an hour produces only about 19 µm inside a ten-minute window, which is below the 20 µm gate — the fixture was wrong, not the estimator). The project's rule here is to ask whether the test or the artifact is broken before changing either. In all three cases the artifact was right.

**The status-sentence defect nearly went unnoticed**, because it reads as harmless prose at the end of a section. It is not: it is a sentence that says pre-declared parameters are provisional, sitting inside the section whose entire purpose is that they are not.

---

## Files created or updated

| Path | What changed |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 9 → Draft 10**, SHA-256 `72fd3490ff4762a5336eb7ef9e5756d05a0dd8f00cb0a2189d9d21c717a3a5a9`. Owner re-review complete; §16.5 gains the null-bias-direction paragraph, §16.8's closing status sentence becomes the binding rule, status line rewritten. Open on Codex. |
| `Reproducibility Packet/scripts/utils/band_drift.py` | **New**, SHA-256 `9e7d691b5e5557bb49336f6518a32b8d981cc71f8641904eed55ca20da5875d0`. The §16 estimator, its deterministic null and its two-number gate. |
| `agents/Claude/tools/test_band_drift.py` | **New**, SHA-256 `d553dcea113777682607920eb70bcbe9c7d2b975f5791b859022dfb8d8343f71`. 53 synthetic checks, 0 failing, at the pinned 200 permutations. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Two appended messages: the owner re-review and Draft 10 handoff, and the implementation report. |
| `README.md` (repository root) | One running-log entry. Banner already carried today's date. |
| `agents/Claude/README.md` | Folder tree, the `tools/` description, the packet `utils/` rows, the selection-document row, and two chat rows that had gone stale since Session 11. |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten for Session 19, then extended with the clone-versus-copy finding. |

---

## Machine state

Measured at 08:12 PDT, before any work: **RAM 5.91 GiB free of 31.67 (81% in use); VRAM 1,031 MiB used of 16,311; 647.9 GB free on `C:`.** Nothing heavy ran and nothing was downloaded. The heaviest computation this session was a 3.4-second NumPy loop over synthetic arrays — the full 200-permutation null on a 14-unit, 61-bin band. That number is worth recording for a different reason than resource safety: it means the pinned permutation count costs nothing worth optimizing, and the parameter never has to be defended on runtime grounds.

---

## Next steps

1. **Codex confirms Draft 10** — one added paragraph and one rewritten sentence against the state it already approved. Until then, no candidate may be measured.
2. **Then the archive-reading script**, which becomes the packet's step 11: targeted range reads over the ragged per-spike time and depth arrays for band units only. Two things it must confirm before it computes anything, both cheap and both still unverified — that the ragged index resolves per-unit slices as expected on these specific assets, and that the depth column is present and finite on every candidate.
3. **Then the drift gate runs down the pinned candidate order**, rank 1 first, at 20 µm.
4. **The capacity gate still needs re-establishing** under the stricter condition the sixth contract amendment imposes — every block's ten scheduled donors must admit a jointly feasible ten-placement assignment. That belongs in a future section and does not reopen anything already approved.
5. **Five of the packet's ten steps still have not been re-run.** The drift work reads the same archive and is the natural place to fold them in.
6. **The clone-versus-copy defect above needs a decision from the other agent**, and then a one-line file plus a file-by-file verification that a fresh checkout reproduces the working tree.
