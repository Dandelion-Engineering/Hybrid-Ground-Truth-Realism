# Human Report 12 — Codex

**Current date and time:** 2026-08-12 21:18 PDT

**Session:** Codex Session 12

**Phase at start:** Phase 2 — Execution. Claim Sheet Amendments 1–5 `In force`; no host pinned; no host-specific eligible pool; no Rung 0, generator, sorter run, or scientific result.

**Phase at end:** unchanged. A Reproducibility Packet review returned a corrected exact state to Claude, and the first pre-pool real-arm donor-matching-rule specification was written and handed to Claude for review. Neither handoff authorizes execution.

**Progress-report trigger:** none. Session 12 is not a multiple of eight, no phase closed, and no Claim Sheet amendment entered force.

---

## Summary

This session completed two separate pieces of Phase 2 work.

First, I performed the required exact-state review of Claude Session 12's Reproducibility Packet changes. The core construction was right: each script retains a runnable packet-relative example, and a checker compares that rendered `--help` example with the packet runbook. I accepted Claude's two explicit judgement calls — keeping examples in every docstring and keeping the checker itself as one hard-coded non-step exception — but found two defects before approval. The packet README named an agent-workspace path despite the packet playbook's outsider-clean rule, and the checker silently ignored every line after the first inside a runbook command fence. The latter meant a correct first line plus a second divergent command still passed. The parser also did not reject duplicate or non-contiguous step numbers. I repaired all three boundaries, added mutations that would have escaped the handed checker, and explicitly approved the new states for genuine Claude owner re-review.

Second, I wrote `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`, the first complete pre-pool specification for the real Tier A control matching Amendment 5 unblocked. It fixes the inputs, eligibility boundary, common scaling, continuous objective, provenance fallback, global no-reuse assignment, tie handling, outputs, and failure semantics before any host-specific pool exists. It also requires the implementation and deterministic tests to receive same-state approval before they may open such a pool. I opened a dedicated review chat and handed Draft 1 to Claude at an exact hash.

No scientific execution occurred. No donor, host, placement configuration, or matching output exists.

## 1. Startup and context restoration

`.agent-turn` named Codex and `.agent-session.lock` did not exist. I created the lock, reread `.agent-turn`, confirmed it still named Codex, and then followed `AgentPrompt.md` in order:

1. read `Project Details/Project Details.md` in full;
2. read Codex's continuity file;
3. read every chat `Summary.md` in a Codex participant path;
4. read both active Codex chats without replying during ingestion;
5. read Claude's latest continuity file and `HumanReport12.md` for the required recent-work cross-review;
6. read the full current `Claim Sheet.md`, including Amendments 1–5, before writing the matching rule.

The live state matched the inherited summary: Amendments 1–5 are in force, Draft 7 of the Tier A host-selection artifact is same-state approved for its declared strategy/evidence scope, Claude's packet handoff was waiting on Codex, and the real-arm matching-rule lane was open but unwritten.

## 2. Reproducibility Packet exact-state review

### 2.1 What passed as designed

All twelve handed hashes matched before review. The underlying design is sound:

- every numbered runbook script keeps a packet-relative command in its module docstring;
- `argparse --help` remains self-sufficient rather than sending the reader elsewhere;
- `check_runbook_consistency.py` parses docstrings through `ast`, so it compares the rendered string rather than source text that may hide escapes;
- commands are compared character for character rather than only as shell tokens;
- every new ordinary script owes a numbered runbook step;
- `check_runbook_consistency.py` is the sole named exception because it reproduces no result.

I ruled that the hard-coded exception should stay hard-coded. A docstring marker would let a new script exempt itself; one explicit name is deliberately fail-closed and makes any new exception a reviewed change.

### 2.2 Outsider-clean defect

The new packet README pointed to `agents/Claude/Tier A Host and Injection Zone Selection.md`. The file was correctly described as unnecessary to run the packet, but `Playbooks/reproducibility-packet.md` explicitly keeps agent paths and project work history out of the public runbook.

I removed the agent-workspace path. The README still points to the public project repository and the two Claim Sheets as living design documents that are not required for reproduction. `screen_host_timing.py` now states its sequential-screening rule and its reason completely, with no outside pointer.

A packet-wide text audit then found three older session-history phrases in script docstrings (`Session 7`, `Session 8`, `Session 10`). I replaced them with direct descriptions of the measurement or refactor. Nothing scientific or executable changed.

### 2.3 Checker parser defect

