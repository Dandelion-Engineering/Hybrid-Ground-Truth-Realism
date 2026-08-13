"""Measure what a distinct-`dataset` count does and does not constrain.

Review support for Draft 3 of `agents/Codex/Tier A Real-Arm Donor Matching
Rule.md`. That rule makes one provenance quantity *binding*: the selected
control set must use exactly `S_T` distinct `dataset` values, where `S_T` is
the distinct-`dataset` count of the surviving target set. Session and subject
counts are reported but never constrain the assignment.

`Reproducibility Packet/scripts/utils/template_metadata.py` establishes that
the `dataset` column *is* the probe-insertion identifier, and that session and
subject are both parsed out of that same string. Two consequences follow and
this script measures both:

1. Insertion, session and subject are nested: fixing which insertions the
   controls use *determines* the control arm's session and subject counts. So
   constraining the coarser counts costs the search nothing -- it filters the
   already-enumerated insertion subsets.

2. Equal insertion counts do not imply equal subject counts. This script
   counts, over the pinned snapshot, how many size-k insertion subsets carry
   exactly k subjects and how many carry fewer. The complement is the set of
   control arms that would satisfy Draft 3's floor while differing from the
   target arm in contributing animals.

Nothing host-specific is read. The input is the pinned pre-host donor-metadata
snapshot and nothing else. Stdlib only.

Example
-------

    python agents/Claude/tools/source_count_granularity_probe.py --cache "Reproducibility Packet/results/templates_snapshot_2026-08-11.csv" --probe "Neuropixels 1.0" --zone CA1
"""

import argparse
import hashlib
import itertools
import os
import sys
from collections import Counter, defaultdict

_PACKET_SCRIPTS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))),
    "Reproducibility Packet", "scripts")
sys.path.insert(0, _PACKET_SCRIPTS)

from utils import template_metadata as tm  # noqa: E402


def insertion_table(rows):
    """Map every insertion to its session and subject.

    Args:
        rows: donor row dicts from the metadata CSV.

    Returns:
        A dict keyed by insertion identifier with ``session`` and ``subject``
        values.

    Raises:
        ValueError: if any row has an unparseable provenance key, or if one
            insertion maps to more than one session or subject.
    """
    table = {}
    for row in rows:
        key = tm.provenance_keys(row)
        if not all(key[level] for level in ("insertion", "session", "subject")):
            raise ValueError(f"unparseable provenance key: {key}")
        prior = table.get(key["insertion"])
        if prior is None:
            table[key["insertion"]] = {"session": key["session"],
                                       "subject": key["subject"]}
        elif prior["session"] != key["session"] or prior["subject"] != key["subject"]:
            raise ValueError(
                f"insertion {key['insertion']} maps to two provenance rows")
    return table


def arm_counts(insertions, table):
    """Count distinct provenance values induced by a set of insertions.

    Args:
        insertions: an iterable of insertion identifiers.
        table: the mapping returned by ``insertion_table``.

    Returns:
        A dict with ``insertion``, ``session`` and ``subject`` counts.
    """
    chosen = list(insertions)
    return {
        "insertion": len(set(chosen)),
        "session": len({table[i]["session"] for i in chosen}),
        "subject": len({table[i]["subject"] for i in chosen}),
    }


def subset_census(table, k):
    """Classify every size-k insertion subset by its induced coarser counts.

    Args:
        table: the mapping returned by ``insertion_table``.
        k: subset size.

    Returns:
        A dict mapping ``(session_count, subject_count)`` to the number of
        size-k insertion subsets inducing it.
    """
    census = Counter()
    for combo in itertools.combinations(sorted(table), k):
        counts = arm_counts(combo, table)
        census[(counts["session"], counts["subject"])] += 1
    return census


def main():
    parser = argparse.ArgumentParser(
        description="Measure what a distinct-dataset count constrains.")
    parser.add_argument("--cache", required=True,
                        help="path to the pinned donor-metadata CSV snapshot")
    parser.add_argument("--probe", default="Neuropixels 1.0",
                        help="probe label to restrict to")
    parser.add_argument("--zone", default="CA1",
                        help="injection-zone brain_area label to profile")
    parser.add_argument("--max-subset-size", type=int, default=4,
                        help="largest S_T to census")
    parser.add_argument("--out", default=None,
                        help="optional path to write the report to")
    args = parser.parse_args()

    with open(args.cache, "rb") as handle:
        payload = handle.read()
    digest = hashlib.sha256(payload).hexdigest()

    lines = []

    def emit(text=""):
        print(text, flush=True)
        lines.append(text)

    emit("Source-count granularity probe")
    emit(f"snapshot sha256   {digest}")
    emit(f"matches pinned    {digest == tm.PINNED_SHA256}")
    emit(f"probe             {args.probe}")
    emit()

    rows = tm.parse_rows(payload, probe=args.probe)
    table = insertion_table(rows)
    emit(f"eligible rows                 {len(rows)}")
    emit(f"distinct insertions/datasets  {len(table)}")
    emit(f"distinct sessions             {len({v['session'] for v in table.values()})}")
    emit(f"distinct subjects             {len({v['subject'] for v in table.values()})}")
    emit()

    per_subject = defaultdict(list)
    for insertion, prov in table.items():
        per_subject[prov["subject"]].append(insertion)
    multi = {s: v for s, v in per_subject.items() if len(v) > 1}
    emit(f"subjects contributing >1 insertion  {len(multi)} of {len(per_subject)}")
    for subject in sorted(multi):
        sessions = len({table[i]["session"] for i in multi[subject]})
        emit(f"  {subject}: {len(multi[subject])} insertions in {sessions} session(s)")
    emit()

    zone_rows = [r for r in rows if (r.get("brain_area") or "") == args.zone]
    zone_ins = sorted({tm.provenance_keys(r)["insertion"] for r in zone_rows})
    zone_counts = arm_counts(zone_ins, table)
    emit(f"zone {args.zone}: {len(zone_rows)} donors")
    emit(f"  insertions {zone_counts['insertion']}  "
         f"sessions {zone_counts['session']}  subjects {zone_counts['subject']}")
    mult = Counter(tm.provenance_keys(r)["insertion"] for r in zone_rows)
    emit(f"  donors per insertion  {sorted(mult.values(), reverse=True)}")
    emit(f"  subjects              "
         f"{', '.join(sorted({table[i]['subject'] for i in zone_ins}))}")
    emit()

    emit("Size-k insertion subsets by induced (sessions, subjects):")
    emit("  k   total     equal-k subjects   fewer-than-k subjects   share equal")
    for k in range(1, args.max_subset_size + 1):
        census = subset_census(table, k)
        total = sum(census.values())
        equal = sum(n for (_, subj), n in census.items() if subj == k)
        emit(f"  {k}   {total:<9} {equal:<18} {total - equal:<23} "
             f"{equal / total:.4f}")
    emit()

    k = args.max_subset_size
    census = subset_census(table, k)
    emit(f"full census at k={k}  (sessions, subjects): count")
    for key in sorted(census):
        emit(f"  {key}: {census[key]}")

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(lines) + "\n")
        print(f"[probe] wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
