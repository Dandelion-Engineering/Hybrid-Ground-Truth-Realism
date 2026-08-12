"""Apply the duration and sampling-regularity gate to surviving Tier A host candidates.

Slot 7 requires a selected host to have "adequate duration", and the anatomy
survey (``survey_host_anatomy.py``) cannot supply it: these IBL raw NWB
``ElectricalSeries`` nodes carry an explicit ``timestamps`` dataset rather than
a ``starting_time`` with a ``rate`` attribute, so the anatomy index records each
AP series' sample count without a sampling rate. A sample count with no rate is
not a duration, and assuming 30 kHz would be inventing the number this gate
exists to measure.

This script reads the real timing. For each candidate it reads the first and
last elements of the AP series' ``timestamps`` dataset over HTTP range requests
-- never the sample data -- and reports the measured sampling rate, the measured
duration, and how regular the timestamps are at the start and end of the
recording. Irregular timestamps matter beyond duration: the injection pipeline
places spikes at sample indices, so a recording whose clock drifts or whose
samples are not evenly spaced would make an injected spike time mean something
slightly different from a real one.

Cost discipline: reading the last timestamp pulls a distant chunk, so this is
deliberately run **only on candidates that already survived the anatomy screen**
rather than on all 429 eligible recordings. That ordering is the reviewer ruling
recorded in ``agents/Claude/Tier A Host and Injection Zone Selection.md`` (7.3):
apply the remaining gates sequentially to the current candidate set rather than
paying for a full census.

What this script does **not** do, and what still gates a host afterwards: drift
quantification, noise measurement, post-rescaling effective SNR, covariate
balance between the region-matched and region-unaware arms, and confirmation
that ten injected units fit the band without overcrowding.

Example
-------
    ./venv/Scripts/python.exe "Reproducibility Packet/scripts/screen_host_timing.py" \
        --index "Reproducibility Packet/results/host_anatomy_index.jsonl" \
        --assets-cache "Reproducibility Packet/results/dandi_000409_assets.json" \
        --target CA1 --min-band-channels 20 --min-duration-s 600 \
        --timing-index "Reproducibility Packet/results/host_timing_index.jsonl" \
        --out "Reproducibility Packet/results/host_timing_CA1.txt"
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import h5py  # noqa: E402

from utils import dandi  # noqa: E402
from utils.remote_hdf5 import RemoteFile  # noqa: E402


def _edge_stats(timestamps, n_edge):
    """Summarise the spacing of a run of timestamps.

    Args:
        timestamps: a sequence of monotonically increasing sample times, in
            seconds.
        n_edge: how many were requested, for the record.

    Returns:
        A dict with the implied rate from the first interval, the mean, minimum
        and maximum intervals, and whether the run is strictly increasing.
    """
    diffs = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
    if not diffs:
        return None
    mean_dt = sum(diffs) / len(diffs)
    return {
        "n": n_edge,
        "mean_dt_s": mean_dt,
        "min_dt_s": min(diffs),
        "max_dt_s": max(diffs),
        "rate_from_mean_hz": 1.0 / mean_dt if mean_dt else None,
        "monotonic": min(diffs) > 0,
    }


def read_series_timing(url, size, block_bytes, n_edge):
    """Read AP-series timing from one remote NWB without touching sample data.

    Args:
        url: direct S3 URL of the NWB blob.
        size: the blob's size in bytes.
        block_bytes: HTTP range-request block size.
        n_edge: how many timestamps to read at each end of each series.

    Returns:
        A dict with ``series`` (one entry per AP acquisition series) and ``io``
        (request count and bytes transferred).

    Raises:
        KeyError: if the file has no acquisition group, which is a malformed
            host and must be reported rather than skipped silently.
    """
    remote = RemoteFile(url, size, block=block_bytes)
    series = []
    with h5py.File(remote, "r") as handle:
        if "acquisition" not in handle:
            raise KeyError(f"{url} has no acquisition group")
        acquisition = handle["acquisition"]
        # Name-first, exactly as the anatomy survey does: iterating the whole
        # acquisition group forces h5py to read every member's object header,
        # and a raw IBL file holds fourteen of them.
        for name in [key for key in acquisition.keys() if key.endswith("AP")]:
            node = acquisition[name]
            if "data" not in node:
                continue
            shape = list(node["data"].shape)
            entry = {"name": name, "shape": shape}
            if "timestamps" not in node:
                # Older or differently written files may carry starting_time
                # instead. Record which path supplied the number rather than
                # silently mixing the two.
                if "starting_time" in node:
                    rate = float(node["starting_time"].attrs.get("rate", float("nan")))
                    entry["timing_source"] = "starting_time"
                    entry["rate_hz"] = rate
                    entry["duration_s"] = shape[0] / rate if rate else None
                else:
                    entry["timing_source"] = "none"
                series.append(entry)
                continue
            stamps = node["timestamps"]
            n_samples = stamps.shape[0]
            take = min(n_edge, n_samples)
            head = [float(v) for v in stamps[:take]]
            tail = [float(v) for v in stamps[-take:]]
            entry.update({
                "timing_source": "timestamps",
                "n_timestamps": int(n_samples),
                "t_first_s": head[0],
                "t_last_s": tail[-1],
                "duration_s": tail[-1] - head[0],
                "rate_hz": (n_samples - 1) / (tail[-1] - head[0])
                if tail[-1] > head[0] else None,
                "head": _edge_stats(head, take),
                "tail": _edge_stats(tail, take),
            })
            series.append(entry)
    return {"series": series, "io": {"requests": remote.n_requests, "bytes": remote.n_bytes}}


def load_jsonl(path):
    """Load a JSONL index keyed by ``asset_id``.

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


