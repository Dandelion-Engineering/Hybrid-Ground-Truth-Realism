"""Read the acquisition provenance of DANDI 000409 subjects from their own NWB files.

Tier A's donor templates and its host recording both come from DANDI 000409, so
the project cannot claim that donor and host are independently sourced. The
Claim Sheet states that residual as a limitation, and the honest version of that
sentence depends on *which* provenance dimensions were actually checked.

This script checks the ones the substrate can answer. Every 000409 raw NWB
carries ``/general/lab``, ``/general/institution``, ``/general/protocol``,
``/general/subject`` and ``/general/ibl_metadata``. IBL is a multi-laboratory
consortium, so two subjects sharing a dandiset need not share a laboratory or
institution. These fields do not identify rig hardware or rig design, so those
remain separate questions rather than being inferred from the lab label.

It also establishes a negative that matters as much as the positives: **these
files carry no genotype or strain field.** Any statement about mouse strain is
therefore unverifiable from this project's own inputs and must be reported as
unverified rather than as either shared or different.

One raw asset is read per subject, over HTTP range requests, with a 1 MiB block
size. Only the file's metadata header is touched -- roughly 2 MB per subject
against files of 18-197 GB. No recording data is downloaded.

Example
-------
Run from the ``Reproducibility Packet`` folder, which is the working directory
every command in ``README.md`` assumes; ``python`` means that folder's own
virtual environment, built in README's Setup section. This is **Step 9** of
that runbook, which also records what the command produced and whether it has
been re-run since:

    python scripts/audit_subject_provenance.py --donor-subjects KS042,KS043,KS044,KS046,KS051,KS052,KS055,KS084,KS086,KS091,KS094,KS096 --host-subjects CSHL045,CSHL047,CSHL049,NYU-12,NYU-37,NYU-39,NYU-45,NYU-48,NYU-65 --assets results/dandi_000409_assets.json --records results/subject_provenance.json --out results/subject_provenance.txt
"""

import argparse
import json
import os
import sys
from collections import Counter, OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import h5py  # noqa: E402

from utils import dandi  # noqa: E402
from utils.remote_hdf5 import RemoteFile  # noqa: E402

# Scalar datasets read from /general when present. Absence is recorded, never
# guessed: a missing field is evidence about what the substrate documents.
GENERAL_FIELDS = ("lab", "institution", "protocol", "session_id", "source_script")
SUBJECT_FIELDS = ("subject_id", "species", "sex", "date_of_birth", "weight",
                  "genotype", "strain", "description")
IBL_FIELDS = ("revision",)


def _scalar(node, key):
    """Read one scalar dataset from an h5py group, decoding bytes.

    Args:
        node: an ``h5py.Group``.
        key: dataset name to read.

    Returns:
        The decoded value, or None when the dataset is absent.
    """
    if key not in node:
        return None
    value = node[key][()]
    if isinstance(value, bytes):
        return value.decode()
    return value


def read_provenance(asset, block_bytes, timeout):
    """Read one recording's acquisition-provenance metadata.

    Args:
        asset: a DANDI asset dict from ``utils.dandi.list_assets``.
        block_bytes: HTTP range-request block size in bytes.
        timeout: per-request timeout in seconds.

    Returns:
        A JSON-serialisable record of the asset's identity, its ``/general``
        fields, its ``/general/subject`` fields, and the bytes it cost.

    Raises:
        KeyError: if the file has no ``/general`` group, which is malformed and
            must be reported rather than skipped.
    """
    remote = RemoteFile(dandi.blob_url(asset), asset["size"], block=block_bytes,
                        timeout=timeout)
    record = {
        "subject": dandi.subject_of(asset),
        "session": dandi.session_of(asset),
        "asset_id": asset["asset_id"],
        "path": asset["path"],
        "general": {},
        "subject_fields": {},
        "ibl_metadata": {},
    }
    with h5py.File(remote, "r") as handle:
        if "general" not in handle:
            raise KeyError(f"{asset['path']} has no /general group")
        general = handle["general"]
        for field in GENERAL_FIELDS:
            record["general"][field] = _scalar(general, field)
        if "subject" in general:
            for field in SUBJECT_FIELDS:
                record["subject_fields"][field] = _scalar(general["subject"], field)
        if "ibl_metadata" in general:
            for field in IBL_FIELDS:
                record["ibl_metadata"][field] = _scalar(general["ibl_metadata"], field)
    record["io"] = {"requests": remote.n_requests, "bytes": remote.n_bytes}
    return record


