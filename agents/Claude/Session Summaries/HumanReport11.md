# Human Report 11 — Claude

**Current date and time:** 2026-08-12 18:24 PDT

**Session:** Claude Session 11

**Phase at start:** Phase 2 — Execution. Amendments 1–4 `In force`; Amendment 5 `Proposed` at the state Codex approved in its Session 10. No host pinned, no Rung 0, no sorter run.

**Phase at end:** Phase 2 — Execution. Unchanged on all of those. **Amendment 5 is still `Proposed`** — I edited it during the owner re-review, so it goes back to Codex rather than into force.

**No progress report is due this session.** The next count-based trigger is Claude Session 16; no phase closed, and no amendment entered force through my work here. (Had I approved Amendment 5 unchanged, that flip would have triggered one — the edits are why it did not.)

---

## Summary

Two pieces of work, unrelated to each other except that the first one finished early enough to leave room for the second.

**One — the owner re-review of Amendment 5.** Codex made two changes to the amendment I proposed last session and approved that state. I re-derived the mathematical one by three independent routes before reading the argument for it; it is right, and I accepted both changes unchanged. Then, checking the corrected amendment against the amendments it sits next to, I found something neither of us had looked for: **Amendment 5 makes a sentence in Amendment 3 false**, and Amendment 3 is already `In force`. Left alone the contract would have carried two agreed clauses pointing opposite ways, with the stale one implying the exact opposite of what the design now says. That is fixed by an explicit, dated supersession rather than by editing Amendment 3, which this project never does.

**Two — the Reproducibility Packet can now actually be run by someone who is not us.** It had ten working scripts and eighteen result files and no way in: no dependency list, no data document, no runbook. It now has all three, plus its own `.gitignore`. The claim that it is self-contained was then **tested rather than asserted** — the folder was copied on its own to a location where nothing else in the project was reachable, a fresh virtual environment was built there from its own `requirements.txt`, and the printed commands were run in it. Five of the ten steps reproduced their recorded output byte for byte with no network access at all. The other five read the public archive and are marked, in the packet's own README, as not re-run.

---

## 1. The owner re-review of Amendment 5

### 1.1 Codex's correction, checked three ways

Codex replaced the amendment's expected-value baseline. The old one multiplied per-slot probabilities as though the sixteen control slots were independent draws; the diagnostic matcher they are the null for never reuses a partner and never pairs a template with itself, so the right null is over **injective, non-self assignments**. Codex derived that by inclusion–exclusion and reported 1.03 for the exact-insertion-blocked case where 0.98 had been.

I re-derived it without importing their function:

| route | what it does | result |
|---|---|---|
| exhaustive enumeration | every injective non-self assignment, pool sizes 2–8 × every zone count | 28 cases, **0 mismatches**, floating-point equality |
| a counting dynamic program | inclusion–exclusion over self-pairs, then splitting free slots between zone and non-zone targets | agrees on all 28 |
| Monte Carlo | rejection sampling, 400,000 accepted assignments | agrees to within 0.002 at n = 20, 88, 60 |

Recomputing the aggregate from the pinned snapshot through a separate CSV reader reproduced Codex's numbers exactly: full pool 0.1100, exact-insertion blocking 1.0321, and inside the provisional caliper 0.1151 and 1.1694. The superseded expression gives 0.9837 — the 0.98 that was there.

**The direction is the part worth stating.** The correction *raises* the null, so the realized 8-of-16 is now measured against a more permissive baseline. Codex's fix makes my own diagnostic weaker. That is the direction a correction should run when the person checking it has a stake in the answer, and it is why I went and checked it rather than accepting a number that flattered nothing of mine either way.

One thing fell out of the per-insertion decomposition that neither of us had noted: of the 1.032 expectation, 0.326 comes from an insertion holding only **eight** templates, two of them CA1 — a tiny block gives a large per-slot rate. Meanwhile six of the eight *realized* hits come from a different, 88-row insertion. The two ends of that table are not describing the same recording, which matters to whoever writes the matching rule.

