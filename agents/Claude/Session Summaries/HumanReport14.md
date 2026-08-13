# Human Report 14 — Claude

**Current date and time:** 2026-08-13 00:24 PDT

**Session:** Claude Session 14

**Phase at start:** Phase 2 — Execution. Amendments 1–5 `In force`. No host pinned, no donor selected, no sorter run, no scientific result. Both active review chats were Codex's move; Codex's Session 13 had blocked the donor-matching rule and named the unblocking step as mine.

**Phase at end:** unchanged. Amendment 6 is written and `Proposed` in both Claim Sheets and handed to Codex. Nothing entered force.

**Progress-report trigger:** none. Session 14 is not a multiple of eight, no phase closed, and no amendment entered *force* — Amendment 6 is a proposal only. The next count-based report is Session 16.

---

## Summary

This session had one job and it was well-defined before I started. Codex's Session 13 review rejected Draft 2 of the Tier A real-arm donor matching rule and ruled that one of the three defects could not be repaired inside that document: the rule aborts if the host recording kills even one of the sixteen CA1 donor waveforms, while the contract explicitly expects the project to survive losing up to six of them. Fixing that properly means changing contract text about how the fifty injection slots are shared out and how the negative-control arms are sized — and I am the default writer for both Claim Sheets. So Codex asked for a synchronized proposed **Amendment 6** before it revises the rule, and blocked its own lane behind it.

I wrote it in both sheets, implemented all seven elements Codex specified, and went past the specification in three places I judged were defects in the specification rather than latitude. I also accepted Codex's two other findings, one of which corrected an arithmetic claim I had written into its document last session.

The part of the session I did not expect was that generalizing the design turned an apparently arbitrary number in the contract into a determined one. Amendment 2 committed the project to abandoning Tier A if more than six of the sixteen donors die, and never said why six. Sixteen minus six is ten, which is exactly the number of synthetic units Slot 7 injects into every recording instance — so "at least ten survivors" and "a block of ten *distinct* donors can still be formed" are the same condition, matching exactly across the whole range rather than approximately. That mattered practically: it converted a constraint I was about to impose on my own authority into a reading of a contract already in force.

No host-specific pool was opened, no donor selected, no dependency installed, no network read, and nothing heavy run.

## 1. Startup and inherited state

`.agent-turn` named Claude and `.agent-session.lock` did not exist. I created the lock, re-read the turn, confirmed it still named Claude, and followed `AgentPrompt.md` in order: the complete `Project Details.md`, my continuity file, every chat summary and active chat involving me, then Codex's latest report.

The repository was clean at `f4419c4` (`Codex Session 13`). Both Claim Sheets matched their recorded approved hashes on disk before I touched them — `ac089232…` and `8bae94bc…` — and the pinned donor snapshot reproduced `a6c86402…`.

**Chat state on arrival.** The Reproducibility Packet Review chat had been concluded by Codex with a summary; my three handed-off states were approved and the one ruling I asked for was given (one command per side is a hard error, and a future two-command verification step becomes two numbered steps — which is the answer I had argued for). The Tier A Selection Review chat had nothing open on me. The Tier A Donor Matching Rule chat had Codex's Session 13 rejection and the request that produced this session's work.

## 2. What Amendment 6 does

`N` is the number of the injection zone's donors that survive the host-specific eligibility gates. The design is now defined for every `10 ≤ N ≤ 16` instead of only for sixteen:

- **`N` and its gates.** Every killed donor is recorded with the gate that killed it and the measured value that failed, and the killed list is published with the result. The numeric thresholds for those gates must be pinned in the tracked configuration *before* any donor is tested against them, so `N` cannot come out of a threshold nudged until the answer looks better.
- **`N < 10` fails Tier A** under the existing Slot 12.3 failure shape. This is Amendment 2's boundary restated, not moved.
- **The fifty occurrences split by quotient and remainder.** With `q = ⌊50/N⌋` and `r = 50 mod N`, exactly `r` survivors appear `q+1` times and the rest `q` times. At `N = 16` that is `2 × 4 + 14 × 3 = 50`, which is what Amendment 2 already said.
- **The control arm and both negative-control pseudo-arms follow `N`**, including the pseudo-selector's matching objective, its starting subset and its tie-breaks. The search cap does not move.
- **The removal set stays at all sixteen** regardless of how many survive.
- **Slot 13.9 is narrowed**: the Tier A claim is conditional on the exact survivors plus the published killed list.

## 3. The three places I went past what Codex asked for

These are the parts most likely to come back, and I flagged all three in the handoff as the things to resist.

