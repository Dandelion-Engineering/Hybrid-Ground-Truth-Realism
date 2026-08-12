"""Survey DANDI 000409 recordings for Tier A host and injection-zone feasibility.

Tier A injects region-matched donor templates into a real host recording, which
means a host is only usable if the project can point at a *specific depth band*
of its probe and say what brain structure that band sits in. A Neuropixels
penetration crosses many structures, so a whole-recording region label is not
good enough and this project never invents one.

The annotation already exists: every 000409 NWB file carries a
``/general/extracellular_ephys/electrodes`` table with one Allen CCF long name
per electrode, plus the electrode's position along the probe. This script reads
that table -- and only that table -- from each candidate recording over HTTP
range requests, so a 18-197 GB file costs a few megabytes to screen instead of
an overnight download.

For each recording it records, per probe: the channel count, the structures the
penetration crosses, and for a requested target structure the deepest
contiguous band of channels carrying that label. It then ranks candidate hosts
by the size of that band.

What this script does **not** do, and what still gates a host afterwards: drift
quantification, noise measurement, post-rescaling effective SNR, covariate
balance between the region-matched and region-unaware arms, and confirmation
that ten injected units fit the band without overcrowding. Those are separate
gates, and a host that ranks first here can still fail them.

Example
-------
    ./venv/Scripts/python.exe "Reproducibility Packet/scripts/survey_host_anatomy.py" \
        --target CA1 --exclude-subjects KS042,KS043 --limit 50 \
        --index "Reproducibility Packet/results/host_anatomy_index.jsonl" \
        --out "Reproducibility Packet/results/host_anatomy_CA1.txt"
"""

import argparse
import json
import os
import sys
from collections import Counter, OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import h5py  # noqa: E402

from utils import ccf_labels, dandi  # noqa: E402
from utils.remote_hdf5 import RemoteFile  # noqa: E402

ELECTRODES_PATH = "general/extracellular_ephys/electrodes"


def read_electrode_table(url, size, block_bytes):
    """Read one NWB file's electrodes table without downloading the recording.

    Args:
        url: direct S3 URL of the NWB blob.
        size: the blob's size in bytes.
        block_bytes: HTTP range-request block size.

    Returns:
        A dict with ``probes`` (an ordered mapping from probe name to a list of
        per-electrode dicts), ``series`` (AP acquisition series descriptions),
        and ``io`` (request count and bytes transferred).

    Raises:
        KeyError: if the file has no electrodes table, which is a malformed
            host and must be reported rather than skipped silently.
    """
    remote = RemoteFile(url, size, block=block_bytes)
    probes = OrderedDict()
    series = []
    with h5py.File(remote, "r") as handle:
        if ELECTRODES_PATH not in handle:
            raise KeyError(f"{url} has no {ELECTRODES_PATH}")
        table = handle[ELECTRODES_PATH]
        locations = [value.decode() if isinstance(value, bytes) else str(value)
                     for value in table["location"][:]]
        groups = [value.decode() if isinstance(value, bytes) else str(value)
                  for value in table["group_name"][:]]
        ids = table["id"][:].tolist()
        depths = table["rel_y"][:].tolist() if "rel_y" in table else [None] * len(ids)
        lateral = table["rel_x"][:].tolist() if "rel_x" in table else [None] * len(ids)
        for index, probe in enumerate(groups):
            probes.setdefault(probe, []).append({
                "id": ids[index],
                "location": locations[index],
                "acronym": ccf_labels.to_acronym(locations[index]),
                "depth_um": depths[index],
                "lateral_um": lateral[index],
            })
        # List names first and open only the AP series. Iterating the whole
        # acquisition group would force h5py to read every member's object
        # header, and a raw IBL file holds fourteen of them -- the video and
        # event series alone triple the bytes this screen has to transfer.
        acquisition = handle["acquisition"] if "acquisition" in handle else {}
        for name in [key for key in acquisition.keys() if key.endswith("AP")]:
            node = acquisition[name]
            if "data" not in node:
                continue
            entry = {"name": name, "shape": list(node["data"].shape)}
            if "starting_time" in node:
                entry["rate_hz"] = float(node["starting_time"].attrs.get("rate", float("nan")))
            if entry.get("rate_hz") and entry["shape"]:
                entry["duration_s"] = entry["shape"][0] / entry["rate_hz"]
            series.append(entry)
    return {
        "probes": probes,
        "series": series,
        "io": {"requests": remote.n_requests, "bytes": remote.n_bytes},
    }


