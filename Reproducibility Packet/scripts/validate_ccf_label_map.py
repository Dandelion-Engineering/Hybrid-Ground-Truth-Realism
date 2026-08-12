"""Validate the CCF long-name to acronym map against the donor library itself.

`utils/ccf_labels.py` is hand-authored. Tier A's whole manipulation rests on it:
if "Field CA1" does not in fact mean the acronym ``CA1``, then a "region-matched"
arm is matched to the wrong structure and every downstream number is about
something else. A hand-written table is exactly the kind of artifact that looks
obviously right and is quietly wrong in two entries.

There is independent evidence available, and it costs almost nothing to use.
Every Neuropixels 1.0 donor template is drawn from a DANDI 000409 session, and
carries both a ``brain_area`` acronym and a ``depth_along_probe``. The same
session's NWB file carries a CCF long name for every electrode, with the
electrode's position along the probe. So for each donor the two vocabularies can
be compared at the same physical place on the same probe:

    donor says   (session S, depth 2900 um) is ``CA1``
    host says    (session S, depth 2900 um) is "Field CA1"

Agreement confirms both the label map *and* that ``depth_along_probe`` and the
NWB's ``rel_y`` are the same coordinate -- which Tier A's placement depends on
just as much, and which nothing else in the project has checked.

Disagreement is reported per acronym rather than aggregated, because one wrong
row is a data quirk and one wrong *structure* is a broken table entry.

Example
-------
    ./venv/Scripts/python.exe "Reproducibility Packet/scripts/validate_ccf_label_map.py" \
        --assets-cache "Reproducibility Packet/results/dandi_000409_assets.json" \
        --out "Reproducibility Packet/results/ccf_label_map_validation.txt"
"""

import argparse
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import h5py  # noqa: E402

from utils import ccf_labels, dandi  # noqa: E402
from utils import template_metadata as tm  # noqa: E402
from utils.remote_hdf5 import RemoteFile  # noqa: E402

ELECTRODES_PATH = "general/extracellular_ephys/electrodes"


