# Human Report 13 — Claude

**Current date and time:** 2026-08-12 22:24 PDT

**Session:** Claude Session 13

**Phase at start:** Phase 2 — Execution. Amendments 1–5 `In force`; no host pinned; no Rung 0, generator, sorter run, or scientific result.

**Phase at end:** unchanged. Two review cycles advanced, both handed back at explicitly approved exact states. Nothing was authorized to run.

**Progress-report trigger:** none. Session 13 is not a multiple of eight, no phase closed, and no amendment entered force. (The next count-based report is Session 16.)

---

## Summary

This session was two reviews and the work they generated.

The first was my owner re-review of the Reproducibility Packet after Codex found two defects in what I handed over last session. Both of Codex's findings were real and I accepted both repairs — but I took the reason behind one of them as a general claim and went looking for the same failure elsewhere, which is a habit this project has already paid for twice. It found two more instances, one on each side of the comparison, and both were confirmed by running rather than by reading. I repaired them, extended the mutation suite from thirteen cases to fifteen, and handed back three changed files.

The second was my review of Codex's Draft 1 of the Tier A real-arm donor matching rule — the rule that decides which control template each of the sixteen CA1 donors is paired with, written deliberately before the candidate pool exists so the choice cannot be made with the answer in view. The construction is sound and I endorsed all three of the decisions Codex asked me to resist, but with corrections and additions in each case, and I found one thing I did not fix: **as written, the rule would abort if the host recording kills a single donor, while the contract explicitly expects the project to survive losing up to six.** That is a contract-adjacent question, so it is now Section 11 of the document rather than an edit I made unilaterally.

No host is pinned, no donor is selected, nothing was generated, and no sorter has run.

## 1. Startup

`.agent-turn` named Claude and no `.agent-session.lock` existed. I created the lock, re-read `.agent-turn`, confirmed it still named Claude, and followed `AgentPrompt.md` in order: `Project Details/Project Details.md` in full, my own continuity file, the chat summaries and both active chats without replying during ingestion, then Codex's `HumanReport12.md` for the required cross-review.

Live state matched what I had inherited. All twelve packet hashes Codex handed back matched on disk, as did the corrected matching-rule hash — Codex had superseded its own first handoff hash after removing trailing line-break spaces, and I checked the corrected one.

## 2. Reproducibility Packet — owner re-review

### 2.1 Codex's two findings, checked rather than accepted

**The outsider-clean removal was right and the pointer was my error.** My packet README had named `agents/Claude/Tier A Host and Injection Zone Selection.md`; `Playbooks/reproducibility-packet.md` keeps agent paths out of the runbook. I checked what removing it costs — `screen_host_timing.py` was the only script that leaned on it, and its replacement paragraph states the sequential-screening rule *and* its reason without sending the reader anywhere. I then re-ran the outsider-clean audit myself instead of accepting the claim: the only remaining `Session` strings in the packet are DANDI session UUIDs inside commands.

**The fence-parser defect was mine and it was substantive.** My checker set `in_fence = False` after the first line inside a command fence, so a step carrying a correct first command and a second divergent one passed. Codex's repair reads to the closing fence, requires exactly one non-empty line, and rejects an unclosed fence, duplicate step numbers, and non-contiguous numbering.

I tested the numbering checks rather than assuming they earned their place. Removing a step heading's `**[offline]**` marker makes that heading invisible to the parser; contiguity is what catches it, and reports the real cause. Coverage alone would have reported a missing step and buried it.

### 2.2 Two escapes of the same class that survived the repair

The question I asked was the general form of Codex's finding: *if stopping early hid a second command on one line, where else does a reader see a command that the comparison does not?* Two answers, both confirmed by running:

1. **A second ` ```bash ` fence inside the same step.** Once a step's command has been read, the parser skips the next fence entirely. A bogus second command in Step 3 passed at exit 0.
2. **A second indented command inside the same `Example` block.** The docstring parser stopped at the first blank line after the command, so an indented command further down was never seen — and `--help` prints the whole block. I rendered the mutated `--help` rather than reasoning about it: both commands appear.

### 2.3 What I changed

- `check_runbook_consistency.py` now tracks whether it is inside a step region, and a second `bash` fence in the same step is a parse error. A `## ` section heading ends the region, which is what keeps the packet's own "Checking this runbook against the scripts" invocation legal.
- `parse_docstring_example` now collects *every* indented non-empty line in the `Example` block and requires exactly one. I measured before choosing that rule: all eleven scripts have exactly one such line today, so it is the packet's actual invariant rather than a convention I imposed.
- Both `Raises:` sections now document the conditions Codex added and the ones I added — Codex's were enforced but undocumented.
- The module docstring gained a fourth numbered item, so `--help` states the invariant a reader is held to. Rendered; it wraps correctly.
- The packet README's description of the checker was incomplete after the change and now names the one-command-per-side rule.
- The mutation harness gained both cases, each on its own clean copy.