def contiguous_band(electrodes, acronym, max_gap_um):
    """Find the largest contiguous depth band labelled with one structure.

    Neuropixels 1.0 contacts sit on rows 20 um apart, so a band is defined as a
    run of matching depths whose successive gaps never exceed ``max_gap_um``.
    Interruptions larger than that mean the probe left the structure and
    re-entered it, which is a different placement problem.

    Args:
        electrodes: per-electrode dicts for one probe.
        acronym: the target structure's template-library acronym.
        max_gap_um: largest tolerated gap between successive matching depths.

    Returns:
        A dict describing the largest band -- ``depth_lo_um``, ``depth_hi_um``,
        ``n_channels``, ``span_um`` -- or None when the structure is absent or
        its depths are unknown.
    """
    depths = sorted({e["depth_um"] for e in electrodes
                     if e["acronym"] == acronym and e["depth_um"] is not None})
    if not depths:
        return None
    best = current = [depths[0]]
    for depth in depths[1:]:
        if depth - current[-1] <= max_gap_um:
            current.append(depth)
        else:
            if len(current) > len(best):
                best = current
            current = [depth]
    if len(current) > len(best):
        best = current
    band = set(best)
    n_channels = sum(1 for e in electrodes
                     if e["acronym"] == acronym and e["depth_um"] in band)
    return {
        "depth_lo_um": best[0],
        "depth_hi_um": best[-1],
        "span_um": best[-1] - best[0],
        "n_rows": len(best),
        "n_channels": n_channels,
    }


def describe_asset(asset, target, max_gap_um, block_bytes):
    """Screen one recording and return a JSON-serialisable record.

    Args:
        asset: a DANDI asset dict.
        target: target structure acronym, or None to survey anatomy only.
        max_gap_um: largest tolerated gap inside a contiguous band.
        block_bytes: HTTP range-request block size.

    Returns:
        A record with the asset's identity, per-probe anatomy, target-band
        geometry, and any unmapped structure labels encountered.
    """
    table = read_electrode_table(dandi.blob_url(asset), asset["size"], block_bytes)
    probes = []
    unmapped = set()
    for probe, electrodes in table["probes"].items():
        counts = Counter(e["acronym"] or f"<unmapped:{e['location']}>" for e in electrodes)
        unmapped.update(e["location"] for e in electrodes if e["acronym"] is None)
        entry = {
            "probe": probe,
            "n_channels": len(electrodes),
            "structures": dict(counts.most_common()),
            "target_band": contiguous_band(electrodes, target, max_gap_um) if target else None,
        }
        probes.append(entry)
    return {
        "asset_id": asset["asset_id"],
        "path": asset["path"],
        "size_bytes": asset["size"],
        "subject": dandi.subject_of(asset),
        "session": dandi.session_of(asset),
        "probes": probes,
        "series": table["series"],
        "unmapped_labels": sorted(unmapped),
        "io": table["io"],
    }


