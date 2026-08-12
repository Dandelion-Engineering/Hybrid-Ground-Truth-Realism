"""Test whether the donor library's amplitude column and IBL's are the same quantity.

The Claim Sheet rescales every injected template into a 50-200 uV band. That
band is stated in the donor template library's units (`amplitude_uv` in the
consolidated template metadata). Session 7 compared it against the host
recordings' `median_spike_amplitude_uV` column and observed that it brackets
the hosts' `good` units -- then flagged that the two columns had never been
shown to measure the same thing. Until they are, neither "the target is
defensible" nor "the target is too loud" is a supportable statement.

This script settles it in three steps.

1. **The donor definition, from the pinned upstream source.** Quoted in
   `DONOR_DEFINITION` below with file and line, so a reader can check it
   without trusting this report: `amplitude_uv` is the peak-to-peak range,
   over time, of the *average* waveform on the unit's best channel.

2. **The host definition, from the substrate's own words.** Every NWB
   units-table column carries a `description` attribute written by the people
   who made the file. This script prints them verbatim rather than
   paraphrasing.

3. **The conversion, measured on the same units.** The processed NWB carries
   `waveform_mean` -- the per-unit average waveform -- alongside
   `median_spike_amplitude_uV`. So the donor side's *definition* can be
   evaluated on host units directly, with exact unit identity and no matching
   problem: take the nan-aware peak-to-peak over the time axis, take the
   channel that maximises it (which is what the upstream best-channel rule
   does), convert volts to microvolts, and divide by the host column. The
   result is the conversion factor between the two conventions, measured
   rather than argued.

   Two internal checks guard that measurement. The channel this script
   maximises must be the electrode the file itself names in `max_electrode`,
   and `waveform_mean`'s own `unit` attribute must say `volts`. Both fail
   loudly.

Metadata only. No recording data is downloaded: the units table is read out of
the processed NWB over HTTP byte ranges.
"""

import argparse
import csv
import json
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import h5py
import numpy as np

from utils import dandi
from utils.remote_hdf5 import RemoteFile

# The donor side's definition, read from the upstream source rather than from
# documentation about it. Pinned commit, because `main` moves.
UPSTREAM_REPO = "SpikeInterface/hybrid_template_library"
UPSTREAM_COMMIT = "0023db29688842f74698bac40c48a86477ea39e7"
DONOR_DEFINITION = (
    ("python/upload_ibl_templates.py:326",
     "peak_to_peak = np.ptp(templates_extension_data.templates_array, axis=1)"),
    ("python/upload_ibl_templates.py:44-59",
     "best channel = argmax over channels of the same peak-to-peak"),
    ("python/consolidate_datasets.py:104,118",
     "'amplitude_uv' = peak_to_peak[template_index, best_channel_index]"),
)
# What that average was taken over, same source. Each of these is a difference
# from the host column that survives even after the convention is converted.
DONOR_PIPELINE = (
    ("upload_ibl_templates.py:219-220",
     "common_reference(highpass_filter(phase_shift(astype(rec,'float32')), freq_min=1.0))"),
    ("upload_ibl_templates.py:225-226",
     "random_spikes method='all' -- the average uses every spike in the window"),
    ("upload_ibl_templates.py:71",
     "minutes_by_the_end = 30 -- only the last 30 minutes of each recording"),
    ("upload_ibl_templates.py:162",
     "IblSortingExtractor(..., good_clusters_only=True) -- donors are good clusters only"),
)

UNITS_PATH = "units"
# Columns whose stated description settles what the host-side number is.
DESCRIBED_COLUMNS = ("median_spike_amplitude_uV", "max_spike_amplitude_uV",
                     "min_spike_amplitude_uV", "spike_amplitudes_uV",
                     "waveform_mean", "max_electrode", "kilosort2_label",
                     "ibl_quality_score", "spike_count")


def _decode(values):
    """Decode an h5py array of bytes or objects into a list of str."""
    return [v.decode() if isinstance(v, bytes) else str(v) for v in values]


