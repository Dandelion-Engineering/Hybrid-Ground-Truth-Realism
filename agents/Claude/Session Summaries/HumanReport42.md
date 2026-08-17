# Claude Human Report — Session 42

**Date and time:** 2026-08-17 09:20 PDT

**Phase:** Phase 2 — Execution (owner response inside an open review card)

**Outcome:** RC-006 Round 1 returned `Revisions Required` with four findings against §18, the section reporting the project's first real measurement. **All four are accepted, none is disputed, and all are repaired.** A fifth instance of one finding's defect — in a section the finding did not name — was found and repaired too. **No code file changed, no archive was read, and the measured result did not move.** Draft 28 is handed back for delta-only Round 2.

---

## 1. What the session was for

Session 41 measured rank 1 (CSHL047 Probe01) against the DANDI archive and reported it in §18 of `agents/Claude/Tier A Host and Injection Zone Selection.md`. Codex reviewed that section as RC-006 Round 1 and returned it.

**The result itself survived the review completely.** Codex re-ran runbook step 11 from the packet and obtained a **byte-identical report and byte-identical JSON record** at the two committed digests. `Delta_10min` is still **1.821 µm** against a 20 µm tolerance, `Q95_null` still **0.526 µm**, the reconciled disposition still `passes` with `advances` True and `conflict` False. What he returned was not the measurement but **the prose reporting it** — specifically the resource-accounting paragraph, which had three defects, and one wrong line count.

This session is the single owner response the review method allows.

## 2. The four findings, and what each repair actually is

### F1 — a four-part total that named three parts

§18.2 said the read plan's **131,985,507-byte** bound comprised the resident arrays, the live Python structures and the HDF5 chunk cache. Those three sum to 72,944,771. The omitted term is `cache_bound_bytes` — **59,040,736 bytes**, the bound on distinct archive block bytes the range reader retains — and it is **the largest of the four.**

I verified this against the committed record rather than accepting it: `plan.cache_bound_bytes` is 59,040,736 and the four terms sum exactly to `plan.peak_resident_bytes`. §18.2 now carries a table of all four with the sum shown, and additionally spells out `resident_bytes`' own three parts, which Draft 27 did not: 50,564,976 bytes of converted float64 arrays, 3,160,311 of retained missing-depth masks, and 1,395,152 for the largest single unit's slice at its stored width (87,197 spikes × 16 bytes).

**Where the defect was not is the part worth recording.** The tool's own report names all four terms in its resource block, and the JSON record carries all four under `plan`. **The instrument was right and the section reading it was wrong.** §18 is entirely a reading of an output, so that is the failure mode this document is most exposed to.

### F2 — a headroom claim that was false by two orders of magnitude

§18.2 said the plan cleared the 75%-of-free admission rule and the 4 GiB remaining-memory floor "by three orders of magnitude". I recomputed both factors from the recorded free-memory reading and reproduced Codex's numbers exactly:

- **75%-of-free:** `0.75 × 15,860,760,576 = 11,895,570,432` bytes against a 131,985,507-byte plan — **90.128×**.
- **4 GiB floor:** `15,860,760,576 − 131,985,507 = 15,728,775,069` bytes remaining — **3.662×** the 4,294,967,296-byte floor.

Admission genuinely cleared, and the binding rule is the floor, at a factor of 3.662. §18.2 now states both factors and which one binds.

**Deriving them surfaced a second thing.** Codex's finding wrote the free-memory reading as *15,126 MiB* where Draft 27 wrote *MB*, and he was right to. I checked the source: the reading comes from `Win32_OperatingSystem`'s kibibyte counters, and its companion total — 32,425 — is only this machine's 31.665 GiB of usable RAM when read as mebibytes. **His factors are correct because he read the unit correctly.** On the megabyte reading they would have been 85.95× and 3.49×. §18.2 now states the unit and states that both factors carry the mebibyte rounding of the reading, which is the only precision it was recorded at.

### F3 — two rough samples presented as an isolated measurement

This is the one that matters. Draft 27 observed the command's process working set at about 162 MB during the archive read and about 213 MB once the missing-depth layer engaged, and turned that ~51 MB step into three claims: that the step **is** the unconditional finite-only split, that §17.12's 50,561,280-byte projection is **now a measurement**, and that any later whole-command memory ceiling **inherits it as one**.

**None of the three follows, and Codex is right.** A process's working set holds the interpreter, the allocator's arenas, every loaded library and every other live allocation, so a difference between two samples of the total bounds no single term inside it. The samples were also recorded rounded to the megabyte, which is coarser than the quantity being attributed. And one sampled pair on one candidate is not a reproducible ceiling even if the attribution held.

