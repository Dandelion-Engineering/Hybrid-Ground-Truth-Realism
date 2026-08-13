"""Audit donor-template provenance and host-specific exclusion for Tier A.

`audit_template_library.py` answered a pool-size question: how many templates
survive an amplitude/SNR caliper per brain area, and how many remain after
dropping each area's largest contributing "dataset". It treated the ``dataset``
column as an opaque provenance token and reported a worst case.

This script answers the question that actually gates Tier A, which the earlier
audit deferred: **for a specific host recording, how many donors remain after
excluding that host's own provenance -- and at which granularity?**

Reading the ``dataset`` column rather than counting it changes the picture.
Every Neuropixels 1.0 donor is a DANDI 000409 session, the same dandiset this
project draws hosts from, so "exclude the host's source dataset" is three
different exclusions:

- **insertion** -- drop donors from the same probe insertion. Bounds the only
  hard leakage path: injecting a template extracted from the very recording it
  is injected into, where the donor unit is already present in the host.
- **session** -- also drop the other probe in the same session: same animal,
  same brain state, same session noise environment.
- **subject** -- also drop every other session from that animal.

The script reports all three, and reports what happens when the host is chosen
from a subject the donor library does not contain at all -- in which case no
exclusion applies and each area keeps its full in-caliper pool.

This remains a *pool-size* audit. It does not test anatomical placement,
post-rescaling effective SNR in a host, or pairwise covariate balance between a
region-matched and a region-unaware arm. Those are separate gates.

Stdlib only: this is a 2 MB CSV and a few group-bys.

Example
-------
Run from the ``Reproducibility Packet`` folder, which is the working directory
every command in ``README.md`` assumes; ``python`` means that folder's own
virtual environment, built in README's Setup section. This is **Step 2** of
that runbook, which also records what the command produced and whether it has
been re-run since:

    python scripts/audit_donor_provenance.py --cache results/templates_snapshot_2026-08-11.csv --host-subject NYU-11 --detail-area CA1 --out results/donor_provenance_2026-08-11.txt
"""

import argparse
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import template_metadata as tm  # noqa: E402


def summarise_area(rows):
    """Count an area's donors and its provenance spread.

    Args:
        rows: donor row dicts for one brain area, already caliper-screened.

    Returns:
        A dict with the total count and, per granularity, the number of
        distinct provenance values and the worst-case count remaining after
        dropping the single largest contributor at that granularity.
    """
    keys = [tm.provenance_keys(row) for row in rows]
    out = {"n": len(rows)}
    for level in ("insertion", "session", "subject"):
        counts = Counter(key[level] for key in keys)
        out[f"n_{level}"] = len(counts)
        out[f"worst_{level}"] = len(rows) - (max(counts.values()) if counts else 0)
    return out


