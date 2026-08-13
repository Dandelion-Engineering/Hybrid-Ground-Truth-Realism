"""Audit the SpikeInterface hybrid template library for region-arm feasibility.

The project's region-matching axis requires that, for some anatomically pinned
host injection zone, the template library holds enough templates to build a
region-matched arm and a region-unaware control arm with nuisance covariates
balanced so that a realism effect is not an amplitude or provenance effect in
disguise.

This script answers whether that is possible, and under what constraints. It:

1. downloads the first-party ``templates.csv`` and records its SHA-256, ETag,
   and Last-Modified, because the table is hosted mutably and any result built
   on it must pin the snapshot it used;
2. reports row counts, probe types, source datasets, and amplitude/SNR ranges;
3. counts, per brain area, how many templates survive an amplitude and SNR
   caliper; and
4. runs a conservative leave-one-dataset-out stress test: for each area, how
   many templates remain after dropping its single largest contributing source
   dataset. This is the *worst-case* remaining count. The exact count for a
   selected host depends on which source dataset that host belongs to; reusing
   the host's own dataset as a donor is a leakage path.

This is a necessary pool-size audit, not a paired-arm feasibility proof. It does
not test anatomical placement, post-rescaling effective SNR in a selected host,
or covariate balance between a region-matched and region-unaware control arm.

Stdlib only, deliberately: this is a 2 MB CSV and a few group-bys, and the
project should not acquire a dependency to answer it.

Fetching, hashing, parsing and the caliper test live in ``utils.template_metadata``
and are imported rather than repeated here; this script owns only the group-bys
and the report. It was written before that module existed and carried its own
copies until Session 10, when they were removed and the refactored script was
shown to reproduce the tracked report byte for byte from a live fetch.

Example
-------
Run from the ``Reproducibility Packet`` folder, which is the working directory
every command in ``README.md`` assumes; ``python`` means that folder's own
virtual environment, built in README's Setup section. This is **Step 1** of
that runbook, which also records what the command produced and whether it has
been re-run since:

    python scripts/audit_template_library.py --cache results/templates_snapshot_2026-08-11.csv --out results/template_audit_2026-08-11.txt

``--cache`` runs the group-bys against the pinned snapshot with no network
request, which is what makes that command reproduce byte for byte. Drop it to
fetch the live table instead; the script then reports whether its SHA-256 still
matches the pinned snapshot and fills in the ETag and Last-Modified lines, which
a cached read cannot carry and which are the only difference between the two.
"""