§18.2 now reports the observation as **consistent with** the projection and says explicitly why that is the ceiling of what it supports. The projection stays a projection. **An empirical whole-command ceiling would need a full-run monitor with an accounting that attributes the resident set to its parts, and this project has not built one.** RC-005's tracked follow-up 1 stays open.

**F3 had a second instance the finding did not name.** §18.7's closing paragraph also said follow-up 1 was "now carrying a measurement instead of a projection". Codex's finding named §18.2 only. **A finding's *reason* is a general claim, so I went looking for the rest of it** — §11's finding 19 — and repaired that sentence too. It now says explicitly that follow-up 1 is neither discharged nor converted into a measurement.

**I found it by rendering the repaired section and reading it, not by reading my own diff.** That is finding 26 doing precisely the job it exists for, and it is the strongest argument this session produced for keeping it.

### F4 — a line count, and where it came from

§18.7 said `--help` renders 165 lines; it renders **164**. I re-derived it rather than taking the number: the rendered help is 11,040 bytes containing 164 newline characters, `splitlines()` gives 164, and splitting on `\n` gives 165 because of the trailing newline.

**But the interesting part is that 165 was not a counting artifact.** The module docstring reaches `--help` verbatim through `argparse`'s `RawDescriptionHelpFormatter`, and I proved the step-11 rewrite made that docstring exactly one line shorter — 129 lines to 128, compared across `2a610dc` and `HEAD` by parsing both files' docstrings. So 165 was **correct for the state before the change §18.7 is reporting**, and HumanReport40's 165 was right for its own state. The number was carried across a state boundary instead of being re-measured on the bytes whose digest §18.7 publishes.

That is §11's **finding 62** on a one-line claim, and §18.7 now records it that way rather than silently correcting the digit. The general form is what will catch the next one: **a rendered-surface count is a property of a state, and a section that publishes a digest is publishing a state.**

### §18.8 — two bullets, one of which had gone stale

The bullet reading "This section is unreviewed" had gone stale in the permissive direction the moment Codex read it. It is replaced by one that records the review, its outcome, and the fact that **Codex's independent replay reproduced the report and record byte-for-byte** — the values in §18.3 and §18.4 have now been produced twice, by two agents, from the archive.

A second bullet records that **the public running-log entry for this measurement overstated it in four ways** and carries Codex's appended forward correction. See §4 below.

## 3. Evidence

`agents/Claude/tools/probe_rc006_repairs.py` is new, read-only, and reads no archive: **61 checks, 0 failed**, recorded in `probe_rc006_repairs_2026-08-17.txt`.

A reversion harness of the `verify_rc00*` shape does not apply here, because prose has no behaviour to break. What the probe checks instead:

| what | result |
|---|---|
| all four plan terms present in §18.2 and summing to `peak_resident_bytes` | ok |
| `resident_bytes`' three parts, including that the slice term is a whole number of spikes | ok, 87,197 |
| both admission factors, to the stated precision | 90.128 and 3.662 |
| the floor is the binding rule; no factor reaches three orders of magnitude | ok |
| the F3 language is "consistent with", the projection is still called a projection | ok |
| rendered `--help` re-measured on the authenticated command | **164 lines, 0 non-ASCII** |
| the five defective sentences are **gone rather than reworded** | ok |
| each of the four repairs is marked exactly once | ok |
| §1–§16 span | **144,664 bytes**, `700b3b9a…` — unchanged |
| §17 body | **21,864 bytes**, `dc73b87f…` — unchanged |
| `Delta_10min`, `Q95_null`, `passed`, `label`, `inside_null`, disposition, `advances`, `conflict` | all unchanged |

**The first version of the probe failed twice, and both failures were in the probe rather than in the repairs.** One assertion required a phrase to be absent from the document when the repair deliberately *quotes* that phrase — the check would have fired on a correct repair. The other read a key that does not exist on the record (`null.q95_lo` rather than `null.q95`). This is §11's finding 25 in its ordinary form: when a check fails, the check is a candidate for being the broken thing.

**One judgement I flagged to Codex rather than settling myself.** The probe is a claim-checker, not a harness that can go red on a real defect, and by §11's finding 57 that is a weaker instrument than the ones this card's other evidence uses. I think it is the right instrument for prose repairs and that a mutation harness over a document would not be worth its cost — but that is a judgement about evidence made by the person whose repairs it checks, so I said so and left it to him.

## 4. The correction that was not part of the review

