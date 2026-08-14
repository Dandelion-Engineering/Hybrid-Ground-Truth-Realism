# Human Report 23 — Codex

**Date and time:** 2026-08-14 08:13 PDT
**Phase:** 2 — Execution
**Session type:** Exact-state review of Claude Draft 20 and direct repair of the per-unit audit interpretation

---

## Summary

Claude handed back three owner-approved states: host-selection Draft 20, the band-drift utility, and its synthetic harness. I verified all three SHA-256 digests before opening them, read the full active review context and §§15–16, read Claude's `HumanReport23.md`, and reran the handed-off validation rather than accepting its reported outputs.

Draft 20 correctly established two boundaries: the per-unit audit values have no unit-level null, and the concentration or scatter of their worst-window starts is not evidence by itself. I nevertheless blocked Draft 20 unchanged because it turned one homogeneous synthetic result into another universal direction. It called the band statistic's `Q95_null` systematically narrower than a single trace's noise floor. That is not guaranteed when unit traces are heterogeneous.

A deterministic quiet counterexample reverses the asserted ordering. Five temporally valid units share one regular spike-time grid. One unit is exactly flat and four carry independent 18 µm Gaussian depth-estimation noise. The band remains measurable; the flat unit's own-worst ten-bin excursion is `0 µm`, while the median-across-units band null has `Q95_null = 16.598127811340 µm`. The valid conclusion is therefore not that the reverse direction holds, but that the two statistics have no fixed ordering and cannot grade one another in either direction.

I directly repaired the artifact and the utility's documentation, made the counterexample permanent in the synthetic harness, and explicitly approved the resulting Draft 21 exact states. All executable utility code is unchanged. Section 16 and both implementation states remain open pending Claude's genuine owner re-review. The archive-reading CLI remains forbidden and no candidate was read.

**No host is pinned. No candidate drift, noise or effective-SNR value exists. No target manifest, donor selection, dependency installation, network/archive/raw-data read, Rung 0, generator or sorter run occurred. No scientific result exists.**

## Work completed

### 1. Startup and context-first review

- Read the automation memory, then `.agent-turn`; it named `Codex`.
- Confirmed `.agent-session.lock` was absent, created it, and re-read `.agent-turn`; it still named `Codex`.
- Read `AgentPrompt.md` and all of `Project Details/Project Details.md`.
- Read Codex's continuity, every concluded chat summary involving Codex, and the entire 1,345-line active Tier A selection transcript before replying.
- Read `Playbooks/review-cycle.md` and `Playbooks/reproducibility-packet.md` before reviewing the handed-off artifact and packet utility.
- Read `Playbooks/live-run-readme.md` before appending the public forward correction.
- Read Claude's latest `HumanReport23.md` and its referenced exact states as the required recent-work cross-review.

### 2. Exact handoff verification

The three handed-off digests matched before review:

- Draft 20: `e2cbcd60dd4d13218ad414a4b46e9ef773ee4e4f0b0b596a233e5309f5ebfeb5`;
- `band_drift.py`: `228f045c5c94d31cf9faa4ba3fd9391c62a42192a45f23d2842c256414690a47`;
- `test_band_drift.py`: `77637e10f0435bfa3d72a97264e15063f9c4afa6b791bd0d678bc4fd5f5560cd`.

Before editing, I reran the handed-off 77-check harness, the three-claim probe, Codex's two safety counterexamples, and the ten-step packet runbook checker. The harness and both counterexamples reproduced. The claim probe required its documented `--module` argument; I reran it with the handed-off module and all three probes passed.

### 3. The remaining one-way claim

Draft 20's homogeneous no-movement fixtures were useful and correctly measured:

- at 9 units, the smallest per-unit own-worst excursion was about `1.62 × Q95_null`;
- at 14 units, about `2.13 ×`;
- at 25 units, about `2.76 ×`.

Those fixtures show what the across-unit median does under one homogeneous independent-noise family. They do not prove that the band null is narrower than every single-unit audit value under arbitrary unit composition and noise.

The counterexample uses 61 full-width bins with ten regularly placed spikes per bin for five units. One unit's depth is constant. Four units have independent Gaussian depth-estimation noise. Every unit clears temporal inclusion and every bin clears the five-unit validity floor. The result is:

- measurable candidate;
- flat unit own-worst excursion: `0 µm`;
- band `Q95_null`: `16.598127811340 µm`;
- at least one per-unit value below the band null.

This establishes only non-comparability. Depending on composition and noise, the band null can sit below or above a particular unit's audit value. It cannot serve as that unit's null.

### 4. Draft 21 repair

Draft 21 preserves Draft 20's useful decisions and narrows the interpretation to what the evidence supports:

- `Q95_null` grades the median-across-units band statistic, not a single trace;
- its ordering against any one per-unit excursion is not fixed;
- neither `Q95_null` nor the gate threshold `L` grades the per-unit outputs;
- within-recording magnitude heterogeneity can flag a pattern consistent with movement suppressed by the band median, but heterogeneous depth-estimation noise can produce it too;
- the pattern is therefore published only as a limitation and carries no threshold, attribution, verdict or effect on the pinned order;
- window-start concentration and scatter remain non-evidentiary on their own.

The utility's two changes are docstrings only. Removing every docstring from the Draft 20 and Draft 21 syntax trees leaves identical abstract syntax trees, so no executable utility line changed.

### 5. Permanent test and exact states

