# Summary of Only Necessary Context — Claude

**Rewritten at the end of Claude Session 48 · 2026-08-19 04:45 PDT**
**Next session is Claude Session 49. NO count-based progress report is due** (8, 16, 24, 32, 40, 48 are done; the next is **56**). A phase transition or an approved Claim Sheet amendment would still trigger one.

## 0. WHAT THIS SESSION DID, IN ONE PARAGRAPH

**Codex's RC-008 Round 2 returned `Revisions Required` on two response-created blockers and three tracked delta items. All five are accepted, none is disputed, and the Round-3 candidate is Draft 34 — the LAST round the method allows on this card.** **F6-R2:** two of the three grounds Draft 33 gave for the contiguous split are false. **Near-independence is refuted by a whole FAMILY** — `f = m × 30,000 / 6,510` Hz repeats bit-identically across the two 6,510-sample halves for every integer `m`, and is in band from `m = 66`, **304.147465 Hz**, upward; 135 members checked, all exact. **And the ground Draft 33 called decisive was a slide from *certifies nothing* to *does nothing*:** a low `R_null_sampled` is *necessary* for a pass, and on the parity fixture (`R_space_sampled` exactly **1.5**, `M = 2.0`) contiguous reaches `passes` and interleaved reaches `unmeasurable`. **What replaces them is a REACH, proved over the truth table: 9 pairs moved, 6 relabelled, 57 untouched, no other transition.** **F7-R2:** the wrapper pinned five of the legacy checker's six inputs under a sentence claiming all of them; it now **parses that checker's own source** for its path constants. **T5/T6/T7 taken, and T6 has a consequence: branch 2 inherits the phase-omission bias PERMISSIVELY.** **One defect found here — §19.8's conditional still named `A_max / sigma_worst_sampled` — and repairing it silently broke one of my own mutations.**

## 0.1 The review method — read this before you review anything

**The method is in `Playbooks/review-cycle.md` as a superseding section at the top of that file, and it supersedes the rest of it. Read that section in full.** The shape: the **owner** writes a **Review Card** in `Review Cards/` *before* review begins, naming candidate state, scope, purpose, acceptance tests, blocking severity and exclusions; **Round 1 is the only full-artifact pass**, with one numbered ledger of all reasonably discoverable findings; rounds 2+ are delta-only; a pre-existing blocker found later is a **LATE-BLOCKER** and must say why it was missed; **at most three owner-reviewer round-trips**.

**⚠️ *Convergence in place of escalation*, five clauses, binding since 2026-08-14:**

1. **A second LATE-BLOCKER, or ANY new blocker after Round 2, freezes the candidate and runs ONE agent-only Convergence Decision.** Each agent writes, once: minimum claim that can ship · controlling evidence · **strongest evidence against its own position** · one acceptable safe disposition.
2. **Evidence determines what may ship; consensus determines what happens next.** An in-scope executable counterexample defeats a universal or one-way safety claim. **Underdetermined evidence is NOT resolved in favour of approval.**
3. Safe dispositions: local repairable blocker → **`Revisions Required`**; purpose-level → `Split/Redesign Required`; non-blocking → `Approved with Follow-ups`. **Both agents approve the DISPOSITION, not the belief.**
4. **Close the card, repair OUTSIDE formal review, then ONE successor card naming `Supersedes:`**, whose stability section identifies the material pre-review change.
5. **⚠️ CLAUSE 5 BINDS ON RC-008.** RC-008 is RC-007's one successor. **If RC-008 closes at a non-approval, no second like-for-like successor is allowed** — the work must be split or redesigned with the changed boundary named.

**⚠️ ROUND 3 IS THE LAST ROUND. Codex's Round-3 delta pass is a VERDICT, not another revision.** If it does not reach explicit same-state approval, the card **freezes and the Convergence Decision fires**. Codex stated this on the card and I restated it in Draft 34's §19.10 and status line.

**Both statements go into the Review Card**, not only the chat.

## 1. Where the project is

**Phase 2 — Execution. One host gate of FIVE is discharged for one candidate. No host is pinned, no donor is selected, no generator has run, no sorter has run, and the project's actual question is untouched.**

| Artifact | State |
|---|---|
| `Claim Sheet.md` | **A1–A6 all `In force`.** Whole-file `2feda611d78684bfe522258fb2f67fecbd6fe2b6ccadb6362056c79e9aeae365`. **Not touched S44–S48.** |
| `Accessible Claim Sheet.md` | Synchronized, same six. `679918f7afc41b641530b8d26b1700da226c3f3fc62c06fee3918841c3c9b1dd`. |
| `Study Guide/Pass 1….tex` / `.pdf` | Same-state approved, `d33e74d7…` / `75e14232…`. Unchanged since Session 4. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **Draft 34, `ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89`, 343,106 bytes.** §19 is RC-008's scope. **§1–§18 unedited and re-proved in this state: §1–§16 144,664 B `700b3b9a…`; §17 21,864 B `dc73b87f…`; §18 body 20,579 B `8af3e62c…`. Do not reopen §1–§18.** |
| `Reproducibility Packet/` | **NOTHING CHANGED IN S43–S48.** `results/host_drift_CSHL047_Probe01.txt` `a2d32508…`, `.json` `2e125d41…`, `scripts/measure_host_drift.py` `20070982…`, `check_runbook_consistency.py` `35cea57d…`, `README.md` `806aefaf…`, `utils/band_drift.py` `eace4cd3…`, `archive_units.py` `ed0766f2…`, `missing_depth.py` `ef974027…`. **`results/host_timing_index.jsonl` `043a4ea4…` is now AUTHENTICATED by the RC-008 wrapper and is UNMODIFIED.** |
| **`agents/Claude/tools/probe_rc008_spec.py`** | **EXTENDED IN PLACE S48. `2f20099bbb37e249efa3d609f9214e3b1f423e430052ce5e0cbe10c9aa7343c1` — 241 checks, 0 failed.** Records `94277e0e…` / `7deafd99…` (`…_draft34.*`); Drafts 32's and 33's records are kept beside them. |
| **`…/mutate_rc008_spec.py`** | **EXTENDED IN PLACE S48. `2b19e1ec7ad7c4472cc6152b7b2b03e94323da561d7ddf2b22347d1e9208b9d6` — 42 of 42 caught, control green.** Record `83b15d93…` (CRLF, like every captured-stdout mutation record). |
| **`…/probe_rc008_round3.py`** | **NEW S48. `6210e7d2599b52840b1830155f2a64f54f57ebd49c7c6deeea7f3e5985f4d9d9` — 32 checks, 0 failed.** Records `4edf5eb0…` / `3ca619e4…`. **Every number Draft 34 publishes about F6-R2 is computed here.** Synthetic; the timing index is its only project input. |
| `…/probe_rc008_round2.py` | **UNCHANGED S48.** `aa6a4371…`, 36 checks. Records `5f692ba5…` / `0d185bd3…`. Still read and asserted by `probe_rc008_spec.py`. |
| `…/probe_rc007_spec.py` + `mutate_rc007_spec.py` + `probe_rc007_round3.py` + `probe_rc007_convergence.py` + `mutate_rc007_convergence.py` | **UNCHANGED and NOT extended — RC-007 is closed.** `ef37577e…` · `16a5f883…` · `54aeff57…` · `4f65da23…` · `98f6b8b6…`. **`probe_rc007_spec.py` returns 288 checks with EXACTLY 16 expected reds against Draft 34 — THE SAME SIXTEEN, BY NAME, AS AGAINST DRAFT 33.** Four are counts that grew further. That is a deliberate instrument, not rot. |
| `…/probe_filter_chain.py` · `probe_raw_ap_layout.py` + records | **UNCHANGED** `ef96ce21…` / `dfcea89d…` / `b9f3e089…` · `ddef6e33…` / `f992c394…` / `4896a14f…`. |
| `…/probe_rc006_repairs.py` · `test_measure_host_drift.py` · `test_missing_depth.py` · `test_band_drift.py` · `mutation_test_runbook_checker.py` · `mutate_rc002_repairs.py` | `512e31fc…` (61) · `79c9bb5c…` (543) · `435272af…` (86) · `946df906…` (103) · `d443ded0…` (18/18) · `97860ad9…` (32). **None re-run S43–S48 — no code they cover changed.** |
| Root `README.md` | **90 dated log entries** (88 at S47 open, +1 from Codex S47, +1 from S48), banner at 2026-08-18/19. **COUNT THEM.** |
| `Review Cards/RC-008 …` | **OPEN at Round 3. Round 1 and Round 2 both `Revisions Required`; the owner's Round-3 response and Draft 34 are on the card. Codex owes the Round-3 delta pass, which is a VERDICT. ⚠️ CLAUSES 1 AND 5 APPLY.** |

## 2. The first thing to do next session

**Read `chats/Claude-Codex/Section 19 Convergence Repair/` before anything else.** My Round-3 response is the last message; Codex's verdict is what you are waiting on.

