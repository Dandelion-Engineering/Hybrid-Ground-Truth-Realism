# Summary — Archive-Reading Drift Command Review

**Date range:** 2026-08-15 (Claude Session 27, 03:28 PDT) — 2026-08-15 (Claude Session 30, 09:11 PDT)
**Participants:** Claude (owner), Codex (reviewer)
**Review Card:** `Review Cards/RC-002 Archive-Reading Drift Command.md`
**Outcome:** **Not approved. Closed at `Revisions Required` by the Convergence Decision**, explicitly agreed by both agents. This is the first card in the project to close without approval, and the first time the convergence mechanism was used.

## What the card covered

The code that turns a processed IBL NWB asset into the arrays RC-001's approved drift estimator consumes: the new packet module `utils/archive_units.py`, the command `measure_host_drift.py`, and their synthetic harness. RC-001 approved the drift *specification*; this card was the *reader*.

## Frozen, unapproved final state

| File | SHA-256 |
|---|---|
| `Reproducibility Packet/scripts/utils/archive_units.py` | `2ee891ce7e167edca37f735c6483ba965b7008e4935611e8d38c0177d961fb4a` |
| `Reproducibility Packet/scripts/measure_host_drift.py` | `dfbb9cc8620ce85c56350ee2c84b178c0081398aee44513a122db8faeb6607ed` |
| `agents/Claude/tools/test_measure_host_drift.py` | `5101d000b3cd803ef53be4930056d0f8608dd9b0736b220519b727e9f2d477b7` |
| `agents/Claude/tools/mutate_rc002_repairs.py` | `1e1ed5a9bbda991dc5d2239de05c5cd40510e2a3dcea8fa7713955618d0eceba` |
| `agents/Claude/tools/mutation_test_runbook_checker.py` | `ea85ede2af89fa18e1cf41633c53bc9a96ee0cd6f6190b0394b02afd4a4678fc` |
| `Reproducibility Packet/scripts/check_runbook_consistency.py` | `848e6d033a424d8a280519765244ed32329dbd53f52594da8cc700310a776c9f` |
| `Reproducibility Packet/README.md` | `ae01b1a2b766a22a25ed0ddf2dc0235bc61e8254045e46655457da2d2cf2d4b5` |

**No approved state moved by a byte** during this review: the selection document stays at `c35987fe…`, `band_drift.py` at `eace4cd3…`, `test_band_drift.py` at `946df906…`, and both Claim Sheets are untouched.

## What the review settled

Three rounds produced eleven findings, and every one was accepted in full by the owner with no dispute in either direction. The repairs that survive on their tested boundaries and should be carried forward rather than re-derived:

- **Input errors never become drift verdicts.** All four §16.8 confirmations have a violating fixture that asserts the command stops without writing a report. Raw/processed pair identity now requires subject and paired stem, not a shared session UUID; an AP clock is rejected unless its timestamps cover its data axis.
- **Structural columns are validated as stored.** The two ragged indices are HDMF `VectorIndex` and are required to be integer-typed; `max_electrode` still accepts a whole-valued float and reports it.
- **The band-contiguity threshold is pinned at 40 µm rather than typeable**, closing a route to a threshold chosen after seeing values.
- **The command lives in the packet** and runs standalone, with its missing runbook step carried as one explicit, mutation-checked `PENDING_STEP` declaration until the first real execution.
- **Transfer placement reads the real chunk index.** Every touched chunk's own `(byte_offset, size)` is read from `get_chunk_info_by_coord`, with three named placement bases and a deliberately loose whole-file fallback.
- **One combined memory figure.** `peak_resident_bytes` = block cache + converted arrays + Python structures + HDF5's own chunk-cache ceiling, enforced as a single number, with its exclusions named.
- **Output paths are resolved rather than string-compared**, and stale artifacts are cleared before a run.
- **Both mutation harnesses.** The repair harness catches 13/13; the runbook-checker harness catches 18/18, including three `PENDING_STEP` mutations added specifically because a mechanism had been called "checked" for a whole round with nothing testing it.

## Why it closed unapproved

**RC-002-F1-R2, a blocking LATE-BLOCKER found in Codex's terminal Round-3 verification.** `read_band_units` computes and enforces `peak_resident_bytes` at `archive_units.py:828`, then calls `source_provenance(handle)` at `:846`, which reads each complete stored provenance dataset with `node[()]`. Those bytes and the returned strings appear in none of the plan's terms. On a generated, schema-valid fixture whose `general/source_script` holds 4,200,030 characters, a plan reporting `cache_bound_bytes = 174,368` and `peak_resident_bytes = 267,001` is admitted at exactly that ceiling and then transfers and retains **4,232,336 bytes** — the transfer bound exceeded more than twenty-four-fold, the admitted resident ceiling more than thirtyfold.

Evidence: `agents/Codex/tools/probe_rc002_round3.py`, SHA-256 `506d7280f7dbcc98ebc9e0ca544195c9dcfe819eca19e5e6f6b41cfa9adc5e15`, generated fixture only, no network or archive read. The owner reproduced it unmodified and to the byte before writing the convergence statement.

**Why it was late.** The call existed in Round 1. Round 1's cost construction isolated logical ragged payload against fixed-block reads; Round 2's isolated fragmented chunks and cache/array coexistence; neither separated a post-plan read from the plan. Round 3's *new* whole-footprint claim is what made the unchanged call directly contradictory to the response.

## The Convergence Decision

Both agents wrote one statement each — minimum shippable claim, controlling evidence, strongest evidence against their own position, one acceptable safe disposition — and both landed on **`Revisions Required`** with no counterproposal. Both statements are recorded in full on the card. The disposition is agreement on *action*: the defect is local, because the two mechanisms that fix it (`spent_bytes` charged into `cache_bound_bytes`, `held` charged into `structures_bytes`) already exist in the candidate, so it is not purpose-level and does not justify a split; and it is demonstrated rather than underdetermined, so it cannot be downgraded to `Approved with Follow-ups`.

Claude's statement added one sweep of the general claim — *no read may occur after the ceiling is enforced except the ones the plan bounds*:

- Inside `read_band_units`, `source_provenance` is the **only** post-check read; everything else is read before `spent_bytes` is captured.
- The defect bites hardest in `--plan-only`, which prints the payload, the bound and the peak but never the actual `io["bytes"]` — so on the exact command the compute rule says to run first, the operator's only cost figure is the understated one.
- The command performs two further reads that no ceiling covers at all, `read_electrode_table` and `read_series_timing` on the raw asset. **These are not a second blocker** — both are bounded by construction — but they are the same accounting gap and belong inside the successor's repair boundary.

## What this closes and what it does not

**Closed:** RC-002, this chat, and any further review of the frozen seven-file state. Under convergence clause 4 the repair happens **outside** formal review. Under clause 5, if the successor also fails to converge on the same scoped purpose, the work must be split or redesigned rather than opening a third like-for-like card.

**Not closed and explicitly still blocked:** no candidate may be read under this state. **No host is pinned, no candidate has been measured, no donor is selected, no generator or sorter has run, and no scientific result exists.** The successor card is `RC-003`, `Supersedes: RC-002`.

## Method note

The convergence mechanism did what it was designed to do on its first real use. Three rounds produced eleven genuine findings and a twelfth that would have justified a fourth round under the old cycle; the boundary stopped it at a recorded disposition instead, with the frozen state, the surviving repairs and the repair boundary all written down, and it cost the two agents one message each rather than a wait on an asynchronous director.
