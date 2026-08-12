# Human Report 5 — Claude

**Date and time:** 2026-08-11 19:11 PDT
**Session:** Claude Session 5
**Phase at start:** Phase 2 — Execution. Codex closed Phase 1 in its Session 4; both Claim Sheets and Study Guide Pass 1 are same-state approved and both review chats are concluded.
**Phase at end:** Phase 2 — Execution. First substantive Phase 2 work done: Tier A host and injection-zone selection, my share of the agreed labor split.

---

## The short version

I found that the project has been reasoning about its central feasibility constraint from a misreading of one column, and that the misreading has now been published twice in the public log.

The rule is sound: a synthetic waveform must not be borrowed from the same recording it is injected into, or the sorter is graded on a duplicate and the test is partly rigged. Applying it, Session 2 reported that the usable brain regions drop from 37 to 7. Session 3's review correctly softened that to "worst case, not the binding number" and said the actual host-specific query had never been run.

I ran it. **Every donor waveform for this probe type comes from the same public dataset the host recordings come from** — DANDI 000409 — from twelve animals. That dataset contains 139 animals. So **127 of them contribute no donor waveforms at all**, and choosing the host from one of those makes the exclusion vacuous rather than a matter of degree. Every region keeps its full pool. The seven-region shortlist that has been shaping this project's thinking since Session 2 only binds if the host is a library recording, and nothing requires it to be.

What that does *not* fix is worth stating as loudly: host and donor still come from one consortium, one rig design, one probe type, one processing chain. No available choice fixes that, because this probe type has exactly one donor collection. It is a property of the substrate and it goes in the limitations rather than being solved.

Separately, and less comfortably: **the hippocampal region the design has been leaning toward, CA1, has a hard ceiling of sixteen donor waveforms in the entire library**, against a budget of ten per run. That is a real constraint on the experiment, it is not fixable by adjusting a threshold, and it is now on the table before anything was built on top of it.

---

## What I did, in order

### 1. Read the provenance column instead of counting it

Session 2's audit treated the donor metadata's `dataset` field as an opaque token: count distinct values, drop the largest, report what survives. Reading the values shows they are structured:

```
000409_sub-KS055_ses-b22f694e-…_behavior+ecephys+image_8b735d77-….zarr
```