The handed parser set `in_fence = False` immediately after the first command line. It therefore never inspected a second line or verified the closing fence. A README step could contain:

```text
correct command
different second command
```

and still pass if the docstring matched the first line. It also did not require unique or contiguous step numbers.

The repaired parser now:

- reads through the closing fence;
- requires exactly one non-empty command line;
- rejects an unclosed or empty command fence;
- rejects duplicate step numbers;
- requires contiguous numbering from 1 through N;
- validates that `--readme` is a file and `--scripts` is a directory; and
- reports parse failures as clean fatal messages.

The mutation harness gained three cases that the handed checker would not have graded correctly: a second README command, duplicate numbering with the corresponding docstring changed to agree, and a numbering gap with the corresponding docstring changed to agree. It also carries stderr into the displayed reason.

### 2.4 Validation and exact states

Validation after the repair:

- clean control passed;
- all original ten mutations still failed;
- all three new mutations failed for their specific reason: **13 of 13 caught**;
- the live checker passed all ten numbered steps;
- all eleven packet Python files compiled;
- all eleven `--help` pages rendered;
- packet text contains no `agents/`, Claude, Codex, or Collaboration Station reference;
- every tracked `results/` file, both dependency pins, `DATA.md`, and every scientific command stayed unchanged;
- `git diff --check` reported no whitespace error.

I explicitly approved and handed back the new packet state in `chats/Claude-Codex/Reproducibility Packet Review/Reproducibility Packet Review - Active.md`. The key changed hashes are:

- packet `README.md`: `00acb8262cee63816a80c9737a0ca1bd3a7a33374347183bcca77b444af4c835`
- `check_runbook_consistency.py`: `094fbff10b7fa33c441b88926042c494c4a0706b0b41b4e7f9bf25caa6e16c00`
- `audit_template_library.py`: `0f98f195a49498096a1cf24fea6e5492a18cdda50cbc2893f2aaf88d75d2bb87`
- `derive_ccf_label_map.py`: `b0b33ce2515d0504f3ebcbbe8606d9ccfef31d428301314121cecf1769a6cd55`
- `screen_host_timing.py`: `bb6681ca6762139832f204fa3ee0256252c2f9bdb0323f74e6b6b856211f2ab5`
- `audit_amplitude_conventions.py`: `7b82543266f3ea4800a1aeac31733e872106ef3bd46d56c2a6e0b27517629fce`
- mutation harness: `3b5a36a9fa46ef91a5b60ad71cd803e3835bf7cecd925087271e8a7864d91627`

The six other handed script states were unchanged and explicitly approved at their original hashes. The packet review remains active until Claude genuinely re-opens the changed state and approves those exact bytes or returns another state.

## 3. Tier A real-arm donor matching rule

### 3.1 Why a specification precedes code and data

Amendment 5 requires the matching rule to be fixed before the eligible pool is visible. A prose-only rule would still leave implementation freedom if code were written after the pool appeared, so Draft 1 adds a second timing guard: the implementation and deterministic tests must be same-state approved before they may construct or open a host-specific pool or rendered edge table.

No host-specific pool was inspected in this session.

### 3.2 Matching objects

The target set is the exact sixteen injection-zone donors, identified by globally unique (`dataset`, `template_index`) pairs. One control partner is assigned to each donor and reused across that donor's three or four appearances in the fixed fifty-occurrence exposure schedule.

The host-dependent input is defined as an edge-occurrence table rather than one row per candidate. A candidate is rendered at every scheduled occurrence of the target donor — same placement and amplitude target — because realized depth, effective SNR, and feasibility can vary with placement. An assignment edge exists only when every occurrence for the target/candidate pair passes hard eligibility.

### 3.3 The two Amendment 5 states

Draft 1 names:

- U: the final eligible region-unaware pool before zone removal;
- Z: the exact injection-zone donor keys; and
- R: `U minus Z`, the post-removal authority.

The same rule runs on U and R. Only R may govern generation. Scaling is computed once from hard-eligible U edge occurrences and reused for both, so the cost of removal is not mixed with a changed ruler.

### 3.4 Continuous objective and manipulation boundary

The soft matching quantities are exactly:

1. realized post-rescaling peak-to-peak amplitude;
2. realized effective host SNR; and
3. realized peak depth along the injection band.

They receive equal weight in standardized L1 distance. Probe/channel geometry and placement feasibility are hard gates. Spatial footprint and other multichannel waveform-shape features are deliberately not matched because they help constitute the region manipulation. Pre-rescaling scale factor stays diagnostic only.

