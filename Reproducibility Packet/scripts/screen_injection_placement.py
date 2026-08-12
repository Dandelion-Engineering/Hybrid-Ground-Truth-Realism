"""Test whether ten injected units fit a candidate host's injection zone.

The Claim Sheet's Slot 7 makes this a gate: "If ten feasible placements cannot
be supported without overcrowding or label ambiguity, that host fails the Tier
A gate rather than having a convenient whole-recording label invented for it."
``survey_host_anatomy.py`` finds each candidate's largest contiguous band of the
target structure and ranks hosts by its size. A band being large is not the same
as ten units fitting inside it, and this script is the difference.

It measures four things per candidate band, all from file metadata:

1. **Label purity.** How many contacts inside the band's depth range actually
   carry the target label, and what the others are. A band admitted with a
   40 um gap tolerance can contain contacts belonging to something else.
2. **Placement capacity.** An injected template has spatial extent, so its peak
   must sit far enough inside the band for its footprint to land in labelled
   target tissue. Capacity is reported as a sweep over edge margin and minimum
   peak separation rather than at one invented number, because neither value is
   measured yet. Measuring the donor templates' real footprint needs the
   template arrays, which this screen does not download, and calibrates the
   edge margin. Minimum peak separation still needs its own basis from native
   peak-depth spacing and the generator's relocation constraints.
3. **Native unit density.** The processed NWB carries IBL's own spike sorting.
   Counting its units inside the same band says what ten injected units do to
   the local density -- which is what "overcrowding" has to be judged against,
   since the Claim Sheet's reason for capping injected units at ten is that
   more of them change the recording's own collision statistics.
4. **Native amplitude distribution.** The same units give the host zone's real
   spike amplitudes, which is the empirical context for the Claim Sheet's
   50-200 uV post-rescaling injection target.

**What this script does not do.** It is not a drift measurement and not a noise
measurement. The processed file carries a ``cumulative_drift_um_per_hour``
column whose values run to millions of micrometres per hour; whatever it
accumulates, it is not net probe drift at that magnitude, and this screen
reports it as uninterpreted rather than using it as a gate.

Example
-------
    ./venv/Scripts/python.exe "Reproducibility Packet/scripts/screen_injection_placement.py" \
        --target CA1 --assets-cache "Reproducibility Packet/results/dandi_000409_assets.json" \
        --index "Reproducibility Packet/results/host_anatomy_index.jsonl" \
        --legacy-index-target CA1 --legacy-index-max-gap-um 40 \
        --out "Reproducibility Packet/results/injection_placement_CA1.txt"
"""

import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import h5py  # noqa: E402

from utils import anatomy_index, dandi  # noqa: E402
from utils.host_anatomy import contiguous_band, read_electrode_table  # noqa: E402
from utils.remote_hdf5 import RemoteFile  # noqa: E402

UNITS_PATH = "units"
ELECTRODES_PATH = "general/extracellular_ephys/electrodes"

# Columns read from the processed file's units table. Every one is a single
# value per unit. The ragged per-spike columns (spike_times, spike_amplitudes_uV,
# spike_distances_from_probe_tip_um) are never touched: they are the size of the
# sorting itself and this screen is metadata-only by design.
UNIT_SCALARS = ("firing_rate", "spike_count", "median_spike_amplitude_uV",
                "cumulative_drift_um_per_hour")


def _decode(values):
    """Decode an h5py string column into a list of str."""
    return [v.decode() if isinstance(v, bytes) else str(v) for v in values]


