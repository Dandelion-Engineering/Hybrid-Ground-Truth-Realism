"""Measure how many band spikes carry non-finite depths, and where they sit.

`measure_host_drift.py` stops with an input error the moment any band unit
carries a non-finite value in ``spike_distances_from_probe_tip_um``. The first
real candidate read hit that condition, so this probe answers the question the
error message does not: how many units and how many spikes are affected, whether
the spike *times* are affected as well, whether the values are NaN or infinite,
and what the affected spikes would do to the 60-second bin occupancy the drift
estimator depends on.

**This probe rules on nothing.** It reads the same band the command reads and
reports what is there. Whether a non-finite depth is an input error that pauses
a candidate, a per-spike exclusion the estimator should absorb, or something
else is a disposition question that belongs to the review, not to the session
that found it.

It is deliberately read-only and computes no drift statistic.

Example
-------
Run from the project root with the project virtual environment::

    ./venv/Scripts/python.exe agents/Claude/tools/probe_nonfinite_depths.py \
        --repo-root . --session b52182e7-39f6-4914-9717-136db589706e \
        --probe Probe01 --target CA1 \
        --out agents/Claude/tools/nonfinite_depths_CSHL047_Probe01.txt \
        --records agents/Claude/tools/nonfinite_depths_CSHL047_Probe01.json
"""

import argparse
import importlib.util
import io
import json
import os
import sys

import numpy as np


