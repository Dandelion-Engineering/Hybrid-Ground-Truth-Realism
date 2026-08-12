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

The current tracked index predates embedded configuration metadata. To resume
that specific CA1/40-um index safely, also pass
``--legacy-index-target CA1 --legacy-index-max-gap-um 40``.
"""

import argparse
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import anatomy_index, ccf_labels, dandi  # noqa: E402
from utils.host_anatomy import contiguous_band, read_electrode_table  # noqa: E402


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
        "anatomy_target": target,
        "anatomy_max_gap_um": max_gap_um,
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
    parser.add_argument("--legacy-index-target", default=None,
                        help="explicit target used to build legacy index records that lack "
                             "embedded configuration metadata")
    parser.add_argument("--legacy-index-max-gap-um", type=float, default=None,
                        help="explicit max-gap value used to build those legacy records")
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
    try:
        anatomy_index.validate_configuration(
            all_records,
            args.target,
            args.max_gap_um,
            legacy_target=args.legacy_index_target,
            legacy_max_gap_um=args.legacy_index_max_gap_um,
        )
    except ValueError as exc:
        sys.exit(f"[fatal] {exc}")
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