### 2.4 Validation

**Fifteen of fifteen mutations caught, unmutated control passes.** Codex's thirteen still fail for their own reasons. The live checker passes all ten steps; all eleven scripts compile; all eleven `--help` pages render. Every `results/` file, both `requirements.txt` files, `DATA.md` and every scientific command are byte-identical — `git status` showed exactly three modified files. `git diff --check` clean; all three stayed LF.

## 3. Tier A real-arm donor matching rule — review

### 3.1 The three decisions Codex asked me to resist

**The source-count floor.** Codex reads Slot 7's "number of contributing source datasets" as the `dataset` column and requires the control set to hold exactly as many distinct values as the target set. I checked the column against my own recorded audit rather than against the description: it resolves the 2,183 Neuropixels 1.0 rows into 37 insertions, 24 sessions and 12 subjects, so it is the insertion-level source key and the reading is right. Exact equality is also the faithful reading of *balance* — Slot 7's worry is symmetric, so a control arm spread over **more** sources than the target is an imbalance, not a bonus. I made that explicit because "floor" reads like a lower bound.

Two consequences went into the draft. First, **the floor is not an ordinary assignment constraint**: an exact count of distinct sources over the selected set is a global cardinality condition that min-cost flow and rectangular assignment do not enforce, so the draft now requires an enumeration over source subsets of the required size — 66,045 constrained problems at the current target count, which is tractable — or another method that provably returns the defined assignment, with infeasibility declared rather than a best effort returned. Second, **stage 1 satisfies the floor automatically but stages 2 and 3 do not.** I wrote the opposite first and caught it against the data: three of the four sessions holding CA1 donors carry further insertions, so a session-blocked control set can span more sources than the target. That is acceptable — Amendment 2 ranks pairwise blocking above count balance — but it is a property worth stating.

**Donor-equal matching cost.** Keep it, and the sentence justifying it contained an arithmetic error: Draft 1 said the rota gives **six** donors an extra occurrence. Fifty slots over sixteen donors is `14 × 3 + 2 × 4`, so it is **two**. Corrected. The correction is what settles the question: the two candidate objectives can disagree only through a 22% weight difference on two of sixteen donors, and donor-equal is preferable anyway because the object being chosen is a donor-level pairing and exposure weighting would let the rota's arbitrary choice of which donors carry a fourth slot influence which partner each donor gets.

**Common U-derived scaling.** Keep it, with two properties stated rather than implied. Only the standard deviation reaches the objective — the common mean cancels exactly in the paired absolute difference — so "common scaling" is a claim about a common standard deviation and nothing weaker is being relied on. And the ruler contains the removed donors by construction, since U includes the injection zone. Codex's stated reason argues for *one* ruler rather than for U's specifically; R-derived scaling would satisfy it equally. I still land on U (larger sample, and the counterfactual is naturally priced in the units the un-removed procedure would have used), but because that is a preference rather than a proof, the draft now requires both reports to record the R-derived standard deviations as a diagnostic. The question gets answered by data later instead of argued now.

### 3.2 Two additions to the reported outputs

**Concentration, not only count.** Sixteen donors over four sources distributed `13, 1, 1, 1` and `4, 4, 4, 4` have the same count and a different structure, and concentration is what Slot 7 is actually worried about. The multiplicity distribution is now reported for both arms. The target's is `[6, 5, 3, 2]`.

**The zone-donor count needs its comparator named.** The realized injection-zone count among selected controls and Amendment 5's uniform unpaired expectation sat adjacent in the outputs list, where they read as a realized/expected pair. They are different sampling models — this project already paid for that distinction once, inside Amendment 5's own review — so the draft now requires whichever comparator a report places beside the realized count to be named with its model.

### 3.3 The thing I did not fix

Draft 1 fixes the target side at exactly sixteen keys and makes anything else a hard failure. Amendment 2's success/failure paragraph makes Slot 12.3 the pre-declared outcome "if the gates kill **more than six** of the sixteen" — so one to six killed donors is a configuration the project is expected to continue in, and the rule as written would convert a survivable loss into a dropped tier. CA1 has exactly sixteen donors and the post-rescaling gates are the demanding ones, so this is not remote.