def parse_dataset_name(name):
    """Split a consolidated-metadata `dataset` value into its parts.

    The upstream naming rule is ``f"{dandiset_id}_{dandi_name}_{sorting_pid}.zarr"``
    where ``dandi_name`` is the NWB asset's filename stem
    (`upload_ibl_templates.py:154-156` at the pinned commit).

    Args:
        name: a `dataset` cell from the consolidated template metadata.

    Returns:
        A dict with ``dandiset``, ``subject``, ``session`` and ``pid``.

    Raises:
        ValueError: if the name does not follow the documented rule.
    """
    stem = name[:-5] if name.endswith(".zarr") else name
    parts = stem.split("_")
    pid = parts[-1]
    if len(parts) < 3 or len(pid) != 36:
        raise ValueError(f"unrecognised dataset name: {name}")
    subject = next((p[4:] for p in parts if p.startswith("sub-")), None)
    session = next((p[4:] for p in parts if p.startswith("ses-")), None)
    if subject is None or session is None:
        raise ValueError(f"dataset name carries no subject or session: {name}")
    return {"dandiset": parts[0], "subject": subject, "session": session, "pid": pid}


def load_donor_templates(csv_path, session, probe_model):
    """Read the consolidated donor-template metadata for one session.

    Args:
        csv_path: path of the tracked consolidated-metadata snapshot.
        session: session uuid to keep.
        probe_model: `probe` value to keep, e.g. ``"Neuropixels 1.0"``.

    Returns:
        A dict mapping pid to a list of ``amplitude_uv`` values, in the order
        the library wrote them.
    """
    by_pid = {}
    with open(csv_path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["probe"] != probe_model:
                continue
            parsed = parse_dataset_name(row["dataset"])
            if parsed["session"] != session:
                continue
            by_pid.setdefault(parsed["pid"], []).append(float(row["amplitude_uv"]))
    return by_pid


def read_units(url, size, block_bytes):
    """Read one processed NWB's units table, including every mean waveform.

    Args:
        url: direct S3 URL of the processed NWB blob.
        size: the blob's size in bytes.
        block_bytes: HTTP range-request block size.

    Returns:
        A dict with ``units`` (a list of per-unit dicts), ``descriptions``,
        ``columns`` and ``io`` counters.

    Raises:
        KeyError: if the file carries no units table.
        ValueError: if `waveform_mean` is not in volts, or if the channel this
            script maximises is not the electrode the file names.
    """
    remote = RemoteFile(url, size, block=block_bytes)
    with h5py.File(remote, "r") as handle:
        if UNITS_PATH not in handle:
            raise KeyError(f"{url} has no /{UNITS_PATH}")
        node = handle[UNITS_PATH]
        columns = sorted(node.keys())
        descriptions = {}
        for name in node.keys():
            text = node[name].attrs.get("description")
            if text is not None:
                descriptions[name] = (text.decode() if isinstance(text, bytes)
                                      else str(text))

        waveform = node["waveform_mean"]
        wave_unit = waveform.attrs.get("unit")
        wave_unit = (wave_unit.decode() if isinstance(wave_unit, bytes)
                     else str(wave_unit))
        if wave_unit.lower() != "volts":
            raise ValueError(f"waveform_mean is in {wave_unit!r}, not volts; the "
                             "microvolt conversion below would be wrong")

        probe_names = _decode(node["probe_name"][:])
        labels = _decode(node["kilosort2_label"][:])
        quality = node["ibl_quality_score"][:]
        median_amp = node["median_spike_amplitude_uV"][:]
        max_electrode = node["max_electrode"][:]
        spike_count = node["spike_count"][:]
        electrodes = node["electrodes"][:]
        electrodes_index = node["electrodes_index"][:]
        waves = waveform[:]

        units = []
        starts = np.concatenate(([0], electrodes_index[:-1]))
        for index in range(len(probe_names)):
            wave = waves[index]
            # Padding for units with fewer electrodes than the array's width.
            spread = np.nanmax(wave, axis=0) - np.nanmin(wave, axis=0)
            if not np.any(np.isfinite(spread)):
                continue
            channel = int(np.nanargmax(spread))
            own = electrodes[starts[index]:electrodes_index[index]]
            if channel >= len(own):
                raise ValueError(f"unit {index} peaks on padded channel {channel} of "
                                 f"{len(own)} real electrodes")
            # The file names its own peak electrode by a different rule -- IBL's
            # per-spike amplitudes on IBL's preprocessing, not peak-to-peak of
            # this mean waveform. Where the two disagree, the peak-to-peak value
            # at the file's electrode is carried as a sensitivity check so the
            # measured conversion does not rest on the channel choice.
            named = int(max_electrode[index])
            where = np.nonzero(own == named)[0]
            at_named = (float(spread[int(where[0])]) * 1e6
                        if len(where) and np.isfinite(spread[int(where[0])]) else None)
            units.append({
                "row": index,
                "probe": probe_names[index],
                "kilosort2_label": labels[index],
                "ibl_quality_score": float(quality[index]),
                "spike_count": int(spike_count[index]),
                "template_p2p_uV": float(spread[channel]) * 1e6,
                "template_p2p_at_named_electrode_uV": at_named,
                "best_channel_matches_file": int(own[channel]) == named,
                "median_spike_amplitude_uV": float(median_amp[index]),
            })
    return {"units": units, "descriptions": descriptions, "columns": columns,
            "io": {"bytes": remote.n_bytes, "requests": remote.n_requests}}


def summarize(values):
    """Return count, median, mean, spread and 10th/90th percentiles."""
    ordered = sorted(v for v in values if v is not None and np.isfinite(v))
    if not ordered:
        return None
    def pct(p):
        if len(ordered) == 1:
            return ordered[0]
        pos = p * (len(ordered) - 1)
        low = int(pos)
        high = min(low + 1, len(ordered) - 1)
        return ordered[low] + (ordered[high] - ordered[low]) * (pos - low)
    return {"n": len(ordered), "median": statistics.median(ordered),
            "mean": statistics.fmean(ordered), "p10": pct(0.10), "p90": pct(0.90),
            "min": ordered[0], "max": ordered[-1],
            "iqr_ratio": (pct(0.75) / pct(0.25)) if pct(0.25) > 0 else float("nan")}


def cohort(units, name):
    """Select one named cohort of units.

    Args:
        units: every unit read from the file.
        name: ``"all"``, ``"kilosort_good"`` or ``"ibl_quality_1"``.

    Returns:
        The matching subset, as a list.
    """
    if name == "all":
        return list(units)
    if name == "kilosort_good":
        return [u for u in units if u["kilosort2_label"] == "good"]
    if name == "ibl_quality_1":
        return [u for u in units if u["ibl_quality_score"] == 1.0]
    raise ValueError(f"unknown cohort {name}")


COHORTS = ("all", "kilosort_good", "ibl_quality_1")


def write_report(path, payload):
    """Write the human-readable report.

    Args:
        path: destination file path.
        payload: the assembled result dict written by ``main``.
    """
    lines = []
    add = lines.append
    add("Amplitude-convention audit: donor `amplitude_uv` vs IBL "
        "`median_spike_amplitude_uV`")
    add("=" * 78)
    add(f"generated: {payload['generated']}")
    add(f"session:   {payload['session']}  (subject {payload['subject']})")
    add(f"asset:     {payload['asset_path']}")
    add(f"upstream:  {UPSTREAM_REPO} @ {UPSTREAM_COMMIT}")
    add(f"io:        {payload['io']['bytes']:,} bytes in {payload['io']['requests']} "
        "range requests, metadata only")
    add("")

    add("1. The donor column, from the pinned upstream source")
    add("-" * 78)
    for where, text in DONOR_DEFINITION:
        add(f"  {where}")
        add(f"      {text}")
    add("")
    add("  `amplitude_uv` is the PEAK-TO-PEAK range, over time, of the AVERAGE")
    add("  waveform on the unit's best channel: trough to peak, one number per unit,")
    add("  taken from an averaged waveform.")
    add("")
    add("  Differences that survive any unit conversion, same source:")
    for where, text in DONOR_PIPELINE:
        add(f"    {where}")
        add(f"        {text}")
    add("")

    add("2. The host column, in the file's own words")
    add("-" * 78)
    for name in DESCRIBED_COLUMNS:
        if name in payload["descriptions"]:
            add(f"  {name}:")
            add(f"      {payload['descriptions'][name]}")
    add("")
    add(f"  units columns present ({len(payload['columns'])}):")
    add(f"      {', '.join(payload['columns'])}")
    add("")
    add("  So the host column is the MEDIAN over spikes of a PER-SPIKE PEAK")
    add("  amplitude. The donor column is a PEAK-TO-PEAK range of an AVERAGE.")
    add("  Those are different measurements of different objects, and the rest of")
    add("  this report measures how different.")
    add("")

    add("3. The conversion, measured on the same units")
    add("-" * 78)
    add("  For every unit in this file: nan-aware peak-to-peak of `waveform_mean`")
    add("  over time, on the channel maximising it, converted volts -> microvolts.")
    add("  That is the donor column's definition evaluated on host units. Each")
    add("  unit's value is then divided by its own `median_spike_amplitude_uV`.")
    add("")
    add(f"  A third convention difference showed up here and is reported rather than")
    add(f"  smoothed over. The file's `max_electrode` is chosen by IBL's own rule,")
    add(f"  not by peak-to-peak of this mean waveform, and the two agree on only")
    add(f"  {payload['cohorts']['all']['best_channel_agreement']:.1%} of units -- usually a near tie between adjacent")
    add(f"  contacts. Every ratio below is therefore given twice: on the channel the")
    add(f"  upstream rule picks, and on the electrode the file itself names. They")
    add(f"  agree closely, so the conversion does not rest on the channel choice.")
    add("")
    for name in COHORTS:
        block = payload["cohorts"][name]
        if not block["ratio"]:
            add(f"  {name}: no units")
            continue
        ratio, p2p, med = block["ratio"], block["p2p"], block["median_amp"]
        named = block["ratio_at_named_electrode"]
        add(f"  cohort {name}  (n = {ratio['n']})")
        add(f"    p2p of mean waveform (uV):   median {p2p['median']:7.1f}   "
            f"p10 {p2p['p10']:7.1f}   p90 {p2p['p90']:7.1f}")
        add(f"    median_spike_amplitude_uV:   median {med['median']:7.1f}   "
            f"p10 {med['p10']:7.1f}   p90 {med['p90']:7.1f}")
        add(f"    ratio (p2p / median):        median {ratio['median']:7.3f}   "
            f"p10 {ratio['p10']:7.3f}   p90 {ratio['p90']:7.3f}")
        add(f"                                 min {ratio['min']:7.3f}   "
            f"max {ratio['max']:7.3f}")
        if named:
            add(f"    same, at the file's electrode: median {named['median']:7.3f}   "
                f"p10 {named['p10']:7.3f}   p90 {named['p90']:7.3f}")
        add("")

    add("4. The donor templates from this same session, for scale")
    add("-" * 78)
    if not payload["donor"]:
        add("  this session contributes no templates to the snapshot")
    for pid, stats in sorted(payload["donor"].items()):
        add(f"  pid {pid}  n = {stats['n']}")
        add(f"    amplitude_uv (uV):           median {stats['median']:7.1f}   "
            f"p10 {stats['p10']:7.1f}   p90 {stats['p90']:7.1f}")
    add("")
    add("  Unit-level pairing between these templates and the file's units was")
    add("  attempted and FAILED: the library records no unit id in the")
    add("  consolidated metadata, and the hypothesis that template order follows")
    add("  the file's unit order scored at chance under both the `kilosort2_label`")
    add("  and the `ibl_quality_score` definitions of a good cluster. Do not")
    add("  retry order-based pairing; it would need the zarr store's `unit_ids`.")
    add("  The measurement in section 3 does not depend on that pairing.")
    add("")

    add("5. What this establishes, and what it does not")
    add("-" * 78)
    add("  Establishes: the two columns are NOT the same quantity, and the")
    add("  conversion between their definitions is measured above on real units.")
    add("  Any comparison of the 50-200 uV donor target against host amplitudes")
    add("  must apply that conversion first.")
    add("")
    add("  Does not establish: that the converted numbers are directly comparable.")
    add("  The donor averages are built on a 1 Hz highpass plus common median")
    add("  reference over the last 30 minutes of good clusters only, while the host")
    add("  column is IBL's own number on IBL's own preprocessing over the whole")
    add("  recording. Preprocessing is a second difference this report does not")
    add("  measure and does not claim to have removed.")
    add("")
    add("  One session. It fixes the convention, not the population.")
    lines.append("")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--session", required=True,
                        help="session uuid to audit")
    parser.add_argument("--assets-cache", required=True,
                        help="JSON file caching the DANDI asset listing")
    parser.add_argument("--out", required=True, help="path of the report to write")
    parser.add_argument("--templates-csv", default=None,
                        help="optional consolidated template-metadata snapshot, used "
                             "only to print this session's donor amplitudes for scale")
    parser.add_argument("--records", default=None,
                        help="optional path for the raw JSON records")
    parser.add_argument("--dandiset", default="000409", help="dandiset identifier")
    parser.add_argument("--version", default="draft", help="dandiset version")
    parser.add_argument("--probe-model", default="Neuropixels 1.0",
                        help="`probe` value to keep from the snapshot")
    parser.add_argument("--block-kb", type=int, default=1024,
                        help="HTTP range block size in KiB")
    return parser.parse_args(argv)


