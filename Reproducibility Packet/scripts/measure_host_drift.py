"""Measure one Tier A host candidate's band drift, and apply the pre-declared gate.

``utils.band_drift`` defines the statistic and ``utils.archive_units`` reads the
arrays; this is the command that puts a candidate through both and prints a
verdict. For one session, one probe and one pinned anatomical band it derives
the band from the raw file's electrode table, reads only that band's units out of
the processed file, confirms the four input properties the gate depends on,
computes the observed excursions and the deterministic permutation null, replays
that null to prove it reproduces, and applies the two-number pass rule at the
declared threshold.

**No number that decides a verdict can be typed on the command line.**
``--gate`` selects between the two values the project declared before any
candidate was read -- ``strict`` at one Neuropixels contact row and ``relaxed``
at the single pre-authorized two-row fallback -- and no other value can be
passed. The band's anatomical contiguity tolerance is pinned here too, at the
40 um the selection document's section 4 uses to define a contiguous band: a wider
tolerance merges separate islands of the target label across intervening
structure, which changes which units are measured and so changes the verdict
just as directly as the threshold does. A number that could be typed is a number
that could be chosen after the data is in.

**An input error is not a drift failure.** A malformed ragged index, a
structural column that is not integral as stored, a depth column that no longer
states its unit, a raw and a processed asset that are not the same subject's
same session, an AP series without aligned timestamps or with fewer timestamps
than samples, a loaded spike outside the raw recording's interval, an electrode
mapping that crosses probes, or a raw/processed electrode-table disagreement all
stop this command with a non-zero status and no verdict. The candidate is not
recorded as having failed the gate, because the selection rule is
first-admissible in a fixed order and a rejection recorded for the wrong reason
hands the host to the next rank irrecoverably.

**A missing depth is neither an input error nor a silent exclusion.** The
archive's depth column is a waveform centre of mass, and a degenerate weight sum
leaves NaN in it; on the two candidates censused so far the pattern is all-NaN,
never infinite, and never in the times. Such a spike still carries a perfectly
good time, so the reader returns the record complete with a positional mask, and
this command does three things with it rather than one. It publishes the
exclusions **per unit, per bin and in total**. It bounds, through
``utils.missing_depth``, what every completion of those missing values could have
done to **both** of the gate's numbers -- the observed excursion and the
permutation null. And it refuses to let the observed verdict stand when that
bound straddles the threshold: the candidate is reported unmeasurable and stays
paused rather than being passed on the strength of a point estimate. An
*infinite* depth remains an input error, because widening a bound around a
corrupt number would turn corruption into uncertainty. **The last line this
command prints is that reconciled decision**, and the gate's own pass/fail is
printed above it marked as a diagnostic: the two can disagree, and a reader or a
script that acts on the final line must not be able to advance a candidate the
reconciliation has paused. **The layer engages only
when something is actually missing**, since with nothing missing its bounds
collapse onto the gate's own two numbers and computing them again would double
the most expensive step of the run to reproduce values already in hand.

**Cost is sized before it is spent, in the units it is actually paid in.**
The ragged columns' index arrays are one integer per unit, so the band's slices
are known before a single spike is read. ``--plan-only`` prints the stored
payload, an upper bound on the block transfer, the converted arrays -- including
the one-byte-per-spike positional mask the reader retains beside them -- and one
combined peak-resident bound, then stops; ``--max-mib`` refuses the read when
that combined bound exceeds it. The combined one is the number to compare
against free RAM, because the range reader's block cache is not released while
the arrays it fed are being accumulated -- the parts are live together, and a
ceiling that checked them one at a time admitted a read that needed their sum.
All of that exists so the machine's free memory can be compared against a
measurement rather than against a guess.

**What the ceiling covers, said here rather than left to be discovered.** It
covers the processed asset's read, and every read that read performs is inside
its plan: the electrode table, the unit scalars, the column descriptions, the
conversion provenance, the column layouts and the chunk index are all read while
the reader's spend is still being counted, and the per-unit slices after the
check are what the plan sizes. **It also covers the raw asset's provenance and
clock read**, which is held inside the same declared ceiling from before its
file is opened: that read fetches half of the pair condition, and a read the
caller's ceiling does not cover is the defect class the ceiling exists to
close. It does **not** cover the other two reads on the *raw* asset -- one
electrode table, and two timestamps from each end of each AP series. Those are
bounded by construction rather than by a ceiling: neither grows with the
recording's length or its spike count. The provenance read is bounded twice
more inside the ceiling by ``utils.archive_units`` -- once on what it may ask
for and once on the distinct bytes its reader may fetch, which are different
quantities whenever the reader fetches in blocks. Every read's actual cost is
measured and reported, under ``raw_electrodes``, ``raw_timing`` and
``raw_provenance``, and each provenance read reports both of its own budgets
beside what it spent, so the transcript states all four costs rather than only
the ones the ceiling governs.

**Both assets are authenticated before anything is measured, and the two have
to declare the same session-time origin.** The bin grid is anchored on that
origin, and the raw file supplies the extent while the processed file supplies
the spikes. Each asset's ``general/source_script`` must *be* the conversion
statement every measured asset of this dandiset carries -- matched end to end,
because searching it for the tool's name admitted a value that denied it -- and
each asset's root ``timestamps_reference_time`` must be a timezone-aware
ISO-8601 instant, which NWB defines as the point every stored time in that file
is counted from. An asset that carries neither, one this command could not read
whole, one that states something else, one whose reference time names no UTC
offset, and a pair whose two instants differ are all input errors that stop the
run. Recording provenance is not confirming it, and a file with no provenance at
all used to reach a verdict.

**The pair check used to compare converter versions and it admitted nothing.**
Measured across 71 sessions of this dandiset, every raw asset was written by
NeuroConv 0.9.1 or 0.9.2 and every processed asset by 0.9.4 -- agreement 0 of
71, so no candidate could have passed. The declared reference instants agree on
63 of the same 71 and differ by exactly one hour on 8, and those 8 carry the
same version pair as the 63. The versions are still parsed and still reported;
they no longer decide anything. **Agreeing instants are a necessary declared
condition and not an identification of the clock** -- the same limit the
selection document already states for endpoint containment.

Example
-------
Run from the ``Reproducibility Packet`` folder, which is the working directory
every command in ``README.md`` assumes; ``python`` means that folder's own
virtual environment, built in README's Setup section:

    python scripts/measure_host_drift.py --session b52182e7-39f6-4914-9717-136db589706e --probe Probe01 --target CA1 --assets-cache results/dandi_000409_assets.json --gate strict --out results/host_drift_CSHL047_Probe01.txt

**The command above is not a numbered runbook step yet.** It becomes one when it
has actually been executed against a candidate and has produced the report that
step would claim -- a runbook step for a command nobody has run is a guess, and
``results/`` holds nothing it produced. It lives here rather than outside the
packet because the first real result must be generated by a script the packet
already contains, and because a command a reader cannot run directly is not a
reproducible command. ``check_runbook_consistency.py`` knows it is here without a
step and says so; the exemption ends with the first execution.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np  # noqa: E402

from screen_host_timing import read_series_timing  # noqa: E402
from utils import archive_units, band_drift, dandi, missing_depth  # noqa: E402
from utils.host_anatomy import contiguous_band, read_electrode_table  # noqa: E402

GATES = {"strict": "threshold_strict_um", "relaxed": "threshold_relaxed_um"}

# The anatomical contiguity tolerance, pinned rather than typed. Section 4 of
# the selection document defines a contiguous band as successive contact rows no
# more than two Neuropixels 1.0 rows apart, and every candidate in the pinned
# order was found under that definition. Supplying a different one here would
# redefine which units the gate measures after the candidates are known.
BAND_MAX_GAP_UM = 40.0

# How an acquisition series names the probe it belongs to. Substring matching
# was the previous rule and it is not ownership: asked for ``Probe00``, a file
# holding ``ElectricalSeriesProbe000AP`` and ``ElectricalSeriesProbe01AP``
# selected the first and took a different probe's clock. The name is decomposed
# instead, and the probe token has to match exactly. The thirteen candidate
# assets in the pinned order carry exactly two series names between them --
# ``ElectricalSeriesProbe00AP`` and ``ElectricalSeriesProbe01AP``, from
# ``results/host_timing_index.jsonl`` -- so this decomposition is checked
# against every asset the order can reach rather than against a guess about the
# converter.
#
# **What it authenticates is the name.** A series whose name and contents
# disagree -- one labelled for this probe but carrying another's channels -- is
# not caught here, and closing that would mean resolving each series'
# ``electrodes`` region in ``screen_host_timing.read_series_timing``, which is
# outside this command and has already produced a recorded index. It is named
# rather than left implied.
SERIES_NAME = re.compile(r"^ElectricalSeries(?P<probe>.+?)(?P<band>AP|LF)$")


def resolve_assets(assets, session):
    """Find the raw and processed assets belonging to one session.

    Args:
        assets: the asset listing from ``utils.dandi.list_assets``.
        session: the session UUID to resolve.

    Returns:
        A ``(raw, processed)`` pair of asset dicts.

    Raises:
        SystemExit: if either asset is missing or either is ambiguous, or if the
            two do not name the same subject and the same paired file stem. The
            session UUID alone does not establish that two assets are one
            recording: the band, the clock and the electrode table are taken
            from the raw file while the units are taken from the processed one,
            so a mismatched pair would measure two recordings as if they were
            one and report it under whichever subject the raw file named.
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
    raw, processed = found["raw"][0], found["processed"][0]
    subjects = (dandi.subject_of(raw), dandi.subject_of(processed))
    if subjects[0] is None or subjects[1] is None or subjects[0] != subjects[1]:
        raise SystemExit(
            "[fatal] session %s pairs %r (subject %r) with %r (subject %r); a raw and a "
            "processed asset must be the same subject's recording, and this is an input "
            "error rather than a drift rejection"
            % (session, raw["path"], subjects[0], processed["path"], subjects[1]))
    stems = (raw["path"][:-len(dandi.RAW_SUFFIX)],
             processed["path"][:-len(dandi.PROCESSED_SUFFIX)])
    if stems[0] != stems[1]:
        raise SystemExit(
            "[fatal] session %s pairs paths whose stems differ: %r and %r; the two assets "
            "are not the same recording's raw and processed halves, and this is an input "
            "error rather than a drift rejection" % (session, stems[0], stems[1]))
    return raw, processed


