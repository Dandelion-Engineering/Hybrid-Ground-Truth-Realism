# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 17 · 2026-08-13 06:22 PDT**
**Next session is Claude Session 18. No count-based progress report is due** (next is Session 24). A phase transition or an approved amendment written in your session still triggers one.

You start with no memory of the last session. This file restores the state and nothing else. It omits anything already in `Project Details/Project Details.md`, the `Playbooks/`, or `AgentPrompt.md` — you re-read those anyway.

**Read `Claim Sheet.md` before doing any work**, including `## Amendments`. **All six amendments are `In force` and govern.** `Accessible Claim Sheet.md` is the same content in plain language and carries the same six.

**⚠️ This file describes the moment it was written.** Twice now Codex has posted a handoff within the hour after a session closed. **Read both active chats before you act on §2.**

---

## 1. Where the project is

**Phase 2 — Execution. No scientific result exists, no sorter has run, no host is pinned, no donor is selected, and nothing beyond bounded metadata reads has been downloaded.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. |
| `Accessible Claim Sheet.md` | Synchronized, same six. Whole-file `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 8, `b104f66596f6a48ad86d5d029ea7be3c437ebbd7b8e83a9d9ea42b748cc4fbef`.** §1–§12 approved by both; §13–§14 owner-approved awaiting Codex; **§15–§16 new in Session 17 and handed to Codex.** Open on Codex. |
| `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` | **Draft 6, `51adae4bd19ffc2ef72445e474371b56eee04d93883c6da1d59fedbca553f282` — you approved it and handed it back. Open on Codex.** |
| `Reproducibility Packet/` | Eleven scripts, `DATA.md`, pinned deps, its own `.gitignore`. All same-state approved; its review chat is concluded. |

## 2. The first thing to do next session

**Check both active chats before assuming anything.** As of writing, **both** artifacts are open on Codex and nothing is open on you.

- `chats/Claude-Codex/Tier A Donor Matching Rule/` — **open on Codex:** Draft 6's exact bytes, plus whether Section 9's manifest boundary should bind all four steps or only step 1 (§3.3).
- `chats/Claude-Codex/Tier A Selection Review/` — **open on Codex:** Draft 8's §15 and §16.
- `chats/Claude-Codex/Reproducibility Packet Review/` — **concluded.** Later packet additions start a new scoped chat.

**If nothing has come back, your lane is the drift estimator implementation (§6.2), which §16 has to be approved before you run against a candidate.** You may write and test it against synthetic inputs meanwhile; you may not measure a candidate until Codex has approved §16's parameters.

## 3. What Session 17 did

Exact-state review of Codex's Draft 5 → **Draft 6, approved and handed back**; and two new sections on your own document → **Draft 8**.

### 3.1 The review: every Draft 5 decision accepted, three changes made

Codex replaced your Draft 4 nuisance-seed repair with something stronger — a **separate exposure-schedule and placement specification** that must be approved before T is measured and before any manifest, pool, or edge table exists. He was right that Draft 4 pinned the word and left the draws selectable. He also caught an input you missed: **the amplitude target is part of the schedule** and the matched quantities are realized at it.

### 3.2 The finding: two sentences describing two different objects

Draft 5's specification list asked for "the mapping from a placement seed and the pinned candidate-site set to **one commanded placement**." Two paragraphs later, every block's ten targets "must **admit** a jointly feasible ten-placement assignment." Those are different objects and the document never said which one the renderer uses.

**The tension is in the contract, not in Codex's prose.** Amendment 6 point 4 leaves placement seeds "randomized exactly as before"; Amendment 6 point 1 requires the joint-feasibility admission and rejects the host on failure. Per-occurrence draws make joint feasibility a property of the *draw* (hosts die often); a block-joint derivation makes the *search* the thing that has to be pinned, since a re-runnable search is a redraw wearing another name.

**Draft 6 requires the specification to name which, and does not choose.** That is Codex's lane and his next declared step.

### 3.3 The tightening, flagged as one

Section 9's operative sentence dropped the target-eligibility manifest from its precondition list while Section 2.2, the Status line, and Section 10 all include it — so read literally it permitted building the manifest before the specification existed. Aligned, **and extended from step 1 to all four steps**: the manifest is where `N`, `S_T`, `E_T` and `B_T` first become visible, and those decide which stage and level bind. **No feasibility cost — every step is synthetic pre-host work.** You offered to approve a narrowing back to step 1 if Codex prefers.

### 3.4 §15 — the candidate order, pinned

Reviewing the host-rejection semantics made visible that **"first-admissible" was not a rule**: "first" is a property of a sequence and the sequence was labelled a *recommendation* in §10.6. A rejected host brings a new `T`, a new schedule and a new balance report, so an unpinned order is compatible with working down the list until one reads well.

**All thirteen are now pinned**, before any remaining gate has run on any candidate. Ranks 1–3 are §10.6's three in its order; ranks 4–13 are the §4.2 table by descending CA1 channel count, ties by ascending `(subject, session, probe)`. **Exhaustion is pinned too:** resume the survey from its recorded index and append new candidates in **discovery order**, never re-sorted, because by then the gates' behaviour is known. **Gate order pinned** (cheapest first; it cannot change a verdict, only cost): drift → noise → effective SNR → joint ten-placement → Codex's balance gate.

### 3.5 §16 — the drift quantity, defined before measuring

**`cumulative_drift_um_per_hour` is retired on its own description**: a path length, scaling with spike count at ~0.79, and "NOT actual electrode displacement" in IBL's own words. The count scaling is specifically disqualifying because Tier B's manipulation *is* population-rate coupling.

**The replacement:** 60 s bins → per-unit per-bin **median** of `spike_distances_from_probe_tip_um` → centre each unit on its own across-bin median → band trace is the **median across units** → report `Delta_net` (whole recording) and **`Delta_10`, the worst ten-minute window, which gates.** Worst window, not chosen window, so the segment cannot be picked after the trace is visible.

**Noise separation:** a **within-recording permutation null** — re-assign each unit's spikes to bins at random within that unit, preserving depths and counts, destroying time order. Observed inside its own null ⇒ **unresolvable, not quiet, and the host fails.** It does **not** bound systematic bias in IBL's depth estimator and does not separate probe from tissue movement; both stated.

**Threshold `Delta_10 ≤ 20 µm`** (one NP1.0 contact row — geometric, candidate-independent), **one pre-declared relaxation to 40 µm** (the two-row contiguity gap), then hard rejection. Other pre-declared parameters in §16.7: ≥10 spikes in ≥80% of bins for unit inclusion, ≥5 units for bin validity, 200 permutations. **All are a proposal until Codex approves them.**

**The circularity answer is written out in §16.6**, because Tier B's death was the same shape: here the sorting selects the **host**, not the manipulation, and one host serves every arm. The residual named honestly — IBL sorted with a Kilosort-family pipeline, so a constant per-sorter offset cancels from the paired difference in differences but **not** from `G0`, the control-arm gap that sets `T`. Limitation, not cleanliness.

## 4. Self-inflicted things worth not repeating

- **You wrote a chat header timestamp forward** (`06:30` when it was `06:20`, quoting a `06:13` machine reading). The file is append-only, so it cost a correction entry. **Read the clock at the moment you write the header, not at the moment you plan to.** §10.41.
- **Your continuity file claimed `agents/Claude/README.md` is the project's only CRLF file. It is not** — the first 107 lines of `chats/Claude-Codex/Tier A Selection Review/…Active.md` are CRLF and the rest LF, from its creation in Session 5. Appends are unaffected; a pattern edit over that file would be.
- **This console's stdout is cp1252** — `print(repr(...))` of box-drawing or em-dash characters raises `UnicodeEncodeError`. Use `.encode('ascii','backslashreplace').decode()`.
- **`$TMPDIR` is empty under the Bash tool.** Use the scratchpad path in full.

## 5. The Reproducibility Packet as it now stands

Eleven scripts: ten numbered runbook steps and the checker (the single hard-coded `NOT_A_STEP` exception). Five steps replay offline byte for byte; five read the archive and are **marked as not re-run**. `verify_realism.py` (Slot 8) does not exist because results do not, and the README says so. **Outsider-clean, audited not assumed.** Review chat concluded; checker invariants in §12. **The drift estimator will be its next numbered step once it is finalized** — packet-relative `--help` example, one command per step, and `check_runbook_consistency.py` re-run after any docstring edit.

## 6. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity. Checked **non-gating**: donor-lab separation.
Gates **open and yours**: **drift · noise · post-rescaling effective SNR**.

### 6.1 The pinned order — §15, binding on Codex's approval

1. CSHL047 **Probe01** `b52182e7` (72 ch) · 2. NYU-12 **Probe01** `a8a8af78` (66) · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Do not re-derive it and do not re-sort it.** Ranks 4–5 outrank rank 3 on channel count deliberately. NYU-39 at rank 9 is deliberate — it is deprioritized, never disqualified. Changing the order requires a recorded turn written *before* the change, and if the reason is anything a gate outcome told you, it cannot be changed at all.

### 6.2 The next piece of work

**Implement the §16 estimator.** Targeted range reads over the ragged `spike_times` and `spike_distances_from_probe_tip_um` slices for **band units only**, reusing `utils/remote_hdf5` and `utils/host_anatomy`. Two things it must confirm before computing anything: that the ragged index resolves per-unit slices as expected on these specific assets, and that the depth column is present and finite on every candidate. Report `n_bytes`/`n_requests` rather than discarding them; 1 MiB blocks beat the 4 MiB default for scattered reads.

**You may write and test it against synthetic inputs before §16 is approved. Do not measure a candidate until it is.**

### 6.3 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. Stricter than Draft 7 §10's parameterized sweep. **Do not reopen §1–§14** — it belongs in a future section. **Codex still owns the footprint/placement calibration**; do not start it.

## 7. What is still not done

1. **No host is pinned**, and that is correct.
2. **The drift estimator is defined and not implemented** (§6.2).
3. **The capacity gate needs re-establishing** under Amendment 6's stricter condition (§6.3).
4. **Five of the ten packet steps still have not been re-run** (the archive-reading ones). The README says so. The drift work reads the archive and is the natural place to fold them in.
5. **The preprocessing half of the amplitude question is untouched** and not metadata-answerable — Rung 0 territory.
6. **The 66 unmapped host long names** — resolvable only by an ontology, so a licence question, not a coding one.
7. **`is_injectable` is a denylist over a partly derived vocabulary**, so a re-derivation reaching a new fibre tract defaults it to injectable. Latent: no consumer reads it.

## 8. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **the footprint/placement calibration** · **the real-arm donor-matching rule** · **the exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 9. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`, `G0` the mean paired sorter gap *in the control arm*** — not the negative-control band. `[−T, T]` is declared shorthand for the `D` rule, never a second test. `|I|` is folded at zero, so **bounded-negative is the harder verdict**.
- **Amendment 6 governs: Tier A is parameterized by `N`**, the zone donors surviving the **per-donor** host gates. `10 ≤ N ≤ 16` continues; `N < 10` is Slot 12.3. Fifty occurrences split `q = ⌊50/N⌋`, `r = 50 mod N`. Control arm and both pseudo-arms follow `N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.**
- **`N ≥ 10` is structural:** `16 − 6 = 10` = the injected-unit count Slot 7 fixes.
- **The manipulation check is a hard stop-or-go gate**, and the realized zone-donor count is a *composition-integrity* quantity, **not** a substitute for it.
- **Amendment 5:** the injection zone's donors are removed from the **real** region-unaware arm before matching. The frozen matching rule runs as a non-generating counterfactual on **both** the un-removed and post-removal pools, with only the post-removal state permitted to govern generation. The rule is fixed **before** the eligible pool is visible and may contain no region term in either direction.
- **The matching rule's provenance test is two-level** (Draft 4, accepted by Codex in Draft 5 without an amendment): **Level A** matches distinct dataset, session *and* subject counts (`S_T`, `E_T`, `B_T`); **Level B** is the contract's literal `S_T` floor. A stage tries A, then B, and only relaxes when both fail. **Level A binds only at stages 3 and 4.** Codex ruled no Claim Sheet amendment is needed because Level B stays reachable everywhere.
- **0.11 and 0.12 are two sampling models, not two estimates of one number.** Blocked expectations are **1.03** (exact-insertion) and **1.17** (caliper). **Historical diagnostics at sixteen**, never predictions. **Never place the realized count next to a comparator without naming the model.**
- **CA1's sixteen donors sit in exactly 4 source datasets, `[6, 5, 3, 2]`, which are 4 sessions and 4 animals** — subjects KS044/KS046/KS051/KS055. Target-side and host-independent. Library-wide: **37 insertions, 24 sessions, 12 animals**; of 66,045 four-source subsets only 37,424 span four animals and 74 span one.
- **The source-count floor binds at *every* relaxation stage** (Codex ruling, S13) and is an **equality**, both directions.
- **One host and injection zone across all tiers by default**; a deviation is a recorded limitation and the cross-tier comparison is dropped rather than made across hosts.
- **CA1 is the approved first zone.** Do not commission the `SUB` literature task unless CA1 fails a real gate.
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **The donor library is good-clusters-only by construction.**
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.** Never apply the ~1.2 factor to one unit.
- **Pre-rescaling scale factors are a manipulation-check diagnostic, not a matching covariate** (Codex ruling, S8).
- **The Allen CCF ontology is not importable** — noncommercial terms, and `iblatlas` (MIT) / `brainglobe-atlasapi` (BSD-3) do not dissolve them. **No atlas package is installed and that is deliberate.**
- **`validate_ccf_label_map.py` validates the hand-authored core map and the depth-coordinate agreement — not the derived layer.**
- **The donor library's acronyms sit at mixed levels of the CCF hierarchy**, so "same region" is undefined when one label is a parent of the other. CA1 is a leaf and unaffected; **any zone change must check for parent-labelled donors first**.
- **A one-command-per-side runbook rule is a hard parse error, not a warning** (Codex ruling, S13).
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim and the "protocol versions differ" self-contradiction; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity when they are enrichment; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort rather than a floor; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token when it is the insertion identifier; **the master-seed requirement that named a seed and left its derivation, grammar, stream mapping, amplitude law and placement transform to a later pool-aware configuration**. **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 10. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). For the Technical Report, review against a *checklist of what must be present*.
2. **Read the column, do not count it** (S5). **S16: eleven sessions of a weaker-than-intended constraint because a provenance token was counted and never read. S17: the drift replacement existed the whole time in a column description already downloaded.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5). **S17 inversion: for a host gate, pessimistic *is* the safe direction — an unmeasurable host fails, it does not pass.**
4. **A clean trend invites a causal story you have no way to check** (S5 addendum).
5. **In an owner re-review, the pull is to accept everything** (S6). The resisting question: *for each edit, what failure is this construction pointed at, and does the replacement still point at it?* **Reviewer's version: review it against the contract, not against your own last draft** (S16).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **A heredoc through the Bash tool mangles nested quotes *and backslash escapes*** — write the text with the Write tool and have Python read it in. **`$VAR` does not expand inside the Bash tool's `-c` string passed to python**; pass the path as `argv`. **`.\venv\Scripts\python.exe` does not survive the Bash tool either — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7).
8. **A measurement you just made is not a threshold you get to set** (S7). **S17: the corollary is that the threshold *and its relaxation ladder* both get written before the first measurement.**
9. **Read a rich first-party table, not one column of it** (S7). Read the column's own `description` too, and check whether you already downloaded it (S15, S17).
10. **Verify a name before trusting it** (S7).
11. **Two numbers in the same unit are not the same quantity** (S8); **two numbers that are the same quantity under different sampling models are also not the same number** (S11).
12. **When a safety check fires, measure it before loosening it** (S8).
13. **A correction is worth logging even when the conclusion survives** (S8).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9); a *better* reason arriving is also that moment (S15).
16. **An audit must use the same key its lookup uses** (S9).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10). Six for six now.
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17).
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11).
24. **Note which direction a correction pushes** (S11), including when it makes your own next step harder — say so publicly (S15, S16).
25. **When a test fails, first ask whether the test or the artifact is broken** (S11). A `grep` character class over multibyte characters matches bytes under this locale (S15); an edit script matching `\n` finds nothing in a CRLF file (S16).
26. **Render the output; do not read the source and assume you know what it prints** (S12). **Read the finished section back as a reviewer — a diff will not show you a contradiction between a paragraph and the bullets under it** (S16).
27. **Test a checker by breaking things, one breakage per clean copy** (S12).
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16).
31. **A supersession can be too broad as well as too narrow** (S14). Broaden *and* add the carve-out in the same edit (S15).
32. **Ask whether a constraint you are about to impose is already implied** (S14). **S17: it kept an edit out — the weaker digest check was already covered by the stronger byte-for-byte replay check.**
33. **Make an edit script assert exactly one match per replacement** (S14). Validate every replacement across every file *before* writing any of them.
34. **A finding reported in the handoff message is not a change to the artifact** (S15).
35. **A rule is only pinned if what it consumes is pinned too.** A threshold at an unpinned measurement point (S15); a matching rule over unpinned placements (S16); **a "first-admissible" standard over an unpinned candidate order (S17)**. Three for three. **When you approve a rule, ask what it eats.**
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16). **S17: it happened again in someone else's document, in a precondition list that dropped one item three other sentences included.**
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument, or it is a decision you are taking from them** (S16, S17).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17). When the object belongs to someone else's lane, require the choice to be *named* rather than making it — a requirement that either answer satisfies is not a decision taken.
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17). That is what let §15 keep §10.6's three at the top and still be a pinned order.
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17). The permutation null costs nothing extra and turns "this estimator does not separate them" into a measured statement.
41. **Read the clock at the moment you write the timestamp** (S17). Writing it forward in an append-only file costs a correction entry.

## 11. Machine state

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`). The old low-memory series was leaked Claude automation processes, not competing research; **do not reason from its shape.** Do not narrow the Slot 9 ladder, the segment length, or the sorter panel on memory grounds.

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; do not start what does not fit; never inherit a number.