The harness now includes the heterogeneous quiet counterexample beside Claude's homogeneous no-movement and common-ramp fixtures. It also corrects its opening count from four defect-derived cases to five.

I explicitly approved and handed Claude these exact states:

- `agents/Claude/Tier A Host and Injection Zone Selection.md` Draft 21 — SHA-256 `bd0f678af4d27862d55044be010524782d1d80bb2bccd6a873cc06e70fa3946c`;
- `Reproducibility Packet/scripts/utils/band_drift.py` — SHA-256 `3420dec17a9717abc7a5078e53a5826bc78c9bd8ad0ec2bca07fdbcc8da70063`;
- `agents/Claude/tools/test_band_drift.py` — SHA-256 `fe889703d67b4ee97a9a6a431dbd9dde389216687f07b139db34f0e2df5c317d`.

This does not close the review cycle. Claude must re-open and approve these exact bytes or edit and return new states. The issue is a new claim-scope finding rather than a repeated disagreement, so no specific dispute exists to escalate under the review-cycle playbook.

### 6. Public heartbeat and append-only record

The root public README received one lean forward correction. It preserves Claude's prior homogeneous-fixture entry and adds the stronger conclusion: the band null and individual excursions have no fixed ordering; individual heterogeneity can expose a limitation but cannot attribute it to movement rather than heterogeneous estimation noise. The entry remains explicitly no-result-bounded.

The active chat append passed the physical-tail safeguards:

- pre-write: 196,789 bytes, 1,345 newline-terminated lines, SHA-256 `cab85070a47f5e3596777d37a4ae115472fb21ef6f49ab7178b713e6b66c6fd8`;
- that exact byte sequence remains the prefix after the append;
- the Codex Session 23 header occurs exactly once and only after the old EOF;
- the file decodes as strict UTF-8 and the new physical tail was read back.

## Validation

- `agents/Claude/tools/test_band_drift.py`: **79 checks, 0 failed** at the pinned 200 permutations.
- `agents/Claude/tools/probe_band_drift_claims.py --module Reproducibility Packet/scripts/utils/band_drift.py`: **3 of 3 probes passed**.
- `agents/Codex/tools/probe_draft16_safety_claims.py`: both earlier counterexamples reproduce to the digit against the repaired module.
- Draft 20 versus Draft 21 utility: docstring-stripped abstract syntax trees are identical.
- `Reproducibility Packet/scripts/check_runbook_consistency.py`: **10 of 10 steps agree**.
- All packet, Claude-tool and Codex-tool Python sources compile in the project virtual environment.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` remain unchanged at `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365` / `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`.
- `git diff --check` passed before closeout.
- No dependency was installed and no network, archive or raw-data read occurred.

## Challenges and reasoning

**Keeping a valid local result from becoming a universal property.** Claude's homogeneous fixtures are correct and valuable. The defect was the jump from those measured fixtures to “systematically narrower.” The repair keeps the evidence and deletes only the unsupported direction.

**Avoiding the equal-and-opposite claim.** The heterogeneous counterexample does not show that the band null is generally wider. It proves that either ordering is possible. Draft 21 therefore says the statistics are non-comparable rather than replacing one one-way claim with another.

**Preserving a useful audit without turning it into attribution.** A subgroup separated in magnitude over overlapping windows may be consistent with suppressed movement, but heterogeneous estimation noise can mimic it. Calling it a limitation flag rather than evidence of movement preserves visibility without creating a post-hoc gate or an interpretation the current design cannot justify.

## Files created or updated

| Path | Change |
|---|---|
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | Draft 21 direct repair and exact-state handoff. |
| `Reproducibility Packet/scripts/utils/band_drift.py` | Narrowed two docstrings to the non-comparability boundary; executable syntax unchanged. |
| `agents/Claude/tools/test_band_drift.py` | Added the quiet heterogeneous counterexample; 79 checks total. |
| `chats/Claude-Codex/Tier A Selection Review/Tier A Selection Review - Active.md` | Append-only exact-state review and handoff. |
| `README.md` | Lean public forward correction, no-result-bounded. |
| `agents/Codex/Session Summaries/HumanReport23.md` | This report. |
| `agents/Codex/README.md` | Workspace map and current review state refreshed. |
| `agents/Codex/Summary of Only Necessary Context.md` | Completely rewritten for Codex Session 24. |

No progress report was due: this is Codex Session 23, no phase changed and no Claim Sheet amendment entered force. No new source was used, so `agents/Codex/references.md` is unchanged.

## Machine state

Measured at 2026-08-14 08:13 PDT: **3.92 GiB RAM free of 31.67 GiB; 1,036 MiB GPU memory used of 16,311 MiB; 582.8 GiB free on `C:`.** Nothing heavy ran. The harness and probes use small synthetic arrays; this measurement is a momentary diagnostic and not later authorization.

## Next steps

1. Claude genuinely owner-reviews Draft 21 and both implementation hashes.
2. If Claude approves those exact bytes, §16 and the numerical utility/harness loop close.
3. Only then may Claude write the archive-reading CLI and its scoped packet step/review; the CLI itself must receive same-state approval before candidate measurement.
4. Only after that separate approval may rank 1 be read for a drift value.
5. Noise, post-rescaling effective SNR, exposure-schedule/placement, matcher implementation, target manifest, joint placement, balance/manipulation, generation and Rung 0 remain separate gates.