def series_probe(name):
    """Return the probe token an acquisition series name claims, or None.

    Args:
        name: the series name as stored in the file's acquisition group.

    Returns:
        The probe token, or None when the name does not decompose. A name that
        does not decompose owns no probe here: it is reported with the others so
        an unexpected naming convention is diagnosable rather than silent.
    """
    match = SERIES_NAME.match(name)
    return match.group("probe") if match else None


def select_ap_series(series, probe):
    """Pick the one AP acquisition series belonging to a probe.

    Args:
        series: the ``series`` list from ``screen_host_timing.read_series_timing``.
        probe: the probe name, e.g. ``"Probe01"``.

    Returns:
        The matching series entry.

    Raises:
        SystemExit: unless exactly one series decomposes to exactly this probe.
            Guessing which stream a probe's clock comes from is not an option
            here: the bin grid's extent is read from it, and a stream whose name
            merely *contains* the probe token belongs to a different probe.

    Note:
        The live failure is zero matches. Two matches cannot arise from one
        acquisition group, because the decomposition is injective on the name
        and HDF5 names within a group are unique; the ``!= 1`` form is a guard
        against a caller assembling the list some other way, not a second check
        with a reachable fixture.
    """
    matches = [entry for entry in series if series_probe(entry["name"]) == probe]
    if len(matches) != 1:
        raise SystemExit(
            "[fatal] %d AP series belong to probe %r, expected exactly one; the file's AP "
            "series decompose as %s. A series whose name only contains the probe token is a "
            "different stream and cannot supply this probe's clock, so this is an input "
            "error, not a drift rejection"
            % (len(matches), probe,
               [(entry["name"], series_probe(entry["name"])) for entry in series]))
    return matches[0]