### 1.2 The second change — accepted, and it corrects a real gap in what I proposed

Codex also found that my 0.12 "expected under a uniform region-blind draw" prices the removal against the **anchor pipeline's** sampling policy and says nothing about what removal costs a design that *pairs*. The zone donors are attractive precisely because they are close matches and satisfy the preferred same-source blocks; taking them away can widen matching distance, force a coarser provenance block, or make a stratum infeasible. Amendment 5 now requires the frozen matching rule to be run as a non-generating counterfactual on both the un-removed and the post-removal pools, with only the post-removal state permitted to govern generation.

I accept this without reservation. Pricing an exclusion under a policy it is not run under is the same shape of error as comparing two numbers in the same unit that are not the same quantity — which this project has already made once, in Session 8, over spike amplitudes. The locking is what makes the counterfactual safe: the removal decision is taken *now*, before either pool exists, so seeing both states later cannot reopen it.

### 1.3 The finding: Amendment 5 falsifies a sentence in Amendment 3

Amendment 3's boundary paragraph, `In force`, says the negative-control band

> does not mirror the chance injection-zone templates that the real region-unaware arm may contain.

Amendment 5 removes the injection zone's donor pool from that arm, which makes its post-removal eligible pool **the same object** as Amendment 3's shared pseudo-base pool. After that the real arm holds zero zone templates by construction — there are no chance zone templates left to fail to mirror.

Two consequences. The contract would carry two `In force` clauses pointing opposite ways with nothing saying which wins; and, worse, the stale clause implies the real region-unaware arm **may contain zone donors**, which is the direct negation of the new Slot 13.11 that the same amendment adds. A reader reconstructing the design from the amendment stack would have had no way to tell.

The fix respects append-never-overwrite. Amendment 3's text is untouched; Amendment 5 gained a **What this supersedes** paragraph naming the clause and dating its retirement. The supersession is deliberately narrow — the rest of that paragraph still holds, including that the band cannot mirror the matched pool's region homogeneity, which no no-manipulation control can.

**The general form, since this is now the second amendment in a row where the finding came from a neighbour rather than from the thing under review:** an amendment that changes a design *property* has to be checked against every in-force sentence that *describes* that property, not only against the slots its own header lists. Amendment 5's header names Slots 5, 7, 11.3 and 13. The sentence it falsified lives in Amendment 3.

### 1.4 The two smaller edits

- **The caliper sensitivity now names its own expectations.** It read "2 of 12 and 5 of 12" beside a table giving expectations for the full pool, inviting a comparison against the wrong denominators. It now gives 0.12 and 1.17, explicitly computed inside that caliper.
- **The 0.12 and the 0.11 were two models under one label.** The table's 0.11 is the paired matcher's null; the rationale's 0.12 is an unpaired anchor-like draw (hypergeometric, 16 × 16 ⁄ 2,183 = 0.1173, P(≥1) = 0.1114, which is where "about one arm in nine" comes from — confirmed rather than inherited). Neither is wrong and neither corrects the other; the gap between them is exactly the pairing's self-exclusion. Two region-blind expectations differing with no note is a failure mode this project has already logged for itself, so both sheets now say which model each number belongs to.

### 1.5 Why I did not simply approve

Approving unchanged would have put Amendment 5 into force this session and unblocked the matching-rule lane, which is the faster outcome and was available. I did not, because §1.3 is a defect in the contract rather than a preference about wording. To keep that from costing a full extra round-trip I told Codex in the chat that **I pre-accept any rewording or removal of my three additions** — the only thing I would not want dropped silently is the supersession fact itself. So this should close on Codex's next turn without coming back to me.

---

## 2. The Reproducibility Packet's self-containment

This was the largest open item that was mine, carried across three sessions.

### 2.1 What was missing, and what it now has

The packet held ten scripts, a `utils/` module, and eighteen result files — all portable, all argparse'd, no hard-coded paths — and **no way for an outsider to start**. The playbook's standard is literal: copy that folder alone to a clean machine and reproduce the result without contacting anyone. Portable is not the same claim as self-contained.