def band_profile(electrodes, band, target):
    """Describe what actually sits inside and around a band's depth range.

    Args:
        electrodes: per-electrode dicts for one probe.
        band: a band dict from ``utils.host_anatomy.contiguous_band``.
        target: the target structure acronym.

    Returns:
        A dict with the contact counts inside the band's depth range, the
        non-target labels found there, and the distance from each band edge to
        the nearest differently-labelled contact outside it.
    """
    lo, hi = band["depth_lo_um"], band["depth_hi_um"]
    inside = [e for e in electrodes
              if e["depth_um"] is not None and lo <= e["depth_um"] <= hi]
    on_target = [e for e in inside if e["acronym"] == target]
    interlopers = {}
    for electrode in inside:
        if electrode["acronym"] == target:
            continue
        key = electrode["acronym"] or f"<unmapped:{electrode['location']}>"
        interlopers[key] = interlopers.get(key, 0) + 1

    below = [e["depth_um"] for e in electrodes
             if e["depth_um"] is not None and e["depth_um"] < lo and e["acronym"] != target]
    above = [e["depth_um"] for e in electrodes
             if e["depth_um"] is not None and e["depth_um"] > hi and e["acronym"] != target]
    return {
        "n_contacts_in_range": len(inside),
        "n_on_target": len(on_target),
        "purity": len(on_target) / len(inside) if inside else 0.0,
        "interlopers": dict(sorted(interlopers.items(), key=lambda kv: -kv[1])),
        "gap_to_other_below_um": (lo - max(below)) if below else None,
        "gap_to_other_above_um": (min(above) - hi) if above else None,
    }


