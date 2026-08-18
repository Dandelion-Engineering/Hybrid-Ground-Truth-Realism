# Codex Human Report — Session 46

**Date and time:** 2026-08-18 07:48 PDT

**Phase:** Phase 2 — Execution and specification review

**Outcome:** RC-008 Draft 32 received a full-artifact Round-1
**`Revisions Required`** verdict. Five defects block approval and four items are
tracked as non-blocking. Draft 32 remains frozen and unapproved; Claude owns the
Round-2 response.

No estimator exists, no archive sample or candidate noise value was read, no
packet file changed, no host is pinned, and rank 2 remains unmeasured.

---

## 1. What this session was for

Claude Session 46 closed RC-007 at `Revisions Required`, repaired its final
convergence defect outside formal review, and opened the sole allowed successor
RC-008. This session performed RC-008's required full-artifact Round-1 review
of §19 at Draft 32. It authenticated the six-file candidate and frozen §1–§18
spans, reproduced the owner evidence, re-read the complete contract, inspected
the exact pinned SpikeInterface filtering implementation, and attacked the
load-bearing numerical and verification claims.

The review stayed pre-measurement. It did not read an archive candidate sample,
write an estimator, produce a candidate noise value, edit a Claude candidate,
change the Claim Sheet or Reproducibility Packet, pin a host, or authorize any
generation or sorter execution.

## 2. Exact-state authentication and owner evidence

All six carded Draft-32 SHA-256 digests matched. The selection document matched
`6933c89ec561a7a9bc3201ea332ed7a6698f179af65cde49621cb0fddaec0db7`.
The three frozen spans also matched their published byte counts and digests:
§1–§16 at 144,664 bytes / `700b3b9a…`, §17 at 21,864 bytes /
`dc73b87f…`, and §18 at 20,579 bytes / `8af3e62c…`.

The owner evidence reproduced in the repository virtual environment:

- `probe_rc008_spec.py`: **57 / 57**, exit 0;
- the invoked RC-007 baseline: **288 checks with exactly the declared six
  failures**, exit 1;
- `mutate_rc008_spec.py`: **12 / 12 mutations caught**, control green.

These green results authenticate the declared candidate but do not discharge
the independently reproduced substantive and oracle-coverage defects below.

## 3. Blocking F1-R1 — lower floor uses the wrong extremum

Section 19.4 defines `sigma_worst_sampled = max_k S(k)` and uses it both for the
upper noise ceiling and for the lower anti-saturation floor. A maximum can
enforce the former, but not the latter across sampled placements.

The reviewer fixture uses 59 sampled windows at `1 µV` and one at `5 µV`. The
current strict level branch passes because `sigma_worst_sampled = 5 µV` lies in
the declared interval. The 59 quiet windows nevertheless violate the lower
floor, and at `A_min = 50 µV` each has peak-to-peak SNR `50`, beyond the ceiling
of `40`. The repair must define/use a quietest sampled statistic, or narrow the
stated guarantee so it no longer claims anti-saturation protection for every
sampled placement.

## 4. Blocking F2-R1 — nominal-rate filter breaks exact identity

Draft 32 deliberately designs the Butterworth filter at nominal `30,000 Hz`
while claiming the retained samples are exactly those produced by pinned
SpikeInterface `FilterRecording.get_traces`. The exact SpikeInterface 0.104.8
source obtains `recording.get_sampling_frequency()` and designs the
coefficients with that rate.

The rank-1 timing index records `30,000.039869961383 Hz`. The nominal-rate and
recording-rate SOS coefficients differ by `1.31860735664e-07`; on a
deterministic signal their retained outputs differ by `3.56153236218e-05 µV`.
The size is small, but the published identity is exact. The contract must
either design from the recording rate or declare and pin the nominal-rate
deviation while narrowing the identity claim to the margin/chunk mechanics it
actually shares.

## 5. Blocking F3-R1 — the split direction is not general

Draft 32 settles on contiguous channel halves and says interleaving positively
correlates the half-estimates, compressing the spread in the permissive
direction. An exact 72-channel periodic construction gives `R_null = 1` for
the pinned contiguous halves and `R_null = 4` for even/odd interleaving. In
that construction interleaving expands rather than compresses the statistic.

If “interleaving” meant another block size or permutation, that alternative is
not pinned. The owner may retain contiguous halves, but the rationale must be
bounded and honest or supported for a precisely defined alternative; the
unqualified direction claim cannot control a pre-measurement choice.

## 6. Blocking F4-R1 — the regression oracle can be counterfeited

The RC-008 checker runs the closed RC-007 checker and accepts a hard-coded list
of its expected text failures. It does not authenticate that executable or its
structured records, and it does not require the expected nonzero child exit.

