"""Measure the conversion provenance and declared clock of both halves of a session.

Why this exists
---------------
``measure_host_drift.py`` stops as an input error when a session's raw and
processed assets name different NeuroConv versions. That rule was written at
Claude Session 32 from a reviewer's finding, on evidence drawn from *raw* assets
only: Session 7 read ``general/source_script`` from 21 raw NWB files and never
read a processed one. The first real candidate run, Claude Session 33, stopped
immediately -- CSHL047 Probe01 raw states ``v0.9.2`` and its processed half
states ``v0.9.4``.

Version equality was a *proxy* for the property the rule is actually about: that
the raw asset's timing coordinate and the processed asset's spike coordinate are
the same coordinate. This probe reads the proxy and the property side by side,
across as many sessions as it is given, so the rule can be judged against a
measurement instead of against one candidate.

What it reads, per asset
------------------------
``general/source_script`` and the other declared provenance paths through
``utils.archive_units.source_provenance``, under that module's own request and
transfer budgets; then, under a second budget of the same shape, the NWB root
values that state the clock directly:

* ``/session_start_time`` -- the wall-clock instant session time is measured from
* ``/timestamps_reference_time`` -- the instant timestamps are measured from,
  which is what a spike time and a sample time are both relative to
* ``/general/session_id`` and the root ``nwb_version`` attribute, as identity

Nothing else is read. No payload, no electrode table, no spike times. The cost
is a few hundred kilobytes per asset and does not grow with the recording.

This is a probe in ``agents/Claude/tools/``, not a packet script: it exists to
produce evidence for a rule decision, and it reads no number that decides a
verdict.

Example
-------
Run from the repository root with the project's own interpreter::

    ./venv/Scripts/python.exe agents/Claude/tools/probe_conversion_pairs.py \
        --assets-cache "Reproducibility Packet/results/dandi_000409_assets.json" \
        --sessions b52182e7-39f6-4914-9717-136db589706e \
        --out agents/Claude/tools/conversion_pairs.txt
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SCRIPTS = os.path.join(REPO_ROOT, "Reproducibility Packet", "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from utils import archive_units, dandi  # noqa: E402

# The NWB root values that state the clock, read in addition to the provenance
# paths ``archive_units`` already declares. Each is a scalar of a few dozen
# characters.
#
# **Why the budget is a separate number rather than the provenance one.** The
# first run of this probe reused ``PROVENANCE_MAX_BYTES`` and left four of
# eleven processed assets undetermined: reaching a root value in those files
# cost a single 61,440-byte structural read that did not fit in what the scope
# had left. An undetermined value is not a null result here -- it is the
# absence of the measurement the probe exists to take, and the four that went
# unread were four of the seven that would have decided the pattern. The budget
# is therefore the probe's own, defaulting well above what any of these reads
# has been observed to need, and it is still a bound rather than an open read.
CLOCK_PATHS = (
    "session_start_time",
    "timestamps_reference_time",
    "general/session_id",
)

CLOCK_SCOPE = "clock probe"

DEFAULT_CLOCK_BUDGET_BYTES = 1024 * 1024


def read_clock_paths(handle, reader, budget=DEFAULT_CLOCK_BUDGET_BYTES):
    """Read the NWB root values that state the session's time coordinate.

    Args:
        handle: an open :class:`h5py.File`.
        reader: the :class:`archive_units.BoundedReader` it was opened on.
        budget: the request budget for this scope, cumulative over every path.

    Returns:
        A dict from path to its stored value as a string, omitting paths the
        file does not carry, plus ``nwb_version`` from the root attributes when
        it is present. A value the budget refuses is recorded as a marker
        rather than raised, for the same reason the provenance read records one:
        a refusal on one path is a fact about that path, not about the file.
    """
    out = {}
    transfer = (None if not reader.block_bytes
                else budget + (len(CLOCK_PATHS) + 1) * int(reader.block_bytes))
    with reader.budget(budget, transfer, label=CLOCK_SCOPE):
        for path in CLOCK_PATHS:
            try:
                if path not in handle:
                    continue
                node = handle[path]
                value = node[()]
            except archive_units.ReadBudgetExceeded as exc:
                out[path] = "<unread: %s>" % exc
                continue
            except (TypeError, ValueError):
                continue
            if isinstance(value, bytes):
                value = value.decode()
            out[path] = str(value)
        try:
            attr = handle.attrs.get("nwb_version")
        except archive_units.ReadBudgetExceeded as exc:
            attr = "<unread: %s>" % exc
        if attr is not None:
            out["nwb_version"] = attr.decode() if isinstance(attr, bytes) else str(attr)
    return out


def read_asset(asset, block_bytes, clock_budget=DEFAULT_CLOCK_BUDGET_BYTES):
    """Read one asset's provenance and declared clock under bounded reads.

    Args:
        asset: an asset dict from ``utils.dandi.list_assets``.
        block_bytes: the range-request block size to ask the reader for. It is
            capped the same way ``archive_units.read_provenance`` caps it, so a
            large block chosen for a payload read cannot inflate this one.
        clock_budget: the request budget for the clock scope, in bytes.

    Returns:
        A dict carrying the asset's identity, its provenance paths, the parsed
        conversion version (None when the value is not the measured statement),
        the clock paths, and what the two bounded reads spent.
    """
    import h5py  # local, so --help costs nothing

    block = min(int(block_bytes), archive_units.PROVENANCE_BLOCK_BYTES)
    remote = archive_units.RemoteFile(dandi.blob_url(asset), asset["size"], block=block)
    reader = archive_units.BoundedReader(remote)
    with h5py.File(reader, "r") as handle:
        provenance = archive_units.source_provenance(handle, reader)
        provenance_spend = reader.last_spend
        clock = read_clock_paths(handle, reader, clock_budget)
        clock_spend = reader.last_spend
    source = provenance.get(archive_units.REQUIRED_PROVENANCE_PATH)
    return {
        "asset_id": asset["asset_id"],
        "path": asset["path"],
        "size": asset["size"],
        "subject": dandi.subject_of(asset),
        "session": dandi.session_of(asset),
        "source_script": source,
        "conversion_version": (archive_units.conversion_version(source)
                               if isinstance(source, str) else None),
        "provenance": provenance,
        "clock": clock,
        "provenance_io": provenance_spend,
        "clock_io": clock_spend,
        "io": {"requests": remote.n_requests, "bytes": remote.n_bytes},
    }


def compare_pair(raw, processed):
    """State what the pair agrees and disagrees on.

    Args:
        raw: the record :func:`read_asset` returned for the raw asset.
        processed: the same for the processed asset.

    Returns:
        A dict with ``version_agrees``, ``clock_agrees`` and the values each
        conclusion rests on. ``clock_agrees`` is None when either asset does not
        carry ``timestamps_reference_time``, because an absent value is not
        agreement and reporting it as one would be the same substitution this
        probe exists to examine.
    """
    versions = (raw["conversion_version"], processed["conversion_version"])
    reference = (raw["clock"].get("timestamps_reference_time"),
                 processed["clock"].get("timestamps_reference_time"))
    start = (raw["clock"].get("session_start_time"),
             processed["clock"].get("session_start_time"))
    clock_agrees = None
    if all(isinstance(value, str) and not value.startswith("<unread")
           for value in reference):
        clock_agrees = reference[0] == reference[1]
    start_agrees = None
    if all(isinstance(value, str) and not value.startswith("<unread")
           for value in start):
        start_agrees = start[0] == start[1]
    return {
        "version_agrees": (versions[0] is not None and versions[0] == versions[1]),
        "raw_version": versions[0],
        "processed_version": versions[1],
        "clock_agrees": clock_agrees,
        "raw_timestamps_reference_time": reference[0],
        "processed_timestamps_reference_time": reference[1],
        "session_start_agrees": start_agrees,
        "raw_session_start_time": start[0],
        "processed_session_start_time": start[1],
        "session_id_agrees": (raw["clock"].get("general/session_id")
                              == processed["clock"].get("general/session_id")),
    }


def build_report(records, dandiset, version, block_bytes, clock_budget):
    """Render the probe's findings as an ASCII report.

    Args:
        records: the per-session records, in the order they were read.
        dandiset: the dandiset identifier that was read.
        version: the dandiset version that was read.
        block_bytes: the block size requested on the command line.
        clock_budget: the request budget the clock scope ran under.

    Returns:
        A list of report lines.
    """
    lines = ["# Conversion provenance and declared clock, both halves of each session",
             "",
             "dandiset            %s (%s)" % (dandiset, version),
             "sessions read       %d" % len(records),
             "requested block     %d bytes (capped at %d for these reads)"
             % (block_bytes, archive_units.PROVENANCE_BLOCK_BYTES),
             "provenance budget   %d bytes requested"
             % archive_units.PROVENANCE_MAX_BYTES,
             "clock budget        %d bytes requested" % clock_budget,
             ""]
    total_bytes = sum(r["raw"]["io"]["bytes"] + r["processed"]["io"]["bytes"]
                      for r in records if r.get("raw"))
    total_requests = sum(r["raw"]["io"]["requests"] + r["processed"]["io"]["requests"]
                         for r in records if r.get("raw"))
    lines += ["metadata read       %d bytes in %d requests" % (total_bytes, total_requests),
              "",
              "## Per session",
              ""]
    header = ("subject    session                              raw ver  proc ver  "
              "ver=  ref=  start=")
    lines += [header, "-" * len(header)]
    for record in records:
        if record.get("error"):
            lines.append("%-10s %-36s  %s" % (record.get("subject") or "?",
                                              record["session"], record["error"]))
            continue
        cmp_ = record["comparison"]
        lines.append("%-10s %-36s %-8s %-9s %-5s %-5s %-5s"
                     % (record["subject"], record["session"],
                        cmp_["raw_version"] or "-",
                        cmp_["processed_version"] or "-",
                        "yes" if cmp_["version_agrees"] else "NO",
                        {True: "yes", False: "NO", None: "-"}[cmp_["clock_agrees"]],
                        {True: "yes", False: "NO", None: "-"}[cmp_["session_start_agrees"]]))
    lines += ["", "## Distributions", ""]
    pairs = {}
    for record in records:
        if record.get("error"):
            continue
        key = "%s -> %s" % (record["comparison"]["raw_version"] or "-",
                            record["comparison"]["processed_version"] or "-")
        pairs[key] = pairs.get(key, 0) + 1
    for key in sorted(pairs):
        lines.append("  raw -> processed version  %-20s %d session(s)" % (key, pairs[key]))
    measured = [r for r in records if not r.get("error")]
    lines += ["",
              "  version agrees            %d of %d"
              % (sum(1 for r in measured if r["comparison"]["version_agrees"]),
                 len(measured)),
              "  timestamps_reference_time agrees  %d of %d (undetermined %d)"
              % (sum(1 for r in measured if r["comparison"]["clock_agrees"] is True),
                 len(measured),
                 sum(1 for r in measured if r["comparison"]["clock_agrees"] is None)),
              "  session_start_time agrees %d of %d (undetermined %d)"
              % (sum(1 for r in measured if r["comparison"]["session_start_agrees"] is True),
                 len(measured),
                 sum(1 for r in measured
                     if r["comparison"]["session_start_agrees"] is None)),
              ""]
    lines += ["## Values, as read", ""]
    for record in records:
        if record.get("error"):
            continue
        cmp_ = record["comparison"]
        lines += ["%s  %s" % (record["subject"], record["session"]),
                  "  raw       source_script  %s"
                  % archive_units.ascii_safe(record["raw"]["source_script"] or "-", 120),
                  "  processed source_script  %s"
                  % archive_units.ascii_safe(record["processed"]["source_script"] or "-", 120),
                  "  raw       reference time %s"
                  % archive_units.ascii_safe(str(cmp_["raw_timestamps_reference_time"]), 80),
                  "  processed reference time %s"
                  % archive_units.ascii_safe(
                      str(cmp_["processed_timestamps_reference_time"]), 80),
                  "  raw       session start  %s"
                  % archive_units.ascii_safe(str(cmp_["raw_session_start_time"]), 80),
                  "  processed session start  %s"
                  % archive_units.ascii_safe(str(cmp_["processed_session_start_time"]), 80),
                  "  nwb_version raw / processed  %s / %s"
                  % (archive_units.ascii_safe(
                      str(record["raw"]["clock"].get("nwb_version")), 40),
                     archive_units.ascii_safe(
                         str(record["processed"]["clock"].get("nwb_version")), 40)),
                  ""]
    return lines


def parse_args(argv=None):
    """Parse the command line.

    Args:
        argv: argument list, or None to read ``sys.argv``.

    Returns:
        The parsed namespace.
    """
    parser = argparse.ArgumentParser(
        description=("Read conversion provenance and the declared session clock from "
                     "both halves of each named session, under bounded reads."))
    parser.add_argument("--assets-cache", required=True,
                        help="JSON asset listing, used to resolve blob URLs and sizes")
    parser.add_argument("--sessions", nargs="+", default=None,
                        help="session UUIDs to read")
    parser.add_argument("--sessions-file", default=None,
                        help="file holding one session UUID per line; "
                             "blank lines and lines starting with # are ignored")
    parser.add_argument("--out", required=True, help="path of the report to write")
    parser.add_argument("--records", default=None,
                        help="optional path for the raw JSON records")
    parser.add_argument("--dandiset", default="000409", help="dandiset identifier")
    parser.add_argument("--version", default="draft", help="dandiset version")
    parser.add_argument("--block-kb", type=int, default=64,
                        help="range block size in KiB, capped at the provenance block")
    parser.add_argument("--clock-budget-kb", type=int, default=1024,
                        help="request budget in KiB for the clock scope, cumulative "
                             "over its paths; the transfer budget is derived from it "
                             "and the block size")
    args = parser.parse_args(argv)
    if not args.sessions and not args.sessions_file:
        parser.error("give --sessions or --sessions-file")
    return args


def load_sessions(args):
    """Return the session UUIDs to read, in the order given.

    Args:
        args: the parsed command line.

    Returns:
        A list of session UUIDs with duplicates removed, first occurrence kept,
        because the pinned host order names some sessions twice under different
        probes and each session's pair only needs reading once.
    """
    sessions = list(args.sessions or [])
    if args.sessions_file:
        with open(args.sessions_file, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line and not line.startswith("#"):
                    sessions.append(line.split()[0])
    seen, ordered = set(), []
    for session in sessions:
        if session not in seen:
            seen.add(session)
            ordered.append(session)
    return ordered


def main(argv=None):
    """Read each session's pair and write the report."""
    args = parse_args(argv)
    sessions = load_sessions(args)
    assets = dandi.list_assets(args.dandiset, args.version, cache_path=args.assets_cache)
    block_bytes = args.block_kb * 1024

    records = []
    for session in sessions:
        by_kind = {"raw": [], "processed": []}
        for asset in assets:
            if dandi.session_of(asset) != session:
                continue
            if asset["path"].endswith(dandi.RAW_SUFFIX):
                by_kind["raw"].append(asset)
            elif asset["path"].endswith(dandi.PROCESSED_SUFFIX):
                by_kind["processed"].append(asset)
        if len(by_kind["raw"]) != 1 or len(by_kind["processed"]) != 1:
            records.append({"session": session, "subject": None,
                            "error": "resolves to %d raw and %d processed assets"
                                     % (len(by_kind["raw"]), len(by_kind["processed"]))})
            print("[pairs] %s unresolved" % session, flush=True)
            continue
        raw_asset, processed_asset = by_kind["raw"][0], by_kind["processed"][0]
        print("[pairs] %s %s" % (dandi.subject_of(raw_asset), session), flush=True)
        clock_budget = args.clock_budget_kb * 1024
        raw = read_asset(raw_asset, block_bytes, clock_budget)
        processed = read_asset(processed_asset, block_bytes, clock_budget)
        comparison = compare_pair(raw, processed)
        print("[pairs]   versions %s -> %s; reference time agrees: %s"
              % (comparison["raw_version"], comparison["processed_version"],
                 comparison["clock_agrees"]), flush=True)
        records.append({"session": session, "subject": raw["subject"],
                        "raw": raw, "processed": processed, "comparison": comparison})

    lines = build_report(records, args.dandiset, args.version, block_bytes,
                         args.clock_budget_kb * 1024)
    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print("[pairs] wrote %s" % args.out, flush=True)
    if args.records:
        with open(args.records, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(records, handle, indent=1, sort_keys=True)
        print("[pairs] wrote %s" % args.records, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