I left it as a question because the minimal fix — parameterizing by `N` with `10 ≤ N ≤ 16` — collides with contract text: the fifty-occurrence rota is derived from sixteen in Amendment 2 point 5, and at `N = 10` "three or four times" becomes five times each. Re-deriving that is amendment work, not specification work. There is also a coherent case for keeping the hard sixteen, but it is a case for a *stricter* contract than the one in force and should arrive as an amendment rather than as a side effect of one rule's error handling. It is Codex's rule and Codex's lane; the draft's new Section 11 states the question and the three candidate shapes.

### 3.4 A pre-pool measurement, with its boundary

I wrote `agents/Claude/tools/zone_provenance_headroom.py` to answer one bounded question: is any provenance stage arithmetically impossible before the host exists? The four insertions holding CA1 donors need 6, 5, 3 and 2 partners and hold 82, 75, 58 and **6** non-CA1 templates. So the insertion stage is not impossible on the snapshot, and KS046's insertion is where it would break — two targets against six candidates, with no room to lose any.

**Read the boundary with it.** Those supply figures are a ceiling and nothing else. Final eligibility is host-specific and post-rescaling; every gate can only cut them. The tool says where stage 1 would break if it breaks. It does not say that it will hold, and it selects nothing.

## 4. Reasoning paths worth recording

**The general-claim habit paid again, and it is now three for three.** Session 10 established that a repair's *reason* is a general claim worth checking elsewhere. Session 12 used it to prove a defect was local. This session used it to find two more instances of a defect Codex had found once. Reading the repaired code would have called it fixed; running mutations against it did not.

**I nearly shipped a wrong sentence into someone else's specification.** My claim that all three finer provenance stages refine the target's source set was wrong at the session and subject levels, and only checking the library's own session structure caught it. Writing an explanatory sentence is exactly the moment the explanation is least likely to be checked, because it feels like a restatement of something already established.

**A strict failure rule can contradict a permissive contract, and it will look like rigor while it does it.** Draft 1's hard sixteen reads as discipline. Against Slot 12.3 it is a stricter contract arriving through error handling. Failure semantics are where a specification quietly makes policy, and they deserve reading against the contract with the same care as the success path.

## 5. Files created or updated

**Created**

- `agents/Claude/tools/zone_provenance_headroom.py`
- `agents/Claude/Session Summaries/HumanReport13.md`

**Updated**

- `Reproducibility Packet/scripts/check_runbook_consistency.py` — two escapes closed, docstrings corrected
- `Reproducibility Packet/README.md` — the checker's description now names the one-command rule
- `agents/Claude/tools/mutation_test_runbook_checker.py` — two new mutation cases (fifteen total)
- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` — Draft 2, reviewed and edited
- `chats/Claude-Codex/Reproducibility Packet Review/Reproducibility Packet Review - Active.md`
- `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md`
- root `README.md` — one running-log entry
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`

**Deliberately unchanged**

- both Claim Sheets and all five in-force amendments
- every packet `results/` file, both `requirements.txt` files, `DATA.md`
- `agents/Claude/Tier A Host and Injection Zone Selection.md` (same-state approved; nothing this session reopened it)
- both `references.md` files — no new source was read
- `director_requests.md` — nothing this session needs the director

## 6. Machine state

Measured at 2026-08-12 22:12 PDT: system RAM **11.07 GiB free of 31.67**; GPU **987 MiB used of 16,311**; `C:` **648.7 GB free**.

Nothing heavy ran. The session was local text reads, hashing, stdlib parsing, compilation, `--help` rendering, one 2 MB tracked CSV read, and nineteen disposable packet copies — three probe copies plus the harness's control and fifteen cases — all deleted. No network read, no dependency install, no raw-recording read, no template-array pull, no Rung 0, no generator, no sorter run.

## 7. Next steps

1. **Codex re-reviews the three changed packet states** and rules on one question I left to it: the one-command-per-side rule is a hard parse error, which is right today but constrains a future `verify_realism.py` step that might want two commands. My position is that such a step should become two numbered steps; if Codex prefers a warning, now is when it costs nothing.
2. **Codex re-reviews Draft 2 of the matching rule** and answers Section 11 — whether the rule parameterizes by `N`, whether an amendment tightens the contract to match Draft 1's strictness, or a third shape.
3. **Drift remains the open gate on my own lane**, and it is still the natural next piece of my work. The library's `cumulative_drift_um_per_hour` column is unusable — it reaches ~6.5 × 10⁶ — so drift has to be *defined* before it can be measured, and the definition must not be chosen after seeing the numbers it produces.
4. **Five packet steps still have not been re-run** (the archive-reading ones), and the README says so. Best folded into work that needs the archive anyway.
5. **No director action is needed.** `director_requests.md` is unchanged.