The matcher receives no anatomical-label column. Zone membership is used only to construct R and report un-removed composition.

### 3.5 Provenance, assignment, and failure

The rule chooses the finest provenance stage at which a complete assignment exists:

1. insertion;
2. session, only after insertion infeasibility;
3. subject, only after session infeasibility;
4. the existing source-count floor, only after subject infeasibility.

At the floor, the selected control set must contain exactly the target set's number of distinct `dataset`/insertion sources. There is no unrestricted fifth stage. Continuous balance can never trigger a relaxation; only assignment infeasibility can.

Within a stage, the assignment is global and one-to-one. It first preserves as many insertion, session, then subject matches as possible; then minimizes total cost, maximum pair cost, and finally the candidate-key vector in target-key order. A greedy nearest-neighbour pass is explicitly not the rule.

Malformed keys, an invalid U/Z/R relation, inconsistent digests, non-finite or zero-variance quantities, fewer than sixteen candidates, no count-floor assignment, or non-deterministic solver/test output all fail loudly. If post-removal matching or the later balance gate fails, Slot 12.3 governs; the project does not rerun with new weights or a more convenient objective.

### 3.6 Review state

Artifact:

- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`
- Draft 1 SHA-256 `1243742131b39dadde8fe86240d718f07d196826186a748e0344085344c1ee3f`

I explicitly approved that exact state and handed it to Claude in the new append-only chat `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md`.

The review asks Claude to resist three specific choices rather than wave through the whole draft: the exact interpretation of the source-count floor, donor-equal matching cost across three/four occurrences while exposure-weighted balance is reported separately, and common U-derived scaling for the removal counterfactual.

## 4. Public heartbeat and housekeeping

The root Live-Run README received one lean entry because fixing the real-arm matching rule before the pool exists is a noteworthy pre-execution event. The orientation now says Draft 1 awaits same-state review and keeps implementation, exact configuration, balance, generation, and sorter execution separate.

Disposable mutation copies and packet `__pycache__` artifacts were removed after validation. The pre-existing `tmp/pdfs/` directory was left untouched. No `.gitignore` change was needed: the ignored categories remain correct, and every changed or new tracked artifact belongs in the repository.

## 5. Machine state and cost boundary

Measured at 2026-08-12 21:18 PDT:

- system RAM: **11.51 GiB free of 31.67 GiB**;
- GPU memory: **981 MiB used of 16,311 MiB**;
- `C:` free space: **604.4 GB**.

Nothing heavy used those resources. The session ran local text reads, hashing, stdlib parsing, compilation, help rendering, and small mutation fixtures on temporary packet copies. No network read, dependency install, raw-recording read, template-array pull, Rung 0, generator, or sorter run occurred.

## 6. Files created or updated

**Created**

- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`
- `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md`
- `agents/Codex/Session Summaries/HumanReport12.md`

**Updated**

- `Reproducibility Packet/README.md`
- `Reproducibility Packet/scripts/check_runbook_consistency.py`
- `Reproducibility Packet/scripts/audit_template_library.py`
- `Reproducibility Packet/scripts/derive_ccf_label_map.py`
- `Reproducibility Packet/scripts/screen_host_timing.py`
- `Reproducibility Packet/scripts/audit_amplitude_conventions.py`
- `agents/Claude/tools/mutation_test_runbook_checker.py`
- `chats/Claude-Codex/Reproducibility Packet Review/Reproducibility Packet Review - Active.md`
- root `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

**Deliberately unchanged**

- both Claim Sheets and all five in-force amendments;
- every packet result and both `requirements.txt` files;
- `Reproducibility Packet/DATA.md`;
- both agents' `references.md` files;
- `director_requests.md`.

## 7. Next steps

1. Claude genuinely re-reviews the packet state handed back in the packet review chat. If Claude edits, Codex must return to that exact state; silence or a later commit is not approval.
2. Claude reviews Draft 1 of the real-arm donor matching rule, especially the three decisions named in the handoff.
3. Only after the prose rule converges, implement it against synthetic fixtures and exhaustive small domains, then complete a separate same-state implementation review **before** constructing or opening a host-specific pool.
4. Keep matching-rule approval, implementation approval, host selection, placement calibration, exact U/Z/R configuration, independent balance/manipulation approval, generation, and sorter execution as separate gates.
5. No director action is needed.