def read_probe_depth_labels(url, size, block_bytes):
    """Read per-probe (depth, CCF long name) pairs from a remote NWB.

    Args:
        url: direct S3 URL of the NWB blob.
        size: blob size in bytes.
        block_bytes: HTTP range-request block size.

    Returns:
        A dict from probe name to a list of (depth_um, location) tuples.

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
    return dict(probes)


def score_probe(donor_rows, depth_labels, tolerance_um):
    """Score how well one probe's annotation agrees with a donor insertion.

    Args:
        donor_rows: donor row dicts from one template-library insertion.
        depth_labels: (depth_um, location) tuples for one probe.
        tolerance_um: how far from a donor's depth an electrode may sit and
            still be treated as describing the same place.

    Returns:
        A tuple of (agreements, comparisons, per-acronym Counter of outcomes),
        where an outcome is ``"agree"``, ``"disagree"``, ``"unmapped"``, or
        ``"undefined"``. ``comparisons`` counts only rows the table could in
        principle have got right -- ``undefined`` rows are excluded from it.
    """
    defined = set(ccf_labels.NAME_TO_ACRONYM.values())
    outcomes = Counter()
    agreements = comparisons = 0
    for row in donor_rows:
        depth = tm.as_float(row, "depth_along_probe")
        acronym = (row.get("brain_area") or "").strip()
        if depth is None or not acronym:
            continue
        nearby = [location for electrode_depth, location in depth_labels
                  if abs(electrode_depth - depth) <= tolerance_um]
        if not nearby:
            continue
        # A donor acronym the table does not define can never agree, whatever
        # the host says. Counting those as disagreements would blame the table
        # for its incompleteness and, worse, disguise it as an incorrectness.
        if acronym not in defined:
            outcomes[(acronym, "undefined")] += 1
            continue
        comparisons += 1
        mapped = {ccf_labels.to_acronym(location) for location in nearby}
        if acronym in mapped:
            agreements += 1
            outcomes[(acronym, "agree")] += 1
        elif mapped == {None}:
            outcomes[(acronym, "unmapped")] += 1
        else:
            outcomes[(acronym, "disagree")] += 1
    return agreements, comparisons, outcomes


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
                        help="asset suffix to read electrode tables from. The processed file "
                             f"carries the same table as the raw one (default: "
                             f"{dandi.PROCESSED_SUFFIX!r})")
    parser.add_argument("--tolerance-um", type=float, default=20.0,
                        help="depth tolerance when matching a donor to electrodes "
                             "(default: 20, one Neuropixels 1.0 contact row)")
    parser.add_argument("--block-kb", type=int, default=1024,
                        help="HTTP range block size in KiB (default: 1024)")
    parser.add_argument("--limit", type=int, default=None,
                        help="validate at most this many donor sessions")
    parser.add_argument("--out", default=None, help="path to write the report to")
    args = parser.parse_args()

    if args.tolerance_um < 0:
        sys.exit("[fatal] --tolerance-um must not be negative")

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

    report = []

    def emit(line=""):
        print(line, flush=True)
        report.append(line)

    emit("# CCF label-map validation")
    emit()
    emit(f"donor snapshot sha256   {digest}")
    emit(f"matches pinned          {digest == tm.PINNED_SHA256}")
    emit(f"probe type              {args.probe_type}")
    emit(f"donor insertions        {len(by_insertion)} (validating {len(insertions)})")
    emit(f"depth tolerance         {args.tolerance_um} um")
    emit(f"electrode table source  {args.suffix}")
    emit()

    totals = Counter()
    missing_sessions = []
    failures = []
    probe_choices = []

    for number, (session, insertion) in enumerate(insertions, start=1):
        asset = asset_by_session.get(session)
        if asset is None:
            missing_sessions.append(session)
            print(f"[{number}/{len(insertions)}] session {session[:8]} not in dandiset listing",
                  flush=True)
            continue
        try:
            probes = read_probe_depth_labels(dandi.blob_url(asset), asset["size"],
                                             args.block_kb * 1024)
        except (OSError, KeyError, ValueError) as exc:
            failures.append((session, f"{type(exc).__name__}: {exc}"))
            print(f"[{number}/{len(insertions)}] FAILED {session[:8]}: {exc}", flush=True)
            continue

        # A session can hold more than one probe and the donor 'dataset' string
        # does not say which. Score every probe and keep the best-agreeing one,
        # which is the only defensible assignment available from metadata alone.
        best = None
        for probe, depth_labels in probes.items():
            agreements, comparisons, outcomes = score_probe(
                by_insertion[(session, insertion)], depth_labels, args.tolerance_um)
            if comparisons and (best is None or agreements > best[1]):
                best = (probe, agreements, comparisons, outcomes)
        if best is None:
            # Either no electrode sat within tolerance of any donor depth, or
            # every donor here carries an acronym the table does not define.
            # Both leave nothing testable; neither is evidence against the table.
            failures.append((session, "no testable comparison: no depth overlap, or every donor "
                                      "acronym in this insertion is undefined in the table"))
            continue
        probe, agreements, comparisons, outcomes = best
        totals.update(outcomes)
        probe_choices.append((session, probe, agreements, comparisons, len(probes)))
        rate = agreements / comparisons if comparisons else 0.0
        print(f"[{number}/{len(insertions)}] {session[:8]} {probe:<9} "
              f"{agreements:>4}/{comparisons:<4} agree ({rate:6.1%})", flush=True)

    emit("## Per-structure agreement")
    emit()
    emit("Only donor acronyms the table actually defines can be tested. For those, 'agree' means")
    emit("the donor's acronym is among the acronyms the host annotation maps to at the same depth,")
    emit("'disagree' means the host names a different structure there, and 'unmapped' means the")
    emit("host's label has no table entry so nothing could be concluded. 'undefined' rows are")
    emit("donor acronyms absent from the table entirely -- they measure its coverage, not its")
    emit("correctness, and are excluded from the rate.")
    emit()
    emit(f"{'acronym':<12}{'agree':>8}{'disagree':>10}{'unmapped':>10}{'undefined':>11}{'rate':>9}")
    emit("-" * 60)
    # Five buckets, not two. A single disagreement among thirty-four agreements
    # is not the same finding as thirty-four disagreements and no agreements,
    # and neither is the same as a donor acronym the table never claimed to
    # define -- which cannot agree no matter how correct the table is.
    acronyms = sorted({key[0] for key in totals})
    confirmed, mixed, contradicted, untested, undefined = [], [], [], [], []
    for acronym in acronyms:
        agree = totals[(acronym, "agree")]
        disagree = totals[(acronym, "disagree")]
        unmapped = totals[(acronym, "unmapped")]
        undef = totals[(acronym, "undefined")]
        decided = agree + disagree
        rate = f"{agree / decided:.1%}" if decided else "-"
        emit(f"{acronym:<12}{agree:>8}{disagree:>10}{unmapped:>10}{undef:>11}{rate:>9}")
        if undef and not (agree or disagree or unmapped):
            undefined.append(f"{acronym} ({undef})")
        elif agree and not disagree:
            confirmed.append(acronym)
        elif agree and disagree:
            mixed.append(f"{acronym} ({agree}/{decided})")
        elif disagree:
            contradicted.append(f"{acronym} (0/{decided})")
        else:
            untested.append(acronym)
    emit()
    total_agree = sum(v for k, v in totals.items() if k[1] == "agree")
    total_disagree = sum(v for k, v in totals.items() if k[1] == "disagree")
    total_unmapped = sum(v for k, v in totals.items() if k[1] == "unmapped")
    total_undefined = sum(v for k, v in totals.items() if k[1] == "undefined")
    emit(f"donor rows placed        "
         f"{total_agree + total_disagree + total_unmapped + total_undefined}")
    emit(f"testable (acronym defined in the table)  "
         f"{total_agree + total_disagree + total_unmapped}")
    emit(f"  agree                  {total_agree}")
    emit(f"  disagree               {total_disagree}")
    emit(f"  host label unmapped    {total_unmapped}")
    emit(f"not testable (donor acronym undefined)   {total_undefined}")
    emit()

    emit("## Verdicts")
    emit()
    emit(f"CONFIRMED, no disagreement ({len(confirmed)}): "
         f"{', '.join(confirmed) if confirmed else 'none'}")
    emit()
    emit(f"MIXED, mostly agreeing ({len(mixed)}): {', '.join(mixed) if mixed else 'none'}")
    emit()
    emit(f"CONTRADICTED, defined but never agreed ({len(contradicted)}): "
         f"{', '.join(contradicted) if contradicted else 'none'}")
    emit()
    emit(f"UNDEFINED, donor acronym not in the table ({len(undefined)}): "
         f"{', '.join(undefined) if undefined else 'none'}")
    emit()
    emit("Read the four lists differently, and note which two are about correctness. A CONFIRMED")
    emit("entry is safe to use as an injection zone label. A MIXED entry is most likely correct")
    emit("with a boundary effect: the depth tolerance admits neighbouring contacts, so a donor at")
    emit("a structure border can be compared against its neighbour's label. A CONTRADICTED entry")
    emit("is the one that means the table is wrong -- it defines the acronym and never once")
    emit("matched -- and must be diagnosed before use. An UNDEFINED entry says nothing about")
    emit("correctness at all: the table never claimed to define that acronym, so no host")
    emit("annotation could have agreed with it. Those measure coverage, and the number to read")
    emit("them against is the count of structures the table would need for a region-unaware arm.")
    emit()
    zero_probes = [(session, probe, compared)
                   for session, probe, agreements, compared, _ in probe_choices
                   if agreements == 0]
    if zero_probes:
        emit(f"**{len(zero_probes)} donor insertion(s) matched no probe at all.** Their testable")
        emit("rows all count as disagreements, so they inflate that column without being evidence")
        emit("about the table. The likely cause is the probe assignment: the donor 'dataset'")
        emit("string names an insertion UUID the NWB does not carry, and a session with two")
        emit("probes offers no other way to tell them apart.")
        emit()
        for session, probe, compared in zero_probes:
            emit(f"  {session[:8]}  {probe}  0/{compared}")
        emit()
    mapped_acronyms = set(ccf_labels.NAME_TO_ACRONYM.values())
    never_seen = sorted(mapped_acronyms - set(acronyms))
    emit(f"in the table but never tested here ({len(never_seen)}): "
         f"{', '.join(never_seen) if never_seen else 'none'}")
    emit()

    if probe_choices:
        emit("## Probe assignment per donor insertion")
        emit()
        emit("The donor 'dataset' string names an insertion UUID that the NWB does not carry, so")
        emit("the probe with the highest agreement was assigned. A session with one probe is")
        emit("unambiguous; a two-probe session where agreement is high is strong evidence the")
        emit("assignment is right.")
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

    emit("This validates the label map and the depth-coordinate correspondence. It does not")
    emit("validate the atlas registration itself, which is IBL's and is inherited as given.")

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write("\n".join(report) + "\n")
        print(f"[write] wrote report to {args.out}", flush=True)


if __name__ == "__main__":
    main()
