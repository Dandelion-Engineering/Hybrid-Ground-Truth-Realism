# Reproducibility Packet — Hybrid Ground Truth Realism

Spike sorting decides which extracellular spikes came from which neuron. Real
recordings have no answer key, so the field grades sorters against **hybrid
recordings** — a real recording with synthetic spikes injected at times that
are known by construction. This project asks whether making those synthetic
spikes more realistic changes the measured accuracy, and in particular whether
it changes the *ranking between sorters*.

This folder holds everything needed to re-run that work on your own machine.
**It is self-contained**: copy this folder alone to a clean machine, follow the
steps below, and nothing will reach outside it.

> **Status: the experiment has not run yet.** What this packet currently
> reproduces is the design and feasibility work that precedes it — the donor
> template audits, the host-recording screens, and the anatomical label
> derivation that the injection-zone choice depends on. No spike sorter has
> been run, no hybrid recording has been generated, and no accuracy result
> exists. The steps below reproduce exactly what is in `results/`, and nothing
> in this packet claims more than that.

---

## Contents

```
Reproducibility Packet/
├─ README.md              this runbook
├─ DATA.md                the two external data sources, licences, citations
├─ requirements.txt       pinned dependencies
├─ .gitignore
├─ scripts/               one script per purpose; shared logic in scripts/utils/
│  └─ utils/              data access, geometry, and the derived label map
└─ results/               recorded reports, and the pinned inputs they used
```

## Setup

Requires Python 3.10 or newer (recorded on 3.12.10). From inside this folder:

```bash
python -m venv .venv
```

Then install the two dependencies — on Windows:

```bash
.venv/Scripts/pip install -r requirements.txt
```

or on macOS and Linux:

```bash
.venv/bin/pip install -r requirements.txt
```

Every command below is written as `python …`, meaning **that** interpreter.
Activate the environment first, or substitute `.venv/Scripts/python` (Windows)
/ `.venv/bin/python` (macOS, Linux) for `python` in each command.