def load_command(scripts_dir):
    """Import the packet's drift command and its utils under that scripts dir."""
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location(
        "measure_host_drift_probe", os.path.join(scripts_dir, "measure_host_drift.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bin_of(times, bin_seconds):
    """Return the 60-second session-grid bin index of each spike time."""
    return np.floor(np.asarray(times, dtype=np.float64) / bin_seconds).astype(np.int64)


def parse_args(argv=None):
    """Parse the probe's command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True,
                        help="project root; the packet is found beneath it")
    parser.add_argument("--session", required=True)
    parser.add_argument("--probe", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--assets-cache", default=None,
                        help="defaults to the packet's results/dandi_000409_assets.json")
    parser.add_argument("--out", required=True)
    parser.add_argument("--records", required=True)
    parser.add_argument("--block-kb", type=int, default=1024)
    parser.add_argument("--dandiset", default="000409")
    parser.add_argument("--version", default="draft")
    return parser.parse_args(argv)


def main(argv=None):
    """Read one candidate's band and report every non-finite value in it."""
    args = parse_args(argv)
    root = os.path.abspath(args.repo_root)
    packet = os.path.join(root, "Reproducibility Packet")
    scripts_dir = os.path.join(packet, "scripts")
    command = load_command(scripts_dir)
    archive_units = command.archive_units
    dandi = command.dandi
    band_drift = command.band_drift
    import h5py  # noqa: E402  (imported here so the packet's utils set the path first)

    cache = args.assets_cache or os.path.join(packet, "results",
                                              "dandi_000409_assets.json")
    assets = dandi.list_assets(args.dandiset, args.version, cache_path=cache)
    raw_asset, processed_asset = command.resolve_assets(assets, args.session)
    subject = dandi.subject_of(raw_asset)
    block_bytes = args.block_kb * 1024
    print("[probe] %s %s session %s" % (subject, args.probe, args.session), flush=True)

    raw = command.read_electrode_table(
        dandi.blob_url(raw_asset), raw_asset["size"], block_bytes)
    band = command.contiguous_band(raw["probes"][args.probe], args.target,
                                   command.BAND_MAX_GAP_UM)
    if band is None:
        raise SystemExit("[fatal] probe %s carries no %s band" % (args.probe, args.target))
    print("[probe] band %.1f-%.1f um, %d channels"
          % (band["depth_lo_um"], band["depth_hi_um"], band["n_channels"]), flush=True)

    timing = command.read_series_timing(
        dandi.blob_url(raw_asset), raw_asset["size"], block_bytes, 2)
    series = command.select_ap_series(timing["series"], args.probe)
    t_first_s, t_last_s = command.check_clock(series, args.probe)
    n_bins, discarded_s = band_drift.complete_bins(t_last_s)
    print("[probe] AP extent t_first %.6f s, t_last %.6f s; %d complete 60 s bins"
          % (t_first_s, t_last_s, n_bins), flush=True)

    url = dandi.blob_url(processed_asset)
    remote = archive_units.RemoteFile(url, processed_asset["size"], block=block_bytes)
    reader = archive_units.BoundedReader(remote)
    units = []
    with h5py.File(reader, "r") as handle:
        electrodes = archive_units.read_flat_electrodes(handle)
        scalars = archive_units.read_unit_scalars(handle)
        archive_units.check_ragged_alignment(scalars)
        unit_electrodes = archive_units.resolve_unit_electrodes(
            scalars, electrodes, args.probe)
        band_units = archive_units.select_band_units(
            unit_electrodes, band["depth_lo_um"], band["depth_hi_um"])
        slices = archive_units.band_slices(band_units, scalars["times_index"])
        node = handle[archive_units.UNITS_PATH]
        times_dataset = node[archive_units.TIME_COLUMN]
        depths_dataset = node[archive_units.DEPTH_COLUMN]
        print("[probe] %d band units of %d on the probe; reading both ragged columns"
              % (len(band_units), len(unit_electrodes)), flush=True)
        for unit, (lo, hi) in zip(band_units, slices):
            times = np.asarray(times_dataset[lo:hi], dtype=np.float64)
            depths = np.asarray(depths_dataset[lo:hi], dtype=np.float64)
            bad_depth = ~np.isfinite(depths)
            bad_time = ~np.isfinite(times)
            record = {
                "row": int(unit["row"]),
                "n_spikes": int(times.size),
                "n_nonfinite_depths": int(bad_depth.sum()),
                "n_nonfinite_times": int(bad_time.sum()),
                "n_nan_depths": int(np.isnan(depths).sum()),
                "n_posinf_depths": int(np.isposinf(depths).sum()),
                "n_neginf_depths": int(np.isneginf(depths).sum()),
                "label": unit.get("label"),
                "rel_y_um": float(unit["rel_y_um"]),
            }
            if record["n_nonfinite_depths"]:
                where = np.flatnonzero(bad_depth)
                record["nonfinite_depth_indices"] = [int(i) for i in where]
                record["nonfinite_depth_times_s"] = [
                    (float(times[i]) if np.isfinite(times[i]) else None) for i in where]
                record["nonfinite_depth_bins"] = [
                    (int(np.floor(times[i] / band_drift.PARAMS["bin_seconds"]))
                     if np.isfinite(times[i]) else None) for i in where]
            # What dropping the non-finite depths would cost this unit's bins.
            # Both counts are taken so the cost is a measurement rather than an
            # argument: "kept" drops the non-finite samples, "all" keeps every
            # spike whose time is usable. A spike with a NaN depth still has a
            # valid time, so the two differ only where a dropped sample was
            # holding a bin at the inclusion floor.
            grid_end = n_bins * band_drift.PARAMS["bin_seconds"]
            on_grid = np.isfinite(times) & (times >= 0.0) & (times < grid_end)
            floor = band_drift.PARAMS["min_spikes_per_bin"]
            for key, mask in (("all", on_grid),
                              ("kept", on_grid & np.isfinite(depths))):
                if mask.any():
                    bins = bin_of(times[mask], band_drift.PARAMS["bin_seconds"])
                    counts = np.bincount(bins, minlength=n_bins)[:n_bins]
                    record["n_bins_at_or_above_floor_%s" % key] = int(
                        (counts >= floor).sum())
                else:
                    record["n_bins_at_or_above_floor_%s" % key] = 0
            record["n_bins_at_or_above_floor"] = record["n_bins_at_or_above_floor_kept"]
            record["support_lost_by_dropping"] = (
                record["n_bins_at_or_above_floor_all"]
                - record["n_bins_at_or_above_floor_kept"])
            units.append(record)

    affected = [u for u in units if u["n_nonfinite_depths"] or u["n_nonfinite_times"]]
    total_spikes = sum(u["n_spikes"] for u in units)
    total_bad_depths = sum(u["n_nonfinite_depths"] for u in units)
    total_bad_times = sum(u["n_nonfinite_times"] for u in units)
    floor_bins = band_drift.PARAMS["min_bin_fraction"] * n_bins
    included = [u for u in units
                if u["n_bins_at_or_above_floor_kept"] >= floor_bins]
    included_all = [u for u in units
                    if u["n_bins_at_or_above_floor_all"] >= floor_bins]

    summary = {
        "session": args.session,
        "subject": subject,
        "probe": args.probe,
        "target": args.target,
        "band_depth_lo_um": float(band["depth_lo_um"]),
        "band_depth_hi_um": float(band["depth_hi_um"]),
        "band_channels": int(band["n_channels"]),
        "t_first_s": float(t_first_s),
        "t_last_s": float(t_last_s),
        "n_bins": int(n_bins),
        "discarded_tail_s": float(discarded_s),
        "n_band_units": len(units),
        "n_units_on_probe": len(unit_electrodes),
        "n_band_spikes": int(total_spikes),
        "n_units_with_nonfinite_depths": sum(1 for u in units if u["n_nonfinite_depths"]),
        "n_units_with_nonfinite_times": sum(1 for u in units if u["n_nonfinite_times"]),
        "n_nonfinite_depths": int(total_bad_depths),
        "n_nonfinite_times": int(total_bad_times),
        "n_units_meeting_support_keeping_everything": len(included_all),
        "n_units_meeting_support_after_dropping": len(included),
        "n_units_that_lose_any_bin_by_dropping": sum(
            1 for u in units if u["support_lost_by_dropping"]),
        "n_bins_lost_by_dropping": sum(u["support_lost_by_dropping"] for u in units),
        "io_requests": int(remote.n_requests),
        "io_bytes": int(remote.n_bytes),
    }

    lines = []
    lines.append("Non-finite spike depths in the drift band")
    lines.append("=========================================")
    lines.append("")
    lines.append("This is a diagnostic read. It computes no drift statistic and")
    lines.append("decides nothing about the candidate.")
    lines.append("")
    for key in ("session", "subject", "probe", "target", "band_depth_lo_um",
                "band_depth_hi_um", "band_channels", "t_first_s", "t_last_s",
                "n_bins", "discarded_tail_s", "n_band_units", "n_units_on_probe",
                "n_band_spikes", "n_units_with_nonfinite_depths",
                "n_units_with_nonfinite_times", "n_nonfinite_depths",
                "n_nonfinite_times", "n_units_meeting_support_keeping_everything",
                "n_units_meeting_support_after_dropping",
                "n_units_that_lose_any_bin_by_dropping", "n_bins_lost_by_dropping",
                "io_requests", "io_bytes"):
        lines.append("%-40s %s" % (key, summary[key]))
    lines.append("")
    lines.append("Affected units")
    lines.append("--------------")
    if not affected:
        lines.append("none")
    for unit in affected:
        lines.append(
            "row %-6d spikes %-9d non-finite depths %-4d (nan %d, +inf %d, -inf %d) "
            "non-finite times %-4d rel_y %.1f um label %s"
            % (unit["row"], unit["n_spikes"], unit["n_nonfinite_depths"],
               unit["n_nan_depths"], unit["n_posinf_depths"], unit["n_neginf_depths"],
               unit["n_nonfinite_times"], unit["rel_y_um"],
               archive_units.ascii_safe(str(unit["label"]), 20)))
        lines.append("    indices %r" % (unit.get("nonfinite_depth_indices"),))
        lines.append("    spike times s %r" % (unit.get("nonfinite_depth_times_s"),))
        lines.append("    60 s bins %r" % (unit.get("nonfinite_depth_bins"),))
    lines.append("")

    text = "\n".join(lines) + "\n"
    with io.open(os.path.join(root, args.out), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with io.open(os.path.join(root, args.records), "w", encoding="utf-8", newline="\n") as handle:
        json.dump({"summary": summary, "units": units}, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(text, end="")
    print("[probe] wrote %s and %s" % (args.out, args.records), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
