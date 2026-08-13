# Summary of Only Necessary Context — Codex

**Rewritten at the end of Codex Session 13 · 2026-08-12 23:09 PDT**

**Next Codex session will be Session 14.** No count-based progress report is due until Session 16.

## Current phase and immovable boundary

**Phase 2 — Execution is open. No scientific result exists.** No host is pinned. No host-specific eligible pool or rendered matching edge table exists. No template-array pull, dependency installation, raw-recording download, Rung 0, hybrid generator run or sorter run occurred in Codex Session 13.

The public state remains `In Progress`. Packet documentation and a pre-pool matcher are design/reproducibility work, not evidence about whether realism changes measured sorter accuracy.

## Contract state

The synchronized contract remains unchanged:

- `Claim Sheet.md`: SHA-256 `ac089232851705be86e8674987f29afd7fa553e0e55e08049868761549465b28`
- `Accessible Claim Sheet.md`: SHA-256 `8bae94bcc84928766214fea64eba234af6a524804afe11bd7eb16504d265c17f`

Amendments 1–5 are all `In force`. No amendment moved in Session 13.

The next required contract work is a synchronized proposed **Amendment 6**. It must resolve the in-force expectation that Tier A survives losing up to six of the sixteen CA1 donors:

- `N` is the exact host-eligible CA1 target count; publish every killed key and reason;
- continue for `10 <= N <= 16`; Slot 12.3 governs at `N < 10`;
- distribute fifty real-arm occurrences so each survivor appears `floor(50/N)` or `ceil(50/N)` times and exactly `50 mod N` receive the extra occurrence;
- pseudo P1 uses a fixed `N`-template subset, pseudo P2 uses `N` matched controls and both use the same `N`-donor schedule;
- Amendment 5's Z remains the **full sixteen-key injection-zone donor set** even when the target side has fewer survivors;
- the Tier A claim is conditional on the exact surviving `N` templates and killed-donor list.

Claude is the default Claim Sheet writer. The matcher is not revised into a convergent state until the synchronized Amendment 6 proposal exists.

## Reproducibility Packet review — concluded

Concluded chat: `chats/Claude-Codex/Reproducibility Packet Review/`.

Final same-state approved changed hashes:

- packet `README.md`: `3b07aa5b94203d3f4c826be7aac40e6550c2a13e7d3b45c997399a84af3df4a1`
- checker: `4eb9401825ec2a4561abf46dc7dc82d89ea316722d338bba9e84bd747d83c651`
- Claude mutation harness: `d64134b1485a8550412c1eb7fba7fd98ab509471050cad71a41fc8f704d5acc3`

The checker keeps runnable examples in every script docstring and compares them character-for-character with the numbered packet step. One command per side is a **hard error**: one `bash` fence with one line per step and one indented command per `Example` block. A genuine two-command future workflow becomes two numbered steps. The live checker passes ten steps; the clean mutation control passes and all fifteen mutations are caught; all eleven packet scripts render `--help`.

The packet remains incomplete as a Phase 2/3 artifact. Five archive-reading steps were not re-run during the runbook work; the headline pipeline and Slot 8 `verify_realism.py` do not exist because no result exists. Future packet changes begin a new scoped review chat rather than reopening the concluded one.

## Real-arm matching rule — active and blocked

Artifact: `agents/Codex/Tier A Real-Arm Donor Matching Rule.md`

Active chat: `chats/Claude-Codex/Tier A Donor Matching Rule/Tier A Donor Matching Rule - Active.md`

Draft 2 SHA-256: `f4ab71c3216d172641706a199d0536520da538aff906eb29d94f06f3d6620310`

Claude explicitly approves Draft 2. Codex **does not** approve those bytes. Accepted pieces are common U-derived scaling with an R-derived diagnostic, donor-equal matching, exact source-count equality, exact constrained optimization, concentration outputs, named count comparators, global no-reuse assignment and gate separation.

Three repairs are required after Amendment 6 is proposed:

1. **Source-count equality is the floor at every provenance stage.** Try insertion+count, session+count, subject+count, then unrestricted hard-eligible edges+count. A stage relaxes only when no complete assignment satisfies both its pairwise rule and the count floor. The exact global-cardinality solver obligation applies wherever equality is not automatic.
2. **Generalize every target/candidate cardinality and output to `N = 10…16`.** Keep Z at the full sixteen zone keys. Fail at `N < 10`, not at the first killed donor.
3. **Remove Draft 2's 22% exposure-weight claim.** With `q = floor(50/N)`, exposure weighting gives the `50 mod N` extra-occurrence donors `(q + 1)/q` times the influence of the others. Donor-equal matching prevents that arbitrary rota choice from changing the selected partner; no percentage is needed.

Claude's `agents/Claude/tools/zone_provenance_headroom.py` is accepted as review support outside the packet. Codex independently reran it against the pinned snapshot: 2,183 NP1.0 rows, sixteen CA1 donors over four sources `[6, 5, 3, 2]`, with insertion-stage non-CA1 supply ceilings 82, 75, 58 and 6. These are upper bounds, not host-specific feasibility.

The matcher implementation and deterministic tests remain a separate same-state review **after** Amendment 6 and the prose rule converge and **before** any host-specific pool or edge table is constructed or opened.

## Host selection and Rung 0 remain unchanged

`agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 7 at `13c192d3478ffdba35d756715ef2236d52a3cb31e6156dc818fd5c002dd19d01` is same-state approved for its declared strategy/evidence scope, not as a host selection.

Candidate order remains:

1. CSHL047 Probe01, session `b52182e7`;
2. NYU-12 Probe01, session `a8a8af78`;
3. CSHL047 Probe00, session `b52182e7`.

Claude owns drift, noise and post-rescaling effective-SNR host gates. Codex owns the two-part footprint/placement calibration, independent balance/manipulation gate, Rung 0, sorter-panel decision and inference/negative-control harness.

Rung 0 remains unrun. It must construct and pin the pre-injection host substrate, avoid phase-shifting injected templates twice, pin the exact approximately 60-second segment, resolve dependencies in the project venv, and take fresh RAM/VRAM immediately before heavy work under Amendment 1's live resource guards. The current venv still pins only `h5py==3.16.0` and `numpy==2.5.2`.

## Gate order — do not collapse

1. Amendment 6 proposal and exact-state convergence;
2. revised matching prose convergence;
3. matching implementation/test convergence before pool access;
4. host selection and placement calibration;
5. exact U/Z/R manifests, edge table, two matching outputs and selected IDs;
6. independent Tier A balance/manipulation approval;
7. generation authorization;
8. Rung 0/sorter execution authorization.

Reviewer edits, downstream use, a later commit or silence do not substitute for same-state approval.

## Public and director state

- Root `README.md` remains State A / `In Progress`. Its latest entry already records the packet-checker repair and the hard-sixteen contract conflict; no new heartbeat was needed in Session 13.
- The Phase 1 director contract-review request remains open and non-blocking.
- No new director action is needed.
- No progress report was due in Session 13.

## Validation and machine record from Session 13

- Packet checker: ten steps pass.
- Mutation suite: clean control passes; 15 of 15 mutations caught.
- All eleven packet scripts rendered `--help`.
- Donor provenance support tool reproduced the pinned snapshot digest and recorded counts.
- Append-only chat safeguards passed: each Session 13 header occurs exactly once after its pre-write line boundary, and the active-chat diffs were addition-only before the packet transcript rename.
- `git diff --check` passed during closeout.
- 2026-08-12 23:09 PDT: 10.73 GiB RAM free of 31.67; 987 MiB VRAM used of 16,311; 604.2 GB free on `C:`. Nothing heavy ran.

`agents/Codex/Session Summaries/HumanReport13.md` contains the full review rationale, validation evidence, exact hashes and file list.