def remaining_after_host(rows, host, level):
    """Count donors left after excluding a named host's provenance.

    Args:
        rows: donor row dicts for one brain area, already caliper-screened.
        host: dict with optional ``subject``, ``session``, ``insertion`` keys.
        level: exclusion granularity -- ``insertion``, ``session``, or
            ``subject``.

    Returns:
        The number of donors whose provenance at ``level`` differs from the
        host's. When the host's value at that level is unknown, every donor is
        retained and the caller is responsible for saying so.
    """
    target = host.get(level)
    if not target:
        return len(rows)
    return sum(1 for row in rows if tm.provenance_keys(row)[level] != target)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--url", default=tm.DEFAULT_CSV_URL,
                        help="donor metadata CSV URL (default: the first-party S3 object)")
    parser.add_argument("--cache", default=None,
                        help="optional local path to cache the CSV, for repeatable offline runs")
    parser.add_argument("--probe", default="Neuropixels 1.0",
                        help="probe type to audit (default: 'Neuropixels 1.0', the IBL subset)")
    parser.add_argument("--amp-lo", type=float, default=50.0,
                        help="lower provisional donor-amplitude screen in uV (default: 50)")
    parser.add_argument("--amp-hi", type=float, default=200.0,
                        help="upper provisional donor-amplitude screen in uV (default: 200)")
    parser.add_argument("--snr-lo", type=float, default=5.0, help="lower SNR caliper (default: 5)")
    parser.add_argument("--snr-hi", type=float, default=15.0, help="upper SNR caliper (default: 15)")
    parser.add_argument("--min-templates", type=int, default=10,
                        help="templates an area needs to support one arm (default: 10, the anchor "
                             "paper's injected-unit count per recording)")
    parser.add_argument("--host-subject", default=None,
                        help="subject identifier of the candidate host, e.g. 'NYU-11'")
    parser.add_argument("--host-session", default=None,
                        help="session UUID of the candidate host")
    parser.add_argument("--host-insertion", default=None,
                        help="exact donor-library 'dataset' string of the candidate host, if the "
                             "host is itself a donor-library insertion")
    parser.add_argument("--detail-area", default=None,
                        help="print every surviving donor row for one area, e.g. 'CA1'")
    parser.add_argument("--out", default=None,
                        help="path to write the report to, in addition to stdout")
    args = parser.parse_args()

    if args.amp_lo >= args.amp_hi or args.snr_lo >= args.snr_hi:
        sys.exit("[fatal] caliper bounds must be strictly increasing")
    if args.min_templates < 1:
        sys.exit("[fatal] --min-templates must be at least 1")

    payload, digest = tm.fetch_metadata(args.url, cache_path=args.cache)
    rows = tm.parse_rows(payload, probe=args.probe)

    report = []

    def emit(line=""):
        print(line, flush=True)
        report.append(line)

    host = {
        "subject": args.host_subject,
        "session": args.host_session,
        "insertion": args.host_insertion,
    }

    emit("# Donor provenance and host-specific exclusion audit")
    emit()
    emit(f"url             {args.url}")
    emit(f"bytes           {len(payload)}")
    emit(f"sha256          {digest}")
    emit(f"matches pinned  {digest == tm.PINNED_SHA256}  (pinned = {tm.PINNED_SHA256})")
    emit(f"probe           {args.probe}  ({len(rows)} rows)")
    emit(f"caliper         amplitude {args.amp_lo}-{args.amp_hi} uV, SNR {args.snr_lo}-{args.snr_hi}")
    emit()

    all_keys = [tm.provenance_keys(row) for row in rows]
    n_insertion = len({key["insertion"] for key in all_keys})
    n_session = len({key["session"] for key in all_keys})
    n_subject = len({key["subject"] for key in all_keys})
    unparsed = sum(1 for key in all_keys if not key["subject"] or not key["session"])
    dandisets = sorted({(row.get("dataset") or "").split("_", 1)[0] for row in rows})

    emit("## What the 'dataset' column actually contains")
    emit()
    emit(f"distinct insertions (raw 'dataset' values)   {n_insertion}")
    emit(f"distinct sessions                            {n_session}")
    emit(f"distinct subjects                            {n_subject}")
    emit(f"rows whose provenance could not be parsed    {unparsed}")
    emit(f"dandiset prefixes present                    {', '.join(dandisets)}")
    emit(f"subjects                                     "
         f"{', '.join(sorted({k['subject'] for k in all_keys if k['subject']}))}")
    emit()
    if dandisets == ["000409"]:
        emit("Every donor template for this probe type comes from DANDI 000409 -- the same")
        emit("dandiset the project's candidate hosts come from. Host and donor provenance are")
        emit("therefore not independent by default, and the exclusion granularity below is a")
        emit("design choice that has to be declared rather than inherited.")
        emit()

    kept = [row for row in rows
            if tm.in_caliper(row, args.amp_lo, args.amp_hi, args.snr_lo, args.snr_hi)]
    emit(f"rows inside caliper   {len(kept)} of {len(rows)}")
    emit(f"distinct areas inside {len({row.get('brain_area', '') for row in kept})}")
    emit()

    by_area = defaultdict(list)
    for row in kept:
        by_area[row.get("brain_area", "")].append(row)

    emit(f"## Areas with at least {args.min_templates} in-caliper templates")
    emit()
    emit("'worst-case' columns drop the area's single largest contributor at that granularity.")
    emit("They are the conservative floor, reached only when the chosen host happens to be that")
    emit("contributor. A host from a subject absent from the library incurs no exclusion at all,")
    emit("and the area keeps its full 'n'.")
    emit()
    header = (f"{'area':<12}{'n':>4}{'ins':>5}{'ses':>5}{'sub':>5}"
              f"{'worst_ins':>11}{'worst_ses':>11}{'worst_sub':>11}")
    emit(header)
    emit("-" * len(header))

    viable = {"n": [], "insertion": [], "session": [], "subject": []}
    for area, area_rows in sorted(by_area.items(), key=lambda item: -len(item[1])):
        if not area or len(area_rows) < args.min_templates:
            continue
        s = summarise_area(area_rows)
        emit(f"{area:<12}{s['n']:>4}{s['n_insertion']:>5}{s['n_session']:>5}{s['n_subject']:>5}"
             f"{s['worst_insertion']:>11}{s['worst_session']:>11}{s['worst_subject']:>11}")
        viable["n"].append(area)
        for level in ("insertion", "session", "subject"):
            if s[f"worst_{level}"] >= args.min_templates:
                viable[level].append(area)
    emit()
    emit(f"areas at >= {args.min_templates} before any exclusion            "
         f"{len(viable['n'])}")
    for level in ("insertion", "session", "subject"):
        names = ", ".join(viable[level]) if viable[level] else "none"
        emit(f"areas surviving worst-case {level:<9} exclusion  {len(viable[level]):>3}  ({names})")
    emit()

    emit("## Host-specific exclusion")
    emit()
    if not any(host.values()):
        emit("No host named (--host-subject / --host-session / --host-insertion). Nothing to")
        emit("exclude, so the exact counts equal the 'n' column above. Name a candidate host to")
        emit("replace the worst case with the number that actually applies to it.")
    else:
        emit(f"host subject    {host['subject'] or '(not given)'}")
        emit(f"host session    {host['session'] or '(not given)'}")
        emit(f"host insertion  {host['insertion'] or '(not given)'}")
        emit()
        library_subjects = {key["subject"] for key in all_keys if key["subject"]}
        if host["subject"] and host["subject"] not in library_subjects:
            emit(f"Subject {host['subject']} does not appear in the donor library. No donor shares")
            emit("this host's animal, session, or insertion, so every exclusion granularity is")
            emit("vacuous and each area below keeps its full in-caliper pool.")
            emit()
        header = (f"{'area':<12}{'n':>4}{'excl_ins':>10}{'excl_ses':>10}{'excl_sub':>10}"
                  f"{'  passes at >= ' + str(args.min_templates)}")
        emit(header)
        emit("-" * (len(header) - 2))
        for area, area_rows in sorted(by_area.items(), key=lambda item: -len(item[1])):
            if not area or len(area_rows) < args.min_templates:
                continue
            counts = {level: remaining_after_host(area_rows, host, level)
                      for level in ("insertion", "session", "subject")}
            passes = [level[:3] for level in ("insertion", "session", "subject")
                      if counts[level] >= args.min_templates]
            emit(f"{area:<12}{len(area_rows):>4}{counts['insertion']:>10}{counts['session']:>10}"
                 f"{counts['subject']:>10}  {', '.join(passes) if passes else 'none'}")
    emit()

    if args.detail_area:
        area_rows = by_area.get(args.detail_area, [])
        emit(f"## Surviving donors in {args.detail_area} (in-caliper, before host exclusion)")
        emit()
        if not area_rows:
            emit(f"No in-caliper templates for area {args.detail_area!r}.")
        else:
            emit(f"{'template_index':>15}{'subject':>10}{'session':>12}"
                 f"{'amp_uv':>9}{'snr':>7}{'depth_um':>10}{'noise_uv':>10}{'spikes':>9}")
            for row in sorted(area_rows, key=lambda r: tm.as_float(r, "depth_along_probe") or 0.0):
                keys = tm.provenance_keys(row)
                emit(f"{row.get('template_index', ''):>15}"
                     f"{(keys['subject'] or '?'):>10}"
                     f"{(keys['session'] or '?')[:8]:>12}"
                     f"{tm.as_float(row, 'amplitude_uv') or float('nan'):>9.1f}"
                     f"{tm.as_float(row, 'signal_to_noise_ratio') or float('nan'):>7.2f}"
                     f"{tm.as_float(row, 'depth_along_probe') or float('nan'):>10.1f}"
                     f"{tm.as_float(row, 'noise_level_uv') or float('nan'):>10.2f}"
                     f"{row.get('spikes_per_unit', ''):>9}")
            emit()
            emit("Note: template_index is unique within an insertion, not across the library.")
            emit("Pin a donor by (dataset, template_index), never by template_index alone.")
        emit()

    emit("This is a pool-size audit. Anatomical placement feasibility, post-rescaling effective")
    emit("SNR in the selected host, and pairwise covariate balance between the region-matched and")
    emit("region-unaware arms are separate gates and are not tested here.")

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write("\n".join(report) + "\n")
        print(f"[write] wrote report to {args.out}", flush=True)


if __name__ == "__main__":
    main()
