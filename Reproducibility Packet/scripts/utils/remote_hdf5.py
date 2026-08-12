"""Read a remote HDF5/NWB file over HTTP range requests, without downloading it.

The host recordings this project screens are 18-197 GB NWB files on S3, and the
only part needed to decide whether a recording is a viable Tier A host is its
``/general/extracellular_ephys/electrodes`` table -- a few hundred kilobytes of
metadata sitting near the front of the file.

``RemoteFile`` is a seekable, read-only, block-caching file object that h5py
accepts in place of a local path, so the electrodes table can be read with a
handful of range requests instead of a multi-hour download. It deliberately
depends on nothing outside the standard library.

The cache is per-instance and unbounded, which is correct for this access
pattern: one file is opened, a small contiguous metadata region is read, and the
object is discarded. Do not reuse a single instance to stream bulk sample data.
"""

import io
import time
import urllib.error
import urllib.request

DEFAULT_BLOCK_BYTES = 4 * 1024 * 1024
DEFAULT_RETRIES = 4


class RemoteFile(io.RawIOBase):
    """A seekable read-only file over HTTP byte-range requests.

    Args:
        url: an HTTP(S) URL whose server honours ``Range`` requests.
        size: the object's total size in bytes, known ahead of time (DANDI's
            asset listing supplies it, which avoids a HEAD round trip).
        block: cache granularity in bytes. Larger blocks mean fewer, bigger
            requests; the default suits HDF5 metadata reads.
        timeout: per-request timeout in seconds.
        retries: how many times to re-issue a failed range request before
            giving up. Screening runs make hundreds of sequential requests to
            one host, and a single dropped connection would otherwise discard
            an entire recording's result.

    Attributes:
        n_requests: how many range requests have been issued.
        n_bytes: how many bytes have been transferred.
    """

    def __init__(self, url, size, block=DEFAULT_BLOCK_BYTES, timeout=180,
                 retries=DEFAULT_RETRIES):
        if size <= 0:
            raise ValueError(f"size must be positive, got {size}")
        if block <= 0:
            raise ValueError(f"block must be positive, got {block}")
        if retries < 0:
            raise ValueError(f"retries must not be negative, got {retries}")
        self.url = url
        self.size = int(size)
        self.block = int(block)
        self.timeout = timeout
        self.retries = int(retries)
        self._pos = 0
        self._cache = {}
        self.n_requests = 0
        self.n_bytes = 0

    def readable(self):
        """Return True; this object is read-only but readable."""
        return True

    def seekable(self):
        """Return True; HDF5 requires random access."""
        return True

    def writable(self):
        """Return False; writes are not supported."""
        return False

    def tell(self):
        """Return the current byte offset."""
        return self._pos

    def seek(self, offset, whence=io.SEEK_SET):
        """Move the read cursor.

        Args:
            offset: byte offset, interpreted according to ``whence``.
            whence: ``io.SEEK_SET``, ``io.SEEK_CUR``, or ``io.SEEK_END``.

        Returns:
            The new absolute offset.
        """
        if whence == io.SEEK_SET:
            new = offset
        elif whence == io.SEEK_CUR:
            new = self._pos + offset
        elif whence == io.SEEK_END:
            new = self.size + offset
        else:
            raise ValueError(f"unsupported whence {whence!r}")
        if new < 0:
            raise ValueError(f"negative seek position {new}")
        self._pos = new
        return self._pos

    def _fetch_block(self, index):
        """Return one cached block, fetching it if this is its first use.

        Args:
            index: block number, i.e. ``offset // self.block``.

        Returns:
            The block's bytes (shorter than ``self.block`` at end of file).

        Raises:
            OSError: if the range request still fails after ``self.retries``
                additional attempts, naming the URL, the range, and the
                attempt count.
        """
        if index in self._cache:
            return self._cache[index]
        lo = index * self.block
        hi = min(lo + self.block, self.size) - 1
        request = urllib.request.Request(self.url, headers={"Range": f"bytes={lo}-{hi}"})
        last_error = None
        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    payload = response.read()
                break
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
                    ConnectionError) as exc:
                # S3 drops a connection now and then. One dropped block would
                # otherwise discard a whole recording's screening result, so
                # back off and try again before failing loudly.
                last_error = exc
                if attempt < self.retries:
                    time.sleep(2 ** attempt)
        else:
            raise OSError(f"range request bytes={lo}-{hi} failed for {self.url} after "
                          f"{self.retries + 1} attempts: {last_error}") from last_error
        self._cache[index] = payload
        self.n_requests += 1
        self.n_bytes += len(payload)
        return payload

    def read(self, n=-1):
        """Read up to ``n`` bytes from the current position.

        Args:
            n: byte count, or a negative value to read to end of file.

        Returns:
            The bytes read, possibly shorter than requested at end of file.
        """
        remaining = self.size - self._pos
        if remaining <= 0:
            return b""
        want = remaining if n is None or n < 0 else min(n, remaining)
        out = bytearray()
        while want > 0:
            index, offset = divmod(self._pos, self.block)
            chunk = self._fetch_block(index)[offset:offset + want]
            if not chunk:
                break
            out += chunk
            self._pos += len(chunk)
            want -= len(chunk)
        return bytes(out)

    def readinto(self, buffer):
        """Read bytes into a pre-allocated buffer.

        Args:
            buffer: a writable ``bytes``-like object.

        Returns:
            The number of bytes written into ``buffer``.
        """
        data = self.read(len(buffer))
        buffer[:len(data)] = data
        return len(data)
