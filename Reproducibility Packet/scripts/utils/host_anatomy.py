"""Read host electrode geometry and find contiguous anatomical bands.

Two screening scripts need the same two operations on a candidate host: read
the NWB electrodes table without downloading the recording, and find the
largest run of contacts carrying one structure label. ``survey_host_anatomy.py``
uses them to rank hosts by injection-zone size; ``screen_injection_placement.py``
uses them to test whether ten injected units fit inside the zone it found.

They live here so both scripts call one implementation. A second copy would
drift, and the two scripts must agree on the band exactly, or the placement
screen would be measuring a different band than the one that was ranked.
"""

from collections import OrderedDict

import h5py

from utils import ccf_labels
from utils.remote_hdf5 import RemoteFile

ELECTRODES_PATH = "general/extracellular_ephys/electrodes"


def read_electrode_table(url, size, block_bytes):
    """Read one NWB file's electrodes table without downloading the recording.

    Args:
        url: direct S3 URL of the NWB blob.
        size: the blob's size in bytes.
        block_bytes: HTTP range-request block size.

    Returns:
        A dict with ``probes`` (an ordered mapping from probe name to a list of
        per-electrode dicts), ``series`` (AP acquisition series descriptions),
        and ``io`` (request count and bytes transferred).

    Raises:
        KeyError: if the file has no electrodes table, which is a malformed
            host and must be reported rather than skipped silently.
    """
    remote = RemoteFile(url, size, block=block_bytes)
    probes = OrderedDict()
    series = []
    with h5py.File(remote, "r") as handle:
        if ELECTRODES_PATH not in handle:
            raise KeyError(f"{url} has no {ELECTRODES_PATH}")
        table = handle[ELECTRODES_PATH]
        locations = [value.decode() if isinstance(value, bytes) else str(value)
                     for value in table["location"][:]]
        groups = [value.decode() if isinstance(value, bytes) else str(value)
                  for value in table["group_name"][:]]
        ids = table["id"][:].tolist()
        depths = table["rel_y"][:].tolist() if "rel_y" in table else [None] * len(ids)
        lateral = table["rel_x"][:].tolist() if "rel_x" in table else [None] * len(ids)
        for index, probe in enumerate(groups):
            probes.setdefault(probe, []).append({
                "id": ids[index],
                "location": locations[index],
                "acronym": ccf_labels.to_acronym(locations[index]),
                "depth_um": depths[index],
                "lateral_um": lateral[index],
            })
        # List names first and open only the AP series. Iterating the whole
        # acquisition group would force h5py to read every member's object
        # header, and a raw IBL file holds fourteen of them -- the video and
        # event series alone triple the bytes this screen has to transfer.
        acquisition = handle["acquisition"] if "acquisition" in handle else {}
        for name in [key for key in acquisition.keys() if key.endswith("AP")]:
            node = acquisition[name]
            if "data" not in node:
                continue
            entry = {"name": name, "shape": list(node["data"].shape)}
            if "starting_time" in node:
                entry["rate_hz"] = float(node["starting_time"].attrs.get("rate", float("nan")))
            if entry.get("rate_hz") and entry["shape"]:
                entry["duration_s"] = entry["shape"][0] / entry["rate_hz"]
            series.append(entry)
    return {
        "probes": probes,
        "series": series,
        "io": {"requests": remote.n_requests, "bytes": remote.n_bytes},
    }


def contiguous_band(electrodes, acronym, max_gap_um):
    """Find the largest contiguous depth band labelled with one structure.

    Neuropixels 1.0 contacts sit on rows 20 um apart, so a band is defined as a
    run of matching depths whose successive gaps never exceed ``max_gap_um``.
    Interruptions larger than that mean the probe left the structure and
    re-entered it, which is a different placement problem.

    Args:
        electrodes: per-electrode dicts for one probe.
        acronym: the target structure's template-library acronym.
        max_gap_um: largest tolerated gap between successive matching depths.

    Returns:
        A dict describing the largest band -- ``depth_lo_um``, ``depth_hi_um``,
        ``n_channels``, ``span_um`` -- or None when the structure is absent or
        its depths are unknown.
    """
    depths = sorted({e["depth_um"] for e in electrodes
                     if e["acronym"] == acronym and e["depth_um"] is not None})
    if not depths:
        return None
    best = current = [depths[0]]
    for depth in depths[1:]:
        if depth - current[-1] <= max_gap_um:
            current.append(depth)
        else:
            if len(current) > len(best):
                best = current
            current = [depth]
    if len(current) > len(best):
        best = current
    band = set(best)
    n_channels = sum(1 for e in electrodes
                     if e["acronym"] == acronym and e["depth_um"] in band)
    return {
        "depth_lo_um": best[0],
        "depth_hi_um": best[-1],
        "span_um": best[-1] - best[0],
        "n_rows": len(best),
        "n_channels": n_channels,
    }