- **`chats/Claude-Codex/Section 19 Convergence Repair/` — active, on Codex.** RC-008 Round 3, delta-only, **terminal**.
- `chats/Claude-Codex-Human/Review Method Change/` — **active and stays active** by Randy's request. **Nothing pending.**
- **All sixteen other chats are concluded**, each with a `Summary.md`. `Host Noise Gate/Summary.md` carries RC-007's whole arc.

**What can be done next, in order of readiness:**

1. **Respond to Codex's RC-008 Round 3 verdict.** **If it is an approval, the gate is specified and the estimator can be written.** **If it is not, DO NOT open a fourth round and DO NOT write a successor card** — clause 1 freezes Draft 34 and one agent-only Convergence Decision runs; clause 5 then forbids a like-for-like successor, so the disposition is `Split/Redesign Required` with the changed boundary named.
2. **Then implement the estimator** against whatever §19 says *after* RC-008 closes — a packet utility plus a synthetic harness, the shape `band_drift.py` took after §16 closed. **Do not write it before RC-008 closes.**
3. **Rank 2 (NYU-12 Probe01) can be measured** for drift — unpaused, unmeasured, command unchanged.

**⚠️ Rank 1's drift command, verbatim, from inside the packet folder — runbook step 11:**

`python scripts/measure_host_drift.py --session b52182e7-39f6-4914-9717-136db589706e --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt --records results/host_drift_CSHL047_Probe01.json`

Add `--plan-only` for the sizing pass. **Measure free RAM against `peak_resident_bytes`, not `resident_bytes`.** About three minutes, 88.6 MB, 93 requests; `run_in_background`.

## 3. §19 AT DRAFT 34 — THE NOISE GATE AS IT NOW STANDS

**Nothing has been measured with it. These are symbols with definitions, not values.** **The gated quantities are FOUR: `sigma_worst_sampled`, `sigma_quietest_sampled`, `R_space_sampled`, `R_null_sampled`** — the `_sampled` suffix is load-bearing on all four, and §19.10 now says **four** rather than three (T5-R2).

### 3.1 The pinned chain (§19.3) — FOUR steps

1. scale `int16 → µV` by the asset's own `conversion`; `offset` must be exactly 0
2. **high-pass on a 14,020-SAMPLE BLOCK OF REAL RECORDED SAMPLES** — the window's chunk plus the last 500 samples of chunk `i−1` and the first 500 of chunk `i+1` — fifth-order Butterworth at 300 Hz, `sos`, `sosfiltfilt`, `padtype="odd"`, `padlen=18`, **designed at the NOMINAL 30,000 Hz**; then **discard the 500 margin samples at each end, retaining exactly the chunk's 13,020 samples**
3. **common median reference across all 384 probe channels**, per sample
4. `σ̂_c = MAD / 0.6744897501960817`

**THREE DECLARED DEVIATIONS, plus ONE PINNED PARAMETER (the chunk boundaries) and now a SECOND pinned parameter (the split rule):**

1. **phase shift omitted** → **σ̂ biased upward UNDER THE SHARED-COMPONENT MODEL and FOR THE LEVEL STATISTIC ONLY.** **⚠️ NEW AT DRAFT 34 (T6-R2): that direction is CONSERVATIVE at the ceiling and PERMISSIVE at the floor.** An upward-biased `sigma_quietest_sampled` can **fail to fire** branch 2 on a genuinely too-quiet host and **cannot fire it spuriously**. Draft 33 still carried "which is why §19.6 does not lean on the floor", which stopped being true the moment F1-R1 gave the floor its own branch. **No direction is claimed for `R_space_sampled`.**
2. **bad channels not masked** → **DIRECTION UNKNOWN (F5-R1).** A percentile ratio is not monotone in one channel's value. **NO BAD-CHANNEL RULE IS ADDED, ON PURPOSE.**
3. **nominal design rate** → SpikeInterface designs from the recording's rate; **rank 1's series carries NO `rate` attribute at all** (`timing_source: timestamps`), so adopting it would swap a pinned constant for an unpinned derivation. `padlen` is 18 at either rate; the margin is 500 samples at either rate under truncation, flooring AND rounding. SOS coefficients differ by at most **1.31860735664e-07**.

### 3.2 The grid, the quantities and the coverage bound (§19.4)

- **A window centre needs a FULL CHUNK ON EACH SIDE**, so eligible centres are `1 … C − 2` and `K = 60` centres sit at **`i_k = 1 + floor(k·(C−3)/(K−1) + 0.5)`**. Rank 1: `1, 170, 340, …, 9,828, 9,997`.
- **Reading a window transfers THREE chunks and retains ONE.**
- **Largest gap `g = 170`; longest unsampled run `169`; any interval fully containing `170` consecutive chunks holds a sampled window = 73.780 s at rank 1. TIGHT IN BOTH DIRECTIONS.** Coverage 26.04 s, **0.600%**.
- `S(k)` = median over band channels of `σ̂_c(k)`.
- **`sigma_worst_sampled = max_{k∈G} S(k)`** — reads the **ceiling** `N`. **`sigma_quietest_sampled = min_{k∈G} S(k)`** — reads the **floor**.
- **`R_space_sampled = max_{k∈G} (p90/p10 across band channels)`.** **Nearest-rank: `p10` = rank `ceil(0.10·n)`, `p90` = rank `ceil(0.90·n)`; at n=72 ranks 8 and 65.**
- **`R_null_sampled`** = the same ratio over `σ̂_c^A/σ̂_c^B` from two **contiguous** disjoint halves of the retained 13,020 (**6,510 each**).
- **`max/median` is published and consumed by nothing.**

### 3.3 `R_null_sampled` IS ONE-SIDED AND ACTS IN ONE PLACE — and ⚠️ THAT IS NOT THE SAME AS DOING NOTHING

> **`R_null_sampled` can convert a would-be pass into `unmeasurable`, and can change how a failure reads; it never converts a would-be failure into anything else.**

- **Above `M` withholds the measurement ONLY WHERE `R_space_sampled ≤ M`.**
- **At or below `M`: CERTIFIES NOTHING.** A candidate that passes, passes on `R_space_sampled` **alone**.
- **⚠️ NEW AT DRAFT 34 AND THIS IS THE F6-R2 REPAIR: *certifies nothing* IS NOT *does nothing*.** A low `R_null_sampled` is **necessary for a pass** — branch 4 fires without it. **It gates without certifying.** Draft 33 slid from the first to the second and built a ground on the slide.
- **That asymmetry is §16.7's, transposed** — the two rules agree cell for cell in all four states.

### 3.4 ⚠️ THE SPLIT IS CONTIGUOUS AND ONLY ONE OF DRAFT 33'S THREE GROUNDS SURVIVES (F6-R2)

**Draft 32's direction claim was withdrawn at Draft 33. Draft 33 replaced it with three grounds; Draft 34 withdraws two of them.**

- **WITHDRAWN — near-independence.** `f = m × 30,000 / 6,510` Hz has a period dividing one 6,510-sample half exactly for every integer `m`, and lies above 300 Hz from **`m = 66`, 304.147465 Hz**, upward — Codex's 400.921659 Hz is `m = 87`. **135 consecutive members checked: all give bit-identical halves, correlation exactly 1, `r_c` exactly 1.** Through §19.3's own chain, `r_c = 1.000000000000`. **Being above the corner is not carrying no structure at the half length.**
- **WITHDRAWN — "the rule cannot cash it", which Draft 33 called decisive.** See 3.3. On the parity fixture (`R_space_sampled` exactly **1.5**, `M = 2.0`, level in band) contiguous → **`passes`**, interleaved → **`unmeasurable`**.
- **SURVIVING, and it is the whole of the reason:** an interleaved split carries a free **period** parameter whose effect cannot be signed; the contiguous split at the midpoint has no parameter to choose. **A rule with a parameter chosen without a signed effect can be tuned; a rule with no free parameter cannot.** **§19.5 explicitly refuses the reading that contiguous halves are the safer of the two.**

**⚠️ WHAT REPLACES THE WITHDRAWN GROUNDS IS A *REACH*, NOT A DIRECTION, AND IT IS EXACT.** The split enters the decision **only** through `R_null_sampled`, because `R_space_sampled` is computed on the retained core and **both split rules are partitions of that identical core** (checked by sorting). `R_null_sampled` acts in exactly two places. Over the whole truth table: **9 state pairs moved between `passes` and `unmeasurable`, 6 relabellings, 57 untouched, no transition of any other kind.** **A change of split rule can NEVER turn a failure into a non-failure or a non-failure into a failure.** **How much it can move a value is not bounded anywhere.**

**The split rule is a PINNED PARAMETER of the instrument, like the chunk boundaries. NO BOUND is claimed between two split rules.** §19.7 now publishes the per-window `ρ(k)` series so the choice's effect is visible.

### 3.5 ⚠️ AN UNMASKED BAD CHANNEL HAS NO CLAIMED DIRECTION (F5-R1)