def check_clock(entry, probe):
    """Confirm the raw AP series supplies the aligned session-time extent.

    Args:
        entry: the AP series entry from :func:`select_ap_series`.
        probe: the probe name, for the error message.

    Returns:
        A ``(t_first_s, t_last_s)`` pair.

    Raises:
        SystemExit: if the series carries no aligned timestamps, if it carries
            fewer or more timestamps than the data array has samples, or if its
            endpoints are not finite and increasing. This validates the session
            clock declared in the selection document; it does not choose one.
    """
    if entry.get("timing_source") != "timestamps":
        raise SystemExit(
            "[fatal] probe %s's AP series carries timing_source %r rather than aligned "
            "timestamps; this is an input error, not a drift rejection"
            % (probe, entry.get("timing_source")))
    n_timestamps = entry.get("n_timestamps")
    shape = entry.get("shape") or []
    n_samples = shape[0] if shape else None
    if n_timestamps is None or n_samples is None or int(n_timestamps) != int(n_samples):
        # t_last_s is the last timestamp, and it is the grid's whole extent. If
        # the timestamp vector does not cover the data it is aligning, the last
        # timestamp is not the recording's last sample time and the extent is a
        # different quantity from the one the grid is defined on.
        raise SystemExit(
            "[fatal] probe %s's AP series has %r samples but %r aligned timestamps; the "
            "last timestamp is the grid's extent, so a timestamp vector that does not "
            "cover the data is an input error, not a drift rejection"
            % (probe, n_samples, n_timestamps))
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


def summarize_missing(band_units, sensitivity, null_bounds, stability, n_spikes):
    """Assemble the missing-depth record, JSON-safe and aggregated three ways.

    The exclusions are published per unit, per bin and in total, because a total
    alone hides whether 200 missing depths are one unit's whole recording or two
    hundred units' single spikes, and those two admit very different bounds. The
    per-unit and per-bin tables are aggregates of the same ``(unit, bin, count)``
    triples the layer produces, and those triples are carried through whole so
    the aggregation can be audited against what it aggregated.

    Args:
        band_units: the band units, each carrying ``row``, ``label`` and
            ``n_missing_depths``.
        sensitivity: the dict from
            ``utils.missing_depth.measure_missing_depth_sensitivity``, or None
            when nothing was missing and the layer was not run.
        null_bounds: the dict from ``utils.missing_depth.null_interval``, or None.
        stability: the dict from ``utils.missing_depth.stability_verdict``, or None.
        n_spikes: the number of spikes loaded, for the fraction.

    Returns:
        A dict carrying the counts, the three aggregations, the support-invariance
        summary, the bounds and the completion disposition. Numpy values are
        converted, because this record is written as JSON.
    """
    n_missing = int(sum(unit["n_missing_depths"] for unit in band_units))
    record = {
        "n_missing": n_missing,
        "n_spikes": int(n_spikes),
        "fraction_percent": (100.0 * n_missing / n_spikes) if n_spikes else 0.0,
        "n_units_in_band": len(band_units),
        "n_units_affected": sum(1 for unit in band_units if unit["n_missing_depths"]),
        "outside_grid": 0,
        "per_unit": [],
        "per_bin": [],
        "per_unit_bin": [],
        "support": None,
        "bounds": None,
        "null_bounds": None,
        "stability": None,
    }
    if sensitivity is None:
        return record

    exclusions = sensitivity["exclusions"]
    record["outside_grid"] = int(exclusions["outside_grid"])
    record["per_unit_bin"] = [[int(band_units[u]["row"]), int(b), int(n)]
                              for u, b, n in exclusions["per_unit_bin"]]
    bins_per_unit = {}
    per_bin = {}
    for u, b, n in exclusions["per_unit_bin"]:
        bins_per_unit[u] = bins_per_unit.get(u, 0) + 1
        counts, units = per_bin.get(b, (0, 0))
        per_bin[b] = (counts + n, units + 1)
    record["per_unit"] = [
        {"row": int(unit["row"]), "label": unit["label"],
         "n_missing": int(unit["n_missing_depths"]),
         "n_bins": int(bins_per_unit.get(u, 0))}
        for u, unit in enumerate(band_units) if unit["n_missing_depths"]]
    record["per_bin"] = [{"bin": int(b), "n_missing": int(per_bin[b][0]),
                          "n_units": int(per_bin[b][1])}
                         for b in sorted(per_bin)]

    support = sensitivity["support"]
    record["support"] = {
        "invariant": bool(support["invariant"]),
        "reason": support.get("reason"),
        "n_included": int(support["included"].sum()),
        "n_included_complete": int(support["included_complete"].sum()),
        "n_bin_mismatches": len(support["bin_mismatches"]),
        "bin_mismatches": [[int(u), int(b)] for u, b in support["bin_mismatches"]],
        "min_units_per_bin": int(support["units_per_bin"].min()),
        "min_units_per_bin_complete": int(support["units_per_bin_complete"].min()),
    }
    record["bounds"] = {key: sensitivity[key] for key in
                        ("measurable", "reason", "bounded", "delta_full_lo",
                         "delta_full_hi", "delta_window_lo", "delta_window_hi",
                         "window_start_hi", "lo_trace", "hi_trace")
                        if key in sensitivity}
    record["null_bounds"] = null_bounds
    record["stability"] = stability
    return record


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