Four files were written, all inside the packet folder:

- **`README.md`** — a ten-step runbook. Each step names its script, says in one line what it does, gives the exact copy-paste command, and lists the files it produces. Steps are marked **[offline]** or **[archive]** so a reader knows before running which ones need network. It carries the dependency licence table, a quality-control section naming every exclusion the work makes, and a section describing the Slot 8 verification artifact and stating plainly that it does not exist yet.
- **`DATA.md`** — both external sources, with what they are, how to get them, licence and commercial-use status, and copy-ready citations. It also records why no atlas ontology is a dependency, which is a licence decision rather than an omission.
- **`requirements.txt`** — `h5py==3.16.0` and `numpy==2.5.2`, both BSD-3-Clause, with install commands for both platform conventions.
- **`.gitignore`** — the packet's own, deliberately narrower than the project's, with an explicit "do not add a rule that catches these" block protecting the pinned snapshots and resumable indexes.

### 2.2 The DANDI citation was fetched, not written from memory

`DATA.md` needed a citation for DANDI 000409. Rather than reconstruct one, I read the dandiset's own metadata from the DANDI API and wrote its 909-character citation string into the file **programmatically**, substituting it into a template. It carries roughly forty author names, several with non-ASCII characters (`Niccolò`, `Gerçek`, `Félix`), which hand-transcription through a Windows console would have corrupted — and in fact the console displayed them as replacement characters throughout, while the file itself is correct. I verified the file's codepoints directly (`0xf2`, `0xe7`, `0xe9`) rather than trusting the terminal. The same read confirmed the licence field is `spdx:CC-BY-4.0` from the dataset's own metadata, and gave the scale figures now in `DATA.md`: 2,048 files, 139 subjects, ~49.7 TB.

### 2.3 The self-containment test, run rather than assumed

Two rounds:

1. **Copy alone.** The packet folder was copied by itself to a location with no other project file reachable, and the five offline-replayable steps were run from inside it with the project interpreter. Four reproduced byte for byte immediately. Two did not, and both told me something: the donor-provenance report needed `--host-subject NYU-11 --detail-area CA1`, and the placement replay needed `--skipped-note 35`. **Those flags were missing from my draft runbook, and the byte-diff is what found them.** With them, both reproduce exactly. The runbook now prints the working commands.
2. **Fresh environment.** A second copy, a virtual environment built inside it from `requirements.txt` alone, and the same five commands. All five reproduced byte for byte — the sole difference anywhere being the two header lines (`etag`, `last-modified`) that only a live HTTP response can carry, which the runbook documents as the expected difference for an offline run of that step.

The first attempt at the fresh-environment test **failed**, with `ImportError: DLL load failed while importing _errors: The filename or extension is too long`. That was the deep scratch path exceeding Windows' legacy 260-character limit, not a packet defect — but the error names neither paths nor the limit, so a reader hitting it would have no idea what it meant. The README now warns about it explicitly. This is the kind of thing that is only findable by actually running the thing somewhere else.

### 2.4 What the packet still does not have

- **The Slot 8 verification artifact (`verify_realism.py`) does not exist**, because the results it renders do not. The README says so in those words rather than omitting the section.
- **Five of the ten steps have not been re-run** since the runbook was written; they read archive metadata, and one of them (the anatomy survey) is not expected to reproduce unchanged because its index is resumable and a second run continues past the 46 assets the recorded report covers. The README states all of this under a **Validation status** heading rather than letting "verified" cover the whole document.

---

## 3. Cross-review of Codex Session 10

Read the report and both code edits. Everything in §1 above is the substance of it. Nothing in the report disagrees with anything I found, and I flagged no defects in it beyond the neighbourhood finding in §1.3, which is not a defect in Codex's work — it is a defect the pair of us created between two amendments.

I also re-ran the corrected audit offline against the tracked snapshot and confirmed it is **byte-identical** to the tracked report, which re-confirms both the script and the pinned upstream object.

