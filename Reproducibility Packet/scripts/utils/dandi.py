"""Enumerate and address assets in a DANDI dandiset, using the standard library.

The project's host recordings come from DANDI 000409 (IBL Brain Wide Map,
CC-BY-4.0). This module lists that dandiset's assets through the public REST
API, caches the listing to disk so a screening run is repeatable and offline,
and turns an asset's blob identifier into the direct S3 URL that
``utils.remote_hdf5.RemoteFile`` reads from.

Nothing here downloads recording data. The listing is JSON metadata; the S3 URL
is only used for byte-range metadata reads elsewhere.
"""

import json
import os
import re
import urllib.error
import urllib.request

DANDI_API = "https://api.dandiarchive.org/api"
DANDI_BLOB_BASE = "https://dandiarchive.s3.amazonaws.com/blobs"

# IBL NWB assets are named
#   sub-<subject>/sub-<subject>_ses-<uuid>_desc-<raw|processed>_<suffix>.nwb
_SUBJECT_RE = re.compile(r"sub-([^/]+)/")
_SESSION_RE = re.compile(r"ses-([0-9a-fA-F-]{36})")

RAW_SUFFIX = "_desc-raw_ecephys.nwb"
PROCESSED_SUFFIX = "_desc-processed_behavior+ecephys.nwb"


def _get_json(url, timeout=180):
    """Fetch and decode a JSON document.

    Args:
        url: the endpoint to request.
        timeout: per-request timeout in seconds.

    Returns:
        The decoded JSON payload.

    Raises:
        OSError: if the request fails, naming the URL and the reason.
    """
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        raise OSError(f"request failed for {url}: {exc}") from exc


def list_assets(dandiset, version="draft", cache_path=None, page_size=1000, verbose=True):
    """List every asset in a dandiset, using a disk cache when one exists.

    Args:
        dandiset: dandiset identifier, e.g. ``"000409"``.
        version: version string, e.g. ``"draft"`` or a published version.
        cache_path: optional JSON file to read from and write to. When it
            exists it is used verbatim, which makes screening runs repeatable
            against a fixed listing rather than a moving archive.
        page_size: assets per API page.
        verbose: print progress to stdout.

    Returns:
        A list of asset dicts, each carrying at least ``asset_id``, ``blob``,
        ``path``, and ``size``.
    """
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as handle:
            assets = json.load(handle)
        if verbose:
            print(f"[dandi] loaded {len(assets)} assets from cache {cache_path}", flush=True)
        return assets

    assets = []
    url = f"{DANDI_API}/dandisets/{dandiset}/versions/{version}/assets/?page_size={page_size}"
    while url:
        page = _get_json(url)
        assets.extend(page["results"])
        if verbose:
            print(f"[dandi] listed {len(assets)} assets", flush=True)
        url = page.get("next")
    if not assets:
        raise OSError(f"dandiset {dandiset}/{version} returned zero assets")
    if cache_path:
        os.makedirs(os.path.dirname(os.path.abspath(cache_path)), exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as handle:
            json.dump(assets, handle)
        if verbose:
            print(f"[dandi] wrote asset cache to {cache_path}", flush=True)
    return assets


def blob_url(asset):
    """Return the direct S3 URL for an asset's blob.

    Args:
        asset: an asset dict from :func:`list_assets`.

    Returns:
        An HTTPS URL that honours ``Range`` requests.

    Raises:
        ValueError: if the asset has no blob (e.g. it is a Zarr asset).
    """
    blob = asset.get("blob")
    if not blob:
        raise ValueError(f"asset {asset.get('path')!r} has no blob identifier")
    return f"{DANDI_BLOB_BASE}/{blob[:3]}/{blob[3:6]}/{blob}"


def subject_of(asset):
    """Return the subject identifier encoded in an asset path, or None."""
    match = _SUBJECT_RE.search(asset["path"])
    return match.group(1) if match else None


def session_of(asset):
    """Return the session UUID encoded in an asset path, or None."""
    match = _SESSION_RE.search(asset["path"])
    return match.group(1) if match else None