Each is one probe insertion from one DANDI 000409 session. Across all 2,183 Neuropixels 1.0 donor rows: **37 insertions, 24 sessions, 12 subjects**, zero rows that failed to parse, and no second source collection. (The library's other 5,694 rows are a different probe geometry and cannot be injected into a Neuropixels 1.0 host.)

That has a consequence nobody had named: **"exclude the host's source dataset" is three different exclusions** — same insertion, same session, same animal — and they give different answers. Of the 37 regions holding at least ten screened templates, the number surviving a worst-case exclusion is **7 at insertion level, 6 at session level, and 4 at subject level**. Regions whose templates all come from one animal — `SUB` with 57, `ENTl5` with 31 — look healthy at the loosest granularity and go to zero at the strictest.

Which granularity the project uses was never declared anywhere. It still needs to be, and §1.1 of the selection document is where I have put the case.

### 2. Established that the exclusion can be made vacuous rather than chosen

DANDI 000409 holds 918 NWB files: 459 raw electrophysiology recordings paired with 459 processed ones, across 139 subjects. Twelve of those subjects are in the donor library. **429 of the 459 raw recordings therefore belong to animals no donor comes from.**

Recommending we draw the host from one of those is not a clever workaround; it is strictly stronger than any exclusion rule applied afterwards, and it costs nothing because 93% of candidates qualify.

### 3. Found that the anatomical annotation the design needs already exists

The Claim Sheet requires each Tier A host to carry a pinned channel-by-channel anatomical mapping, because a Neuropixels probe crosses many structures and the design never assigns one region label to a whole recording. I had assumed this would have to be constructed.

It does not. Every 000409 NWB file already carries an electrode table naming an Allen atlas structure for each of its channels, with the channel's position along the probe. The raw and processed files for a session carry identical tables — I checked.

**And it can be read without downloading the recording.** The raw files are 18 to 197 GB. I wrote a small file object that serves HTTP byte-range requests to the HDF5 reader, so screening one candidate host costs about 5 to 10 megabytes and a handful of requests instead of an overnight download. That is what makes screening hundreds of candidates affordable at all on a project with no budget.

### 4. Built the bridge between two vocabularies, then checked it against the data

The host names structures with Allen long names (`Field CA1`); the donor library uses acronyms (`CA1`). Without a bridge, "region-matched" cannot be evaluated at all. I wrote one.

**A hand-authored lookup table is exactly the kind of artifact that looks obviously right and is quietly wrong in two entries**, so I did not want to trust it. There is independent evidence available and it is nearly free: every donor template carries both an acronym and a depth, and the same session's recording names a structure at that same depth. Comparing the two vocabularies at the same physical place on the same probe checks the table — and checks something else nothing in the project had checked, which is that the two sources mean the same thing by "depth".

Across all 37 donor insertions: of the **1,403 comparisons the table could in principle have got right, 1,401 agree, 1 disagrees, and 1 falls on a host label the table does not cover.** Forty-four structures are confirmed with no disagreement at all, including `CA1` — the one that matters most here — at **16 of 16**, and every large-pool alternative: `CP` 107/107, `SUB` 168/168, `PIR` 94/94, `MRN` 59/59, `ENTl5` 53/53, `AON` 53/53, `VISa5` 49/49, `LP` 47/47. **Nothing was contradicted.** A further 650 donor rows name structures the table does not define, which measures its coverage rather than its correctness.

### 5. Caught my own analysis overstating a problem — twice — and fixed both before anything depended on them

The first version of that check sorted every structure into "confirmed" or "CONTRADICTED", where a single disagreement was enough to land in the second list. That put `ACAd5` — 33 agreements against 1 disagreement — in the same bucket as structures that never matched once.

Fixing that exposed a second and worse one. The check was counting a donor whose structure my table **never defined** as a *disagreement* — but a structure the table makes no claim about cannot disagree with anything. That single confusion manufactured **49 "contradicted" structures out of nothing but the table's own incompleteness**, and reported the agreement rate as 92% when it is 99.9%.

Both errors ran in the same direction: they made my own work look more broken than it was. That is worth saying plainly, because it is the less obvious failure mode. A project that is careful about not overstating its successes can still publish a number that is wrong in the flattering-to-nobody direction, and a reader who acts on "49 structures are unusable" has been misled exactly as much as one who acts on an inflated result. The honest report says: the table has **one** ambiguous entry, **zero** wrong ones, and a large **coverage** gap — three different things that the first two versions blurred into one.

### 6. Surveyed candidate hosts for a CA1 injection zone

Screening criterion: a raw recording, from an animal absent from the donor library, whose probe carries a contiguous run of channels labelled `Field CA1`. **46 of the 429 eligible recordings were screened, and 13 of the 81 probes in them carry a usable band**, the widest spanning 72 channels. Full results are in §4 of the selection document and in `Reproducibility Packet/results/host_anatomy_CA1.txt`.

**This survey is partial, it is not a random sample, and the document says both in its own §4.1.** The 46 are simply the first 46 in the archive's listing order, which clusters by animal — two labs account for 44 of them. So a better host almost certainly sits in the 383 not yet looked at, and no sentence anywhere in this session's output claims otherwise. What the 46 *do* establish is that CA1 hosts are not scarce, which means the binding constraint on Tier A is the donor pool rather than the host supply.

The gates that will actually decide between candidates — drift, noise, effective signal-to-noise after rescaling, ten-placement feasibility, covariate balance — are all untested. A host must not be pinned off a partial ranking without someone explicitly deciding that "good enough" beats "best available".

---

## The decision I am proposing, and what it costs

**Injection zone: CA1. Host: a 000409 recording from an animal absent from the donor library, with a contiguous CA1 band.**

The reason is that CA1 is the only zone that satisfies Tier A and Tier C at once, which Session 3 established as a joint constraint rather than two separate searches. Tier C's burst parameters have to rest on primary evidence, and the evidence the project has secured is CA1-specific (Harris et al. 2001). Moving the zone to a bigger-pool region such as `CP` (70 templates) or `SUB` (57) does not remove work — it moves the work to a literature task nobody has done, and risks exactly the failure Session 3 named: satisfy Tier A, then discover Tier C cannot use the zone Tier A picked.

**The cost, stated plainly.** CA1 has 16 donor templates in the entire library and no threshold produces more, because no more exist. Twelve sit inside the project's screening caliper; the four outside it are high-amplitude, high-quality templates that the Claim Sheet's own logic says should be eligible, since the caliper's amplitude range is an injection *target* rather than a donor requirement. So the working pool is 16 for a 10-unit arm: **six spares**.

That has a second-order consequence I have flagged rather than buried. The design calls for five randomisation blocks with the draws varying between blocks. With 16 candidates and 10 slots, **the region-matched arm has almost no donor variability across blocks** — every block reuses most of the same templates — while the comparison arm draws from over a thousand. That asymmetry is most likely to show up in the negative-control band, which is Codex's to own, and it is better raised now than discovered at analysis time.

I have written four named fallbacks in order, from cheapest to most disruptive, ending with dropping Tier A — which the Claim Sheet already pre-declares as a clean, publishable failure rather than a disaster.

**I am the wrong agent to grade this.** Codex owns Tier A's independent balance and manipulation gate precisely so the agent proposing a selection is not the agent approving it. The document proposes; it does not approve itself.

---

## Challenges, and how they were handled

**The survey is slow and I could not finish it.** Reading one recording's metadata takes 10 to 90 seconds depending on contention, so 459 recordings is many hours. I chose to treat it as a search rather than a census, run it in the background, stop it cleanly at the end of the session rather than leave a process writing files after the work was committed, and state coverage explicitly everywhere the result appears. The index is resumable with the identical command.

**Two background jobs contending slowed both.** Running the anatomy survey and the label-map validation at the same time roughly halved each. Worth knowing for next session: run one at a time, or add parallel workers to the survey.

**A first dependency had to go into the project's environment.** Reading remote HDF5 needs `h5py`. I installed it, pinned it and its transitive `numpy` with versions in a new `requirements.txt` in the same session per the standard, documented both licences (BSD-3-Clause), and left a note in the file for whoever installs the sorting stack that the numpy pin may need to move — so the environment does not quietly drift away from the file.

**I had to decide whether to refactor working code mid-session.** The Session 2 audit script now duplicates logic that lives in the new shared `utils/` module. Refactoring a validated artifact while building on top of it risked breaking it for no gain this session. I left it and recorded the duplication in two places rather than leaving it silent, to be resolved before the packet is assembled.

**A report file has to match the script that produced it.** Fixing the validator's classification meant the already-written output no longer matched the code, including one explanatory sentence that gave the wrong reason for five entries. Re-running cost about ten minutes of background time and I did it, because a packet whose outputs cannot be regenerated from its own scripts fails the standard the packet exists to meet.

**A dropped connection cost a whole recording, and that was a design flaw rather than bad luck.** One re-run hit a transient S3 disconnect and lost an entire insertion's worth of comparisons — the reader issued a range request, the connection closed, and the recording was abandoned. Screening runs make hundreds of sequential requests to one host, so at that volume a dropped connection is routine, not exceptional. I added bounded retries with backoff to the remote reader rather than accepting a thinner result, and re-ran. The alternative — publishing the smaller number with the failure documented — would have been honest but would have left the same flaw waiting for the next run.

---

## Files created or updated

| Path | Change |
|---|---|
| `Reproducibility Packet/scripts/utils/` | **New.** `remote_hdf5.py` (HTTP-range file object for h5py), `dandi.py` (asset listing and addressing), `template_metadata.py` (donor CSV, snapshot pinning, caliper, provenance parsing), `ccf_labels.py` (atlas name ↔ acronym bridge), `__init__.py`. |
| `Reproducibility Packet/scripts/audit_donor_provenance.py` | **New.** Provenance granularity and host-specific donor exclusion. |
| `Reproducibility Packet/scripts/survey_host_anatomy.py` | **New.** Host anatomy survey and injection-zone band finding, resumable. |
| `Reproducibility Packet/scripts/validate_ccf_label_map.py` | **New.** Validates the label map and the depth-coordinate correspondence against the donor library. |
| `Reproducibility Packet/results/` | **New outputs:** `donor_provenance_2026-08-11.txt`, `ccf_label_map_validation.txt`, `host_anatomy_index.jsonl`, `host_anatomy_CA1.txt`, plus two pinned upstream snapshots — `templates_snapshot_2026-08-11.csv` and `dandi_000409_assets.json`. |
| `agents/Claude/Tier A Host and Injection Zone Selection.md` | **New.** The proposal, its evidence, its costs, and what it explicitly has not tested. |
| `requirements.txt` | **New.** First dependency install pinned at install time, with licences and a forward note. |
| `agents/Claude/references.md` | Extended: what the donor `dataset` column actually contains and what it changes; DANDI 000409 asset structure and its electrode annotation; `h5py`. |
| `director_requests.md` | Fifth and sixth memory measurements appended — the contention trend broke, recorded as a data point rather than an answer. |
| `README.md` (root, Live-Run) | One running-log entry: the 37→7 constraint is avoidable, with the residual confound named and the CA1 ceiling stated. |
| `agents/Claude/README.md` | Workspace map, new file descriptions, ownership table, review states corrected to concluded. |
| `.gitignore` | Comment block naming the pinned snapshots as deliberately tracked, so nobody adds a blanket rule that catches them. |
| `chats/Claude-Codex/Tier A Selection Review/` | **New chat**, opened with the handoff and three explicit rulings requested of Codex. |
| `agents/Claude/Summary of Only Necessary Context.md` | Completely rewritten for Session 6. |

---

## Machine measurements, per the contract

| When | Free system RAM | Free VRAM |
|---|---|---|
| 2026-08-11 18:14 PDT | 15.27 GiB of 31.67 | 14,416 MiB of 16,311 |
| 2026-08-11 18:45 PDT | 14.39 GiB of 31.67 | 14,405 MiB of 16,311 |

The four previous sessions measured 3.46, 3.96, 1.01 and 0.89 GiB free. Something released roughly 28 GiB between 16:06 and 18:14. **This is a data point, not an answer** — it argues against adopting a hard small-memory design ceiling on current evidence, and it says nothing about whether a quiet window is predictable. No heavy step was attempted this session; the work was metadata-only and never approached the floor.

---

## Next steps

1. **Codex reviews the selection proposal** in `chats/Claude-Codex/Tier A Selection Review/`, and specifically rules on the exclusion granularity, the CA1-versus-larger-pool trade-off, and whether the near-exhausted matched pool changes the block scheme.
2. **Finish the host survey**, or explicitly accept a good-enough host over a best-available one. Same command, same index.
3. **Complete the atlas label map** before the region-unaware arm's placement can be evaluated. This has a licensing question attached — the permissively licensed packages that redistribute the Allen atlas versus the Allen Institute's own terms — and that should be resolved before importing an ontology, not after.
4. **Codex's Rung 0 feasibility pilot** remains the next heavy step, and memory looks available for it right now in a way it has not all day.
5. Refactor the Session 2 audit script onto the shared `utils/` module before the packet is assembled, and give the packet folder the three files it still owes — its own dependency list, its own ignore file, and the runbook that makes it work when copied somewhere on its own.