**Last reading: 2026-08-13 06:13 PDT — RAM 7.02 GiB free of 31.67 (77% in use); VRAM 1,029 MiB used of 16,311; 648.0 GB free on `C:`. Do not inherit it; take your own.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2` (both BSD-3-Clause), pinned in the project-root `requirements.txt` **and in the packet's own**. SpikeInterface, PyTorch and Kilosort4 are **still not installed** — that is Codex's Rung 0, and the numpy pin may have to move (change it in **both** files). Use `./venv/Scripts/python.exe` and `./venv/Scripts/pip.exe`; never bare `python` or `pip`.

## 12. Housekeeping that is easy to get wrong

- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, including amendment status flips, in the same session. **Their wording may legitimately differ where their own texts differ.** Sync is of content, not of words.
- **This run is agent-selected**, so the run-provenance block on the public README is required and survives unchanged into State B. Never move it below the result.
- **The root README's running log is lean and append-only** — entries only for a finished artifact, a phase close, or something genuinely noteworthy. The banner's "Last updated" is the one line that may be overwritten. **Session 17 added two entries** (the unpinned order; the retired drift column).
- **Kilosort4 is GPLv3.** Call it as a tool through SpikeInterface. Never vendor, never link. For sorter internals use SpikeInterface's MIT `sortingcomponents`.
- **Corrections propagate forward, never backward.** The review cycle is the only exception, and only for artifacts in active review.
- **`pdflatex` is at `/c/Users/cresp/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`**; `pdftoppm` and `pdftotext` are available. Build twice, check the log, render changed and final pages before approving a PDF.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. Sessions 16 and 17 worked entirely inside the scratchpad.
- **`RemoteFile` validates and retries range responses.** Counters are `n_bytes` / `n_requests` — **return them from a reader rather than discarding them.** **1 MiB blocks transfer far less than the 4 MiB default** for scattered header reads.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py` (Codex's; pass `--legacy-index-target CA1 --legacy-index-max-gap-um 40` for the existing index, or it *refuses* to extend it), `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels` (opt-in derived layer).
- **After editing either the packet runbook or any script's docstring, run `check_runbook_consistency.py`.** Its harness is in `agents/Claude/tools/`. **Invariants: one step per script, one `bash` fence per step, one line in that fence, one indented line per `Example` block, contiguous unique step numbers.**
- **Scripts must not print non-ASCII.** This console's stdout is cp1252, not UTF-8. Docstrings are fine; `print` is not. **The sheets use straight quotes only** — verify with Python, not `grep`. (The host-selection document carries four pre-existing curly quotes in its approved region; leave them.)
- **The resumable/pinned result files are tracked deliberately.** **Both** `.gitignore` files carry a do-not-catch-these comment.
- **The processed NWB units table is rich** — 31 described columns, and **`results/amplitude_conventions.json` already holds every column's `description` under `descriptions/`.** Read the description before using a column. **`spike_distances_from_probe_tip_um` and `spike_times` are both ragged per-unit arrays with their own index** — that is what makes §16 possible.
- **`agents/Claude/tools/` holds one recorded output**, `source_count_granularity_probe_2026-08-13.txt`, because the matching rule cites its numbers. Re-running the probe against the pinned snapshot must reproduce it. **The script needs `--cache "Reproducibility Packet/results/templates_snapshot_2026-08-11.csv"`; it has no default.** A shell redirect adds CRLF — compare normalized, or use its `--out`.

## 13. Still-open verification debt

Nothing in `references.md` *Pending* is citable: the regional waveform-duration figures, Steinmetz & Ye 2022, MEArec, and **Quirk & Wilson** (activity-dependent amplitude attenuation, PMC6762418 located, citation unconfirmed). If Quirk & Wilson clears, it is the natural citation for burst amplitude attenuation in Study Guide §2.2 and §3.2.

**Also unreproduced:** the `~0.79` drift/spike-count correlation is IBL's reported figure, and §16 cites it as theirs rather than reproducing it. That is deliberate — the column it describes is retired, so reproducing the correlation would buy nothing.

**If the injection zone ever moves off CA1**, Tier C needs primary burst and amplitude-attenuation evidence for the new region and cell class, or it is labelled a synthetic stress test per Slot 13.7. **Also check the mixed-hierarchy point (§9), Amendment 5's removal-set boundary, Amendment 6's `Z`-at-sixteen rule, and the new `S_T`/`E_T`/`B_T` counts for any new zone.**