def placement_capacity(span_um, n_units, edge_margin_um, min_separation_um):
    """Count how many injection sites a band of this span can hold.

    A unit's peak must sit at least ``edge_margin_um`` inside each band edge so
    that the bulk of its multichannel footprint lands in labelled target tissue,
    and peaks must be at least ``min_separation_um`` apart so that ten units are
    ten placements rather than one crowded one.

    Args:
        span_um: the band's depth span in micrometres.
        n_units: how many units the design injects.
        edge_margin_um: required clearance from each band edge.
        min_separation_um: required separation between successive peaks.

    Returns:
        A dict with the usable span, the maximum number of sites, and whether
        that meets ``n_units``.
    """
    usable = span_um - 2.0 * edge_margin_um
    if usable < 0:
        return {"usable_span_um": usable, "max_sites": 0, "fits": False}
    max_sites = int(usable // min_separation_um) + 1
    return {"usable_span_um": usable, "max_sites": max_sites, "fits": max_sites >= n_units}


def read_native_units(url, size, block_bytes):
    """Read the processed file's sorted units and its electrodes table.

    Reading both from the same file guarantees that ``max_electrode`` indexes
    the table the depths are taken from. The raw file's table is compared
    against this one by the caller rather than assumed identical.

    Args:
        url: direct S3 URL of the processed NWB blob.
        size: the blob's size in bytes.
        block_bytes: HTTP range-request block size.

    Returns:
        A dict with ``units`` (a list of per-unit dicts carrying probe, depth,
        quality label and the scalar metrics), ``electrodes`` (per-probe lists
        matching ``utils.host_anatomy.read_electrode_table``'s shape), and
        ``io``.

    Raises:
        KeyError: if the file carries no units table or no electrodes table.
        ValueError: if a unit's peak-electrode index is invalid or belongs to a
            different probe than the unit names.
    """
    from utils import ccf_labels
    remote = RemoteFile(url, size, block=block_bytes)
    with h5py.File(remote, "r") as handle:
        if UNITS_PATH not in handle:
            raise KeyError(f"{url} has no /{UNITS_PATH}")
        if ELECTRODES_PATH not in handle:
            raise KeyError(f"{url} has no {ELECTRODES_PATH}")
        table = handle[ELECTRODES_PATH]
        rel_y = table["rel_y"][:].tolist()
        groups = _decode(table["group_name"][:])
        locations = _decode(table["location"][:])
        electrodes = {}
        for index, probe in enumerate(groups):
            electrodes.setdefault(probe, []).append({
                "id": index,
                "location": locations[index],
                "acronym": ccf_labels.to_acronym(locations[index]),
                "depth_um": rel_y[index],
                "lateral_um": None,
            })

        node = handle[UNITS_PATH]
        probe_names = _decode(node["probe_name"][:])
        max_electrode = node["max_electrode"][:].tolist()
        labels = (_decode(node["kilosort2_label"][:])
                  if "kilosort2_label" in node else [""] * len(probe_names))
        tip_distance = (node["distance_from_probe_tip_um"][:].tolist()
                        if "distance_from_probe_tip_um" in node else [None] * len(probe_names))
        scalars = {name: node[name][:].tolist() for name in UNIT_SCALARS if name in node}
        units = []
        for index, probe in enumerate(probe_names):
            electrode = max_electrode[index]
            if not 0 <= electrode < len(groups):
                raise ValueError(
                    f"{url} unit {index} has out-of-range max_electrode {electrode} "
                    f"for an electrode table with {len(groups)} rows")
            if groups[electrode] != probe:
                raise ValueError(
                    f"{url} unit {index} says probe {probe!r}, but max_electrode "
                    f"{electrode} belongs to {groups[electrode]!r}")
            unit = {
                "probe": probe,
                "electrode_probe": groups[electrode],
                "depth_um": rel_y[electrode],
                "tip_distance_um": tip_distance[index],
                "label": labels[index],
            }
            for name, column in scalars.items():
                unit[name] = column[index]
            units.append(unit)
    return {"units": units, "electrodes": electrodes,
            "io": {"requests": remote.n_requests, "bytes": remote.n_bytes}}


def summarize_native(units, probe, lo, hi):
    """Summarise the host's own sorted units inside one depth band.

    Args:
        units: per-unit dicts from ``read_native_units``.
        probe: probe name to restrict to.
        lo: band's lower depth bound in micrometres.
        hi: band's upper depth bound in micrometres.

    Returns:
        A dict with unit counts, per-100-um densities, and the amplitude and
        firing-rate distributions of the units inside the band.
    """
    inside = [u for u in units
              if u["probe"] == probe and u["depth_um"] is not None and lo <= u["depth_um"] <= hi]
    good = [u for u in inside if u["label"] == "good"]
    span = max(hi - lo, 1.0)

    def _dist(values):
        clean = sorted(v for v in values if v is not None and v == v)
        if not clean:
            return None
        return {
            "n": len(clean),
            "p10": clean[int(0.10 * (len(clean) - 1))],
            "median": statistics.median(clean),
            "p90": clean[int(0.90 * (len(clean) - 1))],
        }

    return {
        "n_units": len(inside),
        "n_good": len(good),
        "units_per_100um": 100.0 * len(inside) / span,
        "good_per_100um": 100.0 * len(good) / span,
        "amplitude_uv": _dist(u.get("median_spike_amplitude_uV") for u in inside),
        "amplitude_uv_good": _dist(u.get("median_spike_amplitude_uV") for u in good),
        "firing_rate_hz": _dist(u.get("firing_rate") for u in inside),
        "n_drift_finite": sum(1 for u in inside
                              if u.get("cumulative_drift_um_per_hour") is not None
                              and u["cumulative_drift_um_per_hour"] == u["cumulative_drift_um_per_hour"]),
    }


def load_index(path):
    """Load the anatomy index written by ``survey_host_anatomy.py``.

    Args:
        path: JSONL index path.

    Returns:
        A dict from asset_id to record.

    Raises:
        SystemExit: if the index is missing, since this screen has no way to
            choose candidates without it.
    """
    if not path or not os.path.exists(path):
        raise SystemExit(f"[fatal] anatomy index not found: {path}")
    records = {}
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                record = json.loads(line)
                records[record["asset_id"]] = record
    return records


def screen_asset(record, raw_asset, processed_asset, target, max_gap_um, block_bytes, args):
    """Screen one indexed recording's target bands for placement feasibility.

    Args:
        record: an anatomy-index record.
        raw_asset: the raw-file asset the record was built from.
        processed_asset: the matching processed-file asset, or None.
        target: target structure acronym.
        max_gap_um: band contiguity tolerance, matching the anatomy survey.
        block_bytes: HTTP range-request block size.
        args: parsed command-line arguments.

    Returns:
        A JSON-serialisable result record, or None when the recording holds no
        band of at least ``--min-band-channels`` contacts.
    """
    bands = [p for p in record["probes"]
             if p.get("target_band")
             and p["target_band"]["n_channels"] >= args.min_band_channels]
    if not bands:
        return None

    raw = read_electrode_table(dandi.blob_url(raw_asset), raw_asset["size"], block_bytes)

    processed = processed_asset
    native = None
    if processed is not None:
        native = read_native_units(dandi.blob_url(processed), processed["size"], block_bytes)

    result = {
        "asset_id": record["asset_id"],
        "path": record["path"],
        "subject": record["subject"],
        "session": record["session"],
        "processed_path": processed["path"] if processed else None,
        "probes": [],
        "io": {"requests": raw["io"]["requests"], "bytes": raw["io"]["bytes"]},
    }
    if native:
        result["io"]["requests"] += native["io"]["requests"]
        result["io"]["bytes"] += native["io"]["bytes"]

    for probe_entry in bands:
        probe = probe_entry["probe"]
        electrodes = raw["probes"].get(probe, [])
        band = contiguous_band(electrodes, target, max_gap_um)
        indexed = probe_entry["target_band"]
        agrees = bool(band) and all(
            abs(band[key] - indexed[key]) < 1e-9
            for key in ("depth_lo_um", "depth_hi_um", "n_channels")
        )
        entry = {
            "probe": probe,
            "band": band,
            "band_matches_index": agrees,
            "profile": band_profile(electrodes, band, target) if band else None,
            "capacity": {},
            "native": None,
            "electrode_table_agrees": None,
        }
        if band:
            for margin in args.edge_margins:
                for separation in args.separations:
                    key = f"margin{int(margin)}_sep{int(separation)}"
                    entry["capacity"][key] = placement_capacity(
                        band["span_um"], args.n_units, margin, separation)
        if native and band:
            entry["native"] = summarize_native(native["units"], probe,
                                               band["depth_lo_um"], band["depth_hi_um"])
            processed_electrodes = native["electrodes"].get(probe, [])
            entry["electrode_table_agrees"] = (
                [(e["depth_um"], e["acronym"]) for e in processed_electrodes]
                == [(e["depth_um"], e["acronym"]) for e in electrodes])
        entry["passes"] = bool(
            band
            and entry["profile"]["purity"] >= args.min_purity
            and placement_capacity(band["span_um"], args.n_units,
                                   args.edge_margin_um, args.min_separation_um)["fits"])
        result["probes"].append(entry)
    return result


def write_report(path, results, args, skipped):
    """Write the human-readable placement report.

    Args:
        path: output file path.
        results: per-asset result records.
        args: parsed command-line arguments.
        skipped: assets skipped for having no qualifying band.
    """
    lines = []
    total_bytes = sum(r["io"]["bytes"] for r in results)
    total_requests = sum(r["io"]["requests"] for r in results)
    n_bands = sum(len(r["probes"]) for r in results)
    passing = [(r, p) for r in results for p in r["probes"] if p["passes"]]

    lines.append("# Injection-zone placement screen")
    lines.append("")
    lines.append(f"target structure      {args.target}")
    lines.append(f"band contiguity gap   {args.max_gap_um} um")
    lines.append(f"units to place        {args.n_units}")
    lines.append(f"declared edge margin  {args.edge_margin_um} um")
    lines.append(f"declared separation   {args.min_separation_um} um")
    lines.append(f"declared min purity   {args.min_purity}")
    lines.append(f"bands screened        {n_bands} across {len(results)} recording(s)")
    lines.append(f"recordings skipped    {skipped} (no band of >= {args.min_band_channels} contacts)")
    lines.append(f"metadata read         {total_bytes} bytes in {total_requests} requests")
    lines.append("")
    lines.append("Every number here comes from file metadata. No recording data was read,")
    lines.append("no sorter was run, and nothing here measures drift, noise, or effective SNR.")
    lines.append("")

    lines.append("## Verdict at the declared parameters")
    lines.append("")
    lines.append(f"{'subject':<10} {'session':<8} {'probe':<9} {'span':>6} {'chan':>5} {'purity':>7} "
                 f"{'sites':>6} {'native':>7} {'good':>5} {'vs all':>8} {'vs good':>8}  verdict")
    lines.append("-" * 113)
    for result in results:
        for probe in result["probes"]:
            band = probe["band"]
            if not band:
                continue
            key = f"margin{int(args.edge_margin_um)}_sep{int(args.min_separation_um)}"
            capacity = probe["capacity"].get(key, {})
            native = probe["native"] or {}
            vs_all = (f"+{100.0 * args.n_units / native['n_units']:.1f}%"
                      if native.get("n_units") else "-")
            vs_good = (f"+{100.0 * args.n_units / native['n_good']:.0f}%"
                       if native.get("n_good") else "-")
            lines.append("{:<10} {:<8} {:<9} {:>6.0f} {:>5d} {:>6.1f}% {:>6} {:>7} {:>5} {:>8} {:>8}  {}".format(
                result["subject"], result["session"][:8], probe["probe"],
                band["span_um"], band["n_channels"],
                100.0 * probe["profile"]["purity"],
                capacity.get("max_sites", "-"),
                native.get("n_units", "-"), native.get("n_good", "-"),
                vs_all, vs_good,
                "PASS" if probe["passes"] else "FAIL"))
    lines.append("")
    lines.append(f"{len(passing)} of {n_bands} band(s) pass the placement and purity gate.")
    lines.append("")
    lines.append("'vs all' and 'vs good' are what injecting this many units does to the")
    lines.append("band's unit count, against every cluster IBL's sorting reports there and")
    lines.append("against only the ones it labelled 'good'. Injected units are well-isolated")
    lines.append("single units by construction, so 'vs good' is the comparison that matches")
    lines.append("what is being added; 'vs all' is the one that matches what the sorter sees.")
    lines.append("Neither is gated here -- the Claim Sheet does not fix an overcrowding")
    lines.append("threshold, and inventing one in a screening script is not this script's")
    lines.append("call to make.")
    lines.append("")

    lines.append("## Capacity sweep — maximum placeable sites")
    lines.append("")
    lines.append("The edge margin and the minimum separation are declared parameters, not")
    lines.append("measurements. Donor-template footprint can calibrate the edge margin; it")
    lines.append("does not by itself justify the minimum peak separation, which needs a")
    lines.append("separate basis from native peak depths and generator relocation constraints.")
    lines.append("The sweep is here so the verdict can be re-read without another network run.")
    lines.append("")
    header = f"{'subject':<10} {'session':<8} {'probe':<9} {'span':>6}"
    for margin in args.edge_margins:
        for separation in args.separations:
            header += f"  m{int(margin)}/s{int(separation)}"
    lines.append(header)
    lines.append("-" * len(header))
    for result in results:
        for probe in result["probes"]:
            if not probe["band"]:
                continue
            row = "{:<10} {:<8} {:<9} {:>6.0f}".format(
                result["subject"], result["session"][:8], probe["probe"],
                probe["band"]["span_um"])
            for margin in args.edge_margins:
                for separation in args.separations:
                    capacity = probe["capacity"][f"margin{int(margin)}_sep{int(separation)}"]
                    width = len(f"  m{int(margin)}/s{int(separation)}")
                    row += f"{capacity['max_sites']:>{width}d}"
            lines.append(row)
    lines.append("")

    lines.append("## What sits inside and beside each band")
    lines.append("")
    for result in results:
        for probe in result["probes"]:
            band, profile = probe["band"], probe["profile"]
            if not band:
                continue
            lines.append(f"### {result['subject']} {probe['probe']} "
                         f"(session {result['session'][:8]}; "
                         f"{band['depth_lo_um']:.0f}-{band['depth_hi_um']:.0f} um)")
            lines.append("")
            lines.append(f"  contacts in range        {profile['n_contacts_in_range']} "
                         f"({profile['n_on_target']} labelled {args.target})")
            lines.append(f"  non-target inside band   "
                         f"{profile['interlopers'] if profile['interlopers'] else 'none'}")
            lines.append(f"  nearest other structure  "
                         f"{profile['gap_to_other_below_um']} um below, "
                         f"{profile['gap_to_other_above_um']} um above")
            lines.append(f"  band matches the index   {probe['band_matches_index']}")
            lines.append(f"  raw/processed tables agree {probe['electrode_table_agrees']}")
            native = probe["native"]
            if native:
                lines.append(f"  host's own sorted units  {native['n_units']} "
                             f"({native['n_good']} 'good'), "
                             f"{native['units_per_100um']:.1f} per 100 um "
                             f"({native['good_per_100um']:.1f} good per 100 um)")
                if native["amplitude_uv"]:
                    amp = native["amplitude_uv"]
                    lines.append(f"  their median amplitude   {amp['median']:.1f} uV "
                                 f"(p10 {amp['p10']:.1f}, p90 {amp['p90']:.1f})")
                if native["amplitude_uv_good"]:
                    amp = native["amplitude_uv_good"]
                    lines.append(f"  'good' units only        {amp['median']:.1f} uV "
                                 f"(p10 {amp['p10']:.1f}, p90 {amp['p90']:.1f})")
                if native["firing_rate_hz"]:
                    rate = native["firing_rate_hz"]
                    lines.append(f"  their firing rates       {rate['median']:.2f} Hz "
                                 f"(p10 {rate['p10']:.2f}, p90 {rate['p90']:.2f})")
            lines.append("")

    lines.append("## Boundaries on these numbers")
    lines.append("")
    lines.append("- The native unit counts are IBL's own Kilosort 2.5 output as published in")
    lines.append("  the processed NWB, not this project's sorting. They are the right density")
    lines.append("  available first-party density reference for this recording; they are not")
    lines.append("  ground truth and do not become a host-admission threshold by themselves.")
    lines.append("- The amplitude column is the units table's median spike amplitude in")
    lines.append("  microvolts, computed by IBL on their own preprocessed data. Whether its")
    lines.append("  convention matches the donor library's amplitude_uv column has not been")
    lines.append("  verified, so the comparison against the 50-200 uV rescaling target is a")
    lines.append("  flag for that check, not a finding about it.")
    lines.append("- Purity is measured over contacts the CCF label map can name. An unmapped")
    lines.append("  host label inside a band counts against purity rather than being ignored.")
    lines.append("- 'cumulative_drift_um_per_hour' is present in these files and is not used.")
    lines.append("  Its values reach millions of micrometres per hour, so whatever it")
    lines.append("  accumulates it is not net probe drift, and drift remains an open gate.")
    lines.append("")

    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", required=True, help="target structure acronym, e.g. CA1")
    parser.add_argument("--assets-cache", default=None,
                        help="JSON file caching the DANDI asset listing; required unless "
                             "--from-records is given")
    parser.add_argument("--index", default=None,
                        help="anatomy index written by survey_host_anatomy.py; required "
                             "unless --from-records is given")
    parser.add_argument("--from-records", default=None,
                        help="rewrite the report from a previous run's JSON records, with "
                             "no network reads. Use when only the presentation changed.")
    parser.add_argument("--skipped-note", type=int, default=0,
                        help="with --from-records, the skipped-recording count to print")
    parser.add_argument("--out", required=True, help="path of the report to write")
    parser.add_argument("--records", default=None,
                        help="optional path for the raw JSON records")
    parser.add_argument("--dandiset", default="000409", help="dandiset identifier")
    parser.add_argument("--version", default="draft", help="dandiset version")
    parser.add_argument("--max-gap-um", type=float, default=40.0,
                        help="band contiguity tolerance; must match the anatomy survey's")
    parser.add_argument("--min-band-channels", type=int, default=20,
                        help="only screen bands with at least this many contacts")
    parser.add_argument("--n-units", type=int, default=10,
                        help="injected units per recording instance (Claim Sheet Slot 9)")
    parser.add_argument("--edge-margin-um", type=float, default=60.0,
                        help="declared clearance required between a peak and each band edge")
    parser.add_argument("--min-separation-um", type=float, default=40.0,
                        help="declared minimum separation between injected peaks")
    parser.add_argument("--min-purity", type=float, default=0.95,
                        help="declared minimum fraction of in-range contacts on target")
    parser.add_argument("--edge-margins", default="20,60,100,140",
                        help="comma-separated edge margins for the capacity sweep")
    parser.add_argument("--separations", default="20,40,80",
                        help="comma-separated separations for the capacity sweep")
    parser.add_argument("--block-kb", type=int, default=1024,
                        help="HTTP range block size in KiB")
    parser.add_argument("--limit", type=int, default=None,
                        help="screen at most this many recordings, for smoke tests")
    parser.add_argument("--legacy-index-target", default=None,
                        help="explicit target for index records lacking embedded provenance")
    parser.add_argument("--legacy-index-max-gap-um", type=float, default=None,
                        help="explicit max-gap for those legacy records")
    args = parser.parse_args(argv)
    args.edge_margins = [float(v) for v in args.edge_margins.split(",") if v.strip()]
    args.separations = [float(v) for v in args.separations.split(",") if v.strip()]
    if args.min_separation_um <= 0 or args.edge_margin_um < 0:
        raise SystemExit("[fatal] separation must be positive and margin non-negative")
    if not args.from_records and not (args.index and args.assets_cache):
        raise SystemExit("[fatal] --index and --assets-cache are required unless "
                         "--from-records is given")
    return args


def main(argv=None):
    """Screen every indexed candidate and write the placement report."""
    args = parse_args(argv)
    if args.from_records:
        with open(args.from_records, "r", encoding="utf-8") as handle:
            results = json.load(handle)
        write_report(args.out, results, args, args.skipped_note)
        print(f"rewrote {args.out} from {args.from_records} with no network reads", flush=True)
        return 0
    records = load_index(args.index)
    try:
        anatomy_index.validate_configuration(
            records, args.target, args.max_gap_um,
            legacy_target=args.legacy_index_target,
            legacy_max_gap_um=args.legacy_index_max_gap_um)
    except ValueError as exc:
        raise SystemExit(f"[fatal] {exc}")

    assets = dandi.list_assets(args.dandiset, args.version, cache_path=args.assets_cache)
    assets_by_id = {a["asset_id"]: a for a in assets}
    processed_by_session = {}
    for asset in assets:
        if asset["path"].endswith(dandi.PROCESSED_SUFFIX):
            session = dandi.session_of(asset)
            if session in processed_by_session:
                raise SystemExit(
                    f"[fatal] multiple processed assets found for session {session}: "
                    f"{processed_by_session[session]['path']} and {asset['path']}")
            processed_by_session[session] = asset

    block_bytes = args.block_kb * 1024
    results = []
    skipped = 0
    ordered = sorted(records.values(), key=lambda r: -max(
        [p["target_band"]["n_channels"] for p in r["probes"] if p.get("target_band")] or [0]))
    for record in ordered:
        if args.limit is not None and len(results) >= args.limit:
            break
        raw_asset = assets_by_id.get(record["asset_id"])
        if raw_asset is None:
            raise SystemExit(f"[fatal] indexed asset {record['asset_id']} is not in the "
                             f"asset listing; the index and the listing disagree")
        result = screen_asset(record, raw_asset,
                              processed_by_session.get(record["session"]), args.target,
                              args.max_gap_um, block_bytes, args)
        if result is None:
            skipped += 1
            continue
        results.append(result)
        for probe in result["probes"]:
            print("[placement] {:<10} {:<8} {:<9} span={:>5.0f} purity={:>5.1f}% "
                  "native={:<5} verdict={}".format(
                      result["subject"], result["session"][:8], probe["probe"],
                      probe["band"]["span_um"] if probe["band"] else -1,
                      100.0 * probe["profile"]["purity"] if probe["profile"] else -1,
                      (probe["native"] or {}).get("n_units", "-"),
                      "PASS" if probe["passes"] else "FAIL"), flush=True)

    if not results:
        raise SystemExit("[fatal] no candidate band met --min-band-channels; nothing screened")

    write_report(args.out, results, args, skipped)
    print(f"wrote {args.out}", flush=True)
    if args.records:
        with open(args.records, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(results, handle, indent=1, sort_keys=True)
        print(f"wrote {args.records}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
