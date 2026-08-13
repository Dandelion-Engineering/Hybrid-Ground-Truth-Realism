# DATA.md — the datasets this packet runs on, and how to obtain them

This packet reads two external sources. **Neither one needs to be downloaded in
full.** Every script here reads metadata only — asset listings over the DANDI
REST API, and small byte ranges inside remote NWB files over HTTP range
requests. No recording data is ever transferred, and nothing in this packet
writes into either source.

A frozen copy of the second source is included in `results/`, so most of the
pipeline can also be replayed with no network access at all. See *Offline
replay* at the end of this file.

---

## 1. DANDI 000409 — IBL Brain Wide Map

**What it is.** Neuropixels extracellular electrophysiology recordings from
mice, published by the International Brain Laboratory. In this project it
supplies the **host recordings**: the real recordings into which synthetic
spikes are injected, and whose per-channel anatomical annotation determines
where an injection zone can be placed.

**How to get it.** No download or registration is required to run this packet.
The scripts address the archive directly:

- Landing page: <https://dandiarchive.org/dandiset/000409>
- REST API used for asset listings: `https://api.dandiarchive.org/api/dandisets/000409/versions/draft/assets/`
- Asset blobs, read by HTTP range request: `https://dandiarchive.s3.amazonaws.com/blobs/...`

The scripts enumerate assets themselves and cache the listing as
`results/dandi_000409_assets.json`. If you would rather work from a full local
copy, the archive's own client (`pip install dandi`, then
`dandi download DANDI:000409`) will fetch it — but be aware of the size below
before starting.

**Scale, so the size is not a surprise.** 2,048 files, 139 subjects,
approximately 49.7 TB in total. Nothing in this packet downloads any meaningful
fraction of that: the heaviest step here transfers a few hundred megabytes of
file metadata across the whole survey, and each script reports the exact byte
and request count it used.

**Licence and commercial use.** `spdx:CC-BY-4.0` — Creative Commons Attribution
4.0 International, read from the dandiset's own metadata `license` field rather
than inferred from the archive being public. **Commercial use is permitted**,
with attribution required. This packet redistributes none of the underlying
recording data; it references the dataset and reads it in place.

**Citation.**

> International Brain Laboratory; Benson, Brandon; Benson, Julius; Birman, Daniel; Bonacchi, Niccolò; Carandini, Matteo; Catarino, Joana; Chapuis, Gaelle; Dayan, Peter; DeWitt, Eric; Engel, Tatiana; Fabbri, Michele; Faulkner, Mayo; Fiete, Ila; Findling, Charles; Freitas-Silva, Laura; Gerçek, Berk; Harris, Kenneth; Hofer, Sonja; Hu, Fei; Hubert, Félix; Huntenburg, Julia; Khanal, Anup; Langdon, Christopher; Lau, Petrina; Meijer, Guido; Miska, Nathaniel; Noel, Jean-Paul; Nylund, Kai; Pan-Vazquez, Alejandro; Pouget, Alexandre; Rossant, Cyrille; Roth, Noam; Schaeffer, Rylan; Schartner, Michael; Shi, Yanliang; Socha, Karolina; Steinmetz, Nicholas; Svoboda, Karel; Urai, Anne; Wells, Miles; West, Steven; Whiteway, Mathew; Winter, Olivier; Witten, Ilana; Bruijns, Sebastian A.; Paninski, Liam (2026) IBL - Brain Wide Map (Version draft) [Data set]. DANDI Archive. https://dandiarchive.org/dandiset/000409/draft

Version-specific DOIs are issued per published version and are listed on the
landing page above. The runs recorded in `results/` used the `draft` version,
which is what the scripts request by default (`--version draft`).

---

## 2. `hybrid_template_library` — the SpikeInterface donor template set

**What it is.** A published library of averaged extracellular spike waveform
templates extracted from real recordings, together with a metadata table
carrying each template's amplitude, signal-to-noise ratio, depth along the
probe, source dataset, and — the column this project needs — a `brain_area`
label. In this project it supplies the **donor templates**: the synthetic
spikes that get injected into a host recording.

**How to get it.** The metadata table is a single public CSV, fetched
automatically by any script that needs it:

- Metadata table: <https://spikeinterface-template-database.s3.amazonaws.com/templates.csv>
- Source repository: <https://github.com/SpikeInterface/hybrid_template_library>

**A frozen copy travels with this packet.** `results/templates_snapshot_2026-08-11.csv`
is the exact 2,032,640-byte object the recorded results were computed from,
SHA-256 `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`.
Every script that reads this table takes a `--cache` argument: point it at the
snapshot to reproduce the recorded numbers offline and byte-for-byte. Point it
at a new path instead and the script fetches the live object, writes it there,
and reports whether its digest still matches the pinned one.

**Licence and commercial use.** MIT, read from the repository's own licence
file. **Commercial use is permitted**, with the licence and copyright notice
required to travel with any redistributed code. The snapshot in `results/` is
data derived from that repository's published output rather than its source
code; the repository URL above is the attribution path.

**Citation.**

> SpikeInterface contributors. *hybrid_template_library*. GitHub repository,
> <https://github.com/SpikeInterface/hybrid_template_library>. MIT licence.
> Template metadata table retrieved 2026-08-11, SHA-256
> `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`.

---

## What is deliberately *not* here

**The Allen Mouse Brain Common Coordinate Framework ontology is not used and is
not a dependency of this packet.** The host recordings annotate each electrode
with a CCF *long name* while the donor table carries CCF *acronyms*, so a
bridge between the two is needed. The Allen Institute's Terms of Use permit
research and other noncommercial use, which does not fit this project's
commercial-use-permitting default, and wrapping the ontology in a permissively
licensed package does not change the terms attached to the payload.

The bridge is therefore **derived from the two first-party sources above**, by
matching donor acronyms to host long names at the same depth on the same probe
insertion and taking a supermajority vote. `scripts/derive_ccf_label_map.py`
builds it. Separately, `scripts/validate_ccf_label_map.py` gives a non-circular
check of the pre-existing hand-authored core map and of the shared depth
coordinate; it deliberately does not score derived entries against the same
votes that created them. The derived result is
`scripts/utils/ccf_label_map_derived.json`. No atlas package is installed
anywhere in this packet, and that is deliberate.

## Offline replay

Three of the steps in the README reproduce byte-for-byte with **no network
access**, using the frozen inputs already in `results/`:

| script | offline flag |
|---|---|
| `audit_template_library.py` | `--cache results/templates_snapshot_2026-08-11.csv` |
| `audit_zone_neighbour_enrichment.py` | `--cache results/templates_snapshot_2026-08-11.csv` |
| `audit_donor_provenance.py` | `--cache results/templates_snapshot_2026-08-11.csv` |

Two further steps replay from saved per-asset records rather than re-reading
the archive: `derive_ccf_label_map.py --from-records` and
`screen_injection_placement.py --from-records`. The README gives the exact
commands.
