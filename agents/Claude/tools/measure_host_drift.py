"""Measure one Tier A host candidate's band drift, and apply the pre-declared gate.

``utils.band_drift`` defines the statistic and ``utils.archive_units`` reads the
arrays; this is the command that puts a candidate through both and prints a
verdict. For one session, one probe and one pinned anatomical band it derives
the band from the raw file's electrode table, reads only that band's units out of
the processed file, confirms the four input properties the gate depends on,
computes the observed excursions and the deterministic permutation null, replays
that null to prove it reproduces, and applies the two-number pass rule at the
declared threshold.

**The threshold is a choice, so it is not a free number.** ``--gate`` selects
between the two values the project declared before any candidate was read --
``strict`` at one Neuropixels contact row and ``relaxed`` at the single
pre-authorized two-row fallback -- and no other value can be passed. A threshold
that could be typed is a threshold that could be chosen after the data is in.

**An input error is not a drift failure.** A malformed ragged index, a depth
column that no longer states its unit, an AP series without aligned timestamps,
a loaded spike outside the raw recording's interval, an electrode mapping that
crosses probes, or a raw/processed electrode-table disagreement all stop this
command with a non-zero status and no verdict. The candidate is not recorded as
having failed the gate, because the selection rule is first-admissible in a
fixed order and a rejection recorded for the wrong reason hands the host to the
next rank irrecoverably.

**Cost is counted before it is spent.** The ragged columns' index arrays are one
integer per unit, so the exact byte cost of the band's slices is known before a
single spike is read. ``--plan-only`` prints that number and stops;
``--max-mib`` refuses to exceed a declared ceiling. Both exist so that the
machine's free memory can be compared against a measurement rather than a guess.

Example
-------
Run from the ``Reproducibility Packet`` folder, which is the working directory
every command in ``README.md`` assumes; ``python`` means that folder's own
virtual environment, built in README's Setup section:

    python scripts/measure_host_drift.py --session b52182e7-39f6-4914-9717-136db589706e --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt

**This file is not in the packet's ``scripts/`` folder yet, and the command above
is not yet a numbered runbook step.** It becomes Step 11 of ``README.md`` when it
has actually been executed against a candidate and has produced the report that
step would claim -- a runbook step for a command nobody has run is a guess. The
module preamble below is the packet's standard one, so the move is a copy with
no edit: while the file lives outside ``scripts/``, its caller is responsible for
putting the packet's ``scripts/`` directory on ``sys.path``.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np  # noqa: E402

from screen_host_timing import read_series_timing  # noqa: E402
from utils import archive_units, band_drift, dandi  # noqa: E402
from utils.host_anatomy import contiguous_band, read_electrode_table  # noqa: E402

GATES = {"strict": "threshold_strict_um", "relaxed": "threshold_relaxed_um"}


def resolve_assets(assets, session):
    """Find the raw and processed assets belonging to one session.

    Args:
        assets: the asset listing from ``utils.dandi.list_assets``.
        session: the session UUID to resolve.

    Returns:
        A ``(raw, processed)`` pair of asset dicts.

    Raises:
        SystemExit: if either asset is missing or either is ambiguous. Both are
            reasons not to proceed rather than conditions to work around.
    """
    found = {"raw": [], "processed": []}
    for asset in assets:
        if dandi.session_of(asset) != session:
            continue
        if asset["path"].endswith(dandi.RAW_SUFFIX):
            found["raw"].append(asset)
        elif asset["path"].endswith(dandi.PROCESSED_SUFFIX):
            found["processed"].append(asset)
    for kind in ("raw", "processed"):
        if len(found[kind]) != 1:
            raise SystemExit(
                "[fatal] session %s resolves to %d %s assets, expected exactly one: %s"
                % (session, len(found[kind]), kind,
                   [a["path"] for a in found[kind]]))
    return found["raw"][0], found["processed"][0]


def select_ap_series(series, probe):
    """Pick the one AP acquisition series belonging to a probe.

    Args:
        series: the ``series`` list from ``screen_host_timing.read_series_timing``.
        probe: the probe name, e.g. ``"Probe01"``.

    Returns:
        The matching series entry.

    Raises:
        SystemExit: unless exactly one series carries the probe's name. Guessing
            which stream a probe's clock comes from is not an option here: the
            bin grid's extent is read from it.
    """
    matches = [entry for entry in series if probe in entry["name"]]
    if len(matches) != 1:
        raise SystemExit(
            "[fatal] %d AP series match probe %r, expected exactly one: %s"
            % (len(matches), probe, [entry["name"] for entry in series]))
    return matches[0]


def check_clock(entry, probe):
    """Confirm the raw AP series supplies the aligned session-time extent.

    Args:
        entry: the AP series entry from :func:`select_ap_series`.
        probe: the probe name, for the error message.

    Returns:
        A ``(t_first_s, t_last_s)`` pair.

    Raises:
        SystemExit: if the series carries no aligned timestamps or its endpoints
            are not finite and increasing. This validates the session clock
            declared in the selection document; it does not choose one.
    """
    if entry.get("timing_source") != "timestamps":
        raise SystemExit(
            "[fatal] probe %s's AP series carries timing_source %r rather than aligned "
            "timestamps; this is an input error, not a drift rejection"
            % (probe, entry.get("timing_source")))
    t_first = entry.get("t_first_s")
    t_last = entry.get("t_last_s")
    if t_first is None or t_last is None or not np.isfinite([t_first, t_last]).all():
        raise SystemExit(
            "[fatal] probe %s's AP timestamps do not give finite endpoints (%r, %r)"
            % (probe, t_first, t_last))
    if not t_last > t_first:
        raise SystemExit(
            "[fatal] probe %s's AP timestamps do not increase: t_first %r, t_last %r"
            % (probe, t_first, t_last))
    return float(t_first), float(t_last)


def check_containment(band_units, t_first_s, t_last_s):
    """Check every loaded spike falls inside the raw recording's interval.

    Containment is a consistency check and nothing more. It cannot identify an
    unknown clock offset or scale, because the loaded spikes need not reach
    either recording endpoint, so the two margins it leaves are reported beside
    the verdict rather than being read as a resolution.

    Args:
        band_units: the band units returned by ``archive_units.read_band_units``.
        t_first_s: the raw AP stream's first aligned timestamp.
        t_last_s: the raw AP stream's last aligned timestamp.

    Returns:
        A dict with ``earliest_spike_s``, ``latest_spike_s``, and the two
        endpoint-slack values, or None when the band carried no spike at all.

    Raises:
        SystemExit: if a loaded spike falls outside ``[t_first_s, t_last_s]``.
    """
    loaded = [unit for unit in band_units if unit["n_spikes"]]
    if not loaded:
        return None
    earliest = min(float(unit["times"][0]) for unit in loaded)
    latest = max(float(unit["times"][-1]) for unit in loaded)
    if earliest < t_first_s or latest > t_last_s:
        raise SystemExit(
            "[fatal] loaded spikes span [%.6f, %.6f] s, outside the raw AP interval "
            "[%.6f, %.6f] s; this is an input error, not a drift rejection"
            % (earliest, latest, t_first_s, t_last_s))
    return {
        "earliest_spike_s": earliest,
        "latest_spike_s": latest,
        "head_slack_s": earliest - t_first_s,
        "tail_slack_s": t_last_s - latest,
    }


def summarize_set(units):
    """Count a unit set and record every member's row and stored label.

    Args:
        units: unit dicts carrying ``row`` and ``label``.

    Returns:
        A dict with ``n_total``, ``n_good``, ``rows`` and ``labels``, so that a
        candidate's composition is auditable without the label ever having acted
        as a filter.
    """
    return {
        "n_total": len(units),
        "n_good": sum(1 for unit in units if unit["label"] == "good"),
        "rows": [unit["row"] for unit in units],
        "labels": [unit["label"] for unit in units],
    }


def replay_matches(first, second):
    """Compare two permutation nulls for exact reproduction.

    Args:
        first: a null dict from ``band_drift.permutation_null``.
        second: a second null built from identical inputs.

    Returns:
        True when every replicate value and the summary percentile match
        exactly. Anything less is a failed deterministic replay, which the
        declared parameters make an unmeasurable rejection rather than a pass.
    """
    return (first["values"] == second["values"]
            and first["q95"] == second["q95"]
            and first["rank"] == second["rank"])


def nearest_rank(values, percentile):
    """Take one nearest-rank percentile from an ascending list.

    The null's declared summary is a nearest-rank percentile, so every other
    percentile printed beside it uses the same rule. A second convention in the
    same block would invite a reader to compare two quantities that are not
    computed the same way.

    Args:
        values: the replicate values, ascending.
        percentile: the percentile to take, 0 to 100.

    Returns:
        The selected value.
    """
    if percentile <= 0:
        return values[0]
    rank = int(np.ceil(percentile / 100.0 * len(values)))
    return values[rank - 1]


def build_report(record):
    """Render the human-readable drift report.

    Args:
        record: the result record assembled by :func:`main`.

    Returns:
        A list of report lines, ASCII only.
    """
    lines = []
    add = lines.append
    add("# Tier A host drift measurement")
    add("")
    add("subject / session     %s / %s" % (record["subject"], record["session"]))
    add("probe                 %s" % record["probe"])
    add("raw asset             %s" % record["raw_asset_id"])
    add("processed asset       %s" % record["processed_asset_id"])
    add("target structure      %s (band contiguity gap %g um)" % (record["target"],
                                                                  record["max_gap_um"]))
    add("band (rel_y)          %.1f to %.1f um, %d rows, %d channels"
        % (record["band"]["depth_lo_um"], record["band"]["depth_hi_um"],
           record["band"]["n_rows"], record["band"]["n_channels"]))
    add("gate                  %s, L = %.1f um" % (record["gate"], record["threshold_um"]))
    add("numpy                 %s" % record["numpy_version"])
    add("archive transfer      %d bytes in %d requests, total across both assets"
        % (record["io"]["bytes"], record["io"]["requests"]))
    for source in ("raw_electrodes", "raw_timing", "processed_units"):
        add("  %-19s %d bytes in %d requests"
            % (source, record["io"][source]["bytes"], record["io"][source]["requests"]))
    add("")
    add("Every number below is measured from the two assets named above. The bin grid,")
    add("the inclusion rule, the permutation count, the master seed and the threshold")
    add("were all fixed before any candidate was read.")
    add("")

    add("## Input confirmations")
    add("")
    add("  ragged index alignment    %s" % record["checks"]["ragged_alignment"])
    add("  depth column unit         %s" % record["checks"]["depth_unit"])
    add("  electrode tables agree    %s" % record["checks"]["electrode_tables"])
    add("  AP timing source          %s" % record["checks"]["timing_source"])
    add("  spike containment         %s" % record["checks"]["containment"])
    add("")
    add("  spike_times description   %s" % record["descriptions"].get("spike_times"))
    add("  depth description         %s"
        % record["descriptions"].get("spike_distances_from_probe_tip_um"))
    for key in sorted(record["provenance"]):
        add("  provenance %-14s %s" % (key.split("/")[-1][:14], record["provenance"][key]))
    add("")
    add("  The session-time origin is pinned to the conversion repository commit named in")
    add("  the selection document, not inferred here. Containment is a consistency check:")
    add("  it cannot identify a clock offset or scale, and the two slack values below are")
    add("  what it leaves unchecked at the endpoints, not a bound on internal agreement.")
    add("")

    clock = record["clock"]
    add("## Clock, grid and coverage")
    add("")
    add("  t_first_s                 %.9f" % clock["t_first_s"])
    add("  t_last_s (grid extent)    %.9f" % clock["t_last_s"])
    add("  n_bins                    %d full-width 60 s bins from session zero"
        % record["grid"]["n_bins"])
    add("  discarded_s               %.6f (final underlength interval)"
        % record["grid"]["discarded_s"])
    add("  head_partial_s            %.9f (bin 0's clock time before AP coverage begins)"
        % record["grid"]["head_partial_s"])
    add("  spikes before origin      %d (excluded by the binning itself)"
        % record["grid"]["n_spikes_before_origin"])
    if record["containment"]:
        add("  earliest loaded spike     %.9f s" % record["containment"]["earliest_spike_s"])
        add("  latest loaded spike       %.9f s" % record["containment"]["latest_spike_s"])
        add("  head endpoint slack       %.9f s" % record["containment"]["head_slack_s"])
        add("  tail endpoint slack       %.9f s" % record["containment"]["tail_slack_s"])
    add("")

    add("## Unit sets")
    add("")
    in_band = record["sets"]["in_band"]
    included = record["sets"]["included"]
    add("  units in the file         %d" % record["n_units_total"])
    add("  units on probe            %d" % record["n_units_on_probe"])
    add("  in the band               %d total, %d labelled 'good'"
        % (in_band["n_total"], in_band["n_good"]))
    add("  surviving inclusion       %d total, %d labelled 'good'"
        % (included["n_total"], included["n_good"]))
    add("  spikes read               %d in %d slices, %d bytes"
        % (record["plan"]["n_spikes"], record["plan"]["n_units"], record["plan"]["bytes"]))
    add("")
    add("  The band set is selected by valid same-probe max_electrode -> rel_y inside the")
    add("  band and is blind to kilosort2_label. The labels are recorded so composition is")
    add("  auditable; no label filtered anything.")
    add("")
    add("  in-band rows and labels:")
    for row, label in zip(in_band["rows"], in_band["labels"]):
        add("    %6d  %s" % (row, label or "<none>"))
    add("")
    add("  included rows and labels:")
    for row, label in zip(included["rows"], included["labels"]):
        add("    %6d  %s" % (row, label or "<none>"))
    add("")

    observed = record["observed"]
    add("## Observed band excursions")
    add("")
    if not observed.get("measurable"):
        add("  measurable                no")
        add("  reason                    %s" % observed.get("reason"))
    else:
        add("  Delta_full                %.3f um" % observed["delta_full"])
        add("  Delta_10min               %.3f um (11-bin window starting at bin %d)"
            % (observed["delta_window"], observed["window_start"]))
        add("  min units per bin         %d" % observed["min_units_per_bin_observed"])
        add("  invalid bins              %d" % len(observed["invalid_bins"]))
    add("")

    null = record["null"]
    if null:
        add("## Permutation null")
        add("")
        add("  permutations              %d" % null["n_permutations"])
        add("  Q95_null                  %.3f um (nearest-rank, one-based rank %d)"
            % (null["q95"], null["rank"]))
        add("  null range                %.3f to %.3f um"
            % (null["values"][0], null["values"][-1]))
        add("  null deciles              %s um"
            % " ".join("%.3f" % nearest_rank(null["values"], step * 10)
                       for step in range(11)))
        add("  (nearest rank at 0, 10, ... 100; the full replicate list is in --records)")
        add("  deterministic replay      %s" % record["checks"]["replay"])
        add("")

    verdict = record["verdict"]
    add("## Verdict")
    add("")
    add("  passed                    %s" % verdict["passed"])
    add("  label                     %s" % verdict["label"])
    add("  reason                    %s" % verdict["reason"])
    add("")

    audit = record["audit"]
    if audit:
        add("## Per-unit audit values (reported, never consumed)")
        add("")
        add("  No verdict, label or ordering reads these. They carry no null of their own,")
        add("  and Q95_null grades the across-unit band trace rather than any single unit,")
        add("  so comparing a value below against Q95_null or against L is undefined in")
        add("  either direction. An absence of magnitude separation licenses nothing.")
        add("")
        add("    %6s %10s %10s %8s %8s %10s %8s"
            % ("row", "whole", "own_worst", "start", "bins", "band_win", "bins"))
        for entry in audit:
            add("    %6d %10.3f %10.3f %8d %8d %10s %8s"
                % (entry["row"], entry["delta_full"], entry["delta_max_window"],
                   entry["max_window_start"], entry["max_window_defined_bins"],
                   ("%.3f" % entry["delta_band_window"])
                   if entry["delta_band_window"] is not None else "undef",
                   entry["band_window_defined_bins"]
                   if entry["band_window_defined_bins"] is not None else "-"))
        add("")

    add("## Boundaries on this measurement")
    add("")
    add("  - This measures drift as visible in IBL's per-spike centre-of-mass depths, not")
    add("    physical probe displacement, and it does not separate probe movement from")
    add("    tissue movement.")
    add("  - The gate holds at the bin grid's 60-second resolution. It neither bounds")
    add("    sub-minute motion nor is reliably blind to it; how much of a brief episode")
    add("    reaches a bin median depends on the within-bin depth distribution and on")
    add("    where the episode falls on the minute grid.")
    add("  - The result is conditional on the pre-declared label-blind unit set and on")
    add("    movement being expressed in enough of those depth traces for the across-unit")
    add("    median to carry it. The per-unit values above do not discharge that")
    add("    conditional in either direction.")
    add("  - Q95_null is a conservative resolution diagnostic where the additive")
    add("    common-movement picture is credible, not a proved bound on the no-drift")
    add("    noise floor, and it bounds no systematic bias in the depth estimator.")
    add("")
    return lines


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--session", required=True,
                        help="session UUID of the candidate host recording")
    parser.add_argument("--probe", required=True,
                        help="probe name exactly as stored, e.g. Probe01")
    parser.add_argument("--target", required=True,
                        help="target structure acronym whose band is measured, e.g. CA1")
    parser.add_argument("--assets-cache", required=True,
                        help="JSON asset listing, used to resolve blob URLs and sizes")
    parser.add_argument("--out", required=True, help="path of the report to write")
    parser.add_argument("--records", default=None,
                        help="optional path for the raw JSON record")
    parser.add_argument("--gate", choices=sorted(GATES), default="strict",
                        help="which pre-declared threshold to apply (default: strict)")
    parser.add_argument("--dandiset", default="000409", help="dandiset identifier")
    parser.add_argument("--version", default="draft", help="dandiset version")
    parser.add_argument("--max-gap-um", type=float, default=40.0,
                        help="band contiguity tolerance; must match the anatomy survey's")
    parser.add_argument("--block-kb", type=int, default=1024,
                        help="HTTP range block size in KiB")
    parser.add_argument("--max-mib", type=float, default=1024.0,
                        help="refuse to transfer more than this many MiB of spike data")
    parser.add_argument("--plan-only", action="store_true",
                        help="report the exact byte cost of the band's slices and stop")
    args = parser.parse_args(argv)
    if args.block_kb <= 0:
        raise SystemExit("[fatal] --block-kb must be positive")
    if args.max_mib <= 0:
        raise SystemExit("[fatal] --max-mib must be positive")
    return args


def main(argv=None):
    """Measure one candidate's band drift and write the report."""
    args = parse_args(argv)
    threshold_um = band_drift.PARAMS[GATES[args.gate]]

    assets = dandi.list_assets(args.dandiset, args.version, cache_path=args.assets_cache)
    raw_asset, processed_asset = resolve_assets(assets, args.session)
    subject = dandi.subject_of(raw_asset)
    block_bytes = args.block_kb * 1024
    print("[drift] %s %s session %s" % (subject, args.probe, args.session), flush=True)

    raw = read_electrode_table(dandi.blob_url(raw_asset), raw_asset["size"], block_bytes)
    if args.probe not in raw["probes"]:
        raise SystemExit("[fatal] raw electrode table has no probe %r; it has %s"
                         % (args.probe, sorted(raw["probes"])))
    raw_probe_rows = raw["probes"][args.probe]
    band = contiguous_band(raw_probe_rows, args.target, args.max_gap_um)
    if band is None:
        raise SystemExit("[fatal] probe %s carries no %s band; this candidate should not "
                         "have reached the drift gate" % (args.probe, args.target))
    print("[drift] band %.1f-%.1f um, %d channels"
          % (band["depth_lo_um"], band["depth_hi_um"], band["n_channels"]), flush=True)

    timing = read_series_timing(dandi.blob_url(raw_asset), raw_asset["size"], block_bytes, 2)
    series = select_ap_series(timing["series"], args.probe)
    t_first_s, t_last_s = check_clock(series, args.probe)
    print("[drift] AP extent t_first %.6f s, t_last %.6f s" % (t_first_s, t_last_s), flush=True)

    try:
        read = archive_units.read_band_units(
            dandi.blob_url(processed_asset), processed_asset["size"], block_bytes,
            args.probe, band["depth_lo_um"], band["depth_hi_um"],
            max_bytes=int(args.max_mib * 1024 * 1024), plan_only=args.plan_only)
    except ValueError as exc:
        # Every ValueError this reader raises is a statement about the asset,
        # not about drift. Converting it here keeps the two apart in the exit
        # status and in the operator's transcript. A ValueError from the
        # estimator further down is deliberately left to raise: that would be a
        # bug in code this project owns, and a traceback is the right report.
        raise SystemExit("[fatal] input error reading %s probe %s: %s"
                         % (processed_asset["path"], args.probe, exc))
    plan = read["plan"]
    print("[drift] %d band units of %d on the probe; %d spikes, %d bytes to read"
          % (plan["n_units"], read["n_units_on_probe"], plan["n_spikes"], plan["bytes"]),
          flush=True)
    if args.plan_only:
        print("[drift] --plan-only: nothing else was read and no verdict was computed",
              flush=True)
        return 0

    agreement = archive_units.electrode_tables_agree(raw_probe_rows, read["electrodes"],
                                                     args.probe)
    if not agreement["agree"]:
        raise SystemExit(
            "[fatal] the raw and processed electrode tables disagree for probe %s (%s); the "
            "band comes from one and max_electrode indexes the other, so this is an input "
            "error, not a drift rejection" % (args.probe, agreement["detail"]))

    band_units = read["band_units"]
    containment = check_containment(band_units, t_first_s, t_last_s)
    n_bins, discarded_s = band_drift.complete_bins(t_last_s)
    n_before_origin = int(sum(int((unit["times"] < 0.0).sum()) for unit in band_units))

    observed = band_drift.measure_band_drift(
        [unit["times"] for unit in band_units],
        [unit["depths"] for unit in band_units],
        t_last_s)

    null = None
    replay_note = "not reached"
    if observed.get("measurable"):
        rows = [unit["row"] for unit in band_units]
        null = band_drift.permutation_null(
            [unit["times"] for unit in band_units],
            [unit["depths"] for unit in band_units],
            t_last_s, processed_asset["asset_id"], args.probe, rows)
        second = band_drift.permutation_null(
            [unit["times"] for unit in band_units],
            [unit["depths"] for unit in band_units],
            t_last_s, processed_asset["asset_id"], args.probe, rows)
        if replay_matches(null, second):
            replay_note = "identical over %d replicates" % null["n_permutations"]
        else:
            replay_note = "FAILED - the null did not reproduce"
            observed = dict(observed)
            observed["measurable"] = False
            observed["reason"] = ("the permutation null did not reproduce byte for byte on "
                                  "replay, so the result is unmeasurable")
            null = None

    verdict = band_drift.apply_gate(observed, null, threshold_um)

    included_rows = [band_units[i] for i in observed.get("included", [])]
    audit = []
    for position, unit in enumerate(included_rows):
        if not observed.get("measurable"):
            break
        audit.append({
            "row": unit["row"],
            "label": unit["label"],
            "delta_full": observed["unit_delta_full"][position],
            "delta_max_window": observed["unit_delta_max_window"][position],
            "max_window_start": observed["unit_max_window_start"][position],
            "max_window_defined_bins": observed["unit_max_window_defined_bins"][position],
            "delta_band_window": observed["unit_delta_band_window"][position],
            "band_window_defined_bins": observed["unit_band_window_defined_bins"][position],
        })

    io_total = {
        "raw_electrodes": raw["io"],
        "raw_timing": timing["io"],
        "processed_units": read["io"],
        "bytes": raw["io"]["bytes"] + timing["io"]["bytes"] + read["io"]["bytes"],
        "requests": (raw["io"]["requests"] + timing["io"]["requests"]
                     + read["io"]["requests"]),
    }

    record = {
        "subject": subject,
        "session": args.session,
        "probe": args.probe,
        "target": args.target,
        "max_gap_um": args.max_gap_um,
        "raw_asset_id": raw_asset["asset_id"],
        "processed_asset_id": processed_asset["asset_id"],
        "band": band,
        "gate": args.gate,
        "threshold_um": threshold_um,
        "numpy_version": np.__version__,
        "io": io_total,
        "plan": {key: plan[key] for key in ("n_units", "n_spikes", "bytes")},
        "descriptions": read["descriptions"],
        "provenance": read["provenance"],
        "n_units_on_probe": read["n_units_on_probe"],
        "n_units_total": read["n_units_total"],
        "clock": {"t_first_s": t_first_s, "t_last_s": t_last_s},
        "grid": {
            "n_bins": n_bins,
            "discarded_s": discarded_s,
            "head_partial_s": max(t_first_s, 0.0),
            "n_spikes_before_origin": n_before_origin,
        },
        "containment": containment,
        "checks": {
            "ragged_alignment": "identical partitions over %d units" % read["n_units_total"],
            "depth_unit": "description states %r" % archive_units.DEPTH_UNIT_PHRASE,
            "electrode_tables": agreement["detail"],
            "timing_source": series.get("timing_source"),
            "containment": ("all loaded spikes inside [t_first_s, t_last_s]"
                            if containment else "no spikes loaded"),
            "replay": replay_note,
        },
        "sets": {
            "in_band": summarize_set(band_units),
            "included": summarize_set(included_rows),
        },
        "observed": observed,
        "null": null,
        "verdict": verdict,
        "audit": audit,
    }

    lines = build_report(record)
    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print("[drift] wrote %s" % args.out, flush=True)
    print("[drift] verdict: passed=%s label=%s" % (verdict["passed"], verdict["label"]),
          flush=True)

    if args.records:
        with open(args.records, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(record, handle, indent=1, sort_keys=True)
        print("[drift] wrote %s" % args.records, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
