"""Measure how strongly covariate matching would prefer injection-zone donors.

Tier A's primary control arm draws donors **without conditioning on region**
(Slot 5, Tier A) while being covariate-matched to the region-matched arm. Those
two requirements pull against each other: the templates that match the
injection zone's donors best on amplitude, SNR and depth are, plausibly, the
injection zone's own donors. If a matcher that is blind to region nonetheless
selects zone templates at well above their base rate, the control arm carries a
diluted version of the manipulation and the region contrast is weaker than the
arm labels suggest.

This script measures the size of that pull on the evidence available before a
host is pinned: the donor-metadata snapshot's own covariates.

**Read the boundary with the number.** The real matching runs on *post-rescaling*
amplitude, *effective host* SNR, and depth along the injection band, none of
which exist until a host is selected. The covariates here are their pre-host
analogues from the donor table. So this bounds how plausible the pull is and
whether it is worth writing a rule about; it does not predict the realized
count in the real arm, and it is not evidence that any particular matcher would
behave this way. It also uses a plain nearest-neighbour matcher, because no
matching rule has been predeclared yet -- which is precisely the freedom the
measurement is about.

Stdlib only, and offline when pointed at the tracked snapshot.

Example
-------
Run from the ``Reproducibility Packet`` folder, which is the working directory
every command in ``README.md`` assumes; ``python`` means that folder's own
virtual environment, built in README's Setup section. This is **Step 3** of
that runbook, which also records what the command produced and whether it has
been re-run since:

    python scripts/audit_zone_neighbour_enrichment.py --cache results/templates_snapshot_2026-08-11.csv --zone CA1 --out results/zone_neighbour_enrichment_CA1.txt
"""

import argparse
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import template_metadata as tm  # noqa: E402

COVARIATES = ("amplitude_uv", "signal_to_noise_ratio", "depth_along_probe")


def usable_rows(rows, covariates=COVARIATES):
    """Keep rows carrying a finite value for every covariate.

    Args:
        rows: donor metadata row dicts.
        covariates: column names every kept row must parse as a float.

    Returns:
        A list of (row, values) tuples, values being a tuple of floats in the
        order given by ``covariates``.
    """
    kept = []
    for row in rows:
        values = tuple(tm.as_float(row, name) for name in covariates)
        if any(value is None or not math.isfinite(value) for value in values):
            continue
        kept.append((row, values))
    return kept


def standardize(records, covariates=COVARIATES):
    """Standardize each covariate over the supplied records.

    Args:
        records: (row, values) tuples from :func:`usable_rows`.
        covariates: column names, used only for the error message.

    Returns:
        A list of (row, standardized_values) tuples.

    Raises:
        SystemExit: if any covariate has zero spread, which would make the
            distance below undefined rather than merely uninformative.
    """
    columns = list(zip(*(values for _, values in records)))
    stats = []
    for name, column in zip(covariates, columns):
        mean = statistics.fmean(column)
        sigma = statistics.pstdev(column, mu=mean)
        if sigma == 0.0:
            sys.exit(f"[fatal] covariate {name!r} has zero spread over the pool")
        stats.append((mean, sigma))
    return [(row, tuple((value - mean) / sigma
                        for value, (mean, sigma) in zip(values, stats)))
            for row, values in records]


def key_of(row):
    """Return the globally unique template identifier pair.

    Args:
        row: a donor metadata row dict.

    Returns:
        A (dataset, template_index) tuple. ``template_index`` alone is not an
        identifier -- it restarts inside every dataset.
    """
    return (row.get("dataset", ""), row.get("template_index", ""))


