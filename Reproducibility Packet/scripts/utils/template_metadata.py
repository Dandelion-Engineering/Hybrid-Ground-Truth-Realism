"""Fetch and screen the ``hybrid_template_library`` donor metadata table.

The table is a ~2 MB CSV hosted mutably on S3, so every use pins the snapshot by
SHA-256. It carries one row per donor template with ``brain_area``,
``amplitude_uv``, ``signal_to_noise_ratio``, ``depth_along_probe``,
``noise_level_uv``, ``spikes_per_unit``, ``template_index``, ``probe``, and
``dataset``.

The ``dataset`` column is the load-bearing one for leakage control, and its
contents are not what its name suggests. Every Neuropixels 1.0 value is a DANDI
000409 session, spelled

    000409_sub-<subject>_ses-<session-uuid>_<modalities>_<insertion-uuid>.zarr

so the donors and this project's candidate hosts come from the same dandiset.
"Excluding the host's source dataset" therefore has three defensible
granularities -- insertion, session, and subject -- and they give different
answers. :func:`provenance_keys` exposes all three so a script can report the
choice instead of burying it.
"""

import csv
import hashlib
import io
import re
import urllib.error
import urllib.request

DEFAULT_CSV_URL = "https://spikeinterface-template-database.s3.amazonaws.com/templates.csv"

# Snapshot observed on 2026-08-11 and verified independently by both agents. A
# mismatch does not mean a script is wrong; it means upstream moved and every
# downstream selection must be re-derived against the new snapshot.
PINNED_SHA256 = "a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d"

_SUBJECT_RE = re.compile(r"sub-([^_]+)_")
_SESSION_RE = re.compile(r"ses-([0-9a-fA-F-]{36})")


def fetch_metadata(url=DEFAULT_CSV_URL, cache_path=None, timeout=180, verbose=True):
    """Download the donor metadata CSV and record its snapshot hash.

    Args:
        url: HTTP(S) location of the metadata CSV.
        cache_path: optional file to read from and write to, so a screening run
            is repeatable against a fixed snapshot.
        timeout: request timeout in seconds.
        verbose: print progress to stdout.

    Returns:
        A tuple of (payload_bytes, sha256_hex).

    Raises:
        OSError: if the CSV cannot be retrieved, naming the URL and the reason.
    """
    payload = None
    if cache_path:
        try:
            with open(cache_path, "rb") as handle:
                payload = handle.read()
            if verbose:
                print(f"[templates] loaded {len(payload)} bytes from {cache_path}", flush=True)
        except OSError:
            payload = None
    if payload is None:
        if verbose:
            print(f"[templates] fetching {url}", flush=True)
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                payload = response.read()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            raise OSError(f"could not retrieve {url}: {exc}") from exc
        if cache_path:
            with open(cache_path, "wb") as handle:
                handle.write(payload)
    digest = hashlib.sha256(payload).hexdigest()
    if verbose:
        print(f"[templates] {len(payload)} bytes, sha256 {digest}", flush=True)
        print(f"[templates] matches pinned snapshot: {digest == PINNED_SHA256}", flush=True)
    return payload, digest


def parse_rows(payload, probe=None):
    """Parse the metadata CSV, optionally restricted to one probe type.

    Args:
        payload: raw CSV bytes.
        probe: probe label to keep, e.g. ``"Neuropixels 1.0"``. None keeps all.

    Returns:
        A list of row dicts keyed by column name.

    Raises:
        ValueError: if the CSV is empty or the probe filter matches nothing.
    """
    rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8"))))
    if not rows:
        raise ValueError("donor metadata CSV parsed to zero rows")
    if probe is None:
        return rows
    subset = [row for row in rows if row.get("probe") == probe]
    if not subset:
        available = sorted({row.get("probe", "") for row in rows})
        raise ValueError(f"no rows for probe {probe!r}; available: {available}")
    return subset


def as_float(row, key):
    """Read a numeric cell tolerantly.

    Args:
        row: a CSV row dict.
        key: column name to read.

    Returns:
        The cell as a float, or None when blank or unparseable.
    """
    raw = (row.get(key) or "").strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def in_caliper(row, amp_lo, amp_hi, snr_lo, snr_hi):
    """Test whether a donor template falls inside the screening caliper.

    The caliper is a provisional *quality and matching* screen. The anchor
    pipeline's 50-200 uV figure is an injection rescaling target, not evidence
    that a donor must already sit in that range, so this is never the final
    eligibility test -- that is done on the waveform after rescaling into the
    selected host.

    Args:
        row: a CSV row dict.
        amp_lo, amp_hi: inclusive amplitude bounds in microvolts.
        snr_lo, snr_hi: inclusive signal-to-noise-ratio bounds.

    Returns:
        True when both covariates are present and inside their bounds.
    """
    amplitude = as_float(row, "amplitude_uv")
    snr = as_float(row, "signal_to_noise_ratio")
    if amplitude is None or snr is None:
        return False
    return amp_lo <= amplitude <= amp_hi and snr_lo <= snr <= snr_hi


def provenance_keys(row):
    """Return a donor row's provenance identifiers at three granularities.

    Args:
        row: a CSV row dict whose ``dataset`` names a DANDI 000409 session.

    Returns:
        A dict with keys ``insertion`` (the full ``dataset`` string, which is
        one probe insertion), ``session`` (the session UUID), and ``subject``
        (the animal identifier). Values are None when the pattern does not
        match, which is itself worth reporting rather than assuming.
    """
    dataset = row.get("dataset") or ""
    subject_match = _SUBJECT_RE.search(dataset)
    session_match = _SESSION_RE.search(dataset)
    return {
        "insertion": dataset or None,
        "session": session_match.group(1) if session_match else None,
        "subject": subject_match.group(1) if subject_match else None,
    }