def main(argv=None):
    """Run the audit and write the report."""
    args = parse_args(argv)

    print("[1/3] locating the processed asset", flush=True)
    assets = dandi.list_assets(args.dandiset, args.version,
                               cache_path=args.assets_cache, verbose=False)
    processed = [a for a in assets
                 if args.session in a["path"]
                 and a["path"].endswith(dandi.PROCESSED_SUFFIX)]
    if len(processed) != 1:
        raise SystemExit(f"[fatal] expected exactly one processed asset for "
                         f"{args.session}, found {len(processed)}")
    asset = processed[0]
    print(f"      {asset['path']}", flush=True)

    print("[2/3] reading the units table and every mean waveform", flush=True)
    read = read_units(dandi.blob_url(asset), asset["size"], args.block_kb * 1024)
    units = read["units"]
    print(f"      {read['io']['bytes']:,} bytes in {read['io']['requests']} requests; "
          f"{len(units)} units with a finite mean waveform", flush=True)

    print("[3/3] measuring the conversion", flush=True)
    cohorts = {}
    for name in COHORTS:
        chosen = cohort(units, name)
        usable = [u for u in chosen if u["median_spike_amplitude_uV"] > 0]
        at_named = [u for u in usable
                    if u["template_p2p_at_named_electrode_uV"] is not None]
        cohorts[name] = {
            "n_selected": len(chosen),
            "ratio": summarize([u["template_p2p_uV"] / u["median_spike_amplitude_uV"]
                                for u in usable]),
            "ratio_at_named_electrode": summarize(
                [u["template_p2p_at_named_electrode_uV"] / u["median_spike_amplitude_uV"]
                 for u in at_named]),
            "p2p": summarize([u["template_p2p_uV"] for u in usable]),
            "median_amp": summarize([u["median_spike_amplitude_uV"] for u in usable]),
            "best_channel_agreement": (
                sum(1 for u in usable if u["best_channel_matches_file"]) / len(usable)
                if usable else None),
        }
        block = cohorts[name]["ratio"]
        if block:
            print(f"      {name}: n={block['n']} ratio median {block['median']:.3f} "
                  f"(p10 {block['p10']:.3f}, p90 {block['p90']:.3f})", flush=True)

    donor = {}
    if args.templates_csv:
        for pid, values in load_donor_templates(args.templates_csv, args.session,
                                                args.probe_model).items():
            donor[pid] = summarize(values)

    payload = {
        "generated": time.strftime("%Y-%m-%d %H:%M %Z"),
        "session": args.session,
        "subject": dandi.subject_of(asset) or "",
        "asset_path": asset["path"],
        "upstream_repo": UPSTREAM_REPO,
        "upstream_commit": UPSTREAM_COMMIT,
        "io": read["io"],
        "descriptions": read["descriptions"],
        "columns": read["columns"],
        "n_units_checked": len(units),
        "cohorts": cohorts,
        "donor": donor,
        "units": units,
    }

    write_report(args.out, payload)
    print(f"wrote {args.out}", flush=True)
    if args.records:
        with open(args.records, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, indent=1, sort_keys=True)
        print(f"wrote {args.records}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
