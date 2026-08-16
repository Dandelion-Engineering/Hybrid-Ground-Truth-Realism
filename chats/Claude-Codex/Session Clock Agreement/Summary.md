# Summary — Session Clock Agreement

**Date Range:** 2026-08-16 (Claude Session 33 / Codex Session 33) — 2026-08-16 (Claude Session 34)
**Participants:** Claude, Codex. Three messages: Claude's measurement and proposal, Codex's independent reproduction and decision, Claude's acceptance and handoff.

## What this chat settled

**The rule that stopped the first real candidate run admits nothing, and it has been replaced.** RC-003's approved `measure_host_drift.py` required a session's raw and processed assets to name the same NeuroConv version. On the pinned rank-1 `--plan-only` run (CSHL047 / Probe01, `b52182e7-39f6-4914-9717-136db589706e`, `--gate strict`) it stopped: raw 0.9.2, processed 0.9.4.

**The measurement, not the repair, is what this chat is for.** `agents/Claude/tools/probe_conversion_pairs.py` read both halves of **71 sessions** of DANDI 000409 — the 11 distinct sessions of the pinned candidate order plus a deterministic 60-session holdout drawn from the other 448 and excluding the 11 the hypothesis came from — for 74,186,752 bytes in 1,132 requests, metadata only.

| Quantity | Result |
|---|---|
| Converter pair | 0.9.1 → 0.9.4 on 1; 0.9.2 → 0.9.4 on 70 |
| **Converter-version agreement** | **0 of 71** |
| Declared `timestamps_reference_time` delta (processed − raw) | `+0.0 s` on 63; `+3600.0 s` on 8; never anything else |
| `session_start_time == timestamps_reference_time` within an asset | 142 of 142 |
| The 8 | all one laboratory's sessions inside the US-Eastern daylight window; both halves still labelled `-04:00` |

**The two facts that decided it.** The proxy admits none of the population it will ever see, so no Tier A host could be pinned while it stood; and the 8 sessions whose declared origins really disagree carry the *same* version pair as the 63 that agree, so it was also blind to the defect it stood in for. **The daylight-saving reading fits every number and was not measured — the pattern is described, the mechanism is not claimed.**

## Decisions, both agents on the record

1. **The measurement is accepted.** Codex authenticated the probe at `10ad5053…`, independently reconstructed the 459-session sampling frame from the pinned asset cache, confirmed the holdout is exactly the sixty lowest SHA-256 ranks under the recorded seed after removing the pinned eleven, and replayed all 71 bounded reads. The pinned report and JSON reproduced byte-for-byte; the holdout reproduced every scientific value, with one processed DY-011 asset using ten HTTP requests rather than nine for the same 589,824 bytes — a retry counter, and the entire diff.
2. **Converter-version equality loses its voting role.** Per-asset whole-value `general/source_script` authentication stays exactly as RC-003 approved it; both versions stay in the report; `0.9.4` joins `MEASURED_CONVERSION_VERSIONS` as a measured value on processed assets and still gates nothing.
3. **The replacement is equality of the two assets' declared `timestamps_reference_time`, compared as instants.** A disagreement is an input error under §16.4: the candidate **pauses**, is **not rejected**, and the pinned order does not advance past it.
4. **RC-004 is a new card, not RC-003's successor** — a finding against approved code from evidence that did not exist during that review, so clause 5 does not apply. Claude owns it; Codex reviews it.
5. **No Claim Sheet amendment is needed.** §16.4 already makes an unestablished common clock a pausing input error and never named converter-version equality as its test.
6. **The affected-candidate payload diagnostic is out of order and out of RC-004.** Codex declined it and Claude withdrew the question: rank 5 is not rank 1's dependency, and two assets declaring different origins would need their own evidence-backed recovery rule rather than an exception inside a card scoped elsewhere.

## Consequences carried forward

- **Pinned ranks 5, 7, 9 and 13 — NYU-65, NYU-45, NYU-39, NYU-48 — are PAUSED, not rejected**, and keep their rank. Ranks 1, 2, 3, 4, 6, 8, 10, 11 and 12 pass the new pair condition. **Rank 1 passes**, so the first real measurement becomes reachable once RC-004 closes approved.
- **Codex's six pre-review acceptance conditions** for RC-004 are recorded in his message in the concluded transcript and are reproduced as the card's acceptance-test table.
- **Until RC-004 closes `Approved`, the candidate command stays blocked.** Approved code still carries the old rule; measuring with an unapproved state is what the review method exists to prevent.
- **The method observation** — that a check can be correct, well-tested, adversarially reviewed and still admit nothing, because its population lives in the data and not in the harness — was posted separately to `chats/Claude-Codex-Human/Review Method Change/` by both agents and stays live there.

## Where the work went

`Review Cards/RC-004 Session Reference Time Pair Check.md`, reviewed in `chats/Claude-Codex/Session Reference Time Pair Check Review/`.

**Boundary at conclusion.** No host is pinned. No candidate has a drift, noise or effective-SNR value. No donor is selected, no generator or sorter has run, and no scientific result exists.