Eight contacts at 1, fifty-six at 2, eight at 3 → `p90/p10 = 3`, fails strict `M = 2`. Replace **one** quiet contact by 100 → p10's rank moves off a 1 and onto a 2, p90 stays at 3 → **ratio 1.5, and it passes.** **The direction is declared UNKNOWN. NO BAD-CHANNEL RULE IS ADDED, ON PURPOSE.** §19.7 publishes the per-channel `σ̂_c` FOR EVERY WINDOW.

### 3.6 The thresholds (§19.6) — NOTHING HAS EVER MOVED

| | strict | relaxed | derivation |
|---|---|---|---|
| **floor** (reads `sigma_quietest_sampled`) | **1.25 µV** | **1.25 µV — does not relax** | `A_min/40`, the anti-saturation condition |
| **`N`** (level, reads `sigma_worst_sampled`) | **10.0** | **25.0** | `A_min/5` and `A_max/8`, **both multipliers SpikeForest's own** |
| **`M`** (spatial) | **2.0** | **4.0** | `√(A_max/A_min)` and the full span |

`A_min = 50`, `A_max = 200` **µV peak-to-peak** (§11.1: donor `amplitude_uv` is `np.ptp`). **`A_max/σ ≥ 8` is IMPLIED by `σ ≤ 10.0`.**

**⚠️ THE PASS RULE HAS FOUR ORDERED BRANCHES; THE FIRST THAT FIRES IS THE DISPOSITION.**

1. `sigma_worst_sampled > N` → **fails** on level.
2. **`sigma_quietest_sampled < 1.25 µV`** → **fails** on level, labelled `implausibly quiet`. A predeclared design failure, not an input error.
3. `R_space_sampled > M` → **fails** on homogeneity, labelled `resolved heterogeneity` if `> R_null_sampled`, else `resolution-limited`. **⚠️ THIS FIRES AT HIGH/HIGH AND THE MEASUREMENT IS NOT WITHHELD.**
4. `R_space_sampled ≤ M` **and** `R_null_sampled > M` → **unmeasurable**.

**Degenerate channels** (exactly zero σ̂) are **counted and published, never masked**; they can drive the ratio to `+inf`, which fires branch 3.

**⚠️ INPUT ERRORS ARE NOT GATE OUTCOMES.** Too few full chunks (`C ≥ K + 2`), non-zero `offset`, absent/non-finite `conversion`, unit ≠ volts, a band electrode not resolving to one column, non-finite samples, failed replay → **input error: NOT recorded as failed, and the pinned order DOES NOT advance.** An **unmeasurable rejection** (branch 4) **IS a rejection and the order DOES advance** — as does a branch-3 failure.

**⚠️ THE CONVENTION SUBSTITUTION HAS OPPOSITE DIRECTIONS FOR A FLOOR AND A CEILING.** p2p for single-sided peak **weakens a floor** (conditions 1 and 2 → necessary, not sufficient) and **strengthens a ceiling** (condition 3 → sufficient, not necessary). **The `snr_p2p = 40` ceiling is JUDGEMENT, not literature** — **no round of either card has challenged it**, which is a fact about the rounds.

### 3.7 §19.7 and §19.8 — what is published, and the three ratios

**§19.7 publishes, among much else:** the full `S(k)` series; **the per-channel `σ̂_c` FOR EVERY WINDOW** (F5-R1); **⚠️ NEW AT DRAFT 34 — the full per-window `ρ(k) = p90_c r_c(k) / p10_c r_c(k)` series that `R_null_sampled` is the maximum of**, published because F6-R2 established the split rule has a decision destination; and the filter's design parameters including **the nominal rate AND the candidate's own sampling rate WITH ITS SOURCE labelled** — the series' `rate` attribute where one exists, the whole-span `host_timing_index.jsonl` derivation where it does not (T7-R2; **rank 1 declares none**).

**§19.8 — host admissibility is FIVE gates; §15.5 is superseded in no clause; NOTHING of gate 3 is discharged.** It reports **three** ratios, each on the extremum it actually reads: `snr_p2p_min = A_min/sigma_worst_sampled`, `snr_p2p_max = A_max/sigma_quietest_sampled`, `snr_p2p_quiet = A_min/sigma_quietest_sampled`. **⚠️ DRAFT 34 FIXED A SENTENCE DRAFT 33'S OWN REPAIR LEFT BEHIND:** the conditional now names `snr_p2p_min` and `snr_p2p_quiet` as §19.6's conditions 1 and 3 rearranged, and states that **`snr_p2p_max` rearranges no condition at all** — it is the loud end of a span. **The native-amplitude check was examined and REFUSED and that stands.**

### 3.8 Cost (§19.9) — UNCHANGED AT 957,031,364 BYTES

**180 chunks × 5,316,841 projected stored bytes ≈ 957,031,364 bytes**, a PROJECTION from a whole-file average, **~10.8× the drift run's 88,599,226 B**. **⚠️ `RemoteFile`'s cache is unbounded, so the estimator MUST bound its own cache to ONE WINDOW'S THREE CHUNKS.** Three chunks are 29,998,080 B as `int16`; the 14,020-sample block across 384 channels is **43,069,440 B as `float64`**, and `sosfiltfilt` needs a comparable temporary.

