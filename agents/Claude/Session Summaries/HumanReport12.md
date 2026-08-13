# Human Report 12 — Claude

**Current date and time:** 2026-08-12 20:30 PDT

**Session:** Claude Session 12

**Phase at start:** Phase 2 — Execution. Amendments 1–5 all `In force` (Codex put Amendment 5 into force at the end of its Session 11). No host pinned, no Rung 0, no generator, no sorter run, no scientific result.

**Phase at end:** unchanged. Nothing this session touched the contract, a recorded result, a dependency pin or a licence claim.

**Progress-report trigger:** none. My next count-based report is Session 16, no phase closed, and I put no amendment into force.

---

## Summary

Two pieces of work, both in the Reproducibility Packet, which is the artifact that carries this project's entire claim to being checkable.

**First, I closed the review Codex opened.** Codex found that the packet's runbook described a validator as checking the *newly derived* anatomical label map when the code deliberately does not — that check would be circular, since the derived map is built by voting over exactly the comparisons the validator would score. I verified the claim against the source rather than accepting the description, checked whether the same wrong claim appeared anywhere else in the repository (it does not; eight other mentions all describe it correctly), and approved Codex's exact bytes.

**Second, I fixed the defect I had named last session as my own largest open item, and it turned out to be worse than I had recorded.** Every packet script prints a worked example in `--help`, and those examples were written for the project's own working directory rather than for the packet a stranger downloads. So the first thing a reader sees contradicted the runbook they had just been told to follow. Most examples were also stale in substance — missing arguments the recorded results actually used, or showing a mode that does not reproduce the tracked report — and one script had no example at all. One script cited a file that does not exist inside the packet.

The ten examples are now generated from the runbook rather than typed a second time, a new script checks that the two can never silently disagree again, and that checker is tested against ten deliberate breakages rather than by watching it pass.

**The session's most useful finding came from rendering rather than reading**, and it is recorded below because it generalises.

No scientific execution occurred and no result exists.

## 1. Startup, and the state I inherited

`.agent-turn` named Claude; `.agent-session.lock` did not exist. I created the lock, re-read the turn, confirmed it still named Claude, then followed `AgentPrompt.md` in order: Project Details in full, my own continuity summary, every chat `Summary.md` that includes me, and both active chats before replying to either.

The Tier A chat had moved while I was away. Codex approved my Session 11 handoff — Claim Sheet, Accessible Claim Sheet, and Draft 7 of the Tier A artifact — accepted all three of my additions unchanged, and flipped **Amendment 5 to `In force`**, writing the event-triggered progress report that came with it. That closes the item my last summary said was first in line for this session, and nothing in that chat was open for me, so I did not post there.

A new chat existed: `chats/Claude-Codex/Reproducibility Packet Review/`, opened by Codex, with an owner re-review waiting for me.

## 2. The owner re-review, and what I checked rather than accepted

Codex's claim was that `validate_ccf_label_map.py` validates the **hand-authored** label table and the depth-coordinate agreement, not the derived label layer the runbook said it validated.

I checked the code, not the description:

- `utils/ccf_labels.py:133` declares `to_acronym(label, default=None, include_derived=False)`, and the derived branch is behind that flag.
- `validate_ccf_label_map.py` calls `to_acronym(location)` exactly once, at line 113, with the flag left at its default.
- Its two other reads of the module, at lines 94 and 318, both build from `NAME_TO_ACRONYM`, which is the hand-authored table alone.

So importing the module loads the derived JSON, but nothing in that script ever consults it. The description is exact. The circularity argument also holds in a form a reader can check: `derive_ccf_label_map.py` builds each derived entry by supermajority vote over (donor acronym, host long name, same depth, same insertion) tuples, and those are precisely the tuples the validator scores. Scoring the derived entries there would be scoring a vote against its own ballots.

**Then I checked where else the repair applies**, on the principle that a repair's reason is a general claim rather than a local fix. Every other mention of the validator — five places in the Tier A artifact, two entries in `references.md`, two script docstrings, and the Tier A chat — describes it as checking the hand-authored table. There was no third occurrence. That is itself informative: the defect entered when those two public documents were written last session rather than propagating from an older error.

