# Codex Human Report — Session 43

**Date and time:** 2026-08-18 01:42 PDT

**Phase:** Phase 2 — Execution and result review

**Outcome:** RC-007 Round 1 returned **`Revisions Required`** on authenticated
Draft 29. Six blocking finding families require an owner response. No estimator
exists, no candidate noise was measured, no host is pinned, and rank 2 remains
unmeasured.

---

## 1. What this session was for

Claude Session 43 submitted the contract for the second host gate before any
candidate noise value was known. RC-007 puts §19 of the Tier A host-selection
document, a metadata-only raw-layout probe, a prose/specification checker, and
its mutation harness into one Round-1 review boundary. It also proposes a
structural change: remove the separate effective-SNR host gate and reduce host
admissibility from five gates to four.

This session performed the card's full-artifact pass. I authenticated every
candidate digest, reran both owner instruments, independently replayed the
layout probe against rank 1 without reading sample values, checked the cited
preprocessing and SNR conventions against primary sources, and constructed a
reviewer probe for the decision-shape counterexamples.

## 2. Candidate authentication and owner evidence

Draft 29 authenticated at
`d0fdd4626bc3680313ddbae122a10e157d7b8efbbd9f6847752a1379fabc5bd8`.
The seven accompanying tool and output digests in RC-007 also matched. The
three earlier-section spans remain fixed at the card's recorded digests, and no
packet or prior result artifact moved.

The owner specification checker reproduced **99 checks, 0 failed**. The owner
mutation harness reproduced **11 of 11 mutations caught**, with the control
green. Those instruments establish the exact claims they test, but the Round-1
probe shows important claim families they do not test.

The raw-layout probe was independently replayed against rank 1. It made **192
requests**, transferred **12,582,912 bytes**, and reproduced the submitted TXT
and JSON outputs byte-for-byte. AST inspection and the replay established that
the probe reads layout/metadata and no Python-level sample slice. This was the
only live candidate-asset access; no noise sample or value was read.

## 3. Round-1 findings

### F1 — level interval and decision rule disagree

§19 declares `1.25 µV ≤ sigma_worst ≤ 10.0 µV`, yet the pass rule compares
only `sigma_worst ≤ N`. The lower anti-saturation condition has no verdict
branch. The relaxation paragraph separately carries `12.5 → 25.0 µV`, even
though the section derives the strict upper bound as 10.0 µV. Both defects pass
the owner checker. This is blocking because the published admissible interval
and executable contract are different objects.

### F2 — peak and peak-to-peak ceiling direction is reversed

The section states the correct inequality, `snr_peak ≤ snr_p2p`, but draws the
wrong conclusion for an upper ceiling. Requiring `snr_p2p ≤ 40` guarantees the
single-sided peak is at most 40; it is sufficient, not necessary. A waveform
with peak `+30σ` and trough `-20σ` passes the single-sided ceiling while its
peak-to-peak ratio is 50. The rule may still be declared as a conservative
project choice, but it cannot carry the submitted derivation or necessity
claim.

### F3 — verdict branches overlap

When both `R_space > M` and `R_null > M`, §19 says the host fails homogeneity
and is unmeasurable. A resolution diagnostic that withholds the measurement
cannot also permit a measured failure without a precedence rule. Zero and
non-finite percentile denominators are also undefined in the submitted
contract. The owner response must produce one total, deterministic disposition
map.

### F4 — preprocessing comparison and edge locality are false

The official anchor describes a fifth-order Butterworth high-pass applied
forward and backward with `scipy.filtfilt`, hence zero phase. Draft 29 instead
calls the comparison a causal recursive filter. Its rectangular DFT high-pass
also has a global periodic impulse response, not an effect confined to 150
discarded edge samples. For `n = 13020`, the direct impulse calculation is
nonzero at the retained centre: `h[6510] = -1/13020`. The source description
and the locality rationale therefore require repair or replacement.

### F5 — sparse sampling cannot support the universal purpose claim

The fixed grid covers 60 of 9,999 full chunks, about 0.6%. A one-chunk
excursion at any unsampled chunk leaves the sampled maximum unchanged. The
submitted quantity is therefore the worst sampled window, not a bound on noise
“wherever the segment lands.” This is not a nonblocking preference about the
choice of `K`; it is a mismatch between the declared purpose and the quantity
the design can measure.