import argparse
import os
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import template_metadata as tm  # noqa: E402


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--url", default=tm.DEFAULT_CSV_URL,
                        help="template metadata CSV URL (default: the first-party S3 object)")
    parser.add_argument("--cache", default=None,
                        help="read/write the snapshot here; point at the tracked snapshot to "
                             "re-run the group-bys offline, at the cost of the ETag and "
                             "Last-Modified lines, which only a live request carries")
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
    parser.add_argument("--out", default=None,
                        help="path to write the report to (in addition to stdout)")
    args = parser.parse_args()

    if args.amp_lo >= args.amp_hi or args.snr_lo >= args.snr_hi:
        sys.exit("[fatal] caliper bounds must be strictly increasing")

    try:
        payload, digest, headers = tm.fetch_metadata_with_headers(
            args.url, cache_path=args.cache)
    except OSError as exc:
        sys.exit(f"[fatal] {exc}")
    report = []

    def emit(line=""):
        print(line, flush=True)
        report.append(line)

    emit("# Template library audit")
    emit()
    emit(f"url             {args.url}")
    emit(f"bytes           {len(payload)}")
    emit(f"sha256          {digest}")
    emit(f"matches pinned  {digest == tm.PINNED_SHA256}  (pinned = {tm.PINNED_SHA256})")
    emit(f"etag            {headers.get('ETag')}")
    emit(f"last-modified   {headers.get('Last-Modified')}")
    emit()

    try:
        rows = tm.parse_rows(payload)
    except ValueError as exc:
        sys.exit(f"[fatal] {exc}")
    emit(f"total rows      {len(rows)}")
    emit(f"columns         {', '.join(sorted(rows[0].keys()))}")
    for probe, count in sorted(Counter(r.get('probe', '') for r in rows).items()):
        n_ds = len({r.get('dataset', '') for r in rows if r.get('probe') == probe})
        emit(f"  probe '{probe}': {count} rows across {n_ds} source datasets")
    emit()

    subset = [r for r in rows if r.get("probe") == args.probe]
    if not subset:
        sys.exit(f"[fatal] no rows for probe '{args.probe}'; "
                 f"available: {sorted({r.get('probe', '') for r in rows})}")
    emit(f"## Subset: probe = '{args.probe}'  ({len(subset)} rows)")
    amps = [a for a in (tm.as_float(r, "amplitude_uv") for r in subset) if a is not None]
    snrs = [s for s in (tm.as_float(r, "signal_to_noise_ratio") for r in subset)
            if s is not None]
    emit(f"amplitude_uv    min {min(amps):.2f}  median {statistics.median(amps):.2f}  "
         f"max {max(amps):.2f}")
    emit(f"snr             min {min(snrs):.2f}  median {statistics.median(snrs):.2f}  "
         f"max {max(snrs):.2f}")
    emit(f"distinct brain_area labels  {len({r.get('brain_area', '') for r in subset})}")
    emit()

    kept = [r for r in subset
            if tm.in_caliper(r, args.amp_lo, args.amp_hi, args.snr_lo, args.snr_hi)]
    emit(f"## Provisional donor screen: amplitude {args.amp_lo}-{args.amp_hi} uV, "
         f"SNR {args.snr_lo}-{args.snr_hi}")
    emit(f"rows inside caliper         {len(kept)} of {len(subset)}")
    emit(f"distinct areas inside       {len({r.get('brain_area', '') for r in kept})}")
    emit()

    datasets_by_area = defaultdict(list)
    for r in kept:
        datasets_by_area[r.get("brain_area", "")].append(r.get("dataset", ""))

    emit(f"## Areas with at least {args.min_templates} in-caliper templates")
    emit()
    emit("The 'worst-case leave-one-out' column is the count remaining after dropping the")
    emit("area's single largest contributing source dataset. The exact count for a chosen host")
    emit("depends on which source dataset that host belongs to; this column is the conservative")
    emit("minimum, not the count for every host represented in the library.")
    emit()
    emit(f"{'area':<14}{'n':>5}{'datasets':>10}{'worst-case LOO':>17}")
    viable, loo_viable = [], []
    for area, dsets in sorted(datasets_by_area.items(), key=lambda kv: -len(kv[1])):
        n = len(dsets)
        if n < args.min_templates or not area:
            continue
        counts = Counter(dsets)
        remaining = n - max(counts.values())
        viable.append(area)
        if remaining >= args.min_templates:
            loo_viable.append((area, remaining))
        emit(f"{area:<14}{n:>5}{len(counts):>10}{remaining:>17}")
    emit()
    emit(f"areas viable before an exact host-dataset exclusion       {len(viable)}")
    emit(f"areas viable after worst-case source-dataset exclusion     {len(loo_viable)}"
         f"  ({', '.join(a for a, _ in loo_viable) if loo_viable else 'none'})")
    emit()
    emit("Read these as screening bounds, not a completed feasibility result. If the chosen host")
    emit("is outside the donor library, no exact-dataset exclusion is needed. If it is inside,")
    emit("exclude that specific source and recompute; the result lies between the two bounds above")
    emit("and equals the worst case only when that source is the area's largest contributor.")
    emit("Both bounds move with the provisional caliper, and neither tests paired-arm balance.")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(report) + "\n")
        print(f"[write] wrote report to {args.out}", flush=True)


if __name__ == "__main__":
    main()
