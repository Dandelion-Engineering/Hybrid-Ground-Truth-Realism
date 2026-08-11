"""Audit the SpikeInterface hybrid template library for region-arm feasibility.

The project's region-matching axis requires that, for some brain area, the
template library holds enough templates to build a *matched* arm (donor
templates from the host recording's area) and a *mismatched* arm (donor
templates from a distant area), with amplitude and signal-to-noise ratio
balanced across both so that a realism effect is not an amplitude effect in
disguise.

This script answers whether that is possible, and under what constraints. It:

1. downloads the first-party ``templates.csv`` and records its SHA-256, ETag,
   and Last-Modified, because the table is hosted mutably and any result built
   on it must pin the snapshot it used;
2. reports row counts, probe types, source datasets, and amplitude/SNR ranges;
3. counts, per brain area, how many templates survive an amplitude and SNR
   caliper; and
4. runs a leave-one-dataset-out stress test: for each area, how many templates
   remain after dropping its single largest contributing source dataset. This
   is the binding number when the host recording comes from a dataset that also
   contributed donor templates, because reusing the host's own dataset as a
   donor is a leakage path.

Stdlib only, deliberately: this is a 2 MB CSV and a few group-bys, and the
project should not acquire a dependency to answer it.

Example
-------
    python audit_template_library.py --out ../results/template_audit.txt
"""

import argparse
import csv
import hashlib
import io
import statistics
import sys
import urllib.error
import urllib.request
from collections import Counter, defaultdict

DEFAULT_CSV_URL = "https://spikeinterface-template-database.s3.amazonaws.com/templates.csv"

# Snapshot observed on 2026-08-11 by both agents independently. A mismatch does
# not mean the script is wrong; it means the upstream table moved and every
# downstream selection must be re-derived against the new snapshot.
KNOWN_SHA256 = "a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d"


def fetch_csv(url):
    """Download the metadata CSV.

    Args:
        url: HTTP(S) location of the templates metadata CSV.

    Returns:
        A tuple of (payload_bytes, sha256_hex, response_headers_dict).

    Raises:
        SystemExit: if the URL cannot be retrieved, with the underlying reason.
    """
    print(f"[fetch] {url}", flush=True)
    try:
        with urllib.request.urlopen(url, timeout=180) as resp:
            headers = dict(resp.headers)
            payload = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        sys.exit(f"[fatal] could not retrieve {url}: {exc}")
    digest = hashlib.sha256(payload).hexdigest()
    print(f"[fetch] {len(payload)} bytes", flush=True)
    return payload, digest, headers


def parse_rows(payload):
    """Parse CSV bytes into a list of row dicts.

    Args:
        payload: raw CSV bytes.

    Returns:
        List of dicts, one per data row, keyed by column name.
    """
    rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8"))))
    if not rows:
        sys.exit("[fatal] metadata CSV parsed to zero rows")
    return rows


def as_float(row, key):
    """Read a numeric cell tolerantly.

    Args:
        row: a CSV row dict.
        key: column name to read.

    Returns:
        The cell as a float, or None if blank or unparseable.
    """
    raw = (row.get(key) or "").strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def in_caliper(row, amp_lo, amp_hi, snr_lo, snr_hi):
    """Test whether a template falls inside the amplitude and SNR caliper.

    Args:
        row: a CSV row dict.
        amp_lo, amp_hi: inclusive amplitude bounds in microvolts.
        snr_lo, snr_hi: inclusive signal-to-noise-ratio bounds.

    Returns:
        True if both covariates are present and inside their bounds.
    """
    amp = as_float(row, "amplitude_uv")
    snr = as_float(row, "signal_to_noise_ratio")
    if amp is None or snr is None:
        return False
    return amp_lo <= amp <= amp_hi and snr_lo <= snr <= snr_hi


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--url", default=DEFAULT_CSV_URL,
                        help="template metadata CSV URL (default: the first-party S3 object)")
    parser.add_argument("--probe", default="Neuropixels 1.0",
                        help="probe type to audit (default: 'Neuropixels 1.0', the IBL subset)")
    parser.add_argument("--amp-lo", type=float, default=50.0,
                        help="lower amplitude caliper in uV (default: 50, the anchor paper's "
                             "rescaling floor)")
    parser.add_argument("--amp-hi", type=float, default=200.0,
                        help="upper amplitude caliper in uV (default: 200, the anchor paper's "
                             "rescaling ceiling)")
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

    payload, digest, headers = fetch_csv(args.url)
    report = []

    def emit(line=""):
        print(line, flush=True)
        report.append(line)

    emit("# Template library audit")
    emit()
    emit(f"url             {args.url}")
    emit(f"bytes           {len(payload)}")
    emit(f"sha256          {digest}")
    emit(f"matches pinned  {digest == KNOWN_SHA256}  (pinned = {KNOWN_SHA256})")
    emit(f"etag            {headers.get('ETag')}")
    emit(f"last-modified   {headers.get('Last-Modified')}")
    emit()

    rows = parse_rows(payload)
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
    amps = [a for a in (as_float(r, "amplitude_uv") for r in subset) if a is not None]
    snrs = [s for s in (as_float(r, "signal_to_noise_ratio") for r in subset) if s is not None]
    emit(f"amplitude_uv    min {min(amps):.2f}  median {statistics.median(amps):.2f}  "
         f"max {max(amps):.2f}")
    emit(f"snr             min {min(snrs):.2f}  median {statistics.median(snrs):.2f}  "
         f"max {max(snrs):.2f}")
    emit(f"distinct brain_area labels  {len({r.get('brain_area', '') for r in subset})}")
    emit()

    kept = [r for r in subset
            if in_caliper(r, args.amp_lo, args.amp_hi, args.snr_lo, args.snr_hi)]
    emit(f"## Caliper: amplitude {args.amp_lo}-{args.amp_hi} uV, SNR {args.snr_lo}-{args.snr_hi}")
    emit(f"rows inside caliper         {len(kept)} of {len(subset)}")
    emit(f"distinct areas inside       {len({r.get('brain_area', '') for r in kept})}")
    emit()

    datasets_by_area = defaultdict(list)
    for r in kept:
        datasets_by_area[r.get("brain_area", "")].append(r.get("dataset", ""))

    emit(f"## Areas with at least {args.min_templates} in-caliper templates")
    emit()
    emit("The 'leave-one-out' column is the count remaining after dropping the area's single")
    emit("largest contributing source dataset. It is the binding number when the host recording")
    emit("comes from a dataset that also contributed donor templates, since reusing the host's")
    emit("own dataset as a donor is a leakage path.")
    emit()
    emit(f"{'area':<14}{'n':>5}{'datasets':>10}{'leave-one-out':>15}")
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
        emit(f"{area:<14}{n:>5}{len(counts):>10}{remaining:>15}")
    emit()
    emit(f"areas viable, host dataset NOT in the library      {len(viable)}")
    emit(f"areas viable, host dataset excluded as a donor     {len(loo_viable)}"
         f"  ({', '.join(a for a, _ in loo_viable) if loo_viable else 'none'})")
    emit()
    emit("Read this as a conditional, not a count: if the chosen host recording is not one of")
    emit("the library's own source datasets, the first number applies. If it is, the second does.")
    emit("Both numbers move with the caliper, which is a declared parameter and not a fact.")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(report) + "\n")
        print(f"[write] wrote report to {args.out}", flush=True)


if __name__ == "__main__":
    main()
