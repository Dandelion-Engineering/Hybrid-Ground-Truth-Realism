"""Read the storage layout of one raw AP ElectricalSeries, without reading samples.

The noise gate specified in Section 19 of
``agents/Claude/Tier A Host and Injection Zone Selection.md`` is the first gate
in this project that needs raw sample data, so its cost is a property of how
that data is stored rather than of how many samples the estimator wants. This
probe reads only the dataset's *description* -- dtype, chunk shape, filter
pipeline, and the ElectricalSeries scaling attributes that turn stored integers
into volts -- and never slices the sample array. It exists so the section's
transfer model is measured rather than assumed.

The boundary is deliberate and is enforced below: nothing here reads a value
from the ``data`` dataset, so running it discloses no noise, no amplitude and
no candidate gate value. ``channel_conversion`` is read because it is an
acquisition gain table rather than signal, and the microvolt convention cannot
be stated without it.

Example:
    ./venv/Scripts/python.exe "agents/Claude/tools/probe_raw_ap_layout.py" \
        --repo-root . \
        --session b52182e7-39f6-4914-9717-136db589706e \
        --probe Probe01 \
        --assets-cache "Reproducibility Packet/results/dandi_000409_assets.json" \
        --out "agents/Claude/tools/raw_ap_layout_CSHL047_Probe01.txt"
"""

import argparse
import json
import os
import sys

import h5py


def add_packet_scripts(repo_root):
    """Put the reproducibility packet's ``scripts`` directory on ``sys.path``.

    Args:
        repo_root: path to the repository root.

    Returns:
        The absolute scripts path that was added.

    Raises:
        SystemExit: if the directory is absent, which means the caller pointed
            ``--repo-root`` somewhere that is not this repository.
    """
    scripts = os.path.abspath(os.path.join(repo_root, "Reproducibility Packet", "scripts"))
    if not os.path.isdir(scripts):
        raise SystemExit(f"[fatal] no packet scripts directory at {scripts}")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    return scripts


def describe_filters(dataset):
    """Summarize the HDF5 filter pipeline applied to a dataset.

    Args:
        dataset: an open ``h5py.Dataset``.

    Returns:
        A dict naming compression, its options, shuffle and fletcher32. A
        compressed dataset cannot be read below chunk granularity, so this is
        what decides whether a channel subset is cheaper than a whole row.
    """
    return {
        "compression": dataset.compression,
        "compression_opts": dataset.compression_opts,
        "shuffle": bool(dataset.shuffle),
        "fletcher32": bool(dataset.fletcher32),
        "scaleoffset": dataset.scaleoffset,
    }