> **On Windows, keep this folder's path short.** Placing it deep inside a
> nested directory can push `h5py`'s compiled libraries past the legacy 260-
> character path limit, and the failure surfaces as
> `ImportError: DLL load failed while importing _errors: The filename or
> extension is too long` rather than as anything about paths. Somewhere like
> `C:\work\` avoids it, as does enabling long-path support in Windows.

### Convenience values used throughout

Every command is run **from this folder**, and every path below is relative to
it. Two values recur:

| value | meaning |
|---|---|
| `results/` | where reports and their pinned inputs live; also where new output is written |
| `results/dandi_000409_assets.json` | the archive asset listing, created automatically on first use and reused after |

No path in this runbook has to be edited for your machine. **The data is read
in place over the network and is never downloaded in bulk** — see `DATA.md` for
what the two sources are, their licences, and how to obtain them if you would
rather work locally.

### Network, or not

Five steps replay **with no network access at all**, from pinned inputs already
in `results/`. They are marked **[offline]** and they reproduce the tracked
reports byte for byte. The remaining steps read file metadata from the DANDI
archive over HTTP range requests; they are marked **[archive]** and each one
prints the exact number of bytes and requests it used.

### Design documents these scripts refer to

Several scripts explain a choice by naming the project's **Claim Sheet** — the
contract that fixes the question, the method, the numerical budgets and the
pre-declared shapes of success, failure and an inconclusive result, all before
any measurement exists. That living document is not copied into this packet
and **is not needed to run anything here**; a stale copy would be worse than a
pointer. The current contract is in the project repository:

<https://github.com/Dandelion-Engineering/Hybrid-Ground-Truth-Realism>

`Claim Sheet.md` is the technical contract and `Accessible Claim Sheet.md` is
the same content in plain language. Everything needed to *reproduce* the
recorded results is inside this folder.

---

## The runbook

### Step 1 — Audit the donor template library **[offline]**

Runs `audit_template_library.py`. Groups the published template table by probe
type and brain area, and reports how many areas hold at least ten templates
inside the amplitude/SNR caliper — before and after dropping each area's
largest contributing source dataset. That second number is what says whether an
area's donors come from one recording or many.

```bash
python scripts/audit_template_library.py --cache results/templates_snapshot_2026-08-11.csv --out results/template_audit_2026-08-11.txt
```

Produces: `results/template_audit_2026-08-11.txt`

Drop `--cache` to fetch the live table instead; the script then reports whether
its SHA-256 still matches the pinned snapshot, and fills in the `etag` and
`last-modified` header lines that a cached read cannot carry. Those two lines
are the only difference between an offline and a live run of this step.

### Step 2 — Audit donor provenance and host-specific exclusion **[offline]**

Runs `audit_donor_provenance.py`. Parses the source-dataset column into
insertion, session, and subject identities, and reports how the donor pool for
each area changes under each granularity of host exclusion.

```bash
python scripts/audit_donor_provenance.py --cache results/templates_snapshot_2026-08-11.csv --host-subject NYU-11 --detail-area CA1 --out results/donor_provenance_2026-08-11.txt
```

Produces: `results/donor_provenance_2026-08-11.txt`

### Step 3 — Measure the pull toward the injection zone **[offline]**

Runs `audit_zone_neighbour_enrichment.py`. The control arm is drawn without
conditioning on region, but it is also covariate-matched to a region-matched
arm — and the templates that best match a CA1 template are often other CA1
templates. This measures how strong that pull is, against the expectation for a
region-blind matcher under the same no-reuse constraint.

```bash
python scripts/audit_zone_neighbour_enrichment.py --cache results/templates_snapshot_2026-08-11.csv --zone CA1 --out results/zone_neighbour_enrichment_CA1.txt
```

Produces: `results/zone_neighbour_enrichment_CA1.txt`

### Step 4 — Derive the anatomical label bridge **[offline]**

Runs `derive_ccf_label_map.py`. Host recordings annotate each electrode with a
brain-structure *long name*; the donor table carries *acronyms*. This derives
the bridge between them from the two data sources themselves — matching donors
to host electrodes at the same depth on the same insertion and taking a
supermajority vote — rather than importing an atlas ontology whose licence does
not permit commercial use. `DATA.md` explains that choice.

```bash
python scripts/derive_ccf_label_map.py --from-records results/ccf_label_map_derived_records.json --out results/ccf_label_map_derived.txt --json-out scripts/utils/ccf_label_map_derived.json
```

Produces: `results/ccf_label_map_derived.txt`, `scripts/utils/ccf_label_map_derived.json`

`--from-records` replays the saved per-asset votes with no network reads, and
refuses to run if the probe type, asset suffix, or depth tolerance differs from
the settings that produced them. To re-derive from the archive instead, replace
`--from-records …` with `--assets-cache results/dandi_000409_assets.json
--templates-cache results/templates_snapshot_2026-08-11.csv --records-out
results/ccf_label_map_derived_records.json`.

### Step 5 — Validate the hand-authored label core and depth coordinate **[archive]**

Runs `validate_ccf_label_map.py`. Checks the pre-existing hand-authored
long-name-to-acronym table against the donor library at the same depth, and at
the same time checks that donor `depth_along_probe` and NWB electrode `rel_y`
are the same coordinate. It deliberately does **not** validate the newly
derived layer against the votes that produced it; that would be circular rather
than independent confirmation.

```bash
python scripts/validate_ccf_label_map.py --assets-cache results/dandi_000409_assets.json --templates-cache results/templates_snapshot_2026-08-11.csv --out results/ccf_label_map_validation.txt
```

Produces: `results/ccf_label_map_validation.txt`

### Step 6 — Survey candidate host recordings for anatomy **[archive]**

Runs `survey_host_anatomy.py`. Reads each candidate recording's electrode table
and finds contiguous bands of contacts inside the target structure. The twelve
subjects excluded here are the ones that contributed donor templates, so that
host and donor share no animal.

```bash
python scripts/survey_host_anatomy.py --target CA1 --exclude-subjects KS042,KS043,KS044,KS046,KS051,KS052,KS055,KS084,KS086,KS091,KS094,KS096 --assets-cache results/dandi_000409_assets.json --index results/host_anatomy_index.jsonl --legacy-index-target CA1 --legacy-index-max-gap-um 40 --out results/host_anatomy_CA1.txt
```

Produces: `results/host_anatomy_CA1.txt`, and appends to
`results/host_anatomy_index.jsonl`

The index is resumable: assets already in it are not re-read. **The recorded
run indexed 46 of 429 candidates and was stopped deliberately**, because the
selection rule is first-admissible rather than best-available — once enough
admissible candidates exist, surveying the remainder changes no decision.
Re-running this step will extend the index past 46 and is expected to; the
recorded report corresponds to the first 46.

### Step 7 — Apply the duration and sampling-regularity gate **[archive]**

Runs `screen_host_timing.py`. Measures each surviving candidate's duration and
sampling regularity from its own timestamps rather than trusting a declared
rate.

```bash
python scripts/screen_host_timing.py --index results/host_anatomy_index.jsonl --assets-cache results/dandi_000409_assets.json --target CA1 --legacy-index-target CA1 --legacy-index-max-gap-um 40 --timing-index results/host_timing_index.jsonl --out results/host_timing_CA1.txt
```

Produces: `results/host_timing_CA1.txt`, and appends to
`results/host_timing_index.jsonl`

### Step 8 — Screen injection-zone placement capacity **[offline]**

Runs `screen_injection_placement.py`. Tests whether ten injected units fit
inside a candidate's target-structure band under a swept range of edge margins
and minimum separations, using electrode geometry only.

```bash
python scripts/screen_injection_placement.py --target CA1 --from-records results/injection_placement_CA1.json --skipped-note 35 --out results/injection_placement_CA1.txt
```

Produces: `results/injection_placement_CA1.txt`

`--skipped-note 35` carries forward the count of recordings that had no band of
at least twenty contacts, which the saved records do not themselves contain.
To screen from the archive instead, replace `--from-records … --skipped-note 35`
with `--assets-cache results/dandi_000409_assets.json --index
results/host_anatomy_index.jsonl --legacy-index-target CA1
--legacy-index-max-gap-um 40 --records results/injection_placement_CA1.json`.

### Step 9 — Read acquisition provenance **[archive]**

Runs `audit_subject_provenance.py`. Reads laboratory, institution, and task
protocol from each subject's own file, to establish how far apart the donor
subjects and the candidate host subjects actually are.

```bash
python scripts/audit_subject_provenance.py --donor-subjects KS042,KS043,KS044,KS046,KS051,KS052,KS055,KS084,KS086,KS091,KS094,KS096 --host-subjects CSHL045,CSHL047,CSHL049,NYU-12,NYU-37,NYU-39,NYU-45,NYU-48,NYU-65 --assets results/dandi_000409_assets.json --records results/subject_provenance.json --out results/subject_provenance.txt
```

Produces: `results/subject_provenance.txt`, `results/subject_provenance.json`

### Step 10 — Check the amplitude convention **[archive]**

Runs `audit_amplitude_conventions.py`. The donor table and the host recordings
both report a spike amplitude in microvolts, but they are not the same quantity
— one is a peak-to-peak measure on an averaged template, the other a median
over individual spikes. This measures the relationship rather than assuming it.

```bash
python scripts/audit_amplitude_conventions.py --session 07dc4b76-5b93-4a03-82a0-b3d9cc73f412 --assets-cache results/dandi_000409_assets.json --records results/amplitude_conventions.json --out results/amplitude_conventions.txt
```

Produces: `results/amplitude_conventions.txt`, `results/amplitude_conventions.json`

---

## One script here has no step yet

`scripts/measure_host_drift.py` measures a candidate host recording's band
drift and applies the pre-declared gate that decides whether that recording can
be used. It is in this packet, it runs, and its own `--help` prints the command
it expects — but **it has not been run against a recording yet**, so nothing in
`results/` came from it and there is nothing for a numbered step to reproduce.
A step here is a claim that running the command gives you the file beside it,
and that claim is not available yet. It becomes a numbered step at the first
real run, and `check_runbook_consistency.py` reports it as pending until then
rather than passing over it.

---

## Verifying the result without reading the report

The project commits to a single self-contained script, **`verify_realism.py`**,
that produces a two-panel figure and prints a plain-language verdict: panel one
shows whether the realism property actually changed while the nuisance
quantities stayed balanced, and panel two shows whether that changed the
answer — the two sorters' accuracy gap in both conditions, with the
negative-control band drawn behind it. One command, two panels, one printed
sentence.

**It is not in this packet yet**, because the results it renders do not exist
yet. It will appear here, as the last step of this runbook, when they do.

---

## Checking this runbook against the scripts

Each script repeats its own command in its module docstring, which `argparse`
prints as the first thing you see in `--help`. Two copies of one command drift,
and these two already did once: the docstrings assumed a different working
directory from the runbook, so `--help` and this file disagreed about where to
stand and what to pass. Rather than delete one copy — a reader running `--help`
should not have to open a second file to find a working invocation — the copies
are checked against each other:

```bash
python scripts/check_runbook_consistency.py
```

It reads every numbered step above and every script's `Example` block and
compares them character for character, then checks that each script has exactly
one step and names the right step number. It also requires exactly one command
on each side — one `bash` fence per step, one line inside it, one indented line
per `Example` block — because a second command anywhere is a command a reader
would run that nothing is comparing. It reads the docstring through
Python's parser, so what it compares is the string `--help` will print rather
than the source text behind it — which is not a fine distinction: a backslash
line continuation inside an ordinary docstring is an escape, so Python deletes
the newline and `--help` shows one long line with runs of spaces while the
source looks neatly wrapped. That is why the examples here are single lines, and
it is also why they copy-paste on PowerShell, where a trailing backslash is not
a continuation.

Nothing is imported, downloaded, or written. Exit status 0 means the runbook and
the scripts agree; any disagreement is printed. Run it after editing either side.

## Validation status

Being explicit about what has and has not been checked, because a runbook that
has not been run is a guess.

**Verified.** This folder was copied on its own to a location where no other
file from the project was reachable, a fresh virtual environment was built there
from `requirements.txt` alone, and steps 1, 2, 3, 4, and 8 were run in it using
only the commands printed above. All five reproduced their tracked report **byte
for byte** — with the single documented exception of step 1's `etag` and
`last-modified` lines, which only a live HTTP response can supply. The label map
JSON that step 4 writes also matched byte for byte. That test was run twice, on
two separate occasions, the second after the docstring examples above were
rewritten; both gave the same result.

**Also verified in that copy.** Every script compiles; the consistency check
above passes; and `--help` was rendered for all eleven scripts, each showing a
command relative to this folder and none showing a path from outside it. The
`--help` render is what caught the line-continuation defect described above,
which reading the source did not.

**Not re-run.** Steps 5, 6, 7, 9, and 10 read file metadata from the archive.
They have not been re-executed since this runbook was written, and step 6 in
particular is not expected to reproduce its report unchanged: its index is
resumable, so a second run continues past the 46 assets the recorded report
covers. If you run these, expect archive transfer on the order of a few hundred
megabytes across all of them, and expect the reported byte and request counts to
be your own rather than the recorded ones.

## Quality-control records

Every exclusion this work makes is recorded in the reports rather than applied
silently:

- **Twelve subjects are excluded from host candidacy** — the ones that
  contributed donor templates — so that host and donor share no animal. They are
  named in step 6's command and in `results/host_anatomy_CA1.txt`.
- **Thirty-five recordings were skipped** by the placement screen for having no
  band of at least twenty contacts in the target structure; the count is carried
  in `results/injection_placement_CA1.txt`.
- **296 electrode labels were unmapped** in the anatomy survey, and
  `results/ccf_label_map_derived.txt` records both what the derivation covers and
  the entries it deliberately withheld where the evidence was ambiguous.
- **The survey stopped at 46 of 429 candidates** on purpose; see step 6.

## Dependencies and their licences

| dependency | version | licence | commercial use |
|---|---|---|---|
| Python standard library | 3.10+ | PSF-2.0 | permitted |
| h5py | 3.16.0 | BSD-3-Clause | permitted |
| numpy | 2.5.2 | BSD-3-Clause | permitted |

No other package is imported by any script here, and no atlas ontology is
installed — see `DATA.md` for why that is a deliberate licence decision rather
than an omission. Dataset licences are documented in `DATA.md`; both permit
commercial use with attribution.

Spike-sorting dependencies are not listed because no script in this packet
imports one yet. Kilosort4 is GPLv3 and, when it is used, will be invoked as an
external tool rather than vendored into or linked against this code.