def distance(left, right):
    """Euclidean distance between two standardized covariate vectors.

    Args:
        left, right: equal-length tuples of floats.

    Returns:
        The Euclidean distance as a float.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def neighbour_profile(pool, zone_keys, k_values):
    """For each zone template, count zone members among its k nearest others.

    Args:
        pool: (row, standardized_values) tuples for the whole eligible pool.
        zone_keys: set of identifier pairs belonging to the injection zone.
        k_values: neighbourhood sizes to report.

    Returns:
        A dict mapping k to the fraction of neighbours that are zone members,
        pooled over every zone template.
    """
    hits = {k: 0 for k in k_values}
    total = {k: 0 for k in k_values}
    for row, values in pool:
        if key_of(row) not in zone_keys:
            continue
        others = sorted(
            ((distance(values, other_values), key_of(other_row))
             for other_row, other_values in pool
             if key_of(other_row) != key_of(row)),
            key=lambda item: (item[0], item[1]),
        )
        for k in k_values:
            window = others[:k]
            hits[k] += sum(1 for _, other_key in window if other_key in zone_keys)
            total[k] += len(window)
    return {k: (hits[k], total[k]) for k in k_values}


def greedy_partners(pool, zone_keys, block_insertion=False):
    """Match each zone template to its nearest unused non-self partner.

    This is the crudest region-blind matcher that satisfies "one partner per
    matched-arm slot, drawn without conditioning on region". No matching rule
    has been predeclared, so the crudest one is the honest stand-in.

    Args:
        pool: (row, standardized_values) tuples for the whole eligible pool.
        zone_keys: set of identifier pairs belonging to the injection zone.
        block_insertion: restrict each zone template's candidates to its own
            source insertion, which is the exact-source blocking Amendment 2
            prefers before falling back to session and subject granularity.

    Returns:
        A list of (zone_key, partner_key, partner_is_zone, distance) tuples in
        the deterministic order zone templates are visited. ``partner_key`` is
        None when blocking left no candidate, which is a reportable outcome
        rather than a failure.
    """
    by_key = {key_of(row): values for row, values in pool}
    zone_sorted = sorted(zone_keys)
    used = set()
    partners = []
    for zone_key in zone_sorted:
        values = by_key[zone_key]
        candidates = sorted(
            ((distance(values, other_values), other_key)
             for other_key, other_values in by_key.items()
             if other_key != zone_key and other_key not in used
             and not (block_insertion and other_key[0] != zone_key[0])),
            key=lambda item: (item[0], item[1]),
        )
        if not candidates:
            partners.append((zone_key, None, False, float("nan")))
            continue
        best_distance, partner_key = candidates[0]
        used.add(partner_key)
        partners.append((zone_key, partner_key, partner_key in zone_keys, best_distance))
    return partners


def _injective_zone_expectation(pool_size, zone_count):
    """Expected zone outputs in a uniform no-reuse matching block.

    Each of ``zone_count`` labelled zone templates receives one distinct
    partner from ``pool_size`` candidates, and a template cannot partner with
    itself. Inclusion-exclusion counts the admissible injective assignments.
    The simpler ``zone_count * (zone_count - 1) / (pool_size - 1)`` expression
    treats the slots as independent and is therefore not the right baseline
    for :func:`greedy_partners`, which never reuses a control partner.

    Args:
        pool_size: candidate count in the matching block.
        zone_count: zone-template count in that block.

    Returns:
        Expected number of selected partners that belong to the zone.

    Raises:
        ValueError: if a distinct non-self partner cannot exist for every slot.
    """
    if zone_count == 0:
        return 0.0
    if pool_size < zone_count or pool_size < 2:
        raise ValueError(
            f"no injective non-self matching for pool={pool_size}, zone={zone_count}"
        )
    total = sum(
        (-1) ** fixed * math.comb(zone_count, fixed)
        * math.perm(pool_size - fixed, zone_count - fixed)
        for fixed in range(zone_count + 1)
    )
    without_one_zone_output = sum(
        (-1) ** fixed * math.comb(zone_count - 1, fixed)
        * math.perm(pool_size - 1 - fixed, zone_count - fixed)
        for fixed in range(zone_count)
    )
    return zone_count * (1.0 - without_one_zone_output / total)


def region_blind_expectation(pool, zone_keys, block_insertion=False):
    """Expected zone partners under the matcher's no-reuse constraint.

    Under exact-insertion blocking the comparison is not the pool-wide base
    rate: a zone template's candidates are only its insertion-mates, and zone
    templates cluster inside a few insertions. This function applies the same
    distinct-partner and non-self constraints as :func:`greedy_partners`,
    either over the whole pool or separately within each insertion.

    Args:
        pool: (row, standardized_values) tuples for the whole eligible pool.
        zone_keys: set of identifier pairs belonging to the injection zone.

    Returns:
        The expected number of zone partners across all zone slots, as a float.
    """
    sizes = {}
    zone_counts = {}
    for row, _ in pool:
        insertion = key_of(row)[0] if block_insertion else "__all__"
        sizes[insertion] = sizes.get(insertion, 0) + 1
        if key_of(row) in zone_keys:
            zone_counts[insertion] = zone_counts.get(insertion, 0) + 1
    return sum(
        _injective_zone_expectation(sizes[insertion], count)
        for insertion, count in zone_counts.items()
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--url", default=tm.DEFAULT_CSV_URL,
                        help="donor metadata CSV URL (default: the first-party S3 object)")
    parser.add_argument("--cache", default=None,
                        help="read/write the snapshot here; point at the tracked snapshot to "
                             "run offline against the pinned bytes")
    parser.add_argument("--probe", default="Neuropixels 1.0",
                        help="probe type to restrict to (default: 'Neuropixels 1.0')")
    parser.add_argument("--zone", default="CA1",
                        help="injection-zone donor acronym (default: CA1)")
    parser.add_argument("--amp-lo", type=float, default=50.0,
                        help="lower bound of the provisional caliper sensitivity (default: 50)")
    parser.add_argument("--amp-hi", type=float, default=200.0,
                        help="upper bound of the provisional caliper sensitivity (default: 200)")
    parser.add_argument("--snr-lo", type=float, default=5.0,
                        help="lower SNR caliper for the sensitivity (default: 5)")
    parser.add_argument("--snr-hi", type=float, default=15.0,
                        help="upper SNR caliper for the sensitivity (default: 15)")
    parser.add_argument("--out", default=None,
                        help="path to write the report to (in addition to stdout)")
    args = parser.parse_args()

    payload, digest = tm.fetch_metadata(args.url, cache_path=args.cache)
    rows = tm.parse_rows(payload, probe=args.probe)

    report = []

    def emit(line=""):
        print(line, flush=True)
        report.append(line)

    emit("# Injection-zone neighbour enrichment")
    emit()
    emit(f"snapshot sha256   {digest}")
    emit(f"matches pinned    {digest == tm.PINNED_SHA256}")
    emit(f"probe             {args.probe}")
    emit(f"injection zone    {args.zone}")
    emit(f"covariates        {', '.join(COVARIATES)}")
    emit()
    emit("The real matching uses post-rescaling amplitude, effective host SNR, and depth along")
    emit("the injection band. Those do not exist before a host is pinned; the covariates above")
    emit("are their pre-host analogues. This measures whether a region-blind covariate matcher")
    emit("would be pulled toward injection-zone donors at all, not what the real arm will hold.")
    emit()

    for label, pool_rows in (
        ("full probe subset", rows),
        (f"provisional caliper amp {args.amp_lo}-{args.amp_hi} uV, SNR {args.snr_lo}-{args.snr_hi}",
         [row for row in rows
          if tm.in_caliper(row, args.amp_lo, args.amp_hi, args.snr_lo, args.snr_hi)]),
    ):
        records = usable_rows(pool_rows)
        pool = standardize(records)
        zone_keys = {key_of(row) for row, _ in pool
                     if (row.get("brain_area") or "") == args.zone}
        emit(f"## Pool: {label}")
        emit(f"rows with all covariates      {len(pool)} of {len(pool_rows)}")
        emit(f"{args.zone} templates in pool  {len(zone_keys)}")
        if len(zone_keys) < 2:
            emit(f"fewer than two {args.zone} templates in this pool; enrichment is undefined")
            emit()
            continue
        base_rate = (len(zone_keys) - 1) / (len(pool) - 1)
        emit(f"base rate for a non-self draw  {base_rate * 100:.3f}%")
        emit()
        profile = neighbour_profile(pool, zone_keys, (1, 5, 16))
        emit(f"{'k':>4}{'zone hits':>12}{'of':>8}{'observed':>12}{'enrichment':>13}")
        for k, (hit, total) in sorted(profile.items()):
            observed = hit / total if total else float("nan")
            ratio = observed / base_rate if base_rate else float("nan")
            emit(f"{k:>4}{hit:>12}{total:>8}{observed * 100:>11.2f}%{ratio:>12.1f}x")
        emit()
        for blocked, heading in (
            (False, "Nearest-unused-partner matching, one partner per zone template"),
            (True, "The same matching with exact-insertion blocking (Amendment 2's first "
                   "granularity)"),
        ):
            partners = greedy_partners(pool, zone_keys, block_insertion=blocked)
            matched = [item for item in partners if item[1] is not None]
            zone_partners = sum(1 for _, _, is_zone, _ in matched if is_zone)
            emit(f"{heading}:")
            emit(f"  slots with any candidate                 {len(matched)} of {len(partners)}")
            emit(f"  partners that are themselves {args.zone}"
                 f"{'':<{max(0, 12 - len(args.zone))}}{zone_partners} of {len(matched)}")
            expected = region_blind_expectation(
                pool, zone_keys, block_insertion=blocked
            )
            emit(f"  expected under region-blind no-reuse matching  {expected:.2f}")
            if matched:
                distances = [item[3] for item in matched]
                emit(f"  partner distance  min {min(distances):.3f}  "
                     f"median {statistics.median(distances):.3f}  max {max(distances):.3f}")
            emit()
            for zone_key, partner_key, is_zone, dist in partners:
                if partner_key is None:
                    emit(f"  {zone_key[0][:44]:<44} {zone_key[1]:>4}  ->  "
                         f"{'(no candidate under blocking)':<44}")
                    continue
                mark = "  <- zone" if is_zone else ""
                emit(f"  {zone_key[0][:44]:<44} {zone_key[1]:>4}  ->  "
                     f"{partner_key[0][:44]:<44} {partner_key[1]:>4}  d={dist:.3f}{mark}")
            emit()

    emit("Compare the two matchings on the realized count, not on the ratio. Blocking raises")
    emit("the number of zone partners because it shrinks each candidate set to a neighbourhood")
    emit("the zone's own members already occupy; part of that rise is what a region-blind draw")
    emit("under the same blocking would give anyway, which is what the expectation line is for.")
    emit("The ratio to expectation can fall while the realized contamination rises, and it is")
    emit("the realized count that dilutes the manipulation.")
    emit()
    emit("Read this as a statement about the pull, not about the outcome. A matcher that is")
    emit("blind to region is not thereby neutral about it: if zone donors sit at the centre of")
    emit("the covariate neighbourhood the matcher is searching, the control arm inherits them")
    emit("unless a rule says otherwise. Whether that rule should exclude them, cap them, or")
    emit("merely report them is a contract question, not a measurement one.")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write("\n".join(report) + "\n")
        print(f"[write] wrote report to {args.out}", flush=True)


if __name__ == "__main__":
    main()