def reconcile_verdict(verdict, stability):
    """Reconcile the gate's verdict on the record held with the completion bound.

    The approved gate reads the record the archive supplied. When depths were
    missing, ``utils.missing_depth`` bounds what every completion of them could
    have made those same two numbers do, and both statements have to point the
    same way before a candidate advances or is rejected.

    They can point opposite ways, and the reason is worth stating where the rule
    is: the finite-only null permutes the observed spikes while every completion
    permutes all of them, so the finite-only ``Q95_null`` is not one of the
    completions and can sit on the other side of the threshold from the whole
    bound. A disagreement is not resolved in favour of either side. It is
    precisely the state in which the record held does not determine the verdict,
    which is what unmeasurable means here, and the candidate keeps its rank.

    No tolerance is fitted anywhere in this rule and nothing in it is typeable.

    Args:
        verdict: the dict from ``band_drift.apply_gate``.
        stability: the dict from ``utils.missing_depth.stability_verdict``, or
            None when no depth was missing.

    Returns:
        A dict with ``disposition`` (``"passes"``, ``"fails"`` or
        ``"unmeasurable"``), ``advances`` (True only on ``"passes"``),
        ``conflict`` (True only when the two statements point opposite ways) and
        ``reason``.
    """
    passed = bool(verdict["passed"])
    if stability is None:
        return {
            "disposition": "passes" if passed else "fails",
            "advances": passed,
            "conflict": False,
            "reason": "no depth was missing, so the gate's two numbers are the only ones "
                      "any completion of this record could have produced",
        }
    disposition = stability["disposition"]
    if disposition in ("passes", "fails"):
        if (disposition == "passes") == passed:
            return {
                "disposition": disposition,
                "advances": passed,
                "conflict": False,
                "reason": stability["reason"],
            }
        return {
            "disposition": "unmeasurable",
            "advances": False,
            "conflict": True,
            "reason": "the gate %s on the record held while every completion of the "
                      "missing depths %s it; the finite-only null is not one of those "
                      "completions, so the record held does not determine the verdict "
                      "(%s)"
                      % ("passed" if passed else "failed",
                         "passes" if disposition == "passes" else "fails",
                         stability["reason"]),
        }
    return {
        "disposition": "unmeasurable",
        "advances": False,
        "conflict": False,
        "reason": stability["reason"],
    }


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
    add("target structure      %s (band contiguity gap pinned at %g um)"
        % (record["target"], record["max_gap_um"]))
    add("band (rel_y)          %.1f to %.1f um, %d rows, %d channels"
        % (record["band"]["depth_lo_um"], record["band"]["depth_hi_um"],
           record["band"]["n_rows"], record["band"]["n_channels"]))
    add("gate                  %s, L = %.1f um" % (record["gate"], record["threshold_um"]))
    add("numpy                 %s" % record["numpy_version"])
    add("archive transfer      %d bytes in %d requests, total across both assets"
        % (record["io"]["bytes"], record["io"]["requests"]))
    for source in ("raw_provenance", "raw_electrodes", "raw_timing", "processed_units"):
        add("  %-19s %d bytes in %d requests"
            % (source, record["io"][source]["bytes"], record["io"][source]["requests"]))
    add("provenance budgets    stated before the read, not measured after it")
    for label in ("raw", "processed"):
        spend = record["provenance_io"][label]
        # The transfer budget is denominated in blocks, so the block size is
        # part of the number and is printed with it. A reader that fetches
        # exactly what it is asked for has no block size, and printing "0-byte
        # block" for that would read as a measurement rather than as its
        # absence.
        basis = ("at a %d-byte block" % spend["block_bytes"] if spend["block_bytes"]
                 else "through a reader that fetches exactly what it is asked for")
        add("  %-19s %d of %d bytes requested, %d of %d distinct bytes transferred %s"
            % (label, spend["read_bytes"], spend["read_budget_bytes"],
               spend["transfer_bytes"], spend["transfer_budget_bytes"], basis))
    add("")
    add("Every number below is measured from the two assets named above. The bin grid,")
    add("the inclusion rule, the permutation count, the master seed and the threshold")
    add("were all fixed before any candidate was read.")
    add("")

    add("## Input confirmations")
    add("")
    add("  ragged index alignment    %s" % record["checks"]["ragged_alignment"])
    add("  structural columns        %s" % record["checks"]["integer_columns"])
    add("  depth column unit         %s" % record["checks"]["depth_unit"])
    add("  electrode tables agree    %s" % record["checks"]["electrode_tables"])
    add("  asset pair identity       %s" % record["checks"]["asset_pair"])
    add("  conversion provenance     %s" % record["checks"]["conversion_provenance"])
    add("  session reference time    %s" % record["checks"]["reference_time"])
    add("  AP timing source          %s" % record["checks"]["timing_source"])
    add("  AP timestamp coverage     %s" % record["checks"]["timestamp_coverage"])
    add("  spike containment         %s" % record["checks"]["containment"])
    add("")
    add("  spike_times description   %s" % record["descriptions"].get("spike_times"))
    add("  depth description         %s"
        % record["descriptions"].get("spike_distances_from_probe_tip_um"))
    # The key is printed whole. Clipping it to a fixed width rendered
    # general/source_script and general/source_script@file_name as the same
    # nine characters, so two different values sat under one label and the
    # reader could not tell which was which.
    for label, source in (("processed", "provenance"), ("raw", "raw_provenance")):
        add("  %s asset provenance" % label)
        for key in sorted(record[source]):
            add("    %-32s %s"
                % (key, archive_units.ascii_safe(record[source][key], 160)))
    add("")
    add("  Provenance values are rendered ASCII-only and clipped at 160 characters here;")
    add("  the records file carries each value exactly as this command holds it, which is")
    add("  the file's value for a path read whole and a self-describing refusal or")
    add("  truncation marker for one the budgets declined. Only the required")
    add("  general/source_script and timestamps_reference_time are necessarily complete on")
    add("  a verdict, because no verdict is reached without either. The conversion")
    add("  provenance check above matches each asset's whole value against the measured")
    add("  conversion statement; it does not confirm the repository commit, because no")
    add("  asset in this dandiset carries one, and the session-time origin is pinned to")
    add("  that commit in the selection document rather than inferred here. The two")
    add("  converter versions are reported and gate nothing: requiring them to be equal")
    add("  admitted 0 of the 71 sessions of this dandiset that were measured, because")
    add("  every raw half was written by one version and every processed half by another.")
    add("  The reference-time check is what replaced it. It is a necessary declared")
    add("  condition and NOT an identification of the clock: two assets can declare the")
    add("  same origin and still have been written under different internal conventions,")
    add("  so it stands beside the pinned converter semantics and the containment check")
    add("  rather than in place of them. On the same 71 sessions the two declared instants")
    add("  agreed on 63 and differed by exactly one hour on 8.")
    add("  Containment is a consistency check: it cannot identify a clock offset or scale,")
    add("  and the two slack values below are what it leaves unchecked at the endpoints,")
    add("  not a bound on internal agreement.")
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
    plan = record["plan"]
    add("  spikes read               %d in %d slices" % (plan["n_spikes"], plan["n_units"]))
    add("  stored payload            %d bytes (exact)" % plan["logical_bytes"])
    add("  block transfer            at most %d bytes over %d KiB blocks, by %s"
        % (plan["cache_bound_bytes"], plan["block_bytes"] // 1024, plan["bound_basis"]))
    add("  peak resident arrays      %d bytes (the converted arrays and the %d bytes"
        % (plan["resident_bytes"], plan["mask_bytes"]))
    add("                            of missing-depth masks retained beside them)")
    add("  live python structures    %d bytes (measured)" % plan["structures_bytes"])
    add("  hdf5 chunk cache          %d bytes (the library's own ceiling; 0 when neither"
        % plan["library_cache_bytes"])
    add("                            ragged column is chunked)")
    add("  combined peak resident    at most %d bytes -- the ceiling is enforced on this"
        % plan["peak_resident_bytes"])
    add("")
    add("  Those are different questions and only the last is a memory figure to compare")
    add("  against free RAM: the range reader's block cache is not released while the")
    add("  arrays it fed accumulate, so the memory terms are live together and the")
    add("  ceiling is enforced on their sum. Its declared scope is this read's own")
    add("  footprint -- block cache, arrays, structures, HDF5 chunk cache -- and not the")
    add("  interpreter baseline, allocator overhead or transient h5py allocations outside")
    add("  a chunk cache.")
    add("")
    add("  The transfer figure bounds the processed-units read alone -- the line to compare")
    add("  it against is processed_units above, not the total -- and it bounds the distinct")
    add("  block bytes a range reader fetches, including what that read had already spent")
    add("  on metadata before the band was known. A retried range request re-fetches its")
    add("  block and is outside it, so processed_units can exceed the bound by the retries.")
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
        add("  (nearest rank at 0, 10, ... 100; the full replicate list is %s)"
            % ("in the JSON record written beside this report" if record["records_written"]
               else "not written, because --records was not given"))
        add("  deterministic replay      %s" % record["checks"]["replay"])
        add("")

    missing = record["missing_depth"]
    add("## Missing depths and the completion bound")
    add("")
    add("  missing depths            %d of %d loaded spikes (%.6f%%)"
        % (missing["n_missing"], missing["n_spikes"], missing["fraction_percent"]))
    add("  units affected            %d of %d in the band"
        % (missing["n_units_affected"], missing["n_units_in_band"]))
    add("  outside the bin grid      %d (before session zero, or past the last complete bin)"
        % missing["outside_grid"])
    if not missing["n_missing"]:
        add("")
        add("  Nothing was missing, so the sensitivity layer was not run. Every bound it")
        add("  would have produced collapses onto the gate's own two numbers when no depth")
        add("  is missing, and the harness proves that collapse is elementwise exact.")
        add("")
    else:
        support = missing["support"]
        add("  support invariance        %s"
            % ("holds: every unit and every bin has the same inclusion status whether the "
               "missing samples are counted or not" if support["invariant"]
               else "VIOLATED - %s" % support["reason"]))
        add("  included units            %d counting finite depths only, %d counting the "
            "missing ones too"
            % (support["n_included"], support["n_included_complete"]))
        bounds = missing["bounds"]
        if not bounds.get("measurable"):
            add("  bounds                    not computed: %s" % bounds.get("reason"))
        else:
            observed = record["observed"]
            add("  Delta_10min bound         %.3f to %.3f um (the point estimate is %.3f)"
                % (bounds["delta_window_lo"], bounds["delta_window_hi"],
                   observed["delta_window"]))
            add("  Delta_full bound          %.3f to %.3f um (the point estimate is %.3f)"
                % (bounds["delta_full_lo"], bounds["delta_full_hi"],
                   observed["delta_full"]))
            if missing["null_bounds"]:
                null_bounds = missing["null_bounds"]
                add("  Q95_null bound            %.3f to %.3f um over %d replicates "
                    "(nearest-rank, one-based rank %d)"
                    % (null_bounds["q95_lo"], null_bounds["q95_hi"],
                       null_bounds["n_permutations"], null_bounds["rank"]))
                add("  both bounds finite        %s"
                    % (bounds["bounded"] and null_bounds["bounded"]))
        stability = missing["stability"]
        add("  completion disposition    %s" % stability["disposition"])
        add("  reason                    %s" % stability["reason"])
        add("")
        add("  per-unit exclusions (only units with a missing depth appear):")
        add("    %6s %8s %10s %8s" % ("row", "label", "n_missing", "bins"))
        for entry in missing["per_unit"]:
            add("    %6d %8s %10d %8d"
                % (entry["row"], entry["label"] or "<none>", entry["n_missing"],
                   entry["n_bins"]))
        add("")
        add("  per-bin exclusions (only bins holding a missing depth appear):")
        add("    %6s %10s %8s" % ("bin", "n_missing", "units"))
        for entry in missing["per_bin"]:
            add("    %6d %10d %8d" % (entry["bin"], entry["n_missing"], entry["n_units"]))
        add("")
        add("  The (unit, bin, count) triples these two tables aggregate are in the JSON")
        add("  record when --records was given; %s."
            % ("it was" if record["records_written"] else "it was not"))
        add("")
        add("  How to read the bound, including where it is not exact:")
        add("  - Per bin it is the attainable set, not an approximation of one: a median is")
        add("    nondecreasing in every argument, so driving the missing values below every")
        add("    observed depth minimises it and above every observed depth maximises it.")
        add("  - Above the bin it is an OUTER bound. The same missing values enter a bin")
        add("    median and the per-unit centring constant subtracted from it, and interval")
        add("    arithmetic ignores that dependence. The error runs one way: too wide,")
        add("    never too narrow. This layer can call a candidate unmeasurable that a")
        add("    dependence-aware treatment would have called stable; it cannot pass one")
        add("    that some completion would have failed.")
        add("  - The Q95_null bound is assumption-free. The approved null's permutation is")
        add("    drawn from a seed and from the analysed-bin SPIKE count, and a spike whose")
        add("    depth is missing still has a good time, so both are fixed before any")
        add("    missing value is chosen and the unknown values sit in known positions.")
        add("  - The finite-only Q95_null printed above is NOT one of those completions when")
        add("    anything is missing: it permutes the observed spikes where every")
        add("    completion permutes all of them. It is the number the gate itself reads,")
        add("    and it is not claimed to lie inside the bound.")
        add("  - An unbounded side is reported as unbounded and makes the candidate")
        add("    unmeasurable. No completion places a value at infinity; what an unbounded")
        add("    side asserts is that every finite value on it is attainable.")
        add("")

    verdict = record["verdict"]
    reconciled = record["disposition"]
    add("## Verdict")
    add("")
    add("  passed                    %s" % verdict["passed"])
    add("  label                     %s" % verdict["label"])
    add("  reason                    %s" % verdict["reason"])
    add("")
    add("  The three lines above are the approved gate applied to the record the archive")
    add("  supplied. The lines below reconcile that with what the missing depths could")
    add("  have changed; on a candidate with no missing depth they say the same thing.")
    add("")
    add("  final disposition         %s" % reconciled["disposition"])
    add("  advances                  %s" % reconciled["advances"])
    add("  gate and bound conflict   %s" % reconciled["conflict"])
    add("  reason                    %s" % reconciled["reason"])
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


def clear_outputs(paths):
    """Delete this run's declared output files before the run begins.

    A run that stops on an input error writes nothing, which would otherwise
    leave an earlier run's report and record sitting at exactly the paths this
    one named. The non-zero exit distinguishes them, but the files do not, and a
    verdict file that belongs to a different run is the kind of artifact that
    gets read later without its exit status. Clearing them first means an
    artifact at these paths always belongs to the run that most recently used
    them.

    Args:
        paths: output paths, some of which may be None.

    Raises:
        SystemExit: if an existing path cannot be removed, which would leave the
            same ambiguity the clearing exists to remove.
    """
    for path in paths:
        if not path or not os.path.exists(path):
            continue
        try:
            os.remove(path)
        except OSError as exc:
            raise SystemExit("[fatal] could not clear the earlier %s: %s" % (path, exc))


def same_output_path(first, second):
    """Decide whether two output arguments name one file on this filesystem.

    Comparing ``abspath`` strings is not enough. Windows filesystems are
    normally case-insensitive, so ``Verdict.txt`` and ``verdict.txt`` are one
    file there and two distinct strings everywhere; a symbolic link or a
    junction is the same problem by another route. Either way the second write
    would silently destroy the first, which is exactly the collision the guard
    exists to prevent.

    Args:
        first: one output path.
        second: the other.

    Returns:
        True if the two paths resolve to the same file. ``os.path.samefile``
        decides it when both already exist, because it asks the filesystem
        rather than guessing at its rules; otherwise the paths are compared
        after resolving links and normalizing case, which is a no-op on
        case-sensitive filesystems and so does not merge two real files there.
    """
    if os.path.exists(first) and os.path.exists(second):
        try:
            return os.path.samefile(first, second)
        except OSError:
            pass
    return (os.path.normcase(os.path.realpath(first))
            == os.path.normcase(os.path.realpath(second)))


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
    parser.add_argument("--block-kb", type=int, default=1024,
                        help="HTTP range block size in KiB")
    parser.add_argument("--max-mib", type=float, default=1024.0,
                        help="refuse the processed asset's read if its combined peak "
                             "resident bound -- block cache, converted arrays, live "
                             "structures and HDF5's own chunk cache together -- exceeds "
                             "this many MiB. It is also held open as a transfer budget "
                             "around the raw asset's provenance and clock read, which "
                             "happens first, so a ceiling below the cost of opening that "
                             "file refuses before any of its bytes move. The raw "
                             "electrode-table and timing reads are bounded by "
                             "construction, not by this ceiling, and every read's cost "
                             "is reported separately")
    parser.add_argument("--plan-only", action="store_true",
                        help="report what the band's slices would cost, and stop")
    args = parser.parse_args(argv)
    if args.block_kb <= 0:
        raise SystemExit("[fatal] --block-kb must be positive")
    if not np.isfinite(args.max_mib) or args.max_mib <= 0:
        raise SystemExit("[fatal] --max-mib must be positive and finite")
    if args.records and same_output_path(args.records, args.out):
        raise SystemExit(
            "[fatal] --out %r and --records %r name the same path on this filesystem; the "
            "report and the JSON record are two different artifacts and one would "
            "overwrite the other" % (args.out, args.records))
    return args


def main(argv=None):
    """Measure one candidate's band drift and write the report."""
    args = parse_args(argv)
    threshold_um = band_drift.PARAMS[GATES[args.gate]]
    clear_outputs((args.out, args.records))

    assets = dandi.list_assets(args.dandiset, args.version, cache_path=args.assets_cache)
    raw_asset, processed_asset = resolve_assets(assets, args.session)
    subject = dandi.subject_of(raw_asset)
    block_bytes = args.block_kb * 1024
    print("[drift] %s %s session %s" % (subject, args.probe, args.session), flush=True)

    # The declared ceiling is passed here, not only to the processed read.
    # RC-004-F2: this read fetches the raw half of the pair condition, and it
    # used to move its bytes outside the ceiling the caller declared.
    try:
        raw_prov = archive_units.read_provenance(
            dandi.blob_url(raw_asset), raw_asset["size"], block_bytes,
            max_bytes=int(args.max_mib * 1024 * 1024))
    except ValueError as exc:
        raise SystemExit("[fatal] input error reading %s: %s"
                         % (raw_asset["path"], exc))
    try:
        raw_auth = archive_units.authenticate_provenance(
            raw_prov["provenance"], "raw asset %s" % raw_asset["path"])
    except ValueError as exc:
        raise SystemExit("[fatal] input error: %s" % exc)
    print("[drift] raw asset counts its times from %s"
          % archive_units.ascii_safe(raw_auth["reference_value"], 60), flush=True)
    print("[drift] raw conversion provenance %s (version %s), read under a %d-byte "
          "request budget and a %d-byte transfer budget, spending %d and %d"
          % (archive_units.ascii_safe(raw_auth["value"], 120), raw_auth["version"],
             raw_prov["provenance_io"]["read_budget_bytes"],
             raw_prov["provenance_io"]["transfer_budget_bytes"],
             raw_prov["provenance_io"]["read_bytes"],
             raw_prov["provenance_io"]["transfer_bytes"]), flush=True)

    raw = read_electrode_table(dandi.blob_url(raw_asset), raw_asset["size"], block_bytes)
    if args.probe not in raw["probes"]:
        raise SystemExit("[fatal] raw electrode table has no probe %r; it has %s"
                         % (args.probe, sorted(raw["probes"])))
    raw_probe_rows = raw["probes"][args.probe]
    band = contiguous_band(raw_probe_rows, args.target, BAND_MAX_GAP_UM)
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
            max_bytes=int(args.max_mib * 1024 * 1024), plan_only=args.plan_only,
            expect_conversion=raw_auth)
    except ValueError as exc:
        # Every ValueError this reader raises is a statement about the asset,
        # not about drift. Converting it here keeps the two apart in the exit
        # status and in the operator's transcript. A ValueError from the
        # estimator further down is deliberately left to raise: that would be a
        # bug in code this project owns, and a traceback is the right report.
        raise SystemExit("[fatal] input error reading %s probe %s: %s"
                         % (processed_asset["path"], args.probe, exc))
    plan = read["plan"]
    print("[drift] %d band units of %d on the probe; %d spikes"
          % (plan["n_units"], read["n_units_on_probe"], plan["n_spikes"]), flush=True)
    print("[drift] payload %d bytes; transfer bounded at %d bytes (%s); combined peak "
          "resident at most %d bytes (%d arrays, of which %d are the retained missing-depth "
          "masks, + %d structures + %d hdf5 cache + the block cache)"
          % (plan["logical_bytes"], plan["cache_bound_bytes"], plan["bound_basis"],
             plan["peak_resident_bytes"], plan["resident_bytes"], plan["mask_bytes"],
             plan["structures_bytes"], plan["library_cache_bytes"]), flush=True)
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

    rows = [unit["row"] for unit in band_units]
    complete_times = [unit["times"] for unit in band_units]
    complete_depths = [unit["depths"] for unit in band_units]
    n_missing_total = int(sum(unit["n_missing_depths"] for unit in band_units))

    # The record is split exactly once, here, by the one function that owns the
    # split. The approved estimator and the approved null take the observed
    # depths and raise on a non-finite value; the sensitivity layer takes the
    # complete record, because its null bound reads the missing samples'
    # positions and two spikes can share a time. A ValueError from split_unit is
    # left to raise rather than converted: the reader has already refused every
    # infinite depth and every non-finite time, so reaching one here would be a
    # bug in this project's code and a traceback is the right report.
    observed_times, observed_depths = [], []
    for unit in band_units:
        unit_times, unit_depths, _ = missing_depth.split_unit(unit["times"], unit["depths"])
        observed_times.append(unit_times)
        observed_depths.append(unit_depths)

    observed = band_drift.measure_band_drift(observed_times, observed_depths, t_last_s)

    null = None
    replay_note = "not reached"
    if observed.get("measurable"):
        null = band_drift.permutation_null(
            observed_times, observed_depths,
            t_last_s, processed_asset["asset_id"], args.probe, rows)
        second = band_drift.permutation_null(
            observed_times, observed_depths,
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

    sensitivity, null_bounds, stability = None, None, None
    if n_missing_total:
        print("[drift] %d of %d loaded depths are missing; bounding both gate numbers "
              "over every completion" % (n_missing_total, plan["n_spikes"]), flush=True)
        sensitivity = missing_depth.measure_missing_depth_sensitivity(
            complete_times, complete_depths, t_last_s)
        # Two cross-checks, because this layer holds its own copy of the record
        # and its own accounting of what is missing. The first ties the reader's
        # positional mask to the layer's exclusion table; the second ties the
        # layer's internal split to the split this command handed the gate. Both
        # are equalities and neither is a tolerance.
        counted = sensitivity["exclusions"]["total"]
        if counted != n_missing_total:
            raise SystemExit(
                "[fatal] the reader masked %d missing depths and the sensitivity layer "
                "accounted for %d; one of the two is not reading the record this command "
                "holds" % (n_missing_total, counted))
        layer_observed = sensitivity["observed"]
        for key in ("measurable", "delta_full", "delta_window", "window_start"):
            if layer_observed.get(key) != observed.get(key):
                raise SystemExit(
                    "[fatal] the sensitivity layer's observation disagrees with the gate's "
                    "on %r: %r against %r" % (key, layer_observed.get(key),
                                              observed.get(key)))
        if list(layer_observed.get("included", [])) != list(observed.get("included", [])):
            raise SystemExit(
                "[fatal] the sensitivity layer included a different unit set than the gate")
        if sensitivity.get("measurable"):
            null_bounds = missing_depth.null_interval(
                complete_times, complete_depths, t_last_s,
                processed_asset["asset_id"], args.probe, rows)
        stability = missing_depth.stability_verdict(sensitivity, null_bounds, threshold_um)
        print("[drift] completion disposition: %s" % stability["disposition"], flush=True)

    reconciled = reconcile_verdict(verdict, stability)
    missing_record = summarize_missing(band_units, sensitivity, null_bounds, stability,
                                       plan["n_spikes"])

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
        "raw_provenance": raw_prov["io"],
        "raw_electrodes": raw["io"],
        "raw_timing": timing["io"],
        "processed_units": read["io"],
        "bytes": (raw_prov["io"]["bytes"] + raw["io"]["bytes"] + timing["io"]["bytes"]
                  + read["io"]["bytes"]),
        "requests": (raw_prov["io"]["requests"] + raw["io"]["requests"]
                     + timing["io"]["requests"] + read["io"]["requests"]),
    }

    record = {
        "subject": subject,
        "session": args.session,
        "probe": args.probe,
        "target": args.target,
        "max_gap_um": BAND_MAX_GAP_UM,
        "raw_asset_id": raw_asset["asset_id"],
        "processed_asset_id": processed_asset["asset_id"],
        "band": band,
        "gate": args.gate,
        "threshold_um": threshold_um,
        "records_written": bool(args.records),
        "numpy_version": np.__version__,
        "io": io_total,
        "plan": {key: plan[key] for key in
                 ("n_units", "n_spikes", "logical_bytes", "cache_bound_bytes",
                  "resident_bytes", "mask_bytes", "structures_bytes",
                  "library_cache_bytes", "peak_resident_bytes",
                  "bound_basis", "block_bytes", "spent_bytes",
                  "time_layout", "depth_layout")},
        "descriptions": read["descriptions"],
        "integer_dtypes": read["integer_dtypes"],
        "provenance": read["provenance"],
        "raw_provenance": raw_prov["provenance"],
        "provenance_authentication": {
            "raw": archive_units.provenance_record(raw_auth),
            "processed": archive_units.provenance_record(
                read["provenance_authentication"]),
            # The instants necessarily agree, because a disagreement stops the
            # run before this record exists. That half is recorded as a
            # statement of what was enforced, not as a check this record could
            # have failed. ``versions_agree`` is the opposite: it is measured
            # and reported, it gates nothing, and on every session of this
            # dandiset read so far it is False.
            "pair": read["provenance_pair"],
        },
        "provenance_io": {"raw": raw_prov["provenance_io"],
                          "processed": read["provenance_io"]},
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
            "integer_columns": ("integral as stored: %s"
                                % ", ".join("%s %s" % (name, dtype) for name, dtype
                                            in sorted(read["integer_dtypes"].items()))),
            "depth_unit": "description states %r" % archive_units.DEPTH_UNIT_PHRASE,
            "electrode_tables": agreement["detail"],
            "asset_pair": ("one subject %s, one stem %s"
                           % (subject, raw_asset["path"][:-len(dandi.RAW_SUFFIX)])),
            "timing_source": series.get("timing_source"),
            "timestamp_coverage": ("%d timestamps for %d samples"
                                   % (series.get("n_timestamps"), series.get("shape")[0])),
            "containment": ("all loaded spikes inside [t_first_s, t_last_s]"
                            if containment else "no spikes loaded"),
            "conversion_provenance": (
                "both assets' %s match %r; raw names version %s, processed names %s "
                "(%s, and version equality is reported rather than gated); raw %r, "
                "processed %r"
                % (archive_units.REQUIRED_PROVENANCE_PATH,
                   archive_units.CONVERSION_SOURCE_FORM_TEXT,
                   read["provenance_pair"]["raw_version"],
                   read["provenance_pair"]["processed_version"],
                   "both among the versions measured across 71 sessions"
                   if read["provenance_pair"]["versions_are_measured"]
                   else "at least one outside the versions measured across 71 sessions",
                   archive_units.ascii_safe(raw_auth["value"], 60),
                   archive_units.ascii_safe(
                       read["provenance_authentication"]["value"], 60))),
            "reference_time": (
                "both assets state %s as the instant their time values are counted "
                "from; raw declares %r, processed declares %r, and the two denote the "
                "same instant to the microsecond"
                % (read["provenance_pair"]["reference_instant_utc"],
                   archive_units.ascii_safe(raw_auth["reference_value"], 60),
                   archive_units.ascii_safe(
                       read["provenance_authentication"]["reference_value"], 60))),
            "replay": replay_note,
        },
        "sets": {
            "in_band": summarize_set(band_units),
            "included": summarize_set(included_rows),
        },
        "observed": observed,
        "null": null,
        "verdict": verdict,
        "missing_depth": missing_record,
        "disposition": reconciled,
        "audit": audit,
    }

    lines = build_report(record)
    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print("[drift] wrote %s" % args.out, flush=True)

    if args.records:
        with open(args.records, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(record, handle, indent=1, sort_keys=True)
        print("[drift] wrote %s" % args.records, flush=True)

    # The point gate reads the record the archive supplied; the disposition
    # below reads it together with what every completion of the missing depths
    # could have done to it, and only the second decides whether this candidate
    # advances. The two can disagree, so the diagnostic says on its own line
    # that it is one, and the decision is the last thing printed -- an operator
    # or a script that reads only the final line must not be able to act on the
    # gate's number after reconciliation has paused the candidate.
    print("[drift] point gate on the record held (diagnostic, not the decision): "
          "passed=%s label=%s" % (verdict["passed"], verdict["label"]), flush=True)
    print("[drift] decision: %s; advances=%s; gate and completion bound conflict=%s"
          % (reconciled["disposition"], reconciled["advances"], reconciled["conflict"]),
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