I recorded one thing Codex's edit drops and explicitly did **not** ask for it back: the old text mentioned that the report breaks results down per structure. The accuracy gain is worth more than the lost detail, and asking would have cost a round-trip for a cosmetic gain. Saying so makes the omission a decision rather than an oversight.

I approved both exact hashes.

## 3. The defect I owned, and how much of it was mine

Last session I recorded that the packet's script docstrings printed project-root-relative example commands, and that `argparse` puts those docstrings at the top of `--help`. Reading them properly this session showed the problem was larger than a path convention:

| script | what the example actually said |
|---|---|
| `audit_donor_provenance.py` | omitted `--detail-area`, and named an output file that is not the tracked one |
| `audit_template_library.py` | no `--cache`, then a paragraph below telling the reader to pass `--cache` |
| `screen_injection_placement.py` | the archive form, not the `--from-records` replay that reproduces the report |
| `derive_ccf_label_map.py` | likewise the archive form |
| `survey_host_anatomy.py` | two excluded subjects instead of the twelve the recorded run excluded |
| `audit_subject_provenance.py` | four subjects instead of the recorded twenty-one, and no `--records` |
| `validate_ccf_label_map.py` | no `--templates-cache` |
| `audit_amplitude_conventions.py` | no example at all |
| `screen_host_timing.py` | plus a citation of `agents/Claude/Tier A Host and Injection Zone Selection.md`, a path that does not exist inside the packet |

**I generated the ten replacements from `README.md` rather than transcribing them.** Session 11 is the reason: two of five hand-written runbook commands were wrong and looked perfectly plausible, and only a byte-diff found them. A generator cannot make that class of mistake.

Two docstring paragraphs then contradicted their own new command, so I inverted them rather than leaving them: `audit_template_library.py`'s `--cache` note, and `survey_host_anatomy.py`'s note about the `--legacy-index-*` flags — whose refusal behaviour I confirmed in `anatomy_index.validate_configuration` rather than assuming it.

For the out-of-packet references I added a short **Design documents these scripts refer to** section to the packet README. Several scripts explain a choice by naming the project's Claim Sheet, and a reader who copied the folder out had no way to know what that is. The section names the repository, states that neither document is needed to run anything, and says why a stale copy inside the packet would be worse than a pointer.

## 4. The finding: rendering caught what reading could not

I first wrote the examples as backslash-continued multi-line commands. In the source they looked correct. I rendered `--help` to check, and it printed **one long line with runs of spaces in it**.

The cause is that a backslash before a newline inside an ordinary (non-raw) Python docstring is an escape: Python deletes the newline. The source looks neatly wrapped; the string `argparse` prints is not. Reading the file would never have shown this. It also would have handed a Windows PowerShell reader a command that does not work at all, since a trailing backslash is not a line continuation there.

Two consequences, and the second is the one I would have got wrong:

1. The examples are single lines now, matching the README exactly and copy-pasting on every shell.
2. **The checker compares whole strings, not shell tokens.** The collapsed form has *identical* tokens to the correct form — a token comparison would have called it agreement. It also reads the docstring through `ast`, so what it compares is the string `--help` prints rather than the source behind it. When tokens match but characters do not, it prints a note saying to look for a collapsed continuation, because that failure is otherwise invisible in a diff.

## 5. The checker, and testing it by breaking things

`Reproducibility Packet/scripts/check_runbook_consistency.py` compares every numbered runbook step against its script's `Example` block, and checks that each script has exactly one step and names the right step number. It parses; it never imports, downloads or writes.

Deleting one of the two copies would have been the tidier fix, but a reader running `--help` should not have to open a second file to find a working invocation. So both copies stay and are checked against each other.

**Tested by mutation, ten cases, each on its own clean copy so one cannot mask another, plus an unmutated control:**

| mutation | caught |
|---|---|
| flag changed on the docstring side | yes |
| the same flag changed on the README side | yes |
| wrong step number in the docstring | yes |
| step number not named at all | yes |
| `Example` block deleted | yes |
| a second `Example` block added | yes |
| a script added with no runbook step | yes |
| a step naming a script that is gone | yes |
| a doubled space in the command | yes |
| a real backslash line continuation | yes |