---

## 4. Challenges, and how they were handled

- **The temptation to approve.** Amendment 5 was one approval away from force, and the finding that stopped it is in a *different* amendment. The resisting move was to read the amendment against its neighbours instead of only against itself, which is not something the review cycle asks for and which I am now writing down as a rule.
- **Two correct numbers that looked like a contradiction.** 0.11 and 0.12 sat four paragraphs apart under near-identical labels. The wrong response was to "fix" one of them; the right one was to work out that they are different sampling models and say so. I have made the opposite error before — asserting a direction I found plausible — and the check here was to compute both models rather than pick the one I expected.
- **The runbook that did not run.** Two of my five commands were wrong on the first attempt. They would have looked entirely plausible to a reader and produced subtly different output. Only the byte-diff caught them, which is the argument for validating a runbook by executing it rather than by re-reading it.
- **A test failure that was about my test, not the artifact.** The long-path `ImportError` looked like a packet defect for about a minute. Reproducing it in a short path settled it, and the failure became a README warning instead of a false alarm.

---

## 5. Files created or updated

**Created**

- `Reproducibility Packet/README.md` — the ten-step runbook, licence table, QC records, validation status.
- `Reproducibility Packet/DATA.md` — both data sources, licences, access paths, verified citations.
- `Reproducibility Packet/requirements.txt` — pinned dependencies.
- `Reproducibility Packet/.gitignore` — the packet's own ignore rules.
- `agents/Claude/Session Summaries/HumanReport11.md` — this report.

**Updated**

- `Claim Sheet.md` — Amendment 5: caliper expectations, the two-model note, the **What this supersedes** paragraph, status line. SHA-256 `d536b7d3f5d0c14015084c0ef5054bd7a5525ad6a22acc4d23f6bdcc480f698a`.
- `Accessible Claim Sheet.md` — the same three changes in plain language, synchronized. SHA-256 `4eb76bafe4b60abc6af40f7ad3623e61a301386ec9eaaaf9c976ad6e7a84d9a0`.
- `agents/Claude/Tier A Host and Injection Zone Selection.md` — new §14 (Draft 7); §13 left as the recorded Session 10 turn. SHA-256 `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01`.
- `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` — appended the Session 11 turn (638 → 707 lines, prefix verified unchanged).
- `agents/Claude/references.md` — the DANDI entry now points at the verbatim citation in `DATA.md`.
- `README.md` — one running-log entry; the artifact table and data footer now link the packet's runbook and `DATA.md`.
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — session closeout.

**No script in the packet was modified this session.** The docstring examples inside those scripts still print project-root-relative paths, which disagrees with the packet-relative commands the README gives; that is recorded as an open item rather than fixed, because changing ten files Codex has hardened deserves its own handoff.

---

## 6. Machine state

Measured at **2026-08-12 18:14 PDT**: RAM 13.22 GiB free of 31.67 GiB; VRAM 988 MiB used of 16,311 MiB; 601 GB free on `C:`.

Nothing heavy ran. The session's execution was standard-library arithmetic, five offline script replays, one small dependency install into a temporary environment, and two bounded metadata reads (the DANDI dandiset info endpoint). No recording data was transferred, no sorter ran, no generator ran, and both temporary test directories were deleted before closeout.

---

## 7. Next steps

1. **Codex's turn on Amendment 5.** Three additive edits and Draft 7's §14. If Codex approves, the amendment enters force and the matching-rule lane opens — and that flip triggers a progress report for whoever writes it.
2. **The packet's script docstrings** should be brought in line with the packet-relative runbook, with a byte-identical replay as proof, since the `--help` text is what a reader sees first inside the folder.
3. **Host selection stays where it is.** Drift, noise, post-rescaling effective SNR, the footprint/placement calibration and Codex's balance gate remain open, and no host is pinned. That is correct, not overdue.
4. **The five archive-reading packet steps** should be re-executed once at some point so the Validation status section can cover all ten, ideally alongside work that needs the archive anyway rather than as a standalone cost.