def select_candidates(anatomy, target, min_band_channels):
    """Pick the assets whose anatomy record shows a usable injection zone.

    Args:
        anatomy: asset_id -> anatomy record, from the anatomy survey's index.
        target: target structure acronym, e.g. ``"CA1"``.
        min_band_channels: minimum contiguous band size, in channels.

    Returns:
        A list of (asset_id, record, best_band_channels), largest band first.
    """
    selected = []
    for asset_id, record in anatomy.items():
        bands = [probe["target_band"]["n_channels"] for probe in record.get("probes", [])
                 if probe.get("target_band")]
        best = max(bands) if bands else 0
        if best >= min_band_channels:
            selected.append((asset_id, record, best))
    selected.sort(key=lambda item: -item[2])
    return selected


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--index", required=True,
                        help="anatomy survey JSONL index to select candidates from")
    parser.add_argument("--assets-cache", required=True,
                        help="JSON asset listing, used to resolve blob URLs and sizes")
    parser.add_argument("--dandiset", default="000409", help="dandiset id (default: 000409)")
    parser.add_argument("--version", default="draft", help="dandiset version (default: draft)")
    parser.add_argument("--target", default="CA1",
                        help="target structure acronym used by the anatomy screen (default: CA1)")
    parser.add_argument("--min-band-channels", type=int, default=20,
                        help="minimum contiguous target-structure band, in channels "
                             "(default: 20, matching the anatomy report threshold)")
    parser.add_argument("--min-duration-s", type=float, default=600.0,
                        help="declared duration gate in seconds (default: 600, the Rung 2 "
                             "segment length). Reported as pass/fail; hosts are not dropped "
                             "by this script.")
    parser.add_argument("--n-edge", type=int, default=1000,
                        help="timestamps read at each end of each series for the regularity "
                             "check (default: 1000)")
    parser.add_argument("--block-kb", type=int, default=1024,
                        help="HTTP range block size in KiB (default: 1024)")
    parser.add_argument("--limit", type=int, default=None,
                        help="screen at most this many new assets this run")
    parser.add_argument("--timing-index", default=None,
                        help="JSONL index to append to and resume from")
    parser.add_argument("--out", default=None, help="path to write the report to")
    args = parser.parse_args()

    if args.n_edge < 2:
        sys.exit("[fatal] --n-edge must be at least 2 to measure an interval")
    if args.block_kb <= 0:
        sys.exit("[fatal] --block-kb must be positive")

    anatomy = load_jsonl(args.index)
    if not anatomy:
        sys.exit(f"[fatal] no anatomy records found in {args.index!r}; run "
                 f"survey_host_anatomy.py first")
    candidates = select_candidates(anatomy, args.target, args.min_band_channels)
    print(f"[timing] {len(candidates)} of {len(anatomy)} indexed assets carry a "
          f"{args.target} band of >= {args.min_band_channels} channels", flush=True)

    assets = {a["asset_id"]: a for a in
              dandi.list_assets(args.dandiset, args.version, cache_path=args.assets_cache)}
    done = load_jsonl(args.timing_index)
    pending = [item for item in candidates if item[0] not in done]
    if args.limit is not None:
        pending = pending[:args.limit]
    print(f"[timing] {len(done)} already timed, reading {len(pending)} now", flush=True)

    failures = []
    handle_out = open(args.timing_index, "a", encoding="utf-8") if args.timing_index else None
    try:
        for number, (asset_id, record, band) in enumerate(pending, start=1):
            asset = assets.get(asset_id)
            if asset is None:
                failures.append((record.get("path", asset_id), "asset not in listing cache"))
                print(f"[{number}/{len(pending)}] FAILED {record.get('path')}: "
                      f"not in listing cache", flush=True)
                continue
            try:
                timing = read_series_timing(dandi.blob_url(asset), asset["size"],
                                            args.block_kb * 1024, args.n_edge)
            except (OSError, KeyError, ValueError) as exc:
                failures.append((asset["path"], f"{type(exc).__name__}: {exc}"))
                print(f"[{number}/{len(pending)}] FAILED {asset['path']}: {exc}", flush=True)
                continue
            entry = {
                "asset_id": asset_id,
                "path": asset["path"],
                "subject": record.get("subject"),
                "session": record.get("session"),
                "best_band_channels": band,
                "series": timing["series"],
                "io": timing["io"],
            }
            done[asset_id] = entry
            if handle_out:
                handle_out.write(json.dumps(entry) + "\n")
                handle_out.flush()
            durations = [s.get("duration_s") for s in timing["series"] if s.get("duration_s")]
            shortest = min(durations) if durations else float("nan")
            print(f"[{number}/{len(pending)}] {entry['subject']:<14} "
                  f"{len(timing['series'])} AP series  shortest {shortest / 60:.1f} min  "
                  f"({timing['io']['bytes'] / 1e6:.1f} MB)", flush=True)
    finally:
        if handle_out:
            handle_out.close()

    report = []

    def emit(line=""):
        print(line, flush=True)
        report.append(line)

    reported = {asset_id: done[asset_id] for asset_id, _, _ in candidates if asset_id in done}
    total_bytes = sum(e["io"]["bytes"] for e in reported.values())

    emit()
    emit("# Host timing screen")
    emit()
    emit(f"dandiset            {args.dandiset} ({args.version})")
    emit(f"target structure    {args.target}")
    emit(f"band threshold      {args.min_band_channels} channels")
    emit(f"candidates          {len(candidates)}")
    emit(f"timed               {len(reported)}")
    emit(f"failed this run     {len(failures)}")
    emit(f"duration gate       {args.min_duration_s:.0f} s "
         f"({args.min_duration_s / 60:.1f} min)")
    emit(f"bytes transferred   {total_bytes / 1e6:.1f} MB total, metadata only")
    emit()
    emit("Sampling rate and duration are measured from each AP series' own `timestamps`")
    emit("dataset -- first and last elements -- not assumed from a nominal 30 kHz. The")
    emit("regularity columns summarise the intervals across the first and last")
    emit(f"{args.n_edge} timestamps of each series.")
    emit()

    emit("## Measured timing per AP series")
    emit()
    emit(f"{'subject':<14}{'session':<10}{'series':<26}{'samples':>12}{'ch':>5}"
         f"{'rate_hz':>13}{'minutes':>9}  gate")
    emit("-" * 100)
    for entry in sorted(reported.values(), key=lambda e: -e["best_band_channels"]):
        for s in entry["series"]:
            duration = s.get("duration_s")
            rate = s.get("rate_hz")
            shape = s.get("shape") or [None, None]
            gate = "-"
            if duration is not None:
                gate = "pass" if duration >= args.min_duration_s else "FAIL"
            emit(f"{(entry['subject'] or '?'):<14}{(entry['session'] or '?')[:8]:<10}"
                 f"{s['name'][:25]:<26}{(shape[0] if shape else 0):>12}"
                 f"{(shape[1] if len(shape) > 1 else 0):>5}"
                 f"{(f'{rate:.4f}' if rate else '?'):>13}"
                 f"{(f'{duration / 60:.1f}' if duration else '?'):>9}  {gate}")
    emit()

    emit("## Timestamp regularity")
    emit()
    emit(f"{'subject':<14}{'series':<26}{'edge':<6}{'mean_dt_us':>12}{'min_dt_us':>12}"
         f"{'max_dt_us':>12}{'monotonic':>11}")
    emit("-" * 95)
    for entry in sorted(reported.values(), key=lambda e: -e["best_band_channels"]):
        for s in entry["series"]:
            for edge in ("head", "tail"):
                stats = s.get(edge)
                if not stats:
                    continue
                emit(f"{(entry['subject'] or '?'):<14}{s['name'][:25]:<26}{edge:<6}"
                     f"{stats['mean_dt_s'] * 1e6:>12.4f}{stats['min_dt_s'] * 1e6:>12.4f}"
                     f"{stats['max_dt_s'] * 1e6:>12.4f}{str(stats['monotonic']):>11}")
    emit()

    if failures:
        emit("## Failures")
        emit()
        for path, reason in failures:
            emit(f"  {path}: {reason}")
        emit()

    emit("This screen measures duration and timestamp regularity only. Drift, noise level,")
    emit("post-rescaling effective SNR, ten-placement feasibility, and covariate balance")
    emit("remain separate gates that a host passing here can still fail. No host is dropped")
    emit("by this script; the gate column records the declared threshold's verdict.")

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write("\n".join(report) + "\n")
        print(f"[write] wrote report to {args.out}", flush=True)


if __name__ == "__main__":
    main()