All ten fail with the specific reason printed; the control passes. The harness is kept at `agents/Claude/tools/mutation_test_runbook_checker.py` — in my workspace rather than in the packet, because it mutates a copy of the packet and reproduces no result, so it does not belong in a folder whose contents a stranger is told to run.

## 6. Validation, and what it cost

I copied the packet alone to a short path, built a fresh virtual environment from its own `requirements.txt`, and ran only the commands the runbook prints. Twice — once before the final rewrite and once after.

- Steps 2, 3, 4 and 8 reproduce their tracked reports **byte for byte**; step 1 differs in exactly its two documented header lines, which only a live HTTP response can supply; step 4's JSON matches byte for byte.
- The consistency check passes inside the copy.
- All eleven scripts compile, and `--help` renders for every one of them, each showing a packet-relative command and none showing a path from outside the packet.
- `grep` finds no remaining `venv/Scripts`, `Reproducibility Packet/` or `agents/` reference in any packet source.

One piece of housekeeping worth recording because it was self-inflicted: a mid-session `git checkout` restored `screen_host_timing.py` with CRLF line endings, and my generator then wrote an LF block into it, leaving a single mixed-ending file. I normalised it back to LF to match its ten siblings. Related, and caught by the same look: the generator ran against the CRLF version, failed to find its marker, and appended a *second* `Example` block instead of replacing the first. The checker's duplicate-block case exists because of that.

## 7. Two things I flagged for Codex's judgement rather than deciding alone

- The checker treats any new file in `scripts/` as owing a numbered step, with itself as the single hard-coded exception. A docstring marker would be less brittle; I did not want to invent that convention unilaterally.
- I kept an example in every docstring rather than replacing it with "see README Step N". The argument is that `--help` should be sufficient on its own, and the checker is what makes keeping two copies safe. If Codex rejects that premise, the checker is the wrong answer rather than a partial one, and I said so in the handoff.

## 8. Machine state

Measured at 2026-08-12 20:10 PDT, immediately before doing anything: **RAM 12.28 GiB free of 31.67; VRAM 987 MiB used of 16,311; 649 GB free on `C:`.** Re-checked at 20:24 with no material change.

Nothing heavy ran. The session's entire execution was stdlib parsing and arithmetic, two fresh virtual-environment installs of two pure-Python-plus-wheels dependencies, five offline replays against a 2 MB pinned CSV, and eleven `--help` renders. No archive read, no recording data, no template array, no generator, no sorter. Both temporary packet copies and the scratch mutation directories were deleted before closeout.

## 9. Files created or updated

**Created**

- `Reproducibility Packet/scripts/check_runbook_consistency.py`
- `agents/Claude/tools/mutation_test_runbook_checker.py`
- `agents/Claude/Session Summaries/HumanReport12.md`

**Updated**

- `Reproducibility Packet/README.md` — the design-document pointer, the checker section, the validation record
- All ten packet step scripts — `Example` blocks; plus prose in `audit_template_library.py`, `survey_host_anatomy.py`, `screen_host_timing.py`
- `chats/Claude-Codex/Reproducibility Packet Review/Reproducibility Packet Review - Active.md` — two appended turns
- `README.md` (root Live-Run) — one running-log entry
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

**Deliberately unchanged:** `Claim Sheet.md`, `Accessible Claim Sheet.md`, `Reproducibility Packet/DATA.md`, every file in `Reproducibility Packet/results/`, both `requirements.txt` files, `references.md` (no new source was consulted), and `director_requests.md` (nothing this session was blocked on the director).

## 10. Next steps

1. **Codex re-reviews the twelve states handed off** in the packet chat, and rules on the two open judgement calls in §7.
2. **The host-selection gates that are mine are still open**: drift, noise, and post-rescaling effective SNR. Drift is the awkward one — the processed file's own `cumulative_drift_um_per_hour` column reaches values that cannot be net probe drift, so the quantity has to be defined before it can be measured, and a threshold cannot be set from the first numbers seen.
3. **Codex owns the real-arm matching rule**, now unblocked by Amendment 5, and the footprint/placement calibration.
4. Nothing is waiting on the director.
