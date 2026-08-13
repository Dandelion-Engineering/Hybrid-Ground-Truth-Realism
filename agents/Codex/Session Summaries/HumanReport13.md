# Human Report 13 — Codex

**Current date and time:** 2026-08-12 23:09 PDT

**Session:** Codex Session 13

**Phase at start:** Phase 2 — Execution. Amendments 1–5 `In force`; no host pinned; the packet checker and pre-pool real-arm donor matcher were both in active exact-state review.

**Phase at end:** unchanged. The packet checker review converged and its scoped chat concluded. The donor-matching prose review remains open because Draft 2 would violate the in-force provenance floor and silently tighten the predeclared donor-loss boundary.

**Progress-report trigger:** none. Session 13 is not a multiple of eight, no phase closed, and no amendment entered force. The next count-based report is Session 16.

---

## Summary

This session closed one review cycle and deliberately kept another open.

Claude's two additional packet-checker repairs are correct. The checker now rejects a second runnable command whether it appears as another command fence in one README step or later in a script's `Example` block. I kept the one-command-per-side invariant as a **hard error**: if the future verification workflow genuinely needs two commands, the runbook must represent them as two numbered actions with separate purposes and outputs. A warning would allow the packet to pass while showing a reader an unchecked command, recreating the defect the checker exists to prevent. I reran the live checker, all fifteen mutations and every script's `--help`, explicitly approved Claude's three exact states, concluded the chat and wrote its summary.

The real-arm matching rule did not pass owner re-review. Claude correctly found that Draft 1's hard-sixteen guard contradicts Amendment 2, which predeclares Tier A failure only when more than six of the sixteen zone donors die at host-specific gates. I chose the contract-consistent resolution: parameterize the design by `N`, the 10–16 surviving donors, preserve the fifty-slot budget with an exposure-balanced quotient/remainder rota, generalize the pseudo construction to the same `N`, and keep Amendment 5's removal set Z at the full sixteen zone donors. Because that touches in-force language in Amendments 2 and 3 and Slot 13.9, it requires a synchronized proposed Amendment 6 before the prose rule can converge.

The same review found two additional defects. Draft 2 allowed session- and subject-level assignments to violate source-count equality, even though Amendment 2 calls that equality the **floor** under the finer provenance attempts. The floor must apply at every relaxation stage; session or subject blocking is admissible only when a complete assignment also preserves the target's number of contributing `dataset` sources. And Draft 2's “22%” explanation of exposure weighting is denominator-dependent: with sixteen donors, the two four-occurrence donors have one-third more exposure weight than the three-occurrence donors after the irrelevant common factor is removed. The donor-equal decision remains right; the percentage should be removed and generalized algebraically for `N`.

No host-specific pool or edge table was opened. No donor was selected. No contract changed, no dependency was installed, and no Rung 0, generator or sorter run occurred.

## 1. Startup and inherited state

`.agent-turn` named Codex and `.agent-session.lock` did not exist. I created the lock, re-read the turn, confirmed it still named Codex, and followed `AgentPrompt.md` in order: the complete Project Details, Codex continuity, every chat summary and active chat involving Codex, then Claude's latest report and the artifacts it handed back.

The repository was clean at `0f37ae7` (`Claude Session 13`), and local `main` matched `origin/main`. Every handed hash matched on disk:

- packet README `3b07aa5b94203d3f4c826be7aac40e6550c2a13e7d3b45c997399a84af3df4a1`;
- checker `4eb9401825ec2a4561abf46dc7dc82d89ea316722d338bba9e84bd747d83c651`;
- mutation harness `d64134b1485a8550412c1eb7fba7fd98ab509471050cad71a41fc8f704d5acc3`;
- donor matching Draft 2 `f4ab71c3216d172641706a199d0536520da538aff906eb29d94f06f3d6620310`;
- synchronized Claim Sheets remained unchanged at `ac089232851705be86e8674987f29afd7fa553e0e55e08049868761549465b28` / `8bae94bcc84928766214fea64eba234af6a524804afe11bd7eb16504d265c17f`.

## 2. Reproducibility Packet review — converged

### What I accepted

Claude generalized the reason behind my earlier fence-parser repair and found the same early-stop failure at two additional boundaries:

1. a second `bash` fence after the first correct fence in the same numbered step;
2. a second indented command later in the same `Example` block, after a blank line, which `--help` still prints.

Both were real escapes. The repaired README parser keeps a step region open until a new level-two section and rejects a second command fence inside that region. The docstring parser collects every indented non-empty line after the one `Example` marker and requires exactly one. The parser's docstrings and the packet README now state the invariant they enforce.

### Hard-error ruling

I kept the invariant as a hard error. The reproducibility-packet playbook defines a step as one named script, one exact command and its outputs. A future verification workflow needing preparation plus rendering should expose two steps. The current Slot 8 promise remains compatible: `verify_realism.py` may still be one command that produces two panels and a verdict.

### Validation and approval

- Live checker: ten numbered steps agree.
- Mutation harness: clean control passes; **15 of 15** deliberate defects are caught for their stated reasons.
- All eleven packet scripts render `--help` successfully.
- No packet result, scientific command, dependency, licence statement or contract state changed.

I explicitly approved the three hashes above. Claude and Codex now approve the same bytes. The transcript was renamed to `Reproducibility Packet Review - Concluded.md`, and `Summary.md` records the final states and boundaries. The packet itself remains in progress: five archive-reading steps, the headline pipeline and `verify_realism.py` await later work.

## 3. Tier A real-arm donor matching rule — blocked with a defined next path

### Accepted parts of Draft 2

I accept:

- common U-derived scaling for the un-removed/post-removal counterfactual, with R-derived standard deviations reported as a non-governing sensitivity diagnostic;
- donor-equal rather than exposure-weighted edge cost;
- exact equality of the two arms' distinct source counts at the count floor;
- the obligation to solve that global cardinality constraint exactly rather than pretend an ordinary assignment solver enforces it;
- source-concentration outputs, not counts alone;
- naming the sampling model for any comparator shown beside the realized zone-donor count;
- Claude's support tool staying outside the packet as review-only evidence.

I reran `zone_provenance_headroom.py` through the project venv. It reproduced the pinned snapshot SHA-256 `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`, 2,183 Neuropixels 1.0 rows, sixteen CA1 donors, four source insertions at `[6, 5, 3, 2]`, and non-CA1 insertion supply ceilings 82, 75, 58 and 6. Those are pre-host upper bounds only.

### Blocking defect 1 — the floor disappeared at intermediate stages

Draft 2 made source-count equality operative only after insertion, session and subject blocking all failed. That contradicts Amendment 2's “floor, not target” language. The corrected order is insertion+count, session+count, subject+count, and finally unrestricted hard-eligible edges+count. Only infeasibility under both the stage's pairwise rule and the count floor permits relaxation. The exact cardinality solver obligation therefore applies at stages 2–4 wherever equality is not automatic.

### Blocking defect 2 — one killed donor became an undeclared tier failure

Claude's Section 11 diagnosis is correct. I rejected the stricter hard-sixteen option. The intended Amendment 6 shape is:

- `N` equals the host-eligible CA1 target count, with every killed key and reason recorded;
- `10 <= N <= 16` continues; `N < 10` triggers Slot 12.3;
- the fifty real-arm occurrences give each survivor `floor(50/N)` or `ceil(50/N)` appearances, with `50 mod N` receiving the extra occurrence;
- real control and pseudo P2 select `N` no-reuse partners; pseudo P1 selects `N` fixed donors and uses the same exposure schedule;
- Z remains the full sixteen injection-zone keys for Amendment 5 removal even if the target side has fewer survivors;
- the claim is conditional on the exact surviving `N` templates and the published killed list.

Claude is the default Claim Sheet writer. The next turn should write synchronized proposed Amendment 6 in both sheets before the matcher is revised and handed back. Nothing in this decision opens the host pool.

### Blocking defect 3 — weighting arithmetic

Under the current sixteen-donor rota, fourteen donors have exposure weight `3/50` and two have `4/50`. Factoring out the common `3/50` leaves the two extras weighted `4/3` relative to the rest. The draft's 22% statement depends on the denominator chosen and is not the clean invariant. Under variable `N`, with `q = floor(50/N)`, exposure weighting gives the extra-occurrence donors `(q + 1)/q` times the influence of the others. Donor-equal cost removes that rota dependence; the revised rule should state that without a percentage.

## 4. Append-only and repository integrity

Before both chat writes I recorded the UTF-8 physical tail and pre-write line counts, verified a unique multi-line EOF anchor, appended only through that anchor, and re-read the physical tails. The new Session 13 header occurs exactly once after each recorded boundary. `git diff --numstat` showed 30/0 and 45/0 additions/deletions before the packet transcript rename. `git diff --check` found no whitespace error.

The packet review chat was concluded only after the exact-state approval landed. The donor-matching chat remains active. No concluded artifact was reopened.

## 5. Files created or updated

**Created**

- `agents/Codex/Session Summaries/HumanReport13.md`
- `chats/Claude-Codex/Reproducibility Packet Review/Summary.md`

**Updated or renamed**

- `chats/Claude-Codex/Reproducibility Packet Review/Reproducibility Packet Review - Active.md` → `Reproducibility Packet Review - Concluded.md`
- `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

**Deliberately unchanged**

- both Claim Sheets and Amendments 1–5;
- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` at Draft 2, because the contract amendment must precede a convergent revision;
- packet source/result files, all requirements files and `DATA.md`;
- root `README.md`, whose latest entry already records both Session 13 findings without implying approval;
- both references files and `director_requests.md`, because no new external source or director-only dependency arose;
- `.gitignore`, which already ignores the live coordination files and local scratch classes and needs no new rule.

## 6. Machine and execution boundary

Measured at 2026-08-12 23:09 PDT: system RAM **10.73 GiB free of 31.67**, GPU memory **987 MiB used of 16,311**, and `C:` **604.2 GB free**.

Nothing heavy ran. Work was local text reading, hashing, stdlib parsing, `--help` rendering, the mutation harness on isolated system-temp packet copies, and one read of the tracked 2 MB donor snapshot. The validation scratch was isolated under the system temporary directory and no repository file was written by it. No network read, dependency installation, raw-recording read, template-array pull, Rung 0, generator or sorter run occurred.

## 7. Next steps

1. Claude writes synchronized proposed Amendment 6 in both Claim Sheets, covering variable `N`, the quotient/remainder schedule, pseudo-arm generalization, the `N < 10` failure boundary, full-sixteen Z removal and the surviving-set non-transfer statement.
2. Codex revises the matcher only after that proposal exists: enforce source-count equality at every relaxation stage, generalize every cardinality/output to `N`, remove the 22% explanation and return an exact approved state.
3. Claude and Codex converge first on Amendment 6, then on the prose rule. Only after both are in force/approved may implementation and deterministic tests begin; the host-specific pool remains closed until that later implementation review converges.
4. Packet work continues in a new scoped chat when one of the five archive steps or a new headline script changes. The concluded review is not reopened.
5. No director action is needed. The existing Phase 1 contract-review request remains open and non-blocking.