**(a) "Placement feasibility" is not a per-donor property, so `N`'s gate set had to be split.** Codex's specification said `N` is the count surviving "the host-specific target eligibility gates." Slot 7's placement condition is that the injection zone supports *ten* feasible placements without overcrowding or label ambiguity — a joint property of the host and its site set, not a fact about any individual donor. Folding it into `N` would have made `N` ill-defined. Amendment 6 builds `N` from per-donor gates only and leaves the ten-placement condition a host gate: a host that fails it is rejected as a host rather than silently becoming a smaller `N`.

**(b) I fixed which survivors carry the extra occurrence and which block each occurrence lands in — and this narrows Amendment 2 rather than filling a silence in it.** Amendment 2 says each donor appears three or four times but never says *which* two get the fourth; that has been undetermined since it was written, and leaving it open would mean choosing it later with the survivors visible. The construction orders survivors by a SHA-256 digest of their identity under a seed fixed in the amendment, then deals the fifty slots round-robin. Two properties then fall out rather than being separately asserted: the first `r` ranks get the extra occurrence, and every block holds ten distinct donors.

The honesty point matters more than the mechanism. Amendment 2 randomizes "slot assignment" within the schedule, so pinning block membership takes a degree of freedom out of what it left free. That is a narrowing, and I wrote it into the amendment as one and listed it in the supersession paragraph rather than letting it read as clarification. My reason for preferring a fixed deal: at five blocks a random assignment can clump one donor's occurrences by luck and a balanced deal cannot, and donor-to-block assignment carries no treatment to confound, since blocks differ by nuisance seeds rather than by condition. The alternative needs a constrained sampler written into the contract. Codex can reject it.

**(c) Amendment 5's uniform-draw diagnostic is computed at `N`.** That expectation exists to mirror the arm actually being built, so at fewer than sixteen survivors it is a draw of `N`. Codex's list did not name it. The figures already recorded in Amendment 5 stay exactly as they are — they are pre-host diagnostics measured at sixteen, and they were never predictions.

## 4. Reading for the property rather than for the slot list found four more sentences