def chunk_plan(shape, chunks, itemsize, n_band_channels, seconds, rate_hz):
    """Compute what one contiguous time window costs at this chunk layout.

    Args:
        shape: the dataset's ``(n_samples, n_channels)`` shape.
        chunks: the chunk shape, or None for a contiguous dataset.
        itemsize: bytes per stored sample.
        n_band_channels: how many channels the injection band spans.
        seconds: the length of one window in seconds.
        rate_hz: the stream's sampling rate.

    Returns:
        A dict with the number of samples requested, the number of chunks the
        request touches along each axis, and the stored bytes those chunks
        hold. For a contiguous dataset the chunk terms are None and the cost is
        reported as the whole-row span, which is the honest figure: a
        contiguous two-dimensional array is stored row-major, so a channel
        subset of a sample range is not a contiguous byte range.
    """
    n_samples = int(round(seconds * rate_hz))
    plan = {
        "window_s": seconds,
        "window_samples": n_samples,
        "band_channels": n_band_channels,
    }
    if chunks is None:
        plan.update({
            "layout": "contiguous",
            "chunks_time": None,
            "chunks_channel": None,
            "stored_bytes": n_samples * shape[1] * itemsize,
            "basis": "whole-row span; a channel subset is not a byte range",
        })
        return plan
    chunk_t, chunk_c = int(chunks[0]), int(chunks[1])
    # A window of n_samples can straddle one extra chunk boundary in time, and a
    # band of n_band_channels can straddle one extra boundary in channel, so
    # both terms are ceilings plus one rather than exact divisions.
    chunks_time = (n_samples + chunk_t - 1) // chunk_t + 1
    chunks_channel = (n_band_channels + chunk_c - 1) // chunk_c + 1
    chunks_channel = min(chunks_channel, (shape[1] + chunk_c - 1) // chunk_c)
    plan.update({
        "layout": "chunked",
        "chunk_shape": [chunk_t, chunk_c],
        "chunk_stored_bytes": chunk_t * chunk_c * itemsize,
        "chunks_time": chunks_time,
        "chunks_channel": chunks_channel,
        "stored_bytes": chunks_time * chunks_channel * chunk_t * chunk_c * itemsize,
        "basis": "worst-case straddle in both axes, uncompressed chunk size",
    })
    return plan


def read_layout(url, size, probe, block_bytes, band_channels):
    """Describe one probe's raw AP series without reading its samples.

    Args:
        url: the direct S3 URL of the raw NWB blob.
        size: the blob size in bytes.
        probe: the probe token, e.g. ``"Probe01"``.
        block_bytes: HTTP range-request block size.
        band_channels: how many channels the pinned injection band spans, used
            only to size the transfer plan.

    Returns:
        A dict describing the series, its scaling attributes, its filter
        pipeline and the per-window transfer plans.

    Raises:
        KeyError: if the file carries no acquisition group.
        SystemExit: unless exactly one AP series decomposes to this probe.
    """
    from utils import archive_units
    from utils.remote_hdf5 import RemoteFile
    import measure_host_drift as drift

    remote = RemoteFile(url, size, block=block_bytes)
    record = {}
    with h5py.File(remote, "r") as handle:
        if "acquisition" not in handle:
            raise KeyError(f"{url} has no acquisition group")
        acquisition = handle["acquisition"]
        names = [key for key in acquisition.keys() if key.endswith("AP")]
        matches = [name for name in names if drift.series_probe(name) == probe]
        if len(matches) != 1:
            raise SystemExit(
                f"[fatal] probe {probe} resolves to {len(matches)} AP series "
                f"in {url}; names seen: {sorted(names)}"
            )
        name = matches[0]
        node = acquisition[name]
        data = node["data"]
        record["series_name"] = name
        record["shape"] = [int(v) for v in data.shape]
        record["dtype"] = str(data.dtype)
        record["itemsize"] = int(data.dtype.itemsize)
        record["logical_bytes"] = int(data.size) * int(data.dtype.itemsize)
        record["chunks"] = None if data.chunks is None else [int(v) for v in data.chunks]
        record["filters"] = describe_filters(data)
        record["stored_size_bytes"] = (
            int(data.id.get_storage_size()) if hasattr(data.id, "get_storage_size") else None
        )
        attrs = {}
        for key in ("conversion", "offset", "resolution", "unit"):
            if key in node.attrs:
                value = node.attrs[key]
                attrs[key] = (
                    archive_units.ascii_safe(value)
                    if isinstance(value, (str, bytes))
                    else float(value)
                )
            elif key in data.attrs:
                value = data.attrs[key]
                attrs[key] = (
                    archive_units.ascii_safe(value)
                    if isinstance(value, (str, bytes))
                    else float(value)
                )
        record["scaling"] = attrs
        if "channel_conversion" in node:
            gains = node["channel_conversion"][:]
            record["channel_conversion"] = {
                "n": int(gains.shape[0]),
                "min": float(gains.min()),
                "max": float(gains.max()),
                "distinct": int(len({float(v) for v in gains})),
                "unit": archive_units.ascii_safe(
                    node["channel_conversion"].attrs.get("unit", "")
                ),
            }
        else:
            record["channel_conversion"] = None
        rate = None
        if "timestamps" in node:
            record["timing_source"] = "timestamps"
            rate = 30000.0
        elif "starting_time" in node:
            record["timing_source"] = "starting_time"
            rate = float(node["starting_time"].attrs.get("rate", 30000.0))
        else:
            record["timing_source"] = "none"
        record["plan_rate_hz"] = rate
        record["plans"] = [
            chunk_plan(record["shape"], data.chunks, record["itemsize"],
                       band_channels, seconds, rate or 30000.0)
            for seconds in (1.0, 5.0)
        ]
    record["io"] = {"requests": int(remote.n_requests), "bytes": int(remote.n_bytes)}
    return record


def render(record, session, probe, asset_path):
    """Render the layout record as an ASCII report.

    Args:
        record: the dict returned by ``read_layout``.
        session: the session UUID.
        probe: the probe token.
        asset_path: the raw asset's DANDI path.

    Returns:
        The report text.
    """
    lines = []
    lines.append("Raw AP storage layout -- metadata only, no samples read")
    lines.append("=" * 62)
    lines.append(f"session      : {session}")
    lines.append(f"probe        : {probe}")
    lines.append(f"raw asset    : {asset_path}")
    lines.append(f"series       : {record['series_name']}")
    lines.append("")
    lines.append(f"shape        : {record['shape'][0]} samples x {record['shape'][1]} channels")
    lines.append(f"dtype        : {record['dtype']} ({record['itemsize']} bytes/sample)")
    lines.append(f"logical size : {record['logical_bytes']} bytes")
    lines.append(f"stored size  : {record['stored_size_bytes']} bytes")
    lines.append(f"chunks       : {record['chunks']}")
    filters = record["filters"]
    lines.append(
        "filters      : compression={compression} opts={compression_opts} "
        "shuffle={shuffle} fletcher32={fletcher32} scaleoffset={scaleoffset}".format(**filters)
    )
    lines.append("")
    lines.append("scaling attributes")
    for key in sorted(record["scaling"]):
        lines.append(f"  {key:<12}: {record['scaling'][key]}")
    gains = record["channel_conversion"]
    if gains is None:
        lines.append("  channel_conversion: absent")
    else:
        lines.append(
            "  channel_conversion: n={n} distinct={distinct} "
            "min={min} max={max} unit={unit}".format(**gains)
        )
    lines.append("")
    lines.append("transfer plan per contiguous window")
    for plan in record["plans"]:
        lines.append(
            f"  {plan['window_s']:>4.1f} s -> {plan['window_samples']} samples, "
            f"{plan['band_channels']} band channels, layout {plan['layout']}"
        )
        if plan["layout"] == "chunked":
            lines.append(
                f"           chunk {plan['chunk_shape']} = {plan['chunk_stored_bytes']} B; "
                f"touches {plan['chunks_time']} x {plan['chunks_channel']} chunks"
            )
        lines.append(f"           stored bytes {plan['stored_bytes']} ({plan['basis']})")
    lines.append("")
    lines.append(
        f"io           : {record['io']['requests']} requests, {record['io']['bytes']} bytes"
    )
    lines.append("")
    lines.append("This probe reads dataset descriptions and the channel gain table only.")
    lines.append("No sample value was read, so no gate quantity is disclosed by it.")
    return "\n".join(lines) + "\n"


def parse_args(argv=None):
    """Parse command-line arguments.

    Args:
        argv: argument list, or None to read ``sys.argv``.

    Returns:
        The parsed namespace.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo-root", required=True,
                        help="path to the repository root")
    parser.add_argument("--session", required=True,
                        help="session UUID of the candidate host")
    parser.add_argument("--probe", required=True,
                        help="probe token, e.g. Probe01")
    parser.add_argument("--assets-cache", required=True,
                        help="path to the tracked DANDI asset listing")
    parser.add_argument("--out", required=True,
                        help="path to write the ASCII report to")
    parser.add_argument("--records", default=None,
                        help="optional path to write the JSON record to")
    parser.add_argument("--band-channels", type=int, default=72,
                        help="channels spanned by the pinned band, for sizing only")
    parser.add_argument("--block-kb", type=int, default=64,
                        help="HTTP range-request block size in kibibytes")
    return parser.parse_args(argv)


def main(argv=None):
    """Run the probe and write its report.

    Args:
        argv: argument list, or None to read ``sys.argv``.

    Returns:
        Process exit status: 0 on success.
    """
    args = parse_args(argv)
    add_packet_scripts(args.repo_root)
    from utils import dandi
    import measure_host_drift as drift

    assets = dandi.list_assets("000409", cache_path=args.assets_cache, verbose=False)
    raw, _processed = drift.resolve_assets(assets, args.session)
    url = dandi.blob_url(raw)
    print(f"[probe] reading layout metadata for {args.probe} of {args.session}")
    record = read_layout(url, int(raw["size"]), args.probe,
                         args.block_kb * 1024, args.band_channels)
    record["session"] = args.session
    record["probe"] = args.probe
    record["raw_asset_id"] = raw["asset_id"]
    record["raw_path"] = raw["path"]
    text = render(record, args.session, args.probe, raw["path"])
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    if args.records:
        with open(args.records, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(record, handle, indent=1, sort_keys=True)
            handle.write("\n")
    print(text, end="")
    print(f"[probe] wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