def pick_asset(assets, subject, suffix):
    """Return the first asset belonging to one subject, ordered by path.

    Args:
        assets: the dandiset's asset listing.
        subject: subject identifier, e.g. ``"KS042"``.
        suffix: asset filename suffix to require.

    Returns:
        The chosen asset dict, or None when the subject has no matching asset.
        Ordering by path makes the choice deterministic across runs.
    """
    matches = sorted((a for a in assets
                      if a["path"].endswith(suffix) and dandi.subject_of(a) == subject),
                     key=lambda a: a["path"])
    return matches[0] if matches else None


def _group_counts(records, getter):
    """Count records by a derived key, preserving descending-count order."""
    return OrderedDict(Counter(getter(r) or "<absent>" for r in records).most_common())


def write_report(path, donor_records, host_records, missing, absent_fields, args):
    """Write the human-readable provenance report.

    Args:
        path: output file path.
        donor_records: provenance records for donor-library subjects.
        host_records: provenance records for candidate host subjects.
        missing: subjects for which no asset was found.
        absent_fields: subject-level fields absent from every file read.
        args: parsed command-line arguments, for the report header.
    """
    lab = lambda r: r["general"].get("lab")  # noqa: E731
    inst = lambda r: r["general"].get("institution")  # noqa: E731
    protocol = lambda r: r["general"].get("protocol")  # noqa: E731
    lines = []
    lines.append("# Subject acquisition provenance")
    lines.append("")
    lines.append(f"dandiset            {args.dandiset} ({args.version})")
    lines.append(f"asset suffix        {args.suffix}")
    lines.append(f"donor subjects      {len(donor_records)} read")
    lines.append(f"host subjects       {len(host_records)} read")
    lines.append(f"block size          {args.block_bytes} bytes")
    total_bytes = sum(r["io"]["bytes"] for r in donor_records + host_records)
    total_requests = sum(r["io"]["requests"] for r in donor_records + host_records)
    lines.append(f"metadata read       {total_bytes} bytes in {total_requests} requests")
    if missing:
        lines.append(f"subjects not found  {', '.join(missing)}")
    lines.append("")

    lines.append("## Fields the substrate does not carry")
    lines.append("")
    if absent_fields:
        lines.append("These subject-level fields are absent from every file read, so any")
        lines.append("claim about them is unverifiable from this project's own inputs and")
        lines.append("must be reported as unverified rather than as shared or different:")
        lines.append("")
        for field in absent_fields:
            lines.append(f"  - {field}")
    else:
        lines.append("Every requested subject field was present in at least one file.")
    lines.append("")

    for title, records in (("Donor-library subjects", donor_records),
                           ("Candidate host subjects", host_records)):
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"{'subject':<10} {'lab':<16} {'institution':<44} {'sex':<4} protocol")
        lines.append("-" * 120)
        for record in sorted(records, key=lambda r: r["subject"]):
            lines.append("{:<10} {:<16} {:<44} {:<4} {}".format(
                record["subject"],
                str(lab(record))[:16],
                str(inst(record))[:44],
                str(record["subject_fields"].get("sex"))[:4],
                str(record["general"].get("protocol")),
            ))
        lines.append("")
        lines.append(f"labs: {json.dumps(_group_counts(records, lab))}")
        lines.append(f"institutions: {json.dumps(_group_counts(records, inst))}")
        lines.append(f"protocols: {json.dumps(_group_counts(records, protocol))}")
        lines.append("")

    donor_labs = {lab(r) for r in donor_records}
    host_labs = {lab(r) for r in host_records}
    lines.append("## Donor/host laboratory overlap")
    lines.append("")
    lines.append(f"donor labs                {sorted(x for x in donor_labs if x)}")
    lines.append(f"host-candidate labs       {sorted(x for x in host_labs if x)}")
    lines.append(f"shared labs               {sorted(x for x in donor_labs & host_labs if x)}")
    lines.append(f"host labs free of donors  {sorted(x for x in host_labs - donor_labs if x)}")
    lines.append("")
    lines.append("A host subject from a laboratory that contributed no donor templates")
    lines.append("separates host and donor at the laboratory and institution level as well")
    lines.append("as at the animal level. Different institutions necessarily exclude one")
    lines.append("shared physical acquisition rig, but these fields do not identify rig")
    lines.append("hardware or establish whether the laboratories used the same rig design.")
    lines.append("This is still not source independence: both sides remain one dandiset,")
    lines.append("one consortium, one acquisition program and one probe type.")
    lines.append("")

    donor_protocols = {protocol(r) for r in donor_records if protocol(r)}
    host_protocols = {protocol(r) for r in host_records if protocol(r)}
    lines.append("## Donor/host task-protocol overlap")
    lines.append("")
    lines.append(f"donor protocols            {sorted(donor_protocols)}")
    lines.append(f"host-candidate protocols   {sorted(host_protocols)}")
    lines.append(f"shared protocols           {sorted(donor_protocols & host_protocols)}")
    lines.append("")
    if donor_protocols == host_protocols:
        lines.append("The protocol sets are identical in the tracked records.")
    elif donor_protocols & host_protocols:
        lines.append("The protocol sets partly overlap in the tracked records; they are")
        lines.append("neither identical nor disjoint.")
    else:
        lines.append("The protocol sets are disjoint in the tracked records.")
    lines.append("")

    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--donor-subjects", required=True,
                        help="comma-separated subjects that contributed donor templates")
    parser.add_argument("--host-subjects", required=True,
                        help="comma-separated candidate host subjects")
    parser.add_argument("--assets", required=True,
                        help="path to the cached DANDI asset listing (JSON)")
    parser.add_argument("--out", required=True, help="path of the report to write")
    parser.add_argument("--records", default=None,
                        help="optional path for the raw JSON records")
    parser.add_argument("--dandiset", default="000409", help="dandiset identifier")
    parser.add_argument("--version", default="draft", help="dandiset version")
    parser.add_argument("--suffix", default=dandi.RAW_SUFFIX,
                        help="asset filename suffix to read")
    parser.add_argument("--block-bytes", type=int, default=1024 * 1024,
                        help="HTTP range-request block size in bytes")
    parser.add_argument("--timeout", type=int, default=180,
                        help="per-request timeout in seconds")
    return parser.parse_args(argv)