### F6 — four-gate supersession is incomplete

Claim Sheet Amendment 6 explicitly includes effective host SNR among the
per-donor hard host-specific eligibility gates used to determine `N`. A donor
survives only if at least one pinned site passes every gate, and that surviving
count affects whether the host can proceed. Reclassifying effective SNR as
donor-level does not eliminate its host-specific rejection power. Aggregate
noise and a generic amplitude range do not establish the rendered donor/site
result. The separate gate must remain, or the exact replacement predicate,
timing, killed-donor reporting, and host disposition must be defined and
justified before supersession.

### F7 — tracked clarification

The two time halves use the same channels and estimator, but within-window
nonstationarity means their true per-channel scales are not guaranteed
identical by construction. This is nonblocking if the owner narrows the prose
to a conservative disagreement diagnostic without changing the decision
quantity.

## 4. Independent reviewer probe

I added `agents/Codex/tools/probe_rc007_round1.py`, SHA-256
`70fc0a3a1ae8ab916b87329a931aea03b557a89ee5ab768703b11bd612883a15`.
It passed **12/12** and checks:

- exact Draft-29 authentication and a green owner checker;
- the stale relaxed ladder and absent lower-bound decision;
- the peak/peak-to-peak counterexample;
- overlapping homogeneity/unmeasurable branches;
- the sixty unique sampled windows and an invisible unsampled excursion;
- the ideal FFT high-pass response at the retained centre;
- the Claim Sheet's in-force effective-SNR gate against Draft 29's removal;
- absence of a Python-level sample slice in the layout probe.

This is an adversarial specification probe, not an estimator and not a noise
measurement.

## 5. Review decision and communication

The RC-007 card now carries a numbered Round-1 ledger and the direct
**Revisions Required** verdict. The index records that the card remains open
and that Claude owes the bounded owner response. I appended the same verdict to
the active Host Noise Gate chat using the physical-EOF protocol: 149 lines
before the write, one unique Session-43 header after that point, and a physical
tail reread after the append.

The root public README received one lean correction entry. It names the
pre-measurement review failure and corrects the preceding entry's overstatement
that all tolerances came from published numbers. The public state remains
`In Progress` and explicitly says no estimator, candidate noise value, chosen
recording, or sorter result exists.

## 6. Challenges and reasoning paths

The main distinction was between a green prose checker and a correct decision
contract. The checker and its mutation harness were useful authentication
evidence, but both encoded the owner's chosen anchors; they could not reveal a
missing verdict branch, a reversed implication, or a universal claim defeated
by an unsampled chunk. Independent counterexamples were therefore the relevant
second reading.

The supersession finding required following a donor-level quantity through its
host-level consequence. Amendment 6 does not merely ask for a reported donor
diagnostic: the gate determines which donors survive, that count is `N`, and
`N` controls whether the host-specific schedule can exist. “Donor-level” and
“not a host gate” are therefore not equivalent classifications.

The filter finding similarly required separating zero phase from locality. A
forward-backward Butterworth and a rectangular DFT mask may both avoid ordinary
phase delay, but that does not make the latter local in time. The direct impulse
calculation shows the proposed edge discard cannot justify the submitted
claim.

## 7. Files created or updated

**Created**

- `agents/Codex/tools/probe_rc007_round1.py`
- `agents/Codex/Session Summaries/HumanReport43.md`

**Updated**

- `Review Cards/RC-007 Host Noise Gate Specification.md`
- `Review Cards/README.md`
- `chats/Claude-Codex/Host Noise Gate/Host Noise Gate - Active.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/references.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No estimator, Claim Sheet, packet file, candidate result, or prior approved
artifact was edited. No cadence report was due.

## 8. Next steps

**Immediate owner: Claude.** Answer the six blocking finding families and the
tracked clarification in one exact RC-007 response state. Keep every candidate
noise value hidden and do not implement the estimator during the specification
repair. The card remains open and nothing in this session approves Draft 29.

Rank 1 remains first in the pinned host order and has cleared only its drift
gate. Rank 2 remains unmeasured. Until one host clears every in-force gate, no
target manifest, donor assignment, hybrid generation, Rung 0, or sorter run is
authorized.

No count-based progress report was due. Codex's next session is Session 44; the
next cadence report is due in Session 48.
