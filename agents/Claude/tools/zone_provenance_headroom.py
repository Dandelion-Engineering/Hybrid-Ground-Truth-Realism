"""Count what the Tier A provenance-blocking stages have to work with, before any host exists.

The real-arm matching rule blocks donor provenance at insertion, then session,
then subject granularity, and falls back to a source-*count* floor only when the
finer stage admits no complete assignment. Which stage it lands in decides how
strong the control arm's provenance blocking is, and that is currently unknown.

Part of it is knowable now. A stage can only succeed if each provenance group
holds at least as many *eligible partners* as it holds injection-zone targets,
and the donor library's own composition puts a ceiling on that count that no
host can raise. This script computes that ceiling from the pinned donor
snapshot:

- how many injection-zone donors each source insertion / session / subject
  contributes (the demand); and
- how many non-zone templates of the same probe type sit in that same group
  (the supply ceiling).

**Read the boundary with the numbers.** The supply figures are an upper bound
and nothing else. Final eligibility is host-specific and post-rescaling --
realized amplitude, effective host SNR, realized depth and placement
feasibility all cut into these counts, and none of them exists until a host is
pinned. A group that is short here is short for certain; a group that looks
comfortable here may still fail later. The script therefore answers "is this
stage arithmetically impossible already?" and refuses to answer anything else.

It reads only the tracked snapshot, makes no network request, and selects
nothing.

Example
-------
Run from the project root, using the project's own virtual environment:

    python "agents/Claude/tools/zone_provenance_headroom.py" --snapshot "Reproducibility Packet/results/templates_snapshot_2026-08-11.csv" --zone CA1
"""

import argparse
import collections
import csv
import hashlib
import io


def read_snapshot(path):
    """Read the pinned donor-metadata snapshot.

    Args:
        path: path to the tracked templates CSV.

    Returns:
        A tuple of (rows, sha256_hexdigest).
    """
    with io.open(path, "rb") as handle:
        raw = handle.read()
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    return rows, hashlib.sha256(raw).hexdigest()


def provenance_key(dataset, level):
    """Extract an insertion, session, or subject key from a dataset string.

    Args:
        dataset: the library's ``dataset`` value, which is the insertion key.
        level: one of ``insertion``, ``session``, ``subject``.

    Returns:
        The key at that level as a string.

    Raises:
        ValueError: if the level is unknown or the key cannot be parsed.
    """
    if level == "insertion":
        return dataset
    marker = {"session": "_ses-", "subject": "_sub-"}[level]
    if marker not in dataset:
        raise ValueError(f"{level} key not parseable from {dataset!r}")
    return dataset.split(marker, 1)[1].split("_", 1)[0]


def headroom(rows, zone, level):
    """Compare zone-donor demand against non-zone supply within each group.

    Args:
        rows: snapshot rows already restricted to one probe type.
        zone: the injection zone's brain-area label.
        level: provenance level to group by.

    Returns:
        A list of (key, demand, supply) tuples, largest demand first.
    """
    demand = collections.Counter(
        provenance_key(row["dataset"], level) for row in rows if row["brain_area"] == zone)
    supply = collections.Counter(
        provenance_key(row["dataset"], level) for row in rows if row["brain_area"] != zone)
    return sorted(((key, count, supply[key]) for key, count in demand.items()),
                  key=lambda item: (-item[1], item[0]))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--snapshot", required=True,
                        help="pinned donor-metadata CSV to read")
    parser.add_argument("--zone", required=True,
                        help="injection-zone brain-area label, e.g. CA1")
    parser.add_argument("--probe", default="Neuropixels 1.0",
                        help="probe type to restrict to (default: 'Neuropixels 1.0')")
    args = parser.parse_args()

    rows, digest = read_snapshot(args.snapshot)
    probe_rows = [row for row in rows if row["probe"] == args.probe]
    if not probe_rows:
        raise SystemExit(f"[fatal] no rows for probe {args.probe!r} in {args.snapshot}")
    zone_rows = [row for row in probe_rows if row["brain_area"] == args.zone]
    if not zone_rows:
        raise SystemExit(f"[fatal] no {args.zone} rows for probe {args.probe!r}")

    print(f"snapshot        {args.snapshot}")
    print(f"sha256          {digest}")
    print(f"probe           {args.probe}  ({len(probe_rows)} rows)")
    print(f"zone            {args.zone}  ({len(zone_rows)} donors)")
    print()
    print("Supply is an UPPER BOUND: host-specific post-rescaling eligibility can only")
    print("reduce it. A short group is short for certain; a comfortable one is not safe.")

    for level in ("insertion", "session", "subject"):
        table = headroom(probe_rows, args.zone, level)
        possible = all(supply >= demand for _, demand, supply in table)
        print()
        print(f"## {level} stage -- {len(table)} distinct {level}s hold the {args.zone} donors")
        print(f"{'demand':>6}  {'supply ceiling':>14}   {level}")
        for key, demand, supply in table:
            flag = "" if supply >= demand else "   IMPOSSIBLE ALREADY"
            print(f"{demand:>6}  {supply:>14}   {key}{flag}")
        print(f"arithmetically possible on the snapshot alone: {possible}")

    counts = collections.Counter(row["dataset"] for row in zone_rows)
    print()
    print("## source-count floor -- the target set's own composition")
    print(f"distinct source datasets in the target set: {len(counts)}")
    print(f"donors per source dataset: {sorted(counts.values(), reverse=True)}")
    print("At the floor the control set must contain exactly this many distinct source")
    print("datasets, so a more diverse control set is rejected as an imbalance, not")
    print("accepted as a bonus.")


if __name__ == "__main__":
    main()