In a staged copy, the reviewer changed the parameter-table `K` from `60` to
`61` and replaced `probe_rc007_spec.py` with a counterfeit process that printed
the six expected failures and summary. The outer RC-008 checker still exited
zero and reported **57 / 57**; no failure named the changed `K`. The repair must
pin the legacy executable and record digests, assert the expected process
semantics, and include a substitution/undeclared-change mutation.

## 7. Blocking F5-R1 — bad-channel effect can be permissive

Section 19 deliberately does not mask bad channels and describes their effect
on `R_space_sampled` as conservative inflation. Percentile ratios are not
monotone under an arbitrary channel replacement.

A 72-channel vector with 8 values at `1`, 56 at `2`, and 8 at `3` has
`p90/p10 = 3` and fails strict `M = 2`. Replacing one low value with an extreme
`100` moves `p10` to `2`, leaves `p90` at `3`, and compresses the ratio to
`1.5`, flipping failure to pass. The contract needs a defensible bad-channel
boundary/handling rule or must remove the conservative-direction claim and
account for this permissive failure mode.

## 8. Tracked non-blocking findings

Four narrower items were recorded for the owner response:

- **T1-R1:** §19.9 should distinguish a cheaper read that changes clustered
  coverage from one that aggregates three cores and dilutes the statistic;
  “dilution” does not describe both arrangements.
- **T2-R1:** §19.10 still identifies Draft 31 as the current unapproved state.
- **T3-R1:** “stored bit” and “two to three bits” should be “stored-code step”
  and “two to three code steps.”
- **T4-R1:** the upward-bias direction from omitting phase shift is clear for an
  ideal shared component, not automatically for the final nonlinear
  channel-MAD/percentile statistic; narrow or support the stronger claim.

The review did not find a fifth live contradiction in the repaired
`R_null_sampled` branch interpretation. The four repaired surfaces agree with
the ordered branches in Draft 32.

## 9. Independent reviewer evidence

I added `agents/Codex/tools/probe_rc008_round1.py` and its deterministic record.
The probe authenticates the candidate and frozen spans, invokes the owner
checker, and reproduces the five concrete counterexamples plus the stale
current-state sentence. It passes **32 / 32** and reads no archive sample,
candidate noise value, or network resource.

SHA-256 digests:

- probe: `7352afab46034dd7057f4aba4dae45a2532729d747287c867ab14acb7eb06f2f`;
- record: `dad99817d0698819fd39f1bf9aa953f9ca19780bff137aa85decb354d5ba4a0d`.

The exact SpikeInterface source used for F2-R1 is now in `references.md` at
tag commit `76c41846f88de3cc9dc5858d5c7f97dd6cb1955f`. It confirms that filter
coefficients and automatic margins are derived from the recording's sampling
frequency and that real margins are removed after filtering.

## 10. Governance, communication and public state

RC-008 now carries the full Round-1 finding ledger and direct
`Revisions Required` outcome. Its index row says the owner Round-2 response is
owed. The active Section 19 Convergence Repair chat contains the same verdict
and evidence. The append-only write recorded 81 pre-write lines, found exactly
one Session-46 header after that boundary, and re-read the UTF-8 physical tail.

The public README gained one lean forward entry. It reports the five defects as
pre-measurement specification and verification failures, not recording
results, and preserves the no-estimator/no-measurement/no-host boundary.

RC-008 is RC-007's sole like-for-like successor, so clause 5 remains salient:
if this successor ultimately closes at a non-approval disposition, another
like-for-like successor is forbidden and the work must be split or redesigned.
That terminal condition has not fired at Round 1; the ordinary Round-2 response
remains available.

## 11. Files created or updated

**Created**

- `agents/Codex/tools/probe_rc008_round1.py`
- `agents/Codex/tools/rc008_round1_2026-08-18.txt`
- `agents/Codex/Session Summaries/HumanReport46.md`

**Updated**

- `Review Cards/RC-008 Host Noise Gate, Convergence Repair.md`
- `Review Cards/README.md`
- `chats/Claude-Codex/Section 19 Convergence Repair/Section 19 Convergence Repair - Active.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/references.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No Claude candidate, estimator, Claim Sheet, Reproducibility Packet, archive
sample, candidate result, or earlier approved artifact was edited. No
count-based progress report was due; the next one remains Session 48.

## 12. Next steps

**Immediate owner: Claude.** Respond explicitly to F1-R1 through F5-R1 and
dispose of T1-R1 through T4-R1. Repair the candidate outside the frozen Draft
32 bytes, update the card with a fully authenticated exact Round-2 candidate,
and strengthen the checker/mutations so the revised claims are executable.

Codex's next session is Session 47. It should authenticate the exact owner
response and perform the Round-2 delta review under RC-008. No estimator or
candidate-noise measurement is authorized until §19 reaches explicit
same-state approval. The next cadence report is due in Session 48.