Codex named three commitments written in terms of a literal sixteen. Searching both sheets for the property rather than working from that list turned up four more. Three are mechanical (Amendment 3's "name all sixteen selected pairs," its "lexicographically lowest sorted sixteen-pair result," and "P1's fixed sixteen").

The fourth is the interesting one. **Amendment 4's Slot 13.10** conditions the Tier A result on "the sixteen CA1 templates named in Slot 13.9." It follows 13.9's narrowing by reference and needs no separate change, but it sits in an amendment that neither of us was looking at, whose header names entirely different slots. This is the third consecutive time the general form of a finding has paid: an amendment that changes a design *property* has to be checked against every in-force sentence that *describes* that property, not only against the slots its own header lists.

I also identified **three sixteens that must not be superseded** and said so explicitly, because a blanket "read sixteen as `N`" would have broken them: the CA1 library's hard ceiling of sixteen templates, "CA1's Tier A pool is all 16 templates" (the pre-host eligible pool), and the removal set. A supersession that is too broad is as much a defect as one that is too narrow, and it is the easier of the two to write by accident.

## 5. Codex's other two findings, accepted

**The source-count floor applies at every relaxation stage.** Accepted without reservation. I had "floor" doing the work of "last resort," which is not what Amendment 2 says. It is Codex's document to revise and nothing in Amendment 6 depends on which way it went.

**The 22% weighting claim was wrong, and worse than Codex said.** Codex called it denominator-dependent. Checking it rather than accepting the correction on the argument showed that the framing I thought I was using also fails: the disagreement between donor-equal and exposure weighting is each donor's weight under one versus the other — `0.0625 → 0.08` is **+28%** for two donors and `0.0625 → 0.06` is −4% for fourteen. My 22% divided by `0.08` instead of `0.0625`, so it was the wrong denominator for either comparison, not just for Codex's. The conclusion it was attached to survives; the number should go, and `(q+1)/q` is the invariant.

## 6. Challenges, and one thing I nearly got wrong

**Self-review caught two defects in my own draft before handoff.** I wrote the amendment, then read it adversarially against the contract rather than re-reading it for sense. That is where (a) surfaced — my first draft folded overcrowding into a per-donor count, which would have left `N` undefined — and where I noticed that (b) was a narrowing I had written as though it were a clarification. Both were in explanatory passages, which is exactly where my Session 13 note said to look: an explanatory sentence feels like a restatement of something already established, which is why it goes unchecked.

**A third defect was one I introduced during the fix.** Replacing the gate sentence left a following clause reading "the exact predicate for each of those gates," where "those gates" now pointed back past the newly inserted host-gate sentence. Caught by rendering the finished section and reading it as a reviewer would, not by reviewing the edit.

**A quote-character mismatch stopped the second file's write.** My correction script used curly quotes; both sheets use straight quotes exclusively. The script asserted an exact single match per edit and aborted before writing anything, which is why the accessible sheet was untouched rather than half-edited. I then found that the one curly pair in the whole technical sheet was the one I had just inserted, and normalized it. The lesson is the value of the assertion, not the typography: an edit script that requires exactly one match per replacement fails loudly instead of silently doing nothing or doing it twice.

**Everything numerical in the amendment was verified by running it, not by deriving it on paper.** The seed derivation was checked by confirming it reproduces Amendment 3's existing seed from Amendment 3's own string before I used the method for a new one. The rota was checked for every `N` from 10 to 16: totals are 50, the per-donor counts match the quotient/remainder rule exactly, and all five blocks hold ten distinct donors in every case. The boundary coincidence was checked across the range rather than at the endpoints.

## 7. Verification and repository integrity

- Both sheets: `git diff --numstat` shows **58/0** and **48/0** — pure additions, no deletion in either file, so the append-never-overwrite rule holds at the git level and not merely by intention.
- Every write was read back and compared to the intended bytes; both sheets carry six amendments, five `In force` and one `Proposed`, and remain synchronized.
- The chat append was verified by recording the pre-write tail and line count, asserting the Session 14 header was absent beforehand, and confirming afterwards that the prior content is an exact prefix and the new header occurs exactly once.
- The root README's running log is append-only; its single deletion is the banner's "Last updated" date, which is what that field is for.
- `git diff --check` is clean.

## 8. Files created or updated

**Created**

- `agents/Claude/Session Summaries/HumanReport14.md`

**Updated**

- `Claim Sheet.md` — proposed Amendment 6 appended. SHA-256 `40d8b0a698ea3dcedb974b9d61d4de1bc773d32006c7fa3d54f4a5ff06a335e6`
- `Accessible Claim Sheet.md` — the synchronized plain-language Amendment 6 appended. SHA-256 `cbc3b00660f565ae9ebfd59623fb28e0b9b1b81bb3ae1dd380141ae307208b66`
- `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md` — the Session 14 handoff
- `README.md` (repository root, Live-Run) — one running-log entry and the banner date
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

**Deliberately unchanged**

- Amendments 1–5 and all base contract text
- `agents/Codex/Tier A Real-Arm Donor Matching Rule.md` — Codex's to revise, and only after Amendment 6 converges
- `agents/Claude/Tier A Host and Injection Zone Selection.md` — same-state approved at Draft 7; its fixed-sixteen descriptions become narrowed by reference when and if Amendment 6 enters force, and corrections propagate forward rather than into an approved artifact
- The Reproducibility Packet, both `requirements.txt` files, `DATA.md`, `references.md` (no new source), `director_requests.md` (no new director-only dependency), and `.gitignore` (nothing new to exclude; the session's scratch stayed in the system temporary directory)

## 9. Machine and execution boundary

Measured at 2026-08-13 00:20 PDT: system RAM **10.00 GiB free of 31.67**, GPU memory **987 MiB used of 16,311**, `C:` **649.1 GB free**.

Nothing heavy ran and nothing needed a headroom check. The session's only execution was stdlib hashing and arithmetic plus one read of the tracked 2 MB donor snapshot. No network read, no dependency install, no raw-recording read, no template-array pull, no Rung 0, no generator and no sorter run. All scratch work stayed under the system temporary directory; no background job was left running.

## 10. Next steps

1. **Codex reviews Amendment 6 in both sheets**, and specifically the three places I went past its specification: the per-donor/host gate split, the fixed rota deal (which narrows Amendment 2), and computing Amendment 5's uniform-draw expectation at `N`.
2. **Once Amendment 6 converges**, Codex revises the matching rule: the source-count floor at every relaxation stage, every cardinality generalized to `N`, and the 22% explanation removed.
3. **Only after both the amendment is in force and the prose rule is same-state approved** may implementation and deterministic tests begin. The host-specific pool stays closed until that later implementation review converges.
4. **My own lane is next for me.** Host selection still has three gates open and mine — drift, noise, and post-rescaling effective SNR. Drift is the awkward one and the natural next piece: the metadata column that looks like it answers it reaches physically impossible values, so the quantity has to be *defined* before it can be measured.
5. **No director action is needed.** The Phase 1 contract-review request remains open and non-blocking.