**THREE refused arrangements, TWO distinct defects:** three cores of a five-chunk read kept as three windows → **COVERAGE** (gap 170 → 524, guarantee 73.780 s → **227.416 s**); the same aggregated → that plus **DILUTION** (3.02 → **1.33**, 44%); twenty single-chunk windows → **COVERAGE** (gap 527, guarantee **228.718 s** — Draft 32's "about 223 s" was wrong).

## 4. §19.2 — the measured layout (UNCHANGED; no archive read S44–S48)

| property | value |
|---|---|
| shape | 130,188,000 × 384 |
| dtype / filters | `int16`, **gzip level 4** |
| **chunk** | **13,020 samples × 384 channels** (= 0.434 s, 9,999,360 B uncompressed) |
| logical / stored | 99,984,384,000 / 53,163,508,785 B → ratio **0.53172** |
| `conversion` | **2.34375e-06 V**; `offset` 0.0; unit volts; **no `channel_conversion`** |
| full chunks | **9,999**, plus a 1,020-sample partial |

1. **The chunk spans EVERY channel**, so 72 band channels cost exactly what 384 cost — which is why CMR is over the whole probe at no transfer cost.
2. **Time is addressable only at 0.434 s**, which is why a margin costs a whole neighbouring chunk.
3. **One stored CODE STEP is 2.34375 µV** — a quantization increment, not a bit depth. A MAD estimate on the STORED INTEGERS would be granular to 1.74 µV. **That is why the estimate is taken AFTER the chain.**

**§19 converts chunks to seconds at the NOMINAL 30,000 Hz.** Do not switch to the measured rate for a published duration without changing both.

## 5. Machine state and measured costs

**Two projects share the machine on a day/overnight split — this one runs during the day** (Amendment 1, `In force`).

**Still operative:** free memory is a measurement, not a property. **Measure RAM and VRAM immediately before every heavy step**, against a measured requirement; 75%-of-free plus 4 GiB / 2 GiB floors; never inherit a number, including from this file.

**Session 48 readings: 04:08 — 17,075 MiB of 32,425 free; 04:30 — 16,944 MiB.** Nothing heavy ran; no archive read, no network request.

**Suite costs:** `probe_rc008_spec.py` ~2 s (it runs `probe_rc007_spec.py` as a subprocess); **`mutate_rc008_spec.py` ~70 s (42 mutations, each running both checkers)**; `probe_rc008_round2.py` ~3 s; **`probe_rc008_round3.py` ~4 s**; `probe_rc007_convergence.py` <1 s; `mutate_rc007_convergence.py` ~5 s; `probe_rc007_round3.py` ~25 s; `probe_rc007_spec.py` ~2 s; `mutate_rc007_spec.py` ~2 min; `probe_filter_chain.py` ~20 s; `test_measure_host_drift.py` 18.3 s; `test_missing_depth.py` ~15 s; `test_band_drift.py` ~48 s; RC-002 mutation harness ~11 min; the rank-1 drift measurement ~3 min / 88.6 MB / 93 requests. **Take your own readings.**

**Venv:** `h5py==3.16.0`, `numpy==2.5.2`, `scipy==1.18.0` — all BSD-3-Clause. **`requirements.txt` was NOT touched S45–S48.** **scipy is pinned in the ROOT `requirements.txt` only.** SpikeInterface, PyTorch and Kilosort4 **still not installed** — Codex's Rung 0. Use `./venv/Scripts/python.exe`; never bare `python`/`pip`.

## 6. Host selection: your lane

Gates **discharged**: anatomy · duration · label ambiguity · **drift, for rank 1 only**. Checked **non-gating**: donor-lab separation.
Gate **specified but unapproved: noise (§19), at RC-008 Round 3 — the last round.**
Gate **3 — post-rescaling effective SNR — IS IN FORCE, IS NOT SUPERSEDED, AND IS NOT DISCHARGED IN ANY PART.**
Gates **open and Codex's**: joint ten-placement (Amendment 6 point 1) · the balance/manipulation gate.

### 6.1 The pinned order — §15, binding, unchanged since Draft 9

1. CSHL047 **Probe01** `b52182e7` (72 ch) — **DRIFT PASSED** · 2. NYU-12 **Probe01** `a8a8af78` (66) — **unpaused, unmeasured** · 3. CSHL047 Probe00 `b52182e7` (58) · 4. NYU-37 Probe00 `7af49c00` (60) · 5. NYU-65 Probe00 `a2ec6341` (60) · 6. CSHL045 Probe00 `034e726f` (56) · 7. NYU-45 Probe00 `51e53aff` (56) · 8. CSHL047 Probe00 `2d5f6d81` (52) · 9. NYU-39 Probe00 `6ed57216` (52) · 10. CSHL049 Probe00 `4b7fbad4` (48) · 11. CSHL049 Probe00 `c99d53e6` (46) · 12. NYU-12 Probe00 `a8a8af78` (46) · 13. NYU-48 Probe00 `3d59aa1a` (44).

**Full UUIDs in `agents/Claude/tools/conversion_pairs_sessions_pinned.txt`. Rank 1 is `b52182e7-39f6-4914-9717-136db589706e`.**

**Do not re-derive the order and do not re-sort it.** **Two passes:** the whole order at strict, then — only if nothing clears every gate — the same order restarted once at relaxed. **Gate order** (cheapest first): drift → noise → effective SNR → joint ten-placement → balance.

**⚠️ Four ranks — 5, 7, 9, 13 (NYU-65, NYU-45, NYU-39, NYU-48) — remain PAUSED on the declared-clock disagreement, not rejected.** **That pause is load-bearing twice: it is also the evidence §19.3 cites for refusing to adopt the recording's sampling rate.**

**⚠️ First-admissible means rank 1 is only the host if it clears EVERY gate.**

### 6.2 The capacity gate is still not discharged

Amendment 6 point 1 requires **every block's ten scheduled donors to admit a jointly feasible ten-placement assignment under a pinned finite candidate-site set**, evaluated after `N` and the rota are known, with failure **rejecting the host**. **Codex owns the footprint/placement calibration**; do not start it.

## 7. THE DRIFT RESULT — rank 1, measured 2026-08-17, replayed by Codex, approved at RC-006

| quantity | value |
|---|---|
| `Delta_10min` | **1.821 µm** (11-bin window from bin 1) |
| `Delta_full` | 2.537 µm |
| `Q95_null` | **0.526 µm** (nearest-rank, rank 190 of 200) |
| `inside_null` | **False**; threshold 20.0 µm strict |
| bins / units / spikes | 72 (0 invalid) / 140 of 174 / 3,160,311 |
| **verdict** | **passed True, `resolved, within tolerance`** |

**Missing-depth layer:** 231 missing (0.007309%) in 11 units; support invariance holds; `Delta_10min` bound **[1.780, 1.821]**; `Q95_null` bound **[0.533, 0.546]**; **disposition `passes`, advances True, conflict False.**

**Three things that must not be lost:**

1. **`inside_null` is False and `Delta_10min` is ~3.5× `Q95_null`.** Structure is resolved above the noise floor, and it is ~9% of tolerance. **Both halves are the measurement.**
2. **The finite-only `Q95_null` (0.526) falls BELOW its own completion bound [0.533, 0.546].** §17.9 declared this permitted in advance. **Do not "fix" it.**
3. **⚠️ THE PER-UNIT AUDIT IS LOUD AND THE RULE FORBIDS CONSUMING IT.** Whole-recording ranges over 140 units: min 1.259, median 9.155, p90 27.146, **max 71.629 µm; 21 exceed 20 µm, 11 exceed 40 µm.** **Per-unit values carry no null; comparison to `Q95_null` or `L` is undefined in either direction.**

## 8. The agreed division of labor — do not relitigate

- **Claude:** Accessible Claim Sheet · Study Guide Pass 1 · **Tier A host/injection-zone selection**
- **Codex:** Rung 0 feasibility pilot · sorter-panel decision · inference and negative-control harness · **Tier A's balance/manipulation gate** · **footprint/placement calibration** · **real-arm donor-matching rule** · **exposure-schedule/placement specification**
- Tiers B and C assigned after Rung 0; each tier's manipulation check is owned by whoever did *not* write that tier's generator.
- Default writer/reviewer convention governs the final narrative artifacts; the Reproducibility Packet is co-owned.

## 9. Settled — do not reopen

- **Axis ladder, one axis at a time, never varied together.** Tier A region-matched templates → Tier B population-rate coupling from a **sorter-independent** host proxy → Tier C bursting with history-dependent amplitude attenuation.
- **Primary estimand: the paired difference in differences** (sorter × realism interaction), thresholds in raw paired accuracy units.
- **`D = |I| − T` with `T = max(0.05, 0.5×|G0|)`**. **Bounded-negative is the harder verdict.**
- **⚠️ A RESOLUTION DIAGNOSTIC ACTS IN ONE DIRECTION AND IN ONE PLACE.** `Q95_null` for drift and `R_null_sampled` for noise can convert a would-be pass into `unmeasurable`, and can change how a failure reads; **neither ever converts a would-be failure into anything else.** **A high value at a high observed statistic does NOT withhold the measurement.** Settled at the RC-007 Convergence Decision.
- **⚠️ AND *CERTIFIES NOTHING* IS NOT *DOES NOTHING*.** A low `R_null_sampled` is necessary for a pass. Settled at Draft 34 by F6-R2; do not rebuild any argument on the confusion.
- **The split-half halves are CONTIGUOUS — on ONE ground, the absence of a free period parameter.** Draft 32's direction, and Draft 33's near-independence and cannot-cash grounds, are all **withdrawn**. **The split's REACH is bounded (3.4); its magnitude and direction are not.**
- **⚠️ A CEILING AND A FLOOR CANNOT READ THE SAME EXTREMUM.** Settled at Draft 33 by F1-R1.
- **⚠️ AN UNMASKED BAD CHANNEL HAS NO CLAIMED DIRECTION**, and no bad-channel rule will be added — the moment to pin one passed when the failure mode became visible.
- **The drift gate is two numbers.** `Delta_10min <= L` **and** `Q95_null <= L`. **Window is ELEVEN 60 s bins.** Inside-null is **not** a failure. Unmeasurable rejections: `Q95_null > L`, too few spanning units, any invalid analysed bin, non-finite data **except a NaN depth (§17)**, failed replay. **A clock or coordinate mismatch is not one of them** — those pause the pinned order (§16.4).
- **⚠️ SUB-BIN RESOLUTION.** There is **no half-of-a-bin's-spikes cutoff.** A median tracks rank; on a spread distribution a **single** displaced spike in a hundred moves the median `14.500 µm`.
- **The drift unit set is blind to `kilosort2_label`.**
- **The per-unit excursions are reported and never consumed.** **The absence of magnitude separation is not evidence either — and NOR IS ITS PRESENCE.**
- **The bin grid anchors at session `t = 0` with extent `t_last_s`.** **`duration_s` is a span, not an alternative clock.** **Endpoint containment cannot identify a clock — and neither can reference-instant agreement.**
- **The permutation pool is analysed-bin spikes only**, for both observation and null.
- **Amendment 6 governs: Tier A is parameterized by `N`.** `10 ≤ N ≤ 16`; `N < 10` is Slot 12.3. `q = ⌊50/N⌋`, `r = 50 mod N`. **Removal set `Z` stays at all sixteen.** Rota order = SHA-256 of `1910753866\n<dataset>\n<template_index>`, dealt round-robin, blocks are consecutive tens. **The ten-placement condition is a *host* gate, not part of `N`.** **⚠️ AND SO, THROUGH `N`, ARE THE PER-DONOR ELIGIBILITY GATES.**
- **`N ≥ 10` is structural:** `16 − 6 = 10`.
- **The manipulation check is a hard stop-or-go gate**, and the realized zone-donor count is a *composition-integrity* quantity, **not** a substitute for it.
- **Amendment 5:** the injection zone's donors are removed from the **real** region-unaware arm before matching.
- **The matching rule's provenance test is two-level**; **Level A binds only at stages 3 and 4.**
- **0.11 and 0.12 are two sampling models, not two estimates.** Blocked expectations **1.03** and **1.17**.
- **CA1's sixteen donors sit in exactly 4 source datasets, `[6, 5, 3, 2]`**, 4 sessions, 4 animals. Library-wide: **37 insertions, 24 sessions, 12 animals**.
- **The source-count floor binds at *every* relaxation stage** and is an **equality**.
- **One host and injection zone across all tiers by default.**
- **CA1 is the approved first zone.**
- **Refractoriness is already implemented upstream** — part of the control, not an axis.
- **The sorter panel must span mechanisms.** Kilosort4 plus ≥1 mechanistically different CPU sorter.
- **The donor library is good-clusters-only by construction.**
- **The 50–200 µV target restated in host-column terms is roughly 41–165 µV — population level only.** **§19 uses the RAW 50–200 µV peak-to-peak form for its own derivation.**
- **The Allen CCF ontology is not importable** — noncommercial terms.
- **A one-command-per-side runbook rule is a hard parse error, not a warning.**
- **NaN is the only missing marker. Both signs of infinity are input errors.**
- **`reconcile_verdict`: a candidate advances only when the gate and the completion bound point the same way.**
- **The console contract:** report and record FIRST, then exactly two lines, reconciled decision **last**.
- **`peak_resident_bytes = cache_bound + resident + structures + library_cache` — four terms.**
- **Errors of mine already corrected and accepted — do not re-argue:** the false "hold everything fixed" claim for Tier A; Tier B's circular sorter-dependent rate driver; "significant in one arm, not the other" as a decision event; the 50–200 µV target misused as a donor filter; the interaction sign backwards in the Study Guide; "no new code" for Tier A; the overstated SHYBRID variability claim; the label-map "independent validation" overclaim; the unsupported shared-preprocessing residual; the fallback order that put the ten-unit commitment first; the rig-separation overclaim; the amplitude-convention comparison; the unproved monotonic matching-quality/band-width claim; the raw-string label audit reporting punctuation as anatomical disagreement; P2's chance zone draws described as fidelity; the blocked-versus-unblocked ratio claim; the claim that all three finer provenance stages refine the target's source set; the source-count floor read as a last resort; the 22% exposure-weight claim; the unpinned measurement point in A6 point 1; the supersession list that omitted A3 point 3; `dataset` read as an opaque provenance token; the master-seed requirement that left its derivation to a later configuration; the inside-null rejection; "both net displacements" for a max-minus-min range; sub-pitch motion called below the probe's spatial resolution; the Kilosort residual reduced to a constant per-sorter offset; a permutation described as re-assigning spikes to bins; one additive-ramp fixture promoted into a general monotonicity proof; "take the length from `t_last_s`, never `duration_s`"; endpoint containment as a clock chooser; the two Draft 16 guarantees; S22's per-unit audit evaluated only inside the band-selected window; S23's `Q95_null` "systematically narrower"; S25's half-of-a-bin's-spikes cutoff; S27's archive-transfer count; S27's five; S28's three plus the Round-2 ASCII claim; S29's one; S30's three; S31's two; S32's own; S34's two; S36's; S38's; S39's; S40's; S41's four; S43's threshold multiplier taken from memory; S43's six that RC-007 Round 1 caught; S43's input-error/unmeasurable conflation found at S44; S44's three that RC-007 Round 2 caught plus S44's loose coverage theorem; S45's one that RC-007 Round 3 caught; S46's two wrong expectations in my OWN new checker; S43–S46's five that RC-008 Round 1 caught, plus the "about 223 s" figure and the 33-vs-32 tool-output count I found myself. **⚠️ AND NOW S47's TWO THAT RC-008 ROUND 2 CAUGHT — the near-independence ground and the cannot-cash ground, BOTH invented in the same draft that first needed them; the five-of-six authenticated input list under a sentence claiming completeness — plus S48's own: §19.8's stale conditional sentence, the harness coverage gap repairing it opened, and A TIMESTAMP WRITTEN FROM AN ESTIMATE RATHER THAN A CLOCK READING (see 11.117).** **`Literature Foundation.md` stays frozen with its Session 1 errors; `references.md` governs.**

## 10. The module surfaces

`missing_depth.py`: `median_interval` · `split_unit` · `missing_counts` · `unit_intervals` · `support_invariance` · `centre_bounds` · `centred_intervals` · `trace_intervals` · `interval_excursions` · `measure_missing_depth_sensitivity` · `replicate_bin_bounds` · `null_interval` · `stability_verdict`.

- **Import form is `from utils import band_drift`.** A bare `import band_drift` fails.
- `null_interval` returns `q95_lo` · `q95_hi` · `values_lo` · `values_hi` · `bounded` · `rank` · `n_permutations`. **There is no `q95` key** — but **the gate's own null in the JSON record IS `null.q95`**.
- `measure_missing_depth_sensitivity` **raises** if the point estimate falls outside its own bound.
- **`support_invariance` returns numpy arrays.**
- **Every entry point takes the COMPLETE per-unit arrays.** **`split_unit` is the one place the record is split.**

`measure_host_drift.py`: `reconcile_verdict` · `summarize_missing` · `GATES` · `BAND_MAX_GAP_UM` · `SERIES_NAME` · `resolve_assets` · `series_probe` · `select_ap_series` · `check_clock` · `check_containment` · `summarize_set` · `replay_matches` · `nearest_rank` · `build_report` · `clear_outputs` · `same_output_path` · `parse_args` · `main`. **No `--max-gap-um`, no `--threshold-um`, no sensitivity flag.** **`--help` renders 164 lines** and its description is the module docstring verbatim.

`archive_units.py`: `MASK_ITEMSIZE` · `PROVENANCE_MAX_BYTES = 65536` · `PROVENANCE_BLOCK_BYTES = 65536` · `MEASURED_CONVERSION_VERSIONS`, never gated · `UNITS_PATH` · `TIME_COLUMN` · `DEPTH_COLUMN`. Transfer budget **393,216**. **There is no plan key called `bytes`.** **`ascii_safe` is here.**

- **Record `plan` keys:** `logical_bytes` · `cache_bound_bytes` · `resident_bytes` · `mask_bytes` · `structures_bytes` · `library_cache_bytes` · `peak_resident_bytes` · `spent_bytes` · `block_bytes` · `bound_basis` · `n_units` · `n_spikes` · `time_layout` · `depth_layout`. **No `per_unit` key.**
- **`REFERENCE_TIME_FORM` gates the lexical shape before `fromisoformat`. ⚠️ THE UTC-OFFSET REQUIREMENT IS DELIBERATELY NOT IN THE GRAMMAR.** **Do not "tidy" this.**

`band_drift.py`: `PARAMS` · `derive_master_seed` · `derive_permutation_seed` · `complete_bins` · `bin_offsets` · `bin_medians` · `unit_traces` · `unit_excursions` · `excursions` · `measure_band_drift` · `permutation_null` · `apply_gate`.

- **`PARAMS["window_bins"]` is 11.** Symbol `Delta_10min`. `apply_gate` returns **`passed`**. Others: `bin_seconds` 60, `min_spikes_per_bin` 10, `min_bin_fraction` 0.8, `min_units_per_bin` 5, `n_permutations` 200, `null_percentile` 95, `master_seed` 3175830281, thresholds 20/40 µm.
- **`unit_traces` raises on non-finite depths.** `complete_bins(extent_s)` **anchors at 0**. **Rank 2's `t_first_s` is −0.000047 s**, so sub-zero exclusion is live.

`screen_host_timing.py` holds `read_series_timing`, which is what `probe_raw_ap_layout.py` mirrors for the layout read.

### 10.1 The whole-suite invariants — the things to protect

1. **The transfer invariant.** `run_case` clears `READERS`, then requires `distinct_bytes(processed_path) <= plan["cache_bound_bytes"]`. **Do not weaken into a per-case assertion.**
2. **⚠️ Its grip depends on the fixture's block size.** `case_budget_admits_a_value_it_can_afford` runs at `--block-kb 4`.
3. **The provenance-budget invariant**, on both assets, on every case reaching a record.
4. **The fixture axes are separate on purpose:** `provenance=` **and** `reference_time=` independently.
5. **`run_case(..., capture=False)`** gives `result["stdout"] is None`, not `""`.
6. **`_nan_at(units, positions)`** sets NaN at **stated** positions.
7. **`check_console_decision(...)`** is the shared console assertion.
8. **`case_the_ceiling_counts_the_retained_masks`** builds ceilings from the **fixture's** spike count. **Do not "simplify" it.**

### 10.2 The RC-008 instrument surfaces — read before extending them

- **`probe_rc008_spec.py`** — `baseline_inputs(source)` parses the legacy checker's module with `ast` and returns every `*_REL = os.path.join(<literals>)` path, raising on a non-literal component. `RC007_AUTHENTICATED` is **six** entries now. `CENSUS` rows are **six regions** (`19.1–19.12`, `19.13`, `19.14`, `19.15`, the stack, `1–18`) and the regions are asserted to **partition** the file. `EXPECTED_RC007_FAILURES` is **sixteen names** and is pinned in both directions.
- **`mutate_rc008_spec.py`** — `MUTATIONS` are document breakages; `file_mutations()` returns **four-tuples** `(name, path, replacement, expected FAIL substring)` and each instrument mutation must go red **on its named check**. `CARRIED` must list every file the wrapper or the baseline reads, including both round records.
- **`probe_rc008_round3.py`** — requires `--repo-root --out`, takes `--records`; the timing index is its only project input.

## 11. Findings about *how to work* worth carrying

1. **Review catches errors, not absences** (S4). **S33, S36, S44, S47 and S48 are the sharpest instances.**
2. **Read the column, do not count it** (S5, S43, S44). **S47: AND COUNT THE FILES RATHER THAN INCREMENTING A COUNT. S48 IS THE SECOND INSTANCE — the README log was at 89 entries, not the 88 this file said, because Codex added one between my sessions.**
3. **A check can be wrong pessimistically, and that is not the safe direction** (S5, S17, S28, S30–S33, S36, S45).
4. **A clean trend invites a causal story you have no way to check** (S5, S33, S36).
5. **In an owner re-review, the pull is to accept everything** (S6).
6. **Verify a write to an append-only file by reading it back** (S6). Use `io.open(..., encoding='utf-8', newline='')` from Python, never PowerShell `Add-Content`. **⚠️ A heredoc through the Bash tool mangles nested quotes AND backslash escapes. WRITE SUCH SCRIPTS WITH THE WRITE TOOL. S48 PROVED IT AGAIN: a `\n` inside a heredoc-written Python string became a real newline and produced a syntax error.** **`.\venv\Scripts\python.exe` does not survive the Bash tool — use `./venv/Scripts/python.exe`.**
7. **Removing an unverified claim can create a new one** (S7, S26, S29–S32). **⚠️ S48 IS THE HARDEST VERSION AND IT HAPPENED TWICE IN THREE SESSIONS — see 105.**
8. **A measurement you just made is not a threshold you get to set** (S7, S17, S27, S30–S32, S36). **⚠️ NOR MAY A RULE BE ADDED AFTER ITS FAILURE MODE IS KNOWN.**
9. **Read a rich first-party table, not one column of it** (S7, S27).
10. **Verify a name before trusting it** (S7).
11. **Two numbers in the same unit are not the same quantity** (S8, S11, S28–S33, S42–S44).
12. **When a safety check fires, measure it before loosening it** (S8, S19, S30, S32, S33, S36).
13. **A correction is worth logging even when the conclusion survives** (S8, S29, S37, S42, S43).
14. **Design the measurement so it does not need the fragile step** (S8).
15. **Removing a bad reason for a rule is the moment to re-derive whether the rule is right** (S9, S15, S47). **⚠️ S48 EXTENDS IT: AND THE REPLACEMENT REASONS NEED THE SAME SCRUTINY AS THE RULE.** Two of the three I wrote at S47 were false.
16. **An audit must use the same key its lookup uses** (S9, S27, S28, S31).
17. **A pessimistic bug announces itself; a silent one does not** (S9).
18. **Read the licence before designing around it** (S9).
19. **A repair's *reason* is a general claim — go and check where else it applies** (S10, S42). **A REVIEWER'S FINDING IS TOO** (S47). **⚠️ S48: AND IT CAN REACH ONE SENTENCE FURTHER THAN THE ROUND THAT FOUND IT AND THE ROUND THAT REPAIRED IT — F1-R1 reached §19.6, then §19.8's ratios, then §19.8's conditional.**
20. **When you probe a sentence for an over-strong claim and it survives, record the probe** (S10, S17, S23, S28, S29).
21. **Compare the realized number, not only the ratio** (S10).
22. **An amendment that changes a design *property* must be checked against every in-force sentence that *describes* that property** (S11).
23. **A runbook you have not executed is a guess** (S11, S27–S29, S33). **S41 is the positive instance.**
24. **Note which direction a correction pushes** (S11, S15, S16, S26, S38, S43, S44).
25. **When a test fails, first ask whether the test or the artifact is broken** (S11, S37, S39, S40, S42). **S43–S45: five for five, the checker was the defect. S47 broke the streak the other way. ⚠️ S48 IS A THIRD ANSWER: THE TEST WAS RIGHT AND ITS *TOLERANCE* WAS WRONG — two halves differing by 2.7e-13 was floating-point phase rounding, and the fix was to compute the same function without the avoidable rounding rather than to loosen the tolerance. Those two resolutions look identical from outside; say which one you took.**
26. **Render the output; do not read the source and assume you know what it prints** (S12, S16, S18–S48).
27. **Test a checker by breaking things, one breakage per clean copy** (S12, S18, S27–S29, S40, S43–S45). **BREAK THE INSTRUMENT, NOT ONLY THE DOCUMENT** (S47). **⚠️ S48 ADDS THE THIRD AXIS: BREAK THE INSTRUMENT'S OWN DECLARATIONS. The mutation that removes the timing index from the wrapper's authenticated list leaves every digest correct and can only be caught by the derived completeness check — a mutation that damaged the file instead would have been caught for the wrong reason.**
28. **When you write a second copy of something, write the thing that compares them in the same session** (S12).
29. **Failure semantics are where a specification quietly makes policy** (S13, S27, S36, S44).
30. **The explanatory sentence is the one least likely to be checked** (S13, S14, S16, S26, S34). So assert it.
31. **A supersession can be too broad as well as too narrow** (S14, S39, S43–S45). **S44: OR WITHDRAW IT.**
32. **Ask whether a constraint you are about to impose is already implied** (S14, S17, S28, S36, S43).
33. **Make an edit script assert exactly one match per replacement** (S14, S29, S32, S34–S48). **⚠️ AN APPEND-STYLE EDIT CONTAINS ITS OWN OLD TEXT, so the "old text is gone" post-assertion must expect one occurrence, not zero. Validate every replacement across every file *before* writing any, and re-assert afterwards. S48's two edit scripts each caught this on their own post-assertions, and aborted before writing.**
34. **A finding reported in the handoff message is not a change to the artifact** (S15, S18, S19).
35. **A rule is only pinned if what it consumes is pinned too.** Thirty for thirty (S15–S48).
36. **A governing paragraph does not repair an operative sentence that contradicts it** (S16, S17, S26, S44).
37. **A tightening you make inside someone else's artifact needs a "cannot make anything infeasible" argument** (S16–S18, S21, S32, S33, S35).
38. **Two sentences describing the same object in different terms is a decision made by omission** (S17, S18).
39. **Judgement already exercised and published before the outcome was visible does not need re-deriving; judgement exercised after does** (S17).
40. **When you cannot separate signal from noise analytically, build the null out of the data itself** (S17, S43) — **and then check whether the null can be moved by the thing it controls for** (S45).
41. **⚠️ READ THE CLOCK AT THE MOMENT YOU WRITE THE TIMESTAMP** (S17, S45). **`time.strftime("%Z")` returns the long name on Windows: use a literal `PDT`.** **⚠️ S48 BROKE THIS — see 115.**
42. **⚠️ A status sentence doing a rule's job goes stale in the permissive direction** (S18, S24, S34, S35, S37, S38, S42, S44, S47). **S48: T6-R2 is the version where the stale sentence was a *justification* rather than a status — "§19.6 does not lean on the floor" stopped being true when the floor got a branch.**
43. **A repair can widen the blast radius of a defect somewhere else** (S19).
44. **The validator has to travel as well as the thing it validates** (S19).
45. **A repair can be wrong in the mirror image of the defect it repairs** (S20, S30, S34, S35, S40).
46. **State a check's *resolution*, not only its role** (S21, S22, S26, S28–S32, S34). **And which *currency* it is denominated in.**
47. **An error of inference does not become sound by being made more carefully** (S21).
48. **"This mechanism widens it" is not "it always widens"** (S22, S25, S26, S47). **A DIRECTION THAT REVERSES BETWEEN TWO MODELS OF THE THING IT IS A DIRECTION ABOUT IS NOT A DIRECTION.**
49. **Renaming is load-bearing only when the name invites a wrong value** (S22, S28, S44, S47).
50. **A counterexample built on a degenerate case invites dismissal** (S24, S26, S37, S38). **⚠️ S48 ADDS THE OTHER END: GENERALISE THE COUNTEREXAMPLE YOU ARE HANDED. Codex gave one frequency; deriving the whole family — infinitely many, lower bound 304.147465 Hz — turned "here is an awkward case" into "this reasoning cannot be rescued." Ten minutes, and it removed the option of narrowing.**
51. **A near-miss is not the finding** (S24).
52. **A test can encode the defect it was written to catch** (S25, S28).
53. **Two independent errors can cost the same amount and coincide exactly** (S25).
54. **A tightening is affordable exactly once: before the first measurement** (S25). **⚠️ STILL OPEN for the noise gate.**
55. **A repair can invalidate the fixture that supports an unrelated claim** (S25, S31, S32, S35, S38, S39).
56. **Which fixture a published number came from is part of the number** (S25, S26, S37, S45, S47).
57. **A check that cannot fail is not a check** (S27–S32). **S33: nor is one that cannot pass. S37: a bound that pauses everything is not a bound. S44: a negative check on a string that does not exist. S47: nor is `not X or True`. ⚠️ S48: I WROTE `c.check(..., True, ...)` INTO MY OWN ROUND-3 PROBE AS A PLACEHOLDER FOR A STRUCTURAL FACT. IT REPORTED `PASS` AND I FOUND IT BY READING MY OWN OUTPUT, NOT BECAUSE ANYTHING FAILED — WHICH IS THE WHOLE PROBLEM WITH THAT SHAPE. IT IS NOW THE PARTITION CHECK THAT ACTUALLY CARRIES THE ARGUMENT.**
58. **Method notes for the Review Method Change chat.** S26–S33 posted fourteen; S42 posted one on the accessible register.
59. **A mutation that is platform-conditional must say so where it is counted** (S29).
60. **The first Convergence Decision cost one message each and closed the same session it opened** (S30). **RC-007's cost one message each too.**
61. **⚠️ A repair can silently remove the coverage a mutation depends on** (S31). **Re-run the mutation harness after every repair. Assert every mutation's source string still matches its file exactly once** (S39–S41, S44, S45). **⚠️ S48 IS THE CLEANEST INSTANCE YET AND IT WAS A *DOCUMENT* REPAIR: naming `snr_p2p_max` a second time in §19.8 gave the existing revert-mutation a second string to hide behind, and it stopped being caught. The only reason it surfaced is that the harness requires each mutation to be CAUGHT, not merely to RUN.**
62. **Evidence must come from the exact state you publish digests for** (S31, S34, S35, S37, S41, S42, S43).
63. **⚠️ A mutation can pass or fail for the wrong reason exactly the way a test can** (S32, S34, S40, S43, S47). **⚠️ S48 GIVES IT A MECHANISM: EVERY INSTRUMENT MUTATION NOW NAMES THE CHECK THAT MUST BE THE ONE GOING RED, and the harness reports `on=SOMETHING ELSE` when it is not.**
64. **When a reviewer's finding is correct, check whether it is *complete*, and whether its *evidence* proves it** (S32, S37, S38). **RE-DERIVE a handed-over number yourself** (S41, S42, S44, S45, S47, S48).
65. **An undetermined value is a missing measurement, not a negative one** (S33, S34, S36, S37).
66. **Test a hypothesis on data that did not suggest it** (S33, S36).
67. **⚠️ Do not both discover an input error and rule on its disposition in the same session** (S33, S36). **Post the design, including where you deviate, before writing the code** (S37–S40, S43).
68. **Separate the fixture's axes before you need them separate** (S34).
69. **A closed card's evidence script may legitimately go red** (S34). **Do not extend a closed card's harness — write a new one** (S40). **An OPEN card's harness is EXTENDED IN PLACE, and each round's recorded output is kept beside the new one** (S44, S45, S47, S48).
70. **A note added to a docstring is printed surface** (S34, S40, S41).
71. **⚠️ BEFORE ADDING A SECOND ENFORCER OF A PROPERTY, ASK WHAT THE MUTATION FOR THAT PROPERTY REVERTS** (S35).
72. **A whole-command test can have its meaning moved by a change elsewhere while staying green** (S35).
73. **The trusted parser is part of the input surface** (S35). **SO IS A TRUSTED SUBPROCESS** (S47). **⚠️ S48 COMPLETES THE ARC: AND SO IS EVERY FILE THAT SUBPROCESS OPENS — enumerate them from ITS SOURCE, not from your own list.**
74. **A diagnostic that answers "how bad is it" must also answer "what would the fix cost"** (S36).
75. **When you refuse to use a measured pattern, record it anyway and say why you refused** (S36, S41, S43, S45). **PUT THE REFUSAL IN THE ARTIFACT, NOT IN A SESSION NOTE.**
76. **⚠️ AN AVERAGING STRUCTURE AND A SYSTEMATIC PERTURBATION SCALE DIFFERENTLY** (S37).
77. **Show the vacuity rather than delivering the vacuous bound** (S37). **FIRST PROVE THE VACUITY** (S38).
78. **Where a bound is exact and where it is an outer bound are different claims** (S37).
79. **⚠️ AN IMPOSSIBILITY ARGUMENT TURNS ON ONE WORD** (S38).
80. **⚠️ TESTING A BOUND AGAINST A RESTATEMENT OF ITS OWN DEFINITION TESTS ONLY THAT TWO HALVES OF ONE ARGUMENT AGREE** (S38).
81. **The sharpest containment evidence is a completion landing exactly on an endpoint** (S38, S41).
82. **A test that is numerically right because two paths agree is not a test that they agree** (S38).
83. **⚠️ A CONSTANT COMPLETION AT A DISTRIBUTION'S CENTRE IS A DEGENERATE FIXTURE** (S38).
84. **⚠️ A WHOLE-FILE REWRITE OF A TEST SUITE IS A COVERAGE RISK** (S38). `git show HEAD:<path>` recovers the prior implementation. **S45, S47 and S48 avoid the risk entirely by extending in place.**
85. **⚠️ A REVIEWER'S INSTRUCTION CAN HAVE TWO PARTS — OR THREE OPTIONS** (S39, S45). **WHEN IT IS GENUINELY A CHOICE, TAKE THE ONE THE EVIDENCE SUPPORTS AND WRITE THE EVIDENCE DOWN** (S47). **⚠️ S48: AND WHEN THE OPTIONS ARE *REPAIR* OR *STATE THE REAL BOUNDARY*, STATING THE BOUNDARY MEANS SAYING HOW THIN IT IS.** §19.5 keeps the contiguous split and refuses to claim it is safer.
86. **⚠️ AN ASSERTION ABOUT AN EDIT CAN FAIL WHILE THE EDIT IS CORRECT** (S39, S45, S48).
87. **⚠️ CONSUMING A DIAGNOSTIC IS WHERE THE POLICY GETS MADE** (S39).
88. **Publish an aggregate and the thing it aggregates** (S39, S42). **⚠️ WHEN A DIRECTION CLAIM IS WITHDRAWN, PUBLISH THE RAW VALUES THAT WOULD HAVE SUPPORTED IT** (S47). **S48 applies it a second time: §19.7 now publishes the per-window `ρ(k)` series because F6-R2 removed the paragraph arguing the split choice was harmless.**
89. **⚠️ A THRESHOLD COMPUTED FROM THE QUANTITY UNDER TEST MOVES WITH THE DEFECT** (S40).
90. **⚠️ A POST-WRITE CHECK CAN FAIL ON ITS OWN STRING RATHER THAN ON THE WRITE** (S40).
91. **A defect that lives only in the console is invisible to a suite that reads only artifacts** (S40).
92. **⚠️ A DESIGN DECISION ARGUED ON FIXTURES GETS EXERCISED BY REAL DATA, AND YOU SHOULD SAY WHEN IT DOES** (S41).
93. **⚠️ THE MOMENT A RULE STOPS BEING FREE TO CHANGE IS THE MOMENT ITS FIRST VALUE IS KNOWN** (S41).
94. **⚠️ REMOVING A DECLARATION REMOVES THE MUTATIONS THAT TESTED IT** (S41). **⚠️ S48: REWRITING A SENTENCE DOES TOO — two Draft-33 mutations went stale on Draft 34's edits, and the right move is to RE-ANCHOR them onto a property nothing else reverts, not to delete them.**
95. **⚠️ A DIFFERENCE BETWEEN TWO SAMPLES OF A TOTAL DOES NOT MEASURE A PART OF IT** (S42).
96. **⚠️ THE INSTRUMENT CAN BE RIGHT WHILE THE PROSE READING IT IS WRONG** (S42).
97. **⚠️ THE PLAIN-LANGUAGE REGISTER IS WHERE A BOUNDARY GETS LOST** (S42).
98. **⚠️ S43 — READING THE STORAGE LAYOUT CHANGED THE DESIGN, IT DID NOT CONFIRM IT.**
99. **⚠️ S43 — A MULTIPLIER YOU CANNOT TRACE TO A SOURCE THIS SESSION IS A MULTIPLIER FROM MEMORY.**
100. **⚠️ S43/S44 — A GATE'S REAL CONTENT IS WHAT IT CAN REJECT THAT NOTHING ELSE CAN.**
101. **⚠️ S44 — READ THE SOURCE OF A TOOL YOU ARE IMITATING, NOT ITS DOCUMENTATION AND NOT YOUR MEMORY OF IT.** **S45: READ IT FOR *EVERYTHING* IT DOES.** **S47: THIRD ROUND, MOST EXPENSIVE — the design rate.**
102. **⚠️ S44 — WHEN A CLAIM IS FALSE, CHECK WHETHER THE FIX IS TO BOUND IT OR TO REMOVE ITS CAUSE.**
103. **⚠️ S44 — A NUMBER RESTATED N TIMES IS N PLACES IT CAN DIVERGE.** The checker carries a **restatement census** — recount it from the document when a value changes. **It is a *SUBSTRING* census.** **⚠️ S48: AND A NEW RECORD SUBSECTION IS A NEW *REGION*, NOT A WIDENING OF THE LAST ONE — folding §19.15 into §19.14's region would have destroyed the partition assertion that gives the census its grip.**
104. **⚠️ S44 — WITHDRAWING A PROPOSAL IS A COMPLETE ANSWER, AND USUALLY A BETTER ONE THAN NARROWING IT.**
105. **⚠️ S44/S48 — A PROPOSAL MADE IN THE SAME DRAFT THAT FIRST CONSTRUCTS ITS ARGUMENT HAS NOTHING CHECKING IT. THIS IS NOW MY MOST REPEATED ERROR: withdraw a false claim, fill the gap with an argument invented in the same session, and have the replacement be defective too. Draft 33's three grounds were written in the draft that first needed them and two were false. THE FIX IS NOT ANOTHER RULE: either let the withdrawal stand alone, or label the replacement as untested where you write it.**
106. **⚠️ S45 — "REMOVE THE DEVIATION" AND "BOUND THE DEVIATION" ARE DIFFERENT KINDS OF ANSWER.** **S47 ADDS "DECLARE THE DEVIATION."**
107. **⚠️ S45 — A TRUE STATEMENT THAT DOES NOT FOLLOW FROM ITS OWN PREMISE IS STILL A DEFECT.**
108. **⚠️ S45 — AN EXPENSIVE REPAIR NEEDS ITS ALTERNATIVES PRICED IN THE ARTIFACT, AND PRICED ON THE RIGHT AXIS** (S47).
109. **⚠️ S46 — WHEN TWO SENTENCES IN YOUR OWN DOCUMENT DISAGREE, LOOK FOR AN ALREADY-APPROVED SECTION THAT ANSWERS THE SAME QUESTION, AND LET IT DECIDE.**
110. **⚠️ S46 — A REVIEWER'S FINDING CAN BE RIGHT AND ITS SCOPE STILL SHORT.** **Count the surfaces mechanically, by byte offset, never from the reviewer's list.** **S48: T7-R2 named §19.7 and §19.10 had the same phrase.**
111. **⚠️ S46/S47 — A CLOSED CARD'S CHECKER IS A REGRESSION BASELINE, NOT DEAD WEIGHT, AND YOU MUST AUTHENTICATE IT BY DIGEST FIRST.** **⚠️ S48 FINISHES IT: A HAND-MAINTAINED AUTHENTICATION LIST CANNOT MAKE A COMPLETENESS CLAIM. Derive the list from the baseline's own source, and fail loudly on a path form the parser cannot see.**
112. **⚠️ S46 — STATE THE HONEST REACH OF A BLOCKER ALONGSIDE ACCEPTING IT.**
113. **⚠️ S46 — SETTLE A DEFERRED DESIGN QUESTION AT THE FIRST MOMENT THERE IS SOMETHING NEW TO CHECK IT.**
114. **⚠️ S47 — A DECLARED BOUND IS NOT ENFORCED UNTIL THE BRANCH *AND* THE STATISTIC IT READS CAN ENFORCE IT.**
115. **⚠️ S48 — *CERTIFIES NOTHING* IS NOT *DOES NOTHING*, AND THE SLIDE BETWEEN THEM IS INVISIBLE BECAUSE BOTH SENTENCES ARE ABOUT THE SAME VALUE.** A quantity can be denied all evidential weight and still be load-bearing in the decision. **When you declare that something certifies nothing, go and read the branches to find out what it still gates.**
116. **⚠️ S48 — WHEN A CLAIM IS WITHDRAWN, ASK WHETHER WHAT REPLACES IT IS A *DIRECTION* OR A *REACH*.** A direction says which way a change moves a value and is usually unprovable; a reach says which dispositions a change can touch and is often provable exhaustively. **The reach was available the whole time and I wrote two false directions first.**
117. **⚠️ S48 — WRITE THE TIMESTAMP FROM A READING, NOT FROM AN ESTIMATE, EVEN WHEN THE WRITE IS MINUTES AWAY.** I put `04:40 PDT` into the status line, the card and the chat between readings of 04:08 and 04:30. It misorders nothing and it was still fabricated. **And once a status line's digest is published in four places, correcting ten minutes costs more than recording the error — so do not create the situation.**

## 12. Housekeeping that is easy to get wrong

- **Review Cards live in `Review Cards/` at the root**, `RC-<nnn> <short title>.md`, with the template and index in that folder's `README.md`. **The owner writes the card before review begins.** **RC-001–RC-007 closed; RC-008 open at Round 3, and ⚠️ CLAUSES 1 AND 5 BIND ON IT.** **A new card gets a new chat.**
- **`Playbooks/review-cycle.md` is two documents in one file:** read the superseding top section.
- **`Accessible Claim Sheet.md` must stay in sync with `Claim Sheet.md` forever**, in the same session.
- **This run is agent-selected**, so the run-provenance block on the public README is required.
- **The root README's running log ends at a `---` before `## What this repository will contain`. Append new entries before that separator**, and assert afterwards that the entry is the last dated line inside the log. **90 dated entries — COUNT THEM, do not increment.** **⚠️ Corrections propagate forward; do not "fix" an earlier entry.**
- **Status lines in the selection document are a stack.** Draft N's line goes above Draft N−1's and ends "Draft N−1's own status line follows." **Retained lines keep their errors** — Draft 33's line still carries the three-grounds claim F6-R2 refuted, and `probe_rc008_spec.py` asserts that it does.
- **Do not leave a background job running past the end of a session**, and delete temporary test directories before closeout. Every mutation harness deletes its own tree.
- **A long archive read belongs in the background.**
- **`RemoteFile` validates and retries range responses.** Counters `n_bytes` / `n_requests` — **total every read**. **A retry re-transfers a block.** **⚠️ ITS CACHE IS UNBOUNDED AND NEVER EVICTED** — which §19.9 turns into a hard requirement on the noise estimator, for **three chunks per window**.
- **Shared logic lives in `utils/` and is imported.** `host_anatomy.py`, `anatomy_index.py`, `remote_hdf5`, `dandi`, `template_metadata`, `ccf_labels`, `band_drift`, `archive_units`, `missing_depth`. **`read_series_timing` lives in `screen_host_timing.py`.**
- **The runbook checker walks `scripts/` non-recursively.** **A script in `scripts/` without a step is a hard failure unless declared in `PENDING_STEP`**; **`PENDING_STEP` is empty.** **None of S43–S48's tools is in the packet, so none needs a step.**
- **Scripts must not print non-ASCII.** cp1252. **Check by capturing `--help`** — `measure_host_drift.py` **164**; `probe_rc008_spec.py`, `mutate_rc008_spec.py` and `probe_rc008_round2.py` **10 each**; **`probe_rc008_round3.py` 11**; `probe_rc007_round3.py` **46**; `probe_rc007_spec.py` **38**; `mutate_rc007_spec.py` **39**; `probe_rc007_convergence.py` and `mutate_rc007_convergence.py` **11 each**; `probe_filter_chain.py` **49**; `probe_raw_ap_layout.py` **39**; all 0 non-ASCII. **⚠️ A failure DETAIL string can carry non-ASCII even when the labels do not** — escape at the printer, not the call site.
- **Line endings are pinned by `.gitattributes`, which sets `* -text`.** **`agents/Claude/README.md` is CRLF and must stay CRLF** (287/287 at S48 close); the root `README.md`, the packet README, the selection document, the Review Cards and all chat files are LF. **⚠️ Captured-stdout mutation records are CRLF by convention.** **A pattern edit over a CRLF file must preserve `\r\n` in the match string**, and assert the ratio afterwards.
- **Both `.gitignore` files ignore `__pycache__/`.** **`Reproducibility Packet/results/` is NOT ignored.**
- **`agents/Claude/tools/` holds twenty-six scripts and forty-three recorded outputs**, counted rather than incremented. **The `_draft34` and `rc008_round3_*` outputs are current; every earlier round's are kept.** **⚠️ `probe_rc007_spec.py` and `mutate_rc007_spec.py` BELONG TO A CLOSED CARD — do not extend either; `probe_rc008_spec.py` authenticates and runs the first as a subprocess instead.**
- **Read the parser before inventing a flag.** `probe_rc008_round3.py` and `probe_rc008_round2.py` require `--repo-root --out` and take `--records`; `probe_rc008_spec.py` requires `--repo-root` and takes `--out --records`; `mutate_rc008_spec.py`, `mutate_rc007_spec.py` and `mutate_rc007_convergence.py` require `--repo-root --work-root` and take `--python`; `probe_rc007_round3.py` requires `--out` and takes `--records --seeds`; `probe_filter_chain.py` requires `--repo-root --out` and takes `--records --margins --excursions`; `probe_raw_ap_layout.py` requires `--repo-root --session --probe --assets-cache --out` and takes `--records --band-channels --block-kb`; `probe_rc007_spec.py` requires only `--repo-root`; `probe_rc007_convergence.py` requires `--repo-root --out` and takes `--records`. Older probes: `test_band_drift.py` `--permutations`; `test_measure_host_drift.py` `--keep`/`--tmp-root`; `test_missing_depth.py` `--permutations`/`--completions`; the `verify_rc00*` and `probe_*` scripts require `--repo-root`.
- **Git history is a verification tool.** `git show '<sha>:<path>'` recovers any prior exact state. **To prove a closed section of a growing document is byte-identical, hash the section body between two headings** — §19's checker does this for three spans at once.
