"""Derive the CCF long-name to acronym bridge from first-party licensed data.

`utils/ccf_labels.py` is hand-authored and materially incomplete: the recorded
screen found 296 distinct host structure names with no entry, while 650 donor
rows name acronyms it does not define. The region-unaware arm needs that coverage,
because its donors are drawn without conditioning on region and their placement
still has to be evaluated against the local host label.

The obvious fix is to import the Allen CCF structure ontology. **This project may
not.** The Allen Institute Terms of Use permit use "for research or other
noncommercial purposes" and state that you "may not redistribute the Content or
Improvements for commercial purposes without our written permission." Dandelion's
licensing standard prefers commercial-use-permitting licences by default, and a
restrictive input may be used only under an explicitly approved and named
exception stating the downstream limits it creates. Packages that redistribute
the ontology under permissive terms (`iblatlas`, MIT; `brainglobe-atlasapi`,
BSD-3) do not dissolve the upstream terms on the data itself.

So this script derives the bridge instead, from two inputs the project already
holds under commercial-use-permitting licences:

    DANDI 000409          CC-BY-4.0   host electrodes table: CCF *long name*
                                      plus ``rel_y`` depth, per electrode
    hybrid_template_library  MIT       donor rows: CCF *acronym* plus
                                      ``depth_along_probe``, per template

Both vocabularies describe the same physical place on the same probe, so the
correspondence can be read off the data rather than imported:

    donor says   (session S, depth 2900 um) is ``CA1``
    host says    (session S, depth 2900 um) is "Field CA1"
    therefore    "Field CA1" <-> ``CA1``

This is the same evidence `validate_ccf_label_map.py` uses to *check* the
hand-authored table, run in the other direction to *build* entries it lacks. Two
consequences follow and both are reported rather than assumed:

1. **Coverage is bounded by the donor library.** A host structure no donor
   template sits in cannot be derived here, however common it is in the host.
   The report states what was reached and what was not.
2. **Boundary contamination is the failure mode.** A donor at a structure border
   can sit nearest an electrode belonging to its neighbour. Each proposed entry
   therefore carries its vote count, its supporting-insertion count, and every
   competing name, and entries that are not unanimous are tiered rather than
   silently resolved by majority.

The script also audits the hand-authored table against its own derivation, which
is a genuine independent check of the long-name spellings nobody has run.

Example
-------
Run from the ``Reproducibility Packet`` folder, which is the working directory
every command in ``README.md`` assumes; ``python`` means that folder's own
virtual environment, built in README's Setup section. This is **Step 4** of
that runbook, which also records what the command produced and whether it has
been re-run since:

    python scripts/derive_ccf_label_map.py --from-records results/ccf_label_map_derived_records.json --out results/ccf_label_map_derived.txt --json-out scripts/utils/ccf_label_map_derived.json
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import h5py  # noqa: E402

from utils import ccf_labels, dandi  # noqa: E402
from utils import template_metadata as tm  # noqa: E402
from utils.remote_hdf5 import RemoteFile  # noqa: E402

ELECTRODES_PATH = "general/extracellular_ephys/electrodes"

# Tier names, ordered from strongest evidence to weakest.
TIER_UNANIMOUS = "unanimous"
TIER_MAJORITY = "majority"
TIER_AMBIGUOUS = "ambiguous"


def read_probe_depth_labels(url, size, block_bytes):
    """Read per-probe (depth, CCF long name) pairs from a remote NWB.

    Args:
        url: direct S3 URL of the NWB blob.
        size: blob size in bytes.
        block_bytes: HTTP range-request block size.

    Returns:
        A tuple of (probes, bytes transferred, range requests issued), where
        probes maps probe name to a list of (depth_um, location) tuples. The
        transfer counters are returned rather than discarded so the report can
        state what this cost over the network.

    Raises:
        KeyError: if the file carries no electrodes table.
    """
    remote = RemoteFile(url, size, block=block_bytes)
    probes = defaultdict(list)
    with h5py.File(remote, "r") as handle:
        if ELECTRODES_PATH not in handle:
            raise KeyError(f"{url} has no {ELECTRODES_PATH}")
        table = handle[ELECTRODES_PATH]
        locations = [v.decode() if isinstance(v, bytes) else str(v)
                     for v in table["location"][:]]
        groups = [v.decode() if isinstance(v, bytes) else str(v)
                  for v in table["group_name"][:]]
        depths = table["rel_y"][:].tolist()
        for probe, depth, location in zip(groups, depths, locations):
            probes[probe].append((depth, location))
    return dict(probes), remote.n_bytes, remote.n_requests


def score_probe_against_table(donor_rows, depth_labels, tolerance_um):
    """Count how many donor rows the hand-authored table already matches.

    This is used only to assign a probe to a donor insertion, which is the one
    step the derivation cannot do from the data alone: the donor ``dataset``
    string names an insertion UUID the NWB does not carry. Using the validated
    table for assignment and then deriving *new* entries is not circular, but it
    is a dependency, and the report states it.

    Args:
        donor_rows: donor row dicts from one template-library insertion.
        depth_labels: (depth_um, location) tuples for one probe.
        tolerance_um: depth tolerance in micrometres.

    Returns:
        A tuple of (agreements, comparisons) over rows whose acronym the
        hand-authored table defines.
    """
    defined = set(ccf_labels.NAME_TO_ACRONYM.values())
    agreements = comparisons = 0
    for row in donor_rows:
        depth = tm.as_float(row, "depth_along_probe")
        acronym = (row.get("brain_area") or "").strip()
        if depth is None or not acronym or acronym not in defined:
            continue
        nearby = [location for electrode_depth, location in depth_labels
                  if abs(electrode_depth - depth) <= tolerance_um]
        if not nearby:
            continue
        comparisons += 1
        if acronym in {ccf_labels.to_acronym(location) for location in nearby}:
            agreements += 1
    return agreements, comparisons


def nearest_locations(depth_labels, depth, tolerance_um):
    """Return the location names of the electrodes nearest a donor depth.

    Only the nearest electrodes are returned, not every electrode inside the
    tolerance. Voting over the whole tolerance window would count a donor's
    neighbouring structure as often as its own, which is precisely the boundary
    contamination this derivation has to resist.

    Args:
        depth_labels: (depth_um, location) tuples for one probe.
        depth: the donor's ``depth_along_probe`` in micrometres.
        tolerance_um: how far an electrode may sit and still describe the
            same place.

    Returns:
        A list of location strings -- normally one, more only on an exact
        distance tie between contacts. Empty when nothing is within tolerance.
    """
    within = [(abs(electrode_depth - depth), location)
              for electrode_depth, location in depth_labels
              if abs(electrode_depth - depth) <= tolerance_um]
    if not within:
        return []
    closest = min(distance for distance, _ in within)
    return [location for distance, location in within if distance == closest]


def classify(votes, majority_fraction):
    """Assign an evidence tier to one acronym's competing location names.

    Args:
        votes: Counter mapping location name to vote count.
        majority_fraction: the share of votes the leader must reach to be
            accepted as a majority entry.

    Returns:
        A tuple of (tier, winning location name or None).
    """
    if not votes:
        return TIER_AMBIGUOUS, None
    ranked = votes.most_common()
    if len(ranked) == 1:
        return TIER_UNANIMOUS, ranked[0][0]
    total = sum(votes.values())
    leader, leader_votes = ranked[0]
    runner_up_votes = ranked[1][1]
    if leader_votes == runner_up_votes:
        return TIER_AMBIGUOUS, None
    if leader_votes / total >= majority_fraction:
        return TIER_MAJORITY, leader
    return TIER_AMBIGUOUS, None


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--dandiset", default="000409", help="dandiset id (default: 000409)")
    parser.add_argument("--version", default="draft", help="dandiset version (default: draft)")
    parser.add_argument("--assets-cache", default=None,
                        help="JSON file caching the DANDI asset listing")
    parser.add_argument("--templates-cache", default=None,
                        help="local path caching the donor metadata CSV")
    parser.add_argument("--url", default=tm.DEFAULT_CSV_URL, help="donor metadata CSV URL")
    parser.add_argument("--probe-type", default="Neuropixels 1.0",
                        help="template-library probe type (default: 'Neuropixels 1.0')")
    parser.add_argument("--suffix", default=dandi.PROCESSED_SUFFIX,
                        help=f"asset suffix to read electrode tables from "
                             f"(default: {dandi.PROCESSED_SUFFIX!r})")
    parser.add_argument("--tolerance-um", type=float, default=20.0,
                        help="depth tolerance when matching a donor to electrodes "
                             "(default: 20, one Neuropixels 1.0 contact row)")
    parser.add_argument("--majority-fraction", type=float, default=2.0 / 3.0,
                        help="vote share the leading name must reach to be accepted as a "
                             "majority entry (default: 0.667)")
    parser.add_argument("--min-insertions", type=int, default=1,
                        help="supporting insertions an entry needs to be emitted "
                             "(default: 1)")
    parser.add_argument("--block-kb", type=int, default=1024,
                        help="HTTP range block size in KiB (default: 1024)")
    parser.add_argument("--limit", type=int, default=None,
                        help="read at most this many donor sessions")
    parser.add_argument("--out", default=None, help="path to write the text report to")
    parser.add_argument("--json-out", default=None,
                        help="path to write the machine-readable derived map to")
    parser.add_argument("--records-out", default=None,
                        help="path to save the raw per-donor votes, so the report can be "
                             "rebuilt later without re-reading anything over the network")
    parser.add_argument("--from-records", default=None,
                        help="rebuild the report and map from a saved records file. No network "
                             "reads happen at all; use this for any presentation or rule change")
    args = parser.parse_args()

    if args.tolerance_um < 0:
        sys.exit("[fatal] --tolerance-um must not be negative")
    if not 0.5 < args.majority_fraction <= 1.0:
        sys.exit("[fatal] --majority-fraction must be above 0.5 and at most 1.0")
    if args.min_insertions < 1:
        sys.exit("[fatal] --min-insertions must be at least 1")

    if args.from_records:
        with open(args.from_records, encoding="utf-8") as handle:
            saved = json.load(handle)
        # Raw-vote parameters are evidence-generation settings, not report
        # presentation settings. A replay must describe the records it has,
        # and must never accept a different CLI value while silently reusing
        # votes generated under the saved one. Majority/min-insertion rules
        # remain intentionally replayable because they operate on the saved
        # votes rather than changing how those votes were collected.
        replay_checks = (
            ("--probe-type", args.probe_type, saved["probe_type"]),
            ("--suffix", args.suffix, saved["asset_suffix"]),
            ("--tolerance-um", float(args.tolerance_um),
             float(saved["tolerance_um"])),
        )
        for option, requested, recorded in replay_checks:
            if requested != recorded:
                sys.exit(f"[fatal] {option}={requested!r} does not match the saved "
                         f"records value {recorded!r}; replay the records with the "
                         "evidence-generation setting that created them")
        digest = saved["donor_snapshot_sha256"]
        votes = [(record["acronym"], record["name"],
                  (record["session"], record["insertion"])) for record in saved["votes"]]
        host_names_seen = set(saved["host_names_seen"])
        probe_choices = [tuple(row) for row in saved["probe_choices"]]
        missing_sessions = list(saved["missing_sessions"])
        failures = [tuple(row) for row in saved["failures"]]
        placed = saved["placed"]
        skipped_no_electrode = saved["skipped_no_electrode"]
        args.bytes_transferred = saved.get("bytes_transferred")
        args.range_requests = saved.get("range_requests")
        n_insertions_total = saved["insertions_total"]
        n_insertions_read = saved["insertions_read"]
        print(f"[records] replayed {len(votes)} votes from {args.from_records} "
              f"with no network reads", flush=True)
        votes_by_acronym = defaultdict(Counter)
        insertions_by_pair = defaultdict(set)
        for acronym, name, insertion_key in votes:
            votes_by_acronym[acronym][name] += 1
            insertions_by_pair[(acronym, name)].add(tuple(insertion_key))
        return report_and_write(args, digest, votes_by_acronym, insertions_by_pair,
                                host_names_seen, probe_choices, missing_sessions, failures,
                                placed, skipped_no_electrode, n_insertions_total,
                                n_insertions_read)

    payload, digest = tm.fetch_metadata(args.url, cache_path=args.templates_cache)
    donor_rows = tm.parse_rows(payload, probe=args.probe_type)

    by_insertion = defaultdict(list)
    for row in donor_rows:
        keys = tm.provenance_keys(row)
        if keys["session"]:
            by_insertion[(keys["session"], keys["insertion"])].append(row)

    assets = dandi.list_assets(args.dandiset, args.version, cache_path=args.assets_cache)
    asset_by_session = {}
    for asset in assets:
        if asset["path"].endswith(args.suffix):
            asset_by_session[dandi.session_of(asset)] = asset

    insertions = sorted(by_insertion)
    if args.limit is not None:
        insertions = insertions[:args.limit]

    # acronym -> Counter of competing host long names, and the insertions each
    # was seen in. Insertion counts matter separately from vote counts: fifty
    # votes from one probe is one observation repeated, not fifty observations.
    votes_by_acronym = defaultdict(Counter)
    insertions_by_pair = defaultdict(set)
    host_names_seen = set()
    placed = skipped_no_electrode = 0
    failures = []
    missing_sessions = []
    probe_choices = []
    raw_votes = []
    total_bytes = total_requests = 0

    for number, (session, insertion) in enumerate(insertions, start=1):
        asset = asset_by_session.get(session)
        if asset is None:
            missing_sessions.append(session)
            print(f"[{number}/{len(insertions)}] session {session[:8]} not in listing", flush=True)
            continue
        try:
            probes, n_bytes, n_requests = read_probe_depth_labels(
                dandi.blob_url(asset), asset["size"], args.block_kb * 1024)
            total_bytes += n_bytes
            total_requests += n_requests
        except (OSError, KeyError, ValueError) as exc:
            failures.append((session, f"{type(exc).__name__}: {exc}"))
            print(f"[{number}/{len(insertions)}] FAILED {session[:8]}: {exc}", flush=True)
            continue

        rows = by_insertion[(session, insertion)]
        best = None
        for probe, depth_labels in sorted(probes.items()):
            agreements, comparisons = score_probe_against_table(
                rows, depth_labels, args.tolerance_um)
            if comparisons and (best is None or agreements > best[1]):
                best = (probe, agreements, comparisons)
        if best is None:
            failures.append((session, "no probe could be assigned: no depth overlap, or every "
                                      "donor acronym here is undefined in the hand-authored "
                                      "table used for assignment"))
            print(f"[{number}/{len(insertions)}] SKIPPED {session[:8]}: no probe assignment",
                  flush=True)
            continue

        probe, agreements, comparisons = best
        probe_choices.append((session, probe, agreements, comparisons, len(probes)))
        depth_labels = probes[probe]
        for depth, location in depth_labels:
            host_names_seen.add(location)
        for row in rows:
            depth = tm.as_float(row, "depth_along_probe")
            acronym = (row.get("brain_area") or "").strip()
            if depth is None or not acronym:
                continue
            names = nearest_locations(depth_labels, depth, args.tolerance_um)
            if not names:
                skipped_no_electrode += 1
                continue
            placed += 1
            for name in names:
                votes_by_acronym[acronym][name] += 1
                insertions_by_pair[(acronym, name)].add((session, insertion))
                raw_votes.append({"acronym": acronym, "name": name,
                                  "session": session, "insertion": insertion})
        print(f"[{number}/{len(insertions)}] {session[:8]} {probe:<9} "
              f"{len(rows):>4} donor rows, assignment {agreements}/{comparisons}", flush=True)

    if args.records_out:
        document = {
            "donor_snapshot_sha256": digest,
            "probe_type": args.probe_type,
            "asset_suffix": args.suffix,
            "tolerance_um": args.tolerance_um,
            "insertions_total": len(by_insertion),
            "insertions_read": len(probe_choices),
            "placed": placed,
            "skipped_no_electrode": skipped_no_electrode,
            "bytes_transferred": total_bytes,
            "range_requests": total_requests,
            "votes": raw_votes,
            "host_names_seen": sorted(host_names_seen),
            "probe_choices": [list(row) for row in probe_choices],
            "missing_sessions": missing_sessions,
            "failures": [list(row) for row in failures],
        }
        os.makedirs(os.path.dirname(os.path.abspath(args.records_out)), exist_ok=True)
        with open(args.records_out, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=1, sort_keys=True)
            handle.write("\n")
        print(f"[write] wrote {len(raw_votes)} raw votes to {args.records_out}", flush=True)

    args.bytes_transferred = total_bytes
    args.range_requests = total_requests
    return report_and_write(args, digest, votes_by_acronym, insertions_by_pair, host_names_seen,
                            probe_choices, missing_sessions, failures, placed,
                            skipped_no_electrode, len(by_insertion), len(probe_choices))


def report_and_write(args, digest, votes_by_acronym, insertions_by_pair, host_names_seen,
                     probe_choices, missing_sessions, failures, placed, skipped_no_electrode,
                     n_insertions_total, n_insertions_read):
    """Turn accumulated votes into the report, the audit, and the derived map.

    Split from collection so that every presentation or decision-rule change can
    be replayed from saved records with no network reads, which is the pattern
    `screen_injection_placement.py --from-records` already establishes here.

    Args:
        args: parsed command-line arguments.
        digest: SHA-256 of the donor metadata snapshot the votes came from.
        votes_by_acronym: acronym -> Counter of competing host long names.
        insertions_by_pair: (acronym, name) -> set of supporting insertion keys.
        host_names_seen: every host long name on the assigned probes.
        probe_choices: per-insertion probe assignment records.
        missing_sessions: donor sessions absent from the dandiset listing.
        failures: (session, reason) pairs.
        placed: donor rows that produced at least one vote.
        skipped_no_electrode: donor rows with no electrode inside the tolerance.
        n_insertions_total: donor insertions available.
        n_insertions_read: donor insertions that produced votes.

    Returns:
        None. Writes the report and, when asked, the machine-readable map.
    """
    report = []

    def emit(line=""):
        print(line, flush=True)
        report.append(line)

    hand_authored = dict(ccf_labels.NAME_TO_ACRONYM)
    hand_acronyms = set(hand_authored.values())

    emit("# CCF label-map derivation from first-party data")
    emit()
    emit(f"donor snapshot sha256   {digest}")
    emit(f"matches pinned          {digest == tm.PINNED_SHA256}")
    emit(f"probe type              {args.probe_type}")
    emit(f"donor insertions        {n_insertions_total} (assigned a probe: {n_insertions_read})")
    emit(f"depth tolerance         {args.tolerance_um} um")
    emit(f"majority fraction       {args.majority_fraction:.3f}")
    emit(f"min supporting insertions  {args.min_insertions}")
    emit(f"electrode table source  {args.suffix}")
    if getattr(args, "bytes_transferred", None) is not None:
        emit(f"metadata transferred    {args.bytes_transferred / 1e6:.1f} MB in "
             f"{args.range_requests} range requests (no recording data read)")
    emit()
    emit("Licence position, because it is why this script exists rather than an ontology import.")
    emit("The Allen Institute Terms of Use permit use for research or other noncommercial")
    emit("purposes and forbid commercial redistribution without written permission. Both inputs")
    emit("used here instead permit commercial use: DANDI 000409 is CC-BY-4.0 and the")
    emit("hybrid_template_library is MIT. No ontology file is downloaded, vendored, or derived")
    emit("from. Every correspondence below is read off those two licensed sources.")
    emit()

    emit("## Derived entries")
    emit()
    emit("One row per donor acronym. 'votes' counts donor templates whose nearest electrode")
    emit("carried that host name; 'ins' counts the distinct donor insertions those votes came")
    emit("from, which is the number that matters -- many votes from one probe is one observation")
    emit("repeated. A unanimous acronym saw exactly one host name. A majority acronym saw more")
    emit("than one and its leader cleared the fraction above. An ambiguous acronym is reported")
    emit("and NOT emitted into the map.")
    emit()

    entries = {}
    conflicts = []
    tier_counts = Counter()
    audit_agree, audit_disagree, audit_new = [], [], []
    proposals = []

    emit(f"{'acronym':<12}{'tier':<11}{'votes':>7}{'ins':>5}  host long name")
    emit("-" * 96)
    for acronym in sorted(votes_by_acronym):
        votes = votes_by_acronym[acronym]
        tier, winner = classify(votes, args.majority_fraction)
        total_votes = sum(votes.values())
        supporting = (len(insertions_by_pair[(acronym, winner)]) if winner else 0)
        if winner and supporting < args.min_insertions:
            tier = TIER_AMBIGUOUS
        tier_counts[tier] += 1
        shown = winner if winner else "/".join(name for name, _ in votes.most_common())
        emit(f"{acronym:<12}{tier:<11}{total_votes:>7}{supporting:>5}  {shown}")
        if tier == TIER_AMBIGUOUS:
            conflicts.append((acronym, votes.most_common()))
            continue
        if tier == TIER_MAJORITY:
            conflicts.append((acronym, votes.most_common()))
        proposals.append((acronym, tier, winner, votes, total_votes, supporting))

    # Two acronyms can win the same host long name -- a donor sitting one contact
    # outside its own layer proposes its neighbour's name, and the neighbour
    # proposes it too. The map is keyed by name, so emitting both would silently
    # keep whichever was written last. Collisions are refused and reported: one
    # of the two is wrong and the data here cannot say which.
    by_key = defaultdict(list)
    for proposal in proposals:
        by_key[ccf_labels.normalise(proposal[2])].append(proposal)
    collisions = []

    for key, group in sorted(by_key.items()):
        if len(group) > 1:
            collisions.append((group[0][2], [(p[0], p[4], p[5]) for p in group]))
            continue
        acronym, tier, winner, votes, total_votes, supporting = group[0]
        entries[winner] = {
            "acronym": acronym,
            "tier": tier,
            "votes": votes[winner],
            "votes_total": total_votes,
            "insertions": supporting,
            "competing": {name: count for name, count in votes.most_common() if name != winner},
        }
        # Audit against the hand-authored table, which is the independent check
        # nobody has run on its long-name spellings. The comparison must use the
        # same normalised key `to_acronym` looks up with: the NWB export strips
        # the commas the canonical Allen names carry, so a raw string comparison
        # reports punctuation as a disagreement about anatomy.
        existing = ccf_labels.to_acronym(winner)
        if existing is None and acronym in hand_acronyms:
            audit_disagree.append((acronym, winner, "table defines this acronym under "
                                                    "a different long name"))
        elif existing is None:
            audit_new.append((acronym, winner))
        elif existing == acronym:
            audit_agree.append((acronym, winner))
        else:
            audit_disagree.append((acronym, winner,
                                   f"table maps this long name to {existing!r}"))

    emit()
    emit(f"donor rows placed              {placed}")
    emit(f"donor rows with no electrode within tolerance  {skipped_no_electrode}")
    emit(f"distinct donor acronyms seen   {len(votes_by_acronym)}")
    for tier in (TIER_UNANIMOUS, TIER_MAJORITY, TIER_AMBIGUOUS):
        emit(f"  {tier:<10} {tier_counts[tier]}")
    emit(f"withheld for name collision    {sum(len(g) for _, g in collisions)}")
    emit(f"entries emitted                {len(entries)}")
    emit()

    if collisions:
        emit(f"## Withheld: one host long name claimed by more than one acronym ({len(collisions)})")
        emit()
        emit("Each of these is a donor acronym whose winning host name another acronym also won.")
        emit("At most one can be right and this evidence cannot say which, so NONE of them is")
        emit("emitted. The usual cause is a donor one contact outside its own layer.")
        emit()
        for name, group in collisions:
            claimants = ", ".join(f"{acronym} ({total} votes, {ins} ins)"
                                  for acronym, total, ins in group)
            emit(f"  {name!r}: {claimants}")
        emit()

    emit("## Audit against the hand-authored table")
    emit()
    emit("Every emitted entry is compared with utils/ccf_labels.py. This is independent evidence")
    emit("about the long-name spellings in that table, which the existing validation could not")
    emit("give: that run could only test names the table already contained.")
    emit()
    emit(f"AGREE, same long name and acronym ({len(audit_agree)}): "
         f"{', '.join(a for a, _ in audit_agree) if audit_agree else 'none'}")
    emit()
    emit(f"NEW, long name the table did not contain ({len(audit_new)}): "
         f"{', '.join(a for a, _ in audit_new) if audit_new else 'none'}")
    emit()
    emit(f"DISAGREE, table says something different ({len(audit_disagree)}): "
         f"{'none' if not audit_disagree else ''}")
    for acronym, name, reason in audit_disagree:
        emit(f"  {acronym:<12} derived {name!r} -- {reason}")
    emit()
    emit("A DISAGREE row is the one that matters and must be diagnosed before the entry is")
    emit("trusted. It means the derivation and the hand-authored table describe the same place")
    emit("differently, and only one of them can be right.")
    emit()

    if conflicts:
        emit(f"## Acronyms that saw more than one host name ({len(conflicts)})")
        emit()
        emit("Expected at structure borders: a donor sitting at the edge of its structure can be")
        emit("nearest an electrode belonging to the neighbour. Listed so the boundary cases are")
        emit("visible rather than absorbed by the majority rule.")
        emit()
        for acronym, ranked in conflicts:
            detail = ", ".join(f"{name!r} x{count}" for name, count in ranked)
            emit(f"  {acronym:<12} {detail}")
        emit()

    # Coverage: what fraction of the host vocabulary this reaches. The residual
    # is the honest limit of the method and belongs in the report, not in a
    # later session's surprise.
    derived_keys = {ccf_labels.normalise(name) for name in entries}
    covered = {name for name in host_names_seen
               if ccf_labels.normalise(name) in derived_keys
               or ccf_labels.to_acronym(name) is not None}
    uncovered = sorted(host_names_seen - covered)
    emit("## Coverage against the host vocabulary seen in these recordings")
    emit()
    emit(f"distinct host long names seen  {len(host_names_seen)}")
    emit(f"  mapped after derivation      {len(covered)}")
    emit(f"  still unmapped               {len(uncovered)}")
    emit()
    emit("A host structure that holds no donor template cannot be derived here however common")
    emit("it is in the host. That is the method's ceiling, and it is why this closes the donor")
    emit("side of the gap completely and the host side only partly.")
    emit()
    if uncovered:
        emit("Still unmapped:")
        for name in uncovered:
            emit(f"  {name}")
        emit()

    if probe_choices:
        emit("## Probe assignment per donor insertion")
        emit()
        emit("Assignment uses the hand-authored table's agreement, exactly as the validation run")
        emit("does, because the donor 'dataset' string names an insertion UUID the NWB does not")
        emit("carry. The derivation therefore inherits that one dependency; the entries it emits")
        emit("are new, but which probe they were read from is not independent of the table.")
        emit()
        emit(f"{'session':>10}{'probe':>10}{'agree':>8}{'compared':>10}{'probes':>8}")
        for session, probe, agreements, comparisons, n_probes in probe_choices:
            emit(f"{session[:8]:>10}{probe:>10}{agreements:>8}{comparisons:>10}{n_probes:>8}")
        emit()

    if missing_sessions:
        emit(f"## Donor sessions absent from the dandiset listing ({len(missing_sessions)})")
        emit()
        for session in missing_sessions:
            emit(f"  {session}")
        emit()
    if failures:
        emit(f"## Failures ({len(failures)})")
        emit()
        for session, reason in failures:
            emit(f"  {session}: {reason}")
        emit()

    emit("This derives a vocabulary bridge from annotations IBL already made. It does not")
    emit("validate the atlas registration itself, which is inherited as given, and it is not an")
    emit("ontology: it defines only the structures these recordings actually contain.")

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write("\n".join(report) + "\n")
        print(f"[write] wrote report to {args.out}", flush=True)

    if args.json_out:
        document = {
            "source": "derived from DANDI 000409 (CC-BY-4.0) electrode annotations and "
                      "hybrid_template_library (MIT) donor rows; no Allen ontology file used",
            "donor_snapshot_sha256": digest,
            "probe_type": args.probe_type,
            "tolerance_um": args.tolerance_um,
            "majority_fraction": args.majority_fraction,
            "min_insertions": args.min_insertions,
            "asset_suffix": args.suffix,
            "insertions_read": n_insertions_read,
            "entries": entries,
        }
        os.makedirs(os.path.dirname(os.path.abspath(args.json_out)), exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=2, sort_keys=True)
            handle.write("\n")
        print(f"[write] wrote derived map to {args.json_out}", flush=True)


if __name__ == "__main__":
    main()