Outside RC-006, Codex read the **public** running-log entry I wrote about the measurement and appended a forward correction. He is right on all four points, and I have not argued any of them: the entry called the 174 archive objects "neurons" where they are label-blind units or clusters; it described `Q95_null` as what measurement noise can produce rather than as a conservative diagnostic under a stated assumption; it framed the result as a statement about the physical probe holding still; and it dated §16.8's masking fixture to months rather than days ago.

**The part I think is worth carrying out of this project is that §18.8 already said all three of the substantive things correctly, and I wrote §18.8 first.** The technical section had the boundaries; the plain-language entry lost them; and no step in that felt like dropping a qualifier — each felt like writing more clearly. "Label-blind units or clusters" reads as jargon and "neurons" reads as English. "Conservative under a stated additive model" reads as hedging and "the estimator's own noise floor" reads as clear.

That matters beyond this incident because **the Accessible Piece is the artifact Randy takes out of the building**, and it is written in exactly the register most likely to strip the conditions off a result — while the review effort is pointed at the Technical Report, where the boundaries are already careful and almost nobody checks them. I posted this as a method observation in `chats/Claude-Codex-Human/Review Method Change/`, with a concrete suggestion: when accessible writing describes a result whose technical section has a stated-boundaries list, **read the list beside the text sentence by sentence as a review step, rather than recalling it.** Every one of my four overstatements is contradicted by a bullet I had already written; a reader with both open catches all four in one pass.

## 5. Machine state and costs

**No heavy step ran this session.** No archive was read, no measurement was made, and nothing was installed. The venv is unchanged: `h5py==3.16.0`, `numpy==2.5.2`.

Readings taken at the times stated, not inherited:

| moment | free RAM | GPU |
|---|---|---|
| 2026-08-17 09:05 PDT (session open) | 14,021 MiB of 32,425 | 1,127 of 16,311 MiB |
| 2026-08-17 09:20 PDT (close) | 13,422 MiB of 32,425 | 1,179 of 16,311 MiB |

Costs: `probe_rc006_repairs.py` runs in about two seconds and its only subprocess is one `--help` render. Nothing was left running in the background and no temporary directories were created; the standing check for stray scratch trees is 0.

## 6. Files created or updated

**Created**

- `agents/Claude/tools/probe_rc006_repairs.py` — `512e31fc…`
- `agents/Claude/tools/probe_rc006_repairs_2026-08-17.txt` — `745da38a…`
- `agents/Claude/Session Summaries/HumanReport42.md` (this report)

**Updated**

- `agents/Claude/Tier A Host and Injection Zone Selection.md` → **Draft 28**, `157905c90bfd170cc79f82c045a08e60c7da63c8ed5d5740b431ca24583a16d3`
- `Review Cards/RC-006 Rank 1 Drift Measurement and Step 11.md` — Round-2 candidate table, round log, and the owner response
- `Review Cards/README.md` — index row for RC-006
- `README.md` — one running-log entry
- `chats/Claude-Codex/Rank 1 Drift Result/Rank 1 Drift Result - Active.md` — one appended Round-2 handoff
- `chats/Claude-Codex-Human/Review Method Change/Review Method Change - Active.md` — one appended method observation
- `agents/Claude/README.md` — workspace tree
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten

**Unchanged, and deliberately so:** every file in `Reproducibility Packet/`. No script, no utility, no result artifact and no runbook step moved.

## 7. What this does and does not settle

**Rank 1 has cleared one of five host gates.** Noise and post-rescaling effective SNR are open and mine, and **neither is specified yet** — that remains the largest open piece in my lane. The joint ten-placement condition and the balance gate are open and Codex's. **No host is pinned. Rank 2 is unmeasured and keeps its rank.** Ranks 5, 7, 9 and 13 remain paused on the declared-clock disagreement. Nothing about the generator, the donor library, the sorter panel or any tier is touched.

## 8. Next steps

1. **Codex's Round 2 is delta-only** against the repaired reporting surfaces plus candidate authentication. If he returns `Revisions Required` again, one more round-trip remains before the method requires a Convergence Decision.
2. **The noise gate and the effective-SNR gate need specifications**, written in §16's shape — the quantity and its parameters defined before any candidate is read. **I deliberately did not start one this session**, because the document those sections would join is the artifact currently under review, and adding to it mid-card would change what Codex is reviewing. That work starts once RC-006 closes.
3. **Rank 2 can be measured** whenever a session chooses to spend the three minutes and the resource check clears, using the unchanged step-11 command.
4. **RC-005's tracked follow-ups 1, 2 and 4 remain open**, and follow-up 1 is explicitly *not* discharged by this session's working-set observation.
5. My next session is 43; the next count-based progress report falls at Session 48.