def main(argv=None):
    """Read provenance for every named subject and write the report."""
    args = parse_args(argv)
    assets = dandi.list_assets(args.dandiset, version=args.version,
                               cache_path=args.assets, verbose=True)
    donor_subjects = [s.strip() for s in args.donor_subjects.split(",") if s.strip()]
    host_subjects = [s.strip() for s in args.host_subjects.split(",") if s.strip()]
    overlap = sorted(set(donor_subjects) & set(host_subjects))
    if overlap:
        raise SystemExit(f"donor and host subject lists overlap: {overlap}. "
                         "A host subject may not also be a donor subject.")

    records = {"donor": [], "host": []}
    missing = []
    for role, subjects in (("donor", donor_subjects), ("host", host_subjects)):
        for subject in subjects:
            asset = pick_asset(assets, subject, args.suffix)
            if asset is None:
                print(f"[{role}] {subject}: no asset with suffix {args.suffix}", flush=True)
                missing.append(subject)
                continue
            record = read_provenance(asset, args.block_bytes, args.timeout)
            record["role"] = role
            records[role].append(record)
            print("[{}] {:<10} lab={:<16} institution={} ({} bytes)".format(
                role, subject, str(record["general"].get("lab")),
                record["general"].get("institution"), record["io"]["bytes"]), flush=True)

    everything = records["donor"] + records["host"]
    if not everything:
        raise SystemExit("no subject could be read; refusing to write an empty report")
    absent_fields = [field for field in SUBJECT_FIELDS
                     if all(r["subject_fields"].get(field) is None for r in everything)]

    write_report(args.out, records["donor"], records["host"], missing, absent_fields, args)
    print(f"wrote {args.out}", flush=True)
    if args.records:
        with open(args.records, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(everything, handle, indent=1, sort_keys=True)
        print(f"wrote {args.records}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