def load_index(path):
    """Load an existing JSONL index so a run can resume.

    Args:
        path: JSONL file written by a previous run, or None.

    Returns:
        A dict from asset_id to record, empty when no usable index exists.
    """
    records = {}
    if not path or not os.path.exists(path):
        return records
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            records[record["asset_id"]] = record
    return records


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--dandiset", default="000409", help="dandiset id (default: 000409)")
    parser.add_argument("--version", default="draft", help="dandiset version (default: draft)")
    parser.add_argument("--assets-cache", default=None,
                        help="JSON file caching the asset listing, for repeatable runs")
    parser.add_argument("--suffix", default=dandi.RAW_SUFFIX,
                        help="asset path suffix identifying host candidates "
                             f"(default: {dandi.RAW_SUFFIX!r})")
    parser.add_argument("--target", default=None,
                        help="target structure acronym for the injection zone, e.g. 'CA1'")
    parser.add_argument("--max-gap-um", type=float, default=40.0,
                        help="largest gap between successive contact rows still counted as one "
                             "contiguous band (default: 40, two Neuropixels 1.0 rows)")
    parser.add_argument("--exclude-subjects", default="",
                        help="comma-separated subject identifiers to skip, e.g. the donor "
                             "library's subjects when avoiding shared provenance")
    parser.add_argument("--min-band-channels", type=int, default=20,
                        help="report threshold for a usable injection zone (default: 20)")
    parser.add_argument("--limit", type=int, default=None,
                        help="screen at most this many new assets this run")
    parser.add_argument("--block-kb", type=int, default=1024,
                        help="HTTP range block size in KiB (default: 1024). The electrodes table "
                             "and AP headers are scattered, so smaller blocks transfer less; "
                             "larger blocks issue fewer requests.")
    parser.add_argument("--index", default=None,
                        help="JSONL index to append to and resume from")
    parser.add_argument("--out", default=None, help="path to write the ranked report to")
    args = parser.parse_args()

    if args.max_gap_um <= 0:
        sys.exit("[fatal] --max-gap-um must be positive")
    if args.block_kb <= 0:
        sys.exit("[fatal] --block-kb must be positive")
    if args.target and args.target not in set(ccf_labels.NAME_TO_ACRONYM.values()):
        print(f"[warn] target {args.target!r} is not in the CCF label map; host labels for it "
              f"will not be recognised. Add it to utils/ccf_labels.py first.", flush=True)

    excluded = {s.strip() for s in args.exclude_subjects.split(",") if s.strip()}
    assets = dandi.list_assets(args.dandiset, args.version, cache_path=args.assets_cache)
    candidates = [a for a in assets
                  if a["path"].endswith(args.suffix) and dandi.subject_of(a) not in excluded]
    print(f"[survey] {len(candidates)} candidate assets after excluding "
          f"{len(excluded)} subject(s)", flush=True)

    # The index may hold records from earlier runs with different filters. The
    # report must describe the assets this run is about, not everything ever
    # indexed, or an exclusion silently fails to exclude anything.
    all_records = load_index(args.index)
    candidate_ids = {a["asset_id"] for a in candidates}
    records = {k: v for k, v in all_records.items() if k in candidate_ids}
    if len(all_records) != len(records):
        print(f"[survey] index holds {len(all_records)} records; "
              f"{len(records)} match this run's filters and are reported", flush=True)
    pending = [a for a in candidates if a["asset_id"] not in records]
    if args.limit is not None:
        pending = pending[:args.limit]
    print(f"[survey] {len(records)} already indexed, screening {len(pending)} now", flush=True)

    failures = []
    index_handle = open(args.index, "a", encoding="utf-8") if args.index else None
    try:
        for number, asset in enumerate(pending, start=1):
            try:
                record = describe_asset(asset, args.target, args.max_gap_um,
                                        args.block_kb * 1024)
            except (OSError, KeyError, ValueError) as exc:
                failures.append((asset["path"], f"{type(exc).__name__}: {exc}"))
                print(f"[{number}/{len(pending)}] FAILED {asset['path']}: {exc}", flush=True)
                continue
            records[record["asset_id"]] = record
            if index_handle:
                index_handle.write(json.dumps(record) + "\n")
                index_handle.flush()
            bands = [p["target_band"]["n_channels"] for p in record["probes"]
                     if p.get("target_band")]
            best = max(bands) if bands else 0
            print(f"[{number}/{len(pending)}] {record['subject']:<14} "
                  f"{len(record['probes'])} probe(s)  {args.target or '-'} band {best:>4} ch  "
                  f"({record['io']['bytes'] / 1e6:.1f} MB)", flush=True)
    finally:
        if index_handle:
            index_handle.close()

    report = []

    def emit(line=""):
        print(line, flush=True)
        report.append(line)

    emit()
    emit("# Host anatomy survey")
    emit()
    emit(f"dandiset            {args.dandiset} ({args.version})")
    emit(f"asset suffix        {args.suffix}")
    emit(f"subjects excluded   {', '.join(sorted(excluded)) if excluded else '(none)'}")
    emit(f"candidates          {len(candidates)}")
    emit(f"indexed             {len(records)}")
    emit(f"failed this run     {len(failures)}")
    emit(f"target structure    {args.target or '(anatomy only)'}")
    emit(f"max band gap        {args.max_gap_um} um")
    emit()

    unmapped = Counter()
    for record in records.values():
        unmapped.update(record.get("unmapped_labels", []))
    if unmapped:
        emit(f"## Unmapped CCF labels ({len(unmapped)} distinct)")
        emit()
        emit("These host structure names have no entry in utils/ccf_labels.py, so no donor can")
        emit("be matched to them. They are listed rather than dropped.")
        emit()
        for label, count in unmapped.most_common(40):
            emit(f"  {count:>5} recording(s)  {label}")
        if len(unmapped) > 40:
            emit(f"  ... and {len(unmapped) - 40} more")
        emit()

    if args.target:
        rows = []
        for record in records.values():
            for probe in record["probes"]:
                band = probe.get("target_band")
                if band and band["n_channels"] >= args.min_band_channels:
                    rows.append((band["n_channels"], record, probe, band))
        rows.sort(key=lambda item: -item[0])
        emit(f"## Recordings with a contiguous {args.target} band of at least "
             f"{args.min_band_channels} channels")
        emit()
        emit(f"{'ch':>4}{'rows':>6}{'depth_lo':>10}{'depth_hi':>10}{'probe':>10}"
             f"{'subject':>16}  session / path")
        emit("-" * 100)
        for n_channels, record, probe, band in rows[:60]:
            emit(f"{n_channels:>4}{band['n_rows']:>6}{band['depth_lo_um']:>10.0f}"
                 f"{band['depth_hi_um']:>10.0f}{probe['probe']:>10}{record['subject']:>16}  "
                 f"{(record['session'] or '?')[:8]}  {record['path']}")
        emit()
        emit(f"recordings meeting the threshold: {len(rows)} of "
             f"{sum(len(r['probes']) for r in records.values())} probe(s) indexed")
        emit()

    if failures:
        emit("## Failures")
        emit()
        for path, reason in failures:
            emit(f"  {path}: {reason}")
        emit()

    emit("Screening here is anatomical only. Drift, noise level, post-rescaling effective SNR,")
    emit("covariate balance, and whether ten injected units fit the band without overcrowding")
    emit("remain separate gates that a top-ranked host can still fail.")

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write("\n".join(report) + "\n")
        print(f"[write] wrote report to {args.out}", flush=True)


if __name__ == "__main__":
    main()
